> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agent loop, context delivery, instructions

**In one sentence:** The `Agent` class drives a tool-calling chat loop over a system prompt layered from project instructions, injected `@path` file context, and a confined workspace, with pluggable entry points for REPL and one-shot runs.

## Key points

- `Agent` wraps a model, provider, system prompt, tool registry, approval callback, skills, session, and tracer into one drive loop (`harness/agent.py:52`).
- Each turn runs `send()` → `@path` injection via `deliver()` → `_run()` tool loop → verification gate → durable save (`harness/agent.py:137`).
- The instruction layer is `system + AGENTS.md + skills menu`, joined with blank lines in `_system_text()` (`harness/agent.py:118`).
- `deliver()` scans user text for `@path` matches, reads each file, and returns clamped `--- path ---` context blocks (`harness/context.py:25`).
- `load_agents_md()` auto-loads `<directory>/AGENTS.md` or returns `''` so a missing file changes nothing (`harness/instructions.py:19`).
- `test_command()` parses the first fenced code line under a `## Testing` heading as the project's declared test command (`harness/instructions.py:32`).
- `Workspace` confines every read/write/edit to its root via `_safe()`, raising on escape (`harness/workspace.py:33`).
- `git_worktree()` gives the REPL a throwaway detached worktree of HEAD so real code runs while the checkout stays pristine (`harness/workspace.py:94`).

---

## Agent class and constructor

`Agent` is defined at `harness/agent.py:52`:

```python
class Agent:
    """A model wrapped in memory, a system prompt, context delivery, and tools."""
```

Constructor signature, quoted verbatim from `harness/agent.py:55`:

```python
def __init__(
    self,
    model: str | None = None,
    provider: Provider | None = None,
    system: str | None = None,
    agents_dir: str = ".",
    tools: ToolRegistry | None = None,
    approve: Callable[[str, str], bool] | None = None,
    approval_required: frozenset[str] | set[str] | None = None,
    context_limit: int = DEFAULT_CONTEXT_LIMIT,
    skills: list[Skill] | None = None,
    session: str | None = None,
    sessions_dir: str = DEFAULT_DIR,
    verify_attempts: int = CONFIG.verify_attempts,
    require_run: bool = CONFIG.require_run,
    tracer: Tracer | None = None,
) -> None:
```

Behavioral knobs are re-exports of the editable config surface (`harness/agent.py:44`):

```python
DEFAULT_SYSTEM = CONFIG.system_prompt
MAX_TOOL_STEPS = CONFIG.max_tool_steps
DEFAULT_CONTEXT_LIMIT = CONFIG.default_context_limit  # ~tokens; compact above this
APPROVAL_TOOLS = CONFIG.approval_tools  # tools the gate guards
CODE_EXTENSIONS = CONFIG.code_extensions
```

Session resume loads prior conversation from disk when a session id is given (`harness/agent.py:85`), and restores the persisted trace into the tracer when both tracer and session exist (`harness/agent.py:95`).

## Turn lifecycle: send

`send()` is the per-turn entry point (`harness/agent.py:137`):

```python
def send(self, user_text: str, *, on_delta: OnDelta | None = None) -> str:
```

It performs, in order: tracer `turn_start()` (`harness/agent.py:144`), pre-turn compaction (`harness/agent.py:149`), `@path` block injection as `{"role": "user", "content": f"Context file:\n{block}"}` messages (`harness/agent.py:150`), appending the raw user text (`harness/agent.py:152`), snapshotting `turn_start = len(self.messages)` (`harness/agent.py:153`), running the tool loop via `_run()` (`harness/agent.py:154`), enforcing the test-run gate via `_enforce_run()` (`harness/agent.py:156`), and persisting state via `_save()` (`harness/agent.py:157`).

Compaction runs before the turn's messages are appended so the `turn_start` index stays valid for the verification gate (`harness/agent.py:145`).

## Tool loop: _run

`_run()` drives the model until it returns a final answer (`harness/agent.py:277`):

```python
def _run(self, on_delta: OnDelta | None = None) -> str:
```

Each iteration builds the payload via `_payload()`, calls `chat()` with tool specs, records token usage and an LLM trace span, then either executes returned tool calls or appends the final assistant message (`harness/agent.py:283`). Tool execution appends an assistant `tool_calls` message followed by one `tool` result message per call, clamped via `clamp()` (`harness/agent.py:301`). Gated tools go through `_approved()` (`harness/agent.py:313`); without an approver the gate fails closed and returns `"[denied by approval gate]"` (`harness/agent.py:98`). The loop is bounded by `MAX_TOOL_STEPS` and returns `"error: exceeded tool-step budget"` on exhaustion (`harness/agent.py:329`).

