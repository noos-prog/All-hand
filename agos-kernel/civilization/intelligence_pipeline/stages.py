"""
Pipeline Stages
PHASE-02: EXECUTION-000003 - Engineering Intelligence Pipeline

Defines all pipeline stages for converting repositories to engineering intelligence.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import ast
import json
import hashlib
from dataclasses import dataclass


@dataclass
class StageResult:
    """Result of a pipeline stage."""
    success: bool = False
    data: Dict = None
    errors: list = None
    warnings: list = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class PipelineStage(ABC):
    """Base class for pipeline stages."""
    
    name: str = "base"
    description: str = ""
    
    def __init__(self):
        self.dependencies = []
    
    @abstractmethod
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Process the stage."""
        pass
    
    def validate(self, context: Dict) -> bool:
        """Validate stage prerequisites."""
        return True


class RepositoryFingerprintStage(PipelineStage):
    """Stage 1: Create repository fingerprint."""
    
    name = "repository_fingerprint"
    description = "Create basic repository fingerprint"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Create repository fingerprint."""
        result = StageResult()
        repo = Path(repo_path)
        
        # Basic info
        fingerprint = {
            'name': repo.name,
            'path': str(repo.resolve()),
            'exists': repo.exists(),
            'is_dir': repo.is_dir() if repo.exists() else False,
        }
        
        # Git info if available
        import subprocess
        try:
            # Get remote URL
            remote = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=repo, capture_output=True, text=True, timeout=5
            )
            if remote.returncode == 0:
                fingerprint['remote_url'] = remote.stdout.strip()
            
            # Get current branch
            branch = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=repo, capture_output=True, text=True, timeout=5
            )
            if branch.returncode == 0:
                fingerprint['branch'] = branch.stdout.strip()
            
            # Get commit count
            commits = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=repo, capture_output=True, text=True, timeout=5
            )
            if commits.returncode == 0:
                fingerprint['commit_count'] = int(commits.stdout.strip())
                
        except Exception as e:
            result.warnings.append(f"Git info not available: {e}")
        
        # Calculate directory fingerprint
        fingerprint['hash'] = self._calculate_fingerprint(repo_path)
        
        result.success = True
        result.data = fingerprint
        return result
    
    def _calculate_fingerprint(self, repo_path: str) -> str:
        """Calculate directory fingerprint."""
        repo = Path(repo_path)
        elements = []
        
        for item in sorted(repo.rglob('*')):
            if self._should_include(item):
                elements.append(str(item.relative_to(repo)))
        
        content = "\n".join(elements)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _should_include(self, path: Path) -> bool:
        """Check if path should be included."""
        excluded = ['__pycache__', '.git', 'node_modules', 'venv', '.venv']
        return not any(ex in str(path) for ex in excluded)


class TechnologyDetectionStage(PipelineStage):
    """Stage 2: Detect technologies."""
    
    name = "technology_detection"
    description = "Detect technologies used in repository"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Detect technologies."""
        result = StageResult()
        repo = Path(repo_path)
        
        technologies = {
            'languages': {},
            'frameworks': [],
            'build_systems': [],
            'runtimes': [],
            'databases': [],
        }
        
        # Detect by file patterns
        files = [f.name for f in repo.rglob('*') if f.is_file()]
        
        # Languages
        language_markers = {
            'Python': ['setup.py', 'requirements.txt', 'pyproject.toml', 'Pipfile'],
            'JavaScript': ['package.json', 'yarn.lock'],
            'TypeScript': ['tsconfig.json'],
            'Go': ['go.mod', 'go.sum'],
            'Rust': ['Cargo.toml', 'Cargo.lock'],
            'Java': ['pom.xml', 'build.gradle'],
            'C#': ['*.csproj', '*.sln'],
            'Ruby': ['Gemfile', 'Gemfile.lock'],
            'PHP': ['composer.json'],
            'Swift': ['Package.swift'],
            'Kotlin': ['build.gradle.kts'],
        }
        
        for lang, markers in language_markers.items():
            for marker in markers:
                if marker in files:
                    technologies['languages'][lang] = True
        
        # Frameworks
        framework_markers = {
            'Django': ['manage.py', 'settings.py'],
            'Flask': ['app.py', 'flask'],
            'FastAPI': ['fastapi'],
            'React': ['react'],
            'Vue': ['vue'],
            'Angular': ['angular'],
            'Express': ['express'],
            'Spring': ['spring'],
            'Next.js': ['next.config'],
            'Rails': ['config.ru'],
        }
        
        for framework, markers in framework_markers.items():
            for marker in markers:
                if marker in files:
                    technologies['frameworks'].append(framework)
        
        # Build systems
        build_markers = {
            'Make': ['Makefile'],
            'CMake': ['CMakeLists.txt'],
            'Gradle': ['build.gradle', 'gradlew'],
            'Maven': ['pom.xml'],
            'Webpack': ['webpack.config'],
            'Vite': ['vite.config'],
        }
        
        for build, markers in build_markers.items():
            for marker in markers:
                if marker in files:
                    technologies['build_systems'].append(build)
        
        # Runtimes
        if 'Dockerfile' in files:
            technologies['runtimes'].append('Docker')
        
        # Databases
        db_markers = {
            'PostgreSQL': ['postgres', 'postgresql'],
            'MySQL': ['mysql'],
            'MongoDB': ['mongodb', 'mongoose'],
            'Redis': ['redis'],
        }
        
        for db, markers in db_markers.items():
            if any(m in ' '.join(files) for m in markers):
                technologies['databases'].append(db)
        
        result.success = True
        result.data = technologies
        return result


