from .youtube_service import YouTubeService
from .ai_service import AIService
import logging
from typing import List, Dict, Any, Optional
import concurrent.futures
import threading
from functools import partial
import re

logger = logging.getLogger(__name__)

class CourseBuilder:
    def __init__(self):
        try:
            self.youtube_service = YouTubeService()
            self.ai_service = AIService()
            self.max_workers = 3  # Limit concurrent operations
        except Exception as e:
            logger.error(f"Failed to initialize CourseBuilder: {e}")
            raise
    
    def build_course_from_videos(self, video_urls: List[str]) -> Dict[str, Any]:
        """Main method to build a complete course from YouTube video URLs with parallel processing"""
        if not video_urls:
            return {
                "error": "No video URLs provided",
                "processed_videos": 0,
                "concepts_extracted": 0
            }
        
        try:
            # Step 1: Process video URLs in parallel for better performance
            video_data_list = self._process_videos_parallel(video_urls)
            
            if not video_data_list:
                return {
                    "error": "No valid videos could be processed from the provided URLs",
                    "processed_videos": 0,
                    "invalid_urls": len(video_urls)
                }
            
            # Step 2: Extract concepts from videos with transcripts
            all_concepts = self._extract_concepts_from_videos(video_data_list)
            
            if not all_concepts:
                return {
                    "error": "No concepts could be extracted from the provided videos",
                    "processed_videos": len(video_data_list),
                    "videos_with_transcripts": len([v for v in video_data_list if v.get('has_transcript')]),
                    "message": "Videos may not have available transcripts or captions"
                }
            
            # Step 3: Generate course structure
            course_structure = self.ai_service.generate_course_structure(all_concepts, video_data_list)
            
            # Step 4: Compile final course data with enhanced metadata
            course_data = {
                **course_structure,
                "videos": video_data_list,
                "total_videos": len(video_data_list),
                "videos_with_transcripts": len([v for v in video_data_list if v.get('has_transcript')]),
                "concepts_per_video": len(all_concepts) / len(video_data_list) if video_data_list else 0,
                "processing_stats": {
                    "total_urls_provided": len(video_urls),
                    "valid_videos_processed": len(video_data_list),
                    "concepts_extracted": len(all_concepts),
                    "success_rate": len(video_data_list) / len(video_urls) * 100
                }
            }
            
            logger.info(f"Successfully built course: {len(all_concepts)} concepts from {len(video_data_list)} videos")
            return course_data
            
        except Exception as e:
            logger.error(f"Error building course: {e}")
            return {
                "error": f"Failed to build course: {str(e)}",
                "processed_videos": 0,
                "concepts_extracted": 0
            }
    
    def _process_videos_parallel(self, video_urls: List[str]) -> List[Dict[str, Any]]:
        """Process multiple video URLs in parallel for better performance"""
        video_data_list = []
        
        def process_single_video(url: str) -> Optional[Dict[str, Any]]:
            try:
                # Validate URL
                if not self.youtube_service.validate_youtube_url(url):
                    logger.warning(f"Invalid YouTube URL: {url}")
                    return None
                
                # Get video data and transcript
                video_data = self.youtube_service.get_video_data(url)
                if video_data:
                    logger.info(f"Successfully processed video: {video_data.get('title', 'Unknown')}")
                    return video_data
                else:
                    logger.warning(f"Could not process video: {url}")
                    return None
                    
            except Exception as e:
                logger.error(f"Error processing video {url}: {e}")
                return None
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all video processing tasks
            future_to_url = {executor.submit(process_single_video, url): url for url in video_urls}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                if result:
                    video_data_list.append(result)
        
        return video_data_list
    
    def _extract_concepts_from_videos(self, video_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract concepts from videos.
        Always attempt extraction; the AI service will gracefully fall back when transcripts are missing.
        """
        all_concepts = []
        
        for video_data in video_data_list:
            try:
                # Attempt extraction regardless of transcript availability; AI service handles fallback
                concepts = self.ai_service.extract_concepts_and_timestamps(video_data)

                # Add video reference to each concept
                for concept in concepts:
                    concept.update({
                        'video_id': video_data['id'],
                        'video_title': video_data['title'],
                        'video_url': video_data['url'],
                        'video_thumbnail': video_data.get('thumbnail', ''),
                        'video_channel': video_data.get('channel', ''),
                        'video_duration': video_data.get('duration', '')
                    })

                # Compute end timestamps per video to enable range playback
                if concepts:
                    self._compute_end_timestamps_for_video(concepts, video_data.get('duration', ''))

                if concepts:
                    all_concepts.extend(concepts)
                    logger.info(f"Extracted {len(concepts)} concepts from {video_data.get('title', 'Unknown')}")
                else:
                    logger.warning(f"No concepts extracted for {video_data.get('title', 'Unknown')}")
                    
            except Exception as e:
                logger.error(f"Error extracting concepts from video {video_data.get('title', 'Unknown')}: {e}")
                continue
        
        return all_concepts

    def _compute_end_timestamps_for_video(self, concepts: List[Dict[str, Any]], iso_duration: str) -> None:
        """Fill timestamp_end_seconds and timestamp_end for concepts within the same video."""
        def parse_iso_duration_to_seconds(iso: str) -> int:
            if not iso or not isinstance(iso, str):
                return 0
            match = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
            if not match:
                return 0
            days = int(match.group(1) or 0)
            hours = int(match.group(2) or 0)
            minutes = int(match.group(3) or 0)
            seconds = int(match.group(4) or 0)
            return days * 86400 + hours * 3600 + minutes * 60 + seconds

        def format_mmss(seconds: int) -> str:
            if seconds <= 0:
                return "00:00"
            m, s = divmod(int(seconds), 60)
            if m >= 60:
                h, m = divmod(m, 60)
                return f"{h:01d}:{m:02d}:{s:02d}"
            return f"{m:02d}:{s:02d}"

        video_total = parse_iso_duration_to_seconds(iso_duration)
        # Sort by start seconds
        concepts.sort(key=lambda c: c.get('timestamp_seconds', 0))
        for idx, concept in enumerate(concepts):
            start = int(concept.get('timestamp_seconds') or 0)
            if idx < len(concepts) - 1:
                next_start = int(concepts[idx + 1].get('timestamp_seconds') or (start + 60))
                end = max(start, next_start - 1)
            else:
                end = video_total if video_total > 0 else start + 120
            concept['timestamp_end_seconds'] = max(end, start)
            concept['timestamp_end'] = format_mmss(concept['timestamp_end_seconds'])
    
    def get_video_info_only(self, video_urls: List[str]) -> Dict[str, Any]:
        """Get just video metadata without AI processing (for quick preview)"""
        if not video_urls:
            return {
                "error": "No video URLs provided",
                "videos": [],
                "total_videos": 0,
                "preview_only": True
            }
        
        try:
            # Process videos in parallel for faster preview
            video_data_list = self._process_videos_parallel(video_urls)
            
            # Remove transcript data to save bandwidth
            for video_data in video_data_list:
                video_data.pop('transcript', None)
            
            return {
                "videos": video_data_list,
                "total_videos": len(video_data_list),
                "preview_only": True,
                "processing_stats": {
                    "total_urls_provided": len(video_urls),
                    "valid_videos_found": len(video_data_list),
                    "success_rate": len(video_data_list) / len(video_urls) * 100 if video_urls else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error in video preview: {e}")
            return {
                "error": f"Failed to preview videos: {str(e)}",
                "videos": [],
                "total_videos": 0,
                "preview_only": True
            }
