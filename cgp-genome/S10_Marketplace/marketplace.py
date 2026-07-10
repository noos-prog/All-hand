#!/usr/bin/env python3
"""
CGP - Capability Marketplace
===========================

Publish and discover capabilities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class ListingType(Enum):
    """Listing types."""
    OFFICIAL = "official"    # AGOS official
    COMMUNITY = "community"  # Community contributed
    ENTERPRISE = "enterprise" # Enterprise


class QualityLevel(Enum):
    """Quality levels."""
    CERTIFIED = "certified"
    VERIFIED = "verified"
    COMMUNITY = "community"


class PricingModel(Enum):
    """Pricing models."""
    FREE = "free"
    USAGE_BASED = "usage_based"
    SUBSCRIPTION = "subscription"


@dataclass
class CapabilityListing:
    """A capability listing in the marketplace."""
    listing_id: str
    capability_id: str
    name: str
    version: str
    
    # Type
    listing_type: ListingType
    quality_level: QualityLevel
    
    # Provider
    provider_name: str
    provider_id: str
    
    # Description
    description: str = ""
    documentation_url: str = ""
    
    # Pricing
    pricing_model: PricingModel = PricingModel.FREE
    price: float = 0.0
    
    # Stats
    download_count: int = 0
    rating: float = 0.0
    review_count: int = 0
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    # Compatibility
    compatible_with: Tuple[str, ...] = ()


@dataclass
class MarketplaceSearch:
    """Search result for marketplace."""
    query: str
    results: Tuple[CapabilityListing, ...]
    total_count: int
    page: int = 1
    per_page: int = 20


class Marketplace:
    """
    Capability marketplace.
    """
    
    def __init__(self):
        self._listings: Dict[str, CapabilityListing] = {}
        self._by_type: Dict[ListingType, List[str]] = {}
        self._by_quality: Dict[QualityLevel, List[str]] = {}
        self._by_category: Dict[str, List[str]] = {}
    
    def publish(self, listing: CapabilityListing) -> str:
        """Publish a capability listing."""
        self._listings[listing.listing_id] = listing
        
        # Index by type
        if listing.listing_type not in self._by_type:
            self._by_type[listing.listing_type] = []
        self._by_type[listing.listing_type].append(listing.listing_id)
        
        # Index by quality
        if listing.quality_level not in self._by_quality:
            self._by_quality[listing.quality_level] = []
        self._by_quality[listing.quality_level].append(listing.listing_id)
        
        # Index by tags
        for tag in listing.tags:
            if tag not in self._by_category:
                self._by_category[tag] = []
            self._by_category[tag].append(listing.listing_id)
        
        return listing.listing_id
    
    def get(self, listing_id: str) -> Optional[CapabilityListing]:
        """Get a listing by ID."""
        return self._listings.get(listing_id)
    
    def search(
        self,
        query: str = "",
        listing_type: Optional[ListingType] = None,
        quality_level: Optional[QualityLevel] = None,
        pricing_model: Optional[PricingModel] = None,
        tags: List[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> MarketplaceSearch:
        """Search listings."""
        results = list(self._listings.values())
        
        # Filter by query
        if query:
            query_lower = query.lower()
            results = [
                r for r in results
                if query_lower in r.name.lower() or query_lower in r.description.lower()
            ]
        
        # Filter by type
        if listing_type:
            results = [r for r in results if r.listing_type == listing_type]
        
        # Filter by quality
        if quality_level:
            results = [r for r in results if r.quality_level == quality_level]
        
        # Filter by pricing
        if pricing_model:
            results = [r for r in results if r.pricing_model == pricing_model]
        
        # Filter by tags
        if tags:
            results = [
                r for r in results
                if any(tag in r.tags for tag in tags)
            ]
        
        # Sort by rating
        results.sort(key=lambda r: r.rating, reverse=True)
        
        total = len(results)
        paginated = results[offset:offset + limit]
        
        return MarketplaceSearch(
            query=query,
            results=tuple(paginated),
            total_count=total,
            page=offset // limit + 1,
            per_page=limit,
        )
    
    def get_featured(self, limit: int = 10) -> List[CapabilityListing]:
        """Get featured listings."""
        featured = [
            l for l in self._listings.values()
            if l.quality_level == QualityLevel.CERTIFIED
        ]
        featured.sort(key=lambda l: l.rating, reverse=True)
        return featured[:limit]
    
    def get_by_provider(self, provider_id: str) -> List[CapabilityListing]:
        """Get all listings by a provider."""
        return [
            l for l in self._listings.values()
            if l.provider_id == provider_id
        ]
    
    def record_download(self, listing_id: str) -> bool:
        """Record a download."""
        listing = self._listings.get(listing_id)
        if listing:
            listing.download_count += 1
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get marketplace statistics."""
        return {
            "total_listings": len(self._listings),
            "by_type": {t.value: len(ids) for t, ids in self._by_type.items()},
            "by_quality": {q.value: len(ids) for q, ids in self._by_quality.items()},
            "total_downloads": sum(l.download_count for l in self._listings.values()),
        }
