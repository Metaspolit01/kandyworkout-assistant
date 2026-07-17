from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class WorkoutDay(str, Enum):
    """Workout day types."""
    PUSH = "push"
    PULL = "pull"
    LEGS = "legs"
    CORE = "core"
    FULL_BODY = "full_body"
    SKILL_WORK = "skill_work"
    ACTIVE_RECOVERY = "active_recovery"


class Exercise(BaseModel):
    """Exercise model."""
    
    name: str = Field(..., description="Exercise name")
    sets: int = Field(..., ge=1, le=10, description="Number of sets")
    reps: str = Field(..., description="Reps (e.g., '8-12', 'AMRAP')")
    rest_seconds: int = Field(..., ge=0, description="Rest time in seconds")
    technique_tips: List[str] = Field(default_factory=list, description="Technique tips")


class WorkoutSection(BaseModel):
    """Workout section (warm-up, main, cooldown)."""
    
    name: str = Field(..., description="Section name")
    exercises: List[Exercise] = Field(default_factory=list, description="Exercises in this section")


class Workout(BaseModel):
    """Workout model."""
    
    id: Optional[int] = None
    date: datetime = Field(..., description="Workout date")
    day_type: WorkoutDay = Field(..., description="Type of workout day")
    greeting: str = Field(..., description="Motivational greeting")
    warmup: WorkoutSection = Field(..., description="Warm-up section")
    main_workout: WorkoutSection = Field(..., description="Main workout section")
    cooldown: WorkoutSection = Field(..., description="Cooldown section")
    daily_habits: List[str] = Field(default_factory=list, description="Daily habits to follow")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "date": "2024-01-15T00:00:00",
                "day_type": "push",
                "greeting": "Let's crush some push exercises today!",
                "warmup": {"name": "Warm-up", "exercises": []},
                "main_workout": {"name": "Main Workout", "exercises": []},
                "cooldown": {"name": "Cooldown", "exercises": []},
                "daily_habits": ["Drink 3L water", "Sleep 8 hours"]
            }
        }
