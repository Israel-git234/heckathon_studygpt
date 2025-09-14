# 📚 StudyGPT Usage Guide

## 🚀 Getting Started

### Quick Start (Docker - Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd studygpt

# Build and run with Docker
python scripts/build_and_run.py
```

### Development Setup
```bash
# Run the setup script
python scripts/setup.py

# Start backend (Terminal 1)
cd backend
python app.py

# Start frontend (Terminal 2)
cd src
npm start
```

## 🎯 Features Overview

### 1. Video Learning Course Generator
Transform YouTube educational videos into structured learning experiences.

**How to use:**
1. Navigate to the **Videos** tab
2. Enter YouTube URLs (one per line)
3. Click **"Preview Videos"** to validate
4. Click **"Generate Course"** to create AI-powered learning modules
5. Study the AI-generated notes first
6. Watch videos with auto-timestamp navigation
7. Complete quizzes to test comprehension

### 2. Document Summarization
Upload lecture materials and get AI-generated summaries with video recommendations.

**How to use:**
1. Navigate to the **Upload** tab
2. Upload files (PDF, PPTX, DOCX) or paste text
3. Click **"Summarize"** to get AI analysis
4. Review generated notes and recommended videos

### 3. AI Tutor Chat
Ask study questions and get intelligent responses.

**How to use:**
1. Navigate to the **Tutor** tab
2. Type your study questions
3. Get AI-powered explanations and guidance

## 🎓 Learning Workflow

### Recommended Study Process
1. **Preview & Plan**: Use video preview to validate content
2. **Generate Course**: Let AI extract key concepts
3. **Study Notes First**: Read AI-generated concepts before watching
4. **Watch Strategically**: Follow recommended video sequence
5. **Test Knowledge**: Complete quizzes for each concept
6. **Ask Questions**: Use AI tutor for clarification
7. **Track Progress**: Monitor completion across sessions

### Best Practices
- **Use Educational Content**: YouTube videos with clear educational value work best
- **Follow Sequence**: Watch videos in the AI-recommended order
- **Notes Before Videos**: Study AI concepts before watching for better retention
- **Ask Questions**: Use the "Ask AI" feature when confused
- **Regular Review**: Return to incomplete concepts for spaced repetition

## 🔧 Configuration

### Required API Keys
Create `backend/.env` with:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Getting API Keys
1. **YouTube Data API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable YouTube Data API v3
   - Create credentials (API key)

2. **Google Gemini AI**:
   - Visit [Google AI Studio](https://makersuite.google.com/)
   - Generate an API key
   - Copy the key to your `.env` file

## 🐳 Docker Deployment

### Production Deployment
```bash
# Build image
docker build -t studygpt .

# Run container
docker run -d \
  --name studygpt \
  -p 5000:5000 \
  -v $(pwd)/backend/.env:/app/backend/.env:ro \
  studygpt
```

### Development with Docker
```bash
# Use the automated script
python scripts/build_and_run.py

# Or build and run separately
python scripts/build_and_run.py --build-only
python scripts/build_and_run.py --run-only
```

## 🔍 Troubleshooting

### Common Issues

**"API key not found"**
- Ensure `backend/.env` file exists with valid API keys
- Check API key format and permissions



**"Frontend won't start"**
- Run `npm install` in the `src` directory
- Check Node.js version (requires 16+)

**"Backend errors"**
- Run `pip install -r requirements.txt` in backend directory
- Check Python version (requires 3.8+)

### Performance Tips
- Use videos under 30 minutes for faster processing
- Allow 30-60 seconds for course generation
- Chrome/Firefox recommended for best experience

## 📱 Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## 🔗 Demo Video
[Watch Demo Video](youtu.be/placeholder)


