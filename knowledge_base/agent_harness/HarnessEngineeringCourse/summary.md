> [[index|Wiki]] | [[digest|Digest]]

# Technical Analysis: HarnessEngineeringCourse

**Repository:** https://github.com/Satish137-GS/harnessengineering @ edac4be

---

## 1. Overview / What Problem It Solves

HarnessEngineeringCourse is a Python teaching codebase built around one thesis: the model only ever asks, the surrounding harness decides and executes. It is structured as a 15-chapter spine (`ch-00` through `ch-14`, README.md:57-58), each chapter introducing exactly one harness primitive — model seam, history, instructions, context delivery, tools/approval, compaction, skills, sandboxed execution, durable memory, orchestration, subagents, verification, observability, TUI — in its mature form, with every chapter tagged as its own commit (README.md:114-120). It is not a product; it is a worked example meant to be read chapter by chapter and rebuilt.

## 2. Architecture / Layering

```text
tasks/ (verify, accept ch-NN, demo ch-NN)   ── dev tooling, never imported by runtime
        │
ui/ (Textual TUI, ui/tui.py)
        │  imports
        ▼
harness/ (agent.py loop; context, tools, workspace, memory, compaction,
          limits, skills, sandbox, orchestrator, subagents, verification,
          observability, events, render)
        │  imports
        ▼
model/ (provider seam: provider.py, openai_compatible.py, fake.py,
        client.py, pricing.py)
```

Dependencies point strictly one way — `ui/` into `harness/` into `model/` — and the core agent loop never imports the UI (README.md:133-135, restated in AGENTS.md:25-29). `tasks/` sits outside this chain entirely as dev tooling (README.md:129). The single conversation owner is `Agent` (`harness/agent.py:52`); every other module is either a service it calls (`model.chat`, `Sandbox`, `memory.save_session`) or a tool it exposes to the model (`Workspace`, `search_memory_tool`, `delegate_tool`).

## 3. Macro Components

| Component | Module | Responsibility | Key file:line |
|---|---|---|---|
| Agent loop | `harness/agent.py` | Per-turn drive: context injection, tool loop, verification gate, durable save | `harness/agent.py:52`, `harness/agent.py:137` |
| Model seam | `model/client.py`, `model/provider.py` | Sole `chat()` entry point; config-driven dispatch to HTTP or fake | `model/client.py:18`, `model/provider.py:78` |
| Fake provider + pricing | `model/fake.py`, `model/pricing.py` | Offline deterministic responder; substring-matched USD pricing | `model/fake.py:22`, `model/pricing.py:17` |
| Context delivery | `harness/context.py` | `@path` file injection, clamped | `harness/context.py:25` |
| Instructions | `harness/instructions.py` | `AGENTS.md` auto-load, declared test-command parsing | `harness/instructions.py:19`, `harness/instructions.py:32` |
| Workspace | `harness/workspace.py` | Confined read/write/edit, git-worktree REPL sandboxing | `harness/workspace.py:33`, `harness/workspace.py:94` |
| Memory | `harness/memory.py` | JSON-L session + trace persistence, keyword episodic recall | `memory.py:33`, `memory.py:122` |
| Compaction + limits | `harness/compaction.py`, `harness/limits.py` | Middle-summarizing compaction with tool-safe cuts; per-item clamp | `compaction.py:57`, `limits.py:15` |
| Skills | `harness/skills.py` | Progressive-disclosure `SKILL.md` loader | `skills.py:40`, `skills.py:58` |
| Sandbox | `harness/sandbox.py` | Hardened Docker execution, local scoped fallback | `sandbox.py:71`, `sandbox.py:118` |
| Orchestrator | `harness/orchestrator.py` | Plan → gate → execute → retry multi-step runs | `orchestrator.py:21`, `orchestrator.py:58` |
| Subagents | `harness/subagents.py` | Isolated-context delegates; parallel fan-out | `subagents.py:17`, `subagents.py:30` |
| Verification | `harness/verification.py` | Nonce-guarded candidate-code execution against an oracle | `verification.py:39` |
| Observability | `harness/observability.py`, `harness/events.py` | Dual `Event`/OTel-span trace, exporter seam | `harness/observability.py:55`, `harness/events.py:72` |
| Render | `harness/render.py` | Pure plain/JSON/transcript formatters, no UI import | `harness/render.py:23` |
| TUI | `ui/tui.py` | Textual two-pane app: conversation + live trace, approval modal | `ui/tui.py:150`, `ui/tui.py:116` |
| Course gates | `tasks/verify.py`, `tasks/accept.py`, `tasks/checks.py`, `tasks/demo.py` | Offline deterministic gate; live-model gate; per-chapter registries | `tasks/verify.py:19`, `tasks/accept.py:13`, `tasks/checks.py:15` |

