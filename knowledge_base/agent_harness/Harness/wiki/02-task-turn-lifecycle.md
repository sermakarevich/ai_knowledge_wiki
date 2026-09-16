> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Task, Thread, and Turn Lifecycle
**In one sentence:** Harness models agent work as a `Thread` of `Turn`s (single agent-loop iterations) driven by leased `RuntimeJob`s claimed by `RuntimeWorker`s, with a periodic GitHub-state reconciler and startup workspace/lease reconciliation recovering crashed workers.
## Key points
- A `Thread` (project-scoped container with `turns`, status `idle`/`active`/`archived`) advances through `Turn`s (one agent-loop iteration each: `running` → `completed`/`cancelled`/`failed`, carrying `items`, token usage, and timing), defined in `crates/harness-core/src/types.rs:81-90,150-169`.
- The durable unit of execution is a `WorkflowInstance` plus its `RuntimeJob` rows (`pending`/`running`/terminal), not the in-memory `Thread`; a worker turn is one claimed job executed once via `RuntimeWorker::run_once` (`crates/harness-workflow/src/runtime/worker.rs:80-95`, `crates/harness-workflow/src/runtime/model.rs:521-543`).
- Claiming is lease-based: `RuntimeJob::claim` sets `status=running`, bumps `lease_generation`, and stamps `owner` + `expires_at` (`crates/harness-workflow/src/runtime/model.rs:590-602`); the claim SQL accepts `pending` jobs or `running` jobs whose `data.lease.expires_at` has passed, so a dead worker's job becomes reclaimable on expiry (`crates/harness-workflow/src/runtime/job_claim.rs:90-100,168-200`).
- Lease health is tri-state (`active_leased` / `expired_lease` / `missing_lease`) computed from `job.status` and `lease.expires_at` (`crates/harness-workflow/src/runtime/lease_state.rs:6-36`); the worker renews mid-execution at half-TTL intervals and, on losing the lease, cancels the agent and dead-letters the result instead of committing it (`crates/harness-workflow/src/runtime/worker.rs:245-310,168-207`).
- The periodic reconciler (timer loop with 15 s init delay, then every `interval_secs`) does not drive turns: it only closes the gap with external GitHub truth for non-terminal `github_issue_pr` workflows (`done` on merged, `cancelled` on closed) and raises `ready_to_merge` aging alerts (`crates/harness-server/src/reconciliation.rs:174-252`, `crates/harness-server/src/reconciliation_periodic.rs:6-43`).
- Startup recovery is workspace- and host-centric: `reconcile_startup` releases foreign orphaned leases, preserves directories with live persisted leases, and deletes terminal/orphan workspaces (`crates/harness-server/src/workspace_reconcile.rs:57-121`); host/pool topology is restored from the `runtime_state` snapshot keyed by `store_key`, rejecting schema mismatches (`crates/harness-server/src/runtime_state_store.rs:194-246`); host liveness itself is heartbeat-derived (`now - last_heartbeat_at <= heartbeat_timeout_secs`, default 60 s) in `crates/harness-server/src/runtime_hosts.rs:8-10,223-234`.
- Terminal states are definition-scoped: `WorkflowTerminalState` is only `succeeded`/`failed`/`cancelled` (`crates/harness-workflow/src/runtime/state_registry.rs:37-41`), mapped per definition (e.g. `github_issue_pr/done` → `Succeeded`); `WorkflowCommandStatus` further distinguishes `completed`/`failed`/`blocked`/`cancelled`/`skipped`/`superseded`/`handled_inline` (`crates/harness-workflow/src/runtime/status.rs:4-52`), and `is_terminal` consults the definition registry (`crates/harness-workflow/src/runtime/model_workflow_instance.rs:31-37`).
- GC (garbage-collector agent, not git-gc) signals are derived aggregates over the `Event` log — `RepeatedWarn`, `ChronicBlock`, `HotFiles`, `SlowSessions`, `WarnEscalation`, `LinterViolations` — plus mapped external GitHub payloads (CI failure → `ChronicBlock`, `changes_requested` → `RepeatedWarn`), feeding Guard/Rule/Hook/Skill remediation (`crates/harness-gc/src/signal_detector.rs:20-47`, `crates/harness-core/src/types.rs:321-349`).
---
## The lifecycle model
Work exists at three levels. `Thread`/`Turn` in `crates/harness-core/src/types.rs:81-169` is the conversation model: a thread holds an ordered `turns` list and a `ThreadStatus`; each turn holds `items` (`UserMessage`, `AgentReasoning`, `ShellCommand`, `FileEdit`, `FileRead`, `ToolCall`, `ApprovalRequest`, `Error`), an `agent_id`, and `TurnStatus`. Separately, `RunId`/`RunIdentity` (`ar-` + 26-char lowercase ULID, propagated via `AGENT_RUN_ID`/`AGENT_RUN_PARENT`) in `crates/harness-core/src/run_id.rs:6-16,100-151` tracks process lineage, and `BindingRecord` in `crates/harness-core/src/run_registry.rs:19-29` binds a run to its native agent id, pid, and cwd in a rotating JSONL registry. The schedulable unit on the server is the `WorkflowInstance` (definition + state + data) with child `RuntimeJob`s; the worker-facing "turn" is one job claim executed to an `ActivityResult` and committed, with a `RuntimeTurnStarted` event counted against `RuntimeProfile.max_turns` so a workflow has a bounded turn budget (`crates/harness-workflow/src/runtime/worker.rs:378-431`).
## Turn execution
`RuntimeWorker::run_once` (`crates/harness-workflow/src/runtime/worker.rs:80-95`) claims the next eligible non-remote job for its `owner`, short-circuits when the parent workflow is already terminal (`terminal_workflow_result`, `crates/harness-workflow/src/runtime/worker.rs:217-243`), reserves the turn budget, executes via the `RuntimeJobExecutor`, then commits through `commit_runtime_activity_completion_with_transcript_if_owned`. Renewal runs concurrently at `clamp(ttl/2, 1s, 30s)` via `extend_runtime_job_lease_if_owned` (`crates/harness-workflow/src/runtime/worker.rs:245-310`). If the commit finds the lease lost, the result is written to the dead-letter table (`record_lease_expired_completion`) so a later reconciler can decide whether it still applies, and the worker returns `None` rather than double-applying (`crates/harness-workflow/src/runtime/worker.rs:168-207`).
## Reconciliation
Timer-driven reconciliation (`crates/harness-server/src/reconciliation_periodic.rs:17-43`) calls `run_once_with_runtime_config` (`crates/harness-server/src/reconciliation.rs:125-172`), which collects non-terminal `github_issue_pr` instances that reference a PR or issue number (`crates/harness-server/src/reconciliation_runtime.rs:3-59`), resolves each against the GitHub API under a per-minute rate limit (`crates/harness-server/src/reconciliation_runtime.rs:61-85`), and applies `done`/`cancelled` transitions or `ready_to_merge` age alerts (`crates/harness-server/src/reconciliation.rs:186-287`). It is explicitly non-destructive and stateless: terminal rows are skipped, young `ready_to_merge` rows are skipped, and failed applies surface as `reconciliation_anomaly` alerts rather than retries (`crates/harness-server/src/reconciliation_periodic.rs:50-91`).
## Restart and crash recovery
There is no live "reconcile on startup" for workflow instances; recovery is lease-expiry-driven plus workspace/host restore. A crashed worker simply stops renewing; its `running` job matches the expired-lease branch of the claim query and is reclaimed with `lease_generation + 1`, emitting `RuntimeJobReclaimed` for remote-host jobs (`crates/harness-workflow/src/runtime/job_claim.rs:90-100,199-235`). Host liveness is heartbeat-based with `Active`/`Draining` lifecycle (`crates/harness-server/src/runtime_hosts.rs:142-234`). On boot, `reconcile_startup` first releases foreign orphaned workspace leases, then preserves any directory with a live persisted lease (failing closed on lookup error) and removes orphan/terminal/generation-drifted workspaces (`crates/harness-server/src/workspace_reconcile.rs:57-160`); the host/project-cache snapshot is reloaded only on exact schema match (`crates/harness-server/src/runtime_state_store.rs:194-226`). GC `SignalDetector` plays no role in crash recovery — it mines the event history for hygiene patterns (repeated warns, chronic blocks, hot files, slow ops, warn escalation, linter violations) that drive the GC remediation agent (`crates/harness-gc/src/signal_detector.rs:20-29,125-257`).

