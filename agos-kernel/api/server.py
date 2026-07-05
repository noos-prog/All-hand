"""
AGOS REST API Server
====================

REST API server for AGOS system.
Provides HTTP endpoints for kernel operations.
"""

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Route:
    """API route."""
    path: str
    method: HTTPMethod
    handler: Callable
    description: str = ""


@dataclass
class HTTPRequest:
    """HTTP request."""
    method: str
    path: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    query_params: Dict[str, str] = field(default_factory=dict)


@dataclass
class HTTPResponse:
    """HTTP response."""
    status_code: int
    body: Any
    headers: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "status_code": self.status_code,
            "body": self.body,
            "headers": self.headers,
        }


class APIServer:
    """
    AGOS REST API Server.
    
    Provides HTTP endpoints for:
    - Kernel operations
    - Registry operations
    - Workflow execution
    - Knowledge management
    
    Usage:
        server = APIServer(host="0.0.0.0", port=8080)
        server.start()
    """
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        enable_cors: bool = True,
    ):
        """Initialize API server."""
        self.host = host
        self.port = port
        self.enable_cors = enable_cors
        self.logger = logging.getLogger("agos.api.server")
        
        self._routes: Dict[str, Route] = {}
        self._running = False
        self._server_thread: Optional[threading.Thread] = None
        
        # Register default routes
        self._register_default_routes()
    
    def _register_default_routes(self) -> None:
        """Register default API routes."""
        
        # Health endpoints
        self.add_route("/health", HTTPMethod.GET, self._health_handler, "Health check")
        self.add_route("/health/ready", HTTPMethod.GET, self._ready_handler, "Readiness check")
        
        # Kernel endpoints
        self.add_route("/api/v1/kernel/start", HTTPMethod.POST, self._kernel_start_handler, "Start kernel")
        self.add_route("/api/v1/kernel/stop", HTTPMethod.POST, self._kernel_stop_handler, "Stop kernel")
        self.add_route("/api/v1/kernel/status", HTTPMethod.GET, self._kernel_status_handler, "Get kernel status")
        self.add_route("/api/v1/kernel/health", HTTPMethod.GET, self._kernel_health_handler, "Kernel health check")
        
        # Registry endpoints
        self.add_route("/api/v1/registry/components", HTTPMethod.GET, self._list_components_handler, "List components")
        self.add_route("/api/v1/registry/capabilities", HTTPMethod.GET, self._list_capabilities_handler, "List capabilities")
        self.add_route("/api/v1/registry/providers", HTTPMethod.GET, self._list_providers_handler, "List providers")
        self.add_route("/api/v1/registry/workflows", HTTPMethod.GET, self._list_workflows_handler, "List workflows")
        
        # Workflow endpoints
        self.add_route("/api/v1/workflows", HTTPMethod.GET, self._list_workflows_handler, "List workflows")
        self.add_route("/api/v1/workflows/execute", HTTPMethod.POST, self._execute_workflow_handler, "Execute workflow")
        self.add_route("/api/v1/workflows/{id}", HTTPMethod.GET, self._get_workflow_handler, "Get workflow")
        
        # Knowledge endpoints
        self.add_route("/api/v1/knowledge", HTTPMethod.GET, self._list_knowledge_handler, "List knowledge")
        self.add_route("/api/v1/knowledge", HTTPMethod.POST, self._create_knowledge_handler, "Create knowledge")
        self.add_route("/api/v1/knowledge/search", HTTPMethod.GET, self._search_knowledge_handler, "Search knowledge")
        
        # Mission endpoints
        self.add_route("/api/v1/missions", HTTPMethod.GET, self._list_missions_handler, "List missions")
        self.add_route("/api/v1/missions", HTTPMethod.POST, self._create_mission_handler, "Create mission")
        self.add_route("/api/v1/missions/{id}", HTTPMethod.GET, self._get_mission_handler, "Get mission")
    
    def add_route(
        self,
        path: str,
        method: HTTPMethod,
        handler: Callable,
        description: str = "",
    ) -> None:
        """Add a route."""
        route_key = f"{method.value}:{path}"
        self._routes[route_key] = Route(path, method, handler, description)
    
    def start(self) -> bool:
        """Start the API server."""
        if self._running:
            return False
        
        self._running = True
        self._server_thread = threading.Thread(target=self._run_server, daemon=True)
        self._server_thread.start()
        
        self.logger.info(f"API server starting on {self.host}:{self.port}")
        return True
    
    def stop(self) -> bool:
        """Stop the API server."""
        self._running = False
        self.logger.info("API server stopped")
        return True
    
    def _run_server(self) -> None:
        """Run the server (placeholder - would use HTTP server in production)."""
        # In a full implementation, this would use Flask/FastAPI/aiohttp
        # For now, just log that the server is running
        self.logger.info(f"Server running on {self.host}:{self.port}")
        
        # Keep thread alive
        import time
        while self._running:
            time.sleep(1)
    
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        """Handle an HTTP request."""
        route_key = f"{request.method}:{request.path}"
        route = self._routes.get(route_key)
        
        if not route:
            return HTTPResponse(
                status_code=404,
                body={"error": "Not found", "path": request.path},
            )
        
        try:
            result = route.handler(request)
            return HTTPResponse(status_code=200, body=result)
        except Exception as e:
            self.logger.error(f"Handler error: {e}")
            return HTTPResponse(
                status_code=500,
                body={"error": str(e)},
            )
    
    # === Default Handlers ===
    
    def _health_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Health check handler."""
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "agos-api",
            "version": "1.0.0",
        }
    
    def _ready_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Readiness check handler."""
        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _kernel_start_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Start kernel handler."""
        try:
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            result = kernel.start()
            return {
                "success": result,
                "status": kernel.status.value if result else "error",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _kernel_stop_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Stop kernel handler."""
        try:
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            result = kernel.shutdown()
            return {"success": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _kernel_status_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Get kernel status handler."""
        try:
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            state = kernel.get_state()
            return {
                "status": state.status.value if hasattr(state, 'status') else "unknown",
                "state": {
                    "components_registered": state.components_registered if hasattr(state, 'components_registered') else 0,
                    "workflows_executed": state.workflows_executed if hasattr(state, 'workflows_executed') else 0,
                }
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _kernel_health_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Kernel health check handler."""
        try:
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            return kernel.health_check()
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _list_components_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List components handler."""
        try:
            from registry.component import get_component_registry
            reg = get_component_registry()
            components = reg.list_all()
            return {
                "total": len(components),
                "components": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "type": c.component_type.value,
                    }
                    for c in components
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _list_capabilities_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List capabilities handler."""
        try:
            from registry.cap_registry import get_capability_registry
            reg = get_capability_registry()
            caps = reg.list_all()
            return {
                "total": len(caps),
                "capabilities": [
                    {"id": c.id, "name": c.name, "type": c.capability_type.value}
                    for c in caps
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _list_providers_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List providers handler."""
        try:
            from registry.provider_registry import get_provider_registry
            reg = get_provider_registry()
            provs = reg.list_all()
            return {
                "total": len(provs),
                "providers": [
                    {"id": p.id, "name": p.name, "type": p.provider_type.value}
                    for p in provs
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _list_workflows_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List workflows handler."""
        try:
            from registry.workflow_registry import get_workflow_registry
            reg = get_workflow_registry()
            wfs = reg.list_all()
            return {
                "total": len(wfs),
                "workflows": [
                    {"id": w.id, "name": w.name}
                    for w in wfs
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _execute_workflow_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Execute workflow handler."""
        try:
            workflow_id = request.body.get("workflow_id") if request.body else None
            params = request.body.get("params", {}) if request.body else {}
            
            if not workflow_id:
                return {"success": False, "error": "workflow_id required"}
            
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            result = kernel.execute(workflow_id, params)
            
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_workflow_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Get workflow handler."""
        workflow_id = request.query_params.get("id") or self._extract_path_param(request.path)
        try:
            from registry.workflow_registry import get_workflow_registry
            reg = get_workflow_registry()
            wf = reg.get(workflow_id)
            
            if wf:
                return {
                    "id": wf.id,
                    "name": wf.name,
                    "description": wf.description,
                    "steps": len(wf.steps) if hasattr(wf, 'steps') else 0,
                }
            return {"error": "Workflow not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def _list_knowledge_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List knowledge handler."""
        try:
            from registry.knowledge_registry import get_knowledge_registry
            reg = get_knowledge_registry()
            entries = reg.list_all()
            return {
                "total": len(entries),
                "entries": [
                    {"id": e.id, "title": e.title, "type": e.knowledge_type.value}
                    for e in entries
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _create_knowledge_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Create knowledge handler."""
        try:
            if not request.body:
                return {"success": False, "error": "Body required"}
            
            from registry.knowledge_registry import get_knowledge_registry, KnowledgeType
            reg = get_knowledge_registry()
            
            entry_id = reg.add(
                title=request.body.get("title", ""),
                knowledge_type=KnowledgeType.FACT,
                content=request.body.get("content", {}),
                tags=request.body.get("tags", []),
            )
            
            return {"success": True, "id": entry_id}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _search_knowledge_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Search knowledge handler."""
        try:
            query = request.query_params.get("q", "")
            from registry.knowledge_registry import get_knowledge_registry
            reg = get_knowledge_registry()
            
            results = reg.search(query)
            return {
                "total": len(results),
                "query": query,
                "results": [
                    {"id": e.id, "title": e.title}
                    for e in results
                ]
            }
        except Exception as e:
            return {"total": 0, "error": str(e)}
    
    def _list_missions_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """List missions handler."""
        return {
            "total": 0,
            "missions": [],
        }
    
    def _create_mission_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Create mission handler."""
        try:
            if not request.body:
                return {"success": False, "error": "Body required"}
            
            objective = request.body.get("objective", "")
            if not objective:
                return {"success": False, "error": "objective required"}
            
            return {
                "success": True,
                "mission_id": f"mission-{datetime.utcnow().timestamp()}",
                "objective": objective,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_mission_handler(self, request: HTTPRequest) -> Dict[str, Any]:
        """Get mission handler."""
        return {"error": "Mission not found"}
    
    def _extract_path_param(self, path: str) -> Optional[str]:
        """Extract path parameter from path."""
        parts = path.split("/")
        for i, part in enumerate(parts):
            if part.startswith("{") and part.endswith("}"):
                return parts[i - 1] if i > 0 else None
        return None
    
    def get_routes(self) -> List[Dict[str, Any]]:
        """Get all registered routes."""
        return [
            {
                "path": route.path,
                "method": route.method.value,
                "description": route.description,
            }
            for route in self._routes.values()
        ]


# Global server instance
_api_server: Optional[APIServer] = None


def get_api_server() -> APIServer:
    """Get the global API server instance."""
    global _api_server
    if _api_server is None:
        _api_server = APIServer()
    return _api_server
