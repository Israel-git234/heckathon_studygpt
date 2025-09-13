#!/usr/bin/env python3
"""
StudyGPT Docker Build and Run Script
Builds and runs the StudyGPT application in a Docker container
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running!")
        print("Please install Docker and ensure it's running before continuing.")
        return False

def check_env_file():
    """Check if .env file exists with API keys"""
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("⚠️  Warning: backend/.env file not found!")
        print("Please create it with your API keys:")
        print("  YOUTUBE_API_KEY=your_youtube_key")
        print("  GEMINI_API_KEY=your_gemini_key")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Build and run StudyGPT in Docker")
    parser.add_argument("--build-only", action="store_true", help="Only build the image, don't run")
    parser.add_argument("--run-only", action="store_true", help="Only run existing image, don't build")
    parser.add_argument("--port", default="5000", help="Port to run on (default: 5000)")
    parser.add_argument("--name", default="studygpt", help="Container name (default: studygpt)")
    
    args = parser.parse_args()
    
    print("🎓 StudyGPT Docker Manager")
    print("=" * 40)
    
    # Pre-flight checks
    if not check_docker():
        sys.exit(1)
    
    if not args.run_only:
        check_env_file()
    
    image_name = "studygpt:latest"
    container_name = args.name
    port = args.port
    
    # Build stage
    if not args.run_only:
        print(f"\n🏗️  Building Docker image: {image_name}")
        build_cmd = f"docker build -t {image_name} ."
        if not run_command(build_cmd, "Docker image build"):
            sys.exit(1)
    
    # Run stage
    if not args.build_only:
        print(f"\n🚀 Running container: {container_name}")
        
        # Stop existing container if running
        stop_cmd = f"docker stop {container_name} 2>/dev/null || true"
        remove_cmd = f"docker rm {container_name} 2>/dev/null || true"
        run_command(stop_cmd, "Stopping existing container")
        run_command(remove_cmd, "Removing existing container")
        
        # Run new container
        run_cmd = f"""docker run -d \\
            --name {container_name} \\
            -p {port}:5000 \\
            -v "$(pwd)/backend/.env:/app/backend/.env:ro" \\
            --restart unless-stopped \\
            {image_name}"""
        
        if run_command(run_cmd, "Starting new container"):
            print(f"\n🎉 StudyGPT is now running!")
            print(f"📱 Access the application at: http://localhost:{port}")
            print(f"🔍 Check logs with: docker logs {container_name}")
            print(f"⏹️  Stop with: docker stop {container_name}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
