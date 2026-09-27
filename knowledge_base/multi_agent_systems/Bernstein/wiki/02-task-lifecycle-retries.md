> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Task Backlog, Lifecycle, and Retry Handling
**In one sentence:** In Bernstein 3.19.1, tasks move through a fixed set of states, are claimed so only one worker owns them at a time, and failed tasks are retried with a stronger model or effort setting before being stored in a permanent failure list.
## Key points
- Tasks have 17 fixed states (such as open, claimed, in progress, done, failed, suspended) defined in one list, so every part of the system uses the same names (src/bernstein/core/tasks/models.py:187).
- The file-based backlog prevents two workers from taking the same task by holding a thread lock plus an Operating System (OS) file lock while it reloads, picks, marks, and saves the backlog in one step (src/bernstein/core/tasks/claim.py:338).
- The database-backed store prevents double claims with a version check called Compare-And-Swap (CAS): a claim with an old version number is rejected instead of taking over the task (src/bernstein/core/tasks/task_store_core.py:2161).
- After a server restart, tasks stuck in claimed or in progress return to open so new workers can take them, and the reset is written to disk at once so a second crash does not lose it (src/bernstein/core/tasks/task_store_core.py:758).
- A failed task is retried with more effort first and a stronger model later (for example haiku to sonnet to opus), unless the operator fixed the model by hand, in which case the model never changes (src/bernstein/core/tasks/task_lifecycle.py:446).
- Warm retries that resume the old session are only allowed when a verified checkpoint exists and the workspace still matches; any mismatch falls back to a cold restart from zero (src/bernstein/core/tasks/checkpoint_retry.py:478).
- Tasks that use up all retries go to a Dead Letter Queue (DLQ), which is a permanent failure list stored as JSON Lines (JSONL, one JSON object per line) that an operator can read and resubmit (src/bernstein/core/tasks/dead_letter_queue.py:180).
- A completed task that fails the janitor check (the automatic quality checker) is reopened under the same id up to a fixed limit, then marked permanently failed (src/bernstein/core/tasks/task_lifecycle.py:5173).
---
## Task states
All states live in the `TaskStatus` list in src/bernstein/core/tasks/models.py:187. The normal path is open to claimed to in progress to done to closed. Failure paths include failed, orphaned (worker crashed mid-task), blocked, cancelled, abandoned, refused, and blocked by a failed dependency. Two special waiting states are suspended (parked by the operator, resumable) and pending approval (work finished, waiting for a human).

```python
class TaskStatus(Enum):
    PLANNED = "planned"  # Awaiting human approval before execution (plan mode)
    OPEN = "open"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CLOSED = "closed"
    FAILED = "failed"
    BLOCKED = "blocked"
    WAITING_FOR_SUBTASKS = "waiting_for_subtasks"
    CANCELLED = "cancelled"
    ORPHANED = "orphaned"  # Agent crashed mid-task; pending crash recovery
    SUSPENDED = "suspended"  # Operator-parked mid-session; infra released, resumable from an attested receipt (#2552)
    PENDING_APPROVAL = "pending_approval"  # Completed; awaiting human approval before taking effect
    ABANDONED = "abandoned"  # Agent voluntarily abandoned with a structured reason (#1350)
    BLOCKED_BY_ABANDON = "blocked_by_abandon"  # Downstream task waiting on an abandoned dependency (#1350)
    BLOCKED_BY_FAILED_DEP = "blocked_by_failed_dep"  # Downstream task whose dependency ended unsuccessfully (#3452)
    REFUSED = "refused"  # Worker reported a typed refusal via the completion contract (#2244)
```

