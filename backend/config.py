import os
from dotenv import load_dotenv

# Load environment variables from multiple possible locations
load_dotenv()  # Current directory
load_dotenv('../.env')  # Parent directory
load_dotenv('.env')  # Explicit .env file

class Config:
    # API Keys - with fallback values for testing
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyAirVXZJ246Oai1kwF7-St5mMgUNaQ1M0M')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyChJ9ZHK0fdHmk7OvPytV9n89DHLA5ttTU')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # CORS Settings
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    
    # API Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_keys = {
            'YOUTUBE_API_KEY': cls.YOUTUBE_API_KEY,
            'GEMINI_API_KEY': cls.GEMINI_API_KEY
        }
        
        missing_keys = [key for key, value in required_keys.items() if not value]
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {missing_keys}")
        
        return True
