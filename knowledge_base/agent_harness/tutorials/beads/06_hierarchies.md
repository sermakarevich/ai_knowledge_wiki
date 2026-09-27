# 06 — Hierarchies: epics, parent-child, and the five link types

**What you will learn**
- The five link types beads understands — `blocks`, `parent-child`, `related`, `tracks`, `discovered-from` — with the `bd link --type` syntax for each, and when to use hierarchy (structure: what belongs together) vs sequencing (order: what waits on what)
- The epic lifecycle: an **epic** is a large container bead that groups child beads; create one with `bd create --type epic`, attach children with `bd create --parent <epic>`, inspect with `bd children <id>` and `bd list --parent <id>`, track with `bd epic status`, and finish with `bd epic close-eligible`
- When to group with an epic vs a **label** (a free-text tag like `tutorial-docs` you can put on any bead and filter by)
- Tree vs graph: `bd list --parent` draws the family tree while `bd dep tree` draws the dependency graph, and why both matter
- The DAG (Directed Acyclic Graph, nodes + one-way edges with no loops) rule: `blocks` loops are rejected at write time, `bd dep cycles` proves the graph is clean, but `parent-child` back-edges slip through — so validate hierarchy yourself
- The fleet pattern: one epic per feature, children claimed in parallel via `bd ready`, swarm validates the DAG (Directed Acyclic Graph, nodes + one-way edges with no loops) before spawning workers (forward pointer to chapter 07)
- Troubleshooting for three classic confusions (child of a closed epic, mixing `parent-child` + `blocks` on the same pair, orphans) plus takeaways

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/06_hierarchies`. All command outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-hier-final`, built with `python -m beads_tutorial.hierarchy --demo --cwd /tmp/beads-hier-final`, and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. A **CLI** (Command-Line Interface) is a program you drive by typing commands; `bd` is the CLI for beads. **JSON** (JavaScript Object Notation) is the machine-readable text format `bd` prints when you pass `--json`.

## 0. The scenario and the demo graph

Chapters 03–05 worked with a flat graph: tasks wired only by `blocks` edges. That scales poorly — with twenty tasks you cannot tell which belong to the website relaunch and which belong to the billing migration. The fix is hierarchy: one **epic** (a large container bead grouping child beads) per workstream, children underneath it, `blocks` edges only between siblings that truly order each other.

The companion module for this chapter is `project/src/beads_tutorial/hierarchy.py` (imports `db.py` only). Its four functions map one-to-one onto CLI commands:

```python
def make_epic(title: str, cwd: str) -> str: ...          # bd create --type epic
def add_child(epic_id: str, title: str, cwd: str) -> str: ...  # bd create --parent <epic>
def link_blocked(blocked: str, blocker: str, cwd: str, link_type: str = "blocks") -> None: ...
def epic_status(epic_id: str, cwd: str) -> dict: ...    # bd epic status + bd children --json
```

`cwd` is the project folder whose `.beads/` database you want to talk to. The `--demo` entry point builds an epic plus three children plus one `blocks` edge and prints the tree:

```bash
uv run python -m beads_tutorial.hierarchy --demo --cwd /tmp/beads-hier-final
```

```
epic: tut-3id
  child: tut-3id.1
  child: tut-3id.2
  child: tut-3id.3
  blocks: tut-3id.2 waits on tut-3id.1
○ tut-3id ● P2 [epic] Website relaunch
├── ○ tut-3id.1 ● P2 Design homepage
├── ○ tut-3id.2 ● P2 Implement homepage
└── ○ tut-3id.3 ● P2 Write docs

--------------------------------------------------------------------------------
Total: 4 issues (4 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

(The tree at the end is `bd list --parent <epic>` — the module falls back to it when `bd children --pretty` is unavailable; see §4.) The mapping for this chapter (yours will differ — ids contain a random hash — but titles and shapes match):

| id | title | type | parent |
|---|---|---|---|
| `tut-3id` | Website relaunch | epic | — |
| `tut-3id.1` | Design homepage | task | `tut-3id` |
| `tut-3id.2` | Implement homepage | task | `tut-3id` |
| `tut-3id.3` | Write docs | task | `tut-3id` |

Plus one sequencing edge: `tut-3id.2` is blocked by `tut-3id.1` (implement waits on design). Confirm the database first (`bd where` prints the folder `bd` is actually using):

```bash
bd where
```

```
/private/tmp/beads-hier-final/.beads
  prefix: tut
  database: /private/tmp/beads-hier-final/.beads/embeddeddolt
