> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Memory, compaction, limits, skills

**In one sentence:** Durable JSON-L (JSON Lines, one JSON object per line) session memory with keyword recall, middle-summarizing compaction with tool-safe cuts, per-item clamp limits, and progressively disclosed file-based skills together keep the context window (the limited text the model can see at once) usable across kills and long runs.

## Key points

- Sessions persist as append-friendly JSON-L (JSON Lines) via `save_session` / `load_session`, with atomic temp-file plus rename writes and bad-line-tolerant reads so a kill mid-write never corrupts resume (memory.py:33, memory.py:50, memory.py:67, memory.py:71).
- Trace events persist beside messages under `traces/<session>.jsonl` via `save_trace` / `load_trace`, and `/reset` wipes both files idempotently via `delete_session` (memory.py:78, memory.py:83, memory.py:89, memory.py:96).
- Episodic recall is keyword-only with no embeddings: `search_sessions` scores stored messages by query-term overlap and `search_memory_tool` exposes it as a `search_memory` tool that excludes the current session (memory.py:122, memory.py:165).
- Compaction summarizes only the middle into one `[summary of earlier conversation]` system note, keeping head and tail intact and snapping boundaries to whole-turn cuts so assistant `tool_calls` are never orphaned from their `tool` results (compaction.py:57, compaction.py:100).
- Context size is estimated cheaply at ~4 chars per token including tool-call argument JSON, and oversized single items are clamped at the door with a `…[truncated N chars]` marker (compaction.py:20, limits.py:15).
- Skills follow the agentskills.io directory layout `<dir>/<name>/SKILL.md` with YAML frontmatter (a `---` header block with `name` + `description`); only name and description enter the prompt and the model loads the full body on demand via `read_file` (skills.py:40, skills.py:58).

---

## Durable session state

Conversation is not state; the session boundary is the kill point and nothing survives unless written (memory.py:1).

Key signatures/configs quoted verbatim:

```python
DEFAULT_DIR = ".sessions"
```

```python
def _path(session_id: str, base: str | Path = DEFAULT_DIR) -> Path:
```

```python
def _write_jsonl_atomic(path: Path, rows: list[dict]) -> None:
```

```python
def _read_jsonl(path: Path) -> list[dict]:
```

```python
def save_session(session_id: str, messages: list[dict], base: str | Path = DEFAULT_DIR) -> None:
```

```python
def load_session(session_id: str, base: str | Path = DEFAULT_DIR) -> list[dict]:
```

Session IDs come from argv (command-line arguments), so `_path` keeps only the final path component `Path(session_id).name` to block `../secret` traversal writes or unlinks (memory.py:26). Writes use `tempfile.mkstemp` in the same directory plus `os.replace` so the reader never sees a partial file; `save_*` runs after every turn (memory.py:33). Reads skip blank lines and ignore `json.JSONDecodeError` lines so one half-written final line does not break resume in the REPL (Read-Eval-Print Loop, the interactive prompt) (memory.py:50). `list_sessions` globs `*.jsonl`, counts non-blank lines per file, and sorts most-recently-modified first for the sessions pane (memory.py:103).

## Traces and reset

```python
def _trace_path(session_id: str, base: str | Path = DEFAULT_DIR) -> Path:
```

```python
def save_trace(session_id: str, rows: list[dict], base: str | Path = DEFAULT_DIR) -> None:
```

```python
def load_trace(session_id: str, base: str | Path = DEFAULT_DIR) -> list[dict]:
```

```python
def delete_session(session_id: str, base: str | Path = DEFAULT_DIR) -> None:
```

Traces live in a `traces/` subdirectory so trace files are not picked up by `*.jsonl` session globs (memory.py:78). `delete_session` unlinks both the message file and the trace file with `missing_ok=True`, making reset idempotent (safe to repeat) whether or not anything was saved (memory.py:96).

## Episodic retrieval

A log is not memory until the right slice can be recovered (memory.py:7).

```python
def search_sessions(
    query: str,
    base: str | Path = DEFAULT_DIR,
    limit: int = CONFIG.memory_search_limit,
    *,
    exclude: str | None = None,
) -> list[dict]:
```

```python
def search_memory_tool(base: str | Path = DEFAULT_DIR, *, exclude: str | None = None) -> Tool:
```

