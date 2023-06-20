from pydub import AudioSegment
from pytube import YouTube
import os


class VideoProcessor:
    def __init__(self):
        self.audio_extension = "mp3"
        self.video_extension = "mp4"
        self.media_folder = "media"

    def get_video(self, video_url: str) -> str:
        """
        Download the YouTube video, converting it into a local MP4 file.
        ToDo: File format to be agreed on. MP4? Together with #task-06-user-interface

        Parameters
        ----------
        video_url: str
            The URL (HTTP path) to the original YouTube video, to be dubbed.
            Expected format/example:
                - https://www.youtube.com/watch?v=FCkfytrmV1s
                - https://youtu.be/FCkfytrmV1s

        Returns
        -------
        The path to the just created video file
        """

        yt = YouTube(f"{video_url}")

        # this extract the video title, from YouTube
        video_title = yt.title
        base_name = os.path.join(self.media_folder, os.path.basename(video_title))
        file_path = f"{base_name}.{self.video_extension}"

        # remove the file, if already exists
        try:
            os.remove(file_path)
        except FileNotFoundError:
            # File doesn't exist, continue silently
            pass

        yt.streams.filter(progressive=True, file_extension=self.video_extension)\
            .order_by('resolution').desc().first()\
            .download(filename=file_path)

        return file_path

    def extract_audio(self, video_file: str) -> str:
        """
        Extract the audio from the video, saving it to a separate audio file.
        ToDo: File format to be agreed on. MP3? WAV? Together with #task-02-speech-to-text

        Parameters
        ----------
        video_file: str
            The file path to the video file

        Returns
        -------
        The path to the just created audio file
        """
        file_path = ""

        # Check if the  item is a file
        if os.path.isfile(video_file):
            base_name = os.path.splitext(os.path.join(self.media_folder, os.path.basename(video_file)))[0]
            file_path = f"{base_name}.{self.audio_extension}"

            # Use pydub to extract the audio from the video file and save it as an MP3 file
            AudioSegment.from_file(video_file).export(file_path, format=self.video_extension)

        return file_path
