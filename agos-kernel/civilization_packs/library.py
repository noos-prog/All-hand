"""AGOS Civilization Packs Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CivilizationPackMetadata:
    """Civilization pack metadata."""
    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    domains: List[str] = field(default_factory=list)


class CivilizationPack:
    """A civilization pack."""
    
    def __init__(self, name: str, description: str = "", domains: List[str] = None):
        self.metadata = CivilizationPackMetadata(
            id=f"civ-{uuid.uuid4().hex[:8]}",
            name=name,
            description=description,
            domains=domains or [],
        )
        self.capabilities: List[str] = []
        self.knowledge: List[str] = []
        self.policies: List[str] = []
        self.templates: List[str] = []
        self.benchmarks: List[str] = []


# Civilization Packs
CIVILIZATION_PACKS = {
    "software": CivilizationPack(
        "Software Engineering Civilization",
        "Complete software engineering domain",
        ["software", "backend", "frontend"]
    ),
    "backend": CivilizationPack(
        "Backend Engineering Civilization",
        "Backend engineering excellence",
        ["backend", "api"]
    ),
    "frontend": CivilizationPack(
        "Frontend Engineering Civilization",
        "Frontend engineering excellence",
        ["frontend", "ui"]
    ),
    "mobile": CivilizationPack(
        "Mobile Engineering Civilization",
        "Mobile development excellence",
        ["mobile", "ios", "android"]
    ),
    "cloud": CivilizationPack(
        "Cloud Engineering Civilization",
        "Cloud architecture mastery",
        ["cloud", "aws", "azure", "gcp"]
    ),
    "platform": CivilizationPack(
        "Platform Engineering Civilization",
        "Platform engineering excellence",
        ["platform", "kubernetes", "devops"]
    ),
    "devops": CivilizationPack(
        "DevOps Engineering Civilization",
        "DevOps best practices",
        ["devops", "cicd", "infrastructure"]
    ),
    "security": CivilizationPack(
        "Cyber Security Civilization",
        "Security engineering mastery",
        ["security", "cyber", "compliance"]
    ),
    "ai": CivilizationPack(
        "AI Engineering Civilization",
        "AI engineering excellence",
        ["ai", "ml", "llm"]
    ),
    "llm": CivilizationPack(
        "LLM Engineering Civilization",
        "LLM application development",
        ["llm", "nlp", "rag"]
    ),
    "data": CivilizationPack(
        "Data Engineering Civilization",
        "Data engineering mastery",
        ["data", "analytics", "pipeline"]
    ),
    "database": CivilizationPack(
        "Database Engineering Civilization",
        "Database architecture excellence",
        ["database", "sql", "nosql"]
    ),
    "architecture": CivilizationPack(
        "Architecture Engineering Civilization",
        "Software architecture mastery",
        ["architecture", "design", "patterns"]
    ),
    "testing": CivilizationPack(
        "Testing Engineering Civilization",
        "Quality assurance excellence",
        ["testing", "qa", "automation"]
    ),
    "performance": CivilizationPack(
        "Performance Engineering Civilization",
        "Performance optimization mastery",
        ["performance", "optimization", "monitoring"]
    ),
    "observability": CivilizationPack(
        "Observability Civilization",
        "Full-stack observability",
        ["observability", "monitoring", "logging"]
    ),
    "networking": CivilizationPack(
        "Networking Civilization",
        "Network engineering excellence",
        ["networking", "protocols", "security"]
    ),
    "infrastructure": CivilizationPack(
        "Infrastructure Civilization",
        "Infrastructure as code mastery",
        ["infrastructure", "iac", "terraform"]
    ),
    "automation": CivilizationPack(
        "Automation Civilization",
        "Engineering automation excellence",
        ["automation", "scripts", "ci"]
    ),
    "enterprise": CivilizationPack(
        "Enterprise Civilization",
        "Enterprise-grade engineering",
        ["enterprise", "compliance", "governance"]
    ),
    "compliance": CivilizationPack(
        "Compliance Civilization",
        "Regulatory compliance mastery",
        ["compliance", "audit", "security"]
    ),
    "research": CivilizationPack(
        "Research Civilization",
        "Engineering research excellence",
        ["research", "innovation", "experimentation"]
    ),
    "education": CivilizationPack(
        "Education Civilization",
        "Engineering education mastery",
        ["education", "training", "onboarding"]
    ),
    "knowledge": CivilizationPack(
        "Knowledge Engineering Civilization",
        "Knowledge management excellence",
        ["knowledge", "graphs", "semantics"]
    ),
    "opensource": CivilizationPack(
        "Open Source Civilization",
        "Open source contribution mastery",
        ["opensource", "community", "collaboration"]
    ),
    "marketplace": CivilizationPack(
        "Marketplace Civilization",
        "Marketplace development",
        ["marketplace", "distribution", "billing"]
    ),
    "operations": CivilizationPack(
        "Operations Civilization",
        "Operational excellence",
        ["operations", "monitoring", "incident"]
    ),
    "reliability": CivilizationPack(
        "Reliability Engineering Civilization",
        "System reliability mastery",
        ["reliability", "sre", "availability"]
    ),
    "innovation": CivilizationPack(
        "Innovation Civilization",
        "Engineering innovation culture",
        ["innovation", "experiments", "prototypes"]
    ),
    "foundation": CivilizationPack(
        "Foundation Civilization",
        "Core AGOS foundation pack",
        ["foundation", "kernel", "core"]
    ),
}


class CivilizationPackLibrary:
    """Library of civilization packs."""
    
    def __init__(self):
        self.packs = CIVILIZATION_PACKS
    
    def get(self, name: str) -> CivilizationPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[CivilizationPack]:
        return list(self.packs.values())


_library = CivilizationPackLibrary()


def get_library() -> CivilizationPackLibrary:
    return _library