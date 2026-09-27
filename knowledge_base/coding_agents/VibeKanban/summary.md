# Technical Analysis: vibe-kanban

**Repository:** https://github.com/BloopAI/vibe-kanban (commit 4deb7eca8f381f7cbc1f9d15515a9ab8f8009053, 2026-04-24)
**Version analyzed:** 0.1.44
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Vibe Kanban is a local-first kanban board for parallel coding-agent work: plan as issues on a board, execute each issue in an isolated git worktree (linked checkout sharing the repo object store) with its own agent run, review the diff in the UI, and merge via PR (proposed change sent for review). See [[wiki/01-overview-architecture|01-overview]].
It solves worktree sprawl (dozens of branches/checkouts per task), heterogeneous agent CLIs (each agent needs different flags/log formats), and prompt/diff context loss between planning and execution. One Rust `server` binary serves the TypeScript UI and runs agents; state persists in a single SQLite file (`db.v2.sqlite`); remote/cloud is a separate excluded crate plus relay tunnel crates.

## 2. High-Level Architecture (ASCII diagram with │ ▼ ─ ► connectors + 4-6 step data-flow narrative + where state lives)

```
Browser (local-web / web-core / ui) ─ HTTP /api ──► Axum server (server crate)
  │ SSE events + terminal WebSocket + diff WS                  │
  ▼                                                            ▼
Kanban board (issues, drag-drop) ──► workspaces ──► container service ──► git worktree + agent child process (PTY)
  │ bulk status writes              │ branch + container dir   │ spawn/normalize/stream              │ stdout/stderr ─► MsgStore ─► UI
  ▼                                 ▼                          ▼                                     ▼
remote Postgres (issues/PRs)    SQLite db.v2.sqlite     preview-proxy (separate port) ──► dev-server process ──► iframe
relay tunnel (remote browser) ◄── port file + config.json/profiles.json/credentials.json
```

Data flow (6 steps):

1. Launch: `npx vibe-kanban` ► `npx-cli/src/cli.ts:1` downloads/starts the `server` binary; server binds main + preview-proxy listeners (`crates/server/src/main.rs:117`).
2. UI load: browser fetches HTTP API + SSE event bus + terminal/diff WebSockets; routes nested in `crates/server/src/routes/mod.rs:36-80`.
3. Plan: user creates issue (remote Postgres row with `status_id` FK) and workspace (local row + branch + container dir); linkage is nullable `workspaces.issue_id` (`crates/remote/migrations/20260112000000_remote-projects.sql:246`).
4. Execute: container service spawns the selected agent CLI in the worktree with PTY; per-adapter `normalize_logs()` converts heterogeneous JSON logs to `NormalizedEntry` patches on a `MsgStore` (`crates/services/src/services/container.rs:917`).
5. Review/ship: diff computed worktree-vs-base-commit (`crates/git/src/lib.rs:327-353`), streamed over `GET /diff/ws`; PR created by push-then-`gh pr create` (`crates/server/src/routes/workspaces/pr.rs:188-388`); 60s `pr_monitor` polls merge state.
6. Preview: dev-server script runs as `run_reason='devserver'` process; framework-printed `localhost:PORT` is scraped from logs and loaded via subdomain proxy `{devPort}.localhost:{proxyPort}`.

State lives in three places: durable rows in `db.v2.sqlite` (local) + remote Postgres (issues/PRs/workspaces index); on-disk branches/worktree dirs (survive restart); ephemeral in-memory running children, PTY sessions, `MsgStore` streams, relay registrations (rebuilt or marked `failed` on boot; see [[wiki/03-workspaces-and-worktrees|03-workspaces]], [[wiki/07-persistence-config-and-ops|07-ops]]).

## 3. The Executor Adapter (`StandardCodingAgentExecutor`)

Representation: one Rust trait + one dispatch enum; each agent is a config struct plus a trait impl in one file under `crates/executors/src/executors/`. See [[wiki/02-executor-adapter-layer|02-executors]].
Named kinds/types with file:line:

