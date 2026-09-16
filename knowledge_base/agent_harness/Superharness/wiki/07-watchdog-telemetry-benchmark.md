> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Watchdog, Telemetry, Skills, and Benchmarks

**In one sentence:** Stuck work is killed by a dual event-driven watchdog (`idle-timeout` + `absolute-ceiling`), liveness is decided from DB (Structured Query Language database) heartbeats, all activity lands in typed telemetry events with opt-in Langfuse (external observability backend) export, and completed work feeds a skill library plus a cost leaderboard.

## Key points

- **Watchdog A (idle timeout)** fails a task when minutes-since-last-`events`-row >= `idle_timeout_minutes` (`src/superharness/engine/lifecycle_rules.py:505`); **Watchdog B (absolute ceiling)** fails it when total age since `in_progress_at` >= `absolute_ceiling_minutes` even with fresh events (`src/superharness/engine/lifecycle_rules.py:485`).
- **Fresh events spare the task**: with event history present, idle/ceiling semantics fully replace the legacy `deadline_minutes` check, so an active task past its own deadline survives (`src/superharness/engine/lifecycle_rules.py:525`, `tests/unit/test_dual_watchdog.py:66`); with both keys unset behavior is byte-identical to legacy (`src/superharness/engine/lifecycle_rules.py:438`, `tests/unit/test_dual_watchdog.py:170`).
- **Liveness is one pure function**: `is_fresh(ts, ttl)` returns True only if the ISO-8601 (standard text date format) timestamp parses and is within TTL, default `WATCHER_TTL_SECONDS = 90`, never raising (`src/superharness/engine/liveness.py:18`, `src/superharness/engine/liveness.py:23`); the watcher stamps `agent_id="watcher"` each cycle via `touch_watcher` (`src/superharness/engine/liveness.py:40`).
- **Typed events table + fire-and-forget emitter**: `events(ts, kind, task_id, payload_json)` created in migration v31 (`src/superharness/engine/db.py:1306`); `emit()` validates synchronously then queues to a daemon background thread whose DB failures are warn-only (`src/superharness/engine/events.py:158`, `src/superharness/engine/events.py:199`); unconfigured `emit()` is a silent no-op until `configure(project_dir)` (`src/superharness/engine/events.py:187`).
- **Transcript progress feeds the watchdog** via persisted byte-offset cursors (`dispatch_cursors`, migration v32, `src/superharness/engine/db.py:1322`): `tail_step` reads only new complete lines since the stored offset, emits one `transcript_progress` event per tool-use line, resets to 0 on rotation/truncation (`src/superharness/engine/transcript_tail.py:162`).
- **Langfuse is opt-in and failure-isolated**: enabled only by `SUPERHARNESS_LANGFUSE_ENABLED` truthy plus credentials, `DO_NOT_TRACK` truthy is an absolute opt-out (`src/superharness/engine/langfuse_telemetry.py:51`, `src/superharness/engine/langfuse_telemetry.py:68`); dispatches export one pseudonymized event (`task_id_hash`, no content) named `superharness.dispatch.completed` (`src/superharness/engine/langfuse_telemetry.py:143`).
- **Skill flow is extract → persist → inject**: `record_skill` on task completion dedupes by `task_id` into `.superharness/skills.yaml` (`src/superharness/engine/skill_extractor.py:291`, `src/superharness/commands/task.py:769`); `get_skill_hints` keyword-searches top-3 into dispatch context (`src/superharness/engine/skill_extractor.py:360`, `src/superharness/engine/context_hint.py:166`); `skill_usage` table tracks per-skill uses/success-rate best-effort (`src/superharness/engine/skill_metrics.py:16`, `src/superharness/engine/skill_metrics.py:58`).
- **Benchmark is a JSONL (newline-delimited JSON log) leaderboard**: `record_dispatch` appends `BenchmarkRecord(task_id, agent, outcome, duration, cost, model, slot, fanout)` to `benchmark.jsonl` and also triggers the Langfuse export (`src/superharness/engine/benchmark.py:52`); `aggregate` ranks per-task stats by total cost descending (`src/superharness/engine/benchmark.py:139`); `shux benchmark --top 20 --agents/--models` renders it plus a 7-day per-model cost/budget view (`src/superharness/commands/benchmark.py:27`, `src/superharness/commands/benchmark.py:61`).

