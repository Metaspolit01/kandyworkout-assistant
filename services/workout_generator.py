from typing import Dict, Any
from datetime import datetime

from clients.gemini_client import GeminiClient
from services.workout_planner import WorkoutPlanner, WorkoutDay
from config.logger import logger


class WorkoutGenerator:
    """Generates workout plans using Google Gemini."""
    
    def __init__(self, gemini_client: GeminiClient, workout_planner: WorkoutPlanner) -> None:
        self.gemini_client = gemini_client
        self.workout_planner = workout_planner
        logger.info("WorkoutGenerator initialized")
    
    def generate_workout(
        self,
        user_profile: Dict[str, Any],
        workout_history: list[Dict[str, Any]],
        coach_memory: Dict[str, Any],
        date: datetime
    ) -> Dict[str, Any]:
        """Generate a complete workout for the given date."""
        try:
            workout_day = self.workout_planner.get_workout_day(date)
            workout_day_name = self.workout_planner.get_workout_day_name(workout_day)
            focus_areas = self.workout_planner.get_focus_areas(workout_day)
            
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(
                user_profile,
                workout_history,
                coach_memory,
                workout_day,
                workout_day_name,
                focus_areas,
                date
            )
            
            response = self.gemini_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format={"type": "json_object"}
            )
            
            import json
            workout_data = json.loads(response)
            
            # Add metadata
            workout_data["day_type"] = workout_day.value
            workout_data["date"] = date.isoformat()
            
            logger.info(f"Generated workout for {workout_day_name}")
            return workout_data
            
        except Exception as e:
            logger.error(f"Error generating workout: {e}", exc_info=True)
            raise
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for workout generation."""
        return """You are an expert calisthenics coach specializing in progressive training for beginners to advanced athletes. 

Your task is to generate personalized, structured workout plans that follow proper exercise science principles.

Rules:
1. Always include proper warm-up and cool-down
2. Focus on form and technique over volume
3. Use progressive overload principles
4. Include specific rest times
5. Provide technique tips for each exercise
6. Make workouts challenging but achievable
7. Include daily habits that support fitness goals

Output format: JSON with the following structure:
{
    "greeting": "motivational message",
    "warmup": {
        "name": "Warm-up",
        "exercises": [
            {
                "name": "exercise name",
                "sets": number,
                "reps": "rep range or AMRAP",
                "rest_seconds": number,
                "technique_tips": ["tip1", "tip2"]
            }
        ]
    },
    "main_workout": {
        "name": "Main Workout",
        "exercises": [...]
    },
    "cooldown": {
        "name": "Cooldown",
        "exercises": [...]
    },
    "daily_habits": ["habit1", "habit2"]
}"""
    
    def _build_user_prompt(
        self,
        user_profile: Dict[str, Any],
        workout_history: list[Dict[str, Any]],
        coach_memory: Dict[str, Any],
        workout_day: WorkoutDay,
        workout_day_name: str,
        focus_areas: list[str],
        date: datetime
    ) -> str:
        """Build the user prompt with context."""
        prompt = f"""Generate a {workout_day_name} workout for {date.strftime("%A, %B %d, %Y")}.

User Profile:
- Name: {user_profile.get('name', 'Athlete')}
- Age: {user_profile.get('age', 20)}
- Height: {user_profile.get('height_cm', 170)} cm
- Weight: {user_profile.get('weight_kg', 70)} kg
- Level: {user_profile.get('level', 'beginner')}
- Goal: {user_profile.get('goal', 'Improve fitness')}

Focus Areas: {', '.join(focus_areas)}

"""
        
        if workout_history:
            prompt += f"Recent Workouts ({len(workout_history)} total):\n"
            for workout in workout_history[-3:]:  # Last 3 workouts
                prompt += f"- {workout.get('date', 'Unknown')}: {workout.get('day_type', 'Unknown')}\n"
            prompt += "\n"
        
        if coach_memory:
            prompt += "Coach Notes:\n"
            for memory in coach_memory:
                prompt += f"- {memory.get('key', 'Unknown')}: {memory.get('value', {})}\n"
            prompt += "\n"
        
        prompt += f"""Generate a complete workout with:
1. A motivational greeting (2-3 sentences)
2. Warm-up (3-5 exercises, light intensity)
3. Main workout (5-8 exercises appropriate for {user_profile.get('level', 'beginner')} level)
4. Cooldown (3-4 stretching exercises)
5. 3-5 daily habits that support recovery and progress

Ensure exercises are appropriate for the focus areas and user's current level."""
        
        return prompt
