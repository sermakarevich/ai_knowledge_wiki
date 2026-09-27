> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# GasTown v1.0 Deep Dive — Targeted Fleet Lessons

**In one sentence:** Gas Town runs 20–30 coding agents as a self-fixing factory on a Git-backed task ledger, and its v1.0 was earned by fixing worker-killings, data loss, and database bloat the hard way.

## Key points

- Design = durable ledger first (Beads), disposable sessions, throughput over tidiness, explicit roles, workflows as data.
- Restarts work because agent, hook, and workflow are all Beads (saved in Dolt plus Git): any new session resumes via GUPP + nudge + Deacon heartbeat; dead polecat work is re-dispatched.
- Conflicts are serialized, not negotiated: one Refinery owns the Merge Queue; Beads routes cross-project requests by prefix; transaction discipline (BEGIN / DOLT_COMMIT / COMMIT) guards concurrent writes.
- Workflow units are Mayor / Crew / Convoy / patrol / molecule / formula, all implemented as beads + `gt` commands + tmux (a tool showing many text windows) sessions.
- Multi-harness = Claude Code and lookalikes (Codex, Gemini CLI (Command-Line Interface, text control), Amp, Amazon Q) via tmux sessions and role prompts; Beads works with anything as smart as Claude Sonnet 3.5+.
- Fleet can borrow 7 concrete ideas (convoys, sling+hook, wisps, refinery, witness, seance/handoff, mail-budget + nudge).
- Scale dangers to avoid: Dolt commit-graph bloat, two-truths sync, killer watchdogs, spawn storms, orphan databases, mail-as-storage, idle-polling cost.

---

## 1. Design principles stated by the author

Simple version: save everything important in shared notes; treat robot sessions as throwaway; keep moving even if sloppy.

- **Ledger over memory.** Beads (the shared to-do + message store, backed by Dolt, a SQL database with Git-like versioning, plus Git, a version-control system) is the single source of truth. "An agent is a Bead" — identity, inbox, hook, history all live there. Sessions are "cattle" (replaceable); beads are "pets" (kept).
- **Throughput over perfection.** Vibe-coding factory: some fixes land twice, some get lost, designs get redone — acceptable if the whole pile moves fast. Focus is creation + correction at speed of thought.
- **Graceful decay.** Every worker works alone or in small groups; town runs with or without tmux, with or without mail. You choose which parts run.
- **Opinionated roles with cute names as compression.** Mayor (boss helper), Polecats (short-lived task workers), Refinery (merger), Witness (babysitter), Deacon (heartbeat preacher) + Dogs (helpers) + Boot (Deacon watcher), Crew (your personal long-lived helpers). Names make the system clear to humans and to AI (Artificial Intelligence) agents.
- **Workflows as data, not code.** MEOW stack: Epics (big tasks with sub-tasks) → Molecules (ordered chains with loops/gates, Turing-complete, meaning they can express any computation) → Formulas (TOML recipe files) → Wisps (short-lived copies). Survives crashes because the plan is stored, not just in the robot's head.
- **Completion, not uptime.** Kubernetes (a program-keeper) asks "is it running?"; Gas Town asks "is it done?" Finish the convoy (delivery package), then delete the worker.
- **Elbow grease included.** Author is blunt: factory needs care, costs a lot (multiple paid accounts), needs tmux skill and Stage 6–7 operators (people already hand-running many agents).

## 2. Worker restart handling (serial-killer sprees, Deacon, corpse recovery)

Simple version: robots die all the time; the system makes sure their to-do list and identity survive, wakes a replacement, and gives unfinished work to someone else.

