# 🏥 Medical Discharge Summary Assistant

An AI-powered medical documentation system that generates discharge summaries using RAG (Retrieval-Augmented Generation) architecture with Groq API, integrated with AutoGen for conversational AI assistance.

## ✨ Features

- **🤖 AI-Powered Discharge Summary Generation**: Automatically generates comprehensive discharge summaries using Groq API with LLaMA 4 Maverick model
- **💬 Conversational AI Agent**: Interactive chat interface powered by AutoGen for doctor-patient queries
- **🔍 RAG-Based Similar Case Search**: Find similar patient cases using semantic search with Bio ClinicalBERT embeddings
- **📊 Modern Dark Theme UI**: Beautiful, modern interface with smooth animations and professional design
- **⚡ FastAPI Backend**: High-performance async backend for significantly faster response times
- **📄 Multiple Export Formats**: Download summaries as TXT, DOCX, or PDF
- **🎨 Template Support**: Upload PDF templates for custom discharge summary formats
- **💾 Feedback Loop**: Add generated summaries back to the knowledge base for continuous improvement

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one at https://console.groq.com/keys)
- MongoDB connection (cloud or local)
- CUDA-capable GPU (optional, for faster embeddings)

### Step 1: Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account (or log in if you already have one)
3. Navigate to **API Keys** section: https://console.groq.com/keys
4. Click **"Create API Key"**
5. Copy your API key

### Step 2: Set Up Environment Variables

Create a `.env` file in the `ingestion-phase` directory:

```bash
cd ingestion-phase
```

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**Linux/Mac:**
```bash
touch .env
```

Add your API key to the `.env` file:

```env
GROQ_API_KEY=your_actual_api_key_here
```

**Important:** Never commit the `.env` file to git! It's already in `.gitignore`.

For detailed Groq setup instructions, see [GROQ_SETUP.md](GROQ_SETUP.md)

### Step 3: Install Dependencies

```bash
cd ingestion-phase
pip install -r requirements.txt
```

**Key dependencies:**
- `streamlit` - Web interface
- `fastapi` - High-performance async backend
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- `motor` - Async MongoDB driver
- `torch` - PyTorch for embeddings
- `transformers` - Hugging Face transformers
- `chromadb` - Vector database
- `pymongo` - MongoDB driver
- `groq` - Groq API client
- `python-dotenv` - Environment variable management

### Step 4: Start FastAPI Backend (Required)

**Open Terminal 1:**

**Option A: Using Python script (Recommended)**
```bash
cd ingestion-phase
python start_api.py
```

**Option B: Using uvicorn directly**
```bash
cd ingestion-phase
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Option C: Using batch file (Windows)**
```bash
cd ingestion-phase
start_api.bat
```

**Option D: Using shell script (Linux/Mac)**
```bash
cd ingestion-phase
chmod +x start_api.sh
./start_api.sh
```

**Expected output:**
```
============================================================
🚀 Starting FastAPI Backend Server
============================================================
📍 Server will be available at: http://localhost:8000
📡 API Documentation: http://localhost:8000/docs
❤️  Health Check: http://localhost:8000/health
============================================================
⏳ Loading models and connecting to databases...
✅ FastAPI backend initialized successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The FastAPI server must remain running.

### Step 5: Start Streamlit Frontend

**Open Terminal 2** (keep FastAPI terminal running):

**Option A: Using Streamlit directly (Recommended)**
```bash
cd ingestion-phase
streamlit run app.py
```

**Option B: Using Python launcher**
```bash
cd ingestion-phase
python run_app.py
```

**Option C: Using batch file (Windows)**
```bash
cd ingestion-phase
start.bat
```

**Option D: Using shell script (Linux/Mac)**
```bash
cd ingestion-phase
chmod +x start.sh
./start.sh
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 6: Access the Application

1. Open your browser and navigate to: `http://localhost:8501`
2. The app will automatically detect if FastAPI is running
3. If FastAPI is detected, you'll see optimal performance
4. If not, the app will work in fallback mode (slower but functional)

## 📋 Complete Startup Checklist

- [ ] Python 3.8+ installed
- [ ] Groq API key obtained and added to `.env` file
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB accessible (connection string configured)
- [ ] FastAPI backend started (Terminal 1) - `python start_api.py`
- [ ] Streamlit frontend started (Terminal 2) - `streamlit run app.py`
- [ ] Browser opened to `http://localhost:8501`

## 🎯 Usage Guide

### 1. Search for a Patient

1. In the sidebar, enter a patient's **Unit Number** or select from dropdown
2. Click **"🔍 Search Patient"**
3. Patient information will appear in the sidebar

