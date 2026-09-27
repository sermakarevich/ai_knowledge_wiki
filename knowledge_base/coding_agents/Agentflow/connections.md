> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ApacheBurr/summary|Apache Burr: Build Reliable AI Agents and Applications]] — Same-problem-different-method: both tackle durable, observable agent graphs with state persistence and human-in-the-loop gates; Burr does it as an action-based state machine with tracker UI, Agentflow as a Python Graph DSL with run.json/events.jsonl store and success-criteria retry loops.
- [[AgentSwarm/summary|Agent Swarm -- Multi-Agent Self-Learning Teams (OSS)]] — Same-problem-different-method: both orchestrate fleets of coding-agent CLIs via DAG workflows with approval gates; AgentSwarm adds Docker isolation plus compounding vector memory, Agentflow focuses on declarative fanout/merge graphs with Jinja-wired prompts and on_failure_restart cycles.
- [[ClaudeSquad/summary|claude-squad]] — Shares-technique, complementary layer: both isolate parallel coding agents in git worktrees (Agentflow exposes use_worktree); Claude Squad is a manual tmux+TUI console with no scheduler or task graph, Agentflow is the programmable scheduler and graph above that execution floor.
- [[ClaudeOrchestrator/summary|claude-orchestrator + orchestration-playbook]] — Same-problem-different-method: both coordinate parallel worktree agents through review and merge gates; Claude Orchestrator encodes governance as prose dispatch contracts plus evidence labels, Agentflow encodes it as code via success_criteria, concurrency caps, and max_iterations-bounded restart loops.
