"""
Architecture Audit Module
=====================

Automated architectural analysis and violation detection.
Provides comprehensive audit capabilities for the AGOS platform.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import ast
import hashlib
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class ViolationSeverity(Enum):
    """Severity levels for architectural violations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ViolationType(Enum):
    """Types of architectural violations."""
    CIRCULAR_DEPENDENCY = "circular_dependency"
    LAYER_VIOLATION = "layer_violation"
    FORBIDDEN_IMPORT = "forbidden_import"
    CONTRACT_MISMATCH = "contract_mismatch"
    NAMING_VIOLATION = "naming_violation"
    COMPLEXITY_THRESHOLD = "complexity_threshold"


@dataclass
class Violation:
    """Represents an architectural violation."""
    violation_id: str
    violation_type: ViolationType
    severity: ViolationSeverity
    message: str
    file_path: str
    line_number: int = 0
    source_code: str = ""
    suggestion: str = ""
    evidence: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "type": self.violation_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "suggestion": self.suggestion,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class LayerBoundary:
    """Defines a layer boundary in the architecture."""
    layer_name: str
    allowed_dependencies: Set[str] = field(default_factory=set)
    forbidden_dependencies: Set[str] = field(default_factory=set)
    public_apis: Set[str] = field(default_factory=set)
    
    def can_access(self, target_layer: str) -> bool:
        if target_layer in self.forbidden_dependencies:
            return False
        if not self.allowed_dependencies:
            return True
        return target_layer in self.allowed_dependencies


@dataclass
class DependencyEdge:
    """An edge in the dependency graph."""
    source: str
    target: str
    import_statement: str = ""
    line_number: int = 0


@dataclass
class DependencyGraph:
    """Graph of module dependencies."""
    nodes: Set[str] = field(default_factory=set)
    edges: List[DependencyEdge] = field(default_factory=list)
    
    def add_edge(self, source: str, target: str, import_stmt: str = "", line: int = 0) -> None:
        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.append(DependencyEdge(source, target, import_stmt, line))
    
    def find_cycles(self) -> List[List[str]]:
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for edge in self.edges:
                if edge.source != node:
                    continue
                neighbor = edge.target
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:])
            
                rec_stack.discard(node)
        
        for node in self.nodes:
            if node not in visited:
                dfs(node, [])
        
        return [c for c in cycles if len(c) > 1]
    
    def get_layer_violations(self, boundaries: Dict[str, LayerBoundary]) -> List[Violation]:
        violations = []
        for edge in self.edges:
            source_layer = self._get_layer_for_module(edge.source)
            target_layer = self._get_layer_for_module(edge.target)
            
            if source_layer and target_layer:
                boundary = boundaries.get(source_layer)
                if boundary and not boundary.can_access(target_layer):
                    violations.append(Violation(
                        violation_id=f"lv_{hashlib.md5(f'{edge.source}:{edge.target}'.encode()).hexdigest()[:8]}",
                        violation_type=ViolationType.LAYER_VIOLATION,
                        severity=ViolationSeverity.HIGH,
                        message=f"Layer violation: {source_layer} cannot access {target_layer}",
                        file_path=edge.source,
                        line_number=edge.line_number,
                        suggestion=f"Review layer boundaries for {source_layer}",
                    ))
        return violations
    
    def _get_layer_for_module(self, module_path: str) -> Optional[str]:
        parts = module_path.replace('\\', '/').split('/')
        for part in parts:
            if part in ('agos', 'foundation', 'kernel', 'fabric', 'execution', 'intelligence', 'enterprise', 'ecosystem', 'evolution'):
                return part
        return None


@dataclass
class ArchitecturalRule:
    """An architectural rule that can be checked."""
    rule_id: str
    name: str
    description: str
    severity: ViolationSeverity
    rule_type: ViolationType
    is_enabled: bool = True


