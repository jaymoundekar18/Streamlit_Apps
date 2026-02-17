import streamlit as st
from services.api_client import APIClient

def create_new_user(full_name: str, username: str, email: str, password: str):
    try:
        user_data = {
            "fullname": full_name,
            "username": username,
            "email": email, 
            "password": password,
            "books": list()  
            }
        result = APIClient.create_user(user_data)
        print("User created successfully from operations:", result)
        if result:
            return True
        return False
    
    except Exception as e:
        print("Error creating user:", e)

def authenticate_user(username: str, password: str):
    response = APIClient.authenticate_user(username, password)
    # print("Authentication response:", response)

    if "id" in response:
        # print("Authentication successful for user:", username)
        st.session_state.current_user_id = response.get("id")
        print("Current user ID set to:", st.session_state.current_user_id)
        return True
    else:        
        print("Authentication failed")
        return False

def check_user(username: str):
    try:
        response = APIClient.get_byusername(username)
        print("User check response:", response)
        if "username" in response:
            return True
        return False
    
    except Exception as e:
        print("Error checking user:", e)
        return False

def update_userAccount(user_id: str, full_name: str, username: str, email: str):
    # print("Updating user with ID:", user_id, "and data:", {"fullname": full_name, "username": username, "email": email})
    updated_data = {
        "fullname": full_name, 
        "username": username, 
        "email": email
        }
    try:
        result = APIClient.update_user(user_id, updated_data)
        print("User updated successfully from operations:", result)
        if result:
            return True
        return False
    
    except Exception as e:
        print("Error updating user:", e)
        return False

def update_userPassword(user_id: str, new_password: str):
    print("Updating password for user ID:", user_id)
    updated_data = {
        "password": new_password
        }
    try:
        result = APIClient.update_user(user_id, updated_data)
        print("Password updated successfully from operations:", result)
        if result:
            return True
        return False
    
    except Exception as e:
        print("Error updating password:", e)
        return False

def del_account(user_id: str):
    try:
        result = APIClient.delete_user_account(user_id)
        print("User deleted successfully from operations:", result)
        if "message" in result:
            return True
        return False
    
    except Exception as e:
        print("Error deleting user:", e)
        return False

def add_userBook(user_id:str, data:dict):
    try:
        result = APIClient.add_book(user_id,data)
        print("Book added successfully:", result)
        if "books" in result:
            return True
        return False
        
    except Exception as e:
        print("Error while adding book.", e)

def update_Book(user_id:str, bindex:int, data:dict):
    try:
        result = APIClient.update_userBookData(user_id,bindex,data)
        print("Book added successfully:", result)
        if "books" in result:
            return True
        return False
        
    except Exception as e:
        print("Error while adding book.", e)