State changes go through one function so illegal jumps are caught and audit records are written; the restart-recovery code notes that CLAIMED to OPEN and IN_PROGRESS to OPEN are both allowed jumps (src/bernstein/core/tasks/task_store_core.py:780). Marking a task failed also records the result, stamps the finish time, and pushes the failure to dependent tasks (src/bernstein/core/tasks/task_store_core.py:2437).
## Atomic backlog claims
Atomic here means the whole take-a-task step happens as one unbreakable unit. There are two claim paths: a small file-based backlog and the main server store.
For the file backlog, each claim takes a per-file thread lock and then a cross-process OS file lock, reloads the file, marks one fitting row as in progress, stamps the claimer name and time, and saves with an atomic file replace (src/bernstein/core/tasks/claim.py:64). Because load, mark, and save all happen inside the lock, two claimers cannot read the same open row and both take it. Rows that are not open or already have a claimer are skipped (src/bernstein/core/tasks/claim.py:101), and each claim raises the attempt counter (src/bernstein/core/tasks/claim.py:223).

```python
def claim_next_entry(
    backlog_path: Path,
    claimer_id: str,
    filter: ClaimFilter | None = None,
) -> BacklogEntry | None:
    """Atomically claim and return the next eligible backlog entry."""
    claim_filter = filter or ClaimFilter()
    backlog = Backlog(path=backlog_path)
    with _backlog_lock(backlog.lock_path):
        backlog = Backlog.load(backlog_path)
        now = time.time()
        for entry in backlog.entries:
            if claim_filter.allows(entry):
                entry.claim(claimer_id, now=now)
                backlog.save()
                # claimer_id is caller-supplied (it reaches here from the
                # claim-receipt HTTP route); strip CR/LF before logging so it
                # cannot forge additional log lines.
                logger.debug(
                    "claim_next: %s -> %s (backlog=%s)",
                    entry.id,
                    sanitize_log(claimer_id),
                    backlog_path,
                )
                return entry
    return None
```

For the server store, claims run inside an async lock (a mutual-exclusion lock for async code) and move the task from OPEN to CLAIMED in one guarded step (src/bernstein/core/tasks/task_store_core.py:2066). Claiming by id adds a CAS check: the caller sends the version it saw, and the store rejects the claim when the version has moved, when the role does not match, or when the task is no longer open (src/bernstein/core/tasks/task_store_core.py:2125). A claim for a non-open task raises an error that the Hypertext Transfer Protocol (HTTP) layer maps to 409 Conflict instead of handing the task out twice (src/bernstein/core/tasks/task_store_core.py:2169).

```python
        async with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise KeyError(task_id)
            if expected_version is not None and task.version != expected_version:
                raise ValueError(
                    f"Version conflict: task {task_id} is at version {task.version}, expected {expected_version}"
                )
            if agent_role is not None and task.role != agent_role:
                raise ValueError(
                    f"role mismatch: task {task_id} requires role '{task.role}', agent has role '{agent_role}'"
                )
            if task.status != TaskStatus.OPEN:
                # never silently re-return an already-claimed or
                # terminal task - that enables double-claim. Raise so the
                # HTTP layer can map it to 409 Conflict.
                raise ValueError(
                    f"task {task_id} is not open (status={task.status.value}); "
                    f"cannot claim (already claimed by session "
                    f"{task.claimed_by_session!r})"
                )
            if not self._dependencies_satisfied(task):
                raise ValueError(f"task {task_id} has unresolved dependencies")
```

The claim path also refuses tasks whose dependencies are unmet or whose files overlap with running work (src/bernstein/core/tasks/task_store_core.py:2099). Workers tied to one coordinator pass their coordinator id, so they only take tasks from their own group and never steal from another group (src/bernstein/core/tasks/task_store_core.py:2089); the session-scoping tests check exactly this behavior (tests/unit/test_task_claiming_by_session.py:146). When a claim hits a version conflict, the worker re-reads the task and retries with the fresh version, up to 5 tries, then stops instead of looping forever (src/bernstein/core/tasks/task_lifecycle.py:93, src/bernstein/core/tasks/task_lifecycle.py:2040). The `task_claim.py` file itself holds no logic; it only re-exports claim functions that live in `task_lifecycle.py` (src/bernstein/core/tasks/task_claim.py:10).
## Worker restart handling
Two recovery methods handle workers that die without releasing their tasks. On server restart, `recover_stale_claimed_tasks` resets every CLAIMED and IN_PROGRESS task to OPEN and clears the claim owner and time (src/bernstein/core/tasks/task_store_core.py:758). The reset is written to the JSONL log right away so a second crash cannot bring the stale claim back (src/bernstein/core/tasks/task_store_core.py:801).

