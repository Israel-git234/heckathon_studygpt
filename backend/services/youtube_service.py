from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import re
import logging
from config import Config

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=Config.YOUTUBE_API_KEY)
    
    def extract_video_id(self, url):
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:v\/|youtu.be\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        logger.warning(f"Could not extract video ID from URL: {url}")
        return None
    
    def get_video_info(self, video_id):
        """Get video metadata from YouTube API"""
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            
            if response['items']:
                video = response['items'][0]
                return {
                    'id': video_id,
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'duration': video['contentDetails']['duration'],
                    'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'channel': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': video['statistics'].get('viewCount', '0')
                }
            else:
                logger.warning(f"No video found with ID: {video_id}")
                
        except Exception as e:
            logger.error(f"Error fetching video info for {video_id}: {e}")
        
        return None
    
    def get_transcript(self, video_id):
        """Get video transcript with timestamps"""
        try:
            # Try to get transcript in English first, then any available language
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['en', 'en-US', 'en-GB', 'auto']
            )
            
            # Format transcript with timestamps
            formatted_transcript = []
            for entry in transcript_list:
                formatted_transcript.append({
                    'start': float(entry['start']),
                    'duration': float(entry['duration']),
                    'text': entry['text'].replace('\n', ' ').strip()
                })
            
            logger.info(f"Successfully extracted transcript for video {video_id}")
            return formatted_transcript
            
        except Exception as e:
            logger.warning(f"Could not get transcript for {video_id}: {e}")
            return None
    
    def get_video_data(self, url):
        """Get complete video data including transcript"""
        video_id = self.extract_video_id(url)
        if not video_id:
            return None
        
        # Get video metadata
        video_info = self.get_video_info(video_id)
        if not video_info:
            return None
        
        # Get transcript
        transcript = self.get_transcript(video_id)
        
        return {
            **video_info,
            'url': url,
            'transcript': transcript,
            'has_transcript': transcript is not None
        }
    
    def validate_youtube_url(self, url):
        """Validate if URL is a proper YouTube URL"""
        youtube_patterns = [
            r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)',
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        
        return False
