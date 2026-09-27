> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Executor Adapter Layer: One Interface, 10+ Coding Agents
**In one sentence:** Vibe Kanban supports nine production coding-agent CLIs plus one QA mock behind a single Rust trait (`StandardCodingAgentExecutor`), with per-agent adapter structs that build CLI commands, spawn process-group children, normalize heterogeneous JSON logs, and inject per-agent Model Context Protocol (MCP, a standard for exposing tools and servers to agents) configuration.

## Key points
- The adapter interface is `StandardCodingAgentExecutor` in `crates/executors/src/executors/mod.rs:220`, dispatched over the `CodingAgent` enum via `enum_dispatch` (`crates/executors/src/executors/mod.rs:94`).
- Nine production adapters plus one `qa-mode`-gated mock are enumerated in `CodingAgent` (`crates/executors/src/executors/mod.rs:109`): ClaudeCode, Amp, Gemini, Codex, Opencode, CursorAgent, QwenCode, Copilot, Droid, QaMock.
- Every adapter follows the same spawn path: `CommandBuilder::new(base).extend_params(...)` (`crates/executors/src/command.rs:66`), `into_resolved()` PATH lookup (`crates/executors/src/command.rs:34`), `ExecutionEnv::with_profile().apply_to_command()` (`crates/executors/src/env.rs:118`), `group_spawn_no_window()` (e.g. `crates/executors/src/executors/cursor.rs:214`).
- Consumers never construct adapters directly: `CodingAgentInitialRequest::spawn` resolves `ExecutorConfigs::get_cached().get_coding_agent(&profile_id)`, applies overrides, attaches approvals, then calls `agent.spawn()` (`crates/executors/src/actions/coding_agent_initial.rs:63`).
- Discovery is availability probing, not installation management: default `get_availability_info` checks `default_mcp_config_path().exists()` (`crates/executors/src/executors/mod.rs:275`), Claude/Codex overrides check `auth.json` mtime for `LoginDetected`, and `get_recommended_executor_profile` ranks `LoginDetected > InstallationFound` (`crates/executors/src/profile.rs:497`).
- Approvals and permission policy are two layers: the async `ExecutorApprovalService` trait (`crates/executors/src/approvals.rs:30`) injected via `use_approvals`, plus the `PermissionPolicy::{Auto, Supervised, Plan}` enum (`crates/executors/src/model_selector.rs:49`) mapped per adapter to CLI flags (`--yolo`, `--allow-all-tools`, `--dangerously-allow-all`, sandbox modes).
- Log streaming is normalization into `NormalizedEntry` patches on a `MsgStore`: each adapter implements `normalize_logs() -> Vec<JoinHandle<()>>` (`crates/executors/src/executors/mod.rs:260`), spawned by the container service per action type (`crates/services/src/services/container.rs:917`).

---
## 1. The trait and the enum
The entire layer is defined in `crates/executors/src/executors/mod.rs`. The crate root only re-exports modules (`crates/executors/src/lib.rs:1`).

