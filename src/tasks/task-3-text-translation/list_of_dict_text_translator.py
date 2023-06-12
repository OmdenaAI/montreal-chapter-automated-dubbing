#pip install translate
from translate import Translator

text_segments = [
            {"text": "Hola", "start": 1100, "end": 1800, "language": "es", "speaker_gender": "Female"},
            {"text": "Buenos dias", "start": 2000, "end": 2345, "language": "es", "speaker_gender": "Male"},
        ]

def chunk_translator(text, to_lang, from_lang):
    '''input: text (string), 
    to_lang = language of translation (ISO_639-1 format),
    from_language = language of text
    output: text in to_lang'''

    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text)

    return translation

def list_of_dict_text_translator(input_list, language):
    '''input: list of dictionaries and the language for translation, output: list of dictionaries with text translated'''
    translated_list = []
    for dict in input_list:
        new_text = chunk_translator(dict["text"], language, dict["language"])
        new_dict = dict.copy()
        new_dict["text"] = new_text
        new_dict["language"] = language
        translated_list.append(new_dict)

    return translated_list

print(list_of_dict_text_translator(text_segments, "en"))