"""
Knowledge Graph Query Engine
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

Query the Knowledge Graph.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

from agos_kernel.civilization.knowledge_graph.knowledge_graph import KnowledgeGraph
from agos_kernel.civilization.knowledge_graph.nodes.base import GraphNode, NodeType
from agos_kernel.civilization.knowledge_graph.relationships import RelationshipType


class QueryType(Enum):
    """Query types."""
    FIND_NODE = "find_node"
    FIND_NODES = "find_nodes"
    FIND_PATH = "find_path"
    FIND_PATHS = "find_paths"
    TRAVERSE = "traverse"
    AGGREGATE = "aggregate"


@dataclass
class QueryResult:
    """Query result."""
    query_type: QueryType
    nodes: List[GraphNode] = field(default_factory=list)
    relationships: List[Any] = field(default_factory=list)
    paths: List[List[GraphNode]] = field(default_factory=list)
    aggregations: Dict[str, Any] = field(default_factory=dict)
    count: int = 0
    execution_time_ms: float = 0.0
    

class QueryEngine:
    """
    Query Engine for Knowledge Graph.
    
    Provides powerful querying capabilities:
    - Node queries
    - Relationship queries
    - Path finding
    - Aggregation
    """
    
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
    
    def find_node(
        self,
        node_type: Optional[NodeType] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        repository: Optional[str] = None,
        properties: Optional[Dict] = None,
    ) -> Optional[GraphNode]:
        """
        Find a single node matching criteria.
        """
        nodes = self.find_nodes(node_type, name, path, repository, properties)
        return nodes[0] if nodes else None
    
    def find_nodes(
        self,
        node_type: Optional[NodeType] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        repository: Optional[str] = None,
        properties: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[GraphNode]:
        """
        Find all nodes matching criteria.
        """
        results = []
        
        # Start with filtered set
        if node_type:
            node_ids = self.graph._node_type_index.get(node_type.value, set())
            candidates = [
                self.graph._nodes[nid] 
                for nid in node_ids 
                if nid in self.graph._nodes
            ]
        else:
            candidates = list(self.graph._nodes.values())
        
        # Apply filters
        for node in candidates:
            if name and name.lower() not in node.name.lower():
                continue
            
            if path and path not in node.path:
                continue
            
            if repository and repository != node.repository:
                continue
            
            if tags and not any(tag in node.metadata.tags for tag in tags):
                continue
            
            if properties:
                match = True
                for key, value in properties.items():
                    if not hasattr(node, key) or getattr(node, key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            results.append(node)
            
            if len(results) >= limit:
                break
        
        return results
    
    def find_by_relationship(
        self,
        node_id: str,
        relationship_type: RelationshipType,
        direction: str = "both",  # "outgoing", "incoming", "both"
    ) -> List[GraphNode]:
        """
        Find nodes by relationship.
        """
        results = []
        
        for rel in self.graph._relationships.values():
            if rel.type != relationship_type:
                continue
            
            if direction in ["outgoing", "both"]:
                if rel.source_id == node_id:
                    neighbor = self.graph._nodes.get(rel.target_id)
                    if neighbor:
                        results.append(neighbor)
            
            if direction in ["incoming", "both"]:
                if rel.target_id == node_id:
                    neighbor = self.graph._nodes.get(rel.source_id)
                    if neighbor:
                        results.append(neighbor)
        
        return results
    
    def find_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5,
        relationship_types: Optional[List[RelationshipType]] = None,
    ) -> Optional[List[GraphNode]]:
        """
        Find path between two nodes using BFS.
        """
        if source_id == target_id:
            node = self.graph._nodes.get(source_id)
            return [node] if node else None
        
        # BFS
        visited = {source_id}
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            # Get neighbors
            for rel in self.graph._relationships.values():
                if rel.source_id != current:
                    continue
                
                if relationship_types and rel.type not in relationship_types:
                    continue
                
                neighbor = rel.target_id
                
                if neighbor == target_id:
                    return [self.graph._nodes.get(nid) for nid in path + [target_id] if self.graph._nodes.get(nid)]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def find_all_paths(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5,
        max_paths: int = 10,
    ) -> List[List[GraphNode]]:
        """
        Find all paths between two nodes.
        """
        all_paths = []
        
        def dfs(current: str, path: List[str], visited: Set[str]):
            if len(all_paths) >= max_paths:
                return
            
            if current == target_id:
                all_paths.append(path.copy())
                return
            
            if len(path) > max_depth:
                return
            
            for rel in self.graph._relationships.values():
                if rel.source_id != current:
                    continue
                
                neighbor = rel.target_id
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        visited = {source_id}
        dfs(source_id, [source_id], visited)
        
        return [
            [self.graph._nodes.get(nid) for nid in path if self.graph._nodes.get(nid)]
            for path in all_paths
        ]
    
    def traverse(
        self,
        start_id: str,
        relationship_type: RelationshipType,
        direction: str = "outgoing",
        max_depth: int = 3,
    ) -> List[GraphNode]:
        """
        Traverse graph from a starting node.
        """
        visited = {start_id}
        current_level = [start_id]
        all_nodes = []
        
        for _ in range(max_depth):
            next_level = []
            
            for current in current_level:
                for rel in self.graph._relationships.values():
                    if rel.type != relationship_type:
                        continue
                    
                    if direction == "outgoing" and rel.source_id == current:
                        neighbor = rel.target_id
                    elif direction == "incoming" and rel.target_id == current:
                        neighbor = rel.source_id
                    else:
                        continue
                    
                    if neighbor not in visited:
                        visited.add(neighbor)
                        node = self.graph._nodes.get(neighbor)
                        if node:
                            all_nodes.append(node)
                            next_level.append(neighbor)
            
            current_level = next_level
        
        return all_nodes
    
    def aggregate(
        self,
        group_by: str = "type",
        metric: str = "count",
        filters: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Aggregate nodes/relationships.
        """
        results = {}
        
        if filters:
            nodes = self.find_nodes(**filters)
        else:
            nodes = list(self.graph._nodes.values())
        
        if group_by == "type":
            for node in nodes:
                key = node.type.value
                if key not in results:
                    results[key] = []
                results[key].append(node)
        
        elif group_by == "repository":
            for node in nodes:
                key = node.repository or "unknown"
                if key not in results:
                    results[key] = []
                results[key].append(node)
        
        elif group_by == "language":
            for node in nodes:
                key = node.language or "unknown"
                if key not in results:
                    results[key] = []
                results[key].append(node)
        
        # Compute metrics
        aggregations = {}
        for key, group in results.items():
            if metric == "count":
                aggregations[key] = len(group)
            elif metric == "loc":
                aggregations[key] = sum(n.lines_of_code for n in group if hasattr(n, 'lines_of_code'))
        
        return {
            'groups': {k: len(v) for k, v in results.items()},
            'aggregations': aggregations,
            'total': len(nodes),
        }
    
    def search(self, query: str, limit: int = 20) -> List[GraphNode]:
        """
        Full-text search across nodes.
        """
        query_lower = query.lower()
        results = []
        
        for node in self.graph._nodes.values():
            # Search in name
            if query_lower in node.name.lower():
                results.append((node, 1.0))
                continue
            
            # Search in description
            if node.description and query_lower in node.description.lower():
                results.append((node, 0.8))
                continue
            
            # Search in content
            if node.content and query_lower in node.content.lower():
                results.append((node, 0.6))
                continue
        
        # Sort by relevance
        results.sort(key=lambda x: x[1], reverse=True)
        
        return [node for node, _ in results[:limit]]
