"""
Knowledge Graph
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

Engineering Knowledge Graph - The central source of truth.

Requirements:
- Versioned
- Immutable History
- Queryable
- Searchable
- Diffable
- Traceable
- Observable
- Evidence-backed
"""

__version__ = "2.0.0"

from agos_kernel.civilization.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
    GraphStatistics,
    GraphVersion,
)
from agos_kernel.civilization.knowledge_graph.builder import (
    GraphBuilder,
    BuildResult,
)
from agos_kernel.civilization.knowledge_graph.nodes.base import (
    GraphNode,
    NodeType,
    NodeMetadata,
    create_node,
)
from agos_kernel.civilization.knowledge_graph.relationships import (
    Relationship,
    RelationshipType,
    RelationshipMetadata,
    create_relationship,
)

__all__ = [
    'KnowledgeGraph',
    'GraphStatistics',
    'GraphVersion',
    'GraphBuilder',
    'BuildResult',
    'GraphNode',
    'NodeType',
    'NodeMetadata',
    'create_node',
    'Relationship',
    'RelationshipType',
    'RelationshipMetadata',
    'create_relationship',
]
