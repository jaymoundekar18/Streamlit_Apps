import pandas as pd
import streamlit as st
import plotly.express as px
from services.api_client import APIClient

def showanalytics():
    # st.json(APIClient.get_userBookData(st.session_state.current_user_id))
    user_BookData = APIClient.get_userBookData(st.session_state.current_user_id)
    st.markdown("---")

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
        total_pages = total_pages = df[df["book_status"] == "Completed"]["book_pages"].sum()
        new_rdf = df[df["rating"]!=0.0]
        avg_rating =  round(new_rdf["rating"].mean(), 2)
        total_hours = round(df["reading_hours"].sum(), 2)
        new_tdf = df[df["reading_hours"]!=0.0]
        avg_reading_time = round(new_tdf['reading_hours'].mean(),2)

        delta_value = ""
        delta_color = "off"

        if completed_books < 7:
            delta_value = "-"
            delta_color = "red" 
        elif 7 <= completed_books < 14:
            delta_value = "Low"
            delta_color = "yellow"  
        elif 14 <= completed_books < 25:
            delta_value = "Medium"
            delta_color = "blue"
        elif 25 <= completed_books :
            delta_value = "Completed"
            delta_color = "green"

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Books", total_books)
        col2.metric("Completed Books", completed_books)
        col3.metric("Total Pages Read", total_pages)
        col4.metric("Avg Rating ⭐", avg_rating)
        col1.metric("Total Reading Time (in Hours)",total_hours)
        col2.metric("Average Reading Time per Book (Hrs)",avg_reading_time)
        col3.metric("Yearly Goal (25)",value=completed_books, delta=delta_value, delta_color=delta_color)
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
