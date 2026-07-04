"""Universal Memory Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MemoryType(Enum):
    """Memory type."""
    WORKING = "working"
    MISSION = "mission"
    PROJECT = "project"
    REPOSITORY = "repository"
    ORGANIZATION = "organization"
    KNOWLEDGE = "knowledge"
    EXECUTION = "execution"
    DECISION = "decision"
    POLICY = "policy"
    HISTORICAL = "historical"


class MemoryStatus(Enum):
    """Memory status."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPRESSED = "compressed"
    DELETED = "deleted"


class MemoryPriority(Enum):
    """Memory priority."""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class MemoryChunk:
    """A chunk of memory content."""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.now)
    importance: float = 0.5  # 0.0 to 1.0
    access_count: int = 0


@dataclass
class MemoryIndex:
    """Index for memory retrieval."""
    keywords: Dict[str, List[str]] = field(default_factory=dict)
    embeddings: Dict[str, List[float]] = field(default_factory=dict)
    temporal: Dict[str, datetime] = field(default_factory=dict)


@dataclass
class MemoryNode:
    """A node in the memory graph."""
    id: str
    memory_id: str
    node_type: str
    content: str
    connections: List[str] = field(default_factory=list)
    weight: float = 1.0


@dataclass
class Memory:
    """Universal Memory."""
    id: str
    name: str
    memory_type: MemoryType
    
    # Content
    content: Dict[str, Any] = field(default_factory=dict)
    chunks: List[MemoryChunk] = field(default_factory=list)
    
    # Status
    status: MemoryStatus = MemoryStatus.ACTIVE
    
    # Priority
    priority: MemoryPriority = MemoryPriority.MEDIUM
    
    # Relationships
    parent_id: Optional[str] = None
    related_ids: List[str] = field(default_factory=list)
    
    # Index
    index: MemoryIndex = field(default_factory=MemoryIndex)
    graph: Dict[str, MemoryNode] = field(default_factory=dict)
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Consolidation
    consolidation_count: int = 0
    compression_ratio: float = 1.0
    
    # Telemetry
    access_count: int = 0
    relevance_score: float = 0.0
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_chunk(self, content: str, importance: float = 0.5) -> MemoryChunk:
        """Add a chunk to memory."""
        chunk = MemoryChunk(
            id=f"{self.id}-chunk-{len(self.chunks)}",
            content=content,
            importance=importance,
        )
        self.chunks.append(chunk)
        self.updated_at = datetime.now()
        
        words = content.lower().split()
        for word in words:
            if len(word) > 2:
                if word not in self.index.keywords:
                    self.index.keywords[word] = []
                self.index.keywords[word].append(chunk.id)
        
        return chunk
    
    def get_relevant_chunks(self, threshold: float = 0.3) -> List[MemoryChunk]:
        """Get chunks above importance threshold."""
        return [c for c in self.chunks if c.importance >= threshold]
    
    def consolidate(self) -> None:
        """Consolidate memory chunks."""
        if not self.chunks:
            return
        self.consolidation_count += 1
        self.compression_ratio = 0.8
