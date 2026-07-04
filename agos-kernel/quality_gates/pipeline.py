"""AGOS Engineering Quality Gates Pipeline."""
import hashlib
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class GateType(Enum):
    """Gate types."""
    ARCHITECTURE = "architecture"
    CONTRACT = "contract"
    DEPENDENCY = "dependency"
    POLICY = "policy"
    KNOWLEDGE = "knowledge"
    EVIDENCE = "evidence"
    SECURITY = "security"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    COMPATIBILITY = "compatibility"
    DOCUMENTATION = "documentation"
    BENCHMARK = "benchmark"
    CERTIFICATION = "certification"


class GateStatus(Enum):
    """Gate status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class GateResult:
    """Gate result."""
    gate_type: GateType
    status: GateStatus
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class QualityGate:
    """A quality gate."""
    name: str
    gate_type: GateType
    enabled: bool = True
    blocking: bool = True
    threshold: float = 0.0


class QualityGatesPipeline:
    """Immutable quality gates pipeline."""
    
    def __init__(self):
        self.gates: Dict[GateType, QualityGate] = {}
        self.results: List[GateResult] = []
        self._initialize_gates()
    
    def _initialize_gates(self):
        """Initialize all gates."""
        gates = [
            QualityGate("Architecture Validation", GateType.ARCHITECTURE, blocking=True),
            QualityGate("Contract Validation", GateType.CONTRACT, blocking=True),
            QualityGate("Dependency Validation", GateType.DEPENDENCY, blocking=True),
            QualityGate("Policy Validation", GateType.POLICY, blocking=True),
            QualityGate("Knowledge Validation", GateType.KNOWLEDGE, blocking=True),
            QualityGate("Evidence Validation", GateType.EVIDENCE, blocking=True),
            QualityGate("Security Validation", GateType.SECURITY, blocking=True),
            QualityGate("Performance Validation", GateType.PERFORMANCE, blocking=True),
            QualityGate("Reliability Validation", GateType.RELIABILITY, blocking=True),
            QualityGate("Compatibility Validation", GateType.COMPATIBILITY, blocking=True),
            QualityGate("Documentation Validation", GateType.DOCUMENTATION, blocking=True),
            QualityGate("Benchmark Validation", GateType.BENCHMARK, blocking=True),
            QualityGate("Certification Validation", GateType.CERTIFICATION, blocking=True),
        ]
        
        for gate in gates:
            self.gates[gate.gate_type] = gate
    
    async def validate_architecture(self, code: str) -> GateResult:
        """Validate architecture."""
        start = time.time()
        
        issues = []
        
        # Check for circular dependencies
        if re.search(r"from \w+ import.*from \w+ import", code):
            issues.append("Potential circular dependency detected")
        
        # Check for architecture drift
        if len(code.split("\n")) > 10000:
            issues.append("File exceeds recommended size")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.ARCHITECTURE,
            status=status,
            message="Architecture validation complete" if not issues else "; ".join(issues),
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_contract(self, interfaces: List[Dict]) -> GateResult:
        """Validate contracts."""
        start = time.time()
        
        issues = []
        
        # Check for breaking changes
        for iface in interfaces:
            if iface.get("breaking"):
                issues.append(f"Breaking change in {iface.get('name')}")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.CONTRACT,
            status=status,
            message="Contracts valid" if not issues else "; ".join(issues),
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_dependencies(self, deps: List[Dict]) -> GateResult:
        """Validate dependencies."""
        start = time.time()
        
        issues = []
        vulnerable = ["lodash@4.17.15", "request@2.88.0"]
        
        for dep in deps:
            if dep.get("name") in vulnerable:
                issues.append(f"Vulnerable dependency: {dep.get('name')}")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.DEPENDENCY,
            status=status,
            message="Dependencies valid" if not issues else "; ".join(issues),
            details={"vulnerable_count": len(issues)},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_policy(self, policies: List[str]) -> GateResult:
        """Validate policies."""
        start = time.time()
        
        issues = []
        
        # Check for policy violations
        if "no_security_check" in policies:
            issues.append("Security policy violation detected")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.POLICY,
            status=status,
            message="Policies enforced" if not issues else "; ".join(issues),
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_knowledge(self, knowledge: List[Dict]) -> GateResult:
        """Validate knowledge objects."""
        start = time.time()
        
        issues = []
        
        for ko in knowledge:
            if not ko.get("evidence"):
                issues.append(f"Missing evidence for {ko.get('name')}")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.KNOWLEDGE,
            status=status,
            message="Knowledge valid" if not issues else "; ".join(issues),
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_evidence(self, evidence: List[str]) -> GateResult:
        """Validate evidence."""
        start = time.time()
        
        status = GateStatus.PASSED if evidence else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.EVIDENCE,
            status=status,
            message="Evidence present" if evidence else "Missing evidence",
            details={"evidence_count": len(evidence)},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_security(self, scan_results: Dict) -> GateResult:
        """Validate security."""
        start = time.time()
        
        critical = scan_results.get("critical_vulnerabilities", 0)
        status = GateStatus.PASSED if critical == 0 else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.SECURITY,
            status=status,
            message="No critical vulnerabilities" if critical == 0 else f"{critical} critical vulnerabilities",
            details={"critical": critical, "high": scan_results.get("high_vulnerabilities", 0)},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_performance(self, metrics: Dict) -> GateResult:
        """Validate performance."""
        start = time.time()
        
        regression = metrics.get("regression_percent", 0)
        status = GateStatus.PASSED if regression < 10 else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.PERFORMANCE,
            status=status,
            message=f"Performance regression: {regression:.1f}%" if regression > 0 else "No regression",
            details={"regression": regression},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_reliability(self, reliability_score: float) -> GateResult:
        """Validate reliability."""
        start = time.time()
        
        threshold = 95.0
        status = GateStatus.PASSED if reliability_score >= threshold else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.RELIABILITY,
            status=status,
            message=f"Reliability: {reliability_score:.1f}%" if reliability_score >= threshold else f"Reliability below threshold: {reliability_score:.1f}%",
            details={"score": reliability_score, "threshold": threshold},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_compatibility(self, compat_matrix: Dict) -> GateResult:
        """Validate compatibility."""
        start = time.time()
        
        issues = []
        for version, compatible in compat_matrix.items():
            if not compatible:
                issues.append(f"Incompatible: {version}")
        
        status = GateStatus.PASSED if not issues else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.COMPATIBILITY,
            status=status,
            message="Compatible" if not issues else "; ".join(issues),
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_documentation(self, docs: List[Dict]) -> GateResult:
        """Validate documentation."""
        start = time.time()
        
        missing = [d["name"] for d in docs if not d.get("complete")]
        status = GateStatus.PASSED if not missing else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.DOCUMENTATION,
            status=status,
            message="Documentation complete" if not missing else f"Missing docs: {', '.join(missing)}",
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_benchmark(self, benchmark_results: Dict) -> GateResult:
        """Validate benchmarks."""
        start = time.time()
        
        degradation = benchmark_results.get("degradation_percent", 0)
        status = GateStatus.PASSED if degradation < 5 else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.BENCHMARK,
            status=status,
            message=f"Benchmark degradation: {degradation:.1f}%" if degradation > 0 else "Benchmarks maintained",
            details={"degradation": degradation},
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def validate_certification(self, certifications: List[str]) -> GateResult:
        """Validate certifications."""
        start = time.time()
        
        required = ["kernel", "runtime", "capability"]
        missing = [r for r in required if r not in certifications]
        status = GateStatus.PASSED if not missing else GateStatus.BLOCKED
        
        return GateResult(
            gate_type=GateType.CERTIFICATION,
            status=status,
            message="Certified" if not missing else f"Missing certifications: {', '.join(missing)}",
            duration_ms=(time.time() - start) * 1000,
        )
    
    async def run_all_gates(self, context: Dict) -> List[GateResult]:
        """Run all quality gates."""
        results = []
        
        # Run all gates
        gates = [
            ("architecture", self.validate_architecture(context.get("code", ""))),
            ("contract", self.validate_contract(context.get("interfaces", []))),
            ("dependency", self.validate_dependencies(context.get("dependencies", []))),
            ("policy", self.validate_policy(context.get("policies", []))),
            ("knowledge", self.validate_knowledge(context.get("knowledge", []))),
            ("evidence", self.validate_evidence(context.get("evidence", []))),
            ("security", self.validate_security(context.get("security_scan", {}))),
            ("performance", self.validate_performance(context.get("performance_metrics", {}))),
            ("reliability", self.validate_reliability(context.get("reliability_score", 100.0))),
            ("compatibility", self.validate_compatibility(context.get("compat_matrix", {}))),
            ("documentation", self.validate_documentation(context.get("docs", []))),
            ("benchmark", self.validate_benchmark(context.get("benchmark_results", {}))),
            ("certification", self.validate_certification(context.get("certifications", []))),
        ]
        
        for name, coro in gates:
            result = await coro
            results.append(result)
            self.results.append(result)
        
        return results
    
    def can_merge(self) -> tuple[bool, List[str]]:
        """Check if merge is allowed based on gate results."""
        blocking_issues = []
        
        for result in self.results:
            gate = self.gates.get(result.gate_type)
            if gate and gate.blocking and result.status in [GateStatus.BLOCKED, GateStatus.FAILED]:
                blocking_issues.append(f"{result.gate_type.value}: {result.message}")
        
        return len(blocking_issues) == 0, blocking_issues
    
    def get_summary(self) -> Dict[str, Any]:
        """Get pipeline summary."""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == GateStatus.PASSED])
        blocked = len([r for r in self.results if r.status == GateStatus.BLOCKED])
        failed = len([r for r in self.results if r.status == GateStatus.FAILED])
        
        can_merge, issues = self.can_merge()
        
        return {
            "total_gates": total,
            "passed": passed,
            "blocked": blocked,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "can_merge": can_merge,
            "blocking_issues": issues,
        }


# Global pipeline
_pipeline = QualityGatesPipeline()


def get_pipeline() -> QualityGatesPipeline:
    """Get global quality gates pipeline."""
    return _pipeline


# Test
async def test_gates():
    """Test quality gates."""
    print("=" * 60)
    print("Engineering Quality Gates Pipeline")
    print("=" * 60)
    
    pipeline = get_pipeline()
    
    # Run with test context
    context = {
        "code": "from a import b\nfrom c import d",
        "interfaces": [],
        "dependencies": [],
        "policies": [],
        "knowledge": [{"name": "test", "evidence": ["e1"]}],
        "evidence": ["evidence1"],
        "security_scan": {"critical_vulnerabilities": 0},
        "performance_metrics": {"regression_percent": 2.0},
        "reliability_score": 98.5,
        "compat_matrix": {"1.0": True, "2.0": True},
        "docs": [{"name": "api", "complete": True}],
        "benchmark_results": {"degradation_percent": 1.0},
        "certifications": ["kernel", "runtime", "capability"],
    }
    
    results = await pipeline.run_all_gates(context)
    
    print("\nGate Results:")
    for result in results:
        status_icon = "✓" if result.status == GateStatus.PASSED else "✗"
        print(f"  {status_icon} {result.gate_type.value}: {result.message} ({result.duration_ms:.1f}ms)")
    
    summary = pipeline.get_summary()
    print(f"\nSummary:")
    print(f"  Total: {summary['total_gates']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Blocked: {summary['blocked']}")
    print(f"  Can Merge: {summary['can_merge']}")
    
    if not summary['can_merge']:
        print(f"\nBlocking Issues:")
        for issue in summary['blocking_issues']:
            print(f"  - {issue}")
    
    print("\n" + "=" * 60)
    print("Quality Gates Complete!")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_gates())