```

`prefix: tut` means new beads are named `tut-<something>`, and children of `tut-3id` get dotted ids (`tut-3id.1`, …). If this path surprises you, check `echo $BEADS_DIR` first (that variable pins `bd` to one fixed database; chapter 02 troubleshooting covers it).

## 1. The five link types: hierarchy vs sequencing

Every relationship between two beads has a type. There are exactly five, and they answer two different questions — "what belongs together?" (hierarchy) vs "what waits on what?" (sequencing):

| type | question it answers | blocks `bd ready`? | example syntax |
|---|---|---|---|
| `blocks` | sequencing: B must finish before A starts | yes | `bd link tut-3id.2 tut-3id.1` (default type) |
| `parent-child` | hierarchy: A belongs to epic B | no | `bd create "X" --parent tut-3id`, or `bd link A B --type parent-child` |
| `related` | "these touch each other", no order implied | no | `bd link tut-3id.3 tut-3id.1 --type related` |
| `tracks` | "A follows B's progress", soft follow | no | `bd link tut-3id.3 tut-3id.2 --type tracks` |
| `discovered-from` | "A was found while working on B" (provenance) | no | `bd link tut-3id.4 tut-3id.1 --type discovered-from` |

Only `blocks` affects scheduling: `bd ready` ("what can I start right now?") hides beads whose blockers are still open. The other four are information — they show up in `bd dep list` and `bd show` but never gate `ready`. That is the whole decision rule:

- **Hierarchy** (`parent-child`): use when beads form a workstream. "These three tasks are the website relaunch." The epic is the folder; children are the files.
- **Sequencing** (`blocks`): use when order matters. "Implement waits on design." Keep these edges between siblings, never between epic and child (the epic is done when its children are done — that is what `bd epic status` computes, not a `blocks` edge).
- **The other three** (`related` / `tracks` / `discovered-from`): use for cross-references that should notserialize work. A docs task *related* to design can start immediately; a follow-up *discovered from* a bug remembers where it came from.

Here is each non-blocking type being created for real (on `tut-3id.3`, Write docs), then removed again to keep the demo graph clean:

```bash
bd link tut-3id.3 tut-3id.1 --type related
bd link tut-3id.3 tut-3id.2 --type tracks
bd dep list tut-3id.3
```

```
✓ Linked: tut-3id.3 (Write docs) depends on tut-3id.1 (Design homepage) (related)
✓ Linked: tut-3id.3 (Write docs) depends on tut-3id.2 (Implement homepage) (tracks)
  tut-3id: Website relaunch [P2] (open) via parent-child
  tut-3id.1: Design homepage [P2] (open) via related
  tut-3id.2: Implement homepage [P2] (open) via tracks
```

```bash
bd dep remove tut-3id.3 tut-3id.1
bd dep remove tut-3id.3 tut-3id.2
```

```
✓ Removed dependency: tut-3id.3 (Write docs) no longer depends on tut-3id.1 (Design homepage)
✓ Removed dependency: tut-3id.3 (Write docs) no longer depends on tut-3id.2 (Implement homepage)
```

And `discovered-from`, shown later in §6 when a follow-up bead is found during the close-out flow. Note the read-back verbs: `bd dep list <id>` shows every edge regardless of type, with the type printed after `via`.

## 2. Epic lifecycle, step by step

An epic is born, fills with children, drains as children close, and dies when nothing is left open. Each transition is one command.

**Step 1 — create the epic** (`make_epic` / `bd create --type epic`):

```bash
bd create "Website relaunch" --type epic --priority 1 --json
```

(The demo already created `tut-3id` this way; `--type epic` is the only thing distinguishing an epic from a task at creation time.)

**Step 2 — attach children** (`add_child` / `bd create --parent <epic>`). The `--parent` flag does two things at once: it sets the child's `parent` field and stores a `parent-child` dependency edge from child to epic. One JSON record shows both:

```bash
bd children tut-3id --json
```

```json
{
  "id": "tut-3id.4",
  "title": "Late fix",
  "status": "open",
  "priority": 2,
  "issue_type": "task",
  "dependencies": [
    {
      "issue_id": "tut-3id.4",
      "depends_on_id": "tut-3id",
      "type": "parent-child"
    },
    {
      "issue_id": "tut-3id.4",
      "depends_on_id": "tut-3id.1",
      "type": "discovered-from"
    }
  ],
  "parent": "tut-3id"
}
```

(`tut-3id.4` is the late follow-up from §6; the three demo children have the same shape with a single `parent-child` edge.) Two fields tell the same story in two formats: `parent` is the quick pointer, `dependencies[]` is the typed edge the graph commands understand.

**Step 3 — list the family.** Two commands, different defaults — this trips everyone up once:

```bash
bd list --parent tut-3id
```

```
✓ tut-3id ● P2 epic Website relaunch
└── ○ tut-3id.4 ● P2 Late fix

