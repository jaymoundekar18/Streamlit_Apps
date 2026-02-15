import streamlit as st
from core.config import APP_TITLE
from screens import home, authentication, account, add_books

# Page Configurations
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)


# SESSION STATE INITIALIZATION
# Authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Current page
if "page" not in st.session_state:
    st.session_state.page = "None"

# Sidebar visibility
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = False


# AUTHENTICATION ROUTING
# If user is NOT authenticated
if not st.session_state.authenticated:
    st.session_state.sidebar_visible = False
    authentication.render()
    st.stop() 


#IF AUTHENTICATED
st.session_state.sidebar_visible = True

# If user just logged in and page not set → default to Home
if st.session_state.page == "None":
    st.session_state.page = "Home"


# SIDEBAR NAVIGATION
st.sidebar.info(
    "Use the refresh button to update the dashboard.\n"
    "⚠️ Do Not refresh using CTRL+R session will be lost!"
)

st.sidebar.title("Navigation")

if st.sidebar.button("Refresh", icon="🔄", key="refresh_button"):
    st.rerun()

if st.sidebar.button("Home", icon="🏠", key="home_button",width=300):
    st.session_state.page = "Home"

if st.sidebar.button("Add Books", icon="📚", key="addBook_button",width=300):
    st.session_state.page = "AddBook"
    
if st.sidebar.button("Account", icon="👤", key="account_button",width=300):
    st.session_state.page = "Account"

if st.sidebar.button("Logout", icon="↩️", key="logout_button",width=300):
    st.session_state.authenticated = False
    st.session_state.page = "None"
    st.session_state.logged_user = None
    st.session_state.current_user_id = None
    st.rerun()

# PAGE RENDERING
if st.session_state.page == "Home":
    home.render()
    
elif st.session_state.page == "AddBook":
    add_books.render()

elif st.session_state.page == "Account":
    account.render()