- **Serial-killer sprees:** early watchdog code for "hung session detection" killed healthy Witness and Refinery workers mid-job. Fix per CHANGELOG: removed that killer (commit f3d47a96); moved stuck-agent detection to a Dog plugin (5a5deaac); scoped Deacon zombie/orphan scan to the town workspace only; added daemon gates so refinery spawns only on real pending events.
- **Deacon + Dogs + Boot:** the Deacon is a patrol agent (a worker running a checklist in a loop). A background program (daemon) pings it every couple minutes ("do your job", DYFJ signal); it spreads the signal down. Dogs are its town-level helper crew for dirty jobs (clean branches, run plugins) so the long patrol never blocks mail. Boot is a special Dog woken every 5 minutes just to check the Deacon (heartbeat? nudge? restart? leave alone?) then sleep again.
- **Corpse recovery:** agent identity beads survive "nuke" (delete); history builds forever. Documented fixes: "auto re-dispatch recovered beads — Deacon recovers work from dead polecats", "Witness resets abandoned beads — dead polecat detection triggers work recovery", persistent polecat identity model, Mayor sessions survive tmux detach via auto-respawn hooks, `signal stop` handler for clean stop at turn edges.
- **GUPP + nudge:** GUPP (Gastown Universal Propulsion Principle) = "if work is on your hook, you must run it." Hook = personal pinned bead holding molecules. On start, worker must read hook + mail without waiting. Because Claude Code is "miserably polite" and idles, `gt nudge` sends a tmux poke (looks like typing) ~30–60s after start, max ~5 min. Hierarchical heartbeat (Deacon down) plus exponential-backoff patrols (sleep longer when idle; any bead/town change wakes all) keep night-long runs alive.
- **Handoff + seance:** `gt handoff` / `/handoff` / "let's hand off": worker tidies, optionally mails itself next steps, restarts in place in tmux. `gt seance`: new worker revives predecessor via `/resume` (reopen old session) using the session ID (identifier) saved in the nudge title, and asks "where is my stuff?" — fixes lost handoff notes.

## 3. Conflict resolution between workers

Simple version: do not let two robots edit the same pile at once — line them up, give each a lane, and let one trusted merger go one by one.

- **Refinery owns merging.** Polecats (task workers) produce MRs (Merge Requests, proposed code changes); only the Refinery merges to main, one at a time. It can reimagine/reimplement a change if the base moved too far. "No work can be lost, though it is allowed to escalate." Later: pre-verification (polecats test before `gt done`) lets Refinery skip repeat CI (Continuous Integration, automatic checks).
- **Witness smooths the swarm.** Per-project (rig) watcher un-sticks polecats (get MRs filed) and hustles Refinery (get queue drained); also peeks at Deacon for stuckness. Runs project-level plugins.
- **Beads routing + transactions.** Two-tier beads (project-level vs town-level orchestration) with cross-prefix routing (`bd create` / `bd show` pick the right database by prefix like `bd-`, `wy-`). All agents write to `main` branch; every write wraps BEGIN / DOLT_COMMIT / COMMIT together. Mail budget table (Polecat 0–1 mails per run, others protocol-only, Dogs zero-mail, nudge for rest) cuts chatter that used to cause races.
- **What it does NOT do:** no voting, no lock haggling between peers. Order comes from queue + patrol hierarchy, not agreement protocol. Cross-project work uses `gt worktree` (grab own copy of other project) to avoid stepping on feet.

## 4. Workflow abstraction (Mayor, Crew, Convoys, patrols, molecules/formulas) — how implemented

Simple version: everything is a note card (bead); commands move cards; robots live in named screen windows.