Excerpt — trait definition (`crates/executors/src/executors/mod.rs:220-302`):
```rust
#[async_trait]
#[enum_dispatch(CodingAgent)]
pub trait StandardCodingAgentExecutor {
    fn apply_overrides(&mut self, _executor_config: &ExecutorConfig) {}

    fn use_approvals(&mut self, _approvals: Arc<dyn ExecutorApprovalService>) {}

    async fn spawn(
        &self,
        current_dir: &Path,
        prompt: &str,
        env: &ExecutionEnv,
    ) -> Result<SpawnedChild, ExecutorError>;

    /// Continue a session, optionally resetting to a specific message.
    async fn spawn_follow_up(
        &self,
        current_dir: &Path,
        prompt: &str,
        session_id: &str,
        reset_to_message_id: Option<&str>,
        env: &ExecutionEnv,
    ) -> Result<SpawnedChild, ExecutorError>;

    async fn spawn_review(
        &self,
        current_dir: &Path,
        prompt: &str,
        session_id: Option<&str>,
        env: &ExecutionEnv,
    ) -> Result<SpawnedChild, ExecutorError> {
        match session_id {
            Some(id) => {
                self.spawn_follow_up(current_dir, prompt, id, None, env)
                    .await
            }
            None => self.spawn(current_dir, prompt, env).await,
        }
    }

    fn normalize_logs(
        &self,
        _raw_logs_event_store: Arc<MsgStore>,
        _worktree_path: &Path,
    ) -> Vec<JoinHandle<()>> {
        vec![]
    }

    // MCP configuration methods
    fn default_mcp_config_path(&self) -> Option<std::path::PathBuf>;

    async fn get_setup_helper_action(&self) -> Result<ExecutorAction, ExecutorError> {
        Err(ExecutorError::SetupHelperNotSupported)
    }

    fn get_availability_info(&self) -> AvailabilityInfo {
        let config_files_found = self
            .default_mcp_config_path()
            .map(|path| path.exists())
            .unwrap_or(false);

        if config_files_found {
            AvailabilityInfo::InstallationFound
        } else {
            AvailabilityInfo::NotFound
        }
    }

    /// Returns a stream of executor discovered options updates.
    async fn discover_options(
        &self,
        _workdir: Option<&Path>,
        _repo_path: Option<&Path>,
    ) -> Result<BoxStream<'static, json_patch::Patch>, ExecutorError> {
        let options = crate::executor_discovery::ExecutorDiscoveredOptions::default();
        Ok(Box::pin(futures::stream::once(async move {
            patch::executor_discovered_options(options)
        })))
    }

    /// Returns the default overrides defined by this preset/variant.
    fn get_preset_options(&self) -> ExecutorConfig;
}
```

Excerpt — dispatch enum (`crates/executors/src/executors/mod.rs:94-124`):
```rust
#[enum_dispatch]
#[derive(
    Debug, Clone, Serialize, Deserialize, PartialEq, TS, Display, EnumDiscriminants, VariantNames,
)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
#[strum(serialize_all = "SCREAMING_SNAKE_CASE")]
#[strum_discriminants(
    name(BaseCodingAgent),
    // Only add Hash; Eq/PartialEq are already provided by EnumDiscriminants.
    derive(EnumString, Hash, strum_macros::Display, Serialize, Deserialize, TS, Type),
    strum(serialize_all = "SCREAMING_SNAKE_CASE"),
    ts(use_ts_enum),
    serde(rename_all = "SCREAMING_SNAKE_CASE"),
    sqlx(type_name = "TEXT", rename_all = "SCREAMING_SNAKE_CASE")
)]
pub enum CodingAgent {
    ClaudeCode,
    Amp,
    Gemini,
    Codex,
    Opencode,
    #[serde(alias = "CURSOR")]
    #[strum_discriminants(serde(alias = "CURSOR"))]
    #[strum_discriminants(strum(serialize = "CURSOR", serialize = "CURSOR_AGENT"))]
    CursorAgent,
    QwenCode,
    Copilot,
    Droid,
    #[cfg(feature = "qa-mode")]
    QaMock(QaMockExecutor),
}
```
The `EnumDiscriminants` derive generates `BaseCodingAgent` (`crates/executors/src/executors/mod.rs:100`), the serializable identity used in `ExecutorConfig.executor` (`crates/executors/src/profile.rs:128`) and `ExecutorProfileId` (`crates/executors/src/profile.rs:63`). `QaMock` is compiled only under `qa-mode` (`crates/executors/src/executors/mod.rs:42`). Sub-protocol helpers live in subdirectories `acp/`, `claude/`, `codex/`, `cursor/`, `droid/`, `opencode/` under `crates/executors/src/executors/`, declared in `crates/executors/src/executors/mod.rs:33`.

## 2. Agent-to-file-to-CLI mapping
Each adapter is a config struct plus a `StandardCodingAgentExecutor` impl in one file. Base commands are pinned npm package versions except `cursor-agent` and `droid`, which are expected as installed binaries.

