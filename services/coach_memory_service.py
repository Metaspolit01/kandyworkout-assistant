from typing import Dict, Any, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from repositories.coach_memory_repository import CoachMemoryRepository
from config.logger import logger


class CoachMemoryService:
    """Manages coach memory for tracking long-term insights and patterns."""
    
    def __init__(self, coach_memory_repo: CoachMemoryRepository) -> None:
        self.repo = coach_memory_repo
        logger.info("CoachMemoryService initialized")
    
    def get_memory(self, user_id: int, key: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by key."""
        try:
            memory = self.repo.get_by_key(user_id, key)
            if memory:
                return memory.get("value")
            return None
        except Exception as e:
            logger.error(f"Error getting memory: {e}", exc_info=True)
            raise
    
    def set_memory(
        self,
        user_id: int,
        key: str,
        value: Dict[str, Any],
        memory_type: str = "general",
        confidence: float = 1.0
    ) -> Dict[str, Any]:
        """Set a memory value."""
        try:
            memory_data = {
                "memory_type": memory_type,
                "value": value,
                "confidence": confidence
            }
            return self.repo.upsert(user_id, key, memory_data)
        except Exception as e:
            logger.error(f"Error setting memory: {e}", exc_info=True)
            raise
    
    def get_all_memories(self, user_id: int) -> Dict[str, Any]:
        """Get all memories for a user as a dictionary."""
        try:
            memories = self.repo.get_by_user_id(user_id)
            return {m["key"]: m["value"] for m in memories}
        except Exception as e:
            logger.error(f"Error getting all memories: {e}", exc_info=True)
            raise
    
    def get_memories_by_type(self, user_id: int, memory_type: str) -> Dict[str, Any]:
        """Get memories of a specific type."""
        try:
            memories = self.repo.get_by_type(user_id, memory_type)
            return {m["key"]: m["value"] for m in memories}
        except Exception as e:
            logger.error(f"Error getting memories by type: {e}", exc_info=True)
            raise
    
    def update_progression_memory(
        self,
        user_id: int,
        exercise: str,
        current_level: str,
        next_level: str,
        ready_for_progression: bool
    ) -> Dict[str, Any]:
        """Update progression memory for an exercise."""
        try:
            key = f"progression_{exercise}"
            value = {
                "current_level": current_level,
                "next_level": next_level,
                "ready_for_progression": ready_for_progression,
                "last_updated": datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
            }
            return self.set_memory(user_id, key, value, "progression")
        except Exception as e:
            logger.error(f"Error updating progression memory: {e}", exc_info=True)
            raise
    
    def update_strength_memory(
        self,
        user_id: int,
        exercise: str,
        max_reps: int,
        trend: str
    ) -> Dict[str, Any]:
        """Update strength memory for an exercise."""
        try:
            key = f"strength_{exercise}"
            value = {
                "max_reps": max_reps,
                "trend": trend,
                "last_updated": datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
            }
            return self.set_memory(user_id, key, value, "strength")
        except Exception as e:
            logger.error(f"Error updating strength memory: {e}", exc_info=True)
            raise
    
    def update_injury_risk_memory(
        self,
        user_id: int,
        body_part: str,
        risk_level: str,
        notes: str
    ) -> Dict[str, Any]:
        """Update injury risk memory."""
        try:
            key = f"injury_risk_{body_part}"
            value = {
                "risk_level": risk_level,
                "notes": notes,
                "last_updated": datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
            }
            return self.set_memory(user_id, key, value, "injury_risk")
        except Exception as e:
            logger.error(f"Error updating injury risk memory: {e}", exc_info=True)
            raise
    
    def get_consistency_streak(self, user_id: int) -> int:
        """Calculate current workout consistency streak."""
        try:
            consistency_memory = self.get_memory(user_id, "consistency_streak")
            if consistency_memory:
                return consistency_memory.get("current_streak", 0)
            return 0
        except Exception as e:
            logger.error(f"Error getting consistency streak: {e}", exc_info=True)
            return 0
    
    def update_consistency_streak(
        self,
        user_id: int,
        worked_out_today: bool
    ) -> Dict[str, Any]:
        """Update consistency streak based on today's workout."""
        try:
            current_streak = self.get_consistency_streak(user_id)
            
            if worked_out_today:
                new_streak = current_streak + 1
            else:
                new_streak = 0
            
            value = {
                "current_streak": new_streak,
                "last_updated": datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()
            }
            
            return self.set_memory(user_id, "consistency_streak", value, "consistency")
        except Exception as e:
            logger.error(f"Error updating consistency streak: {e}", exc_info=True)
            raise
