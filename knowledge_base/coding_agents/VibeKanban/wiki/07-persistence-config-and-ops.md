> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Persistence, Config, and Ops: SQLite, Services, CLI, MCP
**In one sentence:** Vibe Kanban is a single-tenant local-first app whose state lives in one SQLite file (`db.v2.sqlite` under the OS data dir), mutated through a `Deployment` trait with ~20 services, launched via a Node `npx-cli` wrapper around the `server` binary, and exposed to agents through a stdio MCP task server.

## Key points
- All durable state lives in a single SQLite file at `<asset_dir>/db.v2.sqlite` (`crates/db/src/lib.rs:77-80`), with `create_if_missing(true)` and `JournalMode::Delete` (`crates/db/src/lib.rs:81-83`); 76 migrations ship under `crates/db/migrations/`.
- The `db` crate models 16 domains (`crates/db/src/models/mod.rs:1-16`); the `services` crate registers 20+ services (`crates/services/src/services/mod.rs:1-23`) behind the `Deployment` trait (`crates/deployment/src/lib.rs:1-80`).
- Server startup binds two Axum listeners (main app + preview proxy) with ports from `BACKEND_PORT`/`PORT` and `PREVIEW_PROXY_PORT`, defaulting to port 0 for OS auto-assignment (`crates/server/src/main.rs:96-113`), and records them in a temp-dir port file (`crates/server/src/main.rs:123-125`).
- Runtime config is file-based JSON under the same asset dir: `config.json`, `profiles.json`, `credentials.json` (`crates/utils/src/assets.rs:31-41`), loaded with silent-default fallback (`crates/services/src/services/config/mod.rs:53-63`).
- The `npx-cli` (`npx-cli/src/cli.ts:308-337`) exposes three commands — default app launch, `review`, `mcp` — downloading per-platform zips and caching them under a versioned cache dir (`npx-cli/src/cli.ts:90-94`).
- The MCP server (`crates/mcp/src/bin/vibe_kanban_mcp.rs:23-50`) speaks stdio, resolves the backend URL from `VIBE_BACKEND_URL` else `MCP_HOST`/`MCP_PORT` else the port file (`crates/mcp/src/bin/vibe_kanban_mcp.rs:100-134`), and exposes ~30 tools in global mode vs 7 in orchestrator mode (`crates/mcp/src/task_server/tools/mod.rs:52-73`).
- Operational risks cluster around `unwrap`/`expect` on hot paths, a Windows-only migration-checksum auto-fix, and `Delete` (non-WAL) journal mode limiting write concurrency.

---
## 1. Persistence: SQLite file, connection, migrations

State lives in one file. `DBService::new` constructs the URL from the platform asset dir (`crates/db/src/lib.rs:77-80`):

```rust
// crates/db/src/lib.rs:77-84
let database_url = format!(
    "sqlite://{}",
    asset_dir().join("db.v2.sqlite").to_string_lossy()
);
let options = SqliteConnectOptions::from_str(&database_url)?
    .create_if_missing(true)
    .journal_mode(SqliteJournalMode::Delete);
```

Asset dir resolution (`crates/utils/src/assets.rs:6-22`): debug builds use `<repo>/dev_assets`; release builds use `ProjectDirs::from("ai", "bloop", "vibe-kanban")` (`crates/utils/src/assets.rs:24-29`), i.e. macOS `~/Library/Application Support/ai.bloop.vibe-kanban`, Linux `~/.local/share/vibe-kanban` (XDG), Windows `%APPDATA%`. The server ensures the dir exists at boot (`crates/server/src/main.rs:52-55`) and one-time copies legacy `db.sqlite` to `db.v2.sqlite` for safe downgrade (`crates/server/src/main.rs:58-68`):

```rust
// crates/server/src/main.rs:58-68
let old_db = asset_dir().join("db.sqlite");
let new_db = asset_dir().join("db.v2.sqlite");
if !new_db.exists() && old_db.exists() {
    tracing::info!("Copying database to new location: {:?} -> {:?}", old_db, new_db);
    std::fs::copy(&old_db, &new_db).expect("Failed to copy database file");
}
```

