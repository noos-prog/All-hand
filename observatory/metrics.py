"""Metrics Collection and Analysis - Real-time metrics pipeline."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import uuid


class AggregationType(Enum):
    """Types of metric aggregation."""
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    P50 = "p50"
    P90 = "p90"
    P99 = "p99"


@dataclass
class RealTimeMetrics:
    """Real-time metrics snapshot."""
    snapshot_id: str
    timestamp: datetime
    metrics: Dict[str, float] = field(default_factory=dict)
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class HistoricalMetrics:
    """Historical metrics data."""
    metric_name: str
    start_time: datetime
    end_time: datetime
    data_points: List[RealTimeMetrics] = field(default_factory=list)
    
    def get_duration(self) -> timedelta:
        return self.end_time - self.start_time
    
    def get_count(self) -> int:
        return len(self.data_points)


class MetricsCollector:
    """Collects metrics from various sources."""
    
    def __init__(self):
        self._collectors: Dict[str, Callable] = {}
        self._metrics_buffer: List[RealTimeMetrics] = []
    
    def register_collector(self, name: str, collector: Callable) -> None:
        self._collectors[name] = collector
    
    def collect(self) -> RealTimeMetrics:
        snapshot = RealTimeMetrics(
            snapshot_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            metrics={},
        )
        
        for name, collector in self._collectors.items():
            try:
                snapshot.metrics[name] = collector()
            except:
                snapshot.metrics[name] = 0.0
        
        self._metrics_buffer.append(snapshot)
        return snapshot
    
    def collect_all(self) -> List[RealTimeMetrics]:
        return [self.collect()]


class MetricsAggregator:
    """Aggregates metrics over time periods."""
    
    def __init__(self):
        self._aggregations: Dict[str, List[RealTimeMetrics]] = {}
    
    def add_metric(self, metric_name: str, snapshot: RealTimeMetrics) -> None:
        if metric_name not in self._aggregations:
            self._aggregations[metric_name] = []
        self._aggregations[metric_name].append(snapshot)
    
    def aggregate(
        self,
        metric_name: str,
        aggregation: AggregationType,
        duration: timedelta,
    ) -> float:
        snapshots = self._aggregations.get(metric_name, [])
        cutoff = datetime.utcnow() - duration
        recent = [s for s in snapshots if s.timestamp >= cutoff]
        
        if not recent:
            return 0.0
        
        values = [s.metrics.get(metric_name, 0.0) for s in recent]
        
        if aggregation == AggregationType.SUM:
            return sum(values)
        elif aggregation == AggregationType.AVG:
            return sum(values) / len(values)
        elif aggregation == AggregationType.MIN:
            return min(values)
        elif aggregation == AggregationType.MAX:
            return max(values)
        elif aggregation == AggregationType.COUNT:
            return float(len(values))
        
        return 0.0


class MetricsAnalyzer:
    """Analyzes metrics for anomalies and trends."""
    
    def __init__(self):
        self._thresholds: Dict[str, float] = {}
        self._anomalies: List[Dict[str, Any]] = []
    
    def set_threshold(self, metric_name: str, threshold: float) -> None:
        self._thresholds[metric_name] = threshold
    
    def detect_anomaly(self, metric_name: str, value: float) -> bool:
        threshold = self._thresholds.get(metric_name)
        if threshold is not None and value > threshold:
            self._anomalies.append({
                "metric": metric_name,
                "value": value,
                "threshold": threshold,
                "timestamp": datetime.utcnow().isoformat(),
            })
            return True
        return False
    
    def get_anomalies(self) -> List[Dict[str, Any]]:
        return self._anomalies
    
    def clear_anomalies(self) -> None:
        self._anomalies = []
