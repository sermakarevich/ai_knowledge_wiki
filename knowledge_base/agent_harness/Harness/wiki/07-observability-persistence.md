> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Observability, Persistence, Skills, and Context
**In one sentence:** Harness records every tool decision as a Postgres event row plus optional OTLP traces/metrics/logs, attributes token and cost usage per agent turn, and reassembles skills, rules, and memory into a budgeted prompt at compose time.
## Key points
- OTLP export covers three signals from one pipeline: traces (per-event spans plus workflow/activity/agent-turn trajectory spans), metrics (four counters/histograms), and logs (one record per event), configured by `OtelConfig` and defaulting to disabled (`crates/harness-core/src/config/misc.rs:404-439`, `crates/harness-observe/src/otel_export.rs:98-117`).
- Endpoint resolution order is explicit config endpoint, then `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable, then `http://127.0.0.1:4318` (HTTP) or `http://127.0.0.1:4317` (gRPC), followed by a TCP reachability probe that fails startup of the pipeline when unreachable (`crates/harness-observe/src/otel_export.rs:380-432`).
- The event store is a Postgres table (`events`) with eight versioned migrations, keyed by `(store_key, id)`, with batched inserts using `ON CONFLICT DO NOTHING`, JSONL backfill on first startup, and batched retention purges (`crates/harness-observe/src/event_store/migrations.rs:5-102`, `crates/harness-observe/src/event_store/mod.rs:167-229`, `crates/harness-observe/src/event_store/events.rs:51-80`).
- Usage and cost accounting centers on `UsageMetrics` (input, output, cache-read, cache-creation, reported-total) where the reported provider total takes precedence over the recomputed sum, and per-turn cost is attached to agent-turn spans from `turn.token_usage` (`crates/harness-observe/src/usage.rs:5-93`, `crates/harness-server/src/workflow_runtime_worker/otel_trajectory.rs:68-84`).
- Postgres schema management uses one schema per logical store via `PgStoreContext`, a `schema_migrations` ledger with a per-schema advisory lock, and a `harness_admin.schema_ownership` registry with keep/drop classification for orphaned path-derived schemas (`crates/harness-core/src/db_pg.rs:331-464`, `crates/harness-core/src/db_pg.rs:653-722`, `crates/harness-core/src/db_pg_schema_registry.rs:231-255`).
- Skill dedup is mechanical name-collision resolution by tier priority (Repo 4 > User 3 > Admin 2 > System 1) executed at the end of `discover()`, so a user-persisted skill shadows a same-named builtin (`crates/harness-skills/src/store.rs:204-212`, `crates/harness-skills/src/store.rs:383-410`, `crates/harness-skills/src/store.rs:781-788`).
- Memory and context retrieval is lexical: `LexicalKnowledgeRetriever` scores prompt-to-field token overlap with weights and a phrase bonus, and `ContextComposer` enforces token budgets, per-class quotas, `dedupe_key` elimination, and degradation levels before rendering (`crates/harness-core/src/retrieval.rs:287-348`, `crates/harness-context/src/composer.rs:415-456`, `crates/harness-context/src/types.rs:230-281`).
---
## OTLP observability and trajectory spans
Per-event telemetry is emitted in `OtelPipeline::record_event`: every event increments `harness.tool_decision.total` and writes a `tool_decision` span plus log record; first-seen sessions increment `harness.conversation_starts.total` through a bounded 10,000-entry `SessionStartDeduper`; hook/tool names containing `api`, `http`, or `request` tokens increment `harness.api_request.total`; events carrying `duration_ms` record `harness.tool_execution.duration_ms` (`crates/harness-observe/src/otel_export.rs:25-57`, `crates/harness-observe/src/otel_export.rs:98-172`). Span creation for the per-event path is a short-lived span per signal in `emit_trace`, with severity mapped from decision (Pass/Complete to Info, Warn to Warn, Block/Gate/Escalate to Error) in `emit_log` (`crates/harness-observe/src/otel_export.rs:205-228`, `crates/harness-observe/src/otel_export.rs:521-527`). Prompt payloads are redacted from attributes unless `log_user_prompt` is set (`crates/harness-observe/src/otel_export.rs:184-203`).
Trajectory spans form a separate three-level hierarchy. `WorkflowRootSpan`, `ActivitySpan`, and `AgentTurnSpan` carry a shared `TrajectoryTraceContext` (32-hex-char trace id, 16-hex-char root span id), created at workflow-instantiation time in the workflow runtime (`crates/harness-workflow/src/runtime/otel_trace_context.rs:10-26`, `crates/harness-observe/src/otel_trajectory.rs:18-79`). Recording validates hex ids, builds the workflow root as an explicit root span, derives deterministic activity span ids as `SHA256("activity:{runtime_job_id}")`, and nests agent-turn spans under the activity parent with GenAI allowlisted attributes (`gen_ai.system`, `gen_ai.request.model`, token counts, `harness.cost_usd`, workflow/activity/thread/turn ids, retry attempt) (`crates/harness-observe/src/otel_trajectory.rs:81-166`, `crates/harness-observe/src/otel_attributes.rs:18-71`). Emission happens in the server runtime worker after each runtime-job completion: activity span always, agent-turn span when a `runtime_turn` artifact resolves to a stored turn, workflow-root span only when the workflow reaches a terminal state; the whole path is gated on `otel.trajectory` and failures increment `harness.otel.trajectory_export_errors.total` instead of propagating (`crates/harness-server/src/workflow_runtime_worker/otel_trajectory.rs:13-95`, `crates/harness-observe/src/otel_export.rs:248-260`). Derived analytics (hook pass/warn/block rates, compliance trends, rule stats, quality grades across security/stability/coverage/performance, health reports) are computed from stored events, with `quality_grade` events explicitly excluded from grading to avoid self-reinforcement (`crates/harness-observe/src/stats.rs:39-66`, `crates/harness-observe/src/quality.rs:46-94`, `crates/harness-observe/src/health.rs:42-62`).

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OtelConfig {
    #[serde(default = "default_otel_environment")]
    pub environment: String,
    #[serde(default)]
    pub exporter: OtelExporter,
    #[serde(default)]
    pub endpoint: Option<String>,
    #[serde(default)]
    pub log_user_prompt: bool,
    #[serde(default)]
    pub trajectory: bool,
    #[serde(default)]
    pub capture_content: bool,
}
```
Verbatim from `crates/harness-core/src/config/misc.rs:404-417`.
## Event store and usage attribution
`EventStore` holds a schema-scoped `PgPool`, a `store_key` derived from the canonicalized data directory, and a lazily installed `OtelPipeline`; construction ensures the directory, opens a migrated pool, imports legacy SQLite and JSONL rows idempotently, and applies retention plus OTLP policy (`crates/harness-observe/src/event_store/mod.rs:31-111`, `crates/harness-observe/src/event_store/mod.rs:291-317`, `crates/harness-observe/src/event_store/mod.rs:325-408`). The ledger runs v1 (events table plus session/hook/decision/ts indexes) through v8 (timestamptz conversion), with v5 introducing the `store_key` scoping and composite primary key `(store_key, id)` and v7 adding nullable `run_id` (`crates/harness-observe/src/event_store/migrations.rs:5-102`). Session identity outside Postgres is a `.session` file renewed by mtime within a configurable window (default 1800 s) (`crates/harness-observe/src/session.rs:11-43`, `crates/harness-observe/src/event_store/mod.rs:156-158`).
Usage attribution per run reconciles two sources. Structurally, `UsageMetrics::from_token_usage` splits adapter `TokenUsage` into input/output plus cache-read derived as `total - (input + output)`, while `from_payload`/`parse_result_usage_metrics` parse `result`-type JSON lines with explicit cache fields; `total_tokens()` returns the provider-reported total when present (`crates/harness-observe/src/usage.rs:41-93`). At trajectory time the runtime worker copies the stored turn's `input_tokens`, `output_tokens`, and `cost_usd` into the agent-turn span attributes, with the model taken from the job's runtime profile (`crates/harness-server/src/workflow_runtime_worker/otel_trajectory.rs:59-84`). A separate lightweight probe counts usage surfaces (thread/turn RPC, thread manager, task DB, task runner, eval) into a `probe_report` event for coverage checks (`crates/harness-core/src/usage_probe.rs:5-85`).
## Postgres persistence and migrations
Connection handling separates a bootstrap pool from schema-scoped runtime pools: `resolve_database_url` prefers an explicit URL, then `HARNESS_DATABASE_URL` and config-file discovery; pool sizing defaults to 8 connections (1 under Supabase pooler URLs) with server/env overrides (`crates/harness-core/src/db_pg.rs:98-120`, `crates/harness-core/src/db_pg.rs:65-96`). `PgStoreContext::open_migrated_pool_with_setup_pool` ensures the schema, registers ownership, opens the runtime pool, and runs `PgMigrator` (`crates/harness-core/src/db_pg.rs:448-464`). The migrator takes a schema-level advisory lock on the same connection, creates the ledger table, skips applied versions, runs each body transactionally after splitting multi-statement SQL with a quote/comment-aware splitter, and releases the lock (`crates/harness-core/src/db_pg.rs:653-722`, `crates/harness-core/src/db_pg_split.rs:7-20`). Generic JSON-blob entities use `Db<T>` upsert/select/delete over `(id, data, created_at, updated_at)` tables (`crates/harness-core/src/db.rs:55-146`). The ownership registry (`harness_admin.schema_ownership`) records schema, owner kind/key/path, and retention class; cleanup planning lists `h`-prefixed 17-char schemas with table/row estimates and classifies them as Keep, DropCandidate (registered owner path missing), or Blocked (unregistered, requires explicit allowlist) (`crates/harness-core/src/db_pg_schema_registry.rs:289-314`, `crates/harness-core/src/db_pg_schema_registry.rs:492-543`).
## Skills, memory retrieval, and composed context
Skills load from four tiers (repo `.harness/skills/`, user `~/.harness/skills/`, admin `/etc/harness/skills/`, persist dir, plus 11 compiled-in builtins), parse version from frontmatter, trigger patterns from an HTML comment, hash content for change detection, and persist usage/quality/governance sidecars (`{name}.usage.json`) next to the markdown (`crates/harness-skills/src/store.rs:184-279`, `crates/harness-skills/src/builtin.rs:11-26`, `crates/harness-skills/src/store.rs:742-770`). Governance updates an EMA quality score (`0.8 * old + 0.2 * target` with failures weighted 0.7) and maps score plus sample count to Active/Watch/Quarantine (10% canary by deterministic skill-id plus prompt hash bucket)/Retired (`crates/harness-skills/src/store.rs:305-358`, `crates/harness-skills/src/store.rs:672-692`). Freshness classification uses last-used age thresholds (7/30/90 days) gated on a 5-sample minimum for Dormant (`crates/harness-skills/src/freshness.rs:28-60`). Prompt matching scores trigger patterns at weight 2.0, name 0.8, description 1.2, and content 0.25 through the shared lexical scorer (`crates/harness-skills/src/store.rs:694-723`).
The composer treats skills as one provider among rules, contract, brief, and drafts. Providers propose `ContextItem`s with class, priority (P0/P1/P2), relevance, degrade chains (summary, pointer, NAP-verified summarized), optional `dedupe_key`, and an instruction-bearing flag; composition applies provider timeouts, drops duplicate keys by priority then provider precedence (rules first), guarantees P0 fit or returns `MandatoryOverflow`, allocates per-class quotas (rule 0.30, skill 0.25, contract 0.25, brief 0.15, draft 0.05) with global redistribution, and collapses instruction overload beyond 15 items to pointers (`crates/harness-context/src/types.rs:132-208`, `crates/harness-context/src/composer.rs:169-244`, `crates/harness-context/src/composer.rs:246-339`, `crates/harness-context/src/composer.rs:415-456`, `crates/harness-context/src/composer.rs:525-590`). Project instruction files (`AGENTS.md`/`CLAUDE.md` with `AGENTS.override.md` replacement semantics, 32 KB cap) form the static layer underneath this dynamic composition (`crates/harness-core/src/agents_md.rs:14-50`).

```rust
    pub fn deduplicate(&mut self) {
        let mut seen: HashMap<String, usize> = HashMap::new();
        let mut to_remove = Vec::new();

        for (idx, skill) in self.skills.iter().enumerate() {
            match seen.entry(skill.name.clone()) {
                std::collections::hash_map::Entry::Vacant(slot) => {
                    slot.insert(idx);
                }
                std::collections::hash_map::Entry::Occupied(mut slot) => {
                    let existing_idx = *slot.get();
                    let existing_priority = location_priority(self.skills[existing_idx].location);
                    let new_priority = location_priority(skill.location);
                    if new_priority > existing_priority {
                        to_remove.push(existing_idx);
                        *slot.get_mut() = idx;
                    } else {
                        to_remove.push(idx);
                    }
                }
            }
        }

        to_remove.sort_unstable();
        for idx in to_remove.into_iter().rev() {
            self.skills.remove(idx);
        }
    }
