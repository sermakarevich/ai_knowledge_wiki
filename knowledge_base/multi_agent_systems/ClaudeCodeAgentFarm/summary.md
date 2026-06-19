# Technical Analysis: claude_code_agent_farm

**Repository:** https://github.com/Dicklesworthstone/claude_code_agent_farm
**Version analyzed:** 1.0.0
**Date:** 2026-05-03

---

## 1. Overview / What Problem It Solves

Automated type-checking and linting tools identify large backlogs of code quality issues, but fixing them manually is time-consuming and tedious. Running a single AI coding agent sequentially through hundreds of problems is slow and hits context limits. The primary problem this repo addresses is throughput: how to apply AI-assisted code fixes at scale without manual supervision.

`claude_code_agent_farm` orchestrates N parallel Claude Code (`cc`) sessions, each running in its own tmux pane against the same codebase. Each agent reads a shared problems file (mypy/ruff output), takes a chunk, and applies fixes autonomously. A Python monitoring process polls all panes via `tmux capture-pane`, classifies agent health, handles context exhaustion with `/clear`, and restarts stalled or error-prone agents automatically.

The primary user is a human developer who wants to drain a large backlog of type errors, linting violations, or best-practices gaps with minimal manual intervention. The developer launches the farm, watches the dashboard, and returns to a codebase with fewer problems. No Anthropic API is called directly — the tool shells out to the `cc` CLI alias.

---

## 2. High-Level Architecture

```
User CLI invocation
        │
        ▼
ClaudeAgentFarm.__init__
        │  loads config, validates params
        ▼
 regenerate_problems()
        │  runs mypy + ruff → combined_typechecker_and_linter_problems.txt
        ▼
   setup_tmux()
        │  creates session + N agent panes + controller window
        ▼
  launch_agents()
        │  for each pane: cd project; cc (staggered)
        ▼
  monitor_loop()   ◄─────────────────────────────┐
        │  every check_interval seconds            │
        ▼                                          │
 AgentMonitor.check_agent(i)                      │
        │  tmux_capture → classify status          │
        ▼                                          │
  needs_restart(i)                                │
        │  None / 'context' / 'error' / 'idle'     │
        ├─ context: send /clear ──────────────────►│
        └─ error/idle: start_agent(i, restart=True)┘
        │
        ▼
 write_monitor_state()
        │  .claude_agent_farm_state.json (atomic)
        ▼
 (optional) commit_and_push() every N cycles
        │
        ▼
 generate_html_report() on shutdown
```

**Data flow from CLI invocation to agent restart:**

1. `main()` (`claude_code_agent_farm.py:2385`) validates the project path and agent count, instantiates `ClaudeAgentFarm`, and calls `farm.run()`.
2. `regenerate_problems()` (`~line 1200`) runs `mypy .` and `ruff check .` (or stack-specific equivalents), concatenates their stdout into `combined_typechecker_and_linter_problems.txt` via atomic `tmpfile → rename`.
3. `setup_tmux()` creates a tmux session named `claude_agents` (or configured name) with N numbered panes and a separate `controller` window running the `monitor-only` subcommand.
4. `launch_agents()` iterates agent IDs 0..N-1, calling `start_agent(i)` for each with a configurable stagger (default 10s) to prevent simultaneous `~/.claude/settings.json` writes.
5. `start_agent(i)` acquires `~/.claude/.agent_farm_launch.lock` via `O_CREAT|O_EXCL`, sends `cd <project>` and then `cc` (the Claude Code alias) to the pane, waits `wait_after_cc` seconds, verifies Claude started successfully, then sends the prompt text.
6. `monitor_loop()` polls all panes every `check_interval` seconds, classifies agent status by scraping tmux output, and triggers `/clear` or full restart as needed.

**Persistent state:** `.claude_agent_farm_state.json` at project root (written by `ClaudeAgentFarm`, read by the `monitor-only` subcommand in the controller pane). Settings backups in `<project>/.claude_agent_farm_backups/`. Heartbeat files in `<project>/.heartbeats/agent{N:02d}.heartbeat`.

---

