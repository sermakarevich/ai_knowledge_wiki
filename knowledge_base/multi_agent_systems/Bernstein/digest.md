> [[index|Wiki]] | [[summary|Summary]]

# Bernstein — Digest

The whole source at medium depth: every component's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-deterministic-scheduler|Deterministic Scheduler]]
**In one sentence:** The orchestrator is a single-threaded plain-Python tick loop that matches tasks to agents and verifies completion without calling any model for coordination decisions, and every run is recorded so it can be replayed to an identical task graph.
- The orchestrator module declares itself `DETERMINISTIC CODE, not an LLM` that matches tasks to agents via a spawner and verifies completion via a janitor (`src/bernstein/core/orchestration/orchestrator.py:3`).
- The tick loop is single-threaded (`while self._running` in `run`), so ticks never run concurrently and no tick guard is needed (`src/bernstein/core/orchestration/orchestrator.py:6`).
- Task ordering comes from plain-Python graph code: `topological_iter_with_parallel` walks the DAG (Directed Acyclic Graph = task graph with no cycles), sorts ready tasks by id for stable output, and yields serial tasks one at a time (`src/bernstein/core/orchestration/task_dag.py:225`).
- LLM (Large Language Model) calls that do happen (planning/decomposition) are recorded as prompt-plus-model to `llm_calls.jsonl`, and replay serves the recorded responses instead of calling the model again (`src/bernstein/core/orchestration/deterministic.py:3`).
- Replay is strict by default: a cache miss raises `ReplayMissError` and aborts the run instead of silently calling the live model (`src/bernstein/core/orchestration/deterministic.py:21`).
- Every run appends to an always-on Merkle-chained journal at `.sdd/runs/<run_id>/journal.jsonl`, where each event hash chains the previous hash so divergence shows up as a hash mismatch at an exact step index (`src/bernstein/core/replay/journal.py:14`).
- Adaptive controller state (parallelism level, claim-conflict backoff) survives restarts via the sidecar file `.sdd/runtime/controllers.json`, which is reloaded on startup with expired cooldowns pruned (`src/bernstein/core/orchestration/controller_state.py:3`).

## 2. [[wiki/02-task-lifecycle-retries|Task Backlog, Lifecycle, and Retry Handling]]
**In one sentence:** In Bernstein 3.19.1, tasks move through a fixed set of states, are claimed so only one worker owns them at a time, and failed tasks are retried with a stronger model or effort setting before being stored in a permanent failure list.
- Tasks have 17 fixed states (such as open, claimed, in progress, done, failed, suspended) defined in one list, so every part of the system uses the same names (src/bernstein/core/tasks/models.py:187).
- The file-based backlog prevents two workers from taking the same task by holding a thread lock plus an Operating System (OS) file lock while it reloads, picks, marks, and saves the backlog in one step (src/bernstein/core/tasks/claim.py:338).
- The database-backed store prevents double claims with a version check called Compare-And-Swap (CAS): a claim with an old version number is rejected instead of taking over the task (src/bernstein/core/tasks/task_store_core.py:2161).
- After a server restart, tasks stuck in claimed or in progress return to open so new workers can take them, and the reset is written to disk at once so a second crash does not lose it (src/bernstein/core/tasks/task_store_core.py:758).
- A failed task is retried with more effort first and a stronger model later (for example haiku to sonnet to opus), unless the operator fixed the model by hand, in which case the model never changes (src/bernstein/core/tasks/task_lifecycle.py:446).
- Warm retries that resume the old session are only allowed when a verified checkpoint exists and the workspace still matches; any mismatch falls back to a cold restart from zero (src/bernstein/core/tasks/checkpoint_retry.py:478).
- Tasks that use up all retries go to a Dead Letter Queue (DLQ), which is a permanent failure list stored as JSON Lines (JSONL, one JSON object per line) that an operator can read and resubmit (src/bernstein/core/tasks/dead_letter_queue.py:180).
- A completed task that fails the janitor check (the automatic quality checker) is reopened under the same id up to a fixed limit, then marked permanently failed (src/bernstein/core/tasks/task_lifecycle.py:5173).

