# 01 — Concepts: the bead model, types, statuses, dependencies, storage

**What you will learn**
- What beads is, and the six building blocks of the bead model: bead, type, status, priority, dependency, label/metadata
- How the bead model compares to GitHub Issues and Jira (a popular team issue tracker)
- The shape of `bd` (the beads CLI (Command-Line Interface, the program you talk to by typing commands in the terminal)) commands: reading (`list`, `show`, `ready`) vs writing (`create`, `update`, `close`)
- What the fixed vocabularies are (`bd types`, `bd statuses`), and how `bd create --validate` checks your input
- What a write guarantees, ACID (Atomicity, Consistency, Isolation, Durability — the four promises a good database makes about writes), and the architecture words you'll meet later (Dolt, embedded vs server mode, `bd dolt push/pull`)
- When beads beats a plain markdown TODO list, and when GitHub Issues or Jira beat beads

All examples below were run in a scratch database (`bd init --prefix tut` in `/tmp/beads-concepts-demo`). Every output under a command block is the real output, pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way.

> Shared settings: this tutorial has no `index.md` yet; until it does, the pattern for "settings shared by all chapters" is `../neo4j/index.md` (ports, versions, dataset in one table). Verified on this machine: `bd version 1.0.4`.

## 1. What beads is

**Beads** is an issue tracker that lives inside your project folder. An issue tracker keeps a list of tasks (things to do), bugs (things that are broken) and features (new things to build). The twist: beads issues are **chained like beads on a string** — each bead knows which other beads block it, so the tracker can tell you what is startable *right now* (`bd ready`) instead of just showing a flat list.

A **bead** is one issue: a title, a description, and a handful of fields (type, status, priority) plus links to other beads. You talk to beads through `bd`, a CLI (Command-Line Interface) — one program you run from the terminal. Storage is **Dolt** (a version-controlled SQL (Structured Query Language) database — think of it as git, but for tables instead of files). You never talk to Dolt directly; `bd` does it for you.

### Compared to GitHub Issues / Jira

If you know GitHub Issues or Jira, here is the same idea in both worlds:

| GitHub Issues / Jira term | Beads term |
|---|---|
| issue | bead |
| label | label (free-form tag, same idea) |
| assignee | assignee (called "owner" in `bd show`) |
| milestone | milestone (a bead type that marks a group done) |
| linked issue | dependency (`blocks`, `related`, `parent-child`) |
| project board column (To do / In progress / Done) | status (`open` / `in_progress` / `closed`, plus more) |
| issue number (`#123`) | bead id (`tut-z89` — prefix plus short hash) |
| priority field / label | priority (`P0`–`P4`, built in) |

The key difference: in GitHub Issues, links between issues are decoration — nothing stops you from starting work whose blocker is unfinished. In beads, dependencies are **first-class** (built into the core, not an afterthought): `bd ready` hides everything with an unfinished blocker, so the answer to "what can I work on?" is always computed, never eyeballed.

Our scratch database for this chapter holds two beads, wired like this:

```bash
bd init --prefix tut --non-interactive
bd create --title="Write parser" --type task --priority 1 --description="write the parser" --json   # → tut-z89
bd create --title="Write tests" --type task --priority 2 --description="test the parser" --json     # → tut-eqa
bd dep add tut-eqa tut-z89    # Write tests is blocked by Write parser
```

Real output of the `dep add` (dependency kinds explained in §2):

```
✓ Added dependency: tut-eqa (Write tests) depends on tut-z89 (Write parser) (blocks)
```

## 2. Building blocks with ASCII art

Beads has six building blocks:

- **Bead** — one issue: an id (`tut-z89`), a title, a description. Like a row, but with links to other beads built in.
- **Type** — what kind of work it is: `task`, `bug`, `feature`, `chore`, `epic`, `decision` (and more — see `bd types` below). Like a GitHub issue template, but enforced as a fixed word.
- **Status** — what state it is in: `open`, `in_progress`, `blocked`, `deferred`, `closed` (and more — see `bd statuses` below). Like a board column, but stored on the bead itself.
- **Priority** — how urgent it is: `P0` (critical) down to `P4` (backlog). `P2` is the everyday default.
- **Dependency** — a directed link between exactly two beads: it always has one blocker and one blocked bead, and a **kind** (`blocks`, `related`, `parent-child`, `discovered-from`). "Directed" just means it points one way, like an arrow.
- **Label / metadata** — free-form extras: a **label** is a tag (`frontend`, `backend`); **metadata** is custom key/value data (`team=platform`). Unlike type and status, these are never restricted to a fixed list.

