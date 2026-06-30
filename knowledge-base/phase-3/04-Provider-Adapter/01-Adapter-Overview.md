# Provider Adapter Overview

> **Every Provider has its own Adapter. Core knows NOTHING about Provider internals.**

---

## Adapter Concept

```
┌─────────────────────────────────────────────────────────────┐
│                      Core Brain                               │
│                                                             │
│  Knows ONLY:                                               │
│  - Capability                                              │
│  - Provider ID                                             │
│  - Universal Interface                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Adapter Layer                              │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │OpenHands│  │  Cline │  │  Aider │  │ GitHub │       │
│  │Adapter  │  │ Adapter │  │ Adapter │  │ Adapter  │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │             │
└───────┼────────────┼────────────┼────────────┼─────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Providers                                │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │OpenHands│  │  Cline │  │  Aider │  │ GitHub  │       │
│  │ Agent  │  │  Agent │  │  Agent │  │   API  │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Adapter Responsibilities

```yaml
Adapter Responsibilities:

  1. TRANSLATE REQUESTS
     - Convert universal format → Provider format
     - Handle Provider-specific syntax
     
  2. AUTHENTICATE
     - Handle Provider-specific auth
     - Manage API keys
     - Handle OAuth flows
     
  3. EXECUTE
     - Call Provider API/CLI
     - Handle timeouts
     - Handle retries
     
  4. TRANSLATE RESPONSES
     - Convert Provider format → universal format
     - Handle Provider-specific errors
     
  5. MANAGE RESOURCES
     - Manage connections
     - Manage sessions
     - Cleanup resources
```

---

## Adapter Structure

```python
class ProviderAdapter:
    """
    Base class for all adapters.
    """
    
    # Provider info
    provider_id: str
    provider_name: str
    provider_type: str
    
    # Configuration
    config: AdapterConfig
    
    # Resources
    connection: Connection
    session: Session
    
    async def validate(self, request) -> ValidationResult:
        """Validate request for this Provider."""
        pass
        
    async def authorize(self, request) -> AuthResult:
        """Authenticate with Provider."""
        pass
        
    async def prepare(self, request) -> PreparationResult:
        """Prepare execution."""
        pass
        
    async def execute(self, request) -> ExecutionResult:
        """Execute via Provider."""
        pass
        
    async def collect(self, execution) -> CollectedResult:
        """Collect results."""
        pass
        
    async def cleanup(self, execution) -> CleanupResult:
        """Cleanup resources."""
        pass
```

---

## Adapter Examples

### OpenHands Adapter

```python
class OpenHandsAdapter(ProviderAdapter):
    """
    Adapter for OpenHands AI Agent.
    """
    
    provider_id = "openhands"
    provider_type = "ai_agent"
    
    def __init__(self, config: OpenHandsConfig):
        self.endpoint = config.endpoint
        self.api_key = config.api_key
        
    async def execute(self, request: ProviderRequest) -> ExecutionResult:
        """
        Execute via OpenHands API.
        """
        # 1. Translate request
        payload = {
            "task": request.inputs["task"],
            "instructions": request.inputs.get("instructions", ""),
            "sandbox": request.inputs.get("sandbox", True),
            "model": request.inputs.get("model", "claude")
        }
        
        # 2. Call OpenHands
        response = await self.call_api(
            method="POST",
            endpoint=f"{self.endpoint}/execute",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            body=payload,
            timeout=request.config.timeout
        )
        
        # 3. Translate response
        return ExecutionResult(
            request_id=request.request_id,
            provider_id=self.provider_id,
            success=response.status == "success",
            artifacts=response.artifacts,
            output=response.data,
            logs=response.logs,
            metrics=response.metrics
        )
        
    async def cleanup(self, execution) -> CleanupResult:
        """Cleanup OpenHands session."""
        await self.close_session(execution.session_id)
```

### GitHub Adapter

```python
class GitHubAdapter(ProviderAdapter):
    """
    Adapter for GitHub API.
    """
    
    provider_id = "github"
    provider_type = "api"
    
    async def execute(self, request: ProviderRequest) -> ExecutionResult:
        """
        Execute GitHub API call.
        """
        # 1. Translate request to GitHub API format
        github_call = self.translate_request(request)
        
        # 2. Make GitHub API call
        response = await self.github_api.call(
            method=github_call.method,
            endpoint=github_call.endpoint,
            params=github_call.params
        )
        
        # 3. Translate response to universal format
        return self.translate_response(response)
