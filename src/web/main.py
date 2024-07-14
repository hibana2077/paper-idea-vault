import time
import os
import streamlit as st

USER = os.getenv('USER', 'user')
PASSWORD = os.getenv('PASSWORD', 'password')

pg = st.navigation(
    [
    st.Page("./my_pages/idea.py", title='Idea', icon='💡'),
    st.Page("./my_pages/settings.py", title='Settings', icon='⚙️'),
    ]
)

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    pg.run()
else:
    with st.form(key='login'):
        st.text_input('Username')
        st.text_input('Password', type='password')
        if st.form_submit_button('Login'):
            if st.session_state.username == USER and st.session_state.password == PASSWORD:
                st.success('Login successful')
                st.session_state.login = True
                time.sleep(1.2)
                pg.run()
            else:
                st.error('Invalid username or password')