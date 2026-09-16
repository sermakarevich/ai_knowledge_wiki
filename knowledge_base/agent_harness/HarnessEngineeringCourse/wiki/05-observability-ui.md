> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Observability, events, TUI

**In one sentence:** A dual-shape observability layer (flat `Event` trace plus OpenTelemetry (OTel) GenAI span tree, both recorded by `Tracer`) feeds a Textual two-pane terminal UI (TUI) and pure print renderers, making every model call, tool call, and verify step visible, replayable, and exportable.

## Key points

- The `Event` dataclass in `harness/observability.py:36` records each step with `kind` (`"llm" | "tool" | "verify"`), `label`, `seconds`, `tokens`, `args`, `result`, `cost`, `status`, and `turn`.
- The `Tracer` dataclass in `harness/observability.py:55` is additive (pass no tracer and the loop is unchanged) and carries `events`, `spans`, `exporter`, `on_event` live-UI hook (`harness/observability.py:58`), and a `_turn` index bumped by `turn_start` (`harness/observability.py:71`).
- Every `record_*` call emits one flat `Event` and one OTel span: `record_llm` adds a `chat` child span (`harness/observability.py:106`), `record_tool` adds an `execute_tool` child span (`harness/observability.py:204`), `record_verify` adds a custom `verify` span (`harness/observability.py:254`), `record_plan` adds a `plan` span (`harness/observability.py:283`), all nested under the current `invoke_agent` turn parent opened by `turn_start` (`harness/observability.py:77`).
- The span contract in `harness/events.py:1` hand-rolls OTel GenAI semantic-convention names (`gen_ai.operation.name`, `chat`/`execute_tool`/`invoke_agent` operations at `harness/events.py:33`, `CLIENT`/`INTERNAL` kinds at `harness/events.py:40`) instead of depending on `opentelemetry-sdk`, staying deterministic and offline with an optional exporter seam (`harness/events.py:93`).
- The exporter seam defaults to no-op `NullExporter` (`harness/events.py:99`), with `JsonlExporter` writing one JSON span per line (`harness/events.py:106`) and `ConsoleExporter` printing a one-line summary per span (`harness/events.py:118`); `Tracer.export()` hands assembled spans to it (`harness/observability.py:320`).
- The Textual `AgentTUI` in `ui/tui.py:150` runs the same `Agent` in a worker thread (`@work(thread=True)` at `ui/tui.py:385`), renders conversation plus live trace panes (`ui/tui.py:238`), bridges the blocking approval hook via `call_from_thread` + `threading.Event` (`ui/tui.py:413`), and surfaces the approval gate as `ApprovalModal` with unified-diff previews (`ui/tui.py:64`).
- Pure print renderers in `harness/render.py:1` (`render_plain` at `harness/render.py:23`, `render_json` at `harness/render.py:28`, `render_transcript` at `harness/render.py:39`) format the reply plus tracer totals with no `textual`/`ui` import, keeping the one-way `ui` → `harness` → `model` dependency intact.

---

## Flat event model

Defined in `harness/observability.py:35`:

```python
@dataclass
class Event:
    kind: str  # "llm" | "tool" | "verify"
    label: str
    seconds: float
    tokens: int = 0
    args: str = ""  # tool input
    result: str = ""  # tool output
    cost: float = 0.0  # USD for this step
    status: str = ""  # ok | denied | error | pass | fail
    turn: int = 0  # which user turn this step belongs to
```

- `status` (`harness/observability.py:44`) color-codes the trace via `_STATUS_COLOR` in `ui/tui.py:50`: `{"denied": "yellow", "error": "red", "fail": "red", "pass": "green", "ok": ""}`.
- `turn` (`harness/observability.py:45`) groups events per user turn; the TUI rebuilds the trace tree by turn in `_rebuild_trace` (`ui/tui.py:348`).
- Persistence is a plain dict round-trip: `dump_events` serializes via `asdict` (`harness/observability.py:324`) and `load_events` restores them, resuming turn numbering from the max stored turn (`harness/observability.py:328`).
- Aggregation and display: `totals()` counts llm/tool calls, sums tokens, cost, seconds (`harness/observability.py:334`); `timeline()` renders one line per event plus a totals footer (`harness/observability.py:343`).

