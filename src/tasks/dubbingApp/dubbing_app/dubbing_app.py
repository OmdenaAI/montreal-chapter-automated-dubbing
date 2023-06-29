from .config import *
from .dubbing_processor import DubbingProcessor
from .speech2text_processor import Speech2TextProcessor
from .video_processor import VideoProcessor
from .text2speech_processor import Text2SpeechProcessor
from .text_processor import TextProcessor


class DubbingApp:
    def __init__(self):
        self.languages = LANGUAGES

        # Initialize the processors
        self.video_processor = VideoProcessor()
        self.speech2text_processor = Speech2TextProcessor()
        self.text_processor = TextProcessor()
        self.text2speech_processor = Text2SpeechProcessor()
        self.dubbing_processor = DubbingProcessor()

    async def process_pipeline(self, video_url: str, target_language: str):
        # Gets the video from YouTube, to a local video file
        video_file_path = self.video_processor.get_video(video_url)

        # Preprocess the video and extract the audio
        audio_file_path = self.video_processor.extract_audio(video_file_path)

        # Perform speech-to-text conversion on the audio
        timestamped_text = self.speech2text_processor.speech_to_text(audio_file_path)

        # Translate the text to the selected target language
        translated_text = self.text_processor.translate_text_segments(timestamped_text, target_language)

        # Convert the translated text into speech
        translated_audio = await self.text2speech_processor.text_to_speech(translated_text['segments'], target_language)

        # Concatenate/sync the translated audio segments
        dubbed_audio = self.dubbing_processor.join_audio_segments(translated_audio)

        # Integrate the full translated audio with the original video
        dubbed_video_file_path = self.dubbing_processor.add_audio_to_video(video_file_path, dubbed_audio)

        return dubbed_video_file_path
