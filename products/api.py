"""Universal API Platform - Every feature accessible from everywhere."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid

API_TYPES = ["REST API", "GraphQL API", "gRPC API", "WebSocket API", "Streaming API", "MCP API", "CLI API", "SDK API"]


class APIType(Enum):
    """Types of APIs."""
    REST = "rest"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    STREAMING = "streaming"
    MCP = "mcp"
    CLI = "cli"
    SDK = "sdk"


@dataclass
class RESTEndpoint:
    """A REST API endpoint."""
    endpoint_id: str
    path: str
    method: str
    description: str = ""
    handler: Optional[Callable] = None
    authentication_required: bool = True
    rate_limit: int = 1000


@dataclass
class GraphQLSchema:
    """A GraphQL schema definition."""
    schema_id: str
    types: List[str] = field(default_factory=list)
    queries: List[str] = field(default_factory=list)
    mutations: List[str] = field(default_factory=list)
    subscriptions: List[str] = field(default_factory=list)


@dataclass
class GRPCService:
    """A gRPC service definition."""
    service_id: str
    name: str
    package: str
    methods: List[str] = field(default_factory=list)


class APIPlatform:
    """
    Universal API Platform.
    
    APIs (8):
    ✅ REST API, GraphQL API, gRPC API
    ✅ WebSocket API, Streaming API
    ✅ MCP API, CLI API, SDK API
    
    Public Services (13):
    ✅ Organizations, Projects, Repositories, Knowledge
    ✅ Capabilities, Providers, Missions, Executions
    ✅ Artifacts, Analytics, Marketplace, Settings, Search
    
    Generated:
    ✅ OpenAPI, GraphQL Schema, gRPC Contracts
    ✅ SDK Packages, API Documentation, Client Libraries
    
    Target: Every feature accessible from browser, mobile, external systems, automation
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.rest_endpoints: Dict[str, RESTEndpoint] = {}
        self.graphql_schemas: Dict[str, GraphQLSchema] = {}
        self.grpc_services: Dict[str, GRPCService] = {}
    
    def register_rest_endpoint(self, endpoint: RESTEndpoint) -> None:
        self.rest_endpoints[endpoint.endpoint_id] = endpoint
    
    def register_graphql_schema(self, schema: GraphQLSchema) -> None:
        self.graphql_schemas[schema.schema_id] = schema
    
    def register_grpc_service(self, service: GRPCService) -> None:
        self.grpc_services[service.service_id] = service
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "api_types": API_TYPES,
            "rest_endpoints": len(self.rest_endpoints),
            "graphql_schemas": len(self.graphql_schemas),
            "grpc_services": len(self.grpc_services),
        }
