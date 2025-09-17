@echo off
REM Medical Discharge Summary Assistant - Windows Startup Script

echo 🏥 Starting Medical Discharge Summary Assistant...

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama is not running. Please start it with: ollama serve
    pause
    exit /b 1
)

REM Start the Streamlit application
echo 🚀 Launching Streamlit application...
streamlit run app.py --server.port 8501 --server.address localhost

pause

