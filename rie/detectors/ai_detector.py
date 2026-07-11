"""AI Stack Detector - Detect AI/ML technologies."""
from typing import Dict, List, Set

from ..domain.repository import Repository, Dependency
from ..domain.evidence import Evidence
from .base_detector import BaseDetector, DetectionResult


AI_STACK_SIGNATURES: Dict[str, Dict[str, List[str]]] = {
    "llm_providers": {
        "OpenAI": ["openai", "gpt-", "ChatGPT"],
        "Anthropic": ["anthropic", "claude", "Claude"],
        "Google": ["google-generativeai", "gemini"],
        "Mistral": ["mistralai", "mistral"],
        "Cohere": ["cohere"],
        "Hugging Face": ["transformers", "huggingface_hub"],
        "Azure OpenAI": ["azure-openai"],
    },
    "ml_frameworks": {
        "PyTorch": ["torch", "pytorch"],
        "TensorFlow": ["tensorflow", "tf-keras"],
        "JAX": ["jax", "flax"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "MXNet": ["mxnet", "gluon"],
        "Keras": ["keras"],
    },
    "embedding_models": {
        "OpenAI Embeddings": ["text-embedding-ada", "openai.embeddings"],
        "Sentence Transformers": ["sentence-transformers", "SentenceTransformer"],
        "Cohere Embeddings": ["cohere.embed"],
    },
    "vector_databases": {
        "Pinecone": ["pinecone", "pinecone-client"],
        "Chroma": ["chromadb", "chromadb"],
        "Weaviate": ["weaviate", "weaviate-client"],
        "Milvus": ["milvus", "pymilvus"],
        "Qdrant": ["qdrant", "qdrant-client"],
        "FAISS": ["faiss", "faiss-cpu", "faiss-gpu"],
    },
}


class AIStackDetector(BaseDetector):
    """Detects AI/ML stack in a repository."""
    
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect AI stack by dependencies and file content."""
        llm_providers: Set[str] = set()
        ml_frameworks: Set[str] = set()
        embedding_models: Set[str] = set()
        vector_databases: Set[str] = set()
        evidence_list: List[Evidence] = []
        
        # Check dependencies
        for dep in repo.dependencies:
            dep_name_lower = dep.name.lower()
            
            for category, providers in AI_STACK_SIGNATURES.items():
                for provider, signatures in providers.items():
                    for sig in signatures:
                        if sig.lower() in dep_name_lower:
                            if category == "llm_providers":
                                llm_providers.add(provider)
                            elif category == "ml_frameworks":
                                ml_frameworks.add(provider)
                            elif category == "embedding_models":
                                embedding_models.add(provider)
                            elif category == "vector_databases":
                                vector_databases.add(provider)
                            
                            evidence_list.append(Evidence(
                                file_path=f"dependency: {dep.name}",
                                content=f"Detected via dependency: {provider}",
                                confidence=0.9,
                            ))
        
        has_ai_stack = bool(llm_providers or ml_frameworks or vector_databases)
        confidence = 1.0 if has_ai_stack else 0.0
        
        return DetectionResult(
            detector_name="AIStackDetector",
            detected=has_ai_stack,
            confidence=confidence,
            data={
                "llm_providers": list(llm_providers),
                "ml_frameworks": list(ml_frameworks),
                "embedding_models": list(embedding_models),
                "vector_databases": list(vector_databases),
            },
            evidence=evidence_list,
        )
