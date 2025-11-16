"""
FastAPI Backend for Medical Discharge Summary Assistant
Provides async endpoints for AI agent and RAG operations
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import httpx
import torch
import chromadb
from motor.motor_asyncio import AsyncIOMotorClient
from transformers import AutoTokenizer, AutoModel
import hashlib
import json
import time
import math
from contextlib import asynccontextmanager
from bson import ObjectId
from bson.errors import InvalidId

# Configuration
MONGO_URI = "mongodb+srv://ishaanroopesh0102:6eShFuC0pNnFFNGm@cluster0.biujjg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHROMA_PATH = "vector_db/chroma"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"

# Global state
embedding_cache = {}
tokenizer = None
model = None
chroma_client = None
chroma_collection = None
mongo_client = None
mongo_db = None
patients_collection = None
http_client = None

# Request models
class ChatRequest(BaseModel):
    message: str
    patient_data: Optional[Dict[str, Any]] = None

class SummaryRequest(BaseModel):
    patient_data: str
    template_outline: Optional[List[str]] = None

class SearchRequest(BaseModel):
    query_text: str
    n_results: int = 3

class PatientRequest(BaseModel):
    unit_no: str

# Initialize models and connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    global tokenizer, model, chroma_client, chroma_collection
    global mongo_client, mongo_db, patients_collection, http_client
    
    # Load models
    print("Loading Bio ClinicalBERT model...")
    tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model.eval()
    if torch.cuda.is_available():
        model.to("cuda")
    
    # Connect to ChromaDB
    print("Connecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_or_create_collection("patient_embeddings")
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    mongo_db = mongo_client["hospital_db"]
    patients_collection = mongo_db["test_patients"]
    
    # Create async HTTP client
    http_client = httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
    )
    
    print("✅ FastAPI backend initialized successfully!")
    
    yield
    
    # Cleanup
    if http_client:
        await http_client.aclose()
    if mongo_client:
        mongo_client.close()
    print("✅ FastAPI backend shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Medical Discharge Summary API",
    description="Fast async API for medical RAG and AI agent operations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def get_text_hash(text: str) -> str:
    """Generate hash for text to use as cache key"""
    return hashlib.md5(text.encode()).hexdigest()

async def embed_text_async(text: str) -> List[float]:
    """Generate embedding for text using Bio ClinicalBERT with caching"""
    # Check cache first
    text_hash = get_text_hash(text)
    if text_hash in embedding_cache:
        return embedding_cache[text_hash]
    
    # Generate embedding (run in thread pool to avoid blocking)
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(
        None,
        lambda: _generate_embedding(text)
    )
    
    # Cache the embedding
    embedding_cache[text_hash] = embedding
    return embedding

def _generate_embedding(text: str) -> List[float]:
    """Synchronous embedding generation"""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        emb = cls_embedding.squeeze(0)
        if emb.is_cuda:
            emb = emb.to("cpu")
        return emb.tolist()

async def check_ollama_available() -> bool:
    """Check if Ollama is running and accessible"""
    try:
        response = await http_client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
        return response.status_code == 200
    except:
        return False

async def call_ollama_async(messages: List[Dict], options: Dict = None) -> str:
    """Async call to Ollama API"""
    # Check if Ollama is available first
    if not await check_ollama_available():
        raise HTTPException(
            status_code=503, 
            detail="Ollama service is not available. Please ensure Ollama is running (run 'ollama serve' in a terminal)."
        )
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True
    }
    if options:
        payload["options"] = options
    
    try:
        response = await http_client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=30.0
        )
        
        # Check for server errors
        if response.status_code == 500:
            raise HTTPException(
                status_code=503,
                detail="Ollama server returned an error. Please check if the LLaMA 3 model is installed (run 'ollama pull llama3')."
            )
        
        response.raise_for_status()
        
        full_response = ""
        async for line in response.aiter_lines():
            if not line:
                continue
            try:
                json_data = json.loads(line)
                if 'message' in json_data and 'content' in json_data['message']:
                    content = json_data['message']['content']
                    if content:
                        full_response += content
                if json_data.get('done', False):
                    break
            except json.JSONDecodeError:
                continue
        
        return full_response.strip()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to Ollama timed out. The model may be too large or the system is overloaded.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            raise HTTPException(
                status_code=503,
                detail="Ollama server error. Please check: 1) Ollama is running ('ollama serve'), 2) LLaMA 3 model is installed ('ollama pull llama3'), 3) System has enough resources."
            )
        raise HTTPException(status_code=502, detail=f"Error connecting to Ollama: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to Ollama at {OLLAMA_BASE_URL}. Please ensure Ollama is running (run 'ollama serve' in a terminal)."
        )

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Medical Discharge Summary API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "mongodb": "connected" if mongo_client else "disconnected",
        "chromadb": "connected" if chroma_client else "disconnected",
        "model": "loaded" if model else "not loaded",
        "cache_size": len(embedding_cache)
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with AI agent - optimized for speed"""
    try:
        # Check if user is asking for discharge summary
        if "discharge summary" in request.message.lower() or "generate summary" in request.message.lower():
            if request.patient_data:
                patient_text = format_patient_fields(request.patient_data)
                summary = await generate_summary_async(patient_text)
                return {"response": summary}
            else:
                return {"response": "❌ Please select a patient first to generate a discharge summary."}
        
        # Add patient context if available
        context = ""
        if request.patient_data:
            context = f"\n\nPatient: {request.patient_data.get('name', 'Unknown')} (Unit {request.patient_data.get('unit no', 'N/A')})"
        
        system_prompt = "You are a medical AI assistant. Provide concise, accurate responses. Keep answers brief (2-3 sentences max)."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{request.message}{context}"}
        ]
        
        options = {
            "temperature": 0.4,
            "top_p": 0.85,
            "max_tokens": 150,
            "num_predict": 150
        }
        
        response = await call_ollama_async(messages, options)
        return {"response": response if response else "I'm here to help with medical questions. How can I assist you?"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.post("/api/generate-summary")
async def generate_summary(request: SummaryRequest):
    """Generate discharge summary - async optimized"""
    try:
        if request.template_outline:
            summary = await generate_summary_with_template_async(request.patient_data, request.template_outline)
        else:
            summary = await generate_summary_async(request.patient_data)
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

async def generate_summary_async(patient_data: str) -> str:
    """Generate discharge summary using Ollama LLM"""
    system_prompt = """You are an expert medical AI assistant that generates structured, clinically accurate discharge summaries.
Base your summary entirely on the INPUT PATIENT DATA provided.
The discharge summary MUST include: Name, Unit No, Date Of Birth, Sex, Admission/Discharge Dates, Attending, Chief Complaint, Procedure, History, Physical Exam (on Admission), Pertinent Results, Brief Hospital Course, Medications on Admission, Discharge Medications, Discharge Instructions, Discharge Disposition, Discharge Diagnosis, Discharge Condition, Follow-up.

For Name, Unit No, Date of Birth, and Sex, copy the information verbatim.
If information is missing, state "[Information not available]".
Use concise, professional medical language. Be brief and factual."""

    user_prompt = f"""Generate a discharge summary for this patient:
{patient_data}

Extract Name, Unit No, Date of Birth, and Sex exactly as provided."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    options = {
        "temperature": 0.3,
        "top_p": 0.85,
        "max_tokens": 500,
        "num_predict": 500
    }
    
    return await call_ollama_async(messages, options)

async def generate_summary_with_template_async(patient_data: str, outline_sections: List[str]) -> str:
    """Generate discharge summary following template outline"""
    outline_bullets = "\n".join([f"- {s}" for s in outline_sections])
    system_prompt = f"""You are an expert medical AI assistant that generates a clinically accurate discharge summary.
Follow the section order EXACTLY as specified by the provided outline. Do not add extra sections; if information is missing, write "[Information not available]".

REQUIRED SECTION ORDER (USE EXACT TITLES):
{outline_bullets}

Rules:
- Use concise, professional medical language.
- Base content solely on the input patient data.
- Preserve patient identifiers verbatim if present.
- Be brief and factual."""

    user_prompt = f"""Generate a discharge summary STRICTLY following the section list above, based only on this data:\n\n{patient_data}\n\nReturn plain text with the exact section headings in order."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    options = {
        "temperature": 0.3,
        "top_p": 0.85,
        "max_tokens": 500,
        "num_predict": 500
    }
    
    return await call_ollama_async(messages, options)

