"""AGOS Universal Engineering Ontology - Engineering concepts as first-class citizens."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import uuid

ENGINEERING_CONCEPTS = [
    "Projects", "Repositories", "Modules", "Packages", "Components", "Services",
    "Capabilities", "Skills", "Providers", "Agents", "Models", "Workflows",
    "Policies", "Artifacts", "Knowledge", "Missions", "Executions", "Events"
]


class ConceptType(Enum):
    """Types of concepts in the ontology."""
    PROJECT = "project"
    REPOSITORY = "repository"
    MODULE = "module"
    CAPABILITY = "capability"
    AGENT = "agent"
    MODEL = "model"
    WORKFLOW = "workflow"
    POLICY = "policy"
    ARTIFACT = "artifact"
    MISSION = "mission"


class RelationType(Enum):
    """Types of relations between concepts."""
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    USES = "uses"
    CREATES = "creates"
    MANAGES = "manages"
    HAS_CAPABILITY = "has_capability"
    PROVIDES = "provides"


@dataclass
class Concept:
    """A concept in the engineering ontology."""
    concept_id: str
    name: str
    concept_type: ConceptType
    description: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConceptRelation:
    """A relation between two concepts."""
    relation_id: str
    source_id: str
    target_id: str
    relation_type: RelationType
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyNode:
    """A node in the ontology graph."""
    node_id: str
    concept: Concept
    relations: List[ConceptRelation] = field(default_factory=list)
    embedding: Optional[List[float]] = None


class EngineeringOntology:
    """
    Universal Engineering Ontology.
    
    Concepts:
    ✅ Projects, Repositories, Modules, Packages, Components, Services
    ✅ Capabilities, Skills, Providers, Agents, Models, Workflows
    ✅ Policies, Artifacts, Knowledge, Missions, Executions, Events
    
    Target: Engineering Ontology v1
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[ConceptRelation] = []
        self._build_default_ontology()
    
    def _build_default_ontology(self) -> None:
        """Build the default engineering ontology."""
        for concept_name in ENGINEERING_CONCEPTS:
            concept_type = self._get_concept_type(concept_name)
            concept = Concept(
                concept_id=str(uuid.uuid4()),
                name=concept_name,
                concept_type=concept_type,
                description=f"Engineering concept: {concept_name}",
            )
            self.concepts[concept_id] = concept
    
    def _get_concept_type(self, name: str) -> ConceptType:
        """Get the concept type for a name."""
        name_lower = name.lower()
        if "project" in name_lower:
            return ConceptType.PROJECT
        if "repository" in name_lower:
            return ConceptType.REPOSITORY
        if "module" in name_lower:
            return ConceptType.MODULE
        if "capability" in name_lower or "skill" in name_lower:
            return ConceptType.CAPABILITY
        if "agent" in name_lower:
            return ConceptType.AGENT
        if "model" in name_lower:
            return ConceptType.MODEL
        if "workflow" in name_lower:
            return ConceptType.WORKFLOW
        if "policy" in name_lower:
            return ConceptType.POLICY
        if "artifact" in name_lower:
            return ConceptType.ARTIFACT
        if "mission" in name_lower:
            return ConceptType.MISSION
        return ConceptType.MODULE
    
    def add_concept(self, concept: Concept) -> None:
        """Add a concept to the ontology."""
        self.concepts[concept.concept_id] = concept
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get a concept by ID."""
        return self.concepts.get(concept_id)
    
    def add_relation(self, relation: ConceptRelation) -> None:
        """Add a relation between concepts."""
        self.relations.append(relation)
    
    def find_concepts(self, query: str, limit: int = 10) -> List[Concept]:
        """Find concepts matching a query."""
        results = []
        query_lower = query.lower()
        for concept in self.concepts.values():
            if query_lower in concept.name.lower() or query_lower in concept.description.lower():
                results.append(concept)
        return results[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "concepts": len(self.concepts),
            "relations": len(self.relations),
            "concept_types": len(ConceptType),
        }
