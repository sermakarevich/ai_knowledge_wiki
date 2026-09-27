# 08 — Gates, merge-slot, and worktree parallelism: async coordination for many agents

**What you will learn**
- The five **gate** types — a gate is a wait condition that blocks one workflow step until something happens: `human` (a person resolves it), `timer` (a clock resolves it), `gh:run` (a CI (Continuous Integration, automatic checks that run when code is pushed) workflow run resolves it), `gh:pr` (a PR (Pull Request, a proposal to merge one branch into another) merge resolves it), `bead` (another bead closing resolves it) — and when each one is the right tool
- The gate lifecycle: `bd gate create` (make a gate blocking one issue), `bd gate list` (open gates, `--all` adds closed ones), `bd gate check` (evaluate conditions, auto-close what resolved), `bd gate resolve` (close by hand), `bd gate show` (inspect one gate)
- The **merge-slot**: an exclusive lock so parallel agents do not clash when they merge. Commands `bd merge-slot create/check/acquire/release`, plus the `holder` / `waiters` metadata that shows who holds the lock and who queues behind
- **Worktree** isolation: an isolated git working copy per agent (`bd worktree create/list/info/remove`), all worktrees sharing one beads database via the git common directory — and why `bd` refuses worktrees under `/tmp`
- The fleet mapping: the job worker's human-approval gate (research → design → gate → spawn → observe, `--job-gate off` skips it), `--isolation worktree` vs `--isolation none`, and `isolation_exclude` (repos such as `/Users/sergii/.ai` that must never get worktrees)
- The coordination recipe: epic children plus gates plus a merge-slot acquisition order for parallel agents, what happens on conflict (waiters queue, `bd blocked`), troubleshooting, and finale takeaways

> How to read this tutorial: each chapter is retrieved with `ai show research_topics/agent_harness/tutorials/beads/<chapter>`, for example `ai show research_topics/agent_harness/tutorials/beads/08_gates`. Gate and merge-slot outputs below are real outputs, run in a scratch database created with `bd init --prefix tut` in `/tmp/beads-gates-demo` (bd 1.0.4), pasted as-is. The worktree outputs are also real, but from a throwaway repo at `~/beads-wt-demo` instead of `/tmp` — `bd worktree` refuses `/tmp` checkouts as an unsafe location (see §4a), so the honest demo moved one directory up. A **CLI** (Command-Line Interface) is a program you drive by typing commands; `bd` is the CLI for beads. One environment note: this machine pins a shared fleet database, so every demo command below was run with that pin unset (`unset BEADS_DIR`) — otherwise `bd` talks to the wrong database. Your ids will differ (ids contain a random hash) but titles and shapes match.
>
> This chapter assumes [06_hierarchies.md](06_hierarchies.md) (epic, children, `blocks`, `bd ready`, `bd blocked`) and [07_molecules.md](07_molecules.md) (swarm validate/create/status, pour vs wisp) vocabulary.

## 0. The big picture: three primitives for safe parallelism

Chapters 06 and 07 taught you to *describe* parallel work: one epic, children claimed via `bd ready`, `swarm validate` proving the DAG (Directed Acyclic Graph, nodes plus one-way edges with no loops) is clean. That answers "what can run in parallel?" Three questions remain, and each gets one primitive:

| Question | Primitive | One-line meaning |
|---|---|---|
| "What must wait for the outside world?" | **gate** | A wait condition blocking one step: human approval, a timer, a CI run, a PR merge, another bead |
| "Who merges right now?" | **merge-slot** | An exclusive lock: exactly one agent holds it, the rest queue as waiters |
| "Where does each agent work?" | **worktree** | An isolated git working copy per agent, all sharing one beads database |

The demo epic is the familiar checkout project (same shape as chapter 07):

```bash
bd create --type epic --title "Ship checkout v2"
bd create --parent tut-w6u --title "Design checkout API"
bd create --parent tut-w6u --title "Implement checkout API"
bd create --parent tut-w6u --title "Write checkout docs"
```

```
✓ Created issue: tut-w6u — Ship checkout v2
○ tut-w6u ● P2 [epic] Ship checkout v2
├── ○ tut-w6u.1 ● P2 Design checkout API
├── ○ tut-w6u.2 ● P2 Implement checkout API
└── ○ tut-w6u.3 ● P2 Write checkout docs
```

## 1. Gate types: what can a step wait on?

A gate is created automatically when a formula step carries a `gate:` field — but you can also create one ad-hoc with `bd gate create --blocks <issue>`. Five types exist:

