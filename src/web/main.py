import streamlit as st

pg = st.navigation(
    [
    st.Page("./my_pages/idea.py", title='Idea', icon='💡'),
    st.Page("./my_pages/settings.py", title='Settings', icon='⚙️'),
    ]
)

pg.run()