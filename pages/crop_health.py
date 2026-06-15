import streamlit as st
import numpy as np
import json
import os
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Crop Health", page_icon="📷", layout="centered")

# ── Load model and labels ─────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH  = os.path.join(BASE_DIR, "models", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "models", "crop_labels.json")

@st.cache_resource
def load_model():
    # Import here so streamlit doesn't crash if tensorflow not installed
    import tensorflow as tf
    model  = tf.keras.models.load_model(MODEL_PATH)
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    return model, labels

# ── Page title ────────────────────────────────────────────────────────────────
st.title("📷 Crop Disease Detection")
st.markdown("Upload a **leaf image** and the AI will detect if it is healthy or diseased.")
st.divider()

# ── Check if model exists ─────────────────────────────────────────────────────
if not os.path.exists(MODEL_PATH):
    st.error("⚠️ Model not found! Please run `python models/crop_disease_model.py` first to train the model.")
    st.stop()

model, labels = load_model()

# ── Image upload ──────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"],
    help="Take a clear photo of a single leaf and upload it here."
)

if uploaded_file is not None:

    # Show the uploaded image
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

    # ── Predict button ────────────────────────────────────────────────────────
    if st.button("🔍 Detect Disease", use_container_width=True, type="primary"):

        with st.spinner("Analysing leaf image..."):

            # Preprocess image to match what the model expects
            img_resized = image.resize((224, 224))
            img_array   = np.array(img_resized) / 255.0        # normalize
            img_array   = np.expand_dims(img_array, axis=0)    # add batch dimension

            # Get prediction
            predictions   = model.predict(img_array)
            predicted_idx = str(np.argmax(predictions[0]))
            confidence    = float(np.max(predictions[0])) * 100
            class_name    = labels[predicted_idx]

            # Clean up the class name for display
            # e.g. "Tomato___Early_blight" → "Tomato — Early Blight"
            parts        = class_name.split("___")
            crop_name    = parts[0].replace("_", " ")
            condition    = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"

        # ── Show result ───────────────────────────────────────────────────────
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

        # ── Confidence bar ────────────────────────────────────────────────────
        st.subheader("Confidence Score")
        st.progress(int(confidence))
        st.caption(f"Model is {confidence:.1f}% confident in this prediction")

        # ── Top 3 predictions ─────────────────────────────────────────────────
        with st.expander("📊 Top 3 Predictions"):
            top3_idx = np.argsort(predictions[0])[::-1][:3]
            for rank, idx in enumerate(top3_idx, 1):
                name  = labels[str(idx)].replace("___", " — ").replace("_", " ")
                score = predictions[0][idx] * 100
                st.write(f"{rank}. **{name}** — {score:.1f}%")

else:
    # Show example hint when no image uploaded
    st.info("👆 Upload a leaf photo above to get started.")
    st.markdown("""
    **Tips for best results:**
    - Use a clear, well-lit photo
    - Make sure the leaf fills most of the frame
    - Avoid blurry or dark images
    - Supported crops: Tomato leaves (more crops coming soon)
    """)