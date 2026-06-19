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

# ── Admin credentials ─────────────────────────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ── Login state ───────────────────────────────────────────────────────────────
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if not st.session_state.is_admin:
    st.title("👨‍💼 Admin Login")
    st.markdown("Restricted area — admin only")
    st.divider()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])

with col1:
    st.title("👨‍💼 Admin Panel")

with col2:
    if st.button("Logout"):
        st.session_state.is_admin = False
        st.rerun()

st.markdown("System-wide overview of farmers and reports.")
st.divider()

# ── Stats ─────────────────────────────────────────────────────────────────────
stats = get_stats_summary()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👨‍🌾 Farmers", stats["farmers"])
c2.metric("📋 Reports", stats["reports"])
c3.metric("🌱 Soil", stats["soil"])
c4.metric("🐛 Pest", stats["pest"])
c5.metric("📷 Crop", stats["crop"])

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["👨‍🌾 Farmers", "📋 Reports"])

# ═════════════════ FARMERS ═════════════════
with tab1:
    farmers = get_all_farmers()

    if not farmers:
        st.info("No farmers found.")
    else:
        df = pd.DataFrame(
            farmers,
            columns=["ID", "Name", "Email", "Mobile", "Registered On"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("🗑️ Delete Farmer")

        options = {f"{f[1]} ({f[2]})": f[0] for f in farmers}
        selected = st.selectbox("Select farmer", list(options.keys()))

        if st.button("Delete"):
            delete_farmer(options[selected])
            st.success("Farmer deleted")
            st.rerun()

# ═════════════════ REPORTS ═════════════════
with tab2:
    reports = get_all_reports()

    if not reports:
        st.info("No reports available.")
    else:
        df = pd.DataFrame(
            reports,
            columns=[
                "Farmer Name",
                "Email",
                "Type",
                "Inputs (JSON)",
                "Result",
                "Date"
            ]
        )

        # Filter
        filter_type = st.selectbox(
            "Filter reports",
            ["All", "soil", "pest", "crop"]
        )

        if filter_type != "All":
            df = df[df["Type"] == filter_type]

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Download CSV
        csv = df.to_csv(index=False)

        st.download_button(
            "⬇️ Download Reports",
            data=csv,
            file_name="farm_reports.csv",
            mime="text/csv"
        )