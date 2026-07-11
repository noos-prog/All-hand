"""Engineering Observatory Dashboard - Real-time monitoring dashboards."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import uuid

DASHBOARD_TYPES = [
    "System Health", "Architecture", "Knowledge", "Mission",
    "Capability", "Provider", "Performance", "Reliability", "Security"
]


class DashboardType(Enum):
    """Types of dashboards."""
    SYSTEM_HEALTH = "system_health"
    ARCHITECTURE = "architecture"
    KNOWLEDGE = "knowledge"
    MISSION = "mission"
    CAPABILITY = "capability"
    PROVIDER = "provider"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    SECURITY = "security"


class MetricType(Enum):
    """Types of metrics."""
    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    RATE = "rate"


class AlertSeverity(Enum):
    """Alert severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    """Alert status."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


@dataclass
class Metric:
    """A metric data point."""
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    unit: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TimeSeries:
    """Time series data."""
    series_id: str
    name: str
    data_points: List[Metric] = field(default_factory=list)
    aggregation: str = "avg"
    
    def add_point(self, value: float, timestamp: Optional[datetime] = None) -> None:
        metric = Metric(
            metric_id=str(uuid.uuid4()),
            name=self.name,
            metric_type=MetricType.GAUGE,
            value=value,
            timestamp=timestamp or datetime.utcnow(),
        )
        self.data_points.append(metric)
    
    def get_latest(self) -> Optional[float]:
        if self.data_points:
            return self.data_points[-1].value
        return None
    
    def get_average(self, duration: timedelta = timedelta(hours=1)) -> float:
        cutoff = datetime.utcnow() - duration
        recent = [m.value for m in self.data_points if m.timestamp >= cutoff]
        return sum(recent) / len(recent) if recent else 0.0


@dataclass
class HealthScore:
    """Overall health score."""
    score_id: str
    component: str
    score: float
    status: str
    factors: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    total_agents: int = 0
    active_agents: int = 0
    total_missions: int = 0
    completed_missions: int = 0
    failed_missions: int = 0
    avg_response_time_ms: float = 0.0
    cpu_usage_percent: float = 0.0
    memory_usage_percent: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AgentMetrics:
    """Per-agent metrics."""
    agent_id: str
    name: str
    status: str
    missions_completed: int = 0
    missions_failed: int = 0
    avg_execution_time_ms: float = 0.0
    last_active: Optional[datetime] = None


@dataclass
class DashboardWidget:
    """A widget in a dashboard."""
    widget_id: str
    widget_type: str
    title: str
    metrics: List[str] = field(default_factory=list)
    refresh_interval_seconds: int = 60
    position: Dict[str, int] = field(default_factory=dict)


@dataclass
class Dashboard:
    """A complete dashboard."""
    dashboard_id: str
    name: str
    dashboard_type: DashboardType
    widgets: List[DashboardWidget] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    is_public: bool = False
    owner_id: Optional[str] = None


@dataclass
class Alert:
    """An alert notification."""
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    source: str
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class ObservatoryDashboard:
    """
    Engineering Observatory Dashboard.
    
    Implements:
    ✅ System Health Dashboard
    ✅ Architecture Dashboard
    ✅ Knowledge Dashboard
    ✅ Mission Dashboard
    ✅ Capability Dashboard
    ✅ Provider Dashboard
    ✅ Performance Dashboard
    ✅ Reliability Dashboard
    ✅ Security Dashboard
    
    EVERY METRIC MUST BE REALTIME.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.dashboards: Dict[str, Dashboard] = {}
        self.time_series: Dict[str, TimeSeries] = {}
        self.alerts: Dict[str, Alert] = {}
        self.health_scores: Dict[str, HealthScore] = {}
        self._setup_default_dashboards()
    
    def _setup_default_dashboards(self) -> None:
        """Set up default dashboards."""
        for dash_type in DashboardType:
            dashboard = Dashboard(
                dashboard_id=str(uuid.uuid4()),
                name=f"{dash_type.value.replace('_', ' ').title()} Dashboard",
                dashboard_type=dash_type,
            )
            self.dashboards[dash_type.value] = dashboard
    
    def create_dashboard(self, name: str, dashboard_type: DashboardType) -> Dashboard:
        dashboard = Dashboard(
            dashboard_id=str(uuid.uuid4()),
            name=name,
            dashboard_type=dashboard_type,
        )
        self.dashboards[dashboard.dashboard_id] = dashboard
        return dashboard
    
    def add_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> Metric:
        if name not in self.time_series:
            self.time_series[name] = TimeSeries(
                series_id=str(uuid.uuid4()),
                name=name,
            )
        
        self.time_series[name].add_point(value)
        
        return Metric(
            metric_id=str(uuid.uuid4()),
            name=name,
            metric_type=MetricType.GAUGE,
            value=value,
            labels=labels or {},
        )
    
    def create_alert(
        self,
        title: str,
        description: str,
        severity: AlertSeverity,
        source: str,
    ) -> Alert:
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            title=title,
            description=description,
            severity=severity,
            status=AlertStatus.ACTIVE,
            source=source,
        )
        self.alerts[alert.alert_id] = alert
        return alert
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        alert = self.alerts.get(alert_id)
        if alert:
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_at = datetime.utcnow()
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        alert = self.alerts.get(alert_id)
        if alert:
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.utcnow()
            return True
        return False
    
    def get_active_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Alert]:
        alerts = [a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return alerts
    
    def update_health_score(self, component: str, score: float, factors: Dict[str, float]) -> HealthScore:
        health = HealthScore(
            score_id=str(uuid.uuid4()),
            component=component,
            score=score,
            status="healthy" if score >= 0.8 else "degraded" if score >= 0.5 else "critical",
            factors=factors,
        )
        self.health_scores[component] = health
        return health
    
    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        return self.dashboards.get(dashboard_id)
    
    def get_metric(self, metric_name: str, duration: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        series = self.time_series.get(metric_name)
        if series:
            return {
                "name": metric_name,
                "latest": series.get_latest(),
                "average": series.get_average(duration),
                "data_points": len(series.data_points),
            }
        return {"name": metric_name, "latest": None, "average": 0.0, "data_points": 0}
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "dashboards": len(self.dashboards),
            "metrics": len(self.time_series),
            "active_alerts": len(self.get_active_alerts()),
            "health_scores": len(self.health_scores),
        }
