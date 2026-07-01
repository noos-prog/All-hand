"""Resolvers for Capabilities and Providers."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from context import ExecutionContext
from interfaces import ICapability, IProvider
from mission import Mission
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry


class ResolutionStatus(Enum):
    """Resolution status."""
    SUCCESS = "success"
    NO_MATCH = "no_match"
    AMBIGUOUS = "ambiguous"
    ERROR = "error"


@dataclass
class SelectionScore:
    """Score for a selection."""
    total: float = 0.0
    skill_match: float = 0.0
    constraint_match: float = 0.0
    priority: float = 0.0
    details: Dict[str, float] = field(default_factory=dict)


@dataclass
class CapabilitySelection:
    """Result of capability resolution."""
    capability: ICapability
    capability_name: str
    manifest_id: str
    status: ResolutionStatus
    score: SelectionScore
    reason: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProviderSelection:
    """Result of provider resolution."""
    provider: IProvider
    provider_name: str
    status: ResolutionStatus
    score: SelectionScore
    reason: str
    supported_skills: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class CapabilityResolver:
    """Resolves the best capability for a mission. Deterministic, no AI, no randomness."""
    
    def __init__(self, capability_registry: CapabilityRegistry):
        self.capability_registry = capability_registry
    
    def resolve(
        self,
        mission: Mission,
        context: Optional[ExecutionContext] = None
    ) -> CapabilitySelection:
        """Resolve the best capability for a mission."""
        requested_capability = mission.capability
        required_skills = mission.parameters.get("required_skills", [])
        
        candidates = []
        
        for capability in self.capability_registry.list_all():
            score = self._calculate_score(
                capability=capability,
                requested=requested_capability,
                required_skills=required_skills,
                mission=mission
            )
            candidates.append((capability, score))
        
        if not candidates:
            return CapabilitySelection(
                capability=None, capability_name="", manifest_id="",
                status=ResolutionStatus.NO_MATCH, score=SelectionScore(),
                reason="No capabilities registered"
            )
        
        candidates.sort(key=lambda x: x[1].total, reverse=True)
        best_capability, best_score = candidates[0]
        
        if best_score.total < 0.1:
            return CapabilitySelection(
                capability=None, capability_name=best_capability.name, manifest_id="",
                status=ResolutionStatus.NO_MATCH, score=best_score,
                reason="No capability matches the requirements"
            )
        
        return CapabilitySelection(
            capability=best_capability,
            capability_name=best_capability.name,
            manifest_id=getattr(best_capability, "id", best_capability.name),
            status=ResolutionStatus.SUCCESS,
            score=best_score,
            reason=self._generate_reason(best_capability, best_score, requested_capability)
        )
    
    def _calculate_score(self, capability: ICapability, requested: str,
                         required_skills: List[str], mission: Mission) -> SelectionScore:
        """Calculate match score for a capability."""
        score = SelectionScore()
        
        if capability.name.lower() == requested.lower():
            score.skill_match = 1.0
        elif requested.lower() in capability.name.lower():
            score.skill_match = 0.8
        elif capability.name.lower() in requested.lower():
            score.skill_match = 0.6
        else:
            capability_skills = set(capability.skills)
            required_set = set(required_skills)
            if required_set:
                intersection = len(capability_skills & required_set)
                union = len(capability_skills | required_set)
                score.skill_match = intersection / union if union > 0 else 0.0
            else:
                score.skill_match = 0.3
        
        score.constraint_match = 1.0
        priority = getattr(capability, "priority", 1.0)
        score.priority = priority / 10.0
        
        score.total = (score.skill_match * 0.7 + score.constraint_match * 0.2 + score.priority * 0.1)
        score.details = {"skill_match": score.skill_match, "constraint_match": score.constraint_match, "priority": score.priority}
        
        return score
    
    def _generate_reason(self, capability: ICapability, score: SelectionScore, requested: str) -> str:
        """Generate human-readable reason for selection."""
        if capability.name.lower() == requested.lower():
            return "Exact name match"
        return f"Best skill match ({score.skill_match:.0%})"


class ProviderResolver:
    """Resolves the best provider for a capability. Deterministic, no AI, no randomness."""
    
    def __init__(self, provider_registry: ProviderRegistry, capability_registry: CapabilityRegistry):
        self.provider_registry = provider_registry
        self.capability_registry = capability_registry
    
    def resolve(self, capability: ICapability, mission: Optional[Mission] = None) -> ProviderSelection:
        """Resolve the best provider for a capability."""
        required_skills = capability.skills
        candidates = []
        
        for provider in self.provider_registry.list_all():
            score = self._calculate_score(provider=provider, required_skills=required_skills)
            if score.total > 0:
                candidates.append((provider, score))
        
        if not candidates:
            return ProviderSelection(
                provider=None, provider_name="", status=ResolutionStatus.NO_MATCH,
                score=SelectionScore(), reason="No providers support required skills"
            )
        
        candidates.sort(key=lambda x: x[1].total, reverse=True)
        best_provider, best_score = candidates[0]
        
        supported_skills = [s for s in required_skills if provider.supports_skill(s)]
        
        return ProviderSelection(
            provider=best_provider,
            provider_name=best_provider.name,
            status=ResolutionStatus.SUCCESS,
            score=best_score,
            reason=self._generate_reason(best_provider, best_score, required_skills),
            supported_skills=supported_skills
        )
    
    def _calculate_score(self, provider: IProvider, required_skills: List[str]) -> SelectionScore:
        """Calculate match score for a provider."""
        score = SelectionScore()
        
        if not required_skills:
            score.total = 1.0
            return score
        
        supported = sum(1 for s in required_skills if provider.supports_skill(s))
        score.skill_match = supported / len(required_skills)
        score.constraint_match = 1.0
        priority = getattr(provider, "priority", 1.0)
        score.priority = priority / 10.0
        
        score.total = (score.skill_match * 0.8 + score.constraint_match * 0.1 + score.priority * 0.1)
        score.details = {"skill_match": score.skill_match, "supported_skills": supported, "required_skills": len(required_skills)}
        
        return score
    
    def _generate_reason(self, provider: IProvider, score: SelectionScore, required_skills: List[str]) -> str:
        """Generate human-readable reason for selection."""
        supported = sum(1 for s in required_skills if provider.supports_skill(s))
        return f"Supports {supported}/{len(required_skills)} required skills. Score: {score.total:.0%}"
