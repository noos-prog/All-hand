"""
AGOS Workflow Monitor
====================

Workflow execution monitoring and health tracking.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import threading


class HealthStatus(Enum):
    """Health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class MonitorConfig:
    """Monitor configuration."""
    check_interval: float = 60.0  # seconds
    alert_threshold: float = 0.8  # 80% failure rate triggers alert
    retention_hours: int = 24  # Keep history for 24 hours


@dataclass
class ExecutionRecord:
    """Record of an execution."""
    id: str
    pipeline_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0
    step_results: Dict[str, str] = field(default_factory=dict)
    error: Optional[str] = None


class Monitor:
    """
    Workflow Execution Monitor.
    
    Monitors workflow executions and tracks health:
    - Execution history
    - Health status
    - Performance metrics
    - Alerting
    
    Usage:
        monitor = Monitor(config=MonitorConfig(check_interval=30))
        monitor.start()
        
        # Record an execution
        monitor.record_execution(
            pipeline_id="my-pipeline",
            status="completed",
            duration_ms=1500,
        )
        
        # Get health status
        health = monitor.get_health()
        print(f"System health: {health}")
        
        monitor.stop()
    """
    
    def __init__(self, config: Optional[MonitorConfig] = None):
        """Initialize monitor."""
        self.config = config or MonitorConfig()
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Execution history
        self._executions: Dict[str, ExecutionRecord] = {}
        self._execution_order: List[str] = []
        
        # Health metrics
        self._health_checks: Dict[str, bool] = {}
        self._last_health_check: Optional[datetime] = None
        
        # Callbacks
        self._health_callbacks: List[Callable[[HealthStatus], None]] = []
    
    def start(self) -> None:
        """Start the monitor."""
        if self._running:
            return
        
        self._running = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self._monitor_thread.start()
    
    def stop(self) -> None:
        """Stop the monitor."""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        import time
        while self._running:
            try:
                self._check_health()
            except Exception:
                pass
            time.sleep(self.config.check_interval)
    
    def _check_health(self) -> None:
        """Check system health."""
        health = self._calculate_health()
        self._last_health_check = datetime.utcnow()
        
        # Trigger callbacks
        for callback in self._health_callbacks:
            try:
                callback(health)
            except Exception:
                pass
    
    def _calculate_health(self) -> HealthStatus:
        """Calculate health status."""
        with self._lock:
            # Clean old executions
            self._cleanup_old_executions()
            
            # Get recent executions
            recent = self._get_recent_executions()
            
            if not recent:
                return HealthStatus.UNKNOWN
            
            # Calculate failure rate
            failed = sum(1 for e in recent if e.status == "failed")
            total = len(recent)
            failure_rate = failed / total if total > 0 else 0
            
            # Determine health
            if failure_rate >= self.config.alert_threshold:
                return HealthStatus.UNHEALTHY
            elif failure_rate > 0.1:  # >10% failure rate
                return HealthStatus.DEGRADED
            else:
                return HealthStatus.HEALTHY
    
    def _cleanup_old_executions(self) -> None:
        """Remove old execution records."""
        cutoff = datetime.utcnow() - timedelta(hours=self.config.retention_hours)
        
        to_remove = [
            exec_id for exec_id, record in self._executions.items()
            if record.completed_at and record.completed_at < cutoff
        ]
        
        for exec_id in to_remove:
            del self._executions[exec_id]
            if exec_id in self._execution_order:
                self._execution_order.remove(exec_id)
    
    def _get_recent_executions(self, hours: int = 1) -> List[ExecutionRecord]:
        """Get recent executions."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = []
        
        for record in self._executions.values():
            if record.started_at >= cutoff:
                recent.append(record)
        
        return recent
    
    def record_execution(
        self,
        pipeline_id: str,
        status: str,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        duration_ms: float = 0.0,
        step_results: Optional[Dict[str, str]] = None,
        error: Optional[str] = None,
    ) -> str:
        """
        Record an execution.
        
        Returns:
            Execution ID
        """
        exec_id = f"exec-{uuid.uuid4().hex[:8]}"
        
        record = ExecutionRecord(
            id=exec_id,
            pipeline_id=pipeline_id,
            status=status,
            started_at=started_at or datetime.utcnow(),
            completed_at=completed_at,
            duration_ms=duration_ms,
            step_results=step_results or {},
            error=error,
        )
        
        with self._lock:
            self._executions[exec_id] = record
            self._execution_order.append(exec_id)
        
        return exec_id
    
    def get_execution(self, execution_id: str) -> Optional[ExecutionRecord]:
        """Get an execution record."""
        with self._lock:
            return self._executions.get(execution_id)
    
    def list_executions(
        self,
        pipeline_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[ExecutionRecord]:
        """List executions."""
        with self._lock:
            executions = list(self._executions.values())
        
        if pipeline_id:
            executions = [e for e in executions if e.pipeline_id == pipeline_id]
        
        if status:
            executions = [e for e in executions if e.status == status]
        
        # Sort by start time (most recent first)
        executions.sort(key=lambda e: e.started_at, reverse=True)
        
        return executions[:limit]
    
    def get_health(self) -> HealthStatus:
        """Get current health status."""
        return self._calculate_health()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get monitoring metrics."""
        with self._lock:
            recent = self._get_recent_executions(hours=1)
            recent_24h = self._get_recent_executions(hours=24)
            
            return {
                "health_status": self._calculate_health().value,
                "last_check": self._last_health_check.isoformat() if self._last_health_check else None,
                "metrics_1h": {
                    "total": len(recent),
                    "completed": sum(1 for e in recent if e.status == "completed"),
                    "failed": sum(1 for e in recent if e.status == "failed"),
                    "avg_duration_ms": (
                        sum(e.duration_ms for e in recent) / len(recent)
                        if recent else 0
                    ),
                },
                "metrics_24h": {
                    "total": len(recent_24h),
                    "completed": sum(1 for e in recent_24h if e.status == "completed"),
                    "failed": sum(1 for e in recent_24h if e.status == "failed"),
                },
                "total_recorded": len(self._executions),
            }
    
    def on_health_change(self, callback: Callable[[HealthStatus], None]) -> None:
        """Register a health change callback."""
        self._health_callbacks.append(callback)
    
    def get_pipeline_stats(self, pipeline_id: str) -> Dict[str, Any]:
        """Get statistics for a specific pipeline."""
        executions = self.list_executions(pipeline_id=pipeline_id, limit=1000)
        
        if not executions:
            return {
                "pipeline_id": pipeline_id,
                "total_executions": 0,
            }
        
        completed = [e for e in executions if e.status == "completed"]
        failed = [e for e in executions if e.status == "failed"]
        
        return {
            "pipeline_id": pipeline_id,
            "total_executions": len(executions),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": len(completed) / len(executions) if executions else 0,
            "avg_duration_ms": (
                sum(e.duration_ms for e in executions) / len(executions)
                if executions else 0
            ),
        }


# Global monitor instance
_monitor: Optional[Monitor] = None


def get_monitor() -> Monitor:
    """Get the global monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = Monitor()
    return _monitor