## 3. The Agent State Model

There are no dataclasses, TypedDicts, or Enums in the codebase. Every agent is tracked as a plain `Dict` inside `AgentMonitor.agents: Dict[int, Dict]`.

**Agent state schema** (initialized at `claude_code_agent_farm.py:252`):

```python
{
    "status":        str,       # one of: starting, working, ready, idle, error, unknown
    "start_time":    datetime,
    "cycles":        int,       # completed work cycles
    "last_context":  int,       # context % from most recent pane scrape (0–100)
    "errors":        int,       # consecutive error count
    "last_activity": datetime,
    "restart_count": int,
    "last_restart":  Optional[datetime],
    "last_heartbeat": Optional[datetime],
    "cycle_start_time": Optional[datetime],  # set when entering 'working', cleared on exit
}
```

**Status transitions** (`check_agent`, line ~462):

- `is_claude_working()` → `"working"` — detects substrings: `"✻ Pontificating"`, `"● Bash("`, `"✻ Thinking"`, `"esc to interrupt"`
- `is_claude_ready()` → `"ready"` or `"idle"` — detects prompt-box indicators: `"│ >"`, `"╰─"`, `"❯ Try "`, etc. If `idle_time > idle_timeout`: `"idle"`.
- `has_settings_error()` → `"error"` — detects 30+ substrings: auth prompts, config error messages, `TypeError`, `JSONDecodeError`

**Cycle time tracking:** When an agent transitions `working → ready`, `check_agent` records the elapsed time in `AgentMonitor.cycle_times` (capped at 20 entries). `calculate_adaptive_timeout()` computes `3 × median_cycle_time`, clamped to [30, 600] seconds, and updates `idle_timeout` if the change exceeds 20%.

**Restart decision** (`needs_restart`, line ~554):

```python
def needs_restart(self, agent_id: int) -> Optional[str]:
    agent = self.agents[agent_id]
    heartbeat_age = self._check_heartbeat_age(agent_id)
    if heartbeat_age is not None and heartbeat_age > 120:
        return "error"
    if agent["last_context"] <= self.context_threshold:
        return "context"
    if agent["status"] == "error" or agent["errors"] >= self.max_errors:
        return "error"
    if agent["status"] == "idle":
        return "idle"
    return None
```

**Config knobs:** `context_threshold` (default 20), `idle_timeout` (default 60s), `max_errors` (default 3), `check_interval` (default 10s).

---

## 4. LLM / External Service Integration

The repo does **not** call the Anthropic API or any LLM directly. It shells out to the `cc` CLI alias, which is defined in `setup.sh` as:

```bash
alias cc='ENABLE_BACKGROUND_TASKS=1 claude --dangerously-skip-permissions'
```

Claude Code (`claude`) is the LLM client; the agent farm is purely an orchestration layer around it. Authentication, model selection, and API billing all belong to the Claude Code CLI's configuration, not to this Python process.

The only external dependency is `tmux` (process control) and `git` (optional commit/push). No HTTP calls, no API keys, no SDK imports.

---

## 5. The Farm Launch and Monitoring Pipeline

**Step 1 — Problem file generation** (`regenerate_problems`, `~line 1200`):
Runs `mypy .` and `ruff check .` (or stack-configured equivalents via `problem_commands` config key), concatenating stdout to a tempfile, then atomically renaming it to `combined_typechecker_and_linter_problems.txt`. The `chunk_size` variable substitution in the loaded prompt tells each Claude agent how many lines to process per iteration.

**Step 2 — tmux session setup** (`setup_tmux`):
Creates session `{session}` with `tmux new-session`, enables mouse support if `tmux_mouse=True`, creates N windows/panes (one per agent), and registers pane targets in `self.pane_mapping: Dict[int, str]`. A separate `controller` window is created and runs `claude-code-agent-farm monitor-only --path <project>`.

