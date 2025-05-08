import streamlit as st
from authentication import auth
from authentication.pages import app

st.set_page_config(page_title="Sentiment Analysis Tool", layout="wide")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    app.run_sentiment_tool()
else:
    auth.user_auth_page()
