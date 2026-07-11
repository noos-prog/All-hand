#!/usr/bin/env python3
"""
Command-line demo for the agent factory.

Runs a real batch of tasks through `AgentFactory.spawn_batch()` and prints
live throughput + the final metrics snapshot. Requires `OPENROUTER_API_KEY`
to get real LLM answers; without it, tasks still execute and report the
civilization's standard "LLM not configured" error via the outcome envelope
(the factory never fabricates a fake success).

Usage:
    python -m agos_factory.factory.cli demo --spec analyst --count 200 --concurrency 20
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time


def _add_repo_root_to_path() -> None:
    """Allow `agent_civilization` imports when run from inside agos-factory/."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


_add_repo_root_to_path()

from factory.blueprint import BlueprintRegistry  # noqa: E402
from factory.factory import AgentFactory  # noqa: E402


async def _run_demo(specialization: str, count: int, concurrency: int) -> None:
    registry = BlueprintRegistry.from_agent_civilization(max_concurrency=concurrency)
    if specialization not in registry:
        print(f"unknown specialization '{specialization}'. known: {registry.names()}", file=sys.stderr)
        sys.exit(1)

    factory = AgentFactory(registry)
    await factory.start_autoscaling()

    prompts = (f"[demo task {i}] give a one-sentence status update" for i in range(count))

    started = time.time()
    completed = 0
    failed = 0
    async for outcome in factory.spawn_batch(specialization, prompts, concurrency=concurrency):
        completed += 1 if outcome.get("ok") else 0
        failed += 0 if outcome.get("ok") else 1
        if (completed + failed) % max(1, count // 10) == 0:
            elapsed = time.time() - started
            print(f"progress: {completed + failed}/{count} tasks "
                  f"({(completed + failed) / elapsed:.1f} tasks/s)", file=sys.stderr)

    elapsed = time.time() - started
    print(json.dumps({
        "specialization": specialization,
        "requested": count,
        "completed": completed,
        "failed": failed,
        "elapsed_s": round(elapsed, 3),
        "throughput_tasks_per_s": round(count / elapsed, 2) if elapsed > 0 else None,
        "factory_snapshot": await factory.snapshot(),
    }, indent=2, ensure_ascii=False))

    await factory.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="AGOS Agent Factory demo")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="run a real batch of tasks through the factory")
    demo.add_argument("--spec", required=True, help="specialization name, e.g. analyst")
    demo.add_argument("--count", type=int, default=100, help="number of tasks to run")
    demo.add_argument("--concurrency", type=int, default=20, help="max concurrent agents")

    args = parser.parse_args()
    if args.command == "demo":
        asyncio.run(_run_demo(args.spec, args.count, args.concurrency))


if __name__ == "__main__":
    main()
