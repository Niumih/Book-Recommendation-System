# auth.py
import streamlit as st
import hashlib


# In-memory user database (for demonstration purposes)
user_db = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
}

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate login
def validate_login(username, password):
    if username in user_db and user_db[username] == hash_password(password):
        return True
    return False

# Function to register a new user
def register_user(username, password):
    if username in user_db:
        return "Username already taken."
    else:
        user_db[username] = hash_password(password)
        return "User registered successfully!"

# Function to display login form
def login():
    st.header("Books Recommender")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if validate_login(username, password):
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            return True
        else:
            st.error("Invalid username or password")
    return False

# Function to display registration form
def register():
    st.header("Books Recommender")
    st.subheader("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    if st.button("Register"):
        message = register_user(new_username, new_password)
        if "successfully" in message:
            st.success(message)
        else:
            st.warning(message)

