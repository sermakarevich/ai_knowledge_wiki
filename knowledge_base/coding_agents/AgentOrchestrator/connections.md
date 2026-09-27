> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ClaudeSquad/summary|Claude Squad]] — Same-problem-different-method: terminal-first parallel runner isolating each agent in its own tmux session plus git worktree, but with a no-adapter design versus AO's 27 compiled-in harness adapters and daemon-owned CI/review lifecycle.
- [[GasTown/summary|Gas Town]] — Same-problem-different-method: a Go implementation running coding agents in tmux/worktrees with beads ledger persistence, versus AO's SQLite fact store with read-time derived status and built-in lifecycle reactions.
- [[OpenOrchestrator/summary|OpenOrchestrator]] — Same-problem-different-method: parallel coding-agent orchestration with its own control plane, contrasting with AO's loopback-only daemon, one-PR-per-session invariant, and explicit human-gated merge.
- [[VibeKanban/summary|VibeKanban]] — Shares-technique: kanban-board supervision of parallel agent tasks (Pending / Iterating / In Review / Ready to merge), matching AO's board columns and session-card model with agent, branch, and PR state.
- [[ClaudeOrchestrator/summary|claude-orchestrator + orchestration-playbook]] — Same-problem-different-method: worktree-per-agent dispatch with merge gates as portable prose discipline (SKILL.md contracts) rather than AO's Go runtime with compiled-in adapters and observer-driven lifecycle.
- [[AutonomousLongRunningCodingAgents/summary|Autonomous Long-Running Coding Agents]] — Shares-technique: supervision patterns for long-running agents (goal/evaluator/loop/verifier) that AO instantiates concretely as daemon heartbeat, SCM observation, and signature-deduplicated nudges to session owners.
