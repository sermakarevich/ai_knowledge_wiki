# Technical Analysis: forgecode

**Repository:** https://github.com/tailcallhq/forgecode
**Version analyzed:** 0.1.0 (workspace-wide, `Cargo.toml`)
**Date:** 2026-04-25

---

## 1. Overview / What Problem It Solves

Coding-agent CLIs in 2026 are split into two camps. One camp (Claude Code, Codex, Gemini CLI) is vendor-controlled and hard-coupled to a single provider's billing and inference plane. The other camp (Aider, OpenCode, Continue) is open but typically thin — a single binary that wraps a single provider's HTTP API and a handful of file-system tools. Neither camp solves the operational reality of an engineer who pays for tokens across half a dozen vendors, who works inside a corporate proxy with custom TLS, and who lives at the ZSH prompt rather than in a separate REPL.

`forgecode` (binary name `forge`) is a Rust-native terminal coding agent built as a 24-crate workspace. It speaks to 30+ LLM providers through a single typed `Provider<T>` abstraction (`crates/forge_domain/src/provider.rs:237-251`), persists every conversation in a local SQLite database via Diesel (`crates/forge_repo/src/database/`), and ships three built-in agent personas (`forge`, `sage`, `muse`) loaded from YAML-frontmatter markdown bundled into the binary via `include_dir`. The defining design choice is the ZSH plugin path: instead of running as a separate REPL, `forge` installs a ZLE widget that intercepts `:` at the shell prompt, so `: explain this stack trace` is a first-class shell command alongside `cd` and `ls`. The primary user is a senior engineer or platform team — not a hobbyist — who wants pluggable providers, observable retry behavior, telemetry they can disable, and a build that is reproducible under Nix.

Forge also acts as an **MCP client** (not server) via the `rmcp 0.10.0` crate, so external MCP servers (Sentry, Slack, Notion, custom internal tooling) federate into the agent's tool list at runtime. This positions Forge as a "host" in the MCP ecosystem rather than yet another "server."

---

## 2. High-Level Architecture

```
Shell (ZSH widget)  ─── `: prompt`
       │                    │
       │ stdio              │
       ▼                    ▼
 forge_main (binary)  ──  CLI: clap subcommands
   reedline REPL,         (forge_main/src/cli.rs)
   spinner, syntax HL
       │
       ▼
 forge_api  (facade — wires all layers)
       │
       ├──► forge_app       (agent loop, turn management, dispatch)
       │
       ├──► forge_services  (file I/O, shell, grep, semantic search,
       │                     MCP tool invocation)
       │
       ├──► forge_repo      (Diesel/SQLite, LLM provider HTTP/SSE
       │                     clients, gRPC to workspace server,
       │                     YAML agent loader)
       │
       └──► forge_infra     (rmcp client, OAuth2, HTTP factory,
                             cacache disk cache)
       │
       ▼
 forge_domain  (zero-dependency core types: Agent, Conversation,
                Context, ChatRequest, ChatResponse, Provider,
                Tool, Skill, LifecycleEvent, Error)
```

State persistence: SQLite at `~/.forge/<db-file>` for conversations, history, and credentials; cacache at `~/.forge/cache/` for HTTP and provider model lists; `~/.forge/.forge.toml` for global config and `forge.yaml` / `.forge.yaml` for per-project config.

**Data flow from "user types `: fix this bug`" to "tool result returned":**

1. The ZSH ZLE widget captures the buffer when `:` is the first character and pipes it to `forge --piped-input` (`crates/forge_main/src/main.rs:91-97`). For interactive REPL mode, the equivalent path is `Console::prompt` → `ForgeCommandManager::parse` (`crates/forge_main/src/model.rs:285-394`), which strips `/` or `:` and dispatches via `ClapCmd::try_parse_from` to the same clap tree used by top-level `forge` subcommands.
2. The parsed `AppCommand` (`forge_main/src/model.rs`) lands in `UI::on_command` (`crates/forge_main/src/ui.rs:1976`). A free-text prompt becomes `AppCommand::Message`, which calls `UI::on_chat(chat: ChatRequest)` (`ui.rs:3780`).
3. `self.api.chat(chat)` returns a `ResultStream<ChatResponse>` (typed in `crates/forge_domain/src/error.rs:108-112`). Inside `forge_app`, the agent loop builds a `Context` (`crates/forge_domain/src/context.rs:399-433`) from the conversation messages plus tools resolved through `forge_services`, then calls `ChatRepository::chat` (`crates/forge_domain/src/repo.rs:90-96`) on the provider client.
4. The provider client (`forge_repo`) opens a Server-Sent Events stream via `reqwest-eventsource`, decodes each chunk into `ChatCompletionMessage` (`crates/forge_domain/src/message.rs:79-90`), and forwards it. When a `ToolCall` finishes streaming, the agent loop dispatches to `forge_services` and folds the `ToolResult` back as a new `ContextMessage::Tool` for the next turn.
5. The UI layer renders each `ChatResponse` variant — `TaskMessage`, `ToolCallStart`, `ToolCallEnd`, `RetryAttempt` — through `StreamingWriter` (`crates/forge_main/src/stream_renderer.rs:98`), which interleaves the spinner and markdown output by pausing the spinner before each write and only resuming on `\n` (`stream_renderer.rs:199-221`).
6. After completion, `forge_repo`'s `ConversationRepository::upsert_conversation` (`crates/forge_domain/src/repo.rs:41-87`) writes the updated `Conversation` to SQLite, and a fire-and-forget `tokio::spawn` posts a usage event to PostHog through `forge_tracker` (`crates/forge_main/src/tracker.rs:8`).

