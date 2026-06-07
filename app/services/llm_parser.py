"""
LLM query parser service
"""
import json
import logging
from typing import Dict, Any

try:
    import google.generativeai as genai
    from config import settings
    
    # Configure Gemini if API key available
    if settings.gemini_api_key:
        genai.configure(api_key=settings.gemini_api_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        gemini_model = None
except ImportError:
    gemini_model = None

logger = logging.getLogger(__name__)


async def parse_query_with_llm(query: str) -> Dict[str, Any]:
    """
    Parse natural language query using LLM
    
    Args:
        query: User's natural language query
    
    Returns:
        Parsed query with structured fields
    """
    # If Gemini not available, use fallback
    if not gemini_model:
        return fallback_query_parser(query)
    
    prompt = f"""You are an anime recommendation query parser. Extract structured information from user queries.

USER QUERY: "{query}"

Extract and return ONLY a JSON object with these fields:
- "visual_elements": list of visual/aesthetic descriptions (e.g., ["rain", "pink skies", "neon lights"])
- "emotions": list of emotional tones (e.g., ["melancholic", "uplifting", "intense"])
- "genres": list of genres if mentioned (e.g., ["romance", "thriller"])
- "themes": list of story themes (e.g., ["coming of age", "revenge"])
- "text_description": natural language summary for semantic search

Example:
INPUT: "I want anime with rain and sad vibes"
OUTPUT: {{"visual_elements": ["rain"], "emotions": ["sad", "melancholic"], "genres": [], "themes": [], "text_description": "sad melancholic anime with rain atmosphere"}}

Now parse the user query and return ONLY the JSON:
"""
    
    try:
        response = gemini_model.generate_content(prompt)
        parsed = json.loads(response.text.strip())
        return parsed
    except Exception as e:
        logger.warning(f"LLM parsing failed: {e}. Using fallback parser.")
        return fallback_query_parser(query)


def fallback_query_parser(query: str) -> Dict[str, Any]:
    """
    Fallback query parser using keyword matching
    
    Args:
        query: User query
    
    Returns:
        Parsed query dictionary
    """
    query_lower = query.lower()
    
    # Visual keywords
    visual_keywords = {
        "rain": ["rain", "rainy", "raining"],
        "pink skies": ["pink sky", "pink skies", "sunset"],
        "neon": ["neon", "cyberpunk", "neon lights"],
        "beautiful art": ["beautiful art", "gorgeous animation", "stunning visuals"],
        "dark": ["dark", "gloomy", "shadowy"],
        "colorful": ["colorful", "vibrant", "bright colors"]
    }
    
    # Emotional keywords
    emotion_keywords = {
        "sad": ["sad", "melancholic", "depressing", "tearjerker"],
        "happy": ["happy", "cheerful", "uplifting", "feel-good"],
        "intense": ["intense", "thrilling", "suspenseful"],
        "calm": ["calm", "peaceful", "relaxing", "iyashikei"],
        "emotional": ["emotional", "touching", "heartwarming"]
    }
    
    # Genre keywords
    genre_keywords = {
        "action": ["action", "fighting", "battles"],
        "romance": ["romance", "love", "romantic"],
        "comedy": ["comedy", "funny", "humorous"],
        "drama": ["drama", "dramatic"],
        "fantasy": ["fantasy", "magical"],
        "sci-fi": ["sci-fi", "science fiction", "scifi"],
        "thriller": ["thriller", "suspense", "mystery"],
        "slice of life": ["slice of life", "sol", "daily life"]
    }
    
    # Extract matches
    visual_elements = []
    for element, keywords in visual_keywords.items():
        if any(kw in query_lower for kw in keywords):
            visual_elements.append(element)
    
    emotions = []
    for emotion, keywords in emotion_keywords.items():
        if any(kw in query_lower for kw in keywords):
            emotions.append(emotion)
    
    genres = []
    for genre, keywords in genre_keywords.items():
        if any(kw in query_lower for kw in keywords):
            genres.append(genre)
    
    return {
        "visual_elements": visual_elements,
        "emotions": emotions,
        "genres": genres,
        "themes": [],
        "text_description": query
    }
