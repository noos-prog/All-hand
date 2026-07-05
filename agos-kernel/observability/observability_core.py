"""Runtime Observability - Structured logging, metrics, tracing, and health checks."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Structured log entry."""
    id: str
    level: LogLevel
    message: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    mission_id: Optional[str] = None
    execution_id: Optional[str] = None
    
    @classmethod
    def create(cls, level: LogLevel, message: str, **context) -> "LogEntry":
        return cls(
            id=str(uuid4()),
            level=level,
            message=message,
            timestamp=datetime.utcnow(),
            context=context
        )


class StructuredLogger:
    """Structured logging."""
    
    def __init__(self):
        self._logs: List[LogEntry] = []
        self._max_logs = 10000
    
    def log(self, level: LogLevel, message: str, **context) -> LogEntry:
        entry = LogEntry.create(level, message, **context)
        self._logs.append(entry)
        if len(self._logs) > self._max_logs:
            self._logs = self._logs[-self._max_logs:]
        return entry
    
    def debug(self, message: str, **context) -> LogEntry:
        return self.log(LogLevel.DEBUG, message, **context)
    
    def info(self, message: str, **context) -> LogEntry:
        return self.log(LogLevel.INFO, message, **context)
    
    def warning(self, message: str, **context) -> LogEntry:
        return self.log(LogLevel.WARNING, message, **context)
    
    def error(self, message: str, **context) -> LogEntry:
        return self.log(LogLevel.ERROR, message, **context)
    
    def critical(self, message: str, **context) -> LogEntry:
        return self.log(LogLevel.CRITICAL, message, **context)
    
    def get_logs(self, level: LogLevel = None, limit: int = 100) -> List[LogEntry]:
        logs = self._logs
        if level:
            logs = [l for l in logs if l.level == level]
        return logs[-limit:]


@dataclass
class Metric:
    """Metric data point."""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collects metrics."""
    
    def __init__(self):
        self._metrics: Dict[str, List[Metric]] = {}
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
    
    def record(self, name: str, value: float, **labels) -> Metric:
        metric = Metric(name=name, value=value, timestamp=datetime.utcnow(), labels=labels)
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)
        return metric
    
    def increment(self, name: str, value: float = 1.0) -> None:
        self._counters[name] = self._counters.get(name, 0) + value
        self.record(name, self._counters[name])
    
    def gauge(self, name: str, value: float) -> None:
        self._gauges[name] = value
        self.record(name, value)
    
    def get_counter(self, name: str) -> float:
        return self._counters.get(name, 0)
    
    def get_gauge(self, name: str) -> float:
        return self._gauges.get(name, 0)
    
    def get_metrics(self, name: str = None) -> List[Metric]:
        if name:
            return self._metrics.get(name, [])
        return [m for metrics in self._metrics.values() for m in metrics]


class SpanStatus(Enum):
    STARTED = "started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Span:
    span_id: str
    name: str
    trace_id: str
    parent_id: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: SpanStatus = SpanStatus.STARTED
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    def end(self, status: SpanStatus = SpanStatus.COMPLETED) -> None:
        self.completed_at = datetime.utcnow()
        self.status = status
    
    def duration_ms(self) -> float:
        if not self.completed_at:
            return 0
        return (self.completed_at - self.started_at).total_seconds() * 1000


class Tracer:
    def __init__(self):
        self._spans: Dict[str, Span] = {}
        self._traces: Dict[str, List[Span]] = {}
    
    def start_span(self, name: str, trace_id: str = None, parent_id: str = None) -> Span:
        trace_id = trace_id or str(uuid4())
        span_id = str(uuid4())
        span = Span(span_id=span_id, name=name, trace_id=trace_id, parent_id=parent_id, started_at=datetime.utcnow())
        self._spans[span_id] = span
        if trace_id not in self._traces:
            self._traces[trace_id] = []
        self._traces[trace_id].append(span)
        return span
    
    def end_span(self, span_id: str, status: SpanStatus = SpanStatus.COMPLETED) -> None:
        if span_id in self._spans:
            self._spans[span_id].end(status)
    
    def add_event(self, span_id: str, name: str, **attributes) -> None:
        if span_id in self._spans:
            self._spans[span_id].events.append({"name": name, "timestamp": datetime.utcnow().isoformat(), "attributes": attributes})
    
    def get_trace(self, trace_id: str) -> List[Span]:
        return self._traces.get(trace_id, [])
    
    def get_span(self, span_id: str) -> Optional[Span]:
        return self._spans.get(span_id)


@dataclass
class TimelineEvent:
    event_id: str
    name: str
    timestamp: datetime
    duration_ms: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionTimeline:
    def __init__(self, mission_id: str):
        self.mission_id = mission_id
        self.events: List[TimelineEvent] = []
    
    def add_event(self, name: str, duration_ms: float = 0, **metadata) -> TimelineEvent:
        event = TimelineEvent(event_id=str(uuid4()), name=name, timestamp=datetime.utcnow(), duration_ms=duration_ms, metadata=metadata)
        self.events.append(event)
        return event
    
    def get_duration_ms(self) -> float:
        return sum(e.duration_ms for e in self.events)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"mission_id": self.mission_id, "total_duration_ms": self.get_duration_ms()}


@dataclass
class PerformanceSnapshot:
    timestamp: datetime
    mission_duration_ms_avg: float = 0
    failure_rate: float = 0
    success_rate: float = 0
    total_missions: int = 0


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


class RuntimeObservability:
    def __init__(self):
        self.logger = StructuredLogger()
        self.metrics = MetricsCollector()
        self.tracer = Tracer()
    
    def record_mission_duration(self, duration_ms: float) -> None:
        self.metrics.record("mission_duration_ms", duration_ms, type="mission")
    
    def record_success(self) -> None:
        self.metrics.increment("mission_success_total")
        self.metrics.increment("mission_total")
    
    def record_failure(self) -> None:
        self.metrics.increment("mission_failure_total")
        self.metrics.increment("mission_total")
    
    def get_health_report(self, checks: List[HealthCheck] = None) -> Dict[str, Any]:
        overall = HealthStatus.HEALTHY
        if checks:
            for check in checks:
                if check.status == HealthStatus.UNHEALTHY:
                    overall = HealthStatus.UNHEALTHY
                    break
                elif check.status == HealthStatus.DEGRADED:
                    overall = HealthStatus.DEGRADED
        return {"status": overall.value, "timestamp": datetime.utcnow().isoformat()}
    
    def create_timeline(self, mission_id: str) -> ExecutionTimeline:
        return ExecutionTimeline(mission_id)


_logger = StructuredLogger()
_metrics = MetricsCollector()
_tracer = Tracer()
_runtime = RuntimeObservability()


def get_logger() -> StructuredLogger:
    return _logger


def get_metrics() -> MetricsCollector:
    return _metrics


def get_tracer() -> Tracer:
    return _tracer


def get_runtime_observability() -> RuntimeObservability:
    return _runtime
