#!/usr/bin/env python3
"""
AGOS Canon - Vocabulary (CANON-001)
=====================================

One definition per word. No ambiguity allowed.
This is the ONLY valid interpretation of terms in AGOS.

Canonical definitions for AGOS terminology.
Every term used in AGOS must be defined here and only here.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
import hashlib
import json


class TermCategory(Enum):
    """Categories of canonical terms."""
    CORE = "core"                    # Core AGOS terms
    AGENT = "agent"                  # Agent-related terms
    CAPABILITY = "capability"        # Capability terms
    PROVIDER = "provider"            # Provider terms
    KERNEL = "kernel"               # Kernel terms
    ORCHESTRATION = "orchestration"  # Orchestration terms
    KNOWLEDGE = "knowledge"          # Knowledge terms
    GOVERNANCE = "governance"        # Governance terms


@dataclass(frozen=True)
class CanonicalTerm:
    """
    Immutable canonical term definition.
    
    Once defined, a term CANNOT be redefined.
    If a term needs change, create a NEW term with version.
    """
    term: str                           # The canonical word/phrase
    definition: str                      # Single, unambiguous definition
    category: TermCategory              # Category this term belongs to
    examples: tuple = ()                # Valid usage examples
    anti_examples: tuple = ()            # Invalid usage examples
    related_terms: tuple = ()           # Related canonical terms
    version: str = "1.0"               # Version of this definition
    deprecated: bool = False             # Whether this term is deprecated
    replacement: Optional[str] = None   # If deprecated, what replaces it


class Vocabulary:
    """
    The single source of truth for AGOS terminology.
    
    Rules:
    1. One definition per term (no synonyms allowed as separate definitions)
    2. All terms are immutable once published
    3. Every AGOS component must use ONLY these terms
    4. Non-canonical terms must be mapped to canonical ones
    """
    
    _instance: Optional['Vocabulary'] = None
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._terms: Dict[str, CanonicalTerm] = {}
            self._hash: Optional[str] = None
            self._initialized = True
            self._initialize_terms()
    
    @classmethod
    def _get_instance(cls) -> 'Vocabulary':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _initialize_terms(self) -> None:
        """Initialize all canonical terms."""
        terms = [
            # ============ CORE TERMS ============
            CanonicalTerm(
                term="AGOS",
                definition="Autonomous General Orchestration System. The operating system for AI agents. NOT an AI agent itself, NOT an IDE, NOT a framework. A STANDARD for orchestrating autonomous execution.",
                category=TermCategory.CORE,
                examples=("AGOS defines how agents communicate",),
                anti_examples=("AGOS is an AI agent", "Use AGOS to chat"),
                related_terms=("kernel", "orchestration", "standard"),
            ),
            CanonicalTerm(
                term="kernel",
                definition="The central orchestrator of AGOS. Small, deterministic, observable, portable, replaceable. MUST NOT contain business logic. Only orchestrates.",
                category=TermCategory.KERNEL,
                examples=("The kernel coordinates all components",),
                anti_examples=("The kernel does the actual work", "Kernel contains AI logic"),
                related_terms=("agos", "orchestration", "component"),
            ),
            CanonicalTerm(
                term="orchestration",
                definition="Coordinating multiple agents/capabilities to achieve goals. NOT execution, NOT control. Coordination through well-defined interfaces.",
                category=TermCategory.ORCHESTRATION,
                examples=("The orchestrator routes tasks to agents",),
                anti_examples=("Orchestration executes code directly"),
                related_terms=("kernel", "agent", "capability"),
            ),
            CanonicalTerm(
                term="standard",
                definition="A specification that defines how components interact. Like POSIX for OS, OCI for containers. AGOS is the standard for agent orchestration.",
                category=TermCategory.CORE,
                examples=("Follow the AGOS standard for agent contracts",),
                anti_examples=("This is just a product standard"),
                related_terms=("agos", "specification", "contract"),
            ),
            
            # ============ AGENT TERMS ============
            CanonicalTerm(
                term="agent",
                definition="An autonomous entity that can perceive, decide, and act. In AGOS, agents are TOOLS that provide capabilities. NOT the brain of the system.",
                category=TermCategory.AGENT,
                examples=("The code-review agent analyzes pull requests",),
                anti_examples=("The agent decides everything", "Agent owns the mission"),
                related_terms=("capability", "provider", "tool"),
            ),
            CanonicalTerm(
                term="tool",
                definition="An external capability that AGOS can invoke. Agents ARE tools. OpenHands, Claude Code, Aider are all tools.",
                category=TermCategory.AGENT,
                examples=("Browser-use is a tool for web navigation",),
                anti_examples=("Tools are different from agents"),
                related_terms=("agent", "capability", "provider"),
            ),
            CanonicalTerm(
                term="mission",
                definition="A unit of work assigned to AGOS. Contains goal, context, constraints. The kernel OWNS the mission state.",
                category=TermCategory.ORCHESTRATION,
                examples=("The mission is to deploy this service",),
                anti_examples=("The agent owns the mission"),
                related_terms=("kernel", "goal", "context"),
            ),
            CanonicalTerm(
                term="brain",
                definition="The kernel's reasoning and planning capability. ONLY the kernel has a brain. External AI is FORBIDDEN to plan, reason, or own context.",
                category=TermCategory.KERNEL,
                examples=("The kernel brain creates execution plans",),
                anti_examples=("The agent brain decides what to do"),
                related_terms=("kernel", "planning", "reasoning"),
            ),
            
            # ============ CAPABILITY TERMS ============
            CanonicalTerm(
                term="capability",
                definition="A discrete, testable function that AGOS can perform. Capabilities are registered, versioned, and replaceable.",
                category=TermCategory.CAPABILITY,
                examples=("Web search is a capability", "Code generation is a capability"),
                anti_examples=("The whole AI is one capability"),
                related_terms=("provider", "contract", "registry"),
            ),
            CanonicalTerm(
                term="contract",
                definition="A versioned interface defining how capabilities interact. Contracts MUST be immutable once published. Changes require new version.",
                category=TermCategory.CAPABILITY,
                examples=("The task contract defines task submission",),
                anti_examples=("We'll fix the contract later"),
                related_terms=("capability", "versioning", "provider"),
            ),
            CanonicalTerm(
                term="provider",
                definition="An implementation of one or more capabilities. Multiple providers can implement the same capability. Providers are swappable.",
                category=TermCategory.PROVIDER,
                examples=("OpenAI is a provider for LLM capability", "GitHub is a provider for git capability"),
                anti_examples=("The provider IS the capability"),
                related_terms=("capability", "contract", "registry"),
            ),
            
            # ============ KNOWLEDGE TERMS ============
            CanonicalTerm(
                term="knowledge",
                definition="Verified information with source, evidence, confidence, and lineage. Knowledge is stored, retrieved, and evolves over time.",
                category=TermCategory.KNOWLEDGE,
                examples=("The architecture decision is stored as knowledge",),
                anti_examples=("Whatever the AI says is knowledge"),
                related_terms=("evidence", "source", "lineage"),
            ),
            CanonicalTerm(
                term="evidence",
                definition="Immutable proof supporting a claim or decision. Evidence is traceable, auditable, and versioned.",
                category=TermCategory.KNOWLEDGE,
                examples=("The test result is evidence of capability",),
                anti_examples=("The AI said so is evidence"),
                related_terms=("knowledge", "audit", "trace"),
            ),
            CanonicalTerm(
                term="lineage",
                definition="The complete history of how knowledge was created, modified, and propagated. Required for all knowledge objects.",
                category=TermCategory.KNOWLEDGE,
                examples=("The lineage shows who made each change",),
                anti_examples=("Knowledge appeared from nowhere"),
                related_terms=("knowledge", "evidence", "version"),
            ),
            
            # ============ GOVERNANCE TERMS ============
            CanonicalTerm(
                term="governance",
                definition="The rules and enforcement mechanisms that ensure AGOS operates correctly. Governance is built into the kernel.",
                category=TermCategory.GOVERNANCE,
                examples=("Governance validates all actions",),
                anti_examples=("Governance is optional"),
                related_terms=("kernel", "policy", "audit"),
            ),
            CanonicalTerm(
                term="policy",
                definition="A rule that governs behavior. Policies are versioned, tested, and enforced by governance.",
                category=TermCategory.GOVERNANCE,
                examples=("The privacy policy governs data handling",),
                anti_examples=("We'll decide at runtime"),
                related_terms=("governance", "rule", "enforcement"),
            ),
            CanonicalTerm(
                term="audit",
                definition="The systematic recording of all actions and decisions for accountability. Every action produces audit logs.",
                category=TermCategory.GOVERNANCE,
                examples=("The audit trail shows what happened",),
                anti_examples=("We'll add logging later"),
                related_terms=("governance", "evidence", "trace"),
            ),
            
            # ============ EXECUTION TERMS ============
            CanonicalTerm(
                term="execute",
                definition="To run a capability. Execution is observable, recoverable, and replayable. Nothing executes outside mission runtime.",
                category=TermCategory.ORCHESTRATION,
                examples=("Execute the code-review capability",),
                anti_examples=("Execute a plan in the background"),
                related_terms=("capability", "runtime", "mission"),
            ),
            CanonicalTerm(
                term="runtime",
                definition="The controlled environment where execution occurs. All execution happens within mission runtime.",
                category=TermCategory.ORCHESTRATION,
                examples=("The mission runtime provides isolation",),
                anti_examples=("Execute outside any runtime"),
                related_terms=("execute", "mission", "sandbox"),
            ),
            CanonicalTerm(
                term="decision",
                definition="A choice made by the kernel brain. Decisions are traceable, explainable, repeatable, and auditable.",
                category=TermCategory.KERNEL,
                examples=("The decision was to use the fast path",),
                anti_examples=("The AI decided to do X"),
                related_terms=("brain", "trace", "explain"),
            ),
            
            # ============ REPLACEABILITY TERMS ============
            CanonicalTerm(
                term="replaceable",
                definition="Any component can be swapped without breaking the system. No implementation is permanent. All components expose contracts.",
                category=TermCategory.CORE,
                examples=("The LLM provider is replaceable",),
                anti_examples=("We can't change this, it's core"),
                related_terms=("contract", "provider", "capability"),
            ),
            CanonicalTerm(
                term="version",
                definition="A unique identifier for a specific state of a component, contract, or artifact. Versions are immutable once published.",
                category=TermCategory.CORE,
                examples=("Contract v1.0 vs v2.0 are different",),
                anti_examples=("We updated in place"),
                related_terms=("contract", "lineage", "registry"),
            ),
        ]
        
        for term in terms:
            self._terms[term.term.lower()] = term
    
    def get(self, term: str) -> Optional[CanonicalTerm]:
        """Get a canonical term definition."""
        return self._terms.get(term.lower())
    
    def get_by_category(self, category: TermCategory) -> List[CanonicalTerm]:
        """Get all terms in a category."""
        return [t for t in self._terms.values() if t.category == category]
    
    def get_all_terms(self) -> List[CanonicalTerm]:
        """Get all canonical terms."""
        return list(self._terms.values())
    
    def validate_usage(self, term: str) -> tuple[bool, str]:
        """
        Validate if a term is used correctly.
        Returns (is_valid, reason).
        """
        canonical = self.get(term)
        if not canonical:
            return False, f"'{term}' is not a canonical AGOS term"
        
        if canonical.deprecated:
            replacement = canonical.replacement or "unknown"
            return False, f"'{term}' is deprecated. Use '{replacement}' instead"
        
        return True, f"'{term}' is a valid canonical term"
    
    def compute_hash(self) -> str:
        """Compute a deterministic hash of all terms."""
        if self._hash is None:
            terms_data = []
            for term in sorted(self._terms.keys()):
                t = self._terms[term]
                terms_data.append({
                    "term": t.term,
                    "definition": t.definition,
                    "category": t.category.value,
                    "version": t.version,
                })
            self._hash = hashlib.sha256(
                json.dumps(terms_data, sort_keys=True).encode()
            ).hexdigest()[:16]
        return self._hash
    
    def get_stats(self) -> dict:
        """Get vocabulary statistics."""
        categories = {}
        for term in self._terms.values():
            cat = term.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_terms": len(self._terms),
            "by_category": categories,
            "hash": self.compute_hash(),
            "version": "1.0",
        }


# Singleton accessor
def get_vocabulary() -> Vocabulary:
    """Get the singleton vocabulary instance."""
    return Vocabulary._get_instance()
