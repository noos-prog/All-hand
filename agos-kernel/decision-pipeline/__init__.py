"""Decision Pipeline - All decisions execute through this pipeline."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class DecisionStatus(Enum):
    """Decision status."""
    PENDING = "pending"
    VALIDATING = "validating"
    COLLECTING = "collecting"
    EVALUATING = "evaluating"
    RANKING = "ranking"
    SELECTED = "selected"
    FAILED = "failed"


@dataclass
class DecisionScore:
    """Score for a decision."""
    total: float = 0.0
    skill_match: float = 0.0
    priority: float = 0.0
    compatibility: float = 0.0
    details: Dict[str, float] = field(default_factory=dict)


@dataclass
class DecisionReason:
    """Reason for a decision."""
    rule: str
    description: str
    weight: float = 1.0


@dataclass
class DecisionResult:
    """Result of a decision."""
    decision_id: str
    status: DecisionStatus
    capability: Optional[str] = None
    provider: Optional[str] = None
    score: Optional[DecisionScore] = None
    reasons: List[DecisionReason] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "status": self.status.value,
            "capability": self.capability,
            "provider": self.provider,
            "score": {
                "total": self.score.total if self.score else 0,
                "skill_match": self.score.skill_match if self.score else 0,
                "priority": self.score.priority if self.score else 0
            } if self.score else None,
            "reasons": [{"rule": r.rule, "description": r.description} for r in self.reasons],
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }


class DecisionContext:
    """Context for decision."""
    
    def __init__(self, mission: Any):
        self.decision_id = str(uuid4())
        self.mission = mission
        self.required_capability = getattr(mission, "capability", "")
        self.required_skills = getattr(mission, "parameters", {}).get("required_skills", [])
        self.constraints = getattr(mission, "parameters", {}).get("constraints", [])


class DecisionValidator:
    """Validates decision context."""
    
    def validate(self, context: DecisionContext) -> List[str]:
        """Validate context."""
        errors = []
        
        if not context.required_capability:
            errors.append("Required capability is empty")
        
        return errors


class CandidateCollector:
    """Collects candidate capabilities and providers."""
    
    def __init__(self, capability_registry, provider_registry):
        self.capability_registry = capability_registry
        self.provider_registry = provider_registry
    
    def collect_capabilities(self, context: DecisionContext) -> List[Any]:
        """Collect candidate capabilities."""
        capabilities = self.capability_registry.list_all()
        
        # Filter by required capability name
        candidates = []
        for cap in capabilities:
            cap_name = getattr(cap, "name", "")
            if cap_name.lower() == context.required_capability.lower():
                candidates.append(cap)
        
        # If no exact match, include all
        if not candidates:
            candidates = capabilities
        
        return candidates
    
    def collect_providers(self, context: DecisionContext, capability: Any) -> List[Any]:
        """Collect candidate providers for a capability."""
        providers = self.provider_registry.list_all()
        
        # Filter by skills
        required_skills = getattr(capability, "skills", [])
        
        candidates = []
        for prov in providers:
            if hasattr(prov, "supports_skill"):
                # Check if provider supports all required skills
                supported = all(prov.supports_skill(s) for s in required_skills)
                if supported:
                    candidates.append(prov)
        
        return candidates or providers


class RuleEvaluator:
    """Evaluates rules for decision making."""
    
    def evaluate_capability(self, capability: Any, context: DecisionContext) -> DecisionScore:
        """Evaluate capability against context."""
        score = DecisionScore()
        
        # Skill match
        cap_skills = set(getattr(capability, "skills", []))
        req_skills = set(context.required_skills)
        
        if req_skills:
            intersection = len(cap_skills & req_skills)
            union = len(cap_skills | req_skills)
            score.skill_match = intersection / union if union > 0 else 0.5
        else:
            score.skill_match = 1.0
        
        # Name match
        cap_name = getattr(capability, "name", "").lower()
        req_name = context.required_capability.lower()
        if cap_name == req_name:
            score.skill_match = 1.0
        
        # Priority
        score.priority = getattr(capability, "priority", 1) / 10.0
        
        # Calculate total
        score.total = score.skill_match * 0.8 + score.priority * 0.2
        
        score.details = {
            "skill_match": score.skill_match,
            "priority": score.priority
        }
        
        return score
    
    def evaluate_provider(self, provider: Any, capability: Any) -> DecisionScore:
        """Evaluate provider against capability."""
        score = DecisionScore()
        
        required_skills = getattr(capability, "skills", [])
        
        if not required_skills:
            score.skill_match = 1.0
        else:
            supported = 0
            for skill in required_skills:
                if hasattr(provider, "supports_skill") and provider.supports_skill(skill):
                    supported += 1
            score.skill_match = supported / len(required_skills)
        
        score.priority = 1.0
        score.total = score.skill_match * 0.9 + score.priority * 0.1
        
        return score


class CandidateRanker:
    """Ranks candidates."""
    
    def rank_capabilities(self, candidates: List[Any], scores: List[DecisionScore]) -> List[tuple]:
        """Rank capabilities by score."""
        ranked = list(zip(candidates, scores))
        ranked.sort(key=lambda x: x[1].total, reverse=True)
        return ranked
    
    def rank_providers(self, candidates: List[Any], scores: List[DecisionScore]) -> List[tuple]:
        """Rank providers by score."""
        ranked = list(zip(candidates, scores))
        ranked.sort(key=lambda x: x[1].total, reverse=True)
        return ranked


class DecisionPipeline:
    """
    Decision Pipeline.
    
    Pipeline:
    1. Receive Context
    2. Validate Context
    3. Collect Candidate Capabilities
    4. Collect Candidate Providers
    5. Evaluate Rules
    6. Rank Candidates
    7. Select Best Option
    8. Return Decision
    
    Rules:
    ✅ Deterministic
    ✅ Repeatable
    ✅ Explainable
    ✅ Observable
    """
    
    def __init__(
        self,
        capability_registry,
        provider_registry
    ):
        self.capability_registry = capability_registry
        self.provider_registry = provider_registry
        
        self.validator = DecisionValidator()
        self.collector = CandidateCollector(capability_registry, provider_registry)
        self.evaluator = RuleEvaluator()
        self.ranker = CandidateRanker()
    
    def decide(self, context: DecisionContext) -> DecisionResult:
        """Execute the decision pipeline."""
        result = DecisionResult(
            decision_id=context.decision_id,
            status=DecisionStatus.PENDING
        )
        
        try:
            # Step 1-2: Validate context
            result.status = DecisionStatus.VALIDATING
            errors = self.validator.validate(context)
            if errors:
                result.status = DecisionStatus.FAILED
                result.error = "; ".join(errors)
                return result
            
            # Step 3: Collect capabilities
            result.status = DecisionStatus.COLLECTING
            capabilities = self.collector.collect_capabilities(context)
            
            if not capabilities:
                result.status = DecisionStatus.FAILED
                result.error = "No candidate capabilities found"
                return result
            
            # Step 4: Evaluate capabilities
            result.status = DecisionStatus.EVALUATING
            cap_scores = [self.evaluator.evaluate_capability(cap, context) for cap in capabilities]
            
            # Step 5: Rank capabilities
            result.status = DecisionStatus.RANKING
            ranked_caps = self.ranker.rank_capabilities(capabilities, cap_scores)
            best_cap, best_cap_score = ranked_caps[0]
            
            # Step 6: Collect providers
            providers = self.collector.collect_providers(context, best_cap)
            
            if not providers:
                result.status = DecisionStatus.FAILED
                result.error = "No candidate providers found"
                return result
            
            # Step 7: Evaluate providers
            prov_scores = [self.evaluator.evaluate_provider(prov, best_cap) for prov in providers]
            ranked_provs = self.ranker.rank_providers(providers, prov_scores)
            best_prov, best_prov_score = ranked_provs[0]
            
            # Step 8: Select
            result.status = DecisionStatus.SELECTED
            result.capability = getattr(best_cap, "name", "")
            result.provider = getattr(best_prov, "name", "")
            result.score = best_cap_score
            result.reasons = [
                DecisionReason("skill_match", f"Skill match: {best_cap_score.skill_match:.0%}"),
                DecisionReason("priority", f"Priority: {best_cap_score.priority:.1f}"),
                DecisionReason("provider", f"Provider: {result.provider}")
            ]
            
            return result
            
        except Exception as e:
            result.status = DecisionStatus.FAILED
            result.error = str(e)
            return result
