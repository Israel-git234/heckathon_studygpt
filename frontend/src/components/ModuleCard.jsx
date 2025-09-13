import React, { useState } from 'react';
import QuizComponent from './QuizComponent';
import './ModuleCard.css';

const ModuleCard = ({ concept, conceptId, isCompleted, onComplete }) => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [isWatching, setIsWatching] = useState(false);

  const handleWatchVideo = () => {
    setIsWatching(true);
    // In a real implementation, this would open the video player
    // For now, we'll just show a placeholder
    setTimeout(() => {
      setIsWatching(false);
      onComplete();
    }, 2000);
  };

  const handleQuizComplete = () => {
    setShowQuiz(false);
    onComplete();
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '00:00';
    return timestamp;
  };

  const getVideoEmbedUrl = (videoUrl, timestampSeconds) => {
    if (!videoUrl) return '';
    
    // Extract video ID from various YouTube URL formats
    const videoId = videoUrl.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/);
    if (!videoId) return videoUrl;
    
    return `https://www.youtube.com/embed/${videoId[1]}?start=${timestampSeconds}&autoplay=1`;
  };

  return (
    <div className={`module-card ${isCompleted ? 'completed' : ''}`}>
      <div className="card-header">
        <div className="concept-info">
          <h4 className="concept-name">{concept.name}</h4>
          <div className="concept-meta">
            <span className="video-title">📹 {concept.video_title}</span>
            <span className="timestamp">⏰ {formatTimestamp(concept.timestamp)}</span>
          </div>
        </div>
        <div className="completion-status">
          {isCompleted ? '✅' : '⏳'}
        </div>
      </div>

      <div className="card-content">
        <div className="concept-summary">
          <p>{concept.summary}</p>
        </div>

        {concept.video_url && (
          <div className="video-section">
            <div className="video-player-container">
              {isWatching ? (
                <div className="video-loading">
                  <div className="loading-spinner"></div>
                  <p>Loading video at {formatTimestamp(concept.timestamp)}...</p>
                </div>
              ) : (
                <div className="video-placeholder">
                  <div className="play-button" onClick={handleWatchVideo}>
                    ▶️
                  </div>
                  <p>Click to watch at {formatTimestamp(concept.timestamp)}</p>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="card-actions">
          <button 
            className="btn btn-primary"
            onClick={handleWatchVideo}
            disabled={isWatching}
          >
            {isWatching ? 'Loading...' : 'Watch Video'}
          </button>
          
          {concept.quiz && concept.quiz.length > 0 && (
            <button 
              className="btn btn-secondary"
              onClick={() => setShowQuiz(!showQuiz)}
            >
              {showQuiz ? 'Hide Quiz' : 'Take Quiz'}
            </button>
          )}
        </div>

        {showQuiz && concept.quiz && (
          <div className="quiz-section">
            <QuizComponent 
              quiz={concept.quiz}
              onComplete={handleQuizComplete}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ModuleCard;
