import streamlit as st
from pymongo import MongoClient

mongo_uri = "mongodb+srv://sentimental_analysis:sentimental_analysis_predction@cluster0.vxky4.mongodb.net/"
client = MongoClient(mongo_uri)

db = client["Sentimental_Analysis"]
collection = db["Prediction"]

# Sidebar for navigation
st.title("User Management System")
st.sidebar.title("SideBar")
page = st.sidebar.radio("Go to", ("Register", "Login"))

if page == "Login":
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        # Attempt to find the user in the database
        user = collection.find_one({"username": username, "password": password})
        if user:
            st.success("Logged in successfully!")
            # Save login state in Streamlit's session state
            st.session_state.authenticated = True
            st.switch_page("pages/app.py")
        else:
            st.error("Invalid username or password.")
               

elif page == "Register":
    st.title("Register")
    new_username = st.text_input("Choose a Username", key="reg_username")
    new_email = st.text_input("Choose a Email")
    new_password = st.text_input("Enter a Password", type="password")
    confirm_password = st.text_input("Enter a Password Again", type="password")
    
    if st.button("Register"):
        # Check if the username already exists
        if collection.find_one({"username": new_username}):
            st.error("Username already exists. Please choose another one.")
        else:
            # Insert the new user into the collection
            collection.insert_one({"username": new_username, "password": new_password})
            st.success("Registration successful! You can now login.")