## Payload and instruction layering

`_payload()` puts the composed system text first, then the full history (`harness/agent.py:131`):

```python
def _payload(self) -> list[dict]:
    """System prompt first (if any), then the full conversation history."""
```

`_system_text()` layers `self.system`, `load_agents_md(self.agents_dir)`, and `skills_prompt(self.skills)`, dropping empty parts (`harness/agent.py:118`):

```python
def _system_text(self) -> str:
    """Instruction layer = system prompt + project AGENTS.md + skills menu."""
```

`agents_dir` records where `AGENTS.md` is auto-loaded from (`harness/agent.py:75`).

## Context delivery: @path injection

`deliver()` returns one context block per readable `@path` reference (`harness/context.py:25`):

```python
def deliver(user_text: str) -> list[str]:
```

The attach pattern is compiled from config at the use site (`harness/context.py:22`):

```python
_ATTACH = re.compile(CONFIG.attach_pattern)
```

Each match is read from disk, prefixed with `--- {path} ---`, and clamped so a huge file cannot flood the window (`harness/context.py:39`). Unreadable or binary files are skipped without crashing the turn (`harness/context.py:36`).

## Project instructions: AGENTS.md

`load_agents_md()` returns the directory's `AGENTS.md` contents or `''` (`harness/instructions.py:19`):

```python
def load_agents_md(directory: str | Path = ".") -> str:
```

`test_command()` extracts the declared test command — the first line of the first fenced block under a `## Testing` heading — or `None` when absent (`harness/instructions.py:32`):

```python
def test_command(directory: str | Path = ".") -> str | None:
```

The heading matcher, quoted verbatim (`harness/instructions.py:27`):

```python
_TESTING_RE = re.compile(
    r"^##\s+Test(?:ing|s)?\b.*?\n```[a-zA-Z0-9]*\n\s*([^\n`]+)", re.MULTILINE | re.DOTALL
)
```

The layer is additive: no file means an empty string and unchanged behavior (`harness/instructions.py:9`).

## Workspace confinement

`Workspace` owns a directory whose files survive across calls (`harness/workspace.py:26`):

```python
def __init__(self, root: str | Path | None = None) -> None:
```

A missing root defaults to a fresh `tempfile.mkdtemp(prefix="workspace-")` scratch dir; otherwise the given root is resolved and created (`harness/workspace.py:27`). Path safety is enforced by `_safe()`, which resolves `root / path` and raises `ValueError(f"path escapes workspace: {path}")` on escape (`harness/workspace.py:33`).

Core operations, all routed through `_safe()`:

```python
def write(self, path: str, content: str) -> str:
def read(self, path: str) -> str:
def edit(self, path: str, old: str, new: str) -> str:
```

`write()` creates parents and reports `wrote {path} ({len(content)} chars)` (`harness/workspace.py:39`); `read()` returns file text or `error: no such file: {path}` (`harness/workspace.py:45`); `edit()` replaces the first occurrence of `old` with `new`, rejecting empty `old` and missing text with explicit error strings (`harness/workspace.py:49`).

Model-facing tools wrap the workspace methods: `write_file_tool()` (`harness/workspace.py:64`) and `edit_file_tool()` (`harness/workspace.py:77`) each return a `Tool` with JSON-schema parameters bound to `ws.write` / `ws.edit`.

## Entry points: REPL and one-shot

`_coding_tools()` builds the mature toolset rooted at a workspace: default tools plus read/write/edit file tools, a trusted sandboxed bash tool, memory search, and delegate/fan-out subagent tools (`harness/agent.py:340`). `run_once()` runs exactly one non-interactive turn and renders it as `plain`, `json`, or `transcript` (`harness/agent.py:360`); it is stateless by default (`session=None`) and operates on the real `workspace_root` (`harness/agent.py:384`). `main()` parses an optional prompt plus `--format`, `--yes`, and `--context-limit` flags (`harness/agent.py:419`); a prompt selects print mode, otherwise the interactive REPL starts (`harness/agent.py:451`). The REPL works in a git worktree when inside a repo (else a scratch dir), prompts per-call for gated-tool approval, streams tokens, surfaces compaction, and prints a trace timeline after each turn (`harness/agent.py:468`).

`git_worktree()` creates an ephemeral detached worktree of HEAD and returns `(Workspace(worktree), cleanup)` (`harness/workspace.py:94`); it returns `None` outside a git repo (`harness/workspace.py:111`), syncs uv-project deps once with a bounded 120s offline sync (`harness/workspace.py:129`), and cleans up with `worktree remove --force` (`harness/workspace.py:133`).

**Covers:** component 01
