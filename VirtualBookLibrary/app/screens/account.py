import streamlit as st
from services import operations

def render():
    # Persist current page
    st.session_state.page = "Account"

    st.header("👤 Account Details")

    # ----------------- INITIALIZE STATE ----------------- #
    if "edit_profile" not in st.session_state:
        st.session_state.edit_profile = False

    if "edit_password" not in st.session_state:
        st.session_state.edit_password = False

    if "account_name" not in st.session_state:
        # Fetch user details once
        user = st.session_state.user_details
        st.session_state.account_name = user.get("fullname")
        st.session_state.account_username = user.get("username")
        st.session_state.account_email = user.get("email")

    # ----------------- EDIT BUTTON ----------------- #
    col1, col2 = st.columns([9, 1])
    with col2:
        edit_clicked = st.button("✏️", help="Edit profile")
        if edit_clicked:
            st.session_state.edit_profile = True

    # ----------------- ACCOUNT INFO FORM ----------------- #
    with st.form("account_form"):
        name = st.text_input(
            "Full Name",
            value=st.session_state.account_name,
            disabled=not st.session_state.edit_profile,
            key="account_name_input"
        )

        username = st.text_input(
            "Username",
            value=st.session_state.account_username,
            disabled=not st.session_state.edit_profile,
            key="account_username_input"
        )

        email = st.text_input(
            "Email",
            value=st.session_state.account_email,
            disabled=not st.session_state.edit_profile,
            key="account_email_input"
        )

        save_btn = st.form_submit_button("💾 Save Changes")

        if save_btn:
            if not name or not username or not email:
                st.error("All fields are required")
            else:
                try:
                    # Call API to update user
                    result = operations.update_userAccount(st.session_state.current_user_id, name, username, email)
                    if result['isupdated']:
                        # Update session state
                        st.session_state.account_name = name
                        st.session_state.account_username = username
                        st.session_state.account_email = email

                        st.session_state.edit_profile = False
                        st.success(result['msg'])
                        
                    else:
                        st.error(f"Failed to update account. {result['msg']}")
                except Exception as e:
                    st.error(f"Failed to update account: {str(e)}")


    # ----------------- EDIT BUTTON ----------------- #
    col1, col2 = st.columns([9, 1])
    with col2:
        edit_pwclicked = st.button("✏️", help="Edit Password")
        if edit_pwclicked:
            st.session_state.edit_password = True

    # ----------------- PASSWORD CHANGE FORM ----------------- #
    with st.form("password_form"):
        
        password = st.text_input(
                "Change Password",
                disabled=not st.session_state.edit_password,
                placeholder="Enter your new password",
                type="password",
                key="login_password",
                width=350
            )
        save_pwbtn = st.form_submit_button("💾 Save")
        if save_pwbtn:
            if not password or password.isspace():
                st.error("Password is required")
            else:
                try:
                    # Call API to update user
                    result = operations.update_userPassword(st.session_state.current_user_id, password)
                    if result['changed']:
                        
                        st.session_state.edit_password = False
                        st.success(result['msg'])
                        password = ""
                    else:
                        st.error(f"Failed to update password. {result['msg']}")
                except Exception as e:
                    st.error(f"Failed to update password: {str(e)}")
                    
    # Initialize confirm state
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False


    col11, col12 = st.columns([2, 1])
    with col12:
        if st.button(
            "Delete Account",
            width=300,
            type="primary",
            help="This will permanently delete your account and all associated data. Use with caution!"
        ):
            st.session_state.confirm_delete = True

        if st.session_state.confirm_delete:
            st.warning("Are you sure you want to delete your account?")

            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("Yes, Delete", type="primary"):
                    result = operations.del_account(st.session_state.current_user_id)
                    if result["deleted"]:
                        st.success(result["msg"])

                        st.session_state.confirm_delete = False
                        st.session_state.authenticated = False
                        st.session_state.page = "None"
                        st.session_state.logged_user = None
                        st.session_state.current_user_id = None

                        st.rerun()
                    else:
                        st.error(f"Failed to delete account. {result['msg']}")

            with col_no:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False
   
