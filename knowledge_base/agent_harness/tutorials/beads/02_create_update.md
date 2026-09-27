# 02 — Creating and updating beads: the write lifecycle

**What you will learn**
- Why beads has rules (a **constraint** is a rule the database enforces on every write) and how to see them first with `bd types`
- What priorities `P0`–`P4` mean, and how `bd create --validate` checks your input before writing
- The difference between plain `bd create` (always makes a new bead, like Neo4j's `CREATE`) and the idempotent seed (reuses what exists, like Neo4j's `MERGE`)
- How to create many beads at once: `bd create --file`, a loop with `--json`, and `just seed`
- How to discuss work on a bead (`bd comment`) vs attach lasting notes to it (`bd note`)
- The update/claim flow: `bd update --claim`, `--assignee`, `--priority`, `--status`
- How to finish work (`bd close --reason`) and undo a close (`bd reopen`)
- The check-then-create pattern in Python that makes `seed.py` safe to re-run any number of times

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/02_create_update`. All command outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-writes-demo` and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. **Idempotent** means running an operation twice has the same effect as running it once — the single most important word in this chapter.

## 0. The scenario and the shared graph

Chapter 001 taught you to explore a database; chapter 01 taught you the model. Now you build one from nothing. Every later chapter reuses the same small graph, so let's define it once:

- One **epic** (a big bead that groups work): `Build website`
- Five **tasks**: `Design homepage`, `Implement homepage`, `Write tests`, `Write docs`, `Deploy website`
- Wiring: Implement is blocked by Design; Tests and Docs are each blocked by Implement; Deploy is blocked by both Tests and Docs

Confirm you are in the right database first (`bd where` prints the folder `bd` is actually using — it discovers `.beads/` from your current folder, unless the `BEADS_DIR` environment variable pins it somewhere else):

```bash
bd where
```

```
/private/tmp/beads-writes-demo/.beads
  prefix: tut
  database: /private/tmp/beads-writes-demo/.beads/embeddeddolt
```

`prefix: tut` means new beads will be named `tut-<something>`. If this path surprises you, check `echo $BEADS_DIR` first (see Troubleshooting).

## 1. Constraints first: `bd types` and priorities

A **constraint** is a rule the database enforces on every write, rejecting any change that would break it. In Neo4j you create uniqueness constraints before loading (chapter 02 of that tutorial); in beads two vocabularies are already fixed, so "constraints first" means *reading* them before you write anything:

```bash
bd types
```

```
Core work types (built-in):
  task           General work item (default)
  bug            Bug report or defect
  feature        New feature or enhancement
  chore          Maintenance or housekeeping
  epic           Large body of work spanning multiple issues
  decision       Architecture decision record (ADR)
  spike          Timeboxed investigation to reduce uncertainty before committing to a story
  story          User story describing a feature from the user's perspective
  milestone      Marks completion of a set of related issues (contains no work itself)

No custom types configured.
Configure with: bd config set types.custom "type1,type2,..."
```

An **ADR** (Architecture Decision Record) is a short note explaining *why* a technical choice was made. A **spike** is an investigation with a fixed time limit. Our epic (`Build website`) uses type `epic`; everything else is a `task`.

**Priority** is a number 0–4, printed as `P0`–`P4`:

| value | meaning | when to use it |
|---|---|---|
| `P0` | critical | something is broken or blocked and everything waits on it |
| `P1` | high | the main line of work (our epic, design, implement, deploy) |
| `P2` | medium | the everyday default (`bd create` uses it when you say nothing) |
| `P3` | low | nice to have, no rush |
| `P4` | backlog | someday, maybe never |

`--validate` asks `bd` to check the new bead against the rules *before* writing it — the beads analog of a constraint rejecting a bad write:

```bash
bd create --title="Bad type demo" --type frobnicate --priority 2 --validate
```

```
Error: validation failed for issue : invalid issue type: frobnicate
```

Exit code 1, nothing written. `frobnicate` is not in the `bd types` list, so the write is refused. Pass a real type and the same command succeeds.

## 2. CREATE vs MERGE analog: plain create vs idempotent seed

In Neo4j, `CREATE` always adds a new node (duplicates are your problem) while `MERGE` means "find it, or create it if missing". Beads works the same way:

- **`bd create` always creates.** Run the same command twice and you get two beads with the same title. Watch — this is the single most common mistake when scripting beads:
- **The seed (`seed.py` + `just seed`) is the `MERGE`.** It lists existing beads first and reuses any bead whose title already exists. Run it ten times, still six beads.

The duplicate, reproduced on purpose (note the new id — same title, different bead):

