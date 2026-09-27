> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Clown Show: Worker Failures and What Fixed Them

**In one sentence:** Three months of running 20–30 agents at scale produced a catalog of spectacular failures — killer watchdogs, 22 mass data-loss events, corpse pileups, spawn storms, and database bloat — and v1.0 is the list of fixes that finally held.

## Key points

- A buggy hung-session watchdog murdered healthy Witness and Refinery workers mid-job; the fix removed the killer (commit f3d47a96), moved stuck-detection to a slow Dog plugin (5a5deaac), scoped Deacon scans to the town workspace, and gated spawns on real pending events.
- The "22 noses" Clown Show scored one clown nose per mass Mayor data-loss event over weeks, all rooted in the JSONL-plus-SQLite two-truths sync — ended by the Embedded Dolt migration to a single store.
- Dead workers left corpses (abandoned beads, stale branches, lost handoffs); recovery came from persistent identity beads, Deacon auto-re-dispatch of dead polecats' work, Witness abandoned-bead resets, and `signal stop` handling for clean turn-edge stops.
- Clown show #22 was a polecat spawn storm: duplicate spawns plus TOCTOU (Time-Of-Check-Time-Of-Use, a race where things change between checking and doing) races, fixed with circuit breakers, idempotent (safe-to-retry) spawn, daemon-gated spawns, and batched wisp-reaper updates.
- Dolt history bloat was structural — every bead write is a commit and deletes never shrink history — contained by wisps (control chatter stays out of Git), Reaper + Compactor Dogs, and daily-or-more auto-GC (on since Dolt 1.75).
- Silent data splits came from orphan/duplicate Dolt databases on rig add (legacy `beads_` vs new names): writer and Mayor read different DBs; the rule now is fail loudly on orphans and clean both naming forms.
- The v1.0 verdict rests on evidence, not vibes: maintenance mode "well over a month" post-migration, Beads ~20–23k stars, Gas Town ~13–16k stars with 240+ contributors and ~2000 commits in the early burst, and non-technical users shipping on Beads alone.

---

## 1. Serial-killer sprees

Early "hung session detection" watchdog code killed healthy Witness and Refinery sessions mid-job — in Gas Town murder mysteries, Yegge notes, "it is always the Deacon." The remediation, traceable in the CHANGELOG:

1. Removed the killer outright (commit f3d47a96).
2. Moved stuck-agent detection out of the hot loop into a slow Dog plugin (5a5deaac).
3. Scoped Deacon zombie/orphan scans to the town workspace only.
4. Added daemon gates so refinery spawns fire only on real pending events.
5. Surfaced Deacon heartbeat + status so stuckness is visible instead of guessed.

The standing rule: never auto-kill from the hot loop.

## 2. The 22 noses: mass Mayor data loss

Over several weeks the Mayor suffered repeated mass data-loss incidents — one clown nose awarded per event, 22 total. Root cause was architectural, not operational: JSONL + SQLite with two-way sync, 3-way merges, races, and tombstone bookkeeping meant the two stores silently diverged, and weeks of Mayor state evaporated. Weeks of elbow grease plus the scrubbed-JSONL-every-15-minutes snapshot habit (proven in Clown Show #13) kept losses survivable until Embedded Dolt removed the second truth entirely. First re-sync after any recovery still needs a `--force` push, then normal operation resumes.

## 3. Corpses, orphans, and stuck patrols

At swarm scale, dead polecats, stale branches, hung sessions, and stuck patrols piled up faster than humans could clear them. The recovery machinery:

- **Identity survives "nuke":** agent identity beads persist past session deletion and accumulate history forever, so a replacement inherits the paper trail.
- **Deacon re-dispatch:** recovered beads from dead polecats are automatically re-dispatched.
- **Witness resets:** dead-polecat detection triggers abandoned-bead resets back to ready.
- **Mayor resilience:** Mayor sessions survive tmux detach via auto-respawn hooks.
- **Clean stops:** `signal stop` handlers end work at turn edges instead of mid-write.
- **Orphan databases:** rig-add could create duplicate Dolt DBs under legacy vs new names, silently splitting writer traffic from what the Mayor read. Now: fail loudly, clean both forms.

## 4. Spawn storm #22 and the Refinery under load

Discussion #2283 (v0.10.0) documents clown show #22: duplicate polecat spawns colliding through TOCTOU races, stampeding the merge queue into the classic "monkey knife fight" over rebasing — the baseline moving so far mid-swarm that late merges faced an unrecognizable head. Fixes: circuit breakers, duplicate-spawn prevention, idempotent spawn paths, batched wisp-reaper updates, daemon-gated spawns. On the merge side, the Refinery holds the line as the single serializer (one-at-a-time merges, allowed to reimplement when the base moved), upgraded with pre-verification — polecats test before `gt done`, so the Refinery skips repeat CI.

## 5. Dolt bloat: the paperwork that choked the factory

Every bead create/update/close is a Dolt commit; deletes leave history behind; `dolt gc` trims chunks but the commit graph grows forever. High-speed patrols writing permanent beads meant unbounded growth. The containment stack: wisps for all ephemeral chatter (DB-only + burn), Reaper batching, Compactor flattening with safety checks (row-count verification, concurrency abort, Mayor escalation), plus engine-level auto-GC. Without the wisp discipline, any fleet-scale patrol loop recreates this failure exactly.

## 6. What "v1.0" actually means

The v1.0 post (2026-04-03) declares stability on three legs: same architecture as the January essay, hardened (killer fix, spawn-storm breakers, wisp-reaper rewrite, Witness cleanup, Deacon scoping + heartbeat UI, Refinery pre-verify, Embedded Dolt); maintenance mode with no firefighting for well over a month; and community proof (star counts, 240+ contributors, non-technical builders shipping on Beads). Tone shift from "do not use" to "ready" — with the Stage 6–7 operator, multi-account cost, and tmux-fluency caveats intact.

**Covers:** Medium Clown-Show-to-v1.0 excerpts + discussion #2283 + CHANGELOG fix commits + targeted.md sections 2, 7.
