# 🎓 StudyGPT - AI-Powered Learning Assistant

> **🏆 Hackathon-Ready Educational Platform**  
> Transform any YouTube video into a complete, interactive learning experience powered by Google Gemini AI.

## 🚀 Platform Overview

StudyGPT revolutionizes online learning by converting YouTube educational content into structured, AI-enhanced courses. Whether you're a student, educator, or lifelong learner, our platform provides intelligent study tools that maximize learning efficiency.

## ✨ Core Features

### 🎯 **Smart Course Generation**
- **YouTube Integration**: Paste any educational YouTube URL for instant analysis
- **AI-Powered Extraction**: Gemini AI identifies key concepts with precise timestamps
- **Intelligent Fallbacks**: Works even when video transcripts are unavailable
- **Recommended Sequence**: AI suggests optimal video watching order

### 📚 **Interactive Learning Experience**  
- **Notes-First Approach**: Study AI-generated concepts before watching videos
- **Timestamp Navigation**: Auto-jump to relevant video segments
- **Progress Persistence**: Your learning progress saves across sessions
- **Embedded Player**: Seamless YouTube integration with auto-pause

### 🤖 **AI Study Assistant**
- **Contextual Q&A**: Ask questions about specific concepts or videos
- **Document Analysis**: Upload PDFs, PPTX, DOCX for AI summarization
- **Video Recommendations**: Get suggested related content
- **Generic Tutor Chat**: Clean ChatGPT-style interface for any study questions

### 🎨 **Modern Interface**
- **Tabbed Navigation**: Videos, Upload, and Tutor sections
- **Educational Design**: Calming, professional theme optimized for focus
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Intuitive Workflow**: Streamlined experience for maximum productivity

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- YouTube Data API key
- Google Gemini API key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd studygpt
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp ../env.example .env
# Edit .env with your API keys

# Start backend
python app.py
```

### 3. Frontend Setup
```bash
cd src
npm install
npm start
```

### 4. Quick Start with Docker (Recommended)
```bash
# Automated setup and run
python scripts/setup.py
python scripts/build_and_run.py
```

## 🔑 API Keys Setup

### YouTube Data API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add to `.env`: `YOUTUBE_API_KEY=your_key_here`

### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create account and get API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

## 🏗️ Project Structure

```
studyweave-ai/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration management
│   ├── services/
│   │   ├── youtube_service.py # YouTube API integration
│   │   ├── ai_service.py      # Google Gemini AI integration
│   │   └── course_builder.py  # Main orchestration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoInput.jsx
│   │   │   ├── CourseViewer.jsx
│   │   │   ├── ModuleCard.jsx
│   │   │   └── QuizComponent.jsx
│   │   └── App.js
│   └── package.json
└── test_apis.py              # API testing script
```

## 🎯 How It Works

1. **Input**: Paste YouTube video URLs
2. **Processing**: 
   - Extract video metadata via YouTube API
   - Get transcripts using YouTube Transcript API
   - Analyze content with Google Gemini AI
3. **Output**: Structured course with:
   - Key concepts with timestamps
   - AI-generated summaries
   - Interactive quiz questions
   - Progress tracking

## 🧪 Testing

Run the test suite to verify everything works:
```bash
python test_apis.py
```

This will test:
- YouTube Data API connectivity
- Google Gemini API functionality  
- Backend endpoint responses
- Course generation pipeline

## 🎨 Demo Flow

1. **Enter URLs**: Paste 3-5 YouTube video URLs
2. **Preview**: Click "Preview Videos" to validate URLs
3. **Generate**: Click "Generate Course" to create structured content
4. **Learn**: Watch timestamped videos and take quizzes
5. **Track**: Monitor your progress through the course

## 🛠️ Development

### Backend Development
```bash
cd backend
python app.py  # Runs on http://localhost:5000
```

### Frontend Development  
```bash
cd frontend
npm start      # Runs on http://localhost:3000
```

### API Endpoints
- `GET /api/health` - Health check
- `POST /api/generate-course` - Generate course from videos
- `POST /api/preview-videos` - Preview video metadata

## 📝 Environment Variables

Create a `.env` file in the backend directory:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_key_here
FLASK_DEBUG=true
SECRET_KEY=your-secret-key-here
```

## 🚨 Troubleshooting

### Common Issues
1. **YouTube API Quota Exceeded**: Wait for quota reset or check usage
2. **Gemini API Errors**: Verify API key and billing status
3. **No Transcripts**: Some videos don't have captions available
4. **CORS Issues**: Ensure backend is running on port 5000

### Debug Mode
```bash
# Backend with debug logging
cd backend
FLASK_DEBUG=true python app.py

# Frontend with detailed errors
cd frontend
REACT_APP_DEBUG=true npm start
```

## 🏆 Hackathon Ready Features

### ✅ **Core Implementation**
- **MVP Complete**: Full YouTube-to-course generation pipeline
- **AI Integration**: Google Gemini for intelligent content analysis  
- **Modern Stack**: React + Flask + Docker architecture
- **Production Ready**: Comprehensive error handling and logging

### ✅ **Advanced Features**
- **Document Summarization**: PDF/PPTX/DOCX upload and AI analysis
- **AI Tutor Chat**: Interactive Q&A for learning assistance
- **Progress Persistence**: localStorage tracking across sessions
- **Video Recommendations**: AI-suggested learning sequences



## 📋 Project Structure

```
studygpt/
├── src/              # React frontend application
├── backend/          # Flask API server
├── scripts/          # Automation and deployment scripts
├── docs/             # Comprehensive documentation
├── demo/             # Demo materials and screenshots
├── assets/           # Branding and visual assets
├── Dockerfile        # Container configuration
├── .dockerignore     # Docker build optimization
├── .gitignore        # Version control rules
└── README.md         # Project overview (this file)
```

## 🎥 Demo & Documentation

- **📺 [Demo Video]()** - Complete feature demonstration

## 🚀 Deployment Options

### Local Development
```bash
python scripts/setup.py      # Automated setup
cd backend && python app.py  # Start backend
cd src && npm start          # Start frontend
```

### Docker Production
```bash
python scripts/build_and_run.py  # One-command deployment
```

## 📄 License

MIT License - Built for South African Intervarsity Hackathon 2025

---

**🎓 StudyGPT - Transform Learning with AI**
