import pandas as pd
import streamlit as st
import plotly.express as px
from services.api_client import APIClient
from datetime import datetime


def showanalytics():
    # st.json(APIClient.get_userBookData(st.session_state.current_user_id))
    user_BookData = APIClient.get_userBookData(st.session_state.current_user_id)
    st.markdown("---")

    current_year = datetime.now().date().year

    yearly_goal =  st.session_state.user_details.get('yearly_goal')
    print(current_year, yearly_goal)

    goal = next((item['goal'] for item in yearly_goal if int(item['year']) - current_year == 0), 0)
    print("Goal:", goal)

    st.markdown("### 📚 Book Analytics Dashboard")

    if not user_BookData:
        st.info("No books found in your library")
        col1, col2, col3, col4 = st.columns(4)

        # ----------Analysis Section-------------
        col1.metric("Total Books", 0)
        col2.metric("Completed Books", 0)
        col3.metric("Total Pages Read", 0)
        col4.metric("Avg Rating ⭐", 0)
        col1.metric("Total Reading Time (in Hours)",0)
        col2.metric("Average Reading Time per Book (Hrs)",0)
        st.markdown("---")

    else:

        df = pd.DataFrame(user_BookData)

        # Convert dates
        df["start_date"] = pd.to_datetime(df["start_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])

        # Convert reading_time to hours
        df["reading_hours"] = pd.to_timedelta(df["reading_time"]).dt.total_seconds() / 3600

        # ----------Analysis Section-------------
        
        total_books = len(df)
        completed_books = len(df[df["book_status"] == "Completed"])
        inprogress_book = len(df[df["book_status"] == "In-progress"])
        total_pages = total_pages = df[df["book_status"] == "Completed"]["book_pages"].sum()
        new_rdf = df[df["rating"]!=0.0]
        # avg_rating =  round(new_rdf["rating"].mean(), 2)
        avg_rating = round(new_rdf["rating"].mean(), 2)
        avg_rating = 0 if pd.isna(avg_rating) else avg_rating

        total_hours = round(df["reading_hours"].sum(), 2)
        new_tdf = df[df["reading_hours"]!=0.0]
        # avg_reading_time = round(new_tdf['reading_hours'].mean(),2)
        avg_reading_time = round(new_tdf["reading_hours"].mean(), 2)
        avg_reading_time = 0.0 if pd.isna(avg_reading_time) else avg_reading_time


        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Reading Time (in Hours)",total_hours)
        col2.metric("Average Reading Time per Book (Hrs)",avg_reading_time)
        col3.metric("In Progress Books", inprogress_book)
        col4.metric("Total Pages Read", total_pages)

        col1.metric("Total Books", total_books)
        
        delta_value = ""
        delta_color = "off"

        if goal == 0:
            delta_value = "Set Goal"
            delta_color = "red" 
            completed_books = 0
        elif completed_books < goal*0.3:
            delta_value = "-"
            delta_color = "red" 
        elif goal*0.3 <= completed_books < goal*0.75:
            delta_value = "Low"
            delta_color = "yellow"  
        elif goal*0.75 <= completed_books < goal:
            delta_value = "Very Close"
            delta_color = "blue"
        elif goal <= completed_books :
            delta_value = "Goal Completed"
            delta_color = "green"
        col2.metric("Completed Books",value=completed_books, delta=delta_value, delta_color=delta_color)
        col3.metric(f"Yearly Goal ({current_year})",value=goal)
        col4.metric("Avg Rating ⭐", avg_rating)
        
        st.markdown("---")

        # Status Distribution
        status_count = df["book_status"].value_counts().reset_index()
        status_count.columns = ["book_status", "count"]

        fig_status = px.pie(
            status_count,
            names="book_status",
            values="count",
            color="book_status",
            color_discrete_map={
                "Completed": "green",
                "In-progress": "orange",
                "Not Started": "red"
            },
            title="Book Status Distribution"
        )

        st.plotly_chart(fig_status, use_container_width=True)

        # Genre Distribution
        genre_count = df["genre"].value_counts().reset_index()
        genre_count.columns = ["genre", "count"]

        fig_genre = px.bar(
            genre_count,
            x="genre",
            y="count",
            color="genre",
            title="Books by Genre"
        )

        st.plotly_chart(fig_genre, use_container_width=True)

        # Rating Distribution
        fig_rating = px.histogram(
            df,
            x="rating",
            nbins=5,
            title="Rating Distribution"
        )

        st.plotly_chart(fig_rating, use_container_width=True)

        # Pages vs Rating
        fig_scatter = px.scatter(
            df,
            x="book_pages",
            y="rating",
            color="genre",
            size="reading_hours",
            hover_data=["book_name"],
            title="Pages vs Rating (Bubble = Reading Time)"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        # Reading Timeline
        completed_df = df[df["book_status"] == "Completed"]

        timeline = completed_df.groupby(completed_df["end_date"].dt.to_period("M")).size().reset_index(name="count")
        timeline["end_date"] = timeline["end_date"].astype(str)

        fig_timeline = px.line(
            timeline,
            x="end_date",
            y="count",
            markers=True,
            title="Books Completed Per Month"
        )

        st.plotly_chart(fig_timeline, use_container_width=True)

        # Average Rating per Genre
        avg_rating_genre = (
            df.groupby("genre")["rating"]
            .mean()
            .reset_index()
            .sort_values(by="rating", ascending=False)
        )

        avg_rating_genre["rating"] = avg_rating_genre["rating"].round(2)

        fig_avg_rating = px.bar(
            avg_rating_genre,
            x="genre",
            y="rating",
            color="genre",
            text="rating",
            title="Average Rating per Genre"
        )

        fig_avg_rating.update_traces(textposition="outside")

        st.plotly_chart(fig_avg_rating, use_container_width=True)
