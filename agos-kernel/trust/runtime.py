"""Universal Trust Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TrustFactor(Enum):
    """Trust score factors."""
    VERIFICATION = "verification"
    EVIDENCE = "evidence"
    HISTORY = "history"
    RELIABILITY = "reliability"
    SECURITY = "security"
    BENCHMARKS = "benchmarks"
    HUMAN_VALIDATION = "human_validation"


class TrustLevel(Enum):
    """Trust level."""
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"


@dataclass
class TrustScore:
    """Trust score for an entity."""
    entity_id: str
    entity_type: str
    overall_score: float = 0.0
    trust_level: TrustLevel = TrustLevel.MEDIUM
    
    # Factors
    verification_score: float = 0.0
    evidence_score: float = 0.0
    history_score: float = 0.0
    reliability_score: float = 0.0
    security_score: float = 0.0
    benchmark_score: float = 0.0
    human_validation_score: float = 0.0
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def calculate_overall(self) -> float:
        """Calculate overall trust score."""
        self.overall_score = (
            self.verification_score * 0.2 +
            self.evidence_score * 0.2 +
            self.history_score * 0.15 +
            self.reliability_score * 0.15 +
            self.security_score * 0.1 +
            self.benchmark_score * 0.1 +
            self.human_validation_score * 0.1
        )
        
        # Determine trust level
        if self.overall_score >= 0.9:
            self.trust_level = TrustLevel.VERIFIED
        elif self.overall_score >= 0.7:
            self.trust_level = TrustLevel.HIGH
        elif self.overall_score >= 0.5:
            self.trust_level = TrustLevel.MEDIUM
        elif self.overall_score >= 0.3:
            self.trust_level = TrustLevel.LOW
        else:
            self.trust_level = TrustLevel.UNTRUSTED
        
        self.last_updated = datetime.now()
        return self.overall_score


class TrustRuntime:
    """Universal Trust Runtime."""
    
    def __init__(self):
        """Initialize trust runtime."""
        self.trust_scores: Dict[str, TrustScore] = {}
        self.default_scores: Dict[str, float] = {
            "verification": 0.5,
            "evidence": 0.5,
            "history": 0.5,
            "reliability": 0.5,
            "security": 0.5,
            "benchmark": 0.5,
            "human_validation": 0.5,
        }
    
    def create_trust_score(
        self,
        entity_id: str,
        entity_type: str,
        factors: Optional[Dict[str, float]] = None,
    ) -> TrustScore:
        """Create a trust score for an entity."""
        score = TrustScore(
            entity_id=entity_id,
            entity_type=entity_type,
        )
        
        # Apply default or provided factors
        for factor, value in (factors or self.default_scores).items():
            if hasattr(score, f"{factor}_score"):
                setattr(score, f"{factor}_score", value)
        
        score.calculate_overall()
        self.trust_scores[entity_id] = score
        
        return score
    
    def get_trust_score(self, entity_id: str) -> Optional[TrustScore]:
        """Get trust score for an entity."""
        return self.trust_scores.get(entity_id)
    
    def update_factor(
        self,
        entity_id: str,
        factor: TrustFactor,
        value: float,
    ) -> bool:
        """Update a trust factor."""
        score = self.trust_scores.get(entity_id)
        if not score:
            return False
        
        factor_name = f"{factor.value}_score"
        if hasattr(score, factor_name):
            setattr(score, factor_name, value)
            
            # Record history
            score.history.append({
                "factor": factor.value,
                "old_value": getattr(score, factor_name),
                "new_value": value,
                "timestamp": datetime.now().isoformat(),
            })
            
            score.calculate_overall()
            return True
        
        return False
    
    def verify_entity(self, entity_id: str) -> bool:
        """Mark entity as verified."""
        score = self.trust_scores.get(entity_id)
        if not score:
            score = self.create_trust_score(entity_id, "unknown")
        
        score.verification_score = 1.0
        score.calculate_overall()
        
        # Add to history
        score.history.append({
            "action": "verified",
            "timestamp": datetime.now().isoformat(),
        })
        
        return True
    
    def add_evidence(self, entity_id: str, evidence: Dict[str, Any]) -> bool:
        """Add evidence to trust score."""
        score = self.trust_scores.get(entity_id)
        if not score:
            return False
        
        # Update evidence score
        score.evidence_score = min(1.0, score.evidence_score + 0.1)
        score.calculate_overall()
        
        return True
    
    def add_human_validation(self, entity_id: str, validated: bool) -> bool:
        """Add human validation to trust score."""
        score = self.trust_scores.get(entity_id)
        if not score:
            return False
        
        if validated:
            score.human_validation_score = min(1.0, score.human_validation_score + 0.2)
        else:
            score.human_validation_score = max(0.0, score.human_validation_score - 0.3)
        
        score.calculate_overall()
        return True
    
    def get_trust_level(self, entity_id: str) -> TrustLevel:
        """Get trust level for an entity."""
        score = self.trust_scores.get(entity_id)
        if not score:
            return TrustLevel.UNTRUSTED
        return score.trust_level
    
    def compare_entities(self, entity_id1: str, entity_id2: str) -> Dict[str, Any]:
        """Compare trust scores of two entities."""
        score1 = self.trust_scores.get(entity_id1)
        score2 = self.trust_scores.get(entity_id2)
        
        if not score1 or not score2:
            return {"error": "One or both entities not found"}
        
        return {
            "entity1": {
                "id": score1.entity_id,
                "overall_score": score1.overall_score,
                "trust_level": score1.trust_level.value,
            },
            "entity2": {
                "id": score2.entity_id,
                "overall_score": score2.overall_score,
                "trust_level": score2.trust_level.value,
            },
            "score_diff": score1.overall_score - score2.overall_score,
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get trust statistics."""
        total = len(self.trust_scores)
        
        by_level = {
            "untrusted": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "verified": 0,
        }
        
        for score in self.trust_scores.values():
            by_level[score.trust_level.value] += 1
        
        avg_score = sum(s.overall_score for s in self.trust_scores.values()) / total if total > 0 else 0
        
        return {
            "total_entities": total,
            "by_trust_level": by_level,
            "average_score": avg_score,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