| Agent (`BaseCodingAgent`) | Adapter file | Base command / transport |
|---|---|---|
| `CLAUDE_CODE` | `crates/executors/src/executors/claude.rs:120` (`ClaudeCode`) | `npx -y @anthropic-ai/claude-code@2.1.119` (`crates/executors/src/executors/claude.rs:61`); router variant `npx -y @musistudio/claude-code-router@1.0.66 code` selected by `claude_code_router` flag (`crates/executors/src/executors/claude.rs:61`) |
| `CODEX` | `crates/executors/src/executors/codex.rs:153` (`Codex`) | `npx -y @openai/codex@0.124.0 app-server` (`crates/executors/src/executors/codex.rs:447`); JSON-RPC app-server over stdio via `spawn_app_server` (`crates/executors/src/executors/codex.rs:640`) |
| `OPENCODE` | `crates/executors/src/executors/opencode.rs:46` (`Opencode`) | `npx -y opencode-ai@1.4.7 serve --hostname 127.0.0.1 --port 0` (`crates/executors/src/executors/opencode.rs:92`); spawns local HTTP server then drives sessions over SDK (`crates/executors/src/executors/opencode.rs:105`) |
| `GEMINI` | `crates/executors/src/executors/gemini.rs:32` (`Gemini`) | `npx -y @google/gemini-cli@0.29.3 --experimental-acp` (`crates/executors/src/executors/gemini.rs:49`); driven through shared `AcpAgentHarness` (`crates/executors/src/executors/gemini.rs:84`) |
| `COPILOT` | `crates/executors/src/executors/copilot.rs:27` (`Copilot`) | `npx -y @github/copilot@0.0.403 --acp` (`crates/executors/src/executors/copilot.rs:52`); driven through `AcpAgentHarness` (`crates/executors/src/executors/copilot.rs:107`) |
| `CURSOR_AGENT` | `crates/executors/src/executors/cursor.rs:42` (`CursorAgent`) | `cursor-agent -p --output-format=stream-json` (`crates/executors/src/executors/cursor.rs:140`) |
| `AMP` | `crates/executors/src/executors/amp.rs:22` (`Amp`) | `npx -y @sourcegraph/amp@latest --execute --stream-json` (`crates/executors/src/executors/amp.rs:37`); prompt fed via stdin then EOF (`crates/executors/src/executors/amp.rs:48`) |
| `DROID` | `crates/executors/src/executors/droid.rs:58` (`Droid`) | `droid exec --output-format stream-json` plus `--auto low|medium|high` or `--skip-permissions-unsafe` (`crates/executors/src/executors/droid.rs:88`) |
| `QWEN_CODE` | `crates/executors/src/executors/qwen.rs:26` (`QwenCode`) | `npx -y @qwen-code/qwen-code@0.9.1 --acp` (`crates/executors/src/executors/qwen.rs:45`); `AcpAgentHarness::with_session_namespace("qwen_sessions")` (`crates/executors/src/executors/qwen.rs:81`) |
| `QA_MOCK` (qa-mode only) | `crates/executors/src/executors/qa_mock.rs:32` (`QaMockExecutor`) | No CLI; emits Claude-JSON lines via `sh -c while read...sleep 1` (`crates/executors/src/executors/qa_mock.rs:38`) |

The user-facing list with install/auth links is `docs/supported-coding-agents.mdx:9` (ten cards: Claude Code, Codex, Copilot, Gemini, Amp, Cursor Agent CLI, OpenCode, Droid, Claude Code Router, Qwen Code). Claude Code Router is not a separate enum variant; it is the `claude_code_router` boolean on `ClaudeCode` switching `base_command()` (`crates/executors/src/executors/claude.rs:61`).

## 3. Spawn and consumption
`CommandBuilder` (`crates/executors/src/command.rs:66`) splits the base string with `shlex`/`winsplit` (`crates/executors/src/command.rs:162`), appends `params` and per-profile overrides via `apply_overrides` (`crates/executors/src/command.rs:179`), and resolves the binary with `resolve_executable_path` (`crates/executors/src/command.rs:34`). `ExecutionEnv` carries injected vars plus `RepoContext` and commit-reminder text (`crates/executors/src/env.rs:79`); profile env is merged with `with_profile` (`crates/executors/src/env.rs:118`) and applied with `apply_to_command` (`crates/executors/src/env.rs:127`). The canonical spawn tail is `group_spawn_no_window()` returning `SpawnedChild{child, exit_signal, cancel}` (`crates/executors/src/executors/mod.rs:323`).

