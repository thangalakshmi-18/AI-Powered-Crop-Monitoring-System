import streamlit as st
import joblib
import numpy as np
import os
import sys

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Pest Risk", page_icon="🐛", layout="centered")

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

# ── Load model and encoder ────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model   = joblib.load(os.path.join(BASE_DIR, "models", "pest_model.pkl"))
    encoder = joblib.load(os.path.join(BASE_DIR, "models", "pest_encoder.pkl"))
    return model, encoder

model, encoder = load_model()

# ── Page title ────────────────────────────────────────────────────────────────
st.title("🐛 Pest Risk Prediction")
st.markdown(f"Welcome, **{farmer['name']}**! Enter your farm's weather conditions.")
st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────
crop_type = st.selectbox(
    "Select Crop Type",
    options=["Rice", "Wheat", "Maize", "Sugarcane", "Vegetables"]
)

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("Temperature (°C)", min_value=0,   max_value=50,  value=25, step=1)
    humidity    = st.slider("Humidity (%)",      min_value=0,   max_value=100, value=60, step=1)

with col2:
    rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=300, value=50, step=5)

    if temperature >= 33 and humidity >= 80:
        st.warning("⚠️ High temp + humidity detected")
    elif temperature <= 20 and humidity <= 40:
        st.success("✅ Cool dry conditions")

st.divider()

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("🔍 Predict Pest Risk", use_container_width=True, type="primary"):

    crop_encoded = encoder.transform([crop_type])[0]
    input_data = np.array([[temperature, humidity, rainfall, crop_encoded]])
    prediction = model.predict(input_data)[0]

    # ── Save to database ─────────────────────────────────────────────────────
    inputs_dict = {
        "Crop": crop_type, "Temperature": temperature,
        "Humidity": humidity, "Rainfall": rainfall
    }
    save_report(farmer["id"], "pest", inputs_dict, prediction)

    st.subheader("Result")

    if prediction == "High":
        st.error("🚨 **HIGH** Pest Risk Detected!")
        st.markdown("""
        **Immediate Actions Required:**
        - Apply pesticides within 24–48 hours.
        - Inspect crops daily for visible pest damage.
        - Use pheromone traps to monitor pest population.
        - Contact your local agricultural officer if infestation spreads.
        - Avoid excessive irrigation — it attracts more pests.

        **Common pests at high risk:** Aphids, Stem borers, Whiteflies, Locusts.
        """)

    elif prediction == "Medium":
        st.warning("⚠️ **MEDIUM** Pest Risk Detected.")
        st.markdown("""
        **Preventive Actions:**
        - Monitor crops every 2–3 days for early signs.
        - Apply neem oil spray as a natural deterrent.
        - Keep field borders clean and weed-free.
        - Ensure proper drainage to reduce humidity around roots.

        **Common pests at medium risk:** Thrips, Mites, Leaf miners.
        """)

    else:
        st.success("✅ **LOW** Pest Risk — Conditions look good!")
        st.markdown("""
        **Routine Care:**
        - Continue regular field monitoring once a week.
        - Maintain good crop spacing for airflow.
        - No immediate pesticide application needed.
        - Keep records of weather for future predictions.
        """)

    st.caption("✅ This report has been saved to your dashboard.")

    st.subheader("Risk Level Meter")
    risk_value = {"Low": 15, "Medium": 50, "High": 90}
    st.progress(risk_value[prediction])
    st.caption(f"Risk score: {risk_value[prediction]}/100")

    with st.expander("📋 Your Input Summary"):
        st.write(f"- Crop Type: **{crop_type}**")
        st.write(f"- Temperature: **{temperature}°C**")
        st.write(f"- Humidity: **{humidity}%**")
        st.write(f"- Rainfall: **{rainfall} mm**")
        st.write(f"- Prediction: **{prediction} Risk**")