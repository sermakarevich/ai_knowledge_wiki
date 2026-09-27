> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[AgentOrchestrator/summary|Agent Orchestrator (AO)]] — same-problem-different-method: AO gates shipping with inspector sign-off (tests + review), owt trusts human keystrokes + diff glance; the two designs bracket the autonomy-vs-safety tradeoff for fleet's ship path.
- [[ClaudeOrchestrator/summary|claude-orchestrator + orchestration-playbook]] — shares-technique (worktree isolation, hook-driven status, plan-first discipline) but owt generalizes the harness layer to 5+ providers via a capability-flag plugin protocol where claude-orchestrator is Claude-only.
- [[RalphLoopConductorOrchestratorLandscape/summary|From Conductor to Orchestrator]] — landscape that already compares fleet against Conductor/Claude Squad/Vibe Kanban; owt slots into its "local orchestrator" tier as the tmux+herdr, Conflict-Guard-equipped entry, and its 7 borrowable ideas extend that entry's fleet-borrow list without duplicating it.
- [[AgentSwarm/summary|Agent Swarm]] — contrasts delegation topology: Agent Swarm uses manager-agent hierarchy with shared memory, owt uses human-supervisor + isolated worktrees with a shared status DB; owt's MCP peer messaging (`list_peers/send_message`) is the thin overlap point between the two.
- [[OrchestratingAICodeReviewAtScale/summary|Orchestrating AI Code Review at Scale]] — applies-in-practice complement: Cloudflare's 7-reviewer coordinator is the correctness-gate layer owt lacks; pairing owt-style lanes/verbs for triage with reviewer-swarm gates for ship approval is a plausible combined design.
