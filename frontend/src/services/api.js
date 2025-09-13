import axios from 'axios';

// Configure base URL for API
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000, // 30 second timeout for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  },

  // Generate course from video URLs
  async generateCourse(videoUrls) {
    try {
      const response = await api.post('/generate-course', {
        video_urls: videoUrls
      });
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error(`Course generation failed: ${error.message}`);
    }
  },

  // Preview videos without AI processing
  async previewVideos(videoUrls) {
    try {
      const response = await api.post('/preview-videos', {
        video_urls: videoUrls
      });
      return response.data;
    } catch (error) {
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error(`Video preview failed: ${error.message}`);
    }
  }
};

// Utility functions
export const isValidYouTubeUrl = (url) => {
  const youtubePatterns = [
    /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)/,
    /^https?:\/\/(www\.)?youtube\.com\/playlist\?list=/,
    /^https?:\/\/(www\.)?youtube\.com\/channel\//
  ];
  
  return youtubePatterns.some(pattern => pattern.test(url));
};

export const extractVideoId = (url) => {
  const patterns = [
    /(?:v=|\/)([0-9A-Za-z_-]{11}).*/,
    /(?:embed\/)([0-9A-Za-z_-]{11})/,
    /(?:v\/|youtu\.be\/)([0-9A-Za-z_-]{11})/
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }
  return null;
};

export const formatDuration = (duration) => {
  if (!duration) return 'Unknown';
  
  // Handle ISO 8601 duration format (PT4M13S)
  const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (match) {
    const hours = parseInt(match[1] || 0);
    const minutes = parseInt(match[2] || 0);
    const seconds = parseInt(match[3] || 0);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    } else {
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
  }
  
  return duration;
};

export const formatTimestamp = (timestamp) => {
  if (typeof timestamp === 'number') {
    const minutes = Math.floor(timestamp / 60);
    const seconds = Math.floor(timestamp % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
  
  if (typeof timestamp === 'string' && timestamp.includes(':')) {
    return timestamp;
  }
  
  return '00:00';
};

export default apiService;