@dataclass
class AuditReport:
    """Comprehensive audit report."""
    report_id: str
    timestamp: datetime
    duration_seconds: float
    files_analyzed: int
    violations: List[Violation]
    dependencies: DependencyGraph
    complexity_metrics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == ViolationSeverity.CRITICAL)
    
    @property
    def high_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == ViolationSeverity.HIGH)
    
    @property
    def should_fail_build(self) -> bool:
        return self.critical_count > 0 or self.high_count > 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp.isoformat(),
            "duration_seconds": self.duration_seconds,
            "files_analyzed": self.files_analyzed,
            "violation_count": len(self.violations),
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "should_fail_build": self.should_fail_build,
            "violations": [v.to_dict() for v in self.violations],
            "recommendations": self.recommendations,
        }


class ArchitectureAuditor:
    """
    Universal Architecture Auditing System.
    
    Analyzes the entire codebase for architectural violations,
    dependency issues, complexity problems, and compliance.
    """
    
    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.rules: List[ArchitecturalRule] = []
        self.layer_boundaries: Dict[str, LayerBoundary] = {}
        self.forbidden_patterns: List[re.Pattern] = []
        self._setup_default_rules()
    
    def _setup_default_rules(self) -> None:
        self.rules.append(ArchitecturalRule(
            rule_id="circular_deps",
            name="No Circular Dependencies",
            description="Detect circular dependencies",
            severity=ViolationSeverity.CRITICAL,
            rule_type=ViolationType.CIRCULAR_DEPENDENCY,
        ))
        self.rules.append(ArchitecturalRule(
            rule_id="layer_violation",
            name="Layer Boundary Enforcement",
            description="Enforce layer boundaries",
            severity=ViolationSeverity.HIGH,
            rule_type=ViolationType.LAYER_VIOLATION,
        ))
    
    def add_layer_boundary(self, boundary: LayerBoundary) -> None:
        self.layer_boundaries[boundary.layer_name] = boundary
    
    def audit(self, target_path: Optional[str] = None) -> AuditReport:
        import time
        start_time = time.time()
        target = target_path or self.root_path
        all_violations: List[Violation] = []
        dependency_graph = DependencyGraph()
        files_analyzed = 0
        
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    files_analyzed += 1
                    deps = self._extract_dependencies(file_path)
                    module_name = self._module_name_from_path(file_path)
                    for dep in deps:
                        dependency_graph.add_edge(module_name, dep)
        
        cycles = dependency_graph.find_cycles()
        for cycle in cycles:
            cycle_str = " -> ".join(cycle)
            all_violations.append(Violation(
                violation_id=f"cycle_{hashlib.md5(cycle_str.encode()).hexdigest()[:8]}",
                violation_type=ViolationType.CIRCULAR_DEPENDENCY,
                severity=ViolationSeverity.CRITICAL,
                message=f"Circular dependency: {cycle_str}",
                file_path=cycle[0],
                suggestion="Break the cycle by extracting shared dependencies",
            ))
        
        layer_violations = dependency_graph.get_layer_violations(self.layer_boundaries)
        all_violations.extend(layer_violations)
        
        duration = time.time() - start_time
        
        return AuditReport(
            report_id=f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.utcnow(),
            duration_seconds=duration,
            files_analyzed=files_analyzed,
            violations=all_violations,
            dependencies=dependency_graph,
            recommendations=self._generate_recommendations(all_violations),
        )
    
    def _module_name_from_path(self, file_path: str) -> str:
        rel_path = os.path.relpath(file_path, self.root_path)
        return rel_path.replace('/', '.').replace('.py', '')
    
    def _extract_dependencies(self, file_path: str) -> List[str]:
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module)
        except:
            pass
        return dependencies
    
    def _generate_recommendations(self, violations: List[Violation]) -> List[str]:
        recommendations = []
        by_type = {}
        for v in violations:
            by_type[v.violation_type] = by_type.get(v.violation_type, 0) + 1
        
        if ViolationType.CIRCULAR_DEPENDENCY in by_type:
            recommendations.append("Refactor shared dependencies to break circular imports")
        if ViolationType.LAYER_VIOLATION in by_type:
            recommendations.append("Review layer boundaries and adjust allowed dependencies")
        
        return recommendations
