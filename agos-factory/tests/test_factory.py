#!/usr/bin/env python3
"""
Real, executable tests for the agent factory (blueprint, agent, pool,
autoscaler, factory) using a fake LLM so the suite runs without network
access or an OPENROUTER_API_KEY — the factory logic itself is what's under
test, not the civilization's LLM provider.

Run with:
    python -m pytest agos-factory/tests/test_factory.py -q
or, dependency-free:
    python agos-factory/tests/test_factory.py
"""

from __future__ import annotations

import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from factory.agent import FactoryAgent  # noqa: E402
from factory.autoscaler import Autoscaler, AutoscalerPolicy  # noqa: E402
from factory.blueprint import AgentBlueprint, BlueprintRegistry  # noqa: E402
from factory.factory import AgentFactory  # noqa: E402
from factory.metrics import FactoryMetrics  # noqa: E402
from factory.pool import AgentPool  # noqa: E402


class _FakeLLM:
    """Deterministic stand-in for `agent_civilization.core.llm.get_llm()`."""

    def __init__(self, *, delay_s: float = 0.0, fail: bool = False) -> None:
        self._delay_s = delay_s
        self._fail = fail
        self.calls = 0

    async def complete(self, system: str, prompt: str) -> dict:
        self.calls += 1
        if self._delay_s:
            await asyncio.sleep(self._delay_s)
        if self._fail:
            return {"ok": False, "error": "simulated failure", "model": "fake/test-model"}
        return {"ok": True, "content": f"echo: {prompt}", "model": "fake/test-model"}


def _make_registry(*, max_concurrency: int = 5, fail: bool = False, delay_s: float = 0.0) -> BlueprintRegistry:
    registry = BlueprintRegistry()
    registry.register(AgentBlueprint(
        specialization="tester",
        system_prompt="You are a test specialist.",
        max_concurrency=max_concurrency,
    ))
    return registry


def _run(coro):
    return asyncio.run(coro)


def test_blueprint_rejects_empty_prompt() -> None:
    try:
        AgentBlueprint(specialization="x", system_prompt="")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_registry_prevents_duplicate_without_replace() -> None:
    registry = _make_registry()
    try:
        registry.register(AgentBlueprint(specialization="tester", system_prompt="dup"))
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    registry.register(AgentBlueprint(specialization="tester", system_prompt="dup"), replace=True)
    assert registry.get("tester").system_prompt == "dup"


def test_factory_agent_executes_with_injected_llm() -> None:
    async def scenario():
        registry = _make_registry()
        blueprint = registry.get("tester")
        agent = FactoryAgent(blueprint, llm=_FakeLLM())
        outcome = await agent.execute({"prompt": "hello"})
        assert outcome["ok"] is True
        assert outcome["result"]["answer"] == "echo: hello"
        assert agent.stats.tasks_completed == 1
    _run(scenario())


def test_factory_agent_reports_llm_failure_without_masking_it() -> None:
    async def scenario():
        registry = _make_registry()
        blueprint = registry.get("tester")
        agent = FactoryAgent(blueprint, llm=_FakeLLM(fail=True))
        outcome = await agent.execute({"prompt": "hello"})
        assert outcome["ok"] is False
        assert outcome["result"]["llm_error"] == "simulated failure"
    _run(scenario())


def test_pool_respects_concurrency_cap() -> None:
    async def scenario():
        registry = _make_registry(max_concurrency=2)
        metrics = FactoryMetrics()
        pool = AgentPool(registry.get("tester"), metrics=metrics, llm=_FakeLLM(delay_s=0.05))

        peak = 0

        async def _tracked_run(i: int):
            nonlocal peak
            outcome = await pool.run({"prompt": f"task {i}"})
            return outcome

        tasks = [asyncio.create_task(_tracked_run(i)) for i in range(10)]
        # Sample peak active while tasks are in flight.
        await asyncio.sleep(0.02)
        peak = max(peak, pool.active)
        results = await asyncio.gather(*tasks)

        assert all(r["ok"] for r in results)
        assert peak <= 2
        snap = await metrics.snapshot()
        assert snap["by_specialization"]["tester"]["tasks_completed"] == 10
    _run(scenario())


def test_pool_recycles_idle_agents() -> None:
    async def scenario():
        registry = _make_registry(max_concurrency=3)
        metrics = FactoryMetrics()
        pool = AgentPool(registry.get("tester"), metrics=metrics, llm=_FakeLLM())

        await pool.run({"prompt": "first"})
        assert pool.idle_count == 1
        await pool.run({"prompt": "second"})
        # Second call should have reused the idle agent rather than always
        # creating a brand new one; idle count returns to 1 after release.
        assert pool.idle_count == 1
    _run(scenario())


def test_autoscaler_grows_under_saturation() -> None:
    async def scenario():
        registry = _make_registry(max_concurrency=2)
        metrics = FactoryMetrics()
        pool = AgentPool(registry.get("tester"), metrics=metrics, llm=_FakeLLM(delay_s=0.05))
        autoscaler = Autoscaler(AutoscalerPolicy(min_size=1, max_size=100, target_utilization=0.5))

        tasks = [asyncio.create_task(pool.run({"prompt": f"t{i}"})) for i in range(10)]
        await asyncio.sleep(0.01)
        new_size = await autoscaler.tick(pool)
        assert new_size > 2
        await asyncio.gather(*tasks)
    _run(scenario())


def test_factory_spawn_batch_streams_all_results() -> None:
    async def scenario():
        registry = _make_registry(max_concurrency=4)
        factory = AgentFactory(registry, llm=_FakeLLM())
        prompts = [f"q{i}" for i in range(25)]

        outcomes = []
        async for outcome in factory.spawn_batch("tester", prompts, concurrency=4):
            outcomes.append(outcome)

        assert len(outcomes) == 25
        assert all(o["ok"] for o in outcomes)
        snap = await factory.snapshot()
        assert snap["metrics"]["total_tasks_processed"] == 25
        await factory.shutdown()
    _run(scenario())


def test_factory_scale_to_changes_pool_capacity() -> None:
    async def scenario():
        registry = _make_registry(max_concurrency=5)
        factory = AgentFactory(registry, llm=_FakeLLM())
        await factory.run("tester", {"prompt": "warm up"})
        await factory.scale_to("tester", 50)
        snap = await factory.snapshot()
        assert snap["pools"]["tester"]["max_concurrency"] == 50
        await factory.shutdown()
    _run(scenario())


def _run_all() -> None:
    failures = 0
    tests = [obj for name, obj in globals().items() if name.startswith("test_") and callable(obj)]
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001 - test runner surfaces every failure
            failures += 1
            print(f"FAIL {test.__name__}: {exc}")
    if failures:
        raise SystemExit(f"{failures} test(s) failed")
    print(f"all {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