### 2. Chat with AI Assistant

1. Once a patient is selected, the chat interface becomes active
2. Type your question in the message box
3. Click **"💬 Send Message"** or press Enter
4. The AI will respond with context about the selected patient

**Example questions:**
- "What are the key findings for this patient?"
- "Generate a discharge summary for this patient"
- "What medications should be prescribed?"

### 3. Generate Discharge Summary

**Method 1: Quick Action Button**
- Click **"📝 Generate Summary"** in the Quick Actions section

**Method 2: Chat Interface**
- Type: "Generate discharge summary" or "Create discharge summary"

The summary will appear in the right panel and can be:
- ✅ Edited directly in the text area
- 💾 Saved with edits
- 📥 Downloaded as TXT, DOCX, or PDF

### 4. Patient Overview

1. Click **"👤 Patient Overview"** to view detailed patient information
2. View formatted patient data in a professional modal
3. Close the overview when done

### 5. Upload Template (Optional)

1. In the sidebar, under **"📎 Insurance Template"**
2. Click **"Browse files"** and select a PDF template
3. The system will extract section headings
4. Generated summaries will follow the template structure

### 6. Feedback Loop

After generating and editing a summary:
1. Click **"Commit Summary to Knowledgebase"**
2. The summary is embedded and added to the RAG system
3. Future searches will include this summary for better results

## 🏗️ Architecture

### System Components

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Streamlit  │ ──────> │   FastAPI    │ ──────> │   Groq API  │
│  Frontend   │  HTTP   │   Backend    │  HTTP   │   (LLM)     │
│  (Port 8501)│         │  (Port 8000) │         │  (Cloud)    │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ├──> MongoDB (Patient Records)
                              └──> ChromaDB (Vector Search)
```

### Technology Stack

- **Frontend**: Streamlit with modern dark theme UI
- **Backend**: FastAPI with async/await for high performance
- **LLM**: Groq API with `meta-llama/llama-4-maverick-17b-128e-instruct` model
- **Embeddings**: Bio ClinicalBERT (medical domain-specific)
- **Vector DB**: ChromaDB for similarity search
- **Database**: MongoDB for patient records
- **AI Agent**: AutoGen for conversational interface

## ⚡ Performance Optimizations

### FastAPI Backend Benefits

- **Async Operations**: Non-blocking I/O for all database and HTTP calls
- **Connection Pooling**: Efficient resource management
- **Concurrent Requests**: Handle multiple requests simultaneously
- **Expected Speed Improvements**:
  - AI Agent responses: **40-60% faster**
  - Discharge summary generation: **30-50% faster**
  - Similar case searches: **50-80% faster** (with caching)

### Groq API Benefits

- **Fast Inference**: Groq's specialized hardware provides very fast responses
- **No Local Setup**: No need to install or run Ollama locally
- **Scalable**: Automatically scales with your usage
- **Production Ready**: Built for production deployments
- **Cost Effective**: Free tier available, pay-as-you-go pricing

## 🎨 UI Features

### Modern Dark Theme

- **Professional Design**: Dark color scheme with gradient accents
- **Smooth Animations**: Slide-in effects, hover transitions
- **Responsive Layout**: Optimized for different screen sizes
- **Status Indicators**: Real-time system status display
- **Progress Bars**: Visual feedback for long operations

### Key UI Components

- **Gradient Header**: Eye-catching main header with glow effects
- **Card-based Layout**: Modern card design with hover effects
- **Chat Interface**: Beautiful message bubbles with avatars
- **Status Cards**: Visual indicators for system health
- **Glassmorphism Effects**: Modern glass-like UI elements

## 📡 API Endpoints (FastAPI)

### Health & Status
- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Core Operations
- `POST /api/chat` - Chat with AI agent
- `POST /api/generate-summary` - Generate discharge summary
- `POST /api/patient` - Get patient by unit number
- `GET /api/patients` - Get all patients list

### API Documentation

When FastAPI is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `ingestion-phase` directory:

```bash
# Groq API Configuration (Required)
GROQ_API_KEY=your_groq_api_key_here

# FastAPI URL (optional, defaults to localhost:8000)
FASTAPI_URL=http://localhost:8000

# MongoDB URI (configured in config.py)
MONGO_URI=your_mongodb_connection_string
```

### Configuration Files

- `config.py` - Main configuration file
- `local_config.json` - Local overrides (optional)
- `.env` - Environment variables (not committed to git)

## 🐛 Troubleshooting

### FastAPI Not Starting

**Problem**: Port 8000 already in use

**Solution**:
```bash
# Windows: Find process using port 8000
netstat -ano | findstr :8000

