# Technical Analysis: bernstein

**Repository:** https://github.com/sipyourdrink-ltd/bernstein
**Version analyzed:** 3.19.1
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Bernstein is an AI agent orchestrator: it runs many CLI (Command-Line Interface, a text tool) coding agents in parallel against one codebase without letting them overwrite each other's work. The primary user is the operator who launches a run (a plan with tasks) and is responsible for merging the result.

The core problem it solves is coordination without model judgment. Scheduling, task assignment, lifecycle, and retry decisions are deterministic plain Python, not model (LLM, Large Language Model, the AI text model) calls (`src/bernstein/core/orchestration/orchestrator.py:1`, `docs/scope.md:16`). Agents themselves are model-driven, but the loop that decides what runs next, who gets it, and whether it is retried never consults a model (`src/bernstein/core/orchestration/orchestrator.py:1470`).

Reproducibility is the second problem. Every planning-time model response is recorded to `llm_calls.jsonl` and replayed strictly, every run event goes into a Merkle-chained journal (Merkle chain = each record hashes the previous record, so tampering breaks the chain), and every artifact write goes into a hash-chained lineage spine (`src/bernstein/core/orchestration/deterministic.py:1`, `src/bernstein/core/replay/journal.py:71`, `src/bernstein/core/lineage/spine.py:9`). A past run can therefore be re-executed and audited byte-identically.

## 2. High-Level Architecture

```
  plan / workflow / recipe
        │
        ▼
  deterministic tick loop (single-threaded) ──► task DAG walk (topological, sorted by id)
        │                                              │
        ▼                                              ▼
  claim (CAS-guarded) ──► spawn via adapter registry ──► per-task worktree (agent/<session>)
        │                                                      │
        ▼                                                      ▼
  janitor + quality gates (lint/type/test) ──► serial FIFO merge queue ──► main
        │
        ▼
  lineage spine + replay journal + HMAC audit chain (.sdd/)
```

Data-flow narrative:

1. A plan, workflow manifest, or recipe renders into a task graph with dependencies and role assignments (`src/bernstein/core/workflows/workflow_spec.py:141`, `src/bernstein/core/workflows/recipe_spec.py:335`).
2. The single-threaded tick loop (`while self._running` in `run`) fetches tasks, walks the DAG (DAG = Directed Acyclic Graph, tasks plus dependencies with no cycles) in topological order, and matches ready tasks to agents (`src/bernstein/core/orchestration/orchestrator.py:6`, `src/bernstein/core/orchestration/orchestrator.py:1470`, `src/bernstein/core/orchestration/task_dag.py:225`).
3. Claims are atomic and version-checked (CAS = Compare-And-Swap, claim succeeds only if the task version is unchanged), then the adapter registry spawns the right coding-agent CLI in its own git worktree on branch `agent/<session_id>` (`src/bernstein/core/tasks/task_store_core.py:2161`, `src/bernstein/adapters/registry.py:86`, `src/bernstein/core/git/worktree.py:40`).
4. Completion passes through the janitor (automatic quality checker) and quality gates (lint on by default; type-check and tests opt-in) before any merge (`src/bernstein/core/tasks/task_lifecycle.py:5173`, `src/bernstein/core/quality/quality_gates.py:201`).
5. Merges are serialized one at a time through a FIFO (First In First Out) queue with conflict pre-flight; failures retry on a bounded budget or land in the dead-letter queue (`src/bernstein/core/git/merge_queue.py:200`, `src/bernstein/core/tasks/dead_letter_queue.py:180`).
6. Every step appends to the lineage spine, the replay journal, and (opt-in) the HMAC (Hash-based Message Authentication Code, a keyed checksum) audit chain, all as plain text under `.sdd/` with no database (`src/bernstein/core/lineage/spine.py:9`, `src/bernstein/core/replay/journal.py:71`, `docs/scope.md:33`).

Persistent state location: all under `.sdd/` — `runs/<run_id>/journal.jsonl`, `runs/<run_id>/llm_calls.jsonl`, `lineage/<run_id>/spine.jsonl`, `runtime/controllers.json`, `runtime/dlq.jsonl`, `archive/tasks.jsonl` (`src/bernstein/core/replay/journal.py:71`, `src/bernstein/core/orchestration/deterministic.py:4`, `src/bernstein/core/lineage/spine.py:101`, `src/bernstein/core/orchestration/controller_state.py:3`, `src/bernstein/core/tasks/dead_letter_queue.py:144`, `src/bernstein/core/orchestration/adaptive_timeout.py:49`).

