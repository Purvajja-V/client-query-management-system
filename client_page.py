# client_page.py
import streamlit as st
from db_utils import add_query

def client_query_page():
    st.header("📝 Submit New Query")
    # prefill email if logged in
    email = st.session_state.get("username", "")
    mail = st.text_input("Email ID", value=email)
    mobile = st.text_input("Mobile Number")
    heading = st.text_input("Query Heading")
    desc = st.text_area("Query Description")

    if st.button("Submit Query"):
        if not mail or not mobile or not heading or not desc:
            st.error("Fill all fields.")
        else:
            try:
                add_query(mail, mobile, heading, desc)
                st.success(" Query submitted successfully!")
            except Exception as e:
                st.error("Failed to submit query: " + str(e))

    if st.button("Logout"):
        for k in ("username", "role", "logged_in"):
            if k in st.session_state: del st.session_state[k]
        st.experimental_rerun = None  # safe no-op; main app reads session_state
