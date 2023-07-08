
import streamlit as st
from datetime import date
import os
import glob as glob
from project_utils.page_layout_helper import set_page_settings, get_page_title, main_header
#

def active_contributors():
  ACTIVE_CONTRIBUTORS_PAGE_CHAPTERLEAD='''
| Chapter Name | Lead Name |
|--|--|
| Montreal, Canada Chapter | Mohamed Kandil |
'''

  ACTIVE_CONTRIBUTORS_PAGE_MEMBERS_LIST='''
| Task Name | Active Contributors |
|--|--|
| Knowledge | - |
| Video Processing | - |
| Speech to Text | - |
| Text Translation | - |
| Text to Speech | - |
| Dubbing Processing | - |
| User Interface | - |
| Documentation | - |
'''

  with st.container():
    st.markdown(ACTIVE_CONTRIBUTORS_PAGE_CHAPTERLEAD, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(ACTIVE_CONTRIBUTORS_PAGE_MEMBERS_LIST, unsafe_allow_html=True)


def about_project():
  ABOUT_PROJECT_CONTENT="""
#####  This project is initiated by the Omdena Montreal, Canada Chapter to solve Real World Problems.

### Project background
The challenge is to develop an AI-powered dubbing app that automatically dubs videos in different languages. The app should be able to detect speech in the original video and generate synchronized dubbing in the desired language using advanced machine learning and natural language processing techniques. The application will streamline the dubbing process, making it more accessible and cost-effective for various sectors, including education, entertainment, business, tourism, and news.

### The problem
Traditional dubbing methods are time-consuming, expensive, and often require a large team of professionals. The AI Dubbing App Challenge aims to provide an innovative solution that can streamline the dubbing process and make it more accessible and affordable.

The AI-powered dubbing application can cater to diverse applications, such as entertainment, education, documentaries, webinars, conferences, language learning, tourism, business, news, social media, and accessibility for blind people.

### Project goals
The project's goal is to: - 
+ Develop an AI-powered dubbing app that can detect speech in the original video and generate synchronized dubbing in the desired language.
+ Improve the accuracy and quality of the dubbing process using state-of-the-art machine learning and NLP techniques.
+ Provide an innovative and affordable solution for content creators and language learners.
+ Promote inclusivity and accessibility by designing the AI-powered dubbing application to cater to the needs of diverse users, including individuals with visual impairments and non-native speakers.
+ Contribute to the advancement of machine learning and NLP techniques by sharing the project's findings, challenges, and successes with the broader scientific and research communities.
"""

  with st.container():
    st.markdown(ABOUT_PROJECT_CONTENT, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def about_project_style():
  ABOUT_PROJECT_STYLE='''
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 24px;
  background-color: rgb(240, 242, 246);
}
</style>
'''
  st.write(ABOUT_PROJECT_STYLE, unsafe_allow_html=True)


def main():
  set_page_settings()
  main_header()
  about_project_style()
  project_tab, team_tab = st.tabs(["  **About Project** ", "  **Active Team Contributors**  "])

  with project_tab:
    about_project()
   
  with team_tab:
    active_contributors()

if __name__ == "__main__":
  main()   
