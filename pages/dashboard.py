# pages/dashboard.py
import streamlit as st
from utils.db_operations import link_coverletter_to_application,get_applications, add_application, update_application, delete_application, upload_resume, link_resume_to_application, delete_resume
import pandas as pd
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer


# Auth Check
if "user" not in st.session_state:
    st.switch_page("../app.py")

# Hide sidebar
def load_css():
    hide_sidebar = """
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

load_css()

# Main Dashboard UI
st.title("Your Job Applications Dashboard 📈")
st.write(f"Welcome, {st.session_state.user.email}!")

# Add New Application Form
with st.expander("➕ Add New Application", expanded=False):
    with st.form("add_form"):
        company = st.text_input("Company Name", key="company")
        role = st.text_input("Job Role", key="role")
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"], key="status")
        notes = st.text_area("Notes", key="notes")
        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")
        coverletter = st.file_uploader("Upload Cover Letter (PDF)", type=["pdf"], key="coverletter")
        submitted = st.form_submit_button("Save Application")
        if submitted:
            # Add application
            app_data = add_application(company, role, status, notes)
            app_id = app_data[0]["id"]  # Get the ID of the newly created application

            # Upload resume and link to application
            if resume:
                resume_url = upload_resume(resume, st.session_state.user.id)
                if resume_url:
                    link_resume_to_application(app_id, resume_url)
            if coverletter:
                coverletter_url = upload_resume(coverletter, st.session_state.user.id)
                if coverletter_url:
                    link_coverletter_to_application(app_id, coverletter_url)        
            st.success("Application added!")
            st.rerun()  # Refresh the page

# Application List
st.header("Your Applications")
applications = get_applications()
df = pd.DataFrame(applications)

# Search and Filter
col1, col2 = st.columns(2)
with col1:
    search_term = st.text_input("Search by Company/Role")
with col2:
    status_filter = st.selectbox("Filter by Status", ["All", "Applied", "Interview", "Offer", "Rejected"])

# Apply filters
if search_term:
    df = df[df["company"].str.contains(search_term, case=False) | df["role"].str.contains(search_term, case=False)]
if status_filter != "All":
    df = df[df["status"] == status_filter]

# Display as editable table
for _, row in df.iterrows():
    with st.expander(f"{row['company']} - {row['role']} ({row['status']})"):
        col1, col2 = st.columns([4, 1])
        with col1:
            new_status = st.selectbox(
                "Update Status",
                ["Applied", "Interview", "Offer", "Rejected"],
                index=["Applied", "Interview", "Offer", "Rejected"].index(row["status"]),
                key=f"status_{row['id']}"
            )
        with col2:
            if st.button("💾 Save", key=f"save_{row['id']}"):
                update_application(row["id"], new_status)
                st.rerun()
            if st.button("🗑️ Delete", key=f"delete_{row['id']}"):
                # Delete the resume from Supabase Storage (if it exists)
                if row["resume_url"]:
                    delete_resume(row["resume_url"])
                if row["cover_letter_url"]:
                    delete_resume(row["cover_letter_url"])
                # Delete the application from the database
                delete_application(row["id"])
                st.rerun()
        st.write(f"**Notes:** {row['notes']}")
        st.write(f"**Applied Date:** {row['applied_date']}")
        
        # View Resume Button
        if row["resume_url"]:
            if st.button(f"📄 View Resume for {row['company']}", key=f"view_resume_{row['id']}"):
                st.markdown(f"[Open Resume in New Tab]({row['resume_url']})", unsafe_allow_html=True)
                # Embed PDF using Google Docs Viewer
                google_docs_url = f"https://docs.google.com/viewer?url={row['resume_url']}&embedded=true"
                st.components.v1.iframe(google_docs_url, width=600, height=500)
        if row["cover_letter_url"]:
            if st.button(f"📄 View Cover Letter for {row['company']}", key=f"view_coverletter_{row['id']}"):
                st.markdown(f"[Open Cover Letter in New Tab]({row['cover_letter_url']})", unsafe_allow_html=True)
                # Embed PDF using Google Docs Viewer
                google_docs_url = f"https://docs.google.com/viewer?url={row['cover_letter_url']}&embedded=true"
                st.components.v1.iframe(google_docs_url, width=600, height=500)        

# Analytics Section
st.header("Analytics")
if not df.empty:
    fig = px.pie(df, names="status", title="Application Status Distribution")
    st.plotly_chart(fig)
else:
    st.info("No applications to display yet!")

# Logout Button
if st.button("Logout"):
    del st.session_state.user
    st.switch_page("app.py")