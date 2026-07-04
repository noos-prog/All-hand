"""
Execution Graph
PHASE-02: EXECUTION-000005 - Universal Mission Planner

Supports:
- Sequential Execution
- Parallel Execution
- Conditional Branches
- Loops
- Retries
- Timeouts
- Checkpoints
- Rollback
- Pause/Resume/Replay
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from enum import Enum
import uuid


class GraphNodeType(Enum):
    """Graph node types."""
    TASK = "task"
    SEQUENCE = "sequence"
    PARALLEL = "parallel"
    CONDITION = "condition"
    LOOP = "loop"
    CHECKPOINT = "checkpoint"
    ROLLBACK = "rollback"
    MERGE = "merge"


class EdgeType(Enum):
    """Graph edge types."""
    SEQUENCE = "sequence"
    PARALLEL = "parallel"
    CONDITIONAL_TRUE = "conditional_true"
    CONDITIONAL_FALSE = "conditional_false"
    LOOP_NEXT = "loop_next"
    LOOP_EXIT = "loop_exit"
    ERROR = "error"
    ROLLBACK = "rollback"


@dataclass
class GraphNode:
    """Graph node."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: GraphNodeType = GraphNodeType.TASK
    task_id: str = ""  # If type is TASK
    name: str = ""
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value if isinstance(self.type, GraphNodeType) else self.type,
            'task_id': self.task_id,
            'name': self.name,
            'metadata': self.metadata,
        }


