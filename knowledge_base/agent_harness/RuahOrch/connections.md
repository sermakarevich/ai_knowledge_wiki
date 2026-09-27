> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ClaudeSquad/summary|Claude Squad]] — same-problem-different-method: both isolate parallel coding agents in git worktrees, but Claude Squad multiplexes via tmux with no coordination contract while ruah enforces declared file-claim locks with pre-start rejection and post-execution validation.
- [[GasTown/summary|GasTown]] — shares-technique: both coordinate harness agents in git worktrees, but GasTown tracks work in a beads-backed system (Go) while ruah tracks it in a single revision-guarded JSON state file with claim-aware scheduling.
- [[AgentOrchestrator/summary|Agent Orchestrator]] — same-problem-different-method: both run parallel coding agents in isolated worktrees with PR-style merge lifecycles, but ruah adds the file-claim contract layer (owned/shared-append/read-only) and artifact receipts that AO-style runners leave to convention.
- [[ClaudeOrchestrator/summary|Claude-Orchestrator]] — shares-technique: both pursue harness-agnostic orchestration (executor adapters vs dispatch contracts), but Claude-Orchestrator emphasizes evidence levels and acceptance rules while ruah emphasizes file-ownership enforcement and dependency-ordered merges.