--------------------------------------------------------------------------------
Total: 2 issues (1 open, 0 in progress)
```

`bd list --parent` draws the tree but shows only *open* children by default (the three demo children are closed by now, so only `tut-3id.4` appears). `bd children <id>`, by contrast, is documented as a convenience alias for `bd list --parent <id> --status all` — it *includes closed issues*, since its main use is auditing all work under a parent. Rule of thumb: `bd list --parent` for "what is left?", `bd children` for "what ever happened here?".

**Step 4 — track completion** (`epic_status` / `bd epic status`):

```bash
bd epic status tut-3id
bd epic status tut-3id --json
```

```
○ tut-3id Website relaunch
   Progress: 0/3 children closed (0%)
```

```json
[
  {
    "epic": {
      "id": "tut-3id",
      "title": "Website relaunch",
      "status": "open",
      "priority": 2,
      "issue_type": "epic"
    },
    "total_children": 3,
    "closed_children": 0,
    "eligible_for_close": false
  }
]
```

(The text form was captured when the demo was fresh; the `--json` form shows the machine-readable row.) `eligible_for_close` flips to `true` only when every child is closed. The Python helper merges this row with the child list into one dict:

```bash
uv run python -m beads_tutorial.hierarchy --epic-status tut-3id --cwd /tmp/beads-hier-final
```

```json
{
  "epic_id": "tut-3id",
  "title": "Website relaunch",
  "total_children": 3,
  "closed_children": 0,
  "open_children": [
    "tut-3id.3",
    "tut-3id.2",
    "tut-3id.1"
  ],
  "eligible_for_close": false
}
```

**Step 5 — close the epic.** First check eligibility, then close children, then the epic itself:

```bash
bd epic close-eligible
bd close tut-3id.1 tut-3id.2 tut-3id.3 --reason "tutorial done"
bd epic status tut-3id
bd epic close-eligible
bd close tut-3id --reason "all children done"
```

```
No epics eligible for closure
✓ Closed tut-3id.1 — Design homepage: tutorial done
✓ Closed tut-3id.2 — Implement homepage: tutorial done
✓ Closed tut-3id.3 — Write docs: tutorial done
✓ tut-3id Website relaunch
   Progress: 3/3 children closed (100%)
   Eligible for closure
✓ Closed 1 epic(s)
  - tut-3id
✓ Closed tut-3id — Website relaunch: all children done
```

Two things to notice. First, an epic with open children refuses to close (`cannot close epic tut-3id: 2 open child issue(s); close children first or use --force to override` — captured on the probe database). Second, `bd epic close-eligible` does not just *report* — it *closes* every eligible epic (note `✓ Closed 1 epic(s)`). It is a verb, not a query; preview with `--dry-run` if you only want the list.

## 3. Epic vs label grouping

Epics are not the only way to group beads. A **label** (a free-text tag attached with `--labels`) cuts across hierarchies: one bead can carry many labels, and labels ignore the tree entirely.

```bash
bd create "Extra task" --labels tutorial-docs --json
bd list --label tutorial-docs
```

```
tut-6kh None
○ tut-6kh ● P2 Extra task

