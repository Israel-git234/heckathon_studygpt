#!/usr/bin/env python3
"""
StudyGPT Development Setup Script
Sets up the development environment for StudyGPT
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(command, description, check=True):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr.strip():
                print(f"Warning: {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    requirements = {
        "python": ["python", "--version"],
        "pip": ["pip", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"]
    }
    
    missing = []
    for tool, cmd in requirements.items():
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {tool} is not installed")
            missing.append(tool)
    
    if missing:
        print(f"\n❌ Missing requirements: {', '.join(missing)}")
        print("Please install the missing tools and run this script again.")
        return False
    
    return True

def setup_environment():
    """Set up environment file"""
    env_path = Path("backend/.env")
    env_example_path = Path("env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("\n📝 Setting up environment file...")
            shutil.copy(env_example_path, env_path)
            print(f"✅ Created {env_path} from template")
            print("⚠️  Please edit backend/.env with your actual API keys:")
            print("   - YOUTUBE_API_KEY=your_youtube_key")
            print("   - GEMINI_API_KEY=your_gemini_key")
        else:
            print(f"⚠️  Environment template not found at {env_example_path}")
    else:
        print(f"✅ Environment file already exists at {env_path}")

def setup_backend():
    """Set up Python backend"""
    print("\n🐍 Setting up Python backend...")
    
    # Install backend dependencies
    os.chdir("backend")
    success = run_command("pip install -r requirements.txt", "Installing Python dependencies")
    os.chdir("..")
    
    if success:
        # Test configuration
        test_cmd = 'cd backend && python -c "from config import Config; Config.validate_config(); print(\'Configuration valid!\')"'
        run_command(test_cmd, "Testing backend configuration", check=False)
    
    return success

def setup_frontend():
    """Set up React frontend"""
    print("\n⚛️  Setting up React frontend...")
    
    # Install frontend dependencies
    os.chdir("src")
    success = run_command("npm install", "Installing Node.js dependencies")
    os.chdir("..")
    
    return success

def create_scripts():
    """Create helper scripts"""
    print("\n📜 Creating helper scripts...")
    
    # Start backend script
    start_backend = """#!/bin/bash
echo "🚀 Starting StudyGPT Backend..."
cd backend
python app.py
"""
    
    # Start frontend script
    start_frontend = """#!/bin/bash
echo "🚀 Starting StudyGPT Frontend..."
cd src
npm start
"""
    
    # Start both script
    start_all = """#!/bin/bash
echo "🚀 Starting StudyGPT (Full Stack)..."
echo "Starting backend in background..."
cd backend
python app.py &
BACKEND_PID=$!
cd ../src
echo "Starting frontend..."
npm start &
FRONTEND_PID=$!

echo "StudyGPT is starting up..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop both services"

# Wait for Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
    
    scripts = {
        "scripts/start_backend.sh": start_backend,
        "scripts/start_frontend.sh": start_frontend,
        "scripts/start_all.sh": start_all
    }
    
    for script_path, content in scripts.items():
        with open(script_path, 'w') as f:
            f.write(content)
        os.chmod(script_path, 0o755)
        print(f"  ✅ Created {script_path}")

def main():
    print("🎓 StudyGPT Development Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Setup steps
    setup_environment()
    
    backend_ok = setup_backend()
    frontend_ok = setup_frontend()
    
    create_scripts()
    
    # Summary
    print("\n" + "=" * 40)
    if backend_ok and frontend_ok:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit backend/.env with your API keys")
        print("2. Start backend: python backend/app.py")
        print("3. Start frontend: cd src && npm start")
        print("4. Access application at http://localhost:3000")
        print("\nOr use Docker: python scripts/build_and_run.py")
    else:
        print("⚠️  Setup completed with some issues")
        print("Please check the errors above and resolve them")
        if not backend_ok:
            print("- Backend setup failed")
        if not frontend_ok:
            print("- Frontend setup failed")

if __name__ == "__main__":
    main()
