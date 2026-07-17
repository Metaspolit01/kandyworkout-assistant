from typing import Optional, List, Dict, Any
from datetime import date

from clients.supabase_client import SupabaseClient
from config.logger import logger


class BodyMeasurementsRepository:
    """Repository for body measurements data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "body_measurements"
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all measurements for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id},
                order="date",
                ascending=False
            )
        except Exception as e:
            logger.error(f"Error getting measurements by user ID: {e}", exc_info=True)
            raise
    
    def get_by_date(self, user_id: int, measurement_date: date) -> Optional[Dict[str, Any]]:
        """Get measurement by user ID and date."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"user_id": user_id, "date": str(measurement_date)},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting measurement by date: {e}", exc_info=True)
            raise
    
    def get_latest(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get the latest measurement for a user."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"user_id": user_id},
                order="date",
                ascending=False,
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting latest measurement: {e}", exc_info=True)
            raise
    
    def create(self, measurement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new body measurement."""
        try:
            results = self.client.insert(self.table, measurement_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating measurement: {e}", exc_info=True)
            raise
    
    def update(self, user_id: int, measurement_date: date, measurement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update body measurement."""
        try:
            results = self.client.update(
                self.table,
                measurement_data,
                filters={"user_id": user_id, "date": str(measurement_date)}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating measurement: {e}", exc_info=True)
            raise