**Step 3 — Staggered agent launch** (`launch_agents`, `line 1866`):
Iterates `range(self.agents)`. For each agent:
- Acquires `~/.claude/.agent_farm_launch.lock` via `os.open(O_CREAT|O_EXCL)` (30s stale detection).
- Sends `cd <project>` → `cc` via `tmux_send()` (which uses `tmux load-buffer` + `tmux paste-buffer` for binary-safe payload delivery).
- Waits `wait_after_cc` seconds (default 15s) interruptibly.
- Verifies Claude started by polling `is_claude_ready()` up to 5 times.
- Sends the prompt text to the pane.
- Releases the lock.
- Adaptive stagger: doubles `current_stagger` on consecutive launch failures (up to 60s), halves on recovery.

**Step 4 — Main monitoring loop** (`monitor_loop`, `line 1918`):
`while self.running`: calls `check_agent(i)` for all agents every `check_interval` seconds. If `auto_restart=True`, calls `needs_restart(i)` and dispatches `clear_agent_context(i)` (sends `/clear`) or `start_agent(i, restart=True)` (sends `/exit`, waits for shell, re-launches). Exponential backoff: `min(300, 10 × 2^restart_count)` seconds between restarts.

**Step 5 — Periodic commit** (optional, controlled by `commit_every`):
When all agents have completed at least `commit_every` cycles since last commit, calls `regenerate_problems()` + `commit_and_push()`.

**Step 6 — Shutdown** (`shutdown`):
Writes HTML report via `generate_html_report()` (`line ~2113`), optionally kills tmux session, removes state file and lock file.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `claude_code_agent_farm.py` | 2,991 | Entire implementation: `AgentMonitor`, `ClaudeAgentFarm`, 4 CLI commands |
| `claude_code_agent_farm.py:211-606` | 396 | `AgentMonitor` — status detection, heartbeat tracking, adaptive timeouts, Rich status table |
| `claude_code_agent_farm.py:614-2382` | 1,769 | `ClaudeAgentFarm` — lifecycle: setup, launch, monitoring loop, restart, backup, report |
| `claude_code_agent_farm.py:2385-2524` | 140 | `main()` — primary CLI command, all flags, delegates to `ClaudeAgentFarm.run()` |
| `claude_code_agent_farm.py:2610-2848` | 239 | `doctor` — pre-flight system verification (Python version, tmux, cc alias, project path) |
| `pyproject.toml` | ~120 | Version 1.0.0, entry point, ruff/mypy/pytest configuration |
| `setup.sh` | ~500 | Environment setup: uv install, `cc` alias definition, tool-setup script invocations |
| `view_agents.sh` | ~120 | Opens tmux split-pane view across all agent windows |
| `configs/python_config.json` | ~30 | Sample config: 9 agents, chunk 50, stagger 10s, auto_restart, etc. |
| `configs/sample.json` | ~25 | Minimal config template showing all available keys |
| `prompts/default_prompt.txt` | ~50 | Default bug-fixing prompt with `{chunk_size}` substitution placeholder |
| `prompts/cooperating_agents_improvement_prompt_for_python_fastapi_postgres.txt` | ~400 | Full coordination protocol: lock files, work registry, conflict resolution |
| `prompts/default_best_practices_prompt_python.txt` | ~50 | Best-practices mode prompt for Python/FastAPI stacks |
| `best_practices_guides/PYTHON_FASTAPI_BEST_PRACTICES.md` | ~1,500 | 57KB guide injected (via prompt reference) into agent context |
| `tool_setup_scripts/` | (dir) | Modular setup scripts for each technology stack |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| `typer` | `>=0.15.0` | CLI framework, argument parsing, help generation |
| `rich` | `>=13.7.0` | Terminal tables, progress bars, Live display, HTML report export |
| `pytest` | `>=7.4.0` *(dev)* | Test runner (no tests currently exist in the repo) |
| `pytest-asyncio` | `>=0.21.0` *(dev)* | Async test support |
| `pytest-cov` | `>=4.1.0` *(dev)* | Coverage reporting |
| `ruff` | `>=0.12.0` *(dev)* | Linter and formatter for the project itself |
| `mypy` | `>=1.7.0` *(dev)* | Static type checking for the project itself |
| `pre-commit` | `>=3.0.0` *(dev)* | Git hook runner |
| `mkdocs` | `>=1.5.0` *(docs)* | Documentation site generation |
| `mkdocs-material` | `>=9.0.0` *(docs)* | Material theme for MkDocs |
| `mkdocstrings[python]` | `>=0.24.0` *(docs)* | Auto-generated API docs |

