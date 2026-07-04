"""AGOS Marketplace Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MarketplaceAssetMetadata:
    """Marketplace asset metadata."""
    id: str
    name: str
    category: str
    version: str = "1.0.0"
    publisher: str = ""
    trust_score: float = 0.0
    certifications: List[str] = field(default_factory=list)


class MarketplaceAsset:
    """A marketplace asset."""
    
    def __init__(self, name: str, category: str, publisher: str = ""):
        self.metadata = MarketplaceAssetMetadata(
            id=f"asset-{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            publisher=publisher,
        )
        self.compatibility_matrix: Dict[str, List[str]] = {}
        self.dependencies: List[str] = []
        self.reviews: List[Dict] = []


# Marketplace Categories
MARKETPLACE_CATEGORIES = [
    "capability", "provider", "skill", "adapter", "workflow",
    "knowledge", "template", "policy", "benchmark", "certification",
    "language_pack", "framework_pack", "cloud_pack",
    "agent_pack", "model_pack", "tool_pack",
    "domain", "civilization_pack", "extension",
    "organization", "workspace", "repository",
    "architecture", "playbook", "runbook",
    "training", "sdk", "connector",
    "integration", "automation", "security",
    "testing", "infrastructure", "ai",
    "data", "enterprise", "community",
    "partner", "commercial", "private"
]


class Marketplace:
    """AGOS Marketplace."""
    
    def __init__(self):
        self.assets: Dict[str, MarketplaceAsset] = {}
        self.categories = MARKETPLACE_CATEGORIES
    
    def publish(self, asset: MarketplaceAsset) -> str:
        """Publish an asset."""
        self.assets[asset.metadata.id] = asset
        return asset.metadata.id
    
    def discover(self, category: str = None) -> List[MarketplaceAsset]:
        """Discover assets."""
        if category:
            return [a for a in self.assets.values() if a.metadata.category == category]
        return list(self.assets.values())
    
    def get(self, asset_id: str) -> MarketplaceAsset:
        """Get an asset."""
        return self.assets.get(asset_id)


# Global marketplace
_marketplace = Marketplace()


def get_marketplace() -> Marketplace:
    return _marketplace