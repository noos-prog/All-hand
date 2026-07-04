"""Repository Analyzer - Analyzes repository structure and detects technologies."""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from .models import (
    Language, Framework, BuildSystem, ContainerTech, CloudProvider,
    Database, Queue, DirectoryNode, Module, RepositoryGenome, RepositoryMetrics,
    FileMetrics
)


class RepositoryAnalyzer:
    """Analyzes repository structure and technologies."""
    
    # File extension to language mapping
    EXTENSION_MAP = {
        '.py': Language.PYTHON,
        '.js': Language.JAVASCRIPT,
        '.ts': Language.TYPESCRIPT,
        '.tsx': Language.TYPESCRIPT,
        '.jsx': Language.JAVASCRIPT,
        '.java': Language.JAVA,
        '.kt': Language.KOTLIN,
        '.swift': Language.SWIFT,
        '.go': Language.GO,
        '.rs': Language.RUST,
        '.c': Language.C,
        '.cpp': Language.CPP,
        '.cc': Language.CPP,
        '.cs': Language.CSHARP,
        '.rb': Language.RUBY,
        '.php': Language.PHP,
        '.scala': Language.SCALA,
        '.hs': Language.HASKELL,
        '.sh': Language.SHELL,
        '.bash': Language.SHELL,
        '.zsh': Language.SHELL,
        '.dockerfile': Language.DOCKERFILE,
        'Dockerfile': Language.DOCKERFILE,
    }
    
    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        Framework.DJANGO: ['settings.py', 'manage.py', 'django'],
        Framework.FLASK: ['flask', 'app.route', '@app.route'],
        Framework.FASTAPI: ['fastapi', 'uvicorn'],
        Framework.REACT: ['react', 'React', 'create-react-app'],
        Framework.VUE: ['vue', 'Vue', 'vue-cli'],
        Framework.ANGULAR: ['angular', '@angular'],
        Framework.NEXTJS: ['next', 'next.config', 'getServerSideProps'],
        Framework.NESTJS: ['@nestjs', 'nest-cli.json'],
        Framework.SPRING: ['spring', 'SpringBootApplication', '@SpringBootApplication'],
        Framework.EXPRESS: ['express', 'express()', 'app.use(express)'],
        Framework.FASTIFY: ['fastify'],
        Framework.GIN: ['gin-gonic', 'gin.Run'],
        Framework.FLUTTER: ['flutter', 'pubspec.yaml'],
    }
    
    # Build system files
    BUILD_FILES = {
        'package.json': (BuildSystem.NPM, 'node_modules'),
        'yarn.lock': (BuildSystem.YARN, 'node_modules'),
        'pnpm-lock.yaml': (BuildSystem.PNPM, 'node_modules'),
        'pyproject.toml': (BuildSystem.POETRY, '__pycache__'),
        'requirements.txt': (BuildSystem.PIP, '__pycache__'),
        'Pipfile': (BuildSystem.PIP, '__pycache__'),
        'pom.xml': (BuildSystem.MAVEN, 'target'),
        'build.gradle': (BuildSystem.GRADLE, 'build'),
        'build.gradle.kts': (BuildSystem.GRADLE, 'build'),
        'Cargo.toml': (BuildSystem.CARGO, 'target'),
        'CMakeLists.txt': (BuildSystem.CMAKE, 'build'),
        'Makefile': (BuildSystem.UNKNOWN, None),
    }
    
    # Test framework patterns
    TEST_PATTERNS = {
        'pytest': ['pytest.ini', 'conftest.py', 'test_', '_test.py'],
        'unittest': ['unittest', 'TestCase'],
        'jest': ['jest.config', '.test.', '.spec.'],
        'mocha': ['mocha', '.spec.', '.test.'],
        'junit': ['junit', 'TestSuite'],
        'rspec': ['rspec', '_spec.rb'],
    }
    
    # CI/CD system files
    CI_FILES = {
        '.github/workflows': 'github_actions',
        '.gitlab-ci.yml': 'gitlab_ci',
        'Jenkinsfile': 'jenkins',
        'Jenkinsfile': 'jenkins',
        '.circleci/config.yml': 'circleci',
        '.travis.yml': 'travis',
        '.bitbucket-pipelines.yml': 'bitbucket_pipelines',
        'azure-pipelines.yml': 'azure_devops',
    }
    
    # Container files
    CONTAINER_FILES = {
        'Dockerfile': ContainerTech.DOCKER,
        'docker-compose.yml': ContainerTech.DOCKER,
        'docker-compose.yaml': ContainerTech.DOCKER,
        'podman.yml': ContainerTech.PODMAN,
        'kubernetes/': ContainerTech.KUBERNETES,
        'k8s/': ContainerTech.KUBERNETES,
        'Chart.yaml': ContainerTech.HELM,
    }
    
    # Cloud provider indicators
    CLOUD_FILES = {
        'aws/': CloudProvider.AWS,
        '.aws/': CloudProvider.AWS,
        'azure/': CloudProvider.AZURE,
        '.azure/': CloudProvider.AZURE,
        'gcp/': CloudProvider.GCP,
        '.gcp/': CloudProvider.GCP,
        'vercel.json': CloudProvider.VERCEL,
        'netlify.toml': CloudProvider.UNKNOWN,  # Generic
        'Procfile': CloudProvider.HEROKU,
    }
    
    # Database indicators
    DB_PATTERNS = {
        'postgresql': ['postgres', 'postgresql', 'psycopg2'],
        'mysql': ['mysql', 'mysql2'],
        'mongodb': ['mongodb', 'mongoose', 'pymongo'],
        'redis': ['redis', 'ioredis', 'redis-py'],
        'elasticsearch': ['elasticsearch', 'elastic'],
        'cassandra': ['cassandra', 'scylla'],
        'neo4j': ['neo4j', 'py2neo'],
    }
    
    # Queue indicators
    QUEUE_PATTERNS = {
        'rabbitmq': ['amqp', 'pika', 'rabbitmq'],
        'kafka': ['kafka', 'confluent-kafka', 'kafka-python'],
        'sqs': ['boto3', 'sqs'],
        'nats': ['nats', 'nats-py'],
    }
    
    # Config file patterns
    CONFIG_PATTERNS = [
        r'\.json$', r'\.yaml$', r'\.yml$', r'\.toml$', r'\.ini$',
        r'\.conf$', r'\.config$', r'\.env$', r'\.editorconfig$',
        r'\.prettierrc', r'\.eslintrc', r'\.babelrc', r'\.webpack'
    ]
    
    # Directories to ignore
    IGNORE_DIRS = {
        'node_modules', '.git', '__pycache__', '.pytest_cache',
        '.mypy_cache', '.venv', 'venv', 'env', '.venv',
        'dist', 'build', 'target', '.idea', '.vscode',
        '.sass-cache', '.next', '.nuxt', '.cache'
    }
    
    def __init__(self, root_path: str):
        """Initialize analyzer with repository root path."""
        self.root_path = Path(root_path)
        self.genome = RepositoryGenome(
            name=self.root_path.name,
            path=str(self.root_path),
            root_path=str(self.root_path)
        )
    
    def analyze(self) -> RepositoryGenome:
        """Run complete analysis."""
        self._analyze_structure()
        self._detect_languages()
        self._detect_frameworks()
        self._detect_build_systems()
        self._detect_package_managers()
        self._detect_test_frameworks()
        self._detect_ci_cd()
        self._detect_containers()
        self._detect_cloud_providers()
        self._detect_databases()
        self._detect_queues()
        self._calculate_metrics()
        return self.genome
    
    def _analyze_structure(self) -> None:
        """Analyze directory structure."""
        directories = []
        modules = []
        max_depth = 0
        
        for root, dirs, files in os.walk(self.root_path):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            rel_root = Path(root).relative_to(self.root_path)
            depth = len(rel_root.parts)
            max_depth = max(max_depth, depth)
            
            # Create directory node
            dir_node = DirectoryNode(
                path=str(rel_root),
                name=Path(root).name,
                is_dir=True,
                depth=depth
            )
            directories.append(dir_node)
            
            # Classify files
            for f in files:
                file_path = Path(root) / f
                rel_path = str(file_path.relative_to(self.root_path))
                
                if f in ['package.json', 'setup.py', 'pyproject.toml', 
                         'Cargo.toml', 'go.mod', 'pom.xml']:
                    modules.append(Module(
                        path=rel_path,
                        name=f,
                        type='root',
                        files=[rel_path]
                    ))
        
        self.genome.directories = directories
        self.genome.modules = modules
        self.genome.metrics.depth = max_depth
    
    def _detect_languages(self) -> None:
        """Detect programming languages."""
        languages: Dict[str, int] = {}
        
        for dirpath, _, files in os.walk(self.root_path):
            if any(ignored in dirpath for ignored in self.IGNORE_DIRS):
                continue
                
            for f in files:
                ext = os.path.splitext(f)[1]
                lang = self.EXTENSION_MAP.get(ext)
                if lang:
                    lang_key = lang.value
                    languages[lang_key] = languages.get(lang_key, 0) + 1
                    # Use os.path for path operations
                    full_path = os.path.join(dirpath, f)
                    rel_path = os.path.relpath(full_path, self.root_path)
                    self.genome.source_files.append(rel_path)
        
        self.genome.languages = {Language(l) for l in languages.keys()}
        self.genome.metrics.languages = languages
    
    def _detect_frameworks(self) -> None:
        """Detect frameworks."""
        detected = set()
        
        # Check package.json for JS frameworks
        pkg_json = self.root_path / 'package.json'
        if pkg_json.exists():
            content = pkg_json.read_text()
            for framework, keywords in self.FRAMEWORK_PATTERNS.items():
                if any(k in content for k in keywords):
                    detected.add(framework)
        
        # Check files for Python frameworks
        for root, _, files in os.walk(self.root_path):
            for f in files:
                if f.endswith('.py'):
                    try:
                        content = (Path(root) / f).read_text(errors='ignore')
                        for framework, keywords in self.FRAMEWORK_PATTERNS.items():
                            if any(k in content for k in keywords):
                                detected.add(framework)
                    except:
                        pass
        
        self.genome.frameworks = detected
    
    def _detect_build_systems(self) -> None:
        """Detect build systems."""
        detected = set()
        
        for build_file, (system, _) in self.BUILD_FILES.items():
            if (self.root_path / build_file).exists():
                detected.add(system)
        
        self.genome.build_systems = detected
    
    def _detect_package_managers(self) -> None:
        """Detect package managers."""
        managers = set()
        
        # Python
        if (self.root_path / 'requirements.txt').exists():
            managers.add('pip')
        if (self.root_path / 'pyproject.toml').exists():
            managers.add('poetry')
        
        # JavaScript
        if (self.root_path / 'package.json').exists():
            managers.add('npm')
            if (self.root_path / 'yarn.lock').exists():
                managers.add('yarn')
            if (self.root_path / 'pnpm-lock.yaml').exists():
                managers.add('pnpm')
        
        self.genome.package_managers = managers
    
    def _detect_test_frameworks(self) -> None:
        """Detect test frameworks."""
        detected = set()
        
        for root, _, files in os.walk(self.root_path):
            for f in files:
                for framework, patterns in self.TEST_PATTERNS.items():
                    if any(p in f or p in f for p in patterns):
                        detected.add(framework)
        
        self.genome.test_frameworks = detected
    
    def _detect_ci_cd(self) -> None:
        """Detect CI/CD systems."""
        detected = set()
        
        for path, system in self.CI_FILES.items():
            if (self.root_path / path).exists():
                detected.add(system)
        
        self.genome.ci_cd_systems = detected
    
    def _detect_containers(self) -> None:
        """Detect container technologies."""
        detected = set()
        
        for path, tech in self.CONTAINER_FILES.items():
            if '/' in path:
                if any(p.exists() for p in self.root_path.rglob(path.split('/')[0])):
                    detected.add(tech)
            else:
                if (self.root_path / path).exists():
                    detected.add(tech)
        
        self.genome.container_tech = detected
    
    def _detect_cloud_providers(self) -> None:
        """Detect cloud providers."""
        detected = set()
        
        for path, provider in self.CLOUD_FILES.items():
            if '/' in path:
                if any(p.exists() for p in self.root_path.rglob(path.split('/')[0])):
                    detected.add(provider)
            else:
                if (self.root_path / path).exists():
                    detected.add(provider)
        
        self.genome.cloud_providers = detected
    
    def _detect_databases(self) -> None:
        """Detect databases."""
        detected = set()
        
        for root, _, files in os.walk(self.root_path):
            for f in files:
                if f.endswith(('.py', '.js', '.ts', '.json')):
                    try:
                        content = (Path(root) / f).read_text(errors='ignore')
                        for db, keywords in self.DB_PATTERNS.items():
                            if any(k in content.lower() for k in keywords):
                                detected.add(Database(db))
                    except:
                        pass
        
        self.genome.databases = detected
    
    def _detect_queues(self) -> None:
        """Detect message queues."""
        detected = set()
        
        for root, _, files in os.walk(self.root_path):
            for f in files:
                if f.endswith(('.py', '.js', '.ts', '.json')):
                    try:
                        content = (Path(root) / f).read_text(errors='ignore')
                        for queue, keywords in self.QUEUE_PATTERNS.items():
                            if any(k in content.lower() for k in keywords):
                                detected.add(Queue(queue))
                    except:
                        pass
        
        self.genome.queues = detected
    
    def _calculate_metrics(self) -> None:
        """Calculate repository metrics."""
        total_files = 0
        total_lines = 0
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        largest_files = []
        
        for dirpath, _, files in os.walk(self.root_path):
            if any(ignored in dirpath for ignored in self.IGNORE_DIRS):
                continue
                
            for f in files:
                full_path = os.path.join(dirpath, f)
                total_files += 1
                
                try:
                    with open(full_path, 'r', errors='ignore') as file:
                        lines = file.readlines()
                        lines_count = len(lines)
                        total_lines += lines_count
                        
                        # Find largest files
                        rel_path = os.path.relpath(full_path, self.root_path)
                        largest_files.append((rel_path, lines_count))
                        
                        # Count code, comments, blanks
                        in_block_comment = False
                        for line in lines:
                            stripped = line.strip()
                            if not stripped:
                                blank_lines += 1
                            elif stripped.startswith('#') or stripped.startswith('//'):
                                comment_lines += 1
                            elif stripped.startswith('/*') or stripped.startswith('"""'):
                                comment_lines += 1
                                in_block_comment = True
                            elif in_block_comment:
                                comment_lines += 1
                                if '"""' in stripped or '*/' in stripped:
                                    in_block_comment = False
                            else:
                                code_lines += 1
                except:
                    pass
        
        # Get top 10 largest files
        largest_files.sort(key=lambda x: x[1], reverse=True)
        
        self.genome.metrics = RepositoryMetrics(
            total_files=total_files,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            languages=self.genome.metrics.languages,
            largest_files=largest_files[:10],
            depth=self.genome.metrics.depth
        )
