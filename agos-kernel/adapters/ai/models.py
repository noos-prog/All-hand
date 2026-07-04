"""AI Adapters."""
from typing import Any, Dict, List, Optional
from ..base import Adapter


# ADAPTER-000045: OpenAI Adapter
class OpenAIAdapter(Adapter):
    """OpenAI API adapter."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("OpenAI", "openai", "OpenAI API")
        self.api_key = api_key
        self.metadata.auth_types = ["api_key"]
        self.metadata.capabilities = ["chat", "embeddings", "audio", "vision"]


# ADAPTER-000046: Anthropic Adapter
class AnthropicAdapter(Adapter):
    """Anthropic API adapter."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("Anthropic", "anthropic", "Anthropic API")
        self.api_key = api_key
        self.metadata.auth_types = ["api_key"]
        self.metadata.capabilities = ["chat", "vision"]


# ADAPTER-000047: Google AI Adapter
class GoogleAIAdapter(Adapter):
    """Google AI API adapter."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("GoogleAI", "google_ai", "Google AI API")
        self.api_key = api_key
        self.metadata.auth_types = ["api_key"]
        self.metadata.capabilities = ["chat", "embeddings"]


# ADAPTER-000048: Ollama Adapter
class OllamaAdapter(Adapter):
    """Ollama local AI adapter."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__("Ollama", "ollama", "Ollama Local AI")
        self.base_url = base_url
        self.metadata.auth_types = ["none"]
        self.metadata.capabilities = ["chat", "embeddings", "completion"]


# ADAPTER-000049: OpenRouter Adapter
class OpenRouterAdapter(Adapter):
    """OpenRouter API adapter."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("OpenRouter", "openrouter", "OpenRouter API")
        self.api_key = api_key
        self.metadata.auth_types = ["api_key"]
        self.metadata.capabilities = ["chat", "embeddings"]


# ADAPTER-000050: AWS Bedrock Adapter
class AWSBedrockAdapter(Adapter):
    """AWS Bedrock adapter."""
    
    def __init__(self, region: str = "us-east-1"):
        super().__init__("AWSBedrock", "aws_bedrock", "AWS Bedrock")
        self.region = region
        self.metadata.auth_types = ["aws_iam"]
        self.metadata.capabilities = ["chat", "embeddings"]


# Registry
AI_ADAPTERS = {
    "openai": OpenAIAdapter,
    "anthropic": AnthropicAdapter,
    "google_ai": GoogleAIAdapter,
    "ollama": OllamaAdapter,
    "openrouter": OpenRouterAdapter,
    "aws_bedrock": AWSBedrockAdapter,
}


def get_adapter(name: str):
    """Get an AI adapter."""
    adapter_class = AI_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()