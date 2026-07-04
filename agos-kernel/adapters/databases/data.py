"""Database Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000029: PostgreSQL Adapter
class PostgreSQLAdapter(Adapter):
    """PostgreSQL database adapter."""
    
    def __init__(self):
        super().__init__("PostgreSQL", "postgresql", "PostgreSQL Database")
        self.metadata.auth_types = ["password", "certificate", " IAM"]
        self.metadata.capabilities = ["query", "backup", "replicate"]


# ADAPTER-000030: MySQL Adapter
class MySQLAdapter(Adapter):
    """MySQL database adapter."""
    
    def __init__(self):
        super().__init__("MySQL", "mysql", "MySQL Database")
        self.metadata.auth_types = ["password", "certificate"]
        self.metadata.capabilities = ["query", "backup", "replicate"]


# ADAPTER-000031: MariaDB Adapter
class MariaDBAdapter(Adapter):
    """MariaDB database adapter."""
    
    def __init__(self):
        super().__init__("MariaDB", "mariadb", "MariaDB Database")
        self.metadata.capabilities = ["query", "backup"]


# ADAPTER-000032: SQLite Adapter
class SQLiteAdapter(Adapter):
    """SQLite database adapter."""
    
    def __init__(self):
        super().__init__("SQLite", "sqlite", "SQLite Database")
        self.metadata.auth_types = ["none"]


# ADAPTER-000033: MongoDB Adapter
class MongoDBAdapter(Adapter):
    """MongoDB database adapter."""
    
    def __init__(self):
        super().__init__("MongoDB", "mongodb", "MongoDB Document Database")
        self.metadata.auth_types = ["password", "certificate"]
        self.metadata.capabilities = ["find", "insert", "update", "aggregate"]


# ADAPTER-000034: Redis Adapter
class RedisAdapter(Adapter):
    """Redis cache adapter."""
    
    def __init__(self):
        super().__init__("Redis", "redis", "Redis In-Memory Database")
        self.metadata.auth_types = ["password"]
        self.metadata.capabilities = ["get", "set", "publish", "subscribe"]


# ADAPTER-000035: Elasticsearch Adapter
class ElasticsearchAdapter(Adapter):
    """Elasticsearch adapter."""
    
    def __init__(self):
        super().__init__("Elasticsearch", "elasticsearch", "Elasticsearch Search Engine")
        self.metadata.capabilities = ["search", "index", "aggregate"]


# ADAPTER-000036: Neo4j Adapter
class Neo4jAdapter(Adapter):
    """Neo4j graph database adapter."""
    
    def __init__(self):
        super().__init__("Neo4j", "neo4j", "Neo4j Graph Database")
        self.metadata.capabilities = ["cypher", "graph_traverse"]


# Registry
DATABASE_ADAPTERS = {
    "postgresql": PostgreSQLAdapter,
    "mysql": MySQLAdapter,
    "mariadb": MariaDBAdapter,
    "sqlite": SQLiteAdapter,
    "mongodb": MongoDBAdapter,
    "redis": RedisAdapter,
    "elasticsearch": ElasticsearchAdapter,
    "neo4j": Neo4jAdapter,
}


def get_adapter(name: str):
    """Get a database adapter."""
    adapter_class = DATABASE_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()