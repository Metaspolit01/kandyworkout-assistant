from typing import Optional, List, Dict, Any
from datetime import date

from clients.supabase_client import SupabaseClient
from config.logger import logger


class PersonalRecordsRepository:
    """Repository for personal records data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "personal_records"
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all personal records for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id},
                order="achieved_date",
                ascending=False
            )
        except Exception as e:
            logger.error(f"Error getting personal records by user ID: {e}", exc_info=True)
            raise
    
    def get_by_exercise(self, user_id: int, exercise_name: str) -> List[Dict[str, Any]]:
        """Get personal records for a specific exercise."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id, "exercise_name": exercise_name},
                order="achieved_date",
                ascending=False
            )
        except Exception as e:
            logger.error(f"Error getting personal records by exercise: {e}", exc_info=True)
            raise
    
    def get_best_record(self, user_id: int, exercise_name: str, record_type: str) -> Optional[Dict[str, Any]]:
        """Get the best record for a specific exercise and type."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"user_id": user_id, "exercise_name": exercise_name, "record_type": record_type},
                order="value",
                ascending=False,
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting best record: {e}", exc_info=True)
            raise
    
    def create(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new personal record."""
        try:
            results = self.client.insert(self.table, record_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating personal record: {e}", exc_info=True)
            raise
    
    def update(self, user_id: int, exercise_name: str, record_type: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update personal record."""
        try:
            results = self.client.update(
                self.table,
                record_data,
                filters={"user_id": user_id, "exercise_name": exercise_name, "record_type": record_type}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating personal record: {e}", exc_info=True)
            raise
