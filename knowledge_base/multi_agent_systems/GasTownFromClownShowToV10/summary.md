# Gas Town: From Clown Show to v1.0

**Article:** [*Gas Town: From Clown Show to v1.0*](https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec) — Steve Yegge, Medium, 2026-04-03 (paywalled on direct fetch; supplemented from [*Welcome to Gas Town*](https://yegge.ai/essays/welcome-to-gas-town/), 2026-01-01)
**Code:** https://github.com/gastownhall/gastown and https://github.com/gastownhall/beads

## Human Readable TL;DR

Imagine a factory where 20 to 30 robot helpers (AI coding assistants) all build things at once. The boss needs a foreman, a mail room, a to-do board that never gets lost, and a cleanup crew for when robots break down. Steve Yegge built that factory and called it Gas Town. At first it was a mess — robots got accidentally shut off mid-job, work went missing, and the database grew huge and slow. This article is the story of how he fixed all that and reached a stable version 1.0. No technical background needed: it is a story about organizing many workers so nothing gets lost.

## TL;DR

Gas Town is an IDE (Integrated Development Environment, the editor + tools where code gets written) replacement for orchestrating 20–30 Claude Code (and clone) agents at once, backed by Beads, a Git (version-control system)-backed work ledger (a durable list of tasks). The v1.0 post (2026-04-03) declares Gas Town and Beads stable after 3 months of chaos: serial-killer sprees (a buggy watchdog killing healthy workers), the 22-nose Clown Show (repeated Mayor data-loss incidents), piles of worker corpses, and Dolt (a SQL database with Git-like versioning) history bloat. Fixes: Beads with Embedded Dolt (no more fragile two-source sync), circuit breakers + duplicate-spawn guards, Deacon/Dogs patrol discipline, Refinery merge queue (a waiting line that merges code changes one by one), wisp (short-lived, non-permanent task record) orchestration, and compaction (Reaper + Compactor Dogs). Next step is Gas City, a reusable toolkit built from the same parts.

---

## Problem & Motivation

Single coding agents (CLI (Command-Line Interface, text-based control) helpers like Claude Code) lose track of work: sessions end, context fills up, parallel copies step on each other, nobody knows who is doing what. Yegge predicted orchestration ("Kubernetes (a system that keeps many computer programs running) for agents") was next, pitched it around, then built 4 orchestrators in 2025 (v1, v2 failed but produced Beads; v3 Python; v4 Go Gas Town, 17 days / ~75k lines, vibe-coded). The v1.0 article answers: what broke when this ran at scale for 3 months, and what finally held.

---

## Main Original Ideas

1. **Beads as the universal plane.** Every unit of work (task, fix, message, agent identity, workflow step) is a bead: an ID + status + assignee stored in a versioned database and Git. Agents read/write beads; humans audit. Sessions are disposable ("cattle"); beads persist.
2. **MEOW stack (Molecular Expression of Work).** Beads → Epics (parent tasks with child tasks) → Molecules (workflows: ordered chains of beads with any shape, loops, gates) → Protomolecules (reusable templates) → Formulas (TOML (a simple settings-file format) source files "cooked" into protomolecules) → Wisps/Mols (live copies). A marketplace ("Mol Mall") is planned.
3. **GUPP (Gastown Universal Propulsion Principle).** "If there is work on your hook, YOU MUST RUN IT." Each agent has a Hook bead (its personal to-do hanger). `gt sling` hangs work there. Startup prompt + `gt nudge` (a poke message) + Deacon heartbeat keep agents moving across crashes and restarts.
4. **NDI (Nondeterministic Idempotence, "messy path, sure finish").** Unlike Temporal (a workflow system with exact replay), Gas Town guarantees completion loosely: persistent molecule + persistent hook + persistent agent identity means any fresh session can resume and self-correct to the end.
5. **Wisps (ephemeral beads).** Patrol and orchestration runs use hash-ID beads that live only in the database, never in Git, then burn (delete), optionally squashed to one summary line. This keeps high-speed control chatter out of permanent history.
6. **Roles + patrols.** Seven worker roles (Mayor, Polecats, Refinery, Witness, Deacon, Dogs incl. Boot, Crew) plus Towns/Rigs (HQ vs per-project areas). Patrols are looping wisp-workflows with exponential backoff (sleep longer when idle), woken by any mutating command.
7. **Convoys as the ticket.** Every slung unit (one fix or a big swarm) is wrapped in a Convoy bead: a delivery-tracking wrapper with a dashboard (TUI (Text User Interface, graphics made of text)). Convoys land, then workers are recycled.

---

## Key Findings

- Scale reached: 20–30 parallel agents productively; MAKER 10-disc Hanoi (a 1000-step planning test) in minutes; 20-disc (~1M steps) as a generatable wisp.
- Failure list at scale (Clown Show era): serial-killer watchdog killing healthy Witness/Refinery sessions; 22 clown noses = 22 mass data-loss events scored on the Mayor over weeks; worker corpses piling up; polecat spawn storms (clown show #22: duplicate spawns + TOCTOU (Time-Of-Check-Time-Of-Use, a race where things change between checking and doing) races); Dolt commit-graph bloat (every bead write = a commit; deletes do not shrink history); orphan/duplicate Dolt databases causing silent data splits; hung sessions and stuck patrols needing elbow grease.
- What held for v1.0: Beads with Embedded Dolt (Dolt team build; embedded + server modes; kills bidirectional-sync, 3-way-merge, two-truths, tombstone bugs); circuit breakers, duplicate-spawn prevention, batched wisp-reaper updates; Deacon scoped to workspace, heartbeat surfaced, Dogs offload long steps; Refinery pre-verification + merge queue; maintenance mode "well over a month" post-Dolt-migration.
- Community signal: Beads ~20–23k stars; Gas Town ~13–16k stars, 240+ contributors, ~2000 commits in the early burst; non-technical users shipping tools on Beads alone.
- Cost/warning: needs Stage 6–7 operators (hand-running 3–10 agents already), multiple paid agent accounts, tmux (a tool that shows many text windows in one screen) fluency, tolerance for sloppy/throughput-first vibe work.

---

## Suggestions & Future Directions

1. Gas City: split Gas Town into reusable parts (identity, roles, mail, sessions, cost tracking, multi-model dispatch, skills, hooks, GUPP, NDI, formulas, molecules, convoys, patrols, plugins, tmux, seances) as an SDK (Software Development Kit, building blocks) for custom orchestrators; import Gas Town config directly.
2. Federation + Wasteland: link towns, shared wanted board, portable stamps/character-sheet reputation.
3. Mol Mall: marketplace for formulas/molecules.
4. Remote workers on big servers (hyperscalers), better dashboards/TUI, GUI (Graphical User Interface) / Emacs / web UIs, Refinery plugins + MQ (Merge Queue) reordering, timers/callbacks for plugins.
5. Training fix: get Beads/Gas Town factory-worker behavior into frontier-model training so less prompting is needed.

---

## Authors & Institutions

Steve Yegge (ex-Geoworks/Amazon/Google/Grab/Sourcegraph; independent; yegge.ai). Built with Claude Code-era agents (Opus 4.5/4.6 named; 4.7 noted as breaking Gas Town with a "just two more things" loop), the Dolt team (esp. Dustin Brown / Tim Sehn on embedded Dolt, GC (Garbage Collection, automatic cleanup)), and ~240 GitHub contributors. Community hub: gastownhall.ai. Follow-ons: Gas City, Wheelhouse/Wyvern (later essay).
