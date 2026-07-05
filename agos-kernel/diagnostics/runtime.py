"""Self-Diagnostics Runtime."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DiagnosticStatus(Enum):
    """Diagnostic status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class DiagnosticType(Enum):
    """Diagnostic type."""
    MEMORY = "memory"
    CPU = "cpu"
    DISK = "disk"
    NETWORK = "network"
    MODULE = "module"
    CAPABILITY = "capability"


@dataclass
class DiagnosticResult:
    """Result of a diagnostic check."""
    diagnostic_type: DiagnosticType
    status: DiagnosticStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class SelfDiagnosticsRuntime:
    """
    Self-Diagnostics Runtime.
    
    Monitors system health and detects issues.
    
    Usage:
        diagnostics = SelfDiagnosticsRuntime()
        results = diagnostics.run_all_diagnostics()
    """
    
    def __init__(self):
        """Initialize diagnostics runtime."""
        self._last_check: Optional[datetime] = None
        self._results: List[DiagnosticResult] = []
    
    def run_diagnostic(
        self,
        diagnostic_type: DiagnosticType,
        **kwargs
    ) -> DiagnosticResult:
        """Run a specific diagnostic."""
        if diagnostic_type == DiagnosticType.MEMORY:
            return self._check_memory()
        elif diagnostic_type == DiagnosticType.CPU:
            return self._check_cpu()
        elif diagnostic_type == DiagnosticType.DISK:
            return self._check_disk()
        elif diagnostic_type == DiagnosticType.NETWORK:
            return self._check_network()
        elif diagnostic_type == DiagnosticType.MODULE:
            return self._check_module(kwargs.get("module_name", ""))
        elif diagnostic_type == DiagnosticType.CAPABILITY:
            return self._check_capability(kwargs.get("capability_name", ""))
        else:
            return DiagnosticResult(
                diagnostic_type=diagnostic_type,
                status=DiagnosticStatus.UNKNOWN,
                message=f"Unknown diagnostic type: {diagnostic_type}"
            )
    
    def run_all_diagnostics(self) -> List[DiagnosticResult]:
        """Run all diagnostics."""
        self._results = [
            self._check_memory(),
            self._check_cpu(),
            self._check_disk(),
            self._check_network(),
        ]
        self._last_check = datetime.utcnow()
        return self._results
    
    def _check_memory(self) -> DiagnosticResult:
        """Check memory usage."""
        import psutil
        memory = psutil.virtual_memory()
        status = DiagnosticStatus.HEALTHY
        if memory.percent > 90:
            status = DiagnosticStatus.UNHEALTHY
        elif memory.percent > 70:
            status = DiagnosticStatus.DEGRADED
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.MEMORY,
            status=status,
            message=f"Memory usage: {memory.percent:.1f}%",
            details={
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            }
        )
    
    def _check_cpu(self) -> DiagnosticResult:
        """Check CPU usage."""
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        status = DiagnosticStatus.HEALTHY
        if cpu_percent > 90:
            status = DiagnosticStatus.UNHEALTHY
        elif cpu_percent > 70:
            status = DiagnosticStatus.DEGRADED
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.CPU,
            status=status,
            message=f"CPU usage: {cpu_percent:.1f}%",
            details={"percent": cpu_percent}
        )
    
    def _check_disk(self) -> DiagnosticResult:
        """Check disk usage."""
        import psutil
        disk = psutil.disk_usage('/')
        status = DiagnosticStatus.HEALTHY
        if disk.percent > 95:
            status = DiagnosticStatus.UNHEALTHY
        elif disk.percent > 80:
            status = DiagnosticStatus.DEGRADED
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.DISK,
            status=status,
            message=f"Disk usage: {disk.percent:.1f}%",
            details={
                "total": disk.total,
                "free": disk.free,
                "percent": disk.percent
            }
        )
    
    def _check_network(self) -> DiagnosticResult:
        """Check network connectivity."""
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            status = DiagnosticStatus.HEALTHY
            message = "Network connectivity OK"
        except OSError:
            status = DiagnosticStatus.UNHEALTHY
            message = "Network connectivity FAILED"
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.NETWORK,
            status=status,
            message=message,
            details={}
        )
    
    def _check_module(self, module_name: str) -> DiagnosticResult:
        """Check if a module can be imported."""
        import importlib
        try:
            importlib.import_module(module_name)
            status = DiagnosticStatus.HEALTHY
            message = f"Module '{module_name}' loaded successfully"
        except ImportError:
            status = DiagnosticStatus.UNHEALTHY
            message = f"Module '{module_name}' not found"
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.MODULE,
            status=status,
            message=message,
            details={"module_name": module_name}
        )
    
    def _check_capability(self, capability_name: str) -> DiagnosticResult:
        """Check if a capability is registered."""
        from capabilities import CapabilityRegistry
        
        registry = CapabilityRegistry()
        capability = registry.get(capability_name)
        
        if capability:
            status = DiagnosticStatus.HEALTHY
            message = f"Capability '{capability_name}' is registered"
        else:
            status = DiagnosticStatus.DEGRADED
            message = f"Capability '{capability_name}' not found"
        
        return DiagnosticResult(
            diagnostic_type=DiagnosticType.CAPABILITY,
            status=status,
            message=message,
            details={"capability_name": capability_name}
        )
    
    def get_overall_status(self) -> DiagnosticStatus:
        """Get overall system status."""
        if not self._results:
            return DiagnosticStatus.UNKNOWN
        
        statuses = [r.status for r in self._results]
        
        if DiagnosticStatus.UNHEALTHY in statuses:
            return DiagnosticStatus.UNHEALTHY
        elif DiagnosticStatus.DEGRADED in statuses:
            return DiagnosticStatus.DEGRADED
        elif DiagnosticStatus.HEALTHY in statuses:
            return DiagnosticStatus.HEALTHY
        else:
            return DiagnosticStatus.UNKNOWN