```python
        reset_count = 0
        reset_tasks: list[Task] = []
        for stale_status in (TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS):
            for task in list(self._by_status.get(stale_status, {}).values()):
                snapshot = self._claim_snapshot(task)
                self._index_remove(task)
                # Use the FSM for the transition so audit/telemetry fire and
                # any illegal jump is caught.  CLAIMED→OPEN and
                # IN_PROGRESS→OPEN are both allow-listed in
                # ``lifecycle.TASK_TRANSITIONS``.
                transition_task(
                    task,
                    TaskStatus.OPEN,
                    actor="task_store",
                    reason="recover_stale_after_restart",
                )
                task.claimed_at = None
                task.claimed_by_session = None
                self._index_add(task)
                self._record_release_receipt(
```

FSM above means Finite State Machine, the rule set that lists which state jumps are legal. When one cluster node leaves, `reopen_tasks_for_node` does the same reset but only for tasks owned by that node id (src/bernstein/core/tasks/task_store_core.py:811). Separately, agents prove they are alive with heartbeats; agents whose heartbeat is too old are listed by `stale_agents` and marked dead by `mark_stale_dead` (src/bernstein/core/tasks/task_store_core.py:3546, src/bernstein/core/tasks/task_store_core.py:3580, src/bernstein/core/tasks/task_store_core.py:3585). A `release` method also exists for a worker that claimed a task but could not start: it returns the task to OPEN without marking it failed and keeps its priority (src/bernstein/core/tasks/task_store_core.py:2696).
## Janitor role
The janitor is the automatic quality checker that verifies completed work (for example file checks, test results, and artifact signals) before a task may close. DONE moves to CLOSED only after janitor verification and merge (src/bernstein/core/tasks/task_store_core.py:2393). When verification fails, the store can reopen the same task from DONE to OPEN and count the cycle in `metadata['janitor_reopen_count']` so the loop is bounded (src/bernstein/core/tasks/task_store_core.py:2650). The orchestrator side applies the verdict in `_apply_janitor_verdict_action`: pass means do nothing, fail means reopen under the same id while budget remains, and fail with no budget left means permanently fail the task (src/bernstein/core/tasks/task_lifecycle.py:5173). The default budget is 2 reopen cycles and can be overridden with an environment variable (src/bernstein/core/tasks/task_lifecycle.py:5133).

```python
    server_url: str | None = getattr(orch._config, "server_url", None)
    if not server_url:
        logger.warning(
            "janitor_verdict_action: task=%s verdict=FAIL action=skip reason=no_server_url",
            task.id,
        )
        return

    max_cycles = _janitor_reopen_max()
    prior_cycles = int(task.metadata.get("janitor_reopen_count", 0) or 0)

    if prior_cycles < max_cycles:
        cycle = prior_cycles + 1
        try:
            resp = orch._client.post(
                f"{server_url}/tasks/{task.id}/reopen",
                json={"reason": f"janitor verification failed (reopen cycle {cycle}/{max_cycles})"},
            )
            resp.raise_for_status()
```

A merge failure that is not a conflict uses the same bounded budget and the same counter, so broken merges also terminate instead of burning workers forever (src/bernstein/core/tasks/task_lifecycle.py:5267).
## Checkpoint retry
Checkpoint retry decides whether a retry resumes the old session (warm), branches a new session from the old checkpoint (fork), or restarts from zero (cold). The retry modes are defined as warm, fork, and cold (src/bernstein/core/tasks/checkpoint_retry.py:77). Checkpoints are stored as rows in the task event journal, and the decision function is pure: the same inputs always give the same byte-identical decision plus a stable decision hash (src/bernstein/core/tasks/checkpoint_retry.py:425). The safety rule is a workspace hash comparison: before any warm resume, the recorded hash is compared with the live worktree, and a mismatch forces cold because the old session can no longer be trusted (src/bernstein/core/tasks/checkpoint_retry.py:446). Every decision is also recorded to the journal and mirrored into the Hash-based Message Authentication Code (HMAC) audit chain, so replay can tell warm and cold retries apart (src/bernstein/core/tasks/checkpoint_retry.py:27).

