import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8081')

@st.experimental_dialog('New Idea')
def new_idea():
    with st.form(key='new_idea'):
        st.text_input('Title', key='title')
        st.text_area('Description', key='description')
        # Need to add more fields here and submit to backend
        

st.title('Idea')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Idea')
    idea_left_col, idea_right_col = st.columns([7,3],vertical_alignment='center')
else:
    st.write('Please login first')