| Type | Who resolves it | Typical use | Extra flag |
|---|---|---|---|
| `human` | A person runs `bd gate resolve` | Design review, release approval | `--reason` |
| `timer` | The clock: `bd gate check --type=timer` closes it after `--timeout` | Cool-down after a deploy, smoke pause | `--timeout 2h` |
| `gh:run` | A GitHub Actions workflow run succeeding (`status=completed`, `conclusion=success`) | "Merge only when CI is green" | `--await-id <run-id>` |
| `gh:pr` | A PR merging (`state=MERGED`) | "Start docs only after the code PR lands" | `--await-id <pr-number>` |
| `bead` | Another bead closing (cross-rig: a bead in a *different* project) | "Start here when the other team's bead closes" | `--await-id <rig>:<bead-id>` |

For `bead` gates the await id format is `<rig>:<bead-id>` — rig (the remote project name) first, then a colon, then the bead id, for example `other-project:op-abc123`. Think of it as a postal address: town first, then street.

`gh:run` and `gh:pr` gates were **not run** in this demo: they need a real GitHub repository plus the `gh` CLI (Command-Line Interface) logged in (`gh:run` polls `gh run view <id>`, `gh:pr` polls `gh pr view <id>`), and the scratch repo has neither. Everything below about them is documented from `bd gate check --help`, not from a live run. If a run finishes with `failure`/`canceled` (or a PR closes unmerged), `bd gate check --escalate` flags the gate instead of resolving it.

## 2. Gate lifecycle: create → list → check → resolve → show

### 2a. Human gate: create, block, resolve

Implement (`tut-w6u.2`) must not start until a human approves the design. Create the gate:

```bash
bd gate create --blocks tut-w6u.2 --reason "Need design review"
```

```
✓ Created gate tut-7st (type: human)
  Blocks: tut-w6u.2 (Implement checkout API)
  Reason: Need design review

Resolve with: bd gate resolve tut-7st
```

The gate is a real bead of type `gate` that `blocks` the target. List open gates:

```bash
bd gate list
```

```
⏳ Open Gates (1):

○ tut-7st - human

To resolve a gate: bd close <gate-id>
```

(`bd gate list --all` adds closed gates — shown after the resolve below.) Inspect one gate:

```bash
bd gate show tut-7st
```

```
○ tut-7st - Gate: human
  Status: open
  Await Type: human
  Description: Ad-hoc gate blocking tut-w6u.2

Reason: Need design review
```

The effect on scheduling is immediate. Before the gate, `bd ready` listed implement as claimable; now it is gone from `ready` and appears in `bd blocked`:

```bash
bd blocked
```

```
🚫 Blocked issues (1):

[● P2] tut-w6u.2: Implement checkout API
  Blocked by 1 open dependencies: [tut-7st]
```

That is the whole point of a gate: `blocks` edges order beads relative to *each other* (chapter 06); a gate orders a bead relative to *the outside world*. A worker polling `bd ready` simply never sees gated work — no special client logic needed.

The human approves, and the gate resolves by hand:

```bash
bd gate resolve tut-7st --reason "design approved"
```

```
✓ Gate resolved: tut-7st
  Reason: design approved
```

(`bd gate resolve` is an explicit alias for `bd close <gate-id>` with a reason attached.) The closed gate stays visible for the audit trail:

```bash
bd gate list --all
```

```
● Closed Gates (1):

● tut-7st - human

To resolve a gate: bd close <gate-id>
```

And `bd ready` shows implement as claimable again — four ready items (epic plus three children) where there were three before.

### 2b. Timer gate: create, check, expire

Docs (`tut-w6u.3`) must wait out a two-hour cool-down after the deploy. Same command, `--type=timer` plus `--timeout`:

```bash
bd gate create --type=timer --blocks tut-w6u.3 --timeout=2h --reason "cool-down after deploy"
```

```
✓ Created gate tut-oa0 (type: timer)
  Blocks: tut-w6u.3 (Write checkout docs)
  Reason: cool-down after deploy
  Timeout: 2h0m0s

Resolve with: bd gate resolve tut-oa0
```

Unlike `human`, nobody needs to resolve this — `bd gate check --type=timer` evaluates the clock:

```bash
bd gate check --type=timer
```

```
○ tut-oa0: pending - expires in 1h59m59s

Checked 1 gates: 0 resolved, 0 escalated, 0 errors
```

