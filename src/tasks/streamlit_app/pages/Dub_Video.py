
import streamlit as st
from project_utils.page_layout_helper import main_header
from streamlit_option_menu import option_menu
from dubbing_app.config import SUPPORTED_LANGUAGES, DEFAULT_VOICES
from dubbing_app.dubbing_app import DubbingApp 
import requests, os, asyncio
import time

target_language=''
gender=''
input_video_url=''

CSS_STYLE="""
<style>
[data-testid="stHeader"]{
        display: none;
	    }
div.css-12w0qpk.esravye1{
  position: relative;
  top: 35px; 
}
video.stVideo{width: 400px !important;}
</style>
"""


def main():
  main_header()
  st.markdown(CSS_STYLE, unsafe_allow_html=True)
  input_video_url = st.text_input('Enter Url of Youtube video : ', '')

  #DEFAULT_WIDTH = 80

  col1,col2=st.columns([1,2])
  with col1:
    st.write("Select the target language: ")
  with col2:
    language_list=[itemstr.capitalize() for itemstr in list((SUPPORTED_LANGUAGES.values()))]
    language_icon = []
    for _ in language_list:
      language_icon.append("None")
    target_language = option_menu(None, language_list,
  			  icons=language_icon, menu_icon="", default_index=0, orientation="horizontal")
  col3,col4 = st.columns([1,2])
  with col3:
    st.write("Select the Gender: ")
  with col4:
    if target_language:
      language_key = [k for k, v in SUPPORTED_LANGUAGES.items() if v == target_language.lower()]
      voice_list = list(DEFAULT_VOICES[language_key[0]])
      voice_list.append("Auto-detect gender")
      voice_icon = []
      for _ in voice_list:
        voice_icon.append("None")
      gender = option_menu(None, 
 			 list(voice_list), icons=voice_icon,
  		 menu_icon="", default_index=0, orientation="horizontal")
    else:
      gender = option_menu(None, 
	 		 ["Male", "Female", "Auto-detect gender"], icons=['None', 'None', 'None'],
  		 menu_icon="", default_index=0, orientation="horizontal")
  _,col5,_ = st.columns([2,1,2])
  with col5:
    btn_process =st.button('Process') 
  if btn_process:
    if input_video_url:
      gender_voice = gender
      if gender=="Auto-detect gender":
        gender_voice = None
              
      target_lang= list(SUPPORTED_LANGUAGES.keys())[list(SUPPORTED_LANGUAGES.values()).index(target_language.lower())]
      with st.spinner('Dubbing video process in progress...'):
        dubbed_video_path = asyncio.run(dubapp.process_pipeline(input_video_url, target_lang, gender_voice))
        st.video(dubbed_video_path, )
        with open(dubbed_video_path,'rb') as video_file:
          st.download_button(label = 'Download Video', data = video_file, file_name = os.path.basename(dubbed_video_path))
    else:
      st.write("Enter the input url")
  
#target_language,gender
if __name__ == "__main__":
  dubapp = DubbingApp()
  main()
    
