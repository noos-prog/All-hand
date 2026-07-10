"""Reasoning engine: forward-chaining over declarative rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Tuple


@dataclass(frozen=True)
class Rule:
    name: str
    condition: Callable[[Mapping[str, Any]], bool]
    conclusion: Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class ReasoningStep:
    rule: str
    before: Mapping[str, Any]
    after: Mapping[str, Any]


@dataclass
class ReasoningEngine:
    rules: List[Rule] = field(default_factory=list)
    max_iterations: int = 64

    def add(self, rule: Rule) -> None:
        self.rules.append(rule)

    def infer(self, facts: Mapping[str, Any]) -> Tuple[Dict[str, Any], List[ReasoningStep]]:
        state: Dict[str, Any] = dict(facts)
        trace: List[ReasoningStep] = []
        for _ in range(self.max_iterations):
            fired = False
            for rule in self.rules:
                try:
                    matched = bool(rule.condition(state))
                except Exception:
                    matched = False
                if not matched:
                    continue
                before = dict(state)
                delta = rule.conclusion(state) or {}
                if not delta or all(state.get(k) == v for k, v in delta.items()):
                    continue
                state.update(delta)
                trace.append(ReasoningStep(rule=rule.name, before=before, after=dict(state)))
                fired = True
            if not fired:
                break
        return state, trace