Pending, one hour fifty-nine to go. Add `--dry-run` to preview without changing anything (same output, nothing closed). To watch an expiry end-to-end, create a one-second gate and sleep past it:

```bash
bd gate create --type=timer --blocks tut-w6u.1 --timeout=1s --reason "smoke pause"
sleep 2
bd gate check --type=timer
```

```
✓ Created gate tut-ou5 (type: timer)
  Blocks: tut-w6u.1 (Design checkout API)
  Reason: smoke pause
  Timeout: 1s

Resolve with: bd gate resolve tut-ou5
```

```
✓ tut-ou5: resolved - timer expired 2s ago
○ tut-oa0: pending - expires in 1h59m56s

Checked 2 gates: 1 resolved, 0 escalated, 0 errors
```

The expired gate closed itself; the two-hour gate is still pending. The fleet pattern: a supervisor loop runs `bd gate check` (all types) on a timer, workers just poll `bd ready` — expired gates silently unblock their steps.

## 3. Merge-slot: one merger at a time

Gates serialize *waiting*; the merge-slot serializes *merging*. When several agents finish parallel work and race to merge, each merge can invalidate the next — beads calls this a "monkey knife fight". The merge-slot is an exclusive lock: one holder, everyone else queues. Each rig (project) has exactly one slot bead named `<prefix>-merge-slot`, labeled `gt:slot`, with two states (`open` = free, `in_progress` = held) and two metadata fields (`holder`, `waiters`).

Create it once per rig, then check it is free:

```bash
bd merge-slot create
bd merge-slot check
```

```
✓ Created merge slot: tut-merge-slot
```

```
✓ Merge slot available: tut-merge-slot
```

Agent `ace` acquires it (`--holder` names the requester; default is the `BEADS_ACTOR` environment variable):

```bash
bd merge-slot acquire --holder ace
bd merge-slot check
```

```
✓ Acquired merge slot: tut-merge-slot
  Holder: ace
```

```
○ Merge slot held: tut-merge-slot
  Holder: ace
```

Status flipped to `in_progress`, holder recorded. Now agent `bravo` tries while `ace` holds:

```bash
bd merge-slot acquire --holder bravo
```

```
✗ Slot held by: ace
Use --wait to add yourself to the waiters queue.
```

No silent stealing: without `--wait` the command fails loudly. With `--wait`, `bravo` joins the queue:

```bash
bd merge-slot acquire --holder bravo --wait
```

```
○ Slot held by ace, added to waiters queue (position 1)
```

The slot bead now shows both fields at once:

```bash
bd show tut-merge-slot
```

```
◐ tut-merge-slot · Merge Slot   [● P0 · IN_PROGRESS]
Type: task
Created: 2026-09-08 · Started: 2026-09-08 · Updated: 2026-09-08

DESCRIPTION
Exclusive access slot for serialized conflict resolution in the merge queue.

LABELS: gt:slot

METADATA
  holder: ace
  waiters: ["bravo"]
```

`ace` finishes merging and releases; the slot is free and `bravo` is still listed as next in line:

```bash
bd merge-slot release
bd merge-slot check
```

```
✓ Released merge slot: tut-merge-slot
```

```
✓ Merge slot available: tut-merge-slot
```

Rule of thumb for agents: `acquire` before you merge, `release` the moment the merge lands, never hold the slot while running tests. A slot held across a long test suite serializes the whole fleet behind one agent.

## 4. Worktree isolation: one directory per agent, one database for all

A **worktree** is an extra working directory attached to the same git repository on a different branch — agent `ace` edits `agent-ace` while agent `bravo` edits `agent-bravo`, neither touching the other's files. The beads database is shared automatically: every worktree discovers it through the git common directory, so `bd` in any worktree talks to the same beads DB with no redirect configuration.

### 4a. The /tmp caveat (read this first)

The worktree demo below runs in `~/beads-wt-demo`, **not** `/tmp`. That is deliberate: `bd worktree` refuses checkouts under `/tmp`:

```
Error: no active beads workspace found; run 'bd where' to inspect the resolved workspace, or 'bd init' to create a new database: BEADS_DIR points to unsafe location: /private/tmp/beads-gates-demo/.beads
```

`/tmp` is world-writable scratch space, so beads treats it as unsafe for workspace discovery. The throwaway repo is still outside the real knowledge repo (`~/beads-wt-demo` vs `/Users/sergii/.ai`) — never create demo worktrees inside `/Users/sergii/.ai`, where they would disturb real work. Everything below is pasted as-is from that repo.

### 4b. Create, list, info

