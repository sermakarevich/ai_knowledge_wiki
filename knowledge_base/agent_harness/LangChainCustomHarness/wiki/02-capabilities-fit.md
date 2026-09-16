> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Harness capabilities and task-harness fit

**In one sentence:** A harness earns its keep by delivering the right context at the right time, and production agents stack several middleware capabilities together so the harness tightly fits the task's context, failure, policy, and environment demands.

## Key points

- The harness's core job is getting the model the right context at the right time for the given task, not just wiring tools to a model.
- Most production agents combine several middleware capabilities at once, chosen by whether the run is long-lived, how complex the tasks are, and how sensitive the actions are.
- Context overflow is handled by summarization and context editing, because long-running sessions accumulate message history that would otherwise exceed the context window.
- Memory access lets agents load relevant knowledge at startup and write it back at the end of a run, so the agent improves over time from real usage.
- Action and delegation capabilities expand what agents can do: filesystem/shell/code-execution access unlocks more creative and token-efficient solutions, while subagents give complex subtasks clean context windows with a todo list tracking long-run progress.
- Reliability, policy, steering, and cost are first-class harness concerns: retries with backoff and model fallbacks absorb transient failures, PII/compliance/approval middleware enforces policy on every call outside the prompt, human-in-the-loop gates consequential actions, and call limits plus prompt caching control spend.
- Task-harness fit means matching the harness to the task's actual context needs, likely failures, enforced policies, and operating environment — a customer-service harness looks very different from a long-running coding-agent harness.
- At LangChain every agent (GTM agent, asynchronous coding agent, no-code agent builder) is built on `create_agent` with a middleware stack tailored to that agent's mission, which the article presents as the easiest path to a custom, tightly fitting harness.

---

## Harness capabilities

The job of a harness is to get the model the right context at the right time for the given task.

Most production agents end up using several capabilities together, depending on the agent's needs: is it long running? How complex are the tasks? How sensitive are the agent's actions?

### Prevent context overflow

- Why it matters: long-running sessions accumulate message history fast. Without intervention, it overflows the context window.
- Middleware: SummarizationMiddleware, ContextEditingMiddleware.

### Access and update memory

- Why it matters: load relevant knowledge at startup, write it back at the end of a run. Lets the agent improve over time from real usage.
- Middleware: FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware.

### Take actions in an environment

- Why it matters: a fixed toolset limits what an agent can do. Access to a filesystem and execution environment unlocks more creative solutions, often with greater token efficiency.
- Middleware: ShellToolMiddleware, FilesystemMiddleware, CodeInterpreterMiddleware.

### Delegate tasks

- Why it matters: subagents handle complex sub-tasks with clean context windows. A todo list tracks progress across a long run.
- Middleware: SubAgentMiddleware, AsyncSubAgentMiddleware, TodoListMiddleware.

### Handle transient failures

- Why it matters: models and tools fail unpredictably. Production agents need retry logic with backoff and fallbacks when a model is unavailable.
- Middleware: ToolRetryMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware.

### Enforce policies

- Why it matters: PII handling, compliance checks, approval gates — these need to fire on every call regardless of what the model does. They don't belong in a prompt.
- Middleware: PIIMiddleware, HumanInTheLoopMiddleware.

### Steer the agent

- Why it matters: full autonomy isn't always appropriate. Pause before consequential actions and wait for a human to approve, reject, or redirect.
- Middleware: HumanInTheLoopMiddleware.

### Control costs

- Why it matters: prompt caching reduces token spend on long-running tasks. Call limits prevent costs from accumulating unchecked.
- Middleware: ModelCallLimitMiddleware, ToolCallLimitMiddleware, PromptCachingMiddleware.

See the full list of prebuilt middleware in the middleware reference.

## Task-harness fit

Task-harness fit is how well your harness matches the actual demands of the task: the context it needs, the failures it'll encounter, the policies it must enforce, the environment it operates in.

A harness for a customer service agent looks very different from one built for a long-running coding agent.

Every agent built at LangChain — including the GTM agent, the asynchronous coding agent, and the no-code agent builder — is built on `create_agent` with a middleware stack tailored to that agent's mission.

The best agents aren't just built with capable models, they're built with harnesses that tightly fit the task. The easiest way to build a custom harness is with `create_agent`.

**Covers:** capabilities + fit
