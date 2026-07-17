from typing import Optional, List, Dict, Any

from clients.supabase_client import SupabaseClient
from config.logger import logger


class CoachMemoryRepository:
    """Repository for coach memory data operations."""
    
    def __init__(self, supabase_client: SupabaseClient) -> None:
        self.client = supabase_client
        self.table = "coach_memory"
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all memories for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id}
            )
        except Exception as e:
            logger.error(f"Error getting memories by user ID: {e}", exc_info=True)
            raise
    
    def get_by_key(self, user_id: int, key: str) -> Optional[Dict[str, Any]]:
        """Get memory by user ID and key."""
        try:
            results = self.client.fetch(
                self.table,
                filters={"user_id": user_id, "key": key},
                limit=1
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error getting memory by key: {e}", exc_info=True)
            raise
    
    def get_by_type(self, user_id: int, memory_type: str) -> List[Dict[str, Any]]:
        """Get memories by type for a user."""
        try:
            return self.client.fetch(
                self.table,
                filters={"user_id": user_id, "memory_type": memory_type}
            )
        except Exception as e:
            logger.error(f"Error getting memories by type: {e}", exc_info=True)
            raise
    
    def create(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new coach memory."""
        try:
            results = self.client.insert(self.table, memory_data)
            return results[0]
        except Exception as e:
            logger.error(f"Error creating memory: {e}", exc_info=True)
            raise
    
    def update(self, user_id: int, key: str, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update coach memory."""
        try:
            results = self.client.update(
                self.table,
                memory_data,
                filters={"user_id": user_id, "key": key}
            )
            return results[0]
        except Exception as e:
            logger.error(f"Error updating memory: {e}", exc_info=True)
            raise
    
    def upsert(self, user_id: int, key: str, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert or update a memory."""
        try:
            existing = self.get_by_key(user_id, key)
            if existing:
                return self.update(user_id, key, memory_data)
            else:
                memory_data["user_id"] = user_id
                memory_data["key"] = key
                return self.create(memory_data)
        except Exception as e:
            logger.error(f"Error upserting memory: {e}", exc_info=True)
            raise
