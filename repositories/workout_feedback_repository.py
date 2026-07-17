from typing import Optional, List, Dict, Any

from clients.supabase_client import SupabaseClient
from config.logger import logger


class WorkoutFeedbackRepository:
    """Repository for workout feedback data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "workout_feedback"
    
    def get_by_workout_id(self, workout_id: int) -> Optional[Dict[str, Any]]:
        """Get feedback by workout ID."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"workout_id": workout_id},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting feedback by workout ID: {e}", exc_info=True)
            raise
    
    def get_recent_feedback(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent feedback ordered by creation date."""
        try:
            return self.client.fetch(
                self.table,
                order="created_at",
                ascending=False,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error getting recent feedback: {e}", exc_info=True)
            raise
    
    def create(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new workout feedback."""
        try:
            results = self.client.insert(self.table, feedback_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating feedback: {e}", exc_info=True)
            raise
    
    def update(self, workout_id: int, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update workout feedback."""
        try:
            results = self.client.update(
                self.table,
                feedback_data,
                filters={"workout_id": workout_id}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating feedback: {e}", exc_info=True)
            raise
