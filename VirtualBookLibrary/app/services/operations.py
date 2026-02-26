import streamlit as st
from services.api_client import APIClient
import json

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
        if "fullname" in result:
            return {"iscreated": True, "msg": f"User {result['fullname']}created successfully 🎉"}
        elif "error" in result:
            return {"iscreated": False, "msg": result["error"]}
        return False
    
    except Exception as e:
        print("Error creating user:", e)

def authenticate_user(username: str, password: str):
    response = APIClient.authenticate_user(username, password)
    print("Authentication response:", response)

    if "id" in response:
        # print("Authentication successful for user:", username)
        st.session_state.current_user_id = response.get("id")
        print("Current user ID set to:", st.session_state.current_user_id)
        return {"isvalid": True, "msg": "User credentials matched"}
    elif "error" in response:
        print(response)
        return {"isvalid": False, "msg": json.loads(response['error'])['detail']}

def check_user(username: str):
    try:
        response = APIClient.get_byusername(username)
        print("User check response:", response)
        if "username" in response:
            return {"isexist": True, "msg": "Username already exists. Please choose a different one."}
        elif "error" in response:
            return {"isexist": False, "msg": json.loads(response['error'])['detail']}
        # return False
    
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
        if "fullname" in result:
            return {"isupdated": True, "msg":"Account updated successfully ✅. \n\n Please refresh the page to see changes reflected in the dashboard."}
        elif "error" in result:
            return {"isupdated": False, "msg":result['error']}
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
        if "fullname" in result:
            return {"changed": True, "msg": "Password changed successfully ✅. \n\n Please refresh the page to see changes reflected in the dashboard."}
        elif "error" in result:
            return {"changed": False, "msg": result['error']}
        return False
    
    except Exception as e:
        print("Error updating password:", e)
        return False

def del_account(user_id: str):
    try:
        result = APIClient.delete_user_account(user_id)
        print("User deleted successfully from operations:", result)
        if "message" in result:
            return {"deleted": True, "msg": result["message"]}
        elif "error" in result:
            return {"deleted": False, "msg": result["error"]}
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
