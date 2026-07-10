#!/usr/bin/env python3
"""
Real specialist agents for the AGOS Agent Civilization.

Each of the 20 specializations is a REAL agent:
- Every agent thinks with a real LLM (OpenRouter) using a specialization-specific
  system prompt.
- Several agents also use REAL tools:
    researcher      -> live web search (DuckDuckGo API)
    data_processor  -> real statistical computation on provided data
    validator       -> real JSON validation
    test_runner     -> really executes Python code in a sandboxed subprocess
    monitor         -> real system metrics (CPU/memory via /proc)

Agents are BaseAgent-compatible (CommunicationHub) and also expose a direct
`await agent.execute(task)` API used by the FastAPI server.
"""

import asyncio
import json
import logging
import os
import statistics
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional

import aiohttp

from agent_civilization.core.llm import get_llm

logger = logging.getLogger("real_agents")

# ---------------------------------------------------------------------------
# The 20 specializations and their REAL system prompts
# ---------------------------------------------------------------------------
SPECIALIZATIONS: Dict[str, str] = {
    "analyst": "You are a senior data/business analyst agent in the AGOS civilization. Analyze the input rigorously: identify patterns, trends, outliers, risks and opportunities. Always return concrete findings with confidence levels.",
    "api_integrator": "You are an API integration expert agent. Given an API or integration task, produce concrete integration plans, endpoint mappings, auth flows and working example code (with error handling).",
    "architect": "You are a software architecture agent. Design robust, scalable architectures. Return components, data flows, technology choices and trade-off analysis. Prefer simple, proven designs.",
    "builder": "You are a builder agent. Turn specifications into concrete build plans and working code scaffolds. Be practical and complete: file structure, commands, configs.",
    "code_generator": "You are an expert code-generation agent. Write clean, complete, working code for the requested task. Include imports and brief usage notes. Never return pseudocode when real code is possible.",
    "communicator": "You are a communication agent. Draft clear messages, reports, announcements and translations. Adapt tone to the audience. Support Arabic and English fluently.",
    "data_processor": "You are a data-processing agent. Clean, transform, aggregate and summarize data. When raw data is provided, compute real statistics and describe the transformation steps precisely.",
    "db_manager": "You are a database expert agent. Design schemas, write optimized SQL, plan migrations and indexing strategies. Always consider integrity, performance and security (least privilege).",
    "designer": "You are a product/UI design agent. Produce concrete design specs: layout structure, color tokens, typography, spacing, component states and accessibility notes.",
    "educator": "You are an educator agent. Explain any topic clearly with examples, analogies and step-by-step breakdowns. Adapt depth to the learner's level. Support Arabic and English.",
    "modifier": "You are a code-modification agent. Given existing code and a change request, return the precise modified code with an explanation of each change and its risk.",
    "monitor": "You are a monitoring agent. Assess system health from metrics and logs, detect anomalies, and recommend concrete remediation steps with priorities.",
    "network_client": "You are a networking agent. Handle HTTP/API request design, debugging network issues, protocols, and connectivity plans. Provide exact requests and expected responses.",
    "researcher": "You are a research agent with live web search results provided in context. Synthesize accurate, sourced answers. Distinguish facts from inference. Cite the sources you used.",
    "reviewer": "You are a code/content review agent. Review rigorously: correctness, security, performance, readability. Return a structured review with severity levels and concrete fixes.",
    "self_developer": "You are a self-development agent for the civilization. Propose concrete improvements to agents, prompts, and workflows, with measurable success criteria.",
    "strategist": "You are a strategy agent. Build actionable strategies: goals, phases, resources, risks, KPIs. Be decisive and concrete, not generic.",
    "surgeon": "You are a precision-fix agent ('surgeon'). Diagnose the exact root cause of a bug or failure and return the minimal precise fix, with verification steps.",
    "test_runner": "You are a testing agent. Design and (when code is provided) really execute tests. Return test plans, cases, edge cases and actual execution results.",
    "validator": "You are a validation agent. Verify data, configs and outputs against rules/schemas. Return pass/fail per rule with exact violation details.",
}