## 3. The Deterministic Task Graph

The task graph is the central data structure. A node carries a stable id, description, planner-declared `parallel_safe` flag (never inferred), optional story id, and `depends_on` tuple (`src/bernstein/core/orchestration/task_dag.py:69`). DAGs load from Markdown checkbox lists or YAML (YAML = human-readable config format) under a `tasks:` key (`src/bernstein/core/orchestration/task_dag.py:111`).

Ordering is computed by `topological_iter_with_parallel`, which yields one frozen set per batch of ready tasks (`src/bernstein/core/orchestration/task_dag.py:200`). Ready tasks are sorted by id for stable output; if every ready task is `parallel_safe` they run together, otherwise each serial task yields alone (`src/bernstein/core/orchestration/task_dag.py:225`). A dependency cycle raises `TaskDagCycleError` naming the stuck tasks (`src/bernstein/core/orchestration/task_dag.py:61`).

Task states are a fixed 17-value enum (`TaskStatus` in `src/bernstein/core/tasks/models.py:187`): normal path `open → claimed → in_progress → done → closed`, plus failure/waiting states (`failed`, `orphaned`, `blocked`, `cancelled`, `abandoned`, `refused`, `suspended`, `pending_approval`, and others). All transitions pass through one allow-table (`TASK_TRANSITIONS` in `src/bernstein/core/tasks/lifecycle.py:150`), so illegal jumps raise instead of silently proceeding.

Governed phases constrain which roles may act: the built-in sequence is plan, implement, verify, review, merge, with per-phase `allowed_roles` (e.g. verify allows only qa and security); an empty set means all roles pass (`src/bernstein/core/planning/workflow.py:120`, `src/bernstein/core/planning/workflow.py:265`). A phase counts complete when every role-matching task is terminal (`src/bernstein/core/planning/workflow.py:286`).

## 4. LLM / External Service Integration

Models are used for work, never for coordination. Planning and decomposition calls are recorded as prompt-plus-model to `.sdd/runs/{run_id}/llm_calls.jsonl`, and replay serves cached responses in per-key FIFO order instead of calling the model (`src/bernstein/core/orchestration/deterministic.py:1`, `src/bernstein/core/orchestration/deterministic.py:173`). The lookup key folds in prompt, model, provider, temperature, and max tokens so parameter drift cannot masquerade as a cache hit (`src/bernstein/core/orchestration/deterministic.py:27`).

Replay is strict by default: a cache miss (including over-requesting a recorded key) raises `ReplayMissError` and aborts instead of calling the live model (`src/bernstein/core/orchestration/deterministic.py:21`, `src/bernstein/core/orchestration/deterministic.py:191`). Opt-out is the `BERNSTEIN_REPLAY_ALLOW_LIVE_MISS` flag, which downgrades misses to warn-plus-live (`src/bernstein/core/orchestration/deterministic.py:53`). One store is active per orchestrator subprocess (`src/bernstein/core/orchestration/deterministic.py:407`).

Two model-adjacent subsystems also exist. Intent verification asks a model whether a diff matches its task and blocks on "no" by default (`src/bernstein/core/quality/quality_gates.py:480`, `src/bernstein/core/quality/quality_gates.py:88`). Cost-aware routing picks model plus effort with LinUCB (Linear Upper Confidence Bound, a math method balancing trying new options vs reusing good ones) plus UCB1 (a simpler confidence-bound method) for effort, reward `quality * (1 - normalized_cost)`, state under `.sdd/routing/` (`src/bernstein/core/routing/bandit_router.py:1129`, `src/bernstein/core/routing/bandit_router.py:1647`, `src/bernstein/core/routing/bandit_router.py:26`). No external SaaS (Software as a Service) dependency is required on the coordination path; providers are reached only through spawned agent CLIs.

## 5. The Plan-to-Merge Run Pipeline

The main pipeline runs plan → claim → execute → verify → merge → seal. The `run()` loop sets `_running = True`, records `run_started`, then ticks `while self._running or self._has_active_agents()`, aborting after N consecutive tick failures (`src/bernstein/core/orchestration/orchestrator.py:3151`, `src/bernstein/core/orchestration/orchestrator.py:3313`). Idle ticks back off (double sleep up to 8x, capped at 30 s); each tick binds the executed graph digest into the journal only when changed (`src/bernstein/core/orchestration/orchestrator.py:3334`, `src/bernstein/core/orchestration/orchestrator.py:1482`).

