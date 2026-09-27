> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Deterministic Scheduler: No Model in the Coordination Loop

**In one sentence:** The orchestrator is a single-threaded plain-Python tick loop that matches tasks to agents and verifies completion without calling any model for coordination decisions, and every run is recorded so it can be replayed to an identical task graph.

## Key points

- The orchestrator module declares itself `DETERMINISTIC CODE, not an LLM` that matches tasks to agents via a spawner and verifies completion via a janitor (`src/bernstein/core/orchestration/orchestrator.py:3`).
- The tick loop is single-threaded (`while self._running` in `run`), so ticks never run concurrently and no tick guard is needed (`src/bernstein/core/orchestration/orchestrator.py:6`).
- Task ordering comes from plain-Python graph code: `topological_iter_with_parallel` walks the DAG (Directed Acyclic Graph = task graph with no cycles), sorts ready tasks by id for stable output, and yields serial tasks one at a time (`src/bernstein/core/orchestration/task_dag.py:225`).
- LLM (Large Language Model) calls that do happen (planning/decomposition) are recorded as prompt-plus-model to `llm_calls.jsonl`, and replay serves the recorded responses instead of calling the model again (`src/bernstein/core/orchestration/deterministic.py:3`).
- Replay is strict by default: a cache miss raises `ReplayMissError` and aborts the run instead of silently calling the live model (`src/bernstein/core/orchestration/deterministic.py:21`).
- Every run appends to an always-on Merkle-chained journal at `.sdd/runs/<run_id>/journal.jsonl`, where each event hash chains the previous hash so divergence shows up as a hash mismatch at an exact step index (`src/bernstein/core/replay/journal.py:14`).
- Adaptive controller state (parallelism level, claim-conflict backoff) survives restarts via the sidecar file `.sdd/runtime/controllers.json`, which is reloaded on startup with expired cooldowns pruned (`src/bernstein/core/orchestration/controller_state.py:3`).

---

## 1. What "no model in the coordination loop" means in code

LLM = Large Language Model (the AI text model). The claim is not that Bernstein never calls a model — agents themselves are model-driven. The claim is that the *coordination decisions* (what runs next, which agent gets it, whether it is retried, when it ends) are made by plain Python, with no model call on that path. This matches `docs/scope.md:16`, which lists "scheduling, task assignment, lifecycle management and retry logic" as deterministic Python.

The module docstring states the design directly (`src/bernstein/core/orchestration/orchestrator.py:1`):

```python
"""Orchestrator loop: watch tasks, spawn agents, verify completion, repeat.

The orchestrator is DETERMINISTIC CODE, not an LLM. It matches tasks to agents
via the spawner and verifies completion via the janitor. See ADR-001.

Design note: the tick loop is single-threaded (``while self._running`` in
``run``), so no concurrent-tick guard is required. If threaded ticks are ever
introduced, reintroduce a non-blocking guard (see git history for the removed
``tick_guard`` / ``concurrency_guard`` modules).

This module is the public facade. Heavy lifting lives in:
- tick_pipeline.py   - task fetching, batching, server interaction, TypedDicts
- task_lifecycle.py  - claim/spawn, completion processing, retry/decompose
- agent_lifecycle.py - agent tracking, heartbeat, crash detection, reaping
"""
```

Concretely, inside the files read for this page:

- `tick()` runs one orchestrator cycle: it times the tick, wraps it in a telemetry span, and calls `_tick_internal()` — there is no prompt construction or model call in that path (`src/bernstein/core/orchestration/orchestrator.py:1470`).
- Scheduling order is computed by sorting task ids and checking dependency sets in `task_dag.py` (`src/bernstein/core/orchestration/task_dag.py:220`).
- Parallelism adjustments are arithmetic over error rates and CPU readings (`src/bernstein/core/orchestration/adaptive_parallelism.py:7`).
- Timeout estimates are arithmetic over scope, complexity, model speed factor, history, and file count (`src/bernstein/core/orchestration/adaptive_timeout.py:1`).
- The one place randomness enters routing (`random.choice` / `random.random`) is pinned by seeding Python's `random` module from the `BERNSTEIN_DETERMINISTIC_SEED` environment variable at startup (`src/bernstein/core/orchestration/deterministic.py:17` and `src/bernstein/core/orchestration/orchestrator.py:6714`).