ASCII art of one dependency (the shape from our demo database, with generic ids):

```
  (tut-a1:task:P1) --blocks--> (tut-b2:task:P2)
   blocker bead    dependency   blocked bead
   type + priority   kind        type + priority
```

In our real database that looks like this — `tut-z89` (Write parser, P1) blocks `tut-eqa` (Write tests, P2):

```
  (tut-z89:task:P1) --blocks--> (tut-eqa:task:P2)
```

The four dependency kinds:

- **`blocks`** — the default: the blocked bead cannot start until the blocker finishes. Created with `bd dep add <blocked> <blocker>`. This is the only kind `bd ready` cares about.
- **`related`** — a two-way link with no blocking meaning ("these touch the same area"). Created with `bd link <id1> <id2> --type related`.
- **`parent-child`** — groups work under a bigger bead (usually an `epic` or `milestone`). Created with `bd link <child> <parent> --type parent-child`; listed with `bd children <parent-id>`.
- **`discovered-from`** — records that one bead was found while working on another (provenance, not scheduling).

### `bd types` — the fixed type vocabulary

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

An **ADR** (Architecture Decision Record) is a short note explaining *why* a technical choice was made. A **spike** is a time-boxed (given a fixed time limit) investigation. A **story** describes a feature from the user's point of view ("as a user I want...").

### `bd statuses` — the fixed status vocabulary

```bash
bd statuses
```

```
Built-in statuses:
  ○ open           [active]  Available to work (default)
  ◐ in_progress    [wip   ]  Actively being worked on
  ● blocked        [wip   ]  Blocked by a dependency
  ❄ deferred       [frozen]  Deliberately put on ice for later
  ✓ closed         [done  ]  Completed
  📌 pinned         [frozen]  Persistent, stays open indefinitely
  ◇ hooked         [wip   ]  Attached to an agent's hook

No custom statuses configured.
Configure with: bd config set status.custom "name:category,..."
Categories: active, wip, done, frozen
```

**wip** means "work in progress". Each status belongs to a **category** (active, wip, done, frozen) that tells tooling how to treat it — `bd ready`, for example, only considers `active` beads.

### `bd show` — read one bead fully

```bash
bd show tut-eqa
```

```
○ tut-eqa · Write tests   [● P2 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
test the parser

DEPENDS ON
  → ○ tut-z89: Write parser ● P1


💡 Tip: Install the beads plugin for automatic workflow context, or run 'bd setup claude' for CLI-only mode
```

One screen shows the bead's type, priority, status, owner (the assignee), and both directions of dependencies. The mirror view (`bd show tut-z89`) shows the other direction — a `BLOCKS` section listing `tut-eqa` instead of `DEPENDS ON`.

### `bd dep tree` — draw the chain

```bash
bd dep tree tut-eqa
```

```
🌲 Dependency tree for tut-eqa:

tut-eqa: Write tests [P2] (open) [BLOCKED]
    └── tut-z89: Write parser [P1] (open) [blocks]
```

(Color codes stripped — the terminal also highlights `[BLOCKED]`.) The tree answers "why can't I start this?" at a glance. The blocker's own tree is short and sweet:

```bash
bd dep tree tut-z89
```

```
🌲 Dependency tree for tut-z89:

tut-z89: Write parser [P1] (open) [READY]
```

## 3. Reading vs writing commands

`bd` commands split into two families. Details and more examples come in chapters 02–04; here's the one-line summary of each:

**Reading** (never change the data):
- `list` — human-readable table of beads (open ones by default; `--all` includes closed)
- `show <id>` — everything about one bead: description, labels, metadata, dependencies
- `ready` — open beads with no *active* (unfinished) blockers; "what can I start?"
- `blocked` — beads waiting on unfinished dependencies, and what blocks them
- `search <text>` — find beads by words in the title/description
- `status` — dashboard totals (open, in progress, blocked, closed, ready to work)
- `sql` — run a SQL (Structured Query Language) query directly (server mode only; embedded mode prints "not yet supported" — see §5)

**Writing** (change the data):
- `create` — add a new bead (always creates; duplicates are your problem)
- `update <id>` — change fields: `--status`, `--priority`, `--add-label`, `--assignee`, `--estimate`, `--due`, `--set-metadata`
- `close <id> --reason "..."` — mark finished (the everyday "I'm done")
- `dep add <blocked> <blocker>` — wire a blocking dependency; `dep relate` / `link --type` for the other kinds
- `comment <id> <text>` — attach a note to a bead's discussion

Three reads against our demo database, all real output:

```bash
bd list
```

