"""Strategy engine: select a named strategy against a context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping


@dataclass(frozen=True)
class Strategy:
    name: str
    applies: Callable[[Mapping[str, Any]], bool]
    apply: Callable[[Mapping[str, Any]], Dict[str, Any]]
    priority: int = 0


@dataclass
class StrategyEngine:
    strategies: Dict[str, Strategy] = field(default_factory=dict)

    def register(self, strategy: Strategy) -> None:
        self.strategies[strategy.name] = strategy

    def select(self, context: Mapping[str, Any]) -> Strategy | None:
        matches = [s for s in self.strategies.values() if _safe(s.applies, context)]
        if not matches:
            return None
        matches.sort(key=lambda s: s.priority, reverse=True)
        return matches[0]

    def apply(self, context: Mapping[str, Any]) -> Dict[str, Any]:
        s = self.select(context)
        if s is None:
            return {}
        return s.apply(context) or {}


def _safe(fn: Callable[[Mapping[str, Any]], bool], ctx: Mapping[str, Any]) -> bool:
    try:
        return bool(fn(ctx))
    except Exception:
        return False
