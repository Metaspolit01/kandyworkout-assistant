import pytest
from datetime import datetime

from services.workout_planner import WorkoutPlanner, WorkoutDay


class TestWorkoutPlanner:
    """Tests for WorkoutPlanner."""
    
    @pytest.fixture
    def planner(self):
        return WorkoutPlanner()
    
    def test_get_workout_day_monday(self, planner):
        """Test Monday returns Push day."""
        date = datetime(2024, 1, 15)  # Monday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.PUSH
    
    def test_get_workout_day_tuesday(self, planner):
        """Test Tuesday returns Pull day."""
        date = datetime(2024, 1, 16)  # Tuesday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.PULL
    
    def test_get_workout_day_wednesday(self, planner):
        """Test Wednesday returns Legs day."""
        date = datetime(2024, 1, 17)  # Wednesday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.LEGS
    
    def test_get_workout_day_thursday(self, planner):
        """Test Thursday returns Core day."""
        date = datetime(2024, 1, 18)  # Thursday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.CORE
    
    def test_get_workout_day_friday(self, planner):
        """Test Friday returns Full Body day."""
        date = datetime(2024, 1, 19)  # Friday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.FULL_BODY
    
    def test_get_workout_day_saturday(self, planner):
        """Test Saturday returns Skill Work day."""
        date = datetime(2024, 1, 20)  # Saturday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.SKILL_WORK
    
    def test_get_workout_day_sunday(self, planner):
        """Test Sunday returns Active Recovery day."""
        date = datetime(2024, 1, 21)  # Sunday
        result = planner.get_workout_day(date)
        assert result == WorkoutDay.ACTIVE_RECOVERY
    
    def test_get_workout_day_name(self, planner):
        """Test getting human-readable workout day name."""
        assert planner.get_workout_day_name(WorkoutDay.PUSH) == "Push Day"
        assert planner.get_workout_day_name(WorkoutDay.PULL) == "Pull Day"
        assert planner.get_workout_day_name(WorkoutDay.LEGS) == "Legs Day"
    
    def test_get_focus_areas_push(self, planner):
        """Test focus areas for Push day."""
        areas = planner.get_focus_areas(WorkoutDay.PUSH)
        assert "chest" in areas
        assert "shoulders" in areas
        assert "triceps" in areas
    
    def test_get_focus_areas_pull(self, planner):
        """Test focus areas for Pull day."""
        areas = planner.get_focus_areas(WorkoutDay.PULL)
        assert "back" in areas
        assert "biceps" in areas
        assert "forearms" in areas
    
    def test_get_focus_areas_legs(self, planner):
        """Test focus areas for Legs day."""
        areas = planner.get_focus_areas(WorkoutDay.LEGS)
        assert "quads" in areas
        assert "hamstrings" in areas
        assert "glutes" in areas
