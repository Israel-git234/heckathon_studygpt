# 🏗️ StudyGPT Architecture

## 📋 System Overview

StudyGPT is a full-stack web application that transforms YouTube educational content into interactive learning experiences using AI.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Flask Backend  │    │   AI Services   │
│                 │    │                 │    │                 │
│  • Video Input  │───▶│  • API Routes   │───▶│  • Google Gemini│
│  • Course View  │    │  • File Upload  │    │  • YouTube API  │
│  • AI Chat      │    │  • AI Integration│    │  • Transcript   │
│  • Progress     │◀───│  • Error Handle │◀───│    Processing   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 Core Components

### Frontend (React)
- **Location**: `/src/`
- **Technology**: React 18, Axios, CSS3
- **Responsibilities**:
  - User interface and interaction
  - Video preview and playback
  - Progress tracking with localStorage
  - File upload handling
  - Real-time AI chat interface

### Backend (Flask)
- **Location**: `/backend/`
- **Technology**: Python 3.9, Flask, Flask-CORS
- **Responsibilities**:
  - RESTful API endpoints
  - AI service coordination
  - File processing (PDF, DOCX, PPTX)
  - Error handling and logging
  - Configuration management

### AI Services
- **Google Gemini**: Content analysis and generation
- **YouTube Data API**: Video metadata retrieval
- **YouTube Transcript API**: Automatic transcript extraction

## 🔄 Data Flow

### Course Generation Process
```
1. User Input (URLs) → Frontend Validation
2. Frontend → Backend (/api/preview-videos)
3. Backend → YouTube API (metadata)
4. Backend → YouTube Transcript API (transcripts)
5. Backend → Google Gemini (concept extraction)
6. Backend → Course Builder (structure creation)
7. Backend → Frontend (structured course data)
8. Frontend → Local Storage (progress tracking)
```

### Document Summarization Process
```
1. File Upload → Frontend Processing
2. Frontend → Backend (/api/summarize-upload)
3. Backend → Document Parser (PDF/DOCX/PPTX)
4. Backend → Google Gemini (summarization)
5. Backend → YouTube API (video recommendations)
6. Backend → Frontend (summary + recommendations)
```

## 📁 Project Structure

```
studygpt/
├── src/                          # React Frontend
│   ├── components/               # React Components
│   │   ├── VideoInput.jsx       # URL input and validation
│   │   ├── CourseViewer.jsx     # Course display and navigation
│   │   ├── ModuleCard.jsx       # Individual learning modules
│   │   ├── QuizComponent.jsx    # Interactive quizzes
│   │   ├── UploadSummarize.jsx  # File upload interface
│   │   └── TutorChat.jsx        # AI chat interface
│   ├── services/
│   │   └── api.js               # API communication
│   └── *.css                    # Styling
├── backend/                      # Flask Backend
│   ├── services/                 # Core Services
│   │   ├── ai_service.py        # Google Gemini integration
│   │   ├── youtube_service.py   # YouTube API handling
│   │   └── course_builder.py    # Course structure logic
│   ├── models/                   # Data models
│   ├── utils/                    # Utility functions
│   ├── app.py                   # Main Flask application
│   └── config.py                # Configuration management
├── scripts/                      # Automation Scripts
│   ├── build_and_run.py        # Docker automation
│   └── setup.py                # Development setup
├── docs/                        # Documentation
│   ├── USAGE.md                 # User guide
│   └── ARCHITECTURE.md          # This file
├── demo/                        # Demo materials
├── assets/                      # Project assets
├── Dockerfile                   # Container configuration
└── README.md                    # Project overview
```

## 🔌 API Endpoints

### Core Endpoints
```python
GET  /api/health                 # System health check
POST /api/preview-videos         # Video metadata preview
POST /api/generate-course        # Full course generation
POST /api/ask-question          # AI tutor interaction
POST /api/summarize-upload      # Document summarization
```

### Request/Response Format
```javascript
// Course Generation Request
{
  "video_urls": ["https://youtube.com/watch?v=..."]
}

// Course Generation Response
{
  "course_title": "Generated Course Title",
  "videos": [{
    "id": "video_id",
    "title": "Video Title",
    "duration": "PT10M30S",
    "has_transcript": true,
    "concepts": [{
      "name": "Concept Name",
      "summary": "AI-generated summary",
      "notes": ["Key point 1", "Key point 2"],
      "timestamp_start_seconds": 120,
      "timestamp_end_seconds": 180,
      "quiz": {...}
    }]
  }],
  "processing_stats": {...}
}
```

## 🔧 Configuration

### Environment Variables
```env
# Required API Keys
YOUTUBE_API_KEY=your_youtube_key
GEMINI_API_KEY=your_gemini_key

# Flask Configuration
FLASK_DEBUG=true
SECRET_KEY=your_secret_key
FLASK_ENV=development

# CORS Settings
FRONTEND_URL=http://localhost:3000
```

### AI Service Configuration
- **Gemini Model**: `gemini-1.5-flash`
- **Max Retries**: 3 attempts with exponential backoff
- **Temperature**: 0.3 (focused, educational responses)
- **Token Limits**: Configurable per request type

## 🚀 Deployment Architecture

### Development
```
Frontend (localhost:3000) ←→ Backend (localhost:5000) ←→ AI APIs
```

### Production (Docker)
```
┌─────────────────────────────────────┐
│           Docker Container          │
│  ┌─────────────┐  ┌───────────────┐ │
│  │   Frontend  │  │    Backend    │ │
│  │   (Built)   │  │   Flask App   │ │
│  │             │  │               │ │
│  └─────────────┘  └───────────────┘ │
└─────────────────────────────────────┘
              ↕
        External AI APIs
```

## 📊 Performance Considerations

### Optimization Strategies
1. **Parallel Processing**: Concurrent video analysis using ThreadPoolExecutor
2. **Caching**: Frontend progress in localStorage
3. **Lazy Loading**: On-demand component rendering
4. **Error Recovery**: Retry logic with exponential backoff
5. **Resource Management**: Memory-efficient file processing

### Scalability Features
- **Stateless Backend**: Horizontal scaling ready
- **Docker Containerization**: Easy deployment
- **Modular Architecture**: Independent service scaling
- **API Rate Limiting**: Built-in throttling

## 🔒 Security Features

### Data Protection
- **Environment Variables**: Secure API key storage
- **Input Validation**: Comprehensive request sanitization
- **CORS Configuration**: Restricted origin access
- **File Upload Limits**: Size and type restrictions
- **Error Handling**: Sanitized error responses

### AI Safety
- **Content Filtering**: Educational content focus
- **Response Validation**: Structured output verification
- **Rate Limiting**: API usage throttling
- **Fallback Mechanisms**: Graceful degradation

## 🧪 Testing Strategy

### Automated Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint validation
- **End-to-End Tests**: Complete workflow verification
- **Performance Tests**: Load and stress testing

### Manual Testing
- **Browser Compatibility**: Cross-browser validation
- **Mobile Responsiveness**: Multi-device testing
- **User Experience**: Workflow optimization
- **Error Scenarios**: Edge case handling