# Linux/Mac: Find process using port 8000
lsof -i :8000

# Kill the process or change port in start_api.py
```

**Problem**: Dependencies missing

**Solution**:
```bash
pip install -r requirements.txt
```

### Streamlit Not Connecting to FastAPI

**Problem**: Warning "FastAPI backend not available"

**Solutions**:
1. Verify FastAPI is running: Visit http://localhost:8000/health
2. Check both terminals are running (FastAPI + Streamlit)
3. Refresh the Streamlit page (F5)
4. Check firewall settings

### Groq API Issues

**Problem**: "GROQ_API_KEY environment variable is not set"

**Solutions**:
1. Verify `.env` file exists in `ingestion-phase` directory
2. Check `.env` file contains `GROQ_API_KEY=your_key_here` (no quotes)
3. Restart your terminal/IDE after setting the variable
4. Verify the variable: `echo $GROQ_API_KEY` (Linux/Mac) or `echo %GROQ_API_KEY%` (Windows)

**Problem**: "Invalid Groq API key"

**Solutions**:
1. Verify your API key is correct at https://console.groq.com/keys
2. Make sure there are no extra spaces or quotes around the key
3. Regenerate the key if needed

**Problem**: "Groq API rate limit exceeded"

**Solutions**:
1. Wait a few minutes and try again
2. Consider upgrading your Groq plan for higher limits
3. The code includes automatic retry logic with exponential backoff

### Database Connection Issues

**Problem**: MongoDB connection failed

**Solutions**:
1. Verify MongoDB connection string in `config.py`
2. Check network connectivity
3. Verify MongoDB credentials
4. Check if MongoDB server is running

### Model Loading Issues

**Problem**: Bio ClinicalBERT model not loading

**Solutions**:
1. Check internet connection (first download)
2. Verify disk space available
3. Check Hugging Face access
4. Try clearing cache: `rm -rf ~/.cache/huggingface`

## 📁 Project Structure

```
ingestion-phase/
├── app.py                 # Streamlit frontend application
├── api.py                 # FastAPI backend server
├── config.py              # Configuration settings
├── start_api.py           # FastAPI startup script
├── start_api.bat          # Windows batch file for FastAPI
├── start_api.sh           # Linux/Mac script for FastAPI
├── run_app.py             # Streamlit launcher
├── start.bat              # Windows batch file for Streamlit
├── start.sh               # Linux/Mac script for Streamlit
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── README_FASTAPI.md      # FastAPI-specific documentation
├── GROQ_SETUP.md          # Groq API setup guide
├── .env                   # Environment variables (not in git)
├── data/                  # Data files
├── embeddings/            # Generated embeddings
├── processed/             # Processed data
├── scripts/               # Utility scripts
└── vector_db/             # ChromaDB storage
    └── chroma/            # Vector database files
```

## 🔒 Production Considerations

### Security
- [ ] Add authentication/authorization
- [ ] Restrict CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Add rate limiting

### Performance
- [ ] Increase FastAPI workers: `uvicorn api:app --workers 4`
- [ ] Use production ASGI server (Gunicorn + Uvicorn)
- [ ] Implement Redis caching
- [ ] Use CDN for static assets
- [ ] Database connection pooling

### Monitoring
- [ ] Add logging (structured logging)
- [ ] Implement health checks
- [ ] Add metrics collection
- [ ] Set up error tracking
- [ ] Monitor resource usage

### Deployment
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] Load balancing
- [ ] Auto-scaling
- [ ] Backup strategies

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq API Documentation](https://console.groq.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license information here]

## 👥 Authors

[Add author information here]

## 🙏 Acknowledgments

- Bio ClinicalBERT model by Emily Alsentzer
- Groq API for fast LLM inference
- FastAPI by Sebastián Ramírez
- Streamlit team
- ChromaDB team

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the terminal output for error messages
3. Verify all prerequisites are met
4. Check that all services are running:
   - ✅ Groq API (cloud service, no local setup needed)
   - ✅ FastAPI (port 8000)
   - ✅ Streamlit (port 8501)
   - ✅ MongoDB (accessible)

For detailed FastAPI information, see [README_FASTAPI.md](README_FASTAPI.md)

For Groq API setup, see [GROQ_SETUP.md](GROQ_SETUP.md)

---

**Last Updated**: 2024
**Version**: 2.0.0 (with FastAPI backend, Groq API, and modern UI)
