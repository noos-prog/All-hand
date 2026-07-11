"""
Memory Evolution Module
=====================

Self-evolving memory system with automatic optimization and consolidation.
Enables AGOS to maintain persistent engineering memory.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set

MEMORY_TYPES = [
    "Architectures", "Patterns", "Anti-Patterns", "Incidents", "Failures",
    "Optimizations", "Benchmarks", "Experiments", "Refactorings", "Reviews",
    "Security Findings", "Performance Findings", "Deployment Findings"
]


@dataclass
class EngineeringMemory:
    """A single memory entry in the engineering memory system."""
    memory_id: str
    type: str
    content: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    confidence: float = 1.0
    relevance_score: float = 0.0
    access_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def touch(self) -> None:
        """Record an access to this memory."""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()
        self.relevance_score = min(1.0, self.relevance_score + 0.01)
    
    def update(self, content: str, evidence: Optional[Dict[str, Any]] = None) -> None:
        """Update memory content."""
        self.content = content
        if evidence:
            self.evidence.update(evidence)
        self.updated_at = datetime.utcnow()


class SemanticSearch:
    """Semantic search across memory entries."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
    
    def search(self, query: str, limit: int = 10) -> List[EngineeringMemory]:
        """Search memories by semantic similarity."""
        query_lower = query.lower()
        results = []
        
        for memory in self.memory_system.memories.values():
            content_lower = memory.content.lower()
            if query_lower in content_lower:
                memory.touch()
                results.append(memory)
            elif any(tag in content_lower for tag in query.split()):
                memory.touch()
                results.append(memory)
        
        results.sort(key=lambda m: (m.relevance_score, m.confidence, -m.memory_id))
        return results[:limit]
    
    def search_by_tags(self, tags: Set[str], limit: int = 10) -> List[EngineeringMemory]:
        """Search memories by tags."""
        results = []
        for memory in self.memory_system.memories.values():
            if tags.intersection(memory.tags):
                memory.touch()
                results.append(memory)
        
        results.sort(key=lambda m: (m.relevance_score, -m.memory_id))
        return results[:limit]


class GraphSearch:
    """Graph-based search across memory relationships."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
        self.relationships: List[Dict[str, Any]] = []
    
    def search(self, entity_id: str) -> List[EngineeringMemory]:
        """Find memories related to an entity."""
        related_ids = {entity_id}
        
        for rel in self.relationships:
            if rel.get("source") == entity_id:
                related_ids.add(rel.get("target"))
            elif rel.get("target") == entity_id:
                related_ids.add(rel.get("source"))
        
        results = []
        for memory in self.memory_system.memories.values():
            if memory.memory_id in related_ids:
                memory.touch()
                results.append(memory)
        
        return results
    
    def add_relationship(self, source: str, target: str, relationship_type: str) -> None:
        """Add a relationship between memories."""
        self.relationships.append({
            "source": source,
            "target": target,
            "type": relationship_type,
            "created_at": datetime.utcnow().isoformat(),
        })


class EvidenceSearch:
    """Search memories by evidence type and quality."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
    
    def search(self, evidence_type: str, min_confidence: float = 0.0) -> List[EngineeringMemory]:
        """Find memories with specific evidence types."""
        results = []
        for memory in self.memory_system.memories.values():
            if evidence_type in memory.evidence and memory.confidence >= min_confidence:
                memory.touch()
                results.append(memory)
        
        results.sort(key=lambda m: (m.confidence, m.relevance_score))
        return results
    
    def search_by_sources(self, sources: List[str]) -> List[EngineeringMemory]:
        """Find memories with specific evidence sources."""
        results = []
        for memory in self.memory_system.memories.values():
            if any(source in memory.evidence.get("sources", []) for source in sources):
                memory.touch()
                results.append(memory)
        return results


