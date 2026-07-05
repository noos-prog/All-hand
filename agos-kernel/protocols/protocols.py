"""AGOS Protocols."""
from typing import Any, Dict, Optional
from enum import Enum


class ProtocolType(Enum):
    """Protocol type."""
    HTTP = "http"
    WEBSOCKET = "websocket"
    GRPC = "grpc"
    MQTT = "mqtt"
    CUSTOM = "custom"


class ProtocolHandler:
    """
    Protocol Handler.
    
    Manages communication protocols.
    
    Usage:
        handler = ProtocolHandler()
        handler.register(ProtocolType.HTTP, my_http_handler)
    """
    
    def __init__(self):
        """Initialize protocol handler."""
        self._handlers: Dict[str, Any] = {}
    
    def register(self, protocol: ProtocolType, handler: Any) -> None:
        """Register a protocol handler."""
        self._handlers[protocol.value] = handler
    
    def get(self, protocol: ProtocolType) -> Optional[Any]:
        """Get a protocol handler."""
        return self._handlers.get(protocol.value)
    
    def list_protocols(self) -> list:
        """List registered protocols."""
        return list(self._handlers.keys())


# Global instance
_protocol_handler: Optional[ProtocolHandler] = None


def get_protocol_handler() -> ProtocolHandler:
    """Get the global protocol handler."""
    global _protocol_handler
    if _protocol_handler is None:
        _protocol_handler = ProtocolHandler()
    return _protocol_handler