@dataclass
class GraphEdge:
    """Graph edge."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_id: str = ""
    target_id: str = ""
    type: EdgeType = EdgeType.SEQUENCE
    condition: str = ""  # For conditional edges
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'source_id': self.source_id,
            'target_id': self.target_id,
            'type': self.type.value if isinstance(self.type, EdgeType) else self.type,
            'condition': self.condition,
            'metadata': self.metadata,
        }


class ExecutionGraph:
    """
    Execution Graph.
    
    Represents the execution plan as a directed graph.
    """
    
    def __init__(self, mission_id: str = ""):
        self.mission_id = mission_id
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.entry_point: Optional[str] = None
        self.exit_points: List[str] = []
        
        # Indexes
        self._task_index: Dict[str, str] = {}  # task_id -> node_id
        self._parallel_groups: List[Set[str]] = []
    
    def add_node(self, node: GraphNode) -> str:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        
        if node.task_id:
            self._task_index[node.task_id] = node.id
        
        return node.id
    
    def add_edge(self, edge: GraphEdge) -> str:
        """Add an edge to the graph."""
        self.edges[edge.id] = edge
        return edge.id
    
    def set_entry_point(self, node_id: str) -> None:
        """Set the entry point of the graph."""
        self.entry_point = node_id
    
    def add_exit_point(self, node_id: str) -> None:
        """Add an exit point of the graph."""
        if node_id not in self.exit_points:
            self.exit_points.append(node_id)
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_node_by_task(self, task_id: str) -> Optional[GraphNode]:
        """Get a node by task ID."""
        node_id = self._task_index.get(task_id)
        return self.nodes.get(node_id) if node_id else None
    
    def get_outgoing_edges(self, node_id: str) -> List[GraphEdge]:
        """Get outgoing edges from a node."""
        return [e for e in self.edges.values() if e.source_id == node_id]
    
    def get_incoming_edges(self, node_id: str) -> List[GraphEdge]:
        """Get incoming edges to a node."""
        return [e for e in self.edges.values() if e.target_id == node_id]
    
    def get_execution_order(self) -> List[List[str]]:
        """
        Get execution order as batches.
        
        Each batch contains nodes that can be executed in parallel.
        """
        if not self.entry_point:
            return []
        
        # Find all nodes
        visited = set()
        batches = []
        current_batch = {self.entry_point}
        
        while current_batch:
            # Add current batch to result
            batches.append(list(current_batch))
            
            # Find next batch
            visited.update(current_batch)
            next_batch = set()
            
            for node_id in current_batch:
                for edge in self.get_outgoing_edges(node_id):
                    # Skip conditional edges that need evaluation
                    if edge.type == EdgeType.CONDITIONAL_TRUE or edge.type == EdgeType.CONDITIONAL_FALSE:
                        continue
                    
                    target = edge.target_id
                    if target not in visited:
                        # Check if all incoming edges are satisfied
                        incoming = self.get_incoming_edges(target)
                        if all(e.source_id in visited or e.source_id in current_batch for e in incoming):
                            next_batch.add(target)
            
            current_batch = next_batch
        
        return batches
    
    def add_sequence(self, tasks: List[str]) -> None:
        """Add a sequence of tasks."""
        prev_id = None
        
        for task_id in tasks:
            node_id = self._task_index.get(task_id)
            if not node_id:
                continue
            
            if prev_id is None:
                self.set_entry_point(node_id)
            else:
                edge = GraphEdge(
                    source_id=prev_id,
                    target_id=node_id,
                    type=EdgeType.SEQUENCE
                )
                self.add_edge(edge)
            
            prev_id = node_id
        
        if prev_id:
            self.add_exit_point(prev_id)
    
    def add_parallel_group(self, tasks: List[str], after_node: Optional[str] = None, before_node: Optional[str] = None) -> str:
        """Add a parallel group of tasks."""
        group_id = str(uuid.uuid4())[:8]
        
        # Create parallel node
        parallel_node = GraphNode(
            id=group_id,
            type=GraphNodeType.PARALLEL,
            name=f"parallel_{group_id}",
            metadata={'tasks': tasks}
        )
        self.add_node(parallel_node)
        
        # Connect tasks
        task_nodes = [self._task_index.get(t) for t in tasks if self._task_index.get(t)]
        
        if after_node:
            edge = GraphEdge(
                source_id=after_node,
                target_id=group_id,
                type=EdgeType.SEQUENCE
            )
            self.add_edge(edge)
        
        for task_node in task_nodes:
            if task_node:
                edge = GraphEdge(
                    source_id=group_id,
                    target_id=task_node,
                    type=EdgeType.PARALLEL
                )
                self.add_edge(edge)
        
        if before_node:
            edge = GraphEdge(
                source_id=task_nodes[-1] if task_nodes else group_id,
                target_id=before_node,
                type=EdgeType.SEQUENCE
            )
            self.add_edge(edge)
        
        self._parallel_groups.append(set(task_nodes))
        return group_id
    
    def add_checkpoint(self, name: str, after_node: Optional[str] = None) -> str:
        """Add a checkpoint."""
        checkpoint_id = str(uuid.uuid4())[:8]
        
        node = GraphNode(
            id=checkpoint_id,
            type=GraphNodeType.CHECKPOINT,
            name=name,
            metadata={'checkpoint': True}
        )
        self.add_node(node)
        
        if after_node:
            edge = GraphEdge(
                source_id=after_node,
                target_id=checkpoint_id,
                type=EdgeType.SEQUENCE
            )
            self.add_edge(edge)
        
        return checkpoint_id
    
    def add_rollback_point(self, name: str, checkpoint_id: str) -> str:
        """Add a rollback point."""
        rollback_id = str(uuid.uuid4())[:8]
        
        node = GraphNode(
            id=rollback_id,
            type=GraphNodeType.ROLLBACK,
            name=name,
            metadata={'checkpoint': checkpoint_id}
        )
        self.add_node(node)
        
        return rollback_id
    
    def can_execute_in_parallel(self, task_id1: str, task_id2: str) -> bool:
        """Check if two tasks can execute in parallel."""
        node1_id = self._task_index.get(task_id1)
        node2_id = self._task_index.get(task_id2)
        
        if not node1_id or not node2_id:
            return False
        
        # Check for data dependencies
        node1 = self.get_node(node1_id)
        node2 = self.get_node(node2_id)
        
        if not node1 or not node2:
            return False
        
        # Check incoming edges
        for edge in self.get_incoming_edges(node1_id):
            if edge.target_id == node2_id:
                return False
        
        for edge in self.get_incoming_edges(node2_id):
            if edge.target_id == node1_id:
                return False
        
        return True
    
    def to_dict(self) -> Dict:
        """Export to dictionary."""
        return {
            'mission_id': self.mission_id,
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'edges': {eid: edge.to_dict() for eid, edge in self.edges.items()},
            'entry_point': self.entry_point,
            'exit_points': self.exit_points,
            'parallel_groups': [list(g) for g in self._parallel_groups],
        }
    
    def __len__(self) -> int:
        """Number of nodes."""
        return len(self.nodes)