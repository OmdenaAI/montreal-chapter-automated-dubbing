
import streamlit as st
from project_utils.page_layout_helper import main_header
from streamlit_option_menu import option_menu
from dubbing_app.config import SUPPORTED_LANGUAGES
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
    target_language = option_menu(None, ["English", "French", "German", "Spanish"],
  			  icons=['None', 'None', 'None', 'None'],
  			  menu_icon="", default_index=0, orientation="horizontal")
  col3,col4 = st.columns([1,2])
  with col3:
    st.write("Select the Gender: ")
  with col4:
    gender = option_menu(None, 
			 #["Male", "Female"], icons=['None', 'None'],			 
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
        st.video(dubbed_video_path)
    else:
      st.write("Enter the input url")
  
#target_language,gender
if __name__ == "__main__":
  dubapp = DubbingApp()
  main()
    
