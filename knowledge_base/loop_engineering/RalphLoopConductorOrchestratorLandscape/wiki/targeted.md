> [[index|Wiki]] | [[summary|Summary]]

# Targeted comparison: Ralph loop, Conductor, micro-protocols — and what fleet should borrow

**In one sentence:** The Ralph loop (dumb re-run loop + smart completion check), Conductor (worktree agents + diff-first human review), and four micro-patterns (ralphy, subtask, swarm-protocol, wit) each solve one slice of unattended agent work, and fleet already owns the retry-table and worktree-merge slices while missing completion-checks-as-code and fine-grained conflict guards.

## Key points

- Ralph loop = `while :; do cat PROMPT.md | <agent>; done` plus a completion check (tests pass or a COMPLETE tag); state lives on disk/git, each pass starts with a fresh context window.
- Fleet's retry/re-queue is a superset of the bare loop's persistence idea but rule-driven, not goal-driven: a data table (`retry_policy.py:decide()`) maps each attempt outcome to CLOSE/RELEASE/BLOCK with per-outcome round caps, and STATE.md/RESULT.json carry the "what next" memory the Ralph loop keeps in `tasks.json`/git log.
- Conductor (Melty Labs, closed-source Mac app) = one isolated git worktree per agent + visual dashboard + diff-first review UI + checkpoints/rollback; the human is the scheduler, merger, and quality gate.
- Workflow abstraction: Ralph has almost none (a task list file); Conductor's workflow is the review queue; Microsoft Conductor and Bernstein add real abstractions (YAML parallel groups; Goal → Planner → Task Graph → Janitor → merge pipeline).
- Multi-harness: ralphy and Emdash/Orca-style orchestrators run many CLIs (Claude Code, Codex, OpenCode, Cursor, Qwen, Droid); Ralph/Conductor are harness-thin; fleet spawns headless coder workers per task in isolated worktrees.
- Conflict handling: worktrees (Conductor, subtask, fleet) give file-level isolation; swarm-protocol adds MCP work-claiming + heartbeats; wit goes finer with Tree-sitter function-level locks.
- Borrow list: 7 concrete ideas (completion-check gates, Janitor reviewer, stale-iteration kill + reassign, YAML/static workflow option, work-claim heartbeats, function-level conflict warnings, AGENTS.md human-approved memory). Do NOT copy: unbounded loops without budgets, agent-written memory files, single-vendor lock-in, kanban-for-kanban's-sake dashboards.

---

## 1. Ralph loop mechanics — and how fleet's retry/re-queue compares

### The loop, stripped to its parts

The Ralph loop, popularized by Geoffrey Huntley in July 2025 and named after Ralph Wiggum ("deterministically simple in an unpredictable world"), is three things plus a rule:

