> [[index|Wiki]] | [[summary|Summary]]

# Ralph loop + Conductor + orchestrator landscape — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-ralph-loop-mechanics|Ralph loop mechanics]]

**In one sentence:** The Ralph loop re-runs the same agent on the same prompt file with a fresh context window every pass, keeping all memory in files and git, and stops only when an externally wired completion check (tests green, COMPLETE tag, all PRD stories passing) says done.

- Ralph loop = `while :; do cat PROMPT.md | <agent>; done` plus a completion check (tests pass or a COMPLETE tag); state lives on disk and git, each pass starts with a fresh context window.
- The one-item rule drives progress: one task per pass (highest-priority not-done story in `tasks.json` / `prd.json`), then commit and exit, so a crashed agent loses at most one task.
- Fresh context is the whole trick: long sessions rot as the window fills with chatter, so the loop refuses conversational memory and treats the repository as the memory.
- Packaged variants add iteration caps (budget control), typed stop tags (`COMPLETE` / `BLOCKED` / `DECIDE` with exit codes in `ralph.sh`), per-task verification stacks (typecheck + tests + lint), and multi-backend support.
- Ralph fits only "large, well-specified, mechanically verifiable" work (migrations, coverage backfill, refactors); Huntley himself would not use it on an existing codebase, and success criteria must be numbers.
- Cost is the loop's shadow: every pass re-pays input tokens for the full prompt (Thoughtworks flags "significant token cost"), so iteration caps are budget controls, and self-reported overnight wins ($297–$800 runs) are suggestive, not benchmarked.
- Producer and approver must be separate: the agent that writes code must not declare it good — hard gates (compiler, failing tests) beat soft gates (arguable reviewers), which beat pseudo-gates (self-grading).

## 2. [[wiki/02-conductor-worktrees-review|Conductor: worktrees plus review dashboard]]

**In one sentence:** Conductor (Melty Labs, closed-source Mac app) runs 3–8 parallel agents in isolated git worktrees behind a diff-first review UI where the human is the scheduler, merger, and quality gate.

- Conductor (Melty Labs, YC S24, closed-source Mac app) = one isolated git worktree per agent plus visual dashboard plus diff-first review UI plus checkpoints and rollback; the human is the scheduler, merger, and quality gate.
- One isolated git worktree per agent means each agent owns its own working directory on its own branch, so there are no merge conflicts during parallel work; worktrees with no changes auto-clean and ones with changes persist for review.
- The dashboard answers "who is working on what", but the product is the review flow: file-by-file diffs, checkpoints, rollback, PR creation — review throughput is the whole product.
- In supervision-ladder terms (L0–L4) Conductor is L0, "you are the loop": no programmatic surface, no API, macOS only, closed source, and it does not decompose work, assign tasks, or verify quality itself.
- Multi-model compare runs parallel attempts (including different models) and keeps the best.
- The Conductor name covers three different tools: conductor.build (Melty, closed Mac app, diff-first L0 review cockpit), Code Conductor (MIT, GitHub-issue queue), and Microsoft Conductor (MIT, YAML workflows with parallel groups — strongest long-term bet).
- Worktrees give isolation for free but not decomposition: two agents editing the same file in different worktrees still conflict at merge, so human file-ownership mapping ("no two agents own the same file") is the manual fix.

## 3. [[wiki/03-micro-patterns|Micro-patterns: ralphy, subtask, swarm-protocol, wit]]

**In one sentence:** Four tiny open tools each solve one chore the bare Ralph loop leaves out — ralphy (run the loop on any CLI), subtask (fan work out into worktrees), swarm-protocol (claim work and prove liveness), and wit (lock single functions before writing).

- ralphy (michaelshimeles) is the multi-harness Ralph: one bash script looping Claude Code, Codex, OpenCode, Cursor, Qwen, or Droid until done — the "runs anywhere" Ralph.
- subtask is a Claude Skill that runs tasks through subagents in git worktrees with the workflow "one parent, N file-owned children": cost-neutral fan-out where the human still coordinates.
- swarm-protocol is a coordination protocol over MCP (Model Context Protocol — a standard way for agents to call tools): claim work, detect file conflicts, heartbeat, hand off across sessions, so the workflow is a lease on a work item, not a graph.
- wit is an intent-plus-lock protocol: agents declare intents and acquire symbol-level locks (parsed via Tree-sitter, a code-parser library) before writing, warning about conflicts before they happen instead of at merge.
- Together they form a conflict-granularity ladder: worktrees (file-set isolation, conflicts at merge) → work-claim leases with heartbeats (who works on what) → symbol-level locks (warn before two agents touch the same function).
- Multi-harness breadth leaders (Emdash 34 CLIs, Orca 25+, Bernstein 49 adapters) vs narrow-but-polished (Conductor) vs harness-agnostic-by-construction (bare Ralph bash, ralphy's 6-harness loop).
- Mature setups route by cost: plan expensive, execute cheap, verify independently (OMC claims 30–50% savings from smart routing; OmO routes chores to local Ollama models).

## 4. [[wiki/04-fleet-comparison|Fleet comparison: what to borrow, what not to copy]]

**In one sentence:** Fleet already owns the retry-table and worktree-merge slices of this landscape while missing completion-checks-as-code and fine-grained conflict guards, so it should borrow seven concrete mechanisms and explicitly refuse five others.

- Fleet's retry/re-queue is a superset of the bare loop's persistence idea but rule-driven, not goal-driven: a data table (`retry_policy.py:decide()`) maps each attempt outcome to CLOSE/RELEASE/BLOCK with per-outcome round caps, and STATE.md/RESULT.json carry the "what next" memory the Ralph loop keeps in `tasks.json`/git log.
- Fleet knows what "failed" means (a table it applies) but has no per-task executable completion predicate of the Ralph kind — the worker declares done and the table believes it, so completion-checks-as-code is the single highest-value import.
- Workflow abstraction compared: Ralph has almost none (a task list file); Conductor's workflow is the review queue; Microsoft Conductor and Bernstein add real abstractions (YAML parallel groups; Goal → Planner → Task Graph → Janitor → merge pipeline); fleet has beads + queue + retry table, closest to Microsoft Conductor plus Bernstein's verify-before-merge.
- Borrow list: 7 concrete ideas (completion-check gates, Janitor reviewer, stale-iteration kill + reassign, YAML/static workflow option, work-claim heartbeats, function-level conflict warnings, AGENTS.md human-approved memory).
- Do NOT copy: unbounded loops without budgets, agent-written memory files, single-vendor lock-in, kanban-for-kanban's-sake dashboards, kanban lanes as workflow.
- Agent-written AGENTS.md files show ~−3% success and +20% cost (ETH Zurich, via Busso) while developer-written ones help ~+4%: memory files must stay human-approved and workers must never append unreviewed.
- Fleet's typed restarts (stall-kill ladder, lease expiry, context-pressure path, shutdown-exempt re-queue) already approximate the wild's workload watchdogs; the gap is goal verification, not loop machinery.

## The argument in five moves

1. One agent forgets and rots, so wipe its memory every pass and keep the truth in files and git (Ralph).
2. Many agents collide, so isolate each in its own worktree and review the diffs before merging (Conductor).
3. Isolation is coarse, so add finer guards where they pay: leases for who-works-on-what, locks for who-touches-what-function (micro-patterns).
4. Fleet already has the coarse half (retry table, worktrees, merge gate) but grades its own homework — no executable done-check per task.
5. Close the gap with borrowed gates (completion checks, Janitor, heartbeats, symbol warnings) while refusing the traps (unbounded loops, agent-written memory, dashboards, lock-in).
