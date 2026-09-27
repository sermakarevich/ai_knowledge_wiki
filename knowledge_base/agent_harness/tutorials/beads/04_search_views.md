# 04 — Search, views, and sync: finding beads, counting them, and moving them

**What you will learn**
- Full-text search: `bd search "keyword"` (title search, description search with `--desc-contains`, why closed beads are excluded by default)
- Structured queries: `bd query "status=open AND priority=1"` (a tiny query language with `AND` / `OR` / `NOT`), and the fallback when you forget the syntax: `bd list --title-contains --label`
- Label, priority, and assignee filters on `bd list` (`--label`, `--priority`, `--assignee`, `--no-assignee`), and how they combine
- Health views: `bd status` (dashboard), `bd stale` (forgotten work), `bd orphans` (beads with no links), `bd count` (grouped totals)
- Aggregations two ways: `bd count --by-status/--by-priority/--by-type` (runs everywhere) and raw **SQL** (Structured Query Language — the standard language for asking tables questions) via `bd sql` (server mode only; embedded mode says so honestly)
- `CASE`-like grouping with `jq` (a command-line tool that slices and groups **JSON** — JavaScript Object Notation, the bracket-and-quotes text format scripts parse) over `bd list --json`
- Writing back: `bd update` (labels, assignee, priority) and `bd delete` (permanent — caution box included)
- The `EXPLAIN` analog (in Neo4j, `EXPLAIN` shows the query plan without running the query): `bd doctor`, `bd preflight`, `bd lint`, plus `bd info`
- Sync and backup: `bd export -o file.jsonl`, `bd import`, `bd backup`, and `bd dolt push/pull` (**Dolt** is the version-controlled database under `bd`; push/pull sync it with a remote, like `git push`)
- Troubleshooting (empty search, export paths, `bd sql` table discovery) plus takeaways

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/04_search_views`. All command outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-search-tut`, seeded with the shared graph from `project/src/beads_tutorial/seed.py`, and pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. This chapter is the beads mirror of the Neo4j tutorial's `04_advanced_queries.md`: where Neo4j has `MATCH`/`WHERE`/`COUNT`/`CASE`/`EXPLAIN`, beads has `search`/`query`/`count`/jq-grouping/`doctor` — same ideas, different spelling.

## 0. The scenario and the shared graph

Same six beads as every chapter (`seed.py`: `ITEMS` + `DEPS`, check-then-create so re-running is safe). Seeding prints the six ids in `ITEMS` order:

```bash
uv run python -m beads_tutorial.seed --cwd /tmp/beads-search-tut
```

```
tut-xbl
tut-icv
tut-ra2
tut-y1l
tut-4tn
tut-vhe
```

The mapping for this chapter (yours will differ — ids contain a random hash — but titles and shapes match):

| id | title | type | priority |
|---|---|---|---|
| `tut-xbl` | Build website | epic | P1 |
| `tut-icv` | Design homepage | task | P1 |
| `tut-ra2` | Implement homepage | task | P1 |
| `tut-y1l` | Write tests | task | P2 |
| `tut-4tn` | Write docs | task | P2 |
| `tut-vhe` | Deploy website | task | P1 |

**Priority** is a number 0–4, printed as `P0` (critical) … `P4` (backlog); `P2` is the everyday default. Confirm the database first (`bd where` prints the folder `bd` is actually using):

```bash
bd where
```

```
/private/tmp/beads-search-tut/.beads
  prefix: tut
  database: /private/tmp/beads-search-tut/.beads/embeddeddolt
```

`prefix: tut` means new beads are named `tut-<something>`. A note on running these commands: this machine pins `bd` to the fleet database via the `BEADS_DIR` variable (an environment variable is a named setting inherited by every command you run — chapter 02 troubleshooting covers it). Every command below was run with that pin removed (`env -u BEADS_DIR bd ...`) from inside `/tmp/beads-search-tut`, so `bd` uses the scratch database. If your outputs mention a different folder, check `echo $BEADS_DIR` first.