1. **A prompt file** (`PROMPT.md`) holding the goal and the definition of done.
2. **A shell loop** re-running the same coding agent against that prompt: `while :; do cat PROMPT.md | claude -p --dangerously-skip-permissions; done`.
3. **A completion check** that decides when to stop: tests passing, a `COMPLETE` promise tag in output, or every story in a PRD (product requirements document) file reading `passes: true`.
4. **The one-item rule:** one task per pass, then commit and exit. Each pass starts with a **fresh context window** (the model's short-term memory is wiped); everything persistent — code, task list (`tasks.json` / `prd.json` / `progress.txt`), decisions — lives in files and git history.

Why it works: long agent sessions rot — the context window fills with the agent's own chatter, it forgets early instructions, quality decays. The loop refuses to carry memory in the conversation at all; the repository *is* the memory. Many forgetful agents, each slightly useful, accumulate into steady progress via git.

Packaged versions add what the bare one-liner lacks: iteration caps (budget control), real stop conditions (`COMPLETE` / `BLOCKED` / `DECIDE` tags with exit codes 0/1/2/3 in `ralph.sh`), per-task verification stacks (typecheck + tests + lint before a task counts as done), and multi-backend support (see ralphy below).

### How fleet compares

Fleet's retry/re-queue is the same *shape* (re-run until done, state on disk) but a different *mechanism* — rule-driven rather than goal-driven:

| Aspect | Ralph loop | Fleet |
|---|---|---|
| What repeats | The whole agent on the same prompt | The task via re-queue (RELEASE action) |
| Stop condition | Completion check: tests green / COMPLETE tag / all stories pass | Retry table verdict: CLOSE (done + close requested), BLOCK (round cap exhausted), RELEASE (try again) |
| Round counting | Iteration cap (flat number) | Trailing same-outcome streaks counted from `attempts.jsonl` — separate ladders per outcome (stall, failure, partial, no-close, context), caps in `core/limits.py` |
| Memory between passes | `tasks.json` + git log | `STATE.md` + `RESULT.json` (`summary`, `next_step`, `blocked_reason`) — the single next action is explicit, not inferred from a task list |
| Delays/backoff | None (hot loop) | `retry_after` timestamps + backoff ladders (e.g. failure waits 60/300/900s) so a not-ready task does not spin |
| Fault classification | None — every exit looks the same | Typed outcomes (SUCCESS/KILLED/FAILURE/PARTIAL...); infra faults (`supervisor_shutdown`) re-queue free without consuming a round |
| Verification | External check the loop author wires in | Merge validation for worktrees (clean + ahead-of-base check before merge) |

The honest summary: fleet has the *loop machinery* (arguably better — typed outcomes, backoff, free re-queue for infra faults) but not the *goal machinery*. A Ralph loop knows what "done" means (a check it can run); fleet knows what "failed" means (a table it can apply). Fleet re-queues on `partial`/`failure` but has no per-task executable completion predicate of the Ralph kind — the worker *declares* done and the table believes it. That is the gap Ensuring-Completion-as-Code would close (see section 6).

## 2. Conductor design: worktrees + review dashboard

Conductor (by Melty Labs, YC S24) is the polished Tier-2 "local orchestrator": your machine spawns 3–8 parallel agents, you stay in the loop with dashboards, diff review, and merge control. Its design has four pillars:

1. **One isolated git worktree per agent.** Each agent gets its own working directory on its own branch — no merge conflicts *during* parallel work. (Since Claude Code v2.1.49 this is vendor-native: `claude --worktree feature-auth`.) Worktrees with no changes auto-clean; ones with changes persist for review.
2. **Diff-first review UI.** The dashboard answers "who is working on what", but the product is the review flow: file-by-file diffs, checkpoints, rollback, PR creation. Review throughput is the whole product.
3. **Human as scheduler and merger.** Conductor does not decompose work, assign tasks, or verify quality itself — you do. In supervision-ladder terms (L0–L4, from the DEV comparison): Conductor is L0, "you are the loop". No programmatic surface, no API, macOS only, closed source.
4. **Multi-model compare:** run parallel attempts (including different models) and keep the best.

Do not confuse the three Conductors (Augment Code roundup): **conductor.build** (Melty, closed, Mac desktop, reviewed here) vs **Code Conductor** (ryanmac, MIT, GitHub-native CLI where agents claim `conductor:task`-labeled issues) vs **Microsoft Conductor** (MIT, YAML-defined multi-agent workflows with static/dynamic parallel groups, sub-workflows, conditional routing, web dashboard — the most credible long-term bet of the three).

Fleet parallel: fleet *is* a Tier-2 local orchestrator in the same sense — per-task worktrees on `fleet/<task_id>` branches, merge validation, GC of stale worktrees — but headless and queue-driven rather than dashboard-driven: beads (tasks) are claimed by workers instead of agents being watched by a human. Fleet automated the dispatch; Conductor perfected the review.

## 3. Workflow abstraction in each pattern

"Workflow abstraction" = how the pattern *represents* multi-step work (if at all):

- **Ralph loop: a task list file.** `tasks.json` / `prd.json` (highest-priority not-done story wins, one per pass). No dependencies, no branching, no types — the weakest abstraction that works, and the reason Ralph fits only "large, well-specified, mechanically verifiable" work.
- **Conductor (Melty): the review queue.** The workflow *is* the set of open worktrees awaiting human review. No machine-readable plan at all.
- **Microsoft Conductor: YAML workflows.** Static and dynamic parallel groups, reusable sub-workflows with templated input mapping, script/terminate steps, dialog mode, conditional routing — with no LLM in the orchestration loop (deterministic scheduling, LLM only inside steps).
- **Bernstein: a typed pipeline.** Goal → LLM Planner → Task Graph → Orchestrator → parallel Agents → Janitor (verify) → git merge → main. The Janitor (pre-merge quality gate that caught a type error in the reviewer's test) is the standout idea: verification as a pipeline *stage*, not a hope.
- **subtask: worktree fan-out as a Skill.** A Claude Skill that runs tasks through subagents in git worktrees — the workflow is "one parent, N file-owned children", cost-neutral, human-coordinated.
- **swarm-protocol: a coordination protocol over MCP.** Claim work, detect file conflicts, heartbeat, hand off across sessions. The workflow is a *lease on a work item*, not a graph.
- **wit: intent + lock protocol.** Agents declare intents and acquire symbol-level locks (parsed via Tree-sitter, a code-parser library) before writing — the workflow is defined by what is *locked*, not by a plan.
- **Fleet: beads + queue + retry table.** Work items are beads with dependencies; the queue orders them; the retry table governs re-entry; STATE.md/RESULT.json carry continuation. Closest in spirit to Microsoft Conductor (deterministic orchestration, LLM inside steps) plus Bernstein's verify-before-merge (fleet's merge validation).

## 4. Multi-harness support

"Multi-harness" = can the pattern drive more than one coding-agent CLI (Claude Code, Codex, OpenCode, Cursor, Gemini, Qwen...)?

- **Ralph core: harness-agnostic by construction.** The loop is just bash around *any* headless CLI (`claude -p`, `codex exec`, `cursor-agent`, `aider --message`, Goose with cross-model review). Thinness is the feature: zero harness lock-in, but also zero harness help (you wire flags like `--dangerously-skip-permissions` yourself).
- **ralphy (michaelshimeles): the multi-harness Ralph.** One bash script looping Claude Code, Codex, OpenCode, Cursor, Qwen, or Droid until done — the "runs anywhere" Ralph. (Most starred packaging of the pattern alongside snarktank/ralph at ~21k stars and vercel-labs/ralph-loop-agent.)
- **Conductor (Melty): narrow.** Claude Code, Codex, Cursor, OpenCode — the Mac GUI crowd. No harness abstraction to speak of.
- **Orchestrator tier (Emdash/Orca/Superset): widest.** Emdash auto-detects 34 installed CLIs; Orca claims 25+; Agent Orchestrator (Composio) registers 26 worker harnesses; Bernstein 49 adapters (3 proven for production). These are the true multi-harness players.
- **Fleet: headless multi-coder.** Fleet dispatches each bead to a headless coder worker (cheaper models for grind work, stronger ones for planning/orchestration — the same routing instinct as Oh My OpenAgent's multi-model config, which routes explore/librarian chores to local Ollama models and orchestration to frontier models). Isolation per task makes harness choice per-task safe.

The pattern to note: nobody runs *one* harness everywhere. The mature setups route by cost — plan expensive, execute cheap, verify independently (DEV piece's "route by cost" rule; OMC's 30–50% savings claim from smart routing).

## 5. Conflict and restart handling

Two failure axes: agents colliding with *each other* (conflicts) and agents dying mid-work (restarts).

**Conflicts (three granularity levels, finest last):**

1. **Worktree/branch isolation** (Conductor, subtask, Claude Squad, fleet): each agent owns a directory + branch. Free isolation during work; conflicts surface only at merge. Fleet adds merge validation (refuse to merge a dirty or not-ahead worktree) and GC of stale worktrees. Limitation, per Osmani: worktrees give isolation for free but *not* decomposition — two agents editing the same file in different worktrees still conflict at merge. Human file-ownership mapping ("no two agents own the same file") is the manual fix.
2. **Work-claim + heartbeat leases** (swarm-protocol, NEEDLE's bead queue, fleet's queue): atomic claims on work items, heartbeats proving liveness, hand-off across sessions. Solves *who works on what*; says nothing about *what files they touch*.
3. **Symbol-level locks** (wit): Tree-sitter AST (abstract syntax tree — the code's grammatical structure) parsing lets agents lock individual *functions*, declaring intent and getting conflict warnings *before* writing. Finest granularity in the landscape; the only pattern that prevents same-file collisions rather than detecting them at merge.

**Restarts (who resumes dead work):**

- **Ralph:** restart *is* the design — every pass is a restart from disk state. A crashed agent loses at most one task. No watchdog needed because the loop never expected the agent to survive.
- **Fleet:** typed restarts — stall-kill ladder (kill + re-queue, counting rounds), lease expiry (re-queue immediately), context-pressure path (re-queue for a compacted retry), shutdown-exempt re-queue. Plus a workload watchdog idea exists in the wild (Claude Code Agent Farm auto-restarts stalled agents; amux's self-healing watchdog) that fleet's stall ladder already approximates.
- **Conductor:** no restarts — a dead agent is a dead pane; the human respawns it. L0 means the human is the watchdog.

## 6. What fleet can borrow (7 ideas) — and what NOT to copy

### Borrow

1. **Completion checks as code (the Ralph gate).** Let each bead declare an executable done-predicate (tests, lint, typecheck, or a tag) that the reaper runs before honoring a close request. Today the worker *says* done; borrow Ralph's rule — a producer that grades its own homework is a pseudo-gate. This is the single highest-value import.
2. **A Janitor stage (from Bernstein).** A read-only reviewer (lint + test + security scan) between worker-finish and merge, ~1 reviewer per 3–4 builders. Fleet's merge validation checks *git hygiene* (clean, ahead); a Janitor would check *code correctness*.
3. **Stuck-iteration kill + reassign (Ralph safeguard).** Feed errors back for auto-retry, but after 3+ stuck iterations on the same bead, kill and reassign (different model/harness, or escalate to human) instead of burning another round on the same ladder.
4. **Function-level conflict warnings (from wit).** Before merge, diff the bead's changed symbols against other in-flight beads' changed symbols; warn (or block) on overlap. Cheaper than full wit integration; catches the same-file-different-worktree collision that worktrees alone miss.
5. **Heartbeat work-claims for long beads (from swarm-protocol).** Short heartbeats from running workers so the supervisor can distinguish "slow but alive" from "stalled" without waiting for the full stall timeout — fewer false stall-kills.
6. **Cost-routed harness choice (multi-model routing).** Record per-bead-kind cost/quality and route grind (lint fixes, coverage backfill) to cheap/local models, planning and review to strong ones. Ralph's reframing helps: the loop is cheap, the *check* is where the money should go.
7. **Human-approved memory files (AGENTS.md discipline).** Keep fleet's accumulated conventions (the equivalent of AGENTS.md) human-approved: research shows developer-written context helps (~+4%) while agent-written context hurts (~−3%, +20% cost). Never let a worker append to memory unreviewed; the supervisor approves every line.

### Explicitly do NOT copy

- **Unbounded loops without budgets.** A bare `while :; do` against a metered API is a money fire (Thoughtworks' "significant token cost" caveat; OMC author's $24K token bill). Fleet's round caps + backoff exist for a reason — any Ralph-style looping must keep them.
- **Agent-written memory.** Covered above — garbage tasks in, garbage commits out; garbage notes in, garbage context out.
- **Dashboard-for-dashboard's-sake (Conductor/Vibe Kanban surface).** Fleet is headless by design; a visual "who works on what" board adds maintenance without adding decisions. Log-queryable state (queue, attempts, worktree list) already answers the dashboard questions.
- **Single-vendor coupling.** Vendor-native stacks (Agent Teams, Codex `/goal`, Claude-only flows) are the deepest integrations and the heaviest lock-in; fleet's value is partly *cross-vendor* routing (a mixed fleet only pays off with an external check before merge). Stay harness-agnostic like ralphy, not harness-native like `/goal`.
- **Kanban lanes as workflow (Agent Kanban style).** Lanes + sentinels suit VS Code Copilot teams, not a queue-driven headless fleet — it would duplicate the bead state machine with a worse one.

**Covers:** htdocs.dev conductor-to-orchestrator guide (primary) + Ralph explainers (ralphloop.sh, futureagi, Wiegold, Osmani trends, Liu harness piece) + Augment Code 9-orchestrators roundup + awesome-agent-orchestrators list (ralphy/subtask/swarm-protocol/wit) + fleet repo sources (`src/fleet/core/retry_policy.py`, `src/fleet/orchestrator/worktree.py`, `src/fleet/orchestrator/reap.py`, `src/fleet/orchestrator/merge_validation.py`).
