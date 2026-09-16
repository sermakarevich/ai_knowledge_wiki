---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]]
# Retrieval Practice: Harness
Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.
### Q1. What is Harness's central design bet, and what concretely separates its control plane from its data plane?
> [!tip]- Answer
> Harness bets on a persistent central control plane: an Axum HTTP server backed by Postgres 16 holding all durable state, with thin executor adapters (Claude Code, Codex) running outside the request path. Control-plane writes use REST routes while agent-plane calls use JSON-RPC on `/rpc` behind an initialize handshake, explicitly excluding task submission. The server defaults to `127.0.0.1:9800` with an 8-connection, 10 s acquire-timeout pool. See [[wiki/01-overview-architecture|Overview Architecture]].
### Q2. How does lease-based RuntimeJob claiming, renewal, and loss handling work?
> [!tip]- Answer
> `RuntimeJob::claim` sets `status=running`, bumps `lease_generation`, and stamps `owner` plus `expires_at`, while the claim SQL accepts `pending` jobs or `running` jobs whose `lease.expires_at` has passed so dead workers become reclaimable. The worker renews at half-TTL intervals and checks ownership before commit. On lease loss it cancels the agent and dead-letters the result instead of committing, preventing double-apply. See [[wiki/02-task-turn-lifecycle|Task Turn Lifecycle]].
### Q3. How is the Starlark exec policy expressed, limited, and evaluated?
> [!tip]- Answer
> Policy is three-valued `ExecDecision` (Allow, Prompt, Forbidden) matched as prefixes over tokenized commands, evaluating to the maximum matched severity. Starlark files may call only `prefix_rule` and `host_executable`, with `def`, `lambda`, `load`, and top-level statements disabled, source capped at 512 KiB and stack depth at 512. A second source, `requirements.toml`, converts to the same type but rejects `allow`, merging additively via `merge_overlay`. See [[wiki/03-policy-engine|Policy Engine]].
### Q4. How does the AgentRegistry resolve a name like `claude` to a running backend?
> [!tip]- Answer
> All backends implement `AgentBackend` behind `AgentDescriptor { backend, control_backend, turn_backend_factory }`, with unimplemented control ops defaulting to `Unsupported`. `registry_from_config` registers `claude`, `codex` plus turn factory, `opencode` plus turn factory, and `anthropic-api` only when the API key exists, routing `Critical`/`Complex` tasks to complexity preferences and the rest to the default. Each CLI backend then spawns as a supervised sandboxed child whose JSONL output is parsed by a per-agent streaming parser. See [[wiki/04-agent-adapters|Agent Adapters]].
### Q5. How does a GitHub issue become one executing job in an isolated worktree?
> [!tip]- Answer
> The submissions API maps an issue to `RunPlanning`, `RunImplementation`, or `WaitForDependencies`, emitting an `EnqueueActivity` command plus evidence. The dispatcher runs claim-then-gate-then-enqueue, dropping terminal workflows and checking profile, agent-contract, isolation, and budget gates with `dedupe_key` dedupe. The surviving job executes once as a leased `RuntimeJob` in `config.root/<task>` branched as `harness/<task_id>`, gated by transition rules and quality-gate validation commands. See [[wiki/05-workflow-runtime|Workflow Runtime]].
### Q6. How does Harness observe work and fit skills, rules, and memory into a prompt budget?
> [!tip]- Answer
> One OTLP pipeline exports three signals — per-event traces plus workflow/activity/agent-turn trajectory spans, four counters/histograms, and one log per event — defaulting to disabled with endpoint order config, env var, then `127.0.0.1:4318/4317` plus a reachability probe. Every tool decision is also a Postgres `events` row across eight migrations keyed by `(store_key, id)`. `ContextComposer` then enforces per-class quotas, `dedupe_key` elimination, and degradation levels so P0 items always fit. See [[wiki/07-observability-persistence|Observability Persistence]].
### Q7. Why does the hook enforcer fail open behind a circuit breaker, and what would break if it failed closed?
> [!tip]- Answer
> It passes when disabled, under `CI`, with no guards, with no reported `affected_files`, or on scan failure, returning `Warn` rather than block, because host git inspection is disabled and it depends on agent-reported file lists. The per-session breaker opens after 3 consecutive blocks and auto-passes for 300 s to bound feedback loops. Failing closed would halt benign turns on missing telemetry, spin retry loops, and break CI runs. See [[wiki/03-policy-engine|Policy Engine]].
### Q8. Why is crash recovery lease-expiry-driven rather than startup-replay, and what breaks if renewal is removed?
> [!tip]- Answer
> A crashed worker simply stops renewing, so its `running` job matches the expired-lease branch of the claim query and is reclaimed with `lease_generation + 1` plus a reclaim event, needing no central watchdog. Startup only reconciles workspaces and host snapshots rather than replaying instances. Without concurrent half-TTL renewal and ownership-checked commit, long jobs would be falsely reclaimed and committed twice. See [[wiki/02-task-turn-lifecycle|Task Turn Lifecycle]].
### Q9. Why pair primary-plus-challenger review with staged GC drafts, and what breaks if either gate is skipped?
> [!tip]- Answer
> `Approved` requires an empty consensus set after bounded rounds of `CONFIRMED`/`MISSED`/`FALSE-POSITIVE` verdicts, with `distinct_challenger` id and name checks preventing the same model reviewing itself. GC signals likewise never write directly but persist `Pending` drafts adopted only via path-validated `adopt_if_pending` or `RulesOnly` auto-adoption with TTL expiry. Allowing self-review invites correlated approval, and auto-applying drafts lets noisy hygiene signals mutate the workspace. See [[wiki/06-review-and-gc|Review and GC]].
### Q10. Fleet tracks tasks in beads with supervisor liveness polling. How would you port Harness leases, permits, and isolation to Fleet?
> [!tip]- Answer
> Add `lease_owner`, `lease_expires_at`, and `lease_generation` columns to beads tasks, renew at half-TTL during coder execution, and reclaim via a pending-or-expired-lease predicate with a generation bump. Cap concurrency with two-stage project-then-global semaphores released on drop plus aging so one batch cannot starve small fixes. Run each task in a per-task worktree with sibling do-not-touch prompt blocks. See [[wiki/targeted|Targeted Fleet Lessons]].
### Q11. What is the weakest link in Harness's safety story, and what single change most reduces Fleet's risk if it borrows the design?
> [!tip]- Answer
> The weakest link is enforcement: exec policy is a load-and-query store checked via CLI rather than a per-tool-call interceptor, guards depend on agent-supplied file lists, the enforcer fails open with a 300 s auto-pass window, and the default sandbox is `danger-full-access` passthrough. Borrowing leases, permits, and review without closing this gap leaves execution unconstrained. Fleet should default to `workspace-write`, add an inline pre-spawn policy gate, and verify files independently. See [[wiki/targeted|Targeted Fleet Lessons]].
