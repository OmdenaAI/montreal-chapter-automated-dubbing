from typing import List, Dict
import whisper


class Speech2TextProcessor:
    def speech_to_text(self, audio_file: str) -> List[Dict[str, str]]:
        """
        Perform speech-to-text conversion on the audio.
        During the process the language is detected, as well as each speaker gender.
        The speech is split into shorter transcribed audio segments (phrases?)
        ToDo: Confirm output format together with #task-03, #task-04 and #task-05

        Parameters
        ----------
        audio_file: str
            The path to the audio file

        Returns
        -------
        The list of transcribed, timestamped, text segments. Dictionary elements:
            - text: str - the transcribed text segment (phrase?)
            - start: start time of phrase within the audio, in milliseconds
            - end: end time of phrase within the audio, in milliseconds
            - language: auto detected language in audio segment (language list defined in .config)
            - speaker_gender: auto detected gender of speaker in segment ("Female" / "Male" / "Other")

        Example:

        text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

        """

        text_segments = [dict(), dict(), dict(), dict()]

        return text_segments
