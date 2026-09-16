> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Workflow Runtime and Worktree Isolation
**In one sentence:** GitHub issues enter via a submissions API that builds planning or implementation decisions, which the dispatcher gates on budget, isolation, and profile policy before claiming, enqueueing, and executing them as leased runtime jobs in per-task git worktrees subject to validator and quality-gate checks.
## Key points
- Submissions API (`runtime/submission.rs:62`) maps an issue to one of three actions — `RunPlanning`, `RunImplementation`, `WaitForDependencies` (`runtime/submission.rs:34-39`) — emitting an `EnqueueActivity` command for `implement_issue` or the plan activity plus a `task_submission` evidence record.
- `ExecPlan` (`harness-exec/src/plan.rs:6-19`) is the plan data model: `purpose`, `project_root`, `progress` milestones, `concrete_steps`, `decision_log`, `surprises`, `validation` criteria, and `status`, constructed by `from_spec` (`harness-exec/src/plan.rs:56-78`) and mutated by `activate`, `add_milestone`, `add_step`, `log_decision`, `complete`, `abandon`.
- Dispatch is claim-then-gate-then-enqueue in `RuntimeCommandDispatcher::dispatch_command` (`runtime/dispatcher.rs:178-346`): skip non-runtime commands, drop terminal workflows, resolve effective profile, enforce agent-contract and isolation availability, apply the budget gate, then `enqueue_runtime_job_for_claimed_command` with `AlreadyDispatched` dedupe on `dedupe_key`.
- Profile selection (`runtime/dispatcher_profile_selector.rs:56-68`) resolves workflow-activity > activity > workflow > default; `effective_profile_for_command` (`runtime/dispatcher.rs:139-147`) layers eval policy and candidate-budget rewrites on top before the same profile is rechecked at enqueue.
- Throttling and budgets live in `budget_gate_outcome` (`runtime/dispatcher.rs:370-462`) with `daily_throttle_breach` (`runtime/dispatcher_throttle.rs:38-85`): workflow-budget exhaustion, per-profile daily caps, and a throttle band that yields to an under-threshold alternative profile (via `peek_claimable_commands`) rather than starving a lone busy profile; shadow mode records `BudgetShadowDecision` and dispatches, enforce mode defers with a barrier.
- Concurrency is bounded at two layers: `TaskQueue` holds a global `PriorityPermitQueue` plus per-project queues requiring both permits (`harness-server/src/task_queue/mod.rs:222-248`), and `WorkspacePool::acquire_with_capacity` (`harness-server/src/workspace_pool.rs:91-114`) issues per-project semaphore permits keyed by `project_limit_key` (`harness-server/src/workspace_pool.rs:141-154`) with default capacity 4 (`harness-server/src/workspace_pool.rs:8`).
- Each task executes in an isolated git worktree: `WorkspaceManager` creates `config.root/<sanitized_task_id>` from `remote/base_branch` on branch `harness/<task_id>` (`harness-server/src/workspace_create.rs:8-13`), verified by `is_registered_worktree` and removed by `remove_worktree` (`harness-server/src/workspace_helpers.rs:201,478`), with orphan reclamation (`harness-server/src/workspace_reconcile.rs:504-542`) and `WORKFLOW.md:14-18` declaring `strategy: worktree`, `branch_prefix: harness/`, `cleanup: on_terminal`.
- Validators and quality gates close the loop: `TransitionRule` (`runtime/validator.rs:31-40`) constrains allowed and required commands and evidence per state transition, `build_quality_gate_run_decision` (`runtime/quality_gate.rs:36-73`) enqueues `run_quality_gate` with explicit `validation_commands`, and `WORKFLOW.md:75-89` binds `implement_issue` to `cargo fmt --check`, `cargo check`, `cargo test`, and `clippy -D warnings`.
---
## Submissions API
`CreateTaskRequest` (`harness-server/src/workflow_runtime_submission/runtime_request.rs:15-80`) carries `definition_id`, `prompt`, `issue`, `pr`, `force_execute`, `skip_triage`, `project`, `repo`, `labels`, and priority capped by `MAX_TASK_PRIORITY` (`harness-server/src/workflow_runtime_submission/runtime_request.rs:12`). Issue intake funnels into `build_issue_submission_decision` (`runtime/submission.rs:62-145`): `dependencies_blocked` yields `awaiting_dependencies` with no command; `force_execute` yields `implementing` plus an `implement_issue` command gated by `uncovered_issue_ready_for_implementation`; the default yields `planning` plus the plan-activity command gated by `dependency_analysis_required`. Both paths attach `remote_fact_hash`, `submission_mode` (`Immediate`/`Deferred`, `runtime/submission.rs:9-32`), and candidate-fanout variants via `append_candidate_commands` / `candidate_dedupe_key` (`runtime/submission.rs:147-190`). Instances themselves are `WorkflowInstance` records (`runtime/model.rs:76-98`) created by `WorkflowInstance::new` (`runtime/model_workflow_instance.rs:8-29`); declarative definitions are compiled by `build_declarative_definition` (`runtime/declarative.rs:83-107`) and entered via `build_declarative_submission_decision` (`runtime/declarative_interpreter.rs:8-44`). Project-level progress is tracked separately by `ProjectWorkflowState` (`project_lifecycle.rs:62-73`) and issue-level progress by `IssueLifecycleState` (`issue_lifecycle.rs:17-34`).