```

### Docker Adapter

```python
class DockerAdapter(ProviderAdapter):
    """
    Adapter for Docker containers.
    """
    
    provider_id = "docker"
    provider_type = "container"
    
    async def execute(self, request: ProviderRequest) -> ExecutionResult:
        """
        Execute in Docker container.
        """
        # 1. Pull image if needed
        await self.ensure_image(request.inputs["image"])
        
        # 2. Create container
        container = await self.docker.containers.run(
            image=request.inputs["image"],
            command=request.inputs["command"],
            volumes=request.inputs.get("volumes", {}),
            environment=request.inputs.get("env", {})
        )
        
        # 3. Wait for completion
        result = await container.wait()
        
        # 4. Collect output
        logs = await container.logs()
        
        return ExecutionResult(
            request_id=request.request_id,
            provider_id=self.provider_id,
            success=result["StatusCode"] == 0,
            output={
                "exit_code": result["StatusCode"],
                "logs": logs.decode("utf-8")
            },
            artifacts=[]
        )
```

### Playwright Adapter

```python
class PlaywrightAdapter(ProviderAdapter):
    """
    Adapter for Playwright browser automation.
    """
    
    provider_id = "playwright"
    provider_type = "browser"
    
    async def execute(self, request: ProviderRequest) -> ExecutionResult:
        """
        Execute browser automation.
        """
        # 1. Launch browser
        browser = await self.playwright.chromium.launch(
            headless=request.inputs.get("headless", True)
        )
        
        # 2. Create page
        page = await browser.new_page()
        
        # 3. Navigate if URL provided
        if request.inputs.get("url"):
            await page.goto(request.inputs["url"])
            
        # 4. Execute actions
        if request.inputs.get("actions"):
            for action in request.inputs["actions"]:
                await self.execute_action(page, action)
                
        # 5. Collect results
        screenshot = None
        if request.inputs.get("screenshot"):
            screenshot = await page.screenshot()
            
        return ExecutionResult(
            request_id=request.request_id,
            provider_id=self.provider_id,
            success=True,
            output={"url": page.url},
            artifacts=[{
                "type": "screenshot",
                "data": screenshot
            }] if screenshot else []
        )
```

### PostgreSQL Adapter

```python
class PostgresAdapter(ProviderAdapter):
    """
    Adapter for PostgreSQL database.
    """
    
    provider_id = "postgresql"
    provider_type = "database"
    
    async def execute(self, request: ProviderRequest) -> ExecutionResult:
        """
        Execute database query.
        """
        # 1. Get connection from pool
        conn = await self.pool.acquire()
        
        try:
            # 2. Execute query
            if request.inputs.get("query_type") == "select":
                rows = await conn.fetch(
                    request.inputs["query"],
                    *request.inputs.get("params", [])
                )
                data = [dict(row) for row in rows]
            else:
                await conn.execute(
                    request.inputs["query"],
                    *request.inputs.get("params", [])
                )
                data = {"affected_rows": conn.row_count}
                
            return ExecutionResult(
                request_id=request.request_id,
                provider_id=self.provider_id,
                success=True,
                output={"rows": data}
            )
            
        finally:
            # 3. Release connection
            await self.pool.release(conn)
```

---

## Adapter Registry

```yaml
AdapterRegistry:
  adapters:
    openhands: OpenHandsAdapter
    cline: ClineAdapter
    aider: AiderAdapter
    github: GitHubAdapter
    docker: DockerAdapter
    playwright: PlaywrightAdapter
    postgresql: PostgresAdapter
    sourcegraph: SourcegraphAdapter
    
  # Get adapter by provider
  def get_adapter(provider_id: str) -> ProviderAdapter:
      return adapters[provider_id]
```

---

## Adapter Testing

```python
def test_adapter(adapter: ProviderAdapter):
    """
    Test adapter against universal interface.
    """
    
    # 1. Test validate
    validation = await adapter.validate(sample_request)
    assert validation.valid == True
    
    # 2. Test authorize
    auth = await adapter.authorize(sample_request)
    assert auth.authorized == True
    
    # 3. Test execute
    result = await adapter.execute(sample_request)
    assert result.provider_id == adapter.provider_id
    
    # 4. Test cleanup
    cleanup = await adapter.cleanup(result)
    assert cleanup.success == True
```

---

## Related Documents

- [Provider-Object.md](../01-Provider-Definition/02-Provider-Object.md)
- [Interface-Overview.md](../03-Provider-Interface/01-Interface-Overview.md)
