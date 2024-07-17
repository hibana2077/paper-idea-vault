import streamlit as st

st.title('Settings')

if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.write('Settings')
    with st.form(key='settings'):
        llm_provider = st.text_input('LLM Provider', value=st.session_state.LLM_PROVIDER)
        llm_model = st.text_input('LLM Model', value=st.session_state.LLM_MODEL)
        llm_api_token = st.text_input('LLM API Token', value=st.session_state.LLM_API_TOKEN)
        if st.form_submit_button('Save'):
            st.session_state.LLM_PROVIDER = llm_provider
            st.session_state.LLM_MODEL = llm_model
            st.session_state.LLM_API_TOKEN = llm_api_token
            st.success('Settings saved')
else:
    st.write('Please login first')