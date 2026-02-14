
import streamlit as st
from datetime import date
from services import operations

def render():
    st.header("📚 Add Books")
    books_genre = ['---Select---',
                 'Action Fiction', 'Adventure Fiction', 'Alternate History', 'Autobiography', 'Biography', 
                 'Contemporary Literature', 'Contemporary Romance', 'Crime Fiction', 'Detective Fiction', 'Essay',
                 'Fairy Tale', 'Fantasy', 'Fantasy Fiction', 'Fiction', 'Genre Fiction', 'Graphic Novel', 
                 'Historical Fantasy', 'Historical Fiction', 'Historical Romance', 'History',
                 'Horror Fiction', 'Humor', 'Literary Fiction', 'Magical Realism', 'Memoir', 'Mystery', 'Narrative', 
                 'New Adult Fiction', 'Non-fiction', 'Novel', 'Paranormal Romance', 'Philosophy', 'Poetry', 'Quotation', 
                 'Romance', 'Romance Novel', 'Satire', 'Science', 'Science Fantasy', 'Science Fiction',
                 'Self-help Book', 'Short Story', 'Social Science', 'Speculative Fiction', 'Spirituality', 'Thriller', 
                 'Travel Literature', 'True Crime', 'Western Fiction', "Women's Fiction", 'Young Adult Literature'
                ]


    if "book_name" not in st.session_state:
        st.session_state.book_name = ""

    if "book_author" not in st.session_state:
        st.session_state.book_author = ""

    if "book_page" not in st.session_state:
        st.session_state.book_page = 1

    if "obook_name" not in st.session_state:
        st.session_state.obook_name = ""

    if "obook_author" not in st.session_state:
        st.session_state.obook_author = ""

    if "obook_page" not in st.session_state:
        st.session_state.obook_page = 1

    if "obook_review" not in st.session_state:
        st.session_state.obook_review = ""

    if "obook_rating" not in st.session_state:
        st.session_state.obook_rating = float()

    tab1, tab2 = st.tabs(["Add New Book", "Add Old Book"])

    # -------------------- ADD NEW BOOK --------------------
    with tab1:
        with st.form("add_new_book_form"):

            book_name = st.text_input("Book Name", placeholder="Enter book name", key="book_name")
            book_author = st.text_input("Book Author", placeholder="Enter author name", key="book_author")

            genre = st.selectbox(
                "Genre",books_genre
            )

            book_pages = st.number_input("Number of Pages", min_value=1, step=1, key="book_page")

            book_status = st.selectbox("Book Status", ["Not Started"])

            # Start date defaults to today
            start_date = date.today()

            submitted = st.form_submit_button("➕ Add Book", type="primary")

            if submitted:
                if not book_name or not book_author:
                    st.error("All the fields are required.")
                elif genre == "---Select---":
                    st.error("Please select a genre.")
                else:
                    new_book_data = {
                        "book_name": book_name,
                        "book_author": book_author,
                        "genre": genre,
                        "reading_time": "00:00:00",
                        "book_pages": book_pages,
                        "rating": float(),
                        "book_review":"",
                        "book_status": book_status,
                        "start_date": start_date.isoformat(),
                        "end_date": ""
                    }
                    st.json(new_book_data)
                    if operations.add_userBook(st.session_state.current_user_id,new_book_data):
                        st.success("Book added successfully.")

                        del st.session_state["book_name"]
                        del st.session_state["book_author"]
                        del st.session_state["book_page"]

                    else:
                        st.error("Unable to add book right now.")
            

    # -------------------- ADD OLD BOOK --------------------
    with tab2:
        with st.form("add_old_book_form"):

            book_name = st.text_input("Book Name", placeholder="Enter book name", key="obook_name")
            book_author = st.text_input("Book Author", placeholder="Enter author name", key="obook_author")

            genre = st.selectbox(
                "Genre", books_genre
            )

            st.markdown("##### ⏱ Reading Time (HH:MM:SS)")

            col1, col2, col3 = st.columns(3)

            with col1:
                hours = st.number_input("Hours", min_value=0, step=1)

            with col2:
                minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1)

            with col3:
                seconds = st.number_input("Seconds", min_value=0, max_value=59, step=1)

            book_pages = st.number_input("Number of Pages", min_value=1, step=1, key="obook_page")

            book_review = st.text_area("Book Review", placeholder="Write your book review", key="obook_review")

            rating = st.number_input(
                "Rating (1.0-5.0)",
                min_value=1.0,
                max_value=5.0,
                step=0.1,
                format="%.1f",
                key="obook_rating"
            )

            book_status = st.selectbox(
                "Book Status",
                ["In-progress", "Completed"]
            )

            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")


            submitted = st.form_submit_button("➕ Add Book", type="primary")

            if submitted:
                if not book_name or not book_author:
                    st.error("All the fields are required.")
                elif genre == "---Select---":
                    st.error("Please select a genre.")
                elif end_date and start_date and end_date < start_date:
                    st.error("End Date cannot be before Start Date.")
                else:
                    reading_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

                    st.success("Book added successfully ✅")

                    old_book_data = {
                        "book_name": book_name,
                        "book_author": book_author,
                        "genre": genre,
                        "reading_time": reading_time,
                        "book_pages": book_pages,
                        "book_review": book_review,
                        "rating": float() if book_status=="In-progress" else rating,
                        "book_status": book_status,
                        "start_date": start_date.isoformat() if start_date else None,
                        "end_date": "" if book_status=="In-progress" else end_date.isoformat()
                    }
                    st.json(old_book_data)
                    if operations.add_userBook(st.session_state.current_user_id,old_book_data):
                        st.success("Book added successfully.")
                        del st.session_state["obook_name"]
                        del st.session_state["obook_author"]
                        del st.session_state["obook_page"]   
                        del st.session_state["obook_review"]
                        del st.session_state["obook_rating"]

                    else:
                        st.error("Unable to add book right now.")
    