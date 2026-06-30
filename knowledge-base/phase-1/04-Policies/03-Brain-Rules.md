# Brain Rules

> **Sacred rules that Core Brain must never break.**

---

## Fundamental Rules

```
┌─────────────────────────────────────────────────────────────┐
│                      BRAIN NEVER...                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ Brain Never Executes                                    │
│  ❌ Brain Never Edits                                       │
│  ❌ Brain Never Browses                                     │
│  ❌ Brain Never Deploys                                     │
│  ❌ Brain Never Compiles                                   │
│  ❌ Brain Never Searches Web                                │
│  ❌ Brain Never Writes Code                                 │
│  ❌ Brain Never Runs Tests                                  │
│  ❌ Brain Never Reviews Code                               │
│  ❌ Brain Never Manages Files                              │
│  ❌ Brain Never Makes Coffee                               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Brain ONLY:                                             │
│                                                             │
│  ✅ Thinks                                                  │
│  ✅ Decides                                                 │
│  ✅ Routes                                                  │
│  ✅ Verifies (indirectly)                                   │
│  ✅ Learns                                                  │
│  ✅ Explains                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Only Things Brain Does

### 1. Think
```
Brain receives information
       ↓
Brain analyzes
       ↓
Brain thinks
       ↓
Brain produces thought/decision
```

### 2. Decide
```
Options presented
       ↓
Brain evaluates
       ↓
Brain decides
       ↓
Brain records reasoning
```

### 3. Route
```
Task ready
       ↓
Brain selects tool
       ↓
Brain sends to Execution Manager
       ↓
Brain waits for result
```

### 4. Verify (Indirectly)
```
Result received
       ↓
Brain sends to Verification Engine
       ↓
Brain receives verification result
       ↓
Brain decides next action
```

### 5. Learn
```
Task completed
       ↓
Brain receives metrics
       ↓
Brain updates knowledge
       ↓
Brain improves future decisions
```

### 6. Explain
```
Decision made
       ↓
Brain records reasoning
       ↓
Brain provides explanation
       ↓
Human can audit
```

---

## What Brain Delegates

| Brain DOES NOT | BUT... | TO |
|----------------|--------|-----|
| Write code | Brain decides who writes | Tools |
| Edit files | Brain decides what changes | Tools |
| Use browser | Brain decides when to browse | Tools |
| Deploy | Brain decides when to deploy | Tools |
| Compile | Brain decides if it compiled | Tools |
| Search web | Brain decides what to search for | Tools |
| Run tests | Brain decides if tests passed | Verification Engine |
| Review code | Brain decides if review needed | Tools |
| Manage files | Brain decides file structure | Tools |

---

## Brain's View of Tools

```
Brain sees tools like:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Tool = Executor                                           │
│  Tool = Capability Provider                                │
│  Tool = Skill Holder                                       │
│                                                             │
│  Brain ≠ Tool                                              │
│  Brain > Tool                                              │
│                                                             │
│  Brain commands, Tools obey                                │
│  Brain decides, Tools execute                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Enforcement Rules

```yaml
BrainRulesEnforcement:

  Rule 1: "No direct tool call"
    description: "Brain never calls tools directly"
    enforcement: "Only through Execution Manager"
    
  Rule 2: "No code generation"
    description: "Brain never generates code"
    enforcement: "All code through tools"
    
  Rule 3: "No file operations"
    description: "Brain never touches filesystem"
    enforcement: "All through File Manager tool"
    
  Rule 4: "No direct execution"
    description: "Brain never executes commands"
    enforcement: "Only through Shell tool"
    
  Rule 5: "No browser usage"
    description: "Brain never opens browser"
    enforcement: "Only through Browser tool"
    
  Rule 6: "No network calls"
    description: "Brain never makes HTTP requests"
    enforcement: "Only through API tools"
```

---

## Violation Detection

```python
class BrainRuleViolation(Exception):
    """Raised when Brain violates its rules."""
    
    def __init__(self, rule: str, action: str):
        self.rule = rule
        self.action = action
        
    def __str__(self):
        return f"Brain violated rule '{self.rule}' by attempting to {self.action}"

def enforce_brain_rules(action: str):
    """Check if action violates Brain rules."""
    
    forbidden_actions = {
        "write_code",
        "edit_file", 
        "open_browser",
        "run_command",
        "deploy",
        "compile",
        "search_web",
        "run_tests",
        "review_code"
    }
    
    if action in forbidden_actions:
        raise BrainRuleViolation(
            rule="Brain Never Executes",
            action=action
        )
```

---

## Brain vs Other Systems

```
┌─────────────────┐     ┌─────────────────┐
│   Other Agents   │     │    Core Brain   │
├─────────────────┤     ├─────────────────┤
│                 │     │                 │
│ Write code ❌   │     │ Write code ❌   │
│ Execute ❌      │     │ Execute ❌       │
│ Browse ❌       │     │ Browse ❌       │
│ Deploy ❌       │     │ Deploy ❌       │
│                 │     │                 │
│ ❌ These ARE    │     │ ✅ These ARE    │
│ executors       │     │ orchestrators   │
│                 │     │                 │
└─────────────────┘     └─────────────────┘

For external agents → They are TOOLS
For Core Brain → It is COMMANDER
```

---

## Why These Rules Exist

| Rule | Reason |
|------|--------|
| Brain Never Executes | Focus on decisions, not actions |
| Brain Never Edits | Consistency through tools |
| Brain Never Browses | Delegation to specialized tools |
| Brain Never Deploys | Controlled deployment through tools |
| Brain Never Compiles | Verification through verification engine |
| Brain Never Searches Web | Focus on internal knowledge |

---

## Related Documents

- [Core-Brain-Overview.md](../01-Core-Brain/01-Core-Brain-Overview.md)
- [Decision-Policies.md](./01-Decision-Policies.md)
