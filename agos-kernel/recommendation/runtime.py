"""Universal Recommendation Engine."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RecommendationType(Enum):
    """Recommendation type."""
    CAPABILITY = "capability"
    PROVIDER = "provider"
    SKILL = "skill"
    ARCHITECTURE = "architecture"
    PATTERN = "pattern"
    TOOL = "tool"
    MODEL = "model"
    STRATEGY = "strategy"
    POLICY = "policy"
    WORKFLOW = "workflow"


@dataclass
class RecommendationScore:
    """Score components for recommendation."""
    evidence: float = 0.0
    knowledge: float = 0.0
    benchmark: float = 0.0
    past_success: float = 0.0
    compatibility: float = 0.0
    risk: float = 0.0
    cost: float = 0.0
    quality: float = 0.0


@dataclass
class Recommendation:
    """Universal Recommendation."""
    id: str
    recommendation_type: RecommendationType
    name: str
    description: str
    
    # Scoring
    score: RecommendationScore = field(default_factory=RecommendationScore)
    total_score: float = 0.0
    
    # Reasoning
    reasoning: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    
    # Confidence
    confidence: float = 0.5
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


class RecommendationEngine:
    """Universal Recommendation Engine."""
    
    def __init__(self):
        """Initialize recommendation engine."""
        self.recommendations: List[Recommendation] = []
        self.history: List[Recommendation] = []
    
    def recommend(
        self,
        recommendation_type: RecommendationType,
        name: str,
        description: str,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> Recommendation:
        """Generate recommendation."""
        rec_id = self._generate_id(name)
        
        score = RecommendationScore()
        
        # Calculate total score
        total = (
            score.evidence * 0.2 +
            score.knowledge * 0.15 +
            score.benchmark * 0.15 +
            score.past_success * 0.2 +
            score.compatibility * 0.1 +
            (1 - score.risk) * 0.1 +
            (1 - score.cost) * 0.05 +
            score.quality * 0.05
        )
        
        recommendation = Recommendation(
            id=rec_id,
            recommendation_type=recommendation_type,
            name=name,
            description=description,
            score=score,
            total_score=total,
            evidence=evidence or {},
            confidence=0.5,
        )
        
        self.recommendations.append(recommendation)
        return recommendation
    
    def add_reasoning(self, rec_id: str, reasoning: str) -> bool:
        """Add reasoning to recommendation."""
        for rec in self.recommendations:
            if rec.id == rec_id:
                rec.reasoning.append(reasoning)
                return True
        return False
    
    def set_score(self, rec_id: str, **scores) -> bool:
        """Set score components."""
        for rec in self.recommendations:
            if rec.id == rec_id:
                for key, value in scores.items():
                    if hasattr(rec.score, key):
                        setattr(rec.score, key, value)
                
                # Recalculate total
                rec.total_score = (
                    rec.score.evidence * 0.2 +
                    rec.score.knowledge * 0.15 +
                    rec.score.benchmark * 0.15 +
                    rec.score.past_success * 0.2 +
                    rec.score.compatibility * 0.1 +
                    (1 - rec.score.risk) * 0.1 +
                    (1 - rec.score.cost) * 0.05 +
                    rec.score.quality * 0.05
                )
                return True
        return False
    
    def get_recommendations(
        self,
        recommendation_type: Optional[RecommendationType] = None,
        min_score: float = 0.0,
        limit: int = 10,
    ) -> List[Recommendation]:
        """Get recommendations."""
        results = self.recommendations
        
        if recommendation_type:
            results = [r for r in results if r.recommendation_type == recommendation_type]
        
        results = [r for r in results if r.total_score >= min_score]
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        return results[:limit]
    
    def finalize(self, rec_id: str) -> Optional[Recommendation]:
        """Finalize and archive recommendation."""
        for i, rec in enumerate(self.recommendations):
            if rec.id == rec_id:
                self.recommendations.pop(i)
                self.history.append(rec)
                return rec
        return None
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
