# Build Your Own Agent Harness

**Source:** [How to build your own agent harness??? (Mike Piccolo, 2026)](https://x.com/mfpiccolo/status/2060069083878408689)
**Author:** Mike Piccolo, Founder & CEO @ iiidevs

---

## Human Readable TL;DR

Imagine you're building a robot, and instead of buying all the parts as a single toy kit, you can buy each arm, leg, and brain separately from different stores. Right now, most AI agent teams buy the whole toy kit from one company (LangChain, OpenAI Agents SDK, etc.). If one part doesn't fit your needs, you have to swap out the whole kit. The iii framework flips this: every piece of the "robot brain" is a separate, swappable part connected by one simple plug. You install only what you need, write replacements for what you don't like, and the rest keeps working.

## TL;DR

Most agent teams treat their harness as a monolith -- a single imported framework. The iii (triple-i) framework decomposes the harness into ~13 independent workers, each registered on a shared engine bus via WebSocket. Every worker exposes its capabilities through a single primitive (`iii.trigger()`), making any layer independently replaceable without touching the rest of the stack. This shifts "build your own harness" from "fork a framework" to "swap a few workers."

---

## Problem & Motivation

Every serious agent harness has to do roughly 15 jobs: accept turn requests, resolve credentials, look up model capabilities, drive the per-turn state machine, serve skill definitions, assemble system prompts, stream tokens, enforce policies, handle human-in-the-loop approvals, track budgets, run hooks, persist branching session history, compact context, emit events, and propagate OpenTelemetry traces.

Current frameworks (LangChain, LangGraph, CrewAI, AutoGen, OpenAI Agents SDK) bundle all these into a single monolith. When one component doesn't fit -- say, you need a different policy engine or approval UI -- you can't replace just that layer; you fight the whole framework or eventually rewrite the harness from scratch. This happens to "every long-running agent team."

---

## Main Original Ideas

1. **The Harness as Composable Workers** -- Instead of one framework import, the harness is 11-13 separate processes, each opening a WebSocket to the engine, registering functions and triggers, and running independently. Examples: `turn-orchestrator`, `auth-credentials`, `policy-engine`, `approval-gate`, `llm-budget`, `hook-fanout`, `context-compaction`, `provider-anthropic`.

2. **Single Shared Primitive: `iii.trigger()`** -- Every worker and every business-logic function communicates through the same bus-level trigger call. Replacing a harness layer is writing a worker that registers the same function IDs. The orchestrator never knows which physical process answers.

3. **Thin vs. Thick is a Slider, Not a Fork** -- A minimal harness is just 4 workers (orchestrator + provider + auth + meta-worker). A full production harness is 13+ workers with approvals, budgets, policy enforcement, and Slack-integrated approval surfaces. You add or remove workers from a config file; the wire protocol stays identical.

4. **Reactive Single-Trigger Approval** -- Instead of per-call resume functions, one `turn::on_approval` state trigger on `scope approvals` wakes any session when `approvals/<sid>/<cid>` is written to state. This eliminates startup re-scan and per-call registration overhead.

5. **Fail-Closed Policy Gate** -- Every tool call passes through `dispatchWithHook` → `consultBefore` → `policy::check_permissions` with a 5-second timeout. If the policy worker is unreachable or times out, the call is denied with a `gate_unavailable` envelope. No silent pass-throughs.

6. **Automatic OTel Instrumentation via Proxy** -- `src/runtime/worker.ts` wraps every `registerFunction` in a Proxy, so every worker automatically emits spans tagged with `iii.session.id`, `iii.message.id`, and `iii.function.id` without per-worker instrumentation code.

---

## Key Findings

### The 15 Jobs Every Agent Harness Must Do

| # | Job | iii Worker |
|---|-----|-----------|
| 1 | Accept & persist turn request | `harness-meta` |
| 2 | Resolve provider credentials | `auth-credentials` |
| 3 | Look up model capabilities | `models-catalog` |
| 4 | Drive per-turn state machine | `turn-orchestrator` |
| 5 | Serve skill bodies | `iii-directory` |
| 6 | Assemble system prompt | `turn-orchestrator` |
| 7 | Stream tokens to client | `provider-*` |
| 8 | Policy-check tool calls | `policy-engine` |
| 9 | Human-in-the-loop approvals | `approval-gate` |
| 10 | Track LLM budget | `llm-budget` |
| 11 | Before/after tool call hooks | `hook-fanout` |
| 12 | Persist branching session tree | `session` |
| 13 | Compact context on overflow | `context-compaction` |
| 14 | Emit event stream for UI | `harness-meta` |
| 15 | Propagate OTel trace | Auto via Proxy wrapper |

### Latency Optimizations Demonstrated
- `hook-fanout` short-circuits `publish_collect` via subscriber-presence cache when no durable subscriber is registered: **~500ms saved per function call**
- `tearing_down` inlined into `finishSession()`: removes one durable queue hop per turn
- `context-compaction` subscribes to `agent::turn_end` instead of per-event stream: wakeups are per-turn, not per-event
- FSM collapsed from 11 states to 7 in a recent refactor with zero changes to neighboring workers

### Five Concrete Replacement Examples
- **Dynamic model catalog** -- register `models::list/get/supports` from a live provider API
- **New LLM provider** -- one worker registering `provider::<name>::stream` and `::complete`
- **Private skill store** -- register `directory::skills::get/list` backed by internal S3/docs
- **Custom system prompt** -- pass `system_prompt` to `run::start` to bypass default assembly
- **Slack approval surface** -- write a Slack worker calling `approval::resolve`; orchestrator unchanged

---

## Suggestions & Future Directions

1. **Worker registry expansion** -- `workers.iii.dev` is the current registry; more published workers means more reusable harness components for the ecosystem.
2. **Multi-language SDKs** -- Workers can theoretically be written in any language with an SDK; expanding beyond TypeScript/JavaScript would broaden adoption.
3. **Formal skill schema standard** -- Skills currently use an informal convention; a typed schema (JSON Schema or OpenAPI) per skill would enable validation and tooling.
4. **Community harness configurations** -- Shareable `config.yaml` presets (thin/research, thick/production, compliance-heavy) as templates in the repo.
5. **Open invitation** -- Discord at `discord.gg/iiidev` for community building.

---

## Key Links

- Engine: `github.com/iii-hq/iii`
- Workers monorepo (harness bundle): `github.com/iii-hq/workers/harness`
- Worker registry: `workers.iii.dev`
- Docs: `iii.dev/docs`

## Author & Organization

Mike Piccolo -- Founder & CEO, iiidevs (@iiidevs on X)
