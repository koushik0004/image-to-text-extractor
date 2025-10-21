# Local Trained Model Page
import streamlit as st
from PIL import Image
import os

# Import EasyOCR utilities
try:
    from utils.easyocr_utils import (
        EasyOCRProcessor, 
        display_language_selector,
        handle_image_processing,
        get_default_languages
    )
except ImportError:
    st.error("❌ EasyOCR utilities not found. Please ensure the utils module exists.")

# Page configuration (for this specific page)
st.set_page_config(
    page_title="Local Trained Model - Image Text Extractor",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 Local Trained Model")
st.markdown("""
Welcome to the Local Trained Model page! This page uses **EasyOCR** - a locally trained 
machine learning model that runs entirely within the Docker container. No internet 
connection or API keys required!
""")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About Local Model")
    st.info("""
    This page uses EasyOCR - an open-source OCR engine that runs locally in the container.
    
    **Key Features:**
    - 🔒 **Privacy-focused**: No data leaves your container
    - 🚀 **Offline capability**: Works without internet
    - 🌍 **Multi-language**: Supports 5+ languages
    - 💨 **Fast processing**: Local inference, no network delays
    - 📱 **Handwriting support**: Recognizes handwritten text
    
    **Supported formats:**
    - PNG, JPG/JPEG, WEBP, BMP, TIFF
    - Maximum recommended size: 4096x4096 pixels
    """)

    st.header("🌐 Supported Languages")
    st.markdown("""
    **Default Languages:**
    - 🇬🇧 English (en)
    - 🇪🇸 Spanish (es) 
    - 🇫🇷 French (fr)
    - 🇩🇪 German (de)
    - 🇨🇳 Chinese (zh-cn)
    
    **Additional Languages Available:**
    - 🇦🇪 Arabic (ar)
    - 🇮🇳 Hindi (hi)
    - 🇯🇵 Japanese (ja)
    - 🇰🇷 Korean (ko)
    - 🇷🇺 Russian (ru)
    """)

    st.header("🔧 Model Information")
    st.caption("Model: EasyOCR (qualcomm/EasyOCR)")
    st.caption("Type: CNN + LSTM based OCR")
    st.caption("Accuracy: High for printed text")
    st.caption("Processing: CPU-based inference")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
        help="Upload an image containing text you want to extract. Supports printed and handwritten text."
    )
    
    if uploaded_file is not None:
        st.success("✅ Image uploaded successfully!")
        st.info("Now select the languages you expect to find in your image and click \"Extract Text\".")

with col2:
    st.subheader("🌍 Select Languages")
    
    # Language selection
    default_languages = get_default_languages()
    selected_languages = display_language_selector(default_languages)
    
    st.info(f"Selected languages: {", ".join(selected_languages)}")

# Main processing area
st.divider()
st.subheader("🚀 Text Extraction")

# Handle image processing
if "uploaded_file" in locals():
    handle_image_processing(uploaded_file, selected_languages)
else:
    st.info("👆 Upload an image and select languages to get started!")

# Footer
st.divider()
st.caption("🔧 Local Trained Model - Powered by EasyOCR | Privacy-focused AI Processing")