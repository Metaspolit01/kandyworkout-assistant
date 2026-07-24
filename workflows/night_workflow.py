from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any

from clients.gemini_client import GeminiClient
from clients.supabase_client import SupabaseClient
from clients.notion_client import NotionClientWrapper
from repositories.user_repository import UserRepository
from repositories.workout_repository import WorkoutRepository
from repositories.workout_feedback_repository import WorkoutFeedbackRepository
from repositories.coach_memory_repository import CoachMemoryRepository
from repositories.personal_records_repository import PersonalRecordsRepository
from repositories.achievements_repository import AchievementsRepository
from services.workout_analyzer import WorkoutAnalyzer
from services.coach_memory_service import CoachMemoryService
from services.progression_engine import ProgressionEngine
from config.logger import logger


class NightWorkflow:
    """Night workflow: analyzes completed workout and updates progress."""
    
    def __init__(
        self,
        gemini_client: GeminiClient,
        supabase_client: SupabaseClient,
        notion_client: NotionClientWrapper
    ) -> None:
        self.gemini_client = gemini_client
        self.supabase_client = supabase_client
        self.notion_client = notion_client
        
        # Initialize repositories
        self.user_repo = UserRepository(supabase_client)
        self.workout_repo = WorkoutRepository(supabase_client)
        self.workout_feedback_repo = WorkoutFeedbackRepository(supabase_client)
        self.coach_memory_repo = CoachMemoryRepository(supabase_client)
        self.personal_records_repo = PersonalRecordsRepository(supabase_client)
        self.achievements_repo = AchievementsRepository(supabase_client)
        
        # Initialize services
        self.workout_analyzer = WorkoutAnalyzer(self.gemini_client)
        self.coach_memory_service = CoachMemoryService(self.coach_memory_repo)
        self.progression_engine = ProgressionEngine()
        
        logger.info("NightWorkflow initialized")
    
    def execute(self, date: datetime = None) -> Dict[str, Any]:
        """Execute the night workflow."""
        if date is None:
            date = datetime.now(ZoneInfo('Asia/Kolkata'))
        
        logger.info(f"Starting night workflow for {date}")
        
        try:
            # Step 1: Get user profile
            user_profile = self._get_user_profile()
            logger.info(f"User profile loaded: {user_profile['name']}")
            
            # Step 2: Get today's workout
            workout = self._get_todays_workout(date)
            if not workout:
                logger.warning(f"No workout found for {date}")
                return {
                    "success": True,
                    "message": "No workout to analyze",
                    "date": date.isoformat()
                }
            
            logger.info(f"Found workout: {workout['day_type']}")
            
            # Step 3: Get today's Notion page
            notion_page = self._get_notion_page(workout)
            if not notion_page:
                logger.warning(f"No Notion page found for workout {workout['id']}")
                return {
                    "success": True,
                    "message": "No Notion page to analyze",
                    "date": date.isoformat()
                }
            
            # Step 4: Extract feedback from Notion
            feedback_data = self._extract_feedback_from_notion(notion_page)
            logger.info(f"Extracted feedback: completion={feedback_data.get('completion_percentage', 0)}%")
            
            # Step 5: Save feedback to Supabase
            self._save_feedback(workout['id'], feedback_data)
            logger.info("Saved feedback to Supabase")
            
            # Step 6: Analyze workout
            analysis = self._analyze_workout(workout, feedback_data, user_profile)
            logger.info("Workout analysis completed")
            
            # Step 7: Update coach memory
            self._update_coach_memory(user_profile['id'], analysis, feedback_data)
            logger.info("Updated coach memory")
            
            # Step 8: Calculate progression
            workout_history = self._get_workout_history()
            coach_memory = self._get_coach_memory(user_profile['id'])
            progression = self._calculate_progression(feedback_data, workout_history, coach_memory)
            logger.info(f"Progression decision: {progression['decision']}")
            
            # Step 9: Check for personal records
            self._check_personal_records(user_profile['id'], workout, feedback_data)
            
            # Step 10: Check for achievements
            self._check_achievements(user_profile['id'], feedback_data, workout_history)
            
            result = {
                "success": True,
                "workout_id": workout['id'],
                "workout_type": workout['day_type'],
                "feedback": feedback_data,
                "analysis": analysis,
                "progression": progression,
                "date": date.isoformat()
            }
            
            logger.info("Night workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Night workflow failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "date": date.isoformat()
            }
    
    def _get_user_profile(self) -> Dict[str, Any]:
        """Get user profile from Supabase."""
        from config.settings import settings
        user = self.user_repo.get_by_name(settings.USER_NAME)
        if not user:
            raise ValueError(f"User '{settings.USER_NAME}' not found")
        return user
    
    def _get_todays_workout(self, date: datetime) -> Dict[str, Any]:
        """Get today's workout from Supabase."""
        return self.workout_repo.get_by_date(date.date())
    
    def _get_notion_page(self, workout: Dict[str, Any]) -> Dict[str, Any]:
        """Get Notion page for the workout."""
        notion_page_id = workout.get('notion_page_id')
        if not notion_page_id:
            return None
        return self.notion_client.get_page(notion_page_id)
    
    def _extract_feedback_from_notion(self, notion_page: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured feedback from Notion page."""
        # For now, return default feedback
        # In production, this would parse the actual Notion content
        return {
            "completion_percentage": 100.0,
            "rpe": 7,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 8.0,
            "notes": ""
        }
    
    def _save_feedback(self, workout_id: int, feedback_data: Dict[str, Any]) -> None:
        """Save workout feedback to Supabase."""
        feedback_data['workout_id'] = workout_id
        existing_feedback = self.workout_feedback_repo.get_by_workout_id(workout_id)
        
        if existing_feedback:
            self.workout_feedback_repo.update(workout_id, feedback_data)
        else:
            self.workout_feedback_repo.create(feedback_data)
    
    def _analyze_workout(
        self,
        workout: Dict[str, Any],
        feedback_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze workout using AI."""
        return self.workout_analyzer.analyze_workout(
            workout,
            feedback_data,
            user_profile
        )
    
    def _update_coach_memory(
        self,
        user_id: int,
        analysis: Dict[str, Any],
        feedback_data: Dict[str, Any]
    ) -> None:
        """Update coach memory with analysis results."""
        # Update consistency streak
        worked_out = feedback_data.get('completion_percentage', 0) > 50
        self.coach_memory_service.update_consistency_streak(user_id, worked_out)
        
        # Store analysis
        self.coach_memory_service.set_memory(
            user_id,
            "last_analysis",
            analysis,
            "analysis"
        )
    
    def _calculate_progression(
        self,
        feedback_data: Dict[str, Any],
        workout_history: list[Dict[str, Any]],
        coach_memory: list[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate progression for next workout."""
        return self.progression_engine.calculate_progression(
            feedback_data,
            workout_history,
            coach_memory
        )
    
    def _get_workout_history(self) -> list[Dict[str, Any]]:
        """Get recent workout history."""
        return self.workout_repo.get_recent_workouts(limit=10)
    
    def _get_coach_memory(self, user_id: int) -> list[Dict[str, Any]]:
        """Get coach memory for the user."""
        return self.coach_memory_repo.get_by_user_id(user_id)
    
    def _check_personal_records(
        self,
        user_id: int,
        workout: Dict[str, Any],
        feedback_data: Dict[str, Any]
    ) -> None:
        """Check if any personal records were achieved."""
        # This would analyze the workout data to detect new PRs
        # For now, it's a placeholder
        pass
    
    def _check_achievements(
        self,
        user_id: int,
        feedback_data: Dict[str, Any],
        workout_history: list[Dict[str, Any]]
    ) -> None:
        """Check if any achievements were unlocked."""
        # Check for streak achievements
        streak = self.coach_memory_service.get_consistency_streak(user_id)
        
        if streak == 7:
            self._unlock_achievement(
                user_id,
                "First Week Streak",
                "Completed workouts for 7 consecutive days",
                "consistency",
                "🔥"
            )
        elif streak == 30:
            self._unlock_achievement(
                user_id,
                "Monthly Master",
                "Completed workouts for 30 consecutive days",
                "consistency",
                "💪"
            )
    
    def _unlock_achievement(
        self,
        user_id: int,
        title: str,
        description: str,
        category: str,
        icon: str
    ) -> None:
        """Unlock an achievement for the user."""
        existing = self.achievements_repo.get_by_title(user_id, title)
        if not existing:
            from datetime import datetime
            from zoneinfo import ZoneInfo
            self.achievements_repo.create({
                "user_id": user_id,
                "title": title,
                "description": description,
                "category": category,
                "achieved_date": datetime.now(ZoneInfo('Asia/Kolkata')).date(),
                "icon": icon
            })
            logger.info(f"Unlocked achievement: {title}")
