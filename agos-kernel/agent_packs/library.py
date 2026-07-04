"""AGOS Agent Packs Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentPackMetadata:
    """Agent pack metadata."""
    id: str
    name: str
    provider: str
    version: str = "1.0.0"
    description: str = ""


class AgentPack:
    """An AI agent pack."""
    
    def __init__(self, name: str, provider: str, description: str = ""):
        self.metadata = AgentPackMetadata(
            id=f"agent-{uuid.uuid4().hex[:8]}",
            name=name,
            provider=provider,
            description=description,
        )
        self.capabilities: List[str] = []
        self.benchmark_profile: Dict[str, float] = {}
        self.supports_streaming = False
        self.supports_cancellation = False


# Agent Packs
AGENT_PACKS = {
    # OpenAI
    "openai": AgentPack("OpenAI Agent", "OpenAI", "OpenAI ChatGPT Agent"),
    
    # Anthropic
    "anthropic": AgentPack("Claude Agent", "Anthropic", "Anthropic Claude Agent"),
    
    # Google
    "gemini": AgentPack("Gemini Agent", "Google", "Google Gemini Agent"),
    
    # Chinese AI
    "deepseek": AgentPack("DeepSeek Agent", "DeepSeek", "DeepSeek Agent"),
    "qwen": AgentPack("Qwen Agent", "Alibaba", "Qwen Agent"),
    
    # Local AI
    "ollama": AgentPack("Ollama Agent", "Ollama", "Ollama Local Agent"),
    "lmstudio": AgentPack("LM Studio Agent", "LM Studio", "LM Studio Local Agent"),
    
    # Router
    "openrouter": AgentPack("OpenRouter Agent", "OpenRouter", "OpenRouter Multi-Provider Agent"),
    
    # Cloud AI
    "azure_ai": AgentPack("Azure AI Agent", "Microsoft", "Azure AI Agent"),
    "aws_bedrock": AgentPack("AWS Bedrock Agent", "Amazon", "AWS Bedrock Agent"),
    
    # IDE Agents
    "copilot": AgentPack("GitHub Copilot", "GitHub", "GitHub Copilot Agent"),
    "cursor": AgentPack("Cursor Agent", "Cursor", "Cursor AI Agent"),
    "claude_code": AgentPack("Claude Code", "Anthropic", "Claude Code CLI Agent"),
    "codex": AgentPack("Codex Agent", "OpenAI", "OpenAI Codex Agent"),
    "aider": AgentPack("Aider Agent", "Aider", "Aider CLI Agent"),
    "continue": AgentPack("Continue Agent", "Continue", "Continue VSCode Agent"),
    "cline": AgentPack("Cline Agent", "Cline", "Cline VSCode Agent"),
    "roocode": AgentPack("Roo Code", "Roo", "Roo Code Agent"),
    "openhands": AgentPack("OpenHands Agent", "OpenHands", "OpenHands Agent"),
    "goose": AgentPack("Goose Agent", "Ex Labs", "Goose CLI Agent"),
    "warp": AgentPack("Warp Agent", "Warp", "Warp Terminal AI"),
    "windsurf": AgentPack("Windsurf Agent", "Codeium", "Windsurf AI Agent"),
    "replit": AgentPack("Replit Agent", "Replit", "Replit AI Agent"),
    
    # No-Code/Low-Code
    "firebase_studio": AgentPack("Firebase Studio Agent", "Google", "Firebase Studio Agent"),
    "bolt": AgentPack("Bolt Agent", "StackBlitz", "Bolt.new AI Agent"),
    "lovable": AgentPack("Lovable Agent", "Lovable", "Lovable AI Agent"),
    "v0": AgentPack("v0 Agent", "Vercel", "v0.dev Agent"),
    "manus": AgentPack("Manus Agent", "Manus", "Manus AI Agent"),
    
    # Multi-Agent
    "autogen": AgentPack("AutoGen Agent", "Microsoft", "Microsoft AutoGen Multi-Agent"),
    "crewai": AgentPack("CrewAI Agent", "CrewAI", "CrewAI Multi-Agent"),
    "langgraph": AgentPack("LangGraph Agent", "LangChain", "LangGraph Multi-Agent"),
    "mastra": AgentPack("Mastra Agent", "Mastra", "Mastra AI Agent"),
    "semantic_kernel": AgentPack("Semantic Kernel", "Microsoft", "Microsoft Semantic Kernel"),
    
    # Interpreters
    "open_interpreter": AgentPack("Open Interpreter", "Open Interpreter", "Local Code Interpreter"),
    "browser_use": AgentPack("Browser Use Agent", "Browser Use", "Browser Automation Agent"),
    
    # Browser Automation
    "playwright_agent": AgentPack("Playwright Agent", "Playwright", "Playwright Browser Agent"),
    "puppeteer_agent": AgentPack("Puppeteer Agent", "Puppeteer", "Puppeteer Browser Agent"),
    "selenium_agent": AgentPack("Selenium Agent", "Selenium", "Selenium Browser Agent"),
    
    # Workflow Automation
    "n8n": AgentPack("n8n Agent", "n8n", "n8n Workflow Agent"),
    "flowise": AgentPack("Flowise Agent", "Flowise", "Flowise LLM Flow Agent"),
    "dify": AgentPack("Dify Agent", "Dify", "Dify LLM App Agent"),
    
    # Chat UIs
    "anythingllm": AgentPack("AnythingLLM Agent", "AnythingLLM", "AnythingLLM Chat Agent"),
    "open_webui": AgentPack("Open WebUI Agent", "Open WebUI", "Open WebUI Agent"),
    "librechat": AgentPack("LibreChat Agent", "LibreChat", "LibreChat Agent"),
    
    # SDK & Infrastructure
    "mcp": AgentPack("MCP Native Agent", "MCP", "Model Context Protocol Agent"),
    "local_cli": AgentPack("Local CLI Agent", "CLI", "Local CLI Execution Agent"),
    "remote_ssh": AgentPack("Remote SSH Agent", "SSH", "Remote SSH Execution Agent"),
    "container_agent": AgentPack("Container Agent", "Docker", "Container Execution Agent"),
    "browser_agent": AgentPack("Browser Agent", "Browser", "Browser Control Agent"),
    "custom_sdk": AgentPack("Custom SDK Agent", "SDK", "Custom SDK Agent"),
}


class AgentPackLibrary:
    """Library of agent packs."""
    
    def __init__(self):
        self.packs = AGENT_PACKS
    
    def get(self, name: str) -> AgentPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[AgentPack]:
        return list(self.packs.values())
    
    def negotiate_capability(self, agent_name: str, capability: str) -> Dict:
        """Negotiate capability with agent."""
        agent = self.packs.get(agent_name)
        if not agent:
            return {"supported": False}
        return {"supported": capability in agent.capabilities}


_library = AgentPackLibrary()


def get_library() -> AgentPackLibrary:
    return _library