```bash
bd create --title="Write tests" --type task --priority 2 --description="accidental rerun" --json
```

```json
{
  "created_at": "2026-09-08T14:10:43.109936Z",
  "created_by": "sergii",
  "description": "accidental rerun",
  "id": "tut-j24",
  "issue_type": "task",
  "priority": 2,
  "schema_version": 1,
  "status": "open",
  "title": "Write tests",
  "updated_at": "2026-09-08T14:10:43.109936Z"
}
```

(`--json` asks for machine-readable output — **JSON**, JavaScript Object Notation, the curly-brace text format Python's `json` module reads. This is exactly what `db.bd_create()` parses to get the id.)

Nothing stopped that duplicate: beads has no uniqueness rule on titles, just like Neo4j without a constraint lets `CREATE` duplicate nodes. The fix is the same in both worlds — never blindly create in a script; check first, then create (§8 shows the pattern, and the stray `tut-j24` was deleted after this demo to keep the database at the canonical six).

## 3. Creating the graph, one bead at a time

The epic first (`--type epic`, `--priority 1`):

```bash
bd create --title="Build website" --type epic --priority 1 --description="tutorial epic: a tiny website" --json
```

```json
{
  "created_at": "2026-09-08T14:10:42.187061Z",
  "created_by": "sergii",
  "description": "tutorial epic: a tiny website",
  "id": "tut-wqy",
  "issue_type": "epic",
  "priority": 1,
  "schema_version": 1,
  "status": "open",
  "title": "Build website",
  "updated_at": "2026-09-08T14:10:42.187061Z"
}
```

The id `tut-wqy` starts with our prefix. Then the first task:

```bash
bd create --title="Design homepage" --type task --priority 1 --description="draft layout" --json
```

```json
{
  "created_at": "2026-09-08T14:10:43.109936Z",
  "created_by": "sergii",
  "description": "draft layout",
  "id": "tut-c5b",
  "issue_type": "task",
  "priority": 1,
  "schema_version": 1,
  "status": "open",
  "title": "Design homepage",
  "updated_at": "2026-09-08T14:10:43.109936Z"
}
```

The remaining four are created the same way (one command each, `--json` piped through Python to show just id and title):

```
tut-k85 Implement homepage
tut-5b9 Write tests
tut-t71 Write docs
tut-wwf Deploy website
```

Now wire the dependencies. `bd dep add <blocked> <blocker>` always reads "the first bead is blocked by the second":

```bash
bd dep add tut-k85 tut-c5b   # Implement homepage is blocked by Design homepage
bd dep add tut-5b9 tut-k85   # Write tests is blocked by Implement homepage
bd dep add tut-t71 tut-k85   # Write docs is blocked by Implement homepage
bd dep add tut-wwf tut-5b9   # Deploy website is blocked by Write tests
bd dep add tut-wwf tut-t71   # Deploy website is blocked by Write docs
```

```
✓ Added dependency: tut-k85 (Implement homepage) depends on tut-c5b (Design homepage) (blocks)
✓ Added dependency: tut-5b9 (Write tests) depends on tut-k85 (Implement homepage) (blocks)
✓ Added dependency: tut-t71 (Write docs) depends on tut-k85 (Implement homepage) (blocks)
✓ Added dependency: tut-wwf (Deploy website) depends on tut-5b9 (Write tests) (blocks)
✓ Added dependency: tut-wwf (Deploy website) depends on tut-t71 (Write docs) (blocks)
```

Re-running a `dep add` for an edge that already exists succeeds with the same message (exit code 0) — dependency wiring is naturally idempotent, unlike `create`. (Chapter 03 covers dependency kinds in depth; here `blocks` — the default — is all we need.)

The shape of what we built, drawn by `bd dep tree` (color codes stripped — the terminal also highlights `[BLOCKED]`):

```bash
bd dep tree tut-wwf
```

```
🌲 Dependency tree for tut-wwf:

tut-wwf: Deploy website [P1] (open) [BLOCKED]
    ├── tut-5b9: Write tests [P2] (open) [blocks]
        └── tut-k85: Implement homepage [P1] (open) [blocks]
            └── tut-c5b: Design homepage [P1] (open) [blocks]
    └── tut-t71: Write docs [P2] (open) [blocks]
```

And `bd ready` ("what can I start right now?" — open beads with no *active*, unfinished, blockers):

```bash
bd ready
```

```
○ tut-c5b ● P1 Design homepage
○ tut-wqy ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 2 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Only Design and the epic are startable — everything else waits behind them. That is the whole point of chaining beads.

## 4. Batch creation: file, loop, and `just seed`

Creating six beads by hand is fine once. For ten or a hundred, three faster options — the beads analog of Neo4j's `LOAD CSV` / `UNWIND` batch loading:

**Option A — `bd create --file`.** One markdown file, one heading per bead (demoed in a separate scratch database, `/tmp/beads-batch-demo`):

```bash
bd create --file /tmp/batch.md
```

```
✓ Created 2 issues from /tmp/batch.md:
  tut-h2f: Task one [P2, task]
  tut-ui4: Task two [P2, task]
```

Good for a quick one-off import. It always creates — re-run the same file and you get duplicates (the §2 problem again).

**Option B — a shell loop with `--json`.** This is how the four task ids in §3 were captured: one `bd create --json` per title, parsing each output. One process per bead, simple and readable, fast enough for dozens of beads.

**Option C — `just seed` (the reusable loader).** The `seed` recipe in `project/justfile` runs the Python loader from §8 against any folder:

```just
seed repo=".":
    uv run python -m beads_tutorial.seed --cwd {{repo}}
```

```bash
just seed /tmp/beads-cli-check
```

```
tut-1cz
tut-smg
tut-7kg
tut-fft
tut-3am
tut-eqd
```

With no argument it seeds the current folder (`.`). Unlike A and B it is idempotent: run it again and it prints the *same six ids* without creating anything.

| | `bd create --file` | shell loop with `--json` | `seed.py` (`just seed`) |
|---|---|---|---|
| Runs in | `bd` (markdown parsing) | shell + `bd`, once per bead | Python, calling `bd` per bead |
| Duplicates on re-run? | yes | yes | no (check-then-create) |
| Wires dependencies? | no | only if you add `dep add` calls | yes, built in |
| Good for | quick one-off imports | small scripts | repeatable project setup, used by every later chapter |

## 5. Comments and notes: discussion vs lasting state

Two ways to attach text to a bead, and they are not the same:

- **`bd comment <id> <text>`** — a discussion entry: who said what, when. Think chat log on the bead.
- **`bd note <id> <text>`** — appends to the bead's lasting **notes** field. Think the bead's own notebook.

```bash
bd comment tut-c5b "Started the layout sketch"
```

```
✓ Comment added to tut-c5b — Design homepage
```

```bash
bd note tut-c5b "colors: blue header"
```

```
✓ Note added to tut-c5b — Design homepage
```

Read the discussion back:

```bash
bd comments tut-c5b
```

```

Comments on tut-c5b:

[sergii] at 2026-09-08 14:11
  Started the layout sketch
```

Notes instead show up inside `bd show` (next section) under a `NOTES` heading — they travel with the bead rather than living in the discussion thread. Rule of thumb: progress chatter goes in comments, decisions and facts you will need later go in notes.

## 6. Update and claim: who does what, how urgent, what state

`bd update <id>` changes fields on an existing bead. Three everyday uses:

**Claiming** — "I'm working on this." `--claim` sets the assignee to you and the status to `in_progress` in one step (and it is idempotent — claiming twice is harmless):

```bash
bd update tut-c5b --claim
```

```
✓ Updated issue: tut-c5b — Design homepage
```

(There is no `bd claim` subcommand — fleet workers claim with `update --claim` or `--status in_progress`.)

**Assigning, reprioritizing, moving state** — each flag changes one field; combine them freely:

```bash
bd update tut-k85 --assignee sergii --priority 1 --status in_progress
```

```
✓ Updated issue: tut-k85 — Implement homepage
```

`--assignee` sets the owner, `--priority` takes `0`–`4` (or `P0`–`P4`), `--status` moves the bead (`open`, `in_progress`, `blocked`, `deferred`, `closed` — the `bd statuses` list from chapter 01).

One screen showing everything the last two sections did:

```bash
bd show tut-c5b
```

```
◐ tut-c5b · Design homepage   [● P1 · IN_PROGRESS]
Owner: sergii · Assignee: sergii · Type: task
Created: 2026-09-08 · Started: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
draft layout

NOTES
colors: blue header

BLOCKS
  ← ◐ tut-k85: Implement homepage ● P1

COMMENTS
  2026-09-08 14:11 sergii
    Started the layout sketch
```

`◐` means in progress; the bead now has an owner, a note, a comment, and one bead waiting on it. Passing values safely: `db.py` runs `bd` with `subprocess` (Python's built-in way of starting other programs) and a list of arguments — never glued into a shell string. That is the beads analog of Neo4j's parameters (`$name` instead of pasting values into Cypher): a title containing quotes or spaces can never break the command or change what it does, because values travel as data, never as text mixed into the command.

## 7. Close and reopen: finishing work (and undoing it)

Closing is the everyday "I'm done". Always give a `--reason` — it becomes part of the record:

```bash
bd close tut-c5b --reason "design done"
```

```
✓ Closed tut-c5b — Design homepage: design done
```

Watch what the close does to the schedule — the blocker is finished, so the next bead becomes startable. Before the close, `Implement homepage` was blocked; `bd ready` right after shows the epic still ready (and `Implement`, now `in_progress` from §6, is being worked rather than waiting):

```bash
bd ready
```

```
○ tut-wqy ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 1 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

(A finished blocker no longer blocks — the blocked → ready transition from chapter 01. `bd ready` lists `open` beads here; the `in_progress` implement bead is excluded because it is already claimed, not waiting.)

Closed by mistake, or the work needs another pass? `bd reopen` flips it back to `open` (more explicit than `update --status open`, and it records a Reopened event):

```bash
bd reopen tut-c5b --reason "need a tweak"
```

```
↻ Reopened tut-c5b: need a tweak
```

The dashboard right after the reopen — six beads, none closed, one in progress:

```bash
bd status
```

```

📊 Issue Database Status

Summary:
  Total Issues:           6
  Open:                   5
  In Progress:            1
  Blocked:                4
  Closed:                 0
  Ready to Work:          1

For more details, use 'bd list' to see individual issues.
```

Then close it again for real (the design work is done — the rest of the tutorial assumes it):

```bash
bd close tut-c5b --reason "design done"
```

```
✓ Closed tut-c5b — Design homepage: design done
```

`bd close` accepts several ids at once (`bd close tut-a tut-b --reason "..."`), and `bd close` with no id closes the last-touched bead — convenient, but prefer explicit ids in scripts so a reordered command never closes the wrong bead.

## 8. `seed.py`: a reusable, idempotent loader

The full file lives at `project/src/beads_tutorial/seed.py` (64 lines). Key pieces, in the order they run:

**1. The graph is data** — titles, types, priorities, and dependency pairs at the top, so every chapter shares one definition:

```python
ITEMS = [
    ("Build website", "epic", 1, "tutorial epic: a tiny website"),
    ("Design homepage", "task", 1, "draft layout"),
    ("Implement homepage", "task", 1, "build it"),
    ("Write tests", "task", 2, "test it"),
    ("Write docs", "task", 2, "document it"),
    ("Deploy website", "task", 1, "ship it"),
]

DEPS = [
    ("Implement homepage", "Design homepage"),
    ("Write tests", "Implement homepage"),
    ("Write docs", "Implement homepage"),
    ("Deploy website", "Write tests"),
    ("Deploy website", "Write docs"),
]
```

**2. Check-then-create** — list everything once (`bd list --all --json`, so even *closed* beads match — otherwise re-seeding after closing work would duplicate it), reuse titles that exist, create only what is missing:

```python
existing = {i["title"]: i["id"] for i in db.bd_json("list", "--all", cwd=cwd)}
ids: dict = {}
for title, kind, prio, desc in ITEMS:
    if title in existing:
        ids[title] = existing[title]
    else:
        ids[title] = existing[title] = db.bd_create(
            title, cwd=cwd, type=kind, priority=prio, description=desc)
```

This is the beads version of Neo4j's `MERGE`: match by the natural key (here the title), create only on a miss. `db.bd_create()` is the thin wrapper from chapter 00 — one `bd create --json`, id parsed out of the output.

**3. Wire dependencies after every bead exists** — dependencies need both endpoints, so all creates run first, then the five `dep add` calls (safe to repeat: re-adding an existing edge succeeds):

```python
for blocked, blocker in DEPS:
    try:
        db.run_bd("dep", "add", ids[blocked], ids[blocker], cwd=cwd)
    except RuntimeError as exc:
        if "already" not in str(exc).lower():
            raise
```

**4. A CLI that prints the ids** — `python -m beads_tutorial.seed --cwd <dir>`, wrapped by `just seed`:

```python
def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed the tutorial graph.")
    parser.add_argument("--cwd", default=".", help="project folder with .beads/")
    args = parser.parse_args(argv)
    for bead_id in seed(args.cwd):
        print(bead_id)
    return 0
```

## 9. Proving it works, and proving it's idempotent

First run against a fresh database (`bd init --prefix tut` in `/tmp/beads-cli-check`):

```bash
uv run python -m beads_tutorial.seed --cwd /tmp/beads-cli-check
```

```
tut-1cz
tut-smg
tut-7kg
tut-fft
tut-3am
tut-eqd
```

Six ids: the epic plus five tasks, in `ITEMS` order. Second run, same command, right after:

```
tut-1cz
tut-smg
tut-7kg
tut-fft
tut-3am
tut-eqd
```

Identical ids — nothing new created. The test suite (`project/tests/test_seed.py`) pins this down: it seeds a scratch repo in a temporary folder, seeds *again*, and asserts the second run returns the same ids with the total still at 6:

```bash
uv run pytest tests/test_seed.py tests/test_setup.py tests/test_explore.py -q
```

```
....                                                                     [100%]
4 passed in 29.92s
```

And the database agrees — `bd list --all --json` (which includes closed beads, unlike plain `bd list`) counts exactly 6:

```
6
```

## Troubleshooting

- **Same title twice — which bead is which?** Nothing stops `bd create` from duplicating a title (§2: a second `Write tests` came back as `tut-j24`). If you already have dupes, `bd list --all` shows both — tell them apart by id, description, and status, then `bd delete <stray-id> --force` the stray one. To stop it happening: use `just seed` (check-then-create) instead of raw `bd create` in scripts.
- **`bd create --title="X" --id other-1` fails with "prefix mismatch"** — ids must start with the database prefix (`tut-` here). Real error:
  ```
  Error: prefix mismatch: database uses 'tut-' but ID 'other-1' doesn't match (use --force to override)
  ```
  Either drop `--id` (recommended — let `bd` generate it) or pass `--force` if you really mean it.
- **`bd create --validate` rejects your type** — the type is not in `bd types` (verified above: `frobnicate` → `Error: validation failed for issue : invalid issue type: frobnicate`). Use one of the built-in types or add a custom one with `bd config set types.custom`.
- **"Error: no beads database found"** — you are in a folder without `.beads/`, or `BEADS_DIR` pins `bd` to a different database. Real error:
  ```
  Error: no beads database found
  Hint: run 'bd where' to inspect the resolved workspace, or 'bd init' to create a new database
        or set BEADS_DIR to point to your .beads directory
  ```
  Fix: `cd` into your project and run `bd where` (the path should end in *your* project's `.beads`); if `echo $BEADS_DIR` prints something, `unset BEADS_DIR` for this tutorial. Fresh start: `bd init --prefix <name> --non-interactive`.
- **`bd list` is missing beads you just created** — the default list hides closed beads; use `bd list --all`. `seed.py` uses `--all` for exactly this reason.
- **Reopen says nothing to reopen / close says already closed** — check `bd show <id>` for the current status first; `reopen` only works on closed beads, and closing a closed bead is a no-op complaint, not damage.
- **Want a clean slate?** — a beads project is just files: delete the scratch folder (or `.beads/` inside it) and run `bd init` again, then `just seed <dir>`. Nothing is installed system-wide.

## Key takeaways

- Read the rules before writing: `bd types` (fixed type vocabulary), priorities `P0` (critical) … `P4` (backlog, `P2` default), and `bd create --validate` to check input before it lands — the beads analog of constraints.
- Plain `bd create` always creates (Neo4j's `CREATE`) — re-running a script duplicates titles. The idempotent seed (Neo4j's `MERGE`) checks first via `bd list --all --json` and reuses matches, so any number of runs leaves the same 6 beads.
- Batch options, fastest to most reusable: `bd create --file` (one markdown file, always creates), a loop with `bd create --json` (one process per bead), `just seed` (check-then-create plus dependency wiring — the loader every later chapter uses).
- Discussion (`bd comment`, read back with `bd comments`) is not state (`bd note`, read back in `bd show` under `NOTES`) — chatter in the former, lasting facts in the latter.
- `bd update <id> --claim` records "I'm on it" (assignee + `in_progress`, idempotent); `--assignee`, `--priority`, `--status` change one field each and combine freely. Values travel as argument lists via `db.py`, never pasted into shell strings — the parameters analog.
- `bd close <id> --reason "..."` finishes work and unblocks whatever waited on it (`blocked` → ready); `bd reopen <id> --reason "..."` undoes a close explicitly. Always pass a reason, and prefer explicit ids over the last-touched default in scripts.
- `seed.py` is 64 lines: graph as data, `bd list --all` check-then-create, `dep add` wiring afterwards, `--cwd` CLI — proven by running it twice (same six ids) and by `test_seed.py`.

Next: [03_dependencies.md](03_dependencies.md) — dependency kinds in depth: `blocks` vs `related` vs `parent-child`, trees, cycles, and what `bd ready` really computes.
