"""
Base Node Classes
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid
import hashlib


class NodeType(Enum):
    """First-class node types."""
    # Repository level
    REPOSITORY = "repository"
    WORKSPACE = "workspace"
    ORGANIZATION = "organization"
    PROJECT = "project"
    
    # Module level
    MODULE = "module"
    PACKAGE = "package"
    SERVICE = "service"
    COMPONENT = "component"
    
    # File level
    DIRECTORY = "directory"
    FILE = "file"
    
    # Code level
    CLASS = "class"
    INTERFACE = "interface"
    TRAIT = "trait"
    STRUCT = "struct"
    ENUM = "enum"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    
    # Data level
    CONFIGURATION = "configuration"
    ENVIRONMENT = "environment"
    DATABASE = "database"
    SCHEMA = "schema"
    TABLE = "table"
    COLUMN = "column"
    
    # API level
    API = "api"
    ENDPOINT = "endpoint"
    EVENT = "event"
    MESSAGE = "message"
    QUEUE = "queue"
    TOPIC = "topic"
    
    # Process level
    WORKFLOW = "workflow"
    MISSION = "mission"
    CAPABILITY = "capability"
    SKILL = "skill"
    
    # Integration level
    PROVIDER = "provider"
    ADAPTER = "adapter"
    POLICY = "policy"
    
    # Knowledge level
    KNOWLEDGE_OBJECT = "knowledge_object"
    ARTIFACT = "artifact"
    BENCHMARK = "benchmark"
    CERTIFICATION = "certification"
    TEMPLATE = "template"


@dataclass
class NodeMetadata:
    """Node metadata."""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'version': self.version,
            'tags': self.tags,
            'properties': self.properties,
            'evidence': self.evidence,
        }


@dataclass
class GraphNode:
    """
    Base Graph Node.
    
    All engineering concepts are represented as nodes in the Knowledge Graph.
    """
    
    # Identification
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: NodeType = NodeType.KNOWLEDGE_OBJECT
    name: str = ""
    
    # Location
    path: str = ""  # File path or URI
    repository: str = ""  # Repository name
    workspace: str = ""  # Workspace path
    
    # Content
    content: str = ""  # Source code or content
    description: str = ""
    language: str = ""  # Programming language
    
    # Relationships
    imports: List[str] = field(default_factory=list)  # Node IDs
    depends_on: List[str] = field(default_factory=list)
    implements: List[str] = field(default_factory=list)
    extends: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    creates: List[str] = field(default_factory=list)
    consumes: List[str] = field(default_factory=list)
    produces: List[str] = field(default_factory=list)
    publishes: List[str] = field(default_factory=list)
    subscribes: List[str] = field(default_factory=list)
    owns: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    
    # Metrics
    lines_of_code: int = 0
    complexity: int = 0
    cyclomatic_complexity: int = 0
    
    # Metadata
    metadata: NodeMetadata = field(default_factory=NodeMetadata)
    
    def __post_init__(self):
        """Post initialization."""
        if not self.name and self.path:
            self.name = self.path.split('/')[-1]
    
    def generate_id(self) -> str:
        """Generate deterministic ID based on content."""
        content = f"{self.type.value}:{self.path}:{self.repository}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value,
            'name': self.name,
            'path': self.path,
            'repository': self.repository,
            'workspace': self.workspace,
            'content': self.content,
            'description': self.description,
            'language': self.language,
            'imports': self.imports,
            'depends_on': self.depends_on,
            'implements': self.implements,
            'extends': self.extends,
            'calls': self.calls,
            'creates': self.creates,
            'consumes': self.consumes,
            'produces': self.produces,
            'publishes': self.publishes,
            'subscribes': self.subscribes,
            'owns': self.owns,
            'references': self.references,
            'lines_of_code': self.lines_of_code,
            'complexity': self.complexity,
            'cyclomatic_complexity': self.cyclomatic_complexity,
            'metadata': self.metadata.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GraphNode':
        """Create from dictionary."""
        metadata = NodeMetadata(**data.get('metadata', {}))
        data['metadata'] = metadata
        data['type'] = NodeType(data['type'])
        return cls(**data)
    
    def add_evidence(self, evidence: str) -> None:
        """Add evidence to node."""
        self.metadata.evidence.append(evidence)
        self.metadata.updated_at = datetime.utcnow().isoformat()
        self.metadata.version += 1
    
    def add_tag(self, tag: str) -> None:
        """Add tag to node."""
        if tag not in self.metadata.tags:
            self.metadata.tags.append(tag)
            self.metadata.updated_at = datetime.utcnow().isoformat()
            self.metadata.version += 1


def create_node(node_type: NodeType, name: str, **kwargs) -> GraphNode:
    """Factory function to create nodes."""
    node = GraphNode(type=node_type, name=name, **kwargs)
    return node
