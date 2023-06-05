from translate import Translator

# some hard coded data to test the functions
text1 = 'Imagine a world where artificial intelligence is a seamless part of our everyday lives.'
text2 = 'The smart devices anticipating our needs in our homes, adjusting the room temperature just right, playing our favorite tunes effortlessly, and even preparing our morning coffee to perfection.'
text3 = 'Our virtual assistant being the perfect trusted friend in this utopian world.'
text4 = ' The above scenario seems like a dream come true, right?'
tple1 = (text1, 10, 'Male')
tple2 = (text2, 20, 'Female')
tple3 = (text3, 30, 'Male')
tple4 = (text4, 40, 'Female')
given_list = [tple1, tple2, tple3, tple4]

def chunk_translator(text, lang):
    '''input: text (string), 
    lang = language of translation (ISO_639-1 format),
    language of text is autodetected
    output: text in lang'''

    translator = Translator(to_lang=lang)
    translation = translator.translate(text)

    return translation

def triples_text_translator(input_list, language):
    '''input: list of triples = (text, timestamp, speaker gender) and the language for translation, output: list of triples with text translated'''
    translated_list = []
    for triple in input_list:
        new_text = chunk_translator(triple[0], language)
        new_triple = (new_text, triple[1], triple[2])
        translated_list.append(new_triple)

    return translated_list

print(triples_text_translator(given_list, "fr"))
