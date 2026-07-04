"""Universal Distributed Civilization Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class NodeState(Enum):
    """Node state."""
    JOINING = "joining"
    ACTIVE = "active"
    SUSPECTED = "suspected"
    FAILED = "failed"
    LEFT = "left"


class ClusterState(Enum):
    """Cluster state."""
    FORMING = "forming"
    STABLE = "stable"
    DEGRADED = "degraded"
    RECOVERING = "recovering"


@dataclass
class Node:
    """A cluster node."""
    id: str
    name: str
    address: str
    port: int
    state: NodeState = NodeState.JOINING
    capabilities: List[str] = field(default_factory=list)
    load: float = 0.0
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClusterEvent:
    """A cluster event."""
    id: str
    event_type: str
    source_node: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)


class DistributedLock:
    """Distributed lock."""
    def __init__(self, lock_id: str, owner: str, expires_at: datetime):
        self.id = lock_id
        self.owner = owner
        self.expires_at = expires_at


class DistributedRuntime:
    """Universal Distributed Civilization Runtime."""
    
    def __init__(self):
        """Initialize distributed runtime."""
        # Node management
        self.nodes: Dict[str, Node] = {}
        self.local_node_id: Optional[str] = None
        
        # Cluster state
        self.cluster_state = ClusterState.FORMING
        
        # Registry
        self.node_registry = NodeRegistry()
        
        # Event bus
        self.event_bus = DistributedEventBus()
        
        # State synchronizer
        self.state_synchronizer = DistributedStateSynchronizer()
        
        # Lock manager
        self.lock_manager = DistributedLockManager()
        
        # Telemetry
        self.telemetry = DistributedTelemetry()
    
    def join_cluster(self, name: str, address: str, port: int) -> Node:
        """Join the cluster."""
        node_id = self._generate_id(name)
        
        node = Node(
            id=node_id,
            name=name,
            address=address,
            port=port,
            state=NodeState.ACTIVE,
        )
        
        self.nodes[node_id] = node
        self.local_node_id = node_id
        self.node_registry.register(node)
        
        # Update cluster state
        if len(self.nodes) > 1:
            self.cluster_state = ClusterState.STABLE
        
        return node
    
    def leave_cluster(self, node_id: str) -> bool:
        """Leave the cluster."""
        if node_id in self.nodes:
            self.nodes[node_id].state = NodeState.LEFT
            self.node_registry.unregister(node_id)
            
            if len(self.nodes) == 0:
                self.cluster_state = ClusterState.FORMING
            
            return True
        return False
    
    def discover_nodes(self, capability: Optional[str] = None) -> List[Node]:
        """Discover nodes in the cluster."""
        nodes = list(self.nodes.values())
        
        if capability:
            nodes = [n for n in nodes if capability in n.capabilities]
        
        return [n for n in nodes if n.state == NodeState.ACTIVE]
    
    def send_message(self, target_node: str, message: Dict[str, Any]) -> bool:
        """Send a message to a node."""
        self.event_bus.publish(f"node:{target_node}", message)
        return True
    
    def broadcast(self, message: Dict[str, Any]) -> bool:
        """Broadcast to all nodes."""
        self.event_bus.publish("cluster:broadcast", message)
        return True
    
    def acquire_lock(self, lock_id: str, ttl_seconds: int = 60) -> Optional[str]:
        """Acquire a distributed lock."""
        return self.lock_manager.acquire(lock_id, self.local_node_id, ttl_seconds)
    
    def release_lock(self, lock_id: str) -> bool:
        """Release a distributed lock."""
        return self.lock_manager.release(lock_id, self.local_node_id)
    
    def sync_state(self, key: str, value: Any) -> bool:
        """Synchronize state across cluster."""
        self.state_synchronizer.set(key, value, self.local_node_id)
        return True
    
    def get_state(self, key: str) -> Optional[Any]:
        """Get synchronized state."""
        return self.state_synchronizer.get(key)
    
    def get_health(self) -> Dict[str, Any]:
        """Get cluster health."""
        active = sum(1 for n in self.nodes.values() if n.state == NodeState.ACTIVE)
        failed = sum(1 for n in self.nodes.values() if n.state == NodeState.FAILED)
        
        return {
            "cluster_state": self.cluster_state.value,
            "total_nodes": len(self.nodes),
            "active_nodes": active,
            "failed_nodes": failed,
            "health_score": active / len(self.nodes) if self.nodes else 0,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class NodeRegistry:
    """Node registry."""
    
    def __init__(self):
        """Initialize registry."""
        self.nodes: Dict[str, Node] = {}
    
    def register(self, node: Node) -> None:
        """Register a node."""
        self.nodes[node.id] = node
    
    def unregister(self, node_id: str) -> bool:
        """Unregister a node."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False
    
    def get(self, node_id: str) -> Optional[Node]:
        """Get a node."""
        return self.nodes.get(node_id)
    
    def list_all(self) -> List[Node]:
        """List all nodes."""
        return list(self.nodes.values())


class DistributedEventBus:
    """Distributed event bus."""
    
    def __init__(self):
        """Initialize event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        self.events: List[ClusterEvent] = []
    
    def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
    
    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish to a topic."""
        event = ClusterEvent(
            id=str(uuid.uuid4()),
            event_type=topic,
            source_node="local",
            data=message,
        )
        
        self.events.append(event)
        
        # Notify subscribers
        for handler in self.subscribers.get(topic, []):
            handler(message)


class DistributedStateSynchronizer:
    """Distributed state synchronizer."""
    
    def __init__(self):
        """Initialize synchronizer."""
        self.state: Dict[str, Any] = {}
        self.versions: Dict[str, int] = {}
        self.last_update: Dict[str, datetime] = {}
    
    def set(self, key: str, value: Any, source: str) -> None:
        """Set state."""
        self.state[key] = value
        self.versions[key] = self.versions.get(key, 0) + 1
        self.last_update[key] = datetime.now()
    
    def get(self, key: str) -> Optional[Any]:
        """Get state."""
        return self.state.get(key)
    
    def get_version(self, key: str) -> int:
        """Get state version."""
        return self.versions.get(key, 0)


class DistributedLockManager:
    """Distributed lock manager."""
    
    def __init__(self):
        """Initialize lock manager."""
        self.locks: Dict[str, DistributedLock] = {}
    
    def acquire(self, lock_id: str, owner: str, ttl_seconds: int) -> Optional[str]:
        """Acquire a lock."""
        if lock_id in self.locks:
            lock = self.locks[lock_id]
            if lock.owner != owner and lock.expires_at > datetime.now():
                return None  # Lock held by another
        
        expires_at = datetime.now()
        expires_at = expires_at.replace(second=expires_at.second + ttl_seconds)
        
        self.locks[lock_id] = DistributedLock(lock_id, owner, expires_at)
        return lock_id
    
    def release(self, lock_id: str, owner: str) -> bool:
        """Release a lock."""
        if lock_id in self.locks:
            if self.locks[lock_id].owner == owner:
                del self.locks[lock_id]
                return True
        return False


class DistributedTelemetry:
    """Distributed telemetry."""
    
    def __init__(self):
        """Initialize telemetry."""
        self.metrics: Dict[str, List[float]] = {}
    
    def record(self, metric: str, value: float) -> None:
        """Record a metric."""
        if metric not in self.metrics:
            self.metrics[metric] = []
        self.metrics[metric].append(value)
    
    def get_stats(self, metric: str) -> Dict[str, float]:
        """Get metric statistics."""
        values = self.metrics.get(metric, [])
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }
