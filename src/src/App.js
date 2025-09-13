import React, { useState, useCallback, useEffect, useRef } from 'react';
import VideoInput from './components/VideoInput';
import CourseViewer from './components/CourseViewer';
import { apiService, askAI } from './services/api';
import './App.css';
import './error-styles.css';
 

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [courseData, setCourseData] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [error, setError] = useState(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  // Check online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Handle video preview with improved error handling
  const handlePreviewVideos = useCallback(async (videoUrls) => {
    if (!isOnline) {
      setError('You are offline. Please check your internet connection.');
      return;
    }
    
    if (!videoUrls || videoUrls.length === 0) {
      setError('Please provide at least one YouTube video URL.');
      return;
    }
    
    setError(null);
    
    try {
      const data = await apiService.previewVideos(videoUrls);
      setPreviewData(data);
      
      if (data.error) {
        setError(data.error);
      } else {
        const message = `Found ${data.total_videos} valid videos out of ${videoUrls.length} URLs provided. Ready to generate course!`;
        // Use a better notification system instead of alert
        console.log(message);
        // You could replace this with a toast notification
      }
    } catch (error) {
      console.error('Error previewing videos:', error);
      const errorMessage = error.message || 'Failed to preview videos. Please check your connection.';
      setError(errorMessage);
    }
  }, [isOnline]);

  // Handle course generation with improved error handling and persistence
  const handleGenerateCourse = useCallback(async (videoUrls) => {
    if (!isOnline) {
      setError('You are offline. Please check your internet connection.');
      return;
    }
    
    if (!videoUrls || videoUrls.length === 0) {
      setError('Please provide at least one YouTube video URL.');
      return;
    }
    
    setIsLoading(true);
    setCourseData(null);
    setPreviewData(null);
    setError(null);
    
    try {
      const data = await apiService.generateCourse(videoUrls);
      
      if (data.error) {
        setError(data.error);
        setCourseData({ error: data.error });
      } else {
        setCourseData(data);
        
        // Save to localStorage for persistence
        try {
          localStorage.setItem('lastGeneratedCourse', JSON.stringify(data));
        } catch (e) {
          console.warn('Could not save course to localStorage:', e);
        }
      }
    } catch (error) {
      console.error('Error generating course:', error);
      const errorMessage = error.message || 'Failed to generate course. Please try again.';
      setError(errorMessage);
      setCourseData({ error: errorMessage });
    } finally {
      setIsLoading(false);
    }
  }, [isOnline]);

  // Clear error state
  const clearError = useCallback(() => {
    setError(null);
  }, []);
  
  // Load last course from localStorage on mount
  useEffect(() => {
    try {
      const savedCourse = localStorage.getItem('lastGeneratedCourse');
      if (savedCourse) {
        const parsedCourse = JSON.parse(savedCourse);
        // Only load if it's recent (within 24 hours)
        const dayAgo = Date.now() - 24 * 60 * 60 * 1000;
        if (parsedCourse.generated_at && parsedCourse.generated_at * 1000 > dayAgo) {
          setCourseData(parsedCourse);
        }
      }
    } catch (e) {
      console.warn('Could not load saved course:', e);
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 StudyGPT</h1>
        <p>Transform scattered YouTube videos into structured, interactive learning courses</p>
        
        {!isOnline && (
          <div className="offline-banner">
            😴 You are offline. Please check your internet connection.
          </div>
        )}
        
        {error && (
          <div className="error-banner">
            ❌ {error}
            <button onClick={clearError} className="error-close">×</button>
          </div>
        )}
        
        <div className="header-features">
          <span>✨ AI-Powered Analysis</span>
          <span>📚 Structured Learning</span>
          <span>🧠 Interactive Quizzes</span>
          <span>⏰ Timestamped Content</span>
        </div>
      </header>

      <main className="App-main">
        <FeatureTabs>
          <div label="Videos">
            <VideoInput 
              onGenerateCourse={handleGenerateCourse}
              onPreviewVideos={handlePreviewVideos}
              isLoading={isLoading}
            />
          </div>
          <div label="Upload">
            <div className="preview-section" style={{marginTop: '1rem'}}>
              <h3>📄 Upload Lecture Slides/Transcript (PDF, PPTX, DOCX or paste text)</h3>
              <UploadSummarize />
            </div>
          </div>
          <div label="Tutor">
            <div className="preview-section" style={{marginTop: '1rem'}}>
              <h3>🤖 Study Tutor (Ask anything)</h3>
              <TutorChat />
            </div>
          </div>
        </FeatureTabs>

        {previewData && !courseData && (
          <div className="preview-section">
            <h3>📹 Video Preview</h3>
            <p>Found {previewData.total_videos} valid videos out of {previewData.processing_stats?.total_urls_provided || 'N/A'} URLs provided.</p>
            {previewData.processing_stats && (
              <p>Success rate: {Math.round(previewData.processing_stats.success_rate)}%</p>
            )}
            {Array.isArray(previewData.videos) && previewData.videos.length > 0 && (
              <div className="preview-list">
                {previewData.videos.map((v, idx) => (
                  <div key={idx} className="preview-item">
                    <img src={v.thumbnail} alt={v.title} className="preview-thumb" />
                    <div className="preview-meta">
                      <div className="preview-title">{v.title}</div>
                      <div className="preview-sub">{v.channel} • {v.duration}</div>
                      <div className="preview-flags">
                        <span className={`badge ${v.has_transcript ? 'ok' : 'warn'}`}>
                          {v.has_transcript ? 'Transcript available' : 'No transcript'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            <p>Ready to generate your course!</p>
          </div>
        )}

        <CourseViewer 
          courseData={courseData}
          isLoading={isLoading}
        />
      </main>

      <footer className="App-footer">
        <p>Built with ❤️ for the hackathon - StudyGPT</p>
      </footer>
    </div>
  );
}

export default App;

function FeatureTabs({ children }) {
  const [active, setActive] = React.useState(0);
  const tabs = React.Children.toArray(children);
  return (
    <div>
      <div style={{display:'flex', gap:'0.5rem', flexWrap:'wrap', marginBottom:'1rem', justifyContent:'center'}}>
        {tabs.map((tab, i)=> (
          <button key={i} className={`btn ${i===active? 'btn-primary':'btn-secondary'}`} onClick={()=>setActive(i)}>
            {tab.props.label}
          </button>
        ))}
      </div>
      <div>
        {tabs[active]}
      </div>
    </div>
  );
}

function UploadSummarize() {
  const fileRef = useRef(null);
  const [notes, setNotes] = React.useState('');
  const [recs, setRecs] = React.useState([]);
  const [text, setText] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const submitFile = async () => {
    if (!fileRef.current?.files?.length && !text.trim()) return;
    setLoading(true);
    setNotes('');
    setRecs([]);
    try {
      if (fileRef.current?.files?.length) {
        const form = new FormData();
        form.append('file', fileRef.current.files[0]);
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000'}/api/summarize-upload`, { method: 'POST', body: form });
        const data = await res.json();
        setNotes(data.notes || '');
        setRecs(data.recommended_videos || []);
      } else {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000'}/api/summarize-upload`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ transcript: text })
        });
        const data = await res.json();
        setNotes(data.notes || '');
        setRecs(data.recommended_videos || []);
      }
    } catch (e) {
      setNotes(`Failed to summarize: ${e.message || e}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{display:'flex', gap:'1rem', flexWrap:'wrap', justifyContent:'center'}}>
        <input type="file" ref={fileRef} accept=".pdf,.pptx,.docx" />
        <button className="btn btn-primary" onClick={submitFile} disabled={loading}>{loading ? 'Summarizing…' : 'Summarize'}</button>
      </div>
      <div style={{marginTop:'0.75rem'}}>
        <textarea placeholder="Or paste transcript text here" value={text} onChange={(e)=>setText(e.target.value)} rows={4} style={{width:'100%', border:'1px solid #e5e7eb', borderRadius:8, padding:10}} />
      </div>
      {notes && (
        <div style={{textAlign:'left', marginTop:'1rem'}}>
          <h4>📝 Study Notes</h4>
          <div style={{whiteSpace:'pre-wrap'}}>{notes}</div>
        </div>
      )}
      {recs && recs.length > 0 && (
        <div style={{textAlign:'left', marginTop:'1rem'}}>
          <h4>🔗 Recommended Videos</h4>
          <ul>
            {recs.map((v, i)=> (
              <li key={i}><a href={v.url} target="_blank" rel="noreferrer">{v.title}</a> <span style={{color:'#6b7280'}}>• {v.channel}</span></li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function TutorChat() {
  const [messages, setMessages] = React.useState(() => {
    try {
      const saved = localStorage.getItem('tutorChat');
      return saved ? JSON.parse(saved) : [];
    } catch { return []; }
  });
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    try { localStorage.setItem('tutorChat', JSON.stringify(messages)); } catch {}
  }, [messages]);

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    setInput('');
    const userMsg = { role: 'user', text: q };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    try {
      const res = await askAI(q, null, null);
      const aiText = res?.answer || 'Sorry, I could not generate an answer.';
      setMessages(prev => [...prev, { role: 'ai', text: aiText }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'ai', text: e.message || 'Failed to answer.' }]);
    } finally {
      setLoading(false);
    }
  };

  const clear = () => { setMessages([]); };

  return (
    <div>
      <div style={{maxHeight: 320, overflowY: 'auto', border: '1px solid #e5e7eb', borderRadius: 10, padding: 12, background: '#ffffff'}}>
        {messages.length === 0 && (
          <div style={{color:'#6b7280'}}>Ask any question about your studies. Example: "Explain backpropagation simply with an example".</div>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{marginBottom: 10}}>
            <div style={{fontWeight:600, color: m.role==='user' ? '#1f2937' : '#4f46e5'}}>{m.role==='user' ? 'You' : 'Tutor'}</div>
            <div style={{whiteSpace:'pre-wrap'}}>{m.text}</div>
          </div>
        ))}
      </div>
      <div style={{display:'flex', gap:8, marginTop:10}}>
        <input value={input} onChange={(e)=>setInput(e.target.value)} onKeyDown={(e)=>{ if(e.key==='Enter') send(); }} placeholder="Type your question..." style={{flex:1, border:'1px solid #e5e7eb', borderRadius:8, padding:'10px 12px'}} />
        <button className="btn btn-primary" onClick={send} disabled={loading || !input.trim()}>{loading ? 'Thinking…' : 'Send'}</button>
        <button className="btn btn-secondary" onClick={clear} disabled={messages.length===0}>Clear</button>
      </div>
    </div>
  );
}
