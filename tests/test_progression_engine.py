import pytest

from services.progression_engine import ProgressionEngine, ProgressionDecision


class TestProgressionEngine:
    """Tests for ProgressionEngine."""
    
    @pytest.fixture
    def engine(self):
        return ProgressionEngine()
    
    def test_progress_decision_high_completion_low_rpe(self, engine):
        """Test progress decision with high completion and low RPE."""
        feedback = {
            "completion_percentage": 95,
            "rpe": 6,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 8
        }
        recent_performance = [
            {"completion_percentage": 90},
            {"completion_percentage": 92},
            {"completion_percentage": 95}
        ]
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.PROGRESS.value
    
    def test_maintain_decision_moderate_completion(self, engine):
        """Test maintain decision with moderate completion."""
        feedback = {
            "completion_percentage": 85,
            "rpe": 7,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 7
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.MAINTAIN.value
    
    def test_deload_decision_high_pain(self, engine):
        """Test deload decision with high pain level."""
        feedback = {
            "completion_percentage": 100,
            "rpe": 5,
            "pain_level": 4,
            "recovery_quality": "good",
            "sleep_hours": 8
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.DELOAD.value
    
    def test_deload_decision_poor_recovery(self, engine):
        """Test deload decision with poor recovery."""
        feedback = {
            "completion_percentage": 100,
            "rpe": 6,
            "pain_level": 0,
            "recovery_quality": "poor",
            "sleep_hours": 8
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.DELOAD.value
    
    def test_deload_decision_high_rpe(self, engine):
        """Test deload decision with high RPE."""
        feedback = {
            "completion_percentage": 100,
            "rpe": 9,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 8
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.DELOAD.value
    
    def test_maintain_decision_low_sleep(self, engine):
        """Test maintain decision with low sleep."""
        feedback = {
            "completion_percentage": 95,
            "rpe": 6,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 5
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["decision"] == ProgressionDecision.MAINTAIN.value
    
    def test_adjustments_for_progress(self, engine):
        """Test adjustments for progress decision."""
        feedback = {
            "completion_percentage": 95,
            "rpe": 6,
            "pain_level": 0,
            "recovery_quality": "good",
            "sleep_hours": 8
        }
        recent_performance = [
            {"completion_percentage": 90},
            {"completion_percentage": 92},
            {"completion_percentage": 95}
        ]
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["adjustments"]["intensity"] == "increase"
        assert result["adjustments"]["volume"] == "increase"
    
    def test_adjustments_for_deload(self, engine):
        """Test adjustments for deload decision."""
        feedback = {
            "completion_percentage": 100,
            "rpe": 5,
            "pain_level": 4,
            "recovery_quality": "good",
            "sleep_hours": 8
        }
        recent_performance = []
        coach_memory = {}
        
        result = engine.calculate_progression(feedback, recent_performance, coach_memory)
        assert result["adjustments"]["intensity"] == "decrease"
        assert result["adjustments"]["volume"] == "decrease"
        assert result["adjustments"]["rest_time"] == "increase"
