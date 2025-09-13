import google.generativeai as genai
from config import Config
import json
import re
import logging
from typing import List, Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Configure Gemini API with validation
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required but not provided")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.rate_limit_delay = 1  # seconds between API calls
        self.max_retries = 3
    
    def extract_concepts_and_timestamps(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key concepts with timestamps from video transcript"""
        if not video_data or not isinstance(video_data, dict):
            logger.error("Invalid video_data provided to extract_concepts_and_timestamps")
            return []
        
        if not video_data.get('transcript'):
            logger.warning(f"No transcript available for video: {video_data.get('title', 'Unknown')}")
            return self._create_fallback_concepts(video_data)
        
        # Prepare transcript text with timestamps
        transcript_text = self._format_transcript_for_ai(video_data['transcript'])
        
        # Truncate if too long to fit in context window
        if len(transcript_text) > 4000:
            transcript_text = transcript_text[:4000] + "..."
            logger.info("Truncated transcript to fit context window")
        
        prompt = self._build_concept_extraction_prompt(video_data, transcript_text)
        
        # Retry logic for API calls
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                if attempt > 0:
                    time.sleep(self.rate_limit_delay * attempt)
                
                # Use Gemini API with improved error handling
                response = self.model.generate_content(
                    f"You are an expert educational content analyzer. Extract key learning concepts from video transcripts with precise timestamps.\n\n{prompt}",
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=1500,
                        top_p=0.8,
                        top_k=40
                    )
                )
                
                if not response or not hasattr(response, 'text'):
                    raise ValueError("Empty or invalid response from Gemini API")
            
                result = response.text.strip()
                logger.info(f"AI analysis completed for video: {video_data.get('title', 'Unknown')}")
                
                # Validate response content
                if not result:
                    raise ValueError("Empty response from AI model")
                
                # Try to parse JSON response
                try:
                    parsed_result = json.loads(result)
                    concepts = parsed_result.get('concepts', [])
                    
                    # Validate concepts structure
                    if self._validate_concepts(concepts):
                        return concepts
                    else:
                        logger.warning("Invalid concepts structure, using fallback")
                        return self._parse_concepts_fallback(result)
                        
                except json.JSONDecodeError as json_error:
                    logger.warning(f"Failed to parse JSON response: {json_error}, trying fallback extraction")
                    return self._parse_concepts_fallback(result)
                    
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All attempts failed for video: {video_data.get('title', 'Unknown')}")
                    return self._create_fallback_concepts(video_data)
                continue
        
        return self._create_fallback_concepts(video_data)
    
    def _validate_concepts(self, concepts: List[Dict[str, Any]]) -> bool:
        """Validate the structure and content of extracted concepts"""
        if not isinstance(concepts, list):
            return False
        
        for concept in concepts:
            if not isinstance(concept, dict):
                return False
            
            # Check required fields
            required_fields = ['name', 'timestamp', 'summary']
            for field in required_fields:
                if field not in concept or not concept[field]:
                    return False
            
            # Validate timestamp format
            if not self._is_valid_timestamp(concept.get('timestamp', '')):
                return False
            
            # Validate quiz structure if present
            quiz = concept.get('quiz', [])
            if quiz and not self._validate_quiz(quiz):
                return False
        
        return True
    
    def _is_valid_timestamp(self, timestamp: str) -> bool:
        """Validate timestamp format (MM:SS or HH:MM:SS)"""
        import re
        pattern = r'^(\d{1,2}):([0-5]\d)$|^(\d{1,2}):([0-5]\d):([0-5]\d)$'
        return bool(re.match(pattern, timestamp))
    
    def _validate_quiz(self, quiz: List[Dict[str, Any]]) -> bool:
        """Validate quiz question structure"""
        for question in quiz:
            if not isinstance(question, dict):
                return False
            required_fields = ['question', 'options', 'correct']
            for field in required_fields:
                if field not in question:
                    return False
            
            options = question.get('options', [])
            correct = question.get('correct')
            
            if not isinstance(options, list) or len(options) < 2:
                return False
            
            if not isinstance(correct, int) or correct < 0 or correct >= len(options):
                return False
        
        return True

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
        """Create 3–5 teaching-style concepts when transcripts are missing or AI parsing fails."""
        title = video_data.get('title', 'the topic')
        description = (video_data.get('description') or '').strip()
        # Heuristic bullets from description to create concept stubs
        bullets = []
        for line in description.split('\n'):
            line = line.strip('-• ').strip()
            if 10 <= len(line) <= 140:
                bullets.append(line)
            if len(bullets) >= 5:
                break

        if not bullets:
            bullets = [
                f"Core idea: Introduction to {title}",
                f"Key terms and definitions related to {title}",
                f"Practical example to apply {title}",
            ]

        concepts = []
        for i, bullet in enumerate(bullets[:5]):
            concepts.append({
                'name': bullet.split(':')[0][:60] if ':' in bullet else (bullet[:60] or f"Concept {i+1}"),
                'timestamp': '00:00' if i == 0 else f"0{i}:00" if i < 6 else '00:00',
                'timestamp_seconds': 0 if i == 0 else i * 60,
                'summary': bullet if len(bullet) <= 200 else bullet[:197] + '...',
                'notes': [
                    f"Key idea: {title}",
                    "Definition/intuition in simple words",
                    "One practical example to apply it",
                    "Common pitfall to avoid",
                ],
                'quiz': [{
                    'question': f"What is a key takeaway about {title}?",
                    'options': [
                        'It explains core concepts and examples',
                        'It only shows unrelated content',
                        'It has no educational value',
                        'It is unrelated to the title'
                    ],
                    'correct': 0,
                    'explanation': 'Fallback quiz emphasizes understanding the main idea.'
                }]
            })

        return concepts[:5] if concepts else [{
            'name': f"Introduction to {title}",
            'timestamp': '00:00',
            'timestamp_seconds': 0,
            'summary': f"Overview of {title}.",
            'quiz': [{
                'question': f"What is the main topic of this video?",
                'options': [title, 'Something else', 'Not specified', 'Multiple topics'],
                'correct': 0,
                'explanation': 'The title indicates the topic.'
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

    def answer_question(self, question: str, video_data: Optional[Dict[str, Any]], concept: Optional[Dict[str, Any]] = None) -> str:
        """Answer a learner question grounded in transcript/notes when available."""
        context_parts = []
        if video_data:
            context_parts.append(f"Video Title: {video_data.get('title','')}")
            if video_data.get('transcript'):
                context_parts.append(self._format_transcript_for_ai(video_data['transcript']))
            else:
                context_parts.append((video_data.get('description') or '')[:800])
        if concept:
            context_parts.append(f"Concept: {concept.get('name','')}")
            if concept.get('summary'):
                context_parts.append(f"Summary: {concept['summary']}")
            if concept.get('notes'):
                context_parts.append("Notes:\n- " + "\n- ".join(concept['notes'][:6]))

        prompt = (
            "You are a patient teacher. Answer the learner's question clearly and concisely. "
            "Use the provided context first; if something is unknown, say so and explain how to think about it. "
            "Structure the answer with: brief explanation, simple example, and a takeaway.\n\n"
            f"QUESTION:\n{question}\n\nCONTEXT:\n" + "\n\n".join(context_parts)
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=600,
                    top_p=0.8,
                    top_k=40
                )
            )
            return (response.text or '').strip() if hasattr(response, 'text') else ""
        except Exception as e:
            logger.error(f"Answer question failed: {e}")
            return "Sorry, I couldn't generate an answer right now. Please try again."
    
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
