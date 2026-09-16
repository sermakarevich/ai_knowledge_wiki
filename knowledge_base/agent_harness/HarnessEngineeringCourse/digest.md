> [[index|Wiki]] | [[summary|Summary]]

# HarnessEngineeringCourse — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-agent-core|Agent loop, context delivery, instructions]]

**In one sentence:** The `Agent` class drives a tool-calling chat loop over a system prompt layered from project instructions, injected `@path` file context, and a confined workspace, with pluggable entry points for REPL and one-shot runs.

- `Agent` wraps a model, provider, system prompt, tool registry, approval callback, skills, session, and tracer into one drive loop (`harness/agent.py:52`).
- Each turn runs `send()` → `@path` injection via `deliver()` → `_run()` tool loop → verification gate → durable save (`harness/agent.py:137`).
- The instruction layer is `system + AGENTS.md + skills menu`, joined with blank lines in `_system_text()` (`harness/agent.py:118`).
- `deliver()` scans user text for `@path` matches, reads each file, and returns clamped `--- path ---` context blocks (`harness/context.py:25`).
- `load_agents_md()` auto-loads `<directory>/AGENTS.md` or returns `''` so a missing file changes nothing (`harness/instructions.py:19`).
- `test_command()` parses the first fenced code line under a `## Testing` heading as the project's declared test command (`harness/instructions.py:32`).
- `Workspace` confines every read/write/edit to its root via `_safe()`, raising on escape (`harness/workspace.py:33`).
- `git_worktree()` gives the REPL a throwaway detached worktree of HEAD so real code runs while the checkout stays pristine (`harness/workspace.py:94`).

## 2. [[wiki/02-model-seam|Model seam, fake provider, pricing]]

**In one sentence:** All model access goes through the free `chat()` function dispatched by `Provider` config, with an OpenAI-compatible HTTP path and a deterministic fake responder plus substring-matched USD pricing.

- The `chat()` seam in `model/client.py:18` is the sole entry point — every model call in the course goes through it (`model/client.py:1`).
- `Provider` in `model/provider.py:78` is pure config (`base_url` / `model` / `api_key`) plus an optional `responder` callable; `chat()` calls `responder` when set, else `complete_openai` (`model/client.py:38`).
- `complete_openai()` in `model/openai_compatible.py:23` POSTs to `{base_url}/chat/completions` (`model/openai_compatible.py:59`) and supports blocking plus SSE streaming via `on_delta` (`model/openai_compatible.py:56`).
- `FakeProvider` in `model/fake.py:22` and `fake()` in `model/fake.py:48` provide the offline second implementation: callable / per-turn list / fixed default replies (`model/fake.py:37`).
- `LLMResponse` in `model/provider.py:68` normalizes all results to `content` / `reasoning` / `tool_calls` / `usage` / `finish_reason` / `raw`.
- Pricing in `model/pricing.py:17` maps model-id substrings to `(prompt, completion)` USD-per-1M rates; unknown/local models cost `0.0` (`model/pricing.py:26`).
- Package surface is re-exported in `model/__init__.py:12` (`chat`, `Provider`, `FakeProvider`, `fake`, `complete_openai`, pricing helpers, presets, defaults).

## 3. [[wiki/03-memory-skills|Memory, compaction, limits, skills]]

**In one sentence:** Durable JSON-L (JSON Lines, one JSON object per line) session memory with keyword recall, middle-summarizing compaction with tool-safe cuts, per-item clamp limits, and progressively disclosed file-based skills together keep the context window (the limited text the model can see at once) usable across kills and long runs.

- Sessions persist as append-friendly JSON-L (JSON Lines) via `save_session` / `load_session`, with atomic temp-file plus rename writes and bad-line-tolerant reads so a kill mid-write never corrupts resume (memory.py:33, memory.py:50, memory.py:67, memory.py:71).
- Trace events persist beside messages under `traces/<session>.jsonl` via `save_trace` / `load_trace`, and `/reset` wipes both files idempotently via `delete_session` (memory.py:78, memory.py:83, memory.py:89, memory.py:96).
- Episodic recall is keyword-only with no embeddings: `search_sessions` scores stored messages by query-term overlap and `search_memory_tool` exposes it as a `search_memory` tool that excludes the current session (memory.py:122, memory.py:165).
- Compaction summarizes only the middle into one `[summary of earlier conversation]` system note, keeping head and tail intact and snapping boundaries to whole-turn cuts so assistant `tool_calls` are never orphaned from their `tool` results (compaction.py:57, compaction.py:100).
- Context size is estimated cheaply at ~4 chars per token including tool-call argument JSON, and oversized single items are clamped at the door with a `…[truncated N chars]` marker (compaction.py:20, limits.py:15).
- Skills follow the agentskills.io directory layout `<dir>/<name>/SKILL.md` with YAML frontmatter (a `---` header block with `name` + `description`); only name and description enter the prompt and the model loads the full body on demand via `read_file` (skills.py:40, skills.py:58).

## 4. [[wiki/04-execution|Sandbox, orchestrator, subagents, verification]]

**In one sentence:** The model only ever asks while the harness executes: sandboxed shell commands, planned-and-gated multi-step runs, parallel subagents with isolated context, and nonce-guarded code verification close the loop.

