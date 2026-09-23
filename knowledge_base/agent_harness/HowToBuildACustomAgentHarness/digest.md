> [[index|Wiki]] | [[summary|Summary]]
# How to Build a Custom Agent Harness — Digest

## 1. [[wiki/01-how-to-build-a-custom-agent-harness|How to Build a Custom Agent Harness]]
**In one sentence:** A useful agent is defined as `agent = model + harness`, so you should build a minimal custom harness with LangChain's `create_agent` and tailor it to the task with composable middleware that delivers the right context at every step.
- An agent is a model calling tools in a loop until it completes a task, formalized as `agent = model + harness`, where the harness is the scaffolding connecting the model to the real world.
- How well a harness fits the task determines how useful an agent is, because a harness for a customer service agent looks very different from one for a long-running coding agent.
- The base harness is built with `create_agent(model, tools, system_prompt)` — e.g. `model="anthropic:claude-sonnet-4-6"` — which implements only the core agent loop and leaves customization to middleware.
- Middleware hooks into the agent loop before and after model calls, before and after tool calls, and at agent startup and teardown, with each piece handling one concern and composing freely with others.
- Middleware customizes via four levers: deterministic logic (model swapping, prompt adjustment, history updates), tool lifecycle management (setup/teardown/registration), custom state (counters, flags, shared data), and stream handlers (filtering/routing events to UI, audit log, monitoring).
- Production agents combine several capabilities: context-overflow prevention, memory load/save, environment actions, subagent delegation, retry/fallback, policy enforcement, human steering, and cost control, mapped to specific prebuilt middleware.
- Every agent built at LangChain — including the GTM agent, asynchronous coding agent, and no-code agent builder — is built on `create_agent` with a middleware stack tailored to that agent's mission.

## The argument in five moves
1. An agent is a model looping over tools, so its usefulness is decided by task-harness fit — how well the surrounding harness matches the task's context, failure, policy, and environment demands.
2. Start from a minimal base harness with `create_agent(model, tools, system_prompt)` rather than an opinionated prebuilt stack, keeping only the core agent loop.
3. Customize that loop with composable middleware that hooks in before/after model calls, before/after tool calls, and at startup/teardown, one concern per piece.
4. Pull the four middleware levers — deterministic logic, tool lifecycle management, custom state, and stream handlers — to deliver the right context at every step.
5. Cover the production capabilities every real agent needs: context-overflow prevention, memory load/save, environment actions, subagent delegation, retries/fallbacks, policy enforcement, human steering, and cost control.
6. The proof is reuse: every agent built at LangChain ships as `create_agent` plus a middleware stack tailored to its mission.
