from typing import Dict, Any
from datetime import datetime

from clients.gemini_client import GeminiClient
from config.logger import logger


class WorkoutAnalyzer:
    """Analyzes completed workouts to extract insights and feedback."""
    
    def __init__(self, gemini_client: GeminiClient) -> None:
        self.gemini_client = gemini_client
        logger.info("WorkoutAnalyzer initialized")
    
    def analyze_workout(
        self,
        workout_data: Dict[str, Any],
        feedback_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze a completed workout and provide insights."""
        try:
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(
                workout_data,
                feedback_data,
                user_profile
            )
            
            response = self.gemini_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format={"type": "json_object"}
            )
            
            import json
            analysis = json.loads(response)
            
            logger.info("Workout analysis completed")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing workout: {e}", exc_info=True)
            raise
    
    def extract_feedback_from_notion(self, notion_page_content: str) -> Dict[str, Any]:
        """Extract structured feedback from Notion page content."""
        try:
            system_prompt = """You are a fitness data extractor. Extract structured workout feedback from unstructured text.

Extract the following fields if present:
- completion_percentage (0-100)
- rpe (1-10)
- pain_level (0-5)
- recovery_quality (poor/fair/good/excellent)
- sleep_hours (0-24)
- notes (any additional feedback)

Return as JSON."""
            
            user_prompt = f"Extract workout feedback from this text:\n\n{notion_page_content}"
            
            response = self.gemini_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format={"type": "json_object"}
            )
            
            import json
            feedback = json.loads(response)
            
            logger.debug("Extracted feedback from Notion")
            return feedback
            
        except Exception as e:
            logger.error(f"Error extracting feedback from Notion: {e}", exc_info=True)
            raise
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for workout analysis."""
        return """You are an expert calisthenics coach analyzing workout performance.

Your task is to analyze completed workouts and provide actionable insights.

Analysis should include:
1. Performance assessment (strength, endurance, technique)
2. Recovery evaluation based on feedback
3. Progress indicators
4. Areas for improvement
5. Recommendations for next workout

Output format: JSON with the following structure:
{
    "performance_summary": "brief summary of performance",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "recovery_assessment": "assessment of recovery quality",
    "progress_indicators": {
        "strength": "improving/stable/regressing",
        "endurance": "improving/stable/regressing",
        "technique": "improving/stable/regressing"
    },
    "recommendations": ["recommendation1", "recommendation2"],
    "next_workout_adjustments": {
        "intensity": "increase/maintain/decrease",
        "volume": "increase/maintain/decrease",
        "focus_areas": ["area1", "area2"]
    }
}"""
    
    def _build_user_prompt(
        self,
        workout_data: Dict[str, Any],
        feedback_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> str:
        """Build the user prompt with workout context."""
        prompt = f"""Analyze this completed workout.

User Profile:
- Name: {user_profile.get('name', 'Athlete')}
- Level: {user_profile.get('level', 'beginner')}
- Goal: {user_profile.get('goal', 'Improve fitness')}

Workout Details:
- Date: {workout_data.get('date', 'Unknown')}
- Type: {workout_data.get('day_type', 'Unknown')}
- Greeting: {workout_data.get('greeting', 'N/A')}

Feedback:
- Completion: {feedback_data.get('completion_percentage', 0)}%
- RPE: {feedback_data.get('rpe', 'N/A')}/10
- Pain Level: {feedback_data.get('pain_level', 0)}/5
- Recovery Quality: {feedback_data.get('recovery_quality', 'N/A')}
- Sleep: {feedback_data.get('sleep_hours', 0)} hours
- Notes: {feedback_data.get('notes', 'None')}

Provide a comprehensive analysis with specific recommendations."""
        
        return prompt
