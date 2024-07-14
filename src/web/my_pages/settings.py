import streamlit as st

st.title('Settings')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Settings')
else:
    st.write('Please login first')