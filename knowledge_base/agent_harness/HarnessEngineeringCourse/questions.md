---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# HarnessEngineeringCourse — Retrieval Prompts

## Q1 (Section 1 — Agent loop, context delivery, instructions): Recite the per-turn drive sequence and the instruction layer composition with file:line numbers.

<details>
<summary>Answer</summary>

Each turn runs `send()` → `@path` injection via `deliver()` → `_run()` tool loop → verification gate → durable save (`harness/agent.py:137`).

The instruction layer is `system + AGENTS.md + skills menu`, joined with blank lines in `_system_text()` (`harness/agent.py:118`).

Supporting pieces: `deliver()` scans for `@path` and returns clamped `--- path ---` blocks (`harness/context.py:25`); `load_agents_md()` returns `''` when `AGENTS.md` is missing (`harness/instructions.py:19`); `Workspace._safe()` confines all reads/writes to root (`harness/workspace.py:33`).
</details>

## Q2 (Section 2 — Model seam, fake provider, pricing): Name the sole model entry point, the two call paths, and the pricing rule with file:line numbers.

<details>
<summary>Answer</summary>

The sole entry point is the free `chat()` function (`model/client.py:18`) — every model call goes through it.

`Provider` (`model/provider.py:78`) holds `base_url` / `model` / `api_key` plus optional `responder`; `chat()` calls `responder` when set, else `complete_openai` (`model/client.py:38`).

`complete_openai()` POSTs to `{base_url}/chat/completions` (`model/openai_compatible.py:59`) with blocking plus SSE streaming via `on_delta` (`model/openai_compatible.py:56`).

Offline path: `FakeProvider` (`model/fake.py:22`) / `fake()` (`model/fake.py:48`) with callable / per-turn-list / fixed-default replies (`model/fake.py:37`).

Pricing (`model/pricing.py:17`) maps model-id substrings to `(prompt, completion)` USD-per-1M rates; unknown/local models cost `0.0` (`model/pricing.py:26`).
</details>

## Q3 (Section 3 — Memory, compaction, limits, skills): Why does compaction summarize only the middle and snap cuts to whole-turn boundaries — what breaks if it summarizes the head or cuts mid-turn?

<details>
<summary>Answer</summary>

It keeps the head (system/instructions) and tail (recent work) intact and compresses only the middle into one `[summary of earlier conversation]` system note (`compaction.py:57`, `compaction.py:100`).

Boundaries snap to whole-turn cuts so an assistant `tool_calls` message is never orphaned from its `tool` results — summarizing the head would lose the task framing, and cutting mid-turn would leave a tool call without its result (or vice versa), corrupting replay and the next model step.

Companion guards: JSON-L (JSON Lines, one JSON object per line) sessions with atomic temp-file plus rename writes and bad-line-tolerant reads (`memory.py:33`, `memory.py:67`); keyword-only recall with no embeddings (`memory.py:122`); ~4 chars/token estimate and `…[truncated N chars]` clamping (`compaction.py:20`, `limits.py:15`); skills disclose only name + description, full body loaded on demand via `read_file` (`skills.py:40`, `skills.py:58`).
</details>

## Q4 (Section 4 — Sandbox, orchestrator, subagents, verification): State the sandbox default, the planner contract, the fan-out guard, and the verification success signal with file:line numbers.

<details>
<summary>Answer</summary>

Sandbox prefers hardened Docker (`--network none`, non-root, scoped workdir) and falls back to a scoped local subprocess when no Docker daemon exists (`sandbox.py:4`); only the Docker backend is a genuine containment boundary (network-none, non-root, cap-drop, memory + pid limits, read-only rootfs) (`sandbox.py:11`).

Planner asks for 2–4 short imperative steps as a JSON array only, falling back to the whole task as one step on parse failure (`orchestrator.py:21`); the orchestrator runs steps in order with per-step approval and retry (`orchestrator.py:3`).

Subagents are bounded loops with fresh isolated context returning only the answer (`subagents.py:3`); `fan_out` preserves task order and `fan_out_tool` rejects non-list `tasks` input to avoid spawning one subagent per character (`subagents.py:30`).

