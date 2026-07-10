#!/usr/bin/env python3
"""
AGOS Canon - Rules (CANON-001 to CANON-010)
============================================

The 10 immutable rules of AGOS.
These cannot be overridden, ignored, or extended.
Compliance is MANDATORY for all AGOS components.

CANON-001: Vocabulary     - One definition per word
CANON-002: Forbidden Words - No ambiguous terms
CANON-003: Canonical Flow  - One official flow
CANON-004: Object Ownership - Strict ownership rules
CANON-005: Decision Rules  - Decision-making rules
CANON-006: Principles       - 10 absolute principles
CANON-007: Diagrams         - Official diagram formats
CANON-008: Naming           - Naming conventions
CANON-009: Contracts        - Contract versioning
CANON-010: Testing          - Mandatory testing
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class CanonType(Enum):
    """Types of canons (rules)."""
    VOCABULARY = "canon_001_vocabulary"
    FORBIDDEN_WORDS = "canon_002_forbidden_words"
    CANONICAL_FLOW = "canon_003_canonical_flow"
    OBJECT_OWNERSHIP = "canon_004_object_ownership"
    DECISION_RULES = "canon_005_decision_rules"
    PRINCIPLES = "canon_006_principles"
    DIAGRAMS = "canon_007_diagrams"
    NAMING = "canon_008_naming"
    CONTRACTS = "canon_009_contracts"
    TESTING = "canon_010_testing"


class ViolationSeverity(Enum):
    """Severity levels for canon violations."""
    CRITICAL = "critical"   # System cannot function
    HIGH = "high"           # Major violation
    MEDIUM = "medium"       # Significant violation
    LOW = "low"             # Minor violation
    WARNING = "warning"     # Advisory only


@dataclass(frozen=True)
class CanonRule:
    """Immutable canon rule definition."""
    id: str                      # e.g., "CANON-001"
    name: str                    # Human-readable name
    description: str              # Full description
    rule_text: str               # The actual rule
    examples_valid: Tuple[str, ...]   # Valid examples
    examples_invalid: Tuple[str, ...] # Invalid examples
    enforced_by: Tuple[str, ...]  # Tools that enforce this
    severity: ViolationSeverity  # Default severity if violated
    metadata: Tuple[Tuple[str, str], ...] = ()  # Additional metadata


class CanonRules:
    """
    The 10 immutable canons of AGOS.
    
    These rules are the foundation of AGOS.
    No exceptions. No overrides. No extensions.
    """
    
    # ============ CANON-001: VOCABULARY ============
    CANON_001 = CanonRule(
        id="CANON-001",
        name="Vocabulary",
        description="One definition per word. No ambiguity allowed.",
        rule_text="""
        Every term used in AGOS MUST have exactly ONE definition.
        
        Rules:
        1. No synonyms as separate definitions
        2. No overloaded meanings
        3. All terms defined in Vocabulary class
        4. Non-canonical terms MUST be mapped to canonical ones
        5. Definitions are immutable once published
        
        Forbidden:
        - Defining the same concept with different words
        - Using the same word for different concepts
        - Adding new definitions without version bump
        """,
        examples_valid=(
            "kernel.orchestrate() coordinates components",
            "agent.execute(capability) performs work",
        ),
        examples_invalid=(
            "The 'brain' AI makes decisions",
            "This is 'orchestrated' but also 'coordinated'",
        ),
        enforced_by=("vocabulary.py", "validator.py"),
        severity=ViolationSeverity.CRITICAL,
    )
    
    # ============ CANON-002: FORBIDDEN WORDS ============
    CANON_002 = CanonRule(
        id="CANON-002",
        name="Forbidden Words",
        description="No ambiguous or misleading terms allowed.",
        rule_text="""
        The following words/patterns are FORBIDDEN in AGOS:
        
        1. "AI" as a subject (AI cannot own, decide, or plan)
        2. "Magic" or "auto-magic" (explicit is better than implicit)
        3. "Just" (e.g., "just add this")
        4. "Obviously" or "clearly" (proof required)
        5. "Should" or "would" (use MUST, MAY, SHALL)
        6. "Maybe" or "probably" (decisions must be certain)
        7. "TODO" in production code
        8. "HACK" or "temporary" workarounds
        9. Hardcoded paths outside workspace
        10. Direct external API calls from kernel
        
        Allowed replacements:
        - "AI" → "external AI" or "LLM provider"
        - "Magic" → "explicit mechanism"
        - "Should" → "MUST" or "MAY"
        """,
        examples_valid=(
            "The LLM provider generates text",
            "The kernel MUST validate the input",
            "External AI MAY be used for generation",
        ),
        examples_invalid=(
            "The AI decided to do X",
            "This is magic, don't worry about it",
            "The code should work",
        ),
        enforced_by=("linter.py", "validator.py"),
        severity=ViolationSeverity.HIGH,
    )
    
    # ============ CANON-003: CANONICAL FLOW ============
    CANON_003 = CanonRule(
        id="CANON-003",
        name="Canonical Flow",
        description="One official flow for all operations.",
        rule_text="""
        Every operation in AGOS follows this flow:
        
        1. INTENT → User/system expresses intent
        2. PARSE → Kernel parses and validates intent
        3. PLAN → Kernel creates execution plan
        4. VALIDATE → Governance validates plan
        5. ROUTE → Kernel routes to capability
        6. EXECUTE → Capability executes
        7. OBSERVE → All actions produce events
        8. LOG → All results logged
        9. RESULT → Kernel returns result
        
        Rules:
        1. NO step can be skipped
        2. NO steps can be added
        3. Order MUST be preserved
        4. Events MUST be emitted at each step
        5. Errors at any step stop the flow
        """,
        examples_valid=(
            "Intent → Parse → Plan → Validate → Route → Execute → Observe → Log → Result",
        ),
        examples_invalid=(
            "Intent → Execute → Result (missing steps)",
            "Intent → Parse → Execute (out of order)",
        ),
        enforced_by=("kernel.py", "orchestrator.py", "validator.py"),
        severity=ViolationSeverity.CRITICAL,
    )
    
    # ============ CANON-004: OBJECT OWNERSHIP ============
    CANON_004 = CanonRule(
        id="CANON-004",
        name="Object Ownership",
        description="Strict ownership rules for all objects.",
        rule_text="""
        Every object has exactly ONE owner:
        
        KERNEL OWNS:
        - Intent
        - Goals
        - Context
        - Planning
        - Reasoning
        - Policies
        - Knowledge
        - Execution Graph
        - Mission State
        
        EXTERNAL AI MAY DO:
        - Execute
        - Generate
        - Transform
        - Analyze
        - Summarize
        - Translate
        - Review
        - Evaluate
        
        EXTERNAL AI MUST NOT:
        - Plan
        - Reason
        - Govern
        - Remember
        - Own Context
        - Own Knowledge
        - Own Missions
        
        Rules:
        1. Objects cannot be shared across ownership boundaries
        2. Access to owned objects requires explicit interface
        3. Violations are CRITICAL severity
        """,
        examples_valid=(
            "kernel.context holds mission state",
            "External AI generates code based on kernel plan",
        ),
        examples_invalid=(
            "Agent owns its own mission context",
            "AI decides to use a different policy",
        ),
        enforced_by=("kernel.py", "governance.py"),
        severity=ViolationSeverity.CRITICAL,
    )
    
    # ============ CANON-005: DECISION RULES ============
    CANON_005 = CanonRule(
        id="CANON-005",
        name="Decision Rules",
        description="All decisions must be traceable and auditable.",
        rule_text="""
        Every decision made by AGOS MUST be:
        
        1. TRACEABLE - You can trace how the decision was made
        2. EXPLICABLE - You can explain why the decision was made
        3. REPEATABLE - Same input produces same decision
        4. AUDITABLE - All decisions are logged
        
        Decision Requirements:
        - Input must be documented
        - Logic must be visible
        - Output must be recorded
        - Confidence must be stated
        
        Forbidden:
        - "The AI decided" (must specify the algorithm)
        - Random decisions without seed
        - Heuristics without evidence
        """,
        examples_valid=(
            "Decision: Route to fast-path because size < threshold",
            "Evidence: {size: 100, threshold: 1000}",
        ),
        examples_invalid=(
            "Decision: The AI thought this was best",
            "Decision: Random choice",
        ),
        enforced_by=("decision.py", "audit.py"),
        severity=ViolationSeverity.HIGH,
    )
    
    # ============ CANON-006: PRINCIPLES ============
    CANON_006 = CanonRule(
        id="CANON-006",
        name="10 Principles",
        description="The 10 absolute principles of AGOS.",
        rule_text="""
        The 10 Immutable Principles:
        
        1. KERNEL IS SMALL
           Kernel does nothing but orchestrate.
           No business logic in kernel.
           
        2. OBSERVABILITY ALWAYS
           If you can't observe it, it doesn't exist.
           Every action produces events.
           
        3. KNOWLEDGE HAS EVIDENCE
           Claims require proof.
           Evidence is immutable.
           
        4. EVERYTHING VERSIONED
           Contracts, schemas, events, capabilities.
           Nothing is mutable once published.
           
        5. REPLACEABILITY IS LAW
           Any component can be swapped.
           No vendor lock-in ever.
           
        6. NO SILENT EXECUTION
           Every execution produces logs.
           Every failure produces diagnostics.
           
        7. DECISIONS ARE AUDITED
           Trace every decision.
           Explain every choice.
           
        8. PROVIDERS ARE PLUGGABLE
           Multiple implementations allowed.
           Switch without breaking system.
           
        9. KERNEL PROTECTS ITSELF
           Nothing modifies the kernel.
           Kernel is read-only at runtime.
           
        10. CONSTITUTION IS SUPREME
            Constitution > Implementation.
            If conflict, constitution wins.
        """,
        examples_valid=(
            "New provider follows replaceability principle",
            "Decision logged with full trace",
        ),
        examples_invalid=(
            "Add this feature to the kernel",
            "Skip logging for performance",
        ),
        enforced_by=("kernel.py", "governance.py", "all"),
        severity=ViolationSeverity.CRITICAL,
    )
    
    # ============ CANON-007: DIAGRAMS ============
    CANON_007 = CanonRule(
        id="CANON-007",
        name="Diagram Formats",
        description="Official diagram formats for AGOS.",
        rule_text="""
        All diagrams MUST follow official formats:
        
        1. ARCHITECTURE DIAGRAMS
           Use Mermaid flowcharts
           Components are boxes
           Arrows show data flow
           
        2. SEQUENCE DIAGRAMS
           Use Mermaid sequence
           Vertical axis is time
           Horizontal is components
           
        3. STATE DIAGRAMS
           Use Mermaid state
           States are rounded boxes
           Transitions are arrows
           
        4. CLASS DIAGRAMS
           Use Mermaid class
           Public: +
           Private: -
           Protected: #
           
        5. COMPONENT DIAGRAMS
           Use Mermaid c4 or component
           Show ownership boundaries
           
        Forbidden:
        - UML not in Mermaid format
        - Screenshots of diagrams
        - Proprietary diagram formats
        """,
        examples_valid=(
            "```mermaid\\ngraph TD\\n  A --> B\\n```",
        ),
        examples_invalid=(
            "See the PowerPoint for diagram",
            "Screenshot in docs/",
        ),
        enforced_by=("docs/linter.py",),
        severity=ViolationSeverity.MEDIUM,
    )
    
    # ============ CANON-008: NAMING ============
    CANON_008 = CanonRule(
        id="CANON-008",
        name="Naming Conventions",
        description="Canonical naming for all AGOS entities.",
        rule_text="""
        Naming Rules:
        
        1. MODULES: snake_case
           e.g., capability_registry, knowledge_runtime
           
        2. CLASSES: PascalCase
           e.g., ComponentRegistry, KnowledgeEntry
           
        3. FUNCTIONS/METHODS: snake_case
           e.g., register_component(), get_by_id()
           
        4. CONSTANTS: UPPER_SNAKE_CASE
           e.g., MAX_RETRY_COUNT, DEFAULT_TIMEOUT
           
        5. VARIABLES: snake_case
           e.g., agent_id, task_status
           
        6. ENUMS: PascalCase values, EnumName type
           e.g., StatusType.ACTIVE, KernelState
           
        7. FILES: snake_case.py
           e.g., component_registry.py
           
        8. PACKAGES: snake_case/
           e.g., agent_civilization/
           
        Prefixes:
        - Providers: provider_
        - Capabilities: cap_
        - Contracts: contract_
        - Events: event_
        """,
        examples_valid=(
            "def register_component(component: Component) -> str:",
            "class KnowledgeRegistry:",
            "MAX_RETRY_COUNT = 3",
        ),
        examples_invalid=(
            "def RegisterComponent():",
            "class knowledgeRegistry:",
            "maxRetryCount = 3",
        ),
        enforced_by=("linter.py",),
        severity=ViolationSeverity.LOW,
    )
    
    # ============ CANON-009: CONTRACTS ============
    CANON_009 = CanonRule(
        id="CANON-009",
        name="Contract Versioning",
        description="Contracts must be versioned and immutable.",
        rule_text="""
        Contract Rules:
        
        1. VERSIONED
           Every contract has a version: major.minor
           e.g., contract_task_v1_0, contract_capability_v2_1
           
        2. IMMUTABLE
           Once published, contract cannot change
           Breaking change = new version
           
        3. DISCOVERABLE
           All contracts in registry
           Version info always available
           
        4. TESTED
           Every contract has tests
           Tests prove compliance
           
        5. VERSIONED ENTITIES:
           - Contracts
           - Schemas
           - Events
           - Capabilities
           - Providers
           - Skills
           - Artifacts
           - Knowledge
           - Policies
           - Missions
           - Workflows
           
        Version Format: v{major}_{minor}
        Breaking: increment major
        Additive: increment minor
        """,
        examples_valid=(
            "contract_task_v1_0.submit(task)",
            "contract_task_v1_1.submit(task, priority)",
        ),
        examples_invalid=(
            "contract_task.submit(task) // changed interface",
            "Just update the contract",
        ),
        enforced_by=("registry.py", "validator.py"),
        severity=ViolationSeverity.CRITICAL,
    )
    
    # ============ CANON-010: TESTING ============
    CANON_010 = CanonRule(
        id="CANON-010",
        name="Mandatory Testing",
        description="All capabilities must have tests.",
        rule_text="""
        Testing Requirements:
        
        1. UNIT TESTS
           Every function has tests
           100% coverage for critical paths
           Mock external dependencies
           
        2. INTEGRATION TESTS
           Every contract has tests
           Test provider interactions
           Test capability chains
           
        3. CANON COMPLIANCE TESTS
           Every component tested for canon compliance
           Automated canon checking
           Violations fail build
           
        4. CONTRACT TESTS
           Every version has validation tests
           Test backward compatibility
           Test forward compatibility
           
        5. BENCHMARK TESTS
           Performance tracked
           Regressions blocked
           Load testing for critical paths
        
        Coverage Requirements:
        - Kernel: 100% coverage
        - Capabilities: 90% coverage
        - Providers: 80% coverage
        - Other: 70% coverage
        """,
        examples_valid=(
            "test_capability_registry.py with 95% coverage",
            "contract_test_v1_0.py",
        ),
        examples_invalid=(
            "Manual testing only",
            "Code works, will add tests later",
        ),
        enforced_by=("pytest", "coverage.py", "ci.yml"),
        severity=ViolationSeverity.HIGH,
    )
    
    @classmethod
    def get_all_rules(cls) -> List[CanonRule]:
        """Get all canon rules."""
        return [
            cls.CANON_001,
            cls.CANON_002,
            cls.CANON_003,
            cls.CANON_004,
            cls.CANON_005,
            cls.CANON_006,
            cls.CANON_007,
            cls.CANON_008,
            cls.CANON_009,
            cls.CANON_010,
        ]
    
    @classmethod
    def get_rule(cls, canon_id: str) -> Optional[CanonRule]:
        """Get a specific canon rule by ID."""
        rules = {
            "CANON-001": cls.CANON_001,
            "CANON-002": cls.CANON_002,
            "CANON-003": cls.CANON_003,
            "CANON-004": cls.CANON_004,
            "CANON-005": cls.CANON_005,
            "CANON-006": cls.CANON_006,
            "CANON-007": cls.CANON_007,
            "CANON-008": cls.CANON_008,
            "CANON-009": cls.CANON_009,
            "CANON-010": cls.CANON_010,
        }
        return rules.get(canon_id)
    
    @classmethod
    def get_rule_hash(cls) -> str:
        """Compute hash of all rules for verification."""
        rules_data = []
        for rule in cls.get_all_rules():
            rules_data.append({
                "id": rule.id,
                "name": rule.name,
                "hash": hashlib.sha256(rule.rule_text.encode()).hexdigest()[:8],
            })
        return hashlib.sha256(
            json.dumps(rules_data, sort_keys=True).encode()
        ).hexdigest()[:16]
