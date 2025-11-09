# Basic CNN Model Page
import streamlit as st
from PIL import Image
import os

# Page configuration (for this specific page)
st.set_page_config(
    page_title="Basic CNN Model - Image Text Extractor",
    page_icon="🧠",
    layout="wide"
)

# Header
st.title("🧠 Basic CNN Model from Scratch")
st.markdown("""
Welcome to the Basic CNN Model page! This page will use a custom CNN model built from scratch
for text extraction from images.
""")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About Basic CNN Model")
    st.info("""
    This page will feature a custom-built CNN model for OCR tasks.

    **Features (Coming Soon):**
    - 🔨 **Built from scratch**: Custom CNN architecture
    - 🎯 **Training capability**: Train on your own dataset
    - 📊 **Model insights**: Visualize model performance
    - 🚀 **Lightweight**: Optimized for speed

    **Supported formats:**
    - PNG, JPG/JPEG, WEBP, BMP, TIFF
    - Maximum recommended size: 4096x4096 pixels
    """)

    st.header("🔧 Model Information")
    st.caption("Model: Custom CNN (Coming Soon)")
    st.caption("Type: Convolutional Neural Network")
    st.caption("Framework: TensorFlow/PyTorch")
    st.caption("Processing: CPU/GPU-based inference")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file!",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
        help="Upload an image containing text you want to extract."
    )

    if uploaded_file is not None:
        st.success("✅ Image uploaded successfully!")

        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

with col2:
    st.subheader("⚙️ Model Settings")

    st.info("Model configuration options will be available here.")

    # Placeholder for future settings
    st.caption("Settings coming soon...")

# Main processing area
st.divider()
st.subheader("🚀 Text Extraction")

if uploaded_file is not None:
    st.info("🔨 Feature under development. Text extraction functionality will be available soon!")
else:
    st.info("👆 Upload an image to get started!")

# Footer
st.divider()
st.caption("🧠 Basic CNN Model - Custom Architecture | Built from Scratch")