```bash
bd worktree create agent-ace
bd worktree list
```

```
✓ Created worktree: /Users/sergii/beads-wt-demo/agent-ace
  Branch: agent-ace
```

```
NAME                 PATH                                     BRANCH               BEADS
(main)               /Users/sergii/beads-wt-demo              main                 shared
agent-ace            /Users/sergii/beads-wt-demo/agent-ace    agent-ace            local
```

(With `--branch <name>` the branch can differ from the worktree name.) From inside the worktree, `info` confirms where you are:

```bash
cd ~/beads-wt-demo/agent-ace && bd worktree info
```

```
Worktree: /Users/sergii/beads-wt-demo/agent-ace
  Name: agent-ace
  Branch: agent-ace
  Main repo: /Users/sergii/beads-wt-demo
  Beads: local (no redirect)
```

"Beads: local (no redirect)" means no manual redirect was configured — sharing works out of the box. Proof: `bd where` prints the *same* database path from the main repo and from the worktree:

```
# from /Users/sergii/beads-wt-demo:
/Users/sergii/beads-wt-demo/.beads
  prefix: tut
  database: /Users/sergii/beads-wt-demo/.beads/embeddeddolt

# from /Users/sergii/beads-wt-demo/agent-ace:
/Users/sergii/beads-wt-demo/.beads
  prefix: tut
  database: /Users/sergii/beads-wt-demo/.beads/embeddeddolt
```

Two directories, one database. Agents in different worktrees claim different beads but see each other's closes instantly.

### 4c. Remove (and its safety checks)

Removing a clean worktree is one command. Removing a *dirty* one is refused — twice, for two different reasons. First, uncommitted file changes:

```bash
bd worktree remove agent-ace
```

```
Error: safety check failed: worktree has uncommitted changes
Use --force to skip safety checks
```

Then, after deleting the stray file, unpushed commits (the demo worktree had branched commits):

```
Error: safety check failed: worktree has unpushed commits
Use --force to skip safety checks
```

`--force` skips the checks when you mean it:

```bash
bd worktree remove agent-ace --force
bd worktree list
```

```
✓ Removed worktree: /Users/sergii/beads-wt-demo/agent-ace
```

```
NAME                 PATH                                     BRANCH               BEADS
(main)               /Users/sergii/beads-wt-demo              main                 shared
```

Never `--force` a worktree you did not create: the safety checks exist because a forced remove discards that agent's uncommitted work with no recovery.

## 5. Fleet mapping: how the supervisor uses all three

Fleet (the proprietary supervisor that pulls beads tasks and runs coder agents) wires these three primitives into its worker lifecycle:

- **Job-gate approval.** A `job` epic decomposes itself through fixed phases — `research` (write `RESEARCH.md`), `design` (write `tasks.json`), `gate` (wait for human approval), `spawn` (create child beads), `observe` (watch them). The `gate` phase is a human gate at fleet scale: with the default `job_gate: true` config the job worker stops after `design` and asks the operator to approve the plan; it proceeds to `spawn` only once `APPROVED` exists. Pass `--job-gate off` at `fleet bd create` time (stored as `fleet_job_gate: "off"` bead metadata) to skip approval for routine jobs.
- **`--isolation worktree` vs `--isolation none`.** The fleet config default is `isolation: "worktree"` — every git task runs in its own worktree (§4). Pass `--isolation none` at creation (stored as `fleet_isolation: "none"` metadata) to run in the shared checkout instead. Reach for `none` when the task is read-only (a report, a search) or when worktree setup costs more than the task itself; keep `worktree` for anything that edits files.
- **`isolation_exclude`.** A comma-separated list of repo paths that never get worktrees — for repos where isolation is pointless or harmful because they auto-commit or must stay single-checkout. `/Users/sergii/.ai` (this knowledge repo) is the canonical entry: tutorial tasks edit files in place and commit directly, so a worktree would only hide their changes from the reader. Fleet checks, in order: no git repo → no isolation; global `isolation` is `"none"` → no isolation; repo listed in `isolation_exclude` → no isolation; bead opted out via metadata → no isolation; otherwise isolate.

## 6. Coordination recipe: parallel agents on one epic

Here is the full loop for N agents sharing one beads DB, combining chapters 06–08:

