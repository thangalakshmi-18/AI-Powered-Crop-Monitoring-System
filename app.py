import streamlit as st

st.set_page_config(
    page_title="AI Crop Monitoring System",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 AI-Powered Crop Monitoring System")
st.markdown("""
Welcome to the Smart Agriculture Platform.

Use the **sidebar** to navigate between modules:

| Module | What it does |
|---|---|
| 🌱 Soil Analysis | Checks if your soil is Good, Average, or Poor |
| 🐛 Pest Risk | Predicts pest danger level (coming soon) |
| 📷 Crop Health | Detects disease from a leaf photo (coming soon) |
| 📊 Dashboard | Your full farm report (coming soon) |
""")

st.divider()
st.info("👈 Click **Soil Analysis** in the sidebar to start.")