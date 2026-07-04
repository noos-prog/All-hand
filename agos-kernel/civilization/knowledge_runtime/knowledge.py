"""
Universal Knowledge Runtime
PHASE-02: EXECUTION-000014 - Universal Knowledge Runtime
Knowledge becomes a first-class production asset.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class KnowledgeType(Enum):
    FACT = "fact"
    RULE = "rule"
    PATTERN = "pattern"
    RELATIONSHIP = "relationship"
    METADATA = "metadata"


@dataclass
class KnowledgeObject:
    ko_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    knowledge_type: KnowledgeType = KnowledgeType.FACT
    content: str = ""
    source: str = ""
    confidence: float = 1.0
    version: str = "1.0.0"
    relationships: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'ko_id': self.ko_id,
            'knowledge_type': self.knowledge_type.value if isinstance(self.knowledge_type, KnowledgeType) else self.knowledge_type,
            'content': self.content,
            'source': self.source,
            'confidence': self.confidence,
            'version': self.version,
            'relationships': self.relationships,
            'metadata': self.metadata,
        }


class KnowledgeRegistry:
    def __init__(self):
        self.knowledge: Dict[str, KnowledgeObject] = {}
        self.by_type: Dict[str, List[str]] = {}
    
    def register(self, ko: KnowledgeObject) -> None:
        self.knowledge[ko.ko_id] = ko
        ktype = ko.knowledge_type.value if isinstance(ko.knowledge_type, KnowledgeType) else ko.knowledge_type
        if ktype not in self.by_type:
            self.by_type[ktype] = []
        self.by_type[ktype].append(ko.ko_id)
    
    def get(self, ko_id: str) -> Optional[KnowledgeObject]:
        return self.knowledge.get(ko_id)
    
    def search(self, query: str) -> List[KnowledgeObject]:
        return [k for k in self.knowledge.values() if query.lower() in k.content.lower()]


class KnowledgeRuntime:
    VERSION = "1.0"
    
    def __init__(self):
        self.registry = KnowledgeRegistry()
    
    def create_knowledge(self, ktype: KnowledgeType, content: str, source: str = "") -> KnowledgeObject:
        ko = KnowledgeObject(knowledge_type=ktype, content=content, source=source)
        self.registry.register(ko)
        return ko
    
    def relate(self, ko_id1: str, ko_id2: str) -> None:
        ko1 = self.registry.get(ko_id1)
        ko2 = self.registry.get(ko_id2)
        if ko1 and ko2:
            ko1.relationships.append(ko_id2)
            ko2.relationships.append(ko_id1)
    
    def get_knowledge_report(self) -> Dict:
        return {
            'total_knowledge': len(self.registry.knowledge),
            'by_type': {t: len(ids) for t, ids in self.registry.by_type.items()}
        }