```python
    downgrade_reason = ""
    if force_cold:
        effective = RetryMode.COLD
        downgrade_reason = "fresh_context_restart"
    elif requested is RetryMode.COLD:
        effective = RetryMode.COLD
    elif checkpoint is None:
        effective = RetryMode.COLD
        downgrade_reason = "no_checkpoint"
    elif not checkpoint.session_id:
        effective = RetryMode.COLD
        downgrade_reason = "no_session_id"
    elif capability is CheckpointRetryCapability.NONE:
        effective = RetryMode.COLD
        downgrade_reason = "adapter_capability_none"
    elif not workspace_match:
        effective = RetryMode.COLD
        downgrade_reason = "workspace_hash_mismatch"
    elif requested is RetryMode.FORK and capability is not CheckpointRetryCapability.FORK:
        effective = RetryMode.WARM
        downgrade_reason = "fork_downgraded_to_warm"
    else:
        effective = requested
```

Warm and fork retries send only a fixed template filled with the failed gate name and output, never free text, so the new input stays auditable and short (src/bernstein/core/tasks/checkpoint_retry.py:90). A cold retry resends the full prompt (src/bernstein/core/tasks/checkpoint_retry.py:543). A task pinned to fresh-context restarts is forced cold so the two contracts never fight (src/bernstein/core/tasks/task_lifecycle.py:494). The retry budget itself is capped: the effective limit is the smallest of the per-task limit, the reason-based dynamic limit, and a hard cap of 2 regular retries (src/bernstein/core/tasks/task_lifecycle.py:120, src/bernstein/core/tasks/task_lifecycle.py:1187).

```python
    # source of truth is ``task.retry_count`` (typed field).
    retry_count = task.retry_count
    per_task_limit = task.max_retries if task.max_retries > 0 else max_task_retries
    # Bug 2 hard ceiling (see _MAX_REGULAR_TASK_RETRIES docstring above):
    # applies to every lineage regardless of task.max_retries or the
    # reason-derived dynamic_limit, so a structurally-dead task (e.g. its
    # agent keeps dying for an environment reason no retry can fix) burns at
    # most 2 retries before permanent failure instead of riding whatever
    # higher ceiling those other two knobs would otherwise allow.
    effective_limit = min(per_task_limit, dynamic_limit, _MAX_REGULAR_TASK_RETRIES)
```

The reason-based limit gives transient failures (such as rate limits or timeouts) up to 3 retries and fatal failures (such as syntax errors) 0 retries (src/bernstein/core/tasks/task_lifecycle.py:870).
## Dead-letter queue
The DLQ holds tasks that used up all retries instead of dropping them silently. Entries live in a JSONL file under `.sdd/runtime/dlq.jsonl` (src/bernstein/core/tasks/dead_letter_queue.py:144). Each entry keeps the task id, title, role, reason, retry count, last error, timestamps, and extra context such as model and scope (src/bernstein/core/tasks/dead_letter_queue.py:37). The `enqueue` method creates the entry, appends it to the file, and logs it (src/bernstein/core/tasks/dead_letter_queue.py:180).

```python
    def enqueue(
        *,
        task_id: str,
        title: str,
        role: str,
        reason: str,
        retry_count: int = 0,
        original_error: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> DLQEntry:
        """Add a permanently failed task to the dead letter queue.

        Args:
            task_id: Original task ID.
            title: Task title.
            role: Task role.
            reason: Why the task was permanently failed.
            retry_count: Number of retries before DLQ.
            original_error: Last error from the final attempt.
            metadata: Additional context.

        Returns:
            The created DLQ entry.
        """
        self._ensure_loaded()
        entry = DLQEntry(
```

