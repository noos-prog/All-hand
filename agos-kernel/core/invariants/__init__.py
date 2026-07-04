"""
AGOS Kernel Invariants System
EXECUTION-KERNEL-FINALIZATION-000002

This module establishes executable architectural invariants that protect
the Kernel's structural integrity and enforce its core principles.

Invariant Violation = Validation Failure
"""

from agos_kernel.core.invariants.runtime import InvariantRuntime
from agos_kernel.core.invariants.registry import InvariantRegistry
from agos_kernel.core.invariants.validator import InvariantValidator
from agos_kernel.core.invariants.reporter import InvariantReporter
from agos_kernel.core.invariants.evidence import EvidenceGenerator
from agos_kernel.core.invariants.benchmark import InvariantBenchmark

__all__ = [
    'InvariantRuntime',
    'InvariantRegistry', 
    'InvariantValidator',
    'InvariantReporter',
    'EvidenceGenerator',
    'InvariantBenchmark',
]

# Kernel Invariants Definition
KERNEL_INVARIANTS = [
    # Dependency Invariants - Kernel isolation from external components
    {
        'id': 'INV-001',
        'name': 'Kernel Never Depends on Extensions',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.extension',
        'severity': 'critical',
    },
    {
        'id': 'INV-002', 
        'name': 'Kernel Never Depends on Providers',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.providers',
        'severity': 'critical',
    },
    {
        'id': 'INV-003',
        'name': 'Kernel Never Depends on Agents',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.agent_packs',
        'severity': 'critical',
    },
    {
        'id': 'INV-004',
        'name': 'Kernel Never Depends on Models',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.models',
        'severity': 'critical',
    },
    {
        'id': 'INV-005',
        'name': 'Kernel Never Depends on Domains',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.domains',
        'severity': 'critical',
    },
    {
        'id': 'INV-006',
        'name': 'Kernel Never Depends on Marketplace',
        'category': 'dependency',
        'rule': 'agos_kernel.core must not import from agos_kernel.marketplace',
        'severity': 'critical',
    },
    
    # Business Logic Invariants - Isolation of concerns
    {
        'id': 'INV-010',
        'name': 'Business Logic Exists Only Inside Capabilities',
        'category': 'architecture',
        'rule': 'Business logic must reside exclusively in agos_kernel.capabilities',
        'severity': 'critical',
    },
    {
        'id': 'INV-011',
        'name': 'Providers Never Contain Business Logic',
        'category': 'architecture',
        'rule': 'agos_kernel.providers must only contain interface implementations',
        'severity': 'critical',
    },
    {
        'id': 'INV-012',
        'name': 'Adapters Never Contain Business Logic',
        'category': 'architecture',
        'rule': 'agos_kernel.adapters must only contain protocol conversions',
        'severity': 'critical',
    },
    
    # Orchestration Invariants
    {
        'id': 'INV-020',
        'name': 'Workflows Orchestrate Only',
        'category': 'orchestration',
        'rule': 'agos_kernel.workflows must not contain business logic',
        'severity': 'high',
    },
    
    # Atomicity Invariants
    {
        'id': 'INV-030',
        'name': 'Skills Remain Atomic',
        'category': 'composition',
        'rule': 'Each skill in agos_kernel.skills must be single-responsibility',
        'severity': 'medium',
    },
    
    # Immutability Invariants
    {
        'id': 'INV-040',
        'name': 'Contracts Remain Immutable',
        'category': 'immutability',
        'rule': 'Contract definitions cannot be modified after definition',
        'severity': 'critical',
    },
    {
        'id': 'INV-041',
        'name': 'Events Remain Immutable',
        'category': 'immutability',
        'rule': 'Event definitions cannot be modified after definition',
        'severity': 'critical',
    },
    {
        'id': 'INV-042',
        'name': 'Artifacts Remain Immutable After Publication',
        'category': 'immutability',
        'rule': 'Published artifacts cannot be modified',
        'severity': 'critical',
    },
    
    # Knowledge Invariants
    {
        'id': 'INV-050',
        'name': 'Knowledge Never Executes Code',
        'category': 'security',
        'rule': 'agos_kernel.knowledge must not contain executable code',
        'severity': 'critical',
    },
    
    # Policy Invariants
    {
        'id': 'INV-060',
        'name': 'Policies Never Execute Business Logic',
        'category': 'policy',
        'rule': 'agos_kernel.policies must only contain rule definitions',
        'severity': 'high',
    },
    
    # Reproducibility Invariants
    {
        'id': 'INV-070',
        'name': 'Mission Graphs Remain Reproducible',
        'category': 'reproducibility',
        'rule': 'Mission execution graphs must be deterministic',
        'severity': 'high',
    },
    
    # Observability Invariants
    {
        'id': 'INV-080',
        'name': 'Execution Remains Observable',
        'category': 'observability',
        'rule': 'All kernel execution must emit observable events',
        'severity': 'high',
    },
    
    # State Transition Invariants
    {
        'id': 'INV-090',
        'name': 'Every State Transition Emits Events',
        'category': 'event_sourcing',
        'rule': 'Any state change must generate corresponding event',
        'severity': 'critical',
    },
    
    # Decision Invariants
    {
        'id': 'INV-100',
        'name': 'Every Decision Produces Evidence',
        'category': 'evidence',
        'rule': 'All decision points must generate auditable evidence',
        'severity': 'high',
    },
    
    # Artifact Invariants
    {
        'id': 'INV-110',
        'name': 'Every Execution Produces Artifacts',
        'category': 'artifact',
        'rule': 'All mission executions must produce output artifacts',
        'severity': 'medium',
    },
]
