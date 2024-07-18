import streamlit as st
import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_SERVER', 'localhost:8081')

def suggest_paper_topic(related_work:list, api_key:str)->list:
    response = requests.post(f'http://{BACKEND_URL}/suggest_topic', json={'related_works': related_work, 'api_key': api_key})
    if response.status_code == 200:
        return response.json()['suggestions']
    return []

def search_related_work(description:str, keywords:str, api_key:str)->list:
    response = requests.post(f'http://{BACKEND_URL}/related_work', json={'description': description, 'keywords': keywords, 'api_key': api_key})
    if response.status_code == 200:
        # Return related work
        # list[dict{"title": str, "summary": str, "arxiv_id": str, "authors": list[str]}]
        return response.json()['related_work']
    return []

def generate_keywords(idea_id:int)->list:
    response = requests.get(f'http://{BACKEND_URL}/idea/{idea_id}')
    if response.status_code == 200:
        idea_description = response.json()['description']
        api_key = st.session_state.LLM_API_TOKEN
        response = requests.post(f'http://{BACKEND_URL}/generate_keywords', json={'description': idea_description, 'api_key': api_key})
        if response.status_code == 200:
            return response.json()['keywords']
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
        st.title('Meeting')

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
        if selected_idea:
            idea_id = [idea_id for idea_id, idea in ideas.items() if idea['title'] == selected_idea][0]
            keywords = generate_keywords(idea_id)
            with st.form(key='edit_keywords'):
                edited_keywords = st.text_area('Keywords', value=','.join(keywords)[1:], key='edited_keywords')
                if st.form_submit_button('Search'):
                    st.info(f"Keywords: {edited_keywords}")
                    # Call API
                    related_work = search_related_work(ideas[idea_id]['description'], edited_keywords, st.session_state.LLM_API_TOKEN)
                    st.session_state.related_work = related_work
                    st.success('Search completed')
            
        if 'related_work' in st.session_state:
            related_work_from_session = st.session_state.related_work
            paper_left_col, paper_right_col = st.columns([3,3],vertical_alignment="bottom")
            for idx, work in enumerate(related_work_from_session[:4]):
                # display paper
                with st.expander(f'Paper {idx+1}'):
                    st.write(f'Title: {work["title"]}')
                    st.write(f'Summary: {work["summary"]}')
                    st.write(f'Authors: {work["authors"][:5]}')
                    st.write(f'Arxiv ID: {work["arxiv_id"]}')
            if st.button('Suggest new paper topic', key='suggest_paper'):
                suggested_topics = suggest_paper_topic(related_work_from_session[:5], st.session_state.LLM_API_TOKEN)
                st.markdown('### Suggested Topics')
                for topic in suggested_topics:
                    with st.expander(f'Topic {topic["suggestion"]}'):
                        st.markdown(f'{topic["suggestion_detail"]}')


    with tab_paper_sketch:
        st.write('Paper Sketch')

    with tab_exp_design:
        st.write('Experiment Design')

else:
    st.write('Please login first')