- `StandardCodingAgentExecutor` trait — `crates/executors/src/executors/mod.rs:220` (`spawn`, `spawn_follow_up`, `spawn_review`, `normalize_logs`, `default_mcp_config_path`, `discover_options`, `get_preset_options`, `apply_overrides`, `use_approvals`).
- `CodingAgent` dispatch enum (`enum_dispatch`) — `crates/executors/src/executors/mod.rs:109`: `ClaudeCode, Amp, Gemini, Codex, Opencode, CursorAgent, QwenCode, Copilot, Droid, QaMock` (last `qa-mode`-gated).
- `BaseCodingAgent` discriminants — `crates/executors/src/executors/mod.rs:100` (serializable identity in `ExecutorConfig.executor`, `crates/executors/src/profile.rs:128`).
- `AvailabilityInfo::{LoginDetected, InstallationFound, NotFound}` — `crates/executors/src/executors/mod.rs:203`; `PermissionPolicy::{Auto, Supervised, Plan}` — `crates/executors/src/model_selector.rs:49`.
- `ExecutorActionType` dispatcher (`Executable`) — `crates/executors/src/actions/mod.rs:74` (initial / follow-up / review); `ExecutorApprovalService` trait — `crates/executors/src/approvals.rs:30`.
- `NormalizedEntry` vocabulary (`UserMessage, ToolUse, CommandRun, Thinking, TokenUsageInfo, …`) — `crates/executors/src/logs/mod.rs:71`.

Key query/traversal: consumers never construct adapters; `CodingAgentInitialRequest::spawn` resolves the cached profile, applies overrides, attaches approvals, then dispatches (`crates/executors/src/actions/coding_agent_initial.rs:63`):

```rust
let profile_id = self.executor_config.profile_id();
let mut agent = ExecutorConfigs::get_cached()
    .get_coding_agent(&profile_id)
    .ok_or(ExecutorError::UnknownExecutorType(profile_id.to_string()))?;
if self.executor_config.has_overrides() {
    agent.apply_overrides(&self.executor_config);
}
agent.use_approvals(approvals.clone());
agent.spawn(&effective_dir, &self.prompt, env).await
```

Knobs: per-profile `ExecutorConfig` overrides merged over `crates/executors/default_profiles.json:2` (a `DEFAULT` entry per executor is required, `crates/executors/src/profile.rs:434`); `PermissionPolicy` mapped per adapter to CLI flags (`--yolo`, `--allow-all-tools`, `--dangerously-allow-all`, sandbox modes); MCP config path/shape per agent via `get_mcp_config()` (`crates/executors/src/executors/mod.rs:127`) and `preconfigured_mcp()` (`crates/executors/src/mcp_config.rs:395`); availability probing with `get_recommended_executor_profile` ranking `LoginDetected > InstallationFound` (`crates/executors/src/profile.rs:497`).

## 4. LLM / External Service Integration (it does NOT call LLMs itself — agents are spawned CLIs; say so explicitly + how agents are invoked)

Vibe Kanban makes zero direct LLM (Large Language Model — the AI that writes code) API calls. All model traffic goes through third-party agent CLIs it spawns as child processes. Invocation chain per run: `CommandBuilder::new(base).extend_params(...)` (`crates/executors/src/command.rs:66`) → `into_resolved()` PATH lookup (`crates/executors/src/command.rs:34`) → `ExecutionEnv::with_profile().apply_to_command()` (`crates/executors/src/env.rs:118`) → `group_spawn_no_window()` (e.g. `crates/executors/src/executors/cursor.rs:214`). Transports differ: plain stream-JSON flags (Claude, Amp, Cursor, Droid), JSON-RPC app-server over stdio (Codex, `crates/executors/src/executors/codex.rs:640`), local HTTP server + SDK (Opencode, `crates/executors/src/executors/opencode.rs:92-105`), shared ACP harness (Agent Client Protocol — JSON-RPC stdio for driving agents; Gemini/Copilot/Qwen via `crates/executors/src/executors/acp/harness.rs:30`).
Adjacent external services: MCP (Model Context Protocol — standard for exposing tools to agents) config injection rewrites `default_mcp.json` per agent shape (`crates/executors/src/mcp_config.rs:395`); git hosting via `gh`/`az` CLI wrappers (`crates/git-host/src/github/cli.rs:225-261`); remote issue/PR sync via `RemoteClient` against `VK_SHARED_API_BASE` (`crates/services/src/services/remote_client.rs:725-736`); opt-in PostHog telemetry (`crates/services/src/services/analytics.rs:26-29`) and Sentry error reporting (`crates/utils/src/sentry.rs:30-33`); preview CDN load of Eruda at inject time (`crates/preview-proxy/src/lib.rs:603-618`).

