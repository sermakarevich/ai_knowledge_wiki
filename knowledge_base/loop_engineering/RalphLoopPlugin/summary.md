# Technical Analysis: ralph-loop

**Repository:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop
**Version analyzed:** 1.0.0
**Date:** 2026-06-22

---

## 1. Overview / What Problem It Solves

Claude Code sessions are inherently single-shot: the model works on a task, produces output, and exits. For tasks that require iteration -- writing a test suite, refactoring a module, building a prototype to a spec -- there is no built-in mechanism to have Claude review its own previous output and try again without manual intervention.

Ralph Loop solves this by exploiting Claude Code's `Stop` hook to intercept every exit attempt and re-inject the original prompt. The result is an autonomous iterative loop where Claude reads its own prior file changes and git history on each pass, improving toward a declared completion criterion. The primary user is a developer who wants to run a well-defined, self-verifiable task (tests pass, linter clean, build succeeds) without supervising each iteration.

The plugin is named after the "Ralph Wiggum technique" -- described internally as "deterministically bad in an undeterministic world" -- the idea being that repeated, predictable prompting against a stable workspace eventually converges to a correct result.

---

## 2. High-Level Architecture

```
Developer
    │
    ▼
/ralph-loop <PROMPT> [--max-iterations N] [--completion-promise TEXT]
    │
    ▼
setup-ralph-loop.sh
    │  writes .claude/ralph-loop.local.md (state file)
    │  emits PROMPT to Claude
    ▼
Claude Code session (iteration 1)
    │  works on task, modifies files, attempts exit
    ▼
Stop hook fires → stop-hook.sh reads stdin (HOOK_INPUT JSON)
    │
    ├─ state file missing? → allow exit (no active loop)
    ├─ session_id mismatch? → allow exit (wrong session)
    ├─ max iterations reached? → delete state file, allow exit
    ├─ <promise> tag matches completion_promise? → delete state file, allow exit
    │
    └─ otherwise → increment iteration in state file
                   return JSON { decision:"block", reason:<PROMPT>, systemMessage:... }
                       │
                       ▼
               Claude Code re-runs with same PROMPT
               (sees updated files + git history from previous iteration)
```

**Data flow (one end-to-end path):**

1. User invokes `/ralph-loop "Build a REST API" --completion-promise "API COMPLETE" --max-iterations 20`.
2. `setup-ralph-loop.sh` creates `.claude/ralph-loop.local.md` with YAML frontmatter (`active`, `iteration`, `session_id`, `max_iterations`, `completion_promise`) and the raw prompt text after the closing `---`.
3. Claude receives the prompt, executes tool calls, writes files, potentially commits to git, and calls exit.
4. `stop-hook.sh` reads the hook JSON from stdin (contains `session_id` and `transcript_path`), parses the state file, increments `iteration`, reads the last 100 assistant lines from the JSONL transcript to check for `<promise>` tags.
5. If no completion signal, the hook returns `{"decision":"block","reason":"<PROMPT>","systemMessage":"🔄 Ralph iteration 2 | ..."}` which causes Claude Code to restart with the same prompt.
6. Claude on iteration 2 observes modified files from iteration 1 and attempts to improve. State file tracks current iteration number throughout.

Persistent state lives in `.claude/ralph-loop.local.md` (a markdown file with YAML frontmatter) in the project's working directory. The JSONL transcript lives in a Claude Code-managed path passed at runtime via `HOOK_INPUT`.

---

## 3. The State File

The central domain abstraction is the state file at `.claude/ralph-loop.local.md`. It carries all loop control state between hook invocations.

**Schema (YAML frontmatter + body):**

```yaml
---
active: true
iteration: 1                         # current iteration counter (1-based)
session_id: <CLAUDE_CODE_SESSION_ID> # session isolation guard
max_iterations: 20                   # 0 = unlimited
completion_promise: "API COMPLETE"   # null = no completion check
started_at: "2026-06-22T10:00:00Z"
---

Build a REST API for todos            # raw prompt text (everything after second ---)
```

