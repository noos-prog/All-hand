#!/usr/bin/env python3
"""
AGOS Canon - Constitution (Articles I-XV)
==========================================

The Supreme Law of AGOS.
This document has higher priority than any implementation.
If any implementation conflicts with this constitution, the implementation MUST change.
The constitution never changes during normal development.

Article I:  The One Brain
Article II: Provider Principle
Article III: Capability Independence
Article IV: Versioning
Article V:  Verification
Article VI: Knowledge Evidence
Article VII: Explainable Decisions
Article VIII: Complete Replaceability
Article IX:  Mobile as Interface
Article X:  Kernel's Role
Article XI: Privacy
Article XII: Specification is Law
Article XIII: The Change Process
Article XIV: Canon Compliance
Article XV:  The Eternal Platform
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class ArticleType(Enum):
    """Types of constitutional articles."""
    IDENTITY = "identity"           # Defines what AGOS is
    PRINCIPLE = "principle"         # Operating principles
    RULE = "rule"                   # Mandatory rules
    CONSTRAINT = "constraint"       # Constraints on system
    REQUIREMENT = "requirement"     # Requirements


class ArticleStatus(Enum):
    """Status of article compliance."""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    VIOLATION = "violation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ConstitutionalArticle:
    """Immutable constitutional article."""
    number: int                       # Article number (1-15)
    roman_numeral: str               # Roman numeral (I-XV)
    title: str                       # Article title
    article_type: ArticleType        # Type of article
    statement: str                   # The constitutional statement
    rules: Tuple[str, ...]          # Specific rules
    requirements: Tuple[str, ...]    # Requirements
    forbidden: Tuple[str, ...]       # Forbidden actions
    examples_valid: Tuple[str, ...]  # Valid examples
    examples_invalid: Tuple[str, ...] # Invalid examples


class Constitution:
    """
    AGOS Constitution - The Supreme Law.
    
    This is the single source of truth for AGOS principles.
    All implementations MUST comply with all articles.
    Violations are treated as critical system failures.
    """
    
    VERSION = "1.0"
    
    # ============ ARTICLE I: THE ONE BRAIN ============
    ARTICLE_I = ConstitutionalArticle(
        number=1,
        roman_numeral="I",
        title="The One Brain",
        article_type=ArticleType.IDENTITY,
        statement="""
        AGOS has ONE and ONLY ONE brain: the kernel.
        The kernel owns all reasoning, planning, and decision-making.
        External AI is a TOOL that executes, not thinks.
        """,
        rules=(
            "The kernel creates all execution plans",
            "The kernel makes all routing decisions",
            "The kernel owns all mission state",
            "External AI receives plans, not creates them",
        ),
        requirements=(
            "Kernel must be able to explain any decision",
            "Kernel must track all reasoning paths",
            "Kernel must validate all plans",
        ),
        forbidden=(
            "Agents creating their own plans",
            "External AI making autonomous decisions",
            "Agents owning mission context",
            "Distributed decision-making",
        ),
        examples_valid=(
            "kernel.create_plan(intent) → [capability_1, capability_2]",
            "Agent receives plan and executes",
        ),
        examples_invalid=(
            "Agent creates its own plan",
            "LLM decides what to do next",
            "Agents share context without kernel",
        ),
    )
    
    # ============ ARTICLE II: PROVIDER PRINCIPLE ============
    ARTICLE_II = ConstitutionalArticle(
        number=2,
        roman_numeral="II",
        title="Provider Principle",
        article_type=ArticleType.PRINCIPLE,
        statement="""
        Every capability has one or more providers.
        Providers are replaceable at runtime.
        The kernel never knows WHICH provider is in use.
        """,
        rules=(
            "All capabilities have provider interface",
            "Providers are loaded dynamically",
            "Kernel references capabilities, not providers",
            "Multiple providers can implement same capability",
        ),
        requirements=(
            "Provider switching must not require code changes",
            "Provider must expose standard interface",
            "Provider state must be isolated",
        ),
        forbidden=(
            "Hardcoded provider references",
            "Provider-specific code in kernel",
            "Direct provider instantiation in core",
        ),
        examples_valid=(
            "capability.execute(params)  # kernel doesn't know which provider",
            "Provider A or B can implement this capability",
        ),
        examples_invalid=(
            "openai_provider.generate()  # direct reference",
            "kernel.openai_call()  # kernel knows provider",
        ),
    )
    
    # ============ ARTICLE III: CAPABILITY INDEPENDENCE ============
    ARTICLE_III = ConstitutionalArticle(
        number=3,
        roman_numeral="III",
        title="Capability Independence",
        article_type=ArticleType.PRINCIPLE,
        statement="""
        Each capability is independent and isolated.
        Capabilities cannot directly call each other.
        All inter-capability communication goes through kernel.
        """,
        rules=(
            "Capabilities are single-responsibility",
            "Capabilities communicate only via contracts",
            "No shared mutable state between capabilities",
            "Capabilities can be tested in isolation",
        ),
        requirements=(
            "Each capability has clear inputs/outputs",
            "Capabilities declare dependencies explicitly",
            "Capability isolation is enforced at runtime",
        ),
        forbidden=(
            "Capability A calling Capability B directly",
            "Shared global state between capabilities",
            "Implicit dependencies between capabilities",
        ),
        examples_valid=(
            "kernel.route(intent, capability_a) → capability_b",
            "Each capability has isolated state",
        ),
        examples_invalid=(
            "capability_a.call(capability_b)  # direct call",
            "global_state.shared_by_caps()",
        ),
    )
    
    # ============ ARTICLE IV: VERSIONING ============
    ARTICLE_IV = ConstitutionalArticle(
        number=4,
        roman_numeral="IV",
        title="Versioning",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        Everything that can change is versioned.
        Versions are immutable once published.
        Breaking changes require new major version.
        """,
        rules=(
            "All contracts are versioned",
            "All schemas are versioned",
            "All events are versioned",
            "All capabilities are versioned",
            "Version format: major.minor",
        ),
        requirements=(
            "Version must be in all public interfaces",
            "Old versions must continue working",
            "New versions must be documented",
        ),
        forbidden=(
            "Unversioned contracts",
            "Silent breaking changes",
            "Changing published versions",
        ),
        examples_valid=(
            "contract_v1_0, contract_v1_1, contract_v2_0",
            "Backward compatibility maintained",
        ),
        examples_invalid=(
            "contract.send()  # what version?",
            "Update contract without version bump",
        ),
    )
    
    # ============ ARTICLE V: VERIFICATION ============
    ARTICLE_V = ConstitutionalArticle(
        number=5,
        roman_numeral="V",
        title="Verification",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        Every action is verified before execution.
        Every result is validated after execution.
        Verification is automated and continuous.
        """,
        rules=(
            "Pre-execution validation required",
            "Post-execution verification required",
            "Verification failures block execution",
            "All verification is logged",
        ),
        requirements=(
            "Validation rules are versioned",
            "Verification is deterministic",
            "Verification can be skipped only by kernel",
        ),
        forbidden=(
            "Skipping verification for speed",
            "Silent verification failures",
            "Verification without logging",
        ),
        examples_valid=(
            "kernel.verify(preconditions) → pass/fail",
            "Result validated before return",
        ),
        examples_invalid=(
            "execute() without verify()",
            "Silent validation failure",
        ),
    )
    
    # ============ ARTICLE VI: KNOWLEDGE EVIDENCE ============
    ARTICLE_ARTICLE_VI = ConstitutionalArticle(
        number=6,
        roman_numeral="VI",
        title="Knowledge Evidence",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        All knowledge requires evidence.
        Evidence is immutable once stored.
        Knowledge can evolve, but history is preserved.
        """,
        rules=(
            "Every knowledge entry has source",
            "Every knowledge entry has evidence",
            "Every knowledge entry has confidence",
            "Every knowledge entry has lineage",
        ),
        requirements=(
            "Evidence cannot be modified",
            "Lineage shows all changes",
            "Confidence is quantitative",
        ),
        forbidden=(
            "Knowledge without evidence",
            "Modifying historical evidence",
            "Confidence without basis",
        ),
        examples_valid=(
            "knowledge.add(fact, evidence=..., confidence=0.9)",
            "Lineage shows {created: X, modified: Y}",
        ),
        examples_invalid=(
            "knowledge.add('I think X is true')",
            "Evidence modified after creation",
        ),
    )
    
    # ============ ARTICLE VII: EXPLAINABLE DECISIONS ============
    ARTICLE_VII = ConstitutionalArticle(
        number=7,
        roman_numeral="VII",
        title="Explainable Decisions",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        Every decision can be explained.
        Decisions are traceable to their inputs.
        The same input always produces the same decision.
        """,
        rules=(
            "All decisions are logged with inputs",
            "Decision logic is deterministic",
            "Confidence is stated for every decision",
            "Uncertainty is quantified",
        ),
        requirements=(
            "Decision trail is preserved",
            "Decisions can be replayed",
            "Confidence intervals are provided",
        ),
        forbidden=(
            "Mysterious AI decisions",
            "Random without seed",
            "Decisions without logging",
        ),
        examples_valid=(
            "decision_log = {input: X, logic: Y, output: Z, confidence: 0.95}",
            "Replaying decision produces same result",
        ),
        examples_invalid=(
            "The AI decided this was best",
            "Random selection without seed",
        ),
    )
    
    # ============ ARTICLE VIII: COMPLETE REPLACEABILITY ============
    ARTICLE_VIII = ConstitutionalArticle(
        number=8,
        roman_numeral="VIII",
        title="Complete Replaceability",
        article_type=ArticleType.PRINCIPLE,
        statement="""
        Any component can be replaced without breaking the system.
        No implementation is permanent.
        Replacement is a first-class operation.
        """,
        rules=(
            "All components implement contracts",
            "Components can be hot-swapped",
            "Replacement is tested before deployment",
            "Rollback is always possible",
        ),
        requirements=(
            "Replacement doesn't require restart",
            "Old component can be restored",
            "State is preserved during replacement",
        ),
        forbidden=(
            "Hardcoded implementations",
            "Components without interfaces",
            "State loss during replacement",
        ),
        examples_valid=(
            "kernel.replace_provider(capability, new_provider)",
            "Old provider can be restored",
        ),
        examples_invalid=(
            "This is core, cannot be replaced",
            "Hardcoded OpenAI reference",
        ),
    )
    
    # ============ ARTICLE IX: MOBILE AS INTERFACE ============
    ARTICLE_IX = ConstitutionalArticle(
        number=9,
        roman_numeral="IX",
        title="Mobile as Interface",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        Mobile is a first-class interface, not an afterthought.
        All functionality is accessible via mobile.
        Mobile experience is equal to desktop.
        """,
        rules=(
            "All features work on mobile",
            "Touch interfaces are native",
            "Mobile performance is optimized",
            "Mobile works offline where possible",
        ),
        requirements=(
            "Responsive design for all screens",
            "Touch-optimized interactions",
            "Bandwidth-efficient communication",
        ),
        forbidden=(
            "Desktop-only features",
            "Assuming fast network",
            "Ignoring mobile performance",
        ),
        examples_valid=(
            "Full functionality on mobile",
            "Touch-native controls",
        ),
        examples_invalid=(
            "Use desktop for full features",
            "Mobile is read-only",
        ),
    )
    
    # ============ ARTICLE X: KERNEL'S ROLE ============
    ARTICLE_X = ConstitutionalArticle(
        number=10,
        roman_numeral="X",
        title="Kernel's Role",
        article_type=ArticleType.CONSTRAINT,
        statement="""
        The kernel orchestrates only.
        The kernel never contains business logic.
        The kernel never knows about agents, models, or tools.
        """,
        rules=(
            "Kernel has no domain knowledge",
            "Kernel has no AI/ML logic",
            "Kernel has no tool-specific code",
            "Kernel only orchestrates via contracts",
        ),
        requirements=(
            "Kernel size is minimal",
            "Kernel is easily auditable",
            "Kernel changes rarely",
        ),
        forbidden=(
            "Business logic in kernel",
            "AI/ML in kernel",
            "Agent-specific code in kernel",
            "Tool-specific code in kernel",
        ),
        examples_valid=(
            "kernel.orchestrate(intent, contracts)",
            "kernel.route(intent, capabilities)",
        ),
        examples_invalid=(
            "kernel.analyze_code()",
            "kernel.call_openai()",
        ),
    )
    
    # ============ ARTICLE XI: PRIVACY ============
    ARTICLE_XI = ConstitutionalArticle(
        number=11,
        roman_numeral="XI",
        title="Privacy",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        User data is private by default.
        Data minimization is enforced.
        Privacy is built-in, not opt-in.
        """,
        rules=(
            "Collect only necessary data",
            "Data is encrypted at rest and in transit",
            "User controls their data",
            "Data retention is time-limited",
        ),
        requirements=(
            "Privacy by design",
            "Data minimization",
            "Right to deletion",
            "Audit of data access",
        ),
        forbidden=(
            "Collecting data 'for later'",
            "Sharing data without consent",
            "Data used for training without consent",
        ),
        examples_valid=(
            "Minimal data collection",
            "User controls data lifecycle",
        ),
        examples_invalid=(
            "Store everything for analytics",
            "Share with third parties",
        ),
    )
    
    # ============ ARTICLE XII: SPECIFICATION IS LAW ============
    ARTICLE_XII = ConstitutionalArticle(
        number=12,
        roman_numeral="XII",
        title="Specification is Law",
        article_type=ArticleType.RULE,
        statement="""
        The specification is the source of truth.
        Code must match specification.
        When code and spec conflict, spec wins.
        """,
        rules=(
            "Specification is authoritative",
            "Code is implementation of spec",
            "Spec changes require review",
            "Spec must be testable",
        ),
        requirements=(
            "All behavior is specified",
            "Spec is machine-readable",
            "Spec can be validated automatically",
        ),
        forbidden=(
            "Code that contradicts spec",
            "Features without spec",
            "Spec that cannot be tested",
        ),
        examples_valid=(
            "Spec defines behavior → Code implements it",
            "Conflict → Spec wins",
        ),
        examples_invalid=(
            "Code works differently than spec",
            "Feature added without spec",
        ),
    )
    
    # ============ ARTICLE XIII: THE CHANGE PROCESS ============
    ARTICLE_XIII = ConstitutionalArticle(
        number=13,
        roman_numeral="XIII",
        title="The Change Process",
        article_type=ArticleType.RULE,
        statement="""
        Changes follow a strict process.
        Constitution can only change in emergencies.
        Canon can evolve through proper process.
        """,
        rules=(
            "Proposed changes are reviewed",
            "Impact is assessed",
            "Migration path is defined",
            "Rollback plan exists",
        ),
        requirements=(
            "Change requires proposal",
            "Proposal requires justification",
            "Change requires testing",
            "Change requires documentation",
        ),
        forbidden=(
            "Rush changes without review",
            "Breaking changes without migration",
            "Constitution changes without emergency",
        ),
        examples_valid=(
            "RFC process → Review → Approval → Implementation",
            "Version bump with migration guide",
        ),
        examples_invalid=(
            "Quick fix without process",
            "Breaking change without migration",
        ),
    )
    
    # ============ ARTICLE XIV: CANON COMPLIANCE ============
    ARTICLE_XIV = ConstitutionalArticle(
        number=14,
        roman_numeral="XIV",
        title="Canon Compliance",
        article_type=ArticleType.REQUIREMENT,
        statement="""
        All code must comply with all canons.
        Non-compliant code cannot be merged.
        Compliance is automated where possible.
        """,
        rules=(
            "Canons are enforced automatically",
            "Violations block deployment",
            "Exceptions require approval",
            "Compliance is documented",
        ),
        requirements=(
            "Canons are machine-verifiable",
            "Violations are reported clearly",
            "Waivers require justification",
        ),
        forbidden=(
            "Merging non-compliant code",
            "Bypassing canon checks",
            "Exceptions without approval",
        ),
        examples_valid=(
            "Automated canon checker passes",
            "Violation reported with fix suggestion",
        ),
        examples_invalid=(
            "Canon check disabled for speed",
            "Violation ignored",
        ),
    )
    
    # ============ ARTICLE XV: THE ETERNAL PLATFORM ============
    ARTICLE_XV = ConstitutionalArticle(
        number=15,
        roman_numeral="XV",
        title="The Eternal Platform",
        article_type=ArticleType.IDENTITY,
        statement="""
        AGOS is a platform, not a product.
        AGOS outlives any specific implementation.
        AGOS defines the eternal contract between components.
        """,
        rules=(
            "AGOS standard is stable",
            "Implementations come and go",
            "Standard evolves slowly",
            "Backward compatibility is sacred",
        ),
        requirements=(
            "Standard is documented",
            "Standard is open",
            "Standard has reference implementation",
        ),
        forbidden=(
            "Abandoning backward compatibility",
            "Proprietary extensions to standard",
            "Breaking the platform promise",
        ),
        examples_valid=(
            "AGOS v1.0 still works with v3.0 components",
            "Multiple independent implementations",
        ),
        examples_invalid=(
            "Breaking changes in new version",
            "Proprietary extensions",
        ),
    )
    
    @classmethod
    def get_all_articles(cls) -> List[ConstitutionalArticle]:
        """Get all constitutional articles."""
        return [
            cls.ARTICLE_I,
            cls.ARTICLE_II,
            cls.ARTICLE_III,
            cls.ARTICLE_IV,
            cls.ARTICLE_V,
            cls.ARTICLE_ARTICLE_VI,
            cls.ARTICLE_VII,
            cls.ARTICLE_VIII,
            cls.ARTICLE_IX,
            cls.ARTICLE_X,
            cls.ARTICLE_XI,
            cls.ARTICLE_XII,
            cls.ARTICLE_XIII,
            cls.ARTICLE_XIV,
            cls.ARTICLE_XV,
        ]
    
    @classmethod
    def get_article(cls, number: int) -> Optional[ConstitutionalArticle]:
        """Get a specific article by number."""
        articles = {a.number: a for a in cls.get_all_articles()}
        return articles.get(number)
    
    @classmethod
    def compute_hash(cls) -> str:
        """Compute deterministic hash of constitution."""
        data = []
        for article in cls.get_all_articles():
            data.append({
                "article": article.roman_numeral,
                "title": article.title,
                "hash": hashlib.sha256(
                    article.statement.encode()
                ).hexdigest()[:8],
            })
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()[:16]
    
    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Get constitution summary."""
        return {
            "version": cls.VERSION,
            "articles": len(cls.get_all_articles()),
            "hash": cls.compute_hash(),
            "articles_summary": [
                {"number": a.number, "title": a.title, "type": a.article_type.value}
                for a in cls.get_all_articles()
            ],
        }
