from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Achievement(BaseModel):
    """Achievement model for tracking milestones."""
    
    id: Optional[int] = None
    user_id: int = Field(..., description="ID of the user")
    title: str = Field(..., description="Achievement title")
    description: str = Field(..., description="Achievement description")
    category: str = Field(..., description="Achievement category (e.g., 'strength', 'consistency', 'skill')")
    achieved_date: datetime = Field(..., description="Date when achievement was unlocked")
    icon: Optional[str] = Field(None, description="Emoji or icon for the achievement")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "First Week Streak",
                "description": "Completed workouts for 7 consecutive days",
                "category": "consistency",
                "achieved_date": "2024-01-21T00:00:00",
                "icon": "🔥"
            }
        }
