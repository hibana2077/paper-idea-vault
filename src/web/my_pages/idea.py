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

def get_all_ideas():
    response = requests.get(f'http://{BACKEND_URL}/ideas')
    if response.status_code == 200:
        return response.json()['ideas']
    return []

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Idea')
    idea_left_col, idea_right_col = st.columns([7,3],vertical_alignment='center')

    with idea_left_col:
        st.title('Idea')

    with idea_right_col:
        if st.button('New Idea'):
            new_idea()

    st.divider()

    ideas = get_all_ideas()
    for idea in ideas:
        idea_card = st.container(border=True)
        idea_card.title(idea['title'])
        idea_card.write(f'Description: {idea["description"]}')
        idea_card.write(f'Tags: {idea["tags"]}')
else:
    st.write('Please login first')