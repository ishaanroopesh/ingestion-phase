# Medical Discharge Summary Assistant

A sophisticated AI-powered medical application that generates discharge summaries using RAG (Retrieval-Augmented Generation) and Microsoft AutoGen for conversational AI interactions with doctors.

## 🏥 Features

- **AI-Powered Discharge Summary Generation**: Uses LLaMA 3 via Ollama for generating comprehensive medical discharge summaries
- **RAG System**: Retrieves similar patient cases using Bio ClinicalBERT embeddings stored in ChromaDB
- **Conversational AI**: Microsoft AutoGen integration for natural doctor-AI interactions
- **Patient Database**: MongoDB integration for patient record management
- **Professional UI**: Modern Streamlit interface designed for medical professionals
- **Real-time Chat**: Interactive chat interface for doctor-AI collaboration

## 🚀 Quick Start

### Prerequisites

1. **Ollama with LLaMA 3**: Make sure Ollama is running with LLaMA 3 model
   ```bash
   ollama pull llama3
   ollama serve
   ```

2. **Python 3.8+**: Ensure you have Python 3.8 or higher installed

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
# Navigate to the project directory
cd rag_application/ingestion-phase

# Run the automated setup
python setup.py

# Start the application
python run_app.py
```

#### Option 2: Manual Setup
```bash
# Navigate to the project directory
cd rag_application/ingestion-phase

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p vector_db data embeddings processed logs temp

# Start Ollama (if not already running)
ollama serve

# Pull LLaMA 3 model
ollama pull llama3

# Run the application
streamlit run app.py
```

#### Option 3: Quick Start Scripts
- **Windows**: Double-click `start.bat`
- **Linux/Mac**: Run `./start.sh`

### Access the Application
Open your browser to `http://localhost:8501`

### Test the System
Run the demo to verify everything is working:
```bash
python demo.py
```

## 🏗️ Architecture

### Core Components

1. **MedicalRAGSystem**: 
   - Bio ClinicalBERT for medical text embeddings
   - ChromaDB for vector storage and similarity search
   - MongoDB for patient record management
   - Ollama integration for LLM inference

2. **AutoGenMedicalAgent**:
   - Microsoft AutoGen conversational AI agent
   - Specialized for medical discharge summary assistance
   - Context-aware responses with patient data integration

3. **Streamlit Frontend**:
   - Professional medical UI design
   - Real-time chat interface
   - Patient search and management
   - Discharge summary generation and download

### Data Flow

```
Doctor Input → AutoGen Agent → RAG System → ChromaDB/MongoDB → LLM → Discharge Summary
```

## 📊 Usage

### 1. Patient Search
- Enter a patient's unit number in the sidebar
- The system retrieves patient information from MongoDB
- Patient details are displayed in the sidebar

### 2. AI Conversation
- Chat with the AI assistant about the patient
- Ask questions, request summaries, or discuss treatment plans
- The AI has access to patient data and similar cases

### 3. Discharge Summary Generation
- Click "Generate Summary" to create a comprehensive discharge summary
- The system uses RAG to find similar cases for context
- Summary follows standard medical documentation format

### 4. Similar Cases Search
- Find similar patient cases using semantic search
- View similarity scores and case summaries
- Use for clinical decision support

## 🔧 Configuration

### Environment Variables
- `MONGO_URI`: MongoDB connection string
- `CHROMA_PATH`: Path to ChromaDB storage
- `OLLAMA_MODEL`: LLM model name (default: "llama3")

### Model Configuration
- **Bio ClinicalBERT**: Pre-trained medical embeddings
- **LLaMA 3**: Large language model for text generation
- **ChromaDB**: Vector database for similarity search

## 📁 Project Structure

```
rag_application/ingestion-phase/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Patient datasets
├── embeddings/           # Pre-computed embeddings
├── processed/            # Processed training data
├── scripts/              # Jupyter notebooks and utilities
└── vector_db/            # ChromaDB storage
```

## 🎯 Key Features

### Medical AI Assistant
- **Context-Aware**: Understands current patient context
- **Professional**: Uses medical terminology and standards
- **Comprehensive**: Generates complete discharge summaries
- **Interactive**: Natural conversation with doctors

### RAG System
- **Semantic Search**: Finds clinically relevant similar cases
- **Medical Embeddings**: Bio ClinicalBERT for medical text understanding
- **Vector Database**: Efficient similarity search with ChromaDB
- **Context Integration**: Uses similar cases to improve summary quality

### User Interface
- **Professional Design**: Medical-grade UI with clean aesthetics
- **Real-time Chat**: Instant AI responses
- **Patient Management**: Easy patient search and information display
- **Export Functionality**: Download discharge summaries

## 🔒 Security & Privacy

- **Local Processing**: All AI processing happens locally
- **Secure Database**: MongoDB with authentication
- **No External APIs**: Uses local Ollama instance
- **HIPAA Considerations**: Designed for medical data handling

## 🚀 Advanced Features

### AutoGen Integration
- **Multi-Agent System**: Extensible agent architecture
- **Conversation Memory**: Maintains context across interactions
- **Specialized Agents**: Medical domain-specific AI assistants

### RAG Enhancements
- **Dynamic Retrieval**: Real-time similar case search
- **Contextual Embeddings**: Patient-specific embedding generation
- **Similarity Scoring**: Confidence metrics for retrieved cases

## 📈 Performance

- **Fast Embeddings**: Bio ClinicalBERT optimized for medical text
- **Efficient Search**: ChromaDB for sub-second similarity search
- **Streaming Responses**: Real-time LLM generation
- **Caching**: Session state management for performance

## 🛠️ Development

### Adding New Features
1. Extend `MedicalRAGSystem` class for new functionality
2. Add new AutoGen agents for specialized tasks
3. Update Streamlit UI components as needed

### Customization
- **UI Themes**: Modify CSS in `app.py`
- **Model Selection**: Change LLM model in configuration
- **Database Schema**: Adapt to your patient data structure

## 📞 Support

For technical support or feature requests, please refer to the project documentation or contact the development team.

## 📄 License

This project is designed for medical research and clinical use. Please ensure compliance with local healthcare regulations and data protection laws.

---

**⚠️ Medical Disclaimer**: This application is designed to assist healthcare professionals and should not replace clinical judgment. Always verify AI-generated content and follow established medical protocols.
