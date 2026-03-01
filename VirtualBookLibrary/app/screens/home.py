import streamlit as st
from services.api_client import APIClient
from services import operations
from utils.helpers import is_valid_email
from analytics import reader
from datetime import datetime, date

def render():
    st.session_state.user_details = APIClient.get_user(st.session_state.current_user_id)

    streak = st.session_state.user_details.get('streak')['current_streak']
    print("user streak: ", streak )

    st.session_state.streak = st.session_state.user_details.get('streak')
    # streak_count = calculate_streak(streak)
    
    head_col1, head_col2 = st.columns([6, 1])

    with head_col1:
        st.markdown(f"## Welcome, 👤 {st.session_state.user_details.get('fullname').title()}!")
    with head_col2:
        st.metric(" ", f"{streak} ⚡", delta="days Streak")
        

    reader.showanalytics()


def calculate_streak(streak_data:dict):
    if not streak_data:
        return 0

    else:
        current_streak = streak_data['current_streak']
        longest_streak = streak_data['longest_streak']
        last_read_date = streak_data['last_read_date']
        
        # last_date = date.fromisoformat(streak_data['last_read_date'])
        last_date = (
                    date.fromisoformat(streak_data['last_read_date'])
                    if streak_data.get('last_read_date')
                    else None
                )
        today_date = datetime.now().date()

        if last_date is None:
            current_streak = 1
            longest_streak = 1
            last_read_date = str(today_date)
            operations.set_streak(st.session_state.current_user_id, current_streak,longest_streak,last_read_date)
            return 1

        else:

            difference = (today_date - last_date).days 

            if difference == 0:
                st.session_state.read_today_clicked = True
                st.info("You have already read today 🥳")
                return current_streak
            elif difference == 1:
                current_streak += 1
                longest_streak = current_streak
                last_read_date = str(today_date)
                st.success("You are maintaining the streak 🤩")
                operations.set_streak(st.session_state.current_user_id, current_streak,longest_streak,last_read_date)

                return current_streak
            elif difference > 1:
                st.error(f"Ohh no 🤦🏻‍♂️ \n Your streak is experired because your last read was on {date.fromisoformat(last_read_date).strftime('%d-%m-%Y')} ")
                current_streak = 1
                last_read_date = str(today_date)
                
                operations.set_streak(st.session_state.current_user_id, current_streak,longest_streak,last_read_date)

                return 1
            