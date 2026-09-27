---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Orkes Conductor

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. How are Netflix Conductor, Conductor OSS (open-source software), and Orkes Conductor related, and what durability problem do they all solve?
> [!tip]- Answer
> Conductor started at Netflix as an open-source workflow engine, continued as Conductor OSS (open-source software) with Orkes as the main maintainer, and Orkes Conductor is the commercial distribution built on top of that same engine. All three solve durable execution of long-running processes, meaning a crash, restart, timeout, or multi-day wait must not lose completed work. The engine saves state after every step so a run resumes from the next unfinished task instead of starting over. See [[wiki/01-overview-and-principles|Overview and Principles]].

### Q2. In Conductor's worker model, who initiates contact and what three steps does a worker repeat?
> [!tip]- Answer
> The worker always initiates contact by polling a named task queue, so the server never pushes work and workers need no inbound ports. The loop is poll for a SCHEDULED task of its type, run the business logic with the given inputs, then report COMPLETED, FAILED, or FAILED_WITH_TERMINAL_ERROR with outputs. The server then saves the result, handles retries and timeouts, and schedules the next task. See [[wiki/02-core-abstractions|Core Abstractions]].

### Q3. What is the difference between FAILED, FAILED_WITH_TERMINAL_ERROR, and COMPLETED_WITH_ERRORS for a task?
> [!tip]- Answer
> FAILED means the task errored but the workflow can be retried from that task, while FAILED_WITH_TERMINAL_ERROR means the worker declares the error as non-retryable so Conductor skips remaining retries. COMPLETED_WITH_ERRORS means an optional task failed but the workflow is allowed to continue instead of failing. This distinction lets authors separate transient errors, permanent errors, and safe-to-ignore errors. See [[wiki/02-core-abstractions|Core Abstractions]].

### Q4. When should you use FORK_JOIN with JOIN versus FORK_JOIN_DYNAMIC with JOIN for parallel work?
> [!tip]- Answer
> FORK_JOIN (fan-out/fan-in) is for static parallelism where the branches are fixed at design time, such as three known enrichment calls run together and then joined. FORK_JOIN_DYNAMIC is for runtime-sized parallelism where the number of branches comes from upstream data, such as one branch per order item or per region. A common pattern is an INLINE (small server-side script) task building the branch list, then DYNAMIC_FORK fanning out, then JOIN collecting results. See [[wiki/03-operators-and-system-tasks|Operators and System Tasks]].

### Q5. Why do operators and system tasks need no worker deployment, and what breaks if you move routing logic into worker code?
> [!tip]- Answer
> Operators such as SWITCH (conditional branch) and FORK_JOIN, plus system tasks such as HTTP (web API call) and INLINE, all run inside the Conductor server, so only SIMPLE tasks need your own polling workers. If you hide routing inside worker code, branches disappear from the visual trace, audit history, and versioned definition, making runs harder to inspect and recover. Keeping control flow on the server also lets retries, timeouts, and approvals apply uniformly without custom code. See [[wiki/03-operators-and-system-tasks|Operators and System Tasks]].

### Q6. What are the five ways a workflow can be started or resumed, and how does publishing differ from consuming events?
> [!tip]- Answer
> Direct API (Application Programming Interface) or SDK (Software Development Kit) start, cron (scheduled) start, verified incoming webhook, broker message via an event handler, and a signal into a waiting execution all create or advance the same execution model. Publishing is a workflow task such as EVENT or KAFKA_PUBLISH (a Kafka-specific publish task), while consumption is a separate control-plane object called an event handler that matches a message and runs an action such as start_workflow. Webhooks are a third path that only start workflows or resume WAIT_FOR_WEBHOOK tasks, never general action dispatch. See [[wiki/04-event-driven-and-integrations|Event-Driven and Integrations]].

### Q7. How would you expose an order-processing workflow as a web endpoint for apps and as a tool for an AI agent?
> [!tip]- Answer
> For apps you would use the API (Application Programming Interface) gateway to map an HTTP (Hypertext Transfer Protocol) method plus path to the workflow, running under an application identity with EXECUTE permission. For an AI (Artificial Intelligence) agent you would use the MCP (Model Context Protocol, the standard for exposing tools to models) gateway the same way but with MCP enabled, so each route appears as a callable tool that runs the workflow and returns its output. In both cases secrets and credentials stay in the secrets store and are referenced symbolically, never written into the definition. See [[wiki/04-event-driven-and-integrations|Event-Driven and Integrations]].

### Q8. In an order flow with reserve, charge, and ship steps, why does saga compensation use a failureWorkflow, and what breaks if you undo blindly?
> [!tip]- Answer
> There is no distributed transaction across services, so Conductor runs a separate compensation workflow registered as failureWorkflow only after the main workflow fails terminally. That workflow reads failedWorkflow to see which steps actually reached COMPLETED, then runs undo tasks in reverse order such as refund and release. If you undo blindly without gating on completed steps, you can refund a charge that never happened or release inventory that was never reserved. See [[wiki/05-design-patterns|Design Patterns]].

### Q9. Why does Conductor separate responseTimeoutSeconds, timeoutSeconds, and totalTimeoutSeconds, and what breaks if workers never send heartbeats?
> [!tip]- Answer
> responseTimeoutSeconds is the heartbeat window for a worker that picked up a task but went silent, timeoutSeconds bounds one attempt, and totalTimeoutSeconds caps the wall-clock budget across all retries. Without heartbeats such as IN_PROGRESS updates with callbackAfterSeconds, a silent worker is marked TIMED_OUT and retried while the late result is discarded, which can duplicate side effects. Retries therefore need idempotency keys (caller-supplied dedupe tokens), plus backoff and jitter to avoid hammering a recovering service all at once. See [[wiki/05-design-patterns|Design Patterns]].

### Q10. What makes a Conductor agent durable, and why does a crash at iteration 15 of 20 resume instead of restart?
> [!tip]- Answer
> Every turn is an ordinary persisted workflow task, so each LLM (Large Language Model, a model that generates text from context) proposal, MCP (Model Context Protocol) tool call, approval, and DO_WHILE (loop) iteration checkpoints before the next begins. A crash therefore resumes from the last saved state and only the in-flight unit re-runs, preserving earlier prompts, tool outputs, and decisions. This also saves cost because completed model calls are not re-paid on recovery or retry-from-failed-step. See [[wiki/06-agents-and-ai-orchestration|Agents and AI Orchestration]].

### Q11. For a document-approval agent that can publish externally, where should guardrails and HUMAN approval sit and what happens on failure?
> [!tip]- Answer
> Guardrails attach at the closest enforceable point, with the strongest check on tool-input before a consequential write such as publishing, plus input, output, and tool-output checks around it. Each guardrail declares onFail as retry with feedback, raise to fail closed, fix with corrected output, or human for durable review. A HUMAN (human approval) task must return approved before the single write, so rejection ends the run as a durable no-write decision instead of an accidental publish. See [[wiki/06-agents-and-ai-orchestration|Agents and AI Orchestration]].

### Q12. How would you apply the agent-proposes, workflow-disposes pattern to an Elisity data pipeline where an agent suggests pipeline changes?
> [!tip]- Answer
> A parent workflow would validate the request and IDs, run the agent behind an explicit boundary such as native tasks or an AGENT task, then validate the returned result schema and artifacts before any write. A HUMAN approval gate would be required before applying the change, with correlation and idempotency keys carried into every external effect. On failure the run would compensate via failureWorkflow, keeping model reasoning separate from governed execution and audit. See [[wiki/06-agents-and-ai-orchestration|Agents and AI Orchestration]].
