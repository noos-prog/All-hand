# Universal Provider Interface

> **Every Provider, regardless of type, implements the same interface.**

---

## Interface Concept

```
┌─────────────────────────────────────────────────────────────┐
│              Universal Provider Interface                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Validate()  ──►  Authorize()  ──►  Prepare()             │
│                                                             │
│       │                                               │    │
│       │                                               ▼    │
│  ┌────┴────────────────────────────────────────┐          │
│  │              Execute()                            │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │         Provider-Specific              │  │          │
│  │  │         Implementation                 │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  └────────────────────────────────────────────┘          │
│       │                                                    │
│       ▼                                                    │
│  Collect()  ──►  Verify()  ──►  Return()                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Interface Methods

```python
class UniversalProviderInterface:
    """
    Every Provider must implement this interface.
    """
    
    async def validate(
        self,
        request: ProviderRequest
    ) -> ValidationResult:
        """
        Validate request before execution.
        - Check input schema
        - Check required fields
        - Check constraints
        """
        pass
        
    async def authorize(
        self,
        request: ProviderRequest
    ) -> AuthResult:
        """
        Authorize the request.
        - Check permissions
        - Check authentication
        - Check quotas
        """
        pass
        
    async def prepare(
        self,
        request: ProviderRequest
    ) -> PreparationResult:
        """
        Prepare for execution.
        - Load configuration
        - Setup resources
        - Prepare inputs
        """
        pass
        
    async def execute(
        self,
        request: ProviderRequest,
        context: ExecutionContext
    ) -> ExecutionResult:
        """
        Execute the capability.
        - Call Provider
        - Handle retries
        - Collect outputs
        """
        pass
        
    async def collect(
        self,
        execution: ExecutionResult
    ) -> CollectedResult:
        """
        Collect results from execution.
        - Gather artifacts
        - Gather logs
        - Gather metrics
        """
        pass
        
    async def verify(
        self,
        result: CollectedResult,
        verification_rules: list[Rule]
    ) -> VerificationResult:
        """
        Verify the result.
        - Run verification steps
        - Check quality
        - Check completeness
        """
        pass
        
    async def cleanup(
        self,
        execution: ExecutionResult
    ) -> CleanupResult:
        """
        Cleanup after execution.
        - Release resources
        - Clean temporary files
        - Close connections
        """
        pass
```

---

## Execution Flow

```
1. REQUEST RECEIVED
      ↓
2. VALIDATE
      ↓
   - Input schema valid?
   - Required fields present?
      ↓
3. AUTHORIZE
      ↓
   - Authentication valid?
   - Permissions sufficient?
   - Quota available?
      ↓
4. PREPARE
      ↓
   - Setup resources
   - Load configuration
      ↓
5. EXECUTE
      │
      ├── Try Provider
      ├── Handle errors
      └── Handle retries
      ↓
6. COLLECT
      │
      ├── Gather artifacts
      ├── Gather logs
      └── Gather metrics
      ↓
7. VERIFY
      │
      ├── Run verifications
      ├── Check quality
      └── Check completeness
      ↓
8. CLEANUP
      │
      ├── Release resources
      └── Clean temp files
      ↓
9. RETURN RESULT
```

---

## Request Schema

```yaml
ProviderRequest:
  # Identification
  request_id: string
  capability_id: string
  
  # Input
  inputs: object
  input_schema: object
  
  # Context
  context:
    goal_id: string
    task_id: string
    priority: enum
    deadline: datetime
    environment: string
    
  # Configuration
  config:
    timeout: duration
    retries: integer
    verification_required: boolean
    
  # Provider-specific
  provider_options: object
  
  # Auth
  auth: object
```

---

## Result Schema

```yaml
ProviderResult:
  # Identification
  request_id: string
  capability_id: string
  provider_id: string
  
  # Status
  status: enum              # success, failure, partial, timeout
  message: string
  
  # Output
  output:
    artifacts: list[Artifact]
    data: object
    logs: list[Log]
    
  # Metrics
  metrics:
    duration: duration
    tokens_used: integer
    api_calls: integer
    cost: decimal
    quality_score: float
    
  # Verification
  verification:
    status: enum           # passed, failed, skipped
    checks: list[Check]
    
  # Errors
  errors: list[Error]
  warnings: list[Warning]
  
  # Context
  provider: string
  provider_version: string
  region: string
