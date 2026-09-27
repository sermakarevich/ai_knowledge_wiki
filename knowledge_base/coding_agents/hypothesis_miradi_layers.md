# [Hypothesis] Maryam Miradi — 9 production AI-agent layers
- Source: https://x.com/MaryamMiradi/status/2102112004341154153
- Status: fetched 2026-09-24 | x.com direct (validated: body contains MaryamMiradi)
## Content
- Thesis: Claude Code reaches a working prototype fast; production is harder engineering — path from "Prototype coded by Claude" to "Operable Production AI Agent".
- Layer 1 — Scope Boundary: what the agent may/may not do; keeps prototype sprawl out of production.
- Layer 2 — Durable State: persisted state across runs so agents survive restarts and long tasks.
- Layer 3 — Context Policy: what context (retrieval, memory, tools) the agent sees and when; bounds cost and drift.
- Layer 4 — Action Contracts: typed, validated tool/action interfaces (cf. Model Context Protocol (MCP), PydanticAI-style schemas).
- Layer 5 — Runtime Authority: permission/approval model for side-effecting actions.
- Layer 6 — Failure Recovery: retries, compensation, and graceful degradation when tools/models fail.
- Layer 7 — Release Evals: gate releases on evaluation suites, not vibes; blocks regressions.
- Layer 8 — Runtime Tracing: observable traces/logs of agent decisions and tool calls for debugging.
- Layer 9 — Rollback + Ownership: versioned rollback path and a named owner on call.
- Finish state per infographic: agent that is controllable, measurable, recoverable, and auditable; illustrated with LangChain, OpenAI, PydanticAI, Google Agent Development Kit (ADK), and MCP logos.
## Why it was kept
- Maps to AI-coding team practice at layers 4 (contracts), 7 (release evals), 8 (tracing), 9 (rollback/ownership); layers 2, 3, 5, 6 partially map to fleet runtime concerns.
- Rest (solo-agent ops framing, framework logos) is out of scope: generic single-agent production checklist, not multi-agent coding-team evidence.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