class LanguageDetectionStage(PipelineStage):
    """Stage 3: Detect languages and calculate statistics."""
    
    name = "language_detection"
    description = "Detect programming languages and calculate statistics"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Detect languages."""
        result = StageResult()
        repo = Path(repo_path)
        
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.md': 'Markdown',
            '.sh': 'Shell',
        }
        
        languages = {}
        total_bytes = 0
        
        for py_file in repo.rglob('*'):
            if not py_file.is_file():
                continue
            if self._should_exclude(py_file):
                continue
            
            ext = py_file.suffix.lower()
            if ext in language_extensions:
                lang = language_extensions[ext]
                try:
                    size = py_file.stat().st_size
                    languages[lang] = languages.get(lang, 0) + size
                    total_bytes += size
                except Exception:
                    pass
        
        # Convert to percentages
        if total_bytes > 0:
            languages = {
                lang: round((bytes / total_bytes) * 100, 2)
                for lang, bytes in languages.items()
            }
        
        result.success = True
        result.data = {
            'languages': languages,
            'total_bytes': total_bytes,
            'primary_language': max(languages.items(), key=lambda x: x[1])[0] if languages else 'Unknown',
        }
        return result
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'node_modules', 'venv', '.venv', '.pytest_cache']
        return any(ex in str(path) for ex in excluded)


class DependencyResolutionStage(PipelineStage):
    """Stage 5: Resolve dependencies."""
    
    name = "dependency_resolution"
    description = "Resolve repository dependencies"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Resolve dependencies."""
        result = StageResult()
        repo = Path(repo_path)
        
        dependencies = {
            'total': 0,
            'direct': [],
            'dev': [],
            'internal': [],
        }
        
        # Python requirements.txt
        req_file = repo / 'requirements.txt'
        if req_file.exists():
            try:
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            dependencies['direct'].append(line)
            except Exception as e:
                result.warnings.append(f"Could not parse requirements.txt: {e}")
        
        # package.json
        pkg_file = repo / 'package.json'
        if pkg_file.exists():
            try:
                with open(pkg_file, 'r') as f:
                    pkg_data = json.load(f)
                    dependencies['direct'].extend(pkg_data.get('dependencies', {}).keys())
                    dependencies['dev'].extend(pkg_data.get('devDependencies', {}).keys())
            except Exception as e:
                result.warnings.append(f"Could not parse package.json: {e}")
        
        # Internal modules
        py_files = list(repo.rglob('__init__.py'))
        for init_file in py_files:
            module = init_file.parent.relative_to(repo)
            if module.name != '__pycache__':
                dependencies['internal'].append(str(module))
        
        dependencies['total'] = len(dependencies['direct']) + len(dependencies['dev'])
        
        result.success = True
        result.data = dependencies
        return result


