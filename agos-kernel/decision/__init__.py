"""Decision Engine."""
from dataclasses import dataclass
from typing import List, Optional

from context import ExecutionContext
from interfaces import ICapability, IProvider
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry
from shared import Result, ResultStatus


@dataclass
class Decision:
    """A decision made by the engine."""
    capability: str
    provider: str
    skills: List[str]


class DecisionEngine:
    """
    Decides which capability and provider to use.
    Simple rule-based for now.
    """
    
    def __init__(
        self,
        capability_registry: CapabilityRegistry,
        provider_registry: ProviderRegistry
    ):
        self.capability_registry = capability_registry
        self.provider_registry = provider_registry
    
    def decide(self, context: ExecutionContext) -> Result[Decision]:
        """
        Make decisions for the mission.
        
        Rules:
        1. Find requested capability
        2. Find provider that supports required skills
        3. Return decision
        """
        capability_name = context.mission.capability
        
        # Check capability exists
        capability = self.capability_registry.get(capability_name)
        if capability is None:
            return Result(
                status=ResultStatus.FAILURE,
                error=f"Capability not found: {capability_name}"
            )
        
        # Get skills needed
        skills = capability.skills
        
        # Find provider for skills
        provider = None
        for skill_name in skills:
            p = self.provider_registry.find_for_skill(skill_name)
            if p:
                provider = p
                break
        
        if provider is None:
            return Result(
                status=ResultStatus.FAILURE,
                error=f"No provider found for skills: {skills}"
            )
        
        # Make decision
        decision = Decision(
            capability=capability_name,
            provider=provider.name,
            skills=skills
        )
        
        # Update context
        context.selected_capability = decision.capability
        context.selected_provider = decision.provider
        context.selected_skills = decision.skills
        
        return Result(
            status=ResultStatus.SUCCESS,
            data=decision
        )