## Tracer: dual emit, turn parenting, live hook

Defined in `harness/observability.py:54`:

```python
@dataclass
class Tracer:
    events: list[Event] = field(default_factory=list)
    model: str | None = None  # used to price llm calls
    on_event: Callable[[Event], None] | None = None  # live-UI hook
    spans: list[Span] = field(default_factory=list)
    exporter: SpanExporter = field(default_factory=NullExporter)
    provider_name: str = "openai"  # gen_ai.provider.name (OpenAI-compatible flavor)
    server_address: str | None = None
    server_port: int | None = None
    conversation_id: str | None = None  # our session id → gen_ai.conversation.id
    capture_content: bool = field(default_factory=_capture_content_default)
```

- `turn_start()` (`harness/observability.py:71`) increments `_turn`, generates `span-{seq}` via `_next_span_id` (`harness/observability.py:97`), and appends a root `invoke_agent` span named `f"invoke_agent {self.model or 'agent'}"` (`harness/observability.py:85`); its `duration_s` is filled lazily in `get_spans` as the sum of its children (`harness/observability.py:305`).
- `_emit` (`harness/observability.py:101`) appends to `events` and fires `on_event` so a live UI refreshes as each event lands.
- `record_llm` (`harness/observability.py:106`) prices via `cost_from_usage(request_model or self.model, usage)` (`harness/observability.py:119`), emits an `llm` event with `tokens=int(usage.get("total_tokens", 0))`, `cost`, `status="ok"` (`harness/observability.py:120`), then delegates to `_add_chat_span` (`harness/observability.py:131`).
- `_add_chat_span` (`harness/observability.py:142`) builds `chat` span attributes from `harness/events.py:44` names (`OPERATION_NAME`, `PROVIDER_NAME`, `REQUEST_MODEL`, `USAGE_INPUT_TOKENS`, `USAGE_OUTPUT_TOKENS`, `USAGE_COST` at `harness/observability.py:159`), plus optional `finish_reason` → `RESPONSE_FINISH_REASONS` (`harness/observability.py:167`), `response_id` → `RESPONSE_ID` (`harness/observability.py:169`), server/conversation ids (`harness/observability.py:171`), and opt-in message content (`harness/observability.py:177`); the span is `kind=events.CLIENT`, `name=f"chat {model}"` (`harness/observability.py:187`).
- `record_tool` (`harness/observability.py:204`) clamps captured I/O with `clamp(args, 120)` / `clamp(result, 120)` (`harness/observability.py:221`) to keep the trace small but replayable, sets `TOOL_NAME`/`TOOL_TYPE="function"` attributes (`harness/observability.py:227`), maps `status == "error"` to `ERROR_TYPE` (`harness/observability.py:236`), and appends an `execute_tool` span with `kind=events.INTERNAL`, `name=f"execute_tool {name}"` (`harness/observability.py:241`).
- `record_verify` (`harness/observability.py:254`) emits a `verify` event with `status="pass" if passed else "fail"` (`harness/observability.py:260`) and an `INTERNAL` span with custom non-standard `operation="verify"` (`harness/observability.py:270`) — OTel GenAI has no verify operation.
- `record_plan` (`harness/observability.py:283`) emits both a `plan` event (`harness/observability.py:291`) and an `INTERNAL` span with `operation=events.PLAN` (`harness/observability.py:292`), with caller-measured `duration_s` nested under the current turn.
- Content capture is privacy-first: `_capture_content_default()` (`harness/observability.py:48`) returns true only when env `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` is `1/true/yes/on` (`harness/observability.py:50`); when off, message bodies are omitted from span attributes.

## OTel span contract and exporters

