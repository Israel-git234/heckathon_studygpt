# 🎓 StudyWeave AI

Transform scattered YouTube videos into structured, personalized learning courses with AI-powered analysis and interactive quizzes.

## ✨ Features

- **🎥 YouTube Integration**: Extract video metadata and transcripts automatically
- **🤖 AI-Powered Analysis**: Generate key concepts, summaries, and quizzes using OpenAI
- **⏰ Timestamped Learning**: Jump directly to relevant video sections for each concept
- **🧠 Interactive Quizzes**: Test your knowledge with AI-generated questions
- **📚 Structured Courses**: Organize content into logical learning modules
- **📊 Progress Tracking**: Monitor your learning journey and completion status

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- YouTube Data API key
- OpenAI API key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd studyweave-ai
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
cd frontend
npm install
npm start
```

### 4. Test Everything
```bash
# From project root
python test_apis.py
```

## 🔑 API Keys Setup

### YouTube Data API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add to `.env`: `YOUTUBE_API_KEY=your_key_here`

### OpenAI API
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create account and get API key
3. Add to `.env`: `OPENAI_API_KEY=sk-your_key_here`

## 🏗️ Project Structure

```
studyweave-ai/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration management
│   ├── services/
│   │   ├── youtube_service.py # YouTube API integration
│   │   ├── ai_service.py      # OpenAI integration
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
   - Analyze content with OpenAI GPT-3.5-turbo
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
- OpenAI API functionality  
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
OPENAI_API_KEY=sk-your_openai_key_here
FLASK_DEBUG=true
SECRET_KEY=your-secret-key-here
```

## 🚨 Troubleshooting

### Common Issues
1. **YouTube API Quota Exceeded**: Wait for quota reset or check usage
2. **OpenAI API Errors**: Verify API key and billing status
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

## 🏆 Hackathon Features

- ✅ **MVP Complete**: Full YouTube-to-course pipeline
- ✅ **AI Integration**: OpenAI-powered content analysis
- ✅ **Interactive UI**: Modern React frontend with quizzes
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Progress Tracking**: Learning analytics and completion status
- ✅ **Responsive Design**: Works on desktop and mobile

## 🔮 Future Enhancements

- [ ] Lecture slide integration (PDF/PPT upload)
- [ ] Multi-language support
- [ ] Advanced course customization
- [ ] User authentication and saved courses
- [ ] Mobile app development
- [ ] LMS integration (Canvas, Moodle)

## 📄 License

Built for hackathon demonstration purposes.

---

**Built with ❤️ for the hackathon - StudyWeave AI**