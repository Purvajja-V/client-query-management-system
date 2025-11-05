
import streamlit as st
from login_page import login_register_page
from client_page import client_query_page
from support_page import support_dashboard

st.set_page_config("Client Query Management", layout="wide")
st.title("📩 Client Query Management System")

# Initialize session defaults
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Show login / register
if not st.session_state.get('logged_in'):
    login_register_page()
else:
    # role-aware redirect
    role = st.session_state.get('role')
    if role == "Client":
        client_query_page()
    elif role == "Support":
        support_dashboard()
    else:
        st.error("Unknown role. Please logout and login again.")
