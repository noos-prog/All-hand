"""Mission Manager and Core Kernel with Auto-Discovery."""
import os
import sys
from datetime import datetime
from typing import Any, Optional

from context import ContextBuilder, ExecutionContext
from decision import Decision, DecisionEngine
from discovery import AutoDiscovery
from events import Event, EventBus, EventType
from execution import ExecutionEngine
from mission import Mission, MissionStatus
from pipeline import ExecutionPipeline
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry
from resolvers import CapabilityResolver, ProviderResolver
from shared import Result, ResultStatus


class MissionManager:
    """Main entry point for AGOS Kernel. Coordinates the entire mission execution flow."""
    
    def __init__(
        self,
        event_bus: EventBus,
        capability_registry: CapabilityRegistry,
        provider_registry: ProviderRegistry,
        capability_resolver: CapabilityResolver,
        provider_resolver: ProviderResolver,
        pipeline: ExecutionPipeline
    ):
        self.event_bus = event_bus
        self.capability_registry = capability_registry
        self.provider_registry = provider_registry
        self.capability_resolver = capability_resolver
        self.provider_resolver = provider_resolver
        self.pipeline = pipeline
    
    def execute(self, mission: Mission) -> Result[Any]:
        """Execute a mission from start to finish using the execution pipeline."""
        mission_id = mission.id
        
        mission.status = MissionStatus.RUNNING
        mission.started_at = datetime.utcnow()
        
        self.event_bus.publish(Event(
            type=EventType.MISSION_STARTED,
            mission_id=mission_id,
            data={"mission": mission.name}
        ))
        
        # Execute through pipeline
        execution_result = self.pipeline.execute(mission)
        
        if execution_result.status.value == "completed":
            mission.status = MissionStatus.COMPLETED
            mission.completed_at = datetime.utcnow()
            mission.result = execution_result.result
            
            self.event_bus.publish(Event(
                type=EventType.MISSION_COMPLETED,
                mission_id=mission_id,
                data={"mission": mission.name, "duration_ms": execution_result.duration_ms}
            ))
            
            return Result(status=ResultStatus.SUCCESS, data=execution_result.result)
        else:
            mission.status = MissionStatus.FAILED
            mission.error = execution_result.error
            
            self.event_bus.publish(Event(
                type=EventType.MISSION_FAILED,
                mission_id=mission_id,
                data={"error": execution_result.error}
            ))
            
            return Result(status=ResultStatus.FAILURE, error=execution_result.error)


class AGOSKernel:
    """
    The AGOS Kernel.
    Creates and manages the entire system with auto-discovery.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Create registries (no singletons)
        self.event_bus = EventBus()
        self.capability_registry = CapabilityRegistry()
        self.provider_registry = ProviderRegistry()
        
        # Auto-discovery
        self.discovery = AutoDiscovery(base_path)
        
        # Create resolvers
        self.capability_resolver = CapabilityResolver(self.capability_registry)
        self.provider_resolver = ProviderResolver(
            self.provider_registry,
            self.capability_registry
        )
        
        # Create pipeline
        self.pipeline = ExecutionPipeline(
            event_bus=self.event_bus,
            capability_resolver=self.capability_resolver,
            provider_resolver=self.provider_resolver
        )
        
        # Create mission manager
        self.mission_manager = MissionManager(
            event_bus=self.event_bus,
            capability_registry=self.capability_registry,
            provider_registry=self.provider_registry,
            capability_resolver=self.capability_resolver,
            provider_resolver=self.provider_resolver,
            pipeline=self.pipeline
        )
    
    def discover_and_register(self) -> None:
        """Discover and register all capabilities and providers automatically."""
        print("[KERNEL] Starting auto-discovery...")
        
        # Discover capabilities
        cap_result = self.discovery.discover_capabilities()
        print(f"[KERNEL] Found {cap_result.discovered} capabilities, loaded {cap_result.loaded}")
        
        for manifest in cap_result.manifests:
            if not manifest.errors:
                capability = self.discovery.load_capability(manifest)
                if capability:
                    self.capability_registry.register(capability)
                    print(f"[KERNEL] Registered capability: {capability.name}")
            else:
                print(f"[KERNEL] Failed to load {manifest.name}: {manifest.errors}")
        
        # Discover providers
        prov_result = self.discovery.discover_providers()
        print(f"[KERNEL] Found {prov_result.discovered} providers, loaded {prov_result.loaded}")
        
        for manifest in prov_result.manifests:
            if not manifest.errors:
                provider = self.discovery.load_provider(manifest)
                if provider:
                    self.provider_registry.register(provider)
                    print(f"[KERNEL] Registered provider: {provider.name}")
            else:
                print(f"[KERNEL] Failed to load {manifest.name}: {manifest.errors}")
        
        print("[KERNEL] Auto-discovery complete")
    
    def start(self) -> None:
        """Start the kernel and discover components."""
        print("[KERNEL] AGOS Kernel starting...")
        self.discover_and_register()
        print("[KERNEL] AGOS Kernel started")
    
    def shutdown(self) -> None:
        """Shutdown the kernel."""
        print("[KERNEL] AGOS Kernel shutdown")