**Runtime system requirements (not in pyproject.toml):** Python 3.13+, `tmux` (any recent version), Claude Code CLI (`claude`) installed and authenticated, `git` (optional, for commit/push workflow).

---

## 8. CLI / Usage Surface

**Entry point** (`pyproject.toml:35`):
```
claude-code-agent-farm = "claude_code_agent_farm:app"
```

**Commands:**

```bash
# Primary: launch a farm
claude-code-agent-farm \
  --path /abs/path/to/project \
  --agents 20 \
  --session claude_agents \
  --config configs/python_config.json \
  --stagger 10 \
  --wait-after-cc 15 \
  --check-interval 10 \
  --context-threshold 20 \
  --idle-timeout 60 \
  --max-errors 3 \
  --prompt-file prompts/default_prompt_python.txt \
  --auto-restart \
  --commit-every 5 \
  --full-backup

# Pre-flight check
claude-code-agent-farm doctor --path /abs/path/to/project

# Attach to an existing running session's dashboard (internal, used by controller pane)
claude-code-agent-farm monitor-only --path /abs/path/to/project --session claude_agents

# Install shell completion
claude-code-agent-farm install-completion --shell zsh
```

**Environment variables** — none declared; all configuration is via CLI flags or JSON config files.

**Configuration files:**

| Path | Purpose |
|------|---------|
| `configs/<stack>_config.json` | Per-stack defaults loaded with `--config` |
| `<project>/.claude_agent_farm_state.json` | Live state shared between orchestrator and monitor-only pane |
| `<project>/.claude_agent_farm_backups/` | Timestamped gzip archives of `~/.claude` |
| `<project>/.heartbeats/agent{N:02d}.heartbeat` | Per-agent liveness timestamps |
| `~/.claude/.agent_farm_launch.lock` | Mutual-exclusion lock preventing concurrent `cc` starts |

**JSON config keys** (full set, from `configs/sample.json` and `_load_config`):
`agents`, `chunk_size`, `stagger`, `wait_after_cc`, `session`, `tmux_mouse`, `tmux_kill_on_exit`, `idle_timeout`, `check_interval`, `max_errors`, `context_threshold`, `max_agents`, `auto_restart`, `monitor`, `regenerate`, `prompt_file`, `fast_start`, `full_backup`, `commit_every`, `git_branch`, `git_remote`, `skip_commit`, `skip_regenerate`, `tech_stack`, `problem_commands`, `best_practices_files`.

---

## 9. Extensibility Points

- **New technology stack:** Add `configs/<stack>_config.json` (copy `configs/sample.json`, set `tech_stack`, `problem_commands`, `prompt_file`) and `prompts/default_best_practices_prompt_<stack>.txt`. Optionally add `best_practices_guides/<STACK>_BEST_PRACTICES.md`. No Python changes required.

- **Custom problem-generation commands:** Set `problem_commands` in a JSON config:
  ```json
  {"problem_commands": {"type_check": ["tsc", "--noEmit"], "lint": ["eslint", "."]}}
  ```
  `regenerate_problems()` (`~line 1200`) reads this key via `getattr(self, 'problem_commands', ...)` and substitutes it into the subprocess calls.

- **Custom prompt logic:** The prompt is a plain text file with `{chunk_size}` substitution. Supply any file via `--prompt-file`. The cooperating-agents workflow is entirely prompt-driven — the `coordination/` filesystem protocol in `prompts/cooperating_agents_improvement_prompt_for_python_fastapi_postgres.txt` requires no Python changes to adapt to a new domain.

- **Additional status detection patterns:** `AgentMonitor.is_claude_working()`, `is_claude_ready()`, `has_settings_error()`, and `detect_context_percentage()` (`lines 300–370`) are plain lists of indicator strings. Adding a new Claude Code UI variant requires only appending to those lists.

