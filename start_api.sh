#!/bin/bash

echo "========================================"
echo "Starting FastAPI Backend Server"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "ERROR: FastAPI is not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "ERROR: Uvicorn is not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

python3 start_api.py

