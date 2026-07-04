"""
Invariant Benchmark
EXECUTION-KERNEL-FINALIZATION-000002

Benchmarks kernel invariant verification performance.
"""

from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass, field
import time
import json

from agos_kernel.core.invariants.runtime import InvariantRuntime, InvariantResult


@dataclass
class BenchmarkResult:
    """Result of a benchmark run."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_time_ms: float = 0.0
    invariants_per_second: float = 0.0
    results: Dict[str, float] = field(default_factory=dict)  # invariant_id -> time_ms
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'total_time_ms': self.total_time_ms,
            'invariants_per_second': self.invariants_per_second,
            'results': self.results,
        }


@dataclass
class BenchmarkBaseline:
    """Baseline benchmark for comparison."""
    version: str = "1.0.0"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    baseline: Dict[str, float] = field(default_factory=dict)
    average_total_ms: float = 0.0
    
    def compare(self, current: BenchmarkResult) -> Dict:
        """Compare current results to baseline."""
        changes = {}
        
        for inv_id, current_time in current.results.items():
            if inv_id in self.baseline:
                baseline_time = self.baseline[inv_id]
                diff = current_time - baseline_time
                percent = (diff / baseline_time * 100) if baseline_time > 0 else 0
                changes[inv_id] = {
                    'baseline_ms': baseline_time,
                    'current_ms': current_time,
                    'diff_ms': diff,
                    'diff_percent': percent,
                }
        
        return changes


class InvariantBenchmark:
    """
    Benchmarks kernel invariant verification.
    
    Tracks performance over time.
    Alerts on significant regressions.
    """
    
    def __init__(self, kernel_root=None):
        self.runtime = InvariantRuntime(kernel_root)
        self.baseline: BenchmarkBaseline = BenchmarkBaseline()
        self.history: List[BenchmarkResult] = []
    
    def run_benchmark(self) -> BenchmarkResult:
        """Run complete benchmark."""
        start_time = time.time()
        
        results = self.runtime.verify_all()
        
        total_time = (time.time() - start_time) * 1000
        invariants_per_second = len(results) / (total_time / 1000) if total_time > 0 else 0
        
        result = BenchmarkResult(
            total_time_ms=total_time,
            invariants_per_second=invariants_per_second,
            results={inv_id: r.execution_time_ms for inv_id, r in results.items()},
        )
        
        self.history.append(result)
        return result
    
    def set_baseline(self, version: str = "1.0.0") -> BenchmarkBaseline:
        """Set current results as baseline."""
        result = self.run_benchmark()
        
        self.baseline = BenchmarkBaseline(
            version=version,
            baseline=result.results.copy(),
            average_total_ms=result.total_time_ms,
        )
        
        return self.baseline
    
    def check_regression(self) -> List[Dict]:
        """
        Check for performance regressions.
        
        Returns list of regressions found.
        """
        current = self.run_benchmark()
        regressions = []
        
        # 10% threshold for regression
        REGRESSION_THRESHOLD = 10.0
        
        for inv_id, current_time in current.results.items():
            if inv_id in self.baseline.baseline:
                baseline_time = self.baseline.baseline[inv_id]
                
                if baseline_time > 0:
                    percent_change = ((current_time - baseline_time) / baseline_time) * 100
                    
                    if percent_change > REGRESSION_THRESHOLD:
                        regressions.append({
                            'invariant_id': inv_id,
                            'baseline_ms': baseline_time,
                            'current_ms': current_time,
                            'regression_percent': percent_change,
                        })
        
        return regressions
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary."""
        if not self.history:
            return {'error': 'No benchmark data available'}
        
        latest = self.history[-1]
        
        return {
            'latest_run': latest.to_dict(),
            'baseline': {
                'version': self.baseline.version,
                'average_total_ms': self.baseline.average_total_ms,
            },
            'history_count': len(self.history),
            'avg_time_ms': sum(r.total_time_ms for r in self.history) / len(self.history),
            'min_time_ms': min(r.total_time_ms for r in self.history),
            'max_time_ms': max(r.total_time_ms for r in self.history),
        }
    
    def export_benchmark(self, output_path: str) -> None:
        """Export benchmark data to file."""
        data = {
            'benchmark_baseline': {
                'version': self.baseline.version,
                'timestamp': self.baseline.timestamp.isoformat(),
                'baseline': self.baseline.baseline,
                'average_total_ms': self.baseline.average_total_ms,
            },
            'benchmark_history': [r.to_dict() for r in self.history],
            'performance_summary': self.get_performance_summary(),
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
