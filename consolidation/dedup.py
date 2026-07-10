"""Shingle-based near-duplicate detection using Jaccard similarity."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple


_WORD_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class ShingleFingerprint:
    tokens: Tuple[str, ...]

    @classmethod
    def of(cls, text: str, size: int = 3) -> "ShingleFingerprint":
        if size < 1:
            raise ValueError("shingle size must be >= 1")
        words = [w.lower() for w in _WORD_RE.findall(text or "")]
        if len(words) < size:
            return cls(tokens=tuple(" ".join(words) for _ in range(1)) if words else ())
        return cls(tokens=tuple(" ".join(words[i : i + size]) for i in range(len(words) - size + 1)))

    def jaccard(self, other: "ShingleFingerprint") -> float:
        a: Set[str] = set(self.tokens)
        b: Set[str] = set(other.tokens)
        if not a and not b:
            return 1.0
        union = a | b
        if not union:
            return 0.0
        return len(a & b) / len(union)


class Deduplicator:
    """O(n) deduplication using a running set of accepted fingerprints."""

    def __init__(self, threshold: float = 0.85, shingle_size: int = 3) -> None:
        if not 0.0 < threshold <= 1.0:
            raise ValueError("threshold must be within (0, 1]")
        self.threshold = threshold
        self.shingle_size = shingle_size

    def unique(self, texts: Iterable[str]) -> List[Tuple[int, str]]:
        accepted: List[Tuple[int, str, ShingleFingerprint]] = []
        for idx, text in enumerate(texts):
            fp = ShingleFingerprint.of(text, size=self.shingle_size)
            if not any(fp.jaccard(f) >= self.threshold for _, _, f in accepted):
                accepted.append((idx, text, fp))
        return [(i, t) for i, t, _ in accepted]
