from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, 
    NoTranscriptFound, 
    VideoUnavailable,
    TooManyRequests
)
import re
import logging
from typing import Optional, Dict, Any, List
from config import Config
import time

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        if not Config.YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY is required but not provided")
        
        try:
            self.youtube = build('youtube', 'v3', developerKey=Config.YOUTUBE_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize YouTube API client: {e}")
            raise
        
        self.rate_limit_delay = 0.5  # seconds between API calls
        self.max_retries = 3
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats with improved validation"""
        if not url or not isinstance(url, str):
            logger.error("Invalid URL provided to extract_video_id")
            return None
        
        # Clean and normalize URL
        url = url.strip()
        
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:v\/|youtu.be\/)([0-9A-Za-z_-]{11})',
            r'youtube\.com\/watch\?v=([0-9A-Za-z_-]{11})',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
            r'youtube\.com\/embed\/([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # Validate video ID format (11 characters, alphanumeric plus - and _)
                if re.match(r'^[0-9A-Za-z_-]{11}$', video_id):
                    return video_id
        
        logger.warning(f"Could not extract valid video ID from URL: {url}")
        return None
    
    def get_video_info(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video metadata from YouTube API with improved error handling"""
        if not video_id:
            logger.error("No video ID provided to get_video_info")
            return None
        
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                if attempt > 0:
                    time.sleep(self.rate_limit_delay * attempt)
                
                response = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=video_id
                ).execute()
                
                if response.get('items'):
                    video = response['items'][0]
                    snippet = video.get('snippet', {})
                    content_details = video.get('contentDetails', {})
                    statistics = video.get('statistics', {})
                    
                    return {
                        'id': video_id,
                        'title': snippet.get('title', 'Unknown Title'),
                        'description': snippet.get('description', ''),
                        'duration': content_details.get('duration', ''),
                        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                        'channel': snippet.get('channelTitle', 'Unknown Channel'),
                        'published_at': snippet.get('publishedAt', ''),
                        'view_count': statistics.get('viewCount', '0'),
                        'like_count': statistics.get('likeCount', '0'),
                        'comment_count': statistics.get('commentCount', '0')
                    }
                else:
                    logger.warning(f"No video found with ID: {video_id}")
                    return None
                    
            except HttpError as e:
                if e.resp.status == 403:
                    logger.error(f"API quota exceeded or forbidden access: {e}")
                    return None
                elif e.resp.status == 404:
                    logger.warning(f"Video not found: {video_id}")
                    return None
                else:
                    logger.error(f"HTTP error fetching video info for {video_id}: {e}")
                    if attempt == self.max_retries - 1:
                        return None
            except Exception as e:
                logger.error(f"Unexpected error fetching video info for {video_id}: {e}")
                if attempt == self.max_retries - 1:
                    return None
        
        return None
    
    def get_transcript(self, video_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get video transcript with timestamps and improved error handling"""
        if not video_id:
            logger.error("No video ID provided to get_transcript")
            return None
        
        try:
            # Try multiple language preferences
            language_preferences = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
            
            # First try manually created transcripts
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id, 
                    languages=language_preferences
                )
            except (NoTranscriptFound, TranscriptsDisabled):
                # Fall back to auto-generated transcripts
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(
                        video_id,
                        languages=['en-auto', 'auto']
                    )
                except (NoTranscriptFound, TranscriptsDisabled):
                    # Try any available transcript
                    available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                    transcript_list = None
                    
                    for transcript in available_transcripts:
                        try:
                            transcript_list = transcript.fetch()
                            break
                        except Exception:
                            continue
                    
                    if not transcript_list:
                        logger.warning(f"No transcripts available for video {video_id}")
                        return None
            
            # Validate and format transcript
            if not transcript_list:
                logger.warning(f"Empty transcript for video {video_id}")
                return None
            
            formatted_transcript = []
            for entry in transcript_list:
                try:
                    formatted_entry = {
                        'start': float(entry.get('start', 0)),
                        'duration': float(entry.get('duration', 0)),
                        'text': str(entry.get('text', '')).replace('\n', ' ').strip()
                    }
                    
                    # Skip empty or very short text entries
                    if len(formatted_entry['text']) > 2:
                        formatted_transcript.append(formatted_entry)
                        
                except (ValueError, TypeError) as e:
                    logger.warning(f"Skipping invalid transcript entry: {e}")
                    continue
            
            if formatted_transcript:
                logger.info(f"Successfully extracted {len(formatted_transcript)} transcript entries for video {video_id}")
                return formatted_transcript
            else:
                logger.warning(f"No valid transcript entries found for video {video_id}")
                return None
            
        except VideoUnavailable:
            logger.warning(f"Video {video_id} is unavailable")
            return None
        except TooManyRequests:
            logger.error(f"Rate limit exceeded for transcript API")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting transcript for {video_id}: {e}")
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
