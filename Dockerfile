# Dockerfile

# Use official Python runtime as base image
# Using Python 3.12 slim for smaller image size
FROM python:3.12-slim

# Set metadata labels
LABEL maintainer="your-email@example.com"
LABEL description="Image Text Extractor using Streamlit and Google Gemini API"

# Set working directory in container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Set HOME environment for model downloads
ENV HOME=/root

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libglib2.0-0 \
#     libsm6 \
#     libxext6 \
#     libxrender-dev \
#     libgomp1 \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libblas-dev \
    libjpeg-dev \
    zlib1g-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies using requirements.txt with PyTorch CPU wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Install PyTorch CPU wheels first to ensure compatibility
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
# Install remaining dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download EasyOCR models during build for offline usage
# This ensures models are available in the container without runtime downloads
RUN python -c "import easyocr; reader = easyocr.Reader(['en', 'es', 'fr', 'de']); print('EasyOCR models downloaded successfully')" || echo "EasyOCR download failed, will download at runtime"

# Copy application code
COPY Home.py .
COPY .env.example .
COPY pages/ ./pages/
COPY utils/ ./utils/

# Create directories for user uploads and model storage
RUN mkdir -p /app/uploads
RUN mkdir -p /root/.EasyOCR/model

# Expose Streamlit default port
EXPOSE 8501

# Health check to ensure container is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
# The --server.address flag makes it accessible from outside the container
ENTRYPOINT ["streamlit", "run", "Home.py", \
            "--server.address=0.0.0.0", \
            "--server.port=8501", \
            "--server.headless=true", \
            "--browser.gatherUsageStats=false"]
