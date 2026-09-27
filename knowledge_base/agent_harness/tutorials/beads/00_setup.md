# 00 — Setup: installing `bd` and creating your first beads project

**What you will learn**
- What `bd`, `uv` and `just` are, and why this tutorial uses them
- What each file in `project/` does
- How to check that `bd` (the beads CLI (Command-Line Interface), the program you talk to by typing commands in the terminal) is installed
- How to start a new beads project with `bd init` and what lands in `.beads/`
- How the Python code in `db.py` talks to beads (there is no Python driver — it just runs the `bd` program for you)
- How to prove the whole setup works with `just check`

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/00_setup`. All command outputs below are real outputs, run in a scratch folder (`/tmp/beads-probe-clean`) and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way.

## The tools we use

- **`bd`** is the beads issue tracker in the form of a CLI (Command-Line Interface). An issue tracker keeps a list of tasks (things to do), bugs (things that are broken) and features (new things to build). `bd` stores them in a folder called `.beads/` inside your project, so issues live next to the code they describe and can be committed to git like any other file.
- **Dolt** (the version-controlled SQL database that `bd` uses for storage — think of it as git, but for tables instead of files) is where `bd` keeps the issues. You never talk to Dolt directly; `bd` does it for you. It runs *embedded*, which means no server to install or start — it is just files under `.beads/embeddeddolt/`.
- **JSONL** (JSON Lines, a text format with one JSON object per line) is the file `bd` exports your issues to after every change (`.beads/issues.jsonl`). One line per issue, easy to read and to put into git.
- **uv** is a fast Python package manager. It creates a virtual environment (an isolated folder with its own Python packages, so this tutorial's dependencies never clash with other projects) and installs exactly the packages listed in `pyproject.toml`.
- **just** is a command runner, similar to `make`. Instead of typing long commands, you type short recipes like `just check` or `just demo`.

## Checking that `bd` is installed

```bash
bd --version
```

Real output from this machine:

```
bd version 1.0.4 (ce242a879)
```

Any `1.x` version works for this tutorial. If the command is not found, install `bd` first (see the beads installation docs), then come back here.

## The files in `project/`

```
project/
├── justfile                   # short commands: sync, check, demo, test
├── pyproject.toml             # Python project + dependency list, read by uv
├── src/beads_tutorial/
│   ├── __init__.py            # empty, marks the folder as a Python package
│   └── db.py                  # tiny wrapper that runs the bd CLI for you
└── tests/
    └── test_setup.py          # proves init + create + ready works
```

There is deliberately no Docker, no `.env` file and no server here — unlike the Neo4j tutorial, beads needs nothing running in the background. The "database" is just files in `.beads/`.

### `pyproject.toml`

This file tells `uv` what the project needs:

```toml
[project]
name = "beads-tutorial"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = ["pytest>=8"]        # testing framework
```

`dependencies` is empty on purpose: `bd` is a separate command-line program, not a Python library, so there is no Python driver to install. The only thing `uv` installs is `pytest` (in the `dev` group, which holds tools only needed while developing, not to run the tutorial code itself). The bottom half (`hatchling` build settings) just tells `uv` that the package code lives in `src/beads_tutorial`.

Running `uv sync` reads this file and creates `.venv/` (your isolated virtual environment).

### `src/beads_tutorial/db.py`

Since there is no Python driver, `db.py` drives `bd` through `subprocess` (Python's built-in way of starting other programs and reading their output):

```python
import json, subprocess

def run_bd(*args: str, cwd: str) -> str:
    # Runs `bd <args>` in folder `cwd`, returns its output.
    # Raises RuntimeError with bd's error message on failure.

def bd_json(*args: str, cwd: str) -> list | dict:
    # Same, but adds `--json` and parses the output as JSON.

def bd_create(title: str, cwd: str, type: str = "task",
              priority: int = 2, description: str = "") -> str:
    # Creates one issue, returns its id (e.g. "probe-a3f2dd").

def bd_ready(cwd: str) -> list:
    # Open issues with no blockers, as a list of dicts.

def bd_close(ids: list[str], cwd: str, reason: str = "") -> None:
    # Closes the issues with the given ids.
```

Every function takes `cwd` (current working directory): the folder of the project whose `.beads/` database you want to use. `bd` finds the database automatically by looking at that folder, so we never pass `--db` by hand. One more detail: `db.py` strips the `BEADS_DIR` environment variable before running `bd`, because that variable would pin `bd` to one fixed database and override the automatic discovery from `cwd`.

`priority` is a number from 0 (critical) to 4 (backlog); 2 means medium.

### `justfile`

```just
set dotenv-load := true
```

is the first line (it tells `just` to load a `.env` file if one ever appears; harmless here). The recipes:

```
sync:    # uv sync — install dependencies
check:   # uv run pytest tests -q — prove the setup works
demo:    # bd --version && bd list --limit 5 — show version + first issues
test:    # uv run pytest tests -q — run the test suite
```

## Starting a new beads project

From an empty folder:

```bash
bd init --prefix probe --non-interactive
```

`--prefix probe` says new issues should be named `probe-<something>` (the prefix is usually your project name). `--non-interactive` skips all questions and uses sensible defaults, which is what you want in scripts and tests.

Real output:

```
  ✓ Initialized git repository
  Repository ID: 0e721e50
  Clone ID: e947450ce9843886
  Hooks installed to: .beads/hooks/
  ✓ Created AGENTS.md with agent instructions