---

## Dual watchdog

Two independent kill conditions, evaluated per non-terminal task in `_check_deadlines` (`src/superharness/engine/lifecycle_rules.py:394`). Both are opt-in profile keys defaulting to 0 = disabled (`src/superharness/engine/lifecycle_rules.py:428`): `idle_timeout_minutes` (no telemetry for too long = wedged) and `absolute_ceiling_minutes` (running too long total = runaway). Age is measured from `in_progress_at` when present, else `created_at`, so long-queued tasks are not failed at dispatch (`src/superharness/engine/lifecycle_rules.py:413`). Last-event age comes from `SELECT MAX(ts) ... WHERE task_id = ?` (`src/superharness/engine/lifecycle_rules.py:376`); tasks with no event rows fall through to the unmodified PR #43 `deadline_minutes` path (`src/superharness/engine/lifecycle_rules.py:409`, `tests/unit/test_dual_watchdog.py:142`).

```python
# src/superharness/engine/lifecycle_rules.py:485-505
if absolute_ceiling > 0 and age >= absolute_ceiling:
    reason = (
        f"absolute ceiling exceeded ({int(age)}m elapsed >= "
        f"{absolute_ceiling}m ceiling) — task was in status '{status}'"
    )
    ...
if idle_timeout > 0 and last_event_age >= idle_timeout:
    reason = (
        f"idle timeout exceeded (no events for {int(last_event_age)}m >= "
        f"{idle_timeout}m idle limit) — task was in status '{status}'"
    )
```

The three regression cases pin the semantics: fresh events spare a past-deadline task (`tests/unit/test_dual_watchdog.py:66`), 15-min-silence with a 10-min limit fails with reason containing "idle" (`tests/unit/test_dual_watchdog.py:90`), and a 120-min run with 1-min-fresh events still fails with "ceiling" (`tests/unit/test_dual_watchdog.py:111`).

**Who watches the watcher** (motivated by a 19+-hour silent outage with no alert/restart, `docs/bugs/BUGREPORT-watcher-silent-death-no-recovery.md:12`, and by `operator start` being a foreground blocking loop that dies with its shell, `docs/bugs/watcher-dies-between-sessions.md:24`): three layers. (1) `daemon_monitor.run_monitor` adopts the first watcher PID, polls it with `pid_alive` since it cannot `wait()` on a non-child, then respawns via `_spawn_watcher` (`inbox_watch --once`) forever, rewriting `daemon-state.json` each cycle (`src/superharness/commands/daemon_monitor.py:109`, `src/superharness/commands/daemon_monitor.py:42`, `src/superharness/commands/daemon_monitor.py:69`). The checked-in `.superharness/daemon-monitor.py` is the legacy string-generated version of the same loop (`spawn` + `proc.wait()` + rewrite state, `.superharness/daemon-monitor.py:16`). (2) A per-project launchd/systemd daemon from `shux daemon` tracks state in `.superharness/daemon-state.json` (`src/superharness/commands/daemon.py:28`). (3) macOS launchd self-heal: a watchdog agent runs `operator heal --auto-discover --quiet` every 300s (`src/superharness/engine/launchd_health.py:376`); `heal()` bootouts zombies, removes stale-pattern services and orphan plists, then bootstraps the operator plist unless the user disabled it (`src/superharness/engine/launchd_health.py:315`). Operator labels are deterministic `com.superharness.operator.<md5-8>` hashes (`src/superharness/engine/launchd_health.py:114`), and auto-discovery only enrolls projects carrying a `.superharness/persistent` marker (`src/superharness/engine/launchd_health.py:465`). Note: `commands/watcher_worker.py` is worker-directory scaffolding (copy project, install watcher, `--recover-timeout-minutes/--recover-action` flags at `src/superharness/commands/watcher_worker.py:12`), not the supervise loop — the live respawn loop is `daemon_monitor`.