Claim and execution: file-backlog claims hold a thread lock plus an OS (Operating System) file lock across reload-mark-save (`src/bernstein/core/tasks/claim.py:64`); server-store claims add a CAS version check plus role and dependency checks, mapping double-claim to HTTP (Hypertext Transfer Protocol) 409 Conflict (`src/bernstein/core/tasks/task_store_core.py:2125`, `src/bernstein/core/tasks/task_store_core.py:2169`). Each session gets a worktree under `.sdd/worktrees/<session_id>` on branch `agent/<session_id>` (`src/bernstein/core/git/worktree.py:40`, `src/bernstein/core/git/merge_queue.py:47`). Artifact-mode sessions (reports, datasets, not code) get a plain directory under `.sdd/workspaces/` with no branch and nothing to merge (`src/bernstein/core/agents/spawner_worktree.py:33`, `src/bernstein/core/tasks/artifact_completion.py:168`).

Retry and recovery: failed tasks retry with more effort first, stronger model later (haiku → sonnet → opus ladder), capped at the minimum of per-task limit, reason-based limit, and a hard cap of 2 regular retries (`src/bernstein/core/tasks/task_lifecycle.py:446`, `src/bernstein/core/tasks/task_lifecycle.py:379`, `src/bernstein/core/tasks/task_lifecycle.py:120`). Warm resume of an old session requires a verified checkpoint plus matching workspace hash, else cold restart (`src/bernstein/core/tasks/checkpoint_retry.py:478`). Janitor failures reopen under the same id up to 2 cycles (`BERNSTEIN_JANITOR_REOPEN_MAX`), then permanent failure (`src/bernstein/core/tasks/task_lifecycle.py:5133`, `src/bernstein/core/tasks/task_lifecycle.py:5173`). Exhausted tasks go to the DLQ (Dead Letter Queue, a permanent failure list) at `.sdd/runtime/dlq.jsonl` for operator replay (`src/bernstein/core/tasks/dead_letter_queue.py:180`). Restart resets CLAIMED/IN_PROGRESS to OPEN with an immediate disk write (`src/bernstein/core/tasks/task_store_core.py:758`).

