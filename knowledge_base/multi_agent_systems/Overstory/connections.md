> [[index|Wiki]] | [[summary|Summary]]

# Overstory — Connections

## Related entries in this knowledge base
- [[ClaudeOrchestrator/summary|Claude Orchestrator]] — Another coordinator-led coding setup with leads and workers in separate workspaces; useful contrast on how strictly Overstory limits spawning depth and separates merge authority.
- [[AgentOrchestrator/summary|Agent Orchestrator]] — Covers general orchestration patterns for task decomposition and dispatch; Overstory is a stricter instance with fixed roles and file-based task specs instead of chat messages.
- [[HarnessHandbook/summary|Harness Handbook]] — General harness (agent scaffolding) design guidance on runtimes, guards, and quality gates; Overstory implements this via one shared runtime interface plus central blocklists for risky tools and commands.
- [[MultiAgentsWhatsActuallyWorking/summary|Multi Agents Whats Actually Working]] — Empirical notes on what works in multi-agent systems; relevant to Overstory's progressive watchdog escalation and builder-reviewer-lead rework loop before any merge.

## External comparison points
- Fleet orchestrator itself — Sergii's own multi-worker coding orchestrator with a central task store; closest comparison for Overstory's SQLite (embedded file-based database) mail, watchdog supervision, and merge queue.
- CrewAI — Role-based multi-agent framework with defined roles and task handoffs; Overstory is lower-level and git-centered, with isolated worktrees (separate directory checkouts) per worker instead of shared state.
- LangGraph — Graph-based agent orchestration library where control flow is explicit nodes and edges; Overstory fixes the graph into a three-level hierarchy with typed mail signals between levels.
- Claude Squad (open-source tmux session manager) — Manages multiple Claude sessions in tmux (terminal multiplexer) panes for parallel coding; Overstory adds the missing layers of supervision tiers, guarded tool use, and ordered merging.
