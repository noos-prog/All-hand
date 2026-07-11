"""
Ecosystem Federation
===================

Federated network of AGOS nodes for distributed execution.
Enables seamless communication and resource sharing across nodes.

Author: AGOS Team
Version: 1.0.0
"""

import asyncio
import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
import hashlib


FEDERATION_RULES = [
    "No shared kernel state",
    "No direct database sharing", 
    "Contract-based federation only",
    "All nodes must be authenticated",
    "Messages must be signed",
    "Topology must be discoverable"
]


class ConnectionStatus(Enum):
    """Status of connection to a node."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


class NodeType(Enum):
    """Type of federation node."""
    COORDINATOR = "coordinator"
    WORKER = "worker"
    GATEWAY = "gateway"
    STORAGE = "storage"
    COMPUTE = "compute"
    EDGE = "edge"


class MessageType(Enum):
    """Type of federation message."""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    HEARTBEAT = "heartbeat"
    DISCOVERY = "discovery"
    SYNC = "sync"


@dataclass
class Node:
    """
    Represents a node in the federation network.
    
    Attributes:
        node_id: Unique identifier for the node
        name: Human-readable name
        trust_level: Trust level (untrusted, trusted, verified)
        node_type: Type of node
        status: Current connection status
        endpoints: List of accessible endpoints
        capabilities: Set of node capabilities
        capacity: Available capacity metrics
        load: Current load metrics
        location: Geographic location (optional)
        version: AGOS version running on this node
        last_seen: Timestamp of last heartbeat
        created_at: Timestamp when node joined
    """
    node_id: str
    name: str
    trust_level: str = "trusted"
    node_type: NodeType = NodeType.WORKER
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    endpoints: List[str] = field(default_factory=list)
    capabilities: Set[str] = field(default_factory=set)
    capacity: Dict[str, float] = field(default_factory=lambda: {
        "cpu": 100.0,
        "memory": 100.0,
        "storage": 100.0,
        "network": 100.0
    })
    load: Dict[str, float] = field(default_factory=lambda: {
        "cpu": 0.0,
        "memory": 0.0,
        "storage": 0.0,
        "network": 0.0
    })
    location: Optional[str] = None
    version: str = "1.0.0"
    last_seen: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_available(self) -> bool:
        """Check if node is available for work."""
        return (
            self.status == ConnectionStatus.CONNECTED and
            self.load["cpu"] < self.capacity["cpu"] * 0.9 and
            self.load["memory"] < self.capacity["memory"] * 0.9
        )
    
    @property
    def availability_score(self) -> float:
        """Calculate availability score (0.0 to 1.0)."""
        if not self.is_available:
            return 0.0
        
        cpu_available = 1.0 - (self.load["cpu"] / self.capacity["cpu"])
        mem_available = 1.0 - (self.load["memory"] / self.capacity["memory"])
        
        return (cpu_available + mem_available) / 2.0
    
    def update_load(self, cpu: float, memory: float, storage: float = 0.0, network: float = 0.0) -> None:
        """Update node load metrics."""
        self.load = {
            "cpu": min(max(cpu, 0.0), 100.0),
            "memory": min(max(memory, 0.0), 100.0),
            "storage": min(max(storage, 0.0), 100.0),
            "network": min(max(network, 0.0), 100.0)
        }
        self.last_seen = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "trust_level": self.trust_level,
            "type": self.node_type.value,
            "status": self.status.value,
            "endpoints": self.endpoints,
            "capabilities": list(self.capabilities),
            "capacity": self.capacity,
            "load": self.load,
            "location": self.location,
            "version": self.version,
            "last_seen": self.last_seen.isoformat(),
            "created_at": self.created_at.isoformat(),
            "is_available": self.is_available,
            "availability_score": self.availability_score,
            "metadata": self.metadata
        }


@dataclass
class FederationMessage:
    """Message in the federation network."""
    message_id: str
    message_type: MessageType
    source_node: str
    target_node: Optional[str]
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ttl: int = 60
    priority: int = 0
    correlation_id: Optional[str] = None
    signature: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        message_type: MessageType,
        source_node: str,
        target_node: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        priority: int = 0,
        correlation_id: Optional[str] = None,
    ) -> 'FederationMessage':
        """Create a new federation message."""
        return cls(
            message_id=f"msg-{uuid.uuid4().hex[:16]}",
            message_type=message_type,
            source_node=source_node,
            target_node=target_node,
            payload=payload or {},
            priority=priority,
            correlation_id=correlation_id
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "source_node": self.source_node,
            "target_node": self.target_node,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "ttl": self.ttl,
            "priority": self.priority,
            "correlation_id": self.correlation_id,
            "signature": self.signature
        }


class RouteTable:
    """
    Routing table for federation messages.
    
    Maintains routes to all known nodes.
    """
    
    def __init__(self):
        self._routes: Dict[str, str] = {}
        self._reverse_routes: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
    
    def add_route(self, node_id: str, endpoint: str) -> None:
        """Add a route to the table."""
        with self._lock:
            self._routes[node_id] = endpoint
            if endpoint not in self._reverse_routes:
                self._reverse_routes[endpoint] = []
            if node_id not in self._reverse_routes[endpoint]:
                self._reverse_routes[endpoint].append(node_id)
    
    def remove_route(self, node_id: str) -> None:
        """Remove a route from the table."""
        with self._lock:
            if node_id in self._routes:
                endpoint = self._routes[node_id]
                del self._routes[node_id]
                if endpoint in self._reverse_routes:
                    if node_id in self._reverse_routes[endpoint]:
                        self._reverse_routes[endpoint].remove(node_id)
    
    def get_route(self, node_id: str) -> Optional[str]:
        """Get route for a node."""
        return self._routes.get(node_id)
    
    def get_all_routes(self) -> Dict[str, str]:
        """Get all routes."""
        return dict(self._routes)


class FederationRuntime:
    """
    Runtime for managing federation operations.
    
    Handles node registration, message routing, and topology management.
    """
    
    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._route_table = RouteTable()
        self._message_queue: List[FederationMessage] = []
        self._handlers: Dict[MessageType, List[Callable]] = {
            mt: [] for mt in MessageType
        }
        self._lock = threading.RLock()
        self._running = False
        
        self._stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "messages_failed": 0,
            "bytes_transferred": 0,
            "start_time": datetime.utcnow()
        }
    
    @property
    def nodes(self) -> List[Node]:
        """Get all known nodes."""
        with self._lock:
            return list(self._nodes.values())
    
    @property
    def connected_nodes(self) -> List[Node]:
        """Get all connected nodes."""
        with self._lock:
            return [n for n in self._nodes.values() if n.status == ConnectionStatus.CONNECTED]
    
    def register_node(self, node: Node) -> None:
        """Register a node in the federation."""
        with self._lock:
            node.status = ConnectionStatus.CONNECTED
            self._nodes[node.node_id] = node
            
            for endpoint in node.endpoints:
                self._route_table.add_route(node.node_id, endpoint)
    
    def unregister_node(self, node_id: str) -> bool:
        """Unregister a node from the federation."""
        with self._lock:
            if node_id in self._nodes:
                del self._nodes[node_id]
                self._route_table.remove_route(node_id)
                return True
        return False
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get information about a specific node."""
        with self._lock:
            return self._nodes.get(node_id)
    
    def register_handler(self, message_type: MessageType, handler: Callable[[FederationMessage], None]) -> None:
        """Register a message handler."""
        if message_type in self._handlers:
            self._handlers[message_type].append(handler)
    
    def find_nodes_by_capability(self, capability: str) -> List[Node]:
        """Find nodes that have a specific capability."""
        with self._lock:
            return [
                n for n in self._nodes.values()
                if capability in n.capabilities and n.is_available
            ]
    
    def find_best_node(self, required_capabilities: Optional[List[str]] = None) -> Optional[Node]:
        """Find the best available node for a task."""
        candidates = self.connected_nodes
        
        if required_capabilities:
            candidates = [
                n for n in candidates
                if all(cap in n.capabilities for cap in required_capabilities)
            ]
        
        candidates = [n for n in candidates if n.is_available]
        
        if not candidates:
            return None
        
        return max(candidates, key=lambda n: n.availability_score)
    
    def send_message(self, message: FederationMessage) -> bool:
        """Send a message through the federation."""
        try:
            route = self._route_table.get_route(message.target_node or "")
            if route:
                self._stats["messages_sent"] += 1
                self._stats["bytes_transferred"] += len(json.dumps(message.payload))
                return True
            self._stats["messages_failed"] += 1
            return False
        except Exception:
            self._stats["messages_failed"] += 1
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get federation statistics."""
        return {
            "total_nodes": len(self._nodes),
            "connected_nodes": len(self.connected_nodes),
            "stats": {
                **self._stats,
                "uptime_seconds": (datetime.utcnow() - self._stats["start_time"]).total_seconds()
            },
            "routes": len(self._route_table.get_all_routes())
        }


class UniversalFederationPlatform:
    """
    Universal Federation Platform.
    
    Enables distributed AGOS installations to collaborate
    while maintaining isolation and security.
    
    Rules:
    ✅ No shared kernel state
    ✅ No direct database sharing
    ✅ Contract-based federation only
    ✅ All nodes must be authenticated
    ✅ Messages must be signed
    ✅ Topology must be discoverable
    
    Target: Global federation of AGOS installations
    """
    
    def __init__(self):
        self.version = "3.0.0"
        self.runtime = FederationRuntime()
        self._federation_id = f"fed-{uuid.uuid4().hex[:12]}"
    
    @property
    def federation_id(self) -> str:
        """Get the federation ID."""
        return self._federation_id
    
    def create_node(
        self,
        name: str,
        node_type: NodeType = NodeType.WORKER,
        trust_level: str = "trusted",
        capabilities: Optional[List[str]] = None,
        endpoints: Optional[List[str]] = None,
        location: Optional[str] = None,
    ) -> Node:
        """Create a new federation node."""
        node = Node(
            node_id=f"node-{uuid.uuid4().hex[:12]}",
            name=name,
            node_type=node_type,
            trust_level=trust_level,
            capabilities=set(capabilities or ["execution", "computation"]),
            endpoints=endpoints or [],
            location=location
        )
        self.runtime.register_node(node)
        return node
    
    def join_federation(self, other_platform: 'UniversalFederationPlatform') -> bool:
        """Join another federation platform."""
        for node in other_platform.runtime.connected_nodes:
            self.runtime.register_node(node)
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get complete federation statistics."""
        return {
            "version": self.version,
            "federation_id": self._federation_id,
            "federation_rules": FEDERATION_RULES,
            "registered_nodes": len(self.runtime.nodes),
            "connected_nodes": len(self.runtime.connected_nodes),
            "runtime_stats": self.runtime.get_statistics()
        }
    
    def get_topology(self) -> Dict[str, Any]:
        """Get the current network topology."""
        return {
            "federation_id": self._federation_id,
            "nodes": [n.to_dict() for n in self.runtime.nodes],
            "connections": [
                {"source": n.node_id, "status": n.status.value}
                for n in self.runtime.connected_nodes
            ]
        }
    
    def discover_nodes(self, capability: Optional[str] = None) -> List[Dict[str, Any]]:
        """Discover nodes in the federation."""
        if capability:
            nodes = self.runtime.find_nodes_by_capability(capability)
        else:
            nodes = self.runtime.connected_nodes
        
        return [n.to_dict() for n in nodes]
    
    def select_best_node(self, required_capabilities: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """Select the best node for a task."""
        node = self.runtime.find_best_node(required_capabilities)
        return node.to_dict() if node else None