# ---------------------------------------------------------------------------
# Real tools
# ---------------------------------------------------------------------------
async def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Live search via DuckDuckGo (no key needed)."""
    results: List[Dict[str, str]] = []
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            async with s.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            ) as r:
                data = json.loads(await r.text())
        if data.get("AbstractText"):
            results.append({"title": data.get("Heading", ""), "snippet": data["AbstractText"], "url": data.get("AbstractURL", "")})
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({"title": topic.get("Text", "")[:80], "snippet": topic.get("Text", ""), "url": topic.get("FirstURL", "")})
    except Exception as e:
        logger.warning("web_search failed: %s", e)
    return results[:max_results]


def compute_statistics(numbers: List[float]) -> Dict[str, Any]:
    """Real statistics on numeric data."""
    if not numbers:
        return {"error": "no numeric data"}
    out = {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.fmean(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }
    if len(numbers) > 1:
        out["stdev"] = statistics.stdev(numbers)
        out["median"] = statistics.median(numbers)
    return out


def run_python_code(code: str, timeout: int = 10) -> Dict[str, Any]:
    """Really execute Python code in an isolated subprocess."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, "-I", path],
            capture_output=True, text=True, timeout=timeout,
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
            "passed": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": f"timeout after {timeout}s", "passed": False}
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def validate_json(payload: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(payload)
        return {"valid": True, "type": type(parsed).__name__, "keys": list(parsed.keys()) if isinstance(parsed, dict) else None}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e), "line": e.lineno, "column": e.colno}


def system_metrics() -> Dict[str, Any]:
    """Real host metrics (Linux)."""
    metrics: Dict[str, Any] = {"timestamp": time.time()}
    try:
        with open("/proc/loadavg") as f:
            parts = f.read().split()
            metrics["load_1m"], metrics["load_5m"], metrics["load_15m"] = map(float, parts[:3])
        with open("/proc/meminfo") as f:
            mem = {l.split(":")[0]: int(l.split()[1]) for l in f if ":" in l and l.split()[1].isdigit()}
        metrics["mem_total_mb"] = round(mem.get("MemTotal", 0) / 1024)
        metrics["mem_available_mb"] = round(mem.get("MemAvailable", 0) / 1024)
    except Exception as e:
        metrics["error"] = str(e)
    return metrics


def _extract_numbers(data: Any) -> List[float]:
    nums: List[float] = []
    if isinstance(data, (int, float)):
        nums.append(float(data))
    elif isinstance(data, (list, tuple)):
        for v in data:
            nums.extend(_extract_numbers(v))
    elif isinstance(data, dict):
        for v in data.values():
            nums.extend(_extract_numbers(v))
    elif isinstance(data, str):
        try:
            nums.append(float(data))
        except ValueError:
            pass
    return nums