The full list, fresh after seeding — six beads, all `open`:

```bash
bd list
```

```
○ tut-icv ● P1 Design homepage
○ tut-ra2 ● P1 Implement homepage
○ tut-vhe ● P1 Deploy website
○ tut-xbl ● P1 [epic] Build website
○ tut-4tn ● P2 Write docs
○ tut-y1l ● P2 Write tests

--------------------------------------------------------------------------------
Total: 6 issues (6 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

And the engine facts (`bd version`, `bd info`) — worth knowing before the SQL section surprises you:

```bash
bd version
```

```
bd version 1.0.4 (ce242a879: ce242a879678)
```

```bash
bd info
```

```
Beads Database Information
===========================
Database: /private/tmp/beads-search-tut/.beads/embeddeddolt
Mode: direct

Issue Count: 6
```

`Mode: direct` means embedded mode (the database runs inside the `bd` process; no server). Remember that line — it explains the `bd sql` and `bd doctor` errors in §7 and §9.

## 1. Full-text search: `bd search "keyword"`

In Neo4j you build an index and then `MATCH` against it. In beads the index is built in — `bd search` looks through titles (and ids) out of the box:

```bash
bd search "homepage"
```

```
Found 2 issues matching 'homepage':
tut-ra2 [P1] [task] open - Implement homepage
tut-icv [P1] [task] open - Design homepage
```

Two hits: Design and Implement. Search is case-insensitive substring matching, so `"Homepage"`, `"home"`, and `"page"` all match the same two beads. Partial ids work too — `bd search "tut-r"` finds by id prefix (fast exact/prefix matching, per `--help`).

Descriptions are **not** searched by default. The seed descriptions (`draft layout`, `build it`, `test it`, `document it`, `ship it`) live in a separate field, so `bd search "document"` alone finds nothing about Write docs — you need `--desc-contains`:

```bash
bd search "docs" --desc-contains "document"
```

```
Found 1 issues matching 'docs':
tut-4tn [P2] [task] open - Write docs
```

Here `"docs"` matches the title *and* `--desc-contains "document"` must match the description (`document it`). Both conditions apply — title query plus description filter.

The single most important search default: **closed beads are excluded**. Just as a Neo4j index only contains what you put in it, `bd search` only looks at non-closed beads unless asked:

```bash
bd search "homepage" --status all
```

```
Found 2 issues matching 'homepage':
tut-ra2 [P1] [task] open - Implement homepage
tut-icv [P1] [task] open - Design homepage
```

Same answer here (nothing is closed yet), but after you close beads the two commands diverge: bare `bd search "homepage"` will stop showing finished work, while `--status all` keeps showing it. Other useful search flags from `--help`: `--label` (only beads carrying a label — §3 adds one), `--assignee`, `--priority-min/--priority-max`, `--sort priority|created|updated`, `--limit` (default 50), and `--desc-contains` / `--notes-contains` for the long-text fields.

## 2. Structured queries: `bd query` (and the `bd list` fallback)

`bd search` is one free-text box. `bd query` is the `WHERE` clause: field-by-field comparisons (`field=value`, `field!=value`, `field>value`, `field<=value`) glued with boolean operators (`AND` = both must match, `OR` = either matches, `NOT` = negates). This is the closest beads gets to Cypher's `WHERE`:

```bash
bd query "status=open AND priority=1"
```

```
Found 4 issues:
○ tut-vhe [● P1] [task] - Deploy website
○ tut-ra2 [● P1] [task] - Implement homepage
○ tut-icv [● P1] [task] - Design homepage
○ tut-xbl [● P1] [epic] - Build website
```

Four P1 beads, all open. Narrow by type as well:

```bash
bd query "type=task AND priority=2"
```

```
Found 2 issues:
○ tut-4tn [● P2] [task] - Write docs
○ tut-y1l [● P2] [task] - Write tests
```

The two P2 tasks — the epic is P1 so it drops out, and `type=task` would exclude it anyway. More recipes from `--help` that work on this database: `bd query "NOT status=closed"` (everything not finished — all six here), `bd query "assignee=none AND type=task"` (unassigned tasks — all five tasks, since nobody claimed anything yet), `bd query "title=homepage AND priority=1"` (title-contains plus priority), and date filters like `created>30d` (created in the last 30 days — all six, seeded minutes ago).

Forgot the query syntax? The fallback is `bd list` with one flag per field — same filters, no expression language:

```bash
bd list --title-contains homepage
```

```
○ tut-icv ● P1 Design homepage
○ tut-ra2 ● P1 Implement homepage