Migration count is 76 files in `crates/db/migrations/` (from `20250617183714_init.sql` through `20260317120000_cleanup_attachment_schema.sql`), applied via `sqlx::migrate!("./migrations")` (`crates/db/src/lib.rs:15-20`). The runner has a platform branch: `VersionMismatch` fails hard in debug and on non-Windows release, but on Windows it rewrites the stored checksum and retries once per version (`crates/db/src/lib.rs:21-68`). There are two pool constructors: `DBService::new` (default pool) and `new_migration_pool` with statement logging disabled and `max_connections(64)` (`crates/db/src/lib.rs:89-102`), plus `new_with_after_connect`/`create_pool` hooks for tests (`crates/db/src/lib.rs:104-153`).

Model inventory (16 modules, `crates/db/src/models/mod.rs:1-16`): `task`, `workspace`, `workspace_repo`, `session` (formerly task-attempts, renamed in `20251216142123_refactor_task_attempts_to_workspaces_sessions.sql`), `execution_process`, `execution_process_logs`, `execution_process_repo_state`, `coding_agent_turn`, `project`, `repo`, `pull_request`, `merge`, `tag` (templates converted to tags in `20251020120000_convert_templates_to_tags.sql`), `scratch` (refactored in `20251120000001_refactor_to_scratch.sql`), `file`, `requests`, `session`. Execution logs were additionally migrated from DB rows to filesystem files at deployment startup (`crates/local-deployment/src/lib.rs:~92-96`, `migrate_execution_logs_to_files`).

Concurrency note: `JournalMode::Delete` (not WAL) serializes writers; the codebase compensates with a connection pool and per-execution `MsgStore` log streaming (`crates/services/src/services/execution_process.rs:256-262`, `crates/services/src/services/container.rs:89-91`), but write-heavy parallel agent runs share one SQLite writer.

## 2. Service inventory

Services are declared in `crates/services/src/services/mod.rs:1-23` and consumed through the `Deployment` trait (`crates/deployment/src/lib.rs:1-80`). `LocalDeployment` (`crates/local-deployment/src/lib.rs:1-100`) is the concrete single-node implementation wiring all of them.

| Service module (`crates/services/src/services/`) | Owns |
|---|---|
| `analytics.rs` (`mod.rs:1`) | PostHog telemetry, user-id generation, `session_start` tracking |
| `approvals.rs` (`mod.rs:2`) | Approval workflows for agent actions |
| `auth.rs` (`mod.rs:3`) | `AuthContext`, request identity |
| `config/` (`mod.rs:4`) | Versioned `Config` schema (current `v8`), load/save, editor/notification/theme sub-config |
| `container.rs` (`mod.rs:5`) | Central orchestrator: worktree/container lifecycle, process spawn, cleanup scripts, orphan reaping, msg-stores |
| `diff_stream.rs` (`mod.rs:6`) | Streaming diff state (`known_paths`, `sent_file_stats`) |
| `events.rs` + `events/` (`mod.rs:7`) | SSE event bus, JSON-patch builders |
| `execution_process.rs` (`mod.rs:8`) | Execution-process records, log streaming to storage, log-to-file migration |
| `file.rs` (`mod.rs:9`) | File read/write API used by routes |
| `file_ranker.rs` (`mod.rs:10`) | File relevance ranking |
| `file_search.rs` (`mod.rs:11`) | `FileSearchCache` backing search |
| `filesystem.rs` (`mod.rs:12`) | Filesystem operations service |
| `filesystem_watcher.rs` (`mod.rs:13`) | Debounced directory watching (notify-based) |
| `notification.rs` (`mod.rs:14`) | Desktop/sound notifications |
| `oauth_credentials.rs` (`mod.rs:15`) | OAuth token storage |
| `pr_monitor.rs` (`mod.rs:16`) | PR status polling/sync notifications |
| `qa_repos.rs` (`mod.rs:18-19`, `qa-mode` feature) | QA fixture repos |
| `queued_message.rs` (`mod.rs:20`) | Queued follow-up prompts per session |
| `remote_client.rs` (`mod.rs:21`) | Client for shared remote API (`VK_SHARED_API_BASE`) |
| `remote_sync.rs` (`mod.rs:22`) | Remote/local sync logic |
| `repo.rs` (`mod.rs:23`) | Repo registry, setup/cleanup/dev-script ownership |

