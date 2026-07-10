#!/usr/bin/env python3
"""
AIE - Decision Graph
===================

Graph-based representation of decisions.
Nodes are decisions, edges are relationships.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime


class NodeType(Enum):
    """Types of decision nodes."""
    DECISION = "decision"
    ACTION = "action"
    OUTCOME = "outcome"
    STATE = "state"
    GOAL = "goal"


class EdgeType(Enum):
    """Types of edges between nodes."""
    CAUSES = "causes"
    ENABLES = "enables"
    PREVENTS = "prevents"
    LEADS_TO = "leads_to"
    DEPENDS_ON = "depends_on"


class TraversalType(Enum):
    """Types of graph traversal."""
    BFS = "breadth_first"
    DFS = "depth_first"
    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"


@dataclass
class DecisionNode:
    """
    A node in the decision graph.
    """
    node_id: str
    name: str
    node_type: NodeType
    
    # Content
    content: Dict[str, Any]
    value: float = 0.0               # Value/cost
    probability: float = 1.0          # Probability of reaching
    
    # Relationships
    parents: Tuple[str, ...] = ()
    children: Tuple[str, ...] = ()
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_parent(self, parent_id: str) -> None:
        """Add a parent node."""
        if parent_id not in self.parents:
            object.__setattr__(self, 'parents', self.parents + (parent_id,))
    
    def add_child(self, child_id: str) -> None:
        """Add a child node."""
        if child_id not in self.children:
            object.__setattr__(self, 'children', self.children + (child_id,))
    
    def get_score(self) -> float:
        """Calculate node score."""
        return self.value * self.probability


@dataclass
class DecisionEdge:
    """
    An edge between decision nodes.
    """
    edge_id: str
    from_node: str
    to_node: str
    edge_type: EdgeType
    
    # Edge properties
    weight: float = 1.0              # Cost/distance
    probability: float = 1.0          # Probability of traversing
    
    # Conditions
    condition: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_cost(self) -> float:
        """Calculate edge cost."""
        return self.weight * (1 - self.probability)


class DecisionGraph:
    """
    A graph of decision nodes and edges.
    """
    
    def __init__(self):
        self._nodes: Dict[str, DecisionNode] = {}
        self._edges: Dict[str, DecisionEdge] = {}
        self._adjacency: Dict[str, Set[str]] = {}  # Outgoing edges
        self._reverse_adjacency: Dict[str, Set[str]] = {}  # Incoming edges
        self._initialized = False
    
    def add_node(self, node: DecisionNode) -> str:
        """Add a node to the graph."""
        self._nodes[node.node_id] = node
        
        if node.node_id not in self._adjacency:
            self._adjacency[node.node_id] = set()
        if node.node_id not in self._reverse_adjacency:
            self._reverse_adjacency[node.node_id] = set()
        
        return node.node_id
    
    def add_edge(self, edge: DecisionEdge) -> str:
        """Add an edge to the graph."""
        self._edges[edge.edge_id] = edge
        
        # Update adjacency lists
        if edge.from_node not in self._adjacency:
            self._adjacency[edge.from_node] = set()
        if edge.to_node not in self._reverse_adjacency:
            self._reverse_adjacency[edge.to_node] = set()
        
        self._adjacency[edge.from_node].add(edge.to_node)
        self._reverse_adjacency[edge.to_node].add(edge.from_node)
        
        # Update node relationships
        if edge.from_node in self._nodes:
            self._nodes[edge.from_node].add_child(edge.to_node)
        if edge.to_node in self._nodes:
            self._nodes[edge.to_node].add_parent(edge.from_node)
        
        return edge.edge_id
    
    def get_node(self, node_id: str) -> Optional[DecisionNode]:
        """Get a node by ID."""
        return self._nodes.get(node_id)
    
    def get_edge(self, edge_id: str) -> Optional[DecisionEdge]:
        """Get an edge by ID."""
        return self._edges.get(edge_id)
    
    def get_neighbors(self, node_id: str) -> List[DecisionNode]:
        """Get all neighbors of a node."""
        neighbors = []
        for child_id in self._adjacency.get(node_id, set()):
            node = self._nodes.get(child_id)
            if node:
                neighbors.append(node)
        return neighbors
    
    def get_ancestors(self, node_id: str) -> Set[str]:
        """Get all ancestor node IDs."""
        visited = set()
        queue = list(self._reverse_adjacency.get(node_id, set()))
        
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                queue.extend(self._reverse_adjacency.get(current, set()))
        
        return visited
    
    def get_descendants(self, node_id: str) -> Set[str]:
        """Get all descendant node IDs."""
        visited = set()
        queue = list(self._adjacency.get(node_id, set()))
        
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                queue.extend(self._adjacency.get(current, set()))
        
        return visited
    
    def find_path(
        self,
        from_node: str,
        to_node: str,
        traversal: TraversalType = TraversalType.BFS
    ) -> Optional[List[str]]:
        """Find a path between two nodes."""
        if traversal == TraversalType.BFS:
            return self._bfs(from_node, to_node)
        elif traversal == TraversalType.DFS:
            return self._dfs(from_node, to_node)
        elif traversal == TraversalType.DIJKSTRA:
            return self._dijkstra(from_node, to_node)
        else:
            return self._bfs(from_node, to_node)
    
    def _bfs(self, from_node: str, to_node: str) -> Optional[List[str]]:
        """Breadth-first search."""
        if from_node not in self._nodes or to_node not in self._nodes:
            return None
        
        visited = {from_node}
        queue = [(from_node, [from_node])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == to_node:
                return path
            
            for neighbor in self._adjacency.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def _dfs(self, from_node: str, to_node: str) -> Optional[List[str]]:
        """Depth-first search."""
        if from_node not in self._nodes or to_node not in self._nodes:
            return None
        
        visited = set()
        
        def dfs_recursive(current: str, path: List[str]) -> Optional[List[str]]:
            if current == to_node:
                return path
            
            if current in visited:
                return None
            
            visited.add(current)
            
            for neighbor in self._adjacency.get(current, set()):
                result = dfs_recursive(neighbor, path + [neighbor])
                if result:
                    return result
            
            return None
        
        return dfs_recursive(from_node, [from_node])
    
    def _dijkstra(self, from_node: str, to_node: str) -> Optional[List[str]]:
        """Dijkstra's shortest path."""
        if from_node not in self._nodes or to_node not in self._nodes:
            return None
        
        distances = {from_node: 0}
        previous = {}
        unvisited = set(self._nodes.keys())
        
        while unvisited:
            # Find node with minimum distance
            current = min(unvisited, key=lambda n: distances.get(n, float('inf')))
            
            if distances.get(current, float('inf')) == float('inf'):
                break
            
            if current == to_node:
                break
            
            unvisited.remove(current)
            
            for neighbor in self._adjacency.get(current, set()):
                edge = self._get_edge_between(current, neighbor)
                if edge:
                    distance = distances[current] + edge.get_cost()
                    if distance < distances.get(neighbor, float('inf')):
                        distances[neighbor] = distance
                        previous[neighbor] = current
        
        # Reconstruct path
        if to_node not in previous and to_node != from_node:
            return None
        
        path = []
        current = to_node
        while current in previous:
            path.append(current)
            current = previous[current]
        path.append(from_node)
        
        return list(reversed(path))
    
    def _get_edge_between(self, from_node: str, to_node: str) -> Optional[DecisionEdge]:
        """Get edge between two nodes."""
        for edge in self._edges.values():
            if edge.from_node == from_node and edge.to_node == to_node:
                return edge
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        by_type = {}
        total_value = 0.0
        total_probability = 0.0
        
        for node in self._nodes.values():
            node_type = node.node_type.value
            by_type[node_type] = by_type.get(node_type, 0) + 1
            total_value += node.value
            total_probability += node.probability
        
        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "nodes_by_type": by_type,
            "total_value": round(total_value, 2),
            "average_probability": round(total_probability / len(self._nodes), 3) if self._nodes else 0,
        }


