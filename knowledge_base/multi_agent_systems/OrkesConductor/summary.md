# Orkes Conductor: Agentic Workflow Engine

**Article:** [Orkes Documentation](https://www.orkes.io/content/) — Orkes Docs, retrieved 2026-09-08

## Human Readable TL;DR
Think of a big kitchen where many cooks, helpers, and machines each do one small job. Conductor is like the head chef with a notebook that writes down every finished step, so if the lights go out the team knows exactly where to pick up. The same notebook now also guides smart talking machines that answer questions and use tools, with a person asked to check before anything important is done.

## TL;DR
Conductor is a durable execution engine for microservice processes and AI-agent work, descended from Netflix Conductor and maintained as Conductor OSS with Orkes Conductor as the compatible commercial distribution. The core mechanism is centralized orchestration: a versioned JSON definition declares a task graph, the server schedules and persists state after every task, and external workers poll queues to execute business logic. The key result is one substrate with identical retry, timeout, persistence, and audit semantics for HTTP calls, event publishes, human approvals, LLM calls, MCP tool calls, and retrieval steps. See [[wiki/01-overview-and-principles|overview]], [[wiki/02-core-abstractions|core abstractions]], and [[wiki/06-agents-and-ai-orchestration|agents]].

## Problem & Motivation
Distributed business processes span services, functions, queues, and external APIs, and point-to-point calls bury routing, retry, and undo logic inside each service. AI agents add the same failure modes with higher stakes: crashes mid-loop, lost tool progress, multi-day approvals holding sessions open, and no record of which decision caused which side effect. Conductor addresses both with deterministic durable execution -- persisted per-step state, explicit failure policy in the graph, and an inspectable history -- while leaving reasoning and planning to models or frameworks.

## Main Original Ideas
1. **Durable checkpoint per task** -- Every task input, output, timing, retry count, and status is persisted before the next task schedules. A crash, restart, deploy, or multi-day wait resumes from the next incomplete task instead of re-running completed work. Delivery is at-least-once with a background sweeper requeuing silent tasks.
2. **Central orchestration with poll-based workers** -- The server owns scheduling, retries, timeouts, and state; workers own only business logic and poll named queues over REST/gRPC with no inbound ports. Orchestration logic stays in a versioned definition rather than in application code.
3. **Server-executed operators vs system tasks vs worker tasks** -- Operators route execution (`SWITCH`, `FORK_JOIN`, `FORK_JOIN_DYNAMIC`, `DYNAMIC`, `DO_WHILE`, `SUB_WORKFLOW`, `WAIT`, `HUMAN`, `TERMINATE`); system tasks do commodity work inside the server (`HTTP`, `INLINE`, `JSON_JQ_TRANSFORM`, `EVENT`, `JDBC`); only `SIMPLE` tasks require user-run workers. See [[wiki/03-operators-and-system-tasks|operators and system tasks]].
4. **Agent proposes, workflow disposes** -- Model output is treated as a proposal, not a command. The workflow validates it against schemas and policy, gates writes with guardrails and `HUMAN` approvals, executes tools as bounded tasks, and persists each turn. Authoring paths are declarative AI tasks, code-authored Conductor Agents compiled to graphs and invoked via `AGENT`, and remote A2A agents behind the same `AGENT` boundary.
5. **Events at the edges, orchestration at the core** -- API/SDK starts, cron schedules, verified webhooks, broker event handlers, and direct signals all create or advance the same execution model. Publishing is an `EVENT` task, consumption is an event handler, and gateways expose workflows outward as REST routes or MCP tools.
6. **Saga compensation instead of distributed transactions** -- No transaction spans services. The main definition declares a `failureWorkflow` that receives the failed execution, checks which steps actually completed, and runs undo tasks in reverse order with their own retries and idempotency keys.
7. **Version-pinned evolution** -- Definitions carry integer versions; each execution pins its start-time snapshot. Rollout registers a new version and moves callers, while in-flight runs drain unless deliberately terminated and restarted with latest definitions.

## Key Findings
- Abstractions: versioned workflow definition (`name`, `version`, `tasks`, `inputParameters`, `outputParameters`, `failureWorkflow`) vs workflow execution (`workflowId`, checkpointed state) vs workers (poll, execute, report `COMPLETED`/`FAILED`/`FAILED_WITH_TERMINAL_ERROR`). See [[wiki/02-core-abstractions|core abstractions]].
- Data wiring uses `${...}` expressions over workflow input, prior task input/output, `workflow.variables`, and metadata; `inputParameters` and `inputExpression` are mutually exclusive per task.
- Engine guarantees: persisted state after every step; per-task `retryCount`, `retryLogic` (`FIXED`, `EXPONENTIAL_BACKOFF`, `LINEAR_BACKOFF`), `retryDelaySeconds`, `responseTimeoutSeconds`, `timeoutSeconds`, `totalTimeoutSeconds`, `timeoutPolicy` (`RETRY`, `TIME_OUT_WF`, `ALERT_ONLY`); idempotent starts via `requestId`; pause primitives `WAIT`, `WAIT_FOR_WEBHOOK`, `HUMAN`, `YIELD`.
- Scale claims (vendor claims, not verified from docs pages): up to 1B+ workflows daily, up to 99.99% availability SLA, 1000+ tasks/sec Orkes vs ~100 tasks/sec OSS, 60000 parallel forks per execution. Documented mechanisms are horizontal worker scaling, server instances behind a load balancer, task domains, and rate/concurrency limits.
- SDK languages: Java, Python, Go, JavaScript/TypeScript, C#, Ruby, Rust, plus Clojure listed in concepts; code-first builders generate the same JSON runtime contract.
- Deployment models: Conductor OSS self-hosted via Docker with PostgreSQL/MySQL/Redis/Cassandra/SQLite backends; Orkes Cloud managed SaaS including free Developer Edition; customer-hosted enterprise Orkes Conductor in the customer cloud or data center.
- Broker coverage splits by distribution: OSS covers internal `conductor` queue, Kafka, SQS, NATS variants, AMQP; Orkes adds Azure Service Bus, GCP Pub/Sub, IBM MQ, Confluent Kafka, Amazon MSK. See [[wiki/04-event-driven-and-integrations|events and integrations]].
- Agent controls: multi-agent `strategy` (`handoff`, `router`, `sequential`, `parallel`, `swarm`, `round_robin`, `random`, `plan_execute`, `manual`); guardrail points (agent-input, agent-output, tool-input, tool-output) with `retry`/`raise`/`fix`/`human`; evals assert on the durable trace (tools, order, arguments, handoffs, turns). See [[wiki/06-agents-and-ai-orchestration|agents]].
- Known limits from docs: `HTTP_POLL` has a server-side floor around 60s; scheduler has no native overlap policy and catchup can burst; `JOIN` waits for all listed branches; retrying a failed `DO_WHILE` restarts that loop history. See [[wiki/05-design-patterns|design patterns]].

## Suggestions & Future Directions
1. Pricing: what do managed throughput, retention, vector search, and multi-region failover cost at production volume, and where is the OSS self-host break-even?
2. Determinism-vs-nondeterminism boundary: which parts of an agent run must stay fully determined (tool allowlists, JQ guards, approval gates) and where is model choice permitted to vary without breaking audit or replay?
3. OSS-vs-cloud parity: which broker integrations, gateway features, evals, guardrail types, and observability feeds exist only in Orkes Cloud, and what is the migration cost if starting on OSS?
4. Latency limits: what p50/p99 overhead does the server add per task, and which paths (sub-second API composition, high-frequency polling, large fan-out) should stay inside a service instead?
5. Idempotency coverage: which built-in tasks and catalog connectors supply native idempotency keys, and which writes require caller-built marker reconciliation?
6. Long-history handling: what are the retention, archiving, and `keepLastN` trade-offs for 100+ iteration loops and multi-day human pauses, and what remains queryable after archival?

## Source
See [[source/sources|source provenance]].
