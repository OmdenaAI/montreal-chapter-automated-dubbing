from typing import List, Dict


class TextProcessor:
    def translate_text_segments(self, text_segments: list, target_language: str) -> List[Dict[str, int, int, str, str]]:
        """
        Perform text translation of all text segments.
        ToDo: Confirm output format together with #task-04 and #task-05

        Parameters
        ----------
        text_segments: list
            The list of transcribed, timestamped, text segments. Dictionary elements:
            - text: str - the transcribed text segment (phrase?)
            - start: int - start time of phrase within the audio, in milliseconds
            - end: int - end time of phrase within the audio, in milliseconds
            - language: str - auto detected language in audio segment (language list defined in .config)
            - speaker_gender: str - auto detected gender of speaker in segment ("Female" / "Male" / "Other")

        target_language: str
            The target language for the translation (language code)

        Returns
        -------
        The list of translated, timestamped, text segments. Same format as input

        Example:

        text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

        """

        # iterate through the original text_segments to create a similar list of dicts but with text translated
        translated_text = []
        for segment in text_segments:
            translated_segment = self.translate_text(segment['text'], target_language)

            translated_text = []  # replace original text with translated text, in text_segments

        return translated_text

    @staticmethod
    def translate_text(text: str, target_language: str) -> str:
        """
        Translate a single text string.

        Parameters
        ----------
        text: str
            Text to translate
        target_language: str
            The target language for the translation (language code)

        Returns
        -------
        The translated string.
        """

        return ""
