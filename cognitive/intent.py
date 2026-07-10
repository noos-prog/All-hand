"""Intent engine: minimal utterance -> intent classifier.

Deterministic keyword scoring; production deployments plug in an
LLM-backed reasoner via :class:`cognition.model.Reasoner`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping

from cognition.model import Intent


_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass
class IntentEngine:
    """Score utterances against a table of verbs and their keyword hints."""

    verbs: Mapping[str, Iterable[str]] = field(
        default_factory=lambda: {
            "create": ("create", "make", "build", "generate", "spawn"),
            "read": ("read", "get", "fetch", "list", "show"),
            "update": ("update", "modify", "edit", "change", "patch"),
            "delete": ("delete", "remove", "drop", "destroy"),
            "analyze": ("analyze", "inspect", "review", "audit"),
            "orchestrate": ("run", "orchestrate", "execute", "coordinate"),
        }
    )
    default_verb: str = "process"

    def infer(self, utterance: str) -> Intent:
        tokens = [t.lower() for t in _TOKEN_RE.findall(utterance or "")]
        if not tokens:
            return Intent(verb=self.default_verb, target="", confidence=0.0)

        scores: Dict[str, int] = {v: 0 for v in self.verbs}
        for verb, hints in self.verbs.items():
            hset = {h.lower() for h in hints}
            scores[verb] = sum(1 for t in tokens if t in hset)

        best_verb, best_score = max(scores.items(), key=lambda kv: kv[1])
        if best_score == 0:
            best_verb = self.default_verb

        confidence = min(1.0, 0.4 + 0.2 * best_score)
        target = _first_noun(tokens, exclude=set().union(*[set(h) for h in self.verbs.values()]))
        return Intent(
            verb=best_verb,
            target=target,
            parameters={"tokens": tokens},
            confidence=confidence,
        )


def _first_noun(tokens: List[str], exclude: set[str]) -> str:
    for t in tokens:
        if t not in exclude and not t.isdigit():
            return t
    return ""
