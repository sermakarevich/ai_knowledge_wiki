> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: GasTown

## Claims vs. evidence
- "Runs 20-30 agents in parallel" — **suggestive**. Spawn is careful: `AllocateAndAdd` holds the pool flock (file lock) across alloc+mkdir to close the GH#2215 TOCTOU (time-of-check-time-of-use) race. But limiters confess: `batch_size` defaults to 1 spawn per heartbeat, `RigWorkerPool` is 10 workers with 30s per-rig timeout, and `spawn_delay` exists to damp Dolt (SQL database with version control) lock contention on port 3307.
- "Survives crashes" — **weak as stated, strong narrowly**. Git plus ledger
  survival is strong: branches, `WIP: checkpoint (auto)` commits, beads
  (issue records) rows. Session survival is weak: checkpoint is one JSON file
  via plain `os.WriteFile` (not atomic temp-plus-rename), detection is lazy
  at the next `gt prime --hook`, stale-after-24h is deleted, output is
  advisory context only — in-memory reasoning is lost by design.
- "Multi-harness, 13 coders" — **registry strong, coverage weak**. `AgentPresetInfo` plus `builtinPresets` is clean data-driven design: a new harness is one config row, never a new Go (programming language) class. Yet only `opencode` ships ACP (Agent Client Protocol, JSON-RPC over stdio) config, and most presets carry `SupportsHooks: false`, falling back to `gt prime`-then-`exec` wrappers plus beacon-plus-nudge polling.
- "Daemon keeps the town healthy" — **suggestive**. `RestartTracker` (30s initial, x2, 10m cap, crash-loop at 5 in 15m, reset after 30m stable) plus a 3-minute heartbeat plus GUPP (stuck-agent rule: live session, hooked work, no bead update for 30m) mail is real supervision. But 30 minutes to flag a spinner and 3 minutes to notice death is slow, and rate-limit pauses get a separate 60s `RecordPause` outside the crash budget — quota churn is free.
- "Safe merging via Refinery" — **strong**. `doMerge` verifies head, rehearses,
  runs gates, lands with `MergeNoFF` or vendor PR (pull request) API behind
  one `PRProvider` interface, serializes main pushes, aborts on conflict and
  files rework. Best subsystem in the digest.

## Genuinely new vs. repackaged
- Repackaged: the ledger is `github.com/steveyegge/beads v1.0.5` with a local
  wrapper; tmux (terminal multiplexer) farms, worktree-per-worker, and
  `gofrs/flock` advisory locks are decade-old hats-and-worktrees practice;
  Formula (TOML workflow files with `ReadySteps`) is a weaker cousin of
  Temporal/Hatchet (durable workflow engines with exactly-once retries) —
  interpreted by agents, never executed by a runner; mail beads notify rather
  than coordinate like AutoGen/MetaGPT (multi-agent dialogue frameworks).
- Genuinely useful integration: worktree-per-polecat plus per-rig Dolt routing
  plus convoy `tracks`-edge feeder (one ready issue per close event) with
  mountain auto-skip (3 failures parks the bead as `blocked`) plus a
  rehearsal-abort refinery — a combination no single prior system packages.
- Two small real insights: the nudge queue (JSON files, rename-to-`.claimed` exactly-once, rendered as `<system-reminder>`) avoids destructive tmux `send-keys` into busy agents; the harness registry proves configuration beats inheritance. Both are worth copying without adopting GasTown.

## Weaknesses and blind spots
- Single-machine assumption is load-bearing. One town tmux socket per host
  (`basename-hash6`), liveness via pane-process-tree scans to depth 10, and
  town-wide scheduling (`max_polecats` is host-shared CPU/API) mean no
  demonstrated multi-host dispatch. `AddRig` fails fast when Dolt is down.