## 3. [[wiki/03-worktrees-merge-gates|Per-Task Worktrees, Isolation, and Merge Gates]]
**In one sentence:** Each task runs in its own git worktree (a separate checked-out copy of the repo) on its own branch, and its work reaches the main branch only after passing checks and a one-at-a-time merge queue.
- Each agent session gets its own git worktree under `.sdd/worktrees/<session_id>`, so two agents never write to the same files (`src/bernstein/core/git/worktree.py:3`, `src/bernstein/core/git/worktree.py:40`).
- Each session works on its own branch named `agent/<session_id>`, which is how the system knows which change belongs to which task (`src/bernstein/core/git/merge_queue.py:47`, `src/bernstein/core/worktrees/change_set.py:146`).
- The only shared state between agents is the task list (backlog); a task is claimed with CAS (compare-and-swap, a check that the task version is unchanged before taking it) so two workers cannot claim the same task (`src/bernstein/core/tasks/task_lifecycle.py:2593`).
- Before a merge lands, quality gates can run: lint with ruff, type check with pyright, and tests (`src/bernstein/core/quality/quality_gates.py:203`, `src/bernstein/core/quality/quality_gates.py:205`, `src/bernstein/core/quality/quality_gates.py:207`).
- Merges are serialized (run one at a time, never in parallel) through a FIFO (first-in-first-out) merge queue (`src/bernstein/core/orchestration/orchestrator.py:870`, `src/bernstein/core/git/merge_queue.py:200`).
- Conflicts are detected before merging with `git merge-tree`, which simulates a merge without touching files (`src/bernstein/core/git/merge_queue.py:139`); a real merge that conflicts is aborted with `git merge --abort` (`src/bernstein/core/git/git_pr.py:446`).
- Tasks that produce files instead of code (artifact mode) get a plain directory under `.sdd/workspaces/<session_id>` with no branch and nothing to merge (`src/bernstein/core/agents/spawner_worktree.py:33`, `src/bernstein/core/tasks/artifact_completion.py:168`).
- Worktrees can be turned off with the `use_worktrees` flag (default on); when off, no worktree manager is created (`src/bernstein/core/agents/spawner_core.py:1636`, `src/bernstein/core/agents/spawner_worktree.py:95`).

## 4. [[wiki/04-adapter-registry|Multi-Harness Support: The Adapter Registry]]
**In one sentence:** Bernstein runs many different coding-agent CLIs (CLI = Command-Line Interface) through one registry that maps a short name such as `claude` to an adapter class implementing a shared `spawn` interface.
- The registry is a plain dict named `_ADAPTERS` mapping short names to adapter classes or instances, defined in `src/bernstein/adapters/registry.py:86`.
- `get_adapter()` in `src/bernstein/adapters/registry.py:232` instantiates the class for a name and stamps the name on the instance (`src/bernstein/adapters/registry.py:293`), raising `ValueError` for unknown names (`src/bernstein/adapters/registry.py:284`).
- Every adapter implements the `CLIAdapter` interface in `src/bernstein/adapters/base.py:528`, whose two required methods are `spawn()` (`src/bernstein/adapters/base.py:812`) and `name()` (`src/bernstein/adapters/base.py:1069`).
- Provider strings such as `openai` resolve to adapters through the `provides` tuples declared per adapter (default `src/bernstein/adapters/base.py:1251`), consumed by `adapter_name_for_provider()` in `src/bernstein/adapters/registry.py:517`.
- The `generic` adapter (`src/bernstein/adapters/generic.py:17`) wraps any CLI with a configurable `--prompt` / `--model` command shape, and `get_adapter()` special-cases it in `src/bernstein/adapters/registry.py:266`.
- Third-party adapters register without source edits via the `bernstein.adapters` entry-point group, loaded in `src/bernstein/adapters/registry.py:207` and declared in `pyproject.toml:351`.
- New agents can ship as data-only declarations: `profile_built_adapter_classes()` in `src/bernstein/adapters/capability_profile.py:1507` builds adapter classes from profiles and merges them into the registry in `src/bernstein/adapters/registry.py:160`.
- Each adapter declares a five-axis strategy row (resume, dangerous-mode, event-channel, output-mode, session-state) in `STRATEGY_MATRIX` (`src/bernstein/adapters/_contract.py:659`), read through `strategy_for()` (`src/bernstein/adapters/_contract.py:884`).

