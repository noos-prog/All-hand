"""Universal Memory Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from .models import (
    Memory, MemoryType, MemoryStatus, MemoryPriority,
    MemoryChunk, MemoryIndex, MemoryNode
)


class MemoryRuntime:
    """Universal Memory Runtime."""
    
    def __init__(self):
        """Initialize memory runtime."""
        self.memories: Dict[str, Memory] = {}
        self.working_memory: Optional[Memory] = None
        
        # Global index
        self.index: Dict[str, Set[str]] = {}
    
    def create_memory(
        self,
        name: str,
        memory_type: MemoryType,
        priority: MemoryPriority = MemoryPriority.MEDIUM,
        parent_id: Optional[str] = None,
    ) -> Memory:
        """Create new memory."""
        memory_id = self._generate_id(name)
        
        memory = Memory(
            id=memory_id,
            name=name,
            memory_type=memory_type,
            priority=priority,
            parent_id=parent_id,
        )
        
        self.memories[memory_id] = memory
        
        # If it's working memory, store reference
        if memory_type == MemoryType.WORKING:
            self.working_memory = memory
        
        # If it has parent, add to parent's related
        if parent_id and parent_id in self.memories:
            self.memories[parent_id].related_ids.append(memory_id)
        
        return memory
    
    def get_memory(self, memory_id: str) -> Optional[Memory]:
        """Get memory by ID."""
        memory = self.memories.get(memory_id)
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.now()
        return memory
    
    def update_memory(self, memory_id: str, **kwargs) -> Optional[Memory]:
        """Update memory."""
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        
        for key, value in kwargs.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        memory.updated_at = datetime.now()
        return memory
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete memory."""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.status = MemoryStatus.DELETED
            return True
        return False
    
    def archive_memory(self, memory_id: str) -> bool:
        """Archive memory."""
        memory = self.memories.get(memory_id)
        if not memory:
            return False
        
        memory.status = MemoryStatus.ARCHIVED
        memory.updated_at = datetime.now()
        return True
    
    def list_memories(
        self,
        memory_type: Optional[MemoryType] = None,
        status: Optional[MemoryStatus] = None,
        priority: Optional[MemoryPriority] = None,
    ) -> List[Memory]:
        """List memories with filters."""
        results = list(self.memories.values())
        
        if memory_type:
            results = [m for m in results if m.memory_type == memory_type]
        
        if status:
            results = [m for m in results if m.status == status]
        
        if priority:
            results = [m for m in results if m.priority == priority]
        
        return results
    
    def add_to_memory(
        self,
        memory_id: str,
        content: str,
        importance: float = 0.5,
    ) -> Optional[MemoryChunk]:
        """Add content to memory."""
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        
        chunk = memory.add_chunk(content, importance)
        
        # Update global index
        words = content.lower().split()
        for word in words:
            if len(word) > 2:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(memory_id)
        
        return chunk
    
    def retrieve(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
    ) -> List[Memory]:
        """Retrieve memories by query."""
        query_lower = query.lower()
        words = query_lower.split()
        
        candidate_ids: Set[str] = set()
        
        # Search in global index
        for word in words:
            if word in self.index:
                candidate_ids.update(self.index[word])
        
        # Get memories
        candidates = []
        for mid in candidate_ids:
            m = self.memories.get(mid)
            if m and m.status != MemoryStatus.DELETED:
                if memory_type is None or m.memory_type == memory_type:
                    candidates.append(m)
        
        # Sort by relevance (access count + priority)
        def relevance(m: Memory) -> float:
            return m.access_count * 0.3 + m.priority.value * 0.7 + m.relevance_score
        
        candidates.sort(key=relevance, reverse=True)
        
        return candidates[:limit]
    
    def consolidate(self, memory_id: str) -> bool:
        """Consolidate memory."""
        memory = self.memories.get(memory_id)
        if not memory:
            return False
        
        memory.consolidate()
        return True
    
    def compress(self, memory_id: str) -> bool:
        """Compress memory."""
        memory = self.memories.get(memory_id)
        if not memory:
            return False
        
        memory.status = MemoryStatus.COMPRESSED
        memory.compression_ratio = 0.5
        memory.updated_at = datetime.now()
        return True
    
    def get_working_memory(self) -> Optional[Memory]:
        """Get current working memory."""
        return self.working_memory
    
    def create_graph_connection(
        self,
        memory_id: str,
        node_type: str,
        content: str,
        connections: Optional[List[str]] = None,
    ) -> Optional[MemoryNode]:
        """Create a node in memory graph."""
        memory = self.memories.get(memory_id)
        if not memory:
            return None
        
        node = MemoryNode(
            id=self._generate_id(f"node-{memory_id}"),
            memory_id=memory_id,
            node_type=node_type,
            content=content,
            connections=connections or [],
        )
        
        memory.graph[node.id] = node
        memory.updated_at = datetime.now()
        
        return node
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        stats = {
            "total_memories": len(self.memories),
            "by_type": {},
            "by_status": {},
            "total_chunks": 0,
            "total_nodes": 0,
        }
        
        for m in self.memories.values():
            # By type
            type_name = m.memory_type.value
            stats["by_type"][type_name] = stats["by_type"].get(type_name, 0) + 1
            
            # By status
            status_name = m.status.value
            stats["by_status"][status_name] = stats["by_status"].get(status_name, 0) + 1
            
            # Counts
            stats["total_chunks"] += len(m.chunks)
            stats["total_nodes"] += len(m.graph)
        
        return stats
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
