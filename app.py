import pickle
import streamlit as st
import numpy as np
import pandas as pd
import auth  # Import the auth module

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Display login or registration based on the user's choice
if not st.session_state['logged_in']:
    st.sidebar.title("Authentication")
    auth_option = st.sidebar.selectbox("Login/Register", ["Login", "Register"])
    if auth_option == "Login":
        auth.login()  # Show login form
    else:
        auth.register()  # Show registration form
else:
    # Display the main recommender system if logged in
    st.header("Books Recommender")
    st.success(f"Welcome, {st.session_state['username']}!")


    model = pickle.load(open("artifacts/model.pkl", "rb"))
    books_name = pickle.load(open("artifacts/books_name.pkl", "rb"))
    final_rating = pickle.load(open("artifacts/final_rating_table.pkl", "rb"))
    book_pivot = pickle.load(open("artifacts/pivot_table.pkl", "rb"))

    # def fetch_poster(suggestion):
    #     book_name = []
    #     ids_index = []
    #     poster_url = []

    #     for book_id in suggestion:
    #         book_name.append(book_pivot.index[book_id])
        
    #     for name in book_name:
    #         ids = np.where(final_rating['Title'] == name)[0][0]
    #         ids_index.append(ids)

    #     for idx in ids_index:
    #         url = final_rating.iloc[idx]['Image']
    #         poster_url.append(url)

    #     return poster_url

    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
        poster_url = []

        for book_id in suggestion:
            book_name.append(book_pivot.index[book_id])

        for name in book_name:
            # Check if the name exists in the 'Title' column
            if name in final_rating['Title'].values:
                ids = np.where(final_rating['Title'] == name)[0][0]
                ids_index.append(ids)
            else:
                st.warning(f"Book '{name}' not found in final_rating dataset")

        for idx in ids_index:
            url = final_rating.iloc[idx]['Image']
            if pd.isna(url) or not url.startswith("http"):
                # Handle missing or invalid URLs by adding a placeholder
                poster_url.append(None)  # Indicating no image available
            else:
                poster_url.append(url)

        return poster_url


    def reccommend_books(book_name):
        book_list = []
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=6)

        poster_url = fetch_poster(suggestion[0])

        for i in suggestion[0]:
            books = book_pivot.index[i]
            #for j in books:
            book_list.append(books)
        
        return book_list, poster_url



    selected_books = st.selectbox(
        "Type or Select a Book",
        books_name
    )

    # if st.button('Show Reccomendation'):
    #     recommendation_books, poster_url = reccommend_books(selected_books)
    #     col1,col2,col3,col4,col5 = st.columns(5)

    #     if len(recommendation_books) > 5 and len(poster_url) > 5:
    #         with col1:
    #             st.text(recommendation_books[1])
    #             st.image(poster_url[1])

    #         with col2:
    #             st.text(recommendation_books[2])
    #             st.image(poster_url[2])

    #         with col3:
    #             st.text(recommendation_books[3])
    #             st.image(poster_url[3])

    #         with col4:
    #             st.text(recommendation_books[4])
    #             st.image(poster_url[4])

    #         with col5:
    #             st.text(recommendation_books[5])
    #             st.image(poster_url[5])

    if st.button('Show Reccomendation'):
        recommendation_books, poster_url = reccommend_books(selected_books)
        col1, col2, col3, col4, col5 = st.columns(5)

        # Function to display book and image with fallback message
        def display_book(col, book, poster):
            with col:
                st.text(book)
                if poster:
                    st.image(poster)
                else:
                    st.text("Book image not available")

        # Display recommendations with fallback message
        display_book(col1, recommendation_books[1], poster_url[1])
        display_book(col2, recommendation_books[2], poster_url[2])
        display_book(col3, recommendation_books[3], poster_url[3])
        display_book(col4, recommendation_books[4], poster_url[4])
        display_book(col5, recommendation_books[5], poster_url[5])

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

