"""Universal Capability Discovery Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class Capability:
    """A discovered capability."""
    id: str
    name: str
    type: str  # command, service, library, api, script, pipeline
    description: str = ""
    path: str = ""
    signature: str = ""
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: str = ""
    language: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    score: float = 0.0
    contracts: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityDNA:
    """DNA signature of a capability."""
    type: str
    language: str
    patterns: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    complexity: int = 0
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


@dataclass
class CapabilityMetadata:
    """Metadata about a capability."""
    version: str = "1.0.0"
    author: str = ""
    dependencies: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)


@dataclass
class CandidateCapability:
    """A candidate capability that needs validation."""
    name: str
    type: str
    path: str
    confidence: float = 0.0
    evidence: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class CapabilityDiscoveryEngine:
    """Discovers capabilities within repositories."""
    
    # Capability type detection
    COMMAND_PATTERNS = [
        'cli', 'cmd', 'command', 'runner', 'executor',
        'script', 'tool', 'utility'
    ]
    
    SERVICE_PATTERNS = [
        'service', 'server', 'daemon', 'worker', 'processor',
        'handler', 'agent', 'engine'
    ]
    
    LIBRARY_PATTERNS = [
        'lib', 'library', 'sdk', 'module', 'package',
        'client', 'wrapper', 'adapter'
    ]
    
    API_PATTERNS = [
        'api', 'rest', 'graphql', 'grpc', 'endpoint',
        'route', 'controller', 'handler'
    ]
    
    PIPELINE_PATTERNS = [
        'pipeline', 'workflow', 'task', 'job', 'scheduler',
        'cron', 'batch', 'stream'
    ]
    
    def __init__(self, root_path: str):
        """Initialize discovery engine."""
        self.root_path = Path(root_path)
        self.capabilities: List[Capability] = []
        self.candidates: List[CandidateCapability] = []
    
    def discover(self) -> List[Capability]:
        """Discover all capabilities."""
        self._discover_commands()
        self._discover_services()
        self._discover_libraries()
        self._discover_apis()
        self._discover_scripts()
        self._discover_pipelines()
        self._score_capabilities()
        return self.capabilities
    
    def _discover_commands(self) -> None:
        """Discover command-line tools."""
        patterns = ['cli.py', 'cli/', 'cmd.py', 'commands.py', 'main.py']
        
        for pattern in patterns:
            for path in self.root_path.rglob(pattern):
                rel_path = str(path.relative_to(self.root_path))
                
                capability = Capability(
                    id=f"cmd_{len(self.capabilities)}",
                    name=path.parent.name if path.name == 'cli.py' else path.stem,
                    type="command",
                    path=rel_path,
                    signature=self._extract_main_signature(path),
                    metadata={"entry_point": str(path)}
                )
                self.capabilities.append(capability)
        
        # Discover shell scripts
        for path in self.root_path.rglob('*.sh'):
            if 'bin' in str(path) or 'cmd' in str(path):
                rel_path = str(path.relative_to(self.root_path))
                capability = Capability(
                    id=f"cmd_{len(self.capabilities)}",
                    name=path.stem,
                    type="command",
                    path=rel_path,
                    language="shell"
                )
                self.capabilities.append(capability)
    
    def _discover_services(self) -> None:
        """Discover services."""
        service_names = ['service', 'server', 'daemon', 'worker', 'agent']
        
        for root, dirs, files in self._walk_with_filter():
            for d in dirs:
                if any(s in d.lower() for s in service_names):
                    capability = Capability(
                        id=f"svc_{len(self.capabilities)}",
                        name=d,
                        type="service",
                        path=str(Path(root) / d),
                        description=f"Service component: {d}"
                    )
                    self.capabilities.append(capability)
    
    def _discover_libraries(self) -> None:
        """Discover libraries and SDKs."""
        library_indicators = ['__init__.py', 'setup.py', 'pyproject.toml', 
                             'package.json', 'CMakeLists.txt']
        
        for root, _, files in self._walk_with_filter():
            if any(ind in files for ind in library_indicators):
                rel_path = str(Path(root).relative_to(self.root_path))
                
                # Determine library type
                lib_type = "library"
                if 'package.json' in files:
                    lib_type = "npm_package"
                elif 'setup.py' in files or 'pyproject.toml' in files:
                    lib_type = "python_package"
                
                capability = Capability(
                    id=f"lib_{len(self.capabilities)}",
                    name=Path(root).name,
                    type="library",
                    path=rel_path,
                    language=self._detect_language(files)
                )
                self.capabilities.append(capability)
    
    def _discover_apis(self) -> None:
        """Discover APIs."""
        api_patterns = ['api.py', 'routes.py', 'endpoints.py', 'views.py',
                       'api/', 'routes/', 'endpoints/']
        
        for root, dirs, files in self._walk_with_filter():
            for pattern in api_patterns:
                if pattern in files or pattern.rstrip('/') in dirs:
                    rel_path = str(Path(root).relative_to(self.root_path))
                    capability = Capability(
                        id=f"api_{len(self.capabilities)}",
                        name=Path(root).name,
                        type="api",
                        path=rel_path,
                        description=f"API component: {rel_path}"
                    )
                    self.capabilities.append(capability)
                    break
    
    def _discover_scripts(self) -> None:
        """Discover scripts."""
        script_extensions = ['.sh', '.bash', '.py', '.js', '.rb']
        script_directories = ['scripts', 'tools', 'scripts/', 'bin/']
        
        for root, dirs, files in self._walk_with_filter():
            rel_root = str(Path(root).relative_to(self.root_path))
            
            # Check if in script directory
            if any(s in rel_root for s in script_directories):
                for f in files:
                    if Path(f).suffix in script_extensions:
                        capability = Capability(
                            id=f"script_{len(self.capabilities)}",
                            name=Path(f).stem,
                            type="script",
                            path=str(Path(root) / f),
                            language=self._get_language_from_ext(Path(f).suffix)
                        )
                        self.capabilities.append(capability)
    
    def _discover_pipelines(self) -> None:
        """Discover pipelines and workflows."""
        pipeline_files = [
            'Jenkinsfile', 'pipeline.py', 'pipeline.yml',
            '.github/workflows', 'azure-pipelines.yml'
        ]
        
        for pattern in pipeline_files:
            for path in self.root_path.rglob(pattern):
                if path.is_file():
                    rel_path = str(path.relative_to(self.root_path))
                    capability = Capability(
                        id=f"pipeline_{len(self.capabilities)}",
                        name=path.stem,
                        type="pipeline",
                        path=rel_path,
                        description="CI/CD pipeline"
                    )
                    self.capabilities.append(capability)
    
    def _score_capabilities(self) -> None:
        """Score and rank capabilities."""
        for cap in self.capabilities:
            score = 0.5
            
            # Boost based on documentation
            if cap.description:
                score += 0.1
            
            # Boost based on having parameters
            if cap.parameters:
                score += 0.1
            
            # Boost based on language detection
            if cap.language:
                score += 0.1
            
            # Boost based on path clarity
            if '/' in cap.path and len(cap.path.split('/')) <= 3:
                score += 0.1
            
            # Boost based on naming conventions
            if any(p in cap.name.lower() for p in self.COMMAND_PATTERNS + 
                   self.SERVICE_PATTERNS + self.API_PATTERNS):
                score += 0.1
            
            cap.score = min(score, 1.0)
    
    def _walk_with_filter(self):
        """Walk directory tree with common filter."""
        ignore_dirs = {'node_modules', '.git', '__pycache__', 'venv', 
                      '.venv', 'dist', 'build', '.pytest_cache'}
        
        for root, dirs, files in self.root_path.walk() if hasattr(self.root_path, 'walk') else []:
            pass
        
        import os
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            yield root, dirs, files
    
    def _extract_main_signature(self, path: Path) -> str:
        """Extract main function signature."""
        if path.suffix != '.py':
            return ""
        
        try:
            content = path.read_text()
            if 'def main(' in content:
                start = content.find('def main(')
                end = content.find('\n', start)
                return content[start:end]
        except:
            pass
        
        return ""
    
    def _detect_language(self, files: List[str]) -> Optional[str]:
        """Detect programming language from files."""
        if any(f.endswith('.py') for f in files):
            return 'python'
        elif any(f.endswith('.js') or f.endswith('.ts') for f in files):
            return 'javascript'
        elif any(f.endswith('.java') for f in files):
            return 'java'
        elif any(f.endswith('.go') for f in files):
            return 'go'
        return None
    
    def _get_language_from_ext(self, ext: str) -> str:
        """Get language from file extension."""
        lang_map = {
            '.py': 'python',
            '.sh': 'shell',
            '.bash': 'shell',
            '.js': 'javascript',
            '.rb': 'ruby',
        }
        return lang_map.get(ext, 'unknown')
    
    def get_capabilities_by_type(self, cap_type: str) -> List[Capability]:
        """Get capabilities filtered by type."""
        return [c for c in self.capabilities if c.type == cap_type]
    
    def get_capability_dna(self, capability: Capability) -> CapabilityDNA:
        """Generate DNA signature for a capability."""
        return CapabilityDNA(
            type=capability.type,
            language=capability.language or "unknown",
            patterns=[capability.type],
            keywords=capability.tags,
            complexity=len(capability.parameters),
            inputs=[p['name'] for p in capability.parameters],
            outputs=[capability.return_type]
        )
