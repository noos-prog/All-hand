"""
Universal Artifact System
PHASE-02: EXECUTION-000008 - Universal Artifact System

Every engineering activity performed by AGOS must produce immutable engineering artifacts.
"""

__version__ = "1.0"

from agos_kernel.civilization.artifact_system.artifact import (
    Artifact,
    ArtifactType,
    ArtifactMetadata,
    LifecycleState,
    RetentionPolicy,
    ArtifactRegistry,
    ArtifactStore,
    ArtifactLineageEngine,
    ArtifactIntegrityValidator,
    ArtifactSignatureService,
    ArtifactSearchEngine,
    ArtifactLifecycleManager,
    ArtifactRuntime,
)

__all__ = [
    'Artifact',
    'ArtifactType',
    'ArtifactMetadata',
    'LifecycleState',
    'RetentionPolicy',
    'ArtifactRegistry',
    'ArtifactStore',
    'ArtifactLineageEngine',
    'ArtifactIntegrityValidator',
    'ArtifactSignatureService',
    'ArtifactSearchEngine',
    'ArtifactLifecycleManager',
    'ArtifactRuntime',
]
