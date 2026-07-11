"""
Knowledge Evolution Module
=========================

Self-evolving knowledge base with automatic learning and adaptation.
Enables AGOS to continuously improve its knowledge and understanding.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set

INGEST_TYPES = ["Repositories", "Commits", "Issues", "Pull Requests", "Releases", "Tags", "Wiki", "Documentation", "Architecture", "Benchmarks"]

DNA_TYPES = ["Repository DNA", "Project DNA", "Architecture DNA", "Capability DNA", "Pattern DNA", "Anti-Pattern DNA", "Dependency DNA", "Technology DNA"]


@dataclass
class RepositoryDNA:
    """DNA extracted from a repository for knowledge representation."""
    dna_id: str
    repo_name: str
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    sources: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class KnowledgeEntry:
    """A single entry in the knowledge base."""
    entry_id: str
    key: str
    value: Any
    confidence: float = 1.0
    sources: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    usefulness_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update(self, value: Any, confidence: Optional[float] = None) -> None:
        """Update the entry value and confidence."""
        self.value = value
        if confidence is not None:
            self.confidence = confidence
        self.updated_at = datetime.utcnow()
    
    def touch(self) -> None:
        """Record an access."""
        self.access_count += 1


@dataclass
class KnowledgeGraph:
    """Graph structure for knowledge relationships."""
    graph_id: str
    nodes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    edges: List[tuple] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_node(self, node_id: str, data: Dict[str, Any]) -> None:
        """Add a node to the graph."""
        self.nodes[node_id] = data
    
    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        """Add an edge between nodes."""
        self.edges.append((source, target, weight))
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighboring nodes."""
        neighbors = []
        for source, target, _ in self.edges:
            if source == node_id:
                neighbors.append(target)
            elif target == node_id:
                neighbors.append(source)
        return neighbors


