import asyncio
import random

import edge_tts
from edge_tts import VoicesManager
import tempfile
from pydub import AudioSegment
import os


async def text_to_speech(text_segments) -> None:
    """
    - The module converts the text segments to audio
    - Combines it based on timestamps 
    - Saves the audio in .wav format.
    
    Parameters:
    -----------
    
    text_segments : The list of dictionary containing  translated and timestamped text segments, language, speaker_gender . 
    Example:
        text_segments : list of dictionaries
        [   
            {"text": 'How often do you think about space?', "start": 660, "end": 2700, "language": "en", "speaker_gender": "Female"},
            {"text": 'Probably not enough considering how much we use it every day.'"start":  3320, "end": 6520, "language": "en", "speaker_gender": "Male"}
        ]
        
        speaker: Male, Female
        Language: en, es, fr
    
    
    """
    audio_sum = AudioSegment.empty()  
    with tempfile.TemporaryDirectory() as tmpdirname:          
        print('created temporary directory', tmpdirname)   
        temp_file_path = os.path.join(tmpdirname, "temp.wav")
        print(temp_file_path)
        prev_audio_duration= 0
        for i, segment in enumerate(text_segments):
            speaker = segment['speaker_gender'] 
            lang = segment['language']
            text = segment['text']
            start_ms = segment['start'] 
            
            # Dynamic voice selection using VoicesManager class, 
            # A class to find the correct voice based on their attributes.
            voices = await VoicesManager.create()
            
            voice = voices.find(Gender=speaker, Language=lang)
            
            #  using communicate class from edge tts for communicating with the service.
            communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
            await communicate.save(temp_file_path)
            audio_segment = AudioSegment.from_file(temp_file_path)

            if( i == 0):
                silence_duration = start_ms
            else:
                silence_duration = start_ms - prev_start - prev_audio_duration

            audio_sum = audio_sum + AudioSegment.silent(duration=silence_duration) + audio_segment                   
        
            prev_start = start_ms
            prev_audio_duration = len(audio_segment)

        audio_sum.export("out_f.wav", format='wav')   


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        text_segments = [
            {"text": ' How often do you think about space?',
             "start": 660, "end": 2700, "language": "en", "speaker_gender": "Female"},
            {"text": 'Probably not enough considering how much we use it every day.',
             "start":  3320, "end": 6520, "language": "en", "speaker_gender": "Male"},
            {"text": ' We rely on the thousands of satellites up there to keep our modern lives running smoothly.',
             "start": 7160, "end": 11720, "language": "en", "speaker_gender": "Male"},
            {"text":" But there's an explosive threat approaching on the horizon.",
             "start": 12260, "end": 15400, "language": "en", "speaker_gender": "Male"} ]
        loop.run_until_complete(text_to_speech(text_segments))

    finally:
        loop.close()