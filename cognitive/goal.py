"""Goal engine: goal decomposition and priority-ordered scheduling."""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

from cognition.model import Goal


@dataclass
class GoalEngine:
    _counter: itertools.count = field(default_factory=itertools.count)
    _heap: List[Tuple[int, int, Goal]] = field(default_factory=list)

    def submit(self, goal: Goal) -> None:
        # heapq is min-heap: negate priority so higher priority runs first
        heapq.heappush(self._heap, (-goal.priority, next(self._counter), goal))

    def submit_many(self, goals: Sequence[Goal]) -> None:
        for g in goals:
            self.submit(g)

    def pop(self) -> Goal | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek(self) -> Goal | None:
        return self._heap[0][2] if self._heap else None

    def pending(self) -> int:
        return len(self._heap)

    def decompose(self, goal: Goal, subgoals: Sequence[str]) -> List[Goal]:
        out: List[Goal] = []
        for i, name in enumerate(subgoals):
            child = Goal(
                name=f"{goal.name}::{name}",
                description=f"subgoal {i + 1}/{len(subgoals)} of {goal.name}",
                success_criteria=goal.success_criteria,
                priority=max(0, goal.priority - 1),
            )
            self.submit(child)
            out.append(child)
        return out
