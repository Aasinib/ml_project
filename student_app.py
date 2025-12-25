import streamlit as st
import numpy as np
import joblib
from auth import *
from database import init_db

init_db()   


st.set_page_config(page_title="Student Performance Prediction", layout="centered")

model = joblib.load("student_performance_model.pkl")


# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

st.title("🎓 Student Performance Prediction System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ---------- REGISTER ----------
if menu == "Register":
    st.subheader("📝 Register")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(u, p):
            st.success("Registration successful. Login now.")
        else:
            st.error("Username already exists")

# ---------- LOGIN ----------
if menu == "Login" and st.session_state.user is None:
    st.subheader("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        res = login_user(u, p)
        if res:
            st.session_state.user = u
            st.session_state.role = res[0]
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------- DASHBOARD ----------
if st.session_state.user:

    st.success(f"Logged in as {st.session_state.user} ({st.session_state.role})")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    # ===== USER DASHBOARD =====
    if st.session_state.role == "user":
        st.subheader("📊 Predict Student Performance")

        h = st.slider("Weekly Study Hours", 0.0, 40.0, 10.0)
        a = st.slider("Attendance %", 50.0, 100.0, 80.0)
        p = st.slider("Class Participation (0–10)", 0.0, 10.0, 5.0)

        if st.button("Predict Performance"):
            score = model.predict(np.array([[h, a, p]]))[0]
            save_prediction(st.session_state.user, h, a, p, score)
            st.success(f"Predicted Final Score: {score:.2f}")

        st.subheader("📜 Prediction History")
        hist = get_user_history(st.session_state.user)
        if hist:
            for r in hist:
                st.write(
                    f"🕒 {r[4]} | "
                    f"Hours: {r[0]} | Attendance: {r[1]} | "
                    f"Participation: {r[2]} | 🎯 Score: {r[3]:.2f}"
                )
        else:
            st.info("No predictions yet")

    # ===== ADMIN DASHBOARD =====
    if st.session_state.role == "admin":
        st.subheader("🧑‍💼 Admin Dashboard")

        users = get_all_users()

        for u, role in users:
            col1, col2, col3 = st.columns([3, 2, 2])
            col1.write(f"👤 {u} — {role}")

            if role == "user":
                if col2.button("Promote to Admin", key=f"p{u}"):
                    promote(u)
                    st.rerun()
            else:
                if col2.button("Demote to User", key=f"d{u}"):
                    demote(u)
                    st.rerun()

            if col3.button("Delete", key=f"x{u}"):
                if u != st.session_state.user:
                    delete_user(u)
                    st.rerun()

        st.subheader("📈 All Prediction History")
        preds = get_all_predictions()
        for p in preds:
            st.write(f"👤 {p[0]} | 🎯 {p[1]:.2f} | 🕒 {p[2]}")


