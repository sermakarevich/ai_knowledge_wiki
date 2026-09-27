---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Gas Town: From Clown Show to v1.0

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. Name the seven Gas Town worker roles and the one-line job of each.

> [!tip]- Answer
> Mayor (concierge/chief-of-staff), Polecats (ephemeral per-rig swarm producing MRs), Refinery (single merge-queue serializer), Witness (per-rig babysitter un-sticking polecats), Deacon (daemon-pinged patrol preacher), Dogs incl. Boot (Deacon's helpers + watcher), Crew (long-lived personal agents). See [[wiki/01-town-mayor-crew-convoys|The Town: Roles, Convoys, and the Daily Loop]].

### Q2. Why does every slung unit of work get wrapped in a Convoy, and what problem does that solve?

> [!tip]- Answer
> Because bare issue IDs ("wy-a7je4 finished") carry no context about the larger block they belonged to; the Convoy bead tracks all referenced issues for one delivery with a live tree dashboard until it lands, absorbing multiple swarm attacks. See [[wiki/01-town-mayor-crew-convoys|The Town: Roles, Convoys, and the Daily Loop]].

### Q3. State GUPP in one sentence and explain why the nudge hack is needed alongside it.

> [!tip]- Answer
> GUPP: if there is work on your hook, you must run it. The nudge is needed because Claude Code is "miserably polite" and often idles waiting for input instead of reading hook+mail, so `gt nudge` sends a tmux poke that looks like typing to kick it into action. See [[wiki/01-town-mayor-crew-convoys|The Town: Roles, Convoys, and the Daily Loop]].

### Q4. What does "an agent is a Bead" mean, and why does it make sessions disposable?

> [!tip]- Answer
> Identity, inbox, hook, and history all live as persistent beads in Dolt+Git, so a session is just cattle thrown at persistent work — any fresh session resumes via GUPP because nothing important lived in the dead session's memory. See [[wiki/02-beads-dolt-meow-wisps|Beads on Dolt: Ledger, MEOW, and Wisps]].

### Q5. What was the two-truths sync problem, and what single change ended it?

> [!tip]- Answer
> Beads kept JSONL plus SQLite with bidirectional sync, 3-way merges, races, and tombstones, so the stores diverged into 22 mass Mayor data-loss events; Embedded Dolt collapsed everything to one store with no sync layer. See [[wiki/02-beads-dolt-meow-wisps|Beads on Dolt: Ledger, MEOW, and Wisps]] and [[wiki/03-clown-show-failures|The Clown Show: Worker Failures and What Fixed Them]].

### Q6. Contrast NDI with Temporal-style durability, and say when you would still pick Temporal.

> [!tip]- Answer
> Temporal replays deterministically for exact guarantees; NDI completes loosely via persistent molecule+hook+identity plus self-correcting executors ("messy path, sure finish"). Pick Temporal when you need exact-once semantics; NDI is durable enough for a dev tool. See [[wiki/02-beads-dolt-meow-wisps|Beads on Dolt: Ledger, MEOW, and Wisps]].

### Q7. What are wisps, and which structural failure do they prevent?

> [!tip]- Answer
> Ephemeral hash-ID beads living only in the database, burned after the run (optionally one-line squash); they keep high-velocity patrol/orchestration chatter out of Git, preventing Dolt commit-graph bloat where every write is a permanent commit. See [[wiki/02-beads-dolt-meow-wisps|Beads on Dolt: Ledger, MEOW, and Wisps]].

### Q8. What caused the serial-killer sprees and clown show #22, and what fixed each?

> [!tip]- Answer
> The sprees: buggy hung-session watchdog killing healthy Witness/Refinery workers — fixed by removing the killer, moving stuck-detection to a slow Dog plugin, scoping Deacon scans, gating spawns. #22: duplicate polecat spawns plus TOCTOU races stampeding the merge queue — fixed with circuit breakers, idempotent spawn, daemon-gated spawns, batched reaper updates. See [[wiki/03-clown-show-failures|The Clown Show: Worker Failures and What Fixed Them]].

### Q9. Kubernetes asks "is it running?" — what does Gas Town ask, and what are two design consequences of the difference?

> [!tip]- Answer
> Gas Town asks "is it done?" Consequences: optimize for completion (land the convoy, then nuke the worker) not uptime; credited workers with history chains over disposable session-cattle; terminal goals instead of continuous desired-state reconciliation. See [[wiki/04-scale-lessons-for-fleet|Scale Lessons for Fleet: Costs, Comparisons, and Borrow List]].

### Q10. List four of the seven fleet-borrowable ideas and the failure each one prevents.

> [!tip]- Answer
> Any four: convoy wrapper (mystery completions), sling+hook (lost work on restart), wisps (history bloat), one Refinery (merge knife-fights), per-repo Witness (stuck swarms), seance+handoff (lost handoff notes), mail budgets + nudge-first (commit storms). See [[wiki/04-scale-lessons-for-fleet|Scale Lessons for Fleet: Costs, Comparisons, and Borrow List]].

### Q11. What is the weakest link in the v1.0 stability claim, and what evidence would strengthen or break it? (evaluation)

> [!tip]- Answer
> The claim rests on one operator's "well over a month" of maintenance mode plus star counts — no independent reproduction, no controlled failure-rate numbers, no cost-per-convoy accounting. Independent multi-operator replication with measured incident rates would strengthen it; a second Clown Show under a different model (like the Opus 4.7 convergence break) would weaken it. See [[critical_thinking|Critical Analysis]].
