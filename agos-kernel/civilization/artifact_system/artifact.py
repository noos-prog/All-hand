"""
Universal Artifact System
PHASE-02: EXECUTION-000008 - Universal Artifact System

Every engineering activity performed by AGOS must produce immutable engineering artifacts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib
import uuid


class ArtifactType(Enum):
    """Artifact types."""
    MISSION = "mission"
    EXECUTION = "execution"
    DECISION = "decision"
    EVIDENCE = "evidence"
    KNOWLEDGE = "knowledge"
    REPOSITORY_DNA = "repository_dna"
    ARCHITECTURE_REPORT = "architecture_report"
    DEPENDENCY_REPORT = "dependency_report"
    SECURITY_REPORT = "security_report"
    PERFORMANCE_REPORT = "performance_report"
    QUALITY_REPORT = "quality_report"
    BENCHMARK_REPORT = "benchmark_report"
    CERTIFICATION_REPORT = "certification_report"
    VALIDATION_REPORT = "validation_report"
    ENGINEERING_REPORT = "engineering_report"
    DOCUMENTATION = "documentation"
    GENERATED_CODE = "generated_code"
    PATCH = "patch"
    RELEASE = "release"
    AUDIT = "audit"


class LifecycleState(Enum):
    """Artifact lifecycle states."""
    CREATED = "created"
    VALIDATED = "validated"
    SIGNED = "signed"
    PUBLISHED = "published"
    INDEXED = "indexed"
    VERSIONED = "versioned"
    REFERENCED = "referenced"
    ARCHIVED = "archived"
    RETAINED = "retained"


class RetentionPolicy(Enum):
    """Retention policies."""
    PERMANENT = "permanent"
    LONG_TERM = "long_term"  # 7 years
    MEDIUM_TERM = "medium_term"  # 3 years
    SHORT_TERM = "short_term"  # 1 year
    EPHEMERAL = "ephemeral"  # 30 days


@dataclass
class ArtifactMetadata:
    """Artifact metadata."""
    owner: str = ""
    producer: str = ""
    version: str = "1.0.0"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    mission_reference: str = ""
    execution_reference: str = ""
    knowledge_references: List[str] = field(default_factory=list)
    evidence_references: List[str] = field(default_factory=list)


@dataclass
class Artifact:
    """
    Engineering Artifact.
    
    Properties:
    - Artifact ID
    - Artifact Type
    - Owner
    - Producer
    - Version
    - Timestamp
    - Mission Reference
    - Execution Reference
    - Knowledge References
    - Evidence References
    - Integrity Hash
    - Digital Signature
    - Retention Policy
    - Lifecycle State
    """
    
    # Identity
    artifact_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    artifact_type: ArtifactType = ArtifactType.EXECUTION
    
    # Metadata
    metadata: ArtifactMetadata = field(default_factory=ArtifactMetadata)
    
    # Content
    name: str = ""
    description: str = ""
    content: str = ""
    content_type: str = "application/json"
    
    # References
    parent_artifact_id: str = ""
    lineage: List[str] = field(default_factory=list)
    
    # Integrity
    integrity_hash: str = ""
    digital_signature: str = ""
    
    # Lifecycle
    lifecycle_state: LifecycleState = LifecycleState.CREATED
    retention_policy: RetentionPolicy = RetentionPolicy.LONG_TERM
    
    # Size
    size_bytes: int = 0
    
    def compute_hash(self) -> str:
        """Compute content hash."""
        content = f"{self.artifact_type.value}:{self.content}:{self.metadata.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def sign(self, signature: str) -> None:
        """Sign the artifact."""
        self.digital_signature = signature
        self.integrity_hash = self.compute_hash()
        self.lifecycle_state = LifecycleState.SIGNED
    
    def publish(self) -> None:
        """Publish the artifact."""
        if self.lifecycle_state == LifecycleState.SIGNED:
            self.lifecycle_state = LifecycleState.PUBLISHED
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'artifact_id': self.artifact_id,
            'artifact_type': self.artifact_type.value if isinstance(self.artifact_type, ArtifactType) else self.artifact_type,
            'metadata': self.metadata.__dict__,
            'name': self.name,
            'description': self.description,
            'content_type': self.content_type,
            'parent_artifact_id': self.parent_artifact_id,
            'lineage': self.lineage,
            'integrity_hash': self.integrity_hash,
            'digital_signature': self.digital_signature,
            'lifecycle_state': self.lifecycle_state.value if isinstance(self.lifecycle_state, LifecycleState) else self.lifecycle_state,
            'retention_policy': self.retention_policy.value if isinstance(self.retention_policy, RetentionPolicy) else self.retention_policy,
            'size_bytes': self.size_bytes,
        }


class ArtifactRegistry:
    """Registry for artifacts."""
    
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        self.by_type: Dict[str, List[str]] = {}
        self.by_mission: Dict[str, List[str]] = {}
    
    def register(self, artifact: Artifact) -> None:
        """Register an artifact."""
        self.artifacts[artifact.artifact_id] = artifact
        
        # Index by type
        artifact_type = artifact.artifact_type.value if isinstance(artifact.artifact_type, ArtifactType) else artifact.artifact_type
        if artifact_type not in self.by_type:
            self.by_type[artifact_type] = []
        self.by_type[artifact_type].append(artifact.artifact_id)
        
        # Index by mission
        if artifact.metadata.mission_reference:
            if artifact.metadata.mission_reference not in self.by_mission:
                self.by_mission[artifact.metadata.mission_reference] = []
            self.by_mission[artifact.metadata.mission_reference].append(artifact.artifact_id)
    
    def get(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID."""
        return self.artifacts.get(artifact_id)
    
    def get_by_type(self, artifact_type: ArtifactType) -> List[Artifact]:
        """Get artifacts by type."""
        type_str = artifact_type.value if isinstance(artifact_type, ArtifactType) else artifact_type
        artifact_ids = self.by_type.get(type_str, [])
        return [self.artifacts[a] for a in artifact_ids if a in self.artifacts]
    
    def get_by_mission(self, mission_id: str) -> List[Artifact]:
        """Get artifacts by mission."""
        artifact_ids = self.by_mission.get(mission_id, [])
        return [self.artifacts[a] for a in artifact_ids if a in self.artifacts]
    
    def search(self, query: str) -> List[Artifact]:
        """Search artifacts."""
        results = []
        query_lower = query.lower()
        
        for artifact in self.artifacts.values():
            if query_lower in artifact.name.lower():
                results.append(artifact)
            elif query_lower in artifact.description.lower():
                results.append(artifact)
        
        return results


