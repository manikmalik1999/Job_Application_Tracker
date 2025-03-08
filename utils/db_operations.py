from supabase_client import supabase
import streamlit as st
from urllib.parse import quote  # For URL encoding
import urllib.parse
import time


def get_applications():
    user_id = st.session_state.user.id
    response = supabase.table('applications').select('*').eq('user_id', user_id).execute()
    return response.data

def add_application(company, role, status, notes):
    user_id = st.session_state.user.id
    response = supabase.table('applications').insert({
        "user_id": user_id,
        "company": company,
        "role": role,
        "status": status,
        "notes": notes
    }).execute()
    return response.data

def update_application(app_id, new_status):
    supabase.table('applications').update({"status": new_status}).eq('id', app_id).execute()

def delete_application(app_id):
    supabase.table('applications').delete().eq('id', app_id).execute()

def delete_resume(file_url):
    try:
        # Extract and decode the file path from the URL
        file_path_encoded = file_url.split("/object/public/resumes/")[1]
        file_path = urllib.parse.unquote(file_path_encoded)  # Decode %20 to spaces, etc.
        print(f"🗂️ Decoded file path: {file_path}")  # Debug

        # Delete the file from Supabase Storage
        response = supabase.storage.from_("resumes").remove([file_path])
        print(f"🗑️ Delete response: {response}")  # Debug

        # Check if the response indicates success
        if isinstance(response, list) and not any(item.get("error") for item in response):
            print("✅ Resume deleted successfully!")
            return True
        else:
            st.error(f"❌ Failed to delete resume: {response}")
            return False
    except Exception as e:
        st.error(f"❌ Delete resume error: {e}")
        return False


def upload_resume(file, user_id):
    try:
        # Add timestamp to filename to ensure uniqueness
        timestamp = int(time.time())
        unique_filename = f"{user_id}/{timestamp}_{file.name}"
        
        # Upload file to Supabase Storage
        supabase.storage.from_("resumes").upload(
            unique_filename, 
            file.getvalue(), 
            {"content-type": file.type}
        )
        
        public_url = supabase.storage.from_("resumes").get_public_url(unique_filename)
        normalized_url = public_url.replace(" ", "%20").rstrip("?")
        return normalized_url
    except Exception as e:
        st.error(f"Upload error: {e}")
        return None
def link_resume_to_application(app_id, resume_url):
    try:
        # Update application with resume URL
        print(resume_url)
        response = supabase.table('applications').update({"resume_url": resume_url}).eq('id', app_id).execute()
        if response.data:
            st.success("Resume URL linked to application!")
        else:
            st.error("Failed to link resume URL.")
    except Exception as e:
        st.error(f"Link error: {e}")

def link_coverletter_to_application(app_id, resume_url):
    try:
        # Update application with resume URL
        print(resume_url)
        response = supabase.table('applications').update({"cover_letter_url": resume_url}).eq('id', app_id).execute()
        if response.data:
            st.success("Cover Letter URL linked to application!")
        else:
            st.error("Failed to link resume URL.")
    except Exception as e:
        st.error(f"Link error: {e}")        