Installing Claude hooks for this project...
✓ Registered SessionStart hook
✓ Registered PreCompact hook
Installing Claude Code integration...
✓ Created new CLAUDE.md with beads integration

✓ Claude Code integration installed
  File: /private/tmp/beads-probe-clean/CLAUDE.md
No additional configuration needed!

✓ Claude Code integration installed
  Settings: /private/tmp/beads-probe-clean/.claude/settings.json

Restart Claude Code for changes to take effect.
  ✓ Committed beads files to git

✓ bd initialized successfully!

  Backend: dolt
  Mode: embedded
  Database: probe
  Issue prefix: probe
  Issues will be named: probe-<hash> (e.g., probe-a3f2dd)
```

`bd init` does three things at once: it creates the `.beads/` database, it runs `git init` (beads versions its files with git), and it drops helper files (`AGENTS.md`, `CLAUDE.md`) that teach AI coding assistants how to use beads in this project.

## What landed in `.beads/`

```bash
ls -la .beads/
```

Real output:

```
total 40
drwx------@ 10 sergii  wheel   320  8 wrz 15:47 .
drwxr-xr-x@  8 sergii  wheel   256  8 wrz 15:47 ..
-rw-------@  1 sergii  wheel  1615  8 wrz 15:47 .gitignore
-rw-------@  1 sergii  wheel     6  8 wrz 15:47 .local_version
-rw-------@  1 sergii  wheel  2254  8 wrz 15:47 config.yaml
drwx------@  4 sergii  wheel   128  8 wrz 15:47 embeddeddolt
drwx------@  7 sergii  wheel   224  8 wrz 15:47 hooks
-rw-r--r--@  1 sergii  wheel     0  8 wrz 15:47 interactions.jsonl
-rw-------@  1 sergii  wheel   156  8 wrz 15:47 metadata.json
-rw-r--r--@  1 sergii  wheel  2253  8 wrz 15:47 README.md
```

What matters for this tutorial:

- `config.yaml` — settings for this project (prefix, export behaviour, integrations). You rarely edit it by hand.
- `embeddeddolt/` — the actual Dolt database files. Never edit these directly; always go through `bd`.
- `issues.jsonl` — appears after your first change (see below): the auto-exported copy of every issue, one JSON object per line. This is the file you commit to git so others (and machines without Dolt) can read your issues.

## Asking `bd` where it is and how it feels

Three commands tell you about the current project. Run them from the project folder so `bd` discovers `.beads/` automatically:

```bash
bd where
```

```
/private/tmp/beads-probe-clean/.beads
  prefix: probe
  database: /private/tmp/beads-probe-clean/.beads/embeddeddolt
```

```bash
bd info
```

```

Beads Database Information
===========================
Database: /private/tmp/beads-probe-clean/.beads/embeddeddolt
Mode: direct

Issue Count: 0
```

`Issue Count: 0` is expected — we have not created anything yet; that is the next section.

```bash
bd doctor
```

```
Note: 'bd doctor' is not yet supported in embedded mode.

For embedded mode troubleshooting:
  • Verify database exists:  ls -la .beads/embeddeddolt/
  • Check bd version:        bd version
  • Reinitialize if needed:  bd init --force
  • Switch to server mode:   bd init --server
```

In embedded mode `bd doctor` just prints this checklist instead of running checks — that output above *is* the normal, healthy answer.

## Creating, listing and closing one issue

```bash
bd create --title="Probe task" --type task --priority 2 --description="probe" --json
```

```json
{
  "created_at": "2026-09-08T13:47:19.752794Z",
  "created_by": "sergii",
  "description": "probe",
  "id": "probe-5bj",
  "issue_type": "task",
  "priority": 2,
  "schema_version": 1,
  "status": "open",
  "title": "Probe task",
  "updated_at": "2026-09-08T13:47:19.752794Z"
}
```

The id `probe-5bj` starts with our prefix. `--json` asks for machine-readable output — this is exactly what `db.bd_create()` parses to get the id.

```bash
bd ready --json
```

```json
[
  {
    "id": "probe-5bj",
    "title": "Probe task",
    "description": "probe",
    "status": "open",
    "priority": 2,
    "issue_type": "task",
    "created_at": "2026-09-08T13:47:20Z",
    "created_by": "sergii",
    "updated_at": "2026-09-08T13:47:20Z",
    "dependency_count": 0,
    "dependent_count": 0,
    "comment_count": 0
  }
]
```

`bd ready` shows open issues with no blockers — work you could start right now. (This is what `db.bd_ready()` returns.)

```bash
bd list --limit 5
```

```
○ probe-5bj ● P2 Probe task