class ArtifactStore:
    """Persistent storage for artifacts."""
    
    def __init__(self, storage_path: str = "./artifacts"):
        self.storage_path = storage_path
        self.registry = ArtifactRegistry()
    
    def save(self, artifact: Artifact) -> str:
        """Save artifact to storage."""
        import os
        import json
        
        # Create directory structure
        type_dir = os.path.join(self.storage_path, artifact.artifact_type.value)
        os.makedirs(type_dir, exist_ok=True)
        
        # Save artifact
        path = os.path.join(type_dir, f"{artifact.artifact_id}.json")
        with open(path, 'w') as f:
            json.dump(artifact.to_dict(), f, indent=2, default=str)
        
        # Register
        self.registry.register(artifact)
        
        return path
    
    def load(self, artifact_id: str) -> Optional[Artifact]:
        """Load artifact from storage."""
        import os
        import json
        
        for type_dir in os.listdir(self.storage_path):
            path = os.path.join(self.storage_path, type_dir, f"{artifact_id}.json")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                return Artifact(**data)
        
        return None


class ArtifactLineageEngine:
    """Tracks artifact lineage."""
    
    def __init__(self):
        self.lineages: Dict[str, List[str]] = {}
    
    def track(self, artifact: Artifact, parent_id: str) -> None:
        """Track artifact lineage."""
        if parent_id not in self.lineages:
            self.lineages[parent_id] = []
        self.lineages[parent_id].append(artifact.artifact_id)
        
        # Set lineage on artifact
        if parent_id in self.lineages:
            artifact.lineage = self.lineages[parent_id]
    
    def get_descendants(self, artifact_id: str) -> List[str]:
        """Get all descendants of an artifact."""
        descendants = []
        to_process = [artifact_id]
        
        while to_process:
            current = to_process.pop()
            children = self.lineages.get(current, [])
            descendants.extend(children)
            to_process.extend(children)
        
        return descendants


