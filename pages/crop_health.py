import streamlit as st
import numpy as np
import json
import os
import sys
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Crop Health", page_icon="📷", layout="centered")

# ── Setup paths ───────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH  = os.path.join(BASE_DIR, "models", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "models", "crop_labels.json")
sys.path.append(os.path.join(BASE_DIR, "models"))
from database import save_report

# ── Require login ─────────────────────────────────────────────────────────────
if "farmer" not in st.session_state or not st.session_state.farmer:
    st.warning("⚠️ Please log in first to use this feature.")
    st.info("👈 Go to the **login** page in the sidebar.")
    st.stop()

farmer = st.session_state.farmer

@st.cache_resource
def load_model():
    import tensorflow as tf
    model  = tf.keras.models.load_model(MODEL_PATH)
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    return model, labels

# ── Page title ────────────────────────────────────────────────────────────────
st.title("📷 Crop Disease Detection")
st.markdown(f"Welcome, **{farmer['name']}**! Upload a leaf image to detect disease.")
st.divider()

if not os.path.exists(MODEL_PATH):
    st.error("⚠️ Model not found! Please run `python models/crop_disease_model.py` first to train the model.")
    st.stop()

model, labels = load_model()

uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"],
    help="Take a clear photo of a single leaf and upload it here."
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
    with col2:
        st.markdown("**Image Details**")
        st.write(f"- Format: `{uploaded_file.type}`")
        st.write(f"- Size: `{image.size[0]} x {image.size[1]} px`")
        st.write(f"- File: `{uploaded_file.name}`")

    st.divider()

    if st.button("🔍 Detect Disease", use_container_width=True, type="primary"):

        with st.spinner("Analysing leaf image..."):
            img_resized = image.resize((224, 224))
            img_array   = np.array(img_resized) / 255.0
            img_array   = np.expand_dims(img_array, axis=0)

            predictions   = model.predict(img_array)
            predicted_idx = str(np.argmax(predictions[0]))
            confidence    = float(np.max(predictions[0])) * 100
            class_name    = labels[predicted_idx]

            parts        = class_name.split("___")
            crop_name    = parts[0].replace("_", " ")
            condition    = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"

        # ── Save to database ─────────────────────────────────────────────────
        inputs_dict = {"image_name": uploaded_file.name, "crop": crop_name}
        result_str  = f"{crop_name} - {condition} ({confidence:.1f}%)"
        save_report(farmer["id"], "crop", inputs_dict, result_str)

        st.subheader("Detection Result")

        if "healthy" in condition.lower():
            st.success(f"✅ **{crop_name}** leaf is **Healthy!**")
            st.markdown(f"""
            **Confidence:** {confidence:.1f}%

            **Recommendations:**
            - Your crop looks healthy. Keep up the good work!
            - Continue regular watering and nutrient schedule.
            - Monitor weekly to catch any early signs of disease.
            """)
        else:
            st.error(f"🚨 **{crop_name}** — **{condition}** Detected!")
            st.markdown(f"""
            **Confidence:** {confidence:.1f}%

            **Recommendations:**
            - Remove and destroy heavily infected leaves immediately.
            - Apply appropriate fungicide or pesticide spray.
            - Avoid overhead watering — water at the base of the plant.
            - Isolate affected plants to prevent spread.
            - Consult your local agricultural extension officer if severe.
            """)

        st.caption("✅ This report has been saved to your dashboard.")

        st.subheader("Confidence Score")
        st.progress(int(confidence))
        st.caption(f"Model is {confidence:.1f}% confident in this prediction")

        with st.expander("📊 Top 3 Predictions"):
            top3_idx = np.argsort(predictions[0])[::-1][:3]
            for rank, idx in enumerate(top3_idx, 1):
                name  = labels[str(idx)].replace("___", " — ").replace("_", " ")
                score = predictions[0][idx] * 100
                st.write(f"{rank}. **{name}** — {score:.1f}%")
else:
    st.info("👆 Upload a leaf photo above to get started.")
    st.markdown("""
    **Tips for best results:**
    - Use a clear, well-lit photo
    - Make sure the leaf fills most of the frame
    - Avoid blurry or dark images
    - Supported crops: Tomato leaves (more crops coming soon)
    """)