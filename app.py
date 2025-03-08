# app.py
import streamlit as st
from utils.auth import handle_signup, handle_login, handle_password_reset
from supabase_client import supabase

# Custom CSS to hide sidebar
def load_css():
    hide_sidebar = """
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

load_css()

# Redirect to dashboard if already logged in
if "user" in st.session_state:
    st.switch_page("pages/dashboard.py")

# Auth UI (Full Screen)
st.title("Job Application Tracker 🔒")
tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password?"])

with tab1:  # Login
    with st.form("Login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            handle_login(email, password)

with tab2:  # Sign Up
    with st.form("Sign Up"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Create Account")
        if submitted:
            handle_signup(email, password)

with tab3:  # Password Reset
    with st.form("Reset Password"):
        email = st.text_input("Enter your email")
        submitted = st.form_submit_button("Send Reset Link")
        if submitted:
            handle_password_reset(email)