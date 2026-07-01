"""Runtime Bootstrapper - Initializes the entire AGOS Kernel."""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from container import Container, Lifetime, LifetimeManager
from discovery import AutoDiscovery
from event_engine import EventEngine
from mission_engine import MissionEngine
from pipeline import ExecutionPipeline
from resolvers import CapabilityResolver, ProviderResolver
from registry.capability import CapabilityRegistry
from registry.provider import ProviderRegistry


@dataclass
class BootstrapResult:
    """Result of bootstrap operation."""
    success: bool
    kernel_version: str = "0.2.0"
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration_ms: int = 0
    loaded_capabilities: List[str] = field(default_factory=list)
    loaded_providers: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class Bootstrapper:
    """
    Runtime Bootstrapper.
    
    Boot Order:
    1. Load Configuration
    2. Build Container
    3. Register Infrastructure
    4. Load Capabilities
    5. Load Providers
    6. Validate Contracts
    7. Initialize Event Engine
    8. Initialize Mission Engine
    9. Kernel Ready
    """
    
    KERNEL_VERSION = "0.2.0"
    
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.base_path = base_path
        
        self.container: Optional[Container] = None
        self.event_engine: Optional[EventEngine] = None
        self.mission_engine: Optional[MissionEngine] = None
        self.result: Optional[BootstrapResult] = None
    
    def bootstrap(self) -> BootstrapResult:
        """Bootstrap the kernel."""
        self.result = BootstrapResult(success=False, kernel_version=self.KERNEL_VERSION, started_at=datetime.utcnow())
        
        try:
            print("=" * 60)
            print(f"AGOS KERNEL v{self.KERNEL_VERSION} BOOTSTRAP")
            print("=" * 60)
            
            # Step 1-3: Container
            print("\n[1-3] Building container...")
            self._build_container()
            print("✓ Container built")
            
            # Step 4: Load Capabilities
            print("\n[4] Loading capabilities...")
            self._load_capabilities()
            print(f"✓ {len(self.result.loaded_capabilities)} capabilities loaded")
            
            # Step 5: Load Providers
            print("\n[5] Loading providers...")
            self._load_providers()
            print(f"✓ {len(self.result.loaded_providers)} providers loaded")
            
            # Step 6: Validate Contracts
            print("\n[6] Validating contracts...")
            if not self._validate_contracts():
                raise Exception("Contract validation failed")
            print("✓ Contracts validated")
            
            # Step 7: Initialize Event Engine
            print("\n[7] Initializing event engine...")
            self._initialize_event_engine()
            print("✓ Event engine initialized")
            
            # Step 8: Initialize Mission Engine
            print("\n[8] Initializing mission engine...")
            self._initialize_mission_engine()
            print("✓ Mission engine initialized")
            
            # Step 9: Complete
            self.result.success = True
            self.result.completed_at = datetime.utcnow()
            self.result.duration_ms = int((self.result.completed_at - self.result.started_at).total_seconds() * 1000)
            
            print("\n" + "=" * 60)
            print("✅ AGOS KERNEL READY")
            print("=" * 60)
            print(f"\nVersion: {self.KERNEL_VERSION}")
            print(f"Capabilities: {len(self.result.loaded_capabilities)}")
            print(f"Providers: {len(self.result.loaded_providers)}")
            print(f"Startup time: {self.result.duration_ms}ms")
            
            return self.result
            
        except Exception as e:
            self.result.success = False
            self.result.errors.append(str(e))
            self.result.completed_at = datetime.utcnow()
            self.result.duration_ms = int((self.result.completed_at - self.result.started_at).total_seconds() * 1000)
            print(f"\n❌ BOOTSTRAP FAILED: {e}")
            return self.result
    
    def _build_container(self) -> None:
        """Build dependency injection container."""
        self.container = Container()
        self._capability_registry = CapabilityRegistry()
        self._provider_registry = ProviderRegistry()
    
    def _load_capabilities(self) -> None:
        """Load capabilities via discovery."""
        self._discovery = AutoDiscovery(self.base_path)
        result = self._discovery.discover_capabilities()
        
        for manifest in result.manifests:
            if not manifest.errors:
                capability = self._discovery.load_capability(manifest)
                if capability:
                    self._capability_registry.register(capability)
                    self.result.loaded_capabilities.append(capability.name)
    
    def _load_providers(self) -> None:
        """Load providers via discovery."""
        result = self._discovery.discover_providers()
        
        for manifest in result.manifests:
            if not manifest.errors:
                provider = self._discovery.load_provider(manifest)
                if provider:
                    self._provider_registry.register(provider)
                    self.result.loaded_providers.append(provider.name)
    
    def _validate_contracts(self) -> bool:
        """Validate all contracts."""
        if len(self.result.loaded_capabilities) == 0:
            self.result.errors.append("No capabilities loaded")
            return False
        if len(self.result.loaded_providers) == 0:
            self.result.errors.append("No providers loaded")
            return False
        return True
    
    def _initialize_event_engine(self) -> None:
        """Initialize event engine."""
        self.event_engine = EventEngine()
    
    def _initialize_mission_engine(self) -> None:
        """Initialize mission engine."""
        capability_resolver = CapabilityResolver(self._capability_registry)
        provider_resolver = ProviderResolver(self._provider_registry, self._capability_registry)
        
        pipeline = ExecutionPipeline(
            event_bus=None,
            capability_resolver=capability_resolver,
            provider_resolver=provider_resolver
        )
        
        self.mission_engine = MissionEngine(pipeline)
    
    def get_kernel(self):
        """Get the initialized kernel."""
        return {
            "container": self.container,
            "event_engine": self.event_engine,
            "mission_engine": self.mission_engine,
            "capability_registry": self._capability_registry,
            "provider_registry": self._provider_registry,
        }