**Transcript cursors**: one row per dispatch in `dispatch_cursors(dispatch_id PK, path, byte_offset, updated_at)` (`src/superharness/engine/db.py:1327`); `_get_cursor`/`_set_cursor` do the read/upsert (`src/superharness/engine/transcript_tail.py:97`, `src/superharness/engine/transcript_tail.py:112`); only newline-terminated lines count as consumed so partial writes are re-read next step (`src/superharness/engine/transcript_tail.py:128`); tool-use is recognized in flat `{"type":"tool_use"}` or nested Claude-Code `message.content[]` shape (`src/superharness/engine/transcript_tail.py:146`); selection of which transcript to tail is heuristic — newest `.jsonl` modified after dispatch launch, since no dispatch-to-session-UUID mapping exists (`src/superharness/engine/transcript_tail.py:15`, `src/superharness/engine/transcript_tail.py:71`).

## Liveness

Two heartbeat stores with distinct roles. The legacy `agent_heartbeats` DAO (`shux heartbeat` every 30s, reconciler marks `zombie` after `STALE_THRESHOLD_SECONDS = 120`, `src/superharness/engine/heartbeat_dao.py:1`, `src/superharness/engine/heartbeat_dao.py:14`, `src/superharness/engine/heartbeat_dao.py:141`) coexists with the richer `watcher_heartbeat_dao` backing `heartbeat_contract.AgentHeartbeat` (extended columns from migration v25, `src/superharness/engine/watcher_heartbeat_dao.py:1`). `liveness.touch_watcher` upserts `agent_id="watcher"` at cycle start and `read_watcher_last_seen` reads it back — the same row `status.py` renders, so writer and reader share one signal (`src/superharness/engine/liveness.py:40`, `src/superharness/engine/liveness.py:54`, `src/superharness/engine/liveness.py:1`).

```python
# src/superharness/engine/liveness.py:23-37
def is_fresh(ts_str: str | None, ttl_seconds: int = WATCHER_TTL_SECONDS) -> bool:
    if not ts_str or not isinstance(ts_str, str):
        return False
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except ValueError:
        return False
    ...
    return age < ttl_seconds
```

The contract layer adds durability: SQLite is primary, YAML (`watcher.heartbeat.yaml`, `agents/<id>.heartbeat.yaml`) is skipped on success in `sqlite_only` mode but written as a crash dump on SQLite failure (`src/superharness/engine/heartbeat_contract.py:70`); reads prefer whichever is newer by file mtime, so a fresher crash dump supersedes stale SQLite (`src/superharness/engine/heartbeat_contract.py:154`, `src/superharness/engine/heartbeat_contract.py:217`); `is_stale` defaults to 120s and returns True on unparseable input (`src/superharness/engine/heartbeat_contract.py:274`); `list_agent_heartbeats` merges SQLite (wins on conflict) with YAML-written external runtimes (`src/superharness/engine/heartbeat_contract.py:296`). Singleton exclusion for the watcher itself is a `watcher_instance` lease row: INSERT, steal-if-stale (default 120s), else `SingletonConflict`; only the owning PID can heartbeat or release (`src/superharness/engine/watcher_singleton.py:21`, `src/superharness/engine/watcher_singleton.py:91`, `src/superharness/engine/watcher_singleton.py:100`).

## Telemetry events

