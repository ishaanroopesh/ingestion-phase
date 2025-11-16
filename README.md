# 🏥 Medical Discharge Summary Assistant

An AI-powered medical documentation system that generates discharge summaries using RAG (Retrieval-Augmented Generation) architecture with LLaMA 3, integrated with AutoGen for conversational AI assistance.

## ✨ Features

- **🤖 AI-Powered Discharge Summary Generation**: Automatically generates comprehensive discharge summaries using LLaMA 3
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
- Ollama installed and running with LLaMA 3 model
- MongoDB connection (cloud or local)
- CUDA-capable GPU (optional, for faster embeddings)

### Step 1: Install Dependencies

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

### Step 2: Start Ollama (Required)

Make sure Ollama is running with the LLaMA 3 model:

```bash
# Start Ollama server
ollama serve

# In another terminal, pull LLaMA 3 if not already installed
ollama pull llama3
```

### Step 3: Start FastAPI Backend (Recommended for Best Performance)

**Option A: Using the batch file (Windows)**
```bash
start_api.bat
```

**Option B: Using the shell script (Linux/Mac)**
```bash
chmod +x start_api.sh
./start_api.sh
```

**Option C: Using Python directly**
```bash
python start_api.py
```

**Option D: Using uvicorn directly**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
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

### Step 4: Start Streamlit Frontend

**Open a NEW terminal/command prompt** (keep FastAPI terminal running):

**Option A: Using the launcher script**
```bash
python run_app.py
```

**Option B: Using Streamlit directly**
```bash
streamlit run app.py
```

**Option C: Using the batch file (Windows)**
```bash
start.bat
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 5: Access the Application

1. Open your browser and navigate to: `http://localhost:8501`
2. The app will automatically detect if FastAPI is running
3. If FastAPI is detected, you'll see optimal performance
4. If not, the app will work in fallback mode (slower but functional)

## 📋 Complete Startup Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Ollama running with LLaMA 3 model
- [ ] MongoDB accessible (connection string configured)
- [ ] FastAPI backend started (Terminal 1)
- [ ] Streamlit frontend started (Terminal 2)
- [ ] Browser opened to `http://localhost:8501`

## 🎯 Usage Guide

### 1. Search for a Patient

1. In the sidebar, enter a patient's **Unit Number**
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

### 4. Find Similar Cases

1. Click **"🔍 Find Similar Cases"**
2. The system searches for similar patient cases using RAG
3. View similarity scores and case summaries
4. Use for clinical decision support

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
│  Streamlit  │ ──────> │   FastAPI    │ ──────> │   Ollama   │
│  Frontend   │  HTTP   │   Backend    │  HTTP   │   (LLM)    │
│  (Port 8501)│         │  (Port 8000) │         │ (Port 11434)│
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ├──> MongoDB (Patient Records)
                              └──> ChromaDB (Vector Search)
```

### Technology Stack

- **Frontend**: Streamlit with modern dark theme UI
- **Backend**: FastAPI with async/await for high performance
- **LLM**: LLaMA 3 via Ollama
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

### Additional Optimizations

- **Embedding Cache**: Avoids recomputing embeddings for same text
- **Reduced Token Limits**: Optimized for faster responses
  - Chat: 150 tokens (reduced from 250)
  - Summary: 500 tokens (reduced from 700)
- **Lower Temperature**: More deterministic, faster responses
- **Request Timeouts**: Faster failure handling
- **Streaming Responses**: Real-time response generation

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
- **Custom Scrollbars**: Styled scrollbars for better UX

## 📡 API Endpoints (FastAPI)

### Health & Status
- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Core Operations
- `POST /api/chat` - Chat with AI agent
- `POST /api/generate-summary` - Generate discharge summary
- `POST /api/search-similar` - Search similar cases
- `POST /api/patient` - Get patient by unit number

### API Documentation

When FastAPI is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

```bash
# FastAPI URL (optional, defaults to localhost:8000)
export FASTAPI_URL=http://localhost:8000

# MongoDB URI (configured in config.py)
MONGO_URI=your_mongodb_connection_string

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### Configuration Files

- `config.py` - Main configuration file
- `local_config.json` - Local overrides (optional)

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

### Ollama Connection Issues

**Problem**: "Error connecting to Ollama"

**Solutions**:
1. Verify Ollama is running: `ollama serve`
2. Check LLaMA 3 is installed: `ollama list`
3. Pull model if missing: `ollama pull llama3`
4. Verify port 11434 is accessible

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
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── README_FASTAPI.md      # FastAPI-specific documentation
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
- [Ollama Documentation](https://ollama.ai/docs)
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
- LLaMA 3 by Meta
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
   - ✅ Ollama (port 11434)
   - ✅ FastAPI (port 8000)
   - ✅ Streamlit (port 8501)
   - ✅ MongoDB (accessible)

For detailed FastAPI information, see [README_FASTAPI.md](README_FASTAPI.md)

---

**Last Updated**: 2024
**Version**: 2.0.0 (with FastAPI backend and modern UI)