## 4. Data Flow

A turn enters through `Agent.send()` (`harness/agent.py:137`): tracer `turn_start()` fires, pre-turn `compact()` runs first so the later `turn_start = len(self.messages)` index stays valid for the verification gate (`harness/agent.py:145,153`), `@path` references are resolved by `deliver()` into clamped `--- path ---` context blocks and appended as user messages (`harness/context.py:25`), then the raw user text is appended. `_run()` drives the model until a final answer: it builds the payload via `_payload()` (system text first, then full history, `harness/agent.py:131`), calls `chat()` with tool specs, and on tool calls appends an assistant `tool_calls` message followed by one `tool` result per call, clamped via `clamp()` (`harness/agent.py:301`, `limits.py:15`); gated tools route through `_approved()`, failing closed to `"[denied by approval gate]"` without an approver (`harness/agent.py:98,313`). The loop is capped by `MAX_TOOL_STEPS` (`harness/agent.py:329`). After `_run()` returns, `_enforce_run()` checks the declared test command and `_save()` persists messages plus trace to disk (`harness/agent.py:156-157`, `memory.py:33,78`). `chat()` itself (`model/client.py:18`) either calls a `Provider.responder` (fake, for tests) or `complete_openai()`, which POSTs to `{base_url}/chat/completions` with blocking or SSE streaming (`model/openai_compatible.py:59,56`).

## 5. State Management

In-process conversation state is `Agent.messages`, a list rebuilt from disk on session resume (`harness/agent.py:85`) and bounded by `compact()`, which summarizes only the middle into one `[summary of earlier conversation]` system note, snapping cut boundaries so an assistant `tool_calls` message is never separated from its `tool` results (`compaction.py:57,100`) — if snapping would erase the middle, it returns history unchanged rather than corrupt the window (`compaction.py:57`). Cross-process durability is JSON-L (JSON Lines): `save_session`/`load_session` write via atomic temp-file-plus-rename and read tolerating bad lines, so a kill mid-write cannot corrupt resume (`memory.py:33,50,67,71`); trace events persist alongside under `traces/<session>.jsonl`, and `/reset` wipes both idempotently via `delete_session` with `missing_ok=True` (`memory.py:78,96`). Episodic state is recovered by `search_sessions`, a keyword-overlap scorer with no embeddings, excluding the live session (`memory.py:122`). Observability state is the `Tracer` dataclass (`harness/observability.py:55`) — additive, so omitting it changes nothing — carrying both a flat `events` list and an OTel `spans` list, restorable from disk via `load_events`/`dump_events` (`harness/observability.py:324,328`). UI-side state is the `AgentTUI` worker thread bridging tool approval back to the main thread via `call_from_thread` + `threading.Event` (`ui/tui.py:413`).

## 6. Tool Surface

Model-facing tools are built by `_coding_tools()` (`harness/agent.py:340`): file read/write/edit bound to a confined `Workspace` (`harness/workspace.py:33,64,77`), a trusted sandboxed `bash` tool (`sandbox.py:169`), `search_memory` (`memory.py:165`), and `delegate`/`fan_out` subagent tools (`subagents.py:38,56`). Every write/edit is routed through `Workspace._safe()`, which raises `ValueError` on any path that resolves outside the workspace root (`harness/workspace.py:33`). `fan_out_tool` explicitly validates its `tasks` argument is a list, rejecting a bare JSON string to avoid spawning one subagent per character (`subagents.py:64`). Gated tools (`APPROVAL_TOOLS`, `harness/agent.py:57`) require an `approve` callback; the TUI supplies one via `ApprovalModal` with unified-diff previews and a deny-by-default binding (`ui/tui.py:116,140`).

## 7. Verification Story

Two independent verification layers exist and are not confused with each other. Inside a turn, `_enforce_run()` checks the project's own declared test command, parsed from the first fenced block under a `## Testing` heading in `AGENTS.md` (`harness/instructions.py:32`). Standalone, `run_python()` (`verification.py:39`) is a self-check primitive: it concatenates candidate code, an assertion check, and a `print(nonce)` line with `nonce = f"VERIFIED-{uuid.uuid4().hex}"`, runs it in a fresh scrubbed-env process, and only counts `passed = proc.returncode == 0 and nonce in proc.stdout` — so code that prints a fixed sentinel and exits early cannot fake a pass (`verification.py:54,72`). At the course level, every chapter must clear two gates: `verify` (`tasks/verify.py:19`) — ruff format, ruff lint, mypy, pytest, smoke import, all offline and deterministic — and `accept ch-NN` (`tasks/accept.py:13`), which runs the real agent against a real model and looks up a registered check in `ACCEPTANCE: dict[str, Callable[[], bool]]` (`tasks/checks.py:15`). The rule is stated verbatim in README.md:107-112 and repeated as a working contract in AGENTS.md:16-19: ship only when both are green, never claim a chapter works without a green `accept`.