Excerpt — consumer dispatch (`crates/executors/src/actions/coding_agent_initial.rs:48-77`):
```rust
    async fn spawn(
        &self,
        current_dir: &Path,
        approvals: Arc<dyn ExecutorApprovalService>,
        env: &ExecutionEnv,
    ) -> Result<SpawnedChild, ExecutorError> {
        let effective_dir = self.effective_dir(current_dir);

        #[cfg(feature = "qa-mode")]
        {
            tracing::info!("QA mode: using mock executor instead of real agent");
            let executor = crate::executors::qa_mock::QaMockExecutor;
            return executor.spawn(&effective_dir, &self.prompt, env).await;
        }

        #[cfg(not(feature = "qa-mode"))]
        {
            let profile_id = self.executor_config.profile_id();
            let mut agent = ExecutorConfigs::get_cached()
                .get_coding_agent(&profile_id)
                .ok_or(ExecutorError::UnknownExecutorType(profile_id.to_string()))?;

            if self.executor_config.has_overrides() {
                agent.apply_overrides(&self.executor_config);
            }
            agent.use_approvals(approvals.clone());

            agent.spawn(&effective_dir, &self.prompt, env).await
        }
    }
```
Follow-up (`crates/executors/src/actions/coding_agent_follow_up.rs:74`), review (`crates/executors/src/actions/review.rs:62`), and the `Executable` dispatcher over `ExecutorActionType` (`crates/executors/src/actions/mod.rs:74`) repeat this pattern. The container service resolves executors the same way for log normalization and pre-populates the worktree agent via `get_coding_agent_or_default` (`crates/services/src/services/container.rs:176`); follow-up/review normalization re-resolves per `executor_config.profile_id()` (`crates/services/src/services/container.rs:928`). HTTP routes expose profiles, availability, and discovered options through `ExecutorConfigs::get_cached()` (`crates/server/src/routes/config.rs:161`), with per-executor `discover_options` endpoints (`crates/server/src/routes/config.rs:572`). The special Codex login route applies `CmdOverrides` to the setup command (`crates/server/src/routes/workspaces/codex_setup.rs:82`).

## 4. Extension recipe (adding a new agent)
There is no dynamic plugin registry; a new agent is a new enum variant plus a new adapter module. Steps, each with its anchor:
1. Create `crates/executors/src/executors/<name>.rs` with a serde/TS/JsonSchema config struct holding `append_prompt: AppendPrompt`, model/permission fields, `#[serde(flatten)] cmd: CmdOverrides`, and a skipped `approvals` handle — see `Copilot` (`crates/executors/src/executors/copilot.rs:27`) or `QwenCode` (`crates/executors/src/executors/qwen.rs:26`).
2. Implement `StandardCodingAgentExecutor` (`crates/executors/src/executors/mod.rs:220`): `build_command_builder`, `spawn`, `spawn_follow_up`, `normalize_logs`, mandatory `default_mcp_config_path` (`crates/executors/src/executors/mod.rs:269`), `get_preset_options` (`crates/executors/src/executors/mod.rs:301`), and optionally `apply_overrides`, `use_approvals`, `discover_options`, `get_setup_helper_action`, `get_availability_info`.
3. Declare `pub mod <name>;` (`crates/executors/src/executors/mod.rs:33`), add the variant to `CodingAgent` (`crates/executors/src/executors/mod.rs:109`), extend `capabilities()` (`crates/executors/src/executors/mod.rs:177`), `get_mcp_config()` (`crates/executors/src/executors/mod.rs:127`), and the `preconfigured_mcp` adapter match (`crates/executors/src/mcp_config.rs:395`).
4. Add a `DEFAULT` entry in `crates/executors/default_profiles.json:2` (validated to require a `DEFAULT` per executor in `crates/executors/src/profile.rs:434`); user overrides merge on top (`crates/executors/src/profile.rs:336`).
5. If the CLI speaks Agent Client Protocol (ACP, a JSON-RPC protocol for driving agents over stdio), reuse `AcpAgentHarness` (`crates/executors/src/executors/acp/harness.rs:30`) instead of writing spawn/normalization from scratch, as Gemini/Copilot/Qwen do. Regenerate frontend types via `crates/server/src/bin/generate_types.rs:203`.

