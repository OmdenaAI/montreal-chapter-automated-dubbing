from typing import Dict, List, Union
from translate import Translator


class TextProcessor:
    def translate_text_segments(self, text_dict: dict, target_language: str) -> Dict[str, List[Union[str, int]]]:
        """
        Perform text translation of all text segments.

        Parameters
        ----------
        text_dict: dict
            The dictionary of transcribed, timestamped, text segments. Dictionary elements:
                - language: str - original language in audio (code in ISO_639-1 format, as defined in .config)
                - speaker_gender: str - auto-detected gender of speaker ('female' / 'male' / '')
                - segments: list  - list of dictionaries with the following elements:
                    - id: int - segment sequence number
                    - phrase: str - phrase text
                    - start: int - start time of phrase within the audio, in milliseconds
                    - end: int - end time of phrase within the audio, in milliseconds
                - text: str - transcribed text in full

        target_language: str
            The target language for the translation (language code)

        Returns
        -------
        The list of translated, timestamped, text segments. Same format as input, only "phrase" in each segment is
        replaced by the translated text

        Example:

        translated_text_dict = {
            'language': 'es',
            'speaker_gender': '',
            'segments': [
              {'id': 0,
               'start': 0.0,
               'end': 9.82,
               'phrase': 'What is the worst insect on the planet?'},
              {'id': 1,
               'start': 15.48,
               'end': 17.16,
               'phrase': 'The mosquito.'}
               ],
            'text': 'What is the worst insect on the planet? The mosquito.'
        }
        """

        # iterate through the original text_segments to create a similar list of dicts but with text translated
        translated_list = []
        for segment in text_dict['segments']:
            new_text = self.translate_text(segment['phrase'], target_language, text_dict['language'])
            new_dict = segment.copy()
            new_dict['phrase'] = new_text
            # new_dict["language"] = target_language
            translated_list.append(new_dict)

        translated_text_dict = text_dict
        translated_text_dict['segments'] = translated_list

        return translated_text_dict

    @staticmethod
    def translate_text(text: str, to_language: str, from_language: str = None) -> str:
        """
        Translate a single text string. If not provided in ```from_language```, original language is auto-detected.

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
