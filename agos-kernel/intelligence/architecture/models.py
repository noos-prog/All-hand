"""Data models for Architecture Intelligence."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class LayerType(Enum):
    """Architecture layer types."""
    PRESENTATION = "presentation"
    APPLICATION = "application"
    DOMAIN = "domain"
    INFRASTRUCTURE = "infrastructure"
    DATA = "data"
    EXTERNAL = "external"


class ComponentType(Enum):
    """Component types."""
    MODULE = "module"
    SERVICE = "service"
    CONTROLLER = "controller"
    REPOSITORY = "repository"
    FACTORY = "factory"
    BUILDER = "builder"
    STRATEGY = "strategy"
    ADAPTER = "adapter"
    FACADE = "facade"
    GATEWAY = "gateway"
    HANDLER = "handler"
    MIDDLEWARE = "middleware"
    WORKER = "worker"
    CONSUMER = "consumer"
    PRODUCER = "producer"


class BoundaryType(Enum):
    """Boundary types."""
    PUBLIC_API = "public_api"
    PRIVATE_API = "private_api"
    INTERNAL = "internal"
    EXTERNAL = "external"
    DOMAIN_BOUNDARY = "domain_boundary"
    SERVICE_BOUNDARY = "service_boundary"


class ArchitectureStyle(Enum):
    """Architecture styles."""
    MONOLITHIC = "monolithic"
    LAYERED = "layered"
    MICROSERVICE = "microservice"
    EVENT_DRIVEN = "event_driven"
    SERVERLESS = "serverless"
    HEXAGONAL = "hexagonal"
    ONION = "onion"
    CLEAN = "clean"
    CQRS = "cqrs"
    DDD = "ddd"
    UNKNOWN = "unknown"


@dataclass
class Layer:
    """Architecture layer."""
    name: str
    type: LayerType
    components: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    level: int = 0  # 0 = outermost, higher = inner


@dataclass
class Boundary:
    """Architecture boundary."""
    name: str
    type: BoundaryType
    components: List[str] = field(default_factory=list)
    exposed_apis: List[str] = field(default_factory=list)
    consumed_apis: List[str] = field(default_factory=list)


@dataclass
class Component:
    """Architecture component."""
    name: str
    type: ComponentType
    path: str
    layer: Optional[str] = None
    boundary: Optional[str] = None
    responsibilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)  # Who depends on this
    interfaces: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    policies: List[str] = field(default_factory=list)


@dataclass
class Interface:
    """Component interface."""
    name: str
    component: str
    type: str  # REST, GraphQL, gRPC, etc.
    methods: List[str] = field(default_factory=list)
    path: Optional[str] = None
    contracts: List[str] = field(default_factory=list)


@dataclass
class Contract:
    """Interface contract."""
    name: str
    interface: str
    version: str = "1.0.0"
    schema: Dict[str, Any] = field(default_factory=dict)
    policies: List[str] = field(default_factory=list)


@dataclass
class Event:
    """Domain event."""
    name: str
    component: str
    payload: Dict[str, Any] = field(default_factory=dict)
    published_by: str = ""
    consumed_by: List[str] = field(default_factory=list)


@dataclass
class Policy:
    """Architecture policy."""
    name: str
    description: str
    scope: str  # Component, layer, boundary, global
    rules: List[str] = field(default_factory=list)
    enforced: bool = True


@dataclass
class ArchitectureGraph:
    """Architecture dependency graph."""
    nodes: List[str] = field(default_factory=list)  # Component names
    edges: List[tuple] = field(default_factory=list)  # (source, target, type)
    layers: List[Layer] = field(default_factory=list)
    boundaries: List[Boundary] = field(default_factory=list)


@dataclass
class ArchitectureScore:
    """Architecture quality score."""
    overall: float = 0.0
    modularity: float = 0.0
    cohesion: float = 0.0
    coupling: float = 0.0
    maintainability: float = 0.0
    testability: float = 0.0
    reusability: float = 0.0


@dataclass
class ArchitectureViolation:
    """Architecture rule violation."""
    rule: str
    description: str
    severity: str = "warning"  # error, warning, info
    component: Optional[str] = None
    source: Optional[str] = None
    target: Optional[str] = None


@dataclass
class ArchitectureRisk:
    """Architecture risk."""
    name: str
    description: str
    severity: str  # high, medium, low
    affected_components: List[str] = field(default_factory=list)
    mitigation: str = ""


@dataclass
class ArchitectureGenome:
    """Complete DNA of architecture."""
    # Style
    style: ArchitectureStyle = ArchitectureStyle.UNKNOWN
    confidence: float = 0.0
    
    # Structure
    layers: List[Layer] = field(default_factory=list)
    boundaries: List[Boundary] = field(default_factory=list)
    components: Dict[str, Component] = field(default_factory=dict)
    
    # Contracts
    interfaces: List[Interface] = field(default_factory=list)
    contracts: List[Contract] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    
    # Graph
    graph: ArchitectureGraph = field(default_factory=ArchitectureGraph)
    
    # Quality
    score: ArchitectureScore = field(default_factory=ArchitectureScore)
    violations: List[ArchitectureViolation] = field(default_factory=list)
    risks: List[ArchitectureRisk] = field(default_factory=list)
    
    # Evolution
    evolution_timeline: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "style": self.style.value,
            "confidence": self.confidence,
            "layers_count": len(self.layers),
            "components_count": len(self.components),
            "score": {
                "overall": self.score.overall,
                "coupling": self.score.coupling,
                "cohesion": self.score.cohesion,
            },
            "violations_count": len(self.violations),
        }
