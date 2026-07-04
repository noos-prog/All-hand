"""AGOS Model Packs Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ModelPackMetadata:
    """Model pack metadata."""
    id: str
    name: str
    family: str
    provider: str
    version: str = "1.0.0"
    description: str = ""


class ModelPack:
    """An AI model pack."""
    
    def __init__(self, name: str, family: str, provider: str, description: str = ""):
        self.metadata = ModelPackMetadata(
            id=f"model-{uuid.uuid4().hex[:8]}",
            name=name,
            family=family,
            provider=provider,
            description=description,
        )
        self.context_limit = 128000
        self.capabilities: List[str] = []
        self.pricing_profile: Dict[str, float] = {}
        self.latency_profile: Dict[str, float] = {}


# Model Packs
MODEL_PACKS = {
    # GPT Family
    "gpt4": ModelPack("GPT-4", "GPT", "OpenAI", "GPT-4 model"),
    "gpt4_turbo": ModelPack("GPT-4 Turbo", "GPT", "OpenAI", "GPT-4 Turbo"),
    "gpt4o": ModelPack("GPT-4o", "GPT", "OpenAI", "GPT-4 Omni"),
    "gpt4o_mini": ModelPack("GPT-4o Mini", "GPT", "OpenAI", "GPT-4o Mini"),
    "gpt35_turbo": ModelPack("GPT-3.5 Turbo", "GPT", "OpenAI", "GPT-3.5 Turbo"),
    
    # Claude Family
    "claude3_opus": ModelPack("Claude 3 Opus", "Claude", "Anthropic", "Claude 3 Opus"),
    "claude3_sonnet": ModelPack("Claude 3 Sonnet", "Claude", "Anthropic", "Claude 3 Sonnet"),
    "claude3_haiku": ModelPack("Claude 3 Haiku", "Claude", "Anthropic", "Claude 3 Haiku"),
    "claude35_sonnet": ModelPack("Claude 3.5 Sonnet", "Claude", "Anthropic", "Claude 3.5 Sonnet"),
    "claude35_haiku": ModelPack("Claude 3.5 Haiku", "Claude", "Anthropic", "Claude 3.5 Haiku"),
    
    # Gemini Family
    "gemini_pro": ModelPack("Gemini Pro", "Gemini", "Google", "Gemini Pro"),
    "gemini_ultra": ModelPack("Gemini Ultra", "Gemini", "Google", "Gemini Ultra"),
    "gemini_flash": ModelPack("Gemini Flash", "Gemini", "Google", "Gemini Flash"),
    "gemini_flash_8b": ModelPack("Gemini Flash 8B", "Gemini", "Google", "Gemini Flash 8B"),
    "gemini_exp": ModelPack("Gemini Experimental", "Gemini", "Google", "Gemini Experimental"),
    
    # DeepSeek Family
    "deepseek_chat": ModelPack("DeepSeek Chat", "DeepSeek", "DeepSeek", "DeepSeek Chat"),
    "deepseek_coder": ModelPack("DeepSeek Coder", "DeepSeek", "DeepSeek", "DeepSeek Coder"),
    
    # Qwen Family
    "qwen_turbo": ModelPack("Qwen Turbo", "Qwen", "Alibaba", "Qwen Turbo"),
    "qwen_plus": ModelPack("Qwen Plus", "Qwen", "Alibaba", "Qwen Plus"),
    "qwen_max": ModelPack("Qwen Max", "Qwen", "Alibaba", "Qwen Max"),
    
    # Llama Family
    "llama3_8b": ModelPack("Llama 3 8B", "Llama", "Meta", "Llama 3 8B"),
    "llama3_70b": ModelPack("Llama 3 70B", "Llama", "Meta", "Llama 3 70B"),
    "llama3_1_8b": ModelPack("Llama 3.1 8B", "Llama", "Meta", "Llama 3.1 8B"),
    "llama3_1_70b": ModelPack("Llama 3.1 70B", "Llama", "Meta", "Llama 3.1 70B"),
    "llama3_1_405b": ModelPack("Llama 3.1 405B", "Llama", "Meta", "Llama 3.1 405B"),
    
    # Mistral Family
    "mistral_7b": ModelPack("Mistral 7B", "Mistral", "Mistral AI", "Mistral 7B"),
    "mixtral_8x7b": ModelPack("Mixtral 8x7B", "Mistral", "Mistral AI", "Mixtral 8x7B"),
    "mixtral_8x22b": ModelPack("Mixtral 8x22B", "Mistral", "Mistral AI", "Mixtral 8x22B"),
    "mistral_large": ModelPack("Mistral Large", "Mistral", "Mistral AI", "Mistral Large"),
    
    # Command Family
    "command_r": ModelPack("Command R", "Command", "Cohere", "Command R"),
    "command_r_plus": ModelPack("Command R+", "Command", "Cohere", "Command R+"),
    
    # Phi Family
    "phi3_mini": ModelPack("Phi-3 Mini", "Phi", "Microsoft", "Phi-3 Mini"),
    "phi3_medium": ModelPack("Phi-3 Medium", "Phi", "Microsoft", "Phi-3 Medium"),
    "phi3_5_mini": ModelPack("Phi-3.5 Mini", "Phi", "Microsoft", "Phi-3.5 Mini"),
    
    # Gemma Family
    "gemma2_2b": ModelPack("Gemma 2 2B", "Gemma", "Google", "Gemma 2 2B"),
    "gemma2_9b": ModelPack("Gemma 2 9B", "Gemma", "Google", "Gemma 2 9B"),
    "gemma2_27b": ModelPack("Gemma 2 27B", "Gemma", "Google", "Gemma 2 27B"),
    
    # Audio Models
    "whisper": ModelPack("Whisper", "Whisper", "OpenAI", "Whisper ASR"),
    "parakeet": ModelPack("Parakeet", "Parakeet", "AssemblyAI", "Parakeet TTS"),
    "xtts": ModelPack("XTTS", "XTTS", "Coqui", "XTTS TTS"),
    "elevenlabs": ModelPack("ElevenLabs", "ElevenLabs", "ElevenLabs", "ElevenLabs TTS"),
    
    # Image Models
    "imagen3": ModelPack("Imagen 3", "Imagen", "Google", "Imagen 3"),
    "dalle3": ModelPack("DALL-E 3", "DALL-E", "OpenAI", "DALL-E 3"),
    "stable_diffusion": ModelPack("Stable Diffusion", "SD", "Stability AI", "Stable Diffusion"),
    "flux": ModelPack("FLUX", "FLUX", "BlackForest", "FLUX Image Gen"),
    
    # Vision Models
    "yolo": ModelPack("YOLO", "YOLO", "Ultralytics", "YOLO Object Detection"),
    "sam": ModelPack("SAM", "SAM", "Meta", "Segment Anything Model"),
    "clip": ModelPack("CLIP", "CLIP", "OpenAI", "CLIP Vision"),
    
    # Embedding Models
    "text_embedding_3_large": ModelPack("Embedding 3 Large", "Embedding", "OpenAI", "Embedding 3 Large"),
    "text_embedding_3_small": ModelPack("Embedding 3 Small", "Embedding", "OpenAI", "Embedding 3 Small"),
    "embed_v3": ModelPack("Embed v3", "Embedding", "Google", "Gemini Embedding v3"),
    
    # Reasoning Models
    "o1_preview": ModelPack("o1 Preview", "o1", "OpenAI", "OpenAI o1 Preview"),
    "o1_mini": ModelPack("o1 Mini", "o1", "OpenAI", "OpenAI o1 Mini"),
    
    # Local Models
    "gguf": ModelPack("GGUF", "GGUF", "Local", "Local GGUF Models"),
    "onnx": ModelPack("ONNX", "ONNX", "Local", "ONNX Runtime Models"),
}


class ModelPackLibrary:
    """Library of model packs."""
    
    def __init__(self):
        self.packs = MODEL_PACKS
    
    def get(self, name: str) -> ModelPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[ModelPack]:
        return list(self.packs.values())
    
    def list_by_family(self, family: str) -> List[ModelPack]:
        return [p for p in self.packs.values() if p.metadata.family == family]
    
    def list_by_provider(self, provider: str) -> List[ModelPack]:
        return [p for p in self.packs.values() if p.metadata.provider == provider]


_library = ModelPackLibrary()


def get_library() -> ModelPackLibrary:
    return _library