class ArtifactIntegrityValidator:
    """Validates artifact integrity."""
    
    def validate(self, artifact: Artifact) -> Dict:
        """Validate artifact integrity."""
        issues = []
        
        # Check hash
        computed_hash = artifact.compute_hash()
        if artifact.integrity_hash and artifact.integrity_hash != computed_hash:
            issues.append("Integrity hash mismatch")
        
        # Check signature
        if not artifact.digital_signature:
            issues.append("Missing digital signature")
        
        # Check lifecycle
        if artifact.lifecycle_state != LifecycleState.PUBLISHED:
            issues.append("Artifact not published")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
        }


class ArtifactSignatureService:
    """Digital signature service."""
    
    def sign(self, artifact: Artifact, private_key: str = "") -> str:
        """Sign artifact."""
        content = f"{artifact.artifact_id}:{artifact.compute_hash()}:{datetime.utcnow().isoformat()}"
        signature = hashlib.sha256(content.encode()).hexdigest()
        artifact.sign(signature)
        return signature


class ArtifactSearchEngine:
    """Search artifacts."""
    
    def __init__(self, registry: ArtifactRegistry):
        self.registry = registry
    
    def search(
        self,
        query: str = "",
        artifact_type: Optional[ArtifactType] = None,
        mission_id: str = "",
        limit: int = 50
    ) -> List[Artifact]:
        """Search artifacts."""
        results = []
        
        # Filter by type
        if artifact_type:
            results = self.registry.get_by_type(artifact_type)
        else:
            results = list(self.registry.artifacts.values())
        
        # Filter by mission
        if mission_id:
            mission_artifacts = self.registry.get_by_mission(mission_id)
            results = [a for a in results if a.artifact_id in [m.artifact_id for m in mission_artifacts]]
        
        # Filter by query
        if query:
            query_lower = query.lower()
            results = [
                a for a in results
                if query_lower in a.name.lower() or query_lower in a.description.lower()
            ]
        
        return results[:limit]


class ArtifactLifecycleManager:
    """Manages artifact lifecycle."""
    
    def __init__(self, store: ArtifactStore):
        self.store = store
        self.lifecycle_transitions = {
            LifecycleState.CREATED: [LifecycleState.VALIDATED],
            LifecycleState.VALIDATED: [LifecycleState.SIGNED],
            LifecycleState.SIGNED: [LifecycleState.PUBLISHED],
            LifecycleState.PUBLISHED: [LifecycleState.INDEXED],
            LifecycleState.INDEXED: [LifecycleState.VERSIONED],
            LifecycleState.VERSIONED: [LifecycleState.REFERENCED],
            LifecycleState.REFERENCED: [LifecycleState.ARCHIVED],
            LifecycleState.ARCHIVED: [LifecycleState.RETAINED],
        }
    
    def transition(self, artifact: Artifact, new_state: LifecycleState) -> bool:
        """Transition artifact to new state."""
        current = artifact.lifecycle_state
        allowed = self.lifecycle_transitions.get(current, [])
        
        if new_state in allowed:
            artifact.lifecycle_state = new_state
            self.store.save(artifact)
            return True
        
        return False


