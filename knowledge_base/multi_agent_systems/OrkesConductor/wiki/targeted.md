> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Targeted Brief: the Framework, Its Principles, Design Patterns, and Abstractions

*Answers the request behind this entry: "a very detailed summary of the framework and its principles and design patterns and abstractions" for the docs hub at https://www.orkes.io/content/ (tracking params stripped). Synthesized from all six wiki pages; every claim links to its page.*

## 1. The framework in one paragraph

**Orkes Conductor is a durable workflow-orchestration engine**: you declare a multi-step process as a versioned task graph (JSON (JavaScript Object Notation, the definition format) or SDK (Software Development Kit, the language client library) code-first builders), and a central server schedules each step, persists its result before scheduling the next, and enforces per-step retry, timeout, and compensation policy. Business logic runs in external **workers** that poll queues in any language (Java, Python, Go, JavaScript/TypeScript, C#, Ruby, Rust, Clojure); commodity work (HTTP calls, waits, events, inline scripts, LLM calls, human approvals) runs inside the server as **system tasks**. Lineage: Netflix Conductor (Apache 2.0 open source) → Conductor OSS (`conductor-oss/conductor`, Orkes as primary maintainer) → Orkes Conductor (100% compatible commercial distribution: Cloud SaaS, customer-hosted, free Developer Edition). See [[01-overview-and-principles|Overview and Principles]].

## 2. Guiding principles

1. **Durable execution over best-effort chaining.** State is checkpointed after every task, so crashes, deploys, and multi-day waits resume from the next incomplete task. Delivery is at-least-once with a sweeper requeuing silent tasks — which is why workers must be idempotent. See [[02-core-abstractions|Core Abstractions]].
2. **Central orchestration, distributed execution.** The server owns scheduling, retries, timeouts, and state; workers own only business logic and poll over REST/gRPC (REpresentational State Transfer / gRPC Remote Procedure Call framework) with no inbound ports. Routing, retry, and undo logic lives in the versioned definition, not scattered across services. See [[01-overview-and-principles|Overview]].
3. **One substrate for services and agents.** An LLM call (`LLM_CHAT_COMPLETE`), a tool call (`CALL_MCP_TOOL` over MCP (Model Context Protocol, the tool-calling standard)), a vector search, a human approval (`HUMAN`), and an HTTP call are all ordinary tasks with identical retry, persistence, and audit semantics. Model output is treated as a *proposal*: the workflow validates it, gates writes with guardrails and approvals, and persists every turn. See [[06-agents-and-ai-orchestration|Agents]].
4. **Events at the edges, orchestration at the core.** API/SDK starts, cron schedules, verified webhooks, broker event handlers (Kafka, NATS, AMQP, SQS), and direct signals all create or advance the same execution model; gateways expose workflows outward as REST routes or MCP tools. Pure choreography (services reacting to each other with no controller) is deliberately replaced by observable orchestration. See [[04-event-driven-and-integrations|Event-Driven]].
5. **Explicit failure policy, no distributed transactions.** Every task declares retries, timeouts, and terminal-error behavior; cross-service rollback is the **saga pattern** — a `failureWorkflow` that receives the failed execution and runs undo steps in reverse, idempotently. See [[05-design-patterns|Design Patterns]].
6. **Version-pinned evolution.** Definitions carry integer versions; each execution pins its start-time snapshot. Roll out by registering a new version and moving callers; in-flight runs drain unless deliberately terminated and restarted with latest definitions. See [[05-design-patterns|Design Patterns]].

## 3. Core abstractions

| Abstraction | What it is | Key fields / behavior |
|---|---|---|
| **Workflow definition** | Versioned blueprint: the task graph plus data wiring and failure policy | `name`, `version`, `schemaVersion: 2`, `tasks`, `inputParameters`, `outputParameters`, `variables`, `inputTemplate`, `failureWorkflow`, `timeoutSeconds` + `timeoutPolicy`, `enforceSchema` |
| **Workflow execution** | One durable run of a definition, with a unique `workflowId` | Statuses `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `TIMED_OUT`, `TERMINATED`; checkpointed after every task; pausable, resumable, restartable, retryable, terminable |
| **Task** (worker / system / operator) | One step. `SIMPLE` = user code in a worker; system tasks = server built-ins (`HTTP`, `INLINE`, `EVENT`, `WAIT`, `HUMAN`, `JSON_JQ_TRANSFORM`, `KAFKA_PUBLISH`, `JDBC`, `WAIT_FOR_WEBHOOK`, AI tasks…); operators = control flow (`SWITCH`, `FORK_JOIN`, `FORK_JOIN_DYNAMIC`, `DYNAMIC`, `DO_WHILE`, `SUB_WORKFLOW`, `TERMINATE`, `SET_VARIABLE`, `WAIT`, `YIELD`) | Referenced by `taskReferenceName`; input via `inputParameters` *or* `inputExpression` (mutually exclusive); task statuses `SCHEDULED` → `IN_PROGRESS` → `COMPLETED` / `FAILED` / `FAILED_WITH_TERMINAL_ERROR` / `TIMED_OUT` / `CANCELED` / `SKIPPED` / `COMPLETED_WITH_ERRORS` |
| **Worker** | External process running the poll → execute → report loop | Long-polls its task type, runs domain code, posts output + status; scales horizontally; partitioned by task-to-domain routing; throttled by `rateLimitPerFrequency` / `concurrentExecLimit` |
| **Data wiring** | `${...}` expressions evaluated per task | `${workflow.input.x}`, `${taskRef.output.y}`, `${workflow.variables.z}`, run metadata; unresolved references are their own wiring-error class |
| **Reliability policy** | Per-task-definition retry/timeout/caching fields | `retryCount`, `retryLogic` (`FIXED` / `EXPONENTIAL_BACKOFF` / `LINEAR_BACKOFF`), `retryDelaySeconds`, `maxRetryDelaySeconds`, `backoffJitterMs`, `responseTimeoutSeconds`, `timeoutSeconds`, `totalTimeoutSeconds`, `timeoutPolicy` (`RETRY` / `TIME_OUT_WF` / `ALERT_ONLY`), `optional`, `cache` + `cacheKeyTemplate` + `cacheTTLSeconds` |
| **Event handler** | "When this outside signal arrives, start or advance a run" | Matches `event` + `condition`, fires `start_workflow` or `complete_task` (needs concrete `workflowId` + `taskRefName`) |
| **Agent** (`AGENT` task) | A deployed Conductor Agent or remote A2A agent invoked as a durable step | Authored declaratively (AI tasks), as code compiled to graphs, or brought from frameworks (LangChain, ADK); governed by guardrails, evals, HITL (human-in-the-loop), failure semantics |

Details and worked examples: [[02-core-abstractions|Core Abstractions]], [[03-operators-and-system-tasks|Operators and System Tasks]].

## 4. Design patterns (problem → mechanism)

1. **Microservice orchestration** — chain services with sequential `HTTP`/`SIMPLE` tasks, pass data via `${taskRef.output…}`, branch with `SWITCH`. The recipe replaces point-to-point call chains.
2. **Static fan-out/fan-in** — `FORK_JOIN` with fixed `forkTasks` branches + `JOIN` collecting results (e.g. credit score, history, tickets concurrently).
3. **Dynamic parallelism** — `FORK_JOIN_DYNAMIC` when branch count is known only at runtime: different tasks per branch (`dynamicTasks`), same task over many inputs (`forkTaskName` + `forkTaskInputs`), or parallel sub-workflows (`forkTaskWorkflow`); always ends with `JOIN`.
4. **Wait and timers** — `WAIT` with `duration`, `until`, or bare (block until signaled); resume via signal API, event-handler `complete_task`, or task-update; `HUMAN` and `WAIT_FOR_WEBHOOK` cover approval and verified-callback variants.
5. **Timeouts and retries** — backoff strategy per failure shape (exponential + cap + jitter for rate-limited APIs; heartbeats + long timeout for long jobs; `totalTimeoutSeconds` for SLAs); `FAILED_WITH_TERMINAL_ERROR` skips retries for deterministic failures; `optional: true` lets the run continue past non-critical failures.
6. **Saga and compensation** — `failureWorkflow` reads `failedWorkflow.tasks`, gates each undo on what actually completed, and runs compensating tasks in reverse with their own retries and idempotency keys. Compensation is a new transaction (refund ledger entry), not a rollback.
7. **Polling long-running jobs** — one `HTTP_POLL` task (`terminationCondition`, `pollingInterval`, `pollingStrategy`, `maxPollCount`) instead of a hand-built poll loop; submit step needs an idempotency key.
8. **Scheduled workflows** — scheduler objects (`cronExpression`, `zoneId`, `runCatchupScheduleInstances`, window bounds); no native overlap policy, so design for concurrency or serialize externally.
9. **Dynamic workflows in code** — SDK builders (`ConductorWorkflow`, `>>` chaining, `SwitchTask`, `ForkTask`, `DoWhileTask`, …) or fully runtime graphs via inline `workflow_def`; `DYNAMIC` resolves task types late.
10. **Event-driven edges** — `EVENT` publishes to sinks (`kafka:`, `sqs:`, `nats:`, `amqp_*:`); handlers start workflows or complete blocked waits; narrow handler conditions so one event does not spawn a fleet.
11. **Agentic patterns** — RAG (chunk → embed → index → search → chat-complete), MCP tool calling (`LIST_MCP_TOOLS` / `CALL_MCP_TOOL`), A2A delegation, multi-agent handoff/scatter-gather, guardrailed LLM steps, HITL approvals, evals on the execution trace, token-efficiency controls. See [[06-agents-and-ai-orchestration|Agents]].

Full mechanics, failure notes, and "when NOT to use" guidance: [[05-design-patterns|Design Patterns]].

## 5. How the pieces fit (one run, end to end)

A starter (API call, schedule tick, event, or parent workflow) creates an **execution** pinning a definition version → the server schedules the first **task** → a **worker** polls, executes, and reports (or a **system task** runs in-server) → outputs flow forward through **`${...}` wiring** → **operators** route (branch, fan out, loop, wait, delegate to sub-workflow or agent) → each step checkpoints; failures run retries/timeouts per policy, terminal failure triggers the **failureWorkflow** saga → **events** flow out (`EVENT` publish, status listener, CDC (Change Data Capture, the production event stream)) and back in (signals, handlers) → the run completes with a full searchable history of every input, output, retry, and worker identity.

## 6. What to remember

- **Definition ≠ execution ≠ worker**: the versioned graph, the durable run, and the poll-based executor are three separate things that evolve and scale independently.
- **Failure handling is declared, not improvised**: retries, timeouts, optional tasks, terminal errors, and compensation workflows are fields in the graph — read them before reading any code.
- **Agents are tasks with guardrails**, not a separate system: the same durability, retry, and audit machinery governs model calls, tool calls, and human approvals.
- **The two sharp edges**: at-least-once delivery means workers must be idempotent; compensation means undo logic must be gated on what actually completed.
