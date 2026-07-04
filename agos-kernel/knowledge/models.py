"""Universal Knowledge Fabric - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class KnowledgeType(Enum):
    """Knowledge type."""
    FACT = "fact"
    RULE = "rule"
    EVIDENCE = "evidence"
    PATTERN = "pattern"
    ANTI_PATTERN = "anti_pattern"
    ARCHITECTURE = "architecture"
    CONCEPT = "concept"
    RELATIONSHIP = "relationship"
    POLICY = "policy"
    BENCHMARK = "benchmark"
    STANDARD = "standard"
    ONTOLOGY = "ontology"
    PLAYBOOK = "playbook"
    RUNBOOK = "runbook"
    BEST_PRACTICE = "best_practice"
    LESSON = "lesson"
    DECISION = "decision"


class KnowledgeStatus(Enum):
    """Knowledge status."""
    DRAFT = "draft"
    VALIDATING = "validating"
    VALID = "valid"
    INVALID = "invalid"
    VERIFIED = "verified"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class EvidenceQuality(Enum):
    """Evidence quality."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"


@dataclass
class KnowledgeMetadata:
    """Knowledge metadata."""
    title: str
    description: str = ""
    authors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    license: str = ""
    version: str = "1.0.0"
    domain: str = ""
    language: str = "en"


@dataclass
class KnowledgeRelationship:
    """Relationship between knowledge items."""
    id: str
    source_id: str
    target_id: str
    relationship_type: str  # "depends_on", "related_to", "contradicts", "extends"
    weight: float = 1.0


@dataclass
class Evidence:
    """Evidence supporting a knowledge item."""
    id: str
    content: str
    source: str
    source_url: str = ""
    quality: EvidenceQuality = EvidenceQuality.MEDIUM
    collected_at: datetime = field(default_factory=datetime.now)
    verified: bool = False
    verified_by: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Validation:
    """Validation record for knowledge."""
    id: str
    validated_at: datetime
    validator: str
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class Knowledge:
    """Universal Knowledge."""
    id: str
    
    # Content
    knowledge_type: KnowledgeType
    metadata: KnowledgeMetadata
    
    # Status
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    
    # Evidence
    evidence: List[Evidence] = field(default_factory=list)
    
    # Relationships
    relationships: List[KnowledgeRelationship] = field(default_factory=list)
    related_to: List[str] = field(default_factory=list)  # Knowledge IDs
    
    # Validation
    validations: List[Validation] = field(default_factory=list)
    validation_count: int = 0
    
    # Content
    content: Dict[str, Any] = field(default_factory=dict)
    summary: str = ""
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    
    # Access
    visibility: str = "internal"  # internal, public, private
    
    # Telemetry
    usage_count: int = 0
    last_accessed: Optional[datetime] = None
    accuracy_score: float = 0.0
    
    # Graph
    graph_position: Optional[Dict[str, float]] = None  # x, y for visualization
    
    def add_evidence(self, evidence: Evidence) -> None:
        """Add evidence to knowledge."""
        self.evidence.append(evidence)
        self.updated_at = datetime.now()
    
    def validate(self, validator: str) -> bool:
        """Validate knowledge."""
        validation = Validation(
            id=f"{self.id}-val-{len(self.validations)}",
            validated_at=datetime.now(),
            validator=validator,
            is_valid=len(self.evidence) > 0,
        )
        
        if not self.evidence:
            validation.warnings.append("No evidence provided")
        
        self.validations.append(validation)
        self.validation_count += 1
        self.status = KnowledgeStatus.VALID if validation.is_valid else KnowledgeStatus.INVALID
        self.updated_at = datetime.now()
        
        return validation.is_valid
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.knowledge_type.value,
            "title": self.metadata.title,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class KnowledgeGraph:
    """Knowledge graph structure."""
    nodes: Dict[str, Knowledge] = field(default_factory=dict)
    edges: List[KnowledgeRelationship] = field(default_factory=list)
    adjacency: Dict[str, Set[str]] = field(default_factory=dict)
    
    def add_knowledge(self, knowledge: Knowledge) -> None:
        """Add knowledge to graph."""
        self.nodes[knowledge.id] = knowledge
        if knowledge.id not in self.adjacency:
            self.adjacency[knowledge.id] = set()
    
    def add_edge(self, relationship: KnowledgeRelationship) -> None:
        """Add edge to graph."""
        self.edges.append(relationship)
        
        # Update adjacency
        if relationship.source_id in self.adjacency:
            self.adjacency[relationship.source_id].add(relationship.target_id)
        else:
            self.adjacency[relationship.source_id] = {relationship.target_id}
    
    def get_connected(self, knowledge_id: str) -> List[str]:
        """Get connected knowledge IDs."""
        return list(self.adjacency.get(knowledge_id, set()))
    
    def get_subgraph(self, knowledge_ids: List[str]) -> "KnowledgeGraph":
        """Extract subgraph for given knowledge IDs."""
        subgraph = KnowledgeGraph()
        for kid in knowledge_ids:
            if kid in self.nodes:
                subgraph.add_knowledge(self.nodes[kid])
        for edge in self.edges:
            if edge.source_id in knowledge_ids and edge.target_id in knowledge_ids:
                subgraph.add_edge(edge)
        return subgraph
