
import streamlit as st
from services.api_client import APIClient
from services import operations
from datetime import datetime

def render():
    st.markdown("---")
    st.header("📚 Update Books")

    if "edit_book" not in st.session_state:
        st.session_state.edit_book = False


    books_genre = ['---Select---','Action Fiction','Adventure Fiction','Alternate History','Autobiography','Biography',
                'Business','Contemporary Literature','Contemporary Romance','Crime Fiction','Detective Fiction','Essay',
                'Fairy Tale','Fantasy','Fantasy Fiction','Fiction','Finance','Genre Fiction','Graphic Novel','Historical Fantasy',
                'Historical Fiction','Historical Romance','History','Horror Fiction','Humor','Leadership','Literary Fiction',
                'Magical Realism','Memoir','Motivation','Mystery','Narrative','New Adult Fiction','Non-fiction','Novel','Paranormal Romance',
                'Philosophy','Poetry','Productivity','Psychology','Quotation','Romance','Romance Novel','Satire','Science','Science Fantasy',
                'Science Fiction','Self-Development','Self-Help','Self-Improvement','Self-help Book','Short Story','Social Science','Speculative Fiction',
                'Spirituality','Thriller','Travel Literature','True Crime','Western Fiction',"Women's Fiction",'Young Adult Literature']

    if "curr_book_name" not in st.session_state:
        st.session_state.curr_book_name = ""

    if "curr_book_author" not in st.session_state:
        st.session_state.curr_book_author = ""
    
    if "curr_book_genre" not in st.session_state:
        st.session_state.curr_book_genre = books_genre[0]

    if "curr_book_page" not in st.session_state:
        st.session_state.curr_book_page = 1

    if "curr_book_review" not in st.session_state:
        st.session_state.curr_book_review = ""

    if "curr_book_rating" not in st.session_state:
        st.session_state.curr_book_rating = float()


    try:
        booknames = APIClient.get_userBookNames(st.session_state.current_user_id)
        booknames.insert(0,"---Select---")
    except Exception as e:
        st.error(f"Failed to fetch books: {str(e)}")
        return

    if not booknames:
        st.info("No books found in your library")
    else:
        current_book_toEdit = st.selectbox("Select Book",booknames)

        bookIndex = booknames.index(current_book_toEdit) - 1

        if bookIndex != -1:
            st.session_state.curr_book_data = APIClient.get_userBookDataByIndex(user_id=st.session_state.current_user_id,bookIndex=bookIndex)
            print("-------------------------\n")
            print(st.session_state.curr_book_data)

               # ----------------- EDIT BUTTON ----------------- #
            col1, col2 = st.columns([9, 1])
            with col2:
                edit_clicked = st.button("✏️", help="Edit Book")
                if edit_clicked:
                    st.session_state.edit_book = True



            # ----------------- BOOK UPDATE FORM ----------------- #
            with st.form("update_book_form"):

                book_name = st.text_input("Book Name",  value=st.session_state.curr_book_data.get("book_name"), placeholder="Enter book name", disabled=not st.session_state.edit_book, key="curr_book_name")
                book_author = st.text_input("Book Author",  value=st.session_state.curr_book_data.get("book_author"), placeholder="Enter author name", disabled=not st.session_state.edit_book, key="curr_book_author")

                current_genre = st.session_state.curr_book_data.get("genre")
                genreindex = books_genre.index(current_genre) if current_genre in books_genre else 0
                
                genre = st.selectbox(
                    "Genre", books_genre,
                    index=genreindex,
                    disabled=not st.session_state.edit_book,
                    key="curr_book_genre"
                )

                st.markdown("##### ⏱ Reading Time (HH:MM:SS)")

                col1, col2, col3 = st.columns(3)
                try:
                    hh, mm, ss = map(int, st.session_state.curr_book_data.get("reading_time").split(":"))
                except:
                    hh, mm, ss = 0,0,0
                with col1:
                    hours = st.number_input("Hours", value=hh, disabled=not st.session_state.edit_book, min_value=0, step=1)

                with col2:
                    minutes = st.number_input("Minutes", value=mm, disabled=not st.session_state.edit_book, min_value=0, max_value=59, step=1)

                with col3:
                    seconds = st.number_input("Seconds", value=ss, disabled=not st.session_state.edit_book, min_value=0, max_value=59, step=1)

                book_pages = st.number_input("Number of Pages",  value=st.session_state.curr_book_data.get("book_pages"), disabled=not st.session_state.edit_book, min_value=1, step=1, key="curr_book_page")

                book_review = st.text_area("Book Review",  value=st.session_state.curr_book_data.get("book_review"), disabled=not st.session_state.edit_book, placeholder="Write your book review", key="curr_book_review")

                if st.session_state.curr_book_data.get("rating") is None:
                    defValue = 1.0
                else:
                    defValue = st.session_state.curr_book_data.get("rating")
                rating = st.number_input(
                    "Rating (1.0-5.0)",
                    value= defValue,
                    min_value=0.0,
                    max_value=5.0,
                    step=0.1,
                    format="%.1f",
                    disabled=not st.session_state.edit_book,
                    key="curr_book_rating"
                )

                options = ["Not Started","In-progress", "Completed"]
                optIndex = options.index(st.session_state.curr_book_data.get("book_status")) if st.session_state.curr_book_data.get("book_status") in options else 0
                book_status = st.selectbox(
                    "Book Status",
                    options,
                    index=optIndex,
                    disabled=not st.session_state.edit_book
                )  

                try:
                    start_date_value = (
                        datetime.fromisoformat(st.session_state.curr_book_data.get("start_date")).date()
                        if st.session_state.curr_book_data.get("start_date")
                        else None
                    )
                except:
                    start_date_value = None

                try:
                    end_date_value = (
                        datetime.fromisoformat(st.session_state.curr_book_data.get("end_date")).date()
                        if st.session_state.curr_book_data.get("end_date")
                        else None
                    )
                except:
                    end_date_value = None


                start_date = st.date_input("Start Date", value=start_date_value , disabled=not st.session_state.edit_book)
                end_date = st.date_input("End Date", value=end_date_value, disabled=not st.session_state.edit_book)


                submitted = st.form_submit_button("💾 Save Changes", disabled=not st.session_state.edit_book, type="primary")

                if submitted:
                    if not book_name or not book_author:
                        st.error("All the fields are required.")
                    elif genre == "---Select---":
                        st.error("Please select a genre.")
                    elif end_date and start_date and end_date < start_date:
                        st.error("End Date cannot be before Start Date.")
                    else:
                        reading_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

                        updated_book_data = {
                            "book_name": book_name,
                            "book_author": book_author,
                            "genre": genre,
                            "reading_time": reading_time,
                            "book_pages": book_pages,
                            "book_review": book_review,
                            "rating": float() if book_status=="In-progress" else rating,
                            "book_status": book_status,
                            "start_date": start_date.isoformat() if start_date else None,
                            "end_date": None if book_status=="In-progress" else end_date.isoformat()
                        }
                        # st.json(updated_book_data)
                        result = operations.update_Book(st.session_state.current_user_id,bookIndex,updated_book_data)
                        if result['updated']:
                            st.success(f"{result['msg']} : {book_name} \n\n Please refresh the page to see changes reflected in the dashboard. ")
                            del st.session_state["curr_book_name"]
                            del st.session_state["curr_book_author"]
                            del st.session_state["curr_book_genre"]
                            del st.session_state["curr_book_page"]   
                            del st.session_state["curr_book_review"]
                            del st.session_state["curr_book_rating"]
                            del st.session_state["curr_book_data"]
                            st.session_state.edit_book = False
                        else:
                            st.error(result['msg'])

        else:
            st.session_state.edit_book = False

         

