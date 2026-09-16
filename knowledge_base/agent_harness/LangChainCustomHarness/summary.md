# How to Build a Custom Agent Harness

**Article:** [How to Build a Custom Agent Harness](https://www.langchain.com/blog/how-to-build-a-custom-agent-harness) — langchain.com, 2026

## Human Readable TL;DR

An agent is only as good as the harness around it: `agent = model + harness`. LangChain's `create_agent` is a deliberately minimal harness — model, tools, system prompt, and the basic model-calls-tools loop — with everything else added through composable middleware pieces that hook in before/after model and tool calls. Middleware customizes via four levers (deterministic logic, tool lifecycle, custom state, stream handlers), and production agents stack several capability groups (context management, memory, action/delegation, reliability, policy/steering, cost control) chosen by how long-lived, complex, and sensitive the task is. The article's thesis is task-harness fit: start minimal and add only what the task needs, rather than adopting a fixed, pre-assembled harness.

## TL;DR

The post frames agent quality as a function of harness design, not just model choice. `create_agent` implements only the core loop (model calls tools until done) and exposes middleware as the universal customization primitive, hooking in at model-call and tool-call boundaries plus startup/teardown. Middleware works through four levers — deterministic logic, tool lifecycle management, custom state, and stream handlers — and LangChain ships prebuilt middleware for common needs (summarization, context editing, memory, filesystem/shell/code-execution access, subagents with todo tracking, retries/fallbacks, PII/compliance/approval gates, human-in-the-loop, call limits, prompt caching) while custom behavior is one middleware away. Production fit means picking capabilities based on run length, task complexity, and action sensitivity — a customer-service agent and a long-running coding agent end up with very different stacks, even though both start from the same `create_agent` base. LangChain's own internal agents (GTM, async coding, no-code builder) are presented as proof that this minimal-base-plus-tailored-middleware approach scales across very different missions.

---

## Problem & Motivation

Building useful agents is largely about customization: connecting the agent to the right context, data, and environment for the task. Two teams with the same model get very different results because harness quality — context delivery fitted to the task — is the actual lever, not model choice. Opinionated pre-assembled harnesses (Deep Agents, Claude Agent SDK) ship a fixed stack and get you to production fast, but many agents need finer-grained customization — custom prompting, business logic, guardrails — than fixed stacks support. The middleware abstraction also lets teams isolate and reuse customization units (a memory loader, a cost guard) across every agent they build instead of re-deriving the same logic per agent.

---

## Main Original Ideas

1. **`agent = model + harness`, with context delivery as the job** — The harness is the scaffolding that connects the model to the real world; an agent is only as good as the context the harness provides at every step, so task fit determines agent quality.
2. **`create_agent` as a minimal base** — Pass a model, tools, and a system prompt and you get a working agent implementing just the core model-calls-tools loop — purposefully minimalistic, similar in spirit to Pi, so teams add only what their task needs.
3. **Middleware as the universal customization primitive** — Middleware hooks in before/after model calls, before/after tool calls, and at startup/teardown; each piece handles one concern and composes freely with the others, and isolated units are reusable across every agent in an organization.
4. **Four customization levers** — Deterministic logic (business logic, policy, model swapping, prompt/history control — anything that can't live in a prompt); tool lifecycle (setup, registration, teardown kept next to the governing logic); custom state (counters, flags shared across hooks); stream handlers (filtering events, metadata, routing to UI/audit/monitoring consumers).
5. **Task-harness fit over a universal stack** — Match the harness to the task's context needs, likely failures, enforced policies, and environment. A customer-service harness (memory, PII/compliance/approval, human-in-the-loop) looks very different from a long-running coding harness (summarization, subagents with todos, shell/code execution) — over-fitting (bloat) fails as surely as under-fitting (fragility).

---

## Key Findings

- Most production agents combine several middleware capability groups at once: context-overflow control (summarization, context editing), memory load/write-back, environment action (filesystem/shell/code execution), delegation (subagents, todo lists), reliability (retries with backoff, model fallbacks), policy enforcement (PII, compliance, approvals), steering (human-in-the-loop gates), and cost control (call limits, prompt caching).
- Fixed toolsets limit what agents can do; shell and execution access unlock more creative, often more token-efficient solutions, while subagents give complex subtasks clean context windows.
- Policy must fire on every call regardless of model behavior, so it belongs in middleware, not in a prompt.
- Every agent built at LangChain (GTM, async coding, no-code builder) runs on `create_agent` plus a mission-specific middleware stack — presented as evidence the minimal-base approach scales across missions.

---

## Suggestions & Future Directions

1. **Start with the smallest working agent, then add only what the task demands** — Begin at `create_agent` and grow the middleware stack by demonstrated need.
2. **Build shared middleware as organizational leverage** — Isolated, battle-tested units (memory loader, cost guard, approval gate) transfer across agents for free.
3. **Pick capabilities by run profile** — Long-lived, complex, or action-sensitive runs earn context, memory, delegation, and gating middleware; short, simple, low-stakes ones don't.

---

## Authors & Institutions

LangChain team — vendor engineering blog post (langchain.com, 2026); no individual authors listed.
