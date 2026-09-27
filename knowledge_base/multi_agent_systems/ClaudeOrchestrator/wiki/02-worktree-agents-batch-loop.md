> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worktree Agents and the Batch Loop

**In one sentence:** Work flows in synchronous batches — recon, decompose, parallel dispatch into isolated worktrees, accept, merge, cross-model review — where the orchestrator alone owns merge, push, and cleanup.

## Key points

- The loop is deliberately synchronous: agents "run and return results within the current session — no fire-and-forget, no heartbeat polling" (`SKILL.md:54`), because synchronous dispatch "is what makes review→merge gates enforceable" (`SKILL.md:56`).
- Each agent gets one isolated worktree plus one `build/<slug>` branch, dispatched via concurrent `Agent(isolation:"worktree")` calls in a single message (`SKILL.md:70-79`).
- The orchestrator alone owns merge (`--no-ff` on main), push to `origin/main`, worktree removal, and post-merge integration testing (`SKILL.md:264-309`).
- Same-module tasks are serialized, never parallelized — measured conflicts fell 43% → 0% — and three-agent parallelism requires four preconditions (`SKILL.md:472-496`).
- The worktree base trap (ORC-14): new worktrees must be created from `origin/main` after pushing serial merges, never from a stale local main (`SKILL.md:72-79,314`).
- A Batch Status Report (Delivered / Completed / Rejected / Blocked / Repo State / Next) closes every loop and doubles as the context-rebuild checkpoint after compaction (`SKILL.md:729-757`).
- Durable state is plain markdown — `PROGRESS.md`, `inbox.md`, concepts/glossary, Batch Status Reports — coordination state that survives compaction but is explicitly not proof (`SKILL.md:780-784`).

---

## The six steps

(`SKILL.md:58-68`; `full-guide.md:31`)

1. **Recon** — `git status --short --branch; git log --oneline -10; git worktree list` plus doc reads (PROGRESS, roadmap, concepts, inbox, shared contracts) (`SKILL.md:89-103`).
2. **Decompose** — roadmap or feature → candidates with contracts; shared contracts and migrations serialized first; same-module work serialized (`SKILL.md:101,113-118,472-487`).
3. **Dispatch** — parallel `Agent` calls, one worktree and branch each, base `origin/main`; dispatch skeleton at `SKILL.md:204-215`.
4. **Accept** — per-branch review: phantom-commit check, diff boundary check, gate re-run, evidence honesty, claim verification (see [[03-evidence-discipline-acceptance-rules|Evidence Discipline]]) (`SKILL.md:227-258`).
5. **Merge / cleanup / post-merge test** — `--no-ff` merge on main, push, worktree and branch removal, cleanup verification, mandatory post-merge integration test because per-branch gates do not prove the layers work together (`SKILL.md:264-309`).
6. **Review gate + report** — cross-model review launched before next dispatch; findings triaged P1/P2/P3; Batch Status Report written (see [[05-cross-model-review-fleet-lessons|Cross-Model Review]]) (`SKILL.md:315-325,641-670,729-757`).

Two modes sit on top: single-feature (default) and roadmap-driven looping (`SKILL.md:24-40`).

## Concurrency policy

- **Default:** 1 agent per module; serialize A → merge → push → B when tasks share navigation, resource, or config (`SKILL.md:472`).
- **2 agents:** only across different modules or projects (backend + frontend).
- **3 agents:** only when all four hold — no shared contract/migration/API, no hardware/payment, clean main, disjoint modules and write sets (`SKILL.md:474-480`).
- **Rationale with numbers:** same-module parallelism "almost never saves time" — 10–15 min conflict resolution per batch exceeds wall-clock gain (`SKILL.md:489`); shared-file only-append auto-merge succeeds only ~57% (`SKILL.md:491`).
- **Forced same-module parallelism** requires only-append discipline, scoped naming (`OdPaymentStatus` vs `PaymentStatus`), and a 10–15 min/batch budget (`SKILL.md:493-496`).
- **Lane guard:** "Available slots ≠ dispatch permission" (`SKILL.md:498`).

## Restart and rescue without a ledger

The Claude adapter has no ledger, heartbeat, or stale-task rescue by design — those live in the async codex sibling's Go helper (adapter `README.md:97`). Instead:

- **Package ledger (lightweight):** milestone outcome, active contracts, merge order, gates, blocked evidence — prevents losing package shape across batches, especially after compaction (`SKILL.md:122`).
- **Phantom-commit handling:** check `git -C <worktree> status --short --branch` + `log --oneline -3`; if uncommitted, the orchestrator commits on the agent's behalf before review (`SKILL.md:227-238`). Commit rate went 40% → 100% after the rule (adapter `README.md:85`).
- **Dispatch failure:** stay in the orchestration layer — report the blocker, fix the dispatch, or ask the user; never implement the task yourself (ORC-07, `SKILL.md:221`).
- **Rejected branch:** leave branch/worktree in place; fix via `SendMessage` to the same agent or a new agent carrying the rejection findings (`SKILL.md:286`).
- **Content-filter refusal:** record slug + prompt, retry next batch rephrased; on second failure mark `blocked`, never halt the whole run (`SKILL.md:569-575`).

**Covers:** claude-orchestrator `SKILL.md:24-122,204-238,264-325,472-498,569-575,729-784`, `docs/full-guide.md:31`, `README.md:78-97`.
