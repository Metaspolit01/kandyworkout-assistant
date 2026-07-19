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
    
    def upsert(self, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upsert workout data (insert or update based on date)."""
        try:
            workout_date = workout_data.get("date")
            if not workout_date:
                logger.warning("No date found in workout_data; falling back to create")
                return self.create(workout_data)
            
            # Format the date properly for comparison and database format
            if isinstance(workout_date, (datetime, date)):
                workout_date_obj = workout_date
                if isinstance(workout_date, datetime):
                    workout_date_obj = workout_date.date()
                date_str = workout_date_obj.strftime("%Y-%m-%d")
            else:
                # Assuming it's a string, format or parse it
                # If it's in ISO format (e.g. 2026-07-19T09:41:23) we take the date part
                date_str = str(workout_date).split('T')[0]
                workout_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Ensure workout_data has the clean YYYY-MM-DD string format
            workout_data["date"] = date_str
            
            existing = self.get_by_date(workout_date_obj)
            if existing:
                logger.info(f"Workout already exists for {date_str}. Updating existing workout (ID: {existing['id']})")
                return self.update(existing["id"], workout_data)
            else:
                logger.info(f"Creating new workout for {date_str}")
                return self.create(workout_data)
        except Exception as e:
            logger.error(f"Error upserting workout: {e}", exc_info=True)
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