---

## 3. The Domain Core (`forge_domain`)

The `forge_domain` crate is the zero-dependency leaf that every other crate links to. It holds the types and traits, no I/O. The public surface is a flat namespace produced by `pub use foo::*;` for every module declared in `crates/forge_domain/src/lib.rs:1-121`.

**Central abstractions:**

| Type | File | Role |
|------|------|------|
| `Agent` | `agent.rs:104-155` | Persona: `id`, `provider`, `model`, `system_prompt`, `tools`, `compact`, reasoning/temperature knobs |
| `AgentId` | `agent.rs:17` | `Cow<'static, str>` newtype with constants `FORGE`, `MUSE`, `SAGE` |
| `Conversation` | `conversation.rs:44-50` | `id`, `title`, `context`, `metrics`, `metadata` — what is persisted |
| `Context` | `context.rs:399-433` | The actual LLM request: `messages`, `tools`, `tool_choice`, `reasoning`, sampling params |
| `ContextMessage` | `context.rs:41-45` | Enum: `Text(TextMessage)`, `Tool(ToolResult)`, `Image(Image)` |
| `MessageEntry` | `context.rs:368-375` | `{ message: ContextMessage, usage: Option<Usage> }`, with `Deref` to message |
| `ChatRequest` | `chat_request.rs:5-11` | `{ event: Event, conversation_id: ConversationId }` |
| `ChatResponse` | `chat_response.rs:55-75` | Streaming output: `TaskMessage`, `ToolCallStart`, `ToolCallEnd`, `RetryAttempt`, `Interrupt` |
| `ChatCompletionMessage` | `message.rs:79-90` | One streamed chunk |
| `ChatCompletionMessageFull` | `message.rs:222-232` | Assembled full message after stream |
| `Provider<T>` | `provider.rs:237-251` | Generic over URL type (runtime `Url` vs config `Template<URLParameters>`) |
| `ProviderId` | `provider.rs:28-44` | `Cow<'static, str>` newtype with 30+ built-in constants |
| `Skill` | `skill.rs:7-22` | A reusable named prompt template (the SKILL.md pattern) |
| `LifecycleEvent` | `hook.rs:99-118` | Enum of six lifecycle hooks (Start/End/Request/Response/ToolcallStart/ToolcallEnd) |
| `Compact` | `compact.rs` (re-exported, file not in fetched snapshot) | Compaction policy — fields `token_threshold`, `token_threshold_percentage`, `model` are reachable via `Agent.compact.*` (`agent.rs:231-295`) |

**Token accounting** uses a discriminated union (`context.rs:747-805`):

```rust
pub enum TokenCount {
    Actual(usize),    // from provider billing metadata
    Approx(usize),    // chars/4 heuristic
}
```

This lets the same context-window math operate on real provider numbers when available and fall back to a heuristic before the first response arrives. `Usage::merge` (`message.rs:25-80`) is max-wins — Anthropic streams cumulative usage on every chunk, so naive accumulation would multi-count. `Usage::accumulate` is sum, used for cross-request session totals. The two strategies live side-by-side and callers must pick correctly.

**Knobs:** `ReasoningConfig { effort: Effort, enabled, exclude, token_budget }` (`agent.rs`), with `Effort` ∈ {`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`} — seven discrete steps. `Compact { token_threshold, token_threshold_percentage, model }` — `compaction_threshold()` (`agent.rs:231-295`) computes `min(configured_threshold, context_window * percentage)` so headroom for tool outputs is always preserved. `TextMessage.droppable: bool` (`context.rs:313-315`) flags messages (e.g. attachment file dumps) that compaction may evict.

---

## 4. LLM / External Service Integration

Forge is itself the LLM client; the LLM is the remote service. The provider abstraction is `Provider<T>` (`crates/forge_domain/src/provider.rs:237-251`) with the `T` parameter discriminating two phases — `Provider<Url>` after URL templating, `Provider<Template<URLParameters>>` while loading config from disk. The `AnyProvider` enum (`provider.rs:283-286`) unifies both for listing.

**`ProviderResponseType` enum** (referenced by `forge.schema.json` and used in `forge_repo` to pick the wire decoder): `OpenAI`, `OpenAIResponses`, `Anthropic`, `Bedrock`, `Google`, `OpenCode`. Most of the 30+ supported "providers" are routing labels that map onto one of these six wire formats — e.g. Groq, Cerebras, x.ai, Requesty, OpenRouter all collapse to `OpenAI`-format SSE.

