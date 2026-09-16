> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: superharness

## Claims vs. evidence

- "5,000+ tests": **weak**. Summary §10 marks the count "per README; not verified in source."
- Wiki citations prove strong unit/parity/contract coverage (golden argv (exact command-line arguments),
  dual-watchdog regressions, `test_enforcement_parity.py`), but cite no counted total
  and no multi-agent end-to-end (full run with real CLIs (command-line interfaces)) matrix.
- Verdict on this claim: per-README-not-verified. Count is marketing until counted.
- "Byte-identical parity": **strong, but narrow**. Pinned by `test_enforcement_parity.py:233-261`
  (two hook trees must stay byte-identical) plus golden argv tests (`test_harness_adapters.py:37-123`).
- Verified from wiki citations. But it proves the two paths did not drift, not that either is correct.
- "Agents never step on each other": **suggestive, overstated**.
- Real isolation is per-slot git worktrees (separate checkout directories, `worktree_ops.py:38-50`) — solid.
- The scope-guard hook does zero cross-agent file-set comparison; it only deny-blocks secrets/keys
  and warn-asks on system paths (`scope-guard.sh:27-42`). Same-worktree agents can still collide.
- "Tasks survive sessions": **strong**. Append-only handoffs plus ledger (audit log)
  plus git-stash checkpoints plus per-tick auto-flush YAML (human-readable config format)
  plus durable `recovery_count` in its own column. End-to-end runaway test proves it (`test_runaway_recovery_e2e.py:65-95`).
- Verified from wiki citations. Best-evidenced claim in the repo.

## Genuinely new vs. repackaged

- Novel: typed write boundaries. DAO (Data Access Object, class owning all reads/writes for one table)
  edge rejects bad phase/status with `BoundaryError` (`handoffs_dao.py:29-50`) instead of persisting garbage.
- Novel combination: that boundary plus enforcement parity (contract test forbidding check-drift)
  plus content-addressed dispatch context (prompt parts hashed by sha256 (fingerprint hash), `context_dao.py:16-32`).
- Novel: dual watchdog (idle-silence plus absolute-ceiling) evaluated over typed `events` rows
  (`lifecycle_rules.py:485-505`), where fresh events spare a past-deadline task. Real step past naive timeouts.
- Repackaged: SQLite (file-based database) queue with atomic `UPDATE ... RETURNING` claim
  is job-queue orthodoxy — Sidekiq/Celery did this a decade ago.
- Repackaged: handoffs are shift-logs (hospital handover notes) with Pydantic (Python validation library) validation;
  heartbeats, zombie reaping (`STALE_THRESHOLD_SECONDS=120`), retry ceilings (`max 12`, identical-error 4) are supervisor fare.
- Repackaged: skill extraction is keyword-overlap top-3 (`skill_extractor.py:329-360`), barely above grep (text search).
- Prior work: Beads (shared issue graph, no spawning/supervision), classic job queues,
  tmux (terminal multiplexer) farms like Claude Squad, LangGraph/AutoGen (in-process agent graphs).
- Positioning judgment: crash-safe OS-process (operating-system-level) supervisor for black-box coding CLIs.
  Narrow, useful, not a new coordination theory.

## Weaknesses and blind spots

- Single-machine SQLite (file-based database) ceiling. One `state.db` per project, `busy_timeout` 5000ms,
  WAL (fast local journal mode) local / PERSIST on network mounts. No multi-writer or multi-machine story.
- Split-brain handling fails closed (`StateDatabaseConflictError`, `paths.py:135-165`) instead of merging —
  misconfigured worktrees error rather than sync. Acknowledged in architecture, silent on scale path.
- `inbox_watch.py` at 5594 lines is a god module (one file doing everything): loop, dozen reconcilers,
  auto-approval, auto-recover, GC (garbage collection, automatic cleanup). Summary §10 flags change risk.
- Acknowledged as fact, silent as remediation — no decomposition plan cited.
- YAML legacy tail: export-only in theory, yet auto-flush files, pytest-only auto-ingest,
  and legacy `.superharness/state.sqlite3` roots persist. "Compatibility without split brain" means "we error."
