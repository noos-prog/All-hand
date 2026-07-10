"""Consolidator: episodes -> semantic records with dedup and decay."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Sequence, Tuple

from .decay import DecayPolicy, ExponentialDecay, age_seconds
from .dedup import Deduplicator
from .episode import Episode, EpisodicStream, SemanticRecord


@dataclass
class ConsolidationReport:
    scanned: int = 0
    accepted: int = 0
    duplicates: int = 0
    decayed_out: int = 0
    records: List[SemanticRecord] = field(default_factory=list)


class Consolidator:
    """Deterministic consolidation. Plug in an LLM summarizer when available."""

    def __init__(
        self,
        deduplicator: Deduplicator | None = None,
        decay: DecayPolicy | None = None,
        min_importance: float = 0.05,
    ) -> None:
        self.deduplicator = deduplicator or Deduplicator()
        self.decay = decay or ExponentialDecay()
        self.min_importance = min_importance

    def consolidate(
        self,
        stream: EpisodicStream,
        *,
        now: datetime | None = None,
    ) -> ConsolidationReport:
        now = now or datetime.now(timezone.utc)
        episodes = stream.drain()
        report = ConsolidationReport(scanned=len(episodes))
        if not episodes:
            return report

        # 1) apply decay, filter negligible episodes
        alive: List[Episode] = []
        for ep in episodes:
            decayed = self.decay.decay(ep.importance, age_seconds(ep.created_at, now))
            if decayed < self.min_importance:
                report.decayed_out += 1
                continue
            alive.append(_with_importance(ep, decayed))

        # 2) dedup on content
        kept_indices = {i for i, _ in self.deduplicator.unique(ep.content for ep in alive)}
        report.duplicates = len(alive) - len(kept_indices)
        kept = [ep for i, ep in enumerate(alive) if i in kept_indices]

        # 3) cluster by tag-key and summarize
        clusters: Dict[Tuple[str, ...], List[Episode]] = {}
        for ep in kept:
            clusters.setdefault(ep.tags, []).append(ep)

        for tags, group in clusters.items():
            record = self._summarize(tags, group)
            report.records.append(record)
            report.accepted += len(group)

        return report

    def _summarize(self, tags: Tuple[str, ...], group: Sequence[Episode]) -> SemanticRecord:
        summary = _build_summary(group)
        supports = tuple(ep.episode_id for ep in group)
        avg_importance = sum(ep.importance for ep in group) / len(group)
        rec_id = "sem_" + hashlib.sha1(
            ("|".join(supports) + "|" + summary).encode("utf-8")
        ).hexdigest()[:16]
        return SemanticRecord(
            record_id=rec_id,
            summary=summary,
            supports=supports,
            tags=tags,
            importance=avg_importance,
        )


def _with_importance(ep: Episode, importance: float) -> Episode:
    return Episode(
        episode_id=ep.episode_id,
        agent_id=ep.agent_id,
        content=ep.content,
        tags=ep.tags,
        metadata=ep.metadata,
        created_at=ep.created_at,
        importance=importance,
    )


def _build_summary(group: Sequence[Episode]) -> str:
    contents = [ep.content.strip() for ep in group if ep.content.strip()]
    if not contents:
        return ""
    if len(contents) == 1:
        return contents[0][:512]
    head = contents[0][:256]
    return f"{len(contents)} related episodes: {head} ..."