## 8. Error Handling

Failure modes favor explicit, harness-level containment over exceptions bubbling to the model. A missing `AGENTS.md` yields an empty string with no behavior change (`harness/instructions.py:19`); unreadable or binary `@path` files are skipped without crashing the turn (`harness/context.py:36`); a denied tool call returns the string `"[denied by approval gate]"` rather than raising (`harness/agent.py:98`); exceeding `MAX_TOOL_STEPS` returns `"error: exceeded tool-step budget"` instead of looping forever (`harness/agent.py:329`). Sandbox timeouts kill the whole process group via `os.killpg` and return exit code 124 plus `error: timed out` for both the Docker and local backends (`sandbox.py:49,134,162`). The orchestrator retries a failed step once (`_run_with_retry`, `attempts=2`) before recording `error: {exc}` and moving on rather than aborting the whole plan (`orchestrator.py:81,86`); its planner falls back to treating the whole task as one step when the model's JSON response fails to parse (`orchestrator.py:56`). `Workspace._safe()` is the one place that raises rather than degrades — a path escaping the workspace root is a hard `ValueError`, because silently containing it would be worse than failing loud (`harness/workspace.py:33`).

## 9. Testing

The course layout dedicates `tests/episodes/` to one behavioral test file per chapter (`test_ch01.py` .. `test_ch14.py`, README.md:124-131), run through the offline `verify` gate via `pytest`, with exit code 5 ("no tests collected") explicitly tolerated for the earliest chapters (`tasks/verify.py:23-31,59`). This offline suite is deliberately not sufficient proof of capability: `accept ch-NN` is the second, required gate, asserting the same chapter's behavior against a live model rather than a stub (`tasks/accept.py:13`, README.md:167-170 — "a stub returning the right shape proves nothing about a real model"). `FakeProvider`/`fake()` (`model/fake.py:22,48`) is what makes the offline half of this testable at all — callable, per-turn-list, or fixed-default replies stand in for a live model in `verify`-gated tests.

## 10. How to Extend

Extension follows the module-to-primitive map in README.md:82-103: swapping the model backend means implementing the `Provider` config contract consumed by `chat()` (`model/provider.py:78`, `model/client.py:38`), never touching `harness/agent.py`. Adding a tool means writing a `Tool`-returning function like `write_file_tool()`/`edit_file_tool()` (`harness/workspace.py:64,77`) and registering it into `_coding_tools()` (`harness/agent.py:340`). Adding a skill means dropping a `<name>/SKILL.md` directory under a skills root — no code change, since `load_skills()` globs and parses frontmatter at runtime (`skills.py:40`). Adding a course chapter means registering one `ACCEPTANCE["ch-NN"]` callable and one `DEMOS["ch-NN"]` callable in `tasks/checks.py` (`tasks/checks.py:15-16`), tagging a commit, and ensuring both `verify` and a genuinely live `accept ch-NN` pass before the chapter is considered done (README.md:107-112). The fastest orientation path for a new contributor is the primitive-to-module table itself (README.md:82-103) plus `harness/agent.py:137` (`send()`) as the one place every other module is wired together.

## 11. Verdict

This is a deliberately staged teaching codebase, not a production framework: each of the fifteen chapters adds exactly one primitive, owned by exactly one module, provable by exactly two gates. Its architectural discipline — one-way `ui → harness → model` imports, a single `Agent` conversation owner, an additive `Tracer` that changes nothing when absent, tool-safe compaction that refuses to corrupt the window rather than guess — is real and independently verifiable from source, not just asserted in the README. Its honest limits, several stated in its own docs: keyword-only memory recall with no embeddings (`memory.py:122`); a teaching-grade local sandbox fallback that is not a security boundary, unlike the hardened Docker path (`sandbox.py:11`); a coarse ~4-chars-per-token size estimate that can let the compaction door fire late (`compaction.py:20`); and a planner that silently degrades to "the whole task as one step" on any parse failure (`orchestrator.py:56`). None of these are surprising for a ~15-chapter course meant to be read and extended, not deployed; they would need to be revisited before any of these primitives graduate into unattended production use.
