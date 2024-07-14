import streamlit as st

st.title('Idea')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Idea')
else:
    st.write('Please login first')