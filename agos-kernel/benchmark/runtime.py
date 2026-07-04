"""Universal Benchmark Platform."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class BenchmarkType(Enum):
    """Benchmark type."""
    CAPABILITY = "capability"
    PROVIDER = "provider"
    AGENT = "agent"
    MODEL = "model"
    TOOL = "tool"
    STRATEGY = "strategy"
    ARCHITECTURE = "architecture"
    REPOSITORY = "repository"
    WORKFLOW = "workflow"
    POLICY = "policy"


@dataclass
class BenchmarkMetric:
    """Benchmark metric."""
    name: str
    value: float
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BenchmarkResult:
    """Benchmark result."""
    id: str
    name: str
    benchmark_type: BenchmarkType
    metrics: Dict[str, BenchmarkMetric] = field(default_factory=dict)
    
    # Summary
    latency_ms: float = 0.0
    cost: float = 0.0
    accuracy: float = 0.0
    reliability: float = 0.0
    quality: float = 0.0
    scalability: float = 0.0
    success_rate: float = 0.0
    
    # Score
    overall_score: float = 0.0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BenchmarkPlatform:
    """Universal Benchmark Platform."""
    
    def __init__(self):
        """Initialize benchmark platform."""
        self.benchmarks: Dict[str, BenchmarkResult] = {}
        self.history: List[BenchmarkResult] = []
    
    def run_benchmark(
        self,
        name: str,
        benchmark_type: BenchmarkType,
        metrics: Optional[Dict[str, Any]] = None,
    ) -> BenchmarkResult:
        """Run a benchmark."""
        bench_id = self._generate_id(name)
        
        result = BenchmarkResult(
            id=bench_id,
            name=name,
            benchmark_type=benchmark_type,
        )
        
        # Set metrics from input
        if metrics:
            if "latency_ms" in metrics:
                result.latency_ms = metrics["latency_ms"]
            if "cost" in metrics:
                result.cost = metrics["cost"]
            if "accuracy" in metrics:
                result.accuracy = metrics["accuracy"]
            if "reliability" in metrics:
                result.reliability = metrics["reliability"]
            if "quality" in metrics:
                result.quality = metrics["quality"]
            if "scalability" in metrics:
                result.scalability = metrics["scalability"]
            if "success_rate" in metrics:
                result.success_rate = metrics["success_rate"]
        
        # Calculate overall score
        scores = [
            result.latency_ms / 1000,  # Normalize latency
            result.accuracy,
            result.reliability,
            result.quality,
            result.scalability,
            result.success_rate,
        ]
        result.overall_score = sum(scores) / len(scores) if scores else 0
        
        self.benchmarks[bench_id] = result
        return result
    
    def add_metric(self, bench_id: str, metric: BenchmarkMetric) -> bool:
        """Add metric to benchmark."""
        bench = self.benchmarks.get(bench_id)
        if not bench:
            return False
        
        bench.metrics[metric.name] = metric
        
        # Update specific metrics
        if metric.name == "latency_ms":
            bench.latency_ms = metric.value
        elif metric.name == "cost":
            bench.cost = metric.value
        elif metric.name == "accuracy":
            bench.accuracy = metric.value
        elif metric.name == "reliability":
            bench.reliability = metric.value
        elif metric.name == "quality":
            bench.quality = metric.value
        
        # Recalculate overall score
        self._recalculate_score(bench)
        
        return True
    
    def compare(self, bench_ids: List[str]) -> Dict[str, Any]:
        """Compare benchmark results."""
        benches = [self.benchmarks.get(bid) for bid in bench_ids]
        benches = [b for b in benches if b]
        
        if not benches:
            return {"error": "No valid benchmarks found"}
        
        # Find best in each category
        return {
            "benchmarks": [
                {
                    "id": b.id,
                    "name": b.name,
                    "overall_score": b.overall_score,
                    "latency_ms": b.latency_ms,
                    "cost": b.cost,
                    "accuracy": b.accuracy,
                }
                for b in benches
            ],
            "best_latency": min(benches, key=lambda x: x.latency_ms).name,
            "best_cost": min(benches, key=lambda x: x.cost).name,
            "best_accuracy": max(benches, key=lambda x: x.accuracy).name,
            "best_overall": max(benches, key=lambda x: x.overall_score).name,
        }
    
    def get_benchmark(self, bench_id: str) -> Optional[BenchmarkResult]:
        """Get benchmark by ID."""
        return self.benchmarks.get(bench_id)
    
    def list_benchmarks(
        self,
        benchmark_type: Optional[BenchmarkType] = None,
        limit: int = 100,
    ) -> List[BenchmarkResult]:
        """List benchmarks."""
        results = list(self.benchmarks.values())
        
        if benchmark_type:
            results = [b for b in results if b.benchmark_type == benchmark_type]
        
        results.sort(key=lambda x: x.created_at, reverse=True)
        return results[:limit]
    
    def archive_benchmark(self, bench_id: str) -> bool:
        """Archive benchmark."""
        bench = self.benchmarks.get(bench_id)
        if not bench:
            return False
        
        self.history.append(bench)
        del self.benchmarks[bench_id]
        return True
    
    def _recalculate_score(self, bench: BenchmarkResult) -> None:
        """Recalculate overall score."""
        scores = [
            min(bench.latency_ms / 1000, 1.0) if bench.latency_ms else 0,
            bench.accuracy,
            bench.reliability,
            bench.quality,
            bench.scalability,
            bench.success_rate,
        ]
        bench.overall_score = sum(scores) / len(scores) if scores else 0
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
