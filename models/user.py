from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    """User profile model."""
    
    id: Optional[int] = None
    name: str = Field(..., description="User's name")
    age: int = Field(..., ge=1, le=120, description="User's age in years")
    height_cm: int = Field(..., ge=50, le=250, description="User's height in centimeters")
    weight_kg: float = Field(..., ge=20, le=300, description="User's weight in kilograms")
    level: str = Field(..., description="Fitness level: beginner, intermediate, advanced")
    goal: str = Field(..., description="User's fitness goal")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Karthik",
                "age": 20,
                "height_cm": 163,
                "weight_kg": 58.0,
                "level": "beginner",
                "goal": "Become an advanced calisthenics athlete"
            }
        }
