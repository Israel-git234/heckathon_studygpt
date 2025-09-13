from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from config import Config
from services.course_builder import CourseBuilder

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize course builder
course_builder = CourseBuilder()

# Validate configuration on startup
try:
    Config.validate_config()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    logger.warning("Some features may not work without proper API keys")

# Basic health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "StudyWeave AI Backend Running",
        "config_valid": True
    })

# Main course generation endpoint
@app.route('/api/generate-course', methods=['POST'])
def generate_course():
    """
    Main endpoint for generating structured courses from YouTube videos
    Processes video URLs and returns structured course data with concepts and quizzes
    """
    try:
        data = request.get_json()
        video_urls = data.get('video_urls', [])
        
        if not video_urls:
            return jsonify({"error": "No video URLs provided"}), 400
        
        if not isinstance(video_urls, list):
            return jsonify({"error": "video_urls must be a list"}), 400
        
        logger.info(f"Generating course from {len(video_urls)} video URLs")
        
        # Build the course using our services
        course_data = course_builder.build_course_from_videos(video_urls)
        
        if "error" in course_data:
            return jsonify(course_data), 400
        
        return jsonify(course_data)
        
    except Exception as e:
        logger.error(f"Error in generate_course: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Preview endpoint for quick video info
@app.route('/api/preview-videos', methods=['POST'])
def preview_videos():
    """
    Quick preview of video metadata without AI processing
    Useful for validating URLs before full course generation
    """
    try:
        data = request.get_json()
        video_urls = data.get('video_urls', [])
        
        if not video_urls:
            return jsonify({"error": "No video URLs provided"}), 400
        
        logger.info(f"Previewing {len(video_urls)} video URLs")
        
        # Get just video info without AI processing
        preview_data = course_builder.get_video_info_only(video_urls)
        
        return jsonify(preview_data)
        
    except Exception as e:
        logger.error(f"Error in preview_videos: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
