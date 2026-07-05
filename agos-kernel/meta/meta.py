"""AGOS Metadata Management."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Metadata:
    """Metadata entry."""
    id: str
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetaManager:
    """Manages metadata for AGOS entities."""
    
    def __init__(self):
        """Initialize meta manager."""
        self._metadata: Dict[str, Metadata] = {}
    
    def set(self, key: str, value: Any) -> Metadata:
        """Set a metadata value."""
        if key in self._metadata:
            m = self._metadata[key]
            m.value = value
            m.updated_at = datetime.now()
        else:
            m = Metadata(
                id=f"meta-{uuid.uuid4().hex[:8]}",
                key=key,
                value=value,
            )
            self._metadata[key] = m
        return m
    
    def get(self, key: str) -> Optional[Any]:
        """Get a metadata value."""
        m = self._metadata.get(key)
        return m.value if m else None
    
    def delete(self, key: str) -> bool:
        """Delete a metadata value."""
        if key in self._metadata:
            del self._metadata[key]
            return True
        return False
    
    def list_all(self) -> List[Metadata]:
        """List all metadata."""
        return list(self._metadata.values())


# Global instance
_meta_manager: Optional[MetaManager] = None


def get_meta_manager() -> MetaManager:
    """Get the global meta manager."""
    global _meta_manager
    if _meta_manager is None:
        _meta_manager = MetaManager()
    return _meta_manager
