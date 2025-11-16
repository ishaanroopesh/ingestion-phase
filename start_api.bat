@echo off
echo ========================================
echo Starting FastAPI Backend Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo ERROR: FastAPI is not installed
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Uvicorn is not installed
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python start_api.py

pause

