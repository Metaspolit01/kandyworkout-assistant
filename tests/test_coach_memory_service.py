import pytest
from unittest.mock import Mock

from services.coach_memory_service import CoachMemoryService


class TestCoachMemoryService:
    """Tests for CoachMemoryService."""
    
    @pytest.fixture
    def mock_repo(self):
        return Mock()
    
    @pytest.fixture
    def service(self, mock_repo):
        return CoachMemoryService(mock_repo)
    
    def test_get_memory(self, service, mock_repo):
        """Test getting a memory by key."""
        mock_repo.get_by_key.return_value = {"value": {"test": "data"}}
        
        result = service.get_memory(1, "test_key")
        
        assert result == {"test": "data"}
        mock_repo.get_by_key.assert_called_once_with(1, "test_key")
    
    def test_get_memory_not_found(self, service, mock_repo):
        """Test getting a memory that doesn't exist."""
        mock_repo.get_by_key.return_value = None
        
        result = service.get_memory(1, "nonexistent_key")
        
        assert result is None
    
    def test_set_memory(self, service, mock_repo):
        """Test setting a memory."""
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.set_memory(1, "test_key", {"value": "data"}, "general", 1.0)
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
    
    def test_get_all_memories(self, service, mock_repo):
        """Test getting all memories for a user."""
        mock_repo.get_by_user_id.return_value = [
            {"key": "key1", "value": {"data": 1}},
            {"key": "key2", "value": {"data": 2}}
        ]
        
        result = service.get_all_memories(1)
        
        assert result == {"key1": {"data": 1}, "key2": {"data": 2}}
        mock_repo.get_by_user_id.assert_called_once_with(1)
    
    def test_update_progression_memory(self, service, mock_repo):
        """Test updating progression memory."""
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.update_progression_memory(
            1,
            "pushups",
            "knee_pushups",
            "standard_pushups",
            True
        )
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
    
    def test_update_strength_memory(self, service, mock_repo):
        """Test updating strength memory."""
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.update_strength_memory(1, "pullups", 10, "improving")
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
    
    def test_update_injury_risk_memory(self, service, mock_repo):
        """Test updating injury risk memory."""
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.update_injury_risk_memory(1, "shoulder", "low", "No pain reported")
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
    
    def test_get_consistency_streak(self, service, mock_repo):
        """Test getting consistency streak."""
        mock_repo.get_by_key.return_value = {"value": {"current_streak": 5}}
        
        result = service.get_consistency_streak(1)
        
        assert result == 5
    
    def test_get_consistency_streak_no_memory(self, service, mock_repo):
        """Test getting consistency streak when no memory exists."""
        mock_repo.get_by_key.return_value = None
        
        result = service.get_consistency_streak(1)
        
        assert result == 0
    
    def test_update_consistency_streak_increment(self, service, mock_repo):
        """Test updating consistency streak when workout completed."""
        mock_repo.get_by_key.return_value = {"value": {"current_streak": 5}}
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.update_consistency_streak(1, True)
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
    
    def test_update_consistency_streak_reset(self, service, mock_repo):
        """Test updating consistency streak when workout not completed."""
        mock_repo.get_by_key.return_value = {"value": {"current_streak": 5}}
        mock_repo.upsert.return_value = {"id": 1}
        
        result = service.update_consistency_streak(1, False)
        
        assert result == {"id": 1}
        mock_repo.upsert.assert_called_once()