```rust
pub fn build_issue_submission_decision(
    instance: &WorkflowInstance,
    input: IssueSubmissionDecisionInput<'_>,
) -> IssueSubmissionDecisionOutput {
    let action = if input.dependencies_blocked {
        IssueSubmissionWorkflowAction::WaitForDependencies
    } else if input.force_execute {
        IssueSubmissionWorkflowAction::RunImplementation
    } else {
        IssueSubmissionWorkflowAction::RunPlanning
    };
    let next_state = if input.dependencies_blocked {
        "awaiting_dependencies"
    } else if input.force_execute {
        "implementing"
    } else {
        "planning"
    };
    let reason = if input.dependencies_blocked {
        "operator submitted the GitHub issue and it is waiting for dependencies"
    } else if input.force_execute {
```

## ExecPlan
```rust
pub struct ExecPlan {
    pub id: ExecPlanId,
    pub purpose: String,
    pub project_root: PathBuf,
    pub progress: Vec<Milestone>,
    pub concrete_steps: Vec<Step>,
    pub decision_log: Vec<PlanDecision>,
    pub surprises: Vec<Surprise>,
    pub validation: ValidationCriteria,
    pub status: ExecPlanStatus,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
```
`harness-exec` is a two-module crate (`harness-exec/src/lib.rs:1-2`: `markdown`, `plan`). `ExecPlan::from_spec` derives `purpose` from the first `#` heading or falls back to `"Untitled Plan"` (`harness-exec/src/plan.rs:56-78`); lifecycle methods `activate`, `update_milestone`, `add_milestone`, `add_step`, `log_decision`, `log_surprise`, `complete`, `abandon` (`harness-exec/src/plan.rs:80-137`) stamp `updated_at` on every mutation. Markdown serialization (`to_markdown` / `from_markdown`, `harness-exec/src/plan.rs:140-147`) provides cross-session recovery, covered by round-trip tests (`harness-exec/src/plan.rs:150-204`).

## Dispatch and permits
`dispatch_pending` claims up to `batch_limit` (default 25, `runtime/dispatcher.rs:56-78,100-103,162-176`) via `claim_pending_commands`; `dispatch_once` claims one (`runtime/dispatcher.rs:149-160`). Deferred commands carry a `DispatchBarrier` with exponential backoff (floor 30s, ceiling 15m, `runtime/dispatch_barrier.rs:5-53`) and reason codes for disabled policy, invalid config, unavailable isolation tier, budget exhaustion, daily cap, and throttle (`runtime/dispatch_barrier.rs:55-79`). Deferral is ownership-checked in `defer_claimed_command_if_owned` (`runtime/dispatch_barrier.rs:235-422`) and always requires a project identity via `command_project_id` (`runtime/dispatcher.rs:517-529`). Execution is lease-based: `RuntimeWorker` (`runtime/worker.rs:50-78`) claims jobs through `RuntimeJobExecutor::execute` (`runtime/worker.rs:13-30`) with a `before_execute` claim guard (`runtime/worker.rs:41-48`). Store persistence is split across `store/` submodules wired in `runtime/store.rs:25-60`. `WORKFLOW.md:34-49` sets the operational defaults: dispatch every 30s with batch 32, worker interval 5s with concurrency 8 and 600s leases, up to 6 activity retries.