**Built-in `ProviderId` constants** (`provider.rs:46-80`): `FORGE`, `OPENAI`, `ANTHROPIC`, `AZURE`, `BEDROCK`, `VERTEX_AI`, `OPEN_ROUTER`, plus 23 more. The corresponding env vars (documented in `README.md`) include `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `XAI_API_KEY`, `ZAI_API_KEY`, `CEREBRAS_API_KEY`, `IO_INTELLIGENCE_API_KEY`, `REQUESTY_API_KEY`, `FORGE_API_KEY`. Auth methods extend beyond API keys: `aws-config 1.8.13` with SSO support for Bedrock, `google-cloud-auth 1.8.0` for Vertex token refresh, and `tiny_http` for the OAuth2 device-flow callback during `forge provider login` (`crates/forge_main/src/oauth_callback.rs`).

**Streaming.** All chat calls return `ResultStream<ChatCompletionMessage>` (`error.rs:108-112`), a `Pin<Box<dyn Stream<Item=Result<A,E>> + Send>>`. Wire decoding happens through `reqwest-eventsource 0.6.0` + `eventsource-stream 0.2.3`. The `async-openai 0.34.0` crate is pulled in only for its **type definitions** (`response-types` feature) — the HTTP client is not used.

**MCP.** `rmcp 0.10.0` with feature flags `client`, `transport-sse-client-reqwest`, `transport-child-process`, `transport-streamable-http-client-reqwest`, `auth`. Forge runs MCP servers as child processes (stdio) or connects over SSE / streaming HTTP. There is **no embedded MCP server** in this codebase — the surface advertised in `README.md` (`forge mcp import / list / show / remove / reload`) is purely client-side.

**Workspace server.** `forge_repo` depends on `tonic 0.14.5 + prost`, meaning the semantic-search/indexing service at `https://api.forgecode.dev` is gRPC, not REST. Override via `FORGE_WORKSPACE_SERVER_URL`. Self-hosting is therefore non-trivial — you need the `.proto` definitions and a compatible server, neither of which is in this repo.

**Reasoning / thinking.** Exposed as the `:reasoning-effort` REPL command and `forge config reasoning-effort` CLI. The seven `Effort` levels (`agent.rs`) are translated per provider — the precise mapping lives in the `forge_repo` provider clients (not in the snapshot).

---

## 5. The CLI / REPL Pipeline

The pipeline from keystroke to LLM response is layered across `forge_main` modules. Names below cite real files and line ranges from the source.

**Step 0 — Process setup.** `main.rs:47-129` is a thin shell. It enables ANSI on Windows, installs `rustls::crypto::ring` as the default TLS provider, registers a panic hook that posts a blocking telemetry event before exit, parses `Cli` (`cli.rs:15`), reads `forge.yaml` via `ForgeConfig::read`, and constructs a `UI` with `ForgeAPI::init` injected as a closure factory:

```rust
// main.rs:121-126
let mut ui = UI::init(cli, config, move |config| {
    ForgeAPI::init(cwd.clone(), config)
})?;
ui.run().await;
```

**Step 1 — UI bootstrap.** `UI::init` (`ui.rs:229-251`) stores the factory `F: Fn(ForgeConfig) -> A` as `Arc<F>` under `self.new_api`, so the `:new` REPL command can rebuild the API with a freshly reloaded config. The `SharedSpinner<P>` (`stream_renderer.rs:17`) is created here with the API as the console writer.

**Step 2 — Event loop.** `UI::run_inner` (`ui.rs:309-395`) branches three ways: subcommand → `handle_subcommands`; one-shot prompt or piped stdin → single `on_message` and exit; otherwise enter the REPL loop. Each loop iteration races command execution against Ctrl-C via `tokio::select!`:

```rust
// ui.rs:329-378 (extract)
loop {
    match command {
        Ok(command) => {
            tokio::select! {
                _ = tokio::signal::ctrl_c() => { self.spinner.reset(); }
                result = self.on_command(command) => {
                    match result {
                        Ok(exit) => if exit { return Ok(()) },
                        Err(error) => {
                            tracker::error(&error);
                            self.spinner.stop(None)?;
                            self.writeln_to_stderr(...)?;
                        }
                    }
                }
            }
        }
        ...
    }
    command = self.prompt().await;
}
```

**Step 3 — Command parsing.** `Console::prompt` (`input.rs:30`) calls `ForgeEditor::prompt` which delegates to `Reedline::read_line`, then hands the raw text to `ForgeCommandManager::parse` (`model.rs:285-394`). The parser is unusual: REPL `:` and `/` commands are dispatched through the **same clap tree** as the top-level binary subcommands, so `:model` and `forge model ...` share definitions. The fallthrough handles three cases — `agent-<name>` switch, registered workflow command, raw `Message`.

**Step 4 — Streaming chat.** `UI::on_chat` (`ui.rs:3780-3803`) consumes `Stream<ChatResponse>` and dispatches each item through `handle_chat_response` (`ui.rs:3902`). Tool-call start uses a `Notify`-based RAII guard so the tool name is always printed before tool stdout, even on writer errors:

```rust
// ui.rs:3924-3947
ChatResponse::ToolCallStart { tool_call, notifier } => {
    struct NotifyGuard<'a>(&'a tokio::sync::Notify);
    impl<'a> Drop for NotifyGuard<'a> {
        fn drop(&mut self) { self.0.notify_one(); }
    }
    let _guard = NotifyGuard(&notifier);
    writer.finish()?;
    if tool_call.requires_stdout() {
        self.spinner.stop(None)?;
    }
    drop(_guard);
}
```

**Step 5 — Output rendering.** `StreamingWriter` (`stream_renderer.rs:98`) wraps a `StreamdownRenderer` from `forge_markdown_stream`. The inner `StreamDirectWriter::write` (`stream_renderer.rs:199-221`) pauses the spinner, writes styled bytes, and only resumes the spinner if the buffer ended with `\n` — preventing the spinner from drawing mid-line over partial output. The terminal width is read fresh each frame; markdown is rendered through `termimad 0.34.1` and code via `syntect 5`.

**Step 6 — Cache hydration.** Concurrent with the prompt being shown, `hydrate_caches` (`ui.rs:397-409`) fires four `tokio::spawn` tasks to warm the model list, tool list, agent infos, and channel info, so the first user command finds them ready.

---

## 6. Key Files