--------------------------------------------------------------------------------
Total: 1 issues (1 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

```bash
bd close probe-5bj --reason "probe done"
```

```
✓ Closed probe-5bj — Probe task: probe done
```

After the create, `bd` auto-exported the issue to `.beads/issues.jsonl` (one JSON object on one line — JSONL). Real file content:

```json
{"_type":"issue","id":"probe-5bj","title":"Probe task","description":"probe","status":"open","priority":2,"issue_type":"task","created_at":"2026-09-08T13:47:20Z","created_by":"sergii","updated_at":"2026-09-08T13:47:20Z","dependency_count":0,"dependent_count":0,"comment_count":0}
```

(The export is throttled to about once a minute, so right after a change the file can lag one step behind — that is normal.)

## Teaching your assistant about beads: `bd prime` and `bd onboard`

```bash
bd onboard
```

prints a short snippet to paste into `AGENTS.md` (the file many AI coding assistants read for project instructions). Real output:

```

bd Onboarding

Add this minimal snippet to AGENTS.md (or create it):

--- BEGIN AGENTS.MD CONTENT ---
## Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority 2` - Create issue
- `bd close <id>` - Complete work
- `bd dolt push` - Push beads to remote

For full workflow details: `bd prime`
--- END AGENTS.MD CONTENT ---

For GitHub Copilot users:
Add the same content to .github/copilot-instructions.md

How it works:
   • bd prime provides dynamic workflow context (~80 lines)
   • bd hooks install auto-injects bd prime at session start
   • AGENTS.md only needs this minimal pointer, not full instructions

This keeps AGENTS.md lean while bd prime provides up-to-date workflow details.
```

`bd init` already created an `AGENTS.md` with these instructions for us. `bd prime` prints the full workflow reminder (essential commands, session rules); assistants run it at the start of each session. Its output begins like this (real output, excerpt — the full text is about 80 lines):

```
# Beads Workflow Context

> **Context Recovery**: Run `bd prime` after compaction, clear, or new session
> Hooks auto-call this in Claude Code when a beads workspace is resolved

# 🚨 SESSION CLOSE PROTOCOL 🚨

**CRITICAL**: Before saying "done" or "complete", you MUST run this checklist:

...
```

## Checking the Python setup

From `project/`:

```bash
uv sync
just check
```

Real output:

```
uv run pytest tests -q
.                                                                        [100%]
1 passed in 3.49s
```

`just check` runs the test in `tests/test_setup.py`: it creates a scratch beads repo in a temporary folder, creates one issue through `db.py`, and asserts the new id starts with `probe-` and shows up in `bd ready`. If you see `1 passed`, Python can drive `bd` on this machine.

## Troubleshooting

- **`bd init` says "This workspace is already initialized"** — `bd` found another project's database instead of starting fresh. That happens when the `BEADS_DIR` environment variable is set (it pins `bd` to one fixed database and overrides discovery from the current folder). Check with `echo $BEADS_DIR`; for this tutorial, `unset BEADS_DIR` (or run `env -u BEADS_DIR bd ...`) so `bd` uses the project in front of you. `db.py` already strips it for you.
- **`bd where` points at the wrong project** — same cause as above, or you are simply in the wrong folder. `cd` into your project and run `bd where` again; the printed path should end in *your* project's `.beads`.
- **`bd doctor` prints "not yet supported in embedded mode"** — that is normal, not an error. Follow its checklist (`ls -la .beads/embeddeddolt/`, `bd version`).
- **`bd list` is empty after `bd create`** — you may be looking at a different database (see `bd where`), or the create actually failed — re-run it and check the exit code. Remember the JSONL export lags about a minute, but `list` itself is always live.
- **`just check` fails with "bd: command not found"** — `bd` is not on your `PATH` (the list of folders your shell searches for programs). Install `bd` and open a new terminal.
- **Test complains about `BEADS_DIR`** — the test removes it by itself (`monkeypatch.delenv`), so this should not happen. If you call `db.py` from your own scripts in an environment where `BEADS_DIR` is set on purpose, pass the database differently (explicit `--db`) instead of using `db.py`.
- **Want a clean slate?** — a beads project is just files: delete the scratch folder (or `.beads/` inside it) and run `bd init` again. Nothing is installed system-wide.

## Key takeaways

- `bd` is beads' CLI (Command-Line Interface): one program that tracks tasks, bugs and features per project, storing them in Dolt (a version-controlled SQL database) under `.beads/`, with an auto-exported JSONL (JSON Lines) copy at `.beads/issues.jsonl` for git.
- `bd init --prefix <name>` starts a project; `bd where` / `bd info` / `bd doctor` describe it; `bd create` / `bd ready` / `bd list` / `bd close` are the daily workflow; `bd prime` + the `bd onboard` snippet teach assistants to use it.
- There is no Python driver: `db.py` runs the `bd` program via `subprocess`, always with `cwd=` your project folder so `bd` discovers the right database, and `--json` wherever output needs parsing.
- `uv` manages the (tiny) Python environment from `pyproject.toml`; `just` gives short commands — `just check` (prove it works) and `just demo` (peek at real issues).
- Verified versions on this machine: `bd version 1.0.4`, Python `>=3.11`, `pytest>=8`.

Next: [001_explore.md](001_explore.md) — meeting an existing beads project: listing, showing and navigating issues.
