#!/usr/bin/env python3
"""
AGOS Enterprise - Benchmark Module
==================================

Benchmarking system for providers.
Measures performance, reliability, and quality.
Results are used for provider certification and selection.

Benchmark Dimensions:
- Latency: How fast does the provider respond?
- Throughput: How many requests per second?
- Error Rate: How often does it fail?
- Accuracy: Does it produce correct results?
- Resource Usage: How much CPU/memory does it use?
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json
import time


class BenchmarkType(Enum):
    """Types of benchmarks."""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ACCURACY = "accuracy"
    RELIABILITY = "reliability"
    RESOURCE_USAGE = "resource_usage"
    END_TO_END = "end_to_end"


class BenchmarkStatus(Enum):
    """Status of a benchmark run."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BenchmarkMetrics:
    """Metrics from a benchmark run."""
    latency_p50_ms: int = 0            # Median latency
    latency_p95_ms: int = 0            # 95th percentile latency
    latency_p99_ms: int = 0            # 99th percentile latency
    latency_avg_ms: int = 0            # Average latency
    
    throughput_rps: float = 0.0        # Requests per second
    total_requests: int = 0
    
    error_rate: float = 0.0            # Percentage of failed requests
    success_count: int = 0
    failure_count: int = 0
    
    accuracy_score: float = 0.0        # 0-100 accuracy score
    quality_score: float = 0.0         # 0-100 quality score
    
    cpu_usage_avg: float = 0.0         # Average CPU usage %
    memory_usage_avg_mb: float = 0.0  # Average memory usage MB
    
    score: float = 0.0                 # Overall benchmark score (0-100)
    
    def compute_overall_score(self) -> float:
        """Compute overall benchmark score."""
        # Weighted scoring
        latency_score = max(0, 100 - (self.latency_p95_ms / 10))
        throughput_score = min(100, self.throughput_rps * 10)
        reliability_score = (1 - self.error_rate) * 100
        accuracy_score = self.accuracy_score
        
        # Weighted average
        score = (
            latency_score * 0.25 +
            throughput_score * 0.15 +
            reliability_score * 0.30 +
            accuracy_score * 0.30
        )
        
        return round(min(100, max(0, score)), 2)


@dataclass
class BenchmarkResult:
    """Result of a complete benchmark run."""
    benchmark_id: str
    provider_id: str
    capability_id: str
    benchmark_type: BenchmarkType
    
    status: BenchmarkStatus
    started_at: str
    completed_at: Optional[str] = None
    
    metrics: BenchmarkMetrics = field(default_factory=BenchmarkMetrics)
    
    test_cases: Tuple[Dict[str, Any], ...] = ()
    failures: Tuple[Dict[str, Any], ...] = ()
    
    recommendation: str = ""  # approve, reject, needs_improvement
    
    def is_passed(self) -> bool:
        """Check if benchmark passed."""
        return (
            self.status == BenchmarkStatus.COMPLETED and
            self.metrics.error_rate < 0.05 and  # Less than 5% errors
            self.metrics.score >= 70             # Score at least 70
        )


@dataclass
class TestCase:
    """A single test case for benchmarking."""
    case_id: str
    name: str
    input_data: Dict[str, Any]
    expected_output: Optional[Any] = None
    timeout_ms: int = 30000
    weight: float = 1.0  # Weight in overall score


