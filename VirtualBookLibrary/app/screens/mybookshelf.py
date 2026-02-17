import streamlit as st
from services.api_client import APIClient
from collections import defaultdict
from datetime import datetime
import random

def render():
    st.header("📚 My Library")
    st.markdown("---")

    try:
        books = APIClient.get_userBookData(st.session_state.current_user_id)
    except Exception as e:
        st.error(f"Failed to fetch books: {str(e)}")
        return

    if not books:
        st.info("No books found in your library.")
        return
    
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