`search_sessions` lowercases the query, strips surrounding punctuation via `string.punctuation` so `warehouse passcode?` still matches `passcode`, scores each stored message by how many query terms appear in `content`, sorts descending, and returns `{session, role, content}` up to `limit` (memory.py:122). `exclude` drops the current session so recall surfaces facts not already in live context (memory.py:122). The tool wrapper defines inner `search_memory(query: str) -> str`, joins hits as `[session] role: content`, returns `"no matching memory found"` on zero hits, and advertises `Tool(name="search_memory", description="Search past sessions for relevant facts by keyword.")` with a required `query` string parameter (memory.py:165).

## Compaction

When the conversation outgrows budget, summarize the middle and keep head and tail intact; a good summary preserves what the next turn needs, not merely fewer words (compaction.py:1).

```python
COMPACTION_PROMPT = CONFIG.compaction_prompt
```

```python
def estimate_tokens(messages: list[dict]) -> int:
```

```python
def _is_tool_call_assistant(m: dict) -> bool:
```

```python
def _clean_cut(messages: list[dict], i: int) -> bool:
```

```python
def compact(
    messages: list[dict],
    *,
    keep_head: int = 2,
    keep_tail: int = 4,
    model: str | None = None,
    provider: Provider | None = None,
) -> list[dict]:
```

`estimate_tokens` sums `len(content)` plus `len(json.dumps(tc))` for each entry in `m.get("tool_calls")`, then divides by 4; tool arguments such as a whole file body in `write_file` count toward the window or the compaction door fires late (compaction.py:20). `_clean_cut` rejects index `i` if `messages[i]` is `role == "tool"` or `messages[i-1]` is an assistant with `tool_calls`, because an OpenAI-compatible payload requires each assistant `tool_calls` message to be immediately followed by its results (compaction.py:39). `compact` returns unchanged when `len(messages) <= keep_head + keep_tail`, otherwise snaps `head_end` downward and `tail_start` downward until both are clean cuts; if snapping erases the middle (`head_end >= tail_start`) it returns history unchanged rather than corrupt the window (compaction.py:57). The middle transcript `role: content` lines are summarized via `chat` with the system `COMPACTION_PROMPT`, the same endpoint the turn uses, `max_tokens=512`, then reinserted as `{"role": "system", "content": f"[summary of earlier conversation]\n{summary}"}` between head and tail (compaction.py:89, compaction.py:100).

## Door limits

Hard per-item size limits apply before anything enters the prompt; a single huge file or tool output can drown the window (limits.py:1).

```python
MAX_ITEM_CHARS = CONFIG.max_item_chars  # re-export; the value lives in the editable surface
```

```python
def clamp(text: str, max_chars: int = MAX_ITEM_CHARS) -> str:
```

`clamp` returns text unchanged when within budget, otherwise returns `text[:max_chars]` plus `\n…[truncated {dropped} chars]` where `dropped = len(text) - max_chars` (limits.py:15). Clamping each item at the door is the cheapest defense against distraction, confusion, and poisoning (limits.py:1).

## Skills

A skill is a directory containing `SKILL.md` with YAML frontmatter (`name` + `description`) plus instructions; skills are not tools — a tool is a capability ("run pytest"), a skill is a procedure ("how we cut a release") (skills.py:1).

```python
@dataclass
class Skill:
    name: str
    description: str
    path: Path
```

```python
def _parse_frontmatter(text: str) -> dict[str, str]:
```

```python
def load_skills(directory: str | Path) -> list[Skill]:
```

```python
def skills_prompt(skills: list[Skill]) -> str:
```

`_parse_frontmatter` requires the first line to be `---`, collects only top-level `key: value` lines, skips indented nested lines, and stops at the closing `---` (skills.py:24). `load_skills` returns `[]` for a missing directory, otherwise sorts `*/SKILL.md` globs and defaults `name` to the parent directory name and `description` to `""` when frontmatter keys are absent (skills.py:40). `skills_prompt` returns `""` when empty, otherwise emits `You have skills available. When one applies, use the read_file tool to read its file, then follow it exactly:` followed by one `- {name}: {description} (file: {path})` line per skill, implementing progressive disclosure (only metadata advertised, body loaded on demand) (skills.py:58).

**Covers:** component 03
