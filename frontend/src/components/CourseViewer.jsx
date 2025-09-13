import React, { useState } from 'react';
import ModuleCard from './ModuleCard';
import './CourseViewer.css';

const CourseViewer = ({ courseData, isLoading }) => {
  const [selectedModule, setSelectedModule] = useState(null);
  const [completedConcepts, setCompletedConcepts] = useState(new Set());

  if (isLoading) {
    return (
      <div className="course-viewer loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>AI is analyzing your videos and generating course content...</p>
          <p className="loading-subtitle">This may take 30-60 seconds</p>
        </div>
      </div>
    );
  }

  if (!courseData) {
    return null;
  }

  if (courseData.error) {
    return (
      <div className="course-viewer error">
        <div className="error-content">
          <h3>❌ Error Generating Course</h3>
          <p>{courseData.error}</p>
          {courseData.processed_videos !== undefined && (
            <p>Processed {courseData.processed_videos} videos</p>
          )}
        </div>
      </div>
    );
  }

  const handleConceptComplete = (conceptId) => {
    setCompletedConcepts(prev => new Set([...prev, conceptId]));
  };

  const totalConcepts = courseData.total_concepts || 0;
  const completedCount = completedConcepts.size;
  const progressPercentage = totalConcepts > 0 ? (completedCount / totalConcepts) * 100 : 0;

  return (
    <div className="course-viewer">
      <div className="course-header">
        <h2>🎓 {courseData.course_title}</h2>
        <div className="course-stats">
          <div className="stat">
            <span className="stat-number">{courseData.total_videos || 0}</span>
            <span className="stat-label">Videos</span>
          </div>
          <div className="stat">
            <span className="stat-number">{totalConcepts}</span>
            <span className="stat-label">Concepts</span>
          </div>
          <div className="stat">
            <span className="stat-number">{courseData.estimated_duration || 'N/A'}</span>
            <span className="stat-label">Duration</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {totalConcepts > 0 && (
        <div className="progress-section">
          <div className="progress-header">
            <span>Learning Progress</span>
            <span>{completedCount}/{totalConcepts} concepts completed</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Course Modules */}
      <div className="modules-container">
        {courseData.modules && courseData.modules.length > 0 ? (
          courseData.modules.map((module, moduleIndex) => (
            <div key={moduleIndex} className="module-section">
              <h3 className="module-title">
                📚 {module.module_name}
              </h3>
              
              <div className="concepts-grid">
                {module.concepts && module.concepts.map((concept, conceptIndex) => {
                  const conceptId = `${moduleIndex}-${conceptIndex}`;
                  const isCompleted = completedConcepts.has(conceptId);
                  
                  return (
                    <ModuleCard
                      key={conceptId}
                      concept={concept}
                      conceptId={conceptId}
                      isCompleted={isCompleted}
                      onComplete={() => handleConceptComplete(conceptId)}
                    />
                  );
                })}
              </div>
            </div>
          ))
        ) : (
          <div className="no-modules">
            <p>No course modules were generated. Please try with different videos.</p>
          </div>
        )}
      </div>

      {/* Course Summary */}
      {courseData.videos && courseData.videos.length > 0 && (
        <div className="course-summary">
          <h3>📹 Source Videos</h3>
          <div className="video-list">
            {courseData.videos.map((video, index) => (
              <div key={index} className="video-item">
                <img 
                  src={video.thumbnail} 
                  alt={video.title}
                  className="video-thumbnail"
                />
                <div className="video-info">
                  <h4 className="video-title">{video.title}</h4>
                  <p className="video-channel">{video.channel}</p>
                  <p className="video-duration">{video.duration}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseViewer;