--------------------------------------------------------------------------------
Total: 2 issues (2 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

Same two beads as `bd search "homepage"`. Rule of thumb: `bd search` for "find the bead I'm thinking of", `bd query` for compound conditions (`AND`/`OR`/`NOT`, ranges), `bd list --flag` when you want one simple filter plus the familiar list formatting with totals.

## 3. Filtering reads: labels, priorities, assignees

Chapter 03 showed `--status`, `--priority`, `--type`. Three more filters complete the toolkit: `--label`, `--assignee`, and the negations (`--no-assignee`, `--no-labels`). A **label** is a free-text tag stuck on a bead (like `frontend` or `backend`); the **assignee** is who is currently responsible (empty until someone claims the bead — chapter 03, §4).

First, tag a bead so there is something to filter on:

```bash
bd update tut-ra2 --add-label frontend
```

```
✓ Updated issue: tut-ra2 — Implement homepage
```

Now the label filters light up. On `bd list`:

```bash
bd list --label frontend
```

```
○ tut-ra2 ● P1 Implement homepage

--------------------------------------------------------------------------------
Total: 1 issues (1 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

And combined with text search:

```bash
bd search "homepage" --label frontend
```

```
Found 1 issues matching 'homepage':
tut-ra2 [P1] [task] open [frontend] - Implement homepage
```

Two homepage beads exist, but only Implement carries `[frontend]` — the label narrows search to one. (`--label-any` takes several labels with `OR` meaning: match beads carrying *any* of them. §6 returns to `OR`.) The label was removed right after this section (`bd update tut-ra2 --remove-label frontend`) to keep the canonical graph untagged — demos should not pollute shared data.

Assignees: nobody claimed anything in this fresh database, so the positive filter is empty and the negation shows everything:

```bash
bd list --assignee sergii
```

```
No issues found.
```

```bash
bd list --no-assignee
```

```
○ tut-icv ● P1 Design homepage
○ tut-ra2 ● P1 Implement homepage
○ tut-vhe ● P1 Deploy website
○ tut-xbl ● P1 [epic] Build website
○ tut-4tn ● P2 Write docs
○ tut-y1l ● P2 Write tests

--------------------------------------------------------------------------------
Total: 6 issues (6 open, 0 in progress)

Status: ○ open  ◐ in_progress  ● blocked  ✓ closed  ❄ deferred
```

`No issues found` is a real answer, not an error: `created_by` is `sergii` on all six (he seeded them), but **creator is not assignee** — the assignee field is empty until `bd update --claim` fills it. After a claim, `--assignee <you>` finds your work and `--no-assignee` hides it. Priority ranges work the same way on both commands: `bd search "task" --priority-min 0 --priority-max 1` and `bd list --priority-min 2` (the latter shows the two P2s). All filters combine freely — status plus label plus priority plus assignee in one call.

## 4. Health views: `bd status`, `bd stale`, `bd orphans`, `bd count`

Neo4j has no single "how is my database doing?" command; beads has four. Together they are the saved-views layer: run them every morning instead of eyeballing `bd list`.

**`bd status` — the dashboard.** Like `git status` for the issue database: totals by state, how much is startable, all in one screen:

```bash
bd status
```

```
📊 Issue Database Status

Summary:
  Total Issues:           6
  Open:                   6
  In Progress:            0
  Blocked:                4
  Closed:                 0
  Ready to Work:          2
```

Six total, four blocked behind dependencies (chapter 03, §3), two ready. `Ready to Work: 2` agrees with `bd ready` (Design + the epic). Flags: `--no-activity` (skip git history, faster), `--json` (machine-readable — §5 feeds on it), `--assigned` (your beads only).

**`bd stale` — forgotten work.** Shows beads untouched for N days (default 30). Fresh database, nothing is stale:

```bash
bd stale
```

```
✨ No stale issues found (all active)
```

Tune the window with `--days` (minimum 1 — `--days 0` errors with `--days must be at least 1`), cap output with `--limit`, narrow with `--status open|in_progress|blocked|deferred`. In a real project this is where abandoned `in_progress` beads surface.

**`bd orphans` — beads with no links.** An **orphan** is a bead with no dependencies in either direction — not necessarily bad (the epic is link-free by design), but worth a glance:

```bash
bd orphans
```

```
✓ No orphaned issues found
```

Clean — every bead here participates in at least one `blocks` edge… except, strictly, the epic has none (chapter 03, §6), yet the command reports none orphaned. Takeaway: `orphans` uses its own definition of "linked" (parents, recent activity, and other relations count too), so treat it as a hint, not a proof. Cross-check with `bd dep list <id>` when it matters.

**`bd count` — grouped totals.** Bare `bd count` is one number; `--by-*` splits it — the quick aggregation that always works, no SQL server needed:

```bash
bd count
```

```
6
```

```bash
bd count --by-status
```

```
Total: 6

open: 6
```

```bash
bd count --by-priority
```

```
Total: 6

P1: 4
P2: 2
```

```bash
bd count --by-type
```

```
Total: 6

epic: 1
task: 5
```

Six beads: four P1, two P2; one epic, five tasks. These four outputs are the ground truth §5's SQL recipes must reproduce — keep them in mind.

## 5. Aggregations: `bd count` vs `bd sql` recipes

Neo4j's `COUNT`, `GROUP BY` equivalent in beads has two spellings: the safe one (`bd count --by-*`, just ran above) and the raw one (`bd sql`, the escape hatch into SQL). The SQL recipes below are written for **server mode** (`bd init --server`, where a real Dolt **SQL** server answers). In this chapter's embedded database they do not execute — and that refusal is itself a real output worth seeing (§9 explains why):

```bash
bd sql 'SELECT status, COUNT(*) FROM issues GROUP BY status'
```

```
Error: 'bd sql' is not yet supported in embedded mode
```

Same for the priority/type breakdown the `--by-*` flags just answered:

```sql
-- Recipe (server mode): how many beads per status?
SELECT status, COUNT(*) FROM issues GROUP BY status;
-- Expected on the tutorial graph: open | 6

-- Recipe (server mode): type × priority matrix (§4 ground truth)
SELECT issue_type, priority, COUNT(*) FROM issues GROUP BY issue_type, priority;
-- Expected: task/1 ×3, task/2 ×2, epic/1 ×1
```

So how do you aggregate *today*, in embedded mode? Two runnable stand-ins that produce the same numbers. One is `bd count --by-*` (§4). The other is `jq` over `bd list --json` — machine-readable JSON, one object per bead, grouped locally:

```bash
bd list --json | python3 -c "import json,sys,collections; d=json.load(sys.stdin); print(collections.Counter((i['status'],i['issue_type']) for i in d)); print(collections.Counter(i['priority'] for i in d))"
```

```
Counter({('open', 'task'): 5, ('open', 'epic'): 1})
Counter({1: 4, 2: 2})
```

Five open tasks, one open epic; four P1, two P2 — identical to `bd count --by-type` / `--by-priority`. (The `python3 -c` one-liner plays the `jq` role here; with real `jq` it reads `bd list --json | jq -r '.[].status' | sort | uniq -c`.) Rule: reach for `bd count --by-*` for one-line answers, `--json` + grouping for anything fancier, `bd sql` when you are on a server-mode database and need the full SQL toolbox (`JOIN`s against the dependency tables, `HAVING`, window functions).

## 6. `CASE`-like grouping and `OR` queries: slicing the graph your way

Neo4j's `CASE` buckets rows into named groups; `UNION` stacks two result sets. Beads has no `CASE` keyword — you bucket with `--json` plus a grouping tool, and you stack with `OR`.

**Bucketing (the `CASE` analog).** Question: "which beads are urgent (P0–P1) vs normal (P2+) vs backlog (P3–P4)?" In SQL that is a `CASE` over `priority`; here it is a tiny grouping over JSON. The raw material is one bead object per line — here is the shape (first object, Deploy):

```json
{
    "id": "tut-vhe",
    "title": "Deploy website",
    "description": "ship it",
    "status": "open",
    "priority": 1,
    "issue_type": "task"
}
```

Group those objects and you get buckets: `P1 ×4` (urgent: Design, Implement, Deploy, epic), `P2 ×2` (normal: Tests, Docs), `P3–P4 ×0` (backlog: empty — §5's `Counter({1: 4, 2: 2})` is exactly this bucketing). With `jq`: `bd list --json | jq 'group_by(.priority) | map({p: .[0].priority, n: length})'`. With `bd query` you can materialize one bucket at a time: `bd query "priority<=1"` (urgent), `bd query "priority>=3"` (backlog — empty here, and empty is a real answer).

**Stacking (the `UNION` analog).** Two ways to say "this OR that". Inside one expression with `bd query`:

```bash
bd query "type=task AND priority=2"
```

```
Found 2 issues:
○ tut-4tn [● P2] [task] - Write docs
○ tut-y1l [● P2] [task] - Write tests
```

…and the `OR` form across labels/fields (`bd query "label=frontend OR label=backend"` per `--help` — empty on our untagged graph, meaningful on yours). Across commands, `--label-any` is the built-in `OR`: `--label-any frontend,backend` matches beads carrying *either* label, where repeat `--label frontend --label backend` demands *both* (`AND`). Know which one you asked for — `AND` shrinks, `OR` grows.

## 7. Writing back: `bd update` and `bd delete` (caution)

Neo4j's advanced chapter ends its write section with `SET` / `REMOVE` / `DELETE` / `MERGE`. The beads equivalents are `bd update` (change fields — `SET`) and `bd delete` (`DELETE`, with no undo). §3 already showed `--add-label`; the full update palette: `--assignee`, `--priority`, `--status`, `--description`, `--set-labels` (replace all labels at once), `--remove-label`. Updates combine freely in one call and print one confirmation line:

```bash
bd update tut-3x8 --description "will be deleted"
```

```
✓ Updated issue: tut-3x8 — Throwaway demo
```

(`tut-3x8` is a throwaway bead created for this demo with `bd create --title="Throwaway demo" --type task --priority 3`, which answered `✓ Created issue: tut-3x8 — Throwaway demo / Priority: P3 / Status: open`. Demos that write should use throwaways, never the canonical six.)

Deletion is permanent — no trash bin, no undo. `bd delete` first unwires every dependency edge touching the bead, rewrites text references to `[deleted:ID]` in neighbours, then removes the row:

```bash
bd delete tut-3x8 --force
```

```
✓ Deleted tut-3x8
  Removed 0 dependency link(s)
  Updated text references in 0 issue(s)
```

Zero links removed (the throwaway was never wired into the graph — that is *why* throwaways are safe). The database is back to six:

```
Total: 6 issues (6 open, 0 in progress)
```

> ⚠️ Caution: `bd delete` cannot be undone, and without `--force` it asks interactively (scripts hang). Never delete a bead that other beads depend on without checking `bd dep tree <id>` first — deleting a blocker silently unblocks its dependents (their `DE
...[truncated 8184 chars]