"""Mission Manager and Core Kernel."""
from datetime import datetime
from typing import Any

from context import ContextBuilder, ExecutionContext
from decision import Decision, DecisionEngine
from events import Event, EventBus, EventType
from execution import ExecutionEngine
from mission import Mission, MissionStatus
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry
from shared import Result, ResultStatus


class MissionManager:
    """
    Main entry point for AGOS Kernel.
    Coordinates the entire mission execution flow.
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
        
        # Initialize components
        self.context_builder = ContextBuilder()
        self.decision_engine = DecisionEngine(
            capability_registry,
            provider_registry
        )
        self.execution_engine = ExecutionEngine(
            event_bus,
            capability_registry,
            provider_registry
        )
    
    def execute(self, mission: Mission) -> Result[Any]:
        """
        Execute a mission from start to finish.
        
        Flow:
        1. Create mission
        2. Build context
        3. Make decision
        4. Execute
        5. Complete mission
        """
        mission_id = mission.id
        
        # Update mission status
        mission.status = MissionStatus.RUNNING
        mission.started_at = datetime.utcnow()
        
        # Publish MissionStarted event
        self.event_bus.publish(Event(
            type=EventType.MISSION_STARTED,
            mission_id=mission_id,
            data={"mission": mission.name}
        ))
        
        # Step 1: Build context
        context = self.context_builder.build(mission)
        
        # Step 2: Make decision
        decision_result = self.decision_engine.decide(context)
        if decision_result.is_failure:
            mission.status = MissionStatus.FAILED
            mission.error = decision_result.error
            return Result(
                status=ResultStatus.FAILURE,
                error=decision_result.error
            )
        
        decision: Decision = decision_result.data
        
        # Publish CapabilitySelected event
        self.event_bus.publish(Event(
            type=EventType.CAPABILITY_SELECTED,
            mission_id=mission_id,
            data={"capability": decision.capability}
        ))
        
        # Publish ProviderSelected event
        self.event_bus.publish(Event(
            type=EventType.PROVIDER_SELECTED,
            mission_id=mission_id,
            data={"provider": decision.provider}
        ))
        
        # Step 3: Execute
        execution_result = self.execution_engine.execute(context, decision)
        if execution_result.is_failure:
            mission.status = MissionStatus.FAILED
            mission.error = execution_result.error
            self.event_bus.publish(Event(
                type=EventType.MISSION_FAILED,
                mission_id=mission_id,
                data={"error": execution_result.error}
            ))
            return Result(
                status=ResultStatus.FAILURE,
                error=execution_result.error
            )
        
        # Step 4: Complete mission
        mission.status = MissionStatus.COMPLETED
        mission.completed_at = datetime.utcnow()
        mission.result = execution_result.data
        
        # Publish MissionCompleted event
        self.event_bus.publish(Event(
            type=EventType.MISSION_COMPLETED,
            mission_id=mission_id,
            data={
                "mission": mission.name,
                "capability": decision.capability,
                "provider": decision.provider
            }
        ))
        
        return Result(
            status=ResultStatus.SUCCESS,
            data=execution_result.data
        )


class AGOSKernel:
    """
    The AGOS Kernel.
    Creates and manages the entire system.
    """
    
    def __init__(self):
        # Create registries (no singletons)
        self.event_bus = EventBus()
        self.capability_registry = CapabilityRegistry()
        self.provider_registry = ProviderRegistry()
        
        # Create mission manager
        self.mission_manager = MissionManager(
            event_bus=self.event_bus,
            capability_registry=self.capability_registry,
            provider_registry=self.provider_registry
        )
    
    def start(self) -> None:
        """Start the kernel."""
        print("[KERNEL] AGOS Kernel started")
    
    def shutdown(self) -> None:
        """Shutdown the kernel."""
        print("[KERNEL] AGOS Kernel shutdown")