## 5. The Task-to-PR Pipeline (issue -> workspace -> agent run -> diff review -> PR, with file:line per step)

1. Issue created/moved on board: `POST /v1/issues` + `POST /v1/issues/bulk` (`crates/remote/src/routes/issues.rs:34-49`); columns are per-project `project_statuses` rows, card position is `status_id + sort_order` (`crates/remote/migrations/20260112000000_remote-projects.sql:30-89`); frontend drag handler `handleDragEnd` (`packages/web-core/src/features/kanban/ui/KanbanContainer.tsx:658-750`). See [[wiki/04-kanban-issues-and-workflow|04-issues]].
2. Workspace created + linked: `POST /workspaces/start` → `create_and_start_workspace` (`crates/server/src/routes/workspaces/create.rs:212-320`); prompt pre-filled from issue title+description (`packages/web-core/src/pages/kanban/IssueWorkspacesSectionContainer.tsx:131-156`); one shared branch name `<shortuuid>-<slug>` (`crates/services/src/services/container.rs:786-795`) + one worktree per repo at `<container>/<repo.name>` (`crates/workspace-manager/src/workspace_manager.rs:290-371`).
3. Agent run: `start_execution` spawns setup script then `CodingAgentInitialRequest::spawn` (`crates/executors/src/actions/coding_agent_initial.rs:63`); logs normalized per adapter (`normalize_logs`, `crates/executors/src/executors/mod.rs:260`) and streamed from `MsgStore` (`crates/services/src/services/container.rs:917`); follow-ups/reviews re-resolve per `profile_id` (`crates/services/src/services/container.rs:928`).
4. Diff review: base commit resolved (`crates/git/src/lib.rs:709`), worktree diffed via temp-index `git diff --cached -M --name-status <base>` (`crates/git/src/cli.rs:168-228`), hydrated to `Diff` structs (`crates/git/src/lib.rs:327-353`), streamed on `GET /diff/ws` (`crates/server/src/routes/workspaces/git.rs:140`); inline comments are ephemeral frontend state (`packages/web-core/src/shared/hooks/useReview.ts:5-12`) serialized to a `## Review Comments (n)` markdown block prepended to the next prompt (`packages/web-core/src/shared/lib/promptMessage.ts:11-26`). See [[wiki/05-diff-review-and-pr-flow|05-review]].
5. PR + merge: `POST /workspaces/:id/pull-requests` pushes branch then `gh pr create` and stores a local PR row (`crates/server/src/routes/workspaces/pr.rs:188-388`); `pr_monitor` ticks every 60s and archives the workspace when no open PRs remain (`crates/services/src/services/pr_monitor.rs:68-211`); direct merge `POST /merge` is refused with an open PR (`crates/server/src/routes/workspaces/git.rs:195-213`); three issue automations (first-workspace → In progress, open-PR → In review, all-merged/local-merge → Done) run in `crates/remote/src/db/issues.rs:523-691`.
6. Preview (parallel): dev-server start kills existing dev servers, spawns one `run_reason='devserver'` process per repo with a script (`crates/server/src/routes/workspaces/execution.rs:37-137`); log-scraped port (`packages/web-core/src/shared/hooks/usePreviewUrl.ts:151-220`) loads through the subdomain proxy (`crates/preview-proxy/src/lib.rs:384-400`). See [[wiki/06-preview-browser-and-dev-server|06-preview]].

