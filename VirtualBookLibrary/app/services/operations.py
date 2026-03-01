import streamlit as st
from services.api_client import APIClient
from datetime import datetime

def create_new_user(full_name: str, username: str, email: str, password: str):

    streak = {
    "current_streak": 0,
    "longest_streak": 0,
    "last_read_date": None
   }
    
    user_data = {
        "fullname": full_name,
        "username": username,
        "email": email, 
        "password": password,
        "books": list(),
        "yearly_goal": list(), 
        "streak": streak
        }
    result = APIClient.create_user(user_data)
    print("User created successfully from operations:", result)
    if "fullname" in result:
        return {"iscreated": True, "msg": f"User {result['fullname']}created successfully 🎉"}
    elif "error" in result:
        return {"iscreated": False, "msg": result["error"]}
    return False
    

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
        return {"isvalid": False, "msg": response['error']}

def check_user(username: str):
    
    response = APIClient.get_byusername(username)
    print("User check response:", response)
    if "username" in response:
        return {"isexist": True, "msg": "Username already exists. Please choose a different one."}
    elif "error" in response:
        return {"isexist": False, "msg": "Username available"}
    return {
        "isexist": False,
        "msg": "Username available"
    }
    
    

def update_userAccount(user_id: str, full_name: str, username: str, email: str):
    # print("Updating user with ID:", user_id, "and data:", {"fullname": full_name, "username": username, "email": email})
    updated_data = {
        "fullname": full_name, 
        "username": username, 
        "email": email
        }
    
    result = APIClient.update_user(user_id, updated_data)
    print("User updated successfully from operations:", result)
    if "fullname" in result:
        return {"isupdated": True, "msg":"Account updated successfully ✅. \n\n Please refresh the page to see changes reflected in the dashboard."}
    elif "error" in result:
        return {"isupdated": False, "msg":result['error']}
    return {"isupdated": False, "msg":"Error"}
    

def update_userPassword(user_id: str, new_password: str):
    print("Updating password for user ID:", user_id)
    updated_data = {
        "password": new_password
        }
    
    result = APIClient.update_user(user_id, updated_data)
    print("Password updated successfully from operations:", result)
    if "fullname" in result:
        return {"changed": True, "msg": "Password changed successfully ✅. \n\n Please refresh the page to see changes reflected in the dashboard."}
    elif "error" in result:
        return {"changed": False, "msg": result['error']}
    return {"changed": False, "msg": "Unable to update password at the moment."}


def del_account(user_id: str):
    
    result = APIClient.delete_user_account(user_id)
    print("User deleted successfully from operations:", result)
    if "message" in result:
        return {"deleted": True, "msg": result["message"]}
    elif "error" in result:
        return {"deleted": False, "msg": result["error"]}
    return {"deleted": False, "msg": "Unable to delete account at the moment."}
    
def add_userBook(user_id:str, data:dict):
    
    result = APIClient.add_book(user_id,data)
    print("Book added successfully:", result)
    if "books" in result:
        return {"added": True, "msg": "Book added successfully."}
    elif "error" in result:
        return {"added": False, "msg": result["error"]}
    return {"added": False, "msg": "Unable to add book at the moment."}
        
    

def update_Book(user_id:str, bindex:int, data:dict):
    
    result = APIClient.update_userBookData(user_id,bindex,data)
    print("Book updated successfully:", result)
    if "books" in result:
        return {"updated": True, "msg": "Book updated successfully"}
    elif "error" in result:
        return {"updated": False, "msg": result["error"]}
    return {"updated": False, "msg": "Unable to update book at the moment."}
     

def add_goal(user_id:str, year:str, goal:int):
    data = {
        "year": year,
        "goal": goal,
        "completed": 0
        } 
    result = APIClient.add_user_goals(user_id,data)
    print("Goal added successfully:", result)
    if "fullname" in result:
        return {"added": True, "msg": "Goal added successfully."}
    elif "error" in result:
        return {"added": False, "msg": result["error"]}
    return {"added": False, "msg": "Unable to add goal at the moment."}

def update_goal(user_id:str, gyear: str, gindex:int, goal:int, completed:int):
    data = {
        "year": gyear,
        "goal": goal,
        "completed": completed
        }
    
    result = APIClient.update_user_goal(user_id=user_id, goalIndex=gindex, goal_data=data)

    if "fullname" in result:
        return {"updated": True, "msg": "Goal updated successfully"}
    elif "error" in result:
        return {"updated": False, "msg": result["error"]}
    return {"updated": False, "msg": "Unable to update goal at the moment."}


def set_streak(user_id:str, current_streak:int,longest_streak:int,last_read_date:str):
    data = {
            "streak":{
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                    "last_read_date": last_read_date
                    }
            }
    
    result = APIClient.update_user(user_id=user_id, data=data)
    if "fullname" in result:
        return {"isupdated": True, "msg":"Streak updated successfully"}
    elif "error" in result:
        return {"isupdated": False, "msg":result['error']}
    return {"isupdated": False, "msg":"Error"}