class PathFinder:
    """
    Utility for finding optimal paths in decision graphs.
    """
    
    def __init__(self, graph: DecisionGraph):
        self.graph = graph
    
    def find_best_path(
        self,
        from_node: str,
        to_node: str,
        optimize_for: str = "value"  # "value", "probability", "cost"
    ) -> Dict[str, Any]:
        """Find the best path considering optimization criteria."""
        path = self.graph.find_path(from_node, to_node, TraversalType.DIJKSTRA)
        
        if not path:
            return {"path": None, "total_value": 0, "probability": 0}
        
        total_value = 0.0
        path_probability = 1.0
        
        for i, node_id in enumerate(path):
            node = self.graph.get_node(node_id)
            if node:
                if optimize_for == "value":
                    total_value += node.value
                elif optimize_for == "probability":
                    path_probability *= node.probability
        
        return {
            "path": path,
            "total_value": round(total_value, 3),
            "probability": round(path_probability, 3),
            "node_count": len(path),
        }
    
    def rank_paths(
        self,
        from_node: str,
        to_node: str,
        max_paths: int = 10
    ) -> List[Dict[str, Any]]:
        """Rank all paths between two nodes."""
        all_paths = self._find_all_paths(from_node, to_node)
        
        ranked = []
        for path in all_paths[:max_paths]:
            total_value = 0.0
            path_prob = 1.0
            
            for node_id in path:
                node = self.graph.get_node(node_id)
                if node:
                    total_value += node.value
                    path_prob *= node.probability
            
            ranked.append({
                "path": path,
                "total_value": round(total_value, 3),
                "probability": round(path_prob, 3),
                "score": round(total_value * path_prob, 3),
            })
        
        # Sort by score
        ranked.sort(key=lambda x: x["score"], reverse=True)
        
        return ranked
    
    def _find_all_paths(
        self,
        from_node: str,
        to_node: str,
        current_path: List[str] = None,
        all_paths: List[List[str]] = None
    ) -> List[List[str]]:
        """Find all paths between two nodes."""
        if current_path is None:
            current_path = []
        if all_paths is None:
            all_paths = []
        
        current_path = current_path + [from_node]
        
        if from_node == to_node:
            all_paths.append(current_path)
            return all_paths
        
        for neighbor in self.graph._adjacency.get(from_node, set()):
            if neighbor not in current_path:
                self._find_all_paths(neighbor, to_node, current_path, all_paths)
        
        return all_paths


