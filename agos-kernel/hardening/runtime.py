"""AGOS Production Hardening Framework."""
import asyncio
import gc
import hashlib
import inspect
import memory_profiler
import psutil
import threading
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import random


class TestType(Enum):
    """Test types."""
    UNIT = "unit"
    INTEGRATION = "integration"
    CONTRACT = "contract"
    SYSTEM = "system"
    E2E = "e2e"
    PERFORMANCE = "performance"
    LOAD = "load"
    STRESS = "stress"
    CHAOS = "chaos"
    RECOVERY = "recovery"
    SECURITY = "security"
    REGRESSION = "regression"


class TestStatus(Enum):
    """Test status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class TestResult:
    """Test result."""
    id: str
    name: str
    test_type: TestType
    status: TestStatus
    duration_ms: float
    error: Optional[str] = None
    trace: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class ChaosEvent:
    """Chaos engineering event."""
    type: str
    target: str
    duration_ms: float
    injected: bool
    recovered: bool


@dataclass
class LoadTestMetrics:
    """Load test metrics."""
    requests: int = 0
    failures: int = 0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    throughput_rps: float = 0.0


@dataclass
class MemorySnapshot:
    """Memory snapshot."""
    timestamp: datetime
    rss_mb: float
    vms_mb: float
    objects: int = 0


class FailureInjectionFramework:
    """Framework for injecting failures."""
    
    def __init__(self):
        self.chaos_events: List[ChaosEvent] = []
        self.enabled = True
    
    async def inject_latency(self, duration_ms: int):
        """Inject network latency."""
        await asyncio.sleep(duration_ms / 1000)
    
    async def inject_exception(self, exception_type: type = Exception):
        """Inject an exception."""
        raise exception_type("Injected failure")
    
    async def inject_timeout(self, coro):
        """Inject timeout."""
        try:
            return await asyncio.wait_for(coro, timeout=0.001)
        except asyncio.TimeoutError:
            raise Exception("Injected timeout")
    
    async def inject_crash(self):
        """Simulate crash."""
        raise RuntimeError("Injected crash")


class HardeningRuntime:
    """Production hardening runtime."""
    
    def __init__(self):
        self.framework = FailureInjectionFramework()
        self.test_results: List[TestResult] = []
        self.memory_snapshots: List[MemorySnapshot] = []
        self.process = psutil.Process()
    
    async def run_unit_test(self, name: str, test_func: Callable) -> TestResult:
        """Run a unit test."""
        return await self._run_test(name, TestType.UNIT, test_func)
    
    async def run_integration_test(self, name: str, test_func: Callable) -> TestResult:
        """Run an integration test."""
        return await self._run_test(name, TestType.INTEGRATION, test_func)
    
    async def run_contract_test(self, name: str, test_func: Callable) -> TestResult:
        """Run a contract test."""
        return await self._run_test(name, TestType.CONTRACT, test_func)
    
    async def _run_test(self, name: str, test_type: TestType, test_func: Callable) -> TestResult:
        """Run a test."""
        result = TestResult(
            id=hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8],
            name=name,
            test_type=test_type,
            status=TestStatus.RUNNING,
            duration_ms=0.0,
        )
        
        start = time.time()
        try:
            if asyncio.iscoroutinefunction(test_func):
                await test_func()
            else:
                test_func()
            
            result.status = TestStatus.PASSED
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error = str(e)
            result.trace = traceback.format_exc().split("\n")
        
        result.duration_ms = (time.time() - start) * 1000
        self.test_results.append(result)
        return result
    
    async def run_chaos_test(self, name: str, test_func: Callable, 
                            chaos_types: List[str] = None) -> TestResult:
        """Run a chaos test."""
        result = TestResult(
            id=hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8],
            name=name,
            test_type=TestType.CHAOS,
            status=TestStatus.RUNNING,
            duration_ms=0.0,
        )
        
        chaos_types = chaos_types or ["latency", "exception", "timeout"]
        start = time.time()
        
        try:
            # Inject chaos
            chaos_type = random.choice(chaos_types)
            event = ChaosEvent(
                type=chaos_type,
                target=name,
                duration_ms=100,
                injected=False,
                recovered=False,
            )
            
            if chaos_type == "latency":
                await self.framework.inject_latency(100)
            elif chaos_type == "exception":
                try:
                    await test_func()
                except Exception:
                    pass  # Expected
            elif chaos_type == "timeout":
                try:
                    await self.framework.inject_timeout(asyncio.sleep(1))
                except Exception:
                    pass  # Expected
            
            event.injected = True
            self.framework.chaos_events.append(event)
            
            # Run actual test
            await test_func()
            
            event.recovered = True
            result.status = TestStatus.PASSED
            
        except Exception as e:
            result.status = TestStatus.FAILED
            result.error = str(e)
        
        result.duration_ms = (time.time() - start) * 1000
        self.test_results.append(result)
        return result
    
    async def run_load_test(self, name: str, test_func: Callable,
                           concurrent_users: int = 100,
                           duration_seconds: int = 60) -> Tuple[TestResult, LoadTestMetrics]:
        """Run a load test."""
        result = TestResult(
            id=hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8],
            name=name,
            test_type=TestType.LOAD,
            status=TestStatus.RUNNING,
            duration_ms=0.0,
        )
        
        metrics = LoadTestMetrics()
        latencies = []
        start = time.time()
        
        async def user_session():
            session_start = time.time()
            try:
                await test_func()
                latencies.append((time.time() - session_start) * 1000)
            except:
                metrics.failures += 1
            metrics.requests += 1
        
        # Run concurrent users
        tasks = [user_session() for _ in range(concurrent_users)]
        await asyncio.gather(*tasks)
        
        elapsed = time.time() - start
        result.duration_ms = elapsed * 1000
        result.status = TestStatus.PASSED
        
        # Calculate metrics
        if latencies:
            latencies.sort()
            metrics.avg_latency_ms = sum(latencies) / len(latencies)
            metrics.p50_latency_ms = latencies[int(len(latencies) * 0.5)]
            metrics.p95_latency_ms = latencies[int(len(latencies) * 0.95)]
            metrics.p99_latency_ms = latencies[int(len(latencies) * 0.99)]
        metrics.throughput_rps = metrics.requests / elapsed
        
        result.metrics = asdict(metrics)
        self.test_results.append(result)
        
        return result, metrics
    
    def detect_memory_leak(self, func: Callable, iterations: int = 100) -> bool:
        """Detect memory leaks."""
        snapshots = []
        
        for _ in range(iterations):
            if asyncio.iscoroutinefunction(func):
                asyncio.run(func())
            else:
                func()
            
            gc.collect()
            mem = self.process.memory_info()
            snapshots.append(MemorySnapshot(
                timestamp=datetime.now(),
                rss_mb=mem.rss / 1024 / 1024,
                vms_mb=mem.vms / 1024 / 1024,
            ))
        
        # Check for growth trend
        if len(snapshots) >= 10:
            first_avg = sum(s.rss_mb for s in snapshots[:5]) / 5
            last_avg = sum(s.rss_mb for s in snapshots[-5:]) / 5
            growth = (last_avg - first_avg) / first_avg * 100
            return growth > 10  # 10% growth indicates leak
        
        return False
    
    def detect_deadlock(self, func: Callable, timeout_seconds: int = 5) -> bool:
        """Detect deadlocks."""
        result = {"deadlocked": False}
        
        def run():
            try:
                if asyncio.iscoroutinefunction(func):
                    asyncio.run(func())
                else:
                    func()
            except Exception:
                pass
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout_seconds)
        
        if thread.is_alive():
            result["deadlocked"] = True
        
        return result["deadlocked"]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get hardening summary."""
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r.status == TestStatus.PASSED])
        failed = len([r for r in self.test_results if r.status == TestStatus.FAILED])
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "chaos_events": len(self.framework.chaos_events),
            "memory_snapshots": len(self.memory_snapshots),
        }


