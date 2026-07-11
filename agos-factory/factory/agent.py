#!/usr/bin/env python3
"""
FactoryAgent — a real, ephemeral agent instance stamped out of a Blueprint.

Unlike `agent_civilization/agents/specialists/*.py` (1,021 hand-generated
files with hard-coded results), a `FactoryAgent` is a lightweight object
created in microseconds from an `AgentBlueprint`, backed by the *same* real
LLM client and real tools the rest of the civilization uses. Millions of
task executions can flow through a small number of these objects because
`AgentPool` recycles them instead of leaking one object per task.
"""

from __future__ import annotations

import itertools
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .blueprint import AgentBlueprint

logger = logging.getLogger("agos_factory.agent")

_id_counter = itertools.count(1)


@dataclass
class AgentStats:
    """Lifetime counters for a single `FactoryAgent` instance."""

    tasks_completed: int = 0
    tasks_failed: int = 0
    total_time_s: float = 0.0

    def record(self, elapsed_s: float, ok: bool) -> None:
        self.total_time_s += elapsed_s
        if ok:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1

    def as_dict(self) -> Dict[str, Any]:
        return {
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "total_time_s": round(self.total_time_s, 3),
        }


class FactoryAgent:
    """A real specialist agent instance produced from an `AgentBlueprint`.

    Instances are cheap to create and are meant to be reused by an
    `AgentPool` across many tasks; they carry no per-task state between
    calls to `execute()`.
    """

    __slots__ = ("id", "blueprint", "status", "stats", "created_at", "_llm")

    def __init__(self, blueprint: AgentBlueprint, *, llm: Optional[Any] = None) -> None:
        self.id: int = next(_id_counter)
        self.blueprint = blueprint
        self.status = "idle"
        self.stats = AgentStats()
        self.created_at = time.time()
        self._llm = llm  # injected for testing; defaults to the shared LLM client

    @property
    def specialization(self) -> str:
        return self.blueprint.specialization

    @property
    def name(self) -> str:
        return f"{self.blueprint.specialization}#{self.id}"

    def _get_llm(self) -> Any:
        if self._llm is not None:
            return self._llm
        from agent_civilization.core.llm import get_llm

        return get_llm()

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one task: optional real tool, then real LLM reasoning.

        `task` = {"prompt": str, "data": Any (optional)}.
        Returns the same outcome envelope shape used across the
        civilization: {"ok", "agent", "specialization", "elapsed_s", "result"}.
        """
        prompt = str(task.get("prompt") or task.get("description") or "").strip()
        data = task.get("data")
        started = time.time()
        self.status = "working"

        tool_output: Optional[Dict[str, Any]] = None
        try:
            if self.blueprint.tool is not None:
                tool_output = await self.blueprint.tool(data)
                if tool_output:
                    prompt = f"{prompt}\n\nReal tool output:\n{tool_output}" if prompt else str(tool_output)

            if not prompt:
                elapsed = time.time() - started
                self.stats.record(elapsed, ok=tool_output is not None)
                self.status = "idle"
                return self._envelope(ok=tool_output is not None, elapsed=elapsed,
                                       result={"tool_output": tool_output, "answer": None,
                                               "note": "empty prompt"})

            llm = self._get_llm()
            llm_result = await llm.complete(self.blueprint.system_prompt, prompt)
            ok = bool(llm_result.get("ok"))
            result: Dict[str, Any] = {"answer": llm_result.get("content") if ok else None}
            if tool_output:
                result["tool_output"] = tool_output
            if not ok:
                result["llm_error"] = llm_result.get("error")
            result["model"] = llm_result.get("model")

            elapsed = time.time() - started
            self.stats.record(elapsed, ok=ok or tool_output is not None)
            self.status = "idle"
            return self._envelope(ok=ok or tool_output is not None, elapsed=elapsed, result=result)

        except Exception as exc:  # noqa: BLE001 - surfaced in the outcome, not swallowed
            elapsed = time.time() - started
            self.stats.record(elapsed, ok=False)
            self.status = "idle"
            logger.exception("agent %s failed on task", self.name)
            return self._envelope(ok=False, elapsed=elapsed, result={"error": str(exc)})

    def _envelope(self, *, ok: bool, elapsed: float, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ok": ok,
            "agent": self.name,
            "specialization": self.specialization,
            "elapsed_s": round(elapsed, 3),
            "result": result,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "status": self.status,
            "stats": self.stats.as_dict(),
        }

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<FactoryAgent {self.name} status={self.status}>"
