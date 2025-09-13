import React, { useState } from 'react';
import { apiService, isValidYouTubeUrl } from '../services/api';
import './VideoInput.css';

const VideoInput = ({ onGenerateCourse, onPreviewVideos, isLoading }) => {
  const [videoUrls, setVideoUrls] = useState('');
  const [urls, setUrls] = useState([]);
  const [isValidating, setIsValidating] = useState(false);

  // Handle video URL input changes
  const handleUrlChange = (e) => {
    const value = e.target.value;
    setVideoUrls(value);
    
    // Parse URLs from textarea
    const urlList = value
      .split('\n')
      .map(url => url.trim())
      .filter(url => url.length > 0);
    
    setUrls(urlList);
  };

  // Use the API service validation function
  const validateYouTubeUrl = isValidYouTubeUrl;

  // Get validation status for each URL
  const getUrlStatus = (url) => {
    if (!url) return 'empty';
    if (validateYouTubeUrl(url)) return 'valid';
    return 'invalid';
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (urls.length === 0) {
      alert('Please enter at least one YouTube video URL');
      return;
    }

    // Validate all URLs
    const invalidUrls = urls.filter(url => !validateYouTubeUrl(url));
    if (invalidUrls.length > 0) {
      alert(`Please check these invalid URLs:\n${invalidUrls.join('\n')}`);
      return;
    }

    // Call the parent component's handler
    if (onGenerateCourse) {
      onGenerateCourse(urls);
    }
  };

  // Handle preview request
  const handlePreview = async () => {
    if (urls.length === 0) {
      alert('Please enter at least one YouTube video URL');
      return;
    }

    if (onPreviewVideos) {
      setIsValidating(true);
      try {
        await onPreviewVideos(urls);
      } finally {
        setIsValidating(false);
      }
    }
  };

  return (
    <div className="video-input-container">
      <div className="input-header">
        <h2>📚 Create Your Learning Course</h2>
        <p>Paste YouTube video URLs below to generate a structured course with AI-powered concepts and quizzes</p>
      </div>

      <form onSubmit={handleSubmit} className="video-form">
        <div className="input-group">
          <label htmlFor="video-urls" className="input-label">
            YouTube Video URLs
          </label>
          <textarea
            id="video-urls"
            value={videoUrls}
            onChange={handleUrlChange}
            placeholder="Paste YouTube video URLs here (one per line)&#10;&#10;Examples:&#10;https://www.youtube.com/watch?v=VIDEO_ID_1&#10;https://youtu.be/VIDEO_ID_2&#10;https://www.youtube.com/playlist?list=PLAYLIST_ID"
            rows={8}
            className="video-textarea"
            disabled={isLoading}
          />
          
          {/* URL validation display */}
          {urls.length > 0 && (
            <div className="url-validation">
              <h4>URL Validation ({urls.length} URLs):</h4>
              <div className="url-list">
                {urls.map((url, index) => {
                  const status = getUrlStatus(url);
                  return (
                    <div key={index} className={`url-item ${status}`}>
                      <span className="url-status">
                        {status === 'valid' ? '✅' : status === 'invalid' ? '❌' : '⏳'}
                      </span>
                      <span className="url-text">{url}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        <div className="button-group">
          <button
            type="button"
            onClick={handlePreview}
            disabled={isLoading || urls.length === 0}
            className="btn btn-secondary"
          >
            {isValidating ? 'Validating...' : 'Preview Videos'}
          </button>
          
          <button
            type="submit"
            disabled={isLoading || urls.length === 0 || urls.some(url => !validateYouTubeUrl(url))}
            className="btn btn-primary"
          >
            {isLoading ? 'Generating Course...' : 'Generate Course'}
          </button>
        </div>
      </form>

      <div className="help-text">
        <h4>💡 Tips:</h4>
        <ul>
          <li>Supported formats: youtube.com/watch?v=, youtu.be/, playlists, and channels</li>
          <li>Videos must have captions/transcripts for AI analysis</li>
          <li>Recommended: 3-5 videos for best results</li>
          <li>Use "Preview Videos" to check if videos are accessible</li>
        </ul>
      </div>
    </div>
  );
};

export default VideoInput;
