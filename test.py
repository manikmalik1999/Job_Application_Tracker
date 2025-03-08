
from supabase_client import supabase
import streamlit as st
from urllib.parse import quote  # For URL encoding



x = "https://kepuovpurzksejhpnvmi.supabase.co/storage/v1/object/public/resumes/2541b745-db58-4c75-a67b-dfddfa5fbc32/Demo%20Resume.pdf"
public_url = supabase.storage.from_("resumes").get_public_url("2541b745-db58-4c75-a67b-dfddfa5fbc32/Demo Resume.pdf")

print("Public_url = ",public_url)

normalized_url = public_url.replace(" ", "%20").rstrip("?")

print("url 2 = ", normalized_url)

if (x == normalized_url):
    print("yes")
else:
    print("no")
file_path = normalized_url.split("/object/public/resumes/")[1]
print("file path - ", file_path)
# supabase.storage.from_("resumes").remove([file_path])
# supabase.storage.from_('resumes').remove(['https://kepuovpurzksejhpnvmi.supabase.co/storage/v1/object/public/resumes/2541b745-db58-4c75-a67b-dfddfa5fbc32/Demo%20Resume.pdf'])
# supabase.storage.from_("resumes").upload(file_name, file_bytes, {"content-type": file.type})

# test_delete.py
from utils.db_operations import delete_resume

# Test resume URL
resume_url = "https://kepuovpurzksejhpnvmi.supabase.co/storage/v1/object/public/resumes/2541b745-db58-4c75-a67b-dfddfa5fbc32/Demo%20Resume.pdf"

# Delete the resume
success = supabase.storage.from_("resumes").remove(["xyz.pdf"])
print("Delete successful:", success)