Cross-cutting: `ContainerService` exposes `msg_stores() -> Arc<RwLock<HashMap<Uuid, Arc<MsgStore>>>>` (`crates/services/src/services/container.rs:89`), and spawns background work via `tokio::spawn` for log streaming (`crates/services/src/services/execution_process.rs:59-62,256-262`) and per-execution tasks (`crates/services/src/services/container.rs:979`). Shutdown is cooperative via `CancellationToken` created in `main` (`crates/server/src/main.rs:70`) and honoured by both Axum servers (`crates/server/src/main.rs:164-170`); cleanup kills all running execution processes (`crates/server/src/main.rs:236-242`).

## 3. Config and env surface

File config paths all derive from `asset_dir` (`crates/utils/src/assets.rs:31-53`): `config.json` (`:31-33`), `profiles.json` (`:35-37`), `credentials.json` (`:39-41`), plus `trusted_ed25519_public_keys.json`, `server_ed25519_signing_key`, `relay_host_credentials.json`. Load is infallible-by-design (`crates/services/src/services/config/mod.rs:53-63`):

```rust
// crates/services/src/services/config/mod.rs:53-63
pub async fn load_config_from_file(config_path: &PathBuf) -> Config {
    match std::fs::read_to_string(config_path) {
        Ok(raw_config) => Config::from(raw_config),
        Err(_) => {
            tracing::info!("No config file found, creating one");
            Config::default()
        }
    }
}
```

`Config` is versioned (`versions::v8`, `crates/services/src/services/config/mod.rs:44`), with `save_config_to_file` doing pretty-printed overwrite (`crates/services/src/services/config/mod.rs:66-73`). Current schema covers theme, notifications, editor, GitHub, UI language, showcase state, and default PR/commit prompts (`DEFAULT_PR_DESCRIPTION_PROMPT`, `DEFAULT_COMMIT_REMINDER_PROMPT`, `crates/services/src/services/config/mod.rs:9-30`).

Env-var table (Variable | Default | Purpose):

| Variable | Default | Purpose / read site |
|---|---|---|
| `RUST_LOG` | `info` | Tracing filter level (`crates/server/src/main.rs:41-44`) |
| `BACKEND_PORT` / `PORT` | `0` (OS-assigned) | Main Axum port; ANSI-stripped then parsed (`crates/server/src/main.rs:96-108`) |
| `PREVIEW_PROXY_PORT` | `0` | Preview subdomain proxy port (`crates/server/src/main.rs:110-113`) |
| `HOST` | `127.0.0.1` | Bind host for both listeners (`crates/server/src/main.rs:115`) |
| `VK_ALLOWED_ORIGINS` | — | Extra allowed origins for middleware (`crates/server/src/middleware/origin.rs:142`) |
| `VIBE_BACKEND_URL` | — (else port file) | MCP backend override (`crates/mcp/src/bin/vibe_kanban_mcp.rs:101-108`) |
| `MCP_HOST` / `MCP_PORT` | `127.0.0.1` / `BACKEND_PORT`/`PORT`/port-file | MCP connection target (`crates/mcp/src/bin/vibe_kanban_mcp.rs:9-10,110-129`) |
| `VK_SHARED_API_BASE` | `https://api.vibekanban.com` (set in `local-build.sh:46-47`) | Remote-sync API base (`crates/local-deployment/src/lib.rs:171`) |
| `VK_SHARED_RELAY_API_BASE` | — | Relay API base (`crates/local-deployment/src/lib.rs:174`) |
| `POSTHOG_API_KEY` / `POSTHOG_API_ENDPOINT` | — (analytics disabled if absent) | Telemetry (`crates/services/src/services/analytics.rs:26-29`) |
| `SENTRY_DSN` / `SENTRY_DSN_REMOTE` | — | Error reporting (`crates/utils/src/sentry.rs:30-33`) |
| `DISABLE_WORKTREE_CLEANUP` | unset (cleanup on) | Skip worktree deletion, debugging (`crates/local-deployment/src/container.rs:277`) |
| `VIBE_KANBAN_DEBUG` | unset | Verbose CLI errors + stack traces (`npx-cli/src/cli.ts:141,302,342`) |
| `CODEX_HOME` | — | Codex executor home override (`crates/executors/src/executors/codex.rs:19`) |
| `XDG_CONFIG_HOME` | OS default | OpenCode config discovery (`crates/executors/src/executors/opencode.rs:459,506`) |
| `SHELL` | — | Shell selection for commands (`crates/utils/src/shell.rs:159`) |

