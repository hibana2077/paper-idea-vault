import streamlit as st

st.title('Settings')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Settings')
    with st.form(key='settings'):
        st.text_input('LLM Provider', value=st.session_state.LLM_PROVIDER)
        st.text_input('LLM Model', value=st.session_state.LLM_MODEL)
        st.text_input('LLM API Token', value=st.session_state.LLM_API_TOKEN)
        if st.form_submit_button('Save'):
            st.session_state.LLM_PROVIDER = st.session_state.LLM_PROVIDER
            st.session_state.LLM_MODEL = st.session_state.LLM_MODEL
            st.session_state.LLM_API_TOKEN = st.session_state.LLM_API_TOKEN
else:
    st.write('Please login first')