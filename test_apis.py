#!/usr/bin/env python3
"""
Test script for StudyWeave AI APIs
Run this to verify your API keys and backend functionality
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append('backend')

# Load environment variables from backend/.env
load_dotenv('backend/.env')

def test_youtube_api():
    """Test YouTube Data API"""
    print("🔍 Testing YouTube Data API...")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ YOUTUBE_API_KEY not found in environment")
        return False
    
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Test with a known video
        request = youtube.videos().list(part='snippet', id='dQw4w9WgXcQ')
        response = request.execute()
        
        if response['items']:
            print("✅ YouTube API working!")
            print(f"   Test video: {response['items'][0]['snippet']['title']}")
            return True
        else:
            print("❌ YouTube API returned no results")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API failed: {e}")
        return False

def test_gemini_api():
    """Test Gemini API"""
    print("🤖 Testing Gemini API...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Say 'Hello from StudyWeave AI!'")
        result = response.text.strip()
        
        print("✅ Gemini API working!")
        print(f"   Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API failed: {e}")
        return False

def test_backend_endpoints():
    """Test backend API endpoints"""
    print("🌐 Testing Backend Endpoints...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            data = response.json()
            print(f"   Status: {data.get('status')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test course generation with sample URLs
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (has captions)
            "https://www.youtube.com/watch?v=9bZkp7q19f0"   # PSY - GANGNAM STYLE
        ]
        
        print("📚 Testing course generation...")
        response = requests.post(
            f"{base_url}/api/generate-course",
            json={"video_urls": test_urls},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Course generation working!")
            data = response.json()
            print(f"   Course: {data.get('course_title', 'Unknown')}")
            print(f"   Concepts: {data.get('total_concepts', 0)}")
            print(f"   Videos: {data.get('total_videos', 0)}")
        else:
            print(f"❌ Course generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Start it with: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 StudyWeave AI - API Test Suite")
    print("=" * 50)
    
    tests = [
        test_youtube_api,
        test_gemini_api,
        test_backend_endpoints
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("📊 Test Results Summary:")
    print("=" * 30)
    
    test_names = ["YouTube API", "Gemini API", "Backend Endpoints"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if not all_passed:
        print("\n💡 Troubleshooting Tips:")
        print("1. Make sure your .env file has the correct API keys")
        print("2. Start the backend: cd backend && python app.py")
        print("3. Check your internet connection")
        print("4. Verify API key permissions and quotas")

if __name__ == "__main__":
    main()
