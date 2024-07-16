import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_SERVER', 'localhost:8081')

@st.experimental_dialog('New Idea')
def new_idea():
    with st.form(key='new_idea'):
        title = st.text_input('Title', key='title')
        description = st.text_area('Description', key='description')
        tags = st.text_input('Tags', key='tags')
        if st.form_submit_button('Create Idea'):
            response = requests.post(f'http://{BACKEND_URL}/new_idea', json={'title': title, 'description': description, 'tags': tags})
            if response.status_code == 200:
                st.success('Idea created')
            else:
                st.error('Failed to create idea')

def get_all_ideas()->dict:
    response = requests.get(f'http://{BACKEND_URL}/ideas')
    if response.status_code == 200:
        return response.json()['ideas']
    return {}

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    idea_left_col, idea_right_col = st.columns([7,3],vertical_alignment="bottom")

    with idea_left_col:
        st.title('Idea')

    with idea_right_col:
        if st.button('New Idea'):
            new_idea()

    st.divider()

    ideas = get_all_ideas()
    for idea_key in ideas.keys():
        idea_card = st.container(border=True)
        with idea_card:
            idea_card_left_col, idea_card_right_col = st.columns([7,3],vertical_alignment="bottom")
            
            with idea_card_left_col:
                st.subheader(ideas[idea_key]['title'])
                st.write(f"Description: {ideas[idea_key]['description']}")
                st.write(f"Tags: {ideas[idea_key]['tags']}")
                st.write(f"Idea ID: {idea_key}")

            with idea_card_right_col:
                st.button('Details')
        
else:
    st.write('Please login first')