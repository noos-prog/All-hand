"""
AGOS Adapters Module
====================

Adapters for external systems and integrations.
Provides interfaces for:
- Containers (Docker, Kubernetes)
- Databases (SQL, NoSQL)
- Messaging (Queues, Streams)
- Storage (Object, File)
- Source Control (Git)
- AI Providers
- Infrastructure (Cloud)
"""

from .base import Adapter, AdapterConfig, AdapterStatus

# Container adapters
try:
    from .containers.docker import DockerAdapter
except ImportError:
    DockerAdapter = None

try:
    from .containers.kubernetes import KubernetesAdapter
except ImportError:
    KubernetesAdapter = None

# Database adapters
try:
    from .databases.postgresql import PostgreSQLAdapter
except ImportError:
    PostgreSQLAdapter = None

try:
    from .databases.mongodb import MongoDBAdapter
except ImportError:
    MongoDBAdapter = None

try:
    from .databases.redis import RedisAdapter
except ImportError:
    RedisAdapter = None

# Messaging adapters
try:
    from .messaging.kafka import KafkaAdapter
except ImportError:
    KafkaAdapter = None

try:
    from .messaging.rabbitmq import RabbitMQAdapter
except ImportError:
    RabbitMQAdapter = None

# Storage adapters
try:
    from .storage.s3 import S3Adapter
except ImportError:
    S3Adapter = None

# Source control adapters
try:
    from .source_control.github import GitHubAdapter
except ImportError:
    GitHubAdapter = None

try:
    from .source_control.gitlab import GitLabAdapter
except ImportError:
    GitLabAdapter = None

# AI adapters
try:
    from .ai.openai import OpenAIAdapter
except ImportError:
    OpenAIAdapter = None

__all__ = [
    # Base
    "Adapter",
    "AdapterConfig",
    "AdapterStatus",
    # Containers
    "DockerAdapter",
    "KubernetesAdapter",
    # Databases
    "PostgreSQLAdapter",
    "MongoDBAdapter",
    "RedisAdapter",
    # Messaging
    "KafkaAdapter",
    "RabbitMQAdapter",
    # Storage
    "S3Adapter",
    # Source Control
    "GitHubAdapter",
    "GitLabAdapter",
    # AI
    "OpenAIAdapter",
]
