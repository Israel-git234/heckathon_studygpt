import React, { useState } from 'react';
import './App.css';

function App() {
  const [videoUrls, setVideoUrls] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [courseData, setCourseData] = useState(null);

  // Handle video URL input
  const handleVideoInput = (e) => {
    setVideoUrls(e.target.value);
  };

  // Process video URLs and generate course
  const handleGenerateCourse = async () => {
    if (!videoUrls.trim()) {
      alert('Please enter at least one YouTube video URL');
      return;
    }

    setIsLoading(true);
    
    try {
      // Split URLs by newline and filter out empty strings
      const urls = videoUrls.split('\n').filter(url => url.trim());
      
      const response = await fetch('/api/generate-course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_urls: urls }),
      });

      const data = await response.json();
      setCourseData(data);
    } catch (error) {
      console.error('Error generating course:', error);
      alert('Error generating course. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>StudyWeave AI</h1>
        <p>Transform YouTube videos into structured learning courses</p>
      </header>

      <main className="App-main">
        <div className="input-section">
          <h2>Enter YouTube Video URLs</h2>
          <textarea
            value={videoUrls}
            onChange={handleVideoInput}
            placeholder="Paste YouTube video URLs here (one per line)&#10;Example:&#10;https://www.youtube.com/watch?v=VIDEO_ID_1&#10;https://www.youtube.com/watch?v=VIDEO_ID_2"
            rows={6}
            className="video-input"
          />
          <button 
            onClick={handleGenerateCourse} 
            disabled={isLoading}
            className="generate-btn"
          >
            {isLoading ? 'Generating Course...' : 'Generate Course'}
          </button>
        </div>

        {courseData && (
          <div className="course-section">
            <h2>Generated Course</h2>
            <pre>{JSON.stringify(courseData, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
