# 001 — Exploring an unknown beads database: what is actually inside it?

**What you will learn**
- Three ways to look inside a beads database: the `bd` CLI (Command-Line Interface, the program you talk to by typing commands in the terminal), `bd --json` plus `jq` (a small command-line tool that filters JSON), and Python
- The inventory commands (`bd list`, `bd status`, `bd show`) and what each one tells you
- How to count beads by status, type, priority and assignee, and how to see which types block which other types — the "shape" of the project
- How to inspect properties per bead: labels, estimates, due dates, assignees and metadata
- Structure and health checks (`bd dep cycles`, `bd stale`, `bd orphans`, `bd doctor`, `bd preflight`), plus a reusable `explore.py` recipe

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/001_explore`. All command outputs below are real outputs, run against a scratch database created with `bd init --prefix tut` in `/tmp/beads-tut` and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. JSON (JavaScript Object Notation) is the text format `bd` uses for machine-readable output — the same curly-brace format Python's `json` module reads.

## 0. The scenario

You inherit a repository you have never seen before. It has a `.beads/` folder, so somebody tracked work with beads — but nobody gave you a tour. Before you create a single new bead, you need to answer: how many beads are in there, what kinds (**types** like `task`, `bug`, `feature`, `chore`) do they have, what state (**status** like `open`, `in_progress`, `closed`) are they in, what data (**properties** like labels, estimates, due dates) do they carry, and how do they depend on each other? This chapter is a checklist and toolbox for exactly that situation.

Our scratch database for this chapter holds six beads, seeded like this:

```bash
bd init --prefix tut --non-interactive
bd create --title="Design database schema" --type task --priority 1 --description="draft tables" --json   # → tut-v8p
bd create --title="Login page bug" --type bug --priority 0 --description="500 on empty password" --json   # → tut-9x5
bd create --title="Signup flow" --type feature --priority 2 --description="new signup" --json              # → tut-ipv
bd create --title="Write docs" --type task --priority 3 --description="user guide" --json                  # → tut-sar
bd create --title="Refactor auth" --type chore --priority 2 --description="cleanup" --json                 # → tut-cwf
bd create --title="Add dark mode" --type feature --priority 4 --description="theme toggle" --json          # → tut-jfv
bd dep add tut-ipv tut-v8p    # Signup flow is blocked by Design database schema
bd dep add tut-cwf tut-9x5    # Refactor auth is blocked by Login page bug
bd dep add tut-jfv tut-ipv    # Add dark mode is blocked by Signup flow
bd update tut-sar --status in_progress
bd close tut-v8p --reason "schema done"
bd update tut-9x5 --add-label frontend --estimate 120 --assignee sergii --due tomorrow
bd update tut-ipv --add-label backend --set-metadata team=platform
```

Six beads, three dependencies, one closed, one in progress, labels and an estimate on two of them. Small enough to hold in your head, realistic enough to exercise every command below.

First, confirm you are looking at the right database. `bd where` prints the folder `bd` is actually using (it discovers `.beads/` from your current folder, unless the `BEADS_DIR` environment variable pins it somewhere else — if the path surprises you, check `echo $BEADS_DIR` first):

```bash
bd where
```

```
/private/tmp/beads-tut/.beads
  prefix: tut
  database: /private/tmp/beads-tut/.beads/embeddeddolt
```

And `bd info` (database information) gives the one-line health summary:

```bash
bd info
```

```
Beads Database Information
===========================
Database: /private/tmp/beads-tut/.beads/embeddeddolt
Mode: direct

