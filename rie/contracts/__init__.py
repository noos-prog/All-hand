"""RIE Contracts - Domain contracts for Repository Intelligence Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


@dataclass
class RepositoryDNA:
    """Repository DNA - the identity of a repository."""
    id: str = ""
    name: str = ""
    url: str = ""
    owner: str = ""
    branch: str = "main"
    commit: str = ""
    
    # Languages
    primary_language: str = ""
    languages: List[str] = field(default_factory=list)
    
    # Frameworks
    frameworks: List[str] = field(default_factory=list)
    
    # Dependencies
    package_managers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # Configuration
    config_files: List[str] = field(default_factory=list)
    
    # Structure
    entry_points: List[str] = field(default_factory=list)
    directory_tree: List[str] = field(default_factory=list)
    
    # Documentation
    readme_summary: str = ""
    license: str = ""
    has_documentation: bool = False
    
    # Statistics
    total_files: int = 0
    total_directories: int = 0
    total_size_bytes: int = 0
    
    # Metadata
    generated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "owner": self.owner,
            "branch": self.branch,
            "commit": self.commit,
            "primary_language": self.primary_language,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "package_managers": self.package_managers,
            "dependencies": self.dependencies,
            "config_files": self.config_files,
            "entry_points": self.entry_points,
            "directory_tree": self.directory_tree,
            "readme_summary": self.readme_summary,
            "license": self.license,
            "has_documentation": self.has_documentation,
            "total_files": self.total_files,
            "total_directories": self.total_directories,
            "total_size_bytes": self.total_size_bytes,
            "generated_at": self.generated_at.isoformat(),
            "version": self.version
        }


@dataclass
class UniversalRepositoryObject:
    """Universal repository model - all repos converted to same structure."""
    url: str = ""
    name: str = ""
    owner: str = ""
    branch: str = "main"
    commit: str = ""
    
    # Files and directories
    files: Dict[str, Any] = field(default_factory=dict)  # path -> content
    directories: List[str] = field(default_factory=list)
    
    # Raw metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    cloned_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "name": self.name,
            "owner": self.owner,
            "branch": self.branch,
            "commit": self.commit,
            "directories": self.directories,
            "file_count": len(self.files),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "cloned_at": self.cloned_at.isoformat()
        }


@dataclass
class DetectorResult:
    """Result from a detector."""
    detector_name: str
    features: Dict[str, Any]
    errors: List[str] = field(default_factory=list)
    duration_ms: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


@dataclass
class RepositoryFeatureSet:
    """Aggregated features from all detectors."""
    repository_url: str
    
    # Language features
    languages: Dict[str, float] = field(default_factory=dict)  # lang -> percentage
    
    # Framework features
    frameworks: List[str] = field(default_factory=list)
    
    # Dependency features
    dependencies: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    
    # Configuration features
    config_files: List[str] = field(default_factory=list)
    configurations: Dict[str, Any] = field(default_factory=dict)
    
    # Structure features
    entry_points: List[str] = field(default_factory=list)
    directory_tree: List[str] = field(default_factory=list)
    
    # Documentation features
    has_readme: bool = False
    has_license: bool = False
    has_changelog: bool = False
    readme_summary: str = ""
    license_type: str = ""
    
    # Architecture hints
    architecture_type: str = ""
    project_type: str = ""
    
    # Statistics
    total_files: int = 0
    total_directories: int = 0
    total_size_bytes: int = 0
    
    # Validation
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository_url": self.repository_url,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "dependencies": self.dependencies,
            "package_managers": self.package_managers,
            "config_files": self.config_files,
            "entry_points": self.entry_points,
            "directory_tree": self.directory_tree,
            "has_readme": self.has_readme,
            "has_license": self.has_license,
            "has_changelog": self.has_changelog,
            "readme_summary": self.readme_summary,
            "license_type": self.license_type,
            "architecture_type": self.architecture_type,
            "project_type": self.project_type,
            "total_files": self.total_files,
            "total_directories": self.total_directories,
            "total_size_bytes": self.total_size_bytes,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors
        }
