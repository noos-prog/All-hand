"""Constitutional articles — the highest authority of AGOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple


class ViolationSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class Article:
    number: int
    title: str
    body: str
    mandatory: bool = True
    severity: ViolationSeverity = ViolationSeverity.HIGH
    tags: Tuple[str, ...] = field(default_factory=tuple)


IDENTITY_STATEMENT = (
    "AGOS is an operating system for autonomous execution. It is not an "
    "AI agent, chatbot, IDE, framework, orchestration tool or MCP client."
)

KERNEL_PROPERTIES: Tuple[str, ...] = (
    "small",
    "deterministic",
    "observable",
    "portable",
    "replaceable",
    "vendor-independent",
    "domain-independent",
    "ai-independent",
)

KERNEL_BLACKLIST: Tuple[str, ...] = (
    "models",
    "agents",
    "providers",
    "capabilities",
    "domains",
    "languages",
    "cloud-vendors",
    "tools",
    "storage-engines",
)

CONTRACT_RULES: Tuple[str, ...] = (
    "no direct dependencies",
    "no hidden dependencies",
    "no runtime shortcuts",
    "every capability is discoverable through a contract",
)


ARTICLES: Tuple[Article, ...] = (
    Article(
        number=1,
        title="Identity",
        body=IDENTITY_STATEMENT,
        severity=ViolationSeverity.CRITICAL,
        tags=("identity",),
    ),
    Article(
        number=2,
        title="Kernel Properties",
        body="The kernel must remain " + ", ".join(KERNEL_PROPERTIES) + ".",
        severity=ViolationSeverity.CRITICAL,
        tags=("kernel",),
    ),
    Article(
        number=3,
        title="Kernel Blacklist",
        body="The kernel may never know about: " + ", ".join(KERNEL_BLACKLIST) + ".",
        severity=ViolationSeverity.CRITICAL,
        tags=("kernel", "isolation"),
    ),
    Article(
        number=4,
        title="Contracts",
        body="Every capability crosses a contract. Rules: " + "; ".join(CONTRACT_RULES) + ".",
        severity=ViolationSeverity.HIGH,
        tags=("contracts",),
    ),
    Article(
        number=5,
        title="Versioning",
        body="All contracts are versioned using semantic versioning. Breaking changes require a new major version.",
        severity=ViolationSeverity.HIGH,
        tags=("contracts", "compatibility"),
    ),
    Article(
        number=6,
        title="Observability",
        body="Every cognitive and executive step must emit structured, replayable traces.",
        severity=ViolationSeverity.HIGH,
        tags=("observability",),
    ),
    Article(
        number=7,
        title="Determinism",
        body="Given identical inputs and seeds, cognition must produce identical outputs.",
        severity=ViolationSeverity.HIGH,
        tags=("determinism",),
    ),
    Article(
        number=8,
        title="Isolation",
        body="Agents and workspaces are isolated by default. Sharing requires an explicit grant.",
        severity=ViolationSeverity.HIGH,
        tags=("security", "isolation"),
    ),
    Article(
        number=9,
        title="Auditability",
        body="Every governance-relevant action must be recorded in an append-only audit log.",
        severity=ViolationSeverity.HIGH,
        tags=("governance", "audit"),
    ),
    Article(
        number=10,
        title="Reversibility",
        body="Every destructive operation on shared state must be reversible via snapshot and restore.",
        severity=ViolationSeverity.MEDIUM,
        tags=("safety",),
    ),
)


def article(number: int) -> Article:
    for a in ARTICLES:
        if a.number == number:
            return a
    raise KeyError(f"no article #{number}")
