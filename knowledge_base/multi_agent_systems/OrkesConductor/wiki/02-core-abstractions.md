> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Core Abstractions: Workflows, Tasks, Workers
**In one sentence:** Conductor separates a versioned workflow definition (the task graph and data wiring) from workflow executions (durable runs of that graph) and from workers (external poll-based processes that execute `SIMPLE` tasks), while system tasks and operators execute inside the server.
## Key points
- A workflow definition is a versioned JSON document (`name`, `version`, `schemaVersion: 2`, `tasks`, `inputParameters`, `outputParameters`) that can also be generated code-first with SDKs (Software Development Kits) for Java, Python, Go, JavaScript, C#, Ruby, and Rust; when no version is pinned at start time, the highest registered version runs.
- Data flows between tasks through `${...}` expressions evaluated against workflow input, prior task input/output, variables, and workflow metadata -- e.g. `${workflow.input.orderId}`, `${process_payment_ref.output.transactionId}` -- with `inputParameters` (per-key template) and `inputExpression` (whole-object JSONPath (JavaScript Object Notation path query language)) as mutually exclusive options per task.
- Task kinds split into worker tasks (`type: SIMPLE`, custom code run by user-operated workers), system tasks (server-side built-ins such as `HTTP`, `INLINE`, `EVENT`, `WAIT`, `HUMAN`, `KAFKA_PUBLISH`, `JSON_JQ_TRANSFORM`, sub-workflow operators), and operators (control-flow primitives such as `SWITCH`, `FORK_JOIN`, `DO_WHILE`, `SUB_WORKFLOW`, `TERMINATE`, `SET_VARIABLE`); only `SIMPLE` tasks require a registered task definition plus a polling worker, otherwise the task stays queued.
- Task definitions carry reliability policy as explicit fields: `retryCount`, `retryLogic` (`FIXED`, `EXPONENTIAL_BACKOFF`, `LINEAR_BACKOFF`), `retryDelaySeconds`, `maxRetryDelaySeconds`, `backoffScaleFactor`, `timeoutSeconds`, `responseTimeoutSeconds`, `pollTimeoutSeconds`, `totalTimeoutSeconds`, `concurrentExecLimit`, `rateLimitPerFrequency` with `rateLimitFrequencyInSeconds`, output caching (`cache`, `cacheKeyTemplate`, `cacheTTLSeconds`), and `optional` (failure surfaces as `COMPLETED_WITH_ERRORS` instead of failing the workflow).
- Workers implement a three-step loop -- poll a named task queue, execute business logic, report `COMPLETED`/`FAILED` -- over REST/gRPC (REpresentational State Transfer / gRPC Remote Procedure Call framework); scaling is horizontal (more worker processes polling the same task type), throttled by rate and concurrency limits, and partitioned by task-to-domain routing (`taskToDomain` map on start, `domain` property on the worker).
- Execution state is persisted after every task, so runs survive restarts and can span minutes to weeks; workflow statuses are `RUNNING`, `COMPLETED`, `FAILED`, `TIMED_OUT`, `TERMINATED`, `PAUSED`, and task statuses are `SCHEDULED`, `IN_PROGRESS`, `COMPLETED`, `COMPLETED_WITH_ERRORS`, `FAILED`, `FAILED_WITH_TERMINAL_ERROR`, `TIMED_OUT`, `CANCELED`, `SKIPPED`.
- Cross-cutting controls are orthogonal to the graph: idempotent starts via client-supplied `requestId`, input/output JSON-schema (JavaScript Object Notation schema) validation (`enforceSchema`, `validateTaskDefinition`), and mid-run intervention via signals (`signalTaskAsync` / `signalTaskSync` targeting `workflowId` + `taskRefName` or `taskId`), event handlers, `WAIT`/`HUMAN` tasks, and a compensation path through `failureWorkflow` plus `TIME_OUT_WF` vs `ALERT_ONLY` timeout policy.
---
## Workflow definitions
A definition declares the task graph. Top-level fields include `name`, `description`, `version`, `schemaVersion`, `ownerEmail`, `tasks` (ordered array of task configurations), `inputParameters` (declared input keys), `outputParameters` (map from output keys to `${...}` expressions), `variables` (mutable workflow-scoped map written by `SET_VARIABLE`), `inputTemplate` (default input values overridable at start), `failureWorkflow` plus `failureWorkflowVersion` (compensation workflow triggered on `FAILED`, receiving the original input plus `workflowId`, `failureStatus`, `failureTaskId`), `timeoutSeconds` with `timeoutPolicy` (`TIME_OUT_WF` fails and terminates the run, `ALERT_ONLY` records a counter and keeps running), `workflowStatusListenerEnabled` (fan-out of state changes), and `enforceSchema` (reject inputs/outputs that violate the attached schema).
Versions are integers. Breaking changes to inputs, outputs, task order, or failure semantics go in a new `version`; old versions stay runnable so in-flight executions and unmigrated callers keep working. Docs advise pinning the version on start when repeatability matters and validating the definition (`200 OK` on the validate endpoint) before registration; validation checks structure, not worker availability, credentials, or endpoint reachability.
Code-first construction builds the same document programmatically. SDK (Software Development Kit) workflow builders in Python, Java, JavaScript/TypeScript, Go, and C# assemble task objects with `name`, `taskReferenceName`, `type`, and `inputParameters`, then register the resulting definition; this is the documented path for dynamic graphs whose branch count depends on runtime data.
Minimal adapted sketch (fields renamed from docs examples, structure preserved):
```json
{
  "name": "process_order",
  "version": 1,
  "schemaVersion": 2,
  "inputParameters": ["orderId", "amount"],
  "tasks": [
    {
      "name": "fetch_order",
      "taskReferenceName": "fetch_ref",
      "type": "HTTP",
      "inputParameters": {
        "http_request": {
          "method": "GET",
          "url": "https://api.example.com/orders/${workflow.input.orderId}"
        }
      }
    },
    {
      "name": "charge_payment",
      "taskReferenceName": "charge_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "orderId": "${workflow.input.orderId}",
        "amount": "${workflow.input.amount}",
        "email": "${fetch_ref.output.email}"
      }
    }
  ],
  "outputParameters": {
    "receipt": "${charge_ref.output.transactionId}"
  },
  "failureWorkflow": "order_compensation",
  "timeoutPolicy": "TIME_OUT_WF",
  "timeoutSeconds": 3600
}
```
## Task wiring with expressions
Each task instance receives its input from exactly one of `inputParameters` or `inputExpression`. `inputParameters` is a per-key template where string values may embed `${...}` references; `inputExpression` selects a whole object via one definite JSONPath (JSONPath implementation: jayway/JsonPath) expression such as `workflow.input`.
Reference vocabulary observed across docs:
- `${workflow.input.<key>}` -- run input supplied at start, merged with `inputTemplate` defaults.
- `${<taskRef>.output.<key>}`, `${<taskRef>.input.<key>}` -- output or input of an earlier task addressed by its `taskReferenceName`.
- `${workflow.variables.<key>}` -- mutable variables set by `SET_VARIABLE`; not visible across parent/sub-workflow boundaries except through explicitly declared sub-workflow input parameters.
- `${workflow.version}`, `${workflow.status}`, `${workflow.createTime}`, `${workflow.taskToDomain.<domain>}` -- run metadata.
Unresolved expressions are a wiring error class of their own: misspelled `taskReferenceName`, referencing a task that has not executed yet, or assuming parent variables propagate into a sub-workflow. Per-task flags refine scheduling: `startDelaySeconds` (hold before the task becomes pollable), `optional` (failures become `COMPLETED_WITH_ERRORS`), `asyncComplete: true` (task stays `IN_PROGRESS` until an external signal/event completes it), `callbackAfterSeconds`, `loopCondition` / `decisionCases` / `defaultCase` / `forkTasks` / `joinOn` on the relevant operators, and `subWorkflowParam` (name plus optional version) on `SUB_WORKFLOW`.
## Task definitions: worker tasks vs system tasks
`SIMPLE` (worker) tasks run user code outside the server. Their configuration is thin -- `name` must match a registered task definition, `taskReferenceName` must be unique within the workflow, and `inputParameters` carries the payload -- because behavior lives in the worker process. Example worker binding in Python (adapted from docs):
```python
@worker_task(task_definition_name="charge_payment")
def charge_payment(orderId: str, amount: float) -> dict:
    result = payment_gateway.charge(orderId, amount)
    return {"transactionId": result.id, "status": result.status}
```
System tasks and operators run inside Conductor and need no task definition unless defaults are overridden. Documented built-ins include `HTTP`, `INLINE` (short server-side GraalJS (embedded JavaScript engine) expressions), `EVENT` (publish to a sink), `WAIT` (pause on time, duration, or signal), `HUMAN` (claimable human step), `JSON_JQ_TRANSFORM` (jq/JQ (JSON query/transform language) reshaping), `KAFKA_PUBLISH`, `JDBC` (relational database), `SENDGRID`, `BUSINESS_RULE`, `gRPC`, `UPDATE_TASK`, `UPDATE_SECRET`, `GET_SIGNED_JWT`, `WAIT_FOR_WEBHOOK`, alerting tasks, and AI (Artificial Intelligence) tasks (`LLM_TEXT_COMPLETE`, `LLM_CHAT_COMPLETE`, embedding/index/search/chunk/parse/generate variants, `LIST_MCP_TOOLS` / `CALL_MCP_TOOL` for MCP (Model Context Protocol) tool calling). Operators add branching and fan-out: `SWITCH`, `FORK_JOIN` with `JOIN`, `DYNAMIC_FORK`, `DO_WHILE`, `DYNAMIC`, `SUB_WORKFLOW`, `START_WORKFLOW`, `TERMINATE` / `TERMINATE_WORKFLOW`, `SET_VARIABLE`, `GET_WORKFLOW`, `YIELD`, `EXCLUSIVE_JOIN`.
Reliability fields on the task definition:
- Retries: `retryCount`, `retryLogic`, `retryDelaySeconds`, `maxRetryDelaySeconds`, `backoffScaleFactor`, `backoffJitterMs` (spreads concurrent retries), `totalTimeoutSeconds` (wall-clock budget across all attempts).
- Timeouts: `timeoutSeconds` (per attempt, surfaces `TIMED_OUT`), `responseTimeoutSeconds` (worker picked up the task but stopped responding), `pollTimeoutSeconds` (long-poll hold before the server releases the connection).
- Throughput: `rateLimitPerFrequency` with `rateLimitFrequencyInSeconds`, and `concurrentExecLimit` for parallel executions.
- Caching: `cache: true` with `cacheKeyTemplate` and `cacheTTLSeconds` reuses a prior output for identical inputs within the TTL (Time To Live).
- Placement: `executionNameSpace`, `isolationGroupId`, and domain routing (below).
## Workers: poll-based execution
Workers never receive pushed work. The loop is: poll the queue for a task type, execute, report status. In words as a data-flow sketch using the required characters:
```
Conductor task queue
        │  poll(taskType, domain, workerId)
        ▼
Worker ──► execute(business logic) ──► update(COMPLETED / FAILED + output)
        │                                    │
        │  no task / poll timeout            ▼
        │                              Conductor persists task
        │                              output, advances workflow
```
Concretely: (1) Poll -- the worker long-polls for `SCHEDULED` tasks of its registered type; (2) Execute -- it runs domain code with the resolved `inputParameters`; (3) Report -- it posts output plus `COMPLETED`, `FAILED`, or `FAILED_WITH_TERMINAL_ERROR` (non-retryable). Conductor owns scheduling, retries, and state persistence; the worker owns only business logic and therefore should be idempotent, since retries and redelivery can re-invoke it.
SDK (Software Development Kit) worker frameworks exist for Java, Python, Go, JavaScript/TypeScript, C#, Ruby, and Rust, providing polling threads, metrics, and REST/gRPC (REpresentational State Transfer / gRPC Remote Procedure Call framework) session handling. Configuration most users touch: `pollInterval` / thread or concurrency count on the client side, and the server-side `retryCount`, `timeoutSeconds`, `responseTimeoutSeconds`, `pollTimeoutSeconds`, `rateLimitPerFrequency`, `concurrentExecLimit` from the task definition.
Scaling has three levers. Horizontal scaling adds worker processes; every poller of the same task type shares the queue. Rate and concurrency caps bound throughput per task type. Task-to-domain routing partitions the fleet: the starter passes a `taskToDomain` map (task type to domain label), and each worker sets its `domain`; a worker only receives tasks whose domain matches, which isolates environments, regions, or tenant-specific capacity.
## Execution model
Starting a definition creates a workflow execution with a unique `workflowId`. State is checkpointed after each task, which is why executions tolerate worker restarts, server failover, and waits lasting days. Start paths include direct API (synchronous start for bounded tests, asynchronous start plus status lookup for long runs), schedules (each tick creates an execution), events (create an execution or complete/fail an identified task via `taskId` or `workflowId` + `taskRefName`), parent workflows (`SUB_WORKFLOW`/`START_WORKFLOW`), and signals that resume an existing run. The docs warn against completing waiting work on business correlation keys alone; the event/signal actions require concrete task or workflow identifiers, and delivery follows the event-bus idempotency rules.
Workflow statuses: `RUNNING` (active, scheduling tasks), `PAUSED` (no new tasks until resumed), `COMPLETED` (all tasks done), `FAILED` (unrecoverable task failure, triggers `failureWorkflow` if set, retryable from the failed task), `TIMED_OUT` (exceeded `timeoutSeconds` under `TIME_OUT_WF`), `TERMINATED` (explicitly stopped). Transitions include `RUNNING` to any terminal or `PAUSED` state, `PAUSED` back to `RUNNING` or to `TERMINATED`, and `FAILED`/`TIMED_OUT` back to `RUNNING` on retry.
Task statuses: `SCHEDULED` (queued for a worker), `IN_PROGRESS` (leased by a worker or held by `asyncComplete`), `COMPLETED` (success), `COMPLETED_WITH_ERRORS` (optional task failed but workflow continues), `FAILED` (error, workflow retryable from here), `FAILED_WITH_TERMINAL_ERROR` (error, not retryable), `TIMED_OUT` (per-attempt or response timeout fired; governed by `timeoutPolicy`, `timeoutSeconds`, `pollTimeoutSeconds`, `responseTimeoutSeconds`), `CANCELED` (workflow terminated before the task ran), `SKIPPED` (skip-task API on a running workflow). Each task moves through scheduled to ongoing to exactly one terminal value.
Three orthogonal mechanisms complete the model. Idempotency keys: a client-supplied `requestId` on start (and webhook idempotency keys on event-triggered starts) deduplicates submissions so retries of the start call do not fork duplicate executions. Schema validation: attached JSON schemas gate workflow input/output and, with `validateTaskDefinition`, task payloads; violations fail fast at the boundary rather than deep in the graph. Signals: `WAIT`, `HUMAN`, and `asyncComplete` tasks park the run until `signalTaskAsync`/`signalTaskSync`, an event handler, or a status-listener/CDC (Change Data Capture) reaction advances the named task, which is how people, timers, and external systems re-enter an otherwise server-driven schedule.
**Covers:** https://orkes.io/content/devguide/workflows, https://orkes.io/content/quickstart/workflows, https://orkes.io/content/quickstart/tasks, https://orkes.io/content/quickstart/workers, https://orkes.io/content/documentation/configuration/workflowdef, https://orkes.io/content/developer-guides/write-workflows-using-code, https://orkes.io/content/developer-guides/passing-inputs-to-task-in-conductor, https://orkes.io/content/conceptual-guides/workflow-and-task-status