Port discovery across processes uses a temp-dir file: `write_port_file_with_proxy` writes `{main_port, preview_proxy_port}` JSON to `<tmp>/vibe-kanban/vibe-kanban.port` (`crates/utils/src/port_file.rs:12-28`); `read_port_file`/`read_port_info` read it with legacy bare-port fallback (`crates/utils/src/port_file.rs:30-55`). MCP and desktop helpers consume this file when env vars are absent.

## 4. CLI entry and server boot

Three binaries are built by `local-build.sh:56-58` (`cargo build --release`, plus `vibe-kanban-mcp` and `review`) and zipped per platform into `npx-cli/dist/<os-arch>/` (`local-build.sh:60-78`). The web UI is built first from `packages/local-web` (`local-build.sh:53-54`); `VK_SHARED_API_BASE` is baked in for the build (`local-build.sh:46-47`).

`npx-cli` (`npx-cli/src/cli.ts`) resolves the platform dir among `linux-x64/arm64`, `windows-x64/arm64`, `macos-x64/arm64` (`npx-cli/src/cli.ts:67-84`), with Rosetta detection on macOS (`npx-cli/src/cli.ts:30-48`). Commands registered via `cac` (`npx-cli/src/cli.ts:308-337`):

| Invocation | Effect |
|---|---|
| `npx vibe-kanban [--desktop]` | Default command: browser mode (spawn `vibe-kanban` server binary, auto-open browser) or Tauri desktop bundle (`npx-cli/src/cli.ts:244-279`) |
| `npx vibe-kanban mcp [...args]` | Spawn `vibe-kanban-mcp`, defaulting to `--mode global` (`npx-cli/src/cli.ts:122-124,327-332,216-231`) |
| `npx vibe-kanban review [...args]` | Spawn `vibe-kanban-review` passthrough (`npx-cli/src/cli.ts:233-242,320-325`) |
| `node bin/cli.js --mcp ...` | Legacy flag normalized to `mcp` subcommand (`npx-cli/src/cli.ts:281-295`) |

Binaries are cached under `CACHE_DIR/<BINARY_TAG>/<platformDir>` (or `LOCAL_DIST_DIR` in dev, `npx-cli/src/cli.ts:90-94`), downloaded via `ensureBinary`, extracted with adm-zip, chmodded, then exec/spawned (`npx-cli/src/cli.ts:126-196`). Old version dirs are pruned after a successful launch (`npx-cli/src/cli.ts:96-111,183-186`).

Server boot (`crates/server/src/main.rs:32-198`): install rustls provider (`:34-37`), init Sentry + tracing (`:39-50`), ensure asset dir, migrate DB file, build `DeploymentImpl` (`:72`), run orphan-execution cleanup and commit/name backfills (`:74-88`), fire `session_start` analytics (`:89-91`), preload executor-options cache in background (`:93-95`), bind main + proxy listeners (`:117-121`), write port file (`:123-125`), set client addresses (`:133-140`), build routers, optionally open browser in release (`:145-159`), serve both routers with graceful shutdown (`:167-181`), spawn relay registration (`:183`), then `select!` on signal vs server handles (`:185-191`) and kill running processes on exit (`:236-242`).

## 5. MCP task server

Binary `vibe-kanban-mcp` (`crates/mcp/src/bin/vibe_kanban_mcp.rs:23-50`) runs an rmcp stdio server. CLI surface is `--mode <global|orchestrator>` (default `global`), `-h/--help`; anything else errors (`crates/mcp/src/bin/vibe_kanban_mcp.rs:52-98`). Server identity is `vibe-kanban-mcp 1.0.0`, protocol `V_2025_03_26`, instructions listing all tool names (`crates/mcp/src/task_server/handler.rs:9-44`).

