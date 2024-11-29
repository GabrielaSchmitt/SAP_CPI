import streamlit as st

# Set page configuration with a title, icon, and expanded sidebar
st.set_page_config(
    page_title="CPI Statistics",
    page_icon="🔍",
    initial_sidebar_state="expanded",
    layout="wide",
    menu_items={
        'About': "Made by Wolketech, Sep 2024."
    }
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


st.title("🔍 CPI Statistics")
st.write("Seja bem vindo ao Dashboard de Integrações SAP.")