from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class RPEScale(int, Enum):
    """Rate of Perceived Exertion scale (1-10)."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


class PainLevel(int, Enum):
    """Pain level scale (0-10)."""
    NONE = 0
    MINIMAL = 1
    MILD = 2
    MODERATE = 3
    SEVERE = 4
    EXTREME = 5


class RecoveryQuality(str, Enum):
    """Recovery quality levels."""
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


class WorkoutFeedback(BaseModel):
    """Workout feedback model."""
    
    id: Optional[int] = None
    workout_id: int = Field(..., description="ID of the workout")
    completion_percentage: float = Field(..., ge=0, le=100, description="Percentage of workout completed")
    rpe: RPEScale = Field(..., description="Rate of Perceived Exertion (1-10)")
    pain_level: PainLevel = Field(..., description="Pain level (0-5)")
    recovery_quality: RecoveryQuality = Field(..., description="Quality of recovery")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "workout_id": 1,
                "completion_percentage": 100.0,
                "rpe": 7,
                "pain_level": 1,
                "recovery_quality": "good",
                "sleep_hours": 8.0,
                "notes": "Felt strong on push-ups"
            }
        }
