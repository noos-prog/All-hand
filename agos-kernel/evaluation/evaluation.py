"""
AGOS Evaluation Engine
=====================

Mission evaluation and metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class EvaluationStatus(Enum):
    """Evaluation status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class EvaluationScore(Enum):
    """Evaluation score levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


@dataclass
class EvaluationCriteria:
    """Evaluation criteria."""
    name: str
    weight: float = 1.0
    threshold: float = 0.0
    description: str = ""


@dataclass
class EvaluationResult:
    """Evaluation result."""
    mission_id: str
    score: float
    score_level: EvaluationScore
    criteria_results: Dict[str, float] = field(default_factory=dict)
    passed: bool = True
    feedback: str = ""
    evaluated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class EvaluationEngine:
    """
    Evaluation Engine.
    
    Evaluates mission results and provides feedback.
    
    Usage:
        engine = EvaluationEngine()
        result = engine.evaluate(mission_id="123", output=data)
    """
    
    def __init__(self):
        """Initialize evaluation engine."""
        self._criteria: Dict[str, EvaluationCriteria] = {}
        self._history: List[EvaluationResult] = []
        self._register_default_criteria()
    
    def _register_default_criteria(self) -> None:
        """Register default evaluation criteria."""
        self._criteria = {
            "quality": EvaluationCriteria(name="quality", weight=1.0, description="Output quality"),
            "completeness": EvaluationCriteria(name="completeness", weight=1.0, description="Mission completeness"),
            "efficiency": EvaluationCriteria(name="efficiency", weight=0.8, description="Resource efficiency"),
            "correctness": EvaluationCriteria(name="correctness", weight=1.0, description="Output correctness"),
        }
    
    def add_criteria(self, criteria: EvaluationCriteria) -> None:
        """Add an evaluation criteria."""
        self._criteria[criteria.name] = criteria
    
    def evaluate(
        self,
        mission_id: str,
        output: Any,
        expected: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EvaluationResult:
        """Evaluate mission output."""
        criteria_results = {}
        total_weight = 0.0
        weighted_sum = 0.0
        
        # Evaluate each criteria
        for name, criteria in self._criteria.items():
            score = self._evaluate_criteria(name, output, expected)
            criteria_results[name] = score
            weighted_sum += score * criteria.weight
            total_weight += criteria.weight
        
        # Calculate overall score
        final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # Determine score level
        if final_score >= 0.9:
            score_level = EvaluationScore.EXCELLENT
        elif final_score >= 0.75:
            score_level = EvaluationScore.GOOD
        elif final_score >= 0.5:
            score_level = EvaluationScore.ACCEPTABLE
        elif final_score >= 0.25:
            score_level = EvaluationScore.NEEDS_IMPROVEMENT
        else:
            score_level = EvaluationScore.POOR
        
        result = EvaluationResult(
            mission_id=mission_id,
            score=final_score,
            score_level=score_level,
            criteria_results=criteria_results,
            passed=final_score >= 0.5,
            metadata=metadata or {},
        )
        
        self._history.append(result)
        return result
    
    def _evaluate_criteria(self, name: str, output: Any, expected: Any) -> float:
        """Evaluate a specific criteria."""
        if name == "quality":
            return self._evaluate_quality(output)
        elif name == "completeness":
            return self._evaluate_completeness(output)
        elif name == "efficiency":
            return self._evaluate_efficiency(output)
        elif name == "correctness":
            return self._evaluate_correctness(output, expected)
        return 0.5
    
    def _evaluate_quality(self, output: Any) -> float:
        """Evaluate output quality."""
        if output is None:
            return 0.0
        if isinstance(output, dict) and not output:
            return 0.3
        if isinstance(output, str) and len(output) < 10:
            return 0.4
        return 0.8
    
    def _evaluate_completeness(self, output: Any) -> float:
        """Evaluate completeness."""
        if output is None:
            return 0.0
        if isinstance(output, dict):
            return 0.7 if len(output) > 0 else 0.3
        if isinstance(output, list):
            return 0.7 if len(output) > 0 else 0.3
        return 0.6
    
    def _evaluate_efficiency(self, output: Any) -> float:
        """Evaluate efficiency."""
        return 0.8  # Default
    
    def _evaluate_correctness(self, output: Any, expected: Any) -> float:
        """Evaluate correctness."""
        if expected is None:
            return 0.7
        if output == expected:
            return 1.0
        if type(output) == type(expected):
            return 0.7
        return 0.3
    
    def get_history(self, limit: int = 100) -> List[EvaluationResult]:
        """Get evaluation history."""
        return self._history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get evaluation statistics."""
        if not self._history:
            return {"total_evaluations": 0}
        
        scores = [r.score for r in self._history]
        return {
            "total_evaluations": len(self._history),
            "average_score": sum(scores) / len(scores),
            "passed": sum(1 for r in self._history if r.passed),
            "failed": sum(1 for r in self._history if not r.passed),
            "by_level": {
                level.value: sum(1 for r in self._history if r.score_level == level)
                for level in EvaluationScore
            },
        }


# Global instance
_evaluation: Optional[EvaluationEngine] = None


def get_evaluation() -> EvaluationEngine:
    """Get the global evaluation engine."""
    global _evaluation
    if _evaluation is None:
        _evaluation = EvaluationEngine()
    return _evaluation
