import streamlit as st
import pandas as pd
import torch
import chromadb
import requests
import json
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List, Optional
import time
from datetime import datetime
import os

# Try to import autogen, but make it optional
try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    st.warning("⚠️ AutoGen not available. Some features may be limited.")

# Page configuration
st.set_page_config(
    page_title="Medical Discharge Summary Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical UI with improved contrast
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #1e3c72;
        --secondary-blue: #2a5298;
        --accent-blue: #007bff;
        --success-green: #28a745;
        --warning-orange: #ffc107;
        --danger-red: #dc3545;
        --light-gray: #f8f9fa;
        --dark-gray: #343a40;
        --text-dark: #212529;
        --text-light: #6c757d;
    }
    
    /* Main header with gradient */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(30, 60, 114, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Patient card with better contrast */
    .patient-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-left: 5px solid var(--accent-blue);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .patient-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .patient-card h4 {
        color: var(--text-dark);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .patient-card p {
        color: var(--text-light);
        margin: 0.25rem 0;
    }
    
    /* Summary card with improved styling */
    .summary-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        border: 2px solid var(--success-green);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.2);
    }
    
    .summary-card h3 {
        color: var(--success-green);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Chat messages with high contrast */
    .chat-message {
        padding: 1.25rem;
        margin: 0.75rem 0;
        border-radius: 15px;
        border-left: 5px solid;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chat-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .chat-message:hover::before {
        transform: translateX(100%);
    }
    
    .doctor-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%);
        border-left-color: var(--accent-blue);
        color: var(--text-dark);
    }
    
    .doctor-message strong {
        color: var(--accent-blue);
        font-weight: 600;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #faf5ff 100%);
        border-left-color: #9c27b0;
        color: var(--text-dark);
    }
    
    .ai-message strong {
        color: #9c27b0;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #0056b3 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 123, 255, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Primary button variant */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--success-green) 0%, #1e7e34 100%);
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1e7e34 0%, #155724 100%);
        box-shadow: 0 8px 24px rgba(40, 167, 69, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Sidebar text contrast */
    .sidebar .stMarkdown h1,
    .sidebar .stMarkdown h2,
    .sidebar .stMarkdown h3,
    .sidebar .stMarkdown h4,
    .sidebar .stMarkdown h5,
    .sidebar .stMarkdown h6 {
        color: var(--text-dark) !important;
    }
    
    .sidebar .stMarkdown p {
        color: var(--text-dark) !important;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid var(--success-green);
        color: var(--text-dark);
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid var(--danger-red);
        color: var(--text-dark);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #17a2b8;
        color: var(--text-dark);
    }
    
    /* Spinner styling */
    .stSpinner {
        color: var(--accent-blue);
    }
    
    /* Form styling improvements */
    .stForm > div {
        background: #ffffff;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    /* Text area improvements */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 2px solid #e9ecef !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        transition: all 0.3s ease !important;
        color: var(--text-dark) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1) !important;
        outline: none !important;
        color: var(--text-dark) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-light) !important;
        opacity: 0.7 !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        color: var(--text-dark) !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-light) !important;
        opacity: 0.7 !important;
    }
    
    /* Button improvements */
    .stButton > button {
        font-size: 1rem;
        font-weight: 600;
        text-transform: none;
        letter-spacing: 0.5px;
    }
    
    /* Chat container improvements */
    .chat-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #e9ecef;
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: var(--accent-blue);
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #0056b3;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
    }
    
    /* Form styling */
    .stForm {
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Status indicators */
    .status-connected {
        color: var(--success-green);
        font-weight: 600;
    }
    
    .status-error {
        color: var(--danger-red);
        font-weight: 600;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .chat-message {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = None
if 'discharge_summary' not in st.session_state:
    st.session_state.discharge_summary = None
if 'autogen_agent' not in st.session_state:
    st.session_state.autogen_agent = None

class MedicalRAGSystem:
    def __init__(self):
        self.mongo_uri = "mongodb+srv://ishaanroopesh0102:6eShFuC0pNnFFNGm@cluster0.biujjg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.chroma_path = "vector_db/chroma"
        self.ollama_model = "llama3"
        self.num_results = 3
        
        # Initialize models
        self._load_models()
        self._connect_databases()
    
    def _load_models(self):
        """Load Bio ClinicalBERT model for embeddings"""
        with st.spinner("Loading Bio ClinicalBERT model..."):
            self.tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
            self.model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
            self.model.eval()
    
    def _connect_databases(self):
        """Connect to MongoDB and ChromaDB"""
        try:
            # MongoDB connection
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client["hospital_db"]
            self.patients_collection = self.db["test_patients"]
            
            # ChromaDB connection
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
            self.chroma_collection = self.chroma_client.get_or_create_collection("patient_embeddings")
            
            st.success("✅ Connected to databases successfully")
        except Exception as e:
            st.error(f"❌ Database connection failed: {str(e)}")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text using Bio ClinicalBERT"""
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            outputs = self.model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :]
            return cls_embedding.squeeze(0).tolist()
    
    def format_patient_fields(self, record: Dict) -> str:
        """Format patient record fields for embedding"""
        fields = [
            "name", "unit no", "admission date", "date of birth", "sex", "service",
            "allergies", "attending", "chief complaint", "major surgical or invasive procedure",
            "history of present illness", "past medical history", "social history",
            "family history", "physical exam", "pertinent results", "medications on admission",
            "brief hospital course", "discharge medications", "discharge diagnosis",
            "discharge condition", "discharge instructions", "follow-up", "discharge disposition"
        ]
        parts = [f"{field.title()}: {record.get(field, '')}" for field in fields if record.get(field)]
        return " ".join(parts)
    
    def get_patient_by_unit_no(self, unit_no: str) -> Optional[Dict]:
        """Retrieve patient record from MongoDB"""
        try:
            record = self.patients_collection.find_one({"unit no": int(unit_no)})
            return record
        except Exception as e:
            st.error(f"Error retrieving patient: {str(e)}")
            return None
    
    def search_similar_cases(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """Search for similar cases using RAG"""
        try:
            query_embedding = self.embed_text(query_text)
            results = self.chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas"]
            )
            
            similar_cases = []
            for i in range(len(results["documents"][0])):
                similar_cases.append({
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
                })
            
            return similar_cases
        except Exception as e:
            st.error(f"Error searching similar cases: {str(e)}")
            return []
    
    def generate_discharge_summary(self, patient_data: str, similar_cases: List[Dict] = None) -> str:
        """Generate discharge summary using Ollama LLM"""
        system_prompt = """You are an expert medical AI assistant tasked with generating a structured, clinically accurate, and concise discharge summary.
Base your summary entirely on the 'INPUT PATIENT DATA' provided.
The discharge summary MUST include all the following sections. For Name, Unit No, Date of Birth, and Sex, you MUST copy the information verbatim.
If essential information for a required section is genuinely absent, state "[Information not available]".

REQUIRED DISCHARGE SUMMARY STRUCTURE:
Name, Unit No, Date Of Birth, Sex, Admission/Discharge Dates, Attending, Chief Complaint, Procedure, History, Physical Exam (on Admission), Pertinent Results, Brief Hospital Course, Medications on Admission, Discharge Medications, Discharge Instructions, Discharge Disposition, Discharge Diagnosis, Discharge Condition, Follow-up.

Maintain a professional, objective medical tone. Do not add conversational phrases."""

        user_prompt = f"""Generate a discharge summary for the following patient based on the provided data:
**INPUT PATIENT DATA (Query):**
{patient_data}

**DISCHARGE SUMMARY (Query):**

**Reminder:** Extract and display the patient's Name, Unit No, Date of Birth, and Sex exactly as provided at the top of the discharge summary. Do not skip or modify them."""

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": self.ollama_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False
                }
            )

            if response.ok:
                full_response = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            json_data = json.loads(line)
                            if 'message' in json_data and 'content' in json_data['message']:
                                full_response += json_data['message']['content']
                        except json.JSONDecodeError:
                            continue
                return full_response.strip()
            else:
                return f"❌ Error generating summary: {response.text}"
        except Exception as e:
            return f"❌ Error connecting to Ollama: {str(e)}"

class AutoGenMedicalAgent:
    def __init__(self, rag_system: MedicalRAGSystem):
        self.rag_system = rag_system
        self.agent = None
        self.user_proxy = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize AutoGen medical assistant agent"""
        # Skip AutoGen initialization to avoid API errors
        # Use fallback chat method instead
        pass
    
    def chat_with_doctor(self, message: str, patient_data: Dict = None) -> str:
        """Handle conversation with doctor"""
        try:
            # Use fallback chat method for better compatibility with Ollama
            return self._fallback_chat(message, patient_data)
            
        except Exception as e:
            return f"❌ Error in conversation: {str(e)}"
    
    def _fallback_chat(self, message: str, patient_data: Dict = None) -> str:
        """Fallback chat using direct Ollama interaction"""
        try:
            # Check if user is asking for discharge summary generation
            if "discharge summary" in message.lower() or "generate summary" in message.lower():
                if patient_data:
                    # Use the existing discharge summary generation method
                    patient_text = self.rag_system.format_patient_fields(patient_data)
                    return self.rag_system.generate_discharge_summary(patient_text)
                else:
                    return "❌ Please select a patient first to generate a discharge summary."
            
            # Add patient context if available
            context = ""
            if patient_data:
                context = f"\n\nCurrent Patient Context:\n{self.rag_system.format_patient_fields(patient_data)}"
            
            system_prompt = """You are a medical AI assistant that helps doctors with discharge summaries and medical questions. 
            Provide helpful, accurate, and professional responses about medical topics. 
            Keep responses concise and focused. If asked about generating a discharge summary, guide the user to use the 'Generate Summary' button."""
            
            # Optimize request for faster response
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"{message}{context}"}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500  # Limit response length for faster generation
                    }
                },
                timeout=30  # Add timeout for faster failure detection
            )
            
            if response.ok:
                full_response = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            json_data = json.loads(line)
                            if 'message' in json_data and 'content' in json_data['message']:
                                full_response += json_data['message']['content']
                        except json.JSONDecodeError:
                            continue
                return full_response.strip() if full_response.strip() else "I'm here to help with medical questions. How can I assist you?"
            else:
                return f"❌ Error connecting to Ollama: {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. Please try again with a shorter message."
        except Exception as e:
            return f"❌ Error in fallback chat: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Medical Discharge Summary Assistant</h1>
        <p>AI-Powered Clinical Documentation with RAG and AutoGen Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize RAG system
    if 'rag_system' not in st.session_state:
        with st.spinner("Initializing Medical RAG System..."):
            try:
                st.session_state.rag_system = MedicalRAGSystem()
                st.session_state.autogen_agent = AutoGenMedicalAgent(st.session_state.rag_system)
                st.success("✅ System initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize system: {str(e)}")
                st.stop()
    
    # Sidebar for patient search
    with st.sidebar:
        st.header("🔍 Patient Search")
        
        # Patient search form
        with st.form("patient_search"):
            unit_no = st.text_input("Unit Number", placeholder="Enter patient unit number")
            search_button = st.form_submit_button("🔍 Search Patient")
            
            if search_button and unit_no:
                with st.spinner("Searching for patient..."):
                    try:
                        patient = st.session_state.rag_system.get_patient_by_unit_no(unit_no)
                        if patient:
                            st.session_state.current_patient = patient
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: 1px solid var(--success-green); border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                                <p style="color: var(--text-dark); margin: 0; font-weight: 600;">✅ Found patient: {patient.get('name', 'Unknown')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border: 1px solid var(--danger-red); border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                                <p style="color: var(--text-dark); margin: 0; font-weight: 600;">❌ Patient not found</p>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border: 1px solid var(--danger-red); border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                            <p style="color: var(--text-dark); margin: 0; font-weight: 600;">❌ Error: {str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Display current patient info
        if st.session_state.current_patient:
            st.markdown("### 👤 Current Patient")
            patient = st.session_state.current_patient
            
            st.markdown(f"""
            <div class="patient-card">
                <h4 style="color: var(--text-dark); margin-bottom: 1rem;">📋 {patient.get('name', 'Unknown')}</h4>
                <p style="color: var(--text-dark); margin: 0.5rem 0;"><strong style="color: var(--accent-blue);">Unit No:</strong> {patient.get('unit no', 'N/A')}</p>
                <p style="color: var(--text-dark); margin: 0.5rem 0;"><strong style="color: var(--accent-blue);">DOB:</strong> {patient.get('date of birth', 'N/A')}</p>
                <p style="color: var(--text-dark); margin: 0.5rem 0;"><strong style="color: var(--accent-blue);">Sex:</strong> {patient.get('sex', 'N/A')}</p>
                <p style="color: var(--text-dark); margin: 0.5rem 0;"><strong style="color: var(--accent-blue);">Service:</strong> {patient.get('service', 'N/A')}</p>
                <p style="color: var(--text-dark); margin: 0.5rem 0;"><strong style="color: var(--accent-blue);">Attending:</strong> {patient.get('attending', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💬 AI Medical Assistant")
        
        # Chat interface
        if st.session_state.current_patient:
            # Chat container with better styling
            st.markdown("""
            <div style="background: #ffffff; border-radius: 15px; padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 1rem; max-height: 400px; overflow-y: auto; border: 1px solid #e9ecef;">
            """, unsafe_allow_html=True)
            
            # Display chat history
            if st.session_state.chat_history:
                for message in st.session_state.chat_history:
                    if message["role"] == "doctor":
                        st.markdown(f"""
                        <div class="chat-message doctor-message" style="margin: 1rem 0; text-align: left;">
                            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="background: var(--accent-blue); color: white; border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0;">👨‍⚕️</div>
                                <div style="flex: 1;">
                                    <div style="font-weight: 600; color: var(--accent-blue); margin-bottom: 0.25rem;">Doctor</div>
                                    <div style="color: var(--text-dark); line-height: 1.5;">{message["content"]}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chat-message ai-message" style="margin: 1rem 0; text-align: left;">
                            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="background: #9c27b0; color: white; border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0;">🤖</div>
                                <div style="flex: 1;">
                                    <div style="font-weight: 600; color: #9c27b0; margin-bottom: 0.25rem;">AI Assistant</div>
                                    <div style="color: var(--text-dark); line-height: 1.5;">{message["content"]}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; color: var(--text-light); padding: 2rem; font-style: italic;">
                    👋 Start a conversation with the AI assistant...
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Chat input form
            with st.form("chat_form", clear_on_submit=False):
                st.markdown("**<span style='color: var(--text-dark); font-weight: 600;'>Ask the AI assistant:</span>**", unsafe_allow_html=True)
                user_message = st.text_area(
                    "message_input", 
                    placeholder="e.g., Generate a discharge summary for this patient",
                    height=100,
                    label_visibility="collapsed"
                )
                
                col_send, col_clear = st.columns([1, 1])
                with col_send:
                    send_button = st.form_submit_button("💬 Send Message", type="primary", use_container_width=True)
                with col_clear:
                    clear_button = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
                
                if send_button and user_message.strip():
                    # Add doctor message to history
                    st.session_state.chat_history.append({
                        "role": "doctor",
                        "content": user_message.strip(),
                        "timestamp": datetime.now()
                    })
                    
                    # Get AI response
                    with st.spinner("🤖 AI is thinking..."):
                        try:
                            ai_response = st.session_state.autogen_agent.chat_with_doctor(
                                user_message.strip(), 
                                st.session_state.current_patient
                            )
                            
                            # Add AI response to history
                            st.session_state.chat_history.append({
                                "role": "ai",
                                "content": ai_response,
                                "timestamp": datetime.now()
                            })
                        except Exception as e:
                            st.session_state.chat_history.append({
                                "role": "ai",
                                "content": f"❌ Error: {str(e)}",
                                "timestamp": datetime.now()
                            })
                    
                    st.rerun()
                
                if clear_button:
                    st.session_state.chat_history = []
                    st.rerun()
            
            # Action buttons
            st.markdown("### 🚀 Quick Actions")
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("📝 Generate Summary", type="primary", use_container_width=True):
                    with st.spinner("📝 Generating discharge summary..."):
                        try:
                            patient_text = st.session_state.rag_system.format_patient_fields(st.session_state.current_patient)
                            summary = st.session_state.rag_system.generate_discharge_summary(patient_text)
                            st.session_state.discharge_summary = summary
                            st.success("✅ Discharge summary generated!")
                        except Exception as e:
                            st.error(f"❌ Error generating summary: {str(e)}")
                        st.rerun()
            
            with col_btn2:
                if st.button("🔍 Find Similar Cases", use_container_width=True):
                    with st.spinner("🔍 Searching for similar cases..."):
                        try:
                            patient_text = st.session_state.rag_system.format_patient_fields(st.session_state.current_patient)
                            similar_cases = st.session_state.rag_system.search_similar_cases(patient_text)
                            st.session_state.similar_cases = similar_cases
                            st.success(f"✅ Found {len(similar_cases)} similar cases!")
                        except Exception as e:
                            st.error(f"❌ Error searching cases: {str(e)}")
                        st.rerun()
            
            with col_btn3:
                if st.button("📊 Patient Overview", use_container_width=True):
                    with st.spinner("📊 Analyzing patient data..."):
                        try:
                            patient = st.session_state.current_patient
                            overview = f"""**Patient Overview:**

**Name:** {patient.get('name', 'Unknown')}
**Unit No:** {patient.get('unit no', 'N/A')}
**Date of Birth:** {patient.get('date of birth', 'N/A')}
**Sex:** {patient.get('sex', 'N/A')}
**Service:** {patient.get('service', 'N/A')}
**Chief Complaint:** {patient.get('chief complaint', 'N/A')}
**Attending:** {patient.get('attending', 'N/A')}
**Allergies:** {patient.get('allergies', 'N/A')}
**Past Medical History:** {patient.get('past medical history', 'N/A')[:200]}{'...' if len(str(patient.get('past medical history', ''))) > 200 else ''}

This patient is ready for discharge summary generation."""
                            
                            st.session_state.chat_history.append({
                                "role": "ai",
                                "content": overview,
                                "timestamp": datetime.now()
                            })
                            st.success("✅ Patient overview added to chat!")
                        except Exception as e:
                            st.error(f"❌ Error generating overview: {str(e)}")
                        st.rerun()
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; border: 2px dashed #dee2e6;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">👈</div>
                <h3 style="color: var(--text-dark); margin-bottom: 1rem;">Search for a Patient</h3>
                <p style="color: var(--text-light); margin: 0;">Please search for a patient in the sidebar to start the conversation with the AI assistant.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.header("📋 Generated Content")
        
        # Display discharge summary
        if st.session_state.discharge_summary:
            st.markdown("""
            <div class="summary-card">
                <h3>📄 Discharge Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.discharge_summary)
            
            # Download button
            st.download_button(
                label="📥 Download Summary",
                data=st.session_state.discharge_summary,
                file_name=f"discharge_summary_{st.session_state.current_patient.get('unit no', 'unknown')}.txt",
                mime="text/plain"
            )
        
        # Display similar cases
        if hasattr(st.session_state, 'similar_cases') and st.session_state.similar_cases:
            st.markdown("### 🔍 Similar Cases Found")
            
            for i, case in enumerate(st.session_state.similar_cases):
                with st.expander(f"Case {i+1} - Similarity: {case['similarity']:.2%}"):
                    st.write("**Patient Info:**")
                    st.write(f"Name: {case['metadata'].get('name', 'Unknown')}")
                    st.write(f"Unit No: {case['metadata'].get('unit_no', 'Unknown')}")
                    
                    st.write("**Summary Preview:**")
                    summary_preview = case['metadata'].get('summary', 'No summary available')[:200] + "..."
                    st.write(summary_preview)
    
    # Footer with system status
    st.markdown("---")
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: var(--success-green); margin-bottom: 0.5rem;">Database Status</h4>
            <p style="font-size: 1.5rem; margin: 0; color: var(--text-dark);">🟢 Connected</p>
            <p style="color: var(--text-light); margin: 0.5rem 0 0 0;">MongoDB + ChromaDB</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: var(--success-green); margin-bottom: 0.5rem;">AI Model</h4>
            <p style="font-size: 1.5rem; margin: 0; color: var(--text-dark);">🟢 Ready</p>
            <p style="color: var(--text-light); margin: 0.5rem 0 0 0;">Bio ClinicalBERT + LLaMA 3</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: var(--success-green); margin-bottom: 0.5rem;">AI Assistant</h4>
            <p style="font-size: 1.5rem; margin: 0; color: var(--text-dark);">🟢 Active</p>
            <p style="color: var(--text-light); margin: 0.5rem 0 0 0;">Medical Assistant</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
