import streamlit as st
import os
import sys
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Admin Panel", page_icon="👨‍💼", layout="wide")

# ── Setup paths ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "models"))
from database import get_all_farmers, get_all_reports, get_stats_summary, delete_farmer

# ── Hardcoded admin credentials ───────────────────────────────────────────────
# NOTE: For a real product you'd store this hashed in the DB. For a student
# project, a simple hardcoded check is perfectly fine and easy to explain.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ── Admin login gate ──────────────────────────────────────────────────────────
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if not st.session_state.is_admin:
    st.title("👨‍💼 Admin Login")
    st.markdown("Restricted area — for system administrators only.")
    st.divider()

    username = st.text_input("Admin Username", placeholder="admin")
    password = st.text_input("Admin Password", type="password", placeholder="••••••••")

    if st.button("🔑 Login as Admin", type="primary", use_container_width=True):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("✅ Welcome, Admin!")
            st.rerun()
        else:
            st.error("❌ Invalid admin credentials.")

    st.caption("Default demo credentials — username: `admin`, password: `admin123`")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD (only visible after login)
# ════════════════════════════════════════════════════════════════════════════

# ── Header with logout ────────────────────────────────────────────────────────
col_title, col_logout = st.columns([5, 1])
with col_title:
    st.title("👨‍💼 Admin Panel")
with col_logout:
    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.is_admin = False
        st.rerun()

st.markdown("System-wide overview of all farmers and reports.")
st.divider()

# ── Stats cards ────────────────────────────────────────────────────────────────
stats = get_stats_summary()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👨‍🌾 Total Farmers", stats["farmers"])
c2.metric("📋 Total Reports", stats["reports"])
c3.metric("🌱 Soil Reports", stats["soil"])
c4.metric("🐛 Pest Reports", stats["pest"])
c5.metric("📷 Crop Reports", stats["crop"])

st.divider()

# ── Tabs: Farmers / Reports ──────────────────────────────────────────────────
tab_farmers, tab_reports = st.tabs(["👨‍🌾 All Farmers", "📋 All Reports"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1: FARMERS
# ════════════════════════════════════════════════════════════════════════════
with tab_farmers:
    farmers = get_all_farmers()

    if not farmers:
        st.info("No farmers have registered yet.")
    else:
        farmers_df = pd.DataFrame(
            farmers, columns=["ID", "Name", "Email", "Mobile", "Registered On"]
        )
        st.dataframe(farmers_df, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("🗑️ Remove a Farmer")
        st.caption("This will permanently delete the farmer and all their reports.")

        farmer_options = {f"{f[1]} ({f[2]})": f[0] for f in farmers}
        selected = st.selectbox("Select farmer to delete", options=list(farmer_options.keys()))

        if st.button("Delete Selected Farmer", type="secondary"):
            delete_farmer(farmer_options[selected])
            st.success(f"Deleted {selected}")
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 2: REPORTS
# ════════════════════════════════════════════════════════════════════════════
with tab_reports:
    reports = get_all_reports()

    st.write("DEBUG:", reports[:5])
    st.stop()

    if not reports:
        st.info("No reports submitted yet.")
    else:
        reports_df = pd.DataFrame(
            reports,
            columns=["Farmer Name", "Email", "Type", "Inputs (JSON)", "Result", "Date"]
        )

        # ── Filter by report type ────────────────────────────────────────────
        filter_type = st.selectbox(
            "Filter by report type",
            options=["All", "soil", "pest", "crop"]
        )

        if filter_type != "All":
            reports_df = reports_df[reports_df["Type"] == filter_type]

        st.dataframe(reports_df, use_container_width=True, hide_index=True)

        # ── Download all reports as CSV ──────────────────────────────────────
        csv = reports_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download All Reports (CSV)",
            data=csv,
            file_name="all_farm_reports.csv",
            mime="text/csv"
        )