--------------------------------------------------------------------------------
Total: 1 issues (1 open, 0 in progress)
```

(The `None` is the labels field as this `bd` version renders it in `--json`; `bd list --label` is the reliable way to query.) When to use which:

- **Epic**: the bead *belongs* to exactly one workstream, has a lifecycle (open → eligible → closed), and shows progress (`2/3 children closed`). One parent per bead.
- **Label**: the bead *relates* to a theme across workstreams (`tutorial-docs` could tag beads under three different epics). Many labels per bead, no progress tracking, no lifecycle.

Fleet rule: structure with epics, cross-reference with labels. Never emulate an epic by slapping the same label on ten beads — you lose `bd epic status` and `close-eligible`, the two commands that let a supervisor know a workstream is finished.

## 4. Tree vs graph: `bd list --parent` vs `bd dep tree`

Two commands draw two different pictures of the same database. Confusing them is the most common hierarchy mistake.

- `bd list --parent <epic>` draws the **family tree**: who belongs to whom. One level, `parent-child` edges only, open children by default.
- `bd dep tree <id>` draws the **dependency graph** around one bead: every edge type, blockers and parents mixed, annotated per line.

Compare them on the blocked child `tut-3id.2`:

```bash
bd dep tree tut-3id.2
bd dep tree tut-3id
```

```

🌲 Dependency tree for tut-3id.2:

tut-3id.2: Implement homepage [P2] (open) [BLOCKED]
    ├── tut-3id: Website relaunch [P2] (open) [parent-child]
    └── tut-3id.1: Design homepage [P2] (open) [blocks]
```

```

🌲 Dependency tree for tut-3id:

tut-3id: Website relaunch [P2] (open) [READY]
```

The child's tree shows *both* relationships at a glance: it belongs to the epic (`[parent-child]`) and it waits on design (`[blocks]`, hence `[BLOCKED]`). The epic's own tree shows just itself as `[READY]` — an epic is never blocked by its children; its completion is computed by `bd epic status`, not by the scheduler. And `bd show` splits the same information into sections:

```bash
bd show tut-3id.2
```

```
○ tut-3id.2 · Implement homepage   [● P2 · OPEN]
Owner: sergii · Type: task
Created: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
  (none)

PARENT
  ↑ ○ tut-3id: (EPIC) Website relaunch ● P2

DEPENDS ON
  → ○ tut-3id.1: Design homepage ● P2
```

`PARENT` is hierarchy, `DEPENDS ON` is sequencing — the same split as the link-type table in §1, now visible on a single bead.

## 5. The DAG rule and `bd dep cycles`

A **DAG** (Directed Acyclic Graph, nodes + one-way edges with no loops) is the one scheduling law: arrows must never loop back on themselves, or "what do I do first?" has no answer. Beads enforces this for `blocks` edges *at write time* — try to make design wait on implement while implement already waits on design:

```bash
bd dep add tut-3id.1 tut-3id.2
bd dep cycles
```

```
Error: adding dependency would create a cycle
```

```

✓ No dependency cycles detected

```

The write is refused, and `bd dep cycles` confirms the stored graph is clean. This is the behavior your fleet workers rely on: parallel claims are safe because a `blocks` loop can never be stored.

But — and this matters for supervisors — the guard does **not** cover `parent-child` edges. Linking the epic *back onto its own child* succeeds:

```bash
bd link tut-3id tut-3id.4 --type parent-child
bd dep cycles
```

```
✓ Linked: tut-3id (Website relaunch) depends on tut-3id.4 (Late fix) (parent-child)
```

```

✓ No dependency cycles detected

```

The epic now "depends on" its child via `parent-child`, the arrows loop (child → epic → child), and `bd dep cycles` still reports clean — it only watches the sequencing edges. Lesson: never `bd link` an epic onto one of its own children, and have the swarm validate hierarchy separately from `blocks` (chapter 07 shows the validation molecule). The write-time guard protects scheduling; hierarchy hygiene is the supervisor's job.

## 6. Fleet pattern: one epic per feature

Here is how agentic workers use all of the above. One **epic** per feature, children small enough to claim independently, `blocks` edges only where order truly matters:

1. **Supervisor creates the epic and its children** (`make_epic` + `add_child`), wiring `blocks` edges between siblings with `link_blocked`. No worker has started yet — the DAG (Directed Acyclic Graph, nodes + one-way edges with no loops) is fully known up front.
2. **Workers claim via `bd ready`.** `ready` already understands both halves: hierarchy never gates, `blocks` always gates. On the fresh demo graph:

```bash
bd ready
```

```
○ tut-3id.3 ● P2 Write docs ← Website relaunch
○ tut-3id ● P2 [epic] Website relaunch
○ tut-3id.1 ● P2 Design homepage ← Website relaunch

