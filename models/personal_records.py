from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class PersonalRecord(BaseModel):
    """Personal record model for tracking achievements."""
    
    id: Optional[int] = None
    user_id: int = Field(..., description="ID of the user")
    exercise_name: str = Field(..., description="Name of the exercise")
    record_type: str = Field(..., description="Type of record (e.g., 'max_reps', 'max_time', 'max_weight')")
    value: float = Field(..., description="Record value")
    unit: str = Field(..., description="Unit of measurement (e.g., 'reps', 'seconds', 'kg')")
    achieved_date: datetime = Field(..., description="Date when record was achieved")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "exercise_name": "push_ups",
                "record_type": "max_reps",
                "value": 25.0,
                "unit": "reps",
                "achieved_date": "2024-01-15T00:00:00",
                "notes": "First time hitting 25 reps"
            }
        }
