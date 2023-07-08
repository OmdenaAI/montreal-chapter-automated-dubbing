
from datetime import date
import os
import glob as glob
import streamlit as st
import pathlib
import re

PROFILE_IMAGE="https://omdena.com/wp-content/uploads/2022/07/place-holder.png"

BACKGROUND_IMAGE="https://omdena.com/wp-content/uploads/2023/04/Automate-Dubbing-Process-using-NLP-1.jpeg"

PAGE_TITLE="Breaking Down Language Barriers: Using AI and NLP to Automate Dubbing Process for Improved Accessibility and Inclusivity"

FOOTER_TEXT=f"Project by Omdena Montreal, Canada Chapter - {date.today().year}"

def get_page_title_id():
  s = re.sub(r"[^\w\s]", '', PAGE_TITLE)
  s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', s)
  s = re.sub(r"\s+", '-', s)
  return s.lower()

def get_page_title():
  return PAGE_TITLE

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
            background-image: url("{BACKGROUND_IMAGE}");
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
          st.image(PROFILE_IMAGE, width=300)          
      with right_side:
          st.markdown(HEADER_STYLE, unsafe_allow_html=True)
          st.title(PAGE_TITLE)
  st.markdown("<br>", unsafe_allow_html=True)
