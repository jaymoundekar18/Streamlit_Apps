import streamlit as st
from services.api_client import APIClient

def render():
    st.header("📊 User Dashboard")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        users = APIClient.get_users()
    except Exception as e:
        st.error(str(e))
        return

    if not users:
        st.info("No users found")
        return

    for user in users:
        with st.expander(f"User ID {user['id']}"):
            name = st.text_input(
                "Name",
                user["name"],
                key=f"name_{user['id']}"
            )
            email = st.text_input(
                "Email",
                user["email"],
                key=f"email_{user['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update", key=f"update_{user['id']}"):
                    try:
                        APIClient.update_user(
                            user["id"],
                            {"name": name, "email": email}
                        )
                        st.success("Updated successfully")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

def show_dashboard(): 
    st.header("Dashboard")