Two parallel streams: free-form JSONL for dashboard tailing (`.superharness/events.jsonl`, best-effort append, `src/superharness/engine/event_stream.py:21`) and the typed queryable SQLite `events` table this watchdog consumes. Event shape is structural, not nominal: any frozen dataclass with non-empty str `kind` and a `task_id` (`src/superharness/engine/events.py:77`); core kinds are `TaskTransition(task_id, from_status, to_status)`, `DispatchStarted(task_id, agent)`, `DispatchFinished(task_id, agent, duration_s, exit_code)`, plus `TranscriptProgress(task_id, line_kind)` with `kind="transcript_progress"` (`src/superharness/engine/events.py:35`, `src/superharness/engine/transcript_tail.py:39`). `validate_event` runs synchronously inside `emit()` before queueing — TypeError on wrong shape/field type (int accepted for float), ValueError on empty `task_id` — so malformed payloads never reach the writer regardless of configuration (`src/superharness/engine/events.py:86`, `src/superharness/engine/events.py:199`).

```python
# src/superharness/engine/events.py:158-181
def _write_one(self, event: Event) -> None:
    try:
        ...
        conn.execute(
            "INSERT INTO events (ts, kind, task_id, payload_json) VALUES (?, ?, ?, ?)",
            (now, event.kind, task_id, payload),
        )
        conn.commit()
    except Exception:
        logger.warning(
            "events: emit failed for kind=%r task_id=%r", ...
            exc_info=True,
        )
```

One `_Emitter` per configured project, daemon thread draining a queue with `flush(timeout)` barrier support (`src/superharness/engine/events.py:133`, `src/superharness/engine/events.py:215`); payload is `json.dumps(asdict(event), sort_keys=True)` (`src/superharness/engine/events.py:158`); `configure` is idempotent per project dir (`src/superharness/engine/events.py:187`).

## Langfuse

Readiness is a 4-state gate — `disabled` / `incomplete` (missing keys listed) / `missing-sdk` / `configured` — and anything but `configured` makes export return False (`src/superharness/engine/langfuse_telemetry.py:89`, `src/superharness/engine/langfuse_telemetry.py:143`). Settings come from the machine credential file first, env second (`src/superharness/engine/langfuse_telemetry.py:46`, `src/superharness/engine/langfuse_telemetry.py:68`); failures log only the exception class name to avoid echoing secrets (`src/superharness/engine/langfuse_telemetry.py:122`). Per-dispatch span metadata carries `project_id` hash, `task_id_hash` (sha256 truncated to 12 chars, `src/superharness/engine/langfuse_telemetry.py:139`), agent, outcome, duration, cost, model, slot/fanout, version — `level="ERROR"` on failed/timeout else DEFAULT (`src/superharness/engine/langfuse_telemetry.py:156`). Wired into the benchmark path: `record_dispatch` calls `emit_dispatch_event` after every append, swallowing export faults (`src/superharness/engine/benchmark.py:89`).

## Skill extraction

Triggered on task completion: `task.py` builds a minimal dict and calls `record_skill`, printing `Skill recorded: [<category>] <title>` (`src/superharness/commands/task.py:769`). `extract_skill_from_task` returns None without id+title, else builds a corpus (title + summary + TDD values + acceptance criteria), infers category from first-matching signal list (security/test/bug-fix/refactor/docs/perf/config/feature, default `feature`), extracts up to 8 technique keywords, summarizes `git diff --shortstat` (`files_changed/insertions/deletions`, test-file flag), records TDD use and date (`src/superharness/engine/skill_extractor.py:212`, `src/superharness/engine/skill_extractor.py:33`, `src/superharness/engine/skill_extractor.py:72`, `src/superharness/engine/skill_extractor.py:142`). Persistence dedupes on `task_id` and tolerates write failure (`src/superharness/engine/skill_extractor.py:291`); retrieval is keyword-overlap scoring (`[a-z]{3,}` words) top-N (`src/superharness/engine/skill_extractor.py:329`); hints render as `Prior skill [<category>][TDD][tests]: <title> — <summary> (techniques: …)` capped at 3 per task (`src/superharness/engine/skill_extractor.py:360`). `skill_metrics` is the usage ledger: `record_skill_usage(skill, agent, task_id, outcome)` and `get_skill_insights` (`uses`, `success_rate`) grouped by skill (`src/superharness/engine/skill_metrics.py:16`, `src/superharness/engine/skill_metrics.py:58`).

