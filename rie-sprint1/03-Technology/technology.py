"""Technology Detection - Detect programming languages and frameworks."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set
import os


LANGUAGE_SIGNATURES: Dict[str, List[str]] = {
    "Python": [".py", ".pyw", ".pyx"],
    "JavaScript": [".js", ".jsx", ".mjs", ".cjs"],
    "TypeScript": [".ts", ".tsx"],
    "Java": [".java"],
    "Go": [".go"],
    "Rust": [".rs"],
    "C#": [".cs"],
    "C++": [".cpp", ".cc", ".cxx", ".hpp"],
    "C": [".c", ".h"],
    "Ruby": [".rb"],
    "Swift": [".swift"],
    "Kotlin": [".kt", ".kts"],
    "Scala": [".scala"],
    "PHP": [".php"],
}

FRAMEWORK_SIGNATURES: Dict[str, List[str]] = {
    "Django": ["django", "manage.py"],
    "Flask": ["flask", "app.route"],
    "FastAPI": ["fastapi", "uvicorn"],
    "React": ["react", "jsx", ".tsx"],
    "Vue": ["vue", ".vue"],
    "Angular": ["angular", "@angular"],
    "Next.js": ["next", "next.config"],
    "Express": ["express", "express.js"],
    "Spring": ["spring", "Application.java"],
    "Laravel": ["laravel", "artisan"],
    "Rails": ["rails", "config/routes"],
}


@dataclass
class TechnologyStack:
    """Detected technology stack."""
    languages: Dict[str, int] = field(default_factory=dict)
    frameworks: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)


class TechnologyDetector:
    """Detects programming languages."""
    
    def detect(self, files: List[Dict[str, Any]]) -> Dict[str, int]:
        """Detect languages from file list."""
        languages: Dict[str, int] = {}
        
        for file in files:
            ext = file.get("extension", "")
            for lang, extensions in LANGUAGE_SIGNATURES.items():
                if ext in extensions:
                    languages[lang] = languages.get(lang, 0) + 1
                    break
        
        return languages


class TechnologyStackAnalyzer:
    """Analyzes complete technology stack."""
    
    def __init__(self):
        self.language_detector = TechnologyDetector()
    
    def analyze(
        self,
        files: List[Dict[str, Any]],
        dependencies: List[str] = None,
    ) -> TechnologyStack:
        """Analyze complete technology stack."""
        stack = TechnologyStack()
        
        # Detect languages
        stack.languages = self.language_detector.detect(files)
        
        # Detect frameworks from dependencies
        if dependencies:
            for dep in dependencies:
                dep_lower = dep.lower()
                for framework, signatures in FRAMEWORK_SIGNATURES.items():
                    if any(sig in dep_lower for sig in signatures):
                        if framework not in stack.frameworks:
                            stack.frameworks.append(framework)
        
        return stack
