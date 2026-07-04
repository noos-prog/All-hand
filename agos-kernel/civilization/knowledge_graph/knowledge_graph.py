"""
Knowledge Graph Runtime
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

The central Knowledge Graph that serves as the source of truth.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict
import json
from pathlib import Path

from agos_kernel.civilization.knowledge_graph.nodes.base import (
    GraphNode, NodeType, NodeMetadata
)

try:
    from agos_kernel.civilization.knowledge_graph.relationships import (
        Relationship, RelationshipType, RelationshipMetadata
    )
except ImportError:
    # Will be loaded later
    Relationship = None
    RelationshipType = None
    RelationshipMetadata = None


@dataclass
class GraphStatistics:
    """Graph statistics."""
    total_nodes: int = 0
    total_relationships: int = 0
    node_types: Dict[str, int] = field(default_factory=dict)
    relationship_types: Dict[str, int] = field(default_factory=dict)
    nodes_by_repository: Dict[str, int] = field(default_factory=dict)


@dataclass
class GraphVersion:
    """Graph version for immutability."""
    version: int = 1
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    snapshot_hash: str = ""
    changes: List[Dict] = field(default_factory=list)


class KnowledgeGraph:
    """
    Knowledge Graph Runtime.
    
    The central source of truth for all engineering knowledge.
    
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
    
    VERSION = "2.0.0"
    
    def __init__(self, name: str = "main"):
        self.name = name
        self.created_at = datetime.utcnow()
        
        # Node storage: id -> GraphNode
        self._nodes: Dict[str, GraphNode] = {}
        
        # Relationship storage: id -> Relationship
        self._relationships: Dict[str, Relationship] = {}
        
        # Indexes for fast lookups
        self._node_type_index: Dict[str, Set[str]] = defaultdict(set)
        self._node_name_index: Dict[str, Set[str]] = defaultdict(set)
        self._node_repo_index: Dict[str, Set[str]] = defaultdict(set)
        self._node_path_index: Dict[str, Set[str]] = defaultdict(set)
        
        # Relationship indexes
        self._rel_type_index: Dict[str, Set[str]] = defaultdict(set)
        self._rel_source_index: Dict[str, Set[str]] = defaultdict(set)
        self._rel_target_index: Dict[str, Set[str]] = defaultdict(set)
        
        # Version tracking
        self._versions: List[GraphVersion] = []
        self._current_version = GraphVersion()
        
        # Statistics
        self._stats = GraphStatistics()
    
    # ============ Node Operations ============
    
    def add_node(self, node: GraphNode) -> str:
        """
        Add a node to the graph.
        
        Returns node ID.
        """
        # Generate ID if not set
        if not node.id:
            node.id = node.generate_id()
        
        # Store node
        self._nodes[node.id] = node
        
        # Update indexes
        self._node_type_index[node.type.value].add(node.id)
        self._node_name_index[node.name.lower()].add(node.id)
        
        if node.repository:
            self._node_repo_index[node.repository].add(node.id)
        
        if node.path:
            self._node_path_index[node.path].add(node.id)
        
        # Update statistics
        self._stats.total_nodes = len(self._nodes)
        self._stats.node_types[node.type.value] = \
            self._node_type_index[node.type.value]
        
        # Track change
        self._current_version.changes.append({
            'type': 'add_node',
            'id': node.id,
            'node_type': node.type.value,
            'timestamp': datetime.utcnow().isoformat(),
        })
        
        return node.id
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        return self._nodes.get(node_id)
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[GraphNode]:
        """Get all nodes of a specific type."""
        node_ids = self._node_type_index.get(node_type.value, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]
    
    def get_nodes_by_name(self, name: str) -> List[GraphNode]:
        """Get all nodes with a specific name."""
        node_ids = self._node_name_index.get(name.lower(), set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]
    
    def get_nodes_by_repository(self, repository: str) -> List[GraphNode]:
        """Get all nodes in a repository."""
        node_ids = self._node_repo_index.get(repository, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]
    
    def update_node(self, node_id: str, updates: Dict) -> bool:
        """Update a node."""
        node = self._nodes.get(node_id)
        if not node:
            return False
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        node.metadata.updated_at = datetime.utcnow().isoformat()
        node.metadata.version += 1
        
        # Track change
        self._current_version.changes.append({
            'type': 'update_node',
            'id': node_id,
            'timestamp': datetime.utcnow().isoformat(),
        })
        
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """Delete a node and its relationships."""
        node = self._nodes.pop(node_id, None)
        if not node:
            return False
        
        # Remove from indexes
        self._node_type_index[node.type.value].discard(node_id)
        self._node_name_index[node.name.lower()].discard(node_id)
        self._node_repo_index[node.repository].discard(node_id)
        
        if node.path:
            self._node_path_index[node.path].discard(node_id)
        
        # Remove related relationships
        to_delete = []
        for rel_id, rel in self._relationships.items():
            if rel.source_id == node_id or rel.target_id == node_id:
                to_delete.append(rel_id)
        
        for rel_id in to_delete:
            self._delete_relationship(rel_id)
        
        # Update statistics
        self._stats.total_nodes = len(self._nodes)
        
        # Track change
        self._current_version.changes.append({
            'type': 'delete_node',
            'id': node_id,
            'timestamp': datetime.utcnow().isoformat(),
        })
        
        return True
    
    # ============ Relationship Operations ============
    
    def add_relationship(self, relationship: Relationship) -> str:
        """
        Add a relationship to the graph.
        
        Returns relationship ID.
        """
        if not relationship.id:
            relationship.id = str(uuid.uuid4())
        
        # Store relationship
        self._relationships[relationship.id] = relationship
        
        # Update indexes
        self._rel_type_index[relationship.type.value].add(relationship.id)
        self._rel_source_index[relationship.source_id].add(relationship.id)
        self._rel_target_index[relationship.target_id].add(relationship.id)
        
        # Update statistics
        self._stats.total_relationships = len(self._relationships)
        
        # Track change
        self._current_version.changes.append({
            'type': 'add_relationship',
            'id': relationship.id,
            'rel_type': relationship.type.value,
            'source': relationship.source_id,
            'target': relationship.target_id,
            'timestamp': datetime.utcnow().isoformat(),
        })
        
        return relationship.id
    
    def _delete_relationship(self, rel_id: str) -> bool:
        """Internal delete without tracking."""
        rel = self._relationships.pop(rel_id, None)
        if not rel:
            return False
        
        # Remove from indexes
        self._rel_type_index[rel.type.value].discard(rel_id)
        self._rel_source_index[rel.source_id].discard(rel_id)
        self._rel_target_index[rel.target_id].discard(rel_id)
        
        self._stats.total_relationships = len(self._relationships)
        
        return True
    
    def get_relationship(self, rel_id: str) -> Optional[Relationship]:
        """Get a relationship by ID."""
        return self._relationships.get(rel_id)
    
    def get_relationships_by_node(self, node_id: str) -> List[Relationship]:
        """Get all relationships for a node."""
        rel_ids = self._rel_source_index.get(node_id, set()) | \
                  self._rel_target_index.get(node_id, set())
        return [self._relationships[rid] for rid in rel_ids if rid in self._relationships]
    
    def get_relationships_by_type(self, rel_type: RelationshipType) -> List[Relationship]:
        """Get all relationships of a specific type."""
        rel_ids = self._rel_type_index.get(rel_type.value, set())
        return [self._relationships[rid] for rid in rel_ids if rid in self._relationships]
    
    # ============ Traversal ============
    
    def get_neighbors(self, node_id: str, relationship_type: Optional[RelationshipType] = None) -> List[GraphNode]:
        """
        Get neighboring nodes.
        
        Args:
            node_id: Starting node ID
            relationship_type: Optional filter by relationship type
            
        Returns:
            List of neighboring nodes
        """
        neighbors = []
        
        # Outgoing relationships
        for rel_id in self._rel_source_index.get(node_id, set()):
            rel = self._relationships.get(rel_id)
            if rel and (relationship_type is None or rel.type == relationship_type):
                neighbor = self._nodes.get(rel.target_id)
                if neighbor:
                    neighbors.append(neighbor)
        
        # Incoming relationships
        for rel_id in self._rel_target_index.get(node_id, set()):
            rel = self._relationships.get(rel_id)
            if rel and (relationship_type is None or rel.type == relationship_type):
                neighbor = self._nodes.get(rel.source_id)
                if neighbor:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def get_dependents(self, node_id: str) -> List[GraphNode]:
        """Get all nodes that depend on this node."""
        dependents = []
        
        for rel in self._relationships.values():
            if rel.target_id == node_id and rel.type == RelationshipType.DEPENDS_ON:
                dependent = self._nodes.get(rel.source_id)
                if dependent:
                    dependents.append(dependent)
        
        return dependents
    
    def get_dependencies(self, node_id: str) -> List[GraphNode]:
        """Get all nodes this node depends on."""
        dependencies = []
        
        for rel in self._relationships.values():
            if rel.source_id == node_id and rel.type == RelationshipType.DEPENDS_ON:
                dependency = self._nodes.get(rel.target_id)
                if dependency:
                    dependencies.append(dependency)
        
        return dependencies
    
    # ============ Versioning ============
    
    def create_version(self) -> GraphVersion:
        """Create a new version snapshot."""
        version = GraphVersion(
            version=len(self._versions) + 1,
            timestamp=datetime.utcnow().isoformat(),
            snapshot_hash=self._compute_hash(),
            changes=self._current_version.changes.copy(),
        )
        
        self._versions.append(version)
        self._current_version = GraphVersion(version=version.version + 1)
        
        return version
    
    def get_version(self, version: int) -> Optional[GraphVersion]:
        """Get a specific version."""
        for v in self._versions:
            if v.version == version:
                return v
        return None
    
    def get_versions(self) -> List[GraphVersion]:
        """Get all versions."""
        return self._versions.copy()
    
    def _compute_hash(self) -> str:
        """Compute hash of current graph state."""
        import hashlib
        content = json.dumps(self.to_dict(), sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()
    
    # ============ Statistics ============
    
    def get_statistics(self) -> GraphStatistics:
        """Get graph statistics."""
        self._stats.total_nodes = len(self._nodes)
        self._stats.total_relationships = len(self._relationships)
        
        # Recount types
        self._stats.node_types = {
            ntype: len(nids) 
            for ntype, nids in self._node_type_index.items()
        }
        
        self._stats.relationship_types = {
            rtype: len(rids)
            for rtype, rids in self._rel_type_index.items()
        }
        
        return self._stats
    
    # ============ Serialization ============
    
    def to_dict(self) -> Dict:
        """Export graph to dictionary."""
        return {
            'name': self.name,
            'version': self.VERSION,
            'created_at': self.created_at.isoformat(),
            'nodes': {
                nid: node.to_dict() 
                for nid, node in self._nodes.items()
            },
            'relationships': {
                rid: rel.to_dict()
                for rid, rel in self._relationships.items()
            },
            'statistics': self.get_statistics().__dict__,
        }
    
    def save(self, path: str) -> None:
        """Save graph to file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
        
        print(f"Knowledge Graph saved to: {path}")
    
    @classmethod
    def load(cls, path: str) -> 'KnowledgeGraph':
        """Load graph from file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        graph = cls(name=data.get('name', 'loaded'))
        
        # Load nodes
        for nid, node_data in data.get('nodes', {}).items():
            node = GraphNode.from_dict(node_data)
            graph._nodes[nid] = node
            
            # Rebuild indexes
            graph._node_type_index[node.type.value].add(nid)
            graph._node_name_index[node.name.lower()].add(nid)
            if node.repository:
                graph._node_repo_index[node.repository].add(nid)
            if node.path:
                graph._node_path_index[node.path].add(nid)
        
        # Load relationships
        for rid, rel_data in data.get('relationships', {}).items():
            rel = Relationship.from_dict(rel_data)
            graph._relationships[rid] = rel
            
            # Rebuild indexes
            graph._rel_type_index[rel.type.value].add(rid)
            graph._rel_source_index[rel.source_id].add(rid)
            graph._rel_target_index[rel.target_id].add(rid)
        
        return graph
    
    def __len__(self) -> int:
        """Number of nodes in graph."""
        return len(self._nodes)
    
    def __repr__(self) -> str:
        return f"KnowledgeGraph(name={self.name}, nodes={len(self._nodes)}, relationships={len(self._relationships)})"


import uuid
