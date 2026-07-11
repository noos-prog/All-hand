"""AGOS Engineering Observatory - Real-time monitoring and dashboards."""
from .dashboard import (
    ObservatoryDashboard, Dashboard, DashboardType, DashboardWidget,
    Metric, MetricType, Alert, AlertSeverity, AlertStatus,
    TimeSeries, HealthScore, SystemMetrics, AgentMetrics
)
from .metrics import (
    MetricsCollector, MetricsAggregator, MetricsAnalyzer,
    RealTimeMetrics, HistoricalMetrics
)
from .alerts import (
    AlertManager, AlertRule, AlertChannel, AlertNotification,
    AlertEscalation
)

__all__ = [
    "ObservatoryDashboard", "Dashboard", "DashboardType", "DashboardWidget",
    "Metric", "MetricType", "Alert", "AlertSeverity", "AlertStatus",
    "TimeSeries", "HealthScore", "SystemMetrics", "AgentMetrics",
    "MetricsCollector", "MetricsAggregator", "MetricsAnalyzer",
    "RealTimeMetrics", "HistoricalMetrics",
    "AlertManager", "AlertRule", "AlertChannel", "AlertNotification",
    "AlertEscalation",
]

__version__ = "1.0.0"