Operators can list entries (newest first, with role and pending filters), read one entry, see counts by role and reason, and replay an entry, which creates a new task with the same title and role and marks the entry replayed (src/bernstein/core/tasks/dead_letter_queue.py:228, src/bernstein/core/tasks/dead_letter_queue.py:269, src/bernstein/core/tasks/dead_letter_queue.py:327). The retry path writes to the DLQ only when a work directory is given; without one it keeps the older plain-failure behavior, and any DLQ write error is logged but never blocks the failure path (src/bernstein/core/tasks/task_lifecycle.py:915). A task that reaches the DLQ is also forwarded to the operator error sink (src/bernstein/core/tasks/task_lifecycle.py:886).
## Failed-task routing to a different model
Verified in source. Retries escalate along a model ladder of haiku to sonnet to opus and an effort ladder of low to medium to high to max (src/bernstein/core/tasks/task_lifecycle.py:379). The step function returns the next ladder rung and leaves unknown model names unchanged so a provider alias is never swapped for a wrong tier name (src/bernstein/core/tasks/task_lifecycle.py:403).

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
    model_lower = current_model.lower()
    for i, name in enumerate(_MODEL_LADDER):
        if name in model_lower:
            return _MODEL_LADDER[min(i + 1, len(_MODEL_LADDER) - 1)]
    return current_model
```

The retry policy picks model and effort from the failure type: the first retry only raises effort, while the second and later retries escalate the model and reset effort to high (src/bernstein/core/tasks/task_lifecycle.py:565). Large-scope tasks, architect and security roles, and tasks past their deadline go straight to the strongest model with max effort (src/bernstein/core/tasks/task_lifecycle.py:481).

```python
    if task.scope == _Scope.LARGE or task.role in ("architect", "security"):
        return _model("opus"), "max"

    if task.deadline is not None and time.time() > task.deadline:
        return _model("opus"), "max"

    if next_retry == 1:
        return _model(current_model), _bump_effort(current_effort)

    # Second+ retry: escalate model, reset effort to high
    return _model(_escalate_model(current_model)), "high"
```

An operator-fixed model always wins: a per-role pin or a run-level `--model` flag is carried through every retry unchanged, while effort may still rise (src/bernstein/core/tasks/task_lifecycle.py:420, src/bernstein/core/tasks/task_lifecycle.py:446). The retry also doubles the budget when the last attempt hit the budget cap and waits longer between tries with capped backoff (src/bernstein/core/tasks/task_lifecycle.py:646).
## Suspension
Suspension parks a task mid-session: the worker gives up its machine resources but the task stays resumable from a verified record instead of restarting from zero. The SUSPENDED state marks such tasks (src/bernstein/core/tasks/models.py:199). Parking follows a fixed order that is never reordered: hash the worktree, append the suspend row to the journal, record the suspend receipt before any release, release process and budget resources against that receipt, then persist the suspended transition so it survives a restart (src/bernstein/core/tasks/suspension.py:1000).

```python
    """Durably park ``task_id``: row, receipt, releases, then ledger.

    The order is load-bearing and never reordered:

    1. Compute the workspace hash over the worktree.
    2. Append the suspend row to the task journal (its ``event_hash`` is the
        suspension's identity).
    3. Record the ``task.suspend_receipt`` binding that hash **before any
        effect**.
    4. Release the process, sandbox, seat, and envelope headroom -- each
        referencing the receipt hash, each refused without it.
    5. Persist the ``task.suspended`` transition to the work ledger so the park
        survives an orchestrator restart.
```

Resume checks the receipt and journal before restarting work, and some resumes need human approval first (src/bernstein/core/tasks/suspension.py:1178, src/bernstein/core/tasks/suspension.py:1231). Suspension differs from release (which simply returns a not-yet-started task to OPEN, src/bernstein/core/tasks/task_store_core.py:2696) and from fail (which ends the task as FAILED and notifies dependents, src/bernstein/core/tasks/task_store_core.py:2437).
**Covers:** src/bernstein/core/tasks/models.py, src/bernstein/core/tasks/claim.py, src/bernstein/core/tasks/task_claim.py, src/bernstein/core/tasks/task_store_core.py, src/bernstein/core/tasks/task_lifecycle.py, src/bernstein/core/tasks/checkpoint_retry.py, src/bernstein/core/tasks/dead_letter_queue.py, src/bernstein/core/tasks/suspension.py, tests/unit/test_task_claiming_by_session.py
