
import asyncio
import random
from pydub import AudioSegment
from typing import Dict, List, Union
import edge_tts
from edge_tts import VoicesManager
import tempfile
import os

class Text2SpeechProcessor:
    async def text_to_speech(self, text_segments: List[Dict[str, Union[str, int]]], target_language: str) -> List[Dict[str, Union[AudioSegment, int]]]:
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
            A list of dictionaries containing audio segments and their start times.
            Example:
            [
                {"audio": <AudioSegment>, "start_time": 0},
                {"audio": <AudioSegment>, "start_time": 5000},
                ...
            ]
        """
        audio_sum = AudioSegment.empty()
        result = []
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            print('created temporary directory', tmpdirname)
            temp_file_path = os.path.join(tmpdirname, "temp.wav")
            print(temp_file_path)
            
            prev_audio_duration = 0
            
            for segment in text_segments:
                speaker = segment['speaker_gender']
                lang = segment['language']
                text = segment['text']
                start_ms = segment['start']
                
                # Dynamic voice selection using VoicesManager class,
                # A class to find the correct voice based on their attributes.
                voices = await VoicesManager.create()
                voice = voices.find(Gender=speaker, Language=lang)
                
                # Using communicate class from edge_tts for communicating with the service.
                communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
                await communicate.save(temp_file_path)
                audio_segment = AudioSegment.from_file(temp_file_path)
                
                silence_duration = start_ms - prev_audio_duration
                audio_sum += AudioSegment.silent(duration=silence_duration) + audio_segment
                
                prev_audio_duration = len(audio_segment)
                
                result.append({"audio": audio_segment, "start_time": start_ms})
        
        return result