1. **Supervisor builds the epic** (chapter 06): `bd create --type epic`, children via `--parent`, `blocks` edges between siblings only. Runs `bd swarm validate` (chapter 07) until `✓ Swarmable: YES`, then `bd swarm create`.
2. **Supervisor adds gates for outside-world waits** (this chapter): `bd gate create --type=human --blocks <id>` for approvals, `--type=timer` for cool-downs, `--type=gh:pr` for "after the PR lands". Workers never poll GitHub themselves.
3. **Each worker starts in its own worktree** (this chapter, §4 — or fleet `--isolation worktree`, §5): one branch per agent, one shared beads DB. Claims work with `bd ready` — gated and blocked beads are invisible, so two workers never grab the same step.
4. **Merge in slot order** (this chapter, §3): before merging, `bd merge-slot acquire --wait`; merge; `bd merge-slot release` immediately. The waiters queue (`waiters: ["bravo"]`) is the conflict outcome made visible — no lost updates, just a line.
5. **Supervisor drains** (chapter 06): `bd epic status` / `bd epic close-eligible`, `bd gate check` on a loop for timers, `bd mol progress` as the dashboard.

What happens on conflict, concretely: two agents finishing at once both run `acquire`. The first becomes `holder`; the second gets `✗ Slot held by: <holder>` and — with `--wait` — a queue position. The loser watches `bd blocked`-style state (its merge step waits) instead of pushing into a race. The queue is priority-ordered, so a P0 hotfix overtakes routine merges.

## 7. Troubleshooting

**Gate never resolves → check the type and the await id.** `bd gate show <id>` prints `Await Type` plus the stored condition. The classic mistakes: a `timer` gate whose `--timeout` was typed as `2h` when you meant `2m` (still `pending - expires in …`, just wait or `resolve` by hand); a `gh:run`/`gh:pr` gate whose `--await-id` points at the wrong run or PR number (re-create with the right id — `check` can only poll what the gate stores); a `bead` gate whose await id is not in `<rig>:<bead-id>` form (rig first, colon, bead id — `other-project:op-abc123`, not the reverse). `bd gate check --dry-run` previews without closing anything.

**Slot held forever → read holder and waiters.** `bd show <prefix>-merge-slot` prints `METADATA` with `holder:` (who has it) and `waiters:` (who queues). If the holder's agent died mid-merge, `bd merge-slot release` frees it by hand and the next waiter acquires. If the waiters list only grows, someone is holding the slot across a test suite — shorten the hold to merge-only (§3 rule of thumb).

**Worktree dirty → respect the remove safety.** `bd worktree remove` refuses dirty worktrees (`uncommitted changes`, then `unpushed commits`) — commit or stash inside the worktree first, then remove cleanly. `--force` is for worktrees you own and have already inspected. And if `bd worktree` prints the `unsafe location` error, you are inside `/tmp`: move the demo repo out (e.g. `~/beads-wt-demo`) — beads will not discover workspaces there by design.

**Gate blocks `bd ready` but the step looks free.** Remember `bd list --parent` shows open children by default while gates hide in plain `bd list` output — run `bd gate list` and `bd blocked` together. A step missing from `ready` is either `blocks`-blocked (chapter 06, check `bd dep tree <id>`) or gate-blocked (this chapter, check `bd blocked`).

## Takeaways

- Gates order work against the *outside world* (human, timer, CI run, PR merge, foreign bead); `blocks` edges order beads against *each other*. Workers poll `bd ready`; supervisors manage `bd gate create/list/check/resolve/show`.
- `human` gates resolve by hand, `timer` gates expire via `bd gate check`, `gh:run`/`gh:pr` gates poll GitHub through the `gh` CLI (not run here — no GitHub in the sandbox), `bead` gates watch `<rig>:<bead-id>`.
- The merge-slot serializes merging: `create` once, `acquire --wait` before merging, `release` the moment it lands. `holder`/`waiters` metadata makes conflicts visible instead of destructive.
- Worktrees isolate files while sharing one beads DB via the git common directory — no redirect config. Never demo them in `/tmp` (unsafe-location guard) or inside `/Users/sergii/.ai` (real work lives there).
- Fleet maps 1:1: job phases pause at a human-approval gate (`--job-gate off` skips), tasks isolate per worktree (`--isolation none` opts out), and `isolation_exclude` keeps repos like `/Users/sergii/.ai` single-checkout.
- Finale: chapters 00–05 taught single-agent fluency, 06 taught hierarchy, 07 taught templates and swarms, and this chapter taught async coordination. The full arc — epic → children → swarm → gates → merge-slot → worktrees — is how many agentic workers share one beads DB safely.

Back to the overview: [index.md](index.md)

(End of file - total 438 lines)
