import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8081')

@st.experimental_dialog('New Idea')
def new_idea():
    with st.form(key='new_idea'):
        title = st.text_input('Title', key='title')
        description = st.text_area('Description', key='description')
        tags = st.text_input('Tags', key='tags')
        if st.form_submit_button('Create Idea'):
            response = requests.post(f'{BACKEND_URL}/new_idea', json={'title': title, 'description': description, 'tags': tags})
            if response.status_code == 200:
                st.experimental_dialog('Success', 'Idea created successfully')
            else:
                st.experimental_dialog('Error', 'Failed to create idea')

st.title('Idea')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Idea')
    idea_left_col, idea_right_col = st.columns([7,3],vertical_alignment='center')
else:
    st.write('Please login first')