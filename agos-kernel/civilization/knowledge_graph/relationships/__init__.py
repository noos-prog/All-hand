"""
Knowledge Graph Relationships
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

First-class relationships between nodes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class RelationshipType(Enum):
    """First-class relationship types."""
    # Structural
    CONTAINS = "contains"
    IMPORTS = "imports"
    DEPENDS_ON = "depends_on"
    
    # Inheritance
    IMPLEMENTS = "implements"
    EXTENDS = "extends"
    
    # Behavioral
    CALLS = "calls"
    CREATES = "creates"
    CONSUMES = "consumes"
    PRODUCES = "produces"
    PUBLISHES = "publishes"
    SUBSCRIBES = "subscribes"
    
    # Ownership
    OWNS = "owns"
    REFERENCES = "references"
    
    # Quality
    VALIDATES = "validates"
    VIOLATES = "violates"
    GENERATES = "generates"
    
    # Membership
    BELONGS_TO = "belongs_to"
    USES = "uses"
    
    # Security
    SECURES = "secures"
    CONFIGUREs = "configures"
    EXECUTES = "executes"


@dataclass
class RelationshipMetadata:
    """Relationship metadata."""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1
    evidence: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0  # 0.0 to 1.0
    
    def to_dict(self) -> Dict:
        return {
            'created_at': self.created_at,
            'version': self.version,
            'evidence': self.evidence,
            'properties': self.properties,
            'confidence': self.confidence,
        }


@dataclass
class Relationship:
    """
    Relationship between two nodes.
    
    First-class relationships in the Engineering Knowledge Graph.
    """
    
    # Identification
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: RelationshipType = RelationshipType.CONTAINS
    
    # Source and target
    source_id: str = ""  # Node ID
    target_id: str = ""  # Node ID
    source_name: str = ""
    target_name: str = ""
    
    # Properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    metadata: RelationshipMetadata = field(default_factory=RelationshipMetadata)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value,
            'source_id': self.source_id,
            'target_id': self.target_id,
            'source_name': self.source_name,
            'target_name': self.target_name,
            'properties': self.properties,
            'metadata': self.metadata.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Relationship':
        """Create from dictionary."""
        metadata = RelationshipMetadata(**data.get('metadata', {}))
        data['metadata'] = metadata
        data['type'] = RelationshipType(data['type'])
        return cls(**data)
    
    def add_evidence(self, evidence: str) -> None:
        """Add evidence to relationship."""
        self.metadata.evidence.append(evidence)
        self.metadata.version += 1


def create_relationship(
    rel_type: RelationshipType,
    source_id: str,
    target_id: str,
    source_name: str = "",
    target_name: str = "",
    **kwargs
) -> Relationship:
    """Factory function to create relationships."""
    return Relationship(
        type=rel_type,
        source_id=source_id,
        target_id=target_id,
        source_name=source_name,
        target_name=target_name,
        properties=kwargs,
    )