## 5. Discovery (which CLIs are installed)
`AvailabilityInfo::{LoginDetected, InstallationFound, NotFound}` is defined in `crates/executors/src/executors/mod.rs:203`, with `is_available()` true for the first two (`crates/executors/src/executors/mod.rs:212`). The default impl treats an existing MCP config file as installed (`crates/executors/src/executors/mod.rs:275`). Stronger checks are per-adapter: Claude inspects `~/.claude.json` mtime and returns `LoginDetected{last_auth_timestamp}` (`crates/executors/src/executors/claude.rs:601`); Codex checks `CODEX_HOME`/`~/.codex/auth.json` mtime, falling back to `config.toml` or `version.json` existence (`crates/executors/src/executors/codex.rs:261`); Cursor checks binary resolvability with `resolve_executable_path_blocking(Self::base_command())` plus `~/.cursor/mcp.json` (`crates/executors/src/executors/cursor.rs:615`); Gemini/Qwen/Copilot/Droid/Opencode/Amp check their config paths (`crates/executors/src/executors/gemini.rs:155`, `crates/executors/src/executors/qwen.rs:161`, `crates/executors/src/executors/copilot.rs:164`, `crates/executors/src/executors/droid.rs:202`, `crates/executors/src/executors/opencode.rs:472`, `crates/executors/src/executors/amp.rs:149`). `ExecutorConfigs::get_recommended_executor_profile` probes every cached profile and sorts `LoginDetected` (newest first) above `InstallationFound` (`crates/executors/src/profile.rs:497`). Capabilities advertising `SessionFork`, `SetupHelper`, `ContextUsage` are in `crates/executors/src/executors/mod.rs:58` and per-agent in `crates/executors/src/executors/mod.rs:177`; only Codex and Cursor declare `SetupHelper`, served through `get_setup_helper_action` (`crates/executors/src/executors/mod.rs:271`).

## 6. Approvals and permission policy
`ExecutorApprovalService` (`crates/executors/src/approvals.rs:30`) is the async backend for tool/question approvals (`create_tool_approval`, `wait_tool_approval`, `create_question_approval`, `wait_question_answer`), with an auto-approving `NoopExecutorApprovalService` (`crates/executors/src/approvals.rs:56`). Adapters receive it via `use_approvals` (`crates/executors/src/executors/mod.rs:225`); ACP adapters (Gemini, Qwen, Copilot) forward it into `harness.spawn_with_command(..., approvals)` (`crates/executors/src/executors/gemini.rs:84`), while Claude wires dedicated `AUTO_APPROVE_CALLBACK_ID`/`STOP_GIT_CHECK_CALLBACK_ID` clients (`crates/executors/src/executors/claude.rs:38`). Orthogonal to that, `PermissionPolicy::{Auto, Supervised, Plan}` (`crates/executors/src/model_selector.rs:49`) is the user-selectable policy carried in `ExecutorConfig.permission_policy` (`crates/executors/src/profile.rs:143`) and mapped in `apply_overrides`: Gemini/Qwen set `yolo` from `Auto` (`crates/executors/src/executors/gemini.rs:84`, `crates/executors/src/executors/qwen.rs:81`), Copilot sets `allow_all_tools` (`crates/executors/src/executors/copilot.rs:90`), Amp uses `dangerously_allow_all` (`crates/executors/src/executors/amp.rs:36`), Droid uses the five-level `Autonomy` enum defaulting to `SkipPermissionsUnsafe` (`crates/executors/src/executors/droid.rs:36`), Codex maps `sandbox` + `ask_for_approval` enums (`crates/executors/src/executors/codex.rs:66`) to `ThreadStartParams` (`crates/executors/src/executors/codex.rs:459`), and `default_profiles.json` pins permissive defaults (`dangerously_skip_permissions`, `dangerously_allow_all`, `yolo`, `danger-full-access`, `auto_approve`, `allow_all_tools`) (`crates/executors/default_profiles.json:3`).

