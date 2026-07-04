"""AGOS Knowledge Base."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class KnowledgeObject:
    """A knowledge object."""
    id: str
    name: str
    category: str
    version: str = "1.0.0"
    description: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class KnowledgeBase:
    """Knowledge base for engineering patterns, glossaries, catalogs."""
    
    def __init__(self):
        """Initialize knowledge base."""
        self.objects: Dict[str, KnowledgeObject] = {}
    
    def add(self, obj: KnowledgeObject) -> None:
        """Add a knowledge object."""
        self.objects[obj.id] = obj
    
    def get(self, obj_id: str) -> Optional[KnowledgeObject]:
        """Get a knowledge object."""
        return self.objects.get(obj_id)
    
    def search(self, query: str) -> List[KnowledgeObject]:
        """Search knowledge objects."""
        results = []
        query_lower = query.lower()
        for obj in self.objects.values():
            if query_lower in obj.name.lower() or query_lower in obj.description.lower():
                results.append(obj)
        return results
    
    def list_by_category(self, category: str) -> List[KnowledgeObject]:
        """List objects by category."""
        return [obj for obj in self.objects.values() if obj.category == category]


# Initialize with pattern libraries
_knowledge_base = KnowledgeBase()

# Architecture Patterns
ARCHITECTURE_PATTERNS = [
    KnowledgeObject(
        id="pattern-layered", name="Layered Architecture",
        category="architecture", description="Organize code into layers",
        content={"layers": ["presentation", "business", "data"]}
    ),
    KnowledgeObject(
        id="pattern-microservices", name="Microservices Architecture",
        category="architecture", description="Decompose into small services",
        content={"services": "independent", "communication": "api"}
    ),
    KnowledgeObject(
        id="pattern-event-driven", name="Event-Driven Architecture",
        category="architecture", description="React to events asynchronously",
        content={"events": "first-class", "decoupling": True}
    ),
    KnowledgeObject(
        id="pattern-hexagonal", name="Hexagonal Architecture",
        category="architecture", description="Ports and adapters pattern",
        content={"ports": "abstractions", "adapters": "implementations"}
    ),
    KnowledgeObject(
        id="pattern-clean", name="Clean Architecture",
        category="architecture", description="Independent frameworks",
        content={"entities": "enterprise", "usecases": "application"}
    ),
]

# Design Patterns
DESIGN_PATTERNS = [
    KnowledgeObject(
        id="pattern-singleton", name="Singleton",
        category="design", description="One instance only"
    ),
    KnowledgeObject(
        id="pattern-factory", name="Factory Method",
        category="design", description="Create objects without specifying class"
    ),
    KnowledgeObject(
        id="pattern-observer", name="Observer",
        category="design", description="Notify dependents of state changes"
    ),
    KnowledgeObject(
        id="pattern-strategy", name="Strategy",
        category="design", description="Select algorithms at runtime"
    ),
    KnowledgeObject(
        id="pattern-decorator", name="Decorator",
        category="design", description="Add behavior dynamically"
    ),
]

# Cloud Patterns
CLOUD_PATTERNS = [
    KnowledgeObject(
        id="pattern-circuit-breaker", name="Circuit Breaker",
        category="cloud", description="Prevent cascading failures"
    ),
    KnowledgeObject(
        id="pattern-bulkhead", name="Bulkhead",
        category="cloud", description="Isolate failures"
    ),
    KnowledgeObject(
        id="pattern-retry", name="Retry",
        category="cloud", description="Handle transient failures"
    ),
    KnowledgeObject(
        id="pattern-throttling", name="Throttling",
        category="cloud", description="Limit request rates"
    ),
]

# Security Patterns
SECURITY_PATTERNS = [
    KnowledgeObject(
        id="pattern-zero-trust", name="Zero Trust",
        category="security", description="Never trust, always verify"
    ),
    KnowledgeObject(
        id="pattern-defense-depth", name="Defense in Depth",
        category="security", description="Multiple layers of security"
    ),
    KnowledgeObject(
        id="pattern-least-priv", name="Least Privilege",
        category="security", description="Minimum access required"
    ),
]

# Performance Patterns
PERFORMANCE_PATTERNS = [
    KnowledgeObject(
        id="pattern-caching", name="Caching",
        category="performance", description="Store frequently accessed data"
    ),
    KnowledgeObject(
        id="pattern-pagination", name="Pagination",
        category="performance", description="Load data in chunks"
    ),
    KnowledgeObject(
        id="pattern-async", name="Async Processing",
        category="performance", description="Process in background"
    ),
]

# Register all patterns
for obj in ARCHITECTURE_PATTERNS + DESIGN_PATTERNS + CLOUD_PATTERNS + SECURITY_PATTERNS + PERFORMANCE_PATTERNS:
    _knowledge_base.add(obj)


def get_knowledge_base() -> KnowledgeBase:
    """Get the global knowledge base."""
    return _knowledge_base