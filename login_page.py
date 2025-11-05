# login_page.py
import streamlit as st
from db_utils import register_user, authenticate_user, update_password, init_db

# Initialize DB and ensure support user exists (safe to call multiple times)
try:
    init_db()
except Exception as e:
    st.session_state.setdefault("_db_error", str(e))

def login_register_page():
    st.sidebar.title("Menu")
    choice = st.sidebar.selectbox("Login / Register", ["Login", "Register", "Forgot Password"])

    # show DB connection error if present
    if st.session_state.get("_db_error"):
        st.error("Database connection issue: " + st.session_state["_db_error"])
        st.stop()

    # ------------------- REGISTER -------------------
    if choice == "Register":
        st.subheader("Create Client Account")
        username = st.text_input("Email (username)")
        password = st.text_input("Password", type="password")
        role = "Client"  # registration restricted to clients only
        if st.button("Register"):
            if not username or not password:
                st.error("Enter both username and password.")
            else:
                created = register_user(username, password, role)
                if created:
                    st.success(" Account created — you can now login.")
                    st.rerun()   #  rerun to refresh immediately
                else:
                    st.error("Account already exists or role not allowed.")

    # ------------------- FORGOT PASSWORD -------------------
    elif choice == "Forgot Password":
        st.subheader("Reset Password")
        username = st.text_input("Enter your registered email")
        new_password = st.text_input("New password", type="password")
        if st.button("Reset Password"):
            if not username or not new_password:
                st.error("Enter both fields.")
            else:
                ok = update_password(username, new_password)
                if ok:
                    st.success("Password updated successfully. Please login.")
                    st.rerun()   #  refresh after password reset
                else:
                    st.error("User not found.")

    # ------------------- LOGIN -------------------
    else:
        st.subheader("Login")
        username = st.text_input("Email (username)")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Select Role", ["Client", "Support"])  #  Added dropdown

        if st.button("Login"):
            status, db_role = authenticate_user(username, password)
            if status == "invalid_user":
                st.error("Invalid Email")
            elif status == "wrong_password":
                st.error("Incorrect Password")
            else:
                if db_role != role:
                    st.error(f"Role mismatch! This user is registered as {db_role}.")
                else:
                    st.session_state['username'] = username
                    st.session_state['role'] = role
                    st.session_state['logged_in'] = True
                    st.success(f"Welcome {username}! Role: {role}")
                    st.rerun()   #  Fixes double-click issue — instantly refreshes
