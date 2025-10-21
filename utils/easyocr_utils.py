"""
EasyOCR utility functions for local text extraction.
This module provides the core functionality for the Local Trained Model page.
"""

import easyocr
import numpy as np
from PIL import Image
import streamlit as st
from typing import List, Optional


class EasyOCRProcessor:
    """EasyOCR processor class for text extraction."""
    
    def __init__(self, languages: List[str] = None):
        """
        Initialize EasyOCR processor.
        
        Args:
            languages: List of language codes for text extraction.
                      Default: ['en', 'es', 'fr', 'de']
        """
        if languages is None:
            languages = ['en', 'es', 'fr', 'de']
        
        self.languages = languages
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """Initialize the EasyOCR reader with specified languages."""
        try:
            # Initialize reader with specified languages
            # Download models at runtime if not available during build
            self.reader = easyocr.Reader(self.languages, download_enabled=True)
            st.success("✅ EasyOCR reader initialized successfully!")
        except Exception as e:
            st.error(f"❌ Error initializing EasyOCR reader: {str(e)}")
            st.info("This might be due to missing models. They should download automatically on first use.")
            raise
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from an image using EasyOCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            str: Extracted text from the image
        """
        if self.reader is None:
            raise ValueError("EasyOCR reader not initialized")
        
        try:
            # Convert image to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Extract text using EasyOCR
            results = self.reader.readtext(
                image_array,
                detail=0,  # Return only text, not bounding boxes
                paragraph=True  # Group text into paragraphs
            )
            
            # Join all extracted text
            extracted_text = ' '.join(results) if results else "No text found in the image."
            
            return extracted_text
            
        except Exception as e:
            error_msg = str(e)
            if "CUDA" in error_msg or "cuda" in error_msg:
                return "❌ CUDA error: GPU not available or insufficient memory"
            elif "out of memory" in error_msg:
                return "❌ Memory error: Image too large for processing"
            else:
                return f"❌ Error extracting text: {error_msg}"
    
    def get_supported_languages(self) -> dict:
        """
        Get mapping of language codes to language names.
        
        Returns:
            dict: Language code to name mapping
        """
        return {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'ch_sim': 'Chinese (Simplified)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ru': 'Russian'
        }


def get_default_languages() -> List[str]:
    """Get default list of supported languages."""
    return ['en', 'es', 'fr', 'de']


def validate_image_format(uploaded_file) -> bool:
    """
    Validate that the uploaded file is a supported image format.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        bool: True if format is supported, False otherwise
    """
    if uploaded_file is None:
        return False
    
    # Check file extension
    allowed_extensions = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff']
    file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
    
    return file_extension in allowed_extensions


def convert_uploaded_file(uploaded_file) -> Optional[Image.Image]:
    """
    Convert uploaded file to PIL Image.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        PIL.Image: Image object or None if conversion fails
    """
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"❌ Error loading image: {str(e)}")
        return None


def display_language_selector(default_languages: List[str] = None) -> List[str]:
    """
    Display language selection interface.
    
    Args:
        default_languages: Default selected languages
        
    Returns:
        List[str]: Selected language codes
    """
    if default_languages is None:
        default_languages = ['en']
    
    processor = EasyOCRProcessor()
    language_map = processor.get_supported_languages()
    
    st.subheader("🌐 Select Languages")
    st.info("Choose the languages you expect to find in your image. You can select multiple languages.")
    
    # Create columns for better layout
    cols = st.columns(3)
    
    selected_languages = []
    for i, (code, name) in enumerate(language_map.items()):
        col = cols[i % 3]
        is_selected = code in default_languages
        if col.checkbox(f"{name} ({code})", value=is_selected, key=f"lang_{code}"):
            selected_languages.append(code)
    
    if not selected_languages:
        st.warning("⚠️ Please select at least one language")
        return default_languages
    
    return selected_languages


def display_extraction_stats(text: str):
    """
    Display statistics for extracted text.
    
    Args:
        text: Extracted text string
    """
    st.divider()
    st.subheader("📊 Text Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔤 Characters", len(text))
    
    with col2:
        word_count = len(text.split())
        st.metric("📝 Words", word_count)
    
    with col3:
        line_count = len(text.split('\n'))
        st.metric("📄 Lines", line_count)


def create_download_button(text: str, filename: str = "extracted_text.txt"):
    """
    Create a download button for extracted text.
    
    Args:
        text: Text to download
        filename: Default filename for download
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="⬇️ Download as TXT",
            data=text,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if st.button("🗑️ Clear Results", use_container_width=True):
            # Clear session state
            keys_to_clear = ['easyocr_extracted_text', 'easyocr_selected_languages']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


def handle_image_processing(uploaded_file, selected_languages: List[str]):
    """
    Handle the complete image processing workflow.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        selected_languages: List of selected language codes
    """
    if uploaded_file is None:
        st.info("👆 Upload an image to get started!")
        return
    
    # Validate image format
    if not validate_image_format(uploaded_file):
        st.error("❌ Unsupported file format. Please upload a PNG, JPG, JPEG, or WEBP image.")
        return
    
    # Convert to PIL image
    image = convert_uploaded_file(uploaded_file)
    if image is None:
        return
    
    # Display uploaded image
    st.image(image, caption="Uploaded Image", width=None)
    
    # Show image info
    st.caption(f"📏 Image size: {image.size[0]} x {image.size[1]} pixels")
    st.caption(f"📦 File size: {uploaded_file.size / 1024:.2f} KB")
    
    # Extract text button
    if st.button("🚀 Extract Text with EasyOCR", type="primary", use_container_width=True):
        with st.spinner("🔍 Extracting text using EasyOCR..."):
            try:
                # Initialize processor with selected languages
                processor = EasyOCRProcessor(selected_languages)
                
                # Extract text
                extracted_text = processor.extract_text(image)
                
                # Store in session state
                st.session_state['easyocr_extracted_text'] = extracted_text
                st.session_state['easyocr_selected_languages'] = selected_languages
                
                st.success("✅ Text extraction completed!")
                
            except Exception as e:
                st.error(f"❌ Error during text extraction: {str(e)}")
    
    # Display results if available
    if 'easyocr_extracted_text' in st.session_state:
        extracted_text = st.session_state['easyocr_extracted_text']
        
        st.subheader("📄 Extracted Text")
        st.text_area(
            "Extracted Text:",
            value=extracted_text,
            height=300,
            help="You can copy this text or download it using the button below"
        )
        
        # Display selected languages
        if 'easyocr_selected_languages' in st.session_state:
            selected_langs = st.session_state['easyocr_selected_languages']
            processor = EasyOCRProcessor()
            language_map = processor.get_supported_languages()
            lang_names = [language_map.get(lang, lang) for lang in selected_langs]
            st.caption(f"🔤 Languages used: {', '.join(lang_names)}")
        
        # Action buttons
        create_download_button(extracted_text)
        
        # Statistics
        display_extraction_stats(extracted_text)
