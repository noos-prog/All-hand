"""AI Stack Detection - Detect AI/ML technologies."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


AI_STACK_SIGNATURES: Dict[str, List[str]] = {
    "OpenAI": ["openai", "gpt-", "chatgpt"],
    "Anthropic": ["anthropic", "claude"],
    "Google AI": ["google-generativeai", "gemini", "palm"],
    "Hugging Face": ["transformers", "huggingface", "diffusers"],
    "LangChain": ["langchain", "langsmith"],
    "LlamaIndex": ["llama-index", "llamaindex"],
    "AutoGen": ["autogen", "microsoft/autogen"],
    "CrewAI": ["crewai", "crew.ai"],
    "PyTorch": ["torch", "pytorch"],
    "TensorFlow": ["tensorflow", "tf-keras"],
    "JAX": ["jax", "flax"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Pinecone": ["pinecone"],
    "Chroma": ["chromadb", "chromadb"],
    "Weaviate": ["weaviate"],
    "FAISS": ["faiss"],
    "Qdrant": ["qdrant"],
}


@dataclass
class AIStack:
    """Detected AI stack."""
    llm_providers: List[str] = field(default_factory=list)
    ml_frameworks: List[str] = field(default_factory=list)
    vector_databases: List[str] = field(default_factory=list)
    confidence: float = 0.0


class AIDetector:
    """Detects AI/ML technologies."""
    
    def detect(self, dependencies: List[str]) -> AIStack:
        """Detect AI stack from dependencies."""
        ai_stack = AIStack()
        matched_count = 0
        
        for dep in dependencies:
            dep_lower = dep.lower()
            
            for tech, signatures in AI_STACK_SIGNATURES.items():
                if any(sig in dep_lower for sig in signatures):
                    matched_count += 1
                    
                    # Categorize
                    if tech in ["OpenAI", "Anthropic", "Google AI"]:
                        if tech not in ai_stack.llm_providers:
                            ai_stack.llm_providers.append(tech)
                    elif tech in ["PyTorch", "TensorFlow", "JAX", "scikit-learn"]:
                        if tech not in ai_stack.ml_frameworks:
                            ai_stack.ml_frameworks.append(tech)
                    elif tech in ["Pinecone", "Chroma", "Weaviate", "FAISS", "Qdrant"]:
                        if tech not in ai_stack.vector_databases:
                            ai_stack.vector_databases.append(tech)
        
        # Calculate confidence
        ai_stack.confidence = min(1.0, matched_count / 5.0)
        
        return ai_stack


class AIStackAnalyzer:
    """Analyzes AI stack in detail."""
    
    def __init__(self):
        self.detector = AIDetector()
    
    def analyze(self, dependencies: List[str]) -> AIStack:
        """Analyze AI stack."""
        return self.detector.detect(dependencies)
    
    def has_ai_stack(self, ai_stack: AIStack) -> bool:
        """Check if repository has AI stack."""
        return bool(ai_stack.llm_providers or ai_stack.ml_frameworks)