```
Verbatim from `crates/harness-skills/src/store.rs:383-410`.
**Covers:** crates/harness-observe/src/lib.rs, crates/harness-observe/src/otel_export.rs, crates/harness-observe/src/otel_attributes.rs, crates/harness-observe/src/otel_trajectory.rs, crates/harness-observe/src/usage.rs, crates/harness-observe/src/stats.rs, crates/harness-observe/src/session.rs, crates/harness-observe/src/quality.rs, crates/harness-observe/src/health.rs, crates/harness-observe/src/event_store/mod.rs, crates/harness-observe/src/event_store/migrations.rs, crates/harness-observe/src/event_store/events.rs, crates/harness-observe/src/event_store/trajectory.rs, crates/harness-core/src/db.rs, crates/harness-core/src/db_pg.rs, crates/harness-core/src/db_pg_split.rs, crates/harness-core/src/db_pg_schema_registry.rs, crates/harness-core/src/retrieval.rs, crates/harness-core/src/agents_md.rs, crates/harness-core/src/usage_probe.rs, crates/harness-core/src/config/misc.rs, crates/harness-skills/src/lib.rs, crates/harness-skills/src/store.rs, crates/harness-skills/src/builtin.rs, crates/harness-skills/src/freshness.rs, crates/harness-context/src/lib.rs, crates/harness-context/src/composer.rs, crates/harness-context/src/types.rs, crates/harness-context/src/providers.rs, crates/harness-workflow/src/runtime/otel_trace_context.rs, crates/harness-server/src/workflow_runtime_worker/otel_trajectory.rs
