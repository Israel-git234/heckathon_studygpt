import React, { useEffect, useState, useMemo } from 'react';
import ModuleCard from './ModuleCard';
import './CourseViewer.css';

const CourseViewer = ({ courseData, isLoading }) => {
  const [completedConcepts, setCompletedConcepts] = useState(new Set());

  // Load persisted progress
  useEffect(() => {
    try {
      const key = `progress:${courseData?.course_title || 'course'}`;
      const saved = localStorage.getItem(key);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          setCompletedConcepts(new Set(parsed));
        }
      }
    } catch {}
  }, [courseData?.course_title]);

  // Compute recommended video sequence (must be declared before any return to respect hook order)
  const recommended = useMemo(() => {
    const parseIso = (iso) => {
      if (!iso) return Infinity;
      const m = iso.match(/P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
      if (!m) return Infinity;
      const d = parseInt(m[1]||0)*86400 + parseInt(m[2]||0)*3600 + parseInt(m[3]||0)*60 + parseInt(m[4]||0);
      return d || Infinity;
    };
    const vids = ((courseData && courseData.videos) ? courseData.videos : []).map(v => ({
      ...v,
      _dur: parseIso(v.duration),
      _score: (v.has_transcript?1:0) + 1/Math.max(parseIso(v.duration),1)
    }));
    vids.sort((a,b)=> b._score - a._score);
    const orderMap = {};
    vids.forEach((v,idx)=> { orderMap[v.id] = idx+1; });
    return { vids, orderMap };
  }, [courseData]);

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
    setCompletedConcepts(prev => {
      const updated = new Set([...prev, conceptId]);
      try {
        const key = `progress:${courseData?.course_title || 'course'}`;
        localStorage.setItem(key, JSON.stringify(Array.from(updated)));
      } catch {}
      return updated;
    });
  };

  const totalConcepts = courseData.total_concepts || 0;
  const completedCount = completedConcepts.size;
  const progressPercentage = totalConcepts > 0 ? (completedCount / totalConcepts) * 100 : 0;

  // Basic spaced-review suggestion: concepts not completed become due next session
  const dueCount = Math.max(0, totalConcepts - completedCount);

  const resetProgress = () => {
    try {
      const key = `progress:${courseData?.course_title || 'course'}`;
      localStorage.removeItem(key);
      setCompletedConcepts(new Set());
    } catch {}
  };


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
        <div style={{marginTop:'1rem', display:'flex', gap:'0.5rem', justifyContent:'center', flexWrap:'wrap'}}>
          <button className="btn btn-secondary" onClick={resetProgress} disabled={completedCount===0}>Reset Progress</button>
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
          {dueCount > 0 && (
            <div className="review-banner">
              🔁 {dueCount} concept{dueCount !== 1 ? 's' : ''} due for review. Revisit cards you got wrong or skipped.
            </div>
          )}
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
              {moduleIndex===0 && (
                <div style={{marginBottom:'0.75rem', color:'#6b7280'}}>
                  Suggested order: watch videos in the "Recommended Sequence" below for the smoothest learning path.
                </div>
              )}
              
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
          <h3>📹 Recommended Sequence</h3>
          <div className="video-list">
            {recommended.vids.map((video, index) => (
              <div key={index} className="video-item">
                <img 
                  src={video.thumbnail} 
                  alt={video.title}
                  className="video-thumbnail"
                />
                <div className="video-info">
                  <h4 className="video-title">#{index+1} • {video.title}</h4>
                  <p className="video-channel">{video.channel} • {video.duration}</p>
                  <p className="video-duration">{video.has_transcript ? 'Transcript available' : 'No transcript'}</p>
                </div>
              </div>
            ))}
          </div>

          <h3 style={{marginTop:'1.5rem'}}>📚 All Videos</h3>
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
