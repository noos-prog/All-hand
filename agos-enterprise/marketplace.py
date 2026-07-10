#!/usr/bin/env python3
"""
AGOS Enterprise - Marketplace Module
=====================================

Provider Marketplace - where certified providers are listed.
Providers must go through certification before appearing here.

Provider Lifecycle:
1. Certification
2. Benchmark
3. Security Scan
4. Capability Mapping
5. Publication
6. Available in Marketplace
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json


class ListingStatus(Enum):
    """Status of a marketplace listing."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    DEPRECATED = "deprecated"


class ReviewDecision(Enum):
    """Decision on a marketplace listing."""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"


@dataclass(frozen=True)
class CertificationResult:
    """Result of provider certification."""
    certified: bool
    certification_id: str
    certified_at: datetime
    valid_until: datetime
    tier: str
    authority: str
    notes: str = ""


@dataclass(frozen=True)
class BenchmarkResult:
    """Result of provider benchmarking."""
    benchmark_id: str
    provider_id: str
    capability_id: str
    benchmarked_at: datetime
    score: float  # 0-100
    latency_ms: int
    throughput: float  # requests per second
    error_rate: float
    details: Dict[str, Any]


@dataclass(frozen=True)
class SecurityScanResult:
    """Result of security scan."""
    scanned: bool
    scan_id: str
    scanned_at: datetime
    vulnerabilities_found: int
    severity: str  # none, low, medium, high, critical
    report_url: Optional[str] = None
    passed: bool = True


@dataclass
class ProviderListing:
    """
    A listing in the marketplace.
    Contains all information about a provider and its capabilities.
    """
    listing_id: str                   # Unique identifier
    provider_id: str                  # Provider being listed
    name: str                          # Display name
    description: str                    # What this provider does
    provider_type: str                 # Type of provider
    tier: str                          # Provider tier
    
    # Provider information
    version: str = "1.0"
    documentation_url: Optional[str] = None
    support_contact: Optional[str] = None
    pricing_info: Dict[str, Any] = field(default_factory=dict)
    
    # Capabilities
    capabilities: Tuple[Dict[str, Any], ...] = ()
    
    # Certification & Benchmarking
    certification: Optional[CertificationResult] = None
    benchmarks: Tuple[BenchmarkResult, ...] = ()
    security_scan: Optional[SecurityScanResult] = None
    
    # Listing metadata
    status: ListingStatus = ListingStatus.DRAFT
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    
    # Stats
    downloads: int = 0
    ratings_count: int = 0
    average_rating: float = 0.0
    
    # Tags for search
    tags: Tuple[str, ...] = ()
    
    def is_published(self) -> bool:
        """Check if listing is published and available."""
        return self.status == ListingStatus.APPROVED
    
    def is_certified(self) -> bool:
        """Check if provider is certified."""
        if self.certification is None:
            return False
        if not self.certification.certified:
            return False
        return datetime.utcnow() < self.certification.valid_until
    
    def is_secure(self) -> bool:
        """Check if provider passed security scan."""
        if self.security_scan is None:
            return False
        return self.security_scan.passed
    
    def is_ready_for_publication(self) -> bool:
        """Check if listing is ready to be published."""
        return (
            self.is_certified() and
            self.is_secure() and
            len(self.benchmarks) > 0 and
            self.documentation_url is not None
        )
    
    def approve(self, reviewer: str, notes: str = "") -> None:
        """Approve this listing."""
        self.status = ListingStatus.APPROVED
        self.reviewed_at = datetime.utcnow()
        self.reviewed_by = reviewer
        self.review_notes = notes
    
    def reject(self, reviewer: str, notes: str) -> None:
        """Reject this listing."""
        self.status = ListingStatus.REJECTED
        self.reviewed_at = datetime.utcnow()
        self.reviewed_by = reviewer
        self.review_notes = notes
    
    def suspend(self, reason: str) -> None:
        """Suspend this listing."""
        self.status = ListingStatus.SUSPENDED
        self.review_notes = reason
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "listing_id": self.listing_id,
            "provider_id": self.provider_id,
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


