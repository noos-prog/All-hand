"""
CAPABILITY-000019: Repository DNA Generation

PURPOSE: Generate comprehensive repository DNA combining all analysis results.

VERSION: 1.0.0
"""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class RepositoryDNA:
    """Complete repository DNA."""
    id: str = ""
    name: str = ""
    url: str = ""
    owner: str = ""
    primary_language: str = ""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    directory_tree: List[str] = field(default_factory=list)
    readme_summary: str = ""
    license: str = ""
    fingerprint: str = ""
    health_score: float = 0.0
    generated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "owner": self.owner,
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
            "fingerprint": self.fingerprint,
            "health_score": self.health_score,
            "generated_at": self.generated_at.isoformat(),
        }

class RepositoryDNACapability:
    """
    CAPABILITY-000019: Repository DNA Generation
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000019"
    
    @property
    def name(self) -> str:
        return "RepositoryDNA"
    
    @property
    def description(self) -> str:
        return "Generates comprehensive repository DNA"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> RepositoryDNA:
        """Execute DNA generation."""
        from .capability_001_discovery import RepositoryDiscoveryCapability
        from .capability_004_fingerprint import RepositoryFingerprintCapability
        from .capability_006_technology import TechnologyDetectionCapability
        
        source = input_data.get("source", "")
        path = input_data.get("path", "")
        
        # Discovery
        discovery = RepositoryDiscoveryCapability()
        if source:
            desc = discovery.execute({"source": source})
        else:
            desc = discovery.execute({"source": path})
        
        # Technology detection
        target_path = path or desc.path
        if not target_path or not os.path.isdir(target_path):
            return RepositoryDNA(name=desc.name, url=desc.url, owner=desc.owner)
        
        tech = TechnologyDetectionCapability()
        profile = tech.execute({"path": target_path})
        
        # Find README
        readme_summary = ""
        for root, dirs, files in os.walk(target_path):
            for f in files:
                if "readme" in f.lower():
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                            readme_summary = fp.read()[:500]
                    except:
                        pass
                    break
        
        # Find LICENSE
        license_name = ""
        for root, dirs, files in os.walk(target_path):
            for f in files:
                if "license" in f.lower():
                    license_name = f
                    break
        
        return RepositoryDNA(
            id=desc.name,
            name=desc.name,
            url=desc.url,
            owner=desc.owner,
            primary_language=profile.languages[0] if profile.languages else "",
            languages=profile.languages,
            frameworks=profile.frameworks,
            package_managers=profile.package_managers,
            config_files=[p for p in profile.build_systems],
            license=license_name,
            readme_summary=readme_summary,
            generated_at=datetime.utcnow(),
        )
