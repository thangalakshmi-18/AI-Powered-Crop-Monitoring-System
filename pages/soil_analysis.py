import streamlit as st
import joblib
import numpy as np
import os
import sys

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Soil Analysis", page_icon="🌱", layout="centered")

# ── Setup paths ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "models"))
from database import save_report

# ── Require login ─────────────────────────────────────────────────────────────
if "farmer" not in st.session_state or not st.session_state.farmer:
    st.warning("⚠️ Please log in first to use this feature.")
    st.info("👈 Go to the **login** page in the sidebar.")
    st.stop()

farmer = st.session_state.farmer

# ── Load the trained model ────────────────────────────────────────────────────
model_path = os.path.join(BASE_DIR, "models", "soil_model.pkl")

@st.cache_resource
def load_model():
    return joblib.load(model_path)

model = load_model()

# ── Page title ────────────────────────────────────────────────────────────────
st.title("🌱 Soil Condition Analysis")
st.markdown(f"Welcome, **{farmer['name']}**! Enter your soil values below.")
st.divider()

# ── Input sliders ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    nitrogen   = st.slider("Nitrogen (N)",   min_value=0,   max_value=140, value=50, step=1)
    phosphorus = st.slider("Phosphorus (P)", min_value=0,   max_value=100, value=30, step=1)
    potassium  = st.slider("Potassium (K)",  min_value=0,   max_value=100, value=25, step=1)

with col2:
    ph       = st.slider("Soil pH",     min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    moisture = st.slider("Moisture (%)", min_value=0,   max_value=100,  value=50,  step=1)

st.divider()

# ── Predict button ────────────────────────────────────────────────────────────
if st.button("🔍 Analyse Soil", use_container_width=True, type="primary"):

    input_data = np.array([[nitrogen, phosphorus, potassium, ph, moisture]])
    prediction = model.predict(input_data)[0]

    # ── Save to database ─────────────────────────────────────────────────────
    inputs_dict = {
        "Nitrogen": nitrogen, "Phosphorus": phosphorus,
        "Potassium": potassium, "pH": ph, "Moisture": moisture
    }
    save_report(farmer["id"], "soil", inputs_dict, prediction)

    # ── Show result ───────────────────────────────────────────────────────────
    st.subheader("Result")

    if prediction == "Good":
        st.success("✅ Your soil is in **Good** condition!")
        st.markdown("""
        **Recommendations:**
        - Your soil nutrients are well-balanced. Great job!
        - Continue regular watering and monitoring.
        - Suitable crops: Rice, Wheat, Sugarcane, Maize.
        """)

    elif prediction == "Average":
        st.warning("⚠️ Your soil is in **Average** condition.")
        st.markdown("""
        **Recommendations:**
        - Add organic compost to improve nitrogen levels.
        - Apply balanced NPK fertiliser.
        - Monitor pH and keep it between 6.0 – 7.0.
        - Suitable crops: Millets, Pulses, Vegetables.
        """)

    else:
        st.error("❌ Your soil is in **Poor** condition.")
        st.markdown("""
        **Recommendations:**
        - Soil needs urgent improvement before planting.
        - Apply lime to raise pH if it is too acidic.
        - Add heavy organic matter (compost, manure).
        - Test soil with a lab kit for detailed analysis.
        - Avoid planting until condition improves.
        """)

    st.caption("✅ This report has been saved to your dashboard.")

    with st.expander("📋 Your Input Summary"):
        st.write(f"- Nitrogen: **{nitrogen}**")
        st.write(f"- Phosphorus: **{phosphorus}**")
        st.write(f"- Potassium: **{potassium}**")
        st.write(f"- pH: **{ph}**")
        st.write(f"- Moisture: **{moisture}%**")
        st.write(f"- Prediction: **{prediction}**")