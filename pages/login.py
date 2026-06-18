import streamlit as st
import os
import sys

# ── Make sure database.py can be found ───────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "models"))

from database import init_db, register_farmer, login_farmer

# ── Always initialise the database when this page loads ──────────────────────
init_db()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# ── If already logged in, show welcome message ────────────────────────────────
if "farmer" in st.session_state and st.session_state.farmer:
    farmer = st.session_state.farmer
    st.success(f"✅ You are logged in as **{farmer['name']}**")
    st.info("👈 Use the sidebar to go to Soil Analysis, Pest Risk, or Crop Health.")
    if st.button("🚪 Log Out", type="secondary"):
        st.session_state.farmer = None
        st.rerun()
    st.stop()

# ── Page title ────────────────────────────────────────────────────────────────
st.title("🔐 Farmer Portal")
st.markdown("Login or create an account to access the AI tools.")
st.divider()

# ── Tab switcher: Login vs Register ──────────────────────────────────────────
tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

with tab_login:
    st.subheader("Welcome Back!")
    st.markdown("Enter your email and password to continue.")

    email    = st.text_input("Email Address", placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Your password", key="login_pass")

    if st.button("🔑 Login", use_container_width=True, type="primary"):
        if not email or not password:
            st.error("Please fill in both email and password.")
        else:
            farmer = login_farmer(email, password)
            if farmer:
                st.session_state.farmer = farmer
                st.success(f"✅ Welcome back, **{farmer['name']}**!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Wrong email or password. Please try again.")

with tab_register:
    st.subheader("Create Your Account")
    st.markdown("Fill in the details below to get started.")

    col1, col2 = st.columns(2)
    with col1:
        reg_name   = st.text_input("Full Name",     placeholder="e.g. Ravi Kumar",       key="reg_name")
        reg_email  = st.text_input("Email Address", placeholder="you@example.com",        key="reg_email")
    with col2:
        reg_mobile = st.text_input("Mobile Number", placeholder="e.g. 9876543210",        key="reg_mobile")
        reg_pass   = st.text_input("Password",      type="password", placeholder="Min 6 characters", key="reg_pass")

    reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", key="reg_pass2")

    if st.button("📝 Create Account", use_container_width=True, type="primary"):
        if not reg_name or not reg_email or not reg_pass or not reg_pass2:
            st.error("Please fill in all required fields.")
        elif len(reg_pass) < 6:
            st.error("Password must be at least 6 characters.")
        elif reg_pass != reg_pass2:
            st.error("Passwords do not match. Please try again.")
        elif "@" not in reg_email:
            st.error("Please enter a valid email address.")
        else:
            success, message = register_farmer(reg_name, reg_email, reg_pass, reg_mobile)
            if success:
                st.success(f"✅ Account created! You can now log in.")
                st.balloons()
            else:
                st.error(f"❌ {message}")