> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[GasTown/summary|gastown]] — Same-problem-different-method: parallel coder orchestration with per-worker git worktrees and a data-driven harness registry, but as a Go daemon with tmux sessions, beads ledger, and refinery merge queue rather than Vibe Kanban's Rust server with kanban board UI and per-adapter trait impls.
- [[AgentOrchestrator/summary|Agent Orchestrator (AO) — Run Coding Agents in Parallel]] — Same-problem-different-method: local-first control plane for parallel coding agents with isolated worktree + branch + PR per session and read-time derived status, using 27 compiled-in harnesses versus Vibe Kanban's ten-variant `StandardCodingAgentExecutor` trait.
- [[ClaudeOrchestrator/summary|claude-orchestrator + orchestration-playbook]] — Same-problem-different-method: worktree-per-agent dispatch with evidence checks and merge gates, but as portable prompt/skill discipline rather than Vibe Kanban's executable server, container service, and diff WebSocket review flow.
- [[AgenticCodeReview/summary|Agentic Code Review]] — Same review bottleneck: agent code volume outruns human reading speed, so review depth tiers by blast radius and intent artifacts are required; Vibe Kanban's worktree-vs-base diff stream plus review-comments-to-next-prompt is the tooling half of that prescription.
- [[OpenCodeReview/summary|open-code-review]] — Shares-technique: LLM-assisted review grounded in full-file context rather than diff text alone; contrasts with Vibe Kanban's human diff review in the UI, where inline comments are ephemeral browser state serialized into the follow-up prompt.
