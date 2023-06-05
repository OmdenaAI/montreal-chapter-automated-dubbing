class VideoProcessor:
    @staticmethod
    def get_video(video_url: str) -> str:
        """
        Download the YouTube video, converting it into a local MP4 file.
        ToDo: File format to be agreed on. MP4? Together with #task-06-user-interface

        Parameters
        ----------
        video_url: str
            The URL (HTTP path) to the original YouTube video, to be dubbed

        Returns
        -------
        The path to the just created video file
        """

        output_path = ""

        return output_path

    @staticmethod
    def extract_audio(video_file: str) -> str:
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

        output_path = ""

        return output_path
