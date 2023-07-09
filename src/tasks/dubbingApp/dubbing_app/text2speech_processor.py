import random
from pydub import AudioSegment
from typing import Dict, List, Union
import edge_tts
from edge_tts import VoicesManager
import tempfile
import os

from .config import DEFAULT_VOICES, SUPPORTED_LANGUAGES, SUPPORTED_LOCALE


class Text2SpeechProcessor:
    async def text_to_speech(self, translated_dict: Dict, target_language: str, target_gender: str = None) \
            -> Dict[str, List[Union[str, int]]]:
        """
        Text-to-Speech of the translated text.
        Speaker gender auto-detection is not currently working. Thus, the user has the ability to pre-choose a gender
        for the target speech voice.

        Parameters:
        -----------
        text_dict: dict
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

        target_language: str
            The target language for the translation (language code)

        target_gender: str
            The target speaker gender ('Female', 'Male' or None)


        Returns:
        --------
        dict
            A similar dict, with every `audio` elements now filled with the generated audio
        """
        segments = translated_dict['segments']
        audio_segments = await self.segments_text_to_speech(segments, target_language, target_gender)

        audio_dict = translated_dict
        audio_dict['segments'] = audio_segments

        return audio_dict

    @staticmethod
    async def segments_text_to_speech(text_segments: List[Dict[str, Union[str, int]]], target_language: str,
                                      target_gender: str) -> List[Dict[str, Union[AudioSegment, int]]]:
        """
        The module converts the text segments to audio
        Combines it based on timestamps
        Returns a list of dictionaries containing the audio segments and their respective start times.
        
        Parameters: 
        -----------
        text_segments : list
            The dictionary of transcribed, timestamped, text segments. Dictionary elements:

        target_language: str
            The target language for the translation (language code)

        target_gender: str
            The target speaker gender ('Female', 'Male' or None)

        Returns:
        --------
        list
            A similar list, with every `audio` elements now filled with the generated audio
        """
        result = []
        
        # Set the speaker voice gender
        # If valid gender is provided in `target_gender`, this is used for the whole audio speech.
        if target_gender in ['Female', 'Male']:
            speaker = target_gender
        # Otherwise, tries to get gender from the auto-detection process. If also not
        # provided, it defaults to a 'Female' voice
        else:
            try:
                # speaker = segment['speaker_gender']
                speaker = text_segments[0]['speaker_gender']
                if not speaker:
                    speaker = "Female"
            except:
                speaker = "Female"

        # Dynamic voice selection using VoicesManager class, a class to find the correct voice based on their
        # attributes (language, gender, locale)
        voices = await VoicesManager.create()
        voice = voices.find(Gender=speaker, Language=target_language, Locale=SUPPORTED_LOCALE.get(target_language))
        try:
            voice = random.choice(voice)["ShortName"]
        except:
            if target_language in SUPPORTED_LANGUAGES.keys() and target_language in DEFAULT_VOICES.keys():
                voice = DEFAULT_VOICES[target_language][speaker]
            else:
                voice = 'en-GB-SoniaNeural'

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            temp_file_path = os.path.join(tmp_dir_name, "temp.wav")

            for segment in text_segments:
                text = segment['text']
                if segment.get('voice'):
                    voice = segment.get('voice')

                # Using communicate class from edge_tts for communicating with the service.
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(temp_file_path)
                audio_segment = AudioSegment.from_file(temp_file_path)

                segment['audio'] = audio_segment
                segment['voice'] = voice
                result.append(segment)
        
        return result
