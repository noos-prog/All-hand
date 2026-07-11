#!/usr/bin/env python3
"""
Agent blueprints — the single source of truth for what a specialization IS.

A Blueprint is NOT an agent. It never runs, holds no state, and consumes no
resources beyond a few attributes in memory. `AgentFactory` stamps out real,
ephemeral `FactoryAgent` instances from a Blueprint whenever the civilization
needs one — that indirection is what lets a handful of Blueprints back
millions of agent executions without a million objects ever coexisting.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

logger = logging.getLogger("agos_factory.blueprint")

# A tool is an optional real side-effect the agent performs before reasoning,
# e.g. a live web search or a statistics computation. It receives the raw
# task payload (`data`) and returns a JSON-serializable dict, or None if it
# has nothing to contribute for this particular task.
ToolFn = Callable[[Optional[Any]], Awaitable[Optional[Dict[str, Any]]]]


@dataclass(frozen=True)
class AgentBlueprint:
    """Immutable definition of one agent specialization.

    Attributes:
        specialization: Canonical name, e.g. "analyst", "researcher".
        system_prompt: The LLM system prompt that defines this specialist's
            behavior. Reused verbatim by every ephemeral agent of this kind.
        tool: Optional real tool invoked before the LLM reasoning phase.
        max_concurrency: Hard cap on simultaneously *executing* agents of
            this specialization inside a single `AgentPool`. This is the
            real resource boundary — not the number of agents ever spawned.
        idle_ttl_s: How long an idle pooled agent may sit before the pool is
            allowed to let it go (informational; enforced by `AgentPool`).
        cost_weight: Relative resource cost used by the autoscaler to trade
            off specializations against each other under global limits.
        tags: Free-form labels (e.g. ("io-bound",), ("cpu-bound",)) that
            autoscaling policies or dashboards may use to group blueprints.
    """

    specialization: str
    system_prompt: str
    tool: Optional[ToolFn] = None
    max_concurrency: int = 50
    idle_ttl_s: float = 30.0
    cost_weight: float = 1.0
    tags: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.specialization:
            raise ValueError("AgentBlueprint.specialization must be non-empty")
        if not self.system_prompt:
            raise ValueError(f"AgentBlueprint({self.specialization!r}) requires a system_prompt")
        if self.max_concurrency <= 0:
            raise ValueError(f"AgentBlueprint({self.specialization!r}).max_concurrency must be > 0")
        if self.cost_weight <= 0:
            raise ValueError(f"AgentBlueprint({self.specialization!r}).cost_weight must be > 0")


class BlueprintRegistry:
    """In-memory registry of every specialization the civilization knows.

    This is deliberately a plain dict-backed registry (no database, no
    files-per-agent) — a civilization with a million agents still only has
    as many blueprints as it has *specializations*, typically a few dozen.
    """

    def __init__(self) -> None:
        self._blueprints: Dict[str, AgentBlueprint] = {}

    def register(self, blueprint: AgentBlueprint, *, replace: bool = False) -> None:
        """Register a blueprint. Raises if the name exists unless replace=True."""
        if not replace and blueprint.specialization in self._blueprints:
            raise ValueError(
                f"blueprint '{blueprint.specialization}' already registered "
                f"(pass replace=True to override)"
            )
        self._blueprints[blueprint.specialization] = blueprint
        logger.info("registered blueprint '%s' (max_concurrency=%d)",
                    blueprint.specialization, blueprint.max_concurrency)

    def unregister(self, specialization: str) -> None:
        self._blueprints.pop(specialization, None)

    def get(self, specialization: str) -> AgentBlueprint:
        try:
            return self._blueprints[specialization]
        except KeyError:
            raise KeyError(
                f"unknown specialization '{specialization}'. "
                f"known: {sorted(self._blueprints)}"
            ) from None

    def __contains__(self, specialization: str) -> bool:
        return specialization in self._blueprints

    def all(self) -> Dict[str, AgentBlueprint]:
        return dict(self._blueprints)

    def names(self) -> Tuple[str, ...]:
        return tuple(self._blueprints.keys())

    @classmethod
    def from_agent_civilization(cls, *, max_concurrency: int = 50) -> "BlueprintRegistry":
        """Build a registry from the civilization's real specializations.

        Imports `SPECIALIZATIONS` and `SPECIALIZATION_TOOLS` from
        `agent_civilization.agents.real.real_agents` — the same source of
        truth `server.py` uses — so factory-spawned agents share their
        system prompts and real tools with the rest of the civilization
        instead of duplicating them.
        """
        from agent_civilization.agents.real import real_agents as _real

        registry = cls()
        tool_map: Dict[str, ToolFn] = _build_tool_adapters(_real)
        for specialization, system_prompt in _real.SPECIALIZATIONS.items():
            tool_name = _real.SPECIALIZATION_TOOLS.get(specialization)
            registry.register(
                AgentBlueprint(
                    specialization=specialization,
                    system_prompt=system_prompt,
                    tool=tool_map.get(tool_name) if tool_name else None,
                    max_concurrency=max_concurrency,
                    tags=("real-tool",) if tool_name else (),
                )
            )
        return registry


def _build_tool_adapters(real_agents_module: Any) -> Dict[str, ToolFn]:
    """Adapt the civilization's standalone tool functions to the `ToolFn` shape.

    `real_agents.py` exposes plain functions with heterogeneous signatures
    (`web_search(query, max_results)`, `compute_statistics(data)`, ...). This
    wraps each one behind the uniform `async def tool(data) -> dict | None`
    contract that `FactoryAgent` expects, without modifying the originals.
    """
    import asyncio

    async def _web_search(data: Optional[Any]) -> Optional[Dict[str, Any]]:
        query = data if isinstance(data, str) and data.strip() else None
        if not query:
            return None
        results = await real_agents_module.web_search(query)
        return {"tool": "web_search", "results": results}

    async def _compute_statistics(data: Optional[Any]) -> Optional[Dict[str, Any]]:
        if data is None:
            return None
        stats = await asyncio.to_thread(real_agents_module.compute_statistics, data)
        return {"tool": "compute_statistics", "stats": stats}

    async def _run_python_code(data: Optional[Any]) -> Optional[Dict[str, Any]]:
        if not isinstance(data, str) or not data.strip():
            return None
        execution = await asyncio.to_thread(real_agents_module.run_python_code, data)
        return {"tool": "run_python_code", "execution": execution}

    async def _validate_json(data: Optional[Any]) -> Optional[Dict[str, Any]]:
        if not isinstance(data, str) or not data.strip():
            return None
        validation = real_agents_module.validate_json(data)
        return {"tool": "validate_json", "validation": validation}

    async def _system_metrics(_data: Optional[Any]) -> Optional[Dict[str, Any]]:
        metrics = real_agents_module.system_metrics()
        return {"tool": "system_metrics", "metrics": metrics}

    return {
        "web_search": _web_search,
        "compute_statistics": _compute_statistics,
        "run_python_code": _run_python_code,
        "validate_json": _validate_json,
        "system_metrics": _system_metrics,
    }
