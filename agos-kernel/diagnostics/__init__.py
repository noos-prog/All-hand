"""Kernel Diagnostics - Verifies kernel health and components."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class HealthStatus(Enum):
    """Health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ComponentHealth:
    """Health of a single component."""
    name: str
    status: HealthStatus
    loaded: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyHealth:
    """Health of dependencies."""
    name: str
    resolved: bool = False
    version: str = ""
    error: Optional[str] = None


@dataclass
class RegistryHealth:
    """Health of registries."""
    name: str
    count: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class StartupDiagnostics:
    """Diagnostics from startup."""
    duration_ms: int = 0
    components_loaded: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class RuntimeDiagnostics:
    """Diagnostics from runtime."""
    uptime_ms: int = 0
    missions_executed: int = 0
    events_published: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class KernelHealthReport:
    """Complete health report."""
    status: HealthStatus
    timestamp: datetime = field(default_factory=datetime.utcnow)
    components: List[ComponentHealth] = field(default_factory=list)
    startup: StartupDiagnostics = field(default_factory=StartupDiagnostics)
    runtime: RuntimeDiagnostics = field(default_factory=RuntimeDiagnostics)
    uptime_ms: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "uptime_ms": self.uptime_ms,
            "components": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "loaded": c.loaded,
                    "errors": c.errors,
                    "warnings": c.warnings
                }
                for c in self.components
            ],
            "startup": {
                "duration_ms": self.startup.duration_ms,
                "components_loaded": self.startup.components_loaded,
                "errors": self.startup.errors
            },
            "runtime": {
                "uptime_ms": self.runtime.uptime_ms,
                "missions_executed": self.runtime.missions_executed,
                "events_published": self.runtime.events_published,
                "errors": self.runtime.errors
            }
        }


class KernelHealthService:
    """Service for checking kernel health."""
    
    def __init__(self):
        self._started_at: Optional[datetime] = None
        self._missions_executed: int = 0
        self._events_published: int = 0
        self._errors: List[str] = []
    
    def set_start_time(self, started_at: datetime) -> None:
        """Set the kernel start time."""
        self._started_at = started_at
    
    def record_mission(self) -> None:
        """Record a mission execution."""
        self._missions_executed += 1
    
    def record_event(self) -> None:
        """Record an event publication."""
        self._events_published += 1
    
    def record_error(self, error: str) -> None:
        """Record an error."""
        self._errors.append(error)
    
    def check_startup(self, container: Any) -> StartupDiagnostics:
        """Check startup health."""
        diagnostics = StartupDiagnostics()
        
        if self._started_at:
            diagnostics.duration_ms = int((datetime.utcnow() - self._started_at).total_seconds() * 1000)
        
        # Check components
        components_loaded = 0
        
        # Check capability registry
        try:
            cap_registry = container.get("capability_registry") if hasattr(container, "get") else None
            if cap_registry and hasattr(cap_registry, "list_all"):
                components_loaded += len(cap_registry.list_all())
        except Exception as e:
            diagnostics.errors.append(f"Capability registry error: {e}")
        
        # Check provider registry
        try:
            prov_registry = container.get("provider_registry") if hasattr(container, "get") else None
            if prov_registry and hasattr(prov_registry, "list_all"):
                components_loaded += len(prov_registry.list_all())
        except Exception as e:
            diagnostics.errors.append(f"Provider registry error: {e}")
        
        diagnostics.components_loaded = components_loaded
        
        return diagnostics
    
    def check_runtime(self) -> RuntimeDiagnostics:
        """Check runtime health."""
        diagnostics = RuntimeDiagnostics()
        
        if self._started_at:
            diagnostics.uptime_ms = int((datetime.utcnow() - self._started_at).total_seconds() * 1000)
        
        diagnostics.missions_executed = self._missions_executed
        diagnostics.events_published = self._events_published
        diagnostics.errors = self._errors.copy()
        
        return diagnostics
    
    def check_components(self, capability_registry: Any, provider_registry: Any) -> List[ComponentHealth]:
        """Check component health."""
        components = []
        
        # Capability registry
        cap_health = ComponentHealth(
            name="CapabilityRegistry",
            status=HealthStatus.HEALTHY,
            loaded=True
        )
        
        try:
            if hasattr(capability_registry, "list_all"):
                caps = capability_registry.list_all()
                cap_health.metadata["count"] = len(caps)
                cap_health.metadata["capabilities"] = [c.name for c in caps]
        except Exception as e:
            cap_health.status = HealthStatus.UNHEALTHY
            cap_health.errors.append(str(e))
        
        components.append(cap_health)
        
        # Provider registry
        prov_health = ComponentHealth(
            name="ProviderRegistry",
            status=HealthStatus.HEALTHY,
            loaded=True
        )
        
        try:
            if hasattr(provider_registry, "list_all"):
                provs = provider_registry.list_all()
                prov_health.metadata["count"] = len(provs)
                prov_health.metadata["providers"] = [p.name for p in provs]
        except Exception as e:
            prov_health.status = HealthStatus.UNHEALTHY
            prov_health.errors.append(str(e))
        
        components.append(prov_health)
        
        return components
    
    def generate_report(
        self,
        container: Any,
        capability_registry: Any,
        provider_registry: Any
    ) -> KernelHealthReport:
        """Generate complete health report."""
        # Determine overall status
        all_healthy = True
        has_warnings = False
        
        components = self.check_components(capability_registry, provider_registry)
        
        for comp in components:
            if comp.status == HealthStatus.UNHEALTHY:
                all_healthy = False
            elif comp.status == HealthStatus.DEGRADED:
                has_warnings = True
        
        status = HealthStatus.HEALTHY
        if not all_healthy:
            status = HealthStatus.UNHEALTHY
        elif has_warnings or len(self._errors) > 0:
            status = HealthStatus.DEGRADED
        
        uptime_ms = 0
        if self._started_at:
            uptime_ms = int((datetime.utcnow() - self._started_at).total_seconds() * 1000)
        
        return KernelHealthReport(
            status=status,
            timestamp=datetime.utcnow(),
            components=components,
            startup=self.check_startup(container),
            runtime=self.check_runtime(),
            uptime_ms=uptime_ms
        )
