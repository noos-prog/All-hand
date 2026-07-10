#!/usr/bin/env python3
"""
Real LLM client for the Agent Civilization.
Uses OpenRouter (supports free models). Reads OPENROUTER_API_KEY from env.
"""

import os
import json
import logging
import aiohttp

logger = logging.getLogger("llm")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct:free")


class LLMClient:
    """Async LLM client. One shared instance per process is fine."""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.model = model or DEFAULT_MODEL
        self._session: aiohttp.ClientSession | None = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)
            )
        return self._session

    async def complete(self, system: str, prompt: str, max_tokens: int = 1024) -> dict:
        """Return {"ok": bool, "content": str, "error": str|None, "model": str}."""
        if not self.available:
            return {
                "ok": False,
                "content": "",
                "error": "OPENROUTER_API_KEY is not configured. Set it in the environment to enable real agent intelligence.",
                "model": self.model,
            }
        try:
            session = await self._get_session()
            async with session.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/reeveero-tech/All-hand",
                    "X-Title": "AGOS Agent Civilization",
                },
                json={
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                },
            ) as resp:
                body = await resp.text()
                if resp.status != 200:
                    logger.error("LLM error %s: %s", resp.status, body[:500])
                    return {"ok": False, "content": "", "error": f"LLM HTTP {resp.status}: {body[:300]}", "model": self.model}
                data = json.loads(body)
                content = data["choices"][0]["message"]["content"]
                return {"ok": True, "content": content, "error": None, "model": data.get("model", self.model)}
        except Exception as e:
            logger.exception("LLM call failed")
            return {"ok": False, "content": "", "error": str(e), "model": self.model}

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()


_client: LLMClient | None = None


def get_llm() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
