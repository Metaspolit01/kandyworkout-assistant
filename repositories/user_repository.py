from typing import Optional, List, Dict, Any
from datetime import datetime

from clients.supabase_client import SupabaseClient
from config.logger import logger


class UserRepository:
    """Repository for user data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "users"
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get user by name."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"name": name},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting user by name: {e}", exc_info=True)
            raise
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"id": user_id},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}", exc_info=True)
            raise
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users."""
        try:
            return self.client.fetch(self.table)
        except Exception as e:
            logger.error(f"Error getting all users: {e}", exc_info=True)
            raise
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        try:
            results = self.client.insert(self.table, user_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating user: {e}", exc_info=True)
            raise
    
    def update(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data."""
        try:
            results = self.client.update(
                self.table,
                user_data,
                filters={"id": user_id}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating user: {e}", exc_info=True)
            raise
