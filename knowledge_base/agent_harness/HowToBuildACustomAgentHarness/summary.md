# How to Build a Custom Agent Harness

**Article:** [How to Build a Custom Agent Harness](https://www.langchain.com/blog/how-to-build-a-custom-agent-harness) — LangChain, June 3, 2026

## Human Readable TL;DR

Think of the AI model as a very smart engine and the harness as the car built around it — the steering, brakes, fuel system, and dashboard that let it actually go somewhere useful. A customer-service car looks nothing like a long-haul coding truck, so you do not want a one-size-fits-all vehicle; you want a simple chassis you can outfit for the job. LangChain's `create_agent` is that minimal chassis, and middleware pieces are like snap-on accessories that feed the model the right information, handle breakdowns, enforce rules, and keep costs in check. When the accessories fit the road ahead, the same engine goes much further.

## TL;DR

The article formalizes a useful agent as `agent = model + harness`, where the harness is the scaffolding that connects the model to the real world by delivering the right context at every step of the model-tool loop. It argues that task-harness fit determines agent usefulness, and presents LangChain's minimal `create_agent(model, tools, system_prompt)` as the easiest starting point, with customization done through composable middleware. Middleware hooks into the loop before and after model and tool calls plus startup and teardown, working through deterministic logic, tool lifecycle management, custom state, and stream handlers. A capability table maps production needs — context-overflow prevention, memory, environment actions, delegation, retries, policy enforcement, human steering, and cost control — to prebuilt middleware, noting that every agent built at LangChain is a tailored `create_agent` plus middleware stack.

---

## Problem & Motivation

The central problem the article addresses is that models alone do not make useful agents, because an agent is a model calling tools in a loop and its success depends on the context it receives at each step. A generic, opinionated harness fits some tasks but mismatches others, since a customer-service agent and a long-running coding agent need very different context, failure handling, policies, and environments. Pre-assembled harnesses such as Deep Agents and the Claude Agent SDK bundle memory, context management, and sandboxing for fast production readiness, but they leave teams wanting finer-grained control over prompting, business logic, and guardrails. The motivation is therefore to give builders a minimal yet extensible foundation that makes task-harness fit achievable without rebuilding the whole agent loop from scratch.

## Main Original Ideas

1. **Agent equals model plus harness:** the article defines the agent as the model-tool loop and the harness as all surrounding scaffolding, making harness quality the decisive factor in agent usefulness and introducing task-harness fit as the design goal.
2. **Minimal base harness via create_agent:** `create_agent(model, tools, system_prompt)` implements only the core loop and delegates everything else to middleware, favoring explicit customization over opinionated defaults in the spirit of configurable harnesses like Pi.
3. **Middleware as the customization layer:** small units that hook into the loop before and after model calls, before and after tool calls, and at startup and teardown, where each piece owns one concern and composes freely with others while bundling related logic for reuse across an organization.
4. **Four middleware levers:** deterministic logic for runtime control such as model swapping, prompt adjustment, and history updates; full tool lifecycle management for setup, teardown, and registration; custom state for counters, flags, and shared data across hooks; and stream handlers for filtering, metadata injection, and routing events to UI, audit, and monitoring consumers.
5. **Capability-to-middleware mapping:** production requirements are systematized into a table linking each need to prebuilt middleware, covering summarization and context editing for overflow, filesystem, memory, and skills middleware for persistent knowledge, shell, filesystem, and code-interpreter middleware for environment actions, subagent and todo-list middleware for delegation, retry and fallback middleware for transient failures, PII and human-in-the-loop middleware for policy and steering, and call-limit plus prompt-caching middleware for cost control.

## Key Findings

The article finds that the harness's job can be reduced to getting the model the right context at the right time, and that this is best achieved by composing focused middleware rather than stuffing rules into prompts or scattering configuration. Keeping tool configuration close to its governing logic, enforcing policies such as PII handling and approvals on every call regardless of model behavior, and routing stream events to the appropriate consumers emerge as robust patterns for production agents. The validation offered is organizational rather than experimental: the GTM agent, the asynchronous coding agent, and the no-code agent builder at LangChain are all built on `create_agent` with mission-tailored middleware stacks. The broader takeaway is that capable models matter less than a tightly fitting harness, and that bespoke needs are typically one reusable custom middleware away.

## Suggestions & Future Directions

The article points readers toward deepening task-harness fit by starting from the minimal base and adding only the middleware each mission requires, reusing both LangChain's prebuilt pieces and organization-specific custom middleware across agents. It directs builders to the `create_agent` quickstart and guide, the middleware reference and custom-middleware guide, and Deep Agents for cases where an opinionated stack is preferable. The implied direction is continued growth of the shared middleware catalog alongside patterns for memory that compounds over runs, safe environment access, subagent decomposition with progress tracking, and human steering at consequential moments.

## Authors & Institutions

The article was written by Sydney Runkle for LangChain and published on the LangChain blog as a six-minute guide, with references to LangChain's `create_agent`, its middleware ecosystem, Deep Agents, and related harnesses including the Claude Agent SDK and Pi.
