> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Sandboxing & Execution

Execution safety is critical when agents can run arbitrary code or make system-level decisions. This section covers isolation techniques, resource bounding, and credential management.

### Isolation Techniques (Strongest to Fastest)

| Technique | Isolation | Overhead | Use Case |
|-----------|-----------|----------|----------|
| Firecracker | Hardware VM | ~100ms startup | High-risk code |
| gVisor | Syscall interception | Moderate | Untrusted containers |
| Docker | Process isolation | Low | Trusted code |
| In-process | None | None | Same-team code |

### Per-Task Isolation

Create a fresh, clean environment for each execution:
- Dedicated filesystem
- Isolated network (allowlist only necessary IPs)
- Bounded resources (CPU, memory, disk, time)
- Credential scoping (minimal secrets)
- Cleanup after completion

### Trust Boundaries

Understand what you trust:
- Trust the model's intent ✓
- Trust the model's code ✗
- Trust your sandbox ✓
- Trust audit logs ✓

### Key Concepts

- **Credential scoping:** Temporary tokens scoped to minimal resources
- **Secrets management:** Never log secrets; use a secrets manager with audit trails
- **Filesystem controls:** Immutable logs, restricted paths
- **Network policies:** Allowlist mode; block by default
- **Resource limits:** CPU, memory, disk, execution time

### Interview Questions

- "I give the agent code to execute. How do you prevent it from exfiltrating secrets?"
- "A container execution times out. What's your recovery? Cleanup?"
- "Design a system where agents can run user-uploaded Python safely."

### Future Sections (To be expanded)

- Docker configuration and best practices
- gVisor deep dive
- Firecracker for microVMs
- Network policy design
- Credential scoping patterns
