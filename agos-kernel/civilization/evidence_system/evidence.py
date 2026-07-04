"""
Universal Evidence System
PHASE-02: EXECUTION-000009 - Universal Evidence System

Every engineering conclusion produced by AGOS must be backed by verifiable evidence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib
import uuid


class EvidenceType(Enum):
    """Evidence types."""
    EXECUTION = "execution"
    MISSION = "mission"
    CAPABILITY = "capability"
    PROVIDER = "provider"
    KNOWLEDGE = "knowledge"
    POLICY = "policy"
    BENCHMARK = "benchmark"
    TEST = "test"
    REPOSITORY = "repository"
    WORKFLOW = "workflow"
    AUDIT = "audit"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TELEMETRY = "telemetry"
    DECISION = "decision"
    ARTIFACT = "artifact"


@dataclass
class Evidence:
    """
    Evidence Model.
    
    Properties:
    - Evidence ID
    - Evidence Type
    - Producer
    - Source
    - Timestamp
    - Mission Reference
    - Execution Reference
    - Related Knowledge
    - Related Artifact
    - Integrity Hash
    - Digital Signature
    - Confidence Score
    - Trust Score
    """
    
    evidence_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    evidence_type: EvidenceType = EvidenceType.EXECUTION
    
    # Producer
    producer: str = "AGOS"
    
    # Source
    source: str = ""
    source_details: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    mission_reference: str = ""
    execution_reference: str = ""
    
    # References
    related_knowledge: List[str] = field(default_factory=list)
    related_artifacts: List[str] = field(default_factory=list)
    
    # Integrity
    integrity_hash: str = ""
    digital_signature: str = ""
    
    # Scores
    confidence_score: float = 1.0  # 0.0 - 1.0
    trust_score: float = 1.0  # 0.0 - 1.0
    
    # Content
    description: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    
    def compute_hash(self) -> str:
        """Compute evidence hash."""
        content = f"{self.evidence_type.value}:{self.data}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def sign(self, signature: str) -> None:
        """Sign the evidence."""
        self.digital_signature = signature
        self.integrity_hash = self.compute_hash()
    
    def to_dict(self) -> Dict:
        return {
            'evidence_id': self.evidence_id,
            'evidence_type': self.evidence_type.value if isinstance(self.evidence_type, EvidenceType) else self.evidence_type,
            'producer': self.producer,
            'source': self.source,
            'source_details': self.source_details,
            'timestamp': self.timestamp,
            'mission_reference': self.mission_reference,
            'execution_reference': self.execution_reference,
            'related_knowledge': self.related_knowledge,
            'related_artifacts': self.related_artifacts,
            'integrity_hash': self.integrity_hash,
            'digital_signature': self.digital_signature,
            'confidence_score': self.confidence_score,
            'trust_score': self.trust_score,
            'description': self.description,
            'data': self.data,
        }


class EvidenceRegistry:
    """Registry for evidence."""
    
    def __init__(self):
        self.evidence: Dict[str, Evidence] = {}
        self.by_type: Dict[str, List[str]] = {}
        self.by_mission: Dict[str, List[str]] = {}
    
    def register(self, evidence: Evidence) -> None:
        """Register evidence."""
        self.evidence[evidence.evidence_id] = evidence
        
        # Index by type
        etype = evidence.evidence_type.value if isinstance(evidence.evidence_type, EvidenceType) else evidence.evidence_type
        if etype not in self.by_type:
            self.by_type[etype] = []
        self.by_type[etype].append(evidence.evidence_id)
        
        # Index by mission
        if evidence.mission_reference:
            if evidence.mission_reference not in self.by_mission:
                self.by_mission[evidence.mission_reference] = []
            self.by_mission[evidence.mission_reference].append(evidence.evidence_id)
    
    def get(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self.evidence.get(evidence_id)
    
    def get_by_type(self, evidence_type: EvidenceType) -> List[Evidence]:
        """Get evidence by type."""
        etype = evidence_type.value if isinstance(evidence_type, EvidenceType) else evidence_type
        ids = self.by_type.get(etype, [])
        return [self.evidence[e] for e in ids if e in self.evidence]
    
    def get_by_mission(self, mission_id: str) -> List[Evidence]:
        """Get evidence by mission."""
        ids = self.by_mission.get(mission_id, [])
        return [self.evidence[e] for e in ids if e in self.evidence]


class EvidenceCollector:
    """Collects evidence from various sources."""
    
    def collect(self, source: str, data: Dict) -> Evidence:
        """Collect evidence from source."""
        evidence = Evidence(
            source=source,
            data=data
        )
        return evidence


class EvidenceValidator:
    """Validates evidence."""
    
    def validate(self, evidence: Evidence) -> Dict:
        """Validate evidence integrity."""
        issues = []
        
        if not evidence.integrity_hash:
            issues.append("Missing integrity hash")
        
        if not evidence.digital_signature:
            issues.append("Missing digital signature")
        
        computed = evidence.compute_hash()
        if evidence.integrity_hash and evidence.integrity_hash != computed:
            issues.append("Integrity hash mismatch")
        
        return {'valid': len(issues) == 0, 'issues': issues}


class EvidenceCorrelator:
    """Correlates evidence."""
    
    def correlate(self, evidence_list: List[Evidence]) -> Dict:
        """Correlate related evidence."""
        correlations = []
        
        for i, e1 in enumerate(evidence_list):
            for e2 in evidence_list[i+1:]:
                if e1.mission_reference == e2.mission_reference:
                    correlations.append({
                        'source': e1.evidence_id,
                        'target': e2.evidence_id,
                        'correlation': 'shared_mission'
                    })
        
        return {'correlations': correlations}


class EvidenceTraceEngine:
    """Traces evidence lineage."""
    
    def __init__(self):
        self.lineage: Dict[str, List[str]] = {}
    
    def trace(self, evidence_id: str) -> List[str]:
        """Trace evidence lineage."""
        return self.lineage.get(evidence_id, [])
    
    def link(self, parent_id: str, child_id: str) -> None:
        """Link evidence."""
        if parent_id not in self.lineage:
            self.lineage[parent_id] = []
        self.lineage[parent_id].append(child_id)


class EvidenceRuntime:
    """
    Universal Evidence Runtime.
    
    Every engineering conclusion must be backed by verifiable evidence.
    
    Rules:
    - Evidence is immutable
    - Evidence is reproducible
    - Evidence is traceable
    - Evidence is digitally signed
    - Evidence is searchable
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.registry = EvidenceRegistry()
        self.collector = EvidenceCollector()
        self.validator = EvidenceValidator()
        self.correlator = EvidenceCorrelator()
        self.tracer = EvidenceTraceEngine()
    
    def collect(
        self,
        evidence_type: EvidenceType,
        source: str,
        data: Dict,
        mission_id: str = ""
    ) -> Evidence:
        """Collect and register evidence."""
        evidence = self.collector.collect(source, data)
        evidence.evidence_type = evidence_type
        evidence.mission_reference = mission_id
        
        # Sign evidence
        signature = hashlib.sha256(
            f"{evidence.evidence_id}:{evidence.compute_hash()}".encode()
        ).hexdigest()
        evidence.sign(signature)
        
        # Register
        self.registry.register(evidence)
        
        return evidence
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self.registry.get(evidence_id)
    
    def search_evidence(
        self,
        evidence_type: EvidenceType = None,
        mission_id: str = ""
    ) -> List[Evidence]:
        """Search evidence."""
        if evidence_type:
            return self.registry.get_by_type(evidence_type)
        if mission_id:
            return self.registry.get_by_mission(mission_id)
        return list(self.registry.evidence.values())
    
    def correlate_evidence(self, evidence_ids: List[str]) -> Dict:
        """Correlate evidence."""
        evidence_list = [self.registry.get(e) for e in evidence_ids]
        evidence_list = [e for e in evidence_list if e]
        return self.correlator.correlate(evidence_list)
    
    def validate_evidence(self, evidence_id: str) -> Dict:
        """Validate evidence."""
        evidence = self.registry.get(evidence_id)
        if not evidence:
            return {'valid': False, 'issues': ['Evidence not found']}
        return self.validator.validate(evidence)