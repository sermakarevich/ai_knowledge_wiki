# Claude Ecosystem

Research and documentation on **Anthropic's Claude models and Claude Code** — system cards, best practices, migration guides, leaked/reverse-engineered internals, and Mythos.

## Papers

- [[ClaudeCodeAutoMode]] — Two-layer classifier (prompt-injection + transcript) enables safe autonomous Claude Code; 0.4% false-positive rate.
- [[ClaudeCodeDynamicWorkflows/summary]] — JavaScript scripts executed by the runtime orchestrate up to 1,000 subagents per run; plan lives in code not context, enabling scale, resumability, and adversarial cross-checking.
- [[ClaudeCodeMemory]] — Analysis of Claude Code's 6-layer memory hierarchy; MEMORY.md is a pointer index, not storage.
- [[ClaudeCodeRoutines/summary]] — Managed automation that turns Claude Code into a proactive agent; schedule- or GitHub-event triggered sessions run on Anthropic-managed infra with real-time steerability.
- [[ClaudeCodeSourceAnalysis]] — Deep reverse-engineering of Claude Code's leaked source; 50-line TAOR loop + deterministic scaffolding.
- [[ClaudeForCreativeWork/summary]] — Anthropic launches eight MCP-based connectors integrating Claude into creative tools (Adobe, Blender, Ableton, Fusion); in-tool tutoring, scripting, and batch automation.
- [[ClaudeMigrationGuide/summary]] — Official Anthropic migration guide for Opus 4.7/Sonnet 4.6/Haiku 4.5 with adaptive thinking + new `effort` param.
- [[ClaudeOpus47BestPractices/summary]] — Opus 4.7 uses adaptive (not fixed-budget) thinking; `xhigh` effort level recommended default.
- [[ClaudeOpus47SystemCard/summary]] — Opus 4.7 leads SWE-bench at 87.6%; no new ASL tier; improved prompt-injection robustness.
- [[ClaudeOpus47SystemPrompt/summary]] — Leaked 1,408-line operational prompt: search-first behavior, copyright constraints, refusal tripwires.
- [[DiveIntoClaudeCode/summary]] — Source-level analysis of Claude Code v2.1.88: only 1.6% AI logic, 98.4% deterministic infrastructure.
- [[SystemCardClaudeMythosPreview]] — Anthropic's most capable model restricted to defensive cybersecurity partners; best-aligned yet highest-risk.
- [[AHarnessForEveryTask/summary]] — Claude writes custom JS harnesses on the fly to orchestrate parallel subagents; combats agentic laziness, self-preferential bias, and goal drift across 10+ use cases.
- [[HowWeClaudeCode/summary]] — Anthropic workshop covering three Claude Code practices: Claude-as-interviewer for spec extraction, HTML design explorations over markdown specs, and agent-native DOM contract verification via Storybook + Playwright MCP.
- [[ClaudePersonalGuidance/summary]] — 6% of Claude conversations are personal guidance; sycophancy peaks at 25% in relationships (vs 9% overall); targeted training in Opus 4.7/Mythos Preview halved the relationship rate.
- [[ClaudeAgentTeams/summary]] — Multiple independent Claude Code instances share a file-locked task list and mailbox; best for parallelizable review or research, not sequential or same-file work.
- [[ClaudeFable5AndMythos5/summary]] — Anthropic releases Fable 5 (public) and Mythos 5 (gated to vetted researchers); tiered access separates capability from guardrails; Fable 5 silently reroutes flagged requests to Opus 4.8 rather than refusing.
- [[MyWeekWithFable/summary]] — Week-long practitioner review of Fable (MYTHOS): best-in-class for long-horizon agentic tasks and parallel-agent workflows; needs tuning on verbosity, over-confirmation, and speed.
- [[DesigningLoopsWithFable5/summary]] — Rubric-based feedback loops (`/goal` in Claude Code, `Outcomes` in CMA) let Fable 5 hillclimb autonomously; ~6x improvement over Opus 4.7 on ML optimization, 73% cross-session memory verification coverage.
- [[RunClaudeCodeParallel/summary]] — Five methods for parallelizing Claude Code sessions (Terminal Panes, Git Worktrees, Subagents, Agent Teams, Docker); Git Worktrees handles ~80% of cases and is the recommended starting point.
- [[ClaudeCodeWorktreesGuide/summary]] — Git worktrees give each Claude Code session its own isolated branch, enabling safe concurrent parallel agents; `--worktree`, Desktop auto-isolation, and `isolation: worktree` frontmatter cover all opt-in modes.
