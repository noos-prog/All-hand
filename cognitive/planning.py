"""Planning engine: build a validated DAG plan from a goal + task list."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Sequence

from cognition.model import CognitiveError, Goal, Plan, PlanStep


@dataclass
class Task:
    name: str
    inputs: Dict[str, object]
    depends_on: List[str]


class PlanningEngine:
    def plan(self, goal: Goal, tasks: Sequence[Task]) -> Plan:
        by_name = {t.name: t for t in tasks}
        if len(by_name) != len(tasks):
            raise CognitiveError("task names must be unique")

        order = self._topo_sort(tasks)
        index_by_name = {name: i for i, name in enumerate(order)}
        steps: List[PlanStep] = []
        for i, name in enumerate(order):
            task = by_name[name]
            deps = tuple(index_by_name[d] for d in task.depends_on)
            steps.append(
                PlanStep(
                    index=i,
                    action=task.name,
                    inputs=dict(task.inputs),
                    expected_outcome=f"{task.name} complete",
                    depends_on=deps,
                )
            )
        plan = Plan(goal=goal, steps=tuple(steps))
        if not plan.is_dag():
            raise CognitiveError("planner produced an invalid DAG")
        return plan

    @staticmethod
    def _topo_sort(tasks: Sequence[Task]) -> List[str]:
        indeg: Dict[str, int] = defaultdict(int)
        graph: Dict[str, List[str]] = defaultdict(list)
        for t in tasks:
            indeg.setdefault(t.name, 0)
            for d in t.depends_on:
                graph[d].append(t.name)
                indeg[t.name] += 1

        queue = deque(sorted(n for n, d in indeg.items() if d == 0))
        out: List[str] = []
        while queue:
            n = queue.popleft()
            out.append(n)
            for m in sorted(graph[n]):
                indeg[m] -= 1
                if indeg[m] == 0:
                    queue.append(m)

        if len(out) != len(indeg):
            raise CognitiveError("cyclic dependency in tasks")
        return out