--------------------------------------------------------------------------------
Ready: 3 issues with no active blockers
```

Three claimable items: the epic itself, design, and docs. Implement (`tut-3id.2`) is absent — blocked on design. Two workers can grab design and docs in parallel with zero coordination; whoever finishes design unblocks implement, which appears in `ready` on the next poll. The `← Website relaunch` suffix tells each worker which workstream it serves.

3. **Workers record provenance with `discovered-from`.** Mid-feature, a worker finds a follow-up ("while implementing, noticed the homepage needs a late fix"). It creates the bead under the same epic and links where it came from — no new `blocks` edge, so nothing serializes:

```bash
bd create "Late fix" --parent tut-3id --json
bd link tut-3id.4 tut-3id.1 --type discovered-from
bd dep list tut-3id.4
```

```
tut-3id.4 Late fix open
✓ Linked: tut-3id.4 (Late fix) depends on tut-3id.1 (Design homepage) (discovered-from)
  tut-3id: Website relaunch [P2] (closed) via parent-child
  tut-3id.1: Design homepage [P2] (closed) via discovered-from
```

4. **Swarm validates the DAG before spawning** (chapter 07's molecule): run `bd dep cycles`, assert `epic_status(... )["eligible_for_close"]` is `False` while work remains, and check no epic links back onto its children (§5). Only then fan out.
5. **Supervisor drains with `bd epic status` / `close-eligible`** (§2, Step 5) instead of tracking ten child ids by hand.

## 7. Troubleshooting

**Child of a closed epic is allowed — and that is usually a smell.** After the epic closed in §2, creating `tut-3id.4 --parent tut-3id` succeeded (`tut-3id.4 Late fix open`). Beads does not forbid it: the child is just an open bead with a closed parent. If you meant to reopen the workstream, also reopen the epic (`bd update <epic> --status open`); if the follow-up belongs to new work, create a new epic instead of piling children onto a closed one.

**Mixing `parent-child` + `blocks` on the same pair is rejected.** The two beads already have one typed edge; adding a second type between the same pair fails:

```bash
bd link tut-3id.2 tut-3id.1 --type parent-child
```

```
Error: dependency tut-3id.2 -> tut-3id.1 already exists with type "blocks" (requested "parent-child"); remove it first with 'bd dep remove' then re-add
```

Decide what the relationship *is*: structure (`parent-child`, usually via `--parent` at creation) or order (`blocks`). If you genuinely need to change it, `bd dep remove` the old edge first. Siblings under one epic virtually always want `blocks`.

**Orphaned children: `bd orphans` is not what you think.** The name suggests "children without parents", but `bd orphans` actually finds issues referenced in commit messages that remain open — implemented-but-not-closed work:

```bash
bd orphans
```

```
✓ No orphaned issues found
```

To find *hierarchy* strays (top-level beads that should belong to an epic), list with `bd list --no-parent` and attach them with `bd update <id> --parent <epic>` — or close the loop the other way and create the missing epic.

## Takeaways

- Five link types, two questions: `parent-child` for structure, `blocks` for order, `related` / `tracks` / `discovered-from` for notes that never gate `bd ready`. Only `blocks` serializes work.
- Epic lifecycle in five commands: `bd create --type epic` → `bd create --parent` → `bd children` / `bd list --parent` → `bd epic status` → `bd epic close-eligible`. The Python helpers in `hierarchy.py` wrap exactly these.
- `bd list --parent` shows the open remainder; `bd children` audits everything including closed. `bd dep tree` shows the graph around one bead with per-edge types; `bd show` splits hierarchy (`PARENT`) from sequencing (`DEPENDS ON`).
- The DAG (Directed Acyclic Graph, nodes + one-way edges with no loops) rule is enforced for `blocks` at write time and audited with `bd dep cycles` — but `parent-child` back-edges slip through, so supervisors validate hierarchy themselves.
- Fleet shape: one epic per feature, claim children via `bd ready`, record surprises with `discovered-from`, drain with `epic status` / `close-eligible`. Prefer epics over label-soup for anything with a finish line.

Next: [07_molecules.md](07_molecules.md)