Supporting memory (not skills proper): the **distiller** curates session record (handoffs + ledger, date-filtered) into a condensed transcript and extracts ≤3 `LessonEntry(text, type, confidence)` via an injected `llm_fn`, returning [] on empty input, LLM fault, or malformed JSON (`src/superharness/engine/distiller.py:71`, `src/superharness/engine/distiller.py:137`, `src/superharness/engine/distiller.py:27`); valid lesson types are user/feedback/project/reference (`src/superharness/engine/distiller.py:28`). **Operator memory** is a SQLite failure-pattern table (`pattern_signature UNIQUE, resolution, confidence, hit/miss counts`) with confidence = hits/total, new entries seeded at 0.5, `prune_stale` dropping < 0.3, and `observe_and_promote` returning `permanent_block` once an unknown signature is seen `threshold` (default 3) times so repeat identical failures fail fast (`src/superharness/engine/operator_memory.py:25`, `src/superharness/engine/operator_memory.py:104`, `src/superharness/engine/operator_memory.py:131`, `src/superharness/engine/operator_memory.py:182`, `src/superharness/engine/operator_memory.py:195`). **Agent memory** is two-tier markdown (global `~/.config/superharness/memory/`, project `.superharness/memory/`) with FIFO pruning at 5,000 chars and a confidence-capped distilled index (200 lines / 25KB, manual lines never evicted) (`src/superharness/engine/agent_memory.py:1`, `src/superharness/engine/agent_memory.py:22`, `src/superharness/engine/agent_memory.py:31`).

## Benchmark

`BenchmarkRecord` fields are fixed: task, agent, outcome (`done|failed|timeout|paused`), duration, cost, model, slot_index (-1 = single), fanout_n, timestamp (`src/superharness/engine/benchmark.py:30`). Writes use `os.open(O_APPEND|O_CREAT)` + pre-built line to shrink the write window, warn-and-continue on OSError (`src/superharness/engine/benchmark.py:52`); reads skip malformed lines (`src/superharness/engine/benchmark.py:99`). `aggregate` buckets by task, counts successes (`done`) vs failures (`failed|timeout`, `paused` ignored), averages duration/cost, tracks ordered-unique agents, sorts most-expensive-first (`src/superharness/engine/benchmark.py:139`); `leaderboard(project, top_n=20)` slices (`src/superharness/engine/benchmark.py:183`); `format_leaderboard` prints the fixed-width table plus `Total cost tracked` line (`src/superharness/engine/benchmark.py:194`). The CLI adds `--models` for a last-7-days per-model task/cost table with weekly-budget `% used` when configured (`src/superharness/commands/benchmark.py:61`).

Model tiers behind the `model` field: `engine/models.yaml` maps each agent (claude-code, codex-cli, gemini-cli) to mini/standard/max model IDs plus `pricing` per MTok and `chatgpt_account_overrides` for Codex-on-ChatGPT-auth remaps (`src/superharness/engine/models.yaml:1`, `src/superharness/engine/models.yaml:20`, `src/superharness/engine/models.yaml:24`). `model_router.resolve_model(target, tier)` resolves YAML map → adapter registry → hardcoded `MODEL_MAP`/sonnet fallback, then applies the ChatGPT-auth override for codex-cli (`src/superharness/engine/model_router.py:807`); valid tiers are exactly {mini, standard, max} with `standard` as the fallback tier (`src/superharness/engine/model_router.py:42`); `cheap_model()` returns the mini-tier model for summarizer-class calls (`src/superharness/engine/model_router.py:77`); fleet endpoint failover pairs each tier's endpoint with that same tier's model ordered mini→standard→all (`src/superharness/engine/model_router.py:289`).

**Covers:** dual watchdog (idle + ceiling), watcher supervision (daemon-monitor/launchd/singleton), DB liveness, typed events + JSONL stream, transcript cursors, Langfuse opt-in, skill extractor + metrics, distiller + operator/agent memory, benchmark leaderboard + model tiers/routing.