The stop hook reads this file on every exit attempt. The only mutable field is `iteration`, updated atomically via a `sed` + temp-file-rename pattern (`stop-hook.sh`). All other fields are written once at setup time and treated as read-only. The prompt body after the second `---` is extracted with `awk '/^---$/{i++; next} i>=2'` -- a pattern that correctly handles `---` sequences inside the prompt itself.

Knobs:
- `max_iterations: 0` disables the iteration limit.
- `completion_promise: null` disables promise checking (loop runs forever).
- `session_id` is populated from `$CLAUDE_CODE_SESSION_ID`; if empty in a legacy state file, session isolation is skipped.

---

## 4. LLM / External Service Integration

Ralph Loop does not call an LLM or any external API. It is a pure control-plane plugin for Claude Code -- the LLM is Claude Code itself, acting as the caller and sole executor. The plugin's role is to prevent the session from terminating and to feed the same prompt back into it.

The only runtime dependencies are:
- `bash` (>= 4 for `[[ ]]` and arrays)
- `jq` -- parses the hook input JSON from stdin and builds the block response JSON
- `perl` -- used for multi-line `<promise>` tag extraction (one-liner with `-0777`)
- `sed`, `awk`, `grep` -- frontmatter parsing
- `date` -- ISO-8601 timestamp at setup

No API keys, no env vars for external services. `CLAUDE_CODE_SESSION_ID` is set by Claude Code itself.

---

## 5. The Iteration Pipeline

**Step 1 -- Setup (`scripts/setup-ralph-loop.sh`)**

`/ralph-loop` invokes `setup-ralph-loop.sh` via an `allowed-tools` declaration in `commands/ralph-loop.md`. The script parses CLI arguments (`--max-iterations`, `--completion-promise`, positional prompt words), validates inputs (non-empty prompt, numeric `max_iterations`), and writes the state file. It prints an activation banner and re-emits the prompt, which Claude Code receives as its first task.

**Step 2 -- First iteration**

Claude receives the prompt and works with full tool access. It modifies files, possibly commits to git, and eventually calls exit.

**Step 3 -- Stop hook evaluation (`hooks/stop-hook.sh`)**

Guard checks in order:
1. State file existence -- missing file means no active loop, `exit 0`.
2. Session ID match -- prevents a loop started in one session from blocking another.
3. State file validation -- `ITERATION` and `MAX_ITERATIONS` must be `=~ ^[0-9]+$`; corrupted files trigger cleanup and graceful stop.
4. Max iterations check -- if `ITERATION >= MAX_ITERATIONS` (and limit > 0), delete state and `exit 0`.
5. Transcript read -- pulls `transcript_path` from hook JSON, greps for `"role":"assistant"`, takes last 100 such lines, runs `jq -rs` to extract the last text block.
6. Promise check -- uses `perl -0777` to extract text inside `<promise>...</promise>`; compares with `=` (literal, not glob) against `COMPLETION_PROMISE`.
7. Loop continuation -- increments `iteration` (sed + atomic mv), emits `{"decision":"block","reason":"<PROMPT>","systemMessage":"..."}` via `jq -n`.

**Step 4 -- Cancellation (`commands/cancel-ralph.md`)**

`/cancel-ralph` instructs Claude to read the iteration count, delete `.claude/ralph-loop.local.md`, and confirm cancellation. The next exit attempt succeeds because the state file is gone.

---

## 6. Key Files

