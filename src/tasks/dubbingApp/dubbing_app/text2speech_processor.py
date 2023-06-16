from pydub import AudioSegment
from typing import Dict, List, Union


class Text2SpeechProcessor:
    def text_to_speech(self, text_segments: list, target_language: str) -> List[Dict[str, Union[AudioSegment, int]]]:
        """
        Perform text-to-speech, generating audio segments from the given text segments.
        ToDo: Confirm output format together with  #task-05

        Parameters
        ----------
        text_segments: list
            The list of translated, timestamped, text segments. Dictionary elements:
            - text: str - the translated text segment (phrase?)
            - start: int - start time of phrase within the audio, in milliseconds
            - end: int - end time of phrase within the audio, in milliseconds
            - language: str - auto detected language in audio segment (language list defined in .config)
            - speaker_gender: str - auto detected gender of speaker in segment ("Female" / "Male" / "Other")

        target_language: str
            The target language, that was applied during translation (language code)

        Returns
        -------
        The list of timestamped audio segments. Dictionary elements:
            - audio: AudioSegment - a generated audio segment (phrase?)
            - start: int - start time of phrase within the audio, in milliseconds
            - end: int - end time of phrase within the audio, in milliseconds

        Example:

        audio_segments = [
            {"audio": AudioSegment(), "start": 1100, "end": 1800,
            {"audio": AudioSegment(), "start": 2000, "end": 2345,
        ]

        """

        audio_segment = AudioSegment.empty()

        # create list with all audio generated segments
        audio_segments = [dict(), dict()]

        return audio_segments
