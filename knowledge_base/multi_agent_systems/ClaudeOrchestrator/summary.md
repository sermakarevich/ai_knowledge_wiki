# Technical Analysis: claude-orchestrator + orchestration-playbook

**Repository:** https://github.com/indiekitai/claude-orchestrator (+ supplement https://github.com/indiekitai/orchestration-playbook)
**Version analyzed:** claude-orchestrator @ `7a81c78` (2026-07-27); playbook @ `76d6857` (2026-07-03)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Once coding agents can generate work continuously, the bottleneck shifts from writing code to managing what agents generate: false reporting (says "done" without committing), boundary violations (touches files it shouldn't, works from a stale base), and fake completion (shallow slices dressed as features, local tests passed off as production proof) — playbook `README.md:13-15`. The playbook repo is the harness-agnostic statement of the discipline; the claude-orchestrator repo is its Claude Code adapter, delivered as a skill (`SKILL.md`, 796 lines) invoked via `/build-orchestrator`.

The primary user is a human developer running a long multi-agent build through Claude Code (or Codex/Kimi via sibling adapters), plus the orchestrating agent itself, which reads `SKILL.md` as its operating procedure. The system makes no LLM calls of its own — it is process discipline plus git mechanics, enforced by prompt text and review gates.

---

## 2. High-Level Architecture

```
                    ┌─────────────────────────────┐
                    │  orchestration-playbook     │
                    │  (harness-agnostic core)    │
                    │  loop / evidence / contract │
                    │  iron rules / ORC-01..18    │
                    └──────────────┬──────────────┘
                                   │ shared discipline
            ┌──────────────────────┼──────────────────────┐
            ▼                      ▼                      ▼
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │ claude-orch.   │    │ codex-orch.    │    │ kimi-orch.     │
   │ sync batches,  │    │ async sessions │    │ (not analyzed) │
   │ Agent+worktree │    │ Go CLI: ledger │    │                │
   │ cross-model    │    │ heartbeat,     │    │                │
   │ review via     │    │ routines,      │    │                │
   │ codex-companion│    │ policy/eval    │    │                │
   └────────────────┘    └────────────────┘    └────────────────┘
```

Data flow from feature request to merged code:

1. **Recon** — orchestrator reads `git status/log/worktree list`, PROGRESS/roadmap, concepts/glossary, inbox, shared contracts (`SKILL.md:89-103`).
2. **Decompose + contract** — tasks get bounded ten-field dispatch contracts with allowed/forbidden paths, gates, evidence labels (`SKILL.md:350-464`).
3. **Dispatch** — one isolated worktree + one `build/<slug>` branch per agent; `Agent(isolation:"worktree")` calls in one message run concurrently (`SKILL.md:70-79`).
4. **Accept** — per-branch review: phantom-commit check, diff boundary check, gate re-run, evidence honesty, claim verification (`SKILL.md:227-258`).
5. **Merge + cleanup** — orchestrator merges `--no-ff` on main, pushes to origin, removes worktrees, verifies clean state (`SKILL.md:264-300,314`).
6. **Cross-model review + next batch** — different-family reviewer inspects merged diff; findings feed P1/P2 tracking; Batch Status Report closes the loop (`SKILL.md:321-346,641-670,729-757`).

Persistent state is plain markdown in the target repo (`PROGRESS.md`, `inbox.md`, `concepts.md`/`GLOSSARY.md`, Batch Status Reports) — local/static coordination state, explicitly not proof (`SKILL.md:780-784`). The async codex sibling adds a persistent ledger via its Go helper (adapter `README.md:97`).

---

## 3. The Dispatch Contract

The central domain object is the task contract: ten required fields, "no contract, no dispatch" (playbook `README.md:40-53`) — outcome definition; anti-shallow-slice classification (`vertical-completion | runtime-proof | blocked-removal | owner-gated`); minimum-change rationale; boundaries (allowed/forbidden paths, branch, base commit); acceptance gates as concrete commands ("not green = not done"); labeled evidence requirements; duty to challenge unclear contracts; restart policy; subjective rubric for taste/UI/parity work; handoff format (branch, hashes, file list, actual gate output, residual risks).

The adapter expands this into a twelve-section prompt template (`SKILL.md:350-464`) adding: a MUST-COMMIT rule (`SKILL.md:390-393`), Common P1 Patterns (five checks claimed to cover ~40% of P1s, `SKILL.md:418-425`), the Minimalism Ladder (delete → stdlib → dependency → inline → keep-minimum, `SKILL.md:427-436`), shared-resource append-only rules (`SKILL.md:438-443`), and a ≤~30-line handoff cap (`SKILL.md:453-463`). The contract also carries the restart policy (repeated same-gate failure → clean restart, `SKILL.md:414-416`) and the challenge duty (`SKILL.md:385-389`).

---

## 4. LLM / External Service Integration

These repos do NOT call any LLM or external API — there is no code, no SDK call, no model invocation. They are prompt-text discipline consumed by a host harness: the intended callers are Claude Code (`Agent` tool with `isolation:"worktree"`), Codex App sessions, and Kimi Code, plus one concrete script invocation — cross-model review via `node "$PLUGIN_ROOT/scripts/codex-companion.mjs" review --wait --base <pre-merge-commit>` with `PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/openai-codex/plugins/codex"` (`SKILL.md:651-657`). Standalone `codex review` is explicitly forbidden (parameter conflicts, no `--wait`, large-diff timeouts). Cost-per-call is therefore whatever the host harness charges; the repos' cost lever is organizational instead: model-tier-by-consequence (tier by cost of a wrong answer, not task size; reviewer lanes must differ in family, not tier, `SKILL.md:170-198`).

---

## 5. The Batch Loop

The user-facing workflow is the synchronous batch cycle (`SKILL.md:58-68`; `full-guide.md:31`):

1. **Step 1 Recon** — `git status --short --branch; git log --oneline -10; git worktree list` plus doc reads (`SKILL.md:89-93`).
2. **Step 2 Decompose** — roadmap or feature → candidates with contracts; shared contracts/migrations serialized first; same-module work serialized (`SKILL.md:101,113-118,472-487`).
3. **Step 3 Dispatch** — parallel `Agent` calls, one worktree/branch each, base `origin/main` (`SKILL.md:204-215` skeleton; `SKILL.md:72-79` base trap).
4. **Step 4 Accept** — commit check → diff inspection → checklist (boundaries, self-review, gates, evidence honesty, claim verification, idempotency, authorization separation, live-proof gate) (`SKILL.md:227-258`).
5. **Step 5 Merge/cleanup/post-merge test** — `--no-ff` merge on main, push, worktree/branch removal, cleanup verification, mandatory post-merge integration test (`SKILL.md:264-309`).
6. **Step 6 Review gate + report** — cross-model review launched before next dispatch; findings triaged P1/P2/P3; Batch Status Report written (`SKILL.md:315-325,641-670,729-757`).

Concurrency policy is numeric: default 1 agent per module; 2 only across modules/projects; 3 only with four preconditions (no shared contract/migration/API, no hardware/payment, clean main, disjoint writes) (`SKILL.md:472-480`). Two modes sit on top: single-feature (default) and roadmap-driven looping (`SKILL.md:24-40`).

---

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| claude-orchestrator `SKILL.md:1-796` | 796 | Entire adapter: loop, contracts, gates, review, ORC table, routines-in-prose |
| claude-orchestrator `SKILL.md:350-464` | ~115 | Dispatch Prompt Template (the 12-section contract) |
| claude-orchestrator `SKILL.md:508-524` | ~17 | Evidence discipline table + no-upgrade rules |
| claude-orchestrator `SKILL.md:641-670` | ~30 | Cross-model review method, companion-script invocation, ping-pong guard |
| claude-orchestrator `SKILL.md:700-721` | ~22 | ORC-01–18 anti-pattern table with Claude-specific glosses |
| claude-orchestrator `docs/full-guide.md:1-111` | 111 | Execution model, worked example (4 agents/1400+ lines), lessons table |
| claude-orchestrator `README.md:1-105` | 105 | Install (symlink skill), results table, sibling pointer |
| playbook `README.md:1-106` | 106 | Harness-agnostic core: loop, evidence, contract, iron rules, ORC table |
| playbook `CASE-STUDY.md:1-46` | 46 | 18,782-line split case file: method, landmine, fix, acceptance rigor |

---

## 7. CLI / Usage Surface

- **Entry points** — symlink skill into `~/.claude/skills/build-orchestrator`, invoke `/build-orchestrator <feature>` or `--roadmap docs/roadmap.md` (adapter `README.md:25,37`; `SKILL.md:24-40`). No binary, no package manifest.
- **Commands** — all operations are git + one node script:
```
git status --short --branch; git log --oneline -10; git worktree list   # recon
git -C <worktree> status --short --branch; git log --oneline -3         # phantom-commit check
git -C <worktree> diff --name-status main..HEAD; git diff --check       # boundary check
git checkout main; git merge --no-ff <branch>; git worktree remove ...  # merge/cleanup
node "$PLUGIN_ROOT/scripts/codex-companion.mjs" review --wait --base <pre-merge-commit>  # review
```
- **Environment variables** — `PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/openai-codex/plugins/codex"` (`SKILL.md:654`).
- **Configuration files** — target-repo docs the loop reads/writes: `docs/roadmap.md`, `PROGRESS.md`, `inbox.md`, `concepts.md`/`GLOSSARY.md`, Batch Status Reports (`SKILL.md:89-103,729-784`).

---

## 8. Extensibility Points

- **New harness adapter** — copy the playbook core (loop, evidence, contract, iron rules, ORC IDs) into the harness's system-prompt/skill format per the four-step adoption ladder (playbook `README.md:96-102`); add harness-specific execution bindings (sync vs async, worktree mechanics, review tooling) the way `SKILL.md:54-79` binds Claude Code.
- **New ORC anti-pattern** — append a row to the ORC table (`SKILL.md:700-721` / playbook `README.md:68-91`); IDs are shared across adapters, so coordinate numbering; the prune rule requires evidence the pattern caught a real bug (`SKILL.md:20`).
- **Project-specific evidence rules** — override the default direct/proxy thresholds per project; the adapter explicitly yields precedence to them (`SKILL.md:524`).
- **New gate or check** — add to the acceptance checklist (`SKILL.md:247-258`) and, for mechanical checks, to the contract Gates section (`SKILL.md:372-375`); high-risk domains also need a Design-First entry (`SKILL.md:143-168`).
- **Reviewer backend** — replace the codex-companion invocation (`SKILL.md:649-657`) with another different-family reviewer; the case study shows reviewer vantage (plan-text vs repo-access) matters more than reviewer brand (`CASE-STUDY.md:31-33`).

---

## 9. Limitations and Gotchas

- **Scale numbers lack provenance.** 53 batches / ~95 agents / ~70k lines, 43%→0% conflicts, ~57% only-append auto-merge, ~40% of P1s from five patterns, 15×P1+37×P2 yield ship without datasets, windows, or false-positive rates (`SKILL.md:425,491,670`; adapter `README.md:80-87`; playbook `README.md:5,23,64`). The README itself warns counts measure activity, not capability (adapter `README.md:89`).
- **No async machinery in the Claude adapter.** Teams expecting ledger/heartbeat/stale-rescue must look at the codex sibling's Go helper (adapter `README.md:97`); the Claude skill's durability story is markdown files that survive compaction (`SKILL.md:780-784`).
- **Push-to-origin assumed.** The worktree-base discipline requires pushing to `origin/main` after serial merges (`SKILL.md:314`); forks, protected branches, or offline work break the flow silently.
- **Severity levels undefined.** P1/P2/P3 handling is specified (fix now / record / note) but severity itself is never defined (`SKILL.md:664-666`), so triage consistency depends on unwritten judgment.
- **Sync/async ambiguity.** The skill forbids fire-and-forget (`SKILL.md:54`) yet tolerates background review processes (`SKILL.md:315,324`) — the boundary between forbidden and tolerated async is one sentence wide.
- **Review-order fork.** Default merge→push→review vs pre-merge review for high-risk paths (`SKILL.md:327-341`) creates two pipelines; misclassifying a task's risk picks the wrong one.
- **Magic thresholds.** 2-skip stop, P2→P1 after 3 batches, ≤5-line hotfix, max 2–3 parallel, 600s review timeout are heuristics without derivation (`SKILL.md:325,346,610,777`; `full-guide.md:88`).
- **P1 hotfix exception cuts against the grain.** The orchestrator may directly edit ≤5 lines in one file (`SKILL.md:777`) — a deliberate ORC-07-adjacent carve-out that relies on labeling discipline alone.

---

## 10. How It Compares to Alternatives

- **codex-orchestrator (sibling).** Same philosophy, async session model with a Go CLI for persistent ledger, heartbeat, routines, policy/eval (adapter `README.md:97`). Tradeoff vs the Claude adapter: durable runtime machinery at the cost of a binary to build, install, and trust.
- **kimi-orchestrator (sibling).** Third adapter for Kimi Code, linked from the playbook core (playbook `README.md:7`). Not analyzed here; its existence is the evidence the core actually ports across harnesses.
- **Fleet (this team's supervisor/worktree orchestrator).** Fleet already owns the async side — centralized bead DB, supervisor heartbeats, isolated worktrees — but lacks the sync side this skill contributes: bounded dispatch contracts, evidence labeling, merge-gate checklists, and ORC-style rejection vocabulary. Complementary, not competitive.
- **Claude Squad / GasTown-style session managers.** Harness-level multiplexers (tmux worktrees, session fan-out) solve agent *placement*; this discipline solves agent *governance* (what counts as done, what evidence is required, when to stop). One can run this skill's loop on top of those multiplexers.

Positioning: the only surveyed system whose unit of reuse is prose discipline (contract + evidence + iron rules + numbered anti-patterns) rather than runtime code — portable everywhere, enforceable only where a reviewer (human or cross-model) actually checks.

---

## Appendix: Selected Code Snippets

**Dispatch skeleton (SKILL.md:204-215)**

```text
Agent(isolation:"worktree", task: <contract ...>)
# multiple Agent calls in one message run concurrently (SKILL.md:70)
```

**Companion review invocation (SKILL.md:654-657)**

```bash
PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/openai-codex/plugins/codex"
node "$PLUGIN_ROOT/scripts/codex-companion.mjs" review --wait --base <pre-merge-commit>
```

**House rules (playbook README.md:15; README.md:38)**

```text
Every rule below is backed by a real incident. A rule that never caught a real bug doesn't belong here.
Upgrading an evidence label is lying.
```

**Lane guard (SKILL.md:498)**

```text
Available slots ≠ dispatch permission
```