- **Alternative backup targets:** `_backup_claude_settings()` (`line ~758`) uses `tarfile` and a hardcoded `~/.claude` path. To back up additional directories, extend the `else` branch's `tar.add()` calls.

---

## 10. Limitations and Gotchas

- **POSIX-only:** Uses `fcntl.flock` and `fcntl.LOCK_EX`/`LOCK_SH` for file locking, and `os.open(O_CREAT|O_EXCL)` for the launch lock. Does not run on Windows. The `pyproject.toml` classifier states `Operating System :: POSIX :: Linux` but macOS works too.

- **`--dangerously-skip-permissions` is unconditional:** The `cc` alias always passes this flag (`setup.sh`). All agents bypass Claude Code's permission prompts, allowing unrestricted filesystem writes. This is intentional for automation but means a misbehaving prompt can silently overwrite arbitrary files.

- **No test suite:** `pytest` is listed as a dev dependency and `pytest.ini_options` is configured, but there is no `tests/` directory in the repository. The `pyproject.toml` `testpaths = ["tests"]` setting will simply find nothing.

- **Cooperating agents is prompt-only:** The `configs/python_cooperating_agents_config.json` and the long coordination prompt exist, but there is zero Python code enforcing the lock-file protocol. Agents follow the protocol only insofar as the LLM obeys the prompt instructions. Any model non-compliance silently breaks the coordination.

- **Single-file 2,991-line module:** The entire implementation lives in `claude_code_agent_farm.py` with no internal module structure. Functions that belong to `ClaudeAgentFarm` (e.g., `regenerate_problems`, `commit_and_push`, `generate_html_report`) are methods on a 1,769-line class. Navigation is difficult without an IDE.

- **Config loaded via `setattr` without schema validation:** `_load_config()` (`line ~707`) calls `setattr(self, key, value)` for every JSON key. An unknown key silently becomes an instance attribute; a mistyped key (e.g., `"agentes": 10`) is ignored without warning.

- **Settings backup path hard-coded to `~/.claude`:** `_backup_claude_settings()` assumes Claude Code stores settings at `Path.home() / ".claude"`. If Claude Code changes its config location, the backup silently does nothing (returns `None` with a warning print).

- **tmux pane scraping is fragile:** Status detection relies on substring matching against terminal output captured by `tmux capture-pane -p`. Claude Code UI changes (different prompt box characters, new loading indicators) will break `is_claude_working()` and `is_claude_ready()` without any error signal.

- **Backup rotation uses mtime, not creation time:** `_cleanup_old_backups()` sorts by `st_mtime`, which on some filesystems differs from creation time and can be mutated by `touch`. This is unlikely to cause problems in practice but is a minor correctness note.

---

## 11. How It Compares to Alternatives

**SWE-Agent (Princeton NLP):** Targets discrete GitHub issues using a structured thought–action loop (AgentComputer Interface). Single-agent, designed for reproducible evaluation on SWE-bench. Unlike this repo, it does not sustain parallel agents indefinitely against a shared backlog — it solves one issue and terminates.

**Aider:** Interactive AI pair programmer run from the terminal. Deep git integration, supports multiple models and providers. Designed for human-in-the-loop use with a single coding session; has no parallel agent orchestration, no automatic restart loop, and no concept of a shared problems file being drained by multiple workers.

**OpenHands (All-Hands AI):** Provides Docker-sandboxed environments, a web UI, and micro-agent task delegation. Each task gets an isolated sandbox, which is safer but higher-overhead than tmux panes. OpenHands is task-centric (one task → one agent run), not a sustained parallel farm. It also calls an LLM API directly rather than shelling out to a CLI.

**Agentless (UIUC):** LLM-based fault localization + patch generation for SWE-bench, structured around two phases (localization, repair). Batch-oriented and evaluation-focused, not designed for ongoing best-practices improvement of a live codebase.

**Positioning:** `claude_code_agent_farm` occupies a niche that the others do not: a sustained, parallel, self-healing improvement farm that drains a shared problems backlog using many independent Claude Code sessions in tmux, with no API calls and minimal dependencies.

