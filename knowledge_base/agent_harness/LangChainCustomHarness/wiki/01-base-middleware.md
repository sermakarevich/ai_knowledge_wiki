> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# create_agent base and middleware customization

**In one sentence:** A useful agent is a model plus a task-fitted harness, and LangChain's minimal `create_agent` implements only the core agent loop while exposing composable middleware as the primitive for all customization.

## Key points

- An agent is defined as `agent = model + harness`, where the harness is the scaffolding that connects the model to the real world and delivers the right context at every step.
- An agent is only as good as the context provided to the model, so the harness's job — and the main lever of agent quality — is context delivery fitted to the task.
- `create_agent` is LangChain's minimal harness primitive: pass a model, tools, and a system prompt and you get a working agent implementing just the core model-calls-tools loop.
- Unlike opinionated pre-assembled harnesses (Deep Agents, Claude Agent SDK) that ship a fixed middleware stack (memory, context management, sandboxing), `create_agent` stays purposefully minimalistic so teams can add only what their task needs.
- Middleware hooks into the agent loop at each step — before/after model calls, before/after tool calls, agent startup and teardown — with each piece handling one concern and composing freely with the others.
- Middleware customizes through four cooperating levers: deterministic logic, tool lifecycle management, custom state, and stream handlers.
- LangChain ships prebuilt middleware for common patterns, while bespoke behavior is one custom middleware away, and isolated middleware units are reusable across every agent in an organization.

---

## Agent = model + harness

Building useful agents is largely about customization: connecting the agent to the right context, data, and environment(s) for the task at hand.

At its core, an agent is a model calling tools in a loop until it completes a task and returns a result. Equivalently:

> agent = model + harness

The harness is the scaffolding around the model that connects it to the real world. The post assumes:

- An agent is only as good as the context provided to the model.
- The job of a harness is to provide context to the model at every step.
- So, to build a useful agent, you need a harness that is great at delivering the right context for the given task.

How well a harness fits the task at hand determines how useful an agent is.

## The base harness: create_agent

`create_agent` is LangChain's primitive for building a harness. Pass in a model, tools, and a system prompt, and you have a working agent:

```python
from langchain.agents import create_agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=tools,
    system_prompt="you are a helpful assistant..."
)
```

Design philosophy:

- Harnesses like Deep Agents and the Claude Agent SDK come pre-assembled with an opinionated middleware stack: memory, context management, sandboxing, and more. They get you to a production-ready agent fast and work well for most cases.
- But many agents need finer grained customization than these harnesses support: custom prompting, business logic, guardrails, etc.
- `create_agent` takes a different, purposefully minimalistic approach — similar in spirit to Pi, a highly configurable coding agent harness. It just implements the core agent loop and exposes middleware as a primitive for customization.

## Middleware: how you customize the harness

Middleware hooks into the agent loop at each step: before and after model calls, before and after tool calls, at agent startup and teardown. Each piece handles one concern and composes freely with any other.

### The four customization levers

Middleware adds capabilities via levers that often work together:

1. **Deterministic Logic.** Business logic, policy enforcement, dynamic agent control — anything that needs to fire at a specific point in the loop. This includes runtime control over the agent itself: swapping the model based on task complexity, adjusting the prompt, and updating the agent's message history (during compaction, for example). The right place for anything that can't (or shouldn't) live in a prompt.
2. **Tools.** Rather than registering tools directly on the agent, middleware can handle the full lifecycle — setup, teardown, registration — and hand the agent a clean set of tools to work with. This matters when tools have dependencies, require initialization, or need to be torn down cleanly at the end of a run. It also keeps tool configuration close to the logic that governs it, rather than scattered across the agent definition.
3. **Custom state.** If middleware needs to track state across hooks, it can extend the agent's state with custom properties. This enables middleware to track state throughout execution (maintain counters, flags, or other values that persist throughout agent runs) and share data between hooks.
4. **Stream handlers.** Middleware can intercept and transform the agent's output stream — filtering events, injecting metadata, routing different event types to different consumers. Useful when different parts of the stack need to react to different things the agent does: a UI consuming token deltas, an audit log capturing tool calls, a monitoring system tracking latency.

### Why middleware composes well

The beauty of middleware is that it:

- Enables customization at any point in the agent loop.
- Bundles related logic in composable, sharable units of code.

LangChain ships prebuilt middleware for the most common patterns. Anything bespoke to your use case is one custom middleware away. Because each piece is isolated, the same middleware can be reused across every agent in an organization so that new agents inherit battle-tested behavior without rebuilding it.

**Covers:** base harness + middleware