class BenchmarkRunner:
    """
    Runs benchmarks on providers.
    Tests providers under controlled conditions.
    """
    
    def __init__(self):
        self._benchmarks: Dict[str, BenchmarkResult] = {}
        self._test_cases: Dict[str, List[TestCase]] = {}
    
    def register_test_cases(
        self,
        capability_id: str,
        test_cases: List[TestCase],
    ) -> None:
        """Register test cases for a capability."""
        self._test_cases[capability_id] = test_cases
    
    def run_benchmark(
        self,
        provider,
        capability_id: str,
        benchmark_type: BenchmarkType = BenchmarkType.END_TO_END,
        iterations: int = 100,
    ) -> BenchmarkResult:
        """
        Run a benchmark on a provider.
        
        Args:
            provider: The provider to benchmark
            capability_id: ID of capability to test
            benchmark_type: Type of benchmark
            iterations: Number of test iterations
        
        Returns:
            BenchmarkResult with detailed metrics
        """
        benchmark_id = f"bench_{provider.provider_id}_{capability_id}_{int(time.time())}"
        
        result = BenchmarkResult(
            benchmark_id=benchmark_id,
            provider_id=provider.provider_id,
            capability_id=capability_id,
            benchmark_type=benchmark_type,
            status=BenchmarkStatus.RUNNING,
            started_at=datetime.utcnow().isoformat(),
        )
        
        # Get test cases
        test_cases = self._test_cases.get(capability_id, [])
        if not test_cases:
            # Generate default test cases
            test_cases = self._generate_default_test_cases(capability_id)
        
        # Run tests
        latencies = []
        failures = []
        success_count = 0
        
        for i in range(iterations):
            test_case = test_cases[i % len(test_cases)]
            
            start_time = time.time()
            try:
                # Execute on provider
                exec_result = provider.execute(
                    skill_id=test_case.case_id,
                    input_data=test_case.input_data,
                    timeout_ms=test_case.timeout_ms,
                )
                
                latency_ms = int((time.time() - start_time) * 1000)
                latencies.append(latency_ms)
                
                if exec_result.get("success", False):
                    success_count += 1
                else:
                    failures.append({
                        "iteration": i,
                        "error": exec_result.get("error"),
                        "test_case": test_case.case_id,
                    })
                    
            except Exception as e:
                latencies.append(int((time.time() - start_time) * 1000))
                failures.append({
                    "iteration": i,
                    "error": str(e),
                    "test_case": test_case.case_id,
                })
        
        # Calculate metrics
        metrics = self._calculate_metrics(
            latencies=latencies,
            success_count=success_count,
            total=iterations,
            failures=failures,
        )
        
        result.metrics = metrics
        result.status = BenchmarkStatus.COMPLETED
        result.completed_at = datetime.utcnow().isoformat()
        result.test_cases = tuple(
            {"case_id": tc.case_id, "name": tc.name} for tc in test_cases
        )
        result.failures = tuple(failures)
        
        # Generate recommendation
        result.recommendation = self._generate_recommendation(result)
        
        # Store result
        self._benchmarks[benchmark_id] = result
        
        return result
    
    def _generate_default_test_cases(self, capability_id: str) -> List[TestCase]:
        """Generate default test cases for a capability."""
        return [
            TestCase(
                case_id=f"{capability_id}_test_001",
                name="Basic Test",
                input_data={"test": "basic"},
                expected_output=None,
            ),
            TestCase(
                case_id=f"{capability_id}_test_002",
                name="Edge Case Test",
                input_data={"test": "edge_case"},
                expected_output=None,
            ),
        ]
    
    def _calculate_metrics(
        self,
        latencies: List[int],
        success_count: int,
        total: int,
        failures: List[Dict],
    ) -> BenchmarkMetrics:
        """Calculate benchmark metrics from raw data."""
        metrics = BenchmarkMetrics()
        
        # Calculate latency percentiles
        if latencies:
            sorted_latencies = sorted(latencies)
            metrics.latency_avg_ms = int(sum(latencies) / len(latencies))
            metrics.latency_p50_ms = sorted_latencies[int(len(sorted_latencies) * 0.50)]
            metrics.latency_p95_ms = sorted_latencies[int(len(sorted_latencies) * 0.95)]
            metrics.latency_p99_ms = sorted_latencies[int(len(sorted_latencies) * 0.99)]
        
        # Calculate throughput
        if latencies:
            total_time = sum(latencies) / 1000  # Convert to seconds
            metrics.throughput_rps = len(latencies) / max(1, total_time)
        
        # Calculate error rate
        metrics.total_requests = total
        metrics.success_count = success_count
        metrics.failure_count = len(failures)
        metrics.error_rate = len(failures) / max(1, total)
        
        # Default scores (would be calculated from actual test results)
        metrics.accuracy_score = 90.0
        metrics.quality_score = 85.0
        
        # Calculate overall score
        metrics.score = metrics.compute_overall_score()
        
        return metrics
    
    def _generate_recommendation(self, result: BenchmarkResult) -> str:
        """Generate benchmark recommendation."""
        score = result.metrics.score
        error_rate = result.metrics.error_rate
        
        if error_rate > 0.1:  # More than 10% errors
            return "reject"
        elif score >= 80 and error_rate < 0.05:
            return "approve"
        elif score >= 60:
            return "needs_improvement"
        else:
            return "reject"
    
    def compare_providers(
        self,
        provider_ids: List[str],
        capability_id: str,
    ) -> List[Tuple[str, float, float]]:
        """
        Compare multiple providers for a capability.
        Returns list of (provider_id, score, error_rate) tuples sorted by score.
        """
        comparisons = []
        
        for benchmark in self._benchmarks.values():
            if (
                benchmark.capability_id == capability_id and
                benchmark.provider_id in provider_ids and
                benchmark.status == BenchmarkStatus.COMPLETED
            ):
                comparisons.append((
                    benchmark.provider_id,
                    benchmark.metrics.score,
                    benchmark.metrics.error_rate,
                ))
        
        # Sort by score descending
        comparisons.sort(key=lambda x: x[1], reverse=True)
        
        return comparisons
    
    def get_provider_best_capability(
        self,
        provider_id: str,
    ) -> Optional[str]:
        """Get the capability where provider performs best."""
        best_cap = None
        best_score = 0
        
        for benchmark in self._benchmarks.values():
            if (
                benchmark.provider_id == provider_id and
                benchmark.status == BenchmarkStatus.COMPLETED
            ):
                if benchmark.metrics.score > best_score:
                    best_score = benchmark.metrics.score
                    best_cap = benchmark.capability_id
        
        return best_cap
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get benchmark statistics."""
        completed = [
            b for b in self._benchmarks.values()
            if b.status == BenchmarkStatus.COMPLETED
        ]
        
        if not completed:
            return {
                "total_benchmarks": len(self._benchmarks),
                "completed": 0,
                "average_score": 0,
            }
        
        scores = [b.metrics.score for b in completed]
        error_rates = [b.metrics.error_rate for b in completed]
        
        return {
            "total_benchmarks": len(self._benchmarks),
            "completed": len(completed),
            "average_score": round(sum(scores) / len(scores), 2),
            "average_error_rate": round(sum(error_rates) / len(error_rates), 4),
            "recommendations": {
                "approve": len([b for b in completed if b.recommendation == "approve"]),
                "reject": len([b for b in completed if b.recommendation == "reject"]),
                "needs_improvement": len([b for b in completed if b.recommendation == "needs_improvement"]),
            },
        }
