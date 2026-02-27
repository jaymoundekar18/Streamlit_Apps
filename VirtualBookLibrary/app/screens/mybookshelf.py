import streamlit as st
from services.api_client import APIClient
from collections import defaultdict
from datetime import datetime
import random

def render():
    
    try:
        books = APIClient.get_userBookData(st.session_state.current_user_id)
        
    except Exception as e:
        st.error(f"Failed to fetch books: {str(e)}")
        return

    if not books:
        st.info("No books found in your library.")
        return
    
    completed_count = sum(1 for b in books if b.get("book_status") == "Completed")
    inprogress_count = sum(1 for b in books if b.get("book_status") == "In-progress")
    notstarted_count = sum(1 for b in books if b.get("book_status") == "Not Started")
    totalBooks = completed_count+inprogress_count+notstarted_count

    col1, col2 = st.columns(2)
    with col1:
        st.header("📚 My Library")
    with col2:
        sub_title1 , sub_title2 = st.columns(2)
        with sub_title1:
            st.markdown("##### Status")
        with sub_title2:
            st.markdown(f"Total Books : {totalBooks}")

        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            completed_check = st.checkbox(f"Completed ({completed_count})", value=True)
        with subcol2:
            inProgress_check = st.checkbox(f"In-Progress ({inprogress_count})", value=True)
        with subcol3:
            notStarted_check = st.checkbox(f"Not Started ({notstarted_count})", value=True)

    st.markdown("---")

    selected_statuses = {
        status for status, checked in {
            "Completed": completed_check,
            "In-progress": inProgress_check,
            "Not Started": notStarted_check,
        }.items()
        if checked
    }

    books = [
        book for book in books
        if book.get("book_status") in selected_statuses
    ]

    genre_dict = defaultdict(list)

    for book in books:
        genre = book.get("genre", "Unknown")
        genre_dict[genre].append(book)

    sorted_genres = sorted(genre_dict.keys())
    
    for genre in sorted_genres:
        books_in_genre = genre_dict[genre]

        st.markdown(f"## 📂 {genre}")

        bicon = ["📙", "📘", "📕", "📗"]

        for i in range(0, len(books_in_genre), 2):
            col1, col2 = st.columns(2)
            icon = random.sample(bicon, 2)

            # First column book
            with col1:
                book = books_in_genre[i]
                with st.expander(f"{icon[0]} {book.get('book_name')}"):
                    display_book_details(book)

            # Second column book (if exists)
            if i + 1 < len(books_in_genre):
                with col2:
                    book = books_in_genre[i + 1]
                    with st.expander(f"{icon[1]} {book.get('book_name')}"):
                        display_book_details(book)

            
        st.divider()
        st.divider()
                    

def display_book_details(book):
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Author:** {book.get('book_author')}")
        st.write(f"**Status:** {book.get('book_status')}")

        rating = book.get("rating", 0)
        stars = "⭐" * int(rating)
        st.write(f"**Rating:** {stars}")

        st.write(f"**Pages:** {book.get('book_pages')}")
    
    with col2:
        st.write(f"**Start Date:** {datetime.strptime(book.get('start_date'), '%Y-%m-%d').strftime('%d-%m-%Y')}")
        if book.get('end_date') is None:
            end_date = None
        else:
            end_date =  datetime.strptime(book.get('end_date'), '%Y-%m-%d').strftime('%d-%m-%Y')
        st.write(f"**End Date:** {end_date}")
        st.write(f"**Book Review:** {book.get('book_review')}")
