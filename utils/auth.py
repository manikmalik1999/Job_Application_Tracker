from supabase_client import supabase
import streamlit as st

def handle_signup(email: str, password: str) -> None:
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        st.toast(f"Supabase response: {response}")  # Add this line
        if not response.user:
            st.error("Signup failed. Please try again.")
        else:
            st.success("Account created! Check your email for confirmation.")
    except Exception as e:
        st.error(f"Signup error: {e}")
        st.toast(f"Full error: {e}")  # Add this line

def handle_login(email: str, password: str) -> None:
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.toast(f"Login response: {response}")  # Add this line
        if response.user:
            st.session_state.user = response.user
            st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")
        st.toast(f"Full error: {e}")  # Add this line

def handle_password_reset(email: str) -> None:
    try:
        supabase.auth.reset_password_email(email)
        st.success("Password reset link sent to your email.")
    except Exception as e:
        st.error(f"Reset failed: {e}")