- `Span` dataclass in `harness/events.py:72` with verbatim signature fields `span_id`, `parent_id`, `name`, `kind`, `operation`, `attributes`, `status="ok"`, `duration_s=0.0` (`harness/events.py:82`); `duration_s` is derived from tracer-measured seconds, never a fresh wall-clock read (`harness/events.py:78`).
- Operation constants (`harness/events.py:32`): `CHAT = "chat"`, `EXECUTE_TOOL = "execute_tool"`, `INVOKE_AGENT = "invoke_agent"`, `PLAN = "plan"`, `CREATE_AGENT = "create_agent"` (`harness/events.py:33`).
- Attribute-name constants are exact spec strings (`harness/events.py:43`): `OPERATION_NAME = "gen_ai.operation.name"`, `PROVIDER_NAME = "gen_ai.provider.name"`, `REQUEST_MODEL = "gen_ai.request.model"`, `USAGE_INPUT_TOKENS = "gen_ai.usage.input_tokens"`, `USAGE_OUTPUT_TOKENS = "gen_ai.usage.output_tokens"`, `TOOL_NAME = "gen_ai.tool.name"`, `CONVERSATION_ID = "gen_ai.conversation.id"`, `ERROR_TYPE = "error.type"` (`harness/events.py:44`); `USAGE_COST = "gen_ai.usage.cost"` is a custom extension — OTel has no dollar attribute (`harness/events.py:52`).
- Opt-in content attributes (`harness/events.py:65`): `SYSTEM_INSTRUCTIONS = "gen_ai.system_instructions"`, `INPUT_MESSAGES = "gen_ai.input.messages"`, `OUTPUT_MESSAGES = "gen_ai.output.messages"`, `TOOL_DEFINITIONS = "gen_ai.tool.definitions"` (`harness/events.py:66`).
- Exporter seam (`harness/events.py:92): `class SpanExporter(Protocol)` with `def export(self, spans: list[Span]) -> None: ...` (`harness/events.py:96`); `NullExporter.export` is a no-op keeping `verify` offline (`harness/events.py:102`); `JsonlExporter.__init__(self, path: str)` writes `json.dumps(asdict(span))` per line (`harness/events.py:109`); `ConsoleExporter.export` prints `[span] {operation} {name} {ms} {status} (parent=...)` (`harness/events.py:121`).

## Print renderers

Module contract in `harness/render.py:1`: pure formatting over messages plus `Tracer`, no `textual`/`ui` import.

- `def render_plain(reply: str) -> str:` returns the final answer as-is (`harness/render.py:23`).
- `def render_json(reply: str, tracer: Tracer | None, messages: list[dict]) -> str:` builds `{"reply": reply, "messages": len(messages), "totals": tracer.totals() if tracer is not None else {}}` and returns `json.dumps(payload, indent=2)` (`harness/render.py:28`).
- `def render_transcript(messages: list[dict], tracer: Tracer | None) -> str:` renders `{role}: {content}` per message, appending `[tool_calls: names]` from `m.get("tool_calls")` (`harness/render.py:42`), then `--- trace ---` plus `tracer.timeline()` when events exist (`harness/render.py:50`).

## TUI layout and trace pane

- `class AgentTUI(App):` (`ui/tui.py:150`) composes a header, a conversation pane (`#log` + `#prompt` input) and a trace pane (`#trace-tree` + `#trace-foot`) plus a footer (`ui/tui.py:238`); CSS fixes the trace column at `width: 46` (`ui/tui.py:153`).
- Trace icons (`ui/tui.py:51`): `_KIND_ICON = {"llm": "◆", "tool": "›", "verify": "✓", "plan": "▷"}`; `_span_label` renders `{icon} {label} {ms}` colorized by `_STATUS_COLOR` (`ui/tui.py:340`).
- `_rebuild_trace` (`ui/tui.py:348`) groups `agent.tracer.events` by `turn`, adds one `turn {n} · {ms}` node each, nests per-event nodes with `tokens · cost` / `args` / `→ result` leaves (`ui/tui.py:359`), and updates the footer to `{tokens} tok · {cost}` via `format_cost` (`ui/tui.py:367`).
- Header shows `⚙ {model} · session: {name} · skills: {n} · ctx {tokens}/{limit}` in `_refresh_header` (`ui/tui.py:261`); history rendering skips `Context file:` user messages (`ui/tui.py:269`).
- Streaming: `_mount_live_block` mounts an empty agent block with a dimmed reasoning line plus Markdown body (`ui/tui.py:299`); `_stream_delta(channel, text)` appends reasoning vs content tokens and clears reasoning once the answer begins (`ui/tui.py:314`); `_turn_done` finalizes the streamed block in place with the canonical reply so it is never duplicated (`ui/tui.py:397`).
- Turn execution runs off the UI thread: `@work(thread=True, exclusive=True) def _run_turn` with a `sink` bridging tokens via `call_from_thread(self._stream_delta, ...)` (`ui/tui.py:385`); `/plan` runs the orchestrator the same way with its own `turn_start` so the plan span lands in the trace pane (`ui/tui.py:450`).

## Approval modal and threading bridge

- `APPROVAL_TOOLS = CONFIG.approval_tools` (`ui/tui.py:49`) is the single editable-surface source of truth passed as `approval_required` when building the agent (`ui/tui.py:223`).
- `def approval_preview(name: str, args_json: str, workspace: Workspace | None) -> dict:` (`ui/tui.py:64`) returns `{"title", "kind", "body"}`: `bash` shows `args.get("command", "")` (`ui/tui.py:71`); `write_file`/`edit_file` compute `_unified_diff(current, new, path)` (`ui/tui.py:54`) or `(no change)`, with explicit failure previews (`edit will fail: no such file`, ``old`` must be non-empty, text-not-found at `ui/tui.py:86`); anything else echoes raw `args_json` (`ui/tui.py:113`).
- `class ApprovalModal(ModalScreen[bool]):` (`ui/tui.py:116`) binds `a` allow / `d`·`escape` deny (`ui/tui.py:119`), renders diff vs bash bodies with `Syntax` highlighting (`ui/tui.py:129`), notes `runs fail-closed · a allow · d deny` (`ui/tui.py:135`), and dismisses with `event.button.id == "allow"` (`ui/tui.py:140`).
- `AgentTUI._approve` (`ui/tui.py:413`) builds the preview, pushes the modal via `call_from_thread`, blocks on `threading.Event().wait()`, defaults to denied (`box.get("v", False)`), and echoes allowed diffs into the conversation via `_write_diff` (`ui/tui.py:428`).

## Sessions, commands, headless seam

- Agent construction in `_build_agent` (`ui/tui.py:207`) registers file tools on the worktree root, trusted `bash_tool(Sandbox(trusted=True, timeout=120))`, cross-session `search_memory_tool`, `delegate_tool`/`fan_out_tool`, and `Tracer(model=self.provider.model)` (`ui/tui.py:207`).
- Slash commands in `_handle_command` (`ui/tui.py:433`): `/reset` clears history + trace under the same name via `delete_session` + `_open_session` (`ui/tui.py:492`); `/new` opens `chat-{int(time.time())}` (`ui/tui.py:498`); `/plan <task>` runs the orchestrator off-thread (`ui/tui.py:439`); unknown commands hint ``try `/plan`, `/reset`, or `/new` `` (`ui/tui.py:448`).
- `def run_headless_turn(prompt: str, *, sessions_dir: str | None = None) -> dict:` (`ui/tui.py:507`) drives one real turn through a Textual pilot (`app.run_test()`), waits up to ~60s for `_busy` to clear, and returns `{"turns", "spans", "log_lines", "busy"}` counted from the trace tree and `.msg` blocks (`ui/tui.py:520`); it is the public seam so `tasks/` never imports textual itself (`ui/tui.py:508`).

**Covers:** component 05