class Marketplace:
    """
    The Provider Marketplace.
    Where certified providers are discovered and published.
    """
    
    def __init__(self):
        self._listings: Dict[str, ProviderListing] = {}
        self._providers_index: Dict[str, str] = {}  # provider_id -> listing_id
        self._tags_index: Dict[str, Set[str]] = {}   # tag -> listing_ids
        self._type_index: Dict[str, Set[str]] = {}  # type -> listing_ids
    
    def create_listing(self, listing: ProviderListing) -> str:
        """
        Create a new marketplace listing.
        Returns the listing ID.
        """
        self._listings[listing.listing_id] = listing
        self._providers_index[listing.provider_id] = listing.listing_id
        
        # Update tags index
        for tag in listing.tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = set()
            self._tags_index[tag].add(listing.listing_id)
        
        # Update type index
        ptype = listing.provider_type
        if ptype not in self._type_index:
            self._type_index[ptype] = set()
        self._type_index[ptype].add(listing.listing_id)
        
        return listing.listing_id
    
    def get_listing(self, listing_id: str) -> Optional[ProviderListing]:
        """Get a listing by ID."""
        return self._listings.get(listing_id)
    
    def get_listing_by_provider(self, provider_id: str) -> Optional[ProviderListing]:
        """Get listing for a provider."""
        listing_id = self._providers_index.get(provider_id)
        if listing_id:
            return self._listings.get(listing_id)
        return None
    
    def list_published(self) -> List[ProviderListing]:
        """List all published (approved) listings."""
        return [
            listing for listing in self._listings.values()
            if listing.is_published()
        ]
    
    def list_by_type(self, provider_type: str) -> List[ProviderListing]:
        """List published listings by type."""
        listing_ids = self._type_index.get(provider_type, set())
        return [
            self._listings[lid] for lid in listing_ids
            if lid in self._listings and self._listings[lid].is_published()
        ]
    
    def list_by_tag(self, tag: str) -> List[ProviderListing]:
        """List published listings by tag."""
        listing_ids = self._tags_index.get(tag, set())
        return [
            self._listings[lid] for lid in listing_ids
            if lid in self._listings and self._listings[lid].is_published()
        ]
    
    def search(
        self,
        query: Optional[str] = None,
        provider_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tier: Optional[str] = None,
        certified_only: bool = True,
    ) -> List[ProviderListing]:
        """
        Search for listings.
        """
        results = self.list_published()
        
        # Filter by type
        if provider_type:
            results = [r for r in results if r.provider_type == provider_type]
        
        # Filter by tier
        if tier:
            results = [r for r in results if r.tier == tier]
        
        # Filter by certification
        if certified_only:
            results = [r for r in results if r.is_certified()]
        
        # Filter by tags
        if tags:
            results = [
                r for r in results
                if any(tag in r.tags for tag in tags)
            ]
        
        # Filter by query (simple text search)
        if query:
            query_lower = query.lower()
            results = [
                r for r in results
                if (
                    query_lower in r.name.lower() or
                    query_lower in r.description.lower() or
                    any(query_lower in tag.lower() for tag in r.tags)
                )
            ]
        
        # Sort by rating
        results.sort(key=lambda r: r.average_rating, reverse=True)
        
        return results
    
    def submit_for_review(self, listing_id: str) -> bool:
        """Submit a listing for review."""
        listing = self._listings.get(listing_id)
        if listing is None:
            return False
        
        if not listing.is_ready_for_publication():
            return False
        
        listing.status = ListingStatus.PENDING_REVIEW
        listing.submitted_at = datetime.utcnow()
        return True
    
    def review_listing(
        self,
        listing_id: str,
        decision: ReviewDecision,
        reviewer: str,
        notes: str = "",
    ) -> bool:
        """Review a listing."""
        listing = self._listings.get(listing_id)
        if listing is None:
            return False
        
        if listing.status != ListingStatus.PENDING_REVIEW:
            return False
        
        if decision == ReviewDecision.APPROVE:
            listing.approve(reviewer, notes)
        elif decision == ReviewDecision.REJECT:
            listing.reject(reviewer, notes)
        else:  # REQUEST_CHANGES
            listing.status = ListingStatus.DRAFT
            listing.review_notes = notes
        
        return True
    
    def deprecate(self, listing_id: str, reason: str) -> bool:
        """Deprecate a listing."""
        listing = self._listings.get(listing_id)
        if listing is None:
            return False
        
        listing.status = ListingStatus.DEPRECATED
        listing.review_notes = reason
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get marketplace statistics."""
        all_listings = list(self._listings.values())
        
        by_status = {}
        for listing in all_listings:
            status = listing.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        published = [l for l in all_listings if l.is_published()]
        
        return {
            "total_listings": len(all_listings),
            "published": len(published),
            "by_status": by_status,
            "total_types": len(self._type_index),
            "total_tags": len(self._tags_index),
            "average_rating": (
                sum(l.average_rating for l in published) / len(published)
                if published else 0
            ),
        }
    
    def export_catalog(self) -> Dict[str, Any]:
        """Export marketplace catalog for external use."""
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "listings": [
                {
                    "listing_id": l.listing_id,
                    "provider_id": l.provider_id,
                    "name": l.name,
                    "description": l.description,
                    "type": l.provider_type,
                    "tier": l.tier,
                    "tags": list(l.tags),
                    "capabilities": list(l.capabilities),
                    "certification": (
                        {
                            "tier": l.certification.tier,
                            "valid_until": l.certification.valid_until.isoformat(),
                        }
                        if l.certification else None
                    ),
                    "average_rating": l.average_rating,
                    "documentation_url": l.documentation_url,
                }
                for l in self.list_published()
            ],
        }
