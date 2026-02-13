import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")
    return st.sidebar.radio(
        "Go to",
        ["Home", "Dashboard","My Bookshelf", "Start Reading"]
    )