class SimilaritySearch:
    """Find similar memories based on content and features."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
    
    def calculate_similarity(self, m1: EngineeringMemory, m2: EngineeringMemory) -> float:
        """Calculate similarity between two memories."""
        if m1.type != m2.type:
            return 0.0
        
        score = 0.0
        
        # Tag similarity
        common_tags = m1.tags.intersection(m2.tags)
        total_tags = m1.tags.union(m2.tags)
        if total_tags:
            score += len(common_tags) / len(total_tags) * 0.3
        
        # Content similarity (simple word overlap)
        words1 = set(m1.content.lower().split())
        words2 = set(m2.content.lower().split())
        common_words = words1.intersection(words2)
        total_words = words1.union(words2)
        if total_words:
            score += len(common_words) / len(total_words) * 0.4
        
        # Evidence similarity
        if m1.evidence.keys() == m2.evidence.keys():
            score += 0.3
        
        return score
    
    def search(self, memory: EngineeringMemory, limit: int = 5) -> List[EngineeringMemory]:
        """Find similar memories."""
        similarities = []
        for m in self.memory_system.memories.values():
            if m.memory_id != memory.memory_id:
                sim = self.calculate_similarity(memory, m)
                if sim > 0.2:
                    similarities.append((m, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [m for m, _ in similarities[:limit]]


class RecommendationEngine:
    """Engine for recommending relevant memories based on context."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
    
    def recommend(self, context: Dict[str, Any], limit: int = 5) -> List[EngineeringMemory]:
        """Recommend memories based on context."""
        results = []
        context_tags = set(context.get("tags", []))
        context_type = context.get("type")
        
        for memory in self.memory_system.memories.values():
            score = 0.0
            
            # Type match
            if context_type and memory.type == context_type:
                score += 0.4
            
            # Tag overlap
            if context_tags:
                tag_overlap = len(context_tags.intersection(memory.tags))
                score += tag_overlap * 0.1
            
            # High relevance
            if memory.relevance_score > 0.5:
                score += 0.2
            
            # Frequently accessed
            if memory.access_count > 5:
                score += 0.1
            
            if score > 0.3:
                results.append((memory, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [m for m, _ in results[:limit]]


class MemoryOptimizer:
    """Optimizes memory storage and retrieval."""
    
    def __init__(self, memory_system: MemoryEvolution):
        self.memory_system = memory_system
    
    def optimize(self, max_memories: Optional[int] = None) -> Dict[str, Any]:
        """Optimize memory storage by removing low-value memories."""
        removed = []
        
        if max_memories:
            sorted_memories = sorted(
                self.memory_system.memories.values(),
                key=lambda m: (m.relevance_score, m.access_count, m.confidence),
            )
            
            to_remove = len(self.memory_system.memories) - max_memories
            if to_remove > 0:
                for memory in sorted_memories[:to_remove]:
                    if memory.relevance_score < 0.2:
                        del self.memory_system.memories[memory.memory_id]
                        removed.append(memory.memory_id)
        
        return {
            "removed": removed,
            "remaining": len(self.memory_system.memories),
        }
    
    def consolidate(self, similarity_threshold: float = 0.7) -> int:
        """Consolidate similar memories."""
        consolidated = 0
        memory_list = list(self.memory_system.memories.values())
        
        for i, m1 in enumerate(memory_list):
            for m2 in memory_list[i + 1:]:
                if m1.type == m2.type:
                    sim_engine = SimilaritySearch(self.memory_system)
                    sim = sim_engine.calculate_similarity(m1, m2)
                    
                    if sim >= similarity_threshold:
                        # Keep the one with higher confidence
                        keeper = m1 if m1.confidence >= m2.confidence else m2
                        discarded = m2 if keeper == m1 else m1
                        
                        # Update evidence
                        keeper.evidence.update(discarded.evidence)
                        keeper.tags.update(discarded.tags)
                        
                        del self.memory_system.memories[discarded.memory_id]
                        consolidated += 1
        
        return consolidated


class MemoryEvolution:
    """
    Self-evolving memory system for engineering knowledge.
    Maintains persistent memory with automatic optimization.
    """
    
    def __init__(self, memory_id: Optional[str] = None):
        self.memory_id = memory_id or f"mem_{uuid.uuid4().hex[:8]}"
        self.memories: Dict[str, EngineeringMemory] = {}
        self.semantic_search = SemanticSearch(self)
        self.graph_search = GraphSearch(self)
        self.evidence_search = EvidenceSearch(self)
        self.similarity_search = SimilaritySearch(self)
        self.recommendations = RecommendationEngine(self)
        self.optimizer = MemoryOptimizer(self)
    
    def store(
        self,
        memory_type: str,
        content: str,
        evidence: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None,
    ) -> EngineeringMemory:
        """Store a new memory."""
        memory = EngineeringMemory(
            memory_id=f"mem_{uuid.uuid4().hex[:8]}",
            type=memory_type,
            content=content,
            evidence=evidence or {},
            tags=tags or set(),
        )
        self.memories[memory.memory_id] = memory
        return memory
    
    def get(self, memory_id: str) -> Optional[EngineeringMemory]:
        """Retrieve a memory by ID."""
        if memory_id in self.memories:
            self.memories[memory_id].touch()
            return self.memories[memory_id]
        return None
    
    def evolve(self) -> Dict[str, Any]:
        """Evolve the memory system."""
        optimization_result = self.optimizer.optimize()
        consolidated = self.optimizer.consolidate()
        
        return {
            "optimization": optimization_result,
            "consolidated": consolidated,
            "total_memories": len(self.memories),
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        by_type: Dict[str, int] = {}
        for memory in self.memories.values():
            by_type[memory.type] = by_type.get(memory.type, 0) + 1
        
        return {
            "memory_id": self.memory_id,
            "total_memories": len(self.memories),
            "by_type": by_type,
            "memory_types": MEMORY_TYPES,
            "total_accesses": sum(m.access_count for m in self.memories.values()),
            "average_confidence": sum(m.confidence for m in self.memories.values()) / len(self.memories) if self.memories else 0,
        }


# Backwards compatibility
UniversalEngineeringMemory = MemoryEvolution
