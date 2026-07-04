"""Universal Evidence System"""

__version__ = "1.0"

from agos_kernel.civilization.evidence_system.evidence import (
    Evidence, EvidenceType, EvidenceRegistry,
    EvidenceCollector, EvidenceValidator, EvidenceCorrelator,
    EvidenceTraceEngine, EvidenceRuntime
)

__all__ = [
    'Evidence', 'EvidenceType', 'EvidenceRegistry',
    'EvidenceCollector', 'EvidenceValidator', 'EvidenceCorrelator',
    'EvidenceTraceEngine', 'EvidenceRuntime',
]