## 6. Key Files (table File | Lines | What It Does, 10-20 files by structural importance, line ranges)

| File | Lines | What It Does |
|---|---|---|
| `crates/server/src/main.rs` | 32-198 | Boot: TLS, asset dir, deployment build, orphan cleanup, dual-port bind, router, relay spawn, shutdown kill |
| `crates/server/src/routes/mod.rs` | 9-80 | Route assembly: relay-signed routes, `/api` group, frontend fallback, workspace/process/container/terminal routers |
| `crates/executors/src/executors/mod.rs` | 94-302 | `CodingAgent` enum + `StandardCodingAgentExecutor` trait + availability/capabilities |
| `crates/executors/src/actions/coding_agent_initial.rs` | 48-77 | Consumer spawn dispatch via cached executor profiles |
| `crates/services/src/services/container.rs` | 176-979 | Orchestrator: worktree lifecycle, spawn, log-stream tasks, orphan reaping, archive/delete |
| `crates/services/src/services/mod.rs` | 1-23 | 20+ service registrations behind `Deployment` trait |
| `crates/deployment/src/lib.rs` | 1-80 | `Deployment` async trait + error type (backend abstraction) |
| `crates/local-deployment/src/lib.rs` | 51-100 | `LocalDeployment`: sole production impl wiring all services |
| `crates/db/src/lib.rs` | 15-153 | SQLite URL, `Delete` journal mode, 76 migrations, pool constructors |
| `crates/db/src/models/` | `mod.rs:1-16` | 16 domains: task, workspace, session, execution_process + logs, repo, PR, merge, tags |
| `crates/workspace-manager/src/workspace_manager.rs` | 60-652 | Branch-per-workspace create/ensure/cleanup/move, legacy migration, orphan sweep |
| `crates/git/src/lib.rs` + `cli.rs` | `lib.rs:327-353`, `cli.rs:168-228` | Base-commit diff computation via temp index; branch/rebase/conflict ops |
| `crates/server/src/routes/workspaces/pr.rs` | 188-541 | PR create/attach/comments; push-then-`gh pr create` |
| `crates/preview-proxy/src/lib.rs` | 1-830 | Subdomain proxy, header strip, redirect/Next.js-RSC rewrites, script injection |
| `crates/remote/src/db/issues.rs` | 32-691 | `IssueWorkflowSignal` enum + three status-sync automations |
| `crates/mcp/src/task_server/` | `mod.rs:87-244`, `tools/mod.rs:51-204` | stdio MCP server, context bootstrap, 34 global / 7 orchestrator tools |
| `packages/web-core/src/features/kanban/ui/KanbanContainer.tsx` | 409-750 | Board columns, sort-order formula, drag-drop bulk updates |
| `packages/web-core/src/shared/hooks/ReviewProvider.tsx` + `useReview.ts` | `59-88`, `5-31` | Ephemeral inline comments → review markdown block |

## 7. Dependencies (table Package | Version constraint | Purpose, from Cargo.toml/package.json verbatim constraints)

Agent-CLI pins are verbatim from the adapter layer (only constraints quoted in the wiki pages):

| Package | Version constraint | Purpose |
|---|---|---|
| `@anthropic-ai/claude-code` | `2.1.119` (`claude.rs:61`) | Claude agent backend (`npx -y @anthropic-ai/claude-code@2.1.119`) |
| `@musistudio/claude-code-router` | `1.0.66` (`claude.rs:61`) | Router variant backend selected by `claude_code_router` flag |
| `@openai/codex` | `0.124.0` (`codex.rs:447`) | Codex app-server backend (`npx -y @openai/codex@0.124.0 app-server`) |
| `opencode-ai` | `1.4.7` (`opencode.rs:92`) | OpenCode local-server backend (`serve --hostname 127.0.0.1 --port 0`) |
| `@google/gemini-cli` | `0.29.3` (`gemini.rs:49`) | Gemini backend via ACP harness (`--experimental-acp`) |
| `@github/copilot` | `0.0.403` (`copilot.rs:52`) | Copilot backend via ACP harness (`--acp`) |
| `@qwen-code/qwen-code` | `0.9.1` (`qwen.rs:45`) | Qwen backend via ACP harness (`--acp`) |
| `@sourcegraph/amp` | `latest` (`amp.rs:37`) | Amp backend (`--execute --stream-json`, stdin prompt) |

