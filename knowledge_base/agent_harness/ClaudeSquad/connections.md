> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[multi_agent_systems/ClaudeCodeAgentFarm/summary|Claude Code Agent Farm]] — Closest filed relative: orchestrates N parallel Claude Code sessions in tmux panes with health monitoring and auto-restart, the same tmux-per-agent isolation Claude Squad uses, but adds autonomous backlog-draining where Claude Squad stays a manual single-operator console.
- [[coding_agents/ParallelAgenticDevelopment/summary|Parallel Agentic Development]] — Same-problem-different-method: five-or-more parallel Claude Code agents via git worktrees with per-agent isolation and coordination patterns, the worktree half of Claude Squad's instance-worktree-session triad with a practical 5–8 agent cap versus Claude Squad's hard cap of 10.
- [[claude_ecosystem/RunClaudeCodeParallel/summary|Run Claude Code Parallel]] — Direct practitioner context: five methods for parallelizing Claude Code sessions where Git Worktrees handles ~80% of cases, framing Claude Squad's tmux + worktree combination as one point in that larger solution space.
- [[claude_ecosystem/ClaudeCodeWorktreesGuide/summary|Claude Code Worktrees Guide]] — Shares-technique: git worktrees giving each Claude Code session its own isolated branch for safe concurrent agents, the same filesystem-isolation mechanism Claude Squad pairs with one tmux session per agent.
- [[research/GasTown/summary|GasTown]] — Same-problem-different-method at larger scope (unfiled, research/): Go orchestrator spawning coder CLIs in tmux sessions on isolated worktree branches, but adds a beads ledger, convoy feeder, daemon supervision, and refinery merge queue that Claude Squad deliberately omits.
- [[research/VibeKanban/summary|Vibe Kanban]] — Applies-in-practice alternative UI over the same primitive (unfiled, research/): kanban board where each issue runs in an isolated git worktree with its own agent run and diff-to-PR review, versus Claude Squad's Bubble Tea TUI list with preview/diff/terminal tabs.
