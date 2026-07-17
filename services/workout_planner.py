from datetime import datetime
from typing import Dict, Any
from enum import Enum

from config.logger import logger


class WorkoutDay(str, Enum):
    """Workout day types."""
    PUSH = "push"
    PULL = "pull"
    LEGS = "legs"
    CORE = "core"
    FULL_BODY = "full_body"
    SKILL_WORK = "skill_work"
    ACTIVE_RECOVERY = "active_recovery"


class WorkoutPlanner:
    """Determines the workout day based on the day of the week."""
    
    # Weekly split mapping
    WEEKLY_SPLIT = {
        0: WorkoutDay.PUSH,        # Monday
        1: WorkoutDay.PULL,        # Tuesday
        2: WorkoutDay.LEGS,        # Wednesday
        3: WorkoutDay.CORE,        # Thursday
        4: WorkoutDay.FULL_BODY,   # Friday
        5: WorkoutDay.SKILL_WORK,  # Saturday
        6: WorkoutDay.ACTIVE_RECOVERY  # Sunday
    }
    
    def __init__(self) -> None:
        logger.info("WorkoutPlanner initialized")
    
    def get_workout_day(self, date: datetime) -> WorkoutDay:
        """Get the workout day type for a given date."""
        weekday = date.weekday()
        workout_day = self.WEEKLY_SPLIT.get(weekday, WorkoutDay.FULL_BODY)
        logger.debug(f"Determined workout day: {workout_day} for date: {date}")
        return workout_day
    
    def get_workout_day_name(self, workout_day: WorkoutDay) -> str:
        """Get human-readable name for workout day."""
        names = {
            WorkoutDay.PUSH: "Push Day",
            WorkoutDay.PULL: "Pull Day",
            WorkoutDay.LEGS: "Legs Day",
            WorkoutDay.CORE: "Core Day",
            WorkoutDay.FULL_BODY: "Full Body Day",
            WorkoutDay.SKILL_WORK: "Skill Work Day",
            WorkoutDay.ACTIVE_RECOVERY: "Active Recovery Day"
        }
        return names.get(workout_day, "Workout Day")
    
    def get_focus_areas(self, workout_day: WorkoutDay) -> list[str]:
        """Get focus areas for a workout day."""
        focus_areas = {
            WorkoutDay.PUSH: ["chest", "shoulders", "triceps"],
            WorkoutDay.PULL: ["back", "biceps", "forearms"],
            WorkoutDay.LEGS: ["quads", "hamstrings", "glutes", "calves"],
            WorkoutDay.CORE: ["abs", "obliques", "lower back"],
            WorkoutDay.FULL_BODY: ["chest", "back", "legs", "shoulders", "arms"],
            WorkoutDay.SKILL_WORK: ["handstand", "planche", "front lever", "muscle-up"],
            WorkoutDay.ACTIVE_RECOVERY: ["mobility", "flexibility", "light cardio"]
        }
        return focus_areas.get(workout_day, [])
