"""RIE Detectors - Isolated plugin-based detectors."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class DetectorContext:
    """Context passed to detectors."""
    repository_url: str
    files: Dict[str, Any]  # path -> {size, extension, has_content}
    directories: List[str]
    metadata: Dict[str, Any]
    
    def get_file_content(self, path: str) -> Optional[str]:
        """Get file content if available."""
        return self.metadata.get("_content", {}).get(path)
    
    def get_files_by_extension(self, ext: str) -> List[str]:
        """Get files by extension."""
        return [
            path for path, data in self.files.items()
            if data.get("extension") == ext
        ]
    
    def get_files_in_directory(self, directory: str) -> List[str]:
        """Get files in a directory."""
        return [
            path for path in self.files.keys()
            if path.startswith(directory + "/")
        ]


@dataclass
class DetectorResult:
    """Result from a detector."""
    name: str
    success: bool
    features: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    duration_ms: int = 0


class IDetector(ABC):
    """Detector interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Detector name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Detector description."""
        pass
    
    @abstractmethod
    def detect(self, context: DetectorContext) -> DetectorResult:
        """Run detection."""
        pass


class LanguageDetector(IDetector):
    """Detects programming languages."""
    
    LANGUAGE_EXTENSIONS = {
        "Python": [".py"],
        "JavaScript": [".js", ".jsx", ".mjs"],
        "TypeScript": [".ts", ".tsx"],
        "Java": [".java"],
        "Go": [".go"],
        "Rust": [".rs"],
        "C": [".c", ".h"],
        "C++": [".cpp", ".hpp", ".cc", ".cxx"],
        "C#": [".cs"],
        "Ruby": [".rb"],
        "PHP": [".php"],
        "Swift": [".swift"],
        "Kotlin": [".kt", ".kts"],
        "Scala": [".scala"],
        "Dart": [".dart"],
        "R": [".r", ".R"],
    }
    
    @property
    def name(self) -> str:
        return "LanguageDetector"
    
    @property
    def description(self) -> str:
        return "Detects programming languages in repository"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        language_counts = {}
        
        for path, data in context.files.items():
            ext = data.get("extension", "")
            for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
                if ext in extensions:
                    language_counts[lang] = language_counts.get(lang, 0) + 1
                    break
        
        # Calculate percentages
        total = sum(language_counts.values())
        language_percentages = {
            lang: (count / total * 100) if total > 0 else 0
            for lang, count in language_counts.items()
        }
        
        # Primary language
        primary = max(language_percentages, key=language_percentages.get) if language_percentages else ""
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "languages": list(language_counts.keys()),
                "language_percentages": language_percentages,
                "primary_language": primary,
                "total_files_by_language": language_counts
            },
            duration_ms=duration_ms
        )


class FrameworkDetector(IDetector):
    """Detects frameworks."""
    
    FRAMEWORK_PATTERNS = {
        "Django": ["django", "django.db", "from django"],
        "Flask": ["from flask import", "app = Flask"],
        "FastAPI": ["from fastapi import", "FastAPI()"],
        "React": ["react", "React.Component", "create-react-app"],
        "Vue": ["vue", "Vue.createApp", "@vue"],
        "Angular": ["@angular/core", "NgModule"],
        "Next.js": ["next.config", "getServerSideProps"],
        "Express": ["express()", "app.use(express"],
        "Spring": ["org.springframework", "@SpringBootApplication"],
        "Rails": ["rails", "Rails.application"],
        "Laravel": ["Laravel", "Illuminate\\"],
        "PyTorch": ["import torch", "torch.nn"],
        "TensorFlow": ["import tensorflow", "tf.keras"],
        "LangChain": ["langchain", "from langchain"],
    }
    
    @property
    def name(self) -> str:
        return "FrameworkDetector"
    
    @property
    def description(self) -> str:
        return "Detects frameworks in repository"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        detected_frameworks = set()
        
        for path, data in context.files.items():
            # Check by filename
            path_lower = path.lower()
            if "package.json" in path:
                detected_frameworks.add("Node.js")
            elif "requirements.txt" in path or "pyproject.toml" in path:
                detected_frameworks.add("Python")
            elif "go.mod" in path:
                detected_frameworks.add("Go")
            elif "Cargo.toml" in path:
                detected_frameworks.add("Rust")
            elif "Gemfile" in path:
                detected_frameworks.add("Ruby")
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "frameworks": sorted(list(detected_frameworks))
            },
            duration_ms=duration_ms
        )


class ConfigurationDetector(IDetector):
    """Detects configuration files."""
    
    CONFIG_PATTERNS = [
        "package.json", "package-lock.json",
        "requirements.txt", "pyproject.toml", "setup.py",
        "go.mod", "go.sum",
        "Cargo.toml", "Cargo.lock",
        "Gemfile", "Gemfile.lock",
        "pom.xml", "build.gradle",
        "tsconfig.json", "jsconfig.json",
        "webpack.config.js", "vite.config.js",
        "docker-compose.yml", "Dockerfile",
        ".env", ".env.example",
        "Makefile", "CMakeLists.txt",
        ".eslintrc", ".prettierrc",
    ]
    
    @property
    def name(self) -> str:
        return "ConfigurationDetector"
    
    @property
    def description(self) -> str:
        return "Detects configuration files"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        config_files = []
        
        for path in context.files.keys():
            path_lower = path.lower()
            for pattern in self.CONFIG_PATTERNS:
                if pattern.lower() in path_lower:
                    config_files.append(path)
                    break
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "config_files": sorted(config_files)
            },
            duration_ms=duration_ms
        )


class LicenseDetector(IDetector):
    """Detects license type."""
    
    LICENSE_FILES = ["license", "license.txt", "license.md", "copying", "copying.txt"]
    
    LICENSE_TYPES = {
        "MIT": "mit",
        "Apache": "apache",
        "GPL": "gpl",
        "BSD": "bsd",
        "ISC": "isc",
    }
    
    @property
    def name(self) -> str:
        return "LicenseDetector"
    
    @property
    def description(self) -> str:
        return "Detects license type"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        license_type = ""
        has_license = False
        
        for path in context.files.keys():
            path_lower = path.lower()
            if "license" in path_lower:
                has_license = True
                for ltype, indicator in self.LICENSE_TYPES.items():
                    if indicator in path_lower:
                        license_type = ltype
                        break
                if not license_type:
                    license_type = "Other"
                break
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "has_license": has_license,
                "license_type": license_type
            },
            duration_ms=duration_ms
        )


class ReadmeDetector(IDetector):
    """Detects README."""
    
    README_FILES = ["readme.md", "readme.txt", "readme"]
    
    @property
    def name(self) -> str:
        return "ReadmeDetector"
    
    @property
    def description(self) -> str:
        return "Detects README and documentation"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        has_readme = False
        has_changelog = False
        
        for path in context.files.keys():
            path_lower = path.lower()
            if "readme" in path_lower:
                has_readme = True
            if "changelog" in path_lower:
                has_changelog = True
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "has_readme": has_readme,
                "has_changelog": has_changelog
            },
            duration_ms=duration_ms
        )


class DirectoryDetector(IDetector):
    """Detects directory structure."""
    
    @property
    def name(self) -> str:
        return "DirectoryDetector"
    
    @property
    def description(self) -> str:
        return "Detects directory structure"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        top_level_dirs = set()
        for directory in context.directories:
            parts = directory.split("/")
            if parts:
                top_level_dirs.add(parts[0])
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "top_level_directories": sorted(list(top_level_dirs)),
                "directory_tree": sorted(context.directories)
            },
            duration_ms=duration_ms
        )


class DependencyDetector(IDetector):
    """Detects package managers and dependencies."""
    
    DEPENDENCY_FILES = {
        "pip": ["requirements.txt", "pyproject.toml", "setup.py"],
        "npm": ["package.json"],
        "go": ["go.mod"],
        "cargo": ["Cargo.toml"],
        "bundler": ["Gemfile"],
        "maven": ["pom.xml", "build.gradle"],
    }
    
    @property
    def name(self) -> str:
        return "DependencyDetector"
    
    @property
    def description(self) -> str:
        return "Detects package managers and dependencies"
    
    def detect(self, context: DetectorContext) -> DetectorResult:
        start = datetime.utcnow()
        
        package_managers = []
        
        for path in context.files.keys():
            path_lower = path.lower()
            for pm, files in self.DEPENDENCY_FILES.items():
                if any(f.lower() in path_lower for f in files):
                    if pm not in package_managers:
                        package_managers.append(pm)
        
        duration_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
        
        return DetectorResult(
            name=self.name,
            success=True,
            features={
                "package_managers": package_managers
            },
            duration_ms=duration_ms
        )


class DetectorRegistry:
    """Registry for detectors."""
    
    def __init__(self):
        self._detectors: Dict[str, IDetector] = {}
    
    def register(self, detector: IDetector) -> None:
        """Register a detector."""
        self._detectors[detector.name] = detector
    
    def get(self, name: str) -> Optional[IDetector]:
        """Get a detector."""
        return self._detectors.get(name)
    
    def list_all(self) -> List[IDetector]:
        """List all detectors."""
        return list(self._detectors.values())
    
    def detect_all(self, context: DetectorContext) -> List[DetectorResult]:
        """Run all detectors."""
        results = []
        for detector in self._detectors.values():
            result = detector.detect(context)
            results.append(result)
        return results


def create_default_registry() -> DetectorRegistry:
    """Create registry with default detectors."""
    registry = DetectorRegistry()
    registry.register(LanguageDetector())
    registry.register(FrameworkDetector())
    registry.register(ConfigurationDetector())
    registry.register(LicenseDetector())
    registry.register(ReadmeDetector())
    registry.register(DirectoryDetector())
    registry.register(DependencyDetector())
    return registry
