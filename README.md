# Job Application Tracker 🚀

A web app built with **Streamlit** and **Supabase** to track job applications, manage resumes/cover letters, and visualize application statuses.

---

## Features ✨

- **User Authentication**: Sign up, login, and password reset via Supabase.
- **CRUD Operations**: Add, view, update, and delete job applications.
- **Resume & Cover Letter Management**: Upload, view, and delete PDF files (stored in Supabase Storage).
- **Search & Filter**: Search by company/role and filter by application status (Applied, Interview, Offer, Rejected).
- **Analytics Dashboard**: Visualize application status distribution with interactive charts (Plotly).
- **Responsive Design**: Works on desktop and mobile.

---

## Tech Stack 💻

- **Frontend**: 
  - **Streamlit** (Python framework for web apps)
- **Backend**: 
  - **Supabase** (PostgreSQL database + Storage)
- **Libraries**:
  - `pandas` (data manipulation)
  - `plotly` (visualization)
  - `requests` (HTTP handling)
  - `python-dotenv` (environment variables)

---

## Installation 🛠️

### Prerequisites
- Python 3.10+
- [Supabase](https://supabase.com/) account
- Git

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/job-application-tracker.git
   cd job-application-tracker