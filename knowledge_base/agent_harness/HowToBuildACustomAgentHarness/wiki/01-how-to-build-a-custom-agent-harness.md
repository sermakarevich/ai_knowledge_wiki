[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# How to Build a Custom Agent Harness
**In one sentence:** A useful agent is defined as `agent = model + harness`, so you should build a minimal custom harness with LangChain's `create_agent` and tailor it to the task with composable middleware that delivers the right context at every step.
## Key points
- An agent is a model calling tools in a loop until it completes a task, formalized as `agent = model + harness`, where the harness is the scaffolding connecting the model to the real world.
- How well a harness fits the task determines how useful an agent is, because a harness for a customer service agent looks very different from one for a long-running coding agent.
- The base harness is built with `create_agent(model, tools, system_prompt)` — e.g. `model="anthropic:claude-sonnet-4-6"` — which implements only the core agent loop and leaves customization to middleware.
- Middleware hooks into the agent loop before and after model calls, before and after tool calls, and at agent startup and teardown, with each piece handling one concern and composing freely with others.
- Middleware customizes via four levers: deterministic logic (model swapping, prompt adjustment, history updates), tool lifecycle management (setup/teardown/registration), custom state (counters, flags, shared data), and stream handlers (filtering/routing events to UI, audit log, monitoring).
- Production agents combine several capabilities: context-overflow prevention, memory load/save, environment actions, subagent delegation, retry/fallback, policy enforcement, human steering, and cost control, mapped to specific prebuilt middleware.
- Every agent built at LangChain — including the GTM agent, asynchronous coding agent, and no-code agent builder — is built on `create_agent` with a middleware stack tailored to that agent's mission.
---
## The base harness
**Covers:** Key Takeaways through The base harness

> "A harness is the scaffolding around the model that connects it to the real world."
> "How well a harness fits the task at hand determines how useful an agent is."
> "LangChain's create_agent is the easiest way to build a custom harness tailored to a given task."

The post assumes:

- An agent is only as good as the context provided to the model
- The job of a harness is to provide context to the model at every step

Base example from the chunk:

```python
from langchain.agents import create_agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=tools,
    system_prompt="you are a helpful assistant...")
```

Pre-assembled harnesses like Deep Agents and the Claude Agent SDK come with an opinionated middleware stack (memory, context management, sandboxing) for fast production readiness, while `create_agent` is purposefully minimalistic — similar in philosophy to Pi, a highly configurable coding agent harness — for finer-grained customization (custom prompting, business logic, guardrails).

## Middleware: how you customize the harness
**Covers:** Middleware section

Middleware hooks into the agent loop at each step: before and after model calls, before and after tool calls, at agent startup and teardown. Each piece handles one concern and composes freely with any other.

Four levers:

- **Deterministic Logic:** business logic, policy enforcement, dynamic agent control; includes runtime control such as swapping the model by task complexity, adjusting the prompt, and updating message history (e.g. during compaction).
- **Tools:** full lifecycle — setup, teardown, registration — handing the agent a clean toolset; keeps tool configuration close to governing logic rather than scattered across the agent definition.
- **Custom state:** extends agent state with custom properties to track counters, flags, or other values persisting throughout runs and share data between hooks.
- **Stream handlers:** intercepts and transforms output stream — filtering events, injecting metadata, routing event types to different consumers (UI token deltas, audit log tool calls, monitoring latency).

> "The beauty of middleware is that it: Enables customization at any point in the agent loop; Bundles related logic in composable, sharable units of code."

LangChain ships prebuilt middleware for common patterns; bespoke needs are one custom middleware away, reusable across every agent in an organization.

## Harness capabilities
**Covers:** Harness capabilities table

> "The job of a harness is to get the model the right context at the right time for the given task."

| Capability | Why it Matters | Middleware |
|---|---|---|
| Prevent context overflow | Long-running sessions accumulate message history fast; without intervention it overflows the context window | SummarizationMiddleware, ContextEditingMiddleware |
| Access and update memory | Load relevant knowledge at startup, write it back at end of run; lets agent improve over time | FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware |
| Take actions in an environment | Fixed toolset limits the agent; filesystem and execution access unlocks more creative solutions, often with greater token efficiency | ShellToolMiddleware, FilesystemMiddleware, CodeInterpreterMiddleware |
| Delegate tasks | Subagents handle complex sub-tasks with clean context windows; todo list tracks progress across long runs | SubAgentMiddleware, AsyncSubAgentMiddleware, TodoListMiddleware |
| Handle transient failures | Models and tools fail unpredictably; production agents need retry with backoff and fallbacks | ToolRetryMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware |
| Enforce policies | PII handling, compliance checks, approval gates must fire on every call regardless of model behavior; they don't belong in a prompt | PIIMiddleware, HumanInTheLoopMiddleware |
| Steer the agent | Full autonomy isn't always appropriate; pause before consequential actions for human approve/reject/redirect | HumanInTheLoopMiddleware |
| Control costs | Prompt caching reduces token spend on long tasks; call limits prevent unchecked cost accumulation | ModelCallLimitMiddleware, ToolCallLimitMiddleware, PromptCachingMiddleware |

## Task-harness fit
**Covers:** Task-harness fit through References

> "Task-harness fit is how well your harness matches the actual demands of the task: the context it needs, the failures it'll encounter, the policies it must enforce, the environment it operates in."

> "The best agents aren't just built with capable models, they're built with harnesses that tightly fit the task. The easiest way to build a custom harness is with create_agent."

By Sydney Runkle, June 3, 2026, 6 min. Get-started links listed: Quickstart with create_agent, create_agent guide, Middleware reference, Custom middleware guide, Deep Agents.

**Covers:** Overview of building a custom agent harness (LangChain article).
