# 03 — Dependencies: wiring beads, `ready` vs `blocked`, and the agent loop

**What you will learn**
- The two ways to wire a blocking edge: `bd dep add <blocked> <blocker>` vs the `--blocks` shorthand (`bd dep <blocker> --blocks <blocked>`), and how to read the arrow direction every time
- How to read dependencies back: `bd dep list <id>` (with `--direction down/up`), `bd dep tree <id>`, `bd dep cycles`, and the `DEPENDS ON` / `BLOCKS` sections of `bd show <id>`
- What `bd ready` ("what can I start right now?") and `bd blocked` ("what is waiting, and on what?") actually compute — and why a finished blocker stops blocking
- The agent loop fleet workers run all day: `bd ready` → `bd show` → `bd update --claim` → work → `bd close --reason`, with real outputs at each step
- How to filter reads: `bd list --status open --priority 0 --type task --sort priority`, and what claiming does to `ready`
- The difference between an epic/parent (`--parent`, `bd children`) and a blocking dependency — when to use which
- What happens when you try to build a cycle (a loop: A waits on B waits on A): `bd` rejects it, `bd dep cycles` stays clean, and `bd dep remove` undoes wiring
- Troubleshooting for the three classic confusions (dependency on a closed bead, cycle rejected, `ready` empty while `list` is not) plus takeaways

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/03_dependencies`. All command outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-dep-final`, seeded with the shared graph from `project/src/beads_tutorial/seed.py`, and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. A **dependency** is a directed link between exactly two beads: one **blocker** (must finish first) and one **blocked** bead (waits). **Directed** just means the arrow points one way. A **cycle** is a loop of arrows (A waits on B waits on A) — scheduling nonsense, so `bd` refuses to store one.

## 0. The scenario and the shared graph

Every chapter reuses the same small graph, defined once at the top of `seed.py` (`project/src/beads_tutorial/seed.py`):

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

`ITEMS` is the six beads (one **epic** — a big bead that groups work — plus five **tasks**); `DEPS` is the five blocking edges, each pair reading "(blocked, blocker)". Seeding prints the six ids in `ITEMS` order:

```bash
uv run python -m beads_tutorial.seed --cwd /tmp/beads-dep-final
```

```
tut-b8m
tut-ug1
tut-9oj
tut-zyj
tut-n1n
tut-7ww
```

The mapping for this chapter (yours will differ — ids contain a random hash — but titles and shapes match):

| id | title | type | priority |
|---|---|---|---|
| `tut-b8m` | Build website | epic | P1 |
| `tut-ug1` | Design homepage | task | P1 |
| `tut-9oj` | Implement homepage | task | P1 |
| `tut-zyj` | Write tests | task | P2 |
| `tut-n1n` | Write docs | task | P2 |
| `tut-7ww` | Deploy website | task | P1 |

**Priority** is a number 0–4, printed as `P0` (critical) … `P4` (backlog); `P2` is the everyday default. Confirm the database first (`bd where` prints the folder `bd` is actually using):

```bash
bd where
```

```
/private/tmp/beads-dep-final/.beads
  prefix: tut
  database: /private/tmp/beads-dep-final/.beads/embeddeddolt
```

`prefix: tut` means new beads are named `tut-<something>`. If this path surprises you, check `echo $BEADS_DIR` first (that variable pins `bd` to one fixed database; chapter 02 troubleshooting covers it).

The full list, fresh after seeding — six beads, all `open`:

```bash
bd list
```

