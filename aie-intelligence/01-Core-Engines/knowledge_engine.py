#!/usr/bin/env python3
"""
AIE - Knowledge Engine
====================

The Knowledge Engine stores and retrieves facts, evidence, and patterns.
It is the foundation of the mathematical brain.

Unlike LLMs which learn patterns from text,
the Knowledge Engine stores verified facts with evidence chains.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class KnowledgeType(Enum):
    """Types of knowledge."""
    FACT = "fact"                     # Verified fact
    PATTERN = "pattern"              # Observed pattern
    RULE = "rule"                    # Inferred rule
    CORRELATION = "correlation"      # Statistical correlation
    CAUSATION = "causation"         # Causal relationship
    HEURISTIC = "heuristic"         # Learned heuristic


class EvidenceSource(Enum):
    """Sources of evidence."""
    LLM_CLAUDE = "llm_claude"
    LLM_GPT = "llm_gpt"
    LLM_GEMINI = "llm_gemini"
    LLM_DEEPSEEK = "llm_deepseek"
    BENCHMARK = "benchmark"
    USER_FEEDBACK = "user_feedback"
    REPOSITORY_ANALYSIS = "repository_analysis"
    MANUAL = "manual"


class NodeStatus(Enum):
    """Status of a knowledge node."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    CONTESTED = "contested"
    VERIFYING = "verifying"


@dataclass(frozen=True)
class Evidence:
    """
    Evidence supporting a piece of knowledge.
    
    Evidence is immutable and has a confidence score.
    """
    evidence_id: str
    source: EvidenceSource
    content: Any                       # The evidence content
    confidence: float                  # 0-1 confidence
    timestamp: str                     # When evidence was collected
    lineage: Tuple[str, ...] = ()     # Prior evidence IDs
    
    def supports(self, min_confidence: float = 0.5) -> bool:
        """Check if evidence is supportive."""
        return self.confidence >= min_confidence


@dataclass
class KnowledgeNode:
    """
    A node in the knowledge graph.
    
    Contains:
    - The knowledge itself
    - Evidence supporting it
    - Metadata
    - Relationships to other nodes
    """
    node_id: str
    knowledge_type: KnowledgeType
    statement: str                     # The knowledge statement
    content: Dict[str, Any]           # Structured content
    
    # Evidence chain
    evidence: Tuple[Evidence, ...] = ()
    supporting_count: int = 0
    contradicting_count: int = 0
    
    # Relationships
    parents: Tuple[str, ...] = ()     # Knowledge this depends on
    children: Tuple[str, ...] = ()    # Knowledge that depends on this
    related: Tuple[str, ...] = ()    # Related knowledge
    
    # Metadata
    status: NodeStatus = NodeStatus.ACTIVE
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    author: str = "system"
    
    # Computed properties
    confidence: float = 0.0
    uses_count: int = 0              # How many nodes use this
    
    def compute_confidence(self) -> float:
        """Compute confidence from evidence."""
        if not self.evidence:
            return 0.5  # Default
        
        total_confidence = sum(e.confidence for e in self.evidence)
        avg_confidence = total_confidence / len(self.evidence)
        
        # Penalize contradictions
        penalty = self.contradicting_count * 0.1
        final_confidence = max(0, avg_confidence - penalty)
        
        return round(final_confidence, 3)
    
    def is_verified(self, threshold: float = 0.7) -> bool:
        """Check if knowledge is verified."""
        return self.compute_confidence() >= threshold
    
    def get_evidence_strength(self) -> str:
        """Get human-readable evidence strength."""
        conf = self.compute_confidence()
        if conf >= 0.9:
            return "very_strong"
        elif conf >= 0.7:
            return "strong"
        elif conf >= 0.5:
            return "moderate"
        elif conf >= 0.3:
            return "weak"
        else:
            return "very_weak"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "knowledge_type": self.knowledge_type.value,
            "statement": self.statement,
            "content": self.content,
            "evidence_count": len(self.evidence),
            "confidence": self.compute_confidence(),
            "evidence_strength": self.get_evidence_strength(),
            "status": self.status.value,
            "parents": list(self.parents),
            "children": list(self.children),
            "created_at": self.created_at,
            "version": self.version,
        }


