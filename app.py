# app.py
from pickle import FALSE
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION SECTION - Update API settings here
# ============================================================================

def configure_gemini_api():
    """
    Configure the Gemini API with your API key.
    """
    try:
        # CHANGED: Check environment variable FIRST (from .env)
        api_key = os.getenv('GEMINI_API_KEY')
        
        # If not found in env, try Streamlit secrets
        if not api_key and hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']

        if not api_key:
            st.error("⚠️ Gemini API key not found!")
            st.info("""
            Please set your API key in one of the following ways:
            
            **For Local Development:**
            1. Create a `.env` file in the project root
            2. Add: `GEMINI_API_KEY=your_actual_api_key`
            
            **Get your API key from:** https://makersuite.google.com/app/apikey
            """)
            st.stop()
            return FALSE
        
        # IMPORTANT: Clean the API key thoroughly
        # Remove whitespace, newlines, carriage returns, quotes, and other junk
        api_key = api_key.strip()  # Remove leading/trailing whitespace
        api_key = api_key.strip('"').strip("'")  # Remove quotes
        api_key = api_key.replace('\n', '')  # Remove newlines
        api_key = api_key.replace('\r', '')  # Remove carriage returns
        api_key = api_key.replace(' ', '')  # Remove any spaces
        api_key = api_key.replace('\t', '')  # Remove tabs

        # Remove BOM if present
        if api_key.startswith('\ufeff'):
            api_key = api_key[1:]
        
        # Validate API key format
        if not api_key.startswith('AIza'):
            st.error("⚠️ Invalid API key format!")
            st.info("Gemini API keys should start with 'AIza'")
            st.stop()
        
        if len(api_key) < 30:
            st.error("⚠️ API key seems too short!")
            st.info("Gemini API keys are typically 39 characters long")
            st.stop()
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Test the API key with a simple request
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            # This won't actually make a request, just validates the setup
            st.success("✅ API key configured successfully!")
        except Exception as e:
            st.error(f"❌ Error configuring API: {str(e)}")
            st.stop()
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error configuring Gemini API: {str(e)}")
        return False


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def extract_text_from_image(image):
    """
    Extract text from an image using Google Gemini API.
    
    Args:
        image: PIL Image object
    
    Returns:
        str: Extracted text from the image
    """
    try:
        # Convert PIL Image to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image if it's too large (Gemini has size limits)
        max_size = 4096
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            st.info(f"ℹ️ Image resized to {new_size[0]}x{new_size[1]} for processing")
        
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create a prompt for text extraction
        prompt = """Extract all text from this image. 
        Return only the extracted text without any additional explanation.
        If there is no text, respond with "No text found in the image."
        Preserve the layout and structure of the text."""
        
        # Generate content using the image and prompt
        response = model.generate_content([prompt, image])
        
        # Check if response was blocked
        if response.prompt_feedback.block_reason:
            return f"Content was blocked: {response.prompt_feedback.block_reason}"
        
        # Extract the text from the response
        if response.text:
            return response.text
        else:
            return "No text could be extracted from the image."
        
    except Exception as e:
        error_msg = str(e)
        
        # Provide specific error messages
        if "400" in error_msg:
            return """❌ Error 400: Bad Request
            
                    Possible causes:
                    1. Invalid API key - Please check your GEMINI_API_KEY in .env file
                    2. Image format issue - Try a different image
                    3. API quota exceeded - Check your Gemini API usage

                    Please verify:
                    - API key starts with 'AIza' and is about 39 characters
                    - Image is a valid PNG, JPG, or WEBP file
                    - You have API quota remaining at https://makersuite.google.com/
                    """
        elif "403" in error_msg:
            return "❌ Error 403: API key is invalid or doesn't have permission"
        elif "429" in error_msg:
            return "❌ Error 429: Rate limit exceeded. Please wait a moment and try again"
        else:
            return f"❌ Error extracting text: {error_msg}"


def convert_image_for_display(uploaded_file):
    """
    Convert uploaded file to PIL Image for display and processing.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        PIL.Image: Image object
    """
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    """
    Main function to run the Streamlit application.
    """
    
    # Page configuration
    st.set_page_config(
        page_title="Image Text Extractor",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Configure Gemini API
    if not configure_gemini_api():
        return
    
    # Header
    st.title("📝 Image Text Extractor")
    st.markdown("""
    Upload an image containing text, and this app will extract the text using AI-powered OCR.
    Supports printed text, handwriting, and multiple languages.
    """)
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This application uses Google's Gemini AI model to extract text from images.
        
        **Supported formats:**
        - PNG
        - JPG/JPEG
        - WEBP
        
        **Features:**
        - High accuracy text extraction
        - Handwriting recognition
        - Multi-language support
        - Preserves text structure
        """)
        
        st.header("🔧 Model Settings")
        st.caption("Current model: Gemini 2.5 Flash")
        st.caption("For better accuracy, you can modify the code to use 'gemini-2.5-pro'")
        
        st.header("📊 Usage Tips")
        st.markdown("""
        - Use clear, well-lit images
        - Ensure text is not blurry
        - Higher resolution = better results
        - Avoid extreme angles
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload an image containing text you want to extract"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = convert_image_for_display(uploaded_file)
            
            if image:
                # st.image(image, caption="Uploaded Image", use_container_width=True)
                st.image(image, caption="Uploaded Image", width=None)
                
                # Display image information
                st.caption(f"📏 Image size: {image.size[0]} x {image.size[1]} pixels")
                st.caption(f"📦 File size: {uploaded_file.size / 1024:.2f} KB")
    
    with col2:
        st.subheader("📄 Extracted Text")
        
        if uploaded_file is not None and image:
            # Extract text button
            if st.button("🚀 Extract Text", type="primary", use_container_width=True):
                with st.spinner("🔍 Extracting text from image..."):
                    # Reset the file pointer to the beginning
                    uploaded_file.seek(0)
                    
                    # Extract text
                    extracted_text = extract_text_from_image(image)
                    
                    # Store in session state
                    st.session_state['extracted_text'] = extracted_text
            
            # Display extracted text if available
            if 'extracted_text' in st.session_state:
                extracted_text = st.session_state['extracted_text']
                
                # Text area with extracted text
                st.text_area(
                    "Extracted Text:",
                    value=extracted_text,
                    height=400,
                    help="You can copy this text or download it as a file"
                )
                
                # Action buttons
                col_a, col_b = st.columns(2)
                
                with col_a:
                    # Download button
                    st.download_button(
                        label="⬇️ Download as TXT",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col_b:
                    # Clear button
                    if st.button("🗑️ Clear", use_container_width=True):
                        if 'extracted_text' in st.session_state:
                            del st.session_state['extracted_text']
                        st.rerun()
                
                # Display statistics
                st.divider()
                st.subheader("📊 Statistics")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("Characters", len(extracted_text))
                
                with col_stat2:
                    word_count = len(extracted_text.split())
                    st.metric("Words", word_count)
                
                with col_stat3:
                    line_count = len(extracted_text.split('\n'))
                    st.metric("Lines", line_count)
        else:
            st.info("👆 Upload an image to get started!")
    
    # Footer
    st.divider()
    st.caption("Made with ❤️ using Streamlit and Google Gemini AI | Powered by AI")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()