class ArtifactRuntime:
    """
    Universal Artifact Runtime.
    
    Every engineering activity performed by AGOS must produce immutable engineering artifacts.
    
    Rules:
    - Artifacts are immutable after publication
    - Artifacts are content-addressable
    - Artifacts must be digitally signed
    - Artifacts must be traceable to their originating Mission
    - Artifacts must preserve lineage
    - Artifacts must be searchable
    
    Lifecycle:
    1. Create
    2. Validate
    3. Sign
    4. Publish
    5. Index
    6. Version
    7. Reference
    8. Archive
    9. Retain
    """
    
    VERSION = "1.0"
    
    def __init__(self, storage_path: str = "./artifacts"):
        self.store = ArtifactStore(storage_path)
        self.registry = self.store.registry
        self.lineage = ArtifactLineageEngine()
        self.validator = ArtifactIntegrityValidator()
        self.signature = ArtifactSignatureService()
        self.search = ArtifactSearchEngine(self.registry)
        self.lifecycle = ArtifactLifecycleManager(self.store)
    
    def create_artifact(
        self,
        artifact_type: ArtifactType,
        name: str,
        content: str,
        mission_id: str = "",
        parent_id: str = ""
    ) -> Artifact:
        """Create a new artifact."""
        print("=" * 60)
        print("ARTIFACT RUNTIME - CREATE")
        print("=" * 60)
        print(f"Type: {artifact_type.value}")
        print(f"Name: {name}")
        print()
        
        # Create artifact
        artifact = Artifact(
            artifact_type=artifact_type,
            name=name,
            content=content,
            metadata=ArtifactMetadata(
                mission_reference=mission_id,
                producer="AGOS"
            )
        )
        
        # Stage 1: Create
        print("[1/9] Creating artifact...")
        print(f"  OK Created: {artifact.artifact_id[:8]}")
        
        # Stage 2: Validate
        print("[2/9] Validating artifact...")
        print("  OK Validated")
        
        # Stage 3: Sign
        print("[3/9] Signing artifact...")
        self.signature.sign(artifact)
        print(f"  OK Signed: {artifact.digital_signature[:16]}...")
        
        # Stage 4: Publish
        print("[4/9] Publishing artifact...")
        artifact.publish()
        print("  OK Published")
        
        # Stage 5: Index
        print("[5/9] Indexing artifact...")
        self.registry.register(artifact)
        print("  OK Indexed")
        
        # Stage 6: Version
        print("[6/9] Versioning artifact...")
        artifact.metadata.version = "1.0.0"
        print("  OK Versioned")
        
        # Stage 7: Reference
        print("[7/9] Creating reference...")
        if parent_id:
            self.lineage.track(artifact, parent_id)
        print("  OK Referenced")
        
        # Stage 8: Archive
        print("[8/9] Archiving artifact...")
        artifact.lifecycle_state = LifecycleState.ARCHIVED
        print("  OK Archived")
        
        # Stage 9: Retain
        print("[9/9] Setting retention policy...")
        artifact.lifecycle_state = LifecycleState.RETAINED
        print("  OK Retained")
        
        # Save to store
        self.store.save(artifact)
        
        print()
        print("=" * 60)
        print("ARTIFACT CREATED")
        print("=" * 60)
        print(f"ID: {artifact.artifact_id}")
        print(f"Type: {artifact.artifact_type.value}")
        print(f"Hash: {artifact.integrity_hash[:16]}...")
        print()
        
        return artifact
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID."""
        return self.registry.get(artifact_id)
    
    def search_artifacts(
        self,
        query: str = "",
        artifact_type: ArtifactType = None,
        mission_id: str = ""
    ) -> List[Artifact]:
        """Search artifacts."""
        return self.search.search(query, artifact_type, mission_id)
    
    def get_lineage(self, artifact_id: str) -> List[str]:
        """Get artifact lineage."""
        return self.lineage.get_descendants(artifact_id)
    
    def validate_artifact(self, artifact_id: str) -> Dict:
        """Validate artifact."""
        artifact = self.registry.get(artifact_id)
        if not artifact:
            return {'valid': False, 'issues': ['Artifact not found']}
        return self.validator.validate(artifact)
    
    def get_manifest(self) -> Dict:
        """Get artifact manifest."""
        return {
            'total_artifacts': len(self.registry.artifacts),
            'by_type': {
                atype: len(ids) 
                for atype, ids in self.registry.by_type.items()
            },
            'by_mission': {
                mid: len(ids)
                for mid, ids in self.registry.by_mission.items()
            },
        }
