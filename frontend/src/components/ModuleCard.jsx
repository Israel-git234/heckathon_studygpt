import React, { useMemo, useState } from 'react';
import YouTube from 'react-youtube';
import QuizComponent from './QuizComponent';
import { askAI } from '../services/api';
import './ModuleCard.css';

const ModuleCard = ({ concept, conceptId, isCompleted, onComplete }) => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [showPlayer, setShowPlayer] = useState(false);
  const [askOpen, setAskOpen] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isAsking, setIsAsking] = useState(false);

  const handleWatchVideo = () => {
    setShowPlayer(true);
  };

  const handleQuizComplete = () => {
    setShowQuiz(false);
    onComplete();
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '00:00';
    return timestamp;
  };

  const videoId = useMemo(() => {
    const url = concept.video_url || '';
    const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/);
    return match ? match[1] : null;
  }, [concept.video_url]);

  const startSeconds = useMemo(() => {
    if (typeof concept.timestamp_seconds === 'number') return concept.timestamp_seconds;
    if (typeof concept.timestamp === 'string') {
      const parts = concept.timestamp.split(':').map(Number);
      if (parts.length === 2) return parts[0] * 60 + parts[1];
      if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
    }
    return 0;
  }, [concept.timestamp, concept.timestamp_seconds]);

  const playerOpts = useMemo(() => ({
    width: '100%',
    height: '315',
    playerVars: {
      autoplay: 1,
      start: startSeconds,
      rel: 0,
      modestbranding: 1,
    },
  }), [startSeconds]);

  const onPlayerReady = (event) => {
    try {
      event.target.seekTo(startSeconds, true);
      event.target.playVideo();
    } catch {}
  };

  const onPlayerStateChange = (event) => {
    try {
      const end = typeof concept.timestamp_end_seconds === 'number' ? concept.timestamp_end_seconds : null;
      if (!end) return;
      const player = event.target;
      const check = () => {
        const t = Math.floor(player.getCurrentTime());
        if (t >= end) {
          player.pauseVideo();
        } else if (player.getPlayerState() === 1) {
          requestAnimationFrame(check);
        }
      };
      if (event.data === 1) {
        requestAnimationFrame(check);
      }
    } catch {}
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setIsAsking(true);
    setAnswer('');
    try {
      const video = {
        title: concept.video_title,
        description: concept.video_description || '',
        transcript: null,
      };
      const res = await askAI(question, video, concept);
      setAnswer(res.answer || '');
    } catch (e) {
      setAnswer(e.message || 'Failed to get an answer.');
    } finally {
      setIsAsking(false);
    }
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
          <h5>📝 Study Notes</h5>
          <p>{concept.summary}</p>
          {Array.isArray(concept.notes) && concept.notes.length > 0 && (
            <ul className="notes-list">
              {concept.notes.map((n, i) => (
                <li key={i}>{n}</li>
              ))}
            </ul>
          )}
        </div>

        {concept.video_url && (
          <div className="video-section">
            <div className="video-player-container">
              {showPlayer && videoId ? (
                <YouTube videoId={videoId} opts={playerOpts} onReady={onPlayerReady} onStateChange={onPlayerStateChange} />
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
            disabled={showPlayer}
          >
            {showPlayer ? 'Playing…' : 'Watch Video'}
          </button>
          <button 
            className="btn btn-secondary"
            onClick={onComplete}
            disabled={isCompleted}
          >
            {isCompleted ? 'Completed' : 'Mark Complete'}
          </button>
          {concept.quiz && concept.quiz.length > 0 && (
            <button 
              className="btn btn-secondary"
              onClick={() => setShowQuiz(!showQuiz)}
            >
              {showQuiz ? 'Hide Quiz' : 'Take Quiz'}
            </button>
          )}
          <button className="btn" onClick={() => setAskOpen(!askOpen)}>
            {askOpen ? 'Hide Ask AI' : 'Ask AI'}
          </button>
        </div>

        {showQuiz && concept.quiz && (
          <div className="quiz-section">
            <QuizComponent 
              quiz={concept.quiz}
              onComplete={handleQuizComplete}
            />
          </div>
        )}

        {askOpen && (
          <div className="askai-section">
            <h5>🤖 Ask AI about this concept</h5>
            <textarea
              rows={3}
              placeholder="What didn't make sense? Ask a question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <div className="askai-actions">
              <button className="btn btn-primary" onClick={handleAsk} disabled={isAsking || !question.trim()}>
                {isAsking ? 'Thinking…' : 'Ask'}
              </button>
            </div>
            {answer && (
              <div className="askai-answer">
                {answer}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ModuleCard;
