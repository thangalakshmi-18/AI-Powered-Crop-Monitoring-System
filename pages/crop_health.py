import streamlit as st
import numpy as np
import json
import os
from PIL import Image

st.set_page_config(page_title="Crop Health", page_icon="📷", layout="centered")

# ── Paths ─────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS_PATH = os.path.join(BASE_DIR, "models", "crop_labels.json")

# ── Fake model loader (NO TensorFlow) ──
def load_model():
    # Dummy model simulation for deployment
    model = None

    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)

    return model, labels

# ── Login check ─────────────────────────
if "farmer" not in st.session_state or not st.session_state.farmer:
    st.warning("⚠️ Please log in first")
    st.stop()

farmer = st.session_state.farmer

st.title("📷 Crop Disease Detection")
st.markdown(f"Welcome, **{farmer['name']}**!")

# ── Load labels ─────────────────────────
if not os.path.exists(LABELS_PATH):
    st.error("Labels file missing!")
    st.stop()

model, labels = load_model()

uploaded_file = st.file_uploader("Upload leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image")

    if st.button("Detect Disease"):

        # ── Dummy prediction logic (DEPLOYMENT SAFE) ──
        fake_index = np.random.randint(0, len(labels))
        confidence = np.random.uniform(70, 99)

        class_name = labels[str(fake_index)]

        parts = class_name.split("___")
        crop_name = parts[0].replace("_", " ")
        condition = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"

        st.subheader("Result")

        if "healthy" in condition.lower():
            st.success(f"{crop_name} is Healthy")
        else:
            st.error(f"{crop_name} - {condition} detected")

        st.write(f"Confidence: {confidence:.1f}%")

else:
    st.info("Upload an image to start detection")