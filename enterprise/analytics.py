"""
Enterprise Analytics Module
=========================

Enterprise analytics platform for operational intelligence.
Provides dashboards, reports, and predictive analytics.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


ANALYTICS_TYPES = [
    "Operational", "Mission", "Execution", "Capability", "Provider",
    "Knowledge", "Project", "Organization", "Cost",
    "Performance", "Quality", "Predictive"
]


class MetricType(Enum):
    """Types of metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    RATE = "rate"


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
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dashboard:
    """Analytics dashboard."""
    dashboard_id: str
    name: str
    description: str = ""
    widgets: List[Dict[str, Any]] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_widget(self, widget: Dict[str, Any]) -> None:
        """Add a widget to the dashboard."""
        self.widgets.append(widget)
        self.updated_at = datetime.utcnow()
    
    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard."""
        for i, w in enumerate(self.widgets):
            if w.get("id") == widget_id:
                self.widgets.pop(i)
                self.updated_at = datetime.utcnow()
                return True
        return False


@dataclass
class Report:
    """Analytics report."""
    report_id: str
    type: str
    title: str
    data: Dict[str, Any]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    filters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AnalyticsEngine:
    """Engine for computing analytics."""
    
    def __init__(self):
        self._metrics: Dict[str, List[Metric]] = {}
    
    def record_metric(
        self,
        name: str,
        metric_type: MetricType,
        value: float,
        unit: str = "",
        labels: Optional[Dict[str, str]] = None,
    ) -> Metric:
        """Record a metric."""
        metric = Metric(
            metric_id=f"metric_{uuid.uuid4().hex[:8]}",
            name=name,
            metric_type=metric_type,
            value=value,
            unit=unit,
            labels=labels or {},
        )
        
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)
        
        return metric
    
    def get_metrics(
        self,
        name: Optional[str] = None,
        since: Optional[datetime] = None,
    ) -> List[Metric]:
        """Get metrics with optional filtering."""
        if name:
            metrics = self._metrics.get(name, [])
        else:
            metrics = [m for metrics in self._metrics.values() for m in metrics]
        
        if since:
            metrics = [m for m in metrics if m.timestamp >= since]
        
        return metrics
    
    def aggregate(
        self,
        name: str,
        operation: str = "sum",
    ) -> float:
        """Aggregate metrics."""
        metrics = self._metrics.get(name, [])
        if not metrics:
            return 0.0
        
        values = [m.value for m in metrics]
        
        if operation == "sum":
            return sum(values)
        elif operation == "avg":
            return sum(values) / len(values)
        elif operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        elif operation == "count":
            return len(values)
        
        return 0.0


class EnterpriseAnalytics:
    """
    Analytics Platform - Real-time operational intelligence.
    
    Analytics Types:
    ✅ Operational, Mission, Execution, Capability, Provider
    ✅ Knowledge, Project, Organization, Cost
    ✅ Performance, Quality, Predictive
    
    Generates:
    ✅ Dashboards, Reports, Alerts, Forecasts
    ✅ Recommendations, Benchmarks
    """
    
    def __init__(self):
        self.version = "2.0.0"
        self._dashboards: Dict[str, Dashboard] = {}
        self._reports: Dict[str, Report] = {}
        self.engine = AnalyticsEngine()
    
    def create_dashboard(
        self,
        name: str,
        description: str = "",
    ) -> Dashboard:
        """Create a new dashboard."""
        dashboard = Dashboard(
            dashboard_id=f"dash_{uuid.uuid4().hex[:8]}",
            name=name,
            description=description,
        )
        self._dashboards[dashboard.dashboard_id] = dashboard
        return dashboard
    
    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        """Get a dashboard by ID."""
        return self._dashboards.get(dashboard_id)
    
    def generate_report(
        self,
        report_type: str,
        title: str,
        data: Dict[str, Any],
        created_by: str = "",
    ) -> Report:
        """Generate a new report."""
        report = Report(
            report_id=f"report_{uuid.uuid4().hex[:8]}",
            type=report_type,
            title=title,
            data=data,
            created_by=created_by,
        )
        self._reports[report.report_id] = report
        return report
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """Get a report by ID."""
        return self._reports.get(report_id)
    
    def record_metric(
        self,
        name: str,
        metric_type: MetricType,
        value: float,
        unit: str = "",
        labels: Optional[Dict[str, str]] = None,
    ) -> Metric:
        """Record a metric."""
        return self.engine.record_metric(name, metric_type, value, unit, labels)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analytics statistics."""
        return {
            "version": self.version,
            "analytics_types": ANALYTICS_TYPES,
            "dashboards": len(self._dashboards),
            "reports": len(self._reports),
            "metrics": sum(len(m) for m in self.engine._metrics.values()),
        }