Infra packages attested without verbatim versions in the wiki pages (constraints live in `Cargo.toml` / `package.json` — verify there): `tokio` (async runtime), `axum` (HTTP routers), `sqlx` + SQLite (persistence + migrations), `reqwest` (MCP-to-REST proxy), `rmcp` (stdio MCP server), `enum_dispatch` + `async-trait` (adapter dispatch), `react` + `vite` + `@hello-pangea/dnd` (kanban UI), `@pierre/diffs` (diff viewer), `cac` + `adm-zip` (npx-cli commands/binary install), `gh`/`az` external CLIs (git hosting, not npm).

## 8. CLI / Usage Surface (entry points, commands block, env table, config table)

Entry points: `npx vibe-kanban` → `package.json:5` → `npx-cli/src/cli.ts:1`; server binary `crates/server/src/main.rs:32`; MCP binary `crates/mcp/src/bin/vibe_kanban_mcp.rs:23-50`; standalone `review` CLI (`crates/review/src/main.rs:133-260`, PR-URL-to-narrative — not the in-app review); Tauri desktop shell `crates/tauri-app/src/main.rs:1`.

```sh
npx vibe-kanban [--desktop]      # launch app (browser or Tauri bundle)
npx vibe-kanban mcp [...args]    # spawn vibe-kanban-mcp (default --mode global)
npx vibe-kanban review [...args] # passthrough to vibe-kanban-review
node bin/cli.js --mcp ...        # legacy flag, normalized to mcp subcommand
```

Env (selected): `RUST_LOG` (default `info`); `BACKEND_PORT`/`PORT` (default `0`, OS-assigned); `PREVIEW_PROXY_PORT` (default `0`); `HOST` (default `127.0.0.1`); `VK_ALLOWED_ORIGINS`; `VIBE_BACKEND_URL` / `MCP_HOST` / `MCP_PORT` (MCP target); `VK_SHARED_API_BASE` (default `https://api.vibekanban.com`); `POSTHOG_API_KEY`/`POSTHOG_API_ENDPOINT`; `SENTRY_DSN`/`SENTRY_DSN_REMOTE`; `DISABLE_WORKTREE_CLEANUP`; `VIBE_KANBAN_DEBUG`; `CODEX_HOME`; `XDG_CONFIG_HOME`; `SHELL`. Full read sites in [[wiki/07-persistence-config-and-ops|07-ops]] §3.

Config (file JSON under asset dir — release: `~/Library/Application Support/ai.bloop.vibe-kanban` macOS, `~/.local/share/vibe-kanban` Linux; debug: `<repo>/dev_assets`): `config.json` (v8 schema: theme, notifications, editor, GitHub, UI language, PR/commit prompts), `profiles.json` (executor profiles), `credentials.json` (secrets); load is silent-default fallback (`crates/services/src/services/config/mod.rs:53-63`).

## 9. Extensibility Points (how to add an agent, a tool, a route — file:line each)