| File | Lines (approx.) | What It Does |
|------|----------------:|--------------|
| `crates/forge_main/src/ui.rs` | 4974 | Central UI controller: every command handler, the REPL event loop, streaming response rendering |
| `crates/forge_main/src/cli.rs` | 1905 | All clap derive structs: `Cli` and every subcommand group (`AgentCommandGroup`, `ConversationCommandGroup`, `McpCommandGroup`, etc.) |
| `crates/forge_domain/src/context.rs` | 1754 | `Context`, `ContextMessage`, `TextMessage`, `MessageEntry`, `TokenCount`, `ResponseFormat` — the LLM-request shape |
| `crates/forge_main/src/model.rs` | 1673 | `AppCommand` enum + `ForgeCommandManager` — REPL slash/colon command parsing |
| `crates/forge_domain/src/result_stream_ext.rs` | 1260 | Async stream combinators on top of `tokio_stream` |
| `crates/forge_main/src/info.rs` | 1276 | Rich human-readable info display for `forge info` |
| `crates/forge_main/src/porcelain.rs` | 1248 | Machine-readable tabular output for scripting |
| `crates/forge_domain/src/hook.rs` | 1138 | Lifecycle hooks: `LifecycleEvent`, `EventData<P>`, `EventHandle<T>` trait + combinators |
| `crates/forge_domain/src/conversation_html.rs` | 831 | Static HTML rendering of a conversation for `forge conversation dump` |
| `crates/forge_domain/src/provider.rs` | 833 | `Provider<T>`, `ProviderId` (30+ constants), `AnyProvider`, `ProviderType`, `ModelSource<T>` |
| `crates/forge_domain/src/agent.rs` | 506 | `Agent`, `AgentId`, `AgentInfo`, `ReasoningConfig`, `Effort`, compaction-threshold logic |
| `crates/forge_domain/src/mcp.rs` | 624 | `McpServerConfig`, `McpStdioServer`, `McpHttpServer`, `McpOAuthSetting` |
| `crates/forge_domain/src/attachment.rs` | 568 | `Attachment`, `AttachmentContent`, `FileInfo`, `DirectoryEntry` |
| `crates/forge_domain/src/node.rs` | 508 | Code graph nodes for semantic search results |
| `crates/forge_main/src/oauth_callback.rs` | 526 | OAuth device-flow + code-flow callback (uses `tiny_http`) |
| `crates/forge_domain/src/message.rs` | 473 | `ChatCompletionMessage`, `ChatCompletionMessageFull`, `Usage`, `Content`, `FinishReason` |
| `crates/forge_domain/src/tool_order.rs` | 438 | Weighted/glob-pattern-based tool sorting |
| `crates/forge_domain/src/conversation.rs` | 360 | `Conversation`, `ConversationId`, `MetaData`, cost/token aggregation helpers |
| `forge.schema.json` | 28157 bytes | Authoritative JSON Schema for `forge.yaml` and `ForgeConfig` |
| `crates/forge_main/src/stream_renderer.rs` | 226 | `SharedSpinner` + `StreamingWriter` with spinner/markdown interleaving |

---

## 7. Dependencies

Drawn verbatim from `Cargo.toml [workspace.dependencies]`. Required runtime first; build/dev tools after.

| Package | Version | Purpose |
|---------|---------|---------|
| `tokio` | `1.51.0` | Async runtime (features: macros, rt-multi-thread, sync, time, fs, process, signal, io-util) |
| `anyhow` | `1.0.102` | Application-level error type |
| `thiserror` | `2.0.18` | Library-level typed errors (e.g. `forge_domain::Error`) |
| `reqwest` | `0.12.23` | HTTP client (json, rustls-tls, hickory-dns, http2) |
| `reqwest-eventsource` | `0.6.0` | SSE for streaming LLM responses |
| `eventsource-stream` | `0.2.3` | Lower-level SSE primitives |
| `async-openai` | `0.34.0` | OpenAI **types only** (response-types feature) — no client used |
| `aws-sdk-bedrockruntime` | `1.129.0` | Bedrock LLM API (signed AWS calls) |
| `aws-config` | `1.8.13` | AWS auth (behavior-version-latest, sso) |
| `google-cloud-auth` | `1.8.0` | Vertex AI token refresh |
| `rmcp` | `0.10.0` | MCP client (sse, child-process, streamable-http, auth) |
| `tonic` | `0.14.5` | gRPC for workspace-server semantic search |
| `prost` / `prost-types` | (via Cargo.lock) | Protobuf for tonic |
| `diesel` | (via Cargo.lock, sqlite) | ORM for conversation persistence |
| `diesel_migrations` | (via Cargo.lock) | Schema migrations baked into binary |
| `cacache` | (via Cargo.lock) | On-disk content-addressable cache |
| `handlebars` | `6.4.0` | Prompt template engine |
| `schemars` | `1.2` | JSON Schema generation for tool definitions |
| `serde` / `serde_json` | `1.0.217` / `1.0.143` | Serialization |
| `serde_yml` | `0.0.12` | YAML for agents and `forge.yaml` |
| `gix` | `0.82` | Git operations (no `git2` libgit2 dependency) |
| `reedline` | `0.47.0` | Primary line editor (REPL) |
| `rustyline` | `18.0.0` | Secondary line editor (used by `forge_select`) |
| `clap` | `4.6.0` (derive) | CLI parsing |
| `clap_complete` | `4.6.0` | Shell completion generation |
| `nucleo` | `0.5.0` | Fuzzy matching |
| `fzf-wrapped` | `0.1.4` | External-fzf wrapper for picker UIs |
| `ignore` | `0.4.23` | gitignore-aware directory walk (used in `forge_walker`) |
| `grep-searcher` / `grep-regex` | `0.1.14` / `0.1.13` | Ripgrep search primitives |
| `similar` | `3.0` (inline) | Diff display |
| `termimad` | `0.34.1` | Markdown rendering |
| `syntect` | `5` | Syntax highlighting |
| `gray_matter` | `0.3.2` | YAML frontmatter parsing for agent and skill `.md` files |
| `posthog-rs` | `0.5.3` | Telemetry |
| `machineid-rs` | `1.2.4` | Hardware fingerprint for telemetry |
| `gh-workflow` | `0.8.1` | Programmatic GitHub Actions YAML generation (in `forge_ci`) |
| `toml_edit` | `0.25` (serde) | Config file mutation preserving formatting |
| `insta` | `1.47.2` (json, yaml) | Snapshot testing — set to auto-accept (see Limitations) |