## 5. [[wiki/05-workflow-abstraction|Workflow Abstraction: Task Graphs, Roles, and Artifact Contracts]]
**In one sentence:** Bernstein runs work as a task graph (a set of tasks linked by dependencies) where phases limit which roles can act, edges control order, and each phase or file deliverable must match a written contract before the run moves on.
- Bernstein has two workflow formats: a YAML manifest (YAML = a human-readable config file format) with `nodes` as a list, and a DSL (DSL = Domain-Specific Language, a small config language for one job) with `phases` plus `nodes` as a mapping; the CLI tells them apart by structure (`src/bernstein/cli/commands/workflow_cmd.py:28`, `src/bernstein/cli/commands/workflow_cmd.py:51`).
- A YAML manifest node sets exactly one of `command` or `agent`, with `depends_on`, `when`, `loop`, `fresh_context`, and `timeout_seconds` as options (`src/bernstein/core/workflows/workflow_spec.py:141`, `src/bernstein/core/workflows/workflow_spec.py:176`).
- Nodes form a DAG (DAG = Directed Acyclic Graph, a graph with no loops); the loader rejects unknown dependencies and cycles, and the runner groups nodes into parallel layers in topological order (`src/bernstein/core/workflows/workflow_spec.py:263`, `src/bernstein/core/workflows/workflow_spec.py:310`).
- A governed phase lists `allowed_roles`; an empty set means all roles pass, and only tasks whose role matches count toward phase completion (`src/bernstein/core/planning/workflow.py:56`, `src/bernstein/core/planning/workflow.py:265`).
- A DSL edge is either plain (`depends_on: [decompose]`) or guarded (`source` plus `condition`, for example `status == 'failed'`), and the guard is checked with a safe AST (AST = Abstract Syntax Tree, the parsed form of an expression) evaluator without `eval()` (`src/bernstein/core/planning/workflow_dsl.py:648`, `src/bernstein/core/planning/workflow_dsl.py:126`).
- A non-code deliverable (report, dataset, action log, ops result) completes on the signed lineage entry hash of its canonical bytes, and the receipt is only written after all declared checks pass (`src/bernstein/core/tasks/artifact_completion.py:11`, `src/bernstein/core/tasks/artifact_completion.py:31`).
- A recipe is a workflow plus a typed `params` block; rendering substitutes `{param}` in `prompt`, `command`, and `loop.until` only, leaves `{goal}` for the runner, and then validates as a normal workflow (`src/bernstein/core/workflows/recipe_spec.py:335`, `src/bernstein/core/workflows/recipe_spec.py:291`).
- A registered recipe is identified by the SHA-256 hash (SHA-256 = a function that maps bytes to a fixed 256-bit fingerprint) of its canonical bytes; register, supersede, rollback, pause, and resume are receipts on the HMAC (HMAC = Hash-based Message Authentication Code, a keyed checksum) chain (`src/bernstein/core/workflows/recipe_registry.py:288`, `src/bernstein/core/workflows/recipe_registry.py:943`).

## 6. [[wiki/06-lineage-receipts-audit|Lineage, Receipts, and the Audit Chain]]
**In one sentence:** Bernstein records what each agent wrote as hash-chained, HMAC-tagged (HMAC = Hash-based Message Authentication Code) rows in append-only JSONL (JSONL = one JSON object per line) files, and signs selected records with Ed25519 (Ed25519 = a digital-signature algorithm) so they verify offline.
- The lineage spine is always on: every adapter artifact write routes through `LineageSpine.record`, while the HMAC audit chain is opt-in at runtime via `BERNSTEIN_AUDIT=1` (src/bernstein/core/lineage/spine.py:12, src/bernstein/core/orchestration/orchestrator.py:1061, src/bernstein/core/security/AGENTS.md:29).
- Each spine entry chains `entry_hash = H(prev_hash, artifact_path, content_hash, ...)` and carries an HMAC tag made with the audit-chain key, and `verify` recomputes the whole chain plus every tag (src/bernstein/core/lineage/spine.py:18, src/bernstein/core/lineage/spine.py:21, src/bernstein/core/lineage/spine.py:612).
- The per-run replay journal is a separate Merkle chain with `event_hash = H(prev_hash, event_type, payload_hash, monotonic_index)`, and its head is sealed into the spine at run finalization (src/bernstein/core/replay/journal.py:14, src/bernstein/core/replay/journal.py:1265).
- Signed lineage entries add attributable non-repudiation on top of the spine: an Ed25519 detached JWS (JWS = JSON Web Signature) over canonical bytes plus an operator-HMAC envelope over every field (src/bernstein/core/lineage/signed_write.py:16, src/bernstein/core/lineage/entry.py:4).
- Evidence bundles bind task-producer outputs into one signed, spine-anchored record stored content-addressed (address = content hash) under a per-blob 1 MiB cap, mirrored into the HMAC audit chain (src/bernstein/core/evidence/bundle.py:104, src/bernstein/core/evidence/bundle.py:114, src/bernstein/core/evidence/bundle.py:703).
- Offline verification needs no orchestrator and no network: the `verify_cli` wheel checks Ed25519 signatures, parent-hash linkage, and canonical bytes using only the pack plus `cryptography` and `click` (verify_cli/README.md:9, verify_cli/README.md:28, verify_cli/README.md:43).
- Any one-byte change surfaces as a named hash mismatch (`entry_hash mismatch`, `hmac mismatch`, `prev_hash break`, blob-diverges messages), which is also how non-deterministic replay shows up: as a mismatch at a precise step index (src/bernstein/core/lineage/spine.py:690, src/bernstein/core/replay/journal.py:1149, src/bernstein/core/evidence/bundle.py:980).

## 7. [[wiki/07-policy-quality-gates|Policy as Code and Quality Gates]]
**In one sentence:** Bernstein declares checks and limits in YAML (YAML Ain't Markup Language, a text config format) files and enforces them in code that can block merges, tool calls, task starts, and credential use.
- Quality gates are declared in `bernstein.yaml` under `quality_gates:` and loaded as `QualityGatesConfig` defaults in code (src/bernstein/core/quality/quality_gates.py:201, bernstein.yaml:33).
- The gate runner treats the run as passing only when no result is marked blocked, and refuses bypass unless config allows it (src/bernstein/core/quality/gate_runner.py:96, src/bernstein/core/quality/gate_runner.py:138).
- A change that contains a run-configuration path is blocked by the run-config gate, which checks the changed-file names (src/bernstein/core/quality/run_config_gate.py:73, src/bernstein/core/quality/gate_pipeline.py:394).
- Tool-call approval defaults to off (`interactive=False`) with a 10 minute TTL (TTL, Time To Live, how long a request waits) and an opt-in classifier shortcut (src/bernstein/core/approval/gate.py:97, src/bernstein/core/approval/queue.py:45).
- Task-start approval uses files under `.sdd/runtime/approvals/` with `.pending`, `.approved`, and `.rejected` sentinels (src/bernstein/core/orchestration/approval_gate.py:57, src/bernstein/core/orchestration/approval_gate.py:416).
- Adapter spawn requires proof: the adapter admission gate seals admit or refusal receipts and anchors them in the audit chain (src/bernstein/adapters/admission.py:1198, src/bernstein/adapters/registry.py:267).
- Per-agent credentials are scoped grants bound to task, audience (the service the token may be shown to), expiry, and capability ceiling (a list that caps what the token may do), signed and hash-chained (src/bernstein/core/identity/grants.py:109, src/bernstein/core/identity/grants.py:540).
- Cost-aware routing uses LinUCB (Linear Upper Confidence Bound, a math method that balances trying new options and reusing good ones) plus UCB1 for effort, with reward `quality * (1 - normalized_cost)` (src/bernstein/core/routing/bandit_router.py:1129, src/bernstein/core/routing/bandit_router.py:1647).

## 8. [[wiki/targeted|Targeted Comparison for Fleet]]
**In one sentence:** Fleet should borrow Bernstein's deterministic (fully predictable, no randomness) coordination loop, bounded retries with model escalation, dead-letter queue (DLQ, a permanent list of tasks that failed for good), per-task worktrees with a serial merge queue, and a plugin-style adapter registry.
- Coordination is plain Python with no model call on the decision path: one single-threaded tick loop matches tasks to agents and verifies completion (`src/bernstein/core/orchestration/orchestrator.py:1470`).
- Reproducibility comes from recording model responses to `llm_calls.jsonl` and replaying them strictly — a cache miss aborts instead of calling the live model (`src/bernstein/core/orchestration/deterministic.py:21`).
- Failed tasks retry on a bounded budget (hard cap of 2 regular retries), escalating effort first then model strength (haiku to sonnet to opus), and exhausted tasks land in a JSONL (JSON Lines, one JSON object per line) dead-letter queue the operator can resubmit (`src/bernstein/core/tasks/task_lifecycle.py:120`, `src/bernstein/core/tasks/dead_letter_queue.py:180`).
- Warm retries that resume an old session are only allowed when a verified checkpoint exists and the workspace hash still matches; anything else restarts cold from zero (`src/bernstein/core/tasks/checkpoint_retry.py:493`).
- Each task works in its own git worktree (a separate checked-out copy of the repo) on its own `agent/<session_id>` branch, and merges go through a strict FIFO (first-in-first-out) queue one at a time with lint, type-check, and test gates (`src/bernstein/core/git/worktree.py:1046`, `src/bernstein/core/git/merge_queue.py:277`).
- Double-claims are blocked by version checks (Compare-And-Swap, CAS: the claim only succeeds if the task version is unchanged) and stale claims from crashed workers reset to open on restart (`src/bernstein/core/tasks/task_store_core.py:2163`, `src/bernstein/core/tasks/task_store_core.py:758`).
- Any coding-agent CLI (command-line tool) plugs in through one adapter registry: a name-to-class dict plus a shared `spawn` interface, so fleet could support many coder backends without rewriting orchestration (`src/bernstein/adapters/registry.py:86`).

## The system in five moves
1. A goal enters as a workflow or plan and decomposes into a dependency-ordered task graph with roles and phases.
2. Workers claim tasks atomically with version checks so only one owner holds each task.
3. Each claimed task executes in its own worktree and branch via a registry-resolved agent adapter.
4. Completion passes through quality gates, approval gates, and retry or escalation on failure.
5. Merges serialize through a FIFO queue with conflict pre-flight onto the main branch.
6. Every artifact, event, and receipt anchors into hash-chained lineage and audit stores for offline verification.