Context bootstrap: on `init()` the server queries `GET /api/containers/attempt-context?container_ref=<cwd>` (500 ms timeout) and, if found, builds `McpContext` (workspace, branch, repos, plus remote org/project/issue via `/api/remote/...`) (`crates/mcp/src/task_server/mod.rs:87-153,190-244`). If no context in global mode the `get_context` tool is unregistered (`crates/mcp/src/task_server/mod.rs:90-99`). Orchestrator mode requires context and scopes `workspace_id` plus `orchestrator_session_id` (`crates/mcp/src/task_server/tools/mod.rs:77-86,190-204`).

Routers (`crates/mcp/src/task_server/tools/mod.rs:51-74`): global composes all 11 tool routers; orchestrator keeps only context + workspaces (minus `list_workspaces`/`delete_workspace`) + sessions. The pinned orchestrator set is asserted in tests (`crates/mcp/src/task_server/tools/mod.rs:414-428`): `create_session, get_context, get_execution, list_sessions, run_session_prompt, update_session, update_workspace`.

| Tool | File:line | Purpose |
|---|---|---|
| `get_context` | `tools/context.rs:10` | Return active workspace/repo/remote/orchestrator metadata |
| `list_workspaces` | `tools/workspaces.rs:102` | List local workspaces with filters/pagination |
| `update_workspace` | `tools/workspaces.rs:172` | Rename/edit workspace (kept in orchestrator mode) |
| `delete_workspace` | `tools/workspaces.rs:213` | Delete workspace + branches (global only) |
| `list_organizations` | `tools/organizations.rs:67` | List available organizations |
| `list_org_members` | `tools/organizations.rs:95` | List members of an org |
| `list_repos` | `tools/repos.rs:84` | List all repos |
| `get_repo` | `tools/repos.rs:110` | Get one repo by id |
| `update_setup_script` | `tools/repos.rs:132` | Edit repo setup script |
| `update_cleanup_script` | `tools/repos.rs:161` | Edit repo cleanup script |
| `update_dev_server_script` | `tools/repos.rs:190` | Edit repo dev-server script |
| `list_projects` | `tools/remote_projects.rs:49` | List remote projects |
| `create_issue` | `tools/remote_issues.rs:258` | Create remote issue (resolves status, expands `@tags`) |
| `list_issues` | `tools/remote_issues.rs:322` | List/filter/sort remote issues |
| `get_issue` | `tools/remote_issues.rs:468` | Get issue detail (incl. PRs, tags, relations) |
| `update_issue` | `tools/remote_issues.rs:486` | Edit issue fields |
| `list_issue_priorities` | `tools/remote_issues.rs:559` | List allowed priorities |
| `delete_issue` | `tools/remote_issues.rs:569` | Delete issue by id |
| `list_issue_assignees` | `tools/issue_assignees.rs:66` | List assignees for an issue |
| `assign_issue` | `tools/issue_assignees.rs:101` | Assign user to issue |
| `unassign_issue` | `tools/issue_assignees.rs:124` | Remove assignee by `issue_assignee_id` |
| `list_tags` | `tools/issue_tags.rs:93` | List all tags |
| `list_issue_tags` | `tools/issue_tags.rs:127` | List tags on an issue |
| `add_issue_tag` | `tools/issue_tags.rs:155` | Attach tag to issue |
| `remove_issue_tag` | `tools/issue_tags.rs:178` | Remove tag by `issue_tag_id` |
| `create_issue_relationship` | `tools/issue_relationships.rs:47` | Link two issues |
| `delete_issue_relationship` | `tools/issue_relationships.rs:75` | Unlink two issues |
| `start_workspace` | `tools/task_attempts.rs:95` | Create workspace + start first session |
| `link_workspace_issue` | `tools/task_attempts.rs:227` | Link workspace to remote issue |
| `create_session` | `tools/sessions.rs:146` | Create session in workspace |
| `list_sessions` | `tools/sessions.rs:194` | List sessions for workspace |
| `update_session` | `tools/sessions.rs:225` | Rename session |
| `run_session_prompt` | `tools/sessions.rs:258` | Send prompt to session (expands `@tags`) |
| `get_execution` | `tools/sessions.rs:321` | Get execution status |

