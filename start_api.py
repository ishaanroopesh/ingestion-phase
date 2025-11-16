#!/usr/bin/env python3
"""
Start FastAPI backend server
"""

import uvicorn
import sys
from pathlib import Path
import socket

def check_port_available(port: int) -> bool:
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

if __name__ == "__main__":
    port = 8000
    
    # Check if port is available
    if not check_port_available(port):
        print(f"⚠️  Port {port} is already in use!")
        print("   Another instance might be running, or another application is using this port.")
        print("   You can:")
        print("   1. Stop the other application using port 8000")
        print("   2. Or modify the port in this script")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 Starting FastAPI Backend Server")
    print("=" * 60)
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"📡 API Documentation: http://localhost:{port}/docs")
    print(f"❤️  Health Check: http://localhost:{port}/health")
    print("=" * 60)
    print("⏳ Loading models and connecting to databases...")
    print("   This may take a minute on first startup.")
    print("=" * 60)
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    try:
        # Run FastAPI server
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=True,  # Auto-reload on code changes
            workers=1  # Single worker for now (can increase for production)
        )
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if Ollama is running: ollama serve")
        print("3. Verify MongoDB connection string is correct")
        sys.exit(1)