- The sandbox prefers hardened Docker (`--network none`, non-root, scoped workdir) and falls back to a scoped local subprocess when no Docker daemon is available (sandbox.py:4).
- The Docker backend is a genuine containment boundary (network-none, non-root, cap-drop, memory + pid limits, read-only rootfs) while the local fallback is teaching-grade, not a security boundary (sandbox.py:11).
- The orchestrator plans a task into steps, runs them in order through an agent, gates each step with approval, and retries on failure (orchestrator.py:3).
- The planner prompt asks for 2-4 short imperative steps returned as a JSON array only, falling back to the whole task as one step on parse failure (orchestrator.py:21).
- Subagents are bounded loops with fresh isolated context and tools that return only the answer, never the transcript, with independent subtasks fanning out in parallel (subagents.py:3).
- `fan_out` preserves task order and `fan_out_tool` rejects non-list `tasks` input to avoid spawning one subagent per character (subagents.py:30).
- Verification runs candidate code plus an assertion check in a fresh scrubbed-env process, with success signalled by a per-run random nonce printed only after the check completes (verification.py:39).

## 5. [[wiki/05-observability-ui|Observability, events, TUI]]

**In one sentence:** A dual-shape observability layer (flat `Event` trace plus OpenTelemetry (OTel) GenAI span tree, both recorded by `Tracer`) feeds a Textual two-pane terminal UI (TUI) and pure print renderers, making every model call, tool call, and verify step visible, replayable, and exportable.

- The `Event` dataclass in `harness/observability.py:36` records each step with `kind` (`"llm" | "tool" | "verify"`), `label`, `seconds`, `tokens`, `args`, `result`, `cost`, `status`, and `turn`.
- The `Tracer` dataclass in `harness/observability.py:55` is additive (pass no tracer and the loop is unchanged) and carries `events`, `spans`, `exporter`, `on_event` live-UI hook (`harness/observability.py:58`), and a `_turn` index bumped by `turn_start` (`harness/observability.py:71`).
- Every `record_*` call emits one flat `Event` and one OTel span: `record_llm` adds a `chat` child span (`harness/observability.py:106`), `record_tool` adds an `execute_tool` child span (`harness/observability.py:204`), `record_verify` adds a custom `verify` span (`harness/observability.py:254`), `record_plan` adds a `plan` span (`harness/observability.py:283`), all nested under the current `invoke_agent` turn parent opened by `turn_start` (`harness/observability.py:77`).
- The span contract in `harness/events.py:1` hand-rolls OTel GenAI semantic-convention names (`gen_ai.operation.name`, `chat`/`execute_tool`/`invoke_agent` operations at `harness/events.py:33`, `CLIENT`/`INTERNAL` kinds at `harness/events.py:40`) instead of depending on `opentelemetry-sdk`, staying deterministic and offline with an optional exporter seam (`harness/events.py:93`).
- The exporter seam defaults to no-op `NullExporter` (`harness/events.py:99`), with `JsonlExporter` writing one JSON span per line (`harness/events.py:106`) and `ConsoleExporter` printing a one-line summary per span (`harness/events.py:118`); `Tracer.export()` hands assembled spans to it (`harness/observability.py:320`).
- The Textual `AgentTUI` in `ui/tui.py:150` runs the same `Agent` in a worker thread (`@work(thread=True)` at `ui/tui.py:385`), renders conversation plus live trace panes (`ui/tui.py:238`), bridges the blocking approval hook via `call_from_thread` + `threading.Event` (`ui/tui.py:413`), and surfaces the approval gate as `ApprovalModal` with unified-diff previews (`ui/tui.py:64`).
- Pure print renderers in `harness/render.py:1` (`render_plain` at `harness/render.py:23`, `render_json` at `harness/render.py:28`, `render_transcript` at `harness/render.py:39`) format the reply plus tracer totals with no `textual`/`ui` import, keeping the one-way `ui` → `harness` → `model` dependency intact.

## 6. [[wiki/06-gates-course|Two-gate verification and course map]]

**In one sentence:** Every chapter passes an offline deterministic gate (`verify`) and a live-model gate (`accept`), across a 15-chapter spine where each chapter adds one harness primitive owned by one module.

- The course defines two gates because "the tests pass" and "the agent actually works" are different claims (README.md:107).
- `verify` is the offline floor — ruff format plus lint, mypy, pytest, smoke import — while `accept` is the live truth against a real model (README.md:109-112).
- The spine is 15 chapters `ch-00` through `ch-14`, each introducing one harness primitive in its mature form (README.md:57-58).
- Each chapter is its own tagged commit, so `git checkout ch-05` shows the project at chapter 5 and `git checkout main` returns to latest (README.md:114-120).
- Live checks and demos are registered per chapter in two dicts, `ACCEPTANCE` and `DEMOS`, with folded chapters AND-ing all parts so no proven capability is lost (tasks/checks.py:3-8).
- The `tasks/` package is dev tooling only, invoked as `uv run verify` / `accept ch-NN` / `demo ch-NN`, separate from the `model/` and `harness/` runtime (README.md:129).
- The AGENTS.md working rule ships a change only when both gates are green and never claims a chapter works without a green `accept` (AGENTS.md:16-17).

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Drive every task through a tool-calling agent loop with layered instructions and a confined workspace.
2. Route all model access through one provider seam with an offline fake and substring pricing.
3. Sustain long runs with durable JSON-L memory, tool-safe compaction, and on-demand skills.
4. Let the model ask while the harness executes via sandbox, orchestrator, subagents, and nonce-guarded verification.
5. Make each step visible through dual event/span observability feeding the TUI and print renderers.
6. Prove each primitive with offline verify plus live-model accept across the 15-chapter spine.
<!-- FIVE_MOVES_END -->