```
○ tut-z89 ● P1 Write parser
○ tut-eqa ● P2 Write tests

--------------------------------------------------------------------------------
Total: 2 issues (2 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

```bash
bd status
```

```
📊 Issue Database Status

Summary:
  Total Issues:           2
  Open:                   2
  In Progress:            0
  Blocked:                1
  Closed:                 0
  Ready to Work:          1

For more details, use 'bd list' to see individual issues.
```

```bash
bd ready
```

```
○ tut-z89 ● P1 Write parser

--------------------------------------------------------------------------------
Ready: 1 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Only `tut-z89` is ready — `tut-eqa` waits on it. And the two remaining reads:

```bash
bd search parser
```

```
Found 1 issues matching 'parser':
tut-z89 [P1] [task] open - Write parser
```

```bash
bd blocked
```

```
🚫 Blocked issues (1):

[● P2] tut-eqa: Write tests
  Blocked by 1 open dependencies: [tut-z89]
```

## 4. Schema: optional, but you can add rules

Beads is **schema-optional**: unlike a relational database table, you don't have to declare labels or metadata keys before using them — you just start attaching them. But two vocabularies *are* fixed, and one flag checks your input.

### Labels are free-form

Any bead can carry any labels — `frontend`, `backend`, `urgent`, anything. Nothing rejects an unknown label, and nothing requires a bead to have one. Filter with `bd list --label frontend`. Metadata (custom key/value pairs like `team=platform`) works the same way: set with `--set-metadata team=platform`, filtered with `bd list --has-metadata-key team`. Chapter 001 shows how to audit consistency (count how many beads actually carry a property) on an unknown repo.

### Types, statuses and priorities are enums

An **enum** (enumeration) is a fixed list of allowed values. Type and status come from the `bd types` / `bd statuses` lists in §2 (extendable with `bd config set types.custom` / `status.custom`, but fixed unless you do). Priority is a number 0–4 (`P0` critical … `P4` backlog, `P2` default). Anything outside these is rejected at write time — which brings us to validation.

### Validation with `bd create --validate`

`--validate` asks `bd` to check the new bead against the rules *before* writing it:

```bash
bd create --title="Bad type demo" --type frobnicate --priority 2 --validate
```

```
Error: validation failed for issue : invalid issue type: frobnicate
```

Exit code 1, nothing written. Without `--validate`, some checks still apply at write time, but `--validate` is the explicit "check first, write second" switch — the beads analog of a constraint (a rule the database enforces on every write, rejecting any change that would break it). Chapter 02 covers the full create/update flag set.

## 5. Transactions and the ACID analog

A **transaction** is a group of writes that either all succeed or all fail together — nothing is left half-done. Beads leans on Dolt (the version-controlled SQL database under `.beads/`) for this.

What each write does under the hood:

1. `bd` applies your change (create, update, close, dep add, comment) to the Dolt tables.
2. Dolt **commits** (saves a versioned snapshot, like a git commit) — one commit per write by default.
3. `bd` auto-exports every issue to `.beads/issues.jsonl` — one JSON (JavaScript Object Notation, the curly-brace text format) object per line, **JSONL** (JSON Lines, one object per line) — so the current state is always readable as plain text and committable to git.

Beads (via Dolt) gives you the **ACID** guarantees for each write:

