"""
AGOS Knowledge Registry
=================

Registry for all AGOS knowledge entries.
Every knowledge entry must be registered to be discoverable.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import threading
import hashlib


class KnowledgeType(Enum):
    """Type of knowledge."""
    FACT = "fact"
    RULE = "rule"
    PATTERN = "pattern"
    DECISION = "decision"
    EVIDENCE = "evidence"
    EXPERIENCE = "experience"
    ARCHITECTURE = "architecture"


class KnowledgeStatus(Enum):
    """Knowledge status."""
    DRAFT = "draft"
    VALIDATED = "validated"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass
class KnowledgeEntry:
    """
    A registered AGOS knowledge entry.
    
    Attributes:
        id: Unique identifier
        title: Human-readable title
        knowledge_type: Type of knowledge
        content: The knowledge content
        version: Semantic version
        status: Current status
        evidence: List of evidence IDs
        tags: List of tags for search
        created_at: When this was created
        updated_at: When this was last updated
        validated_at: When this was validated
        metadata: Additional metadata
    """
    id: str
    title: str
    knowledge_type: KnowledgeType
    content: Dict[str, Any]
    version: str = "1.0.0"
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    evidence: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    validated_at: Optional[datetime] = None
    validated_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self, validated_by: str = "system") -> bool:
        """Validate this knowledge entry."""
        if self.status == KnowledgeStatus.DRAFT:
            self.status = KnowledgeStatus.VALIDATED
            self.validated_at = datetime.utcnow()
            self.validated_by = validated_by
            return True
        return False
    
    def activate(self) -> bool:
        """Activate this knowledge entry."""
        if self.status == KnowledgeStatus.VALIDATED:
            self.status = KnowledgeStatus.ACTIVE
            return True
        return False
    
    def deprecate(self) -> bool:
        """Deprecate this knowledge entry."""
        self.status = KnowledgeStatus.DEPRECATED
        self.updated_at = datetime.utcnow()
        return True
    
    def archive(self) -> bool:
        """Archive this knowledge entry."""
        self.status = KnowledgeStatus.ARCHIVED
        self.updated_at = datetime.utcnow()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "knowledge_type": self.knowledge_type.value,
            "content": self.content,
            "version": self.version,
            "status": self.status.value,
            "evidence": self.evidence,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "validated_at": self.validated_at.isoformat() if self.validated_at else None,
            "validated_by": self.validated_by,
            "metadata": self.metadata,
        }


class KnowledgeRegistry:
    """
    Thread-safe singleton registry for all AGOS knowledge entries.
    
    Usage:
        registry = KnowledgeRegistry.get_instance()
        registry.add(
            title="Git Best Practices",
            knowledge_type=KnowledgeType.RULE,
            content={"rules": [...]},
        )
        entry = registry.get("kb_abc123")
        results = registry.search("git")
    """
    
    _instance: Optional['KnowledgeRegistry'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        """Initialize registry."""
        self._knowledge: Dict[str, KnowledgeEntry] = {}
        self._index: Dict[str, set] = {}  # word -> set of entry IDs
        self._lock = threading.RLock()
    
    @classmethod
    def get_instance(cls) -> 'KnowledgeRegistry':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def _generate_id(self, title: str) -> str:
        """Generate a unique ID for a knowledge entry."""
        hash_input = f"{title}_{datetime.utcnow().isoformat()}"
        return f"kb_{hashlib.sha256(hash_input.encode()).hexdigest()[:12]}"
    
    def _index_entry(self, entry: KnowledgeEntry) -> None:
        """Index a knowledge entry for search."""
        words = []
        
        # Index title
        words.extend(entry.title.lower().split())
        
        # Index tags
        words.extend([tag.lower() for tag in entry.tags])
        
        # Index content
        def extract_words(obj: Any) -> None:
            if isinstance(obj, str):
                words.extend(obj.lower().split())
            elif isinstance(obj, dict):
                for v in obj.values():
                    extract_words(v)
            elif isinstance(obj, (list, tuple)):
                for item in obj:
                    extract_words(item)
        
        extract_words(entry.content)
        
        # Add to index
        for word in words:
            if len(word) > 2:
                if word not in self._index:
                    self._index[word] = set()
                self._index[word].add(entry.id)
    
    def add(
        self,
        title: str,
        knowledge_type: KnowledgeType,
        content: Dict[str, Any],
        tags: Optional[List[str]] = None,
        evidence: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a knowledge entry.
        
        Args:
            title: Human-readable title
            knowledge_type: Type of knowledge
            content: The knowledge content
            tags: Tags for categorization
            evidence: List of evidence IDs
            metadata: Additional metadata
            
        Returns:
            The knowledge entry ID
        """
        with self._lock:
            entry_id = self._generate_id(title)
            
            entry = KnowledgeEntry(
                id=entry_id,
                title=title,
                knowledge_type=knowledge_type,
                content=content,
                tags=tags or [],
                evidence=evidence or [],
                metadata=metadata or {},
            )
            
            self._knowledge[entry_id] = entry
            self._index_entry(entry)
            
            return entry_id
    
    def update(
        self,
        id: str,
        title: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a knowledge entry."""
        with self._lock:
            entry = self._knowledge.get(id)
            if not entry:
                return False
            
            if title is not None:
                entry.title = title
            if content is not None:
                entry.content = content
            if tags is not None:
                entry.tags = tags
            if metadata is not None:
                entry.metadata.update(metadata)
            
            entry.updated_at = datetime.utcnow()
            
            # Re-index
            self._index_entry(entry)
            
            return True
    
    def get(self, id: str) -> Optional[KnowledgeEntry]:
        """Get a knowledge entry."""
        return self._knowledge.get(id)
    
    def delete(self, id: str) -> bool:
        """Delete a knowledge entry."""
        with self._lock:
            if id in self._knowledge:
                del self._knowledge[id]
                return True
            return False
    
    def list_all(self) -> List[KnowledgeEntry]:
        """List all knowledge entries."""
        return list(self._knowledge.values())
    
    def list_by_type(self, knowledge_type: KnowledgeType) -> List[KnowledgeEntry]:
        """List knowledge entries by type."""
        return [k for k in self._knowledge.values() if k.knowledge_type == knowledge_type]
    
    def list_by_status(self, status: KnowledgeStatus) -> List[KnowledgeEntry]:
        """List knowledge entries by status."""
        return [k for k in self._knowledge.values() if k.status == status]
    
    def list_active(self) -> List[KnowledgeEntry]:
        """List active knowledge entries."""
        return self.list_by_status(KnowledgeStatus.ACTIVE)
    
    def search(self, query: str, limit: int = 10) -> List[KnowledgeEntry]:
        """Search knowledge entries."""
        query_words = query.lower().split()
        
        # Find matching entry IDs
        matching_ids = set()
        for word in query_words:
            if len(word) > 2:
                for indexed_word, ids in self._index.items():
                    if word in indexed_word:
                        matching_ids.update(ids)
        
        # Get entries and sort by relevance
        results = []
        for entry_id in matching_ids:
            entry = self._knowledge.get(entry_id)
            if entry and entry.status == KnowledgeStatus.ACTIVE:
                # Calculate relevance score
                score = 0
                entry_text = entry.title.lower() + " " + " ".join(entry.tags)
                for word in query_words:
                    if word in entry_text:
                        score += 1
                results.append((score, entry))
        
        # Sort by score
        results.sort(key=lambda x: -x[0])
        
        return [entry for _, entry in results[:limit]]
    
    def validate(self, id: str, validated_by: str = "system") -> bool:
        """Validate a knowledge entry."""
        entry = self.get(id)
        if entry:
            return entry.validate(validated_by)
        return False
    
    def activate(self, id: str) -> bool:
        """Activate a knowledge entry."""
        entry = self.get(id)
        if entry:
            return entry.activate()
        return False
    
    def check_health(self) -> Dict[str, Any]:
        """Check health of knowledge registry."""
        by_type: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        
        for entry in self._knowledge.values():
            type_key = entry.knowledge_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            status_key = entry.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1
        
        return {
            "total": len(self._knowledge),
            "active": len(self.list_active()),
            "by_type": by_type,
            "by_status": by_status,
        }
    
    def reset(self) -> None:
        """Reset registry (for testing)."""
        with self._lock:
            self._knowledge.clear()
            self._index.clear()

_knowledge_registry_instance = None
_knowledge_registry_lock = threading.Lock()
def get_knowledge_registry() -> KnowledgeRegistry:
    global _knowledge_registry_instance
    if _knowledge_registry_instance is None:
        with _knowledge_registry_lock:
            if _knowledge_registry_instance is None:
                _knowledge_registry_instance = KnowledgeRegistry()
    return _knowledge_registry_instance