---

## Appendix: Selected Code Snippets

**`tmux_send` — binary-safe payload delivery to a pane** (`claude_code_agent_farm.py:145-192`)

```python
def tmux_send(target: str, data: str, enter: bool = True, update_heartbeat: bool = True) -> None:
    """Send keystrokes to a tmux pane (binary-safe)"""
    max_retries = 3
    base_delay = 0.5

    for attempt in range(max_retries):
        try:
            if data:
                import uuid
                with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
                    tmp.write(data)
                    tmp_path = tmp.name

                buf_name = f"agentfarm_{uuid.uuid4().hex[:8]}"
                try:
                    run(f"tmux load-buffer -b {buf_name} {shlex.quote(tmp_path)}", quiet=True)
                    run(f"tmux paste-buffer -d -b {buf_name} -t {target}", quiet=True)
                finally:
                    with contextlib.suppress(FileNotFoundError):
                        os.unlink(tmp_path)

                if enter:
                    time.sleep(0.2)

            if enter:
                run(f"tmux send-keys -t {target} C-m", quiet=True)
            break
        except subprocess.CalledProcessError:
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))
            else:
                raise
```

**`calculate_adaptive_timeout` — median-based idle timeout adjustment** (`claude_code_agent_farm.py:265-295`)

```python
def calculate_adaptive_timeout(self) -> int:
    """Calculate adaptive idle timeout based on median cycle time"""
    if len(self.cycle_times) < 3:
        return self.base_idle_timeout

    sorted_times = sorted(self.cycle_times)
    median_time = sorted_times[len(sorted_times) // 2]

    adaptive_timeout = int(median_time * 3)

    min_timeout = 30
    max_timeout = 600
    adaptive_timeout = max(min_timeout, min(adaptive_timeout, max_timeout))

    if abs(adaptive_timeout - self.idle_timeout) / self.idle_timeout > 0.2:
        console.print(
            f"[dim]Adjusting idle timeout: {self.idle_timeout}s → {adaptive_timeout}s "
            f"(median cycle: {median_time:.1f}s)[/dim]"
        )
        self.idle_timeout = adaptive_timeout

    return self.idle_timeout
```

**`_acquire_claude_lock` — atomic launch lock with stale detection** (`claude_code_agent_farm.py:1574-1607`)

```python
def _acquire_claude_lock(self, timeout: float = 5.0) -> bool:
    """Acquire a lock file to prevent concurrent Claude Code launches"""
    lock_file = Path.home() / ".claude" / ".agent_farm_launch.lock"
    lock_file.parent.mkdir(exist_ok=True)

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()}\n".encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                if lock_file.exists():
                    if time.time() - lock_file.stat().st_mtime > 30:
                        lock_file.unlink()
                        continue
            except Exception:
                pass
            time.sleep(0.1)
    return False
```

**Cooperating-agents coordination protocol** (from `prompts/cooperating_agents_improvement_prompt_for_python_fastapi_postgres.txt`, lines 1-35)

```
# Task Instructions for AI-Powered Project Enhancement with Multi-Agent Coordination

## CRITICAL: Multi-Agent Coordination Protocol

### Before Starting ANY Work:

1. **Check the Agent Coordination System:**
   /coordination/
   ├── active_work_registry.json     # Central registry of all active work
   ├── completed_work_log.json       # Log of completed tasks
   ├── agent_locks/                  # Directory for individual agent locks
   │   └── {agent_id}_{timestamp}.lock
   └── planned_work_queue.json       # Queue of planned but not started work

2. **Claim Your Work BEFORE Planning:**
   - Generate a unique agent ID: agent_{timestamp}_{random_4_chars}
   - Check active_work_registry.json for conflicts
   - Create a lock file in agent_locks/ with:
     {
       "agent_id": "your_agent_id",
       "timestamp": "ISO_8601_timestamp",
       "planned_scope": {
         "files": ["list", "of", "files"],
         "features": ["features", "or", "best_practices"],
         "estimated_duration": "minutes"
       },
       "status": "planning|implementing|testing|completed"
     }
```
