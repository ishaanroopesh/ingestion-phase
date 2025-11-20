#!/bin/bash
# Medical Discharge Summary Assistant - Startup Script

echo "🏥 Starting Medical Discharge Summary Assistant..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Please start it with: ollama serve"
    exit 1
fi

# Start the Streamlit application
echo "🚀 Launching Streamlit application..."
streamlit run app.py --server.port 8501 --server.address localhost
