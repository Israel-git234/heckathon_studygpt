from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Basic health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "StudyWeave AI Backend Running"})

# Placeholder for course generation endpoint
@app.route('/api/generate-course', methods=['POST'])
def generate_course():
    """
    Main endpoint for generating structured courses from YouTube videos
    Will process video URLs and return structured course data
    """
    try:
        data = request.get_json()
        video_urls = data.get('video_urls', [])
        
        if not video_urls:
            return jsonify({"error": "No video URLs provided"}), 400
        
        # TODO: Implement course generation logic
        return jsonify({
            "message": "Course generation endpoint ready",
            "videos_received": len(video_urls),
            "status": "development"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
