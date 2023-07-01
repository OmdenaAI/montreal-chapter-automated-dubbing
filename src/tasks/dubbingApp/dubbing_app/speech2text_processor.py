import logging
#import malaya_speech
#from malaya_speech import Pipeline
import torch  # conda install pytorch -c pytorch
from typing import Dict, List, Union
import whisper  # pip install -U openai-whisper


class Speech2TextProcessor:
    def __init__(self):
        self.logger = self.setup_log()

    def speech_to_text(self, audio_file: str) -> Dict[str, List[Union[str, int]]]:
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
            - segments: list - list of dictionaries with the following elements:
                - id: int - segment sequence number
                - start: int - start time of phrase within the audio, in milliseconds
                - end: int - end time of phrase within the audio, in milliseconds
                - speaker_gender: str - auto-detected gender of speaker ('Female' / 'Male' / '')
                - text: str - phrase text
                - audio: AudioSegment - corresponding generated audio (empty, filled later)
            - original_language: str - detected language in original audio (code in ISO_639-1 format, as in .config)
            - original_text: str - transcribed text in full
        """

        torch.cuda.is_available()
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f'Device used: {DEVICE}')
        model = whisper.load_model("base", device=DEVICE)
        self.add_log_line()
        self.logger.info(f"Model is {'multilingual' if model.is_multilingual else 'English-only'} ")

        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        lang = max(probs, key=probs.get)
        self.logger.info(f"Detected language: {lang}")

        # just text and phrases, no by-word timestamps
        result = model.transcribe(audio_file)

        final_result = self.process_transcription(result, lang)

        return final_result

    @staticmethod
    def process_transcription(full_result, language):
        """
        processes Whisper output into proper dictionary of results
        """
        result_dict = {'segments': [],
                       'original_language': language,
                       'original_text': full_result['text']}
        for s in full_result['segments']:
            d = {'id': s['id'],
                 'start': s['start'],
                 'end': s['end'],
                 'speaker_gender': '',
                 'text': s['text'],
                 'audio': None
                 }
            result_dict['segments'].append(d)
        return result_dict

    def setup_log(self):
        """
            log file setup
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='dubbing_app_backend.log',
                            filemode='w')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        self.logger = logging.getLogger(__name__)

        return self.logger

    def add_log_line(self):
        self.logger.info(108 * '#')

    '''
    @staticmethod
    def get_speakers_gender(audio, g_model='vggvox-v2', vgg_quantized=False, frame_duration=30):
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
        # check model
        if (g_model == 'deep_speaker'):
            vgg_quantized = False
        elif (g_model != 'vggvox-v2'):
            g_model = 'vggvox-v2'
        print(f"Using {g_model} model, quantized = {vgg_quantized}")

        y, sr = malaya_speech.load(audio)
        print(len(y), sr)

        # load deep model for genders:
        ms_g_model = malaya_speech.gender.deep_model(model=g_model, quantized=vgg_quantized)
        # load vad model
        ms_vad_model = malaya_speech.vad.deep_model(model=g_model, quantized=vgg_quantized)

        frames = list(malaya_speech.utils.generator.frames(y, frame_duration, sr))
        print(f"Number of frames: {len(frames)}")

        # make a pipeline with model for prediction of vad
        pl = Pipeline()
        pipeline = (pl.batching(5).foreach_map(ms_vad_model.predict).flatten())

        result = pipeline.emit(frames)
        print(result.keys)

        frames_vad = [(frame, result['flatten'][no]) for no, frame in enumerate(frames)]
        grouped_vad = malaya_speech.utils.group.group_frames(frames_vad)
        grouped_vad = malaya_speech.utils.group.group_frames_threshold(grouped_vad, threshold_to_stop=0.3)

        # final pipeline:
        p_final = Pipeline()
        pipeline_final = (
            p_final.foreach_map(ms_g_model).flatten()
        )
        # pipeline_final.visualize()

        samples_vad = [g[0] for g in grouped_vad]
        result_genders = pipeline_final.emit(samples_vad)
        print("Detected genders: {result_genders.keys()}")
        return [(result_genders['flatten'][no]) for no, _ in enumerate(samples_vad)]
    '''
