import streamlit as st
from services import operations


def render():
    # Initialize state before widgets
    if "login_username" not in st.session_state:
        st.session_state.login_username = ""

    if "login_password" not in st.session_state:
        st.session_state.login_password = ""

    if "register_full_name" not in st.session_state:
        st.session_state.register_full_name = ""

    if "register_username" not in st.session_state:
        st.session_state.register_username = ""

    if "register_email" not in st.session_state:
        st.session_state.register_email = ""

    if "register_password" not in st.session_state:
        st.session_state.register_password = ""

    st.header("🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # Show login success message
    if st.session_state.get("login_success"):
        del st.session_state["login_success"]

    if st.session_state.get("register_success"):
        st.success("Registration successful! Please log in 🎉")
        del st.session_state["register_success"]


    # ------------------ LOGIN TAB ------------------ #
    with tab1:
        with st.form("login_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password",
                key="login_password"
            )

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                login_btn = st.form_submit_button("Login", use_container_width=True)

        if login_btn:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                if operations.authenticate_user(username, password):
                    st.toast(f"Logged in as {username} 🎉")
                    st.session_state.login_success = True
                    st.session_state.logged_user = username
                    st.session_state.authenticated = True

                    del st.session_state["login_username"]
                    del st.session_state["login_password"]

                    st.rerun()

                else:
                    st.error("Invalid username or password")

    # ------------------ REGISTRATION TAB ------------------ #
    with tab2:
        with st.form("register_form"):

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="register_full_name"
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="register_username"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="register_email"
            )

            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password",
                key="register_password"
            )

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                register_btn = st.form_submit_button("Register", use_container_width=True)

        if register_btn:
            if not full_name or not username or not email or not password:
                st.error("All fields are required")
            else:
                if operations.check_user(username):
                    st.error("Username already exists. Please choose a different one.")
                    return
                if operations.create_new_user(full_name, username, email, password):
                    st.success(f"User {username} created successfully 🎉")
                    st.session_state.register_success = True
                    # ✅ SAFE RESET
                    del st.session_state["register_full_name"]
                    del st.session_state["register_username"]
                    del st.session_state["register_email"]
                    del st.session_state["register_password"]

                    st.rerun()
                else:
                    st.error("Failed to create user. Please try again.")
