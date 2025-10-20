# 📝 Image Text Extractor

A web application built with Streamlit that extracts text from images using Google's Gemini AI. Upload any image containing text, and the app will intelligently extract and display the text content.

## ✨ Features

- 🖼️ **Image Upload**: Support for PNG, JPG, JPEG, and WEBP formats
- 🤖 **AI-Powered OCR**: Uses Google Gemini 1.5 Flash for accurate text extraction
- ✍️ **Handwriting Recognition**: Capable of recognizing handwritten text
- 🌍 **Multi-language Support**: Extracts text in multiple languages
- 📊 **Text Statistics**: Displays character, word, and line counts
- ⬇️ **Download Feature**: Save extracted text as a TXT file
- 🐳 **Dockerized**: Easy deployment with Docker

## 🚀 Quick Start

### Prerequisites

- Python 3.12 (or Python 3.9+)
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd image-text-extractor
```

2. **Set up environment** (using conda)
```bash
   conda activate your_pytorch_env_name
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure API key**
```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
```

5. **Run the application**
```bash
   streamlit run app.py
```

6. **Open browser**
   Navigate to `http://localhost:8501`

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t image-text-extractor .
```

### Run Container

**Option 1: Pass API key directly**
```bash
docker run -p 8501:8501 -e GEMINI_API_KEY=your_actual_api_key image-text-extractor
```

**Option 2: Use .env file**
```bash
docker run -p 8501:8501 --env-file .env image-text-extractor
```

**Option 3: Run in detached mode**
```bash
docker run -d -p 8501:8501 --name text-extractor --env-file .env image-text-extractor
```

### View Logs
```bash
docker logs -f text-extractor
```

### Stop Container
```bash
docker stop text-extractor
docker rm text-extractor
```

## 📁 Project Structure
```
image-text-extractor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker build exclusions
├── .env.example          # Environment variables template
├── .gitignore           # Git exclusions
└── README.md            # This file
```

## 🔧 Configuration

### Changing the Gemini Model

In `app.py`, line 68, you can change the model:
```python
# For faster processing (default)
model = genai.GenerativeModel('gemini-1.5-flash')

# For better accuracy
model = genai.GenerativeModel('gemini-1.5-pro')
```

### API Key Setup Locations

The app looks for the API key in this order:

1. **Streamlit Secrets** (for cloud deployment)
   - Add to `.streamlit/secrets.toml` or Streamlit Cloud settings

2. **Environment Variable** (for local development)
   - Add to `.env` file

## 📊 Usage Tips

- Use clear, well-lit images for best results
- Higher resolution images produce better text extraction
- Avoid extreme angles or distorted images
- The app handles both printed and handwritten text
- Supports multiple languages automatically

## 🛠️ Troubleshooting

### API Key Issues
```
Error: Gemini API key not found!
```
**Solution**: Ensure your `.env` file exists and contains:
```
GEMINI_API_KEY=your_actual_api_key
```

### Port Already in Use
```
Error: Port 8501 is already in use
```
**Solution**: Either stop the other process or use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Docker Permission Denied
```
Error: permission denied while trying to connect to Docker daemon
```
**Solution**: Run with sudo or add your user to docker group:
```bash
sudo usermod -aG docker $USER
```

## 🐳 Docker Compose Deployment (Recommended)

### Quick Start with Docker Compose

1. **Setup environment**
```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
```

2. **Start the application**
```bash
   docker-compose up -d
```

3. **Access the application**
   Open http://localhost:8501

4. **View logs**
```bash
   docker-compose logs -f
```

5. **Stop the application**
```bash
   docker-compose down
```

### Docker Compose Commands Reference

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start in background |
| `docker-compose up` | Start in foreground (see logs) |
| `docker-compose down` | Stop and remove containers |
| `docker-compose restart` | Restart the application |
| `docker-compose logs -f` | View logs (follow mode) |
| `docker-compose ps` | Check container status |
| `docker-compose build` | Rebuild the image |
| `docker-compose build --no-cache` | Rebuild without cache |

### Using Makefile (Optional)

If you have `make` installed:
```bash
make help      # Show all available commands
make up        # Start application
make down      # Stop application
make logs      # View logs
make dev       # Start in development mode
make prod      # Start in production mode
make clean     # Clean all resources
```

### Environment Modes

**Development Mode:**
```bash
docker-compose up
# or
make dev
```
- Hot-reloading enabled
- Source code mounted as volume
- Verbose logging

**Production Mode:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
# or
make prod
```
- Optimized for performance
- No source code mounting
- Resource limits enforced
- Enhanced security

### Troubleshooting Docker Compose

**Issue: Port already in use**
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process or change port in docker-compose.yml
```

**Issue: API key not found**
```bash
# Verify .env file exists and contains API key
cat .env

# Restart containers
docker-compose restart
```

**Issue: Container keeps restarting**
```bash
# Check logs
docker-compose logs --tail=100 app

# Check health status
docker-compose ps
```

**Issue: Build fails**
```bash
# Clean and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue in the repository.

---

Made with ❤️ using Streamlit and Google Gemini AI