Merge and seal: gates run on the live worktree before merge (ruff lint on; pyright and tests opt-in per `bernstein.yaml`) and a blocking failure refuses the merge (`src/bernstein/core/agents/spawner_merge.py:414`, `src/bernstein/core/quality/quality_gates.py:201`). Merges serialize through the FIFO `MergeQueue.submit` context manager; conflicts are pre-checked with `git merge-tree` and aborted with `git merge --abort` on conflict (`src/bernstein/core/git/merge_queue.py:277`, `src/bernstein/core/git/merge_queue.py:139`, `src/bernstein/core/git/git_pr.py:443`). At finalization the journal head is sealed into the lineage spine under prefix `replay-journal-head:` (`src/bernstein/core/replay/journal.py:1273`, `src/bernstein/core/lineage/spine.py:90`).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `src/bernstein/core/orchestration/orchestrator.py` | 1–100, 1470, 3151–3368, 6714 | Single-threaded tick loop, run loop, seed pinning, merge-queue holder |
| `src/bernstein/core/orchestration/task_dag.py` | 61–225 | Task node type, cycle error, topological walk with parallel batches |
| `src/bernstein/core/orchestration/deterministic.py` | 1–426 | LLM call recording, per-key FIFO replay, strict-miss abort |
| `src/bernstein/core/replay/journal.py` | 11–741, 1265–1282 | Merkle-chained per-run event log, verification, journal-head seal |
| `src/bernstein/core/tasks/task_lifecycle.py` | 120–915, 446–565, 5133–5267 | Retry budgets, model/effort escalation, janitor verdicts, DLQ write |
| `src/bernstein/core/tasks/task_store_core.py` | 758–811, 2066–2696, 3546–3585 | CAS claims, restart recovery, release, heartbeat/crash detection |
| `src/bernstein/core/tasks/models.py` | 187–199 | 17-state `TaskStatus` enum incl. suspended/pending-approval |
| `src/bernstein/core/tasks/checkpoint_retry.py` | 77–543 | Warm/fork/cold retry decision, workspace-hash gate |
| `src/bernstein/core/tasks/dead_letter_queue.py` | 37–327 | Permanent failure list, list/read/count/replay operators |
| `src/bernstein/adapters/registry.py` | 86–384, 517 | Name-to-class adapter table, lookup, entry-point discovery |
| `src/bernstein/adapters/base.py` | 528–1259 | `CLIAdapter` contract: `spawn`, `name`, parsers, resume, strategy |
| `src/bernstein/core/git/merge_queue.py` | 47–277 | Branch naming, conflict pre-flight, FIFO serialized merges |
| `src/bernstein/core/quality/quality_gates.py` | 1–1202 | Gate defaults, lint/type/test/PII/DLP/mutation/intent checks |
| `src/bernstein/core/lineage/spine.py` | 9–705 | Always-on hash-chained artifact spine, four-way verify verdicts |
| `src/bernstein/core/lineage/signed_write.py` | 12–306 | Ed25519 (digital-signature algorithm) sealing over canonical bytes |
| `src/bernstein/core/workflows/recipe_registry.py` | 288–1111 | Recipe identity by SHA-256 (256-bit fingerprint hash), supersede/rollback/pause |
| `src/bernstein/core/routing/bandit_router.py` | 1129–1647 | LinUCB/UCB1 cost-aware model-plus-effort routing |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `cryptography` | (per manifest; confirm in pyproject.toml) | Ed25519 signatures, HMAC chains, offline verification wheel |
| `click` | (per manifest; confirm in pyproject.toml) | CLI (command-line interface) parsing; only non-stdlib import of `verify_cli` besides `cryptography` (`verify_cli/README.md:28`) |
| `fastapi` | (per manifest; confirm in pyproject.toml) | HTTP server for task-store routes incl. claim receipts (claim path surfaces as 409 via HTTP layer, `src/bernstein/core/tasks/task_store_core.py:2169`) |
| `uvicorn` | (per manifest; confirm in pyproject.toml) | ASGI (Async Server Gateway Interface) server runner for the FastAPI app |
| `httpx` | (per manifest; confirm in pyproject.toml) | HTTP client used by orchestrator verdict/merge posts (e.g. reopen post, `src/bernstein/core/tasks/task_lifecycle.py:5173` region) |
| `pyyaml` | (per manifest; confirm in pyproject.toml) | YAML manifests, DSL phases/nodes, `bernstein.yaml` policy loading |
| `rich` | (per manifest; confirm in pyproject.toml) | Terminal output formatting |
| `textual` | (per manifest; confirm in pyproject.toml) | Terminal UI (user interface) screens |
| `openai` | (per manifest; confirm in pyproject.toml) | Model provider client for planning/intent-verification calls |
| `pydantic-settings` | (per manifest; confirm in pyproject.toml) | Typed settings/config management |
| `ruff` | invoked as `ruff check .`, not necessarily a Python import (`src/bernstein/core/quality/quality_gates.py:201`) | Default lint gate command |
| `pyright` | invoked as `pyright`, opt-in (`src/bernstein/core/quality/quality_gates.py:204`) | Opt-in type-check gate command |

Note: only `cryptography` and `click` are directly attested in the wiki pages (`verify_cli/README.md:28`); the remainder are the manifest set named in the analysis brief and marked accordingly.

## 8. CLI / Usage Surface

Entry points: `bernstein run --seed 42` (record), `bernstein replay <run_id>` (strict replay), `bernstein replay <run_id> --verify` / `--from-step N` (per docs; not verified in source), `bernstein run --cli myagent` (adapter select, `pyproject.toml:351` comment), `bernstein audit verify` (bundle check, `src/bernstein/core/evidence/bundle.py:988`), `bernstein-verify pack <zip>` plus `chain`/`forks` subcommands in the standalone wheel (`verify_cli/README.md:24`, `verify_cli/README.md:37`).

Workflow commands distinguish manifest vs DSL (DSL = Domain-Specific Language, small config language) by structure: top-level `phases` means DSL, list-form `nodes` without `phases` means manifest (`src/bernstein/cli/commands/workflow_cmd.py:51`).

Environment variables: `BERNSTEIN_DETERMINISTIC_SEED` (pins `random`, `src/bernstein/core/orchestration/orchestrator.py:6714`), `BERNSTEIN_REPLAY_ALLOW_LIVE_MISS` (downgrades replay misses to live, `src/bernstein/core/orchestration/deterministic.py:53`), `BERNSTEIN_JANITOR_REOPEN_MAX` (janitor reopen budget, default 2, `src/bernstein/core/tasks/task_lifecycle.py:5133`), `BERNSTEIN_AUDIT=1` (opts into HMAC audit chain, `src/bernstein/core/orchestration/orchestrator.py:1061`), `BERNSTEIN_AUDIT_KEY_PATH` (key override, `src/bernstein/core/security/audit.py:68`), `BERNSTEIN_RECORD` (older gateway recording path, `src/bernstein/core/replay/gateway.py:1`), `BERNSTEIN_REPLAY_RETENTION` (prunes past runs only, `src/bernstein/core/replay/journal.py:741`).

