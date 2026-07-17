from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CoachMemory(BaseModel):
    """Coach memory model for storing AI coach insights."""
    
    id: Optional[int] = None
    user_id: int = Field(..., description="ID of the user")
    memory_type: str = Field(..., description="Type of memory (e.g., 'progression', 'injury_risk', 'strength_trend')")
    key: str = Field(..., description="Memory key for lookup")
    value: Dict[str, Any] = Field(..., description="Memory value as JSON")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence score")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "memory_type": "progression",
                "key": "push_up_progression",
                "value": {"current_level": "knee_pushups", "next_level": "standard_pushups", "ready_for_progression": True},
                "confidence": 0.9
            }
        }
