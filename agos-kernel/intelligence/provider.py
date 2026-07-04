"""Universal Provider Discovery Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class ProviderProfile:
    """Profile of an infrastructure provider."""
    id: str
    name: str
    type: str  # api, database, queue, storage, etc.
    category: str  # rest, graphql, mcp, cli, container
    endpoint: Optional[str] = None
    base_url: Optional[str] = None
    authentication: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    health_endpoint: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderContract:
    """Contract definition for a provider."""
    name: str
    provider_id: str
    version: str = "1.0.0"
    schema: Dict[str, Any] = field(default_factory=dict)
    endpoints: List[str] = field(default_factory=list)
    authentication_methods: List[str] = field(default_factory=list)
    rate_limits: Dict[str, int] = field(default_factory=dict)


@dataclass
class ProviderHealth:
    """Health status of a provider."""
    provider_id: str
    status: str  # healthy, degraded, down, unknown
    latency_ms: float = 0.0
    last_check: datetime = field(default_factory=datetime.now)
    uptime_percentage: float = 100.0
    errors: List[str] = field(default_factory=list)


@dataclass
class ProviderBenchmark:
    """Performance benchmark for a provider."""
    provider_id: str
    operation: str
    latency_ms: float = 0.0
    throughput_rps: float = 0.0
    error_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProviderDiscoveryEngine:
    """Discovers infrastructure providers in repositories."""
    
    # REST API patterns
    REST_PATTERNS = [
        'api', 'rest', 'http', 'client', 'endpoint',
        'requests', 'axios', 'fetch', 'urllib', 'httpx'
    ]
    
    # GraphQL patterns
    GRAPHQL_PATTERNS = [
        'graphql', 'gql', 'apollo', 'hasura'
    ]
    
    # MCP Server patterns
    MCP_PATTERNS = [
        'mcp', 'model context protocol', 'mcp-server',
        'mcp_client', 'mcp-server'
    ]
    
    # CLI patterns
    CLI_PATTERNS = [
        'subprocess', 'click', 'argparse', 'typer', 'commander',
        'yargs', 'oclif'
    ]
    
    # Container patterns
    CONTAINER_PATTERNS = [
        'docker', 'podman', 'container', 'docker-compose',
        'kubernetes', 'k8s', 'helm'
    ]
    
    # Database patterns
    DATABASE_PATTERNS = [
        'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'postgres', 'sqlite', 'dynamodb', 'cassandra'
    ]
    
    # Queue patterns
    QUEUE_PATTERNS = [
        'rabbitmq', 'kafka', 'sqs', 'nats', 'pubsub',
        'redis-queue', 'celery'
    ]
    
    # Storage patterns
    STORAGE_PATTERNS = [
        's3', 'gcs', 'azure-blob', 'minio', 'local-storage',
        'file-storage', 'bucket'
    ]
    
    # Auth patterns
    AUTH_PATTERNS = [
        'oauth', 'jwt', 'bearer', 'api-key', 'api_key',
        'basic-auth', 'auth0', 'okta'
    ]
    
    def __init__(self, root_path: str):
        """Initialize discovery engine."""
        self.root_path = Path(root_path)
        self.providers: List[ProviderProfile] = []
    
    def discover(self) -> List[ProviderProfile]:
        """Discover all providers."""
        self._discover_rest_apis()
        self._discover_graphql_apis()
        self._discover_mcp_servers()
        self._discover_cli_programs()
        self._discover_containers()
        self._discover_databases()
        self._discover_message_queues()
        self._discover_storage()
        self._discover_auth_providers()
        return self.providers
    
    def _discover_rest_apis(self) -> None:
        """Discover REST APIs."""
        config_files = [
            'package.json',  # npm packages with REST clients
            'requirements.txt',  # Python HTTP libraries
            'pom.xml',  # Java HTTP clients
        ]
        
        rest_libraries = [
            'requests', 'httpx', 'axios', 'fetch', 'urllib',
            'aiohttp', 'fastapi', 'express', 'rest-framework'
        ]
        
        # Check configuration files
        for config_file in config_files:
            config_path = self.root_path / config_file
            if config_path.exists():
                content = config_path.read_text()
                for lib in rest_libraries:
                    if lib.lower() in content.lower():
                        self.providers.append(ProviderProfile(
                            id=f"rest_{len(self.providers)}",
                            name=f"REST: {lib}",
                            type="api",
                            category="rest",
                            capabilities=['http', 'rest'],
                            metadata={'library': lib}
                        ))
        
        # Check source code
        for path in self.root_path.rglob('*.py'):
            try:
                content = path.read_text(errors='ignore')
                for lib in rest_libraries:
                    if lib.lower() in content.lower():
                        provider_id = f"rest_{lib}"
                        if not any(p.id == provider_id for p in self.providers):
                            self.providers.append(ProviderProfile(
                                id=provider_id,
                                name=f"REST API: {lib}",
                                type="api",
                                category="rest",
                                capabilities=['http', 'rest'],
                                configuration={'source': str(path.relative_to(self.root_path))}
                            ))
            except:
                pass
    
    def _discover_graphql_apis(self) -> None:
        """Discover GraphQL APIs."""
        graphql_libraries = [
            'graphql', 'gql', 'apollo', 'hasura', 'strawberry',
            'graphene', 'ariadne'
        ]
        
        for path in self.root_path.rglob('*.py'):
            try:
                content = path.read_text(errors='ignore')
                for lib in graphql_libraries:
                    if lib.lower() in content.lower():
                        provider_id = f"graphql_{lib}"
                        if not any(p.id == provider_id for p in self.providers):
                            self.providers.append(ProviderProfile(
                                id=provider_id,
                                name=f"GraphQL: {lib}",
                                type="api",
                                category="graphql",
                                capabilities=['graphql', 'query', 'mutation', 'subscription']
                            ))
            except:
                pass
        
        # Check for schema files
        for path in self.root_path.rglob('schema.graphql'):
            self.providers.append(ProviderProfile(
                id=f"graphql_schema_{len(self.providers)}",
                name="GraphQL Schema",
                type="api",
                category="graphql",
                endpoint=str(path.relative_to(self.root_path)),
                capabilities=['schema']
            ))
    
    def _discover_mcp_servers(self) -> None:
        """Discover MCP Servers."""
        mcp_keywords = ['mcp', 'model context protocol', 'mcp-server']
        
        for path in self.root_path.rglob('*'):
            try:
                if path.is_file():
                    content = path.read_text(errors='ignore')
                    for keyword in mcp_keywords:
                        if keyword in content.lower():
                            self.providers.append(ProviderProfile(
                                id=f"mcp_{len(self.providers)}",
                                name=f"MCP Server: {path.stem}",
                                type="server",
                                category="mcp",
                                endpoint=str(path.relative_to(self.root_path)),
                                capabilities=['mcp', 'tool', 'resource']
                            ))
                            break
            except:
                pass
    
    def _discover_cli_programs(self) -> None:
        """Discover CLI programs."""
        cli_libraries = ['click', 'typer', 'argparse', 'commander', 'yargs', 'oclif']
        
        for path in self.root_path.rglob('*.py'):
            try:
                content = path.read_text(errors='ignore')
                for lib in cli_libraries:
                    if lib in content:
                        self.providers.append(ProviderProfile(
                            id=f"cli_{lib}_{len(self.providers)}",
                            name=f"CLI: {lib}",
                            type="program",
                            category="cli",
                            endpoint=str(path.relative_to(self.root_path)),
                            capabilities=['cli', 'command']
                        ))
                        break
            except:
                pass
    
    def _discover_containers(self) -> None:
        """Discover container technologies."""
        container_files = {
            'Dockerfile': 'docker',
            'docker-compose.yml': 'docker',
            'docker-compose.yaml': 'docker',
            'Containerfile': 'podman',
            'podman.yml': 'podman',
        }
        
        for filename, container_type in container_files.items():
            for path in self.root_path.rglob(filename):
                self.providers.append(ProviderProfile(
                    id=f"container_{container_type}_{len(self.providers)}",
                    name=f"{container_type.title()} Container",
                    type="container",
                    category=container_type,
                    endpoint=str(path.relative_to(self.root_path)),
                    capabilities=['container', 'orchestration']
                ))
        
        # Kubernetes
        k8s_patterns = ['kubernetes/', 'k8s/', 'Chart.yaml', 'values.yaml']
        for pattern in k8s_patterns:
            for path in self.root_path.rglob(pattern):
                if path.is_dir() or path.name == 'Chart.yaml' or path.name == 'values.yaml':
                    self.providers.append(ProviderProfile(
                        id=f"k8s_{len(self.providers)}",
                        name="Kubernetes",
                        type="orchestration",
                        category="kubernetes",
                        capabilities=['orchestration', 'deployment', 'scaling']
                    ))
                    break
    
    def _discover_databases(self) -> None:
        """Discover databases."""
        db_libraries = {
            'psycopg2': ('postgresql', 'PostgreSQL'),
            'pg': ('postgresql', 'PostgreSQL'),
            'mysql': ('mysql', 'MySQL'),
            'pymongo': ('mongodb', 'MongoDB'),
            'mongoose': ('mongodb', 'MongoDB'),
            'redis': ('redis', 'Redis'),
            'ioredis': ('redis', 'Redis'),
            'elasticsearch': ('elasticsearch', 'Elasticsearch'),
            'sqlalchemy': ('sqlalchemy', 'SQLAlchemy'),
            'prisma': ('prisma', 'Prisma'),
        }
        
        for path in self.root_path.rglob('*'):
            if path.suffix in ['.py', '.js', '.ts', '.json']:
                try:
                    content = path.read_text(errors='ignore')
                    for lib, (db_type, db_name) in db_libraries.items():
                        if lib in content.lower():
                            provider_id = f"db_{db_type}"
                            if not any(p.id == provider_id for p in self.providers):
                                self.providers.append(ProviderProfile(
                                    id=provider_id,
                                    name=f"Database: {db_name}",
                                    type="database",
                                    category=db_type,
                                    capabilities=['storage', 'query']
                                ))
                except:
                    pass
        
        # Check config files for database URLs
        for path in self.root_path.rglob('*.env*'):
            try:
                content = path.read_text(errors='ignore')
                if 'DATABASE_URL' in content or 'DB_' in content:
                    self.providers.append(ProviderProfile(
                        id=f"db_config_{len(self.providers)}",
                        name="Database (configured via env)",
                        type="database",
                        category="configured",
                        capabilities=['storage']
                    ))
            except:
                pass
    
    def _discover_message_queues(self) -> None:
        """Discover message queues."""
        queue_libraries = {
            'pika': ('rabbitmq', 'RabbitMQ'),
            'aiormq': ('rabbitmq', 'RabbitMQ'),
            'kafka': ('kafka', 'Apache Kafka'),
            'confluent_kafka': ('kafka', 'Confluent Kafka'),
            'redis': ('redis-queue', 'Redis Queue'),
            'celery': ('celery', 'Celery'),
            'nats': ('nats', 'NATS'),
            'boto3': ('sqs', 'AWS SQS'),
        }
        
        for path in self.root_path.rglob('*'):
            if path.suffix in ['.py', '.js', '.ts', '.json']:
                try:
                    content = path.read_text(errors='ignore')
                    for lib, (queue_type, queue_name) in queue_libraries.items():
                        if lib.lower() in content.lower():
                            provider_id = f"queue_{queue_type}"
                            if not any(p.id == provider_id for p in self.providers):
                                self.providers.append(ProviderProfile(
                                    id=provider_id,
                                    name=f"Queue: {queue_name}",
                                    type="queue",
                                    category=queue_type,
                                    capabilities=['messaging', 'pub_sub']
                                ))
                except:
                    pass
    
    def _discover_storage(self) -> None:
        """Discover storage providers."""
        storage_libraries = {
            'boto3': ('s3', 'AWS S3'),
            'google-cloud-storage': ('gcs', 'Google Cloud Storage'),
            'azure-storage': ('azure-blob', 'Azure Blob'),
            'minio': ('minio', 'MinIO'),
        }
        
        for path in self.root_path.rglob('*'):
            if path.suffix in ['.py', '.js', '.ts', '.json']:
                try:
                    content = path.read_text(errors='ignore')
                    for lib, (storage_type, storage_name) in storage_libraries.items():
                        if lib.lower() in content.lower():
                            provider_id = f"storage_{storage_type}"
                            if not any(p.id == provider_id for p in self.providers):
                                self.providers.append(ProviderProfile(
                                    id=provider_id,
                                    name=f"Storage: {storage_name}",
                                    type="storage",
                                    category=storage_type,
                                    capabilities=['storage', 'files']
                                ))
                except:
                    pass
    
    def _discover_auth_providers(self) -> None:
        """Discover authentication providers."""
        auth_libraries = {
            'auth0': ('auth0', 'Auth0'),
            'okta': ('okta', 'Okta'),
            'firebase-auth': ('firebase', 'Firebase Auth'),
            'passport': ('passport', 'Passport.js'),
            'jwt': ('jwt', 'JWT'),
            'pyjwt': ('jwt', 'JWT (Python)'),
            'oauth': ('oauth', 'OAuth'),
        }
        
        for path in self.root_path.rglob('*'):
            if path.suffix in ['.py', '.js', '.ts', '.json']:
                try:
                    content = path.read_text(errors='ignore')
                    for lib, (auth_type, auth_name) in auth_libraries.items():
                        if lib.lower() in content.lower():
                            provider_id = f"auth_{auth_type}"
                            if not any(p.id == provider_id for p in self.providers):
                                self.providers.append(ProviderProfile(
                                    id=provider_id,
                                    name=f"Auth: {auth_name}",
                                    type="auth",
                                    category=auth_type,
                                    capabilities=['authentication', 'authorization']
                                ))
                except:
                    pass
    
    def get_providers_by_type(self, provider_type: str) -> List[ProviderProfile]:
        """Get providers filtered by type."""
        return [p for p in self.providers if p.type == provider_type]
    
    def get_providers_by_category(self, category: str) -> List[ProviderProfile]:
        """Get providers filtered by category."""
        return [p for p in self.providers if p.category == category]
    
    def create_contract(self, provider: ProviderProfile) -> ProviderContract:
        """Create a contract for a provider."""
        return ProviderContract(
            name=provider.name,
            provider_id=provider.id,
            version="1.0.0",
            endpoints=provider.capabilities,
            authentication_methods=list(provider.authentication.keys())
        )
