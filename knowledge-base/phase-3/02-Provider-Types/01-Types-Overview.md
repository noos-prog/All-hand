# Provider Types

> **20+ types of Providers in the system.**

---

## Provider Type Hierarchy

```
Provider Types
    │
    ├─── AI Providers
    │       ├─── AI Agent
    │       ├─── LLM
    │       └─── MCP
    │
    ├─── API Providers
    │       ├─── REST API
    │       └─── GraphQL
    │
    ├─── CLI Providers
    │       └─── CLI
    │
    ├─── Container Providers
    │       ├─── Docker
    │       └─── Kubernetes
    │
    ├─── Browser Providers
    │       ├─── Browser
    │       └─── Playwright
    │
    ├─── Data Providers
    │       ├─── Database
    │       ├─── Storage
    │       └─── Queue
    │
    ├─── Integration Providers
    │       ├─── GitHub
    │       ├─── Git
    │       ├─── CI/CD
    │       └─── Deployment
    │
    ├─── Utility Providers
    │       ├─── Shell
    │       ├─── Filesystem
    │       ├─── Search
    │       └─── Documentation
    │
    └─── Communication Providers
            ├─── Notification
            ├─── Email
            └─── Slack
```

---

## Type 1: AI Agent

```yaml
AI Agent:
  description: "AI-powered coding agents"
  
  examples:
    - OpenHands
    - Cline
    - Aider
    - Goose
    - Claude Code
    - Cursor
    
  interface_type: "cli" or "api"
  
  capabilities:
    - generate_code
    - edit_code
    - deploy
    - search_code
    
  authentication:
    - api_key
    - oauth
    - token
    
  costs:
    - per_use
    - subscription
    - free
    
  limitations:
    - rate_limits
    - context_window
    - model_restrictions
```

---

## Type 2: LLM

```yaml
LLM:
  description: "Large Language Models"
  
  examples:
    - Claude
    - GPT-4
    - Gemini
    - Llama
    - Mistral
    
  interface_type: "api"
  
  capabilities:
    - generate_text
    - analyze_code
    - explain_code
    - translate_code
    
  authentication:
    - api_key
    
  costs:
    - per_token
    - subscription
```

---

## Type 3: MCP (Model Context Protocol)

```yaml
MCP:
  description: "Model Context Protocol servers"
  
  examples:
    - Filesystem MCP
    - Git MCP
    - Database MCP
    - Web Search MCP
    
  interface_type: "sdk" or "api"
  
  capabilities:
    - filesystem_operations
    - git_operations
    - database_queries
    - web_search
    
  authentication:
    - none
    - api_key
    
  costs:
    - free
    - included_in_subscription
```

---

## Type 4: REST API

```yaml
REST API:
  description: "REST API services"
  
  examples:
    - GitHub API
    - GitLab API
    - Slack API
    - Stripe API
    - AWS API
    
  interface_type: "api"
  
  capabilities:
    - varies_by_service
    
  authentication:
    - api_key
    - oauth
    - bearer_token
    
  costs:
    - free (with limits)
    - per_request
    - subscription
```

---

## Type 5: CLI

```yaml
CLI:
  description: "Command-line tools"
  
  examples:
    - Git
    - Docker
    - kubectl
    - npm
    - pip
    - cargo
    
  interface_type: "cli"
  
  capabilities:
    - git_operations
    - container_management
    - package_management
    
  authentication:
    - key_file (SSH)
    - token
    
  costs:
    - free
    - license
```

---

## Type 6: Docker

```yaml
Docker:
  description: "Docker containers"
  
  examples:
    - Database containers
    - Service containers
    - Build containers
    
  interface_type: "docker"
  
  capabilities:
    - run_container
    - build_image
    - manage_volumes
    
  authentication:
    - docker_registry_auth
    
  costs:
    - compute_resources
    - storage
    
  limitations:
    - requires_docker
    - resource_limits
```

---

## Type 7: Browser

```yaml
Browser:
  description: "Web browsers for automation"
  
  examples:
    - Playwright
    - Selenium
    - Puppeteer
    
  interface_type: "sdk"
  
  capabilities:
    - browse_webpage
    - take_screenshot
    - fill_form
    - click_element
    
  authentication:
    - none
    
  costs:
    - compute_resources
```

---

## Type 8: Database

```yaml
Database:
  description: "Database systems"
  
  examples:
    - PostgreSQL
    - MongoDB
    - Redis
    - Elasticsearch
    
  interface_type: "native" or "api"
  
  capabilities:
    - query
    - insert
    - update
    - delete
    - migrate
    
  authentication:
    - username_password
    - api_key
    - connection_string
    
  costs:
    - infrastructure
    - managed_service
```

---

## Type 9: GitHub

```yaml
GitHub:
  description: "GitHub integration"
  
  interface_type: "api"
  
  capabilities:
    - read_repository
    - create_issue
    - create_pr
    - review_pr
    - merge_pr
    - manage_actions
    
  authentication:
    - personal_access_token
    - oauth_app
    - github_app
    
  costs:
    - free (public_repos)
    - subscription (private_repos)
```

---

## Type 10: CI/CD

