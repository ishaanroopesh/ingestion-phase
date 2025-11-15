#!/usr/bin/env python3
"""
Medical Discharge Summary Assistant - Launcher Script
This script provides an easy way to launch the Streamlit application with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import torch
        import chromadb
        import pymongo
        import transformers
        import pyautogen
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            llama_models = [m for m in models if "llama3" in m.get("name", "")]
            if llama_models:
                print("✅ Ollama is running with LLaMA 3 model")
                return True
            else:
                print("⚠️ Ollama is running but LLaMA 3 model not found")
                print("Please run: ollama pull llama3")
                return False
        else:
            print("❌ Ollama is not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Ollama is not running")
        print("Please start Ollama: ollama serve")
        return False

def check_directories():
    """Check if required directories exist"""
    required_dirs = ["vector_db", "data", "embeddings", "processed"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"⚠️ Missing directories: {', '.join(missing_dirs)}")
        print("Creating missing directories...")
        for dir_name in missing_dirs:
            Path(dir_name).mkdir(exist_ok=True)
            print(f"✅ Created directory: {dir_name}")
    else:
        print("✅ All required directories exist")
    
    return True

def launch_app():
    """Launch the Streamlit application"""
    print("\n🚀 Launching Medical Discharge Summary Assistant...")
    print("=" * 60)
    
    # Set environment variables for better performance
    env = os.environ.copy()
    env["TOKENIZERS_PARALLELISM"] = "false"  # Avoid tokenizer warnings
    
    try:
        # Launch Streamlit with custom configuration
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light",
            "--theme.primaryColor", "#007bff",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa"
        ], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    
    return True

def main():
    """Main launcher function"""
    print("🏥 Medical Discharge Summary Assistant")
    print("=" * 60)
    
    # Pre-flight checks
    print("\n🔍 Running pre-flight checks...")
    
    checks = [
        ("Requirements", check_requirements),
        ("Ollama Service", check_ollama),
        ("Directories", check_directories)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Pre-flight checks failed. Please resolve the issues above.")
        print("\n💡 Quick fixes:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Start Ollama: ollama serve")
        print("3. Pull LLaMA 3: ollama pull llama3")
        return 1
    
    print("\n✅ All pre-flight checks passed!")
    
    # Launch application
    success = launch_app()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

