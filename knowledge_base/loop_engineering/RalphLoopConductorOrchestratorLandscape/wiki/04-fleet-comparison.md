> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Fleet comparison: what to borrow, what not to copy

**In one sentence:** Fleet already owns the retry-table and worktree-merge slices of this landscape while missing completion-checks-as-code and fine-grained conflict guards, so it should borrow seven concrete mechanisms and explicitly refuse five others.

## Key points

- Fleet's retry/re-queue is a superset of the bare loop's persistence idea but rule-driven, not goal-driven: a data table (`retry_policy.py:decide()`) maps each attempt outcome to CLOSE/RELEASE/BLOCK with per-outcome round caps, and STATE.md/RESULT.json carry the "what next" memory the Ralph loop keeps in `tasks.json`/git log.
- Fleet knows what "failed" means (a table it applies) but has no per-task executable completion predicate of the Ralph kind — the worker declares done and the table believes it, so completion-checks-as-code is the single highest-value import.
- Workflow abstraction compared: Ralph has almost none (a task list file); Conductor's workflow is the review queue; Microsoft Conductor and Bernstein add real abstractions (YAML parallel groups; Goal → Planner → Task Graph → Janitor → merge pipeline); fleet has beads + queue + retry table, closest to Microsoft Conductor plus Bernstein's verify-before-merge.
- Borrow list: 7 concrete ideas (completion-check gates, Janitor reviewer, stale-iteration kill + reassign, YAML/static workflow option, work-claim heartbeats, function-level conflict warnings, AGENTS.md human-approved memory).
- Do NOT copy: unbounded loops without budgets, agent-written memory files, single-vendor lock-in, kanban-for-kanban's-sake dashboards, kanban lanes as workflow.
- Agent-written AGENTS.md files show ~−3% success and +20% cost (ETH Zurich, via Busso) while developer-written ones help ~+4%: memory files must stay human-approved and workers must never append unreviewed.
- Fleet's typed restarts (stall-kill ladder, lease expiry, context-pressure path, shutdown-exempt re-queue) already approximate the wild's workload watchdogs; the gap is goal verification, not loop machinery.

---

## 1. Retry vs loop: same shape, different mechanism

| Aspect | Ralph loop | Fleet |
|---|---|---|
| What repeats | The whole agent on the same prompt | The task via re-queue (RELEASE action) |
| Stop condition | Completion check: tests green / COMPLETE tag / all stories pass | Retry table verdict: CLOSE (done + close requested), BLOCK (round cap exhausted), RELEASE (try again) |
| Round counting | Iteration cap (flat number) | Trailing same-outcome streaks counted from `attempts.jsonl` — separate ladders per outcome (stall, failure, partial, no-close, context), caps in `core/limits.py` |
| Memory between passes | `tasks.json` + git log | `STATE.md` + `RESULT.json` (`summary`, `next_step`, `blocked_reason`) — the single next action is explicit, not inferred from a task list |
| Delays/backoff | None (hot loop) | `retry_after` timestamps + backoff ladders (e.g. failure waits 60/300/900s) so a not-ready task does not spin |
| Fault classification | None — every exit looks the same | Typed outcomes (SUCCESS/KILLED/FAILURE/PARTIAL...); infra faults (`supervisor_shutdown`) re-queue free without consuming a round |
| Verification | External check the loop author wires in | Merge validation for worktrees (clean + ahead-of-base check before merge) |

The honest summary: fleet has the *loop machinery* (arguably better — typed outcomes, backoff, free re-queue for infra faults) but not the *goal machinery*.

## 2. Workflow abstractions, ranked

"Workflow abstraction" = how the pattern *represents* multi-step work (if at all): Ralph loop a task list file (`tasks.json` / `prd.json`, no dependencies); Conductor (Melty) the review queue (no machine-readable plan); Microsoft Conductor YAML workflows (static/dynamic parallel groups, sub-workflows, conditional routing, deterministic scheduling with LLM only inside steps); Bernstein a typed pipeline (Goal → LLM Planner → Task Graph → Orchestrator → parallel Agents → Janitor → git merge → main); subtask "one parent, N file-owned children"; swarm-protocol a lease on a work item; wit locks defining the workflow. Fleet (beads + queue + retry table, STATE.md/RESULT.json continuation) sits closest to Microsoft Conductor plus Bernstein's verify-before-merge.

## 3. Seven borrows

1. **Completion checks as code (the Ralph gate).** Let each bead declare an executable done-predicate (tests, lint, typecheck, or a tag) that the reaper runs before honoring a close request. Today the worker *says* done; borrow Ralph's rule — a producer that grades its own homework is a pseudo-gate.
2. **A Janitor stage (from Bernstein).** A read-only reviewer (lint + test + security scan) between worker-finish and merge, ~1 reviewer per 3–4 builders. Fleet's merge validation checks *git hygiene* (clean, ahead); a Janitor would check *code correctness*.
3. **Stuck-iteration kill + reassign (Ralph safeguard).** Feed errors back for auto-retry, but after 3+ stuck iterations on the same bead, kill and reassign (different model/harness, or escalate to human) instead of burning another round on the same ladder.
4. **YAML/static workflow option (from Microsoft Conductor).** A declarative bead-graph for multi-step plans alongside the queue, deterministically scheduled.
5. **Heartbeat work-claims for long beads (from swarm-protocol).** Short heartbeats from running workers so the supervisor can distinguish "slow but alive" from "stalled" without waiting for the full stall timeout — fewer false stall-kills.
6. **Function-level conflict warnings (from wit).** Before merge, diff the bead's changed symbols against other in-flight beads' changed symbols; warn (or block) on overlap. Cheaper than full wit integration; catches the same-file-different-worktree collision that worktrees alone miss.
7. **Human-approved memory files (AGENTS.md discipline).** Keep fleet's accumulated conventions human-approved: developer-written context helps (~+4%) while agent-written context hurts (~−3%, +20% cost). Never let a worker append to memory unreviewed.

## 4. Five do-not-copies

- **Unbounded loops without budgets.** A bare `while :; do` against a metered API is a money fire (Thoughtworks' "significant token cost" caveat; OMC author's $24K token bill). Fleet's round caps + backoff exist for a reason — any Ralph-style looping must keep them.
- **Agent-written memory.** Garbage tasks in, garbage commits out; garbage notes in, garbage context out.
- **Dashboard-for-dashboard's-sake (Conductor/Vibe Kanban surface).** Fleet is headless by design; a visual "who works on what" board adds maintenance without adding decisions. Log-queryable state (queue, attempts, worktree list) already answers the dashboard questions.
- **Single-vendor coupling.** Vendor-native stacks (Agent Teams, Codex `/goal`, Claude-only flows) are the deepest integrations and the heaviest lock-in; fleet's value is partly *cross-vendor* routing. Stay harness-agnostic like ralphy, not harness-native like `/goal`.
- **Kanban lanes as workflow (Agent Kanban style).** Lanes + sentinels suit VS Code Copilot teams, not a queue-driven headless fleet — it would duplicate the bead state machine with a worse one.

**Covers:** fleet retry-table vs Ralph goal-check comparison, workflow abstraction ranking (Ralph / Conductor / Microsoft Conductor / Bernstein / subtask / swarm / wit / fleet), 7 borrowable ideas, 5 explicit do-not-copies, typed-restart coverage; sources: htdocs.dev primary plus fleet repo sources (`src/fleet/core/retry_policy.py`, `src/fleet/orchestrator/worktree.py`, `reap.py`, `merge_validation.py`).
