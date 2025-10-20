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

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY .env.example .

# Create a directory for user uploads (optional)
RUN mkdir -p /app/uploads

# Expose Streamlit default port
EXPOSE 8501

# Health check to ensure container is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
# The --server.address flag makes it accessible from outside the container
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.address=0.0.0.0", \
            "--server.port=8501", \
            "--server.headless=true", \
            "--browser.gatherUsageStats=false"]
