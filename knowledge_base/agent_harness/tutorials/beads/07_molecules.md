# 07 — Molecules: formulas, protos, pour vs wisp, and swarms

**What you will learn**
- The template chain: **formula** (a reusable workflow file) → **cook** (compile the file into a template) → **proto** (an uninstantiated template epic) → **pour** (spawn persistent, long-lived beads) vs **wisp** (spawn ephemeral, short-lived beads that vanish when done)
- How to list and inspect formulas with `bd formula list` and `bd formula show`, and what an honestly empty formula store looks like
- How to **distill** (extract a reusable proto from an ad-hoc epic you built by hand) and **bond** (combine two templates or molecules into one)
- How to finish the lifecycle with **squash** (condense a molecule into a summary digest) and **burn** (delete a wisp with no trace)
- How to run a **swarm** (structured parallel execution over an epic's children DAG (Directed Acyclic Graph, nodes plus one-way edges with no loops)): `bd swarm validate`, `bd swarm create`, `bd swarm status`, plus `bd mol progress`
- When templates pay off vs a plain epic plus children (chapter 06 vocabulary), especially for fleet multi-agent fan-out

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/07_molecules`. All command outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-mol-demo` (bd 1.0.4), pasted as-is. On macOS `/tmp` is really `/private/tmp`, which is why some paths print that way. A **CLI** (Command-Line Interface) is a program you drive by typing commands; `bd` is the CLI for beads. One environment note: this machine exports `BEADS_DIR` pointing at a shared fleet database, so every demo command below was run with that variable unset (`unset BEADS_DIR`) — otherwise `bd init` refuses and `bd` talks to the wrong database. If your shell pins a shared database the same way, unset it first in your scratch terminal.
>
> This chapter assumes you know [06_hierarchies.md](06_hierarchies.md): epic (a large container bead grouping child beads), children, `blocks` edges, and the DAG rule (no loops). Your ids will differ — ids contain a random hash — but titles and shapes match.

## 0. The big picture: formula → cook → proto → pour / wisp

Chapter 06 taught you to build an epic with children by hand. That is fine once. But when every feature needs the same shape — design, implement, document — you want a **template**: write the shape once, stamp out copies.

Beads calls this the molecule system, borrowing chemistry words:

| Word | Plain meaning |
|---|---|
| **formula** | A reusable workflow file (YAML (YAML Ain't Markup Language, a human-readable data format) / JSON (JavaScript Object Notation, a machine-readable text format)) stored under `.beads/formulas/`. The recipe. |
| **cook** | Compile a formula into a proto (`bd cook`). Macros expand, aspects apply, `{{variables}}` stay as placeholders until you fill them. |
| **proto** | An uninstantiated template epic. A mold sitting on the shelf — no real work yet. |
| **pour** | Stamp a proto into **persistent** beads (liquid phase). Real work, synced with git, kept for the audit trail. |
| **wisp** | Stamp a proto into **ephemeral** beads (vapor phase). Short-lived work, NOT synced via git, auto-cleaned. |
| **bond** | Combine two protos or molecules into a compound. |
| **distill** | Reverse of pour: extract a proto (formula file) from an ad-hoc epic you built by hand. |
| **squash** | Condense a molecule's ephemeral children into one permanent summary (a digest). |
| **burn** | Delete a wisp with no trace. |
| **swarm** | Structured parallel execution over an epic's children DAG: validate the shape, then hand waves of ready work to workers. |

The demo epic for this chapter is a checkout project, built exactly like chapter 06 taught:

```bash
bd create --type epic --title "Ship checkout v2"
bd create --parent tut-6do --title "Design checkout API"
bd create --parent tut-6do --title "Implement checkout API"
bd create --parent tut-6do --title "Write checkout docs"
bd dep add tut-6do.2 tut-6do.1
```

```
✓ Created issue: tut-6do — Ship checkout v2
✓ Created issue: tut-6do.1 — Design checkout API
✓ Created issue: tut-6do.2 — Implement checkout API
✓ Created issue: tut-6do.3 — Write checkout docs
○ tut-6do ● P2 [epic] Ship checkout v2
├── ○ tut-6do.1 ● P2 Design checkout API
├── ○ tut-6do.2 ● P2 Implement checkout API
└── ○ tut-6do.3 ● P2 Write checkout docs
✓ Added dependency: tut-6do.2 (Implement checkout API) depends on tut-6do.1 (Design checkout API) (blocks)
```

(The `✓ Created` lines are the real per-command confirmations, squeezed together here; the tree is `bd list --parent tut-6do`.)

## 1. Formulas: list and show

A formula lives in the formula store. Beads searches four places, in order: `<beads-dir>/formulas/` (active project), `<checkout-root>/.beads/formulas/` (repo-local), `~/.beads/formulas/` (your user account), `$GT_ROOT/.beads/formulas/` (orchestrator). A fresh scratch database has none — and `bd` says so honestly:

```bash
bd formula list
```

```
No formulas found.

Search paths:
  /private/tmp/beads-mol-demo/.beads/formulas
  /Users/sergii/.beads/formulas
```

Do not invent formula names from memory — always start from this list. An empty store is normal on a new project; §3 shows the way out (`bd mol distill` turns an epic you already built into a formula).

### 1a. Distill first, list second

Since the store was empty, distill the checkout epic into a formula named `checkout-flow`:

```bash
bd mol distill tut-6do checkout-flow
```

```
✓ Distilled formula: 3 steps
  Formula: checkout-flow
  Path: /private/tmp/beads-mol-demo/.beads/formulas/checkout-flow.formula.json

To instantiate:
  bd mol pour checkout-flow
```

Now the list is non-empty — and every name here is real, safe to pour:

```bash
bd formula list
```

```
📜 Formulas (1 found)

📋 Workflow:
  checkout-flow
```

Inspect it before stamping copies:

```bash
bd formula show checkout-flow
```

```
📋 checkout-flow
   Type: workflow
   Source: /private/tmp/beads-mol-demo/.beads/formulas/checkout-flow.formula.json

🌲 Steps (3):
   ├── design-checkout-api: Design checkout API
   ├── implement-checkout-api: Implement checkout API [depends: design-checkout-api]
   └── write-checkout-docs: Write checkout docs
```

Notice the `[depends: design-checkout-api]` survivor: distill preserved the `blocks` edge from the original epic. The template remembers the shape, not just the titles.

## 2. Cook, pour, wisp

### 2a. Cook: compile the formula

`bd cook` compiles a `.formula.json` file into a proto and prints the resolved structure as JSON. Default mode is compile-time: `{{variable}}` placeholders stay intact so you can review the template shape:

```bash
bd cook checkout-flow
```

```json
{
  "formula": "checkout-flow",
  "schema_version": 1,
  "source": "/private/tmp/beads-mol-demo/.beads/formulas/checkout-flow.formula.json",
  "steps": [
    {
      "id": "design-checkout-api",
      "priority": 2,
      "title": "Design checkout API",
      "type": "task"
    },
    {
      "depends_on": [
        "design-checkout-api"
      ],
      "id": "implement-checkout-api",
      "priority": 2,
      "title": "Implement checkout API",
      "type": "task"
    },
    {
      "id": "write-checkout-docs",
      "priority": 2,
      "title": "Write checkout docs",
      "type": "task"
    }
  ],
  "type": "workflow",
  "version": 1
}
```

Two modes exist: compile-time (default, placeholders intact — good for review and planning) and runtime (`--mode=runtime` or `--var key=value`, variables substituted — good for final validation before pour). Add `--persist` only if you want the proto written to the database for repeated reuse; normally `pour` and `wisp` cook inline from the formula name and you never handle the proto directly.

### 2b. Pour: persistent molecules (liquid phase)

Pour stamps the template into real, persistent beads — synced with git, kept for the audit trail. Use it for feature work spanning sessions:

```bash
bd mol pour checkout-flow
```

```
✓ Poured mol: created 4 issues
  Root issue: tut-mol-2ev
  Phase: liquid (persistent in .beads/)
```

Four issues: one root plus three steps. The tree and the molecule view agree:

```bash
bd list --parent tut-mol-2ev
bd mol show tut-mol-2ev
```

```
○ tut-mol-2ev ● P2 checkout-flow
├── ○ tut-mol-2tn ● P2 Design checkout API
├── ○ tut-mol-3yy ● P2 Implement checkout API
└── ○ tut-mol-xwj ● P2 Write checkout docs
```

```
🧪 Molecule: checkout-flow
   ID: tut-mol-2ev
   Steps: 4

🌲 Structure:
   checkout-flow (root)
   ├── Design checkout API
   ├── Implement checkout API
   └── Write checkout docs
```

Track completion with `bd mol progress` (more in §4):

```bash
bd mol progress tut-mol-2ev
```

```
Molecule: tut-mol-2ev (checkout-flow)
Progress: 0 / 3 (0.0%)
```

Close one step and watch it move:

```bash
bd close tut-mol-2tn
bd mol progress tut-mol-2ev
```

```
✓ Closed tut-mol-2tn — Design checkout API: Closed
Molecule: tut-mol-2ev (checkout-flow)
Progress: 1 / 3 (33.3%)
```

### 2c. Wisp: ephemeral molecules (vapor phase)

Wisp stamps the same template as short-lived beads: stored locally, NOT synced via git. Use it for one-shot operational work — release runs, health checks, recurring loops — anything with no audit value:

```bash
bd mol wisp checkout-flow
```

```
✓ Created wisp: 1 issues
  Root issue: tut-wisp-wmz
  Phase: vapor (ephemeral, not synced via git)

Next steps:
  bd close tut-wisp-wmz.<step>       # Complete steps
  bd mol squash tut-wisp-wmz         # Condense to digest (promotes to persistent)
  bd mol burn tut-wisp-wmz           # Discard without creating digest
```

A wisp starts life as a single root (`bd children tut-wisp-wmz` prints `Issue 'tut-wisp-wmz' has no children`) — step children materialize as the workflow runs. The rule of thumb:

- **pour** (liquid): you will want to reference this work later → persistent, git-synced.
- **wisp** (vapor): nobody needs to see this next week → ephemeral, auto-cleaned.
- A formula can declare `phase: "vapor"` to recommend wisp; pouring it anyway prints a warning.

## 3. The lifecycle: bond, distill, squash, burn

### 3a. Bond: combine templates or molecules

`bd mol bond` is polymorphic — it accepts any pair of formulas, protos, or molecules:

- formula + formula → compound proto (reusable template)
- formula/proto + mol → cook, spawn, and attach to the molecule
- mol + mol → join into one compound molecule

Bond types: `sequential` (default, B runs after A), `parallel` (B runs alongside A), `conditional` (B runs only if A fails). Here both operands are poured molecules, so they join:

```bash
bd mol bond tut-mol-2ev tut-mol-hqn
```

```
✓ Bonded: tut-mol-2ev + tut-mol-hqn
  Result: tut-mol-2ev (compound_molecule)
```

(`tut-mol-hqn` is a second pour of `checkout-flow` — see the troubleshooting note in §6 about pouring twice.) A fleet-flavored trick: `bd mol bond <formula> <patrol-epic> --ref arm-{{worker_name}} --var worker_name=ace` spawns readable per-worker children like `bd-patrol.arm-ace` — one bonded arm per agent.

### 3b. Distill: from ad-hoc epic to reusable proto

You already saw distill in §1a — it is the reverse of pour (molecule → formula instead of formula → molecule):

1. Loads the epic and all its children.
2. Writes a `.formula.json` file (project formulas dir wins).
3. Replaces concrete values with `{{variable}}` placeholders for every `--var name=value` flag.

```bash
bd mol distill tut-6do checkout-flow
```

```
✓ Distilled formula: 3 steps
  Formula: checkout-flow
  Path: /private/tmp/beads-mol-demo/.beads/formulas/checkout-flow.formula.json

To instantiate:
  bd mol pour checkout-flow
```

Use it when a team builds a good workflow organically and wants to reuse it: distill captures tribal knowledge as an executable template. The `--var` syntax accepts both directions (`--var branch=feature-auth` or `--var feature-auth=branch`) — bd detects which side is the concrete value.

### 3c. Squash and burn: graceful vs traceless endings

- **squash** collects a molecule's ephemeral children, writes one permanent digest (summary) issue, and either promotes the children to persistent or deletes them. It is how a wisp graduates: run the workflow as vapor, keep only the summary.
- **burn** deletes a molecule with no digest and no trace. For abandoned cycles, crashed workflows, test molecules.

Squash needs ephemeral children to condense — a fresh wisp root with no children has nothing to squash:

```bash
bd mol squash tut-wisp-6jk
```

```
No ephemeral children found for molecule tut-wisp-6jk
```

Burn asks for confirmation, then deletes:

```bash
echo y | bd mol burn tut-wisp-wmz
```

```
About to burn wisp tut-wisp-wmz (1 issues)
This will permanently delete all wisp data with no digest.
Use 'bd mol squash' instead if you want to preserve a summary.

Continue? [y/N] ✓ Burned wisp: 1 issues deleted
  Ephemeral: tut-wisp-wmz
```

Without the piped `y`, the same command prints `Continue? [y/N] Canceled.` and deletes nothing — safe by default.

## 4. Swarm: parallel execution over the DAG

A **swarm** is a structured body of work defined by one epic plus its children, with `blocks` edges forming the DAG. Three commands drive it: validate the shape, create the swarm molecule, watch the status. A fourth, `bd mol progress`, tracks any molecule including swarm-backed ones.

### 4a. Validate before you parallelize

`bd swarm validate` checks dependency direction, orphaned roots, missing dependencies, cycles, and disconnected subgraphs, then prints ready fronts (waves of parallel work), estimated worker-sessions, and maximum parallelism:

```bash
bd swarm validate tut-6do
```

```
🐝 Swarm Analysis: Ship checkout v2
   Epic ID: tut-6do
   Total issues: 3 (0 closed)

📊 Ready Fronts (waves of parallel work):
   Wave 1: 2 issues
      • tut-6do.1: Design checkout API
      • tut-6do.3: Write checkout docs
   Wave 2: 1 issues
      • tut-6do.2: Implement checkout API

📈 Summary:
   Estimated worker-sessions: 3
   Max parallelism: 2
   Total waves: 2

✓ Swarmable: YES
```

Read it as a schedule: two workers can start immediately (design + docs), the implement step waits for design. Validation works on poured molecules too — the stamped copy keeps the DAG:

```bash
bd swarm validate tut-mol-2ev
```

```
🐝 Swarm Analysis: checkout-flow
   Epic ID: tut-mol-2ev
   Total issues: 3 (0 closed)

📊 Ready Fronts (waves of parallel work):
   Wave 1: 2 issues
      • tut-mol-2tn: Design checkout API
      • tut-mol-xwj: Write checkout docs
   Wave 2: 1 issues
      • tut-mol-3yy: Implement checkout API

📈 Summary:
   Estimated worker-sessions: 3
   Max parallelism: 2
   Total waves: 2

✓ Swarmable: YES
```

### 4b. Create the swarm molecule

```bash
bd swarm create tut-6do
```

```
✓ Created swarm molecule: tut-8pq
   Epic: tut-6do (Ship checkout v2)
   Total issues: 3
   Max parallelism: 2
   Waves: 2
```

The swarm molecule (`tut-8pq`, `mol_type=swarm`) links to the epic it orchestrates. Any coordinator agent can pick it up; pass `--coordinator=<address>` to name one, `--force` to create a second swarm when one already exists. Hand it a single task instead of an epic and it auto-wraps: creates an epic with that issue as its only child, then swarms it. List active swarms anytime:

```bash
bd swarm list
```

```
🐝 Active Swarms (1)

tut-8pq Swarm: Ship checkout v2
   Epic: tut-6do (Ship checkout v2)
   Progress: 0/3 (0%)
```

### 4c. Status and progress while workers run

`bd swarm status` shows the live ready front — what is done, active, ready, or still blocked:

```bash
bd swarm status tut-6do
```

```
🐝 Ready Front Analysis: Ship checkout v2

Completed:     (none)
Active:        (none)
Ready:         ○ tut-6do.1, ○ tut-6do.3
Blocked:       ◌ tut-6do.2 (needs tut-6do.1)

Progress: 0/3 complete (0%)
```

`bd mol progress` gives the same completion fraction for any molecule, swarm-backed or plain poured (§2b showed `1 / 3 (33.3%)` after closing one step). The fleet loop is: `swarm validate` once, `swarm create` once, then each worker asks `swarm status` (or `bd ready`) for the next claimable bead.

## 5. When templates pay off vs plain epic + children

Chapter 06's plain epic is best when the work is one of a kind: stamp nothing, just `bd create --parent` three children and go. Templates earn their keep when the **shape repeats**:

| Signal | Plain epic (ch. 06) | Formula → pour (this chapter) |
|---|---|---|
| One-off feature | ✓ Faster, no ceremony | Overkill |
| Same 3–5 steps per feature, many features | Tedious, drifts over time | ✓ One formula, identical stamps |
| Parallel agents (fleet fan-out) | Workers must agree on shape out-of-band | ✓ `swarm validate` agrees for them; waves + max parallelism computed |
| One-shot ops loops (releases, patrols) | Clutters git history | ✓ `wisp`: vapor phase, burn when done |
| Good workflow discovered mid-project | Already built — nothing to reuse | ✓ `distill` captures it as a formula |

The fleet multi-agent fan-out is the flagship case: one coordinator distills (or writes) a formula, pours one molecule per worker (or bonds per-worker arms onto one patrol epic with `--ref arm-{{worker_name}}`), runs `swarm validate` to prove the DAG is clean, creates the swarm, and lets workers claim ready fronts in parallel. `bd mol progress` is the dashboard.

## 6. Troubleshooting

**Pour twice, get two molecules.** Pouring is stamping, not linking — every `bd mol pour checkout-flow` creates a fresh root with fresh children. The demo did it twice (`tut-mol-2ev`, then `tut-mol-hqn`):

```
✓ Poured mol: created 4 issues
  Root issue: tut-mol-hqn
  Phase: liquid (persistent in .beads/)
```

If you meant to extend an existing molecule, `bd mol bond` it instead of pouring again. If the duplicate was a mistake, close the extra root or burn it (wisps) — duplicates are cheap but confusing in `swarm list`.

**Wisp cleanup: `bd mol wisp gc` and `bd gc`.** Wisps are ephemeral but not invisible — abandoned ones linger locally. `bd mol wisp gc` sweeps them:

```bash
bd mol wisp gc
```

```
No abandoned wisps found
```

(`bd gc` is the bigger hammer: decay closed issues older than 90 days, compact Dolt commits, run Dolt garbage collection. `bd mol wisp gc` is the wisp-only subset — prefer it when molecules are all you touched.)

**`bd swarm validate` failures: cycles and disconnected graphs.** `blocks` loops are rejected at write time (chapter 06's DAG rule), but a validate failure usually means one of: a cycle smuggled in via another link type, orphaned roots with no dependents, leaves missing dependencies, or two disconnected subgraphs under one epic. Fix the graph (`bd dep add` the missing edge, move the stray child), re-validate until `✓ Swarmable: YES`, and only then `bd swarm create` — creating a swarm over a broken DAG schedules workers onto work that can never unblock.

**`bd formula list` is empty.** Normal on a fresh database — not an error. Either distill what you already built (`bd mol distill <epic> <name>`, §1a/§3b) or check the other search paths (`~/.beads/formulas/` for user-level formulas shared across projects).

**Burn asks twice.** `bd mol burn` without piped confirmation cancels safely (`Continue? [y/N] Canceled.`). Pipe `echo y` only in scripts where you mean it — burn leaves no digest, unlike squash.

## Takeaways

- Formula → cook → proto is the template shelf; pour (persistent, liquid) vs wisp (ephemeral, vapor) is how templates become work.
- `bd formula list` tells the truth — empty store? Distill (`bd mol distill`) an epic you already built instead of inventing names.
- Bond combines (proto+proto, proto+mol, mol+mol); squash graduates a wisp to a digest; burn erases without a trace.
- Swarm is validate → create → status: prove the DAG clean, spawn the coordinator molecule, let workers claim ready-front waves. `bd mol progress` is the dashboard for any molecule.
- Templates pay off when the shape repeats — especially fleet multi-agent fan-out, where one formula plus `swarm validate` replaces out-of-band coordination.

Next: [08_gates.md](08_gates.md)
