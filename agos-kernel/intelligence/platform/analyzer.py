"""
AGOS Platform Analyzer
=====================

Analyzes deployment platforms and infrastructure configuration.
"""

import os
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class PlatformType(Enum):
    """Platform type."""
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    VERCEL = "vercel"
    HEROKU = "heroku"
    SERVERLESS = "serverless"
    ON_PREMISE = "on_premise"
    UNKNOWN = "unknown"


@dataclass
class DeploymentConfig:
    """Deployment configuration."""
    id: str
    platform: PlatformType
    config: Dict[str, Any] = field(default_factory=dict)
    env_vars: Dict[str, str] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PlatformAnalyzer:
    """
    Platform Analyzer.
    
    Analyzes deployment configuration to understand:
    - Infrastructure platform
    - Container setup
    - Cloud services
    - Resource requirements
    
    Usage:
        analyzer = PlatformAnalyzer()
        result = analyzer.analyze("/path/to/project")
        print(f"Platform: {result['platform']}")
    """
    
    def __init__(self):
        """Initialize platform analyzer."""
        self._configs: Dict[str, DeploymentConfig] = {}
    
    def analyze(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze platform configuration.
        
        Args:
            project_path: Path to project root
            
        Returns:
            Analysis result dictionary
        """
        path = Path(project_path)
        if not path.exists():
            return {"error": "Project not found"}
        
        # Detect platform
        platform = self._detect_platform(path)
        
        # Analyze configuration
        config = self._analyze_config(path, platform)
        
        # Extract resources
        resources = self._extract_resources(path, platform)
        
        return {
            "id": f"platform-{uuid.uuid4().hex[:8]}",
            "path": str(path),
            "timestamp": datetime.now().isoformat(),
            "platform": platform.value,
            "config": config,
            "resources": resources,
        }
    
    def _detect_platform(self, path: Path) -> PlatformType:
        """Detect deployment platform."""
        # Check for Kubernetes
        yaml_files = list(path.rglob("*.yaml")) + list(path.rglob("*.yml"))
        if yaml_files:
            for yml_file in yaml_files[:10]:
                try:
                    with open(yml_file, 'r') as f:
                        content = f.read(500)  # Just check first 500 chars
                        if 'apiVersion' in content:
                            return PlatformType.KUBERNETES
                except:
                    pass
        
        # Check for Docker
        if (path / "Dockerfile").exists() or (path / "docker-compose.yml").exists():
            return PlatformType.DOCKER
        
        # Check for serverless
        if (path / "serverless.yml").exists():
            return PlatformType.SERVERLESS
        
        # Check for cloud platforms
        if (path / ".vercel").exists():
            return PlatformType.VERCEL
        
        return PlatformType.UNKNOWN
    
    def _analyze_config(self, path: Path, platform: PlatformType) -> Dict[str, Any]:
        """Analyze platform-specific configuration."""
        config = {"files": [], "settings": {}}
        
        if platform == PlatformType.DOCKER:
            if (path / "Dockerfile").exists():
                config["files"].append("Dockerfile")
                config["settings"]["dockerfile"] = True
            
            if (path / "docker-compose.yml").exists():
                config["files"].append("docker-compose.yml")
                config["settings"]["compose"] = True
        
        elif platform == PlatformType.KUBERNETES:
            k8s_files = list(path.rglob("*.yaml")) + list(path.rglob("*.yml"))
            config["files"] = [str(f.relative_to(path)) for f in k8s_files]
            config["settings"]["manifests"] = len(k8s_files)
        
        return config
    
    def _extract_resources(self, path: Path, platform: PlatformType) -> Dict[str, Any]:
        """Extract resource requirements."""
        resources = {
            "cpu": "unknown",
            "memory": "unknown",
            "storage": "unknown",
            "network": "unknown",
        }
        
        # Try to extract from docker-compose
        if (path / "docker-compose.yml").exists():
            try:
                with open(path / "docker-compose.yml", 'r') as f:
                    compose = yaml.safe_load(f)
                    if compose and 'services' in compose:
                        for service, details in compose['services'].items():
                            if 'deploy' in details:
                                deploy = details['deploy']
                                if 'resources' in deploy:
                                    resources.update(deploy['resources'])
            except:
                pass
        
        return resources


# Global analyzer instance
_platform_analyzer: Optional[PlatformAnalyzer] = None


def get_platform_analyzer() -> PlatformAnalyzer:
    """Get the global platform analyzer."""
    global _platform_analyzer
    if _platform_analyzer is None:
        _platform_analyzer = PlatformAnalyzer()
    return _platform_analyzer
