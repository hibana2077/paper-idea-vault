import time
import os
import streamlit as st

USER = os.getenv('USER', 'user')
PASSWORD = os.getenv('PASSWORD', 'password')
BACKEND_SERVER = os.getenv('BACKEND_SERVER', 'http://localhost:8081')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq')
LLM_MODEL = os.getenv('LLM_MODEL', 'gemma2-9b-it')
LLM_API_TOKEN = os.getenv('LLM_API_TOKEN', 'null')

pg = st.navigation(
    [
    st.Page("./my_pages/idea.py", title='Idea', icon='💡'),
    st.Page("./my_pages/settings.py", title='Settings', icon='⚙️'),
    st.Page("./my_pages/meeting.py", title='Meeting', icon='📝'),
    ]
)

if "login" not in st.session_state:
    st.session_state.login = False

if "LLM_PROVIDER" not in st.session_state:
    st.session_state.LLM_PROVIDER = LLM_PROVIDER

if "LLM_MODEL" not in st.session_state:
    st.session_state.LLM_MODEL = LLM_MODEL

if "LLM_API_TOKEN" not in st.session_state:
    st.session_state.LLM_API_TOKEN = LLM_API_TOKEN

if st.session_state.login:
    pg.run()
else:
    with st.form(key='login_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.form_submit_button('Login'):
            if username == USER and password == PASSWORD:
                st.success('Login successful')
                st.session_state.login = True
                time.sleep(1.2)
                st.rerun()
            else:
                st.error('Invalid username or password')