"""
Universal Telemetry Runtime
PHASE-02: EXECUTION-000011 - Universal Telemetry Runtime

Every engineering action must be observable.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
import time


class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class Metric:
    """Telemetry metric."""
    metric_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    metric_type: MetricType = MetricType.GAUGE
    value: float = 0.0
    unit: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    labels: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'metric_id': self.metric_id,
            'name': self.name,
            'metric_type': self.metric_type.value if isinstance(self.metric_type, MetricType) else self.metric_type,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp,
            'labels': self.labels,
        }


@dataclass
class Trace:
    """Distributed trace."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = ""
    parent_span_id: str = ""
    operation_name: str = ""
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: str = ""
    duration_ms: float = 0.0
    status: str = "ok"
    annotations: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'trace_id': self.trace_id,
            'span_id': self.span_id,
            'parent_span_id': self.parent_span_id,
            'operation_name': self.operation_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_ms': self.duration_ms,
            'status': self.status,
            'annotations': self.annotations,
        }


@dataclass
class LogEntry:
    """Log entry."""
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    level: str = "INFO"  # DEBUG, INFO, WARN, ERROR
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'log_id': self.log_id,
            'level': self.level,
            'message': self.message,
            'timestamp': self.timestamp,
            'source': self.source,
            'context': self.context,
        }


@dataclass
class HealthReport:
    """Health report."""
    component: str = ""
    status: str = "healthy"  # healthy, degraded, unhealthy
    checks: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MetricsRuntime:
    """Metrics collection runtime."""
    
    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
    
    def record(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, unit: str = "", labels: Dict = None) -> Metric:
        """Record a metric."""
        metric = Metric(name=name, value=value, metric_type=metric_type, unit=unit, labels=labels or {})
        
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)
        
        return metric
    
    def get_metrics(self, name: str = "") -> List[Metric]:
        """Get metrics."""
        if name:
            return self.metrics.get(name, [])
        all_metrics = []
        for m_list in self.metrics.values():
            all_metrics.extend(m_list)
        return all_metrics


class TracingRuntime:
    """Distributed tracing runtime."""
    
    def __init__(self):
        self.traces: Dict[str, Trace] = {}
    
    def start_span(self, operation_name: str, parent_span_id: str = "") -> Trace:
        """Start a trace span."""
        trace = Trace(
            span_id=str(uuid.uuid4())[:16],
            parent_span_id=parent_span_id,
            operation_name=operation_name
        )
        self.traces[trace.trace_id] = trace
        return trace
    
    def end_span(self, trace: Trace, status: str = "ok") -> None:
        """End a trace span."""
        trace.end_time = datetime.utcnow().isoformat()
        trace.status = status
        trace.duration_ms = (time.time() - datetime.fromisoformat(trace.start_time).timestamp()) * 1000
    
    def get_traces(self, trace_id: str = "") -> List[Trace]:
        """Get traces."""
        if trace_id:
            return [self.traces.get(trace_id)] if trace_id in self.traces else []
        return list(self.traces.values())


class LoggingRuntime:
    """Logging runtime."""
    
    def __init__(self):
        self.logs: List[LogEntry] = []
    
    def log(self, level: str, message: str, source: str = "", context: Dict = None) -> LogEntry:
        """Log an entry."""
        entry = LogEntry(level=level, message=message, source=source, context=context or {})
        self.logs.append(entry)
        return entry
    
    def get_logs(self, level: str = "", limit: int = 100) -> List[LogEntry]:
        """Get logs."""
        logs = self.logs
        if level:
            logs = [l for l in logs if l.level == level]
        return logs[-limit:]


class HealthRuntime:
    """Health monitoring runtime."""
    
    def __init__(self):
        self.reports: Dict[str, HealthReport] = {}
    
    def report(self, component: str, status: str, checks: List[Dict]) -> HealthReport:
        """Report health."""
        report = HealthReport(component=component, status=status, checks=checks)
        self.reports[component] = report
        return report
    
    def get_health(self, component: str = "") -> Dict:
        """Get health status."""
        if component:
            return self.reports.get(component, HealthReport()).__dict__
        
        # Aggregate health
        all_healthy = all(r.status == "healthy" for r in self.reports.values())
        return {
            'overall_status': 'healthy' if all_healthy else 'degraded',
            'components': {k: v.__dict__ for k, v in self.reports.items()}
        }


class ExecutionTimelineRuntime:
    """Execution timeline runtime."""
    
    def __init__(self):
        self.events: List[Dict] = []
    
    def record_event(self, event_type: str, mission_id: str, details: Dict) -> None:
        """Record an execution event."""
        self.events.append({
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'mission_id': mission_id,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details
        })
    
    def get_timeline(self, mission_id: str = "") -> List[Dict]:
        """Get execution timeline."""
        if mission_id:
            return [e for e in self.events if e['mission_id'] == mission_id]
        return self.events


class TelemetryRuntime:
    """
    Universal Telemetry Runtime.
    
    Every engineering action must be observable.
    
    Mission Metrics:
    - Mission Duration
    - Task Duration
    - Capability Duration
    - Provider Duration
    - Queue Time
    - Wait Time
    - Retry Count
    - Failure Count
    - Recovery Count
    - Memory Usage
    - CPU Usage
    - Network Usage
    - Storage Usage
    
    Output:
    - Metrics
    - Traces
    - Logs
    - Execution Timeline
    - Health Reports
    - Performance Reports
    
    Rules:
    - Telemetry is automatic
    - Telemetry cannot be disabled for Core Runtime
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.metrics = MetricsRuntime()
        self.tracing = TracingRuntime()
        self.logging = LoggingRuntime()
        self.health = HealthRuntime()
        self.timeline = ExecutionTimelineRuntime()
    
    def record_metric(self, name: str, value: float, unit: str = "", labels: Dict = None) -> Metric:
        """Record a metric."""
        return self.metrics.record(name, value, unit=unit, labels=labels)
    
    def start_trace(self, operation_name: str, parent_span_id: str = "") -> Trace:
        """Start a trace."""
        return self.tracing.start_span(operation_name, parent_span_id)
    
    def end_trace(self, trace: Trace, status: str = "ok") -> None:
        """End a trace."""
        self.tracing.end_span(trace, status)
    
    def log(self, level: str, message: str, source: str = "", context: Dict = None) -> LogEntry:
        """Log an entry."""
        return self.logging.log(level, message, source, context)
    
    def report_health(self, component: str, status: str, checks: List[Dict]) -> HealthReport:
        """Report health."""
        return self.health.report(component, status, checks)
    
    def record_mission_metric(self, mission_id: str, metric_name: str, value: float, unit: str = "") -> Metric:
        """Record mission-specific metric."""
        return self.record_metric(
            f"mission.{metric_name}",
            value,
            unit,
            labels={'mission_id': mission_id}
        )
    
    def record_execution_event(self, event_type: str, mission_id: str, details: Dict) -> None:
        """Record execution event."""
        self.timeline.record_event(event_type, mission_id, details)
    
    def get_telemetry_summary(self) -> Dict:
        """Get telemetry summary."""
        return {
            'metrics_count': len(self.metrics.get_metrics()),
            'traces_count': len(self.tracing.get_traces()),
            'logs_count': len(self.logging.get_logs()),
            'health_reports': list(self.health.reports.keys()),
            'timeline_events': len(self.timeline.get_timeline()),
        }