- **Mayor:** town-level concierge / chief-of-staff agent (Claude Code session in tmux with Mayor prompting + status line). Kicks off most convoys, gets pinged on landing, reads worker output so you do not have to, holds context/dreams, can summon polecats/Crew/convoys/dog-patrols. Implementation: role bead (job description) + agent bead (identity) + hook bead + inbox (beads) + tmux session + daemon supervision. Social trick: "Mayors are there to get yelled at" — close enough to yell at, powerful enough to act.
- **Crew:** per-project long-lived named agents you pick (e.g. design partners). Not managed by Witness. Cycle with `C-b n/p` (Control-b then n/p) in tmux. Same bead identity machinery, but driven directly by you (the Overseer, with own inbox).
- **Convoys:** delivery wrapper bead around any slung work (one fix or a swarm). Not an Epic (children have other parents; convoy tracks by reference). Created on every `gt sling`; shown in Charmbracelet TUI (text graphics) expanding-tree dashboard; "landed/finished" = done. Can take multiple swarm attacks before done; manager (e.g. Witness) recycles polecats onto it. Gate-state trick: polecat vanishes while waiting on GH (GitHub) Action / CI, then a Gate bead wakes a fresh polecat to continue.
- **Patrols:** looping wisp-molecules for Refinery / Witness / Deacon (+ Dogs). Steps: preflight clean → drain queue / check health / run plugins → postflight handoff. Backoff when empty; wake on any `gt`/`bd` (beads CLI) mutation or manual `gt` start (single worker / group / rig / town).
- **Molecules / formulas:** molecule = chain of beads with dependencies, loops, gates (wait states). Protomolecule = template graph (e.g. design→plan→build→review→test). Formula = TOML source cooked into protomolecule, then instantiated as wisp/mol with variable fill-in. Example: 20-step Beads release with CI waits; Rule-of-Five formula (each step reviewed 4 extra times with different focus). Future "Mol Mall" marketplace. NDI (described above) is why this is durable enough for a dev tool.

## 5. Multi-harness support (which agents, how dispatched)

Simple version: today it drives Claude-style terminal robots; the memory layer works with almost any smart robot.

- **Gas Town proper:** "only works with a handful of agents today" — in practice Claude Code plus stated clones: Codex, Gemini CLI, Amp, Amazon Q-developer CLI. "Claude Code" in the essay means all of them. Opus 4.5 named as able to handle any reasonably sized task; Opus 4.6 worked brilliantly; Opus 4.7 "just two more things" tic broke convergence (later essay). Dispatch = spawn tmux session per role + inject role prompt/priming + hook + mailbox; drive via `gt sling` (assign), `gt nudge` (poke), `gt handoff` (restart), `gt seance` (ask predecessor), daemon pings.
- **Beads alone:** "works with anything and everything, as long as it is roughly as smart as Claude Sonnet 3.5 was." Install via coding agent, no Gas Town needed. That is why Beads (~20k+ stars) outgrew Gas Town: memory/ledger is harness-neutral; orchestration is not yet.
- **Not yet:** federation/remote hyperscaler workers (Python version had GCP (Google Cloud Platform, rented computers) remotes; Go v1 needs design), GUI beyond tmux, fine multi-model dispatch (listed under Gas City SDK features: cost tracking, multi-model dispatch).

## 6. What concrete features/ideas can fleet borrow? List 5–8

Simple version: steal the cheap tricks that stop work from getting lost.

1. **Convoy wrapper for every dispatch.** Wrap each slung unit in a tracking bead with live tree view; "landed" = done. Fixes "issue wy-a7je4 finished — what was that part of?" confusion. Cheap in fleet: one parent record per batch.
2. **`sling + hook` (hang work, do not push sessions).** Keep per-worker hook list in the DB (database); dispatch = add row, poke session. Worker survives restarts because the list survives. Fleet already has a task DB (database) — add hook-per-worker view.
3. **Wisps for control chatter.** Patrol ticks, heartbeats, spawn events as DB-only rows burned after 24h (optional one-line squash to Git). Keeps the permanent log clean while keeping a live feed. Direct fix for history bloat.
4. **One Refinery for merges.** Single serializer for the merge queue with pre-verify (worker tests before hand-off) + skip-repeat-CI. Ends "monkey knife fight" rebases when many workers land at once.
5. **Witness per repo.** A babysitter loop per project that only un-sticks workers and drains the queue (no building). Bounded job = fewer stuck swarms, less manager prompting.
6. **Seance + graceful handoff.** Save session ID in the poke title; on restart, new session auto-`/resume`s the old one to recover dropped notes. Plus explicit hand-off command that tidies + restarts in place.
7. **Mail budget + nudge-first prompting.** Cap mails per role (workers 0–1, dogs zero, nudges for status); teach agents to prefer pokes over mails; zero-commit status paths (`gt nudge` over `gt mail send`). Cuts commit storms at the source.

