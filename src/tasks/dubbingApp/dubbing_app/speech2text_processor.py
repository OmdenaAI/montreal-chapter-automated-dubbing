from typing import Dict, List, Union
import whisper


class Speech2TextProcessor:
    def speech_to_text(self, audio_file: str) -> List[Dict[str, Union[str, int]]]:
        """
        Perform speech-to-text conversion on the audio.
        During the process, the language is detected, as well as each speaker's gender.
        The speech is split into shorter transcribed audio segments (phrases?).
        ToDo: Confirm output format together with #task-03, #task-04, and #task-05

        Parameters
        ----------
        audio_file: str
            The path to the audio file

        Returns
        -------
        List of transcribed, timestamped, text segments. Dictionary elements:
            - text: str - the transcribed text segment (phrase?)
            - start: int - start time of phrase within the audio, in milliseconds
            - end: int - end time of phrase within the audio, in milliseconds
            - language: str - auto-detected language in audio segment (language list defined in .config)
            - speaker_gender: str - auto-detected gender of speaker in segment ("Female" / "Male" / "Other")

        Example
        -------
        text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

        """

        text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

        return text_segments

'''

from typing import List, Dict
import whisper
import numpy as np
import torch
import logging
import malaya_speech
from malaya_speech import Pipeline

import os

def setup_log():
    """
        log file setup
    """
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename= 's2c_processing.log',
                filemode='w')
    
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)
    
    return logger
    

def add_log_line():
    logger.info('#####################################################' +
                '#####################################################' +
                '#####################################################'
                )  
logger = setup_log()
class Speech2TextProcessor:

    #TBD
    def __init__(self) -> None:
        pass
    
    def get_speakers_gender(self, audio, g_model='vggvox-v2', vgg_quantized = False, frame_duration = 30):
        """
        Perform diarization with gender recognition on the audio.
        malaya-speach non-quantized 'vggvox-v2' model (accuracy 97%, the highest available) 
        is set as default, other options available: 'vggvox-v2' + quantized and 'deep_speaker'

        Parameters
        ----------
        audio: str
            The path to the audio file
        g_model: str ['vggvox-v2', 'deep_speaker']
            malaya-speach gender recognition model
        vgg_quantized: bool
            whether to use vggvox quantized, ignored for deep_speaker
        frame_duration: int
            frame duration in msec


        Returns
        -------
        The list of genders for each second in video
        """
        #check model 
        if (g_model=='deep_speaker'):
            vgg_quantized = False
        elif (g_model != 'vggvox-v2'):
            g_model = 'vggvox-v2'
        logger.log(f"Using {g_model} model, quantized = {vgg_quantized}")

        y, sr = malaya_speech.load(audio)
        logger.log(len(y), sr)
        frames = list(malaya_speech.utils.generator.frames(y, frame_duration, sr))
        frames_vad = [(frame, result['flatten'][no]) for no, frame in enumerate(frames)]
        grouped_vad = malaya_speech.utils.group.group_frames(frames_vad)
        #grouped_vad = malaya_speech.utils.group.group_frames_threshold(grouped_vad, threshold_to_stop = 0.3)

        ms_model = malaya_speech.gender.deep_model(model = g_model, quantized = vgg_quantized)
        #make a pipeline with model
        pl = Pipeline()
        pipeline = (pl.foreach_map(ms_model).flatten())

        samples_vad = [g[0] for g in grouped_vad]
        result = pipeline.emit(samples_vad)
        logger.log("Detected genders: {result.keys()}")
        return [(result['flatten'][no]) for no, _ in enumerate(samples_vad)]

    def speech_to_text(self, audio_file: str):
        """
        Perform speech-to-text conversion of the audio.
        Using WhisperAI pretrained model
        The speech is split into shorter transcribed audio segments (phrases)

        Parameters
        ----------
        audio_file: str
            The path to the audio file

        Returns
        -------
        The dictionary of transcribed, timestamped, text segments. Dictionary elements:
            - text: str - the transcribed text
            - lang: str - detected language
            - segments - list of dictionaries with the following elements:
                - phrase: str phrase
                - start: int - start time of phrase within the audio, in milliseconds
                - end: int - end time of phrase within the audio, in milliseconds

        """

        def process_final_result(result, lang):
            """
            processes Whisper output into proper dictionary of results
            """
            final_result = {}
            final_result['text'] = result["text"]
            final_result['lang'] = lang
            final_result['segments'] = []
            for s in result['segments']:
                d={}
                d['id'] = s['id']
                d['start'] = s['start']
                d['end'] = s['end']
                d['phrase'] = s['text']
                final_result['segments'].append(d)
            return final_result

        torch.cuda.is_available()
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f'Device used: {DEVICE}')
        model = whisper.load_model("base", device=DEVICE)
        add_log_line()
        logger.info(f"Model is {'multilingual' if model.is_multilingual else 'English-only'} ")
        
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        lang = max(probs, key=probs.get)
        logger.info(f"Detected language: {lang}")

        #just text and phrases, no by-word timestamps
        result = model.transcribe(audio_file)

        final_result = process_final_result(result, lang)

        return final_result



if __name__ == "__main__":
    
    #########################################
    # Example of how to use the above code: #
    #########################################
    s2t = Speech2TextProcessor()

    audio_f = 'languages.mp3'

    print(os.getcwd())

    repository_root_dir = os.path.dirname(os.path.dirname(__file__))
    print("repository_root_dir", repository_root_dir)

    audio_f = os.path.join(repository_root_dir, 'dubbing_app', audio_f)

    print(os.path.exists(audio_f))

    with open('text_result.txt', 'w') as f:
        f.write(str(s2t.speech_to_text(audio_f)))

    with open('text_result.txt', 'w') as f:
        f.write(str(s2t.get_speakers_gender(audio_f)))

    '''

