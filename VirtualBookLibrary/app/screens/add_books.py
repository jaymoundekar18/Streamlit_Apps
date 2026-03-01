import streamlit as st
from datetime import date
from services import operations, api_client

def render():
    st.markdown("---")
    st.header("📚 Add Books")
    books_genre = ['---Select---','Action Fiction','Adventure Fiction','Alternate History','Autobiography','Biography',
                'Business','Contemporary Literature','Contemporary Romance','Crime Fiction','Detective Fiction','Essay',
                'Fairy Tale','Fantasy','Fantasy Fiction','Fiction','Finance','Genre Fiction','Graphic Novel','Historical Fantasy',
                'Historical Fiction','Historical Romance','History','Horror Fiction','Humor','Leadership','Literary Fiction',
                'Magical Realism','Memoir','Motivation','Mystery','Narrative','New Adult Fiction','Non-fiction','Novel','Paranormal Romance',
                'Philosophy','Poetry','Productivity','Psychology','Quotation','Romance','Romance Novel','Satire','Science','Science Fantasy',
                'Science Fiction','Self-Development','Self-Help','Self-Improvement','Self-help Book','Short Story','Social Science','Speculative Fiction',
                'Spirituality','Thriller','Travel Literature','True Crime','Western Fiction',"Women's Fiction",'Young Adult Literature']


    if "book_name" not in st.session_state:
        st.session_state.book_name = ""

    if "book_author" not in st.session_state:
        st.session_state.book_author = ""

    if "book_page" not in st.session_state:
        st.session_state.book_page = 1
        
    if "book_genre" not in st.session_state:
        st.session_state.book_genre = books_genre[0]
        
    if "obook_name" not in st.session_state:
        st.session_state.obook_name = ""

    if "obook_author" not in st.session_state:
        st.session_state.obook_author = ""
    
    if "obook_genre" not in st.session_state:
        st.session_state.obook_genre = books_genre[0]

    if "obook_page" not in st.session_state:
        st.session_state.obook_page = 1

    if "obook_review" not in st.session_state:
        st.session_state.obook_review = ""

    if "obook_rating" not in st.session_state:
        st.session_state.obook_rating = float()
    if "show_add_goal_form" not in st.session_state:
        st.session_state.show_add_goal_form = False

    tab1, tab2, tab3 = st.tabs(["Add New Book", "Add Old Book", "Your Goals"])

    # -------------------- ADD NEW BOOK --------------------
    with tab1:
        with st.form("add_new_book_form"):

            book_name = st.text_input("Book Name", placeholder="Enter book name", key="book_name")
            book_author = st.text_input("Book Author", placeholder="Enter author name", key="book_author")

            genre = st.selectbox(
                "Genre",books_genre,
                key="book_genre"
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
                        "book_review":None,
                        "book_status": book_status,
                        "start_date": start_date.isoformat(),
                        "end_date": None
                    }
                    # st.json(new_book_data)
                    if operations.add_userBook(st.session_state.current_user_id,new_book_data):
                        st.success("Book added successfully.\n\n Please refresh the page to see changes reflected in the dashboard.")

                        del st.session_state["book_name"]
                        del st.session_state["book_author"]
                        del st.session_state["book_page"]
                        del st.session_state["book_genre"]

                    else:
                        st.error("Unable to add book right now.")
            

    # -------------------- ADD OLD BOOK --------------------
    with tab2:
        with st.form("add_old_book_form"):

            book_name = st.text_input("Book Name", placeholder="Enter book name", key="obook_name")
            book_author = st.text_input("Book Author", placeholder="Enter author name", key="obook_author")

            genre = st.selectbox(
                "Genre", books_genre,
                key="obook_genre"
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
                    # st.json(old_book_data)
                    result = operations.add_userBook(st.session_state.current_user_id,old_book_data)
                    if result['added']:
                        st.success(f"{result['msg']}\n\n Please refresh the page to see changes reflected in the dashboard.")
                        del st.session_state["obook_name"]
                        del st.session_state["obook_author"]
                        del st.session_state["obook_genre"]
                        del st.session_state["obook_page"]   
                        del st.session_state["obook_review"]
                        del st.session_state["obook_rating"]

                    else:
                        st.error(result['msg'])

    with tab3:
        
        goals_list = api_client.APIClient.get_user_goals(st.session_state.current_user_id)
        #print(goals_list)
        
        goals_list_new = sorted(goals_list, key=lambda x: int(x['year']), reverse=True)

        title_cols1, title_cols2 =  st.columns([6, 1])
        with title_cols1:
            st.markdown("### 🎯 Your Reading Goals")
        with title_cols2:
            if st.button("➕ Add Goal", type="primary"):
                st.session_state.show_add_goal_form = True

        st.markdown("---")

        header_cols = st.columns([1, 1, 1, 0.6])
        header_cols[0].markdown("**Year**")
        header_cols[1].markdown("**Goal**")
        header_cols[2].markdown("**Completed**")
        header_cols[3].markdown("**Edit**")

        for goal in goals_list_new:
            row_cols = st.columns([1, 1, 1, 0.6])

            row_cols[0].subheader(goal['year'])
            row_cols[1].badge(label=f"{goal['goal']}",color="green")
            row_cols[2].markdown(f":violet-badge[{goal['completed']}]")

            if row_cols[3].button("✏️", key=f"edit_{goal['year']}"):
                st.session_state.edit_goal_id = goal['year']
                st.session_state.edit_goal_value = goal['goal']
                st.session_state.goal_completed_values = goal['completed'] 
                st.rerun()


        if st.session_state.show_add_goal_form:
            st.markdown("---")
            st.markdown("### 🎯 Add New Reading Goal")

            with st.form("add_goal_form"):
                goal_year = st.number_input(
                    "Year",
                    min_value=2000,
                    max_value=2100,
                    step=1
                )

                goal_value = st.number_input(
                    "Goal (Number of Books)",
                    min_value=1,
                    step=1
                )

                sub_btn_col1,sub_btn_col2 = st.columns(2)
                with sub_btn_col1:
                    submitted = st.form_submit_button("Add Goal")

                    if submitted:
                        result = operations.add_goal(
                            st.session_state.current_user_id,
                            str(goal_year),
                            goal_value
                        )

                        if result["added"]:
                            st.success(result["msg"])
                            st.session_state.show_add_goal_form = False
                            st.rerun()
                        else:
                            st.error(result["msg"])

                with sub_btn_col2:
                    cancel = st.form_submit_button("Cancel")

                    if cancel:
                        st.session_state.show_add_goal_form = False
                        st.rerun()


        if "edit_goal_id" in st.session_state:
            st.markdown("---")
            st.markdown(f"### ✏️ Edit {st.session_state.edit_goal_id} Goal")

            index = next((i for i, d in enumerate(goals_list) if d['year'] == st.session_state.edit_goal_id), None)

            with st.form("edit_goal_form"):
                new_goal = st.number_input(
                    "Goal",
                    value=st.session_state.edit_goal_value
                )

                submitted = st.form_submit_button("Update Goal")

                if submitted:
                    result = operations.update_goal(
                        st.session_state.current_user_id,
                        st.session_state.edit_goal_id,
                        index,
                        new_goal,
                        st.session_state.goal_completed_values
                    )

                    if result['updated']:
                        st.success("Goal updated successfully!")
                        del st.session_state.edit_goal_id
                        st.rerun()
                    else:
                        st.error("Failed to update goal.")
        
    