class ArchitectureAnalysisStage(PipelineStage):
    """Stage 7: Analyze architecture."""
    
    name = "architecture_analysis"
    description = "Analyze repository architecture"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Analyze architecture."""
        result = StageResult()
        repo = Path(repo_path)
        
        architecture = {
            'modules': 0,
            'packages': 0,
            'classes': 0,
            'functions': 0,
            'patterns': [],
            'layers': [],
        }
        
        # Count modules
        init_files = list(repo.rglob('__init__.py'))
        architecture['modules'] = len(init_files)
        
        # Analyze Python files
        for py_file in repo.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        architecture['classes'] += 1
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        architecture['functions'] += 1
                        
            except Exception:
                pass
        
        # Detect patterns
        patterns = self._detect_patterns(repo)
        architecture['patterns'] = patterns
        
        result.success = True
        result.data = architecture
        return result
    
    def _detect_patterns(self, repo: Path) -> list:
        """Detect architectural patterns."""
        patterns = []
        files = [f.name for f in repo.rglob('*') if f.is_file()]
        
        pattern_markers = {
            'MVC': ['controller', 'model', 'view'],
            'Repository': ['repository', 'repo'],
            'Service': ['service', 'manager'],
            'Factory': ['factory', 'creator'],
            'Observer': ['observer', 'listener', 'subscriber'],
        }
        
        for pattern, markers in pattern_markers.items():
            if any(m.lower() in ' '.join(files).lower() for m in markers):
                patterns.append(pattern)
        
        return patterns
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_', '_test.py']
        return any(ex in str(path) for ex in excluded)


class CodeGraphConstructionStage(PipelineStage):
    """Stage 8: Construct code graph."""
    
    name = "code_graph_construction"
    description = "Construct code dependency graph"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Construct code graph."""
        result = StageResult()
        repo = Path(repo_path)
        
        graph = {
            'nodes': [],
            'edges': [],
            'imports': [],
        }
        
        for py_file in repo.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content, filename=str(py_file))
                
                file_node = {
                    'id': str(py_file.relative_to(repo)),
                    'type': 'file',
                    'classes': [],
                    'functions': [],
                }
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        file_node['classes'].append(node.name)
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        file_node['functions'].append(node.name)
                
                graph['nodes'].append(file_node)
                
                # Extract imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            graph['imports'].append({
                                'from': str(py_file.relative_to(repo)),
                                'import': node.module,
                            })
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            graph['imports'].append({
                                'from': str(py_file.relative_to(repo)),
                                'import': alias.name,
                            })
                            
            except Exception:
                pass
        
        result.success = True
        result.data = graph
        return result
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = ['__pycache__', '.git', 'venv', 'test_']
        return any(ex in str(path) for ex in excluded)


class EvidenceGenerationStage(PipelineStage):
    """Stage 11: Generate evidence."""
    
    name = "evidence_generation"
    description = "Generate immutable evidence"
    
    def process(self, repo_path: str, context: Dict) -> StageResult:
        """Generate evidence."""
        result = StageResult()
        
        import hashlib
        import uuid
        
        evidence = {
            'evidence_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'artifacts': [],
            'verifications': [],
            'signatures': [],
        }
        
        # Generate artifact hashes
        repo = Path(repo_path)
        for py_file in list(repo.rglob('*.py'))[:100]:  # Limit for performance
            try:
                with open(py_file, 'rb') as f:
                    content = f.read()
                    file_hash = hashlib.sha256(content).hexdigest()
                
                evidence['artifacts'].append({
                    'path': str(py_file.relative_to(repo)),
                    'hash': file_hash,
                    'size': len(content),
                })
            except Exception:
                pass
        
        # Generate repository signature
        repo_content = str(sorted([str(p) for p in repo.rglob('*') if p.is_file()]))
        evidence['signatures'].append(hashlib.sha256(repo_content.encode()).hexdigest())
        
        result.success = True
        result.data = evidence
        return result


from datetime import datetime
