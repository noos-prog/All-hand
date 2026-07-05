"""Repository Analysis Capability."""
import os
import subprocess
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts import RepositoryDNA, RepositorySnapshot
from interfaces import ICapability


class RepositoryAnalysisInput:
    """Input for Repository Analysis."""
    def __init__(self, url: str, branch: str = "main"):
        self.url = url
        self.branch = branch


class RepositoryAnalysisCapability(ICapability):
    """
    Analyzes a repository and generates its DNA.
    
    Pipeline:
    1. CloneRepository
    2. ReadRepository
    3. DetectLanguages
    4. DetectFrameworks
    5. GenerateDNA
    """
    
    @property
    def name(self) -> str:
        return "RepositoryAnalysis"
    
    @property
    def description(self) -> str:
        return "Analyzes repositories and generates DNA"
    
    @property
    def skills(self) -> List[str]:
        return ["CloneRepository", "ReadRepository", "GenerateDNA"]
    
    def execute(self, input_data: Any) -> RepositoryDNA:
        """Execute the capability."""
        if isinstance(input_data, dict):
            url = input_data.get("url", "")
            branch = input_data.get("branch", "main")
        elif hasattr(input_data, "url"):
            url = input_data.url
            branch = input_data.branch
        else:
            raise ValueError("Invalid input type")
        
        # Import provider here to avoid circular imports
        from providers import LocalRepositoryProvider
        provider = LocalRepositoryProvider()
        
        # Step 1: Clone
        print(f"[CAPABILITY] Cloning {url}")
        clone_result = provider._clone(RepositoryAnalysisInput(url, branch))
        repo_path = clone_result.path
        
        try:
            # Step 2: Read
            print(f"[CAPABILITY] Reading repository")
            read_result = provider._read(RepositoryAnalysisInput(repo_path))
            snapshot = read_result.snapshot
            
            # Step 3 & 4: Detect (inline for now)
            print(f"[CAPABILITY] Detecting languages")
            languages = self._detect_languages(snapshot)
            print(f"[CAPABILITY] Detecting frameworks")
            frameworks = self._detect_frameworks(snapshot)
            
            # Step 5: Generate DNA
            print(f"[CAPABILITY] Generating DNA")
            dna = self._generate_dna(snapshot, languages, frameworks)
            
            return dna
            
        finally:
            # Cleanup
            if os.path.exists(repo_path):
                import shutil
                parent = os.path.dirname(repo_path)
                if os.path.exists(parent):
                    shutil.rmtree(parent, ignore_errors=True)
    
    def _detect_languages(self, snapshot: RepositorySnapshot) -> List[str]:
        """Detect programming languages."""
        languages = set()
        
        # Language patterns
        patterns = {
            "Python": [".py", "requirements.txt", "setup.py", "pyproject.toml"],
            "JavaScript": [".js", ".jsx", "package.json"],
            "TypeScript": [".ts", ".tsx", "tsconfig.json"],
            "Java": [".java", "pom.xml", "build.gradle"],
            "Go": [".go", "go.mod", "go.sum"],
            "Rust": [".rs", "Cargo.toml", "Cargo.lock"],
            "C": [".c", ".h"],
            "C++": [".cpp", ".hpp", ".cc"],
            "C#": [".cs", ".csproj", ".sln"],
            "Ruby": [".rb", "Gemfile", "Gemfile.lock"],
            "PHP": [".php", "composer.json"],
            "Swift": [".swift", "Package.swift"],
            "Kotlin": [".kt", "build.gradle.kts"],
            "Scala": [".scala", "build.sbt"],
            "Dart": [".dart", "pubspec.yaml"],
        }
        
        for file_node in snapshot.files:
            if file_node.is_dir:
                continue
            path = file_node.path.lower()
            for lang, exts in patterns.items():
                for ext in exts:
                    if path.endswith(ext.lower()):
                        languages.add(lang)
                        break
        
        return sorted(list(languages))
    
    def _detect_frameworks(self, snapshot: RepositorySnapshot) -> List[str]:
        """Detect frameworks from files and dependencies."""
        frameworks = set()
        
        framework_patterns = {
            "Django": ["django", "django.db"],
            "Flask": ["flask", "from flask import"],
            "FastAPI": ["fastapi", "uvicorn"],
            "React": ["react", "react-dom"],
            "Vue": ["vue", "@vue"],
            "Angular": ["@angular/core"],
            "Next.js": ["next", "next.config"],
            "Express": ["express"],
            "Spring": ["org.springframework"],
            "Rails": ["rails"],
            "Laravel": ["laravel"],
            "FastAPI": ["fastapi"],
            "PyTorch": ["torch", "import torch"],
            "TensorFlow": ["tensorflow", "import tensorflow"],
            "LangChain": ["langchain"],
            "LlamaIndex": ["llama_index", "llamaindex"],
        }
        
        for file_node in snapshot.files:
            if file_node.is_dir or not file_node.content:
                continue
            
            content = file_node.content
            path = file_node.path.lower()
            
            # Check content
            for framework, keywords in framework_patterns.items():
                for keyword in keywords:
                    if keyword.lower() in content.lower():
                        frameworks.add(framework)
                        break
            
            # Check filenames
            if "package.json" in path:
                frameworks.add("Node.js")
            elif "requirements.txt" in path or "pyproject.toml" in path:
                frameworks.add("Python")
        
        return sorted(list(frameworks))
    
    def _generate_dna(
        self,
        snapshot: RepositorySnapshot,
        languages: List[str],
        frameworks: List[str]
    ) -> RepositoryDNA:
        """Generate Repository DNA."""
        metadata = snapshot.metadata
        
        # Find README
        readme_summary = ""
        for file_node in snapshot.files:
            if not file_node.is_dir:
                path_lower = file_node.path.lower()
                if "readme" in path_lower and file_node.content:
                    readme_summary = file_node.content[:500]
                    break
        
        # Find license
        license_name = ""
        for file_node in snapshot.files:
            if not file_node.is_dir:
                path_lower = file_node.path.lower()
                if "license" in path_lower or path_lower == "license":
                    license_name = os.path.basename(file_node.path)
                    break
        
        # Find config files
        config_extensions = [
            ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
            "package.json", "requirements.txt", "Gemfile", "go.mod"
        ]
        config_files = []
        for file_node in snapshot.files:
            if file_node.is_dir:
                continue
            path_lower = file_node.path.lower()
            for ext in config_extensions:
                if path_lower.endswith(ext) or ext in path_lower:
                    config_files.append(file_node.path)
                    break
        
        # Find package managers
        package_managers = set()
        for file_node in snapshot.files:
            if file_node.is_dir:
                continue
            path = file_node.path
            if "requirements.txt" in path or "pyproject.toml" in path:
                package_managers.add("pip")
            elif "package.json" in path:
                package_managers.add("npm")
            elif "go.mod" in path:
                package_managers.add("go")
            elif "Cargo.toml" in path:
                package_managers.add("cargo")
            elif "Gemfile" in path:
                package_managers.add("bundler")
            elif "pom.xml" in path or "build.gradle" in path:
                package_managers.add("maven")
        
        # Directory tree (top level)
        dirs = set()
        for file_node in snapshot.files:
            if file_node.is_dir:
                parts = file_node.path.split("/")
                if len(parts) > 0:
                    dirs.add(parts[0])
        
        return RepositoryDNA(
            name=metadata.name,
            url=metadata.url,
            owner=metadata.owner,
            primary_language=languages[0] if languages else "",
            languages=languages,
            frameworks=frameworks,
            package_managers=sorted(list(package_managers)),
            dependencies=[],
            config_files=config_files[:20],  # Limit to 20
            entry_points=[],
            directory_tree=sorted(list(dirs))[:20],
            readme_summary=readme_summary,
            license=license_name,
            generated_at=datetime.utcnow(),
            snapshot_path=""
        )
