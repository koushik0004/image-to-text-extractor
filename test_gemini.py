# test_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print(f"API Key loaded: {api_key[:10]}... (length: {len(api_key) if api_key else 0})")

if not api_key:
    print("❌ API key not found!")
    exit(1)

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✅ API configured successfully")
    
    # Test with a simple text prompt
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✅ API working! Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")