## 7. What problems at scale should fleet avoid (Dolt bloat, data loss/Clown Show)

Simple version: the factory choked on its own paperwork — copy these warnings onto fleet's wall.

- **Dolt commit-graph bloat.** Every bead create/update/close = a Dolt commit; deletes leave history behind; `dolt gc` (cleanup) trims chunks but graph grows forever. High-speed patrols without wisps = unbounded growth. Fleet rule: ephemeral data (ticks, events, links) must be wisp-class (DB-only + Reaper delete + Compactor flatten via `DOLT_RESET --soft` / rebase / gc, with row-count check, concurrency abort, Mayor-escalate). Design doc notes auto-GC on since Dolt 1.75 + "flatten is pointer moves" — run daily+.
- **Two-truths sync (pre-Dolt).** Old Beads had JSONL (a text log file) + SQLite (a small database) with two-way sync, 3-way merges, races, tombstone (delete-marker) hell → weeks of Mayor data loss ("22 noses": a clown nose per mass-loss event). Fix was Embedded Dolt (one truth). Fleet rule: one primary store; JSONL only for disaster snapshots (Gas Town: scrubbed export every 15 min, proven in Clown Show #13); first re-sync after recovery needs `--force` push, then normal.
- **Killer watchdogs.** Hung-session killer murdered healthy workers ("always the Deacon" in murder mysteries). Fleet rule: never auto-kill from the hot loop; move stuck-detection to a slow plugin, scope scans, require spawn gates on real pending work, surface heartbeat + status.
- **Spawn storms + orphans.** Duplicate Dolt DBs on rig add (legacy `beads_` vs new names) split data silently (writer vs Mayor read different DBs); polecat duplicate spawns + TOCTOU races (clown show #22). Fleet rule: fail loudly on orphans, clean both naming forms, circuit breakers + idempotent (safe-to-retry) spawn, batched reaper updates, daemon-gated spawns.
- **Mail-as-storage + idle polling.** Unbounded mails = commits = bloat + cost; naked polling burns tokens. Fleet rule: mail budgets, nudge-first, backoff-to-sleep patrols, wake-on-mutation only.
- **Model + cost fragility.** Opus 4.7 loopiness killed convergence; 12–30 workers need multiple paid accounts and constant feeding (plans/formulas) or the factory starves. Fleet rule: pin known-good models per role, cap concurrency, generate work ahead (formulas/epics), track cost per convoy.

---

## Deltas: Clown Show v1.0 vs Welcome to Gas Town (Jan)

- Welcome (Jan, 17-day-old Go port): GUPP + nudge hack, MEOW invention, roles/patrols/convoys just flying (Dec 29), tmux UI, no federation/GUI/plugins/Mol Mall/million-step demo yet.
- v1.0 (Apr, +3 months): same bones, hardened — serial-killer fix, spawn-storm circuit breakers, wisp-reaper rewrite (formula-driven, batched), Witness ZFC cleanup, Deacon scoping + heartbeat UI, Refinery pre-verify, Embedded Dolt (the big one), maintenance mode, Gas City alpha as the reusable next step. Tone shifts from "do not use" to "ready; non-technical users shipping."
- Later arc (for context, not ingested here): Wasteland federation (Mar), Wheelhouse lessons (Opus 4.7 burn-down, legal-system governance) — out of scope for this entry.

**Covers:** Medium Clown-Show-to-v1.0 excerpts + yegge.ai Welcome essay (full) + gastown hub + dolt-storage + changelog/discussion excerpts, retrieved 2026-09-09.
