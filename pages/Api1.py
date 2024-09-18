import streamlit as st

st.set_page_config(
    page_title="API 1",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto",
)

# Botão Dark/Light Mode 
if "theme" not in st.session_state:
    st.session_state.theme = st.config.get_option("theme.base")
    st.session_state.theme == "light"

with st.sidebar:
    
    # Get the current theme and create a button to switch themes
    if st.session_state.theme == "light":
        switch = st.button("🌞")  # Light mode button
    else:
        switch = st.button("🌙")  # Dark mode button

    # Check the button value and toggle the theme
    if switch:
        if st.session_state.theme == "light":
            st.session_state.theme = "dark"
            st.config.set_option("theme.base", "dark")
        else:
            st.session_state.theme = "light"
            st.config.set_option("theme.base", "light")
        st.rerun()

st.title("Api1")
