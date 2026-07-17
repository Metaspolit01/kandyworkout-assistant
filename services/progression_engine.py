from typing import Dict, Any, Literal
from enum import Enum

from config.logger import logger


class ProgressionDecision(str, Enum):
    """Progression decision types."""
    PROGRESS = "progress"
    MAINTAIN = "maintain"
    DELOAD = "deload"


class ProgressionEngine:
    """Determines workout progression based on feedback and history."""
    
    def __init__(self) -> None:
        logger.info("ProgressionEngine initialized")
    
    def calculate_progression(
        self,
        feedback_data: Dict[str, Any],
        recent_performance: list[Dict[str, Any]],
        coach_memory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate progression decision for next workout."""
        try:
            decision = self._make_progression_decision(
                feedback_data,
                recent_performance,
                coach_memory
            )
            
            adjustments = self._calculate_adjustments(
                decision,
                feedback_data,
                recent_performance
            )
            
            result = {
                "decision": decision.value,
                "reasoning": self._generate_reasoning(decision, feedback_data),
                "adjustments": adjustments,
                "confidence": self._calculate_confidence(feedback_data, recent_performance)
            }
            
            logger.info(f"Progression decision: {decision.value}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating progression: {e}", exc_info=True)
            raise
    
    def _make_progression_decision(
        self,
        feedback_data: Dict[str, Any],
        recent_performance: list[Dict[str, Any]],
        coach_memory: Dict[str, Any]
    ) -> ProgressionDecision:
        """Make the core progression decision."""
        # Check for pain - always deload if pain is present
        pain_level = feedback_data.get("pain_level", 0)
        if pain_level >= 3:
            return ProgressionDecision.DELOAD
        
        # Check recovery quality
        recovery_quality = feedback_data.get("recovery_quality", "good")
        if recovery_quality == "poor":
            return ProgressionDecision.DELOAD
        
        # Check RPE - if too high, maintain or deload
        rpe = feedback_data.get("rpe", 5)
        if rpe >= 9:
            return ProgressionDecision.DELOAD
        elif rpe >= 7:
            return ProgressionDecision.MAINTAIN
        
        # Check completion percentage
        completion = feedback_data.get("completion_percentage", 0)
        if completion < 80:
            return ProgressionDecision.MAINTAIN
        
        # Check sleep - poor sleep affects recovery
        sleep_hours = feedback_data.get("sleep_hours", 8)
        if sleep_hours < 6:
            return ProgressionDecision.MAINTAIN
        
        # Check recent performance trend
        if recent_performance:
            avg_completion = sum(
                w.get("completion_percentage", 0) 
                for w in recent_performance[-3:]
            ) / min(len(recent_performance), 3)
            
            if avg_completion >= 90 and rpe <= 7:
                return ProgressionDecision.PROGRESS
        
        # Default to maintain if conditions are good but not great
        return ProgressionDecision.MAINTAIN
    
    def _calculate_adjustments(
        self,
        decision: ProgressionDecision,
        feedback_data: Dict[str, Any],
        recent_performance: list[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate specific workout adjustments."""
        adjustments = {
            "intensity": "maintain",
            "volume": "maintain",
            "rest_time": "maintain",
            "exercise_progression": []
        }
        
        if decision == ProgressionDecision.PROGRESS:
            adjustments["intensity"] = "increase"
            adjustments["volume"] = "increase"
            adjustments["rest_time"] = "maintain"
            adjustments["exercise_progression"] = self._suggest_progressions(recent_performance)
        
        elif decision == ProgressionDecision.MAINTAIN:
            adjustments["intensity"] = "maintain"
            adjustments["volume"] = "maintain"
            adjustments["rest_time"] = "maintain"
        
        elif decision == ProgressionDecision.DELOAD:
            adjustments["intensity"] = "decrease"
            adjustments["volume"] = "decrease"
            adjustments["rest_time"] = "increase"
            adjustments["exercise_progression"] = self._suggest_regressions(recent_performance)
        
        return adjustments
    
    def _suggest_progressions(self, recent_performance: list[Dict[str, Any]]) -> list[str]:
        """Suggest exercise progressions."""
        progressions = []
        
        # Common progressions for calisthenics
        progressions.extend([
            "Increase reps by 1-2 per set",
            "Decrease rest time by 10-15 seconds",
            "Add 1 set to main exercises",
            "Progress to harder exercise variation"
        ])
        
        return progressions[:3]  # Return top 3
    
    def _suggest_regressions(self, recent_performance: list[Dict[str, Any]]) -> list[str]:
        """Suggest exercise regressions for deload."""
        regressions = []
        
        regressions.extend([
            "Decrease reps by 20-30%",
            "Increase rest time by 30 seconds",
            "Reduce sets by 1",
            "Use easier exercise variation"
        ])
        
        return regressions[:3]
    
    def _generate_reasoning(self, decision: ProgressionDecision, feedback_data: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for the decision."""
        if decision == ProgressionDecision.PROGRESS:
            return "Great workout! High completion and good recovery indicate readiness for progression."
        
        elif decision == ProgressionDecision.MAINTAIN:
            return "Good workout, but let's maintain current intensity to ensure consistent progress."
        
        elif decision == ProgressionDecision.DELOAD:
            pain = feedback_data.get("pain_level", 0)
            recovery = feedback_data.get("recovery_quality", "good")
            return f"Deload recommended due to {'pain' if pain > 0 else 'poor recovery'}. Prioritize recovery."
        
        return "Maintain current intensity."
    
    def _calculate_confidence(
        self,
        feedback_data: Dict[str, Any],
        recent_performance: list[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score for the progression decision."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence if we have good data
        if feedback_data.get("completion_percentage"):
            confidence += 0.1
        
        if feedback_data.get("rpe"):
            confidence += 0.1
        
        if feedback_data.get("recovery_quality"):
            confidence += 0.1
        
        if recent_performance and len(recent_performance) >= 3:
            confidence += 0.2
        
        return min(confidence, 1.0)
