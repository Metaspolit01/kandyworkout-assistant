from typing import Optional, List, Dict, Any
from datetime import datetime, date

from clients.supabase_client import SupabaseClient
from config.logger import logger


class WorkoutRepository:
    """Repository for workout data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "workouts"
    
    def get_by_date(self, workout_date: date) -> Optional[Dict[str, Any]]:
        """Get workout by date."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"date": str(workout_date)},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting workout by date: {e}", exc_info=True)
            raise
    
    def get_by_id(self, workout_id: int) -> Optional[Dict[str, Any]]:
        """Get workout by ID."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"id": workout_id},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting workout by ID: {e}", exc_info=True)
            raise
    
    def get_recent_workouts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workouts ordered by date."""
        try:
            return self.client.fetch(
                self.table,
                order="date",
                ascending=False,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error getting recent workouts: {e}", exc_info=True)
            raise
    
    def get_by_day_type(self, day_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get workouts by day type."""
        try:
            return self.client.fetch(
                self.table,
                filters={"day_type": day_type},
                order="date",
                ascending=False,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Error getting workouts by day type: {e}", exc_info=True)
            raise
    
    def get_date_range(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get workouts within a date range."""
        try:
            # Supabase doesn't support range filters directly, so we fetch all and filter
            all_workouts = self.client.fetch(self.table, order="date", ascending=True)
            return [
                w for w in all_workouts
                if start_date <= datetime.strptime(w["date"], "%Y-%m-%d").date() <= end_date
            ]
        except Exception as e:
            logger.error(f"Error getting workouts by date range: {e}", exc_info=True)
            raise
    
    def create(self, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workout."""
        try:
            results = self.client.insert(self.table, workout_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating workout: {e}", exc_info=True)
            raise
    
    def update(self, workout_id: int, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update workout data."""
        try:
            results = self.client.update(
                self.table,
                workout_data,
                filters={"id": workout_id}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating workout: {e}", exc_info=True)
            raise
    
    def update_notion_page_id(self, workout_id: int, notion_page_id: str) -> Dict[str, Any]:
        """Update the Notion page ID for a workout."""
        try:
            return self.update(workout_id, {"notion_page_id": notion_page_id})
        except Exception as e:
            logger.error(f"Error updating Notion page ID: {e}", exc_info=True)
            raise
