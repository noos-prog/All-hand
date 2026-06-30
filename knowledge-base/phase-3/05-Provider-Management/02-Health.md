# Provider Health

> **Every Provider is monitored continuously.**

---

## Health States

```yaml
HealthStates:
  HEALTHY:
    icon: "✅"
    description: "Fully operational"
    can_use: true
    selection_priority: 1
    
  DEGRADED:
    icon: "⚠️"
    description: "Working but with limitations"
    can_use: true
    selection_priority: 2
    reasons:
      - "High latency"
      - "Rate limiting"
      - "Partial outage"
      
  UNHEALTHY:
    icon: "❌"
    description: "Not responding or erroring"
    can_use: false
    selection_priority: 99
    
  MAINTENANCE:
    icon: "🔧"
    description: "Under maintenance"
    can_use: false
    selection_priority: 99
    
  OFFLINE:
    icon: "📴"
    description: "Not accessible"
    can_use: false
    selection_priority: 99
    
  UNKNOWN:
    icon: "❓"
    description: "Health unknown"
    can_use: true (with caution)
    selection_priority: 3
```

---

## Health Metrics

```yaml
HealthMetrics:
  # Real-time metrics
  
  uptime_percentage: decimal       # 99.9%
  response_time_avg: duration      # 150ms
  response_time_p95: duration      # 500ms
  error_rate: decimal             # 0.1%
  success_rate: decimal           # 99.9%
  
  # Historical
  mtbf: duration                  # Mean Time Between Failures
  mttr: duration                  # Mean Time To Recovery
  
  # Current
  is_healthy: boolean
  last_check: datetime
  consecutive_failures: integer
  consecutive_successes: integer
```

---

## Health Check Types

```yaml
HealthCheckTypes:
  PASSIVE:
    description: "Monitor actual usage"
    frequency: "continuous"
    metrics:
      - success_rate
      - error_rate
      - latency
      
  ACTIVE:
    description: "Proactive health checks"
    frequency: "every 30 seconds"
    endpoint: "/health"
    
  DEEP:
    description: "Comprehensive health check"
    frequency: "every 5 minutes"
    checks:
      - "Authentication"
      - "Basic operation"
      - "Rate limits"
```

---

## Health Check Implementation

```python
class ProviderHealthMonitor:
    """
    Continuously monitors provider health.
    """
    
    async def check_health(
        self,
        provider: Provider
    ) -> HealthStatus:
        """
        Perform health check.
        """
        
        start = time.now()
        
        try:
            # 1. Call health endpoint
            response = await self.call_health_endpoint(provider)
            
            # 2. Check response time
            duration = time.now() - start
            
            if duration > provider.max_latency:
                return HealthStatus(
                    status="degraded",
                    reason="high_latency",
                    latency=duration
                )
                
            # 3. Parse response
            if response.status == 200:
                data = response.json()
                
                if data.get("healthy"):
                    return HealthStatus(
                        status="healthy",
                        latency=duration,
                        details=data
                    )
                else:
                    return HealthStatus(
                        status="degraded",
                        reason=data.get("reason", "unknown"),
                        latency=duration
                    )
                    
            return HealthStatus(
                status="unhealthy",
                reason="bad_status",
                status_code=response.status
            )
            
        except TimeoutError:
            return HealthStatus(
                status="unhealthy",
                reason="timeout"
            )
            
        except Exception as e:
            return HealthStatus(
                status="unhealthy",
                reason=str(e)
            )
```

---

## Health History

```yaml
HealthHistory:
  provider_id: "openhands"
  
  records:
    - timestamp: "2024-01-15T10:00:00Z"
      status: "healthy"
      latency: "120ms"
      
    - timestamp: "2024-01-15T10:30:00Z"
      status: "degraded"
      latency: "800ms"
      reason: "high_load"
      
    - timestamp: "2024-01-15T11:00:00Z"
      status: "healthy"
      latency: "130ms"
      
  # Analysis
  total_checks: 1000
  healthy_percentage: 99.5
  avg_latency: "150ms"
  incidents: 5
```

---

## Automatic Remediation

```python
class HealthRemediation:
    """
    Automatically handle health issues.
    """
    
    async def handle_unhealthy(
        self,
        provider: Provider,
        status: HealthStatus
    ):
        """
        Take action based on health status.
        """
        
        if status.consecutive_failures == 1:
            # First failure - just log
            await self.log_warning(provider, status)
            
        elif status.consecutive_failures == 3:
            # Multiple failures - switch to fallback
            await self.switch_to_fallback(provider)
            
        elif status.consecutive_failures == 5:
            # Persistent failures - disable provider
            await self.disable_provider(provider)
            await self.alert(f"Provider {provider.id} disabled after 5 failures")
            
        elif status.status == "maintenance":
            # Scheduled maintenance
            await self.notify_users(provider, "maintenance")
```

---

## Health Dashboard

```yaml
HealthDashboard:
  # Real-time health overview
  
  providers:
    - id: "openhands"
      status: "healthy"
      uptime: "99.9%"
      latency: "150ms"
      
    - id: "github"
      status: "degraded"
      uptime: "98.5%"
      latency: "800ms"
      reason: "rate_limit"
      
    - id: "docker"
      status: "healthy"
      uptime: "100%"
      latency: "50ms"
```

---

## Related Documents

- [Discovery.md](./01-Discovery.md)
- [Failover.md](./04-Failover.md)
