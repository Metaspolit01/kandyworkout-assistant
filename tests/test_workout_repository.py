import pytest
from unittest.mock import Mock
from datetime import datetime, date
from repositories.workout_repository import WorkoutRepository


class TestWorkoutRepository:
    """Tests for WorkoutRepository."""

    @pytest.fixture
    def mock_supabase_client(self):
        return Mock()

    @pytest.fixture
    def repository(self, mock_supabase_client):
        return WorkoutRepository(mock_supabase_client)

    def test_upsert_insert(self, repository, mock_supabase_client):
        """Test upserting when the workout does not exist yet (should insert)."""
        repository.get_by_date = Mock(return_value=None)
        repository.create = Mock(return_value={"id": 123, "date": "2026-07-19"})
        repository.update = Mock()

        workout_data = {"date": "2026-07-19T09:41:23", "day_type": "push", "greeting": "Let's go!"}
        result = repository.upsert(workout_data)

        assert workout_data["date"] == "2026-07-19"
        repository.get_by_date.assert_called_once_with(date(2026, 7, 19))
        repository.create.assert_called_once_with(workout_data)
        repository.update.assert_not_called()
        assert result == {"id": 123, "date": "2026-07-19"}

    def test_upsert_update(self, repository, mock_supabase_client):
        """Test upserting when the workout already exists (should update)."""
        existing_workout = {"id": 456, "date": "2026-07-19", "day_type": "push"}
        repository.get_by_date = Mock(return_value=existing_workout)
        repository.create = Mock()
        repository.update = Mock(return_value={"id": 456, "date": "2026-07-19", "day_type": "pull"})

        workout_data = {"date": date(2026, 7, 19), "day_type": "pull", "greeting": "Updated!"}
        result = repository.upsert(workout_data)

        assert workout_data["date"] == "2026-07-19"
        repository.get_by_date.assert_called_once_with(date(2026, 7, 19))
        repository.update.assert_called_once_with(456, workout_data)
        repository.create.assert_not_called()
        assert result == {"id": 456, "date": "2026-07-19", "day_type": "pull"}
