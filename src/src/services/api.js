import axios from 'axios';

// Configure base URL for API
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// Create axios instance with enhanced config
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 60000, // Increased timeout for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
  // Retry configuration
  retry: 3,
  retryDelay: 1000,
  retryCondition: (error) => {
    return error.response?.status >= 500 || error.code === 'ECONNABORTED';
  }
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
    
    // Enhanced error handling with user-friendly messages
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data;
      
      switch (status) {
        case 400:
          error.message = data.message || 'Invalid request. Please check your input.';
          break;
        case 403:
          error.message = 'API access forbidden. Please check your API keys.';
          break;
        case 404:
          error.message = 'API endpoint not found.';
          break;
        case 413:
          error.message = 'Request too large. Please try with fewer videos.';
          break;
        case 429:
          error.message = 'Too many requests. Please wait and try again.';
          break;
        case 500:
          error.message = data.message || 'Server error. Please try again later.';
          break;
        case 503:
          error.message = 'Service temporarily unavailable. Please try again later.';
          break;
        default:
          error.message = data.message || `Server error (${status}). Please try again.`;
      }
    } else if (error.request) {
      // Network error
      error.message = 'Network error. Please check your internet connection.';
    } else {
      // Other error
      error.message = error.message || 'An unexpected error occurred.';
    }
    
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

// Tutor Q&A
export async function askAI(question, video, concept) {
  const payload = { question, video, concept };
  const response = await api.post('/ask-question', payload);
  return response.data;
}

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
