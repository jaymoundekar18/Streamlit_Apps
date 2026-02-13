# import streamlit as st
# from app.core.config import APP_TITLE
# from app.screens import home, dashboard, authentication, account
# from app.services.api_client import APIClient

# st.set_page_config(page_title=APP_TITLE, layout="wide")

# st.title(APP_TITLE)

# if "sidebar_visible" not in st.session_state:
#     st.session_state.sidebar_visible = True

# # Initialize auth state
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# # Routing logic
# if st.session_state.authenticated:
#    st.session_state.page = "Home"
#    st.session_state.sidebar_visible = True
# else:
#     st.session_state.sidebar_visible = False
#     authentication.render()

# # Initialize session state
# if "page" not in st.session_state:
#     st.session_state.page = "None"


# if st.session_state.sidebar_visible:

#     # Sidebar buttons
#     st.sidebar.info("Use the refresh button to update the dashboard. Please don't refresh the tab using CTRL+R, your session will be lost!")
#     st.sidebar.title("Navigation")

#     is_disabled = not st.session_state.authenticated

#     if st.sidebar.button(" 🔄 Refresh",disabled=is_disabled,key="refresh_button"):
#         st.rerun()

#     if st.sidebar.button("🏠 Home",width=200,disabled=is_disabled,key="home_button"):
#         st.session_state.page = "Home"

#     if st.sidebar.button("📊 Dashboard",width=200,disabled=is_disabled,key="dashboard_button"):
#         st.session_state.page = "Dashboard"

#     if st.sidebar.button("👤 Account",width=200,disabled=is_disabled,key="account_button"):
#         st.session_state.page = "Account"

#     if st.sidebar.button("↩️ Logout",width=200,disabled=is_disabled,key="logout_button"):
#         st.session_state.authenticated = False
#         st.session_state.page = "None"
#         st.session_state.logged_user = None
#         st.session_state.current_user_id = None
#         st.rerun()
    
    

# # Render selected page
# if st.session_state.page == "Home":
#     home.render()

# elif st.session_state.page == "Dashboard":
#     dashboard.show_dashboard()

# elif st.session_state.page == "Account":
#     account.render()




# main.py

import streamlit as st
from app.core.config import APP_TITLE
from app.screens import home, dashboard, authentication, account

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

# Authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Current page
if "page" not in st.session_state:
    st.session_state.page = "None"

# Sidebar visibility
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = False


# --------------------------------------------------
# AUTHENTICATION ROUTING
# --------------------------------------------------

# If user is NOT authenticated → show login page only
if not st.session_state.authenticated:
    st.session_state.sidebar_visible = False
    authentication.render()
    st.stop()  # 🚨 Prevent rest of script from running


# --------------------------------------------------
# USER IS AUTHENTICATED
# --------------------------------------------------

st.session_state.sidebar_visible = True

# If user just logged in and page not set → default to Home
if st.session_state.page == "None":
    st.session_state.page = "Home"


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.info(
    "Use the refresh button to update the dashboard.\n"
    "⚠️ Do Not refresh using CTRL+R session will be lost!"
)

st.sidebar.title("Navigation")

if st.sidebar.button("Refresh", icon="🔄", key="refresh_button"):
    st.rerun()

if st.sidebar.button("Home", icon="🏠", key="home_button",width=200):
    st.session_state.page = "Home"

if st.sidebar.button("Dashboard", icon="📊", key="dashboard_button",width=200):
    st.session_state.page = "Dashboard"

if st.sidebar.button("Account", icon="👤", key="account_button",width=200):
    st.session_state.page = "Account"

if st.sidebar.button("Logout", icon="↩️", key="logout_button",width=200):
    st.session_state.authenticated = False
    st.session_state.page = "None"
    st.session_state.logged_user = None
    st.session_state.current_user_id = None
    st.rerun()


# --------------------------------------------------
# PAGE RENDERING
# --------------------------------------------------

if st.session_state.page == "Home":
    home.render()

elif st.session_state.page == "Dashboard":
    dashboard.show_dashboard()

elif st.session_state.page == "Account":
    account.render()