# Alias for tuple
from typing import Tuple


def asdict(obj):
    """Convert dataclass to dict."""
    if hasattr(obj, '__dataclass_fields__'):
        return {k: asdict(v) if hasattr(v, '__dataclass_fields__') else v 
                for k, v in obj.__dict__.items() if not k.startswith('_')}
    return obj


# Global hardening runtime
_hardening = HardeningRuntime()


def get_hardening_runtime() -> HardeningRuntime:
    """Get global hardening runtime."""
    return _hardening


# Test Examples
async def test_example():
    """Example test."""
    await asyncio.sleep(0.01)


async def test_hardening():
    """Test hardening framework."""
    print("=" * 60)
    print("Production Hardening Framework")
    print("=" * 60)
    
    runtime = get_hardening_runtime()
    
    # Unit test
    result = await runtime.run_unit_test("basic_test", test_example)
    print(f"Unit Test: {result.status.value}")
    
    # Integration test
    result = await runtime.run_integration_test("integration_test", test_example)
    print(f"Integration Test: {result.status.value}")
    
    # Contract test
    result = await runtime.run_contract_test("contract_test", test_example)
    print(f"Contract Test: {result.status.value}")
    
    # Chaos test
    result = await runtime.run_chaos_test("chaos_test", test_example, ["latency"])
    print(f"Chaos Test: {result.status.value}")
    
    # Memory leak detection
    has_leak = runtime.detect_memory_leak(lambda: [1] * 1000, iterations=20)
    print(f"Memory Leak Detected: {has_leak}")
    
    # Deadlock detection
    is_deadlock = runtime.detect_deadlock(lambda: time.sleep(0.1), timeout_seconds=1)
    print(f"Deadlock Detected: {is_deadlock}")
    
    # Summary
    summary = runtime.get_summary()
    print(f"\nSummary:")
    print(f"  Total: {summary['total_tests']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Pass Rate: {summary['pass_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("Hardening Tests Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_hardening())