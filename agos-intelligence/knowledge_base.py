#!/usr/bin/env python3
"""
AGOS Intelligence - Knowledge Base
================================

Evidence-based knowledge for intelligence.
Every piece of knowledge has source, evidence, and lineage.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json


class KnowledgeSource(Enum):
    """Sources of knowledge."""
    REPOSITORY_ANALYSIS = "repository_analysis"
    BENCHMARK = "benchmark"
    USER_FEEDBACK = "user_feedback"
    ARI_RESULT = "ari_result"
    ACADEMY = "academy"
    MANUAL = "manual"
    PROVIDER_METRICS = "provider_metrics"


class EvidenceType(Enum):
    """Types of evidence."""
    STATISTICAL = "statistical"       # From data analysis
    EMPIRICAL = "empirical"           # From experiments
    TESTIMONIAL = "testimonial"       # From users/experts
    AUTHORITATIVE = "authoritative"  # From official sources


@dataclass(frozen=True)
class Evidence:
    """Evidence supporting knowledge."""
    evidence_id: str
    evidence_type: EvidenceType
    source: KnowledgeSource
    content: Dict[str, Any]
    confidence: float  # 0-1
    timestamp: str
    lineage: Tuple[str, ...] = ()  # IDs of prior evidence
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "source": self.source.value,
            "content": self.content,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "lineage": list(self.lineage),
        }


@dataclass
class IntelligenceKnowledge:
    """
    A piece of intelligence knowledge.
    
    Requirements:
    - Source: Where knowledge came from
    - Evidence: Proof supporting knowledge
    - Confidence: How confident we are (0-1)
    - Version: For tracking changes
    - Timestamp: When knowledge was created
    - Lineage: How knowledge evolved
    """
    knowledge_id: str
    topic: str                      # Main topic
    statement: str                   # The knowledge statement
    category: str                   # e.g., "architecture", "best_practice"
    
    # Evidence supporting this knowledge
    evidence: Tuple[Evidence, ...]
    
    # Metadata
    confidence: float               # Overall confidence (0-1)
    version: str = "1.0"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Lineage (how knowledge evolved)
    lineage: Tuple[str, ...] = ()   # IDs of prior knowledge versions
    
    # Tags for search
    tags: Tuple[str, ...] = ()
    
    # Source information
    primary_source: Optional[str] = None
    author: Optional[str] = None
    
    def is_verified(self) -> bool:
        """Check if knowledge is verified with sufficient evidence."""
        return (
            len(self.evidence) >= 2 and
            self.confidence >= 0.7
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "topic": self.topic,
            "statement": self.statement,
            "category": self.category,
            "evidence": [e.to_dict() for e in self.evidence],
            "confidence": self.confidence,
            "version": self.version,
            "timestamp": self.timestamp,
            "lineage": list(self.lineage),
            "tags": list(self.tags),
            "primary_source": self.primary_source,
            "author": self.author,
            "is_verified": self.is_verified(),
        }


class KnowledgeBase:
    """
    The intelligence knowledge base.
    
    Manages:
    - Knowledge entries
    - Evidence
    - Search and retrieval
    - Knowledge evolution
    """
    
    def __init__(self):
        self._knowledge: Dict[str, IntelligenceKnowledge] = {}
        self._evidence: Dict[str, Evidence] = {}
        self._topic_index: Dict[str, Set[str]] = {}  # topic -> knowledge_ids
        self._tag_index: Dict[str, Set[str]] = {}     # tag -> knowledge_ids
        self._category_index: Dict[str, Set[str]] = {}  # category -> knowledge_ids
    
    def add_knowledge(self, knowledge: IntelligenceKnowledge) -> str:
        """Add knowledge to the base."""
        self._knowledge[knowledge.knowledge_id] = knowledge
        
        # Update indices
        topic = knowledge.topic.lower()
        if topic not in self._topic_index:
            self._topic_index[topic] = set()
        self._topic_index[topic].add(knowledge.knowledge_id)
        
        for tag in knowledge.tags:
            tag_lower = tag.lower()
            if tag_lower not in self._tag_index:
                self._tag_index[tag_lower] = set()
            self._tag_index[tag_lower].add(knowledge.knowledge_id)
        
        category = knowledge.category.lower()
        if category not in self._category_index:
            self._category_index[category] = set()
        self._category_index[category].add(knowledge.knowledge_id)
        
        # Store evidence
        for ev in knowledge.evidence:
            self._evidence[ev.evidence_id] = ev
        
        return knowledge.knowledge_id
    
    def get_knowledge(self, knowledge_id: str) -> Optional[IntelligenceKnowledge]:
        """Get knowledge by ID."""
        return self._knowledge.get(knowledge_id)
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self._evidence.get(evidence_id)
    
    def search(
        self,
        query: Optional[str] = None,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        limit: int = 10
    ) -> List[IntelligenceKnowledge]:
        """Search for knowledge."""
        results = set(self._knowledge.keys())
        
        # Filter by topic
        if topic:
            topic_results = self._topic_index.get(topic.lower(), set())
            results &= topic_results
        
        # Filter by category
        if category:
            cat_results = self._category_index.get(category.lower(), set())
            results &= cat_results
        
        # Filter by tags
        if tags:
            for tag in tags:
                tag_results = self._tag_index.get(tag.lower(), set())
                results &= tag_results
        
        # Filter by confidence
        results = {
            kid for kid in results
            if self._knowledge[kid].confidence >= min_confidence
        }
        
        # Filter by query
        if query:
            query_lower = query.lower()
            query_results = {
                kid for kid in results
                if query_lower in self._knowledge[kid].statement.lower() or
                   query_lower in self._knowledge[kid].topic.lower()
            }
            results &= query_results
        
        # Sort by confidence and get results
        sorted_ids = sorted(
            results,
            key=lambda kid: self._knowledge[kid].confidence,
            reverse=True
        )
        
        return [self._knowledge[kid] for kid in sorted_ids[:limit]]
    
    def query(self, topic: str, limit: int = 5) -> List[Evidence]:
        """Query evidence for a topic."""
        knowledge_list = self.search(topic=topic, limit=limit)
        
        evidence_list = []
        for knowledge in knowledge_list:
            evidence_list.extend(knowledge.evidence)
        
        # Sort by confidence
        evidence_list.sort(key=lambda e: e.confidence, reverse=True)
        
        return evidence_list[:limit]
    
    def add_evidence_to_knowledge(
        self,
        knowledge_id: str,
        evidence: Evidence
    ) -> bool:
        """Add additional evidence to existing knowledge."""
        knowledge = self._knowledge.get(knowledge_id)
        if not knowledge:
            return False
        
        # Update confidence based on new evidence
        total_confidence = (
            knowledge.confidence * len(knowledge.evidence) +
            evidence.confidence
        ) / (len(knowledge.evidence) + 1)
        
        # Create new version with additional evidence
        new_evidence = knowledge.evidence + (evidence,)
        
        updated_knowledge = IntelligenceKnowledge(
            knowledge_id=knowledge.knowledge_id,
            topic=knowledge.topic,
            statement=knowledge.statement,
            category=knowledge.category,
            evidence=new_evidence,
            confidence=total_confidence,
            version=f"{float(knowledge.version.split('.')[0]) + 1}.0",
            timestamp=datetime.utcnow().isoformat(),
            lineage=knowledge.lineage + (knowledge.knowledge_id,),
            tags=knowledge.tags,
            primary_source=knowledge.primary_source,
            author=knowledge.author,
        )
        
        # Update knowledge
        self._knowledge[knowledge_id] = updated_knowledge
        
        # Store evidence
        self._evidence[evidence.evidence_id] = evidence
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        total_knowledge = len(self._knowledge)
        total_evidence = len(self._evidence)
        
        by_category = {}
        by_source = {}
        avg_confidence = 0.0
        
        for knowledge in self._knowledge.values():
            # By category
            cat = knowledge.category
            by_category[cat] = by_category.get(cat, 0) + 1
            
            # By source
            for ev in knowledge.evidence:
                source = ev.source.value
                by_source[source] = by_source.get(source, 0) + 1
            
            avg_confidence += knowledge.confidence
        
        avg_confidence = avg_confidence / total_knowledge if total_knowledge > 0 else 0
        
        return {
            "total_knowledge": total_knowledge,
            "total_evidence": total_evidence,
            "by_category": by_category,
            "by_source": by_source,
            "average_confidence": round(avg_confidence, 3),
            "topics_indexed": len(self._topic_index),
            "tags_indexed": len(self._tag_index),
        }
    
    def export_knowledge(self, format: str = "json") -> Dict[str, Any]:
        """Export knowledge base."""
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "knowledge": [k.to_dict() for k in self._knowledge.values()],
            "evidence": [e.to_dict() for e in self._evidence.values()],
        }