class KnowledgeGraph:
    """
    A graph of interconnected knowledge nodes.
    
    Features:
    - Add/remove nodes
    - Traverse relationships
    - Query by type, evidence, confidence
    - Find paths between nodes
    """
    
    def __init__(self):
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._type_index: Dict[KnowledgeType, Set[str]] = {}
        self._source_index: Dict[EvidenceSource, Set[str]] = {}
        self._initialized = False
    
    def add_node(self, node: KnowledgeNode) -> str:
        """Add a knowledge node to the graph."""
        # Compute confidence
        node.confidence = node.compute_confidence()
        
        # Store node
        self._nodes[node.node_id] = node
        
        # Update indices
        ktype = node.knowledge_type
        if ktype not in self._type_index:
            self._type_index[ktype] = set()
        self._type_index[ktype].add(node.node_id)
        
        # Update source index
        for evidence in node.evidence:
            source = evidence.source
            if source not in self._source_index:
                self._source_index[source] = set()
            self._source_index[source].add(node.node_id)
        
        # Update relationship counts
        for parent_id in node.parents:
            if parent_id in self._nodes:
                self._nodes[parent_id].uses_count += 1
        
        return node.node_id
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get a node by ID."""
        return self._nodes.get(node_id)
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the graph."""
        if node_id not in self._nodes:
            return False
        
        node = self._nodes[node_id]
        
        # Update parent nodes
        for parent_id in node.parents:
            if parent_id in self._nodes:
                parent = self._nodes[parent_id]
                # Remove this from parent's children
                new_children = tuple(c for c in parent.children if c != node_id)
                object.__setattr__(parent, 'children', new_children)
                parent.uses_count = max(0, parent.uses_count - 1)
        
        # Remove from indices
        ktype = node.knowledge_type
        if ktype in self._type_index:
            self._type_index[ktype].discard(node_id)
        
        for evidence in node.evidence:
            source = evidence.source
            if source in self._source_index:
                self._source_index[source].discard(node_id)
        
        # Remove node
        del self._nodes[node_id]
        return True
    
    def add_relationship(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_type: str = "related"
    ) -> bool:
        """Add a relationship between nodes."""
        if from_node_id not in self._nodes or to_node_id not in self._nodes:
            return False
        
        from_node = self._nodes[from_node_id]
        to_node = self._nodes[to_node_id]
        
        if relationship_type == "parent":
            # from_node depends on to_node
            if to_node_id not in from_node.parents:
                new_parents = from_node.parents + (to_node_id,)
                object.__setattr__(from_node, 'parents', new_parents)
            
            if from_node_id not in to_node.children:
                new_children = to_node.children + (from_node_id,)
                object.__setattr__(to_node, 'children', new_children)
                to_node.uses_count += 1
        
        elif relationship_type == "related":
            if to_node_id not in from_node.related:
                new_related = from_node.related + (to_node_id,)
                object.__setattr__(from_node, 'related', new_related)
            
            if from_node_id not in to_node.related:
                new_related = to_node.related + (from_node_id,)
                object.__setattr__(to_node, 'related', new_related)
        
        return True
    
    def find_path(self, from_id: str, to_id: str) -> Optional[List[str]]:
        """Find a path between two nodes using BFS."""
        if from_id not in self._nodes or to_id not in self._nodes:
            return None
        
        if from_id == to_id:
            return [from_id]
        
        # BFS
        visited = {from_id}
        queue = [(from_id, [from_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            node = self._nodes[current]
            neighbors = list(node.parents) + list(node.children) + list(node.related)
            
            for neighbor in neighbors:
                if neighbor == to_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def query(
        self,
        knowledge_type: Optional[KnowledgeType] = None,
        min_confidence: float = 0.0,
        source: Optional[EvidenceSource] = None,
        status: Optional[NodeStatus] = None,
        limit: int = 100
    ) -> List[KnowledgeNode]:
        """Query nodes with filters."""
        results = set(self._nodes.keys())
        
        # Filter by type
        if knowledge_type:
            results &= self._type_index.get(knowledge_type, set())
        
        # Filter by source
        if source:
            results &= self._source_index.get(source, set())
        
        # Filter by confidence
        if min_confidence > 0:
            results = {
                nid for nid in results
                if self._nodes[nid].compute_confidence() >= min_confidence
            }
        
        # Filter by status
        if status:
            results = {nid for nid in results if self._nodes[nid].status == status}
        
        # Sort by confidence
        sorted_ids = sorted(
            results,
            key=lambda nid: self._nodes[nid].compute_confidence(),
            reverse=True
        )
        
        return [self._nodes[nid] for nid in sorted_ids[:limit]]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        by_type = {kt.value: len(nids) for kt, nids in self._type_index.items()}
        by_status = {}
        avg_confidence = 0.0
        
        for node in self._nodes.values():
            status = node.status.value
            by_status[status] = by_status.get(status, 0) + 1
            avg_confidence += node.compute_confidence()
        
        avg_confidence = avg_confidence / len(self._nodes) if self._nodes else 0
        
        return {
            "total_nodes": len(self._nodes),
            "by_type": by_type,
            "by_status": by_status,
            "average_confidence": round(avg_confidence, 3),
            "verified_nodes": len(self.query(min_confidence=0.7)),
        }


class KnowledgeEngine:
    """
    The Knowledge Engine - first stage of AIE.
    
    Responsibilities:
    - Store facts, evidence, and patterns
    - Query knowledge by type, confidence, source
    - Maintain evidence chains
    - Compute knowledge confidence
    
    The Knowledge Engine does NOT:
    - Make decisions
    - Generate text
    - Reason about knowledge
    
    It only stores and retrieves.
    """
    
    def __init__(self):
        self.graph = KnowledgeGraph()
        self._evidence_store: Dict[str, Evidence] = {}
        self._initialized = True
    
    def add_knowledge(
        self,
        node_id: str,
        knowledge_type: KnowledgeType,
        statement: str,
        content: Dict[str, Any],
        evidence: List[Evidence],
        parents: List[str] = None
    ) -> KnowledgeNode:
        """Add knowledge to the engine."""
        node = KnowledgeNode(
            node_id=node_id,
            knowledge_type=knowledge_type,
            statement=statement,
            content=content,
            evidence=tuple(evidence),
            parents=tuple(parents or []),
        )
        
        self.graph.add_node(node)
        
        # Store evidence
        for ev in evidence:
            self._evidence_store[ev.evidence_id] = ev
        
        return node
    
    def get_knowledge(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get knowledge by ID."""
        return self.graph.get_node(node_id)
    
    def query_knowledge(
        self,
        knowledge_type: Optional[KnowledgeType] = None,
        min_confidence: float = 0.5,
        sources: List[EvidenceSource] = None
    ) -> List[KnowledgeNode]:
        """Query knowledge with filters."""
        if sources:
            # Get union of source results
            results = set()
            for source in sources:
                source_results = self.graph.query(source=source)
                results.update(r.node_id for r in source_results)
            
            # Filter and return
            filtered = [
                self.graph.get_node(nid) for nid in results
                if self.graph.get_node(nid) and
                self.graph.get_node(nid).compute_confidence() >= min_confidence
            ]
            return filtered
        
        return self.graph.query(
            knowledge_type=knowledge_type,
            min_confidence=min_confidence
        )
    
    def add_evidence_to_knowledge(
        self,
        node_id: str,
        evidence: Evidence
    ) -> bool:
        """Add evidence to existing knowledge."""
        node = self.graph.get_node(node_id)
        if not node:
            return False
        
        # Update evidence
        new_evidence = node.evidence + (evidence,)
        node.evidence = new_evidence
        
        # Recompute confidence
        node.confidence = node.compute_confidence()
        node.updated_at = datetime.utcnow().isoformat()
        
        # Store evidence
        self._evidence_store[evidence.evidence_id] = evidence
        
        return True
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self._evidence_store.get(evidence_id)
    
    def find_related_knowledge(
        self,
        node_id: str,
        depth: int = 1
    ) -> List[KnowledgeNode]:
        """Find related knowledge up to a certain depth."""
        node = self.graph.get_node(node_id)
        if not node:
            return []
        
        visited = {node_id}
        current_level = {node_id}
        
        for _ in range(depth):
            next_level = set()
            for current_id in current_level:
                current = self.graph.get_node(current_id)
                if current:
                    neighbors = (
                        list(current.parents) +
                        list(current.children) +
                        list(current.related)
                    )
                    for neighbor_id in neighbors:
                        if neighbor_id not in visited:
                            visited.add(neighbor_id)
                            next_level.add(neighbor_id)
            
            current_level = next_level
        
        return [
            self.graph.get_node(nid)
            for nid in visited
            if nid != node_id and self.graph.get_node(nid)
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        graph_stats = self.graph.get_statistics()
        
        return {
            **graph_stats,
            "total_evidence": len(self._evidence_store),
            "evidence_by_source": {
                source.value: len(nids)
                for source, nids in self.graph._source_index.items()
            },
        }
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Export all knowledge."""
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "nodes": [n.to_dict() for n in self.graph._nodes.values()],
            "evidence": [
                {"evidence_id": e.evidence_id, "source": e.source.value}
                for e in self._evidence_store.values()
            ],
        }