**Release profile** (`Cargo.toml`): `lto = true`, `codegen-units = 1`, `opt-level = 3`, `strip = true` — maximally optimized, stripped binary.

---

## 8. CLI / Usage Surface

### Entry points

- Binary `forge` from crate `forge_main` (`flake.nix` `cargoBuildFlags = ["--bin" "forge"]`).
- Source: `crates/forge_main/src/main.rs:47-48`.
- Workspace member declared in `Cargo.toml [workspace.dependencies]`.

### Top-level invocations

```
forge                              # interactive REPL
forge -p "explain this dir"        # one-shot prompt → exit
forge -e '{...}'                   # dispatch a JSON event to the workflow
forge -C ./subdir                  # change directory before starting
forge --sandbox feature-x          # create an isolated git worktree + branch
forge --conversation file.json     # execute a conversation from JSON
forge --conversation-id <uuid>     # resume an existing conversation
forge --agent <id>                 # select agent for this session
echo "context" | forge -p "fix"    # piped stdin becomes context
```

### Subcommands (from `crates/forge_main/src/cli.rs:81-152`)

```
forge conversation list | resume <id> | new | dump <id> | compact <id>
                  | retry <id> | clone <id> | rename <id> <name>
                  | delete <id> | info <id> | stats <id> | show <id>
forge commit [--preview] [<extra-context>]
forge suggest "<natural language>"
forge provider login | logout
forge list provider | model | agent | tool --agent <id>
forge workspace sync | init | status | query <text>
forge mcp list | import | show | remove | reload
forge config <field> [<value>]      # subcommands defined in cli.rs:516
forge cmd ...                       # custom-command management (cli.rs:156)
forge data ...                      # data import/export (cli.rs:773)
forge vscode install                # cli.rs:808
forge update                        # self-update
forge zsh plugin | theme | doctor | rprompt | setup | keyboard | format
forge setup                         # alias for `zsh setup`
forge doctor                        # alias for `zsh doctor`
forge info | banner
```

### REPL `:` / `/` commands (parsed by `ForgeCommandManager::parse`, `model.rs:285`)

`:new`, `:conversation`, `:clone`, `:rename`, `:retry`, `:copy`, `:dump`, `:compact`, `:commit`, `:commit-preview`, `:suggest`, `:edit`, `:sage`, `:muse`, `:agent`, `:model`, `:config-model`, `:config-provider`, `:config-reasoning-effort`, `:config-commit-model`, `:config-suggest-model`, `:config-reload`, `:info`, `:config`, `:config-edit`, `:tools`, `:skill`, `:login`, `:logout`, `:sync`, `:workspace-init`, `:workspace-status`, `:workspace-info`, `:keyboard-shortcuts`, `:doctor`. Aliases: `:n`, `:c`, `:r`, `:d`, `:s`, `:m`, `:cm`, `:cr`, `:i`, `:t`, `:a`, `:ask`, `:plan`, `:p`, `:ed`, `:re`, `:rn`, `:cre`, `:ccm`, `:csm`, `:ce`. The `!` prefix executes a raw shell command (`model.rs:286-288`).

### Environment variables (selected — full list in `README.md`)

