import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from well-known locations with BOM-safe encoding
_BACKEND_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _BACKEND_DIR.parent

# Use utf-8-sig to handle potential BOM characters created by some editors/PowerShell
for _dotenv_path in (
    _BACKEND_DIR / '.env',
    _ROOT_DIR / '.env',
):
    try:
        load_dotenv(dotenv_path=_dotenv_path, override=True, encoding='utf-8-sig')
    except Exception:
        # Fallback without encoding if the environment doesn't support it
        load_dotenv(dotenv_path=_dotenv_path, override=True)

class Config:
    # API Keys - required environment variables
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # CORS Settings
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
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
