# Provider Discovery

> **System can discover Providers automatically.**

---

## Discovery Types

```yaml
DiscoveryTypes:
  INSTALLED:
    description: "Providers installed locally"
    example: "CLI tools, Docker containers"
    
  AVAILABLE:
    description: "Providers accessible via network"
    example: "APIs, SaaS, Cloud services"
    
  DEPRECATED:
    description: "Providers no longer supported"
    example: "Old versions, sunset providers"
    
  DISABLED:
    description: "Providers manually disabled"
    example: "Disabled for testing, cost reasons"
    
  EXPERIMENTAL:
    description: "New providers being tested"
    example: "Beta features, new integrations"
```

---

## Discovery Process

```
┌─────────────────────────────────────────────────────────────┐
│                    Provider Discovery                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SCAN                                                    │
│     - Scan installed providers                               │
│     - Scan configured providers                             │
│     - Scan available providers                              │
│                                                             │
│  2. IDENTIFY                                                │
│     - Read provider manifest                                │
│     - Validate capabilities                                 │
│     - Check version compatibility                            │
│                                                             │
│  3. REGISTER                                                │
│     - Add to registry                                       │
│     - Map capabilities                                      │
│     - Initialize metrics                                     │
│                                                             │
│  4. MONITOR                                                 │
│     - Health checks                                         │
│     - Benchmark                                             │
│     - Update status                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Provider Manifest

```yaml
ProviderManifest:
  # Each provider declares itself
  
  provider_id: "openhands"
  version: "1.5.0"
  
  manifest_version: "1.0"
  
  capabilities:
    - id: "generate_code"
      version: "1.0"
    - id: "edit_code"
      version: "1.0"
    - id: "deploy"
      version: "1.0"
      
  requirements:
    permissions:
      - "filesystem:read"
      - "filesystem:write"
      - "network:allow"
      
    environment:
      - "python>=3.10"
      
  limits:
    rate_limit: 100  # per minute
    timeout: 300    # seconds
    concurrent: 5
    
  security:
    permissions: [...]
    forbidden_actions: [...]
    
  endpoints:
    health: "/health"
    execute: "/execute"
```

---

## Discovery Sources

```yaml
DiscoverySources:
  # Local installations
  local:
    - type: "cli"
      paths: 
        - "/usr/local/bin"
        - "$HOME/.local/bin"
      extensions: [".sh", ""]
      
    - type: "docker"
      images:
        prefix: "provider-"
        
    - type: "python"
      paths:
        - "$HOME/.providers"
        
  # Network
  network:
    - type: "api"
      endpoints:
        - "https://registry.providers.io/v1"
        - "https://internal.provider-registry/api"
        
  # Configuration
  config:
    file: "providers.yaml"
    directory: "./providers"
```

---

## Discovery Implementation

```python
class ProviderDiscovery:
    """
    Discovers and registers providers.
    """
    
    async def discover_all(self) -> list[Provider]:
        """
        Discover all available providers.
        """
        providers = []
        
        # 1. Discover local
        local = await self.discover_local()
        providers.extend(local)
        
        # 2. Discover network
        network = await self.discover_network()
        providers.extend(network)
        
        # 3. Discover from config
        configured = await self.discover_from_config()
        providers.extend(configured)
        
        # 4. Return unique
        return self.deduplicate(providers)
        
    async def discover_local(self) -> list[Provider]:
        """
        Discover local providers.
        """
        providers = []
        
        # Scan CLI paths
        for path in CLI_PATHS:
            providers.extend(await self.scan_cli_path(path))
            
        # Scan Docker
        providers.extend(await self.discover_docker())
        
        # Scan Python packages
        providers.extend(await self.discover_python_packages())
        
        return providers
        
    async def register_provider(self, provider: Provider):
        """
        Register discovered provider.
        """
        # 1. Read manifest
        manifest = await self.read_manifest(provider)
        
        # 2. Validate
        if not self.validate_manifest(manifest):
            raise InvalidManifestError(provider)
            
        # 3. Register
        await self.registry.add(provider, manifest)
        
        # 4. Initialize metrics
        await self.metrics.initialize(provider)
```

---

## Health Check

```yaml
HealthCheck:
  # Provider health status
  
  HEALTHY:
    status: "healthy"
    meaning: "Provider fully operational"
    
  DEGRADED:
    status: "degraded"
    meaning: "Provider working but slow/limited"
    
  UNHEALTHY:
    status: "unhealthy"
    meaning: "Provider not responding"
    
  MAINTENANCE:
    status: "maintenance"
    meaning: "Provider under maintenance"
    
  OFFLINE:
    status: "offline"
    meaning: "Provider not accessible"
    
  UNKNOWN:
    status: "unknown"
    meaning: "Health status unknown"
```

---

## Health Check Implementation

```python
async def check_health(provider: Provider) -> HealthStatus:
    """
    Check provider health.
    """
    
    try:
        # 1. Call health endpoint
        response = await provider.health_endpoint.call(
            timeout=5  # seconds
        )
        
        if response.status == 200:
            data = response.json()
            
            if data.get("status") == "healthy":
                return HealthStatus.HEALTHY
            elif data.get("status") == "degraded":
                return HealthStatus.DEGRADED
                
        # 2. Try basic operation
        result = await provider.try_operation(
            operation="ping",
            timeout=5
        )
        
        if result.success:
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNHEALTHY
            
    except TimeoutError:
        return HealthStatus.UNHEALTHY
        
    except Exception as e:
        return HealthStatus.UNKNOWN
```

---

## Provider Status Lifecycle

```
UNKNOWN
   ↓ (discovered)
REGISTERED
   ↓ (first health check)
PENDING
   ↓ (health check passes)
ACTIVE
   ↓ (health check fails)
DEGRADED
   ↓ (continues to fail)
UNHEALTHY
   ↓ (recovered)
ACTIVE
   ↓ (manual disable)
DISABLED
   ↓ (version deprecated)
DEPRECATED
```

---

## Related Documents

- [Provider-Object.md](../01-Provider-Definition/02-Provider-Object.md)
- [Health.md](./02-Health.md)