## 7. Log streaming and normalization
Raw stdout/stderr chunks land in a `MsgStore`; each adapter spawns background tasks converting them to `NormalizedEntry` patches. The shared vocabulary (`UserMessage`, `ToolUse`, `CommandRun`, `Thinking`, `TokenUsageInfo`, `ErrorMessage`, `AskUserQuestion`, `TodoManagement`, etc.) is in `crates/executors/src/logs/mod.rs:71`. Container code spawns the normalizer per action on a temp store and collects `JoinHandle`s (`crates/services/src/services/container.rs:917`). Transports differ: Claude parses `--output-format stream-json` plus a 2s-gap stderr processor suppressing known warnings (`crates/executors/src/executors/claude.rs:54`); Codex normalizes app-server JSON-RPC events (`crates/executors/src/executors/codex/normalize_logs.rs:1` via `crates/executors/src/executors/codex.rs:249`); Opencode consumes server-sent events (`crates/executors/src/executors/opencode/normalize_logs.rs:1` via `crates/executors/src/executors/opencode.rs:439`); ACP agents share `acp/normalize_logs.rs`; Amp reuses `ClaudeLogProcessor` (`crates/executors/src/executors/amp.rs:127`); Cursor builds file/third-party diffs with `create_unified_diff` (`crates/executors/src/executors/cursor.rs:186`); Droid has its own `droid/normalize_logs.rs` (`crates/executors/src/executors/droid.rs:186`); QaMock reuses `ClaudeLogProcessor` (`crates/executors/src/executors/qa_mock.rs:92`). Generic stderr grouping is `normalize_stderr_logs` with a 2-second latency threshold (`crates/executors/src/logs/stderr_processor.rs:38`), and plain-text chunking is `PlainTextLogProcessor` (`crates/executors/src/logs/plain_text_processor.rs:1`). When an adapter needs to inject synthetic stdout (Opencode server mode, Codex app-server), it replaces the child stdout with an `os_pipe` writer via `create_stdout_pipe_writer` / `spawn_local_output_process` (`crates/executors/src/stdout_dup.rs:23`).

## 8. MCP config injection
`CodingAgent::get_mcp_config()` selects per-agent `servers_path`, JSON template, and TOML flag (`crates/executors/src/executors/mod.rs:127`): Codex uses `["mcp_servers"]` with TOML on, Amp uses `["amp.mcpServers"]`, Opencode uses `["mcp"]`, Droid and the default use `["mcpServers"]`. `preconfigured_mcp()` rewrites the canonical `default_mcp.json` servers (vibe-kanban, context7, playwright, exa, chrome-devtools) per agent shape (`crates/executors/src/mcp_config.rs:395`): passthrough for Claude/Amp/Droid, `httpUrl`+Accept-header rewrite for Gemini/Qwen (`crates/executors/src/mcp_config.rs:244`), url/headers flattening for Cursor (`crates/executors/src/mcp_config.rs:267`), stdio-only filtering for Codex (`crates/executors/src/mcp_config.rs:280`), `remote`/`local`+`enabled` rewriting for Opencode (`crates/executors/src/mcp_config.rs:291`), `tools:["*"]` injection for Copilot (`crates/executors/src/mcp_config.rs:356`). Read/write helpers handle JSON vs TOML vs comment-preserving JSONC (`crates/executors/src/mcp_config.rs:59`); per-agent config paths are listed in section 5. The workspace integration route demonstrates consumption: it resolves the agent and branches `CursorAgent` vs `Codex` for MCP setup (`crates/server/src/routes/workspaces/integration.rs:67`).

**Covers:** `crates/executors/src/executors/mod.rs`, `claude.rs`, `codex.rs`, `opencode.rs`, `gemini.rs`, `copilot.rs`, `cursor.rs`, `amp.rs`, `droid.rs`, `qwen.rs`, `qa_mock.rs`, `acp/harness.rs`, `command.rs`, `env.rs`, `profile.rs`, `approvals.rs`, `model_selector.rs`, `mcp_config.rs`, `executor_discovery.rs`, `logs/mod.rs`, `logs/stderr_processor.rs`, `stdout_dup.rs`, `actions/`, `default_profiles.json`, `docs/supported-coding-agents.mdx`, `crates/services/src/services/container.rs`, `crates/server/src/routes/config.rs` at commit `4deb7eca8f381f7cbc1f9d15515a9ab8f8009053`.
