> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[GasTown/summary|GasTown]] — Same-problem-different-method: Go orchestrator with per-worker git worktrees, beads ledger, 13-harness registry, and refinery merge queue, versus Bernstein's Python deterministic tick loop, adapter registry, and serial FIFO merge queue with lineage receipts.
- [[AgentOrchestrator/summary|Agent Orchestrator (AO) — Run Coding Agents in Parallel]] — Same-problem-different-method: local-first control plane where one session owns one worktree plus one PR with 27 compiled-in harnesses, versus Bernstein's adapter registry and janitor plus quality-gate merge path.
- [[ClaudeOrchestrator/summary|Claude Orchestrator + Orchestration Playbook]] — Shares-technique: harness-agnostic orchestration discipline with git mechanics and review gates and no LLM calls of its own, paralleling Bernstein's no-model-in-the-coordination-loop rule.
- [[FactoryMissionsMultiAgentSystem/summary|Factory Missions: Building Multi-Agent Systems for Long-Running Software Development]] — Same-problem-different-method: orchestrator/worker/validator roles with serial workers and validation contracts for long runs, contrasting with Bernstein's parallel worktrees plus gates, bounded retries with model escalation, and dead-letter queue.
- [[OrkesConductor/summary|Orkes Conductor: Agentic Workflow Engine]] — Shares-technique: durable external workflow engine with queues, retries, and audit history that keeps coordination out of model reasoning, like Bernstein's deterministic scheduler, but for general workflows rather than coder CLIs in worktrees.
