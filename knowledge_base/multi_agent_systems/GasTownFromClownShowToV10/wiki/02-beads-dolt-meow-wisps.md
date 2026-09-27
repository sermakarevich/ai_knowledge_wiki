> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Beads on Dolt: Ledger, MEOW, and Wisps

**In one sentence:** Beads is the Git-backed universal work ledger underneath everything in Gas Town, hardened for v1.0 by collapsing a fragile two-store sync into Embedded Dolt and expressing all work — from issues to multi-day workflows — as molecules on the MEOW stack with ephemeral wisps for control chatter.

## Key points

- A bead is an ID + description + status + assignee issue stored in Dolt (a SQL database with Git-like versioning) and tracked in Git; "an agent is a Bead" — identity, inbox, hook, and history all live in the ledger, so sessions are disposable cattle and beads are the persistent pets.
- The v1.0 headline fix is Beads with Embedded Dolt (built with the Dolt team, embedded + server modes), which killed an entire bug family: bidirectional JSONL-vs-SQLite sync, 3-way merges, two-truths races, and tombstone (delete-marker) hell.
- The MEOW stack (Molecular Expression of Work) climbs Beads → Epics → Molecules → Protomolecules → Formulas (TOML recipe files "cooked" into templates) → Wisps/Mols, with a planned Mol Mall marketplace.
- NDI (Nondeterministic Idempotence, "messy path, sure finish") guarantees completion loosely unlike Temporal's exact replay: persistent molecule + persistent hook + persistent agent identity means any fresh session resumes and self-corrects to the end.
- Wisps are ephemeral hash-ID beads that live only in the database, never in Git, then burn (optionally squashed to one summary line) — they keep high-velocity patrol and orchestration chatter out of permanent history.
- Patrols are looping wisp-molecules (Refinery / Witness / Deacon) with exponential backoff and wake-on-any-mutation; Gate beads let workers vanish during CI waits and wake a fresh worker to continue.
- Plugins are "coordinated or scheduled attention from an agent": Deacon runs town-level plugins with Dogs (unbounded time), Witness runs rig-level ones, Refinery plugins (e.g. merge-queue reordering) were queued post-v1.0.

---

## 1. Beads: the universal plane

Beads began in October as a 15-minute compromise — Yegge wanted Git, Claude wanted SQLite, they took both — and grew to ~225k lines of Go used daily by tens of thousands. The design bet: every unit of work (task, fix, message, agent identity, workflow step) is a bead, agents read/write beads, humans audit. Beads works "with anything and everything, as long as it is roughly as smart as Claude Sonnet 3.5 was" — which is why Beads (~20k+ stars) outgrew Gas Town itself: the memory/ledger layer is harness-neutral, the orchestration is not yet.

There are two tiers (project-level rig beads vs town-level orchestration beads) with cross-prefix routing, and all agents write to the `main` branch with every write wrapped as BEGIN / DOLT_COMMIT / COMMIT. Pinned beads (Role, Agent, Hook) float like yellow-sticky notes: never closed, hidden from `bd ready`, carrying identity and GUPP state.

## 2. Embedded Dolt: the migration that ended the Clown Show

The pre-v1.0 architecture kept JSONL (a text log file, one issue per line) plus SQLite with bidirectional sync, 3-way merges, tombstones, and races — "two truths" that diverged into weeks of Mayor data loss (the 22-nose Clown Show). The fix, built with the Dolt team (Dustin Brown / Tim Sehn), embeds Dolt directly: one truth, embedded + server modes, no sync layer at all. Post-migration the town sat in maintenance mode "well over a month" — the stability signal behind the v1.0 declaration. The disaster-recovery habit survived anyway: a scrubbed JSONL export every 15 minutes, proven in Clown Show #13, with a `--force` push required for the first re-sync after recovery.

## 3. The MEOW stack, layer by layer

| Layer | What it is |
|-------|------------|
| Beads | Atomic work units (issues with ID/status/assignee) |
| Epics | Beads with children (parallel by default, explicit dependencies force sequence; "upside-down" plans allowed) |
| Molecules | Workflows: chained beads of arbitrary shape with loops and gates, Turing-complete (able to express any computation), stitched at runtime |
| Protomolecules | Template graphs (e.g. design→plan→build→review→test) instantiated by copying beads + variable substitution |
| Formulas | TOML source form with a macro-expansion ("cooking") phase for loops/gates, cooked into protomolecules |
| Wisps / Mols | Live instantiated copies — wisps ephemeral, mols durable |

Yegge frames MEOW as more discovery than invention and the likeliest part to outlive Gas Town itself ("Gas Town may not live 12 months; the bones may live for years"). The motivating example is the 20-step Beads release with CI wait states: agents used to skip steps and need nagging; as a molecule, the agent walks the chain one bead at a time and the activity feed writes itself. Planned next: the Mol Mall marketplace for formulas.

## 4. NDI: completion without replay

Temporal (a workflow system) gets durability from deterministic replay; Gas Town gets it from NDI. The argument: molecules have well-specified acceptance criteria, AIs are good at following TODO lists, and the bureaucracy of checking off beads keeps them on track without boredom or self-managed TODO drift. Since agent, hook, and molecule are all persistent, a crash/compaction/restart just means the next session picks up the chain — mistakes included, because the agent can self-correct against the acceptance criteria. "Messy path, sure finish": not a Temporal replacement (edge cases abound), but durable enough for a dev tool. Demonstrated scale: 10-disc Hanoi (a 1000-step planning test) in minutes, 20-disc (~1M steps) as a generatable wisp.

## 5. Wisps and the Reaper/Compactor

Wisps (invented Dec 21st) are the vapor phase of matter for Gas Town work: database-only, hash-ID addressed, burned at run end, optionally squashed to a single digest line committed to git. Every patrol and workflow run mints a wisp molecule so execution is transactional without polluting Git. The supporting cast is the Reaper (batched wisp-reaper updates, rewritten formula-driven for v1.0) plus Compactor Dogs (history flattening via `DOLT_RESET --soft` / rebase / gc (Garbage Collection, automatic cleanup), with row-count checks, concurrency abort, and Mayor escalation). Design notes record auto-GC since Dolt 1.75 with "flatten is pointer moves" — run daily or more.

## 6. Patrols, gates, and plugins

A patrol is an ephemeral wisp-workflow run in a loop: preflight clean → drain queue / check health / run plugins → postflight handoff, with exponential backoff when idle (sleep longer and longer) and wake-on-any-`gt`/`bd`-mutation. The Refinery patrol drains the merge queue; the Witness patrol checks polecats, refineries, and peeks at the Deacon; the Deacon patrol runs town plugins and session-recycling protocol (offloaded to Dogs so long steps never block town mail). Gate beads suspend a workflow across long waits (GH Actions, CI) without holding a worker. Plugins are lifecycle-hook steps any workflow can embed; timers/callbacks exist but the subsystem is admittedly under-designed — most future add-on functionality is expected to ship as Mol Mall formulas instead.

**Covers:** Welcome essay Beads/MEOW/NDI/wisps/patrols/plugins sections (Figs 6, 9–13) + targeted.md sections 1, 3 + dolt-storage design excerpts.
