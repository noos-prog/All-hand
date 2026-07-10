#!/usr/bin/env python3
"""
ARI - Judge Engine
================

Judges evaluation outputs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class JudgementType(Enum):
    """Types of judgement."""
    EXACT_MATCH = "exact_match"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    CODE_QUALITY = "code_quality"
    TEST_COVERAGE = "test_coverage"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class JudgementCriteria:
    """Criteria for judgement."""
    criteria_id: str
    name: str
    description: str
    
    # Scoring
    weight: float = 1.0
    max_score: float = 100.0
    
    # Thresholds
    pass_threshold: float = 70.0
    fail_threshold: float = 30.0
    
    # Configuration
    judging_func: Optional[Callable] = None


@dataclass
class Judgement:
    """A judgement result."""
    judgement_id: str
    result_id: str
    
    # Overall result
    passed: bool
    overall_score: float
    
    # Individual criteria scores
    criteria_scores: Tuple[Dict[str, Any], ...]
    
    # Details
    passed_criteria: int = 0
    failed_criteria: int = 0
    
    # Metadata
    judged_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    judge_name: str = "default"


@dataclass
class JudgeConfig:
    """Configuration for a judge."""
    config_id: str
    name: str
    
    # Criteria
    criteria: Tuple[JudgementCriteria, ...]
    
    # Thresholds
    overall_pass_threshold: float = 70.0
    
    # Mode
    strict_mode: bool = False
    allow_partial: bool = True
    
    # Metadata
    version: str = "1.0"


@dataclass
class JudgeResult:
    """Result of judging."""
    result_id: str
    config_id: str
    
    # Status
    status: str  # success, error
    passed: bool
    
    # Score
    overall_score: float
    max_score: float = 100.0
    
    # Breakdown
    criteria_breakdown: Dict[str, float] = field(default_factory=dict)
    
    # Details
    feedback: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    # Metadata
    judged_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    duration_ms: int = 0


class JudgeEngine:
    """
    Engine for judging evaluation outputs.
    """
    
    def __init__(self):
        self._configs: Dict[str, JudgeConfig] = {}
        self._judges: Dict[str, Callable] = {}
        self._default_config: Optional[JudgeConfig] = None
        
        # Register default judge
        self._register_default_judge()
    
    def _register_default_judge(self) -> None:
        """Register the default judge."""
        def default_judge(task: Any, result: Any) -> Dict[str, Any]:
            # Simple default judge
            return {
                "score": 80.0,
                "passed": True,
                "feedback": ["Default judgement applied"],
            }
        
        self._judges["default"] = default_judge
    
    def register_judge(
        self,
        name: str,
        judge: Callable[[Any, Any], Dict]
    ) -> None:
        """Register a judge function."""
        self._judges[name] = judge
    
    def create_config(
        self,
        name: str,
        criteria: List[Dict[str, Any]]
    ) -> JudgeConfig:
        """Create a judgement configuration."""
        config_id = f"config_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        judgement_criteria = [
            JudgementCriteria(
                criteria_id=f"crit_{i}",
                name=c.get("name", f"Criteria {i}"),
                description=c.get("description", ""),
                weight=c.get("weight", 1.0),
                max_score=c.get("max_score", 100.0),
                pass_threshold=c.get("pass_threshold", 70.0),
            )
            for i, c in enumerate(criteria)
        ]
        
        config = JudgeConfig(
            config_id=config_id,
            name=name,
            criteria=tuple(judgement_criteria),
        )
        
        self._configs[config_id] = config
        
        if self._default_config is None:
            self._default_config = config
        
        return config
    
    def judge(
        self,
        task: Any,
        result: Any,
        config_id: str = None,
        judge_name: str = "default"
    ) -> JudgeResult:
        """Judge an evaluation result."""
        result_id = result.result_id if hasattr(result, 'result_id') else str(id(result))
        
        config = None
        if config_id and config_id in self._configs:
            config = self._configs[config_id]
        else:
            config = self._default_config
        
        start_time = datetime.utcnow()
        
        if judge_name not in self._judges:
            return JudgeResult(
                result_id=result_id,
                config_id=config_id or "default",
                status="error",
                passed=False,
                overall_score=0.0,
                errors=[f"Unknown judge: {judge_name}"],
            )
        
        judge_func = self._judges[judge_name]
        
        try:
            judge_output = judge_func(task, result)
            
            # Calculate overall score
            overall_score = judge_output.get("score", 0)
            passed = judge_output.get("passed", overall_score >= 70)
            
            return JudgeResult(
                result_id=result_id,
                config_id=config_id or "default",
                status="success",
                passed=passed,
                overall_score=overall_score,
                feedback=judge_output.get("feedback", []),
                warnings=judge_output.get("warnings", []),
                duration_ms=int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                ),
            )
            
        except Exception as e:
            return JudgeResult(
                result_id=result_id,
                config_id=config_id or "default",
                status="error",
                passed=False,
                overall_score=0.0,
                errors=[str(e)],
                duration_ms=int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                ),
            )
    
    def judge_with_criteria(
        self,
        task: Any,
        result: Any,
        criteria: List[JudgementCriteria]
    ) -> Judgement:
        """Judge using specific criteria."""
        judgement_id = f"judge_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        result_id = result.result_id if hasattr(result, 'result_id') else str(id(result))
        
        criteria_scores = []
        total_weighted_score = 0.0
        total_weight = 0.0
        passed_count = 0
        failed_count = 0
        
        for criterion in criteria:
            # Run judgement function if provided
            if criterion.judging_func:
                score = criterion.judging_func(task, result)
            else:
                # Default scoring
                score = criterion.max_score * 0.8
            
            passed = score >= criterion.pass_threshold
            
            if passed:
                passed_count += 1
            else:
                failed_count += 1
            
            criteria_scores.append({
                "criteria_id": criterion.criteria_id,
                "name": criterion.name,
                "score": score,
                "max_score": criterion.max_score,
                "passed": passed,
                "weight": criterion.weight,
            })
            
            total_weighted_score += score * criterion.weight
            total_weight += criterion.weight
        
        overall_score = (
            total_weighted_score / total_weight
            if total_weight > 0 else 0
        )
        
        return Judgement(
            judgement_id=judgement_id,
            result_id=result_id,
            passed=failed_count == 0,
            overall_score=overall_score,
            criteria_scores=tuple(criteria_scores),
            passed_criteria=passed_count,
            failed_criteria=failed_count,
        )


class CodeQualityJudge:
    """
    Judge for code quality.
    """
    
    def __init__(self):
        self.criteria = [
            JudgementCriteria(
                criteria_id="correctness",
                name="Correctness",
                description="Code produces correct output",
                weight=2.0,
                pass_threshold=80.0,
            ),
            JudgementCriteria(
                criteria_id="readability",
                name="Readability",
                description="Code is readable and well-structured",
                weight=1.0,
                pass_threshold=70.0,
            ),
            JudgementCriteria(
                criteria_id="efficiency",
                name="Efficiency",
                description="Code is efficient",
                weight=1.0,
                pass_threshold=70.0,
            ),
            JudgementCriteria(
                criteria_id="maintainability",
                name="Maintainability",
                description="Code is maintainable",
                weight=1.0,
                pass_threshold=70.0,
            ),
        ]
    
    def judge(self, task: Any, result: Any) -> Dict[str, Any]:
        """Judge code quality."""
        output = result.output if hasattr(result, 'output') else str(result)
        
        # Simple heuristics
        score = 80.0
        
        if output:
            # Check for common issues
            if "error" in output.lower():
                score -= 20
            
            # Check code length
            if len(output) > 10000:
                score -= 10
        
        return {
            "score": score,
            "passed": score >= 70,
            "feedback": [f"Code quality score: {score:.1f}"],
        }