Lease-claim candidate selection (`crates/harness-workflow/src/runtime/job_claim.rs:90-100`):
```sql
WHERE (
    (
        job.status = 'pending'
        AND (job.not_before IS NULL OR job.not_before <= CURRENT_TIMESTAMP)
    ) OR (
        job.status = 'running'
        AND job.data ? 'lease'
        AND (job.data->'lease' ? 'expires_at')
        AND (job.data->'lease'->>'expires_at')::timestamptz <= CURRENT_TIMESTAMP
    )
)
```

Claim + generation bump (`crates/harness-workflow/src/runtime/model.rs:590-602`):
```rust
pub fn claim(&mut self, owner: impl Into<String>, expires_at: DateTime<Utc>) {
    self.status = RuntimeJobStatus::Running;
    self.lease_generation = self.lease_generation.saturating_add(1);
    self.renew_lease(owner, expires_at);
}

pub fn renew_lease(&mut self, owner: impl Into<String>, expires_at: DateTime<Utc>) {
    self.lease = Some(WorkflowLease {
        owner: owner.into(),
        expires_at,
    });
    self.updated_at = Utc::now();
}
```
**Covers:** crates/harness-core/src/types.rs, crates/harness-core/src/run_id.rs, crates/harness-core/src/run_registry.rs, crates/harness-server/src/reconciliation.rs, crates/harness-server/src/reconciliation_runtime.rs, crates/harness-server/src/reconciliation_periodic.rs, crates/harness-server/src/runtime_state_store.rs, crates/harness-server/src/runtime_hosts.rs, crates/harness-server/src/workspace_reconcile.rs, crates/harness-workflow/src/runtime/job_claim.rs, crates/harness-workflow/src/runtime/lease_state.rs, crates/harness-workflow/src/runtime/worker.rs, crates/harness-workflow/src/runtime/model.rs, crates/harness-workflow/src/runtime/model_workflow_instance.rs, crates/harness-workflow/src/runtime/status.rs, crates/harness-workflow/src/runtime/state_registry.rs, crates/harness-workflow/src/runtime/terminal_state.rs, crates/harness-gc/src/signal_detector.rs
