"""Framework Detector - Detect frameworks."""
from typing import Dict, List

from ..domain.repository import Repository, FileInfo
from .base_detector import BaseDetector, DetectionResult


FRAMEWORK_SIGNATURES: Dict[str, List[str]] = {
    "React": ["react", "jsx", "tsx"],
    "Vue": ["vue", ".vue"],
    "Angular": ["@angular", "ng-"],
    "Django": ["django", "settings.py"],
    "Flask": ["flask", "app.route"],
    "FastAPI": ["fastapi", "app = FastAPI"],
    "Express": ["express", "express.js"],
    "Spring": ["spring", "Application.java"],
    "Next.js": ["next", "next.config"],
    "Laravel": ["laravel", "artisan"],
    "Rails": ["rails", "config/routes"],
    "Flutter": ["flutter", "pubspec.yaml"],
    "PyTorch": ["torch", "import torch"],
    "TensorFlow": ["tensorflow", "tf.function"],
    "LangChain": ["langchain", "from langchain"],
    "OpenAI": ["openai", "openai.ChatCompletion"],
}


class FrameworkDetector(BaseDetector):
    """Detects frameworks and libraries."""
    
    def detect(self, repo: Repository) -> DetectionResult:
        """Detect frameworks by file content and dependencies."""
        detected_frameworks: List[str] = []
        
        # Check dependencies
        for dep in repo.dependencies:
            for framework, signatures in FRAMEWORK_SIGNATURES.items():
                if any(sig.lower() in dep.name.lower() for sig in signatures):
                    if framework not in detected_frameworks:
                        detected_frameworks.append(framework)
        
        # Check file names
        for file in repo.files:
            for framework, signatures in FRAMEWORK_SIGNATURES.items():
                for sig in signatures:
                    if sig in file.name or sig in file.path:
                        if framework not in detected_frameworks:
                            detected_frameworks.append(framework)
        
        confidence = 1.0 if len(detected_frameworks) > 0 else 0.0
        
        return DetectionResult(
            detector_name="FrameworkDetector",
            detected=len(detected_frameworks) > 0,
            confidence=confidence,
            data={
                "frameworks": detected_frameworks,
                "count": len(detected_frameworks),
            },
        )
