#!/usr/bin/env python3
"""
AGOS Enterprise - Capability Pack Module
=======================================

Ready-made packages of capabilities for specific domains.
Capability packs enable rapid deployment of enterprise solutions.

Example Packs:
- Healthcare Pack: HIPAA Compliance, Medical Data Processing, HL7 Integration
- FinTech Pack: PCI-DSS Compliance, Financial APIs, Risk Analysis
- Enterprise Pack: SSO Integration, Audit Logging, Compliance Reporting
- Mobile Pack: iOS Development, Android Development, App Store Deployment
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class PackType(Enum):
    """Types of capability packs."""
    HEALTHCARE = "healthcare"
    FINTECH = "fintech"
    ENTERPRISE = "enterprise"
    MOBILE = "mobile"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    GOVERNMENT = "government"
    CUSTOM = "custom"


class PackStatus(Enum):
    """Status of a capability pack."""
    DRAFT = "draft"
    TESTING = "testing"
    STABLE = "stable"
    DEPRECATED = "deprecated"


@dataclass(frozen=True)
class PackRequirement:
    """A requirement for the pack."""
    requirement_id: str
    name: str
    description: str
    required: bool = True


@dataclass(frozen=True)
class PackCapability:
    """A capability included in the pack."""
    capability_id: str
    name: str
    description: str
    skills: Tuple[str, ...]  # Skill IDs required
    providers: Tuple[str, ...]  # Recommended providers


@dataclass
class CapabilityPack:
    """
    A ready-made package of capabilities.
    Enables rapid deployment for specific domains.
    """
    pack_id: str                       # Unique identifier
    name: str                           # Pack name
    description: str                    # What this pack provides
    pack_type: PackType                # Type of pack
    status: PackStatus = PackStatus.DRAFT
    
    # Contents
    capabilities: Tuple[PackCapability, ...] = ()
    requirements: Tuple[PackRequirement, ...] = ()
    
    # Configuration
    version: str = "1.0"
    config_template: Dict[str, Any] = field(default_factory=dict)
    
    # Dependencies
    required_packs: Tuple[str, ...] = ()  # Other packs required
    optional_packs: Tuple[str, ...] = ()   # Other packs optional
    
    # Metadata
    tags: Tuple[str, ...] = ()
    author: str = "AGOS"
    documentation_url: Optional[str] = None
    
    # Compliance
    compliance_frameworks: Tuple[str, ...] = ()  # e.g., HIPAA, PCI-DSS
    security_requirements: Tuple[str, ...] = ()
    
    def get_capability_ids(self) -> List[str]:
        """Get all capability IDs in this pack."""
        return [c.capability_id for c in self.capabilities]
    
    def get_skill_ids(self) -> Set[str]:
        """Get all skill IDs required by this pack."""
        skills = set()
        for cap in self.capabilities:
            skills.update(cap.skills)
        return skills
    
    def get_provider_ids(self) -> Set[str]:
        """Get all recommended provider IDs."""
        providers = set()
        for cap in self.capabilities:
            providers.update(cap.providers)
        return providers
    
    def check_requirements_met(
        self,
        available_capabilities: Set[str],
        available_skills: Set[str],
    ) -> Tuple[bool, List[str]]:
        """
        Check if all requirements are met.
        Returns (all_met, unmet_list).
        """
        unmet = []
        
        # Check required requirements
        for req in self.requirements:
            if req.required:
                if req.requirement_id not in available_capabilities:
                    unmet.append(f"Missing capability: {req.requirement_id}")
        
        # Check skill requirements
        required_skills = self.get_skill_ids()
        missing_skills = required_skills - available_skills
        if missing_skills:
            unmet.append(f"Missing skills: {', '.join(missing_skills)}")
        
        return len(unmet) == 0, unmet
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "pack_id": self.pack_id,
            "name": self.name,
            "pack_type": self.pack_type.value,
            "version": self.version,
            "capabilities": self.get_capability_ids(),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]


class PackRegistry:
    """
    Registry of all capability packs.
    Manages pack discovery and installation.
    """
    
    def __init__(self):
        self._packs: Dict[str, CapabilityPack] = {}
        self._installed: Set[str] = set()  # Installed pack IDs
        self._tags_index: Dict[str, Set[str]] = {}
        self._type_index: Dict[PackType, Set[str]] = {}
    
    def register(self, pack: CapabilityPack) -> None:
        """Register a capability pack."""
        self._packs[pack.pack_id] = pack
        
        # Update type index
        if pack.pack_type not in self._type_index:
            self._type_index[pack.pack_type] = set()
        self._type_index[pack.pack_type].add(pack.pack_id)
        
        # Update tags index
        for tag in pack.tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = set()
            self._tags_index[tag].add(pack.pack_id)
    
    def install(self, pack_id: str) -> bool:
        """Mark a pack as installed."""
        if pack_id in self._packs:
            self._installed.add(pack_id)
            return True
        return False
    
    def uninstall(self, pack_id: str) -> bool:
        """Mark a pack as uninstalled."""
        if pack_id in self._installed:
            self._installed.discard(pack_id)
            return True
        return False
    
    def is_installed(self, pack_id: str) -> bool:
        """Check if pack is installed."""
        return pack_id in self._installed
    
    def get_pack(self, pack_id: str) -> Optional[CapabilityPack]:
        """Get a pack by ID."""
        return self._packs.get(pack_id)
    
    def list_all(self) -> List[CapabilityPack]:
        """List all packs."""
        return list(self._packs.values())
    
    def list_installed(self) -> List[CapabilityPack]:
        """List installed packs."""
        return [self._packs[pid] for pid in self._installed if pid in self._packs]
    
    def list_by_type(self, pack_type: PackType) -> List[CapabilityPack]:
        """List packs by type."""
        pack_ids = self._type_index.get(pack_type, set())
        return [self._packs[pid] for pid in pack_ids if pid in self._packs]
    
    def list_stable(self) -> List[CapabilityPack]:
        """List stable packs."""
        return [p for p in self._packs.values() if p.status == PackStatus.STABLE]
    
    def search(
        self,
        query: Optional[str] = None,
        pack_type: Optional[PackType] = None,
        tags: Optional[List[str]] = None,
        stable_only: bool = True,
    ) -> List[CapabilityPack]:
        """Search for packs."""
        results = list(self._packs.values())
        
        # Filter by type
        if pack_type:
            results = [r for r in results if r.pack_type == pack_type]
        
        # Filter by stable
        if stable_only:
            results = [r for r in results if r.status == PackStatus.STABLE]
        
        # Filter by tags
        if tags:
            results = [
                r for r in results
                if any(tag in r.tags for tag in tags)
            ]
        
        # Filter by query
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
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_packs": len(self._packs),
            "installed": len(self._installed),
            "by_type": {
                ptype.value: len(pids)
                for ptype, pids in self._type_index.items()
            },
            "by_status": {
                status.value: len([p for p in self._packs.values() if p.status == status])
                for status in PackStatus
            },
        }


# ============ BUILT-IN CAPABILITY PACKS ============

def create_healthcare_pack() -> CapabilityPack:
    """Create Healthcare Pack."""
    return CapabilityPack(
        pack_id="pack_healthcare_001",
        name="Healthcare Pack",
        description="Complete healthcare AI capabilities with HIPAA compliance",
        pack_type=PackType.HEALTHCARE,
        status=PackStatus.STABLE,
        capabilities=(
            PackCapability(
                capability_id="cap_hipaa_compliance",
                name="HIPAA Compliance Checker",
                description="Check systems for HIPAA compliance",
                skills=("skill_validate_phi", "skill_check_access"),
                providers=("prov_security_scanner",),
            ),
            PackCapability(
                capability_id="cap_medical_data",
                name="Medical Data Processor",
                description="Process and analyze medical records",
                skills=("skill_parse_hl7", "skill_anonymize"),
                providers=("prov_data_processor",),
            ),
            PackCapability(
                capability_id="cap_hl7_integration",
                name="HL7 FHIR Integration",
                description="Integrate with healthcare systems via HL7",
                skills=("skill_parse_hl7", "skill_api_client"),
                providers=("prov_api_gateway",),
            ),
        ),
        requirements=(
            PackRequirement(
                requirement_id="req_hipaa_compliance",
                name="HIPAA Compliance Module",
                description="Must have HIPAA compliance capabilities",
            ),
        ),
        tags=("healthcare", "hipaa", "medical", "compliance"),
        compliance_frameworks=("HIPAA",),
        security_requirements=("encryption_at_rest", "audit_logging", "access_control"),
    )


def create_fintech_pack() -> CapabilityPack:
    """Create FinTech Pack."""
    return CapabilityPack(
        pack_id="pack_fintech_001",
        name="FinTech Pack",
        description="Financial services capabilities with PCI-DSS compliance",
        pack_type=PackType.FINTECH,
        status=PackStatus.STABLE,
        capabilities=(
            PackCapability(
                capability_id="cap_pci_compliance",
                name="PCI-DSS Compliance Checker",
                description="Check systems for PCI-DSS compliance",
                skills=("skill_scan_security", "skill_validate_config"),
                providers=("prov_security_scanner",),
            ),
            PackCapability(
                capability_id="cap_financial_api",
                name="Financial API Integration",
                description="Integrate with financial services APIs",
                skills=("skill_api_client", "skill_authenticate"),
                providers=("prov_api_gateway",),
            ),
            PackCapability(
                capability_id="cap_risk_analysis",
                name="Risk Analysis Engine",
                description="Analyze financial risk factors",
                skills=("skill_analyze_data", "skill_generate_report"),
                providers=("prov_ai_model",),
            ),
        ),
        requirements=(),
        tags=("fintech", "pci-dss", "financial", "compliance"),
        compliance_frameworks=("PCI-DSS", "SOC2"),
        security_requirements=("encryption_at_rest", "encryption_in_transit", "audit_logging"),
    )


def create_enterprise_pack() -> CapabilityPack:
    """Create Enterprise Pack."""
    return CapabilityPack(
        pack_id="pack_enterprise_001",
        name="Enterprise Pack",
        description="Enterprise-grade capabilities for large organizations",
        pack_type=PackType.ENTERPRISE,
        status=PackStatus.STABLE,
        capabilities=(
            PackCapability(
                capability_id="cap_sso_integration",
                name="SSO Integration",
                description="Single Sign-On integration with enterprise IdPs",
                skills=("skill_authenticate", "skill_manage_session"),
                providers=("prov_identity_provider",),
            ),
            PackCapability(
                capability_id="cap_audit_logging",
                name="Enterprise Audit Logging",
                description="Comprehensive audit logging for compliance",
                skills=("skill_log_event", "skill_generate_report"),
                providers=("prov_log_service",),
            ),
            PackCapability(
                capability_id="cap_compliance_reporting",
                name="Compliance Reporting",
                description="Generate compliance reports for regulations",
                skills=("skill_aggregate_data", "skill_generate_report"),
                providers=("prov_reporting_service",),
            ),
        ),
        requirements=(),
        tags=("enterprise", "sso", "audit", "compliance"),
        compliance_frameworks=("SOC2", "ISO27001"),
        security_requirements=("audit_logging", "access_control", "encryption"),
    )


def create_mobile_pack() -> CapabilityPack:
    """Create Mobile Pack."""
    return CapabilityPack(
        pack_id="pack_mobile_001",
        name="Mobile Pack",
        description="Mobile development and deployment capabilities",
        pack_type=PackType.MOBILE,
        status=PackStatus.STABLE,
        capabilities=(
            PackCapability(
                capability_id="cap_ios_develop",
                name="iOS Development",
                description="Build and test iOS applications",
                skills=("skill_compile_xcode", "skill_run_tests"),
                providers=("prov_xcode", "prov_firebase_test"),
            ),
            PackCapability(
                capability_id="cap_android_develop",
                name="Android Development",
                description="Build and test Android applications",
                skills=("skill_compile_gradle", "skill_run_tests"),
                providers=("prov_android_sdk", "prov_firebase_test"),
            ),
            PackCapability(
                capability_id="cap_app_store_deploy",
                name="App Store Deployment",
                description="Deploy to iOS and Android app stores",
                skills=("skill_upload_store", "skill_manage_metadata"),
                providers=("prov_app_store_connect",),
            ),
        ),
        requirements=(),
        tags=("mobile", "ios", "android", "app-store"),
    )
