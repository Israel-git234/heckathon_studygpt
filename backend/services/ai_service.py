import google.generativeai as genai
from config import Config
import json
import re
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_concepts_and_timestamps(self, video_data):
        """Extract key concepts with timestamps from video transcript"""
        if not video_data.get('transcript'):
            logger.warning(f"No transcript available for video: {video_data.get('title', 'Unknown')}")
            return []
        
        # Prepare transcript text with timestamps
        transcript_text = self._format_transcript_for_ai(video_data['transcript'])
        
        # Truncate if too long to fit in context window
        if len(transcript_text) > 4000:
            transcript_text = transcript_text[:4000] + "..."
            logger.info("Truncated transcript to fit context window")
        
        prompt = self._build_concept_extraction_prompt(video_data, transcript_text)
        
        try:
            # Use Gemini API instead of OpenAI
            response = self.model.generate_content(
                f"You are an expert educational content analyzer. Extract key learning concepts from video transcripts with precise timestamps.\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1500,
                )
            )
            
            result = response.text.strip()
            logger.info(f"AI analysis completed for video: {video_data.get('title', 'Unknown')}")
            
            # Try to parse JSON response
            try:
                parsed_result = json.loads(result)
                return parsed_result.get('concepts', [])
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, trying fallback extraction")
                return self._parse_concepts_fallback(result)
                
        except Exception as e:
            logger.error(f"Error extracting concepts: {e}")
            return self._create_fallback_concepts(video_data)
    
    def _format_transcript_for_ai(self, transcript):
        """Format transcript with timestamps for AI analysis"""
        formatted_lines = []
        
        for entry in transcript[:50]:  # Limit to first 50 entries to avoid token limits
            timestamp = int(entry['start'])
            minutes = timestamp // 60
            seconds = timestamp % 60
            formatted_lines.append(f"[{minutes:02d}:{seconds:02d}] {entry['text']}")
        
        return "\n".join(formatted_lines)
    
    def _build_concept_extraction_prompt(self, video_data, transcript_text):
        """Build the prompt for concept extraction"""
        return f"""
Analyze this educational video transcript and extract 3-5 key learning concepts. 

Video Title: {video_data['title']}
Video Description: {video_data.get('description', '')[:200]}...

For each concept:
1. Identify the main topic/concept name (be specific and clear)
2. Find the best timestamp where it's first explained (format: MM:SS)
3. Write a 2-3 sentence summary explaining the concept
4. Create 1-2 multiple choice quiz questions to test understanding

Transcript with timestamps:
{transcript_text}

Return response as valid JSON in this exact format:
{{
    "concepts": [
        {{
            "name": "Concept Name",
            "timestamp": "MM:SS",
            "timestamp_seconds": 123,
            "summary": "Clear 2-3 sentence explanation of the concept",
            "quiz": [
                {{
                    "question": "What is the main purpose of this concept?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": 0,
                    "explanation": "Brief explanation of why this is correct"
                }}
            ]
        }}
    ]
}}
        """
    
    def _parse_concepts_fallback(self, text):
        """Fallback parsing if JSON parsing fails"""
        concepts = []
        
        # Try to extract concepts using regex patterns
        concept_patterns = {
            'name': r'"name":\s*"([^"]+)"',
            'timestamp': r'"timestamp":\s*"([^"]+)"',
            'summary': r'"summary":\s*"([^"]+)"',
        }
        
        concept_matches = {}
        for key, pattern in concept_patterns.items():
            concept_matches[key] = re.findall(pattern, text)
        
        # Build concepts from matches
        max_concepts = min(len(matches) for matches in concept_matches.values())
        
        for i in range(max_concepts):
            try:
                concept = {
                    'name': concept_matches['name'][i],
                    'timestamp': concept_matches['timestamp'][i],
                    'timestamp_seconds': self._convert_timestamp(concept_matches['timestamp'][i]),
                    'summary': concept_matches['summary'][i],
                    'quiz': [{
                        'question': f"What is the key point about {concept_matches['name'][i]}?",
                        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                        'correct': 0,
                        'explanation': 'This is a fallback question.'
                    }]
                }
                concepts.append(concept)
            except (IndexError, KeyError):
                continue
        
        return concepts[:3]  # Return at most 3 concepts
    
    def _create_fallback_concepts(self, video_data):
        """Create basic concepts when AI fails"""
        return [{
            'name': f"Introduction to {video_data.get('title', 'Topic')}",
            'timestamp': "00:00",
            'timestamp_seconds': 0,
            'summary': f"This video covers {video_data.get('title', 'the main topic')}. Watch to learn the key concepts and practical applications.",
            'quiz': [{
                'question': 'What is the main topic of this video?',
                'options': [
                    video_data.get('title', 'Main Topic'),
                    'Something else',
                    'Not specified',
                    'Multiple topics'
                ],
                'correct': 0,
                'explanation': 'The video title indicates the main topic.'
            }]
        }]
    
    def _convert_timestamp(self, timestamp_str):
        """Convert MM:SS or HH:MM:SS to seconds"""
        try:
            parts = timestamp_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except (ValueError, IndexError):
            logger.warning(f"Could not parse timestamp: {timestamp_str}")
        return 0
    
    def generate_course_structure(self, all_concepts, video_data_list):
        """Organize concepts into a structured course"""
        if not all_concepts:
            return {
                "course_title": "Generated Course",
                "modules": []
            }
        
        # Simple grouping for MVP - can be enhanced later
        course_title = self._generate_course_title(video_data_list)
        
        # Group concepts by video or create logical modules
        modules = self._create_modules(all_concepts)
        
        return {
            "course_title": course_title,
            "modules": modules,
            "total_concepts": len(all_concepts),
            "estimated_duration": f"{len(all_concepts) * 10}-{len(all_concepts) * 15} minutes"
        }
    
    def _generate_course_title(self, video_data_list):
        """Generate a course title based on video titles"""
        if not video_data_list:
            return "Generated Course"
        
        # Extract common themes from video titles
        titles = [video.get('title', '') for video in video_data_list]
        
        # Simple heuristic: use first video title as base
        base_title = titles[0] if titles else "Video Course"
        
        # Clean up and make it course-like
        if len(titles) > 1:
            return f"Complete Guide: {base_title.split()[0] if base_title.split() else 'Learning'} Course"
        else:
            return f"Learning: {base_title}"
    
    def _create_modules(self, all_concepts):
        """Create course modules from concepts"""
        if not all_concepts:
            return []
        
        # Simple approach: group by video or create single module
        # Can be enhanced with AI-based grouping later
        
        modules = []
        current_module = {
            "module_name": "Core Concepts",
            "concepts": all_concepts
        }
        modules.append(current_module)
        
        return modules
