"""
CAPABILITY-000006: Technology Detection

PURPOSE: Detect languages, frameworks, package managers, build systems, containers, and cloud providers.

VERSION: 1.0.0
"""
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Set

@dataclass
class TechnologyProfile:
    """Complete technology profile of a repository."""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    build_systems: List[str] = field(default_factory=list)
    containers: List[str] = field(default_factory=list)
    cloud_providers: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "languages": self.languages,
            "frameworks": self.frameworks,
            "package_managers": self.package_managers,
            "build_systems": self.build_systems,
            "containers": self.containers,
            "cloud_providers": self.cloud_providers,
            "detected_at": self.detected_at.isoformat(),
        }

class TechnologyDetectionCapability:
    """
    CAPABILITY-000006: Technology Detection
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000006"
    
    # Language detection patterns
    LANGUAGES = {
        "Python": [".py", "requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
        "JavaScript": [".js", ".jsx", "package.json"],
        "TypeScript": [".ts", ".tsx", "tsconfig.json"],
        "Java": [".java", "pom.xml", "build.gradle"],
        "Go": [".go", "go.mod", "go.sum"],
        "Rust": [".rs", "Cargo.toml", "Cargo.lock"],
        "C": [".c", ".h"],
        "C++": [".cpp", ".hpp", ".cc", ".cxx"],
        "C#": [".cs", ".csproj", ".sln"],
        "Ruby": [".rb", "Gemfile", "Gemfile.lock"],
        "PHP": [".php", "composer.json"],
        "Swift": [".swift", "Package.swift"],
        "Kotlin": [".kt", ".kts", "build.gradle.kts"],
        "Scala": [".scala", "build.sbt"],
        "Dart": [".dart", "pubspec.yaml"],
        "R": [".r", ".R", "DESCRIPTION"],
        "MATLAB": [".m"],
        "Julia": [".jl", "Project.toml"],
        "Lua": [".lua"],
        "Perl": [".pl", ".pm", "cpanfile"],
    }
    
    # Framework detection
    FRAMEWORKS = {
        "Django": ["django", "django.db", "settings.py"],
        "Flask": ["flask", "from flask import"],
        "FastAPI": ["fastapi", "uvicorn"],
        "Pyramid": ["pyramid"],
        "Rails": ["rails", "ActiveRecord"],
        "Laravel": ["laravel", "Illuminate"],
        "Spring": ["org.springframework"],
        "Angular": ["@angular/core"],
        "React": ["react", "react-dom"],
        "Vue.js": ["vue", "@vue"],
        "Next.js": ["next", "next.config"],
        "Express": ["express"],
        "NestJS": ["@nestjs"],
        "Svelte": ["svelte"],
        "PyTorch": ["torch", "import torch"],
        "TensorFlow": ["tensorflow", "import tensorflow"],
        "LangChain": ["langchain"],
        "LlamaIndex": ["llama_index"],
        "Scikit-learn": ["sklearn", "from sklearn"],
    }
    
    # Package managers
    PACKAGE_MANAGERS = {
        "pip": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "Pipfile.lock"],
        "npm": ["package.json", "package-lock.json"],
        "yarn": ["yarn.lock"],
        "pnpm": ["pnpm-lock.yaml"],
        "go": ["go.mod", "go.sum"],
        "cargo": ["Cargo.toml", "Cargo.lock"],
        "maven": ["pom.xml"],
        "gradle": ["build.gradle", "build.gradle.kts"],
        "bundler": ["Gemfile", "Gemfile.lock"],
        "composer": ["composer.json", "composer.lock"],
        "nuget": ["packages.config", ".csproj"],
    }
    
    # Build systems
    BUILD_SYSTEMS = {
        "Make": ["Makefile"],
        "CMake": ["CMakeLists.txt"],
        "Bazel": ["BUILD", "BUILD.bazel"],
        "Meson": ["meson.build"],
        "Ninja": ["build.ninja"],
        "Webpack": ["webpack.config.js"],
        "Vite": ["vite.config.js", "vite.config.ts"],
        "esbuild": ["esbuild.config.js"],
    }
    
    # Containers
    CONTAINERS = {
        "Docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"],
        "Podman": ["Containerfile"],
        "Kubernetes": ["kubernetes/", "k8s/"],
        "Helm": ["Chart.yaml"],
    }
    
    # Cloud providers
    CLOUD_PROVIDERS = {
        "AWS": ["aws/", ".aws/", "aws-sdk"],
        "Azure": ["azure/", ".azure/", "azure-sdk"],
        "GCP": ["gcp/", ".gcp/", "google-cloud"],
        "Heroku": ["Procfile"],
        "Vercel": ["vercel.json", ".vercel"],
        "Netlify": ["netlify.toml"],
        "Terraform": ["terraform/", ".tf"],
    }
    
    @property
    def name(self) -> str:
        return "TechnologyDetection"
    
    @property
    def description(self) -> str:
        return "Detects languages, frameworks, package managers, build systems, containers, and cloud providers"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> TechnologyProfile:
        """Execute technology detection."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        languages = set()
        frameworks = set()
        package_managers = set()
        build_systems = set()
        containers = set()
        cloud_providers = set()
        
        for root, dirs, files in os.walk(path):
            # Skip .git
            if ".git" in root:
                continue
            
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            
            for filename in files:
                if filename.startswith("."):
                    continue
                
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, path)
                
                # Language detection
                for lang, patterns in self.LANGUAGES.items():
                    if any(p in rel_path for p in patterns):
                        languages.add(lang)
                
                # Package manager detection
                for pm, patterns in self.PACKAGE_MANAGERS.items():
                    if any(p in rel_path for p in patterns):
                        package_managers.add(pm)
                
                # Build system detection
                for bs, patterns in self.BUILD_SYSTEMS.items():
                    if any(p in rel_path for p in patterns):
                        build_systems.add(bs)
                
                # Container detection
                for container, patterns in self.CONTAINERS.items():
                    if any(p in rel_path for p in patterns):
                        containers.add(container)
                
                # Cloud provider detection
                for cloud, patterns in self.CLOUD_PROVIDERS.items():
                    if any(p in rel_path for p in patterns):
                        cloud_providers.add(cloud)
                
                # Framework detection from content
                try:
                    if os.path.getsize(filepath) < 1024 * 1024:  # Skip > 1MB
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        for framework, keywords in self.FRAMEWORKS.items():
                            if any(kw.lower() in content.lower() for kw in keywords):
                                frameworks.add(framework)
                except:
                    pass
        
        return TechnologyProfile(
            languages=sorted(list(languages)),
            frameworks=sorted(list(frameworks)),
            package_managers=sorted(list(package_managers)),
            build_systems=sorted(list(build_systems)),
            containers=sorted(list(containers)),
            cloud_providers=sorted(list(cloud_providers)),
        )