- **Atomicity** — a write's changes all happen, or none do (no half-created bead).
- **Consistency** — a write can never leave the database violating a rule (bad type/status/priority is rejected, as §4 showed).
- **Isolation** — concurrent `bd` processes don't see each other's half-finished changes (Dolt serializes the writes).
- **Durability** — once `bd` reports success, the change survives a crash right afterward (it's committed in Dolt *and* exported to `issues.jsonl`).

You can also sync history like git, because Dolt versions the tables:

- `bd dolt push` — push committed bead history to the Dolt remote (shared backup / team sync).
- `bd dolt pull` — pull teammates' bead history down.
- `bd dolt commit` — commit explicitly when auto-commit is deferred to batch mode.

### Embedded vs server mode

- **Embedded mode** (the default, `bd init`) — no server to install or start; Dolt runs inside the `bd` process and the database is just files under `.beads/embeddeddolt/`. This is what the whole tutorial uses.
- **Server mode** (`bd init --server`) — Dolt runs as a separate SQL server process that `bd` talks to over the network. Needed for `bd sql` (direct SQL queries) and for multiple machines sharing one live database. In embedded mode that command is honest about its limits:

```bash
bd sql 'SELECT status, COUNT(*) FROM issues GROUP BY status'
```

```
Error: 'bd sql' is not yet supported in embedded mode
```

That is normal, not a broken install. The replacement is `bd list --all --json` plus counting in Python or `jq` (a small command-line tool that filters JSON) — exactly what chapter 001's `explore.py` does. You lose nothing: every column SQL would read is present in the JSON.

## 6. Architecture words you will meet

- **Database vs DBMS** — the **DBMS** (Database Management System, the running database program) here is Dolt; a **database** is one named set of tables inside it (ours is named `tut`, after the `--prefix`). One Dolt DBMS can host several databases.
- **`.beads/` layout** — what `bd init` created (real listing from the demo database):

```
total 72
drwx------@ 13 sergii  wheel   416  8 wrz 16:03 .
drwxr-xr-x@  8 sergii  wheel   256  8 wrz 16:03 ..
-rw-------@  1 sergii  wheel  1615  8 wrz 16:03 .gitignore
-rw-------@  1 sergii  wheel     6  8 wrz 16:03 .local_version
-rw-------@  1 sergii  wheel  2254  8 wrz 16:03 config.yaml
drwx------@  4 sergii  wheel   128  8 wrz 16:03 embeddeddolt
-rw-------@  1 sergii  wheel   126  8 wrz 16:03 export-state.json
drwx------@  7 sergii  wheel   224  8 wrz 16:03 hooks
-rw-r--r--@  1 sergii  wheel   197  8 wrz 16:03 interactions.jsonl
-rw-r--r--@  1 sergii  wheel   291  8 wrz 16:03 issues.jsonl
-rw-------@  1 sergii  wheel     8  8 wrz 16:03 last-touched
-rw-------@  1 sergii  wheel   154  8 wrz 16:03 metadata.json
-rw-r--r--@  1 sergii  wheel  2253  8 wrz 16:03 README.md
```

What matters: `config.yaml` (project settings: prefix, export behaviour — rarely edited by hand), `embeddeddolt/` (the actual Dolt database files — never edit directly, always go through `bd`), `issues.jsonl` (appears after the first change: the auto-exported copy of every issue, the file you commit to git).

- **Dolt vs SQLite** — older beads versions stored issues in SQLite (a lightweight file-based SQL database). That backend has been removed: Dolt is now the only storage. You may still see SQLite mentioned in old docs or chat logs — treat it as history. If a command mentions `--db` pointing at a `*.db` file, that's a leftover from the SQLite era.
- **fleet (supervisor) + the ready/work/close loop** — **fleet** is the supervisor program that hands bead ids to AI coding workers. The loop is: `bd ready` (find unblocked work) → do the work → `bd close <id> --reason "..."` (mark done) → `bd dolt push` (share it). There is no `bd claim` subcommand (verified: `unknown command "claim"`); to record "I'm working on this", workers use `bd update <id> --status in_progress` or `bd assign`. Watch the loop fire in our demo — closing the blocker unblocks the next bead:

```bash
bd close tut-z89 --reason "parser done"
```

```
✓ Closed tut-z89 — Write parser: parser done
```

```bash
bd ready
```

```
○ tut-eqa ● P2 Write tests

--------------------------------------------------------------------------------
Ready: 1 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

`tut-eqa` was blocked a minute ago; with `tut-z89` closed, a finished blocker no longer blocks, and the tests bead becomes ready. That transition — blocked → ready on close — is the whole point of chaining beads.

- **Hooks (`bd hooks`)** — git hooks (small scripts git runs automatically before/after commit, push, merge) that keep beads in sync: pre-commit, post-merge, pre-push, post-checkout. Installed by `bd init` into `.beads/hooks/`; managed with `bd hooks install` / `bd hooks list`. They stop "beads pollution" (stale `issues.jsonl` diffs) and add agent-identity notes to commits.
- **Memories (`bd remember`)** — `bd remember "<insight>"` stores a note that persists across sessions (for AI assistants: injected at `bd prime` time, so every session sees it without manual loading). Example: `bd remember "always run tests with -race flag"`. Project-level long-term memory; per-bead discussion belongs in `bd comment` instead.

## 7. When to reach for beads

**Good fit (use beads):**
- Work with ordering — "B can't start until A finishes" (dependencies + `ready`)
- Many small tasks shared between humans and AI agents (fleet hands out bead ids)
- You want history versioned with the code (`.beads/issues.jsonl` commits to git next to the source)
- Offline-first tracking — no server, no account, just files (embedded mode)
- Agent coordination — `bd prime` teaches each new assistant session the workflow in ~80 lines

**Reach for a plain markdown TODO list instead:**
- One person, a dozen items, no ordering ("buy milk, fix typo, water plants")
- Throwaway notes you will delete this week — beads' commits and exports are overhead
- No one will ever ask "who blocked whom" — dependencies are beads' whole reason to exist

**Reach for GitHub Issues / Jira instead:**
- Non-technical stakeholders need a web UI, notifications, and access control
- Cross-repo planning with milestones, roadmaps, and burndown charts
- External contributors who already live on GitHub — meet them where they are
- Compliance needs (audit logs, permissions, SLAs (Service-Level Agreements, promised response times)) that files in git can't provide

Rule of thumb: markdown TODO answers "what did I write down?", beads answers "what can I start now?", GitHub Issues/Jira answers "what is the whole organization doing?".

## 8. Vocabulary cheat-sheet

| term | meaning |
|---|---|
| bead | one issue; roughly like a GitHub issue |
| type | what kind of work: `task`, `bug`, `feature`, `chore`, `epic`, `decision` (+ `spike`, `story`, `milestone`); see `bd types` |
| status | what state it's in: `open`, `in_progress`, `blocked`, `deferred`, `closed` (+ `pinned`, `hooked`); see `bd statuses` |
| priority | urgency `P0` (critical) … `P4` (backlog); `P2` is the default |
| dependency | a directed link between two beads: `blocks` (scheduling), `related`, `parent-child`, `discovered-from` |
| `blocks` | the default dependency kind: blocker must finish before the blocked bead starts |
| label | free-form tag (`frontend`); never restricted |
| metadata | custom key/value data (`team=platform`); never restricted |
| assignee / owner | who owns the bead (`bd show` prints it as "Owner") |
| estimate | time estimate in minutes (`--estimate 120` = 2 hours; stored as `estimated_minutes`) |
| `bd ready` | open beads with no active blockers — "what can I start?" |
| `bd blocked` | beads waiting on unfinished dependencies |
| `bd status` | dashboard totals |
| constraint (analog) | fixed enums + `bd create --validate` reject bad writes |
| transaction | one `bd` write = one Dolt commit; all-or-nothing |
| ACID | Atomicity, Consistency, Isolation, Durability — write guarantees |
| Dolt | the version-controlled SQL database `bd` stores beads in |
| DBMS | Database Management System — here, the running Dolt engine |
| embedded mode | default `bd init`: Dolt runs inside `bd`, database is files |
| server mode | `bd init --server`: Dolt runs as a separate process; enables `bd sql` |
| `issues.jsonl` | auto-exported plain-text copy of every issue, committed to git |
| fleet | supervisor that hands bead ids to AI workers (`ready` → work → `close`) |
| hooks | git hooks keeping beads in sync (`bd hooks`) |
| memories | cross-session notes for assistants (`bd remember`, injected at `bd prime`) |
| `bd prime` | prints the ~80-line workflow reminder assistants run each session |

## Cleanup

Close the demo beads (the same command fleet workers run when work is done):

```bash
bd close tut-eqa --reason "tests done"
```

```
✓ Closed tut-eqa — Write tests: tests done
```

Then remove the scratch database — a beads project is just files, so deleting the folder is a complete reset:

```bash
rm -rf /tmp/beads-concepts-demo
```

Nothing is installed system-wide; there is no server to stop and no Docker container to remove (unlike the Neo4j tutorial's `just down`).

## Key takeaways

- Beads is an issue tracker where issues are chained like beads: each bead knows its blockers, so `bd ready` computes "what can I start?" instead of showing a flat list.
- The bead model has six parts: beads (issues), types (fixed enum via `bd types`), statuses (fixed enum via `bd statuses`), priorities (`P0`–`P4`), dependencies (`blocks` / `related` / `parent-child` / `discovered-from`), and labels/metadata (free-form, never restricted).
- `bd` commands split into reads (`list`, `show`, `ready`, `blocked`, `search`, `status`, `sql`) and writes (`create`, `update`, `close`, `dep add`, `comment`); reads never change data.
- Labels and metadata are schema-optional, but types/statuses/priorities are enums — and `bd create --validate` rejects bad input before writing, the beads analog of a constraint.
- Every write is one Dolt (version-controlled SQL database) commit with ACID guarantees, auto-exported to `.beads/issues.jsonl`; `bd dolt push/pull` sync history like git. Embedded mode (`bd init`) needs no server; server mode (`--server`) enables `bd sql`.
- Beads shines at ordered, agent-shared work versioned with the code; plain markdown TODO wins for throwaway personal lists; GitHub Issues/Jira win for org-wide planning with a web UI and permissions.

Next: [02_create_update.md](02_create_update.md) — creating and updating beads: `create` flags, `update` fields, closing with reasons, comments, idempotent creation from Python.
