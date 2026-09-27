# Beads tutorial

A from-zero, hands-on tutorial for **beads** — a lightweight issue tracker (database) for agentic workers (AI coding agents) task orchestration, with first-class dependencies. It uses an embedded Dolt (version-controlled SQL database) backend, so no server is needed. It is CLI (Command-Line Interface) first, with `--json` flags for scripting, plus fleet (proprietary supervisor that pulls beads tasks and runs coder agents) integration.

Retrieve chapters with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — install `bd` 1.0.4, scaffold the `uv` project, `justfile` recipes, first bead create/list in a temp demo database.
- [001_explore.md](001_explore.md) — exploring an unknown beads database: counts, status breakdown, prefixes, dependency edges, orphaned blockers, JSON output for scripting.
- [01_concepts.md](01_concepts.md) — the beads model (issues, status, priority, types like epic/task/bug), dependencies (`blocks`, `relates`), JSON-first CLI habits for agents.
- [02_create_update.md](02_create_update.md) — creating and updating beads: `bd create` with title/priority/type, `bd update`, `bd close`/`reopen`, idempotent seeding from Python.
- [03_dependencies.md](03_dependencies.md) — linking work with `bd dep add <child> --blocks <parent>` (child waits on parent), reading ready work, closing in dependency order.
- [04_search_views.md](04_search_views.md) — finding work: `bd list` filters, `bd search` full-text, `bd show <id>`, ready/blocked views for picking the next task.
- [05_python_fleet.md](05_python_fleet.md) — Python wrapper plus fleet patterns: `db.py` subprocess helper, `seed.py` loader, `explore.py` reporter, claiming and closing beads as a fleet worker.
- [06_hierarchies.md](06_hierarchies.md) — parent-child vs blocks, epic lifecycle, link types.
- [07_molecules.md](07_molecules.md) — formulas/protos, pour vs wisp, swarm.
- [08_gates.md](08_gates.md) — gates, merge-slot, worktree parallelism.

## Runnable project
`project/` — `justfile`, `pyproject.toml`, `src/beads_tutorial/` (`db.py` wrapper, `explore.py`, `seed.py`), `tests/`.
Start with `cd project && uv sync && just test` (no Docker needed, unlike neo4j).
`db.py` runs the CLI (Command-Line Interface) via subprocess and parses `--json` output.
`just test` runs the full `pytest` suite; `just seed` loads the demo graph into a temp dir.

## Local settings (shared by all chapters)
| setting | value |
|---|---|
| `bd` version | `1.0.4` |
| issue prefix | `tut` for the tutorial demo database in temp dirs |
| scripting | `bd --json` flags for machine-readable output |
| fleet coder | `opencode` |
| fleet model | `opencode-go/muse-spark-1.3-contributor` |

## Dataset (shared by all chapters)
A small "tutorial website" task graph, seeded by `seed.py`:

- epic `website` plus tasks: design, implement, tests, docs
- linked by a `blocks` dependency chain (design first, docs last)
- `blocks` means the child waits: it is not ready until the parent closes
- ~6 beads in total, safe to recreate in any temp directory
- `seed.py` is idempotent (safe to re-run): it wipes `tut-*` beads first
- The seed graph is grouped under an epic and extended by `hierarchy.py` for 06–08.

Verified on: `bd` 1.0.4, 2026-09-08.