All tools are HTTP proxies: `send_json`/`send_empty_json` wrap `reqwest` calls against the local REST API and enforce the `{success, data, message}` envelope (`crates/mcp/src/task_server/tools/mod.rs:113-175`); failures surface as `CallToolResult::error` with serialized JSON (`crates/mcp/src/task_server/tools/mod.rs:98-111`).

## 6. Deployment crates

`crates/deployment` is the abstraction: it declares the async `Deployment` trait plus `DeploymentError` (`crates/deployment/src/lib.rs:1-80`), so server routes depend on behavior (container, git, events, config, remote, preview proxy, relay, worktree) rather than a concrete backend. `crates/local-deployment` is the sole production implementation (`LocalDeployment`, `crates/local-deployment/src/lib.rs:51-100`), composing `WorkspaceManager`, `WorktreeManager`, `LocalContainerService`, `GitService`, `PtyService`, `PreviewProxyService`, `RelayControl`/`RelayHosts`/WebRTC host, `RemoteClient`, analytics, and all services above; `DeploymentImpl` is aliased to it at server startup (`crates/server/src/main.rs:72`). Supporting modules `container.rs`, `pty.rs`, `command.rs`, `copy.rs` (`crates/local-deployment/src/`) implement local process/PTY execution and file copying. There is no remote-execution deployment in-tree; multi-host reachability is handled via relay/WebRTC and `remote_client`/`remote_sync` services instead.

## 7. Operational gotchas and concurrency

- `unwrap` on executor-action and script `Option`s will panic the task rather than return an error: `ctx.execution_process.executor_action().unwrap()` (`crates/services/src/services/container.rs:216`) and `first.cleanup_script.clone().unwrap()` / `repo.cleanup_script.clone().unwrap()` / archive/setup variants (`crates/services/src/services/container.rs:420-431,457-468,574-585`). Missing per-repo scripts must therefore be impossible by the time these run, or the process crashes.
- Lock/unlock discipline is `std::sync::Mutex` + `RwLock` `.unwrap()` on watcher and diff state (`crates/services/src/services/filesystem_watcher.rs:486-487,506-507`; `crates/services/src/services/diff_stream.rs:322-338,520-525,566-583,750-783`); a poisoned lock from a panicking thread will cascade into further panics.
- Serialization/path construction uses `.expect(...)` in event-patch builders (`crates/services/src/services/events/patches.rs:28-41,50-82,107-118`); malformed UUIDs/paths fail the whole patch.
- Only one FIXME is registered in services: file-type capture deferred in the watcher (`crates/services/src/services/filesystem_watcher.rs:149`).
- SQLite runs in `Delete` journal mode (`crates/db/src/lib.rs:83`); concurrent writers block. The 64-connection migration pool (`crates/db/src/lib.rs:98-102`) helps reads, not write parallelism.
- Port handling trims ANSI escapes before parsing (`crates/server/src/main.rs:99-104`) because npm-wrapped output can inject color codes; unparseable values silently fall back to port 0.
- Shutdown ordering: `CancellationToken` cancels both servers, then `kill_all_running_processes` runs unconditionally with `.expect` (`crates/server/src/main.rs:236-242`) — a stuck child can fail process exit.
- Analytics identity hashes `USER`/`HOME` (`crates/services/src/services/analytics.rs:163-168`); mismatched env in containers yields divergent user ids.

**Covers:** SQLite path and journal mode; 76-migration chain and Windows checksum branch; 16 DB models; 20+ service inventory; `Deployment` vs `LocalDeployment` split; `config.json`/`profiles.json`/`credentials.json` surface and v8 schema; full env-var table; dual-port Axum boot and temp-dir port file; npx-cli platform matrix and 3 commands; MCP stdio modes, context bootstrap, and 34-tool table; `unwrap`/`expect`/`FIXME` gotchas and `Delete`-mode + `RwLock`/`CancellationToken` concurrency notes.
