# need pip install translate 
# this script will need to be extended once we know
# the form of output from task-02, and the
# required form of input for task-04
import sys
from translate import Translator

def chunk_translator(text, lang):
    '''input: text (string), 
    lang: language of translation (ISO_639-1 format)
    language of text is autodetected
    output: text in lang'''

    translator = Translator(to_lang=lang)
    translation = translator.translate(text)

    return translation


if __name__ == '__main__': 
    if len(sys.argv) != 3:
        print("Usage: function requires text and the language to translate it to")
        sys.exit()

    text = sys.argv[1]
    lang = sys.argv[2]
   
    print(chunk_translator(text, lang))