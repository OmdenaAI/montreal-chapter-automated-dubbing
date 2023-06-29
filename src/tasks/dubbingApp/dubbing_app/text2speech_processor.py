import random
from pydub import AudioSegment
from typing import Dict, List, Union
import edge_tts
from edge_tts import VoicesManager
import tempfile
import os


class Text2SpeechProcessor:
    async def text_to_speech(self, translated_dict: Dict, target_language: str) -> Dict[str, List[Union[str, int]]]:

        segments = translated_dict['segments']
        audio_segments = await self.segments_text_to_speech(segments, target_language)

        audio_dict = translated_dict
        audio_dict['segments'] = audio_segments

        return audio_dict

    @staticmethod
    async def segments_text_to_speech(text_segments: List[Dict[str, Union[str, int]]], target_language: str) \
            -> List[Dict[str, Union[AudioSegment, int]]]:
        """
        The module converts the text segments to audio
        Combines it based on timestamps
        Returns a list of dictionaries containing the audio segments and their respective start times.
        
        Parameters: 
        -----------
        text_segments : list 
            A list of dictionaries containing translated and timestamped text segments, language, and speaker gender.
            Example:
            [
                {"text": 'How often do you think about space?', "start": 660, "end": 2700, "language": "en", "speaker_gender": "Female"},
                {"text": 'Probably not enough considering how much we use it every day.', "start": 3320, "end": 6520, "language": "en", "speaker_gender": "Male"}
            ]
        target_language : str
            The target language for the text-to-speech conversion.
        
        Returns:
        --------
        list
            A similar list, with every `audio` elements now filled with the generated audio
        """
        result = []
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_file_path = os.path.join(tmpdirname, "temp.wav")

            for segment in text_segments:
                try:
                    speaker = segment['speaker_gender']
                except:
                    speaker = "Female"
                text = segment['text']
                start_ms = segment['start']
                
                # Dynamic voice selection using VoicesManager class,
                # A class to find the correct voice based on their attributes.
                voices = await VoicesManager.create()
                voice = voices.find(Gender=speaker, Language=target_language)
                try:
                    voice = random.choice(voice)["Name"]
                except:
                    voice = "en-GB-SoniaNeural"

                # Using communicate class from edge_tts for communicating with the service.
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(temp_file_path)
                audio_segment = AudioSegment.from_file(temp_file_path)

                segment['audio'] = audio_segment
                result.append(segment)
        
        return result
