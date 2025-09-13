from youtube_service import YouTubeService
from ai_service import AIService
import logging

logger = logging.getLogger(__name__)

class CourseBuilder:
    def __init__(self):
        self.youtube_service = YouTubeService()
        self.ai_service = AIService()
    
    def build_course_from_videos(self, video_urls):
        """Main method to build a complete course from YouTube video URLs"""
        try:
            # Step 1: Process each video URL
            video_data_list = []
            all_concepts = []
            
            for url in video_urls:
                logger.info(f"Processing video: {url}")
                
                # Validate URL
                if not self.youtube_service.validate_youtube_url(url):
                    logger.warning(f"Invalid YouTube URL: {url}")
                    continue
                
                # Get video data and transcript
                video_data = self.youtube_service.get_video_data(url)
                if not video_data:
                    logger.warning(f"Could not process video: {url}")
                    continue
                
                video_data_list.append(video_data)
                
                # Extract concepts using AI
                if video_data.get('has_transcript'):
                    concepts = self.ai_service.extract_concepts_and_timestamps(video_data)
                    
                    # Add video reference to each concept
                    for concept in concepts:
                        concept['video_id'] = video_data['id']
                        concept['video_title'] = video_data['title']
                        concept['video_url'] = video_data['url']
                        concept['video_thumbnail'] = video_data.get('thumbnail', '')
                    
                    all_concepts.extend(concepts)
                    logger.info(f"Extracted {len(concepts)} concepts from {video_data['title']}")
                else:
                    logger.warning(f"No transcript available for {video_data['title']}")
            
            if not all_concepts:
                return {
                    "error": "No concepts could be extracted from the provided videos",
                    "processed_videos": len(video_data_list),
                    "videos_with_transcripts": len([v for v in video_data_list if v.get('has_transcript')])
                }
            
            # Step 2: Generate course structure
            course_structure = self.ai_service.generate_course_structure(all_concepts, video_data_list)
            
            # Step 3: Add video metadata to course
            course_data = {
                **course_structure,
                "videos": video_data_list,
                "total_videos": len(video_data_list),
                "concepts_per_video": len(all_concepts) / len(video_data_list) if video_data_list else 0
            }
            
            logger.info(f"Successfully built course with {len(all_concepts)} concepts from {len(video_data_list)} videos")
            return course_data
            
        except Exception as e:
            logger.error(f"Error building course: {e}")
            return {
                "error": f"Failed to build course: {str(e)}",
                "processed_videos": 0,
                "concepts_extracted": 0
            }
    
    def get_video_info_only(self, video_urls):
        """Get just video metadata without AI processing (for quick preview)"""
        video_data_list = []
        
        for url in video_urls:
            if not self.youtube_service.validate_youtube_url(url):
                continue
                
            video_data = self.youtube_service.get_video_data(url)
            if video_data:
                # Remove transcript to save bandwidth
                video_data.pop('transcript', None)
                video_data_list.append(video_data)
        
        return {
            "videos": video_data_list,
            "total_videos": len(video_data_list),
            "preview_only": True
        }
