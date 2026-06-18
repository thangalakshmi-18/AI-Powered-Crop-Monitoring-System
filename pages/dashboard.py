import streamlit as st
import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# ── Setup paths ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "models"))
from database import get_farmer_reports

# ── Require login ─────────────────────────────────────────────────────────────
if "farmer" not in st.session_state or not st.session_state.farmer:
    st.warning("⚠️ Please log in first to view your dashboard.")
    st.info("👈 Go to the **login** page in the sidebar.")
    st.stop()

farmer = st.session_state.farmer

# ── Page title ────────────────────────────────────────────────────────────────
st.title("📊 Farm Dashboard")
st.markdown(f"Welcome, **{farmer['name']}**! Here's your complete farm analysis history.")
st.divider()

# ── Fetch all reports for this farmer ─────────────────────────────────────────
reports = get_farmer_reports(farmer["id"])

if not reports:
    st.info("📭 No reports yet. Go run a **Soil Analysis**, **Pest Risk**, or **Crop Health** check first!")
    st.stop()

# ── Convert to DataFrame for easy handling ────────────────────────────────────
df = pd.DataFrame(reports, columns=["report_type", "inputs", "result", "created_at"])
df["created_at"] = pd.to_datetime(df["created_at"])

# ── Top metric cards ──────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_reports = len(df)
soil_count    = len(df[df["report_type"] == "soil"])
pest_count    = len(df[df["report_type"] == "pest"])
crop_count    = len(df[df["report_type"] == "crop"])

with col1:
    st.metric("📋 Total Reports", total_reports)
with col2:
    st.metric("🌱 Soil Checks", soil_count)
with col3:
    st.metric("🐛 Pest Checks", pest_count)
with col4:
    st.metric("📷 Crop Scans", crop_count)

st.divider()

# ── Charts section ────────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

# ── Chart 1: Reports by type (bar chart) ──────────────────────────────────────
with chart_col1:
    st.subheader("Reports by Type")
    type_counts = df["report_type"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(5, 4))
    colors = {"soil": "#8B4513", "pest": "#DC143C", "crop": "#228B22"}
    bar_colors = [colors.get(t, "#999999") for t in type_counts.index]
    ax1.bar(type_counts.index, type_counts.values, color=bar_colors)
    ax1.set_ylabel("Number of Reports")
    ax1.set_xlabel("Report Type")
    st.pyplot(fig1)

# ── Chart 2: Soil condition distribution (pie chart) ──────────────────────────
with chart_col2:
    st.subheader("Soil Condition Breakdown")
    soil_df = df[df["report_type"] == "soil"]

    if len(soil_df) > 0:
        soil_results = soil_df["result"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        pie_colors = {"Good": "#2ECC71", "Average": "#F39C12", "Poor": "#E74C3C"}
        colors_list = [pie_colors.get(r, "#999999") for r in soil_results.index]
        ax2.pie(soil_results.values, labels=soil_results.index, autopct="%1.0f%%",
                colors=colors_list, startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)
    else:
        st.info("No soil reports yet.")

st.divider()

# ── Pest risk trend over time ─────────────────────────────────────────────────
pest_df = df[df["report_type"] == "pest"]
if len(pest_df) > 0:
    st.subheader("🐛 Pest Risk History")
    risk_map = {"Low": 1, "Medium": 2, "High": 3}
    pest_df_sorted = pest_df.sort_values("created_at")
    pest_df_sorted["risk_numeric"] = pest_df_sorted["result"].map(risk_map)

    fig3, ax3 = plt.subplots(figsize=(10, 3))
    ax3.plot(pest_df_sorted["created_at"], pest_df_sorted["risk_numeric"],
              marker="o", color="#DC143C", linewidth=2)
    ax3.set_yticks([1, 2, 3])
    ax3.set_yticklabels(["Low", "Medium", "High"])
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Risk Level")
    ax3.grid(True, alpha=0.3)
    plt.xticks(rotation=30)
    st.pyplot(fig3)

st.divider()

# ── Full history table ────────────────────────────────────────────────────────
st.subheader("📅 Full Analysis History")

# Build a clean display table
display_rows = []
for _, row in df.sort_values("created_at", ascending=False).iterrows():
    icon = {"soil": "🌱", "pest": "🐛", "crop": "📷"}.get(row["report_type"], "📋")
    display_rows.append({
        "Type": f"{icon} {row['report_type'].capitalize()}",
        "Result": row["result"],
        "Date": row["created_at"].strftime("%d %b %Y, %I:%M %p")
    })

history_df = pd.DataFrame(display_rows)
st.dataframe(history_df, use_container_width=True, hide_index=True)

# ── Download report as CSV ────────────────────────────────────────────────────
csv = history_df.to_csv(index=False)
st.download_button(
    label="⬇️ Download Full Report (CSV)",
    data=csv,
    file_name=f"{farmer['name']}_farm_report.csv",
    mime="text/csv"
)