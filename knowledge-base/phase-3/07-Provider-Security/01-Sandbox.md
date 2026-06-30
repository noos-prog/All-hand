# Provider Sandbox

> **Every Provider runs in isolated sandbox. Cannot access anything outside.**

---

## Sandbox Concept

```
┌─────────────────────────────────────────────────────────────┐
│                       Provider Sandbox                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Provider A ──► Sandbox A ──► Isolated                     │
│  Provider B ──► Sandbox B ──► Isolated                     │
│  Provider C ──► Sandbox C ──► Isolated                     │
│                                                             │
│  Sandbox CANNOT access:                                     │
│  ❌ Other Sandboxes                                         │
│  ❌ System Secrets                                          │
│  ❌ Other Users' Data                                        │
│  ❌ Core Brain                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Isolation Layers

```yaml
IsolationLayers:
  NETWORK:
    description: "Network isolation"
    rules:
      - "Each provider in own network namespace"
      - "No cross-provider communication"
      - "Only whitelisted endpoints"
      
  FILESYSTEM:
    description: "Filesystem isolation"
    rules:
      - "Own working directory"
      - "No access to other directories"
      - "Temp files auto-deleted"
      
  PROCESS:
    description: "Process isolation"
    rules:
      - "Own process group"
      - "Limited CPU allocation"
      - "Limited memory allocation"
      
  CREDENTIALS:
    description: "Credential isolation"
    rules:
      - "Only own credentials"
      - "No access to other providers' secrets"
      - "Secrets injected at runtime"
      
  DATA:
    description: "Data isolation"
    rules:
      - "Only own data"
      - "No cross-provider data access"
      - "Data encrypted at rest"
```

---

## Sandbox Types

```yaml
SandboxTypes:
  CONTAINER:
    type: "docker"
    isolation: "full"
    use_case: "CLI tools, databases"
    
  VM:
    type: "virtual_machine"
    isolation: "maximum"
    use_case: "Untrusted code, risky operations"
    
  PROCESS:
    type: "namespace"
    isolation: "moderate"
    use_case: "Trusted tools, low risk"
    
  BROWSER:
    type: "browser_context"
    isolation: "moderate"
    use_case: "Web scraping, automation"
```

---

## Sandbox Configuration

```yaml
SandboxConfig:
  provider_id: "openhands"
  
  # Resources
  resources:
    cpu: 2
    memory_mb: 2048
    disk_mb: 1024
    
  # Network
  network:
    isolation: true
    allowed_endpoints:
      - "api.openai.com"
      - "github.com"
      - "pypi.org"
    blocked_endpoints:
      - "*.internal"
      - "localhost"
      
  # Filesystem
  filesystem:
    working_dir: "/sandbox/openhands"
    allowed_paths:
      - "/workspace/project"
      - "/tmp"
    blocked_paths:
      - "/etc"
      - "/root"
      - "/home/*/other"
      
  # Environment
  environment:
    inherit_env: false
    env_vars:
      PATH: "/usr/local/bin:/usr/bin:/bin"
      HOME: "/sandbox/openhands"
    blocked_vars:
      - "API_KEY_*"
      - "SECRET_*"
      - "PRIVATE_*"
```

---

## Resource Limits

```yaml
ResourceLimits:
  # Per execution
  
  cpu:
    limit: 2
    period: "100ms"
    quota: 200
    
  memory:
    limit: "2GB"
    swap: "0"
    
  disk:
    limit: "1GB"
    inodes: 100000
    
  network:
    bandwidth: "100Mbps"
    connections: 50
    
  processes:
    max_processes: 100
    max_threads: 500
```

---

## Security Policy

```yaml
SecurityPolicy:
  # Provider security rules
  
  allowed_actions:
    - "read_files"
    - "write_files"
    - "execute_commands"
    - "network_requests"
    
  forbidden_actions:
    - "access_other_providers"
    - "access_system_secrets"
    - "access_other_users_data"
    - "escalate_privileges"
    - "modify_system_files"
    
  secrets:
    injection: "runtime_only"
    access: "read_once"
    storage: "encrypted"
    
  audit:
    enabled: true
    log_all: true
    log_network: true
    log_filesystem: true
```

---

## Sandbox Lifecycle

```
1. PROVIDER EXECUTION REQUEST
         ↓
2. CREATE SANDBOX
         ↓
3. INJECT CREDENTIALS
         ↓
4. EXECUTE IN SANDBOX
         ↓
5. COLLECT RESULTS
         ↓
6. DELETE CREDENTIALS
         ↓
7. DESTROY SANDBOX
         ↓
8. RETURN RESULTS
```

---

## Example: OpenHands in Sandbox

```yaml
Provider: "openhands"

Sandbox:
  type: "container"
  
  resources:
    cpu: 2
    memory_mb: 4096
    
  filesystem:
    allowed_paths:
      - "/workspace/project"  # User workspace
      - "/tmp/openhands"     # Working directory
      
  network:
    allowed:
      - "api.anthropic.com"
      - "api.github.com"
      - "pypi.org"
      - "github.com"
    blocked:
      - "*.internal"
      - "192.168.*.*"
      
  environment:
    injected_vars:
      ANTHROPIC_API_KEY: "<injected at runtime>"
      GITHUB_TOKEN: "<injected at runtime>"
    blocked_vars:
      - "*_SECRET"
      - "*_PRIVATE_KEY"
```

---

## Related Documents

- [Security-Policy.md](./02-Security-Policy.md)
