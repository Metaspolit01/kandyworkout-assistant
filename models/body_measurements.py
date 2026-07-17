from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BodyMeasurements(BaseModel):
    """Body measurements model for tracking physical changes."""
    
    id: Optional[int] = None
    user_id: int = Field(..., description="ID of the user")
    date: datetime = Field(..., description="Measurement date")
    weight_kg: float = Field(..., ge=20, le=300, description="Weight in kilograms")
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100, description="Body fat percentage")
    chest_cm: Optional[float] = Field(None, ge=0, description="Chest circumference in cm")
    waist_cm: Optional[float] = Field(None, ge=0, description="Waist circumference in cm")
    arms_cm: Optional[float] = Field(None, ge=0, description="Arm circumference in cm")
    thighs_cm: Optional[float] = Field(None, ge=0, description="Thigh circumference in cm")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "date": "2024-01-15T00:00:00",
                "weight_kg": 58.0,
                "body_fat_percentage": 15.0,
                "chest_cm": 90.0,
                "waist_cm": 75.0,
                "arms_cm": 30.0,
                "thighs_cm": 50.0
            }
        }
