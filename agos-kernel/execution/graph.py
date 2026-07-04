"""Universal Execution Graph Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class NodeType(Enum):
    """Node types in execution graph."""
    MISSION = "mission"
    GOAL = "goal"
    CAPABILITY = "capability"
    SKILL = "skill"
    PROVIDER = "provider"
    ADAPTER = "adapter"
    VALIDATION = "validation"
    APPROVAL = "approval"
    KNOWLEDGE = "knowledge"
    ARTIFACT = "artifact"
    CHECKPOINT = "checkpoint"
    CONDITION = "condition"
    LOOP = "loop"
    MERGE = "merge"
    SPLIT = "split"


class EdgeType(Enum):
    """Edge types in execution graph."""
    DEPENDS_ON = "depends_on"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    BLOCKS = "blocks"
    REQUIRES = "requires"
    TRIGGERS = "triggers"
    SYNCHRONIZES = "synchronizes"


class NodeStatus(Enum):
    """Node execution status."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class GraphNode:
    """A node in the execution graph."""
    id: str
    node_type: NodeType
    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    status: NodeStatus = NodeStatus.PENDING
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class GraphEdge:
    """An edge in the execution graph."""
    id: str
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionGraph:
    """Universal Execution Graph."""
    id: str
    name: str
    nodes: Dict[str, GraphNode] = field(default_factory=dict)
    edges: List[GraphEdge] = field(default_factory=list)
    adjacency: Dict[str, Set[str]] = field(default_factory=dict)
    reverse_adjacency: Dict[str, Set[str]] = field(default_factory=dict)
    is_dag: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_node(self, node: GraphNode) -> None:
        """Add node to graph."""
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = set()
        if node.id not in self.reverse_adjacency:
            self.reverse_adjacency[node.id] = set()
    
    def add_edge(self, edge: GraphEdge) -> None:
        """Add edge to graph."""
        self.edges.append(edge)
        
        # Update adjacency
        if edge.source_id in self.adjacency:
            self.adjacency[edge.source_id].add(edge.target_id)
        else:
            self.adjacency[edge.source_id] = {edge.target_id}
        
        # Update reverse adjacency
        if edge.target_id in self.reverse_adjacency:
            self.reverse_adjacency[edge.target_id].add(edge.source_id)
        else:
            self.reverse_adjacency[edge.target_id] = {edge.source_id}
    
    def get_dependencies(self, node_id: str) -> List[str]:
        """Get all dependencies for a node."""
        return list(self.reverse_adjacency.get(node_id, set()))
    
    def get_dependents(self, node_id: str) -> List[str]:
        """Get all nodes that depend on this node."""
        return list(self.adjacency.get(node_id, set()))
    
    def topological_sort(self) -> List[str]:
        """Topological sort of the graph."""
        in_degree = {nid: len(self.reverse_adjacency.get(nid, set())) for nid in self.nodes}
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        result = []
        
        while queue:
            node_id = queue.pop(0)
            result.append(node_id)
            
            for dep in self.adjacency.get(node_id, set()):
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)
        
        if len(result) != len(self.nodes):
            self.is_dag = False
        
        return result
    
    def find_parallel_groups(self) -> List[List[str]]:
        """Find groups of nodes that can run in parallel."""
        sorted_nodes = self.topological_sort()
        groups = []
        processed = set()
        
        for node_id in sorted_nodes:
            deps = self.get_dependencies(node_id)
            
            # Check if all dependencies are in previous groups
            group_idx = 0
            for dep in deps:
                for i, group in enumerate(groups):
                    if dep in group:
                        group_idx = max(group_idx, i + 1)
            
            # Add to appropriate group
            while len(groups) <= group_idx:
                groups.append([])
            groups[group_idx].append(node_id)
        
        return groups


class GraphRuntime:
    """Universal Execution Graph Runtime."""
    
    def __init__(self):
        """Initialize graph runtime."""
        self.graphs: Dict[str, ExecutionGraph] = {}
        self.scheduler = GraphScheduler()
        self.validator = GraphValidator()
        self.optimizer = GraphOptimizer()
    
    def create_graph(self, name: str) -> ExecutionGraph:
        """Create a new execution graph."""
        graph_id = self._generate_id(name)
        
        graph = ExecutionGraph(
            id=graph_id,
            name=name,
        )
        
        self.graphs[graph_id] = graph
        return graph
    
    def add_node(
        self,
        graph_id: str,
        name: str,
        node_type: NodeType,
        config: Optional[Dict[str, Any]] = None,
    ) -> Optional[GraphNode]:
        """Add node to graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return None
        
        node = GraphNode(
            id=self._generate_id(name),
            node_type=node_type,
            name=name,
            config=config or {},
        )
        
        graph.add_node(node)
        return node
    
    def add_edge(
        self,
        graph_id: str,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
    ) -> bool:
        """Add edge to graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return False
        
        edge = GraphEdge(
            id=self._generate_id(f"edge-{source_id}-{target_id}"),
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
        )
        
        graph.add_edge(edge)
        return True
    
    def get_graph(self, graph_id: str) -> Optional[ExecutionGraph]:
        """Get graph by ID."""
        return self.graphs.get(graph_id)
    
    def validate_graph(self, graph_id: str) -> Dict[str, Any]:
        """Validate a graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return {"valid": False, "error": "Graph not found"}
        
        return self.validator.validate(graph)
    
    def optimize_graph(self, graph_id: str) -> bool:
        """Optimize a graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return False
        
        return self.optimizer.optimize(graph)
    
    def get_execution_order(self, graph_id: str) -> List[str]:
        """Get topological execution order."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return []
        
        return graph.topological_sort()
    
    def get_parallel_groups(self, graph_id: str) -> List[List[str]]:
        """Get parallel execution groups."""
        graph = self.graphs.get(graph_id)
        if not graph:
            return []
        
        return graph.find_parallel_groups()
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class GraphScheduler:
    """Graph scheduler."""
    
    def schedule(self, graph: ExecutionGraph) -> List[List[str]]:
        """Schedule graph execution."""
        return graph.find_parallel_groups()


class GraphValidator:
    """Graph validator."""
    
    def validate(self, graph: ExecutionGraph) -> Dict[str, Any]:
        """Validate graph structure."""
        errors = []
        warnings = []
        
        # Check for cycles
        sorted_nodes = graph.topological_sort()
        if not graph.is_dag:
            errors.append("Graph contains cycles")
        
        # Check for orphan nodes
        for node_id in graph.nodes:
            if not graph.get_dependencies(node_id) and not graph.get_dependents(node_id):
                if len(graph.nodes) > 1:
                    warnings.append(f"Node {node_id} is orphaned")
        
        # Check for missing edges
        for node in graph.nodes.values():
            if node.inputs and not graph.get_dependencies(node.id):
                errors.append(f"Node {node.id} has inputs but no incoming edges")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "is_dag": graph.is_dag,
        }


class GraphOptimizer:
    """Graph optimizer."""
    
    def optimize(self, graph: ExecutionGraph) -> bool:
        """Optimize graph execution."""
        # Remove redundant edges
        original_count = len(graph.edges)
        
        # Merge sequential nodes if possible
        # This is a simplified implementation
        
        return True