| Variable | Default | Purpose |
|----------|---------|---------|
| `FORGE_CONFIG` | `~/.forge` | Base config directory |
| `FORGE_API_URL` | `https://api.forgecode.dev` | ForgeCode services endpoint |
| `FORGE_WORKSPACE_SERVER_URL` | (api.forgecode.dev) | gRPC semantic-index server |
| `FORGE_BIN` | `forge` | Binary name for ZSH plugin |
| `FORGE_TRACKER` | `true` | `false` disables telemetry |
| `FORGE_LOG` | unset | Tracing filter (e.g. `forge=debug`) |
| `FORGE_RETRY_INITIAL_BACKOFF_MS` | `1000` | First retry delay |
| `FORGE_RETRY_BACKOFF_FACTOR` | `2` | Exponential factor |
| `FORGE_RETRY_MAX_ATTEMPTS` | `3` | Cap |
| `FORGE_RETRY_STATUS_CODES` | `429,500,502,503,504` | Retriable HTTP statuses |
| `FORGE_HTTP_CONNECT_TIMEOUT` | `30s` | Connect timeout |
| `FORGE_HTTP_READ_TIMEOUT` | `900s` | Body-read timeout |
| `FORGE_HTTP_TLS_BACKEND` | `default` | `rustls` to force |
| `FORGE_HTTP_ACCEPT_INVALID_CERTS` | `false` | **Disables TLS cert verification** — security risk |
| `FORGE_HTTP_ROOT_CERT_PATHS` | unset | Add custom root certs |
| `FORGE_TOOL_TIMEOUT` | `300s` | Per-tool execution cap |
| `FORGE_MAX_IMAGE_SIZE` | `10 MB` | Attachment cap |
| `FORGE_DUMP_AUTO_OPEN` | `false` | Auto-open dump HTML in browser |
| `FORGE_DEBUG_REQUESTS` | unset | Path to write HTTP debug files |
| `FORGE_MAX_SEARCH_RESULT_BYTES` | `10 KB` | Truncate grep results |
| `FORGE_MAX_LINE_LENGTH` | `2000` chars | Truncate long lines |
| `FORGE_SEM_SEARCH_LIMIT` | `200` | Semantic-search cap |
| `FORGE_SEM_SEARCH_TOP_K` | `20` | Semantic-search top-K |
| `FORGE_MAX_CONVERSATIONS` | `100` | Local conversation cap |
| `OPENAI_API_KEY` / `OPENAI_URL` | unset | OpenAI + compatibles (Groq, etc.) |
| `ANTHROPIC_API_KEY` | unset | Anthropic |
| `OPENROUTER_API_KEY` | unset | OpenRouter |
| `XAI_API_KEY` | unset | x.ai (Grok) |
| `ZAI_API_KEY` / `ZAI_CODING_API_KEY` | unset | z.ai |
| `CEREBRAS_API_KEY` | unset | Cerebras |
| `IO_INTELLIGENCE_API_KEY` | unset | IO Intelligence |
| `REQUESTY_API_KEY` | unset | Requesty |
| `FORGE_API_KEY` | unset | ForgeCode services |
| `_FORGE_CONVERSATION_ID` / `_FORGE_ACTIVE_AGENT` | injected | Set by ZSH plugin, read by `forge zsh rprompt` |

### Configuration files

| Path | Purpose |
|------|---------|
| `~/.forge/.forge.toml` | Global user config |
| `forge.yaml` or `.forge.yaml` (project root) | Project config — schema at `forge.schema.json` |
| `.mcp.json` (project) and `~/forge/.mcp.json` (global) | MCP server registry |
| `~/.forge/<sqlite>.db` | Conversation history |
| `~/.forge/cache/` | `cacache` HTTP / model-list cache |
| `~/.forge/agents/*.md` | Custom agents (YAML frontmatter + system prompt) |
| `~/.forge/skills/SKILL.md` | Custom skills |
| `~/.forge/commands/*.md` | Custom REPL commands |

---

## 9. Extensibility Points

- **Add a new LLM provider.** Edit the `forge.yaml` `providers:` array (schema in `forge.schema.json` `$defs.ProviderEntry`) — set `id`, `url` template (with `URLParameters` placeholders), `response_type` (one of `OpenAI` / `OpenAIResponses` / `Anthropic` / `Bedrock` / `Google` / `OpenCode`), and `auth_methods`. For native code-level support add a `ProviderId` constant in `crates/forge_domain/src/provider.rs:46-80` and a wire client in `crates/forge_repo/src/`.

- **Add a new agent.** Drop a `<name>.md` file with YAML frontmatter into `~/.forge/agents/` or commit it to the project under the project's agents directory. The frontmatter is parsed against the `Agent` struct at `crates/forge_domain/src/agent.rs:104-155` — set `provider`, `model`, `tools`, `system_prompt`, `compact`, `reasoning`. The body of the markdown becomes the system prompt template (Handlebars). Built-in `forge`, `sage`, `muse` are bundled at compile time via `include_dir`.

- **Add a new skill.** Create `SKILL.md` with frontmatter (`name`, `description`, optional `resources`) under `~/.forge/skills/` or per-project. Loaded via `SkillRepository::load_skills` (`crates/forge_domain/src/repo.rs:207-215`). The body is the prompt template; resources are file paths to embed.

- **Add a new tool.** Define a Rust struct in `forge_services` (or a new crate) and apply the macro from `forge_tool_macros` (a proc-macro crate at `crates/forge_tool_macros/`). The macro derives the JSON Schema (via `schemars`) used to describe the tool to the LLM. Wire the implementation into the service layer — exact registration site lives in `forge_services/src/` (not in the snapshot).

- **Federate an external MCP server.** Run `forge mcp import` with a JSON definition or edit `.mcp.json` directly. Three transports supported: stdio child-process, SSE, streamable HTTP. OAuth is supported via `rmcp`'s `auth` feature. Tool names from MCP servers are merged into the agent's tool list at session start.

- **Hook into lifecycle events.** Implement `EventHandle<T>` (`crates/forge_domain/src/hook.rs:125-135`) for one of the six `LifecycleEvent` payload types (`Start`, `End`, `Request`, `Response`, `ToolcallStart`, `ToolcallEnd`). Use `EventHandleExt::and` (`hook.rs:141-164`) to chain multiple handlers. The integration points are in `forge_app` (not in the snapshot).

- **Custom REPL command.** Drop a `<name>.md` file into `~/.forge/commands/`. The command becomes available as `:<name>` and falls through `ForgeCommandManager::parse` (`crates/forge_main/src/model.rs:285-394`) into `AppCommand::Custom(UserCommand::new(...))`.

---

## 10. Limitations and Gotchas

- **Self-hosting the workspace server is impractical.** The semantic-search/indexing service is reached over **gRPC** via `tonic` (`forge_repo` deps include `tonic 0.14.5` + `prost` + `tonic-prost-build`), and the `.proto` files are not vendored in this repo. Setting `FORGE_WORKSPACE_SERVER_URL` to point elsewhere requires an upstream-compatible gRPC server you cannot trivially build from this source.