## Worktree isolation
`WORKFLOW.md:14-18` fixes `workspace.strategy: worktree` with `reuse_existing_workspace: true` and `cleanup: on_terminal`. At runtime the server resolves the main worktree by walking up from the task directory (`harness-server/src/workflow_runtime_submission/runtime_request.rs:327-378: detect_main_worktree`, `find_main_worktree_from`), creates the per-task linked worktree from the remote head, and tracks registration through `git worktree list --porcelain` (`harness-server/src/workspace_helpers.rs:461-499`). Failure paths clean partial worktrees after add, owner-record, or hook errors (`harness-server/src/workspace_create.rs:604-756`); stale entries are pruned and orphan directories reclaimed (`harness-server/src/workspace_helpers.rs:404-434`, `harness-server/src/workspace_reconcile.rs:689-742`). The legacy issue store retains a `list_with_worktree_project_ids` query for rows whose `project_id` still points at an isolated worktree (`harness-workflow/src/issue_workflow_store/maintenance.rs:7-8`).

## Validators
Every `WorkflowDecision` passes `validator.rs` allowlists (`TransitionRule::matches`, `runtime/validator.rs:74-80`) plus command rules, evidence contracts, and per-definition checks (`runtime/validator.rs:11-25`: `validator_command_rules`, `validator_evidence`, `validator_github_issue_pr`, `validator_hidden_transitions`, `validator_prompt_task`). Quality gates are first-class workflows: `quality_gate_workflow_id` (`runtime/quality_gate.rs:32-34`) scopes a gate per project and subject, and completion feeds back through the reducer and terminal-state helpers (`runtime/model_workflow_instance.rs:31-48`, `runtime/store.rs` activity-completion modules). The prompt contract in `WORKFLOW.md:92-125` reinforces the loop: work only inside the admitted workspace, confirm the issue signal, run scoped validation, push a PR, and report blockers in a `harness-activity-result` block.
**Covers:** crates/harness-exec/src/lib.rs, crates/harness-exec/src/plan.rs, crates/harness-workflow/src/runtime/submission.rs, crates/harness-workflow/src/runtime/dispatcher.rs, crates/harness-workflow/src/runtime/dispatcher_throttle.rs, crates/harness-workflow/src/runtime/dispatcher_profile_selector.rs, crates/harness-workflow/src/runtime/dispatch_barrier.rs, crates/harness-workflow/src/runtime/model.rs, crates/harness-workflow/src/runtime/model_workflow_instance.rs, crates/harness-workflow/src/runtime/declarative.rs, crates/harness-workflow/src/runtime/declarative_interpreter.rs, crates/harness-workflow/src/runtime/store.rs, crates/harness-workflow/src/runtime/validator.rs, crates/harness-workflow/src/runtime/quality_gate.rs, crates/harness-workflow/src/runtime/worker.rs, crates/harness-workflow/src/issue_lifecycle.rs, crates/harness-workflow/src/project_lifecycle.rs, crates/harness-workflow/src/issue_workflow_store/maintenance.rs, crates/harness-server/src/workspace_create.rs, crates/harness-server/src/workspace_helpers.rs, crates/harness-server/src/workspace_reconcile.rs, crates/harness-server/src/workspace_pool.rs, crates/harness-server/src/task_queue/mod.rs, crates/harness-server/src/workflow_runtime_submission/runtime_request.rs, WORKFLOW.md
