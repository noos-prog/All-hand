"""Universal Knowledge Fabric Runtime."""
import hashlib
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from .models import (
    Knowledge, KnowledgeType, KnowledgeStatus, KnowledgeMetadata,
    KnowledgeRelationship, Evidence, EvidenceQuality, Validation, KnowledgeGraph
)


class KnowledgeRuntime:
    """Universal Knowledge Fabric Runtime."""
    
    def __init__(self):
        """Initialize knowledge runtime."""
        self.knowledge_store: Dict[str, Knowledge] = {}
        self.graph = KnowledgeGraph()
        self.index: Dict[str, Set[str]] = {}  # word -> knowledge IDs
        
        # Cache
        self.cache: Dict[str, Knowledge] = {}
        self.cache_enabled = True
    
    def create_knowledge(
        self,
        title: str,
        knowledge_type: KnowledgeType,
        content: Optional[Dict[str, Any]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        evidence: Optional[List[Evidence]] = None,
    ) -> Knowledge:
        """Create new knowledge."""
        knowledge_id = self._generate_id(title)
        
        metadata = KnowledgeMetadata(
            title=title,
            description=description,
            tags=tags or [],
        )
        
        knowledge = Knowledge(
            id=knowledge_id,
            knowledge_type=knowledge_type,
            metadata=metadata,
            content=content or {},
            evidence=evidence or [],
        )
        
        # Index knowledge
        self._index_knowledge(knowledge)
        
        # Add to graph
        self.graph.add_knowledge(knowledge)
        
        # Store
        self.knowledge_store[knowledge_id] = knowledge
        
        return knowledge
    
    def get_knowledge(self, knowledge_id: str) -> Optional[Knowledge]:
        """Get knowledge by ID."""
        # Check cache first
        if self.cache_enabled and knowledge_id in self.cache:
            k = self.cache[knowledge_id]
            k.usage_count += 1
            k.last_accessed = datetime.now()
            return k
        
        knowledge = self.knowledge_store.get(knowledge_id)
        if knowledge:
            knowledge.usage_count += 1
            knowledge.last_accessed = datetime.now()
            
            # Cache it
            if self.cache_enabled:
                self.cache[knowledge_id] = knowledge
            
            return knowledge
        
        return None
    
    def update_knowledge(self, knowledge_id: str, **kwargs) -> Optional[Knowledge]:
        """Update knowledge."""
        knowledge = self.knowledge_store.get(knowledge_id)
        if not knowledge:
            return None
        
        for key, value in kwargs.items():
            if hasattr(knowledge, key):
                setattr(knowledge, key, value)
        
        knowledge.updated_at = datetime.now()
        
        # Invalidate cache
        if knowledge_id in self.cache:
            del self.cache[knowledge_id]
        
        return knowledge
    
    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete knowledge."""
        if knowledge_id in self.knowledge_store:
            del self.knowledge_store[knowledge_id]
            
            # Remove from graph
            if knowledge_id in self.graph.nodes:
                del self.graph.nodes[knowledge_id]
            
            # Invalidate cache
            if knowledge_id in self.cache:
                del self.cache[knowledge_id]
            
            return True
        
        return False
    
    def list_knowledge(
        self,
        knowledge_type: Optional[KnowledgeType] = None,
        status: Optional[KnowledgeStatus] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Knowledge]:
        """List knowledge with filters."""
        results = list(self.knowledge_store.values())
        
        if knowledge_type:
            results = [k for k in results if k.knowledge_type == knowledge_type]
        
        if status:
            results = [k for k in results if k.status == status]
        
        if tags:
            results = [k for k in results if any(t in k.metadata.tags for t in tags)]
        
        return results
    
    def search_knowledge(self, query: str) -> List[Knowledge]:
        """Search knowledge by query."""
        query_lower = query.lower()
        results = []
        
        # Search in index
        for word in query_lower.split():
            if word in self.index:
                for kid in self.index[word]:
                    if kid not in results:
                        results.append(kid)
        
        # Get knowledge objects
        knowledge_results = []
        for kid in results:
            k = self.knowledge_store.get(kid)
            if k:
                knowledge_results.append(k)
        
        # Sort by relevance (usage count)
        knowledge_results.sort(key=lambda k: k.usage_count, reverse=True)
        
        return knowledge_results
    
    def add_evidence(self, knowledge_id: str, evidence: Evidence) -> bool:
        """Add evidence to knowledge."""
        knowledge = self.knowledge_store.get(knowledge_id)
        if not knowledge:
            return False
        
        knowledge.add_evidence(evidence)
        
        # Invalidate cache
        if knowledge_id in self.cache:
            del self.cache[knowledge_id]
        
        return True
    
    def validate_knowledge(self, knowledge_id: str, validator: str) -> bool:
        """Validate knowledge."""
        knowledge = self.knowledge_store.get(knowledge_id)
        if not knowledge:
            return False
        
        is_valid = knowledge.validate(validator)
        
        if is_valid:
            knowledge.status = KnowledgeStatus.VERIFIED
        
        # Invalidate cache
        if knowledge_id in self.cache:
            del self.cache[knowledge_id]
        
        return is_valid
    
    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        weight: float = 1.0,
    ) -> bool:
        """Add relationship between knowledge items."""
        if source_id not in self.knowledge_store or target_id not in self.knowledge_store:
            return False
        
        relationship = KnowledgeRelationship(
            id=self._generate_id(f"rel-{source_id}-{target_id}"),
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            weight=weight,
        )
        
        self.graph.add_edge(relationship)
        
        # Update knowledge related_to
        self.knowledge_store[source_id].related_to.append(target_id)
        
        return True
    
    def get_related_knowledge(self, knowledge_id: str) -> List[Knowledge]:
        """Get related knowledge."""
        related_ids = self.graph.get_connected(knowledge_id)
        return [self.knowledge_store[kid] for kid in related_ids if kid in self.knowledge_store]
    
    def compile_knowledge(self, knowledge_ids: List[str]) -> Dict[str, Any]:
        """Compile knowledge into a structured format."""
        compiled = {
            "compiled_at": datetime.now().isoformat(),
            "knowledge_ids": knowledge_ids,
            "items": [],
        }
        
        for kid in knowledge_ids:
            k = self.knowledge_store.get(kid)
            if k:
                compiled["items"].append({
                    "id": k.id,
                    "type": k.knowledge_type.value,
                    "title": k.metadata.title,
                    "content": k.content,
                    "evidence_count": len(k.evidence),
                    "validations": [
                        {
                            "validator": v.validator,
                            "is_valid": v.is_valid,
                        }
                        for v in k.validations
                    ],
                })
        
        return compiled
    
    def get_graph(self) -> KnowledgeGraph:
        """Get the knowledge graph."""
        return self.graph
    
    def clear_cache(self) -> None:
        """Clear the knowledge cache."""
        self.cache.clear()
    
    def _index_knowledge(self, knowledge: Knowledge) -> None:
        """Index knowledge for search."""
        # Index title words
        words = knowledge.metadata.title.lower().split()
        
        # Index description
        if knowledge.metadata.description:
            words.extend(knowledge.metadata.description.lower().split())
        
        # Index tags
        words.extend([t.lower() for t in knowledge.metadata.tags])
        
        # Index summary
        if knowledge.summary:
            words.extend(knowledge.summary.lower().split())
        
        # Add to index
        for word in words:
            if len(word) > 2:  # Skip short words
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(knowledge.id)
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Export all knowledge."""
        return {
            "exported_at": datetime.now().isoformat(),
            "count": len(self.knowledge_store),
            "knowledge": [
                {
                    "id": k.id,
                    "type": k.knowledge_type.value,
                    "title": k.metadata.title,
                    "content": k.content,
                    "status": k.status.value,
                }
                for k in self.knowledge_store.values()
            ],
        }