- Partially acknowledged, never costed (dual-path maintenance, DB-path divergence bug class where any consumer
  resolving the path differently silently reads a different database).
- Event emitter degrades silently: unconfigured `emit()` is a no-op, background-writer DB failures are warn-only
  (`events.py:187-199`). Watchdog input can vanish without the caller noticing. Silent.
- Transcript-to-task attribution is heuristic — newest `.jsonl` modified after launch, no session-UUID
  (unique session identifier) mapping (`transcript_tail.py:15-71). Watchdog can credit the wrong task. Silent.
- Gates are bypassable suggestions: every `close` check (`close.py:123-168`) yields to `--force`/`--skip-verify`;
  subtask gate defaults off (`subtask_gate.py:3-10`); preflight blocks only deps/capabilities, spec/TDD gaps warn.
- Platform matrix thin: macOS launchd (background scheduler) self-heal every 300s is first-class,
  systemd (Linux equivalent) second-class, Windows absent. Silent.
- Silent-death history as evidence: 19+-hour watcher outage with no alert
  (`BUGREPORT-watcher-silent-death-no-recovery.md:12`), plus `operator start` dying with its shell.
- Three-layer supervision (daemon monitor plus launchd plus self-heal) is scar tissue retrofitted after failure,
  not designed-in reliability. Acknowledged in bug docs, underplayed in README (front-page docs) posture.
- Hygiene signal: `VERSION` file stale at 1.77.0 vs `pyproject.toml` 1.84.1 (Summary §10). Small, but version-truth
  drift in a system selling auditability is a bad look.

## Applicability

- Works: single-operator, single-machine, single-project multi-agent coding where each worker is a killable CLI.
- The solo power-user running Claude/Codex/Gemini/opencode/Pi overnight against one repo. That is the design center.
- Fails: fleet-scale multi-machine dispatch (no distributed queue, no auth beyond loopback dashboard).
- Fails: non-coding agents without a CLI surface; MCP (Model Context Protocol, tool-exposure standard) layer is auxiliary.
- **Relevance to my work:**
  - Borrow: typed DAO boundary plus `BoundaryError` (caller bug, re-raised) vs `StateError` (infrastructure, swallowed)
    split — directly fixes silent-corruption bugs in fleet state writes.
  - Borrow: durable retry counter in its own column plus identical-error threshold (4) plus absolute cap (12).
  - Trial: dual watchdog over typed events as replacement for single wall-clock timeouts in fleet workers; cheap prototype.
  - Ignore: whole harness as dependency — single-SQLite, single-machine, CLI-only assumptions contradict fleet scope.
    Port ideas, not code. Ignore skill/benchmark modules: keyword overlap plus local JSONL (newline-delimited JSON log)
    cost tables add weight without signal for ML (machine learning) experiment tracking.

## What this changes

- If claims hold, black-box CLI supervision becomes commodity: atomic claim, respawn-with-full-context,
  content-addressed prompts move from custom glue to importable patterns.
- Obsolete: hand-rolled tmux farms, YAML-status-file coordination, single wall-clock kill switches.
- Newly possible: unattended overnight multi-agent runs with bounded blast radius (retry ceilings plus worktree isolation),
  plus prompt-level reproducibility via hashed dispatch components (`shux diff --context`).
- Second-order effect: risk concentrates in the supervisor — stale bypassable gates, heuristic transcript attribution,
  and a 5594-line watcher nobody wants to refactor become the new single point of failure.

## Verdict

- Superharness is the best-built single-machine supervisor for coding-agent CLIs at this evidence depth,
  and its crash-recovery pipeline plus typed-boundary discipline deserves direct imitation in fleet.
- But its SQLite ceiling, god-module watcher, heuristic event attribution, and flag-bypassable gates
  disqualify it as a platform dependency for multi-machine orchestration.
- It solves the solo-operator problem well and the fleet problem not at all.
- Use the patterns, skip the dependency. trial