```yaml
CI/CD:
  description: "Continuous Integration/Deployment"
  
  examples:
    - GitHub Actions
    - GitLab CI
    - Jenkins
    - CircleCI
    
  interface_type: "api" or "cli"
  
  capabilities:
    - run_pipeline
    - deploy
    - run_tests
    - build_artifacts
    
  authentication:
    - api_key
    - oauth
    
  costs:
    - compute_minutes
    - subscription
```

---

## Type 11: Shell

```yaml
Shell:
  description: "Shell commands"
  
  interface_type: "native"
  
  capabilities:
    - execute_command
    - run_script
    - manage_processes
    
  authentication:
    - none
    
  costs:
    - compute_resources
    
  limitations:
    - security_risks
    - platform_specific
```

---

## Type 12: Filesystem

```yaml
Filesystem:
  description: "File operations"
  
  interface_type: "native"
  
  capabilities:
    - read_file
    - write_file
    - delete_file
    - list_directory
    - search_files
    
  authentication:
    - none
    
  costs:
    - storage
    
  limitations:
    - permissions
    - path_restrictions
```

---

## Type 13: Search Engine

```yaml
Search Engine:
  description: "Code and documentation search"
  
  examples:
    - Sourcegraph
    - Algolia
    - Elasticsearch
    
  interface_type: "api"
  
  capabilities:
    - search_code
    - search_docs
    - search_web
    
  authentication:
    - api_key
    
  costs:
    - per_query
    - subscription
```

---

## Type 14: Documentation

```yaml
Documentation:
  description: "Documentation systems"
  
  examples:
    - GitBook
    - Notion
    - Confluence
    - ReadTheDocs
    
  interface_type: "api"
  
  capabilities:
    - read_docs
    - write_docs
    - search_docs
    
  authentication:
    - api_key
    - oauth
```

---

## Type 15: Deployment

```yaml
Deployment:
  description: "Deployment platforms"
  
  examples:
    - Vercel
    - Netlify
    - AWS
    - GCP
    - Azure
    - Railway
    
  interface_type: "api" or "cli"
  
  capabilities:
    - deploy
    - rollback
    - configure
    - scale
    
  authentication:
    - api_key
    - oauth
```

---

## Type 16: Storage

```yaml
Storage:
  description: "Cloud storage"
  
  examples:
    - S3
    - GCS
    - Azure Blob
    - Cloudflare R2
    
  interface_type: "api"
  
  capabilities:
    - upload
    - download
    - list
    - delete
    
  authentication:
    - api_key
    - access_token
    
  costs:
    - per_gb_stored
    - per_gb_transfer
```

---

## Type 17: Queue

```yaml
Queue:
  description: "Message queues"
  
  examples:
    - AWS SQS
    - RabbitMQ
    - Kafka
    - Redis Queue
    
  interface_type: "api" or "sdk"
  
  capabilities:
    - send_message
    - receive_message
    - create_queue
    
  authentication:
    - api_key
    - connection_string
```

---

## Type 18: Notification

```yaml
Notification:
  description: "Notification services"
  
  examples:
    - Slack
    - Discord
    - PagerDuty
    - Twilio
    
  interface_type: "api"
  
  capabilities:
    - send_message
    - send_alert
    - send_email
    
  authentication:
    - api_key
    - webhook_url
```

---

## Type 19: Local Model

```yaml
Local Model:
  description: "Self-hosted AI models"
  
  examples:
    - Ollama
    - LM Studio
    - vLLM
    - Local Llama
    
  interface_type: "api"
  
  capabilities:
    - generate_text
    - analyze_code
    - similar to LLM
    
  authentication:
    - none
    - api_key
    
  costs:
    - compute_resources
    - no_per_token_cost
```

---

## Type 20: Git

```yaml
Git:
  description: "Git operations"
  
  examples:
    - GitHub
    - GitLab
    - Bitbucket
    - Azure DevOps
    
  interface_type: "cli" or "api"
  
  capabilities:
    - clone
    - commit
    - push
    - pull
    - branch
    - merge
    
  authentication:
    - ssh_key
    - personal_access_token
```

---

## Type Matrix

| Type | Interface | Auth | Cost | Examples |
|------|-----------|------|------|----------|
| AI Agent | CLI/API | API Key | Per Use | OpenHands, Cline |
| LLM | API | API Key | Per Token | Claude, GPT-4 |
| MCP | SDK | None/API Key | Free | Filesystem MCP |
| REST API | API | Various | Various | GitHub API |
| CLI | CLI | SSH/Token | Free | Git, Docker |
| Docker | Docker | Registry Auth | Compute | Containers |
| Browser | SDK | None | Compute | Playwright |
| Database | Native/API | Credentials | Infra | PostgreSQL |
| CI/CD | API/CLI | API Key | Minutes | GitHub Actions |
| Shell | Native | None | Compute | Bash |
| Filesystem | Native | None | Storage | Local FS |
| Search | API | API Key | Per Query | Sourcegraph |
| Storage | API | API Key | Per GB | S3 |
| Queue | API/SDK | Various | Per Message | SQS |
| Notification | API | API Key/Webhook | Per Message | Slack |
| Local Model | API | None | Compute | Ollama |
| Git | CLI/API | SSH/Token | Free | GitHub |

---

## Related Documents

- [Provider-Object.md](../01-Provider-Definition/02-Provider-Object.md)
- [Adapter-Overview.md](../04-Provider-Adapter/01-Adapter-Overview.md)
