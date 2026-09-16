> [[index|Wiki]] | [[summary|Summary]]

# LangChainCustomHarness — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-base-middleware|create_agent base and middleware customization]]

**In one sentence:** A useful agent is a model plus a task-fitted harness, and LangChain's minimal `create_agent` implements only the core agent loop while exposing composable middleware as the primitive for all customization.

- An agent is defined as `agent = model + harness`, where the harness is the scaffolding that connects the model to the real world and delivers the right context at every step.
- An agent is only as good as the context provided to the model, so the harness's job — and the main lever of agent quality — is context delivery fitted to the task.
- `create_agent` is LangChain's minimal harness primitive: pass a model, tools, and a system prompt and you get a working agent implementing just the core model-calls-tools loop.
- Unlike opinionated pre-assembled harnesses (Deep Agents, Claude Agent SDK) that ship a fixed middleware stack (memory, context management, sandboxing), `create_agent` stays purposefully minimalistic so teams can add only what their task needs.
- Middleware hooks into the agent loop at each step — before/after model calls, before/after tool calls, agent startup and teardown — with each piece handling one concern and composing freely with the others.
- Middleware customizes through four cooperating levers: deterministic logic, tool lifecycle management, custom state, and stream handlers.
- LangChain ships prebuilt middleware for common patterns, while bespoke behavior is one custom middleware away, and isolated middleware units are reusable across every agent in an organization.

## 2. [[wiki/02-capabilities-fit|Harness capabilities and task-harness fit]]

**In one sentence:** A harness earns its keep by delivering the right context at the right time, and production agents stack several middleware capabilities together so the harness tightly fits the task's context, failure, policy, and environment demands.

- The harness's core job is getting the model the right context at the right time for the given task, not just wiring tools to a model.
- Most production agents combine several middleware capabilities at once, chosen by whether the run is long-lived, how complex the tasks are, and how sensitive the actions are.
- Context overflow is handled by summarization and context editing, because long-running sessions accumulate message history that would otherwise exceed the context window.
- Memory access lets agents load relevant knowledge at startup and write it back at the end of a run, so the agent improves over time from real usage.
- Action and delegation capabilities expand what agents can do: filesystem/shell/code-execution access unlocks more creative and token-efficient solutions, while subagents give complex subtasks clean context windows with a todo list tracking long-run progress.
- Reliability, policy, steering, and cost are first-class harness concerns: retries with backoff and model fallbacks absorb transient failures, PII/compliance/approval middleware enforces policy on every call outside the prompt, human-in-the-loop gates consequential actions, and call limits plus prompt caching control spend.
- Task-harness fit means matching the harness to the task's actual context needs, likely failures, enforced policies, and operating environment — a customer-service harness looks very different from a long-running coding-agent harness.
- At LangChain every agent (GTM agent, asynchronous coding agent, no-code agent builder) is built on `create_agent` with a middleware stack tailored to that agent's mission, which the article presents as the easiest path to a custom, tightly fitting harness.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Define the agent as model plus task-fitted harness whose job is delivering the right context.
2. Introduce `create_agent` as a minimal harness implementing only the core model-calls-tools loop.
3. Contrast this minimalism with opinionated pre-assembled harnesses to motivate composing only what each task needs.
4. Present middleware hooks and four customization levers as the universal primitive for all harness behavior.
5. Stack production capabilities — memory, context management, tools, subagents, reliability, policy, and cost — onto that primitive.
6. Close with task-harness fit: match the middleware stack to each task, as LangChain's own agents do.
<!-- FIVE_MOVES_END -->
