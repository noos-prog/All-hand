#!/usr/bin/env python3
"""
AGOS Agent Civilization - REST API Server (FastAPI)

Wires the whole civilization together:
- 20 specializations x N real agents (LLM brains + real tools)
- External open-source agents via OpenAI-compatible HTTP adapter
- Task dispatching by specialization with async execution
- Natural-language /chat endpoint that routes commands to the right agents

Run locally:   uvicorn server:app --reload
Run on Render: uvicorn server:app --host 0.0.0.0 --port $PORT
"""

import asyncio
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent_civilization.agents.real import SPECIALIZATIONS, create_civilization
from agent_civilization.agents.external_adapter import (
    ExternalAgentAdapter,
    load_external_agents_from_env,
)
from agent_civilization.core.llm import get_llm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("server")

app = FastAPI(
    title="AGOS Agent Civilization",
    description="A real AI agent civilization: 20 specializations of working agents serving the user.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
CIVILIZATION = create_civilization()
EXTERNAL_AGENTS: List[ExternalAgentAdapter] = load_external_agents_from_env()
TASKS: Dict[str, Dict[str, Any]] = {}
STARTED_AT = time.time()
MAX_TASKS_KEPT = 500


def _all_agents():
    for agents in CIVILIZATION.values():
        yield from agents
    yield from EXTERNAL_AGENTS


def _pick_agent(specialization: str):
    """Pick the least-busy real agent of a specialization."""
    if specialization == "external" and EXTERNAL_AGENTS:
        return min(EXTERNAL_AGENTS, key=lambda a: a.stats["tasks_completed"])
    pool = CIVILIZATION.get(specialization)
    if not pool:
        raise HTTPException(404, f"Unknown specialization: {specialization}")
    idle = [a for a in pool if a.status == "idle"]
    return (idle or pool)[0]


def _prune_tasks():
    if len(TASKS) > MAX_TASKS_KEPT:
        for tid in sorted(TASKS, key=lambda t: TASKS[t]["created_at"])[: len(TASKS) - MAX_TASKS_KEPT]:
            TASKS.pop(tid, None)


async def _run_task(task_id: str, specialization: str, prompt: str, data: Any):
    agent = _pick_agent(specialization)
    TASKS[task_id]["status"] = "running"
    TASKS[task_id]["agent"] = agent.name
    outcome = await agent.execute({"prompt": prompt, "data": data})
    TASKS[task_id]["status"] = "completed" if outcome["ok"] else "failed"
    TASKS[task_id]["result"] = outcome
    TASKS[task_id]["finished_at"] = time.time()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class TaskRequest(BaseModel):
    specialization: str = Field(..., description="One of the 20 specializations, or 'external'")
    prompt: str = Field(..., min_length=1, max_length=20000)
    data: Optional[Any] = Field(None, description="Optional payload: numbers for data_processor, code for test_runner, JSON string for validator...")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=20000)


class ExternalAgentRequest(BaseModel):
    name: str
    url: str
    model: str = ""
    api_key: str = ""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "name": "AGOS Agent Civilization",
        "status": "alive",
        "specializations": list(SPECIALIZATIONS.keys()),
        "docs": "/docs",
    }


@app.get("/system/status")
async def system_status():
    agents = [a.snapshot() for a in _all_agents()]
    completed = sum(a["stats"]["tasks_completed"] for a in agents)
    failed = sum(a["stats"]["tasks_failed"] for a in agents)
    return {
        "status": "healthy",
        "uptime_s": round(time.time() - STARTED_AT),
        "llm_configured": get_llm().available,
        "llm_model": get_llm().model,
        "specializations": len(SPECIALIZATIONS),
        "total_agents": len(agents),
        "external_agents": len(EXTERNAL_AGENTS),
        "tasks_completed": completed,
        "tasks_failed": failed,
        "tasks_in_memory": len(TASKS),
    }


@app.get("/agents")
async def list_agents(specialization: Optional[str] = None):
    agents = [a.snapshot() for a in _all_agents()]
    if specialization:
        agents = [a for a in agents if a["specialization"] == specialization]
    return {"count": len(agents), "agents": agents}


@app.get("/specializations")
async def list_specializations():
    return {
        "specializations": [
            {"name": name, "description": prompt.split(".")[0], "agents": len(CIVILIZATION[name])}
            for name, prompt in SPECIALIZATIONS.items()
        ]
    }


@app.post("/tasks", status_code=202)
async def create_task(req: TaskRequest):
    if req.specialization not in SPECIALIZATIONS and req.specialization != "external":
        raise HTTPException(400, f"Unknown specialization '{req.specialization}'. Valid: {list(SPECIALIZATIONS)} + ['external']")
    task_id = uuid.uuid4().hex[:12]
    TASKS[task_id] = {
        "id": task_id,
        "specialization": req.specialization,
        "prompt": req.prompt[:500],
        "status": "queued",
        "created_at": time.time(),
        "result": None,
    }
    _prune_tasks()
    asyncio.create_task(_run_task(task_id, req.specialization, req.prompt, req.data))
    return {"task_id": task_id, "status": "queued"}


@app.get("/tasks")
async def list_tasks(limit: int = 50):
    items = sorted(TASKS.values(), key=lambda t: t["created_at"], reverse=True)[: min(limit, 200)]
    return {"count": len(items), "tasks": items}


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(404, "task not found")
    return task


ROUTER_SYSTEM = (
    "You are the dispatcher of an AI agent civilization with these specializations: "
    + ", ".join(SPECIALIZATIONS.keys())
    + ". Given a user command (in any language, including Arabic), reply with ONLY the single "
    "best specialization name from the list, nothing else."
)


@app.post("/chat")
async def chat(req: ChatRequest):
    """Natural-language command: route to the best specialist and execute."""
    llm = get_llm()
    spec = "communicator"
    if llm.available:
        routed = await llm.complete(ROUTER_SYSTEM, req.message, max_tokens=20)
        if routed["ok"]:
            candidate = routed["content"].strip().lower().replace("-", "_")
            for name in SPECIALIZATIONS:
                if name in candidate:
                    spec = name
                    break
    agent = _pick_agent(spec)
    outcome = await agent.execute({"prompt": req.message})
    return {
        "routed_to": spec,
        "agent": agent.name,
        "outcome": outcome,
    }


@app.post("/agents/external", status_code=201)
async def register_external_agent(req: ExternalAgentRequest):
    """Attach a real open-source agent (any OpenAI-compatible endpoint)."""
    if not req.url.startswith(("http://", "https://")):
        raise HTTPException(400, "url must be http(s)")
    if any(a.name == req.name for a in EXTERNAL_AGENTS):
        raise HTTPException(409, f"external agent '{req.name}' already registered")
    adapter = ExternalAgentAdapter(req.name, req.url, req.model, req.api_key)
    EXTERNAL_AGENTS.append(adapter)
    return {"registered": adapter.snapshot()}


@app.delete("/agents/external/{name}")
async def remove_external_agent(name: str):
    for i, a in enumerate(EXTERNAL_AGENTS):
        if a.name == name:
            EXTERNAL_AGENTS.pop(i)
            return {"removed": name}
    raise HTTPException(404, "external agent not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
