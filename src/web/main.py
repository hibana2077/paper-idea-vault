import streamlit as st

pg = st.navigation(
    [
    st.Page("./my_pages/chat.py", title='Chat', icon='💬'),
    st.Page("./my_pages/settings.py", title='Settings', icon='⚙️'),
    ]
)

pg.run()