- **Telemetry secret baked into the binary.** `POSTHOG_API_SECRET` is injected at compile time (visible in `Cross.toml` `passthrough` and the `flake.nix` build env). Anyone reverse-engineering the binary can extract the key. `FORGE_TRACKER=false` disables sending, but the key still ships.

- **Insta snapshot tests auto-accept everything.** `insta.yaml` sets both `auto_accept: true` and `auto_accept_unseen: true`. CI snapshot tests will never fail on changed output — they silently update and pass. This convenience tradeoff means snapshot regressions cannot be caught by the test suite.

- **`FORGE_HTTP_ACCEPT_INVALID_CERTS` is a documented, named env var.** Disabling TLS verification by env var is one `export` away. The README documents it explicitly with a security note, but its presence as a first-class flag (not a hidden debug toggle) signals corporate-MITM-proxy is an explicit deployment target.

- **Five domain modules are missing from publicly fetchable source.** `crates/forge_domain/src/lib.rs` declares `mod compact; mod tools; mod auth; mod policies; mod transformer;` but the corresponding files were not returned by the GitHub MCP fetch in this analysis. They are real modules (other files import from them — e.g. `Agent.compact: Compact`), so they exist somewhere; the directory layout may use subfolders not surfaced by the directory listing tool.

- **Reasoning level mapping is provider-specific and opaque.** `Effort` has seven values (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`) but the per-provider translation lives in `forge_repo` and is not visible from the domain layer. Setting `:reasoning-effort high` does not have a uniform meaning across OpenAI o-series, Anthropic extended thinking, and Google Gemini thinking — the mapping is buried.

- **No embedded MCP server.** Despite the strong MCP messaging in `README.md`, Forge is purely an MCP **client**. There is no way to expose `forge`'s own tools (file search, semantic index, conversation history) to other MCP-host applications. The `rmcp` features enabled are `client`, `transport-*-client-*`, `auth` — never `server`.

- **REPL and CLI share the clap tree, with non-obvious aliases.** `:` and `/` are equivalent prefixes (`model.rs:296-298`); `!cmd` is a shell escape; `agent-<name>` is a special fallthrough that doesn't match any clap subcommand. Unfamiliar users will hit confusing parser errors when these special cases collide.

- **Auto-accept-snapshot + auto-update.** `forge update` self-updates the binary by default (the `Update` config controls auto-frequency). Combined with auto-accepted CI snapshots, regressions can ship to user machines without any failing test catching them.

- **Two line-editor crates.** Both `reedline 0.47.0` (primary REPL) and `rustyline 18.0.0` (used inside `forge_select`) are workspace dependencies. Behaviour, keybindings, and history conventions differ between the two — bugs about cursor or history state often map to "which editor was active for this prompt".

- **Edition 2024 + Rust 1.92 minimum.** `rust-toolchain.toml` pins to 1.92 and `Cargo.toml` declares `edition = "2024"`. Both are leading-edge as of release; older toolchains in CI or contributors' environments will fail outright.

- **`.DS_Store` files in snapshot.** The repo dump shows operational sloppiness in places — multiple workspaces, generated `Cargo.lock` checked in (correct for a binary), but the bounty TypeScript scripts under `.github/scripts/bounty/` mix two languages and two test frameworks in one repository.

---

## 11. How It Compares to Alternatives

- **Claude Code (Anthropic).** Single-vendor terminal agent built on the Claude API. Tighter UX integration with Anthropic's billing, prompt caching, and managed subagents; no choice of provider, no SQLite-based local conversation store, no ZSH-prompt embedding. Forge trades vendor depth for vendor breadth — six wire formats, 30+ provider IDs, no proprietary inference plane.

- **OpenCode.** Go-based open-source agent CLI also targeting multi-provider use. Comparable scope (TUI, providers, MCP). OpenCode's plugin model is JavaScript/TypeScript via a shared runtime; Forge's is Rust at compile time plus YAML at config time. Forge's `OpenCode` wire format in `ProviderResponseType` suggests deliberate compatibility with OpenCode's HTTP shape.

- **Aider.** Python CLI focused on git-integrated edit loops. Smaller scope (no built-in MCP host, no agent personas, no semantic search server), simpler install (`pip install`), strong git diff/commit ergonomics. Forge ships AI-commit (`forge commit`) too, but Aider's edit loop is the product — Forge's is one feature among many.

- **Cursor / Continue.** IDE-embedded, not terminal-embedded. Different surface entirely: their value is inline diff suggestions and chat panels inside the editor. Forge's ZSH-prompt path is the inverse — the agent lives where shell commands live, not where source code is being edited.

- **Codex CLI (OpenAI).** Single-vendor like Claude Code. TypeScript runtime. Forge is faster to start (Rust binary, LTO + strip) and pluggable across vendors; Codex is tighter to OpenAI's reasoning models and Responses API.

**Positioning:** Forge is the maximalist multi-provider terminal coding agent — broad provider coverage, deep ZSH integration, MCP-host capability, local SQLite persistence, and a first-class config schema (`forge.schema.json`) — at the cost of carrying significantly more surface area, build-time complexity (Rust 1.92, gRPC, Diesel, libsqlite3), and seven-level reasoning knobs that don't translate cleanly across providers.

---

## Appendix: Selected Code Snippets

### A1. UI factory injection (`crates/forge_main/src/ui.rs:229-251`)

```rust
pub fn init(cli: Cli, config: ForgeConfig, f: F) -> Result<Self> {
    let api = Arc::new(f(config.clone()));
    let env = api.environment();
    let command = Arc::new(ForgeCommandManager::default());
    let spinner = SharedSpinner::new(SpinnerManager::new(api.clone()));
    Ok(Self {
        state: Default::default(),
        api,
        new_api: Arc::new(f),
        console: Console::new(env.clone(), config.custom_history_path.clone(), command.clone()),
        cli,
        command,
        spinner,
        markdown: MarkdownFormat::new(),
        config,
        _guard: forge_tracker::init_tracing(env.log_path(), TRACKER.clone())?,
    })
}
```

The factory `F: Fn(ForgeConfig) -> A` is stored as `Arc<F>` so `:new` can rebuild `api` from a freshly-read config without re-instantiating the whole UI.

### A2. The `Agent` domain struct (`crates/forge_domain/src/agent.rs:100-125`)

```rust
#[derive(Debug, Clone, PartialEq, Setters, Serialize, Deserialize, JsonSchema)]
#[setters(strip_option, into)]
pub struct Agent {
    pub id: AgentId,
    pub title: Option<String>,
    pub description: Option<String>,
    pub tool_supported: Option<bool>,
    pub path: Option<String>,
    pub provider: ProviderId,
    pub model: ModelId,
    pub system_prompt: Option<Template<SystemContext>>,
    pub user_prompt: Option<Template<EventContext>>,
    pub tools: Option<Vec<ToolName>>,
    pub max_turns: Option<u64>,
    pub compact: Compact,
    pub custom_rules: Option<String>,
    pub temperature: Option<Temperature>,
    pub top_p: Option<TopP>,
    pub top_k: Option<TopK>,
    pub max_tokens: Option<MaxTokens>,
    pub reasoning: Option<ReasoningConfig>,
    pub max_tool_failure_per_turn: Option<usize>,
    pub max_requests_per_turn: Option<usize>,
}
```

### A3. Compaction-threshold computation (`crates/forge_domain/src/agent.rs:231-295`, condensed)

```rust
pub fn compaction_threshold(mut self, selected_model: Option<&Model>) -> Self {
    const DEFAULT_CONTEXT_WINDOW: usize = 128_000;
    const DEFAULT_TOKEN_THRESHOLD: usize = 100_000;
    const DEFAULT_CONTEXT_WINDOW_PERCENTAGE: f64 = 0.7;

    let context_window = selected_model
        .and_then(|m| m.context_length)
        .and_then(|cw| usize::try_from(cw).ok())
        .unwrap_or(DEFAULT_CONTEXT_WINDOW);

    let configured_threshold = self.compact.token_threshold.unwrap_or(DEFAULT_TOKEN_THRESHOLD);
    let pct = self.compact.token_threshold_percentage
        .unwrap_or(DEFAULT_CONTEXT_WINDOW_PERCENTAGE);
    let context_threshold = ((context_window as f64) * pct).floor() as usize;

    self.compact.token_threshold = Some(configured_threshold.min(context_threshold));
    self
}
```

`min(configured, context_window * pct)` always preserves headroom for tool outputs, even when the user sets a high absolute threshold against a small-context model.

### A4. The streaming chat trait (`crates/forge_domain/src/repo.rs:90-96`)

```rust
#[async_trait::async_trait]
pub trait ChatRepository: Send + Sync {
    async fn chat(
        &self,
        model_id: &ModelId,
        context: Context,
        provider: Provider<Url>,
    ) -> ResultStream<ChatCompletionMessage, anyhow::Error>;
    async fn models(&self, provider: Provider<Url>) -> anyhow::Result<Vec<Model>>;
}
```

`ResultStream<A, E>` (`error.rs:108-112`) is `Result<Pin<Box<dyn Stream<Item=Result<A,E>> + Send>>, E>`, so the entire stream can fail at start (auth error) or mid-flight (token cutoff).

### A5. Spinner-aware byte writer (`crates/forge_main/src/stream_renderer.rs:199-221`)

```rust
impl<P: ConsoleWriter> io::Write for StreamDirectWriter<P> {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        self.pause_spinner();
        let content = match buf.to_str() {
            Ok(c) => Cow::Borrowed(c),
            Err(_) => buf.to_str_lossy(),
        };
        let styled = self.style.apply(content.into_owned());
        self.printer.write(styled.as_bytes())?;
        self.printer.flush()?;
        if buf.last() == Some(&b'\n') {
            self.resume_spinner();
        }
        Ok(buf.len())  // input length, not styled output length
    }
}
```

Two subtle properties: (1) the spinner only resumes at line boundaries, so it never overdraws partial markdown chunks; (2) the returned `usize` is the **input** length, not the ANSI-inflated output length, satisfying the `io::Write` contract that callers expect.

### A6. Lifecycle hook combinator (`crates/forge_domain/src/hook.rs:141-164`)

```rust
pub trait EventHandleExt<T: Send + Sync>: EventHandle<T> {
    fn and<H: EventHandle<T> + 'static>(self, other: H) -> Box<dyn EventHandle<T>>
    where Self: Sized + 'static;
}

impl<T: Send + Sync + 'static, A: EventHandle<T> + 'static> EventHandleExt<T> for A {
    fn and<H: EventHandle<T> + 'static>(self, other: H) -> Box<dyn EventHandle<T>>
    where Self: Sized + 'static {
        Box::new(CombinedHandler(Box::new(self), Box::new(other)))
    }
}
```

A blanket `impl` lets any `EventHandle` chain via `.and(other)`, producing a `Box<dyn EventHandle<T>>`. This is the pattern used to compose telemetry, logging, and audit handlers without a registry.
