import pandas as pd
import streamlit as st
import plotly.express as px
from services.api_client import APIClient

def showanalytics():
    # st.json(APIClient.get_userBookData(st.session_state.current_user_id))
    user_BookData = APIClient.get_userBookData(st.session_state.current_user_id)
    
    df = pd.DataFrame(user_BookData)

    # Convert dates
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    # Convert reading_time to hours
    df["reading_hours"] = pd.to_timedelta(df["reading_time"]).dt.total_seconds() / 3600

    st.title("📚 Book Analytics Dashboard")

    # -----------------------
    # 📊 KPI SECTION
    # -----------------------
    total_books = len(df)
    completed_books = len(df[df["book_status"] == "Completed"])
    total_pages = total_pages = df[df["book_status"] == "Completed"]["book_pages"].sum()
    avg_rating = round(df["rating"].mean(), 2)
    total_hours = round(df["reading_hours"].sum(), 2)
    avg_reading_time = round(df['reading_hours'].mean(),2)
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Books", total_books)
    col2.metric("Completed Books", completed_books)
    col3.metric("Total Pages Read", total_pages)
    col4.metric("Avg Rating ⭐", avg_rating)
    col1.metric("Total Reading Time (in Hours)",total_hours)
    col2.metric("Average Reading Time per Book (Hrs)",avg_reading_time)
    st.markdown("---")

    # -----------------------
    # 📌 1. Status Distribution
    # -----------------------
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

    # -----------------------
    # 📚 2. Genre Distribution
    # -----------------------
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

    # -----------------------
    # ⭐ 3. Rating Distribution
    # -----------------------
    fig_rating = px.histogram(
        df,
        x="rating",
        nbins=5,
        title="Rating Distribution"
    )

    st.plotly_chart(fig_rating, use_container_width=True)

    # -----------------------
    # 📈 4. Pages vs Rating
    # -----------------------
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

    # -----------------------
    # 📅 5. Reading Timeline
    # -----------------------
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

    # -----------------------
    # ⭐ Average Rating per Genre
    # -----------------------

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




# import pandas as pd
# import streamlit as st
# from services.api_client import APIClient

# def showanalytics():
#     user_BookData = APIClient.get_userBookData(st.session_state.current_user_id)
    
#     df = pd.DataFrame(user_BookData)

#     if df.empty:
#         st.warning("No book data available.")
#         return

#     # Convert dates
#     df["start_date"] = pd.to_datetime(df["start_date"])
#     df["end_date"] = pd.to_datetime(df["end_date"])

#     # Convert reading_time to hours
#     df["reading_hours"] = pd.to_timedelta(df["reading_time"]).dt.total_seconds() / 3600

#     st.title("📚 Book Analytics Dashboard")

#     # -----------------------
#     # 📊 KPI SECTION
#     # -----------------------
#     total_books = len(df)
#     completed_books = len(df[df["book_status"] == "Completed"])
#     total_pages = df[df["book_status"] == "Completed"]["book_pages"].sum()
#     avg_rating = round(df["rating"].mean(), 2)
#     total_hours = round(df["reading_hours"].sum(), 2)
#     avg_reading_time = round(df['reading_hours'].mean(), 2)

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Total Books", total_books)
#     col2.metric("Completed Books", completed_books)
#     col3.metric("Total Pages Read", total_pages)
#     col4.metric("Avg Rating ⭐", avg_rating)

#     col1.metric("Total Reading Time (Hrs)", total_hours)
#     col2.metric("Avg Reading Time per Book (Hrs)", avg_reading_time)

#     st.markdown("---")

#     # -----------------------
#     # 📌 1. Status Distribution
#     # -----------------------
#     st.subheader("📌 Book Status Distribution")
#     status_count = df["book_status"].value_counts()
#     st.bar_chart(status_count)

#     # -----------------------
#     # 📚 2. Genre Distribution
#     # -----------------------
#     st.subheader("📚 Books by Genre")
#     genre_count = df["genre"].value_counts()
#     st.bar_chart(genre_count)

#     # -----------------------
#     # ⭐ 3. Rating Distribution
#     # -----------------------
#     st.subheader("⭐ Rating Distribution")
#     rating_dist = df["rating"].value_counts().sort_index()
#     st.bar_chart(rating_dist)

#     # -----------------------
#     # 📈 4. Pages vs Rating
#     # -----------------------
#     st.subheader("📈 Pages vs Rating")

#     scatter_df = df[["book_pages", "rating"]]
#     scatter_df = scatter_df.rename(columns={
#         "book_pages": "Pages",
#         "rating": "Rating"
#     })

#     st.scatter_chart(scatter_df)

#     # -----------------------
#     # 📅 5. Books Completed Per Month
#     # -----------------------
#     st.subheader("📅 Books Completed Per Month")

#     completed_df = df[df["book_status"] == "Completed"]

#     timeline = (
#         completed_df
#         .groupby(completed_df["end_date"].dt.to_period("M"))
#         .size()
#     )

#     timeline.index = timeline.index.astype(str)
#     st.line_chart(timeline)

#     # -----------------------
#     # ⭐ Average Rating per Genre
#     # -----------------------
#     st.subheader("⭐ Average Rating per Genre")

#     avg_rating_genre = (
#         df.groupby("genre")["rating"]
#         .mean()
#         .round(2)
#         .sort_values(ascending=False)
#     )

#     st.bar_chart(avg_rating_genre)
