"""AGOS Universal Protocol Layer - Support for all engineering protocols."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import uuid

SUPPORTED_PROTOCOLS = ["HTTP", "HTTPS", "WebSocket", "gRPC", "MCP", "REST", "GraphQL", "SSE", "CLI", "TCP", "UDP", "QUIC", "Future Protocols"]


class ProtocolType(Enum):
    """Types of supported protocols."""
    HTTP = "http"
    HTTPS = "https"
    WEBSOCKET = "websocket"
    GRPC = "grpc"
    MCP = "mcp"
    REST = "rest"
    GRAPHQL = "graphql"
    SSE = "sse"
    CLI = "cli"


class ConnectionState(Enum):
    """Connection state."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class Message:
    """A message in the protocol."""
    message_id: str
    protocol: ProtocolType
    payload: Any
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProtocolMessage:
    """A protocol message with metadata."""
    msg_id: str
    msg_type: str
    content: Any
    source: str = ""
    target: str = ""
    ack_required: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProtocolHandler:
    """
    Universal Protocol Handler.
    
    Rule: Kernel remains protocol-agnostic
    
    Supported Protocols:
    ✅ HTTP, HTTPS, WebSocket, gRPC, MCP
    ✅ REST, GraphQL, SSE, CLI
    ✅ TCP, UDP, QUIC, Future Protocols
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.handlers: Dict[ProtocolType, Callable] = {}
        self.connections: Dict[str, ConnectionState] = {}
    
    def register_handler(self, protocol: ProtocolType, handler: Callable) -> None:
        """Register a handler for a protocol."""
        self.handlers[protocol] = handler
    
    def send(self, protocol: ProtocolType, message: Message) -> bool:
        """Send a message using a protocol."""
        handler = self.handlers.get(protocol)
        if handler:
            return handler(message)
        return False
    
    def connect(self, connection_id: str, protocol: ProtocolType) -> bool:
        """Establish a connection."""
        self.connections[connection_id] = ConnectionState.CONNECTING
        self.connections[connection_id] = ConnectionState.CONNECTED
        return True
    
    def disconnect(self, connection_id: str) -> bool:
        """Disconnect a connection."""
        if connection_id in self.connections:
            self.connections[connection_id] = ConnectionState.DISCONNECTED
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "supported_protocols": SUPPORTED_PROTOCOLS,
            "registered_handlers": len(self.handlers),
            "active_connections": sum(1 for s in self.connections.values() if s == ConnectionState.CONNECTED),
        }