```

---

## Adapter Implementation Example

### OpenHands Adapter

```python
class OpenHandsAdapter(UniversalProviderInterface):
    """
    Adapter for OpenHands agent.
    """
    
    def __init__(self, config: OpenHandsConfig):
        self.config = config
        self.endpoint = config.endpoint
        self.api_key = config.api_key
        
    async def validate(self, request: ProviderRequest) -> ValidationResult:
        """
        Validate OpenHands-specific request.
        """
        # Check required fields for OpenHands
        if not request.inputs.get("task"):
            return ValidationResult(
                valid=False,
                errors=["Missing required field: task"]
            )
            
        return ValidationResult(valid=True)
        
    async def authorize(self, request: ProviderRequest) -> AuthResult:
        """
        Authorize OpenHands API access.
        """
        # Verify API key
        if not await self.verify_api_key(self.api_key):
            return AuthResult(
                authorized=False,
                error="Invalid API key"
            )
            
        # Check rate limits
        if await self.is_rate_limited():
            return AuthResult(
                authorized=False,
                error="Rate limit exceeded"
            )
            
        return AuthResult(authorized=True)
        
    async def prepare(self, request: ProviderRequest) -> PreparationResult:
        """
        Prepare OpenHands execution.
        """
        # Setup environment
        env = self.setup_environment(request)
        
        # Prepare task
        task = self.prepare_task(request)
        
        return PreparationResult(
            ready=True,
            environment=env,
            prepared_task=task
        )
        
    async def execute(
        self,
        request: ProviderRequest,
        context: ExecutionContext
    ) -> ExecutionResult:
        """
        Execute via OpenHands API.
        """
        # Call OpenHands
        response = await self.call_api(
            endpoint=f"{self.endpoint}/execute",
            payload={
                "task": request.inputs["task"],
                "instructions": request.inputs.get("instructions"),
                "sandbox": request.inputs.get("sandbox", True)
            },
            timeout=request.config.timeout
        )
        
        # Handle response
        if response.status == "success":
            return ExecutionResult(
                success=True,
                artifacts=response.artifacts,
                output=response.data,
                logs=response.logs
            )
        else:
            return ExecutionResult(
                success=False,
                error=response.error
            )
```

### GitHub Adapter

```python
class GitHubAdapter(UniversalProviderInterface):
    """
    Adapter for GitHub API.
    """
    
    async def execute(
        self,
        request: ProviderRequest,
        context: ExecutionContext
    ) -> ExecutionResult:
        """
        Execute GitHub API call.
        """
        # Translate to GitHub API
        github_api = self.translate_request(request)
        
        # Make API call
        response = await self.github_api.call(
            endpoint=github_api.endpoint,
            method=github_api.method,
            params=github_api.params
        )
        
        # Translate response
        return self.translate_response(response)
```

### Database Adapter

```python
class PostgresAdapter(UniversalProviderInterface):
    """
    Adapter for PostgreSQL database.
    """
    
    async def execute(
        self,
        request: ProviderRequest,
        context: ExecutionContext
    ) -> ExecutionResult:
        """
        Execute database query.
        """
        # Get connection
        conn = await self.get_connection()
        
        try:
            # Execute query
            result = await conn.execute(
                request.inputs["query"],
                params=request.inputs.get("params")
            )
            
            return ExecutionResult(
                success=True,
                data=result.rows,
                artifacts=[]
            )
        finally:
            await conn.release()
```

---

## Type-to-Interface Mapping

```yaml
TypeMapping:
  AI_Agent:
    interface: "cli" or "api"
    adapter_example: "OpenHandsAdapter"
    
  LLM:
    interface: "api"
    adapter_example: "ClaudeAdapter"
    
  REST_API:
    interface: "http"
    adapter_example: "GitHubAdapter"
    
  CLI:
    interface: "shell"
    adapter_example: "DockerAdapter"
    
  Docker:
    interface: "docker"
    adapter_example: "DockerAdapter"
    
  Browser:
    interface: "sdk"
    adapter_example: "PlaywrightAdapter"
    
  Database:
    interface: "native"
    adapter_example: "PostgresAdapter"
```

---

## Related Documents

- [Provider-Object.md](../01-Provider-Definition/02-Provider-Object.md)
- [Adapter-Overview.md](../04-Provider-Adapter/01-Adapter-Overview.md)