- Dolt operations cost is unpriced. Central server, 15-minute backups,
  24-hour compactor, 1-hour wisp reaper, copytruncate log rotation (child
  file descriptors forbid rename), explicit `spawn_delay` for contention.
  Doctor's 100+ checks plus `internal/health` probes read as a symptom list
  for a substrate that needs constant babysitting.
- The most crash-exposed writer uses the weakest primitive. Settings files got
  `atomicfile.WriteFile` after gh#3500 truncated-JSON failures, yet the
  checkpoint file — the one recovery depends on — still uses bare
  `os.WriteFile`. The fix went where Claude complained, not where correct.
- Quota rotation is screen-scraping: regexes over the bottom 20 of 30 captured
  pane lines, 2-minute shell-out, keychain token swap under file lock, then
  restarts. Clever, provider-UI-dependent, one prompt-format change from
  silent misrotation.
- Coordination sprawl: durable mail with `delivery:pending`/`acked` labels, protocol mail (`MERGE_READY`, `FIX_NEEDED`), handoffs as self-mail, file nudges, plus five record systems (events, feed, town log, agentlog, activity). Auditable, expensive to query — no single "what happened" view.
- Prototype seams: `security-audit` formula keys with no matching struct fields; Gas City (role/capability layer) is one design doc, no runtime; Wasteland federation is declared Phase 1 "wild-west" unenforced; Deacon is a single long-running Claude patrol — one model, one point of judgment.

## Applicability
- Works when: one beefy host, git-native repos, parallelizable bead-shaped
  work, tolerance for 3-minute detection and 30-minute stuck-agent latency.
  Prerequisites: Go binary, tmux, Dolt server, `gh` CLI (command-line tool),
  disk for a bare `.repo.git` plus N full worktrees with submodule costs.
- Fails when: multi-machine teams, high-conflict monorepos (refinery never
  auto-merges — rework grows linearly with conflicts), GPU (graphics
  processor) training or stateful services (kill-then-recreate keeps files,
  kills processes), or Windows-first shops despite `flock_windows.go`.
- Honest niche: parallel coder isolation with auditable branch-per-task
  merges across many harnesses — not single-agent quality, not deterministic
  retries, not cross-host scale.

**Relevance to my work**
- Fleet orchestrator — **trial** three portable patterns: data-driven harness
  registry (one preset row per coder), refinery rehearsal-abort rule (workers
  never push to main), `RestartTracker` backoff plus file-based nudge queue
  instead of keystroke injection.
- AI/ML (artificial intelligence / machine learning) engineering — **ignore**
  as a training runner, **trial** as a parallel codegen harness: worktree
  isolation fits repo sweeps, but recovery covers files only, never weights
  or GPU state.
- Elisity data platform (Athena/S3 lake) — **watch, do not adopt**: convoy
  feeder plus `ReadySteps`/topological-sort batching suits pipeline batches,
  but a bespoke per-town SQL server contradicts the Athena (serverless query
  engine) lake model; borrow the feeder, not the backend.

## What this changes
- Demotes "agent recovery" to "branch plus bead survival": successors re-read
  git and ledger, never resurrect conversation. Fleet should copy this and
  stop promising session resume.
- Proves harness support scales by data rows, not code branches: fleet's coder
  matrix belongs in one config table (launch argv — command arguments, resume
  style, hooks provider), not one class per tool.
- Makes the merge queue the coordination primitive: abort-on-conflict with
  preserved branch and merge-request bead plus filed rework beats another
  messaging channel or shared-file merge.

## Verdict
GasTown is a well-integrated single-host worktree farm with one excellent
subsystem (Refinery merge queue) and one excellent configuration idea (the
harness registry), assembled from ordinary tmux, flock, and beads parts with
honest but slow supervision. Its crash-survival and parallel-scale claims
overreach what lazy non-atomic checkpoints and a single Dolt server show.
For fleet work the portable patterns merit a focused trial, while the runtime
as a whole stays on watch. **trial** — the refinery-plus-registry combination
is the single strongest reason.
