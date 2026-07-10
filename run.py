#!/usr/bin/env python3
"""
AGOS Agent Civilization - Direct runner (no web server).
Boots the real agent system and accepts commands from stdin.
"""

import asyncio
import logging
import signal
import sys

from agent_civilization.agents.real import SPECIALIZATIONS, create_civilization
from agent_civilization.core.llm import get_llm
from agent_civilization.agents.external_adapter import load_external_agents_from_env

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('main')


async def interactive():
    """Interactive REPL: type a prompt, get routed to the best agent."""
    civ = create_civilization(agents_per_spec=1)
    external = load_external_agents_from_env()
    llm = get_llm()

    print("\n" + "=" * 60)
    print("  AGOS Agent Civilization - Interactive Mode")
    print(f"  LLM: {'configured (' + llm.model + ')' if llm.available else 'NOT configured'}")
    print(f"  Agents: {sum(len(v) for v in civ.values()) + len(external)} across {len(SPECIALIZATIONS)} specializations")
    print("  Type 'status' for system info, 'quit' to exit")
    print("=" * 60 + "\n")

    router_prompt = (
        "You are the dispatcher of an AI agent civilization with these specializations: "
        + ", ".join(SPECIALIZATIONS.keys())
        + ". Reply with ONLY the single best specialization name, nothing else."
    )

    while True:
        try:
            user_input = await asyncio.to_thread(input, "you> ")
        except (EOFError, KeyboardInterrupt):
            break

        user_input = user_input.strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "status":
            total_completed = sum(a.stats["tasks_completed"] for agents in civ.values() for a in agents)
            total_failed = sum(a.stats["tasks_failed"] for agents in civ.values() for a in agents)
            print(f"  Tasks completed: {total_completed} | Failed: {total_failed}")
            continue

        # Route via LLM
        spec = "communicator"
        if llm.available:
            routed = await llm.complete(router_prompt, user_input, max_tokens=20)
            if routed["ok"]:
                candidate = routed["content"].strip().lower().replace("-", "_")
                for name in SPECIALIZATIONS:
                    if name in candidate:
                        spec = name
                        break

        agent = civ[spec][0] if civ.get(spec) else (external[0] if external else None)
        if not agent:
            print("  No agent available.")
            continue

        print(f"  -> routed to [{spec}] agent: {agent.name}")
        outcome = await agent.execute({"prompt": user_input})
        if outcome["ok"]:
            result = outcome.get("result", {})
            answer = result.get("answer") or result.get("error") or str(result)
            print(f"  agent> {answer}\n")
        else:
            print(f"  error> {outcome.get('result', {}).get('error', 'unknown error')}\n")

    print("\nGoodbye!")


async def main():
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            asyncio.get_running_loop().add_signal_handler(sig, lambda: asyncio.create_task(asyncio.sleep(0)))
        except NotImplementedError:
            pass

    try:
        await interactive()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    print("Starting AGOS Agent Civilization (interactive mode)...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
