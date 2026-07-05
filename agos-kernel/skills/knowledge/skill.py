"""
AGOS Knowledge Skill
==================

Knowledge-based skill for information retrieval and reasoning.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class KnowledgeType(Enum):
    """Knowledge type."""
    FACT = "fact"
    CONCEPT = "concept"
    PROCEDURE = "procedure"
    RULE = "rule"
    PATTERN = "pattern"


@dataclass
class KnowledgeEntry:
    """A knowledge entry."""
    id: str
    content: str
    knowledge_type: KnowledgeType
    confidence: float = 1.0
    source: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.knowledge_type.value,
            "confidence": self.confidence,
            "source": self.source,
            "tags": self.tags,
        }


@dataclass
class KnowledgeSkill:
    """
    Knowledge Skill.
    
    Provides knowledge-based capabilities:
    - Information retrieval
    - Concept mapping
    - Reasoning chains
    - Fact checking
    
    Usage:
        skill = KnowledgeSkill()
        skill.add_fact("Python is a programming language", source="docs")
        
        facts = skill.query("programming")
        reasoning = skill.reason("What is Python?")
    """
    
    def __init__(self):
        """Initialize knowledge skill."""
        self._knowledge: Dict[str, KnowledgeEntry] = {}
        self._index: Dict[str, List[str]] = {}  # tag -> entry IDs
    
    def add_fact(self, content: str, source: str = "", tags: List[str] = None) -> KnowledgeEntry:
        """Add a fact."""
        entry = KnowledgeEntry(
            id=f"fact-{uuid.uuid4().hex[:8]}",
            content=content,
            knowledge_type=KnowledgeType.FACT,
            source=source,
            tags=tags or [],
        )
        self._knowledge[entry.id] = entry
        self._index_entry(entry)
        return entry
    
    def add_concept(self, content: str, source: str = "", tags: List[str] = None) -> KnowledgeEntry:
        """Add a concept."""
        entry = KnowledgeEntry(
            id=f"concept-{uuid.uuid4().hex[:8]}",
            content=content,
            knowledge_type=KnowledgeType.CONCEPT,
            source=source,
            tags=tags or [],
        )
        self._knowledge[entry.id] = entry
        self._index_entry(entry)
        return entry
    
    def add_procedure(self, content: str, source: str = "", tags: List[str] = None) -> KnowledgeEntry:
        """Add a procedure."""
        entry = KnowledgeEntry(
            id=f"procedure-{uuid.uuid4().hex[:8]}",
            content=content,
            knowledge_type=KnowledgeType.PROCEDURE,
            source=source,
            tags=tags or [],
        )
        self._knowledge[entry.id] = entry
        self._index_entry(entry)
        return entry
    
    def query(self, query: str, knowledge_type: Optional[KnowledgeType] = None, limit: int = 10) -> List[KnowledgeEntry]:
        """Query knowledge base."""
        results = []
        query_lower = query.lower()
        
        for entry in self._knowledge.values():
            if knowledge_type and entry.knowledge_type != knowledge_type:
                continue
            
            # Simple keyword matching
            if query_lower in entry.content.lower():
                results.append(entry)
                continue
            
            # Tag matching
            for tag in entry.tags:
                if query_lower in tag.lower():
                    results.append(entry)
                    break
        
        return sorted(results, key=lambda e: e.confidence, reverse=True)[:limit]
    
    def reason(self, question: str) -> List[str]:
        """Perform reasoning over knowledge base."""
        facts = self.query(question, KnowledgeType.FACT, limit=5)
        concepts = self.query(question, KnowledgeType.CONCEPT, limit=3)
        
        reasoning_steps = []
        
        # Build reasoning chain
        if facts:
            reasoning_steps.append(f"Relevant facts:")
            for fact in facts:
                reasoning_steps.append(f"  - {fact.content}")
        
        if concepts:
            reasoning_steps.append(f"Related concepts:")
            for concept in concepts:
                reasoning_steps.append(f"  - {concept.content}")
        
        if not reasoning_steps:
            reasoning_steps.append(f"No relevant knowledge found for: {question}")
        
        return reasoning_steps
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge statistics."""
        by_type = {}
        for entry in self._knowledge.values():
            type_name = entry.knowledge_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        return {
            "total_entries": len(self._knowledge),
            "by_type": by_type,
            "total_tags": len(self._index),
        }
    
    def _index_entry(self, entry: KnowledgeEntry) -> None:
        """Index an entry."""
        for tag in entry.tags:
            if tag not in self._index:
                self._index[tag] = []
            self._index[tag].append(entry.id)
    
    def export_knowledge(self) -> List[Dict[str, Any]]:
        """Export all knowledge."""
        return [e.to_dict() for e in self._knowledge.values()]
    
    def import_knowledge(self, entries: List[Dict[str, Any]]) -> int:
        """Import knowledge entries."""
        count = 0
        for entry_data in entries:
            try:
                entry = KnowledgeEntry(
                    id=entry_data.get("id", f"import-{uuid.uuid4().hex[:8]}"),
                    content=entry_data["content"],
                    knowledge_type=KnowledgeType(entry_data.get("type", "fact")),
                    confidence=entry_data.get("confidence", 1.0),
                    source=entry_data.get("source", ""),
                    tags=entry_data.get("tags", []),
                )
                self._knowledge[entry.id] = entry
                self._index_entry(entry)
                count += 1
            except:
                pass
        return count


# Global instance
_knowledge_skill: Optional[KnowledgeSkill] = None


def get_knowledge_skill() -> KnowledgeSkill:
    """Get the global knowledge skill instance."""
    global _knowledge_skill
    if _knowledge_skill is None:
        _knowledge_skill = KnowledgeSkill()
    return _knowledge_skill
