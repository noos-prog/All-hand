"""
Engineering Nodes
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

First-class nodes for engineering concepts.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from agos_kernel.civilization.knowledge_graph.nodes.base import (
    GraphNode, NodeType, NodeMetadata, create_node
)


@dataclass
class RepositoryNode(GraphNode):
    """Repository node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.REPOSITORY, **kwargs)
        self.url: str = kwargs.get('url', '')
        self.default_branch: str = kwargs.get('default_branch', 'main')
        self.language: str = kwargs.get('language', '')
        self.stars: int = kwargs.get('stars', 0)
        self.forks: int = kwargs.get('forks', 0)
        self.open_issues: int = kwargs.get('open_issues', 0)
        self.contributors: int = kwargs.get('contributors', 0)
        self.size_bytes: int = kwargs.get('size_bytes', 0)
        self.file_count: int = kwargs.get('file_count', 0)
        self.languages: Dict[str, int] = kwargs.get('languages', {})


@dataclass
class WorkspaceNode(GraphNode):
    """Workspace node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.WORKSPACE, **kwargs)
        self.workspace_path: str = kwargs.get('workspace_path', '')
        self.repositories: List[str] = kwargs.get('repositories', [])


@dataclass
class OrganizationNode(GraphNode):
    """Organization node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.ORGANIZATION, **kwargs)
        self.org_name: str = kwargs.get('org_name', '')
        self.members: List[str] = kwargs.get('members', [])
        self.teams: List[str] = kwargs.get('teams', [])


@dataclass
class ProjectNode(GraphNode):
    """Project node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.PROJECT, **kwargs)
        self.project_type: str = kwargs.get('project_type', 'software')
        self.status: str = kwargs.get('status', 'active')


@dataclass
class ModuleNode(GraphNode):
    """Module node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.MODULE, **kwargs)
        self.module_name: str = kwargs.get('module_name', '')
        self.exports: List[str] = kwargs.get('exports', [])
        self.is_entry_point: bool = kwargs.get('is_entry_point', False)


@dataclass
class PackageNode(GraphNode):
    """Package node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.PACKAGE, **kwargs)
        self.package_name: str = kwargs.get('package_name', '')
        self.version: str = kwargs.get('version', '0.0.0')
        self.dependencies: List[str] = kwargs.get('dependencies', [])
        self.dev_dependencies: List[str] = kwargs.get('dev_dependencies', [])


@dataclass
class ServiceNode(GraphNode):
    """Service node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.SERVICE, **kwargs)
        self.service_name: str = kwargs.get('service_name', '')
        self.service_type: str = kwargs.get('service_type', 'microservice')
        self.port: int = kwargs.get('port', 0)
        self.endpoints: List[str] = kwargs.get('endpoints', [])


@dataclass
class ComponentNode(GraphNode):
    """Component node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.COMPONENT, **kwargs)
        self.component_type: str = kwargs.get('component_type', 'generic')
        self.dependencies: List[str] = kwargs.get('dependencies', [])


@dataclass
class DirectoryNode(GraphNode):
    """Directory node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.DIRECTORY, **kwargs)
        self.directory_path: str = kwargs.get('directory_path', '')
        self.children: List[str] = kwargs.get('children', [])
        self.depth: int = kwargs.get('depth', 0)


@dataclass
class FileNode(GraphNode):
    """File node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.FILE, **kwargs)
        self.file_path: str = kwargs.get('file_path', '')
        self.file_size: int = kwargs.get('file_size', 0)
        self.file_type: str = kwargs.get('file_type', '')
        self.executable: bool = kwargs.get('executable', False)