@app.post("/api/search-similar")
async def search_similar(request: SearchRequest):
    """Search for similar cases using RAG - async optimized"""
    try:
        # Generate embedding
        query_embedding = await embed_text_async(request.query_text)
        
        # Search ChromaDB (run in thread pool since it's synchronous)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=request.n_results,
                include=["documents", "metadatas"]
            )
        )
        
        similar_cases = []
        for i in range(len(results["documents"][0])):
            similar_cases.append({
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity": 1 - results["distances"][0][i]
            })
        
        return {"similar_cases": similar_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching similar cases: {str(e)}")

@app.post("/api/patient")
async def get_patient(request: PatientRequest):
    """Get patient by unit number"""
    try:
        # Try to convert unit_no to int
        try:
            unit_no_int = int(request.unit_no)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid unit number format")
        
        # Query MongoDB
        patient = await patients_collection.find_one({"unit no": unit_no_int})
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Clean the patient data (handle NaN, ObjectId, etc.)
        cleaned_patient = clean_patient_data(patient)
        
        return {"patient": cleaned_patient}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patient: {str(e)}")

def clean_patient_data(patient: Dict) -> Dict:
    """Clean patient data for JSON serialization - handle NaN, ObjectId, etc."""
    cleaned = {}
    for key, value in patient.items():
        # Handle NaN values
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            cleaned[key] = None
        # Handle ObjectId
        elif isinstance(value, ObjectId):
            cleaned[key] = str(value)
        # Handle nested dictionaries
        elif isinstance(value, dict):
            cleaned[key] = clean_patient_data(value)
        # Handle lists
        elif isinstance(value, list):
            cleaned[key] = [
                clean_patient_data(item) if isinstance(item, dict) else 
                (None if isinstance(item, float) and (math.isnan(item) or math.isinf(item)) else item)
                for item in value
            ]
        # Handle other types
        else:
            cleaned[key] = value
    return cleaned

def format_patient_fields(record: Dict) -> str:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