| File | Lines (approx.) | What It Does |
|------|-----------------|--------------|
| `hooks/stop-hook.sh` | ~215 | Core loop engine: reads hook input, validates state, checks completion, blocks or allows exit |
| `scripts/setup-ralph-loop.sh` | ~145 | Parses CLI args, writes state file, emits activation banner and initial prompt |
| `commands/ralph-loop.md` | ~20 | Slash command definition; invokes setup script, restricts allowed tools, carries loop instructions to Claude |
| `commands/cancel-ralph.md` | ~15 | Slash command definition; instructs Claude to delete the state file |
| `commands/help.md` | ~40 | User-facing help text |
| `hooks/hooks.json` | 12 | Hook registration: maps `Stop` event to `stop-hook.sh` |
| `.claude-plugin/plugin.json` | ~8 | Plugin manifest: name `ralph-loop`, version 1.0.0, author Anthropic |
| `README.md` | ~120 | Full usage docs, philosophy, best practices, Windows notes |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| `bash` | >= 4 (implied) | Script runtime for setup and stop hook |
| `jq` | any (system) | Parse hook input JSON; build block response JSON |
| `perl` | any (system) | Multi-line `<promise>` tag extraction in stop hook |
| `sed` | POSIX | Frontmatter parsing and iteration counter update |
| `awk` | POSIX | Extract prompt body after frontmatter |
| `grep` | POSIX | Detect assistant lines in JSONL transcript |
| `date` | POSIX | ISO-8601 `started_at` timestamp |

No `pyproject.toml`, `package.json`, or other language manifest. All dependencies are standard Unix CLI tools expected on macOS and Linux.

---

## 8. CLI / Usage Surface

**Entry points**

| Command | File | What It Does |
|---------|------|--------------|
| `/ralph-loop` | `commands/ralph-loop.md` | Start an iterative loop in current session |
| `/cancel-ralph` | `commands/cancel-ralph.md` | Cancel active loop by deleting state file |

Both have `hide-from-slash-command-tool: "true"` -- accessible as user-typed slash commands but not surfaced in Claude's internal tool list.

**Flags for `/ralph-loop`:**

```bash
/ralph-loop PROMPT [OPTIONS]

Options:
  --max-iterations <n>           Stop after N iterations (0 = unlimited, default: 0)
  --completion-promise '<text>'  Phrase that signals completion (multi-word must be quoted)
  -h, --help                     Show usage

Examples:
  /ralph-loop Build a todo API --completion-promise 'DONE' --max-iterations 20
  /ralph-loop --max-iterations 10 Fix the auth bug
  /ralph-loop Refactor cache layer          # runs forever
```

**Environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLAUDE_CODE_SESSION_ID` | (set by Claude Code) | Session isolation: written into state file at setup, checked on each hook invocation |
| `CLAUDE_PLUGIN_ROOT` | (set by plugin loader) | Absolute path to plugin directory; used in `allowed-tools` and hook command path |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `.claude/ralph-loop.local.md` | Per-project loop state (written at start, deleted on completion or cancel) |
| `hooks/hooks.json` | Hook registration for the `Stop` event |
| `.claude-plugin/plugin.json` | Plugin manifest (name, version, author) |

**Windows note:** On Windows, `hooks.json` must specify Git Bash explicitly (`Git/bin/bash.exe`) to avoid WSL path conflicts.

---

## 9. Extensibility Points

- **Adding a new termination condition:** Edit `hooks/stop-hook.sh` after the max-iterations check and before the promise check. Insert a guard that reads from the state file or transcript and calls `exit 0` when met. No other files need changes.

- **Changing the state file schema:** Edit the `cat > .claude/ralph-loop.local.md` heredoc in `scripts/setup-ralph-loop.sh` to add fields, then add matching `grep`/`sed` extraction lines in `hooks/stop-hook.sh` after the existing frontmatter parsing block. Both files must stay in sync.

- **Per-iteration callbacks (logging, notifications):** Insert a call at the end of `stop-hook.sh` before the final `jq -n` block. The state file's `iteration` field is already incremented at that point.

- **Background (non-interactive) loop mode:** Add a new command in `commands/` and a separate setup script in `scripts/` that launches `claude --continue` in a while loop via Bash rather than relying on the Stop hook. The stop-hook mechanism is session-bound; a background variant needs its own process management.

---

## 10. Limitations and Gotchas

- **No manual stop by design.** Without `--max-iterations` or `--completion-promise`, the loop runs forever. `/cancel-ralph` deletes the state file but only takes effect at the *next* exit attempt -- if Claude is mid-task, it finishes the current iteration first.

- **Session isolation depends on `CLAUDE_CODE_SESSION_ID`.** Legacy state files written before this field was introduced have an empty `session_id` and will match any session, potentially blocking unrelated Claude Code sessions open in the same project directory.

- **Transcript format coupling.** The hook relies on `grep '"role":"assistant"'` and a specific `jq -rs` expression to extract the last assistant text block. Any change in Claude Code's JSONL transcript format (key order, nesting, encoding) can break promise detection silently -- the loop continues rather than stopping.

- **Promise comparison is exact and case-sensitive.** `[[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]` uses literal `=`. Any whitespace difference or capitalization difference prevents completion. The `perl` extraction normalizes internal whitespace and trims edges, but edge cases (unicode spaces, BOM, trailing newline from jq) have not been systematically tested.

- **`set -euo pipefail` in stop-hook.sh.** Any unexpected command failure (`jq` not installed, `perl` not installed, disk full during temp-file write) causes the hook to exit with a non-zero code. Whether Claude Code treats this as "allow exit" or "block exit" is not documented; behavior may be undefined.

- **State file written without filesystem locking.** The atomic `sed > tempfile && mv` pattern is safe for a single writer but could produce duplicate iteration counts if two Stop hook invocations somehow race (an unlikely but non-zero scenario with concurrent exit calls).

- **Windows path issues with hooks.json.** The hook command uses `bash "${CLAUDE_PLUGIN_ROOT}/hooks/stop-hook.sh"`. On Windows, WSL's bash resolves paths differently from Git Bash; the plugin requires explicit configuration of Git Bash in `hooks.json`.

---

## 11. How It Compares to Alternatives

**Claude Code native `--continue`:** Built-in `--continue` resumes a previous session but requires manual invocation each time. Ralph Loop automates this by hooking the Stop event. The trade-off: no partial-result review between iterations.

**LangGraph / multi-agent frameworks:** Tools like LangGraph model iterative workflows as explicit state machines with typed transitions, conditional branching, and human-in-the-loop checkpoints. They offer fine-grained observability but require writing agent code in Python. Ralph Loop requires only a natural language prompt -- no code, no framework installation.

**Aider / Devin-style autonomous coding agents:** These embed planning-and-reflection loops internally with web search and multi-file context, and are opinionated about workflow structure. Ralph Loop makes no assumptions about task structure -- any Claude Code session becomes iterable by adding two arguments.

**Raw shell loop (`while true; do claude --continue; done`):** Achieves the same effect but has no iteration tracking, no completion detection, and no session isolation. Ralph Loop adds structured state management and promise-based termination on top of the same basic pattern.

**Positioning:** Ralph Loop occupies the gap between "manually retry Claude" and "write a full agent framework." It is the minimal viable autonomous loop for Claude Code -- trivial to start, zero external dependencies, and fully transparent about its mechanism (the state file is human-readable markdown).

---

## Appendix: Selected Code Snippets

**Block response emission (`hooks/stop-hook.sh`)**

The pivot point of the plugin: when no exit condition is met, this JSON tells Claude Code to block the stop and re-inject the prompt.

```bash
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'
```

**Atomic iteration counter update (`hooks/stop-hook.sh`)**

Avoids partial writes by writing to a PID-suffixed temp file and renaming atomically.

```bash
TEMP_FILE="${RALPH_STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$RALPH_STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$RALPH_STATE_FILE"
```

**Multi-line promise detection via Perl (`hooks/stop-hook.sh`)**

`-0777` slurps the entire input; `s` flag makes `.` match newlines; non-greedy `.*?` takes the first tag; whitespace is normalized.

```bash
PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe \
  's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' \
  2>/dev/null || echo "")
```

**Slash command with restricted tools (`commands/ralph-loop.md`)**

`allowed-tools` limits Claude during setup to only the setup script -- no arbitrary bash execution.

```markdown
---
description: "Start Ralph Loop in current session"
argument-hint: "PROMPT [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh:*)"]
hide-from-slash-command-tool: "true"
---
```