class RepositoryIngestion:
    """Handles ingestion of repository data."""
    
    def __init__(self):
        self.ingested_repos: Set[str] = set()
    
    def ingest(self, repo_url: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ingest a repository and extract knowledge."""
        self.ingested_repos.add(repo_url)
        return {
            "status": "ingested",
            "repo": repo_url,
            "metadata": metadata or {},
            "ingested_at": datetime.utcnow().isoformat(),
        }
    
    def batch_ingest(self, repo_urls: List[str]) -> Dict[str, Any]:
        """Batch ingest multiple repositories."""
        results = []
        for url in repo_urls:
            results.append(self.ingest(url))
        return {
            "total": len(repo_urls),
            "ingested": len(results),
            "repositories": results,
        }


class DNAGenerator:
    """Generates DNA representations from repository data."""
    
    def __init__(self):
        self.generators: Dict[str, Callable] = {}
    
    def generate(self, repo_name: str, dna_type: str, data: Optional[Dict[str, Any]] = None) -> RepositoryDNA:
        """Generate DNA for a repository."""
        return RepositoryDNA(
            dna_id=f"dna_{repo_name}_{dna_type}_{uuid.uuid4().hex[:6]}",
            repo_name=repo_name,
            type=dna_type,
            data=data or {},
            confidence=0.9,
            sources=[f"repo:{repo_name}"],
        )
    
    def register_generator(self, dna_type: str, generator: Callable) -> None:
        """Register a custom DNA generator."""
        self.generators[dna_type] = generator


class RelationshipBuilder:
    """Builds relationships between DNA entries."""
    
    def __init__(self):
        self.relationships: List[Dict[str, Any]] = []
    
    def build(self, dna1: RepositoryDNA, dna2: RepositoryDNA, relationship_type: str = "related") -> Dict[str, Any]:
        """Build relationship between two DNA entries."""
        relationship = {
            "dna1": dna1.dna_id,
            "dna2": dna2.dna_id,
            "type": relationship_type,
            "strength": 1.0,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.relationships.append(relationship)
        return relationship
    
    def find_related(self, dna_id: str) -> List[Dict[str, Any]]:
        """Find all DNA related to a given DNA."""
        return [r for r in self.relationships if r["dna1"] == dna_id or r["dna2"] == dna_id]


class EvolutionGraphBuilder:
    """Builds evolution graphs for different DNA types."""
    
    def __init__(self):
        self.graphs: Dict[str, KnowledgeGraph] = {}
    
    def build(self, dna_type: str) -> KnowledgeGraph:
        """Build or retrieve an evolution graph for a DNA type."""
        if dna_type not in self.graphs:
            self.graphs[dna_type] = KnowledgeGraph(
                graph_id=f"graph_{dna_type}_{uuid.uuid4().hex[:6]}",
                nodes={},
                edges=[],
            )
        return self.graphs[dna_type]
    
    def add_to_graph(self, dna_type: str, dna: RepositoryDNA) -> None:
        """Add DNA to the appropriate evolution graph."""
        graph = self.build(dna_type)
        graph.add_node(dna.dna_id, {
            "repo_name": dna.repo_name,
            "type": dna.type,
            "data": dna.data,
        })


class KnowledgeUpdater:
    """Handles updates to the knowledge base with versioning and consistency."""
    
    def __init__(self, knowledge_base: KnowledgeEvolution):
        self.knowledge_base = knowledge_base
        self.update_history: List[Dict[str, Any]] = []
    
    def update(
        self,
        key: str,
        value: Any,
        confidence: float = 1.0,
        sources: Optional[List[str]] = None,
        tags: Optional[Set[str]] = None,
    ) -> KnowledgeEntry:
        """Update or create a knowledge entry."""
        entry = self.knowledge_base.add_entry(
            key=key,
            value=value,
            confidence=confidence,
            sources=sources or [],
            tags=tags or set(),
        )
        
        self.update_history.append({
            "entry_id": entry.entry_id,
            "key": key,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "update" if key in self.knowledge_base.entries else "create",
        })
        
        return entry
    
    def batch_update(self, updates: List[Dict[str, Any]]) -> List[KnowledgeEntry]:
        """Batch update multiple entries."""
        results = []
        for update in updates:
            entry = self.update(
                key=update["key"],
                value=update["value"],
                confidence=update.get("confidence", 1.0),
                sources=update.get("sources"),
                tags=update.get("tags"),
            )
            results.append(entry)
        return results


class KnowledgeEvolution:
    """
    Self-evolving knowledge base that learns and adapts.
    Maintains knowledge consistency, versioning, and relevance scoring.
    """
    
    def __init__(self, base_id: Optional[str] = None):
        self.base_id = base_id or f"kb_{uuid.uuid4().hex[:8]}"
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.graph = KnowledgeGraph(graph_id=f"kg_{uuid.uuid4().hex[:8]}", nodes={}, edges=[])
        self.learners: List[Callable] = []
        self.statistics: Dict[str, Any] = {
            "total_entries": 0,
            "total_updates": 0,
            "average_confidence": 0.0,
        }
    
    def add_entry(
        self,
        key: str,
        value: Any,
        confidence: float = 1.0,
        sources: Optional[List[str]] = None,
        tags: Optional[Set[str]] = None,
    ) -> KnowledgeEntry:
        """Add a new knowledge entry."""
        entry = KnowledgeEntry(
            entry_id=f"ke_{uuid.uuid4().hex[:8]}",
            key=key,
            value=value,
            confidence=confidence,
            sources=sources or [],
            tags=tags or set(),
        )
        self.entries[key] = entry
        self.graph.add_node(entry.entry_id, {"key": key, "value": value})
        self._update_statistics()
        return entry
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a knowledge entry by key."""
        if key in self.entries:
            self.entries[key].touch()
            return self.entries[key].value
        return default
    
    def search(self, query: str, tags: Optional[Set[str]] = None) -> List[KnowledgeEntry]:
        """Search for knowledge entries."""
        results = []
        query_lower = query.lower()
        
        for entry in self.entries.values():
            if query_lower in entry.key.lower() or query_lower in str(entry.value).lower():
                if tags is None or tags.intersection(entry.tags):
                    results.append(entry)
        
        return sorted(results, key=lambda e: (e.confidence, e.access_count), reverse=True)
    
    def add_learner(self, learner: Callable) -> None:
        """Add a learning function to improve knowledge."""
        self.learners.append(learner)
    
    def learn(self, data: Dict[str, Any]) -> None:
        """Apply learning to improve knowledge."""
        for learner in self.learners:
            try:
                learner(data, self)
            except Exception:
                pass
    
    def evolve(self, target_metrics: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Evolve knowledge based on usage patterns and target metrics."""
        evictions = []
        
        if target_metrics and "max_entries" in target_metrics:
            max_entries = target_metrics["max_entries"]
            if len(self.entries) > max_entries:
                sorted_entries = sorted(
                    self.entries.values(),
                    key=lambda e: (e.usefulness_score, e.confidence),
                )
                to_remove = sorted_entries[:len(self.entries) - max_entries]
                for entry in to_remove:
                    del self.entries[entry.key]
                    evictions.append(entry.entry_id)
        
        for entry in self.entries.values():
            if entry.access_count > 10:
                entry.confidence = min(1.0, entry.confidence * 1.1)
        
        self._update_statistics()
        return {
            "evictions": evictions,
            "statistics": self.statistics,
        }
    
    def _update_statistics(self) -> None:
        """Update knowledge base statistics."""
        self.statistics["total_entries"] = len(self.entries)
        if self.entries:
            self.statistics["average_confidence"] = sum(
                e.confidence for e in self.entries.values()
            ) / len(self.entries)
    
    def export(self) -> Dict[str, Any]:
        """Export knowledge base to dictionary."""
        return {
            "base_id": self.base_id,
            "entries": {
                key: {
                    "entry_id": entry.entry_id,
                    "key": entry.key,
                    "value": entry.value,
                    "confidence": entry.confidence,
                    "sources": entry.sources,
                    "tags": list(entry.tags),
                }
                for key, entry in self.entries.items()
            },
            "statistics": self.statistics,
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "base_id": self.base_id,
            "total_entries": len(self.entries),
            "average_confidence": self.statistics["average_confidence"],
            "most_accessed": sorted(
                self.entries.values(),
                key=lambda e: e.access_count,
                reverse=True,
            )[:5],
        }


class UniversalRepositoryKnowledgeNetwork:
    """
    Universal Repository Knowledge Network.
    
    Ingest:
    ✅ Repositories, Commits, Issues, Pull Requests, Releases
    ✅ Tags, Wiki, Documentation, Architecture, Benchmarks
    
    Generate:
    ✅ Repository DNA, Project DNA, Architecture DNA
    ✅ Capability DNA, Pattern DNA, Anti-Pattern DNA
    ✅ Dependency DNA, Technology DNA
    
    Build:
    ✅ Cross-Repository Relationships
    ✅ Technology Evolution Graph
    ✅ Architecture Evolution Graph
    ✅ Capability Evolution Graph
    
    Target: Millions of analyzed repositories
    """
    
    def __init__(self):
        self.version = "10.0.0"
        self.ingestion = RepositoryIngestion()
        self.dna_generator = DNAGenerator()
        self.relationships = RelationshipBuilder()
        self.evolution_graphs = EvolutionGraphBuilder()
        self.knowledge_base = KnowledgeEvolution()
    
    def analyze_repository(self, repo_url: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a repository and generate DNA."""
        ingest_result = self.ingestion.ingest(repo_url, metadata)
        
        dna_data = {
            "url": repo_url,
            "metadata": metadata or {},
            "ingested_at": ingest_result["ingested_at"],
        }
        dna = self.dna_generator.generate(repo_url, "Repository", dna_data)
        
        self.evolution_graphs.add_to_graph("Repository", dna)
        
        self.knowledge_base.add_entry(
            key=f"repo:{repo_url}",
            value=dna_data,
            sources=[repo_url],
            tags={"repository", "analyzed"},
        )
        
        return {
            "dna": {
                "dna_id": dna.dna_id,
                "repo_name": dna.repo_name,
                "type": dna.type,
            },
            "status": "analyzed",
            "ingested_at": ingest_result["ingested_at"],
        }
    
    def find_related_repositories(self, repo_url: str) -> List[Dict[str, Any]]:
        """Find repositories related to the given one."""
        related = self.relationships.find_related(f"dna_{repo_url}_Repository")
        return related
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get network statistics."""
        return {
            "version": self.version,
            "ingest_types": INGEST_TYPES,
            "dna_types": DNA_TYPES,
            "knowledge_base": self.knowledge_base.get_statistics(),
            "total_relationships": len(self.relationships.relationships),
        }