```
○ tut-7ww ● P1 Deploy website
○ tut-9oj ● P1 Implement homepage
○ tut-b8m ● P1 [epic] Build website
○ tut-ug1 ● P1 Design homepage
○ tut-n1n ● P2 Write docs
○ tut-zyj ● P2 Write tests

--------------------------------------------------------------------------------
Total: 6 issues (6 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

## 1. Wiring: `bd dep add` vs the `--blocks` shorthand

There are two spellings for the same edge. Learn both — you will meet both in the wild.

**Spelling 1 — `bd dep add <blocked> <blocker>`.** Reads "the first bead is blocked by the second". This is what `seed.py` runs (chapter 02, §8), one call per `DEPS` pair:

```bash
bd dep add tut-9oj tut-ug1   # Implement homepage is blocked by Design homepage
```

```
✓ Added dependency: tut-9oj (Implement homepage) depends on tut-ug1 (Design homepage) (blocks)
```

**Spelling 2 — `bd dep <blocker> --blocks <blocked>`.** Reads "the first bead blocks the second". Same edge, mirrored phrasing:

```bash
bd dep tut-ug1 --blocks tut-9oj   # Design homepage blocks Implement homepage
```

```
✓ Added dependency: tut-ug1 (Design homepage) blocks tut-9oj (Implement homepage)
```

(Re-adding an edge that already exists succeeds with the same message — dependency wiring is naturally idempotent, unlike `bd create`. That is why `seed.py` can re-run safely.)

The two commands from the demo below used throwaway beads (`Cycle A` / `Cycle B`, deleted afterwards) so the canonical graph stays untouched — but the phrasing difference is exactly what you see on real beads:

```bash
bd dep add tut-elx tut-4qq   # Cycle A is blocked by Cycle B
```

```
✓ Added dependency: tut-elx (Cycle A) depends on tut-4qq (Cycle B) (blocks)
```

```bash
bd dep tut-4qq --blocks tut-elx   # Cycle B blocks Cycle A (same edge)
```

```
✓ Added dependency: tut-4qq (Cycle B) blocks tut-elx (Cycle A)
```

Rule of thumb for reading any wiring command: find the word `blocks` / `depends on`, then ask "who waits?". In `dep add A B`, **A waits** (A is blocked by B). In `dep A --blocks B`, **B waits** (A blocks B). Both lines above describe one arrow: `tut-4qq → tut-elx` (blocker first, waiter second).

The default (and only scheduling) kind is `blocks`. Other kinds exist (`related`, `parent-child`, `discovered-from` — chapter 01, §2) but `bd ready` ignores everything except `blocks`. When this chapter says "dependency" without qualification, it means a `blocks` edge.

## 2. Reading dependencies: `dep list`, `dep tree`, `show`

Three reads answer three questions: "what does X wait on?", "what is the whole chain?", "what does one bead look like?".

### `bd dep list <id>`: direct neighbours

Default direction is `down` (dependencies = blockers = "what does this bead wait on?"):

```bash
bd dep list tut-9oj
```

```
  tut-ug1: Design homepage [P1] (open) via blocks
```

```bash
bd dep list tut-9oj --direction down
```

```
  tut-ug1: Design homepage [P1] (open) via blocks
```

Same answer — `down` is the default. Flip to `up` (dependents = "who waits on this bead?"):

```bash
bd dep list tut-9oj --direction up
```

```
  tut-n1n: Write docs [P2] (open) via blocks
  tut-zyj: Write tests [P2] (open) via blocks
```

Two beads wait on Implement. The design bead has no blockers and one dependent:

```bash
bd dep list tut-ug1
```

```
tut-ug1 has no dependencies
```

```bash
bd dep list tut-ug1 --direction up
```

```
  tut-9oj: Implement homepage [P1] (open) via blocks
```

And the deploy bead waits on two:

```bash
bd dep list tut-7ww
```

```
  tut-n1n: Write docs [P2] (open) via blocks
  tut-zyj: Write tests [P2] (open) via blocks
```

(Note: bare `bd dep list` with no id errors with `requires at least 1 arg(s)` — always pass at least one id. That error is normal, not a broken install.)

### `bd dep tree <id>`: the whole chain

`dep list` shows one hop; `dep tree` draws the full ancestry:

```bash
bd dep tree tut-7ww
```

```
🌲 Dependency tree for tut-7ww:

tut-7ww: Deploy website [P1] (open) [BLOCKED]
    ├── tut-n1n: Write docs [P2] (open) [blocks]
        └── tut-9oj: Implement homepage [P1] (open) [blocks]
            └── tut-ug1: Design homepage [P1] (open) [blocks]
    └── tut-zyj: Write tests [P2] (open) [blocks]