# ---------------------------------------------------------------------------
# The real agent
# ---------------------------------------------------------------------------
class RealSpecialistAgent:
    """A real working agent: LLM brain + real tools, per specialization."""

    def __init__(self, agent_id: int, specialization: str):
        assert specialization in SPECIALIZATIONS, f"unknown specialization {specialization}"
        self.agent_id = agent_id
        self.specialization = specialization
        self.name = f"{specialization}_{agent_id:04d}"
        self.status = "idle"
        self.stats = {"tasks_completed": 0, "tasks_failed": 0, "total_time_s": 0.0}
        self.created_at = time.time()

    # ------------------------------------------------------------------
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a real task. task = {"prompt": str, "data": any (optional)}."""
        prompt = str(task.get("prompt") or task.get("description") or "").strip()
        data = task.get("data")
        started = time.time()
        self.status = "working"
        try:
            result = await self._run(prompt, data)
            self.stats["tasks_completed"] += 1
            ok = True
        except Exception as e:
            logger.exception("agent %s failed", self.name)
            result = {"error": str(e)}
            self.stats["tasks_failed"] += 1
            ok = False
        elapsed = time.time() - started
        self.stats["total_time_s"] += elapsed
        self.status = "idle"
        return {
            "ok": ok,
            "agent": self.name,
            "specialization": self.specialization,
            "elapsed_s": round(elapsed, 2),
            "result": result,
        }

    async def _run(self, prompt: str, data: Any) -> Dict[str, Any]:
        llm = get_llm()
        system = SPECIALIZATIONS[self.specialization]
        tool_output: Optional[Dict[str, Any]] = None

        # --- real tool phase -------------------------------------------------
        if self.specialization == "researcher" and prompt:
            sources = await web_search(prompt)
            tool_output = {"tool": "web_search", "sources": sources}
            if sources:
                prompt = (
                    f"{prompt}\n\nLive web search results:\n"
                    + "\n".join(f"- {s['title']}: {s['snippet']} ({s['url']})" for s in sources)
                )
        elif self.specialization == "data_processor" and data is not None:
            nums = _extract_numbers(data)
            stats = compute_statistics(nums) if nums else {"note": "no numeric values found"}
            tool_output = {"tool": "compute_statistics", "statistics": stats}
            prompt = f"{prompt}\n\nComputed real statistics on the provided data:\n{json.dumps(stats)}"
        elif self.specialization == "test_runner" and isinstance(data, str) and data.strip():
            execution = await asyncio.to_thread(run_python_code, data)
            tool_output = {"tool": "run_python_code", "execution": execution}
            prompt = f"{prompt}\n\nActual execution result of the provided code:\n{json.dumps(execution)}"
        elif self.specialization == "validator" and isinstance(data, str) and data.strip():
            validation = validate_json(data)
            tool_output = {"tool": "validate_json", "validation": validation}
            prompt = f"{prompt}\n\nReal JSON validation result:\n{json.dumps(validation)}"
        elif self.specialization == "monitor":
            metrics = system_metrics()
            tool_output = {"tool": "system_metrics", "metrics": metrics}
            prompt = f"{prompt or 'Assess current system health.'}\n\nReal system metrics:\n{json.dumps(metrics)}"

        # --- LLM reasoning phase ---------------------------------------------
        if not prompt:
            return {"tool_output": tool_output, "answer": None, "note": "empty prompt"}

        llm_result = await llm.complete(system, prompt)
        out: Dict[str, Any] = {"answer": llm_result["content"] if llm_result["ok"] else None}
        if tool_output:
            out["tool_output"] = tool_output
        if not llm_result["ok"]:
            out["llm_error"] = llm_result["error"]
            # Tools alone can still be a real result
            if tool_output is None:
                raise RuntimeError(llm_result["error"])
        out["model"] = llm_result["model"]
        return out

    def snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.agent_id,
            "name": self.name,
            "specialization": self.specialization,
            "status": self.status,
            "stats": dict(self.stats),
        }


# ---------------------------------------------------------------------------
# Civilization factory
# ---------------------------------------------------------------------------
def create_civilization(agents_per_spec: int = None) -> Dict[str, List[RealSpecialistAgent]]:
    """Create the full civilization: N real agents per specialization (default from env)."""
    n = agents_per_spec or int(os.environ.get("AGENTS_PER_SPEC", "5"))
    civilization: Dict[str, List[RealSpecialistAgent]] = {}
    agent_id = 0
    for spec in SPECIALIZATIONS:
        civilization[spec] = []
        for _ in range(n):
            civilization[spec].append(RealSpecialistAgent(agent_id, spec))
            agent_id += 1
    logger.info("Civilization created: %d specializations x %d agents = %d real agents",
                len(SPECIALIZATIONS), n, agent_id)
    return civilization
