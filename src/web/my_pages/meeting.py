import streamlit as st
import requests
import os

BACKEND_URL = os.getenv('BACKEND_SERVER', 'localhost:8081')

def get_all_paper_sketches()->dict:
    response = requests.get(f'http://{BACKEND_URL}/paper_sketches')
    if response.status_code == 200:
        return response.json()['paper_sketches']
    return {}

def save_paper_sketch(paper_sketch)->bool:
    response = requests.post(f'http://{BACKEND_URL}/save_paper_sketch', json={'paper_sketch': paper_sketch})
    if response.status_code == 200:
        return True
    return False

def generate_paper_sketch(suggestion_title:str, suggestion:str, suggestion_detail:str, api_key:str)->str:
    response = requests.post(f'http://{BACKEND_URL}/generate_paper_sketch', json={'suggestion_title': suggestion_title, 'suggestion': suggestion, 'suggestion_detail': suggestion_detail, 'api_key': api_key})
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to generate paper sketch"}

def get_all_suggestions()->dict:
    response = requests.get(f'http://{BACKEND_URL}/suggestions')
    if response.status_code == 200:
        return response.json()['suggestions']
    return {}

def save_suggestion(suggestion_title:str, suggestion:str, suggestion_detail:str)->bool:
    response = requests.post(f'http://{BACKEND_URL}/save_suggestion', json={'suggestion_title': suggestion_title, 'suggestion': suggestion, 'suggestion_detail': suggestion_detail})
    if response.status_code == 200:
        return True
    return False

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
        st.subheader('Idea Meansure')
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
                st.session_state.suggested_topics = suggested_topics
        
        if 'suggested_topics' in st.session_state:
            suggested_topics = st.session_state.suggested_topics
            st.markdown('### Suggested Topics')
            for topic in suggested_topics:
                with st.expander(f'{topic["suggestion_title"]}'):
                    st.markdown(f'### suggestion')
                    st.markdown(f'{topic["suggestion"]}')
                    st.markdown(f'### suggestion detail')
                    st.markdown(f'{topic["suggestion_detail"]}')
            with st.form(key='save_suggestion'):
                save_suggestion_title = st.selectbox('Select Suggestion', [topic['suggestion_title'] for topic in suggested_topics], key='save_suggestion_title')
                sumbit_button = st.form_submit_button('Save Suggestion')
                if sumbit_button:
                    save_suggestion_dict = [topic for topic in suggested_topics if topic['suggestion_title'] == save_suggestion_title][0]
                    status = save_suggestion(save_suggestion_dict['suggestion_title'], save_suggestion_dict['suggestion'], save_suggestion_dict['suggestion_detail'])
                    if status:
                        st.success('Suggestion saved')
                    else:
                        st.error('Failed to save suggestion')

    with tab_paper_sketch:
        st.subheader('Paper Sketch')

        # List all saved suggestions
        suggestions = get_all_suggestions()
        selected_suggestion = st.selectbox('Select Suggestion', [suggestions[key]['suggestion_title'] for key in suggestions.keys()], key='selected_suggestion')

        if selected_suggestion:
            suggestion = [suggestions[key] for key in suggestions.keys() if suggestions[key]['suggestion_title'] == selected_suggestion][0]
            with st.form('generate_paper_sketch'):
                edit_title = st.text_input('Title', value=suggestion['suggestion_title'], key='edit_title')
                edit_suggestion = st.text_area('Suggestion', value=suggestion['suggestion'], key='edit_suggestion')
                edit_suggestion_detail = st.text_area('Suggestion Detail', value=suggestion['suggestion_detail'], key='edit_suggestion_detail')
                if st.form_submit_button('Generate Paper Sketch'):
                    st.session_state.generated_paper_sketch = generate_paper_sketch(edit_title, edit_suggestion, edit_suggestion_detail, st.session_state.LLM_API_TOKEN)
                    st.success('Paper Sketch generated')

        if 'generated_paper_sketch' in st.session_state:
            generated_paper_sketch = st.session_state.generated_paper_sketch
            st.json(generated_paper_sketch)
            with st.form("Save paper sketch"):
                name_of_paper_sketch = st.text_input('Name of Paper Sketch', key='name_of_paper_sketch')
                save_button = st.form_submit_button('Save Paper Sketch')
                if save_button:
                    status = save_paper_sketch(generated_paper_sketch)
                    if status:
                        st.success('Paper Sketch saved')
                    else:
                        st.error('Failed to save Paper Sketch')
            
    with tab_exp_design:
        st.subheader('Experiment Design')

        # List all saved paper sketches
        paper_sketches = get_all_paper_sketches()
        selected_paper_sketch = st.selectbox('Select Paper Sketch', paper_sketches.keys(), key='selected_paper_sketch')

        if selected_paper_sketch:
            paper_sketch = paper_sketches[selected_paper_sketch]
            st.json(paper_sketch)
            st.session_state.selected_paper_sketch_dict = paper_sketch
else:
    st.write('Please login first')