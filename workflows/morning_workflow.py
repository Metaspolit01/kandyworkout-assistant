from datetime import datetime
from typing import Dict, Any

from clients.gemini_client import GeminiClient
from clients.supabase_client import SupabaseClient
from clients.notion_client import NotionClientWrapper
from repositories.user_repository import UserRepository
from repositories.workout_repository import WorkoutRepository
from repositories.coach_memory_repository import CoachMemoryRepository
from services.workout_planner import WorkoutPlanner
from services.workout_generator import WorkoutGenerator
from services.coach_memory_service import CoachMemoryService
from config.logger import logger


class MorningWorkflow:
    """Morning workflow: generates and creates daily workout."""
    
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
        self.coach_memory_repo = CoachMemoryRepository(supabase_client)
        
        # Initialize services
        self.workout_planner = WorkoutPlanner()
        self.workout_generator = WorkoutGenerator(self.gemini_client, self.workout_planner)
        self.coach_memory_service = CoachMemoryService(self.coach_memory_repo)
        
        logger.info("MorningWorkflow initialized")
    
    def execute(self, date: datetime = None) -> Dict[str, Any]:
        """Execute the morning workflow."""
        if date is None:
            date = datetime.now()
        
        logger.info(f"Starting morning workflow for {date}")
        
        try:
            # Step 1: Get user profile
            user_profile = self._get_user_profile()
            logger.info(f"User profile loaded: {user_profile['name']}")
            
            # Step 2: Get workout history
            workout_history = self._get_workout_history()
            logger.info(f"Loaded {len(workout_history)} previous workouts")
            
            # Step 3: Get coach memory
            coach_memory = self._get_coach_memory(user_profile['id'])
            logger.info(f"Loaded {len(coach_memory)} coach memories")
            
            # Step 4: Generate today's workout
            workout_data = self._generate_workout(
                user_profile,
                workout_history,
                coach_memory,
                date
            )
            logger.info(f"Generated {workout_data['day_type']} workout")
            
            # Step 5: Save workout to Supabase
            saved_workout = self._save_workout(workout_data)
            logger.info(f"Saved workout to Supabase (ID: {saved_workout['id']})")
            
            # Step 6: Create Notion page
            notion_page = self._create_notion_page(saved_workout, workout_data, date)
            logger.info(f"Created Notion page: {notion_page['url']}")
            
            # Step 7: Update workout with Notion page ID
            self._update_workout_notion_id(saved_workout['id'], notion_page['id'])
            
            result = {
                "success": True,
                "workout_id": saved_workout['id'],
                "workout_type": workout_data['day_type'],
                "notion_page_id": notion_page['id'],
                "notion_url": notion_page['url'],
                "date": date.isoformat()
            }
            
            logger.info("Morning workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Morning workflow failed: {e}", exc_info=True)
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
    
    def _get_workout_history(self) -> list[Dict[str, Any]]:
        """Get recent workout history."""
        return self.workout_repo.get_recent_workouts(limit=10)
    
    def _get_coach_memory(self, user_id: int) -> list[Dict[str, Any]]:
        """Get coach memory for the user."""
        return self.coach_memory_repo.get_by_user_id(user_id)
    
    def _generate_workout(
        self,
        user_profile: Dict[str, Any],
        workout_history: list[Dict[str, Any]],
        coach_memory: list[Dict[str, Any]],
        date: datetime
    ) -> Dict[str, Any]:
        """Generate workout using AI."""
        return self.workout_generator.generate_workout(
            user_profile,
            workout_history,
            coach_memory,
            date
        )
    
    def _save_workout(self, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save workout to Supabase."""
        return self.workout_repo.create(workout_data)
    
    def _create_notion_page(
        self,
        saved_workout: Dict[str, Any],
        workout_data: Dict[str, Any],
        date: datetime
    ) -> Dict[str, Any]:
        """Create Notion page for the workout."""
        title = f"Workout - {date.strftime('%Y-%m-%d')} ({workout_data['day_type'].replace('_', ' ').title()})"
        date_str = date.strftime('%Y-%m-%d')
        
        return self.notion_client.create_workout_page(
            title=title,
            workout_data=workout_data,
            date=date_str
        )
    
    def _update_workout_notion_id(self, workout_id: int, notion_page_id: str) -> None:
        """Update workout with Notion page ID."""
        self.workout_repo.update_notion_page_id(workout_id, notion_page_id)