- Add an agent (no plugin registry — new enum variant + module): create `crates/executors/src/executors/<name>.rs` (model after `copilot.rs:27`/`qwen.rs:26`); implement `StandardCodingAgentExecutor` (`crates/executors/src/executors/mod.rs:220`); declare `pub mod <name>` (`mod.rs:33`), extend `CodingAgent` (`mod.rs:109`), `capabilities()` (`mod.rs:177`), `get_mcp_config()` (`mod.rs:127`), `preconfigured_mcp` match (`crates/executors/src/mcp_config.rs:395`); add `DEFAULT` entry in `crates/executors/default_profiles.json:2`; reuse `AcpAgentHarness` (`crates/executors/src/executors/acp/harness.rs:30`) for ACP-speaking CLIs; regenerate frontend types (`crates/server/src/bin/generate_types.rs:203`).
- Add an MCP tool: implement under `crates/mcp/src/task_server/tools/<domain>.rs` (e.g. `tools/sessions.rs:258` for `run_session_prompt`), register the router in `crates/mcp/src/task_server/tools/mod.rs:51-74`, proxy via `send_json`/`send_empty_json` against the REST envelope (`mod.rs:113-175`); orchestrator-mode set is test-pinned (`mod.rs:414-428`) — update the assertion if the tool belongs in orchestrator scope.
- Add a route: mount in the workspace router (`crates/server/src/routes/workspaces/mod.rs:24-61`) or preview router (`crates/server/src/routes/preview.rs:13-17`), implement the handler against the `Deployment` trait (not `LocalDeployment` directly) so alternate backends reuse it; shared request/row types go in `crates/api-types/src/lib.rs:1`.

## 10. Limitations and Gotchas (bullets, bold 3-6 word lead each; real gotchas incl. shutdown Apr 2026 community-maintained status)

- **Project shut down April 2026**: upstream BloopAI archived the repo; builds now come from community forks — pin commit `4deb7eca`, expect stale agent-CLI pins and no official relay backend.
- **Delete-mode SQLite serializes writers**: `JournalMode::Delete` (`crates/db/src/lib.rs:83`), not WAL — parallel agent runs share one writer; heavy concurrent writes block.
- **Restart kills running work**: every `status='running'` execution flips to `failed` on boot (`crates/services/src/services/container.rs:272-326`); dev servers and PTY terminals never auto-restart.
- **Terminals are non-persistent sockets**: fresh PTY per WebSocket, destroyed on close, no reattach (`crates/server/src/routes/terminal.rs:165`; map `crates/local-deployment/src/pty.rs:36-39`).
- **Review comments live only in browser**: no comment table/route; switching workspace or sending clears drafts (`ReviewProvider.tsx:44-46`; `SessionChatBoxContainer.tsx:514-516`) — unsent feedback is lost.
- **Status renames break automation**: syncs match literal names ("In progress", "In review", "Done"); renaming "Done" silently disables merge-to-Done (`crates/remote/src/db/issues.rs:523-599`).
- **`completed_at` never set by syncs**: Done-ness reads from the status name, so timestamp queries disagree with board position.
- **One stale PR pins the card**: Done requires *all* linked PRs merged (`crates/remote/src/db/issues.rs:534-542`).
- **Pinned agent versions rot fast**: adapters hard-pin npm versions (e.g. codex `0.124.0`, copilot `0.0.403`); upstream CLI changes break spawn/normalization until pins are bumped.
- **Hot-path `unwrap` panics tasks**: executor-action and script `Option`s unwrapped (`container.rs:216,420-431`); poisoned `Mutex`/`RwLock` cascades (`filesystem_watcher.rs:486-507`); Windows-only migration-checksum auto-fix diverges by platform (`crates/db/src/lib.rs:21-68`).
- **Dev ports are unreserved guesses**: no allocator; log-scraped detection requires the dev command to print its URL, and conflicts are manual `lsof` work (`usePreviewUrl.ts:151-220`).
- **Preview weakens framing guardrails**: proxy strips `CSP`/`X-Frame-Options` (`preview-proxy/src/lib.rs:77-86`); Eruda loads from `cdn.jsdelivr.net` (offline/CDN-compromise risk); `postMessage(command, '*')` trusts any holder.

## 11. How It Compares to Alternatives (3-4 REAL named alternatives: e.g. GitHub Copilot Workspaces, SWE-bench harnesses, OpenHands, AutoCodeRover/Claude Code Task system — 2-3 sentences each + 1-sentence positioning)