Verification runs candidate code plus an assertion check in a fresh scrubbed-env process, signalling success with a per-run random nonce printed only after the check completes (`verification.py:39`).
</details>

## Q5 (Section 5 — Observability, events, TUI): Why does every `record_*` call emit both a flat `Event` and an OTel span — what do you lose if you keep only one shape?

<details>
<summary>Answer</summary>

`Tracer` (`harness/observability.py:55`) is additive — pass no tracer and the loop is unchanged — and each `record_*` emits one flat `Event` (`kind`: `"llm" | "tool" | "verify"`, with `label`, `seconds`, `tokens`, `cost`, `status`, `turn` at `harness/observability.py:36`) plus one OTel span nested under the current `invoke_agent` turn parent (`harness/observability.py:77`): `record_llm` → `chat` span (`:106`), `record_tool` → `execute_tool` (`:204`), `record_verify` → `verify` (`:254`), `record_plan` → `plan` (`:283`).

Lose the flat `Event` and you lose the simple replayable totals and pure-print rendering (`render_plain` / `render_json` / `render_transcript` at `harness/render.py:23/28/39`, with no `textual` import). Lose the span tree and you lose the GenAI-convention parent/child timing (`gen_ai.operation.name`, `CLIENT`/`INTERNAL` kinds at `harness/events.py:33/40`) and the exporter seam (`NullExporter` default at `:99`, `JsonlExporter` at `:106`, `ConsoleExporter` at `:118`).

The Textual `AgentTUI` (`ui/tui.py:150`) needs both: conversation + live trace panes (`:238`), worker-thread agent (`:385`), `call_from_thread` + `threading.Event` approval bridge (`:413`).
</details>

## Q6 (Section 6 — Two-gate verification and course map): Your new harness project passes `ruff + mypy + pytest` but you have never run it against a real model — ship it or not, and which gate and working rule decide?

<details>
<summary>Answer</summary>

Do not ship. You have passed only `verify` (the offline floor: ruff format plus lint, mypy, pytest, smoke import) but not `accept` (the live truth against a real model) (`README.md:109-112`).

The course defines two gates precisely because "the tests pass" and "the agent actually works" are different claims (`README.md:107`).

The AGENTS.md working rule ships a change only when both gates are green and never claims a chapter works without a green `accept` (`AGENTS.md:16-17`).

Orientation facts for the fix: the spine is 15 chapters `ch-00` through `ch-14`, one primitive per module (`README.md:57-58`), each its own tagged commit (`README.md:114-120`); live checks/demos live in `ACCEPTANCE` / `DEMOS` dicts with folded chapters AND-ing all parts (`tasks/checks.py:3-8`); run via `uv run verify` / `accept ch-NN` / `demo ch-NN`, with `tasks/` as dev tooling separate from `model/` + `harness/` runtime (`README.md:129`).
</details>

## Q7 (Evaluation — see [[critical_thinking|Critical Analysis]]): The course's central rigor claim is that every chapter clears both `verify` and a live `accept ch-NN`. What single failure mode would let a chapter appear rigorously accepted while actually being weakly verified, and where in the codebase does that risk live?

<details>
<summary>Answer</summary>

The risk lives in the `ACCEPTANCE`/`DEMOS` registries themselves (`tasks/checks.py:15-16`), not in the two-gate mechanism. `accept ch-NN` only proves that the *registered* callable for that chapter returned `True` against a live model (`tasks/accept.py:13-26`) — nothing in the codebase checks that `_accept_chNN` actually asserts the chapter's claimed capability rather than a weaker proxy (e.g., "the agent returned non-empty text"). The two-gate rule (README.md:107-112) is genuinely enforced as a workflow — `accept` hard-fails with `no live acceptance check registered` when a check is missing (`tasks/accept.py:25`) — but it cannot detect a check that exists yet asserts too little. See [[critical_thinking|Critical Analysis]] § "Weaknesses and blind spots" for why this is a genuine, un-audited blind spot rather than a flaw in the gate design itself.
</details>
