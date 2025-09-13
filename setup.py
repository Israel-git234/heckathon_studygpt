#!/usr/bin/env python3
"""
StudyWeave AI - Setup Script
This script helps you set up the development environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_node():
    """Check Node.js version"""
    print("📦 Checking Node.js version...")
    success, stdout, stderr = run_command("node --version", check=False)
    if not success:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False
    
    version = stdout.strip()
    print(f"✅ Node.js {version}")
    return True

def setup_backend():
    """Set up backend dependencies"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        cwd=backend_dir
    )
    
    if not success:
        print(f"❌ Failed to install Python dependencies: {stderr}")
        return False
    
    print("✅ Python dependencies installed")
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_example = Path("env.example")
        if env_example.exists():
            env_content = env_example.read_text()
            env_file.write_text(env_content)
            print("✅ .env file created from template")
            print("⚠️  Please edit backend/.env and add your API keys!")
        else:
            print("❌ env.example not found!")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def setup_frontend():
    """Set up frontend dependencies"""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
    
    if not success:
        print(f"❌ Failed to install Node.js dependencies: {stderr}")
        return False
    
    print("✅ Node.js dependencies installed")
    return True

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing setup...")
    
    # Test backend
    print("🔍 Testing backend...")
    success, stdout, stderr = run_command(
        f"{sys.executable} test_apis.py",
        check=False
    )
    
    if success:
        print("✅ Backend test passed")
    else:
        print("⚠️  Backend test failed (this is normal if API keys are not set)")
        print("   Please add your API keys to backend/.env and run: python test_apis.py")
    
    return True

def main():
    """Main setup function"""
    print("🎓 StudyWeave AI - Setup Script")
    print("=" * 40)
    
    # Check system requirements
    if not check_python():
        return
    
    if not check_node():
        return
    
    # Set up backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        return
    
    # Set up frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        return
    
    # Test setup
    test_setup()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit backend/.env and add your API keys:")
    print("   - YOUTUBE_API_KEY=your_youtube_key")
    print("   - GEMINI_API_KEY=your_gemini_key")
    print("\n2. Test the setup:")
    print("   python test_apis.py")
    print("\n3. Start the application:")
    print("   python start_app.py")
    print("\n4. Or start services separately:")
    print("   Backend:  cd backend && python app.py")
    print("   Frontend: cd frontend && npm start")
    print("\n🚀 Happy coding!")

if __name__ == "__main__":
    main()
