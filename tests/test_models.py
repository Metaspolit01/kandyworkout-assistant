import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import ValidationError

from models.user import User
from models.workout import Workout, WorkoutDay, Exercise, WorkoutSection
from models.workout_feedback import WorkoutFeedback, RPEScale, PainLevel, RecoveryQuality


class TestUser:
    """Tests for User model."""
    
    def test_valid_user(self):
        """Test creating a valid user."""
        user = User(
            name="Karthik",
            age=20,
            height_cm=163,
            weight_kg=58.0,
            level="beginner",
            goal="Become advanced"
        )
        assert user.name == "Karthik"
        assert user.age == 20
    
    def test_invalid_age(self):
        """Test user with invalid age."""
        with pytest.raises(ValidationError):
            User(
                name="Test",
                age=150,
                height_cm=170,
                weight_kg=70,
                level="beginner",
                goal="Test"
            )
    
    def test_invalid_level(self):
        """Test user with invalid level."""
        with pytest.raises(ValidationError):
            User(
                name="Test",
                age=20,
                height_cm=170,
                weight_kg=70,
                level="expert",
                goal="Test"
            )


class TestWorkout:
    """Tests for Workout model."""
    
    def test_valid_workout(self):
        """Test creating a valid workout."""
        workout = Workout(
            date=datetime.now(ZoneInfo('Asia/Kolkata')),
            day_type=WorkoutDay.PUSH,
            greeting="Let's go!",
            warmup=WorkoutSection(name="Warm-up", exercises=[]),
            main_workout=WorkoutSection(name="Main", exercises=[]),
            cooldown=WorkoutSection(name="Cooldown", exercises=[])
        )
        assert workout.day_type == WorkoutDay.PUSH
    
    def test_exercise(self):
        """Test creating an exercise."""
        exercise = Exercise(
            name="Push-ups",
            sets=3,
            reps="8-12",
            rest_seconds=60,
            technique_tips=["Keep core tight"]
        )
        assert exercise.name == "Push-ups"
        assert exercise.sets == 3


class TestWorkoutFeedback:
    """Tests for WorkoutFeedback model."""
    
    def test_valid_feedback(self):
        """Test creating valid feedback."""
        feedback = WorkoutFeedback(
            workout_id=1,
            completion_percentage=100.0,
            rpe=RPEScale.SEVEN,
            pain_level=PainLevel.MINIMAL,
            recovery_quality=RecoveryQuality.GOOD,
            sleep_hours=8.0
        )
        assert feedback.completion_percentage == 100.0
        assert feedback.rpe == 7
    
    def test_invalid_completion_percentage(self):
        """Test feedback with invalid completion percentage."""
        with pytest.raises(ValidationError):
            WorkoutFeedback(
                workout_id=1,
                completion_percentage=150.0,
                rpe=RPEScale.FIVE,
                pain_level=PainLevel.NONE,
                recovery_quality=RecoveryQuality.GOOD,
                sleep_hours=8.0
            )
    
    def test_invalid_rpe(self):
        """Test feedback with invalid RPE."""
        with pytest.raises(ValidationError):
            WorkoutFeedback(
                workout_id=1,
                completion_percentage=100.0,
                rpe=15,
                pain_level=PainLevel.NONE,
                recovery_quality=RecoveryQuality.GOOD,
                sleep_hours=8.0
            )
