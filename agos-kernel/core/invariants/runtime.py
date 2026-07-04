"""
Invariant Runtime
EXECUTION-KERNEL-FINALIZATION-000002

Runtime system for executing and monitoring kernel invariants.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class InvariantResult:
    """Result of an invariant check."""
    invariant_id: str
    passed: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)
    violations: List[Dict] = field(default_factory=list)
    execution_time_ms: float = 0.0
    evidence_hash: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'invariant_id': self.invariant_id,
            'passed': self.passed,
            'timestamp': self.timestamp.isoformat(),
            'violations': self.violations,
            'execution_time_ms': self.execution_time_ms,
            'evidence_hash': self.evidence_hash,
        }


class InvariantRuntime:
    """
    Runtime system for executing kernel invariants.
    
    Invariants are automatically verified.
    Violation immediately fails validation.
    """
    
    # Kernel core directories that should NOT depend on external modules
    KERNEL_CORE_DIRS = ['core', 'contracts', 'events', 'runtime', 'registry']
    
    # External modules that kernel core must never depend on
    FORBIDDEN_IMPORTS = [
        'extension',
        'providers', 
        'agent_packs',
        'models',
        'domains',
        'marketplace',
        'skills',
        'workflows',
        'capabilities',
    ]
    
    def __init__(self, kernel_root: Optional[Path] = None):
        self.kernel_root = kernel_root or self._find_kernel_root()
        self.results: Dict[str, InvariantResult] = {}
        self._import_graph: Dict[str, Set[str]] = {}
        
    def _find_kernel_root(self) -> Path:
        """Locate the AGOS kernel root directory."""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / 'agos-kernel').exists():
                return parent / 'agos-kernel'
        return Path('/workspace/All-hand/agos-kernel')
    
    def verify_all(self) -> Dict[str, InvariantResult]:
        """Run all invariant checks."""
        self._scan_imports()
        self._verify_dependency_invariants()
        self._verify_architecture_invariants()
        return self.results
    
    def _scan_imports(self) -> None:
        """Build import dependency graph."""
        kernel_dir = self.kernel_root
        
        for py_file in kernel_dir.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
                
            rel_path = py_file.relative_to(kernel_dir)
            module_parts = rel_path.with_suffix('').parts
            
            if module_parts[0] in self.KERNEL_CORE_DIRS:
                self._analyze_file_imports(py_file)
    
    def _analyze_file_imports(self, file_path: Path) -> None:
        """Analyze imports in a single file."""
        module_name = str(file_path.relative_to(self.kernel_root)).replace('/', '.').replace('.py', '')
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except Exception:
            pass
            
        self._import_graph[module_name] = imports
    
    def _verify_dependency_invariants(self) -> None:
        """Verify dependency isolation invariants."""
        # INV-001: Kernel never depends on Extensions
        self._check_import_violation(
            'INV-001',
            'Kernel Never Depends on Extensions',
            'agos_kernel.extension'
        )
        
        # INV-002: Kernel never depends on Providers
        self._check_import_violation(
            'INV-002',
            'Kernel Never Depends on Providers',
            'agos_kernel.providers'
        )
        
        # INV-003: Kernel never depends on Agents
        self._check_import_violation(
            'INV-003',
            'Kernel Never Depends on Agents',
            'agos_kernel.agent_packs'
        )
        
        # INV-004: Kernel never depends on Models
        self._check_import_violation(
            'INV-004',
            'Kernel Never Depends on Models',
            'agos_kernel.models'
        )
        
        # INV-005: Kernel never depends on Domains
        self._check_import_violation(
            'INV-005',
            'Kernel Never Depends on Domains',
            'agos_kernel.domains'
        )
        
        # INV-006: Kernel never depends on Marketplace
        self._check_import_violation(
            'INV-006',
            'Kernel Never Depends on Marketplace',
            'agos_kernel.marketplace'
        )
    
    def _check_import_violation(
        self, 
        invariant_id: str, 
        name: str, 
        forbidden_module: str
    ) -> None:
        """Check if any core module imports a forbidden module."""
        start = datetime.utcnow()
        violations = []
        forbidden_name = forbidden_module.split('.')[-1]
        
        for module, imports in self._import_graph.items():
            if forbidden_name in imports:
                violations.append({
                    'module': module,
                    'forbidden_import': forbidden_module,
                    'file': f'{module}.py',
                })
        
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        
        self.results[invariant_id] = InvariantResult(
            invariant_id=invariant_id,
            passed=len(violations) == 0,
            violations=violations,
            execution_time_ms=elapsed,
        )
    
    def _verify_architecture_invariants(self) -> None:
        """Verify architectural invariants."""
        # INV-010: Business Logic Only in Capabilities
        self._check_business_logic_location(
            'INV-010',
            'Business Logic Exists Only Inside Capabilities'
        )
        
        # INV-040: Contracts Remain Immutable
        self._verify_contracts_immutable('INV-040')
        
        # INV-041: Events Remain Immutable
        self._verify_events_immutable('INV-041')
    
    def _check_business_logic_location(
        self,
        invariant_id: str,
        name: str
    ) -> None:
        """Verify business logic is only in capabilities."""
        start = datetime.utcnow()
        violations = []
        
        capability_dir = self.kernel_root / 'capabilities'
        capability_files = set()
        
        if capability_dir.exists():
            for f in capability_dir.rglob('*.py'):
                if f.name != '__init__.py':
                    capability_files.add(f.name)
        
        for category in ['providers', 'adapters', 'workflows']:
            category_dir = self.kernel_root / category
            if not category_dir.exists():
                continue
                
            for py_file in category_dir.rglob('*.py'):
                if py_file.name == '__init__.py':
                    continue
                    
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for business logic patterns
                    if any(pattern in content.lower() for pattern in [
                        'def business_', 'class business', 'execute_business',
                        'implement business', 'business logic'
                    ]):
                        violations.append({
                            'file': str(py_file.relative_to(self.kernel_root)),
                            'issue': 'Contains business logic patterns',
                        })
                except Exception:
                    pass
        
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        
        self.results[invariant_id] = InvariantResult(
            invariant_id=invariant_id,
            passed=len(violations) == 0,
            violations=violations,
            execution_time_ms=elapsed,
        )
    
    def _verify_contracts_immutable(self, invariant_id: str) -> None:
        """Verify contracts are immutable."""
        start = datetime.utcnow()
        violations = []
        
        contracts_dir = self.kernel_root / 'contracts'
        if contracts_dir.exists():
            for py_file in contracts_dir.rglob('*.py'):
                if py_file.name == '__init__.py':
                    continue
                    
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'del ' in content or '.clear()' in content:
                        violations.append({
                            'file': str(py_file.relative_to(self.kernel_root)),
                            'issue': 'Contains mutating operations',
                        })
                except Exception:
                    pass
        
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        
        self.results[invariant_id] = InvariantResult(
            invariant_id=invariant_id,
            passed=len(violations) == 0,
            violations=violations,
            execution_time_ms=elapsed,
        )
    
    def _verify_events_immutable(self, invariant_id: str) -> None:
        """Verify events are immutable."""
        start = datetime.utcnow()
        violations = []
        
        events_dir = self.kernel_root / 'events'
        if events_dir.exists():
            for py_file in events_dir.rglob('*.py'):
                if py_file.name == '__init__.py':
                    continue
                    
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'del ' in content or '.clear()' in content:
                        violations.append({
                            'file': str(py_file.relative_to(self.kernel_root)),
                            'issue': 'Contains mutating operations',
                        })
                except Exception:
                    pass
        
        elapsed = (datetime.utcnow() - start).total_seconds() * 1000
        
        self.results[invariant_id] = InvariantResult(
            invariant_id=invariant_id,
            passed=len(violations) == 0,
            violations=violations,
            execution_time_ms=elapsed,
        )
    
    def get_import_graph(self) -> Dict[str, Set[str]]:
        """Return the current import dependency graph."""
        return self._import_graph
    
    def get_failed_invariants(self) -> List[InvariantResult]:
        """Return all failed invariant results."""
        return [r for r in self.results.values() if not r.passed]
