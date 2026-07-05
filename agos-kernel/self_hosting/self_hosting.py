"""AGOS Self-Hosting."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class HostStatus(Enum):
    """Host status."""
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


@dataclass
class Host:
    """A host."""
    id: str
    name: str
    address: str
    port: int = 8080
    status: HostStatus = HostStatus.ONLINE
    metadata: Dict[str, Any] = field(default_factory=dict)


class SelfHostManager:
    """
    Self-Hosting Manager.
    
    Manages self-hosted instances.
    
    Usage:
        manager = SelfHostManager()
        host = manager.add_host("my-server", "192.168.1.100")
    """
    
    def __init__(self):
        """Initialize self-host manager."""
        self._hosts: Dict[str, Host] = {}
    
    def add_host(self, name: str, address: str, port: int = 8080) -> Host:
        """Add a host."""
        host = Host(
            id=f"host-{uuid.uuid4().hex[:8]}",
            name=name,
            address=address,
            port=port,
        )
        self._hosts[host.id] = host
        return host
    
    def get_host(self, host_id: str) -> Optional[Host]:
        """Get a host by ID."""
        return self._hosts.get(host_id)
    
    def remove_host(self, host_id: str) -> bool:
        """Remove a host."""
        if host_id in self._hosts:
            del self._hosts[host_id]
            return True
        return False
    
    def list_hosts(self) -> List[Host]:
        """List all hosts."""
        return list(self._hosts.values())
    
    def set_status(self, host_id: str, status: HostStatus) -> bool:
        """Set host status."""
        host = self._hosts.get(host_id)
        if host:
            host.status = status
            return True
        return False


# Global instance
_self_host_manager: Optional[SelfHostManager] = None


def get_self_host_manager() -> SelfHostManager:
    """Get the global self-host manager."""
    global _self_host_manager
    if _self_host_manager is None:
        _self_host_manager = SelfHostManager()
    return _self_host_manager