```

(Color codes stripped — the terminal also highlights `[BLOCKED]`.) Deploy waits on two beads; one branch goes three deep. A bead with nothing above it shows `[READY]`:

```bash
bd dep tree tut-ug1
```

```
🌲 Dependency tree for tut-ug1:

tut-ug1: Design homepage [P1] (open) [READY]
```

### `bd show <id>`: both directions on one screen

```bash
bd show tut-9oj
```

```
○ tut-9oj · Implement homepage   [● P1 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
build it

DEPENDS ON
  → ○ tut-ug1: Design homepage ● P1

BLOCKS
  ← ○ tut-n1n: Write docs ● P2
  ← ○ tut-zyj: Write tests ● P2
```

`DEPENDS ON` (with `→`) lists blockers — "I wait on these". `BLOCKS` (with `←`) lists dependents — "these wait on me". One screen, both arrow directions. The deploy bead shows only the first section:

```bash
bd show tut-7ww
```

```
○ tut-7ww · Deploy website   [● P1 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
ship it

DEPENDS ON
  → ○ tut-n1n: Write docs ● P2
  → ○ tut-zyj: Write tests ● P2
```

## 3. `bd ready` vs `bd blocked`: the scheduler

These two commands are beads' killer feature — the answer to "what can I start?" computed from the arrows, never eyeballed.

- **`bd ready`** — open beads with no *active* (unfinished) blockers. "Active" means not `closed` (and not deferred/ done-category states): a finished blocker no longer blocks.
- **`bd blocked`** — beads waiting on at least one unfinished dependency, with the blocker list attached.

Fresh database, nothing done yet:

```bash
bd ready
```

```
○ tut-ug1 ● P1 Design homepage
○ tut-b8m ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 2 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Only Design and the epic are startable — everything else waits behind them. The mirror view:

```bash
bd blocked
```

```
🚫 Blocked issues (4):

[● P1] tut-7ww: Deploy website
  Blocked by 2 open dependencies: [tut-n1n tut-zyj]

[● P1] tut-9oj: Implement homepage
  Blocked by 1 open dependencies: [tut-ug1]

[● P2] tut-n1n: Write docs
  Blocked by 1 open dependencies: [tut-9oj]

[● P2] tut-zyj: Write tests
  Blocked by 1 open dependencies: [tut-9oj]
```

Four blocked, two ready, six total — the arithmetic always adds up (`ready + blocked + in_progress + closed = total`). The epic is ready because nothing blocks it (epics group work; §6 explains why it has no arrows at all).

This is the Neo4j-chapter-03 moment for beads: just as `MATCH`/`WHERE`/`RETURN` are the reads everything else builds on, `dep list` / `dep tree` / `ready` / `blocked` are the reads every agent loop builds on.

## 4. The agent loop: `ready` → `show` → `claim` → work → `close`

Fleet workers (AI coding agents handed bead ids by the **fleet** supervisor program) run one loop all day. Here it is against the real database, step by step.

**Step 1 — `bd ready`: find unblocked work.**

```
○ tut-ug1 ● P1 Design homepage
○ tut-b8m ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 2 issues with no active blockers
```

Pick the highest-priority real task: `tut-ug1` (Design homepage, P1). (The epic is a container, not work — §6.)

**Step 2 — `bd show`: read the bead before touching it.**

```bash
bd show tut-ug1
```

```
○ tut-ug1 · Design homepage   [● P1 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
draft layout

BLOCKS
  ← ○ tut-9oj: Implement homepage ● P1
```

Description says what to do; `BLOCKS` says who is waiting on you (Implement) — extra motivation to finish.

**Step 3 — `bd update --claim`: say "I'm on it".** `--claim` sets the assignee to you and the status to `in_progress` in one step (there is no `bd claim` subcommand — fleet workers claim with `update --claim`). It is idempotent: claiming twice is harmless.

```bash
bd update tut-ug1 --claim
```

```
✓ Updated issue: tut-ug1 — Design homepage
```

Watch what claiming does to the schedule — the claimed bead leaves `ready` (it is being worked, not waiting):

```bash
bd ready
```

```
○ tut-b8m ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 1 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Design vanished from `ready` — not because it is blocked, but because it is `in_progress`. (`bd ready` lists `open` beads here; claimed work is excluded.)

**Step 4 — do the work.** (Draft the layout. This chapter skips the actual homepage.)

**Step 5 — `bd close --reason`: finish, always with a reason.**

```bash
bd close tut-ug1 --reason "design done"
```

```
✓ Closed tut-ug1 — Design homepage: design done
```

The close unblocks the next bead — a finished blocker no longer blocks:

```bash
bd ready
```

```
○ tut-9oj ● P1 Implement homepage
○ tut-b8m ● P1 [epic] Build website

--------------------------------------------------------------------------------
Ready: 2 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Implement flipped from blocked to ready. The `--reason` (`design done`) becomes part of the record — future `bd history` shows *why* it closed. And `show` now renders the finished blocker with a tick:

```bash
bd show tut-9oj
```

```
○ tut-9oj · Implement homepage   [● P1 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
build it

DEPENDS ON
  → ✓ tut-ug1: Design homepage ● P1

BLOCKS
  ← ○ tut-n1n: Write docs ● P2
  ← ○ tut-zyj: Write tests ● P2
```

`→ ✓ tut-ug1` — the tick means "finished, no longer blocking". The loop then repeats: `ready` says Implement, so claim Implement, build it, close it — and Tests and Docs both become ready at once.

## 5. Filtering reads and claim semantics

`bd list` takes filters that combine freely. The most precise one first — open, P0, tasks, sorted by priority:

```bash
bd list --status open --priority 0 --type task --sort priority
```

```
No issues found.
```

Empty is a real answer: nothing in this database is P0. (A **filter** is a flag that narrows which beads a read returns; `--sort priority` orders them most-urgent first.) Loosen to P1:

```bash
bd list --status open --priority 1 --type task --sort priority
```

```
○ tut-7ww ● P1 Deploy website
○ tut-9oj ● P1 Implement homepage

--------------------------------------------------------------------------------
Total: 2 issues (2 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

(Taken before the §4 close; after it, Design is `closed` so the same filter still shows these two — Design left the `open` set.) All open tasks regardless of priority:

```bash
bd list --status open --type task --sort priority
```

```
○ tut-7ww ● P1 Deploy website
○ tut-9oj ● P1 Implement homepage
○ tut-n1n ● P2 Write docs
○ tut-zyj ● P2 Write tests

--------------------------------------------------------------------------------
Total: 4 issues (4 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

P1s first, then P2s — `--sort priority` earns its keep. Note the epic is missing: `--type task` excludes it (it is `--type epic`). Drop the type filter to see everything, epic included.

**Claim semantics, precisely:** `--claim` = `--assignee <you> --status in_progress` in one flag. Effects on reads: the bead leaves `bd ready` (no longer `open`), appears as `in_progress` in `bd list` totals and `bd status`, and still appears in `bd blocked` *dependents* lists of others (claiming does not unwire arrows — only `close` / `dep remove` change the graph). Claiming is advisory ("hands off, I'm on it"), not structural; closing is structural (it changes what `ready` computes). Fleet relies on both: claim so two workers never grab the same bead, close so the next bead becomes ready.

## 6. Epic/parent vs blocking dep: grouping is not scheduling

Two different relationships, two different commands. Mixing them up is the most common modeling mistake after duplicate titles.

- **Blocking dep** (`bd dep add`) — scheduling: "B can't start until A finishes". Affects `ready`/`blocked`. Drawn by `dep tree`.
- **Parent** (`--parent`, listed by `bd children`) — grouping: "this small bead belongs to that big bead". Does **not** affect `ready`/`blocked`. Drawn by `children`.

The tutorial epic has no arrows at all — verify:

```bash
bd dep list tut-b8m
```

```
tut-b8m has no dependencies
```

```bash
bd children tut-b8m
```

```
Issue 'tut-b8m' has no children
```

No dependencies *and* no children: the seed wires scheduling only, and the epic floats beside the graph rather than above it. To group work under it, create with `--parent`:

```bash
bd create --title="Subtask demo" --type task --priority 2 --parent tut-b8m --json
```

```json
{
  "created_at": "2026-09-08T14:20:48.029375Z",
  "created_by": "sergii",
  "id": "tut-b8m.1",
  "issue_type": "task",
  "priority": 2,
  "schema_version": 1,
  "status": "open",
  "title": "Subtask demo",
  "updated_at": "2026-09-08T14:20:48.029375Z"
}
```

Note the dotted id (`tut-b8m.1`) — children of a parent get hierarchical ids. Now the epic has a child:

```bash
bd children tut-b8m
```

```
○ tut-b8m ● P1 [epic] Build website
└── ○ tut-b8m.1 ● P2 Subtask demo

--------------------------------------------------------------------------------
Total: 2 issues (2 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

But the child is still `ready` — parenting never blocks:

```bash
bd ready
```

```
○ tut-9oj ● P1 Implement homepage
○ tut-b8m ● P1 [epic] Build website
○ tut-b8m.1 ● P2 Subtask demo ← Build website

--------------------------------------------------------------------------------
Ready: 3 issues with no active blockers

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

(The `← Build website` suffix marks parented beads in `ready`.) The demo child was deleted after this section (`bd delete tut-b8m.1 --force`) to restore the canonical six — grouping demos should not pollute the scheduling graph.

**When to use which:**

| | parent (`--parent` / `children`) | blocking dep (`dep add` / `dep tree`) |
|---|---|---|
| Answers | "what belongs together?" | "what must wait?" |
| Affects `ready`? | never | yes — the only thing `ready` reads |
| Typical parent | epic, milestone | any finished task |
| Create with | `bd create --parent <epic>` or `bd link <child> <parent> --type parent-child` | `bd dep add <blocked> <blocker>` |
| Good for | breaking an epic into subtasks, dashboards | ordering work, agent scheduling |

Use both on the same beads when both are true: subtasks grouped under the epic *and* chained among themselves with `dep add`. They are orthogonal — one bead can have a parent and blockers simultaneously.

## 7. Cycles: `bd` refuses them, `dep cycles` proves it, `dep remove` cleans up

A cycle (A waits on B waits on A) means nothing can ever start — so `bd` rejects the closing edge at write time. Reproduce it with the throwaway beads (real output):

```bash
bd dep add tut-elx tut-4qq   # Cycle A is blocked by Cycle B — fine
```

```
✓ Added dependency: tut-elx (Cycle A) depends on tut-4qq (Cycle B) (blocks)
```

```bash
bd dep add tut-4qq tut-elx   # Cycle B blocked by Cycle A — would close the loop
```

```
Error: adding dependency would create a cycle
```

Exit code non-zero, nothing written. The `--no-cycle-check` flag (meant for bulk wiring — "wire fast now, verify with `dep cycles` after") does not override this: the same command with the flag errors identically on this version (`bd version 1.0.4`). Verify the graph is still clean:

```bash
bd dep cycles
```

```
✓ No dependency cycles detected
```

(The `--json` form prints `[]` — an empty **JSON** array, JavaScript Object Notation, the bracket text format scripts parse.) And the tree shows a plain one-hop chain, not a loop:

```bash
bd dep tree tut-elx
```

```
🌲 Dependency tree for tut-elx:

tut-elx: Cycle A [P2] (open) [BLOCKED]
    └── tut-4qq: Cycle B [P2] (open) [blocks]
```

One level deep — B has nothing above it, so no loop exists. Now undo the demo edge:

```bash
bd dep remove tut-elx tut-4qq
```

```
✓ Removed dependency: tut-elx (Cycle A) no longer depends on tut-4qq (Cycle B)
```

(`bd dep rm` is an alias.) The tree flips to `[READY]` — with no blockers, A is startable again:

```bash
bd dep tree tut-elx
```

```
🌲 Dependency tree for tut-elx:

tut-elx: Cycle A [P2] (open) [READY]
```

```bash
bd dep cycles
```

```
✓ No dependency cycles detected
```

Both demo beads were deleted afterwards (`bd delete tut-elx tut-4qq --force`), restoring the canonical six. Takeaway: you will likely never *see* a cycle in `bd dep cycles` output precisely because the write path refuses to create one — the command exists as a bulk-wiring safety net and a troubleshooting backstop, and `dep remove <blocked> <blocker>` (blocked first, blocker second — same order as `dep add`) is how any unwanted edge comes off.

## 8. Troubleshooting

- **Depending on a closed bead is allowed — and usually harmless.** `bd dep add` does not reject a finished blocker (verified: wiring Tests to the already-closed Design succeeds). A closed blocker simply does not block: `ready` ignores it, `show` renders it with a `✓`, and the tree prints it as `(closed)`. The demo edge was removed right after (`bd dep remove tut-zyj tut-ug1`) to keep the canonical graph. If you *meant* the bead to gate work, you wired the wrong id — check `bd show` statuses first.
- **"Error: adding dependency would create a cycle"** — you just tried to close a loop (§7). Nothing was written; the graph is unchanged. Draw the chain with `bd dep tree <id>` on both endpoints to see which existing arrow completes the loop, then either drop the new edge (change the plan) or `bd dep remove` the old edge that should not be there.
- **`bd ready` is empty but `bd list` is not** — every open bead has an unfinished blocker. Run `bd blocked` to see the waiter → blocker table, then `bd dep tree` on the bead you expected to be ready to find the hidden blocker (often two hops up — e.g. Deploy looks ready until the tree reveals Implement behind Tests). Either finish the blocker (`claim` → work → `close`) or, if the arrow is wrong, `bd dep remove` it.
- **`bd dep list` with no id says "requires at least 1 arg(s)"** — the command needs a bead. `bd dep list tut-9oj` (one hop down by default), `--direction up` for dependents. There is no whole-database edge dump; `bd blocked` plus per-bead `dep list` cover it.
- **Parent shows no children / child not blocked** — both normal. `bd children` only lists `--parent` / `parent-child` links, never `blocks` edges; and parenting never affects `ready` (§6). If the child should wait, add a real `bd dep add` alongside the parent.
- **`bd list --status open --priority 0` prints "No issues found"** — not an error: no bead matches. Loosen one filter at a time (drop `--priority`, then `--type`) until beads appear, as §5 does.
- **Want a clean slate?** — a beads project is just files: delete the scratch folder (or `.beads/` inside it), `bd init --prefix tut --non-interactive` again, then re-seed (`uv run python -m beads_tutorial.seed --cwd <dir>` from `project/`). Nothing is installed system-wide.

## Key takeaways

- Two spellings, one arrow: `bd dep add <blocked> <blocker>` ("A waits on B") and `bd dep <blocker> --blocks <blocked>` ("A blocks B"). Re-adding an existing edge succeeds — wiring is idempotent.
- Three reads: `bd dep list <id>` (one hop; `--direction down` for blockers, `up` for dependents), `bd dep tree <id>` (full ancestry, `[READY]` vs `[BLOCKED]`), `bd show <id>` (`DEPENDS ON →` blockers, `← BLOCKS` dependents).
- `bd ready` (open beads, no unfinished blockers) and `bd blocked` (waiters plus who blocks them) are computed from `blocks` edges only; a `closed` blocker stops blocking (`→ ✓` in `show`).
- The agent loop: `bd ready` (pick work) → `bd show` (read it) → `bd update --claim` (assignee + `in_progress`, leaves `ready`) → work → `bd close --reason` (unblocks dependents, rejoins `ready`). Reasons are mandatory history.
- `bd list` filters (`--status`, `--priority`, `--type`, `--sort priority`) combine freely; `No issues found` means "no match", not failure. Claiming is advisory (visibility), closing is structural (schedule).
- Parent (`--parent`, `bd children`, dotted ids like `tut-b8m.1`) groups; `dep add` schedules. They are orthogonal — use both when both are true. Only `blocks` feeds `ready`.
- Cycles are rejected at write time (`Error: adding dependency would create a cycle`); `bd dep cycles` confirms clean (`✓ No dependency cycles detected` / `[]`), and `bd dep remove <blocked> <blocker>` unwires any edge.
- The graph lives in `seed.py` (`ITEMS` + `DEPS`, check-then-create + `dep add` wiring) — every chapter seeds the same six beads, so trees and `ready` sets are comparable across chapters.

Next: [04_search_views.md](04_search_views.md) — finding beads: `search`, `list` filters in depth, `status` dashboards, and saved views.
