#hello this is a sample text-to-speech function for google collab i hope it would be helpful to beginners like me.
#first step install the packages needed

# ! pip install pyttsx3
# !apt-get update
# !apt-get install -y espeak

#2nd step
#mount your collab to google drive 
#add working path in here it is named audio_path

from google.colab import drive
drive.mount('/content/drive')

import os

root_dir= "/content/drive/My Drive/"

audio_path="Colab Notebooks/audio_path/"

def create_working_directory(audio_path):
  if os.path.isdir(root_dir + audio_path)==False:
    os.mkdir(root_dir + audio_path)
    print(root_dir + audio_path+ 'did not exist and was created')
  os.chdir(root_dir + audio_path)

  
create_working_directory(audio_path)

#3rd step input txt file to audio_path in this function it is named hello.txt wherin the file contains "hello omdena"
import pyttsx3
import IPython.display as ipd

def text_to_speech_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speech rate (words per minute)
    engine.setProperty('volume', 0.8)  # You can adjust the volume (0.0 to 1.0)

    # Save the audio output to a file
    audio_path = 'output.wav'
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    # Play the audio using IPython.display.Audio
    return ipd.Audio(audio_path)

# Example usage: Provide the path to your text file
file_path = 'hello.txt'
text_to_speech_from_file(file_path)