Issue Count: 6
```

`Issue Count: 6` matches the six beads we seeded. If it says `0` on a repo you expected work in, you are probably in the wrong folder (see Troubleshooting).

## 1. Three ways to look

| Tool | When to use it |
|---|---|
| **`bd list` / `bd show` CLI** | First 30 seconds with a new database — one command, human-readable table, no setup. Good for eyeballing a handful of beads. |
| **`bd --json` + `jq`** | Scripting, counting and filtering from a terminal. `--json` asks `bd` for machine-readable output; `jq` (or plain Python) slices it up. Fast and repeatable. |
| **Python** (`just explore` / `just describe`) | Programmatic exploration — looping over results, building a report, feeding counts into another tool. Best when you want to save or reuse the output. |

From the terminal:

```bash
bd list                  # human-readable table of open beads
bd show tut-ipv          # everything about one bead
bd list --all --json | jq '.[] | .issue_type'   # just the types, via jq
```

From Python (from `project/`, pointing at any beads repo with `repo=`):

```bash
just explore /tmp/beads-tut     # compact summary: counts by status and type
just describe /tmp/beads-tut    # dependency shape + orphan check
```

`just explore` with no argument inspects the current folder (`.`). The recipes call `src/beads_tutorial/explore.py`, which uses only `db.bd_json` / `db.run_bd` — the same wrapper from chapter 00, so `BEADS_DIR` is stripped and the database is always discovered from the folder you point at.

## 2. Inventory: what beads exist and what state are they in?

`bd list` is the front door. By default it shows open and in-progress beads; closed ones are hidden (use `--all` to see everything):

```bash
bd list
```

```
○ tut-9x5 ● P0 [bug] Login page bug
○ tut-cwf ● P2 Refactor auth
○ tut-ipv ● P2 Signup flow
◐ tut-sar ● P3 Write docs
○ tut-jfv ● P4 Add dark mode

