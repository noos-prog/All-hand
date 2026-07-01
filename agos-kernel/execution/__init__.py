"""Execution Engine."""
from datetime import datetime
from typing import Any

from context import ExecutionContext
from decision import Decision
from events import Event, EventBus, EventType
from interfaces import ICapability, IProvider
from mission import MissionStatus
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry
from shared import Result, ResultStatus


class ExecutionEngine:
    """
    Executes capabilities using providers.
    """
    
    def __init__(
        self,
        event_bus: EventBus,
        capability_registry: CapabilityRegistry,
        provider_registry: ProviderRegistry
    ):
        self.event_bus = event_bus
        self.capability_registry = capability_registry
        self.provider_registry = provider_registry
    
    def execute(self, context: ExecutionContext, decision: Decision) -> Result[Any]:
        """
        Execute the capability.
        """
        mission_id = context.mission.id
        
        # Publish ExecutionStarted event
        self.event_bus.publish(Event(
            type=EventType.EXECUTION_STARTED,
            mission_id=mission_id,
            data={
                "capability": decision.capability,
                "provider": decision.provider,
                "skills": decision.skills
            }
        ))
        
        # Get capability
        capability = self.capability_registry.get(decision.capability)
        if capability is None:
            return Result(
                status=ResultStatus.FAILURE,
                error=f"Capability not found: {decision.capability}"
            )
        
        # Get provider
        provider = self.provider_registry.get(decision.provider)
        if provider is None:
            return Result(
                status=ResultStatus.FAILURE,
                error=f"Provider not found: {decision.provider}"
            )
        
        try:
            # Execute capability
            result_data = capability.execute(context.mission.parameters)
            
            # Publish ExecutionCompleted event
            self.event_bus.publish(Event(
                type=EventType.EXECUTION_COMPLETED,
                mission_id=mission_id,
                data={
                    "capability": decision.capability,
                    "success": True
                }
            ))
            
            return Result(
                status=ResultStatus.SUCCESS,
                data=result_data
            )
            
        except Exception as e:
            # Publish failure
            self.event_bus.publish(Event(
                type=EventType.EXECUTION_FAILED,
                mission_id=mission_id,
                data={
                    "capability": decision.capability,
                    "error": str(e)
                }
            ))
            
            return Result(
                status=ResultStatus.FAILURE,
                error=str(e)
            )
