import streamlit as st
from services.api_client import APIClient
from utils.helpers import is_valid_email
from analytics import reader

def render():
    st.session_state.user_details = APIClient.get_user(st.session_state.current_user_id)

    st.markdown(f"## Welcome, 👤 {st.session_state.user_details.get('fullname').title()}!")
    
    reader.showanalytics()