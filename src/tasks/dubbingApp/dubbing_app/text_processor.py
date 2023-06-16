from typing import Dict, List, Union
from translate import Translator


class TextProcessor:
    def translate_text_segments(self, text_segments: list, target_language: str) -> List[Dict[str, Union[str, int]]]:
        """
        Perform text translation of all text segments.

        Parameters
        ----------
        text_segments: list
            The list of transcribed, timestamped, text segments. Dictionary elements:
            - text: str - the transcribed text segment (phrase?)
            - start: int - start time of phrase within the audio, in milliseconds
            - end: int - end time of phrase within the audio, in milliseconds
            - language: str - original language in audio segment (code in ISO_639-1 format, as defined in .config)
            - speaker_gender: str - auto detected gender of speaker in segment ("Female" / "Male" / "Other")

        target_language: str
            The target language for the translation (language code)

        Returns
        -------
        The list of translated, timestamped, text segments. Same format as input, only "text" is now the translated text

        Example:

        text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

        """

        # iterate through the original text_segments to create a similar list of dicts but with text translated
        translated_list = []
        for segment in text_segments:
            new_text = self.translate_text(segment["text"], target_language, segment["language"])
            new_dict = segment.copy()
            new_dict["text"] = new_text
            # new_dict["language"] = target_language
            translated_list.append(new_dict)

        return translated_list

    @staticmethod
    def translate_text(text: str, to_language: str, from_language: str = None) -> str:
        """
        Translate a single text string. Original language of text is currently auto-detected.

        Parameters
        ----------
        text: str
            Text to translate
        to_language: str
            The target language for the translation. 2-letter language code in ISO_639-1 format, as defined in .config
        from_language: str
            The original language in text. 2-letter language code in ISO_639-1 format, as defined in .config

        Returns
        -------
        The translated string.
        """

        translator = Translator(to_lang=to_language, from_lang=from_language)
        translation = translator.translate(text)

        return translation
