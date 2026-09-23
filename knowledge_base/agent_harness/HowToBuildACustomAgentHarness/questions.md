---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: How to Build a Custom Agent Harness
### Q1. What does the formula `agent = model + harness` mean, and what job does the harness do?
> [!tip]- Answer
> An agent is a model calling tools in a loop until the task is done, and the harness is the scaffolding that connects the model to the real world. Its core job is to deliver the right context to the model at every step, since an agent is only as good as the context it receives. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q2. What is task-harness fit, and why does it determine how useful an agent is?
> [!tip]- Answer
> Task-harness fit is how well the harness matches the task's demands: the context it needs, the failures it will encounter, the policies it must enforce, and the environment it operates in. A customer-service agent and a long-running coding agent need very different harnesses, so fit decides usefulness more than raw model capability. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q3. How do you build the minimal base harness with `create_agent`, and how does it differ from a pre-assembled harness?
> [!tip]- Answer
> You call `create_agent(model, tools, system_prompt)` — for example with `model="anthropic:claude-sonnet-4-6"` — which implements only the core agent loop and leaves customization to middleware. Pre-assembled harnesses like Deep Agents or the Claude Agent SDK ship an opinionated stack (memory, context management, sandboxing) for fast production readiness, while `create_agent` stays minimal for finer-grained control over prompting, business logic, and guardrails. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q4. Where does middleware hook into the agent loop, and what makes it composable?
> [!tip]- Answer
> Middleware hooks in before and after model calls, before and after tool calls, and at agent startup and teardown. Each piece handles one concern and composes freely with any other, so related logic stays bundled in sharable, reusable units instead of scattered across the agent definition. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q5. What are the four middleware levers, and what does each one control?
> [!tip]- Answer
> The four levers are deterministic logic (model swapping by task complexity, prompt adjustment, history updates such as compaction), tool lifecycle management (setup, teardown, registration of a clean toolset), custom state (counters, flags, and shared data persisting across runs and hooks), and stream handlers (filtering events, injecting metadata, routing token deltas to UI, tool calls to audit log, latency to monitoring). Together they let you customize the loop at any point. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q6. Which middleware covers each production capability: context overflow, memory, environment actions, delegation, failures, policies, steering, and costs?
> [!tip]- Answer
> Context overflow is handled by SummarizationMiddleware and ContextEditingMiddleware; memory load/save by Filesystem, Memory, and Skills middleware; environment actions by ShellTool, Filesystem, and CodeInterpreter middleware; and delegation by SubAgent, AsyncSubAgent, and TodoList middleware. Transient failures use ToolRetry, ModelRetry, and ModelFallback middleware; policies use PII and HumanInTheLoop middleware; steering pauses via HumanInTheLoopMiddleware; and cost control uses ModelCallLimit, ToolCallLimit, and PromptCaching middleware. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
### Q7. (evaluation) A team must choose between starting from minimal `create_agent` plus custom middleware versus adopting Deep Agents as-is — what should they recommend and why?
> [!tip]- Answer
> They should recommend minimal `create_agent` when the task has unusual context, policy, or environment demands (e.g. strict PII gates, custom tools, human approval before consequential actions), because task-harness fit matters more than model power and only composable middleware can match it. They should recommend Deep Agents when speed to production outweighs fit and the default memory, context-management, and sandboxing stack already covers the need, accepting opinionated defaults to avoid rebuilding common capabilities. See [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]].
