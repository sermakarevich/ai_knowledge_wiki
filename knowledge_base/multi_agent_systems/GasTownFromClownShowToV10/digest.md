> [[index|Wiki]] | [[summary|Summary]]

# Gas Town: From Clown Show to v1.0 — Digest

The whole source at medium depth: every page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-town-mayor-crew-convoys|The Town: Roles, Convoys, and the Daily Loop]]

**In one sentence:** Gas Town runs 20–30 coding agents as a self-managing factory town with seven worker roles, per-project rigs, mail-based messaging, and delivery-tracking convoys driven through tmux.

- The Town (`~/gt`, Go binary `gt`) is HQ; each managed git repo beneath it is a Rig, and the human is the Overseer — the eighth role with their own identity and inbox.
- Seven worker roles split the labor: Mayor (concierge/chief-of-staff), Polecats (ephemeral per-rig task swarm), Refinery (single serializer owning the merge queue), Witness (per-rig babysitter that un-sticks polecats and hustles the Refinery), Deacon (daemon-pinged patrol preacher), Dogs incl. Boot (Deacon's helper crew and its watcher), and Crew (long-lived named personal agents).
- Every unit of slung work is wrapped in a Convoy bead — a delivery-tracking wrapper with a Charmbracelet TUI (Text User Interface, graphics made of text) expanding-tree dashboard — and a convoy can absorb multiple swarm attacks before it lands.
- The core verbs are `gt sling` (hang work on a hook), `gt nudge` (tmux poke that kicks a polite idling agent into reading hook+mail), `gt handoff` (tidy + restart in place), and `gt seance` (revive a predecessor via `/resume` using the session ID saved in the nudge title).
- GUPP (Gastown Universal Propulsion Principle — "if there is work on your hook, YOU MUST RUN IT") plus the nudge hack plus the Deacon's hierarchical heartbeat keep convoys starting, completing, and landing unattended overnight.
- The daily loop is tmux-native (`C-b s` list/snoop, `C-b n/p` cycle crew, `C-b [` scroll, `C-b a` activity feed) and degrades gracefully: no-tmux mode and naked sessions still work, just slower.
- Opinionated cute names are deliberate compression: they make the org chart legible to humans and to the agents themselves.

## 2. [[wiki/02-beads-dolt-meow-wisps|Beads on Dolt: Ledger, MEOW, and Wisps]]

**In one sentence:** Beads is the Git-backed universal work ledger underneath everything in Gas Town, hardened for v1.0 by collapsing a fragile two-store sync into Embedded Dolt and expressing all work — from issues to multi-day workflows — as molecules on the MEOW stack with ephemeral wisps for control chatter.

- A bead is an ID + description + status + assignee issue stored in Dolt (a SQL database with Git-like versioning) and tracked in Git; "an agent is a Bead" — identity, inbox, hook, and history all live in the ledger, so sessions are disposable cattle and beads are the persistent pets.
- The v1.0 headline fix is Beads with Embedded Dolt (built with the Dolt team, embedded + server modes), which killed an entire bug family: bidirectional JSONL-vs-SQLite sync, 3-way merges, two-truths races, and tombstone (delete-marker) hell.
- The MEOW stack (Molecular Expression of Work) climbs Beads → Epics → Molecules → Protomolecules → Formulas (TOML recipe files "cooked" into templates) → Wisps/Mols, with a planned Mol Mall marketplace.
- NDI (Nondeterministic Idempotence, "messy path, sure finish") guarantees completion loosely unlike Temporal's exact replay: persistent molecule + persistent hook + persistent agent identity means any fresh session resumes and self-corrects to the end.
- Wisps are ephemeral hash-ID beads that live only in the database, never in Git, then burn (optionally squashed to one summary line) — they keep high-velocity patrol and orchestration chatter out of permanent history.
- Patrols are looping wisp-molecules (Refinery / Witness / Deacon) with exponential backoff and wake-on-any-mutation; Gate beads let workers vanish during CI waits and wake a fresh worker to continue.
- Plugins are "coordinated or scheduled attention from an agent": Deacon runs town-level plugins with Dogs (unbounded time), Witness runs rig-level ones, Refinery plugins (e.g. merge-queue reordering) were queued post-v1.0.

## 3. [[wiki/03-clown-show-failures|The Clown Show: Worker Failures and What Fixed Them]]

**In one sentence:** Three months of running 20–30 agents at scale produced a catalog of spectacular failures — killer watchdogs, 22 mass data-loss events, corpse pileups, spawn storms, and database bloat — and v1.0 is the list of fixes that finally held.

- A buggy hung-session watchdog murdered healthy Witness and Refinery workers mid-job; the fix removed the killer (commit f3d47a96), moved stuck-detection to a slow Dog plugin (5a5deaac), scoped Deacon scans to the town workspace, and gated spawns on real pending events.
- The "22 noses" Clown Show scored one clown nose per mass Mayor data-loss event over weeks, all rooted in the JSONL-plus-SQLite two-truths sync — ended by the Embedded Dolt migration to a single store.
- Dead workers left corpses (abandoned beads, stale branches, lost handoffs); recovery came from persistent identity beads, Deacon auto-re-dispatch of dead polecats' work, Witness abandoned-bead resets, and `signal stop` handling for clean turn-edge stops.
- Clown show #22 was a polecat spawn storm: duplicate spawns plus TOCTOU (Time-Of-Check-Time-Of-Use, a race where things change between checking and doing) races, fixed with circuit breakers, idempotent (safe-to-retry) spawn, daemon-gated spawns, and batched wisp-reaper updates.
- Dolt history bloat was structural — every bead write is a commit and deletes never shrink history — contained by wisps (control chatter stays out of Git), Reaper + Compactor Dogs, and daily-or-more auto-GC (on since Dolt 1.75).
- Silent data splits came from orphan/duplicate Dolt databases on rig add (legacy `beads_` vs new names): writer and Mayor read different DBs; the rule now is fail loudly on orphans and clean both naming forms.
- The v1.0 verdict rests on evidence, not vibes: maintenance mode "well over a month" post-migration, Beads ~20–23k stars, Gas Town ~13–16k stars with 240+ contributors and ~2000 commits in the early burst, and non-technical users shipping on Beads alone.

## 4. [[wiki/04-scale-lessons-for-fleet|Scale Lessons for Fleet: Costs, Comparisons, and Borrow List]]

**In one sentence:** Gas Town's v1.0 is a field manual for fleet: who may operate it and at what cost, why it resembles Kubernetes and Temporal without being either, which seven cheap tricks transfer directly, and what comes next with Gas City and federation.

- Gas Town demands Stage 6–7 operators (people already hand-running 3–10+ agents daily), multiple paid agent accounts (Yegge burned through two toward a third in a week), tmux fluency, and tolerance for throughput-first sloppiness — it is "a cash guzzler" by design.
- Kubernetes asks "is it running?" while Gas Town asks "is it done?": same control-plane/node/local-agent/source-of-truth shape, but completion (land the convoy, nuke the worker) instead of uptime, credited workers instead of anonymous pods, terminal goals instead of continuous desired state.
- Temporal gets durability from deterministic replay; Gas Town gets it from NDI (persistent molecule + hook + identity, self-correcting superintelligent executors) — plenty for a dev tool, not a Temporal replacement.
- Seven concrete borrowable ideas: convoy wrapper per dispatch, sling+hook instead of pushed sessions, wisps for control chatter, one Refinery for the merge queue, a Witness babysitter per repo, seance + graceful handoff, mail budgets with nudge-first prompting.
- Scale dangers for fleet's wall: Dolt commit-graph bloat, two-truths sync, killer watchdogs, spawn storms, orphan databases, mail-as-storage, idle-polling token burn, model fragility (Opus 4.7's "just two more things" loop broke convergence), and factory starvation without pre-generated plans.
- Only Claude Code and close clones (Codex, Gemini CLI, Amp, Amazon Q) drive the town today; Beads alone runs on anything ~Sonnet 3.5-smart — the ledger is portable, the orchestration is not yet.
- Gas City is the stated next step: the town split into reusable SDK (Software Development Kit, building blocks) parts (identity, roles, mail, sessions, cost tracking, multi-model dispatch, GUPP, NDI, formulas, convoys, patrols, plugins, seances), plus federation/Wasteland, Mol Mall, remote hyperscaler workers, and real dashboards.

## The argument in five moves

1. Single coding agents lose work at scale, so orchestration — "Kubernetes for agents" — is the next layer.
2. The answer is a factory town: disposable sessions throwing themselves at persistent work in a Git-backed ledger (Beads), with opinionated roles and propulsion (GUPP + nudge + heartbeat) instead of uptime management.
3. All work becomes chemistry: the MEOW stack turns issues into workflows into cookable formulas, with NDI guaranteeing completion and wisps keeping control chatter out of permanent history.
4. Three months at 20–30 agents burned off every naive assumption — killer watchdogs, 22 data-loss events, corpse pileups, spawn storms, history bloat — and each scar became a mechanism (Embedded Dolt, circuit breakers, Reaper/Compactor, mail budgets).
5. What held for "well over a month" is v1.0, and what generalizes is the borrow list: convoys, hooks, wisps, one merge serializer, per-repo babysitters, seances, and nudge-first thrift — the parts Gas City will factor into a reusable kit.
