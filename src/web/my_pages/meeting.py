import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_SERVER', 'localhost:8081')


def generate_keywords(idea_id:int)->list:
    response = requests.get(f'http://{BACKEND_URL}/keywords/{idea_id}')
    if response.status_code == 200:
        idea_description = response.json()['description']
    return []

def get_all_ideas()->dict:
    response = requests.get(f'http://{BACKEND_URL}/ideas')
    if response.status_code == 200:
        return response.json()['ideas']
    return {}

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    meeting_left_col, meeting_right_col = st.columns([7,3],vertical_alignment="bottom")

    with meeting_left_col:
        st.title('Chat')

    with meeting_right_col:
        # Select Idea to chat
        st.write('Select Idea to chat')
        ideas = get_all_ideas()
        idea_list = [idea['title'] for idea in ideas.values()]
        selected_idea = st.selectbox('Select Idea', idea_list, key='selected_idea')
        st.write(f'You selected: {selected_idea}') if selected_idea else st.write('Please select an idea')

    st.divider()

    tab_idea_meansure, tab_paper_sketch, tab_exp_design = st.tabs(['Idea Meansure', 'Paper Sketch', 'Experiment Design'])

    with tab_idea_meansure:
        st.write('Idea Meansure')

    with tab_paper_sketch:
        st.write('Paper Sketch')

    with tab_exp_design:
        st.write('Experiment Design')

else:
    st.write('Please login first')