The seed block, copied verbatim (`src/bernstein/core/orchestration/orchestrator.py:6714`):

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

## 2. Tick and loop mechanics

One tick = one pass of `tick()`, which delegates to `_tick_internal()` and warns if a tick takes over 30 seconds (`src/bernstein/core/orchestration/orchestrator.py:1470`):

```python
    def tick(self) -> TickResult:
        """Execute one orchestrator cycle."""
        from bernstein.core.telemetry import start_span

        tick_start = time.monotonic()
        with start_span("orchestrator.tick", attributes={"tick": self._tick_count + 1}):
            result = self._tick_internal()
        tick_duration = time.monotonic() - tick_start
        if tick_duration > 30.0:
            logger.warning("Tick took %.1fs (threshold 30s)", tick_duration)
        return result
```

The `run()` method sets `self._running = True`, records a `run_started` journal event, then loops `while self._running or self._has_active_agents()`, calling `self.tick()` each iteration (`src/bernstein/core/orchestration/orchestrator.py:3151`, `src/bernstein/core/orchestration/orchestrator.py:3313`):

```python
        while self._running or self._has_active_agents():
            tick_result: TickResult | None = None
            try:
                tick_result = self.tick()
                consecutive_failures = 0
            except Exception:
                consecutive_failures += 1
                logger.exception(
                    "Tick %d failed (%d consecutive failures)",
                    self._tick_count,
                    consecutive_failures,
                )
                if consecutive_failures >= max_consecutive_failures:
                    logger.error(
                        "Stopping after %d consecutive tick failures",
                        consecutive_failures,
                    )
                    self._closure_outcome = RunClosureOutcome.FAILED
                    break
            if self._config.dry_run:
                break
```

Loop flow (ASCII):

```
  run() sets _running = True
        │
        ▼
  ┌─ while _running or active agents ─┐
  │  tick() → _tick_internal()        │
  │  failure? log, count; abort       │
  │  after N consecutive failures     │
  │  work found? sleep poll_interval  │
  │  idle? double sleep up to 30 s    │
  └─────────────── │ ─────────────────┘
                   ▼
  _persist_controller_sidecar() + _cleanup()
```

Sleep behavior between ticks: when work was found the loop paces at `poll_interval_s`; when idle it doubles the sleep multiplier up to 8x, capped at 30 seconds; server failures back off at 5 s per failure capped at 30 s (`src/bernstein/core/orchestration/orchestrator.py:3334`). Before cleanup on exit, the controller sidecar is persisted so the next run resumes with usable state (`src/bernstein/core/orchestration/orchestrator.py:3368`).

Each tick also binds the executed task graph to the run: `_record_plan_graph_digest` hashes the structural triple `(task_id, role, sorted(depends_on))` with `canonical_graph_digest` and appends a `plan.graph` journal event only when the digest changes, so a 60-tick run with a static graph writes one row (`src/bernstein/core/orchestration/orchestrator.py:1482`).

## 3. Scheduling in plain Python: the task DAG walk

DAG = Directed Acyclic Graph = a set of tasks with dependencies and no dependency cycles. A node carries a stable id, a description, a `parallel_safe` flag declared by the planner (never inferred), an optional story id, and a `depends_on` tuple (`src/bernstein/core/orchestration/task_dag.py:69`).

`topological_iter_with_parallel` yields one frozen set per batch of ready tasks, copied verbatim (`src/bernstein/core/orchestration/task_dag.py:200`):

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
    pending: dict[str, TaskNode] = dag.nodes.copy()
    completed: set[str] = set()

    while pending:
        ready = [n for n in pending.values() if all(d in completed for d in n.depends_on)]
        if not ready:
            raise TaskDagCycleError(remaining=list(pending))

        # Stable ordering for deterministic output.
        ready.sort(key=lambda n: n.task_id)
```

Batching rule in short form:

```
  ready tasks = deps all completed, sorted by task_id
        │
        ▼
  all parallel_safe and more than 1? ── yes ─► yield whole batch together
        │
        no
        ▼
  yield one serial task alone (parallel-safe nodes wait for next round)
```

A dependency cycle raises `TaskDagCycleError` naming the stuck tasks (`src/bernstein/core/orchestration/task_dag.py:61`). DAGs load from Markdown checkbox lists or YAML under a `tasks:` key (`src/bernstein/core/orchestration/task_dag.py:111`).

The coordinator layer on top tracks multi-agent sessions through phases `PLANNING → DISPATCH → WORKER_EXECUTION → SYNTHESIS → COMPLETE` (`src/bernstein/core/orchestration/coordinator.py:13`). Worker fan-out is capped — the default `max_workers` is 5 and `assign_worker` refuses new assignments at the cap with a warning (`src/bernstein/core/orchestration/coordinator.py:83`):

```python
    def __init__(
        self,
        enabled: bool = False,
        max_workers: int = 5,
        synthesis_model: str = "sonnet",
    ) -> None:
        self.enabled = enabled
        self.max_workers = max_workers
```

## 4. Deterministic replay: recording model responses, strict by default

Since planning calls do use a model, reproducibility comes from recording those calls. Every LLM call (prompt + model → response) is appended to `.sdd/runs/{run_id}/llm_calls.jsonl`, and a later run with the same seed replays cached responses instead of calling the model, producing an identical task decomposition (`src/bernstein/core/orchestration/deterministic.py:1`).

The lookup key folds in every response-determining input so parameter drift cannot masquerade as a cache hit (`src/bernstein/core/orchestration/deterministic.py:27`):

```python
def _prompt_key(
    prompt: str,
    model: str,
    *,
    provider: str = _DEFAULT_PROVIDER,
    temperature: float = _DEFAULT_TEMPERATURE,
    max_tokens: int = _DEFAULT_MAX_TOKENS,
) -> str:
    """Compute a stable lookup key for one LLM request.

    The key folds in every input that changes the model's response so a
    cache hit cannot mask a parameter drift (issue #1832). Widening the key
    invalidates ``llm_calls.jsonl`` files recorded before this change.

    Args:
        prompt: Full prompt string.
        model: Model identifier.
        provider: Provider name (e.g. ``"openrouter_free"``).
        temperature: Sampling temperature.
        max_tokens: Maximum response tokens.

    Returns:
        Hex-encoded SHA-256 over the NUL-separated request tuple.
    """
    # NUL separators keep field boundaries unambiguous; ``temperature`` is
    # formatted with ``repr`` so 0.7 and 0.70 hash identically while 0.7 and
    # 0.0 stay distinct.
    data = f"{model}\x00{prompt}\x00{provider}\x00{temperature!r}\x00{max_tokens}".encode()
    return hashlib.sha256(data).hexdigest()
```

Key replay rules (`src/bernstein/core/orchestration/deterministic.py:173`):

- `DeterministicStore` has two modes: recording (default, appends to `llm_calls.jsonl`) and replay (pre-loads the file, serves responses without writing).
- Order and multiplicity are preserved: a key called N times records N responses in a per-key FIFO (First In First Out) queue, and the Nth replay call gets the Nth recorded response (`src/bernstein/core/orchestration/deterministic.py:183`).
- Strict mode is the default: a cache miss — including requesting a key more times than recorded — raises `ReplayMissError` and aborts instead of calling the live model (`src/bernstein/core/orchestration/deterministic.py:191`).
- Opt-out exists via the `BERNSTEIN_REPLAY_ALLOW_LIVE_MISS` environment flag, which downgrades misses to a logged warning plus live fall-through (`src/bernstein/core/orchestration/deterministic.py:53`).
- Strict replay against a run with no recording raises `ReplayRecordingMissingError` before any agent spawns, so the run cannot silently degrade to live (`src/bernstein/core/orchestration/deterministic.py:426`).
- One store is active per orchestrator subprocess via the module-level `get_active_store` / `set_active_store` pair (`src/bernstein/core/orchestration/deterministic.py:407`).

Replay flow (ASCII):

```
  bernstein run --seed 42 ──► record to llm_calls.jsonl
        │
        ▼
  bernstein replay <run_id> ──► load llm_calls.jsonl into per-key FIFO
        │
        ├── hit ──► serve Nth recorded response, consume from queue
        │
        └── miss ──► strict (default): raise ReplayMissError, abort run
                     allow-live-miss: warn + call live model
