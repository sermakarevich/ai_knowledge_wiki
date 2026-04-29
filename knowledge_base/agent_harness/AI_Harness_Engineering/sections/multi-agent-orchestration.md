> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Multi-Agent Orchestration

As systems scale, you often need multiple agents coordinating on complex problems. This section covers composition patterns, durable orchestration, and failure handling across agents.

### Single vs. Multi-Agent Decision

**Use a single agent when:**
- Problem fits in one conversation
- One tool/knowledge set needed
- Latency matters more than capability

**Use multiple agents when:**
- Problem requires different expertise (specialist agents)
- High concurrency needed
- Cost optimization by routing to cheaper agents
- Fault isolation (one agent failing doesn't block others)

### Composition Patterns

**Pattern 1: Sequential Handoff**
```
Agent1 (data retriever) → Agent2 (analyzer) → Agent3 (approver)
Each agent takes the output of the previous as input.
```

**Pattern 2: Parallel Branching**
```
Agent1, Agent2, Agent3 run in parallel on different sub-problems.
Results are merged by a coordinator.
```

**Pattern 3: Hierarchical**
```
Coordinator Agent delegates to Specialist Agents (customer, product, refunds).
Specialists return results; coordinator synthesizes.
```

### Durable Orchestration

Multi-agent systems must be durable (survive failures):
- Checkpoints: Save state after each step
- Idempotency: Retrying doesn't cause double-execution
- Timeouts: Each agent call has a deadline
- Fallbacks: If Agent A times out, try Agent B

### Handoff Protocols

When Agent1 passes state to Agent2:
1. Include complete context (what have we learned?)
2. Include decision history (why we got here)
3. Include deadlines (how much time left?)
4. Include failure modes (what went wrong before?)

### Failure Handling

| Failure | Recovery |
|---------|----------|
| Agent times out | Escalate to human or try fallback agent |
| Agent returns error | Log error; try different approach |
| Agents disagree | Escalate for human arbitration |
| Cascade of failures | Circuit breaker; stop retrying |

### Interview Questions

- "Design a 3-agent system for customer support: routing → analysis → decision."
- "What goes in the handoff state between agents?"
- "One agent fails; the others complete. How do you handle partial results?"

### Future Sections (To be expanded)

- Orchestration frameworks (LangGraph, etc.)
- Checkpointing and recovery
- Inter-agent messaging patterns
- Distributed tracing across agents
- Cost optimization with agent routing