class GraphTraversal:
    """
    Utilities for traversing decision graphs.
    """
    
    def __init__(self, graph: DecisionGraph):
        self.graph = graph
    
    def traverse_bfs(
        self,
        start_node: str,
        visitor: Callable[[DecisionNode], bool] = None
    ) -> List[DecisionNode]:
        """Traverse graph BFS and optionally visit each node."""
        if start_node not in self.graph._nodes:
            return []
        
        visited = set()
        queue = [start_node]
        visited_order = []
        
        while queue:
            current = queue.pop(0)
            
            if current in visited:
                continue
            
            visited.add(current)
            node = self.graph.get_node(current)
            
            if node:
                visited_order.append(node)
                
                if visitor and visitor(node):
                    break
                
                for neighbor in self.graph._adjacency.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return visited_order
    
    def traverse_dfs(
        self,
        start_node: str,
        visitor: Callable[[DecisionNode], bool] = None
    ) -> List[DecisionNode]:
        """Traverse graph DFS and optionally visit each node."""
        if start_node not in self.graph._nodes:
            return []
        
        visited = set()
        visited_order = []
        
        def dfs(current: str):
            if current in visited:
                return
            
            visited.add(current)
            node = self.graph.get_node(current)
            
            if node:
                visited_order.append(node)
                
                if visitor and visitor(node):
                    return
                
                for neighbor in self.graph._adjacency.get(current, set()):
                    if neighbor not in visited:
                        dfs(neighbor)
        
        dfs(start_node)
        return visited_order
