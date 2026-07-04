"""
Universal Audit Runtime
PHASE-02: EXECUTION-000019 - Universal Audit Runtime
Complete engineering accountability.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class AuditEntry:
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    action: str = ""
    actor: str = ""
    target: str = ""
    target_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'entry_id': self.entry_id,
            'action': self.action,
            'actor': self.actor,
            'target': self.target,
            'target_type': self.target_type,
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'evidence': self.evidence,
        }


class AuditRegistry:
    def __init__(self):
        self.entries: Dict[str, AuditEntry] = {}
        self.by_actor: Dict[str, List[str]] = {}
        self.by_target: Dict[str, List[str]] = {}
    
    def register(self, entry: AuditEntry) -> None:
        self.entries[entry.entry_id] = entry
        
        if entry.actor not in self.by_actor:
            self.by_actor[entry.actor] = []
        self.by_actor[entry.actor].append(entry.entry_id)
        
        if entry.target not in self.by_target:
            self.by_target[entry.target] = []
        self.by_target[entry.target].append(entry.entry_id)
    
    def get(self, entry_id: str) -> Optional[AuditEntry]:
        return self.entries.get(entry_id)
    
    def get_by_actor(self, actor: str) -> List[AuditEntry]:
        ids = self.by_actor.get(actor, [])
        return [self.entries[e] for e in ids if e in self.entries]
    
    def get_by_target(self, target: str) -> List[AuditEntry]:
        ids = self.by_target.get(target, [])
        return [self.entries[e] for e in ids if e in self.entries]


class AuditSearch:
    def search(self, registry: AuditRegistry, query: Dict) -> List[AuditEntry]:
        results = list(registry.entries.values())
        
        if 'actor' in query:
            results = [e for e in results if e.actor == query['actor']]
        
        if 'target' in query:
            results = [e for e in results if e.target == query['target']]
        
        if 'action' in query:
            results = [e for e in results if e.action == query['action']]
        
        return results


class AuditRuntime:
    VERSION = "1.1"
    
    def __init__(self):
        self.registry = AuditRegistry()
        self.search = AuditSearch()
    
    def log(self, action: str, actor: str, target: str, target_type: str, metadata: Dict = None, evidence: List[str] = None) -> AuditEntry:
        entry = AuditEntry(
            action=action,
            actor=actor,
            target=target,
            target_type=target_type,
            metadata=metadata or {},
            evidence=evidence or []
        )
        self.registry.register(entry)
        return entry
    
    def reconstruct(self, target: str) -> List[AuditEntry]:
        return self.registry.get_by_target(target)
    
    def generate_report(self) -> Dict:
        return {
            'total_entries': len(self.registry.entries),
            'actors': list(self.registry.by_actor.keys()),
            'targets': list(self.registry.by_target.keys())
        }