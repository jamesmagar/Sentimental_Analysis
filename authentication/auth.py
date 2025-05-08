import streamlit as st
from pymongo import MongoClient

mongo_uri = "mongodb+srv://sentimental_analysis:sentimental_analysis_predction@cluster0.vxky4.mongodb.net/"
client = MongoClient(mongo_uri)

db = client["Sentimental_Analysis"]
collection = db["Prediction"]

def user_auth_page():
    st.title("User Management")

    option = st.radio("Select Option", ("Login", "Register"))

    if option == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user = collection.find_one({"username": username, "password": password})
            if user:
                st.session_state.authenticated = True
                st.success("Login successful! Please wait...")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    elif option == "Register":
        new_username = st.text_input("Choose Username", key="reg_username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if collection.find_one({"username": new_username}):
                st.error("Username already exists.")
            elif "@" not in new_email:
                st.error("Invalid email.")
            elif new_password != confirm_password:
                st.error("Passwords don't match.")
            else:
                collection.insert_one({
                    "username": new_username,
                    "password": new_password,
                    "email": new_email
                })
                st.success("Registered! You can now login.")
