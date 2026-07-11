"""AGOS Products - Universal Product Layer for AI Agent Civilization."""
from .projects import Project, ProjectType, ProjectPlatform, ProjectManager
from .missions import Mission, MissionType, MissionPlatform, MissionExecutor
from .artifacts import Artifact, ArtifactType, ArtifactPlatform, ArtifactRegistry
from .api import APIPlatform, RESTEndpoint, GraphQLSchema, GRPCService

__all__ = [
    "Project", "ProjectType", "ProjectPlatform", "ProjectManager",
    "Mission", "MissionType", "MissionPlatform", "MissionExecutor",
    "Artifact", "ArtifactType", "ArtifactPlatform", "ArtifactRegistry",
    "APIPlatform", "RESTEndpoint", "GraphQLSchema", "GRPCService",
]

__version__ = "1.0.0"
