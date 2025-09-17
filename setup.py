#!/usr/bin/env python3
"""
Setup script for Medical Discharge Summary Assistant
Handles installation, configuration, and initial setup
"""

import subprocess
import sys
import os
from pathlib import Path
import json

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install Python requirements"""
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python requirements")

def create_directories():
    """Create necessary directories"""
    directories = [
        "vector_db",
        "data", 
        "embeddings",
        "processed",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("❌ Ollama is not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Ollama is not running or not installed")
        print("Please install Ollama from: https://ollama.ai/")
        print("Then run: ollama serve")
        return False

def pull_llama_model():
    """Pull LLaMA 3 model for Ollama"""
    return run_command("ollama pull llama3", "Pulling LLaMA 3 model")

def create_config_file():
    """Create a local configuration file"""
    config = {
        "mongo_uri": "mongodb+srv://ishaanroopesh0102:6eShFuC0pNnFFNGm@cluster0.biujjg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        "chroma_path": "vector_db/chroma",
        "ollama_model": "llama3",
        "ollama_base_url": "http://localhost:11434",
        "num_similar_cases": 3,
        "embedding_max_length": 512
    }
    
    with open("local_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created local configuration file")
    return True

def test_imports():
    """Test if all required packages can be imported"""
    packages = [
        "streamlit",
        "pandas", 
        "torch",
        "chromadb",
        "requests",
        "pymongo",
        "transformers",
        "autogen",
        "numpy",
        "tqdm"
    ]
    
    failed_imports = []
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All packages imported successfully")
    return True

def create_startup_script():
    """Create a startup script for easy launching"""
    startup_script = """#!/bin/bash
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
"""
    
    with open("start.sh", "w") as f:
        f.write(startup_script)
    
    # Make it executable on Unix systems
    if os.name != 'nt':
        os.chmod("start.sh", 0o755)
    
    print("✅ Created startup script: start.sh")
    return True

def main():
    """Main setup function"""
    print("🏥 Medical Discharge Summary Assistant - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        return 1
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        return 1
    
    # Test imports
    if not test_imports():
        print("❌ Some packages failed to import")
        return 1
    
    # Check Ollama
    if not check_ollama_installation():
        print("⚠️ Ollama is not running. Please start it manually.")
        print("Run: ollama serve")
        print("Then: ollama pull llama3")
    else:
        # Pull LLaMA model if Ollama is running
        pull_llama_model()
    
    # Create configuration
    create_config_file()
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Run: python run_app.py")
    print("   or: streamlit run app.py")
    print("3. Open your browser to: http://localhost:8501")
    print("\n📚 For more information, see README.md")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

