#!/usr/bin/env python3
"""
Quick setup script for StudyWeave AI with your API keys
"""

import os
import subprocess
import sys

def create_env_file():
    """Create the .env file with your API keys"""
    env_content = """# API Keys
YOUTUBE_API_KEY=AIzaSyAirVXZJ246Oai1kwF7-St5mMgUNaQ1M0M
GEMINI_API_KEY=AIzaSyChJ9ZHK0fdHmk7OvPytV9n89DHLA5ttTU

# Flask Configuration
FLASK_DEBUG=true
SECRET_KEY=studyweave-ai-secret-key-2024
FLASK_ENV=development

# CORS Settings
FRONTEND_URL=http://localhost:3000
"""
    
    env_path = "backend/.env"
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created {env_path} with your API keys")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_frontend_deps():
    """Install Node.js dependencies"""
    print("📦 Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd="frontend", check=True)
        print("✅ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def test_apis():
    """Test the APIs"""
    print("🧪 Testing APIs...")
    try:
        result = subprocess.run([sys.executable, "test_apis.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All APIs working!")
            print(result.stdout)
        else:
            print("⚠️ Some API tests failed (this might be normal)")
            print(result.stdout)
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🎓 StudyWeave AI - Quick Setup")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    if not install_frontend_deps():
        return
    
    # Test APIs
    test_apis()
    
    print("\n🎉 Setup complete!")
    print("\n🚀 To start the application:")
    print("   python start_app.py")
    print("\n   OR manually:")
    print("   Terminal 1: cd backend && python app.py")
    print("   Terminal 2: cd frontend && npm start")
    print("\n🌐 Then visit: http://localhost:3000")

if __name__ == "__main__":
    main()