```

A second, older replay path exists: `ReplayGateway` records `(kind, key)` pairs to `.sdd/runs/<run_id>/events.jsonl` with opt-in recording via `BERNSTEIN_RECORD`, serving fixtures in replay mode without invoking the provider (`src/bernstein/core/replay/gateway.py:1`). The newer canonical journal (section 5) replaced the old `BERNSTEIN_RECORD` on/off gate with a retention knob (`src/bernstein/core/replay/journal.py:30`).

## 5. Journal: the always-on Merkle-chained event log

The `EventJournal` is the single canonical per-run event log at `.sdd/runs/<run_id>/journal.jsonl` (`src/bernstein/core/replay/journal.py:71`). Each event hash is computed as `event_hash = H(prev_hash, event_type, payload_hash, monotonic_index)`, where `payload_hash` is SHA-256 over the canonical JSON of the payload with wall-clock fields (`ts`, `elapsed_s`) excluded, so two executions that differ only in timing produce the same hash chain (`src/bernstein/core/replay/journal.py:11`).

Hash functions, copied verbatim (`src/bernstein/core/replay/journal.py:189`):

```python
def _payload_hash(event_type: str, payload: dict[str, Any]) -> str:
    """Return the SHA-256 of the canonical, timing-excluded payload.

    The ``event`` type and the decision-relevant payload keys are hashed;
    the wall-clock envelope and the derived chain fields are dropped so a
    faithful replay - which differs only in timing - hashes identically.
    """
    projected = {k: v for k, v in payload.items() if k not in _NON_DETERMINISTIC_FIELDS}
    projected["event"] = event_type
    canonical = json.dumps(projected, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def compute_event_hash(*, prev_hash: str, event_type: str, payload_hash: str, index: int) -> str:
    """Return ``event_hash = H(prev_hash, event_type, payload_hash, index)``.

    The pre-image is canonical JSON of the ordered field tuple, so the
    digest is stable across processes and platforms.
    """
    preimage = json.dumps(
        {
            "prev_hash": prev_hash,
            "event_type": event_type,
            "payload_hash": payload_hash,
            "index": index,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(preimage).hexdigest()
```

Chain shape (ASCII):

```
  genesis ("") ──► event 0 ──► event 1 ──► event 2 ──► head
  each row stores prev_hash + payload_hash + event_hash
  verify recomputes every row; first mismatch names divergent_index
```

Verification reports three independent verdicts — chain consistency, reader coverage, and identity against an external seal — and names the first divergent step index with expected vs stored hash (`src/bernstein/core/replay/journal.py:283`). Without an external seal, even a consistent chain is `unverifiable` as a *complete* journal, since only comparison with an independently sealed head proves nothing was truncated (`src/bernstein/core/replay/journal.py:20`). `bernstein replay <run_id> --verify` recomputes the head and `--from-step N` rebuilds deterministic state to step N (per docs; CLI wiring not verified in source).

Journal writes are thread-safe for the single-writer tick loop under one lock covering sequence, head, and file write (`src/bernstein/core/replay/journal.py:354`). Retention via `BERNSTEIN_REPLAY_RETENTION` prunes only past run directories, never the active chain mid-run (`src/bernstein/core/replay/journal.py:741`).

## 6. Adaptive parallelism and adaptive timeouts

Both controllers are arithmetic, not model calls.

**Adaptive parallelism** scales effective concurrent agents between 1 and the configured maximum (`src/bernstein/core/orchestration/adaptive_parallelism.py:1`):

- Start at configured `max_agents`.
- Error rate above 20% over the sliding window: reduce parallelism by 1 (floor 1).
- Error rate below 5% for 10 continuous minutes: increase by 1 (up to max).
- CPU above 80%: pause spawning (effective max 0) until load drops.

**Adaptive timeout** computes per-task timeouts from scope, complexity, model speed, historical averages, and file count instead of one static value (`src/bernstein/core/orchestration/adaptive_timeout.py:1`). Baked-in factors include complexity multipliers (low 0.7, medium 1.0, high 1.5), model speed factors (haiku 0.5, sonnet 1.0, opus 1.5), a 300 s minimum, a 7200 s maximum, 1.5x headroom over historical averages, and 30 s per file (`src/bernstein/core/orchestration/adaptive_timeout.py:32`). History comes from `.sdd/archive/tasks.jsonl` (`src/bernstein/core/orchestration/adaptive_timeout.py:49`).

**Persistence across restarts:** the orchestrator's `AdaptiveParallelism` state and claim-conflict backoff dictionary are in-process only, so the sidecar at `.sdd/runtime/controllers.json` saves a snapshot on every slow tick and on shutdown and restores it on startup (`src/bernstein/core/orchestration/controller_state.py:1`). Loading is best-effort: a missing, corrupt, or version-mismatched sidecar logs a warning and starts fresh rather than crashing (`src/bernstein/core/orchestration/controller_state.py:43`):

```python
def load(
    workdir: Path,
) -> tuple[AdaptiveParallelismState, dict[str, ClaimConflictEntry]]:
    """Load persisted controller state from the sidecar.

    Returns:
        A ``(ap_state, conflict_state)`` tuple. On any error (missing file,
        corrupt JSON, version mismatch, I/O failure) the functions log a
        warning and return clean-naive state — the orchestrator starts as if
        no sidecar was ever written.
    """
    path = _sidecar_path(workdir)
    if not path.exists():
        logger.debug("Controller sidecar not found at %s — starting fresh", path)
        return _naive_state()

    try:
        raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Controller sidecar corrupt at %s — starting fresh: %s", path, exc)
        return _naive_state()

    return _unmarshal(raw, path)
```

Expired backoff entries (windows already elapsed) are pruned on load so restarts do not resurrect dead cooldowns (`src/bernstein/core/orchestration/controller_state.py:18`).

## 7. Where persistent state lives

All persistent orchestrator state is plain text under `.sdd/` — YAML, Markdown, JSONL (JSON Lines = one JSON object per line), JSON — with no database (`docs/scope.md:33`, confirmed by the file paths below in source):

| Path | Content | Written by |
|---|---|---|
| `.sdd/runs/<run_id>/journal.jsonl` | Canonical Merkle-chained event log | `EventJournal` (`src/bernstein/core/replay/journal.py:71`) |
| `.sdd/runs/<run_id>/llm_calls.jsonl` | Recorded LLM prompt→response pairs | `DeterministicStore` (`src/bernstein/core/orchestration/deterministic.py:4`) |
| `.sdd/runs/<run_id>/events.jsonl` | Gateway fixtures (older replay path) | `ReplayGateway` (`src/bernstein/core/replay/gateway.py:53`) |
| `.sdd/runtime/controllers.json` | Parallelism + claim-conflict snapshot | controller sidecar (`src/bernstein/core/orchestration/controller_state.py:3`) |
| `.sdd/archive/tasks.jsonl` | Historical task completions for timeout estimates | timeout history (`src/bernstein/core/orchestration/adaptive_timeout.py:49`) |

## 8. Docs claims vs source

- "Scheduling is plain Python, so a run is reproducible end to end. Replay yesterday's plan and get yesterday's task graph." (`README.md:46`) — confirmed: tick loop, DAG walk, seed, and `llm_calls.jsonl` replay are all in source as cited above.
- "The scheduler executes it as plain Python — nothing in the file is a prompt, and no model decides what happens next." (`README.md:55`) — confirmed for the scheduling files read (tick, DAG, parallelism, timeout, seed); no model call appears on those paths.
- "No model sits in the coordination loop, so replaying a plan reproduces its task graph byte-identically." (`commands/run.md:5`, `action.yml:2`) — confirmed as the replay mechanism: same seed plus cached responses reproduces the same decomposition, and the `plan.graph` digest event binds the executed graph into the journal (`src/bernstein/core/orchestration/orchestrator.py:1482`).
- "Zero tokens are spent on coordination." (`docs/scope.md:17`) — (per docs; not verified in source): no token counter was found in the scheduling files read; the mechanism (no model call on the coordination path) supports it but the zero-token measurement itself was not verified.
- "The deterministic scheduler keeps the coordination plan and delegates each leaf's mechanical execution to a native subagent ... the outer DAG is a pure function of the plan, so it replays byte-identically even when inner execution is stochastic." (`docs/reference/capabilities.md:37`) — (per docs; not verified in source): subagent delegation was not examined in the files read for this page.

**Covers:** README.md (at a glance, what a run looks like), docs/scope.md, src/bernstein/core/orchestration/orchestrator.py, src/bernstein/core/orchestration/deterministic.py, src/bernstein/core/orchestration/coordinator.py, src/bernstein/core/orchestration/controller_state.py, src/bernstein/core/orchestration/task_dag.py, src/bernstein/core/orchestration/adaptive_parallelism.py, src/bernstein/core/orchestration/adaptive_timeout.py, src/bernstein/core/replay/journal.py, src/bernstein/core/replay/gateway.py
