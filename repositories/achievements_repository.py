from typing import Optional, List, Dict, Any
from datetime import date

from clients.supabase_client import SupabaseClient
from config.logger import logger


class AchievementsRepository:
    """Repository for achievements data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "achievements"
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all achievements for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id},
                order="achieved_date",
                ascending=False
            )
        except Exception as e:
            logger.error(f"Error getting achievements by user ID: {e}", exc_info=True)
            raise
    
    def get_by_category(self, user_id: int, category: str) -> List[Dict[str, Any]]:
        """Get achievements by category for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id, "category": category},
                order="achieved_date",
                ascending=False
            )
        except Exception as e:
            logger.error(f"Error getting achievements by category: {e}", exc_info=True)
            raise
    
    def get_by_title(self, user_id: int, title: str) -> Optional[Dict[str, Any]]:
        """Get achievement by user ID and title."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"user_id": user_id, "title": title},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting achievement by title: {e}", exc_info=True)
            raise
    
    def create(self, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new achievement."""
        try:
            results = self.client.insert(self.table, achievement_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating achievement: {e}", exc_info=True)
            raise
    
    def update(self, user_id: int, title: str, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update achievement."""
        try:
            results = self.client.update(
                self.table,
                achievement_data,
                filters={"user_id": user_id, "title": title}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating achievement: {e}", exc_info=True)
            raise
