"""AI Stack Detector - Detects AI/ML frameworks and providers."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from rie.detectors import DetectorContext, DetectorResult, IDetector


@dataclass
class AIStackFeatureSet:
    """Detected AI stack."""
    llm_frameworks: List[str] = field(default_factory=list)
    model_providers: List[str] = field(default_factory=list)
    inference_libraries: List[str] = field(default_factory=list)
    prompt_frameworks: List[str] = field(default_factory=list)
    embedding_libraries: List[str] = field(default_factory=list)
    vector_databases: List[str] = field(default_factory=list)
    inference_servers: List[str] = field(default_factory=list)
    ai_sdks: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "llm_frameworks": self.llm_frameworks,
            "model_providers": self.model_providers,
            "inference_libraries": self.inference_libraries,
            "prompt_frameworks": self.prompt_frameworks,
            "embedding_libraries": self.embedding_libraries,
            "vector_databases": self.vector_databases,
            "inference_servers": self.inference_servers,
            "ai_sdks": self.ai_sdks,
            "agents": self.agents
        }


class AIStackDetector(IDetector):
    """
    Detects AI/ML stack in repository.
    
    Rules:
    ✅ Evidence Based
    ✅ No Guessing
    ✅ No AI
    """
    
    # Evidence patterns for AI technologies
    PATTERNS = {
        # LLM Frameworks
        "LangChain": {
            "files": ["langchain", "langchain_core", "langchain_community"],
            "imports": ["from langchain", "import langchain"],
            "indicators": ["langchain.dll", "langchain.version"]
        },
        "LlamaIndex": {
            "files": ["llama_index", "llamaindex"],
            "imports": ["from llama_index", "import llama_index"],
            "indicators": []
        },
        "Haystack": {
            "files": ["haystack"],
            "imports": ["from haystack", "import haystack"],
            "indicators": []
        },
        "CrewAI": {
            "files": ["crewai", "crew_ai"],
            "imports": ["from crewai", "import crewai"],
            "indicators": []
        },
        "AutoGen": {
            "files": ["autogen"],
            "imports": ["from autogen", "import autogen"],
            "indicators": []
        },
        "OpenHands": {
            "files": ["openhands"],
            "imports": ["from openhands", "import openhands"],
            "indicators": []
        },
        
        # Model Providers
        "OpenAI": {
            "files": [],
            "imports": ["from openai", "import openai"],
            "indicators": ["openai.api_key"]
        },
        "Anthropic": {
            "files": [],
            "imports": ["from anthropic", "import anthropic"],
            "indicators": ["anthropic.api_key"]
        },
        "Google AI": {
            "files": [],
            "imports": ["from google import genai", "import google.ai.generativelanguage"],
            "indicators": ["google.generativeai", "gemini"]
        },
        "DeepSeek": {
            "files": [],
            "imports": ["from deepseek"],
            "indicators": ["deepseek.api_key"]
        },
        "Qwen": {
            "files": [],
            "imports": ["from dashscope"],
            "indicators": ["qwen", "dashscope"]
        },
        "Mistral": {
            "files": [],
            "imports": ["from mistralai", "import mistralai"],
            "indicators": ["mistral.ai"]
        },
        "Ollama": {
            "files": [],
            "imports": ["from ollama", "import ollama"],
            "indicators": ["ollama.base_url"]
        },
        
        # Inference Libraries
        "LiteLLM": {
            "files": [],
            "imports": ["from litellm", "import litellm"],
            "indicators": []
        },
        "OpenRouter": {
            "files": [],
            "imports": ["from openrouter", "import openrouter"],
            "indicators": ["openrouter.ai"]
        },
        
        # Vector Databases
        "Pinecone": {
            "files": [],
            "imports": ["from pinecone", "import pinecone"],
            "indicators": ["pinecone.api_key"]
        },
        "Weaviate": {
            "files": [],
            "imports": ["import weaviate", "from weaviate"],
            "indicators": ["weaviate.client"]
        },
        "Chroma": {
            "files": [],
            "imports": ["import chromadb", "from chromadb"],
            "indicators": ["chromadb.client"]
        },
        "Qdrant": {
            "files": [],
            "imports": ["from qdrant_client", "import qdrant_client"],
            "indicators": []
        },
        "Milvus": {
            "files": [],
            "imports": ["from pymilvus", "import pymilvus"],
            "indicators": []
        },
        "FAISS": {
            "files": [],
            "imports": ["import faiss", "from faiss"],
            "indicators": []
        },
        
        # Embedding Libraries
        "sentence-transformers": {
            "files": [],
            "imports": ["from sentence_transformers", "import sentence_transformers"],
            "indicators": []
        },
        "OpenAI Embeddings": {
            "files": [],
            "imports": ["openai.embeddings"],
            "indicators": []
        },
        
        # MCP
        "MCP": {
            "files": [],
            "imports": ["from mcp", "import mcp"],
            "indicators": ["modelcontextprotocol", "mcp_server"]
        },
    }
    
    @property
    def name(self) -> str:
        return "AIStackDetector"
    
    @property
    def description(self) -> str:
        return "Detects AI/ML frameworks and providers"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        import time
        start = time.time()
        
        detected = AIStackFeatureSet()
        
        # Check each technology
        for tech_name, patterns in self.PATTERNS.items():
            if self._detect_technology(context, patterns):
                self._classify_technology(detected, tech_name)
        
        duration_ms = int((time.time() - start) * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features=detected.to_dict(),
            duration_ms=duration_ms
        )
    
    def _detect_technology(self, context: DetectorContext, patterns: Dict) -> bool:
        """Detect a technology based on evidence patterns."""
        # Check file names
        for pattern in patterns.get("files", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    return True
        
        # Check file contents
        for pattern in patterns.get("imports", []):
            for path, data in context.files.items():
                if pattern.lower() in path.lower():
                    return True
        
        # Check indicators
        for pattern in patterns.get("indicators", []):
            for path in context.files.keys():
                if pattern.lower() in path.lower():
                    return True
        
        return False
    
    def _classify_technology(self, detected: AIStackFeatureSet, tech_name: str) -> None:
        """Classify detected technology."""
        if tech_name in ["LangChain", "LlamaIndex", "Haystack", "CrewAI", "AutoGen", "OpenHands"]:
            detected.llm_frameworks.append(tech_name)
        elif tech_name in ["OpenAI", "Anthropic", "Google AI", "DeepSeek", "Qwen", "Mistral"]:
            detected.model_providers.append(tech_name)
        elif tech_name in ["LiteLLM", "OpenRouter"]:
            detected.inference_libraries.append(tech_name)
        elif tech_name in ["sentence-transformers", "OpenAI Embeddings"]:
            detected.embedding_libraries.append(tech_name)
        elif tech_name in ["Pinecone", "Weaviate", "Chroma", "Qdrant", "Milvus", "FAISS"]:
            detected.vector_databases.append(tech_name)
        elif tech_name in ["Ollama"]:
            detected.inference_servers.append(tech_name)
        elif tech_name in ["MCP"]:
            detected.ai_sdks.append(tech_name)
