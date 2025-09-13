import React, { useState } from 'react';
import VideoInput from './components/VideoInput';
import CourseViewer from './components/CourseViewer';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [courseData, setCourseData] = useState(null);
  const [previewData, setPreviewData] = useState(null);

  // Handle course generation
  const handleGenerateCourse = async (videoUrls) => {
    setIsLoading(true);
    setCourseData(null);
    setPreviewData(null);
    
    try {
      const data = await apiService.generateCourse(videoUrls);
      setCourseData(data);
    } catch (error) {
      console.error('Error generating course:', error);
      setCourseData({ 
        error: error.message || 'Failed to generate course. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle video preview
  const handlePreviewVideos = async (videoUrls) => {
    try {
      const data = await apiService.previewVideos(videoUrls);
      setPreviewData(data);
      alert(`Found ${data.total_videos} valid videos. Ready to generate course!`);
    } catch (error) {
      console.error('Error previewing videos:', error);
      alert(`Preview failed: ${error.message || 'Please check your connection.'}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 StudyWeave AI</h1>
        <p>Transform scattered YouTube videos into structured, interactive learning courses</p>
        <div className="header-features">
          <span>✨ AI-Powered Analysis</span>
          <span>📚 Structured Learning</span>
          <span>🧠 Interactive Quizzes</span>
          <span>⏰ Timestamped Content</span>
        </div>
      </header>

      <main className="App-main">
        <VideoInput 
          onGenerateCourse={handleGenerateCourse}
          onPreviewVideos={handlePreviewVideos}
          isLoading={isLoading}
        />

        {previewData && !courseData && (
          <div className="preview-section">
            <h3>📹 Video Preview</h3>
            <p>Found {previewData.total_videos} valid videos. Ready to generate your course!</p>
          </div>
        )}

        <CourseViewer 
          courseData={courseData}
          isLoading={isLoading}
        />
      </main>

      <footer className="App-footer">
        <p>Built with ❤️ for the hackathon - StudyWeave AI</p>
      </footer>
    </div>
  );
}

export default App;
