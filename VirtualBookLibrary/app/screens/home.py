import streamlit as st
from services.api_client import APIClient
from utils.helpers import is_valid_email

def render():
    st.session_state.user_details = APIClient.get_user(st.session_state.current_user_id)

    st.header(f"Welcome, 👤 {st.session_state.user_details.get('fullname').title()}!")
    