- **OpenHands (ex-OpenDevin):** an autonomous software-agent runtime with its own Docker sandbox, action/observation loop, and micro-agent Delegation — it *is* the agent, whereas Vibe Kanban is agent-agnostic scaffolding that shells to nine external CLIs and never calls a model. OpenHands optimizes single-task autonomy; Vibe Kanban optimizes parallel human-supervised task farming. Positioning: choose OpenHands for hands-off task solving, Vibe Kanban for running many agent CLIs side by side under one board.
- **SWE-bench harnesses (e.g. SWE-agent / R2E runners):** evaluation-first Docker harnesses that score patches against hidden tests with strict instance isolation — built for benchmarking, not interactive development. They lack kanban planning, live diff review, dev-server preview, and follow-up prompting. Positioning: harnesses measure agents; Vibe Kanban manages them day-to-day.
- **GitHub Copilot Workspaces:** a cloud task-to-PR planner tied to the Copilot model and GitHub flow (spec → plan → branch → PR), single-agent and single-vendor by design. Vibe Kanban is local-first, multi-agent (Claude/Codex/Gemini/Copilot/… behind one trait), and keeps data in local SQLite. Positioning: Copilot Workspaces for one-click GitHub-native drafting; Vibe Kanban for local multi-agent parallelism with model choice.
- **Claude Code Task system (Task tool / subagents):** a prompt-level fan-out inside one CLI session (background tasks, subagent teams) with no persistent board, no cross-CLI abstraction, and no preview proxy. Vibe Kanban persists every run as queryable rows, isolates each in its own worktree, and adds review-to-prompt feedback. Positioning: Claude Code tasks for in-session decomposition; Vibe Kanban when runs need durable identity, isolation, and review across agent vendors.

## Appendix: Selected Code Snippets (2-4 verbatim 10-30 line snippets with file:line)

Base-command pin with router variant (`crates/executors/src/executors/claude.rs:61`):

```rust
// crates/executors/src/executors/claude.rs:61
fn base_command(&self) -> String {
    if self.claude_code_router { "npx -y @musistudio/claude-code-router@1.0.66 code" }
    else { "npx -y @anthropic-ai/claude-code@2.1.119" }
}
```

Branch-name slug scheme (`crates/services/src/services/container.rs:786-795`):

```rust
async fn git_branch_from_workspace(&self, workspace_id: &Uuid, task_title: &str) -> String {
    let task_title_id = git_branch_id(task_title);
    let prefix = self.git_branch_prefix().await;
    if prefix.is_empty() {
        format!("{}-{}", short_uuid(workspace_id), task_title_id)
    } else {
        format!("{}/{}-{}", prefix, short_uuid(workspace_id), task_title_id)
    }
}
```

Worktree-vs-base diff hydration (`crates/git/src/lib.rs:327-353`, abbreviated):

```rust
pub fn get_diffs(
    &self,
    worktree_path: &Path,
    base_commit: &Commit,
    path_filter: Option<&[&str]>,
) -> Result<Vec<Diff>, GitServiceError> {
    // Use Git CLI to compute diff vs base to avoid sparse false deletions
    let repo = Repository::open(worktree_path)?;
    ...
    let entries = git
        .diff_status(worktree_path, base_commit, cli_opts)
        .map_err(|e| GitServiceError::InvalidRepository(format!("git diff failed: {e}")))?;
```

Review-markdown prepended to the next prompt (`packages/web-core/src/shared/lib/promptMessage.ts:11-26`):

```ts
export function buildAgentPrompt(
  rawUserMessage: string,
  contextParts: (string | null | undefined)[]
) {
  const trimmed = rawUserMessage.trim();
  const isSlashCommand = !!trimmed && isSlashCommandPrompt(trimmed);
  const parts = isSlashCommand
    ? [trimmed]
    : [...contextParts, rawUserMessage].filter(Boolean);
  return {
    prompt: parts.join('\n\n'),
    isSlashCommand,
  };
}
```