--------------------------------------------------------------------------------
Total: 5 issues (4 open, 1 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Reading one row: `○` is the status icon (open), `tut-9x5` the id, `P0` the priority (0 = critical, 4 = backlog), `[bug]` the type, then the title. Notice the closed `tut-v8p` is missing — that is the default filter, not lost data. Compare with `--all`:

```bash
bd list --all
```

```
○ tut-9x5 ● P0 [bug] Login page bug
✓ tut-v8p ● P1 task Design database schema
○ tut-cwf ● P2 Refactor auth
○ tut-ipv ● P2 Signup flow
◐ tut-sar ● P3 Write docs
○ tut-jfv ● P4 Add dark mode

--------------------------------------------------------------------------------
Total: 6 issues (4 open, 1 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

There it is: `✓ tut-v8p`, closed. Rule of thumb: `bd list` answers "what could I work on?", `bd list --all` answers "what is (or was) in here?".

`bd status` is the dashboard — one screen with totals:

```bash
bd status
```

```
📊 Issue Database Status

Summary:
  Total Issues:           6
  Open:                   4
  In Progress:            1
  Blocked:                2
  Closed:                 1
  Ready to Work:          2

For more details, use 'bd list' to see individual issues.
```

`Blocked: 2` means two beads wait on unfinished dependencies; `Ready to Work: 2` means two beads have no blockers. That matches `bd ready` (the command that lists work you could start right now — the same call `db.bd_ready()` makes):

```bash
bd ready
```

```
○ tut-9x5 ● P0 [bug] Login page bug
○ tut-ipv ● P2 Signup flow

--------------------------------------------------------------------------------
Ready: 2 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Why is `tut-ipv` ready even though it depends on `tut-v8p`? Because `tut-v8p` is closed — a finished blocker no longer blocks. `bd ready` only counts *active* (unfinished) blockers. `tut-cwf` and `tut-jfv` stay out because their blockers (`tut-9x5`, `tut-ipv`) are still open.

`bd show <id>` opens one bead fully — description, labels, metadata (custom key-value data attached to a bead), and both directions of dependencies:

```bash
bd show tut-ipv
```

```
○ tut-ipv · Signup flow   [● P2 · OPEN]
Owner: sergii · Type: feature
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
new signup

LABELS: backend

METADATA
  team: platform

DEPENDS ON
  → ✓ tut-v8p: Design database schema ● P1

BLOCKS
  ← ○ tut-jfv: Add dark mode ● P4


💡 Tip: Install the beads plugin for automatic workflow context, or run 'bd setup claude' for CLI-only mode
```

In one screen you see the bead sits in the middle of a chain: finished schema work behind it, dark-mode work waiting ahead of it.

A note on SQL (Structured Query Language, the language for asking tabular questions of a database): on a server-mode beads database you could run `bd sql 'SELECT status, COUNT(*) FROM issues GROUP BY status'` for direct counts. In embedded mode (what this tutorial uses — the database is just files, no server), that command is not available, and it says so honestly:

```bash
bd sql 'SELECT status, COUNT(*) FROM issues GROUP BY status'
```

```
Error: 'bd sql' is not yet supported in embedded mode
```

That is normal, not a broken install. The replacement is `bd list --all --json` plus counting in Python or `jq` — which is exactly what `explore.py`'s `summary()` does (§6). You lose nothing: every column SQL (Structured Query Language) would read is present in the JSON (JavaScript Object Notation).

## 3. Counting: how much of everything is there

Totals first. `bd list --all --json` returns every bead including closed ones (6 objects here); plain `bd list --json` returns only the 5 visible ones. Always use `--all` when counting history, plain `list` when counting actionable work.

Priorities and assignees, counted from the JSON (JavaScript Object Notation) with a few lines of Python (the `jq` equivalent is `bd list --all --json | jq 'group_by(.priority) | map({p: .[0].priority, n: length})'`):

```python
priorities: {0: 1, 1: 1, 2: 2, 3: 1, 4: 1}       # P0..P4 — spread across the whole range
assignees:  {'sergii': 1, 'unassigned': 5}        # only the bug has an owner
```

One P0 (the login bug — the most urgent thing here), two P2s, and five of six beads with nobody assigned. On an unknown repo that pattern — urgent bug owned, everything else unowned — tells you where attention actually went.

Types and statuses come from `explore.summary()`, which is just `bd list --all --json` plus `bd status` wrapped for reuse:

```bash
uv run python -m beads_tutorial.explore --summary --cwd /tmp/beads-tut
```

```
Total: 6
By status:
  closed: 1
  in_progress: 1
  open: 4
By type:
  bug: 1
  chore: 1
  feature: 2
  task: 2
Ready to work: 2
```

(`Ready to work` is parsed out of the `bd status` text; it is `None` on bd versions that print no such line.)

## 4. Who blocks whom: the shape of the project

This is the single most useful view in this chapter — for every dependency, which type is blocked by which other type:

```bash
uv run python -m beads_tutorial.explore --shape --cwd /tmp/beads-tut
```

```
chore -[blocks]-> bug: 1
feature -[blocks]-> feature: 1
feature -[blocks]-> task: 1
```

Read it like a diagram: the `chore` (Refactor auth) waits on the `bug` (Login page bug) — cleanup held up by an unfixed crash, sensible. The `feature`→`feature`→`task` chain (dark mode → signup → schema) is one line of work in dependency order. If a type showed up blocking *itself* in a big loop, or everything blocked one ancient bead nobody owns, that would be worth asking the previous owner about.

The raw material is the `dependencies` array embedded in `bd list --all --json`, or `bd dep list <id> --json` per bead (note: `bd dep list` with no id is an error — it needs at least one bead id):

```bash
bd dep list tut-jfv --json
```

```json
[
  {
    "id": "tut-ipv",
    "title": "Signup flow",
    "description": "new signup",
    "status": "open",
    "priority": 2,
    "issue_type": "feature",
    "created_at": "2026-09-08T13:58:39Z",
    "created_by": "sergii",
    "updated_at": "2026-09-08T13:58:44Z",
    "metadata": {
      "team": "platform"
    },
    "labels": [
      "backend"
    ],
    "dependency_type": "blocks"
  }
]
```

`dependency_type: blocks` is the default (and currently the common) kind: the listed bead must finish before the one that depends on it. `explore.shape()` maps each bead's id to its type and aggregates `(blocked-type, blocker-type)` pairs — with a per-bead `bd dep list` fallback for bd versions that omit the embedded array.

## 5. Properties: what data does each bead carry?

Beads have no fixed schema — a property is simply present or absent per bead. The ones to check on an unknown repo:

- **labels** — free-form tags (`frontend`, `backend`). Filter with `bd list --label frontend`. Our seed has one label each on two beads, none on the rest — `bd list --no-labels` would show the untagged majority.
- **assignee** — who owns it (`bd list --assignee sergii`, `bd list --no-assignee` for orphans of ownership). Here: one owned, five unowned.
- **estimate** — time estimate in minutes (`--estimate 120` = 2 hours). Stored as `estimated_minutes` in JSON (JavaScript Object Notation).
- **due date** — `due_at` in JSON (JavaScript Object Notation); set with human words (`--due tomorrow`), stored as a timestamp.
- **metadata** — custom key-value pairs (`team=platform`), set with `--set-metadata team=platform`, filtered with `bd list --has-metadata-key team`.

One full bead as JSON (JavaScript Object Notation) shows every field at once — this is also what `db.bd_json("list", "--all")` hands your Python code:

```json
{
  "id": "tut-9x5",
  "title": "Login page bug",
  "description": "500 on empty password",
  "status": "open",
  "priority": 0,
  "issue_type": "bug",
  "assignee": "sergii",
  "estimated_minutes": 120,
  "created_at": "2026-09-08T13:58:38Z",
  "created_by": "sergii",
  "updated_at": "2026-09-08T13:58:44Z",
  "due_at": "2026-09-09T15:58:44Z",
  "labels": [
    "frontend"
  ],
  "dependency_count": 0,
  "dependent_count": 1,
  "comment_count": 0
}
```

Fields that matter: `priority` 0–4 (0 = critical, 4 = backlog); `dependency_count` / `dependent_count` (how many beads it waits on / how many wait on it — the quick way to spot the most load-bearing bead); `comment_count` (discussion happened here). Missing keys mean "not set" — no assignee key at all means unassigned, not assigned-to-nobody.

**The manual equivalent**, useful when you want to check how *consistently* a property is filled: dump all beads as JSON (JavaScript Object Notation) and count. Five of six beads with no `assignee` key tells you ownership is the exception here, not the rule — the same kind of "optional in practice" signal the Neo4j chapter finds by counting property occurrences.

## 6. Structure and health checks

Dependency cycles (A blocks B blocks A — nobody can ever start). Ours is clean:

```bash
bd dep cycles
```

```
✓ No dependency cycles detected
```

Stale beads (open work untouched for a long time — often abandoned). Fresh seed, so clean:

```bash
bd stale
```

```
✨ No stale issues found (all active)
```

Orphans (beads whose dependencies point at beads that no longer exist — leftover references after deletions or bad imports):

```bash
bd orphans
```

```
✓ No orphaned issues found
```

`explore.orphans_check()` runs `bd orphans` first and, when its output is not machine-readable, falls back to checking every dependency id against `bd list --all` itself — returning `[]` when healthy, or `[{"id": ..., "missing": ...}]` listing each broken edge.

`bd doctor` and `bd preflight` need a caveat in embedded mode. `bd doctor` does not run checks locally — it prints a troubleshooting checklist instead (that output below *is* the normal, healthy answer, same as in chapter 00):

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

`bd preflight` is not a database health check at all — it prints a *release* checklist for the `bd` tool's own repository (tests, lint, formatting), not for your beads. Real output:

```bash
bd preflight
```

```
PR Readiness Checklist:

[ ] Tests pass: go test -tags gms_pure_go -short ./...
[ ] Lint passes: golangci-lint run --build-tags=gms_pure_go ./...
[ ] Formatting: gofmt -l .
[ ] No beads pollution: check .beads/issues.jsonl diff
[ ] Nix hash current: go.sum unchanged or vendorHash updated
[ ] Version sync: version.go matches default.nix

Run 'bd preflight --check' to validate automatically.
```

Do not mistake its checklist for problems in your data. For "is my data healthy", the commands that matter are `dep cycles`, `stale` and `orphans` above.

## 7. A reusable recipe

The `explore.py` module (`project/src/beads_tutorial/explore.py`) collects this chapter into three functions — `summary()`, `shape()`, `orphans_check()` — runnable individually or through the `just` recipes:

```bash
just explore /tmp/beads-tut     # every count in this chapter, one after another
just describe /tmp/beads-tut    # just the "who blocks whom" table + orphan check
```

Real output of `just explore /tmp/beads-tut` (from `project/`):

```
uv run python -m beads_tutorial.explore --summary --cwd /tmp/beads-tut
Total: 6
By status:
  closed: 1
  in_progress: 1
  open: 4
By type:
  bug: 1
  chore: 1
  feature: 2
  task: 2
Ready to work: 2
```

Real output of `just describe /tmp/beads-tut`:

```
uv run python -m beads_tutorial.explore --shape --cwd /tmp/beads-tut && uv run python -m beads_tutorial.explore --orphans --cwd /tmp/beads-tut
chore -[blocks]-> bug: 1
feature -[blocks]-> feature: 1
feature -[blocks]-> task: 1
No orphaned issues found
```

With no path argument both recipes inspect the current folder (`.`), so inside any beads project plain `just explore` just works. Under the hood it is `python -m beads_tutorial.explore --summary --cwd <dir>` — the same call the tests exercise.

### First 10 minutes with an unknown beads repo — checklist

1. Confirm you look at the right database (`bd where`, `bd info`), and note the `bd` version (`bd --version` — `1.0.4` in this tutorial).
2. List beads and the dashboard (`bd list`, `bd list --all`, `bd status`) — open vs. closed tells you what is actionable vs. historical.
3. Find what is startable right now (`bd ready` — open beads with no active blockers).
4. Count by status, type, priority, assignee (`just explore <dir>`, or `bd list --all --json` plus Python/`jq`).
5. Run the "who blocks whom" view (`just describe <dir>`) — this is your mental map of the work.
6. Open a few beads fully (`bd show <id>`) and check labels, estimates, due dates, metadata — and how consistently they are filled.
7. Check for cycles, stale beads and orphans (`bd dep cycles`, `bd stale`, `bd orphans`) — quick data-quality smell tests.
8. Remember embedded-mode limits: `bd sql` and `bd doctor` print "not yet supported" instead of running — use JSON (JavaScript Object Notation) counting and the checklist output instead.
9. Write down what you found (even a short note) — the next person to touch this repo will thank you.

## Troubleshooting

- **`bd list` is empty but the repo should have work** — the default list hides closed beads; try `bd list --all`. If still empty, check `bd where` — you may be in the wrong folder, or `BEADS_DIR` pins `bd` to a different database (`echo $BEADS_DIR`; `unset BEADS_DIR` for this tutorial).
- **`bd sql` says "not yet supported in embedded mode"** — expected, not an error. Count via `bd list --all --json` plus Python or `jq`, or call `explore.summary()`.
- **`bd doctor` prints "not yet supported in embedded mode"** — that is normal, not a failure. Follow its checklist (`ls -la .beads/embeddeddolt/`, `bd version`).
- **`bd dep list` says "requires at least 1 arg(s)"** — it needs a bead id: `bd dep list <id> --json`. There is no whole-database dep dump; `explore.shape()` builds it by combining per-bead data.
- **`bd preflight` shows a checklist about Go tests and lint** — that is the `bd` tool's own release checklist, not your data. Ignore it for exploration; use `dep cycles` / `stale` / `orphans`.
- **`just explore` says "no beads database found"** — the recipe inspects the folder you pass (default: current folder). From `project/` there is no `.beads/`, so pass a repo explicitly: `just explore /tmp/beads-tut`. (Also note `uv run` executes from the project root, which is why the recipe passes `--cwd` explicitly instead of relying on your shell's folder.)
- **Closed beads missing from counts** — `bd list --json` excludes closed by default; `explore.summary()` uses `bd list --all --json` so history is included. If your own script counts fewer than `bd status` reports, you forgot `--all`.
- **Want a clean slate?** — a beads project is just files: delete the scratch folder (or `.beads/` inside it) and run `bd init` again. Nothing is installed system-wide.

## Key takeaways

- `bd list` / `bd show` (human-readable CLI (Command-Line Interface)), `bd --json` + `jq` (scriptable terminal), and Python via `explore.py` + `just` recipes (reusable reports) each answer "what's in here?" — pick CLI (Command-Line Interface) for a first glance, `--json` for quick scripted counts, Python when you want to save or process the output.
- `bd list`, `bd list --all`, `bd status` and `bd show <id>` give you the inventory of an unknown database; `bd ready` narrows it to work with no active blockers (closed blockers stop blocking).
- Counting `bd list --all --json` by status, type, priority and assignee — plus the type-blocks-type table from `shape()` — is the single most valuable overview; it is your mental map of the project.
- Labels, assignees, estimates, due dates and metadata are per-bead and optional — always check how consistently they are filled before relying on them, since nothing enforces their presence.
- `bd dep cycles` / `bd stale` / `bd orphans` tell you whether the data is healthy; `bd sql` and `bd doctor` are unavailable in embedded mode (use JSON (JavaScript Object Notation) counting instead), and `bd preflight` is a release checklist, not a health check.
- `explore.py`'s `summary()` / `shape()` / `orphans_check()` package this whole checklist into two commands (`just explore`, `just describe`) you can reuse on any beads database.

Next: [01_concepts.md](01_concepts.md) — beads core ideas: issues, dependencies, priorities and the daily workflow.
