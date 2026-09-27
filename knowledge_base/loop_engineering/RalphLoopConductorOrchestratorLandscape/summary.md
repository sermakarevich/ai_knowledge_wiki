# From Conductor to Orchestrator: Ralph loop, Conductor, and the agent-orchestrator landscape

**Article:** [From Conductor to Orchestrator: A Practical Guide to Multi-Agent Coding in 2026 (Stephane Busso, 2026)](https://htdocs.dev/posts/from-conductor-to-orchestrator-a-practical-guide-to-multi-agent-coding-in-2026/)

## Human Readable TL;DR

Imagine you hire one assistant (a "conductor" setup): you watch every keystroke. Now imagine you run a kitchen (an "orchestrator" setup): several cooks work at separate stations, and you only taste the dishes before they go out. This entry is about three recipes for running that kitchen. The **Ralph loop** is the simplest: give a cook the same recipe card over and over until the dish passes the taste test — the cook forgets everything between attempts, so the recipe card and the pantry (files and git history) are the only memory. **Conductor** is the kitchen counter with a window: every cook gets a separate workstation (a git worktree, i.e. an isolated copy of the code), and you review each dish through the glass before serving. The **meta-lists** are the restaurant guide: which kitchens are open-source, which cost money, and four tiny tools (ralphy, subtask, swarm-protocol, wit) that each solve one chore like claiming orders or labeling ingredients down to the single function.

## TL;DR

The primary source (Busso, htdocs.dev, April 2026) frames 2026 multi-agent coding as a conductor→orchestrator shift across three tiers: in-process agents (subagents, Agent Teams), local orchestrators (Conductor, Claude Squad, Vibe Kanban, OpenCode+OmO), and cloud async (Codex Web, Copilot Coding Agent, Jules). Its load-bearing patterns are the Ralph loop (stateless-but-iterative re-execution with a completion check), worktree isolation, the Architect-Executor-Reviewer loop, and human-approved AGENTS.md memory. Supplemented with the Augment Code "9 Open-Source Agent Orchestrators" roundup, the awesome-agent-orchestrators list, and five Ralph explainers, this entry compares all of it against fleet's queue + retry-table + worktree-merge architecture and distills 7 borrowable ideas (headlined by completion-checks-as-code and a Janitor review stage) plus 5 things fleet should not copy.

---

## Problem & Motivation

A single coding agent hits three walls: context overload (one context window cannot hold a large codebase), no specialization (a generalist writes worse database code than a focused data-layer agent), and no coordination (helpers cannot share a task list or resolve dependencies). The landscape exists to answer: how do you run *several* agents at once without them clobbering each other's work, burning unbounded tokens, or serving unreviewed code? The entry additionally answers fleet's own question: which of these patterns (Ralph's dumb loop, Conductor's review cockpit, the micro-protocols) are worth importing into a headless queue-driven fleet?

---

## Main Original Ideas

1. **The three-tier model.** Every 2026 orchestration tool fits Tier 1 (in-process: subagents, Agent Teams — start here), Tier 2 (local orchestrators: 3–10 agents in isolated worktrees with human review), or Tier 3 (cloud async: assign a task, close the laptop, return to a PR). Smart developers use all three by task shape.
2. **The Ralph loop as stateless-but-iterative execution.** Re-run the same agent on the same prompt file with a fresh context window every pass; persist only in files + git. Pick → Implement → Validate → Commit → Reset. The loop is dumb; the completion check (tests green, COMPLETE tag, all PRD stories passing) is the entire engineering.
3. **Producer/approver separation (back-pressure).** The agent that writes code must not be the one that declares it good. Hard gates (compiler, failing tests) beat soft gates (reviewers you can argue with), which beat pseudo-gates (self-grading). Anthropic's generator/evaluator split and Bernstein's Janitor stage are instantiations.
4. **Worktree isolation as the universal primitive.** Every Tier-2 tool isolates agents in git worktrees (now vendor-native via `claude --worktree`). Isolation is free; *decomposition* (slicing work into non-overlapping pieces) remains the human's hard problem.
5. **Conflict granularity ladder.** Worktrees (file-set isolation, conflicts at merge) → work-claim leases with heartbeats (swarm-protocol: who works on what) → symbol-level locks (wit via Tree-sitter: warn before two agents touch the same function).
6. **Fleet's counter-position: rule-driven re-queue.** Fleet re-runs work too, but via a data-table retry policy (typed outcomes → CLOSE/RELEASE/BLOCK with per-outcome round caps, backoff delays, infra-fault exemptions) and explicit continuation memory (STATE.md/RESULT.json with a single next action) instead of Ralph's goal-file + git-log memory.

---

## Key Findings

- Ralph fits "large, well-specified, mechanically verifiable" work (migrations, coverage backfill, refactors, overnight build-out); Huntley himself would not use it on an existing codebase, and success criteria must be numbers (tests, lint, types, coverage).
- Cost is the loop's shadow: fresh context every pass re-pays input tokens each iteration (Thoughtworks: "significant token cost"); iteration caps are budget controls, not just correctness controls. Self-reported wins (CURSED language, $297–$800 overnight runs) come from the technique's advocates — treat as suggestive, not benchmarked.
- The Conductor *name* covers three different tools: conductor.build (Melty, closed Mac app, diff-first L0 review cockpit), Code Conductor (MIT, GitHub-issue queue), Microsoft Conductor (MIT, YAML workflows with parallel groups — strongest long-term bet).
- Multi-harness breadth leaders (Emdash 34 CLIs, Orca 25+, Bernstein 49 adapters) vs narrow-but-polished (Conductor) vs harness-agnostic-by-construction (bare Ralph bash, ralphy's 6-harness loop).
- Mature setups route by cost: plan expensive, execute cheap, verify independently (OMC claims 30–50% savings from smart routing; OmO routes chores to local Ollama models).
- Agent-written AGENTS.md files show ~−3% success and +20% cost (ETH Zurich, via Busso); developer-written ones +~4%. Memory files must be human-approved.

| Tool / pattern | Isolation | Who checks the work | License / status |
|---|---|---|---|
| Ralph loop (bare) | Fresh context + git | Completion check you wire in | Public pattern |
| ralphy | Same as Ralph | Same as Ralph | Open (bash) |
| subtask | Git worktrees via subagents | You (human) | Claude Skill |
| swarm-protocol | MCP work-claims + heartbeats | Lease/hand-off protocol | Open (MCP) |
| wit | Tree-sitter function locks | Pre-write conflict warnings | Open (protocol) |
| Conductor (Melty) | Worktrees, Mac app | You, diff-first UI | Closed source |
| Microsoft Conductor | YAML workflow | Deterministic scheduler + HITL (human in the loop) | MIT |
| Bernstein | Worktrees + Janitor gate | Deterministic scheduler + Janitor | Apache-2.0 |
| Fleet | Worktrees + merge validation | Retry table + merge gate (no per-task exec predicate yet) | Own repo |

---

## Suggestions & Future Directions

1. **Adopt completion-checks-as-code per bead** (fleet's highest-value import): an executable done-predicate the reaper runs before honoring close requests.
2. **Add a Janitor review stage** between worker-finish and merge (read-only lint/test/security reviewer, ~1 per 3–4 builders).
3. **Kill + reassign after 3+ stuck iterations** instead of burning further rounds on the same ladder (escalate model/harness or human).
4. **Emit function-level conflict warnings** by diffing changed symbols across in-flight beads (wit-inspired, merge-time).
5. **Add worker heartbeats** to separate "slow but alive" from "stalled" and cut false stall-kills.
6. **Route harnesses by cost** per bead kind (cheap/local for grind, frontier for planning/review); spend the budget on the *check*, not the loop.
7. **Keep accumulated memory human-approved** — never let workers append to convention files unreviewed.
8. Explicitly avoid: unbounded loops without budgets, agent-written memory, review dashboards for their own sake, single-vendor coupling, kanban-lane workflow duplication.

---

## Authors & Institutions

Primary: Stephane Busso (engineering leader; htdocs.dev). Supplement authors: Addy Osmani (2026 trends / code-agent orchestra framing), Dan Mindru (ralphloop.sh), Thomas Wiegold (Ralph practice), Yanli Liu (harness=loop thesis), Ankit Jain (Aviator orchestrator rise), Augment Code team (9-OSS roundup), andyrewlee (awesome list), OpenAlternative/Nimbalyst/DEV authors (comparison tables, supervision ladder). Fleet-side grounding: fleet repo `src/fleet/core/retry_policy.py`, `src/fleet/orchestrator/worktree.py`, `reap.py`, `merge_validation.py`.

## Figures

Omitted — the primary article's diagrams (conductor→orchestrator shift, three-tier model, Architect-Executor-Reviewer loop, Ralph loop cycle) are referenced by name in `wiki/targeted.md` prose; no images were extracted (headless run, no browser capture). Revisit with screenshots if the entry is ever promoted to a full wiki.