Config files: `bernstein.yaml` (quality gates, autofix caps, `bernstein.yaml:33`, `bernstein.yaml:62`), `.sdd/` state tree, `.bernstein/workflows/` recipe/DSL files (e.g. `.bernstein/workflows/audit-evidence-pack.yaml:9`), `templates/plan.yaml:105` seed skeleton.

## 9. Extensibility Points

Add an adapter: create `src/bernstein/adapters/<name>.py` with a `CLIAdapter` subclass implementing `spawn()` (`src/bernstein/adapters/base.py:812`) and `name()` (`src/bernstein/adapters/base.py:1069`); import it and add one line to `_ADAPTERS` in `src/bernstein/adapters/registry.py:86` (or call `register_adapter()`, `src/bernstein/adapters/registry.py:348`); add a strategy row to `STRATEGY_MATRIX` (`src/bernstein/adapters/_contract.py:659`); add a YAML contract `tests/contract/contracts/<name>.yaml` loaded by `ContractSpec.load()` (`src/bernstein/adapters/_contract.py:116`). Zero-edit options: ship via the `bernstein.adapters` entry-point group (`src/bernstein/adapters/registry.py:207`, `pyproject.toml:351`), or as a data-only capability profile built by `profile_built_adapter_classes()` (`src/bernstein/adapters/capability_profile.py:1507`), or fall back to `GenericAdapter` with `--prompt`/`--model` flags (`src/bernstein/adapters/generic.py:17`).

Add a gate: declare flags in `QualityGatesConfig` (`src/bernstein/core/quality/quality_gates.py:201`), add a pipeline row in `gate_pipeline.py` (`src/bernstein/core/quality/gate_pipeline.py:378`), and note the final verdict is a conjunction over `blocked` flags with bypass closed unless `allow_bypass` (`src/bernstein/core/quality/gate_runner.py:96`, `src/bernstein/core/quality/gate_runner.py:136`).

Add a workflow recipe: write a workflow body plus typed `params` block; rendering substitutes `{param}` in `prompt`, `command`, and `loop.until` only (`src/bernstein/core/workflows/recipe_spec.py:335`); registration hashes canonical bytes with SHA-256 as identity, with supersede/rollback/pause/resume as receipts (`src/bernstein/core/workflows/recipe_registry.py:288`, `src/bernstein/core/workflows/recipe_registry.py:943`). Apply many recipes at once via a fleet manifest with `plan_hash` drift refusal (`src/bernstein/core/workflows/recipe_fleet.py:105`).

## 10. Limitations and Gotchas

1. Strict replay aborts instead of degrading. A cache miss — including calling a recorded key one time too many — raises `ReplayMissError` and aborts the run; replaying a run with no recording raises `ReplayRecordingMissingError` before any agent spawns (`src/bernstein/core/orchestration/deterministic.py:191`, `src/bernstein/core/orchestration/deterministic.py:426`). Expect brittle replays unless seeds, prompts, and parameters are frozen.
2. Worktrees are directory separation, not kernel isolation. The default worktree backend shares the host filesystem and network; artifact-mode directories under `.sdd/workspaces/` are the same (`docs/architecture/sandbox.md:533`, `docs/architecture/sandbox.md:535`). Stronger backends (docker, e2b, modal, daytona, microvm, and others) are opt-in and some need installs or keys (`docs/architecture/sandbox.md:98`).
3. Quality defaults are weaker than they look. Lint is on, but type-check and tests are off in the library default (`src/bernstein/core/quality/quality_gates.py:201`), while the repo-root `bernstein.yaml` enables tests (`bernstein.yaml:33`) — behavior depends on which config actually loads. The evidence completion gate is fail-open: sealing errors never block completion (`src/bernstein/core/evidence/completion_gate.py:103`).
4. Audit and provenance are partially opt-in. The lineage spine is always on, but the HMAC audit chain requires `BERNSTEIN_AUDIT=1` and features degrade without it (`src/bernstein/core/orchestration/orchestrator.py:1061`, `src/bernstein/core/security/AGENTS.md:29`). A chain of only journal-head seals verifies as `SEAL_ONLY`, not `OK`, and without an external seal even a consistent chain is `unverifiable` as complete (`src/bernstein/core/lineage/spine.py:294`, `src/bernstein/core/replay/journal.py:20`).
5. Failure paths have sharp edges. The DLQ write happens only when a work directory is given, otherwise the older plain-failure path applies, and DLQ write errors are logged but never block (`src/bernstein/core/tasks/task_lifecycle.py:915`). Controller-sidecar load is best-effort: corrupt or version-mismatched state starts fresh with only a warning (`src/bernstein/core/orchestration/controller_state.py:43`). Merges that would stage `.sdd/`, keys, or `bernstein.yaml` are aborted (`src/bernstein/core/git/git_pr.py:404`).

