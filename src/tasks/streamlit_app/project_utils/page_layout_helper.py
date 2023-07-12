
from datetime import date
import os, glob, pathlib, re, base64
import streamlit as st


PAGE_TITLE="Automate Video Dubbing Process"

FOOTER_TEXT=f"Project by Omdena Montreal, Canada Chapter - {date.today().year}"

def image_to_base64(image_path):
  with open(image_path, "rb") as f:
     data = f.read()
  return base64.b64encode(data).decode()
	
def get_page_title_id():
  s = re.sub(r"[^\w\s]", '', PAGE_TITLE)
  s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', s)
  s = re.sub(r"\s+", '-', s)
  return s.lower()

def get_page_title():
  return PAGE_TITLE

BACKGROUND_IMAGE = image_to_base64(os.path.abspath('./images/cover.png'))  #"https://omdena.com/wp-content/uploads/2023/04/Automate-Dubbing-Process-using-NLP-1.jpeg"

PROFILE_IMAGE = os.path.abspath('./images/omdena_montreal_logo.png')  #"https://omdena.com/wp-content/uploads/2022/07/place-holder.png"

HEADER_STYLE=f"""<style>
	          [data-testid="stToolbar"]{{
	          visibility: hidden;
	          top: -50px;
	          }}
            #root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(1) > div > div > div > div:nth-child(1) > div > div > div > div > div
            {{
            height: 300px;
            width: 300px;
            }}
            #root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(1) > div > div > div > div:nth-child(1) > div > div > div > div > div > img
            {{
            height: 300px;
            width: 300px;
            padding-top: 40%;
            padding-bottom: 10%;
            padding-left: 15%;
            padding-right: 10%;
            }}
            #root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(1) > div{{
            background-image: url("data:image/png;base64,{ BACKGROUND_IMAGE }");
            background-size: cover; 
            background-position: center;
            }}
            #{get_page_title_id()}{{
            height: 250px;
            }}
            #{get_page_title_id()} > div {{
            bottom: 1%;
            position: absolute;
            color: white;
            }}

            footer {{
            visibility: hidden;
            position: relative;
            }}
            footer:before {{
            visibility: visible;
            position: relative;
	          content: {FOOTER_TEXT}
            }}
        </style>
    """

def set_page_settings():
  st.set_page_config(
    page_title=get_page_title(),
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded", 
)
def main_header():
  with st.container():
      left_side, right_side = st.columns([1,2], gap="small")
      with left_side:
          st.image(PROFILE_IMAGE, width = 300, output_format = "auto")          
      with right_side:
          st.markdown(HEADER_STYLE, unsafe_allow_html=True)
          st.title(PAGE_TITLE)
  st.markdown("<br>", unsafe_allow_html=True)
