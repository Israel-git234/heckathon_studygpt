#!/usr/bin/env python3
"""
StudyWeave AI - Application Startup Script
This script helps you start both backend and frontend services
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def run_backend():
    """Start the Flask backend server"""
    print("🚀 Starting StudyWeave AI Backend...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Check if .env file exists
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  .env file not found in backend directory!")
        print("   Please copy env.example to backend/.env and add your API keys")
        return False
    
    try:
        # Start Flask server
        os.chdir(backend_dir)
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
        return True

def run_frontend():
    """Start the React frontend server"""
    print("🎨 Starting StudyWeave AI Frontend...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
        return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import google.generativeai as genai
        from googleapiclient.discovery import build
        from youtube_transcript_api import YouTubeTranscriptApi
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("   Run: cd backend && pip install -r requirements.txt")
        return False
    
    # Check Node.js dependencies
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("❌ Node.js dependencies not installed")
            print("   Run: cd frontend && npm install")
            return False
        print("✅ Node.js dependencies OK")
    
    return True

def main():
    """Main startup function"""
    print("🎓 StudyWeave AI - Starting Application")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install dependencies before starting the app")
        return
    
    print("\n🚀 Starting services...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    finally:
        print("👋 Thanks for using StudyWeave AI!")

if __name__ == "__main__":
    main()