## 11. How It Compares to Alternatives

Note: alternatives below are external context, not named in the wiki pages; positioning is relative to Bernstein's wiki-attested design.

- **LangGraph** — graph-execution framework with model-driven nodes; Bernstein differs by keeping coordination as plain Python with zero model calls on the tick path (`src/bernstein/core/orchestration/orchestrator.py:1470`).
- **CrewAI / AutoGen-style role frameworks** — role-based multi-agent conversation; Bernstein differs by adding git-worktree isolation per task plus a serialized FIFO merge queue with gates (`src/bernstein/core/git/worktree.py:40`, `src/bernstein/core/git/merge_queue.py:200`).
- **OpenHands (OpenDevin)** — sandboxed coding-agent runtime; Bernstein differs by sitting above many such CLIs through one adapter registry instead of being one agent (`src/bernstein/adapters/registry.py:86`).
- **MetaGPT-style SOP (Standard Operating Procedure) pipelines** — fixed role pipelines producing code; Bernstein differs by making phases, conditional edges, retries, and receipts auditable and replayable artifacts (journals, spines, bundles) rather than transcript conventions (`src/bernstein/core/replay/journal.py:71`, `src/bernstein/core/evidence/bundle.py:703`).

## Appendix: Selected Code Snippets

Seed pinning (`src/bernstein/core/orchestration/orchestrator.py:6714`):

```python
    # Apply deterministic random seed if requested via env var.
    _deterministic_seed_env = os.environ.get("BERNSTEIN_DETERMINISTIC_SEED", "").strip()
    if _deterministic_seed_env:
        import random

        try:
            _seed_int = int(_deterministic_seed_env)
            random.seed(_seed_int)
            logger.info("Deterministic mode: random.seed(%d)", _seed_int)
        except ValueError:
            logger.warning("Invalid BERNSTEIN_DETERMINISTIC_SEED=%r, ignoring", _deterministic_seed_env)
```

DAG walk head (`src/bernstein/core/orchestration/task_dag.py:200`):

```python
def topological_iter_with_parallel(dag: TaskDag) -> Iterator[frozenset[TaskNode]]:
    """Walk ``dag`` yielding batches of tasks ready to run.

    A batch is a frozen set of :class:`TaskNode` objects whose
    dependencies are already complete.  Batches preserve the planner's
    parallel-safety declaration:

    * If at least one ready task has ``parallel_safe = False`` we yield
      that task alone (and yield each serial task individually).
    * If every ready task has ``parallel_safe = True`` we yield them
      together as a single concurrent batch.

    Raises:
        TaskDagCycleError: if the DAG has a cycle (unmet deps remain
            after no node can progress).
    """
```

CAS claim guard (`src/bernstein/core/tasks/task_store_core.py:2125` region):

```python
        async with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise KeyError(task_id)
            if expected_version is not None and task.version != expected_version:
                raise ValueError(
                    f"Version conflict: task {task_id} is at version {task.version}, expected {expected_version}"
                )
```

Model-escalation ladder (`src/bernstein/core/tasks/task_lifecycle.py:403` region):

```python
def _escalate_model(current_model: str) -> str:
    """Return the next model in the escalation ladder, capped at 'opus'.

    A name that matches no rung is returned unchanged. The ladder is a
    Claude tier ordering; a model outside it has no "next" rung, and
    inventing one substitutes a name the configured provider may not serve
    (#4274). The historical behaviour picked the sonnet position for any
    unmatched name and escalated to "opus" from there, which is how a
    gateway alias became a 4xx on the first retry.
    """
```
