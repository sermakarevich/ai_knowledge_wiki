# Technical Analysis: AgentSpace

**Repository:** https://github.com/HKUDS/AgentSpace
**Version analyzed:** 0.1.0 (workspace), 0.1.3 (daemon)
**Date:** 2026-06-22

---

## 1. Overview / What Problem It Solves

Most AI coding agent frameworks are single-user by design: one engineer, one terminal, one agent session. AgentSpace addresses the gap when agent work needs to cross organizational boundaries -- assigned to specific people, governed by permissions, tracked across multiple days, and audited after the fact. The primary users are engineering teams and operations teams who want to treat AI agents as persistent "digital employees" that belong to the organization rather than to a single developer's laptop.

The platform solves three concrete problems. First, agent execution is fragmented across incompatible CLIs (Claude Code, Codex, OpenClaw, Hermes, Gemini); AgentSpace's AgentRouter layer provides a single typed interface over all of them. Second, there is no shared context store -- attachments, channel history, knowledge base pages, and Google Workspace documents scatter across personal drives; AgentSpace centralizes these into a PostgreSQL-backed workspace accessible to both humans and agents. Third, approval workflows and permission governance are absent from vanilla agent frameworks; AgentSpace adds a multi-tenant approval queue with a full audit trail of tool calls and decisions.

---

## 2. High-Level Architecture

```
  Browser / CLI Client
         │
         ▼
  ┌──────────────────────────────────────────┐
  │  apps/web  (Next.js 16 App Router)       │
  │  apps/cli  (Node --experimental-strip-types) │
  └────────────┬─────────────────────────────┘
               │
               ▼
  ┌────────────────────────────┐
  │  @agent-space/services     │  business logic layer
  └──┬──────────┬──────────────┘
     │          │
     ▼          ▼
  @agent-space/db         Task Queue / Approval Queue
  (PostgreSQL 16)                   │
                                    ▼
                         agent-space-daemon  (remote host)
                                    │
                                    ▼
                         packages/daemon/src/provider-runtime.ts
                              │                │
                              ▼                ▼
                         AgentRouter        Legacy path
                         (claude/codex/     (gemini/opencode/
                          openclaw/hermes)   nanobot)
                              │
                              ▼
                      Subprocess (stdin/stdout/JSON events)
```

Data flow for a task assigned to Claude Code:

1. User submits a task via the web UI; `@agent-space/services` creates a task queue record in PostgreSQL.
2. The remote daemon polls the task queue endpoint (`/api/daemon/tasks`) and claims the task.
3. `task-context.ts` assembles the full prompt: task payload + channel history + agent skills + knowledge pages + attachment text.
4. `provider-runtime.ts` routes to `runAgentRouterProviderTask()` for Claude.
5. `agent-router/adapters/claude.ts` spawns `claude -p --output-format stream-json --input-format stream-json --verbose` and delivers the prompt via stdin as JSON.
6. Events stream back from stdout; the adapter normalizes them into `AgentRouterEvent` objects and forwards them to the server via `/api/daemon/tasks/[taskId]/output-bundle`.

Persistent state lives in PostgreSQL (tasks, messages, documents, sessions, permissions). Runtime working directories are created per-task under the daemon's `--state-dir` (default `$HOME/.agent-space-daemon`).

---

## 3. The AgentRouter Harness

The AgentRouter is the central technical abstraction: a typed subprocess execution harness that normalizes four incompatible agent CLIs into one interface.

**Harness registry** (`packages/daemon/src/agent-router/types.ts`):
```
AGENT_ROUTER_HARNESSES = ["claude", "codex", "openclaw", "hermes"]
```

Each harness implements the `HarnessAdapter` interface:
- `id` / `label`
- `detect(executablePath?)` → `HarnessDetectResult` (found, version, diagnostics)
- `buildLaunch(request)` → `HarnessLaunchPlan` (executable, args, cwd, env, stdin, redactions)
- `run(plan, observer)` → `AgentRouterRunResult`
- `normalizeError(error)` → `AgentRouterDiagnostic`

**Event stream** (`packages/daemon/src/agent-router/types.ts`):
Normalized events emitted during a run:
- `harness_detected`, `harness_started` (carries PID)
- `text_delta`, `thought_delta`
- `approval_requested` / `approval_decision` (for tool permission bridge)
- `tool_started`, `tool_output`, `tool_finished`
- `session_updated` (sessionId for resume)
- `harness_exited` (exitCode, signal, durationMs)

**Diagnostic codes** cover 15 failure categories: `harness.cli_missing`, `harness.auth_required`, `harness.auth_invalid`, `harness.profile_missing`, `harness.model_unavailable`, `harness.tool_available/missing/unauthorized`, `harness.empty_response`, `harness.protocol_parse_failed`, `harness.timeout`, `harness.session_missing`, `harness.exited_nonzero`, `harness.unknown_failure`.

**Session continuation** uses three modes (`packages/daemon/src/task-context.ts`):
- `same_provider_resume` -- resume the exact prior session with `--resume <sessionId>`
- `cold_rebuild` -- rebuild context from transcript, start new session
- `fallback` -- switch provider when the primary is degraded

**Capability injection**: `RuntimeToolCapability` records (source: builtin | cli-hub | workspace | runtime) are translated into `Bash(<pattern>)` allowed-tool strings and injected into the Claude invocation, giving workspace admins declarative control over which shell commands agents may run.

---

## 4. LLM / External Service Integration

AgentSpace does **not** call LLMs directly via API. It instead spawns agent CLIs as local subprocesses and communicates via their stdin/stdout protocols. The platform is therefore LLM-provider-agnostic at the API level.

**Subprocess-based providers** (packages/daemon/src/provider-runtime.ts):

| Provider | Binary | Protocol | Session resume |
|----------|--------|----------|----------------|
| Claude Code | `claude` | `stream-json` bidirectional stdin/stdout | `--resume <sessionId>` |
| Codex CLI | `codex` | JSON events + temp output file | `codex exec resume <id> <prompt>` |
| OpenClaw | `openclaw` | JSON events | `--session-id <id>` |
| Hermes | `hermes` / `hermes-agent` | plain text | none |
| Gemini CLI | `gemini` | one-shot CLI | none (legacy path) |
| OpenCode | `opencode` | one-shot JSON CLI | none (legacy path) |
| NanoBot | `nanobot` | one-shot CLI | none (legacy path) |

**External services:**
- **PostgreSQL 16** -- primary storage; required. Also supports Neon cloud connection string via `DATABASE_URL`.
- **Google OAuth 2.0** -- workspace login; required for multi-tenant Google login (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
- **Google Workspace** -- optional per-agent delegated OAuth for Docs/Sheets read/write.
- **Cloudflare R2** -- optional attachment storage (falls back to local filesystem at `/var/lib/agentspace/workspaces`).
- **Cube sandbox API** -- experimental; not production-wired (packages/sandbox/src/cube/).

---

## 5. The Task Execution Pipeline

The end-to-end path from task creation to agent completion:

1. **Task creation** -- `@agent-space/services` inserts a task queue record with status `queued`; triggers notification to daemon via heartbeat.

2. **Claim** -- remote daemon polls `/api/daemon/tasks` (configurable `taskPollIntervalMs`); server returns a `ClaimedDaemonTask` + `DaemonTaskInputBundle` (version `json-inline-v1`): prompt text, metadata, runtime tool capabilities, router session info, and file attachments.

3. **Context assembly** (`packages/daemon/src/task-context.ts`) -- `buildDaemonTaskContext()` merges: channel history (up to N messages), agent skill files (copied to `skillContextDir`), knowledge page text, channel documents, attachments, orchestration step dependencies, mention cascade context, and auto-continuation state into a `PreparedDaemonTaskContext`.

4. **Provider selection** (`packages/daemon/src/provider-runtime.ts`) -- `runProviderTask()` reads the agent's assigned provider from `agentProfile`, checks `ProviderHealthStatus`, routes to `runAgentRouterProviderTask()` (claude/codex/openclaw/hermes) or legacy path (gemini/opencode/nanobot).

5. **AgentRouter dispatch** (`packages/daemon/src/agent-router/router.ts`) -- `runAgentRouter(request, observer)`:
   - Validates harness name
   - Calls `adapter.detect()` to verify binary exists and is functional
   - Calls `adapter.buildLaunch()` to produce `HarnessLaunchPlan`
   - Runs `runCapabilityDiagnostics()` against declared `RuntimeToolCapability` entries
   - Calls `adapter.run(plan, observer)` which spawns subprocess via `runLaunchPlan()`
   - Streams normalized events back to observer

6. **Approval bridge** (Claude only) -- when `handleControlRequests: true`, the adapter reads `control_request` events from Claude's stdout and calls `onApprovalRequest`; the daemon posts to `/api/daemon/tasks/[taskId]/approval-request`, polls for human decision, and writes `control_response` back into Claude's stdin.

7. **Completion** (`apps/web/app/api/daemon/tasks/[taskId]/complete/route.ts`) -- daemon POSTs `CompleteTaskRequest` containing `outputText`, final `sessionId`, `routerSessionId`, `workDir`, and an `outputBundle` (manifest of runtime output files). Server stores result, updates task status, distributes output to channel.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `packages/daemon/src/agent-router/types.ts` | ~200 | All AgentRouter type definitions: HarnessAdapter interface, event union, diagnostic codes, run request/result |
| `packages/daemon/src/agent-router/router.ts` | ~150 | Core routing: detect → buildLaunch → capability diagnostics → adapter.run |
| `packages/daemon/src/agent-router/adapters/openclaw.ts` | ~370 | OpenClaw adapter: ephemeral agent lifecycle, preflight health checks, error mapping |
| `packages/daemon/src/agent-router/adapters/claude.ts` | ~320 | Claude Code adapter: stream-json protocol, approval bridge, env sanitization |
| `packages/daemon/src/agent-router/adapters/codex.ts` | ~125 | Codex adapter: temp output file pattern, session resume |
| `packages/daemon/src/agent-router/adapters/hermes.ts` | ~80 | Hermes adapter: plain-text output, dual binary detection |
| `packages/daemon/src/agent-router/subprocess.ts` | ~90 | `runLaunchPlan()`: spawn + SIGTERM/SIGKILL timeout, bidirectional stdin |
| `packages/daemon/src/agent-router/events.ts` | ~90 | Per-harness event normalization (Claude, Codex, OpenClaw) |
| `packages/daemon/src/agent-router/capabilities.ts` | ~175 | RuntimeToolCapability: normalize, path-build, env-merge, diagnostic-run |
| `packages/daemon/src/provider-runtime.ts` | ~1840 | Provider catalog, task routing, legacy CLI execution paths |
| `packages/daemon/src/task-context.ts` | ~1070 | Prompt assembly: channel history, skills, knowledge, attachments, orchestration |
| `packages/daemon/src/remote-daemon.ts` | ~625 | Remote daemon: registration, heartbeat, task poll loop |
| `packages/daemon/src/runtime-output-manifests.ts` | ~1900 | Runtime output file manifests: JSONL, screenshots, session artifacts |
| `packages/domain/src/daemon-api.ts` | ~460 | Canonical daemon API types: DaemonTaskInputBundle, RuntimeToolCapability, all response shapes |
| `packages/domain/src/workspace.ts` | ~465 | Core domain types: WorkspaceMessage, WorkspaceSkill, ActiveEmployee |
| `packages/db/src/postgres-schema.ts` | ~1180 | Full PostgreSQL schema DDL |
| `packages/db/src/task-queue.ts` | ~930 | Task queue CRUD, claim/unclaim, status transitions |
| `packages/db/src/agent-router-sessions.ts` | ~840 | RouterSession storage and continuation mode resolution |
| `packages/services/src/permissions/permissions.ts` | ~2380 | Full RBAC: workspace roles, channel access, document permissions, approval rules |
| `apps/web/app/api/daemon/tasks/[taskId]/complete/route.ts` | ~520 | Task completion: output ingestion, session storage, channel message distribution |
| `apps/web/features/channels/channels-page-client.tsx` | ~3290 | Main workspace UI: channel list, message thread, task panel, agent presence |
| `apps/cli/src/commands/daemon.ts` | ~1235 | Full daemon CLI: register, start, stop, status, task management |
| `apps/cli/src/commands/output.ts` | ~1145 | Runtime output viewer: stream, download, format manifests |

---

## 7. Dependencies

**Root workspace:**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `npm` | `11.6.2` (packageManager) | Package manager, workspaces |
| `node` | `>=20.20.0` (daemon engine) | Runtime; 24 recommended |

**apps/web:**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `next` | `^16.1.6` | Web framework (App Router) |
| `react` | `^19.2.0` | UI library |
| `react-dom` | `^19.2.0` | DOM renderer |
| `@agent-space/domain` | `file:../../packages/domain` | Domain types |
| `@agent-space/services` | `file:../../packages/services` | Business logic |
| `agent-space-daemon` | `file:../../packages/daemon` | Daemon API client types |
| `@playwright/test` | `^1.56.0` (dev) | E2E tests |
| `@testing-library/react` | `^16.3.0` (dev) | Component tests |
| `typescript` | `^5.9.3` (dev) | Type checker |
| `vitest` | `^3.2.4` (dev) | Unit/integration test runner |

**packages/daemon:**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `@agent-space/db` | `file:../db` | PostgreSQL access |
| `@agent-space/domain` | `file:../domain` | Shared types |
| `@agent-space/sandbox` | `file:../sandbox` | Sandbox abstraction |
| `@agent-space/services` | `file:../services` | Business services |
| `esbuild` | `^0.27.7` (dev) | Daemon bundle build |

---

## 8. CLI / Usage Surface

**Entry points:**

| Binary | Origin | Description |
|--------|--------|-------------|
| `agent-space` | `apps/cli/bin/agent-space.js` | Workspace management CLI |
| `agent-space-daemon` | `packages/daemon/bin/agent-space-daemon.js` | Daemon lifecycle |
| `agent-router` | `packages/daemon/bin/agent-router.js` | Direct AgentRouter access |

**Commands (workspace CLI):**

```bash
npm run cli -- help
npm run cli -- doctor [--json]
npm run cli -- workspace status [--json]
npm run cli -- daemon register|start|stop|status
npm run cli -- task list|show|assign|cancel
npm run cli -- output show|stream|download <taskId>
npm run cli -- skill list|import|remove
npm run cli -- employee list|show
npm run cli -- channel list|messages
npm run cli -- cost summary [--period=7d]
npm run cli -- db init|migrate|status
```

**Daemon start:**

```bash
agent-space-daemon start \
  --foreground \
  --server-url "https://your-agentspace-domain" \
  --daemon-token "adt_xxx" \
  --daemon-id "daemon-prod-01" \
  --device-name "prod-daemon-host-01" \
  --runtime-name "Remote Agent" \
  --task-timeout "43200000" \
  --state-dir "$HOME/.agent-space-daemon"
```

**AgentRouter direct:**

```bash
agent-router harnesses                         # list available harnesses
agent-router detect                            # parallel detect all harnesses
agent-router run --harness claude \
  --cwd /project \
  --model claude-sonnet-4-6 \
  --json-events \
  "your prompt here"
```

**Environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | — | PostgreSQL connection string (required) |
| `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` | — | Stable encryption key for server actions (required) |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | — | Google OAuth (required for login) |
| `AGENT_SPACE_DEPLOYMENT_MODE` | `self-hosted` | `self-hosted` or `cloud` |
| `AGENT_SPACE_STORAGE_PROVIDER` | `local` | `local` or `r2` |
| `AGENT_SPACE_UPLOAD_MAX_SIZE_BYTES` | `52428800` | 50 MB upload limit |
| `AGENT_SPACE_SANDBOX_PROVIDER` | `local` | `local` or `cube` |
| `AGENT_SPACE_CUBE_API_URL` | — | Cube sandbox API URL |
| `OPENCLAW_PROFILE` | — | OpenClaw auth profile override |
| `AGENT_SPACE_OPENCLAW_PROFILE_OVERRIDE` | — | Per-task OpenClaw profile |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `.env` / `.env.example` | All environment variables |
| `deploy/postgres/docker-compose.yml` | Local PostgreSQL setup |
| `deploy/systemd/agentspace.service` | systemd unit for web server |
| `deploy/systemd/agentspace-daemon.service` | systemd unit for daemon |
| `deploy/nginx/agentspace.conf` | Nginx reverse proxy config |

---

## 9. Extensibility Points

- **New AgentRouter harness**: Add a file in `packages/daemon/src/agent-router/adapters/` implementing the `HarnessAdapter` interface (`types.ts`). Register the harness id in `AGENT_ROUTER_HARNESSES` (`types.ts`) and add the adapter to the router's catalog in `router.ts`. The router's detect/launch/normalize pipeline then covers it automatically.

- **New legacy provider** (one-shot CLI without session support): Add a branch in `provider-runtime.ts` alongside `runGeminiProviderTask()` and `runOpenCodeProviderTask()`. Legacy providers bypass AgentRouter entirely and use direct `child_process.spawn`. Add the provider id to `DAEMON_PROVIDER_IDS` in `packages/domain/src/daemon-provider.ts`.

- **New RuntimeToolCapability source**: The `source` field on `RuntimeToolCapability` (`daemon-api.ts`) supports `builtin | cli-hub | workspace | runtime`. A new source type requires extending `capabilities.ts:normalizeRuntimeToolCapabilities()` and the DB record in `packages/db/src/runtime-apps.ts`.

- **New sandbox backend**: Implement the `SandboxInterface` (`packages/sandbox/src/interface.ts`) and add a branch in `packages/sandbox/src/factory.ts:connectSandbox()`. Set `AGENT_SPACE_SANDBOX_PROVIDER` to the new provider name.

- **New agent template**: Add a `SystemAgentTemplatePreset` entry to the template array in `packages/domain/src/agent-templates.ts`. The preset includes display name, instructions, and skill recommendations; it is immediately available in the web UI's agent creation flow.

- **New document integration**: Follow the pattern in `packages/services/src/integrations/` (google-workspace-cli.ts, external-sheets.ts, external-google-docs.ts). Add the integration type to the `StoredAgentGoogleWorkspaceDelegationRecord` scopes in `packages/db/src/types.ts`.

---

## 10. Limitations and Gotchas

- **Pre-built daemon tgz committed to git**: `agent-space-daemon-0.1.3.tgz` (503 KB) is committed to the repository root. Any binary artifact in git history is a supply-chain hygiene concern and bloats clone size permanently.

- **No semantic versioning discipline visible**: Version is `0.1.0` (workspace) and `0.1.3` (daemon), with a June 2026 initial-release changelog entry. The `^16.1.6` Next.js constraint references a version not yet stable at knowledge cutoff, which may cause silent breakage if `npm install` resolves to a newer incompatible release.

- **Cube sandbox exec unimplemented**: `packages/sandbox/src/cube/cube-sandbox.ts` has only the lifecycle scaffold (create/pause/snapshot/destroy). The `exec()` path is not wired to the Cube data plane. Using `AGENT_SPACE_SANDBOX_PROVIDER=cube` will silently fail on any tool call requiring subprocess execution.

- **Hermes adapter has no structured event stream**: The Hermes adapter parses plain text output. There is no tool-call visibility, no session state, and no approval bridge for Hermes tasks -- admins cannot audit Hermes tool use at the same fidelity as Claude or OpenClaw.

- **AgentRouter timeout is 12 hours wall-clock**: `DEFAULT_AGENT_ROUTER_TIMEOUT_MS = 12 * 60 * 60 * 1000`. With no adaptive timeout, a stuck process holds a task slot for 12 hours before SIGTERM is sent.

- **OpenClaw ephemeral agent cleanup is best-effort**: The `finally` block in the OpenClaw adapter calls `openclaw agents delete <name> --force --json`, but if the daemon process is killed mid-task, the ephemeral agent is orphaned in the local OpenClaw installation.

- **Node `--experimental-strip-types` used in production CLI**: The CLI runs TypeScript source directly using Node's experimental native stripping. This means the production CLI behavior is coupled to the Node.js version's experimental feature stability -- not a transpiled artifact.

- **Google OAuth credential storage encrypted but key management undocumented**: Access and refresh tokens are stored as `accessTokenEncrypted` / `refreshTokenEncrypted` in the DB (`types.ts`). The encryption key derivation and rotation procedure are not documented in the README or deploy scripts.

- **No multi-agent isolation or sandbox policy**: The roadmap explicitly lists "multi-agent isolation and sandbox policy layer" as planned. Currently, all agents on a daemon host share the same filesystem namespace.

- **RouterSession `cold_rebuild` can truncate context**: When `same_provider_resume` is unavailable and the full transcript exceeds context, `cold_rebuild` mode compresses to `memorySummary` + recent `transcriptLines`. Long-running tasks may silently lose earlier context.

---

## 11. How It Compares to Alternatives

**vs. AutoGen (Microsoft)** -- AutoGen is a Python framework for multi-agent conversation graphs with LLM API calls baked in. AgentSpace is higher in the stack: it manages human organizational structure (workspaces, permissions, assignments, audit trails) and drives existing agent CLIs as subprocesses rather than calling LLM APIs directly. AutoGen is a code library; AgentSpace is a deployable product with a web UI and PostgreSQL backend.

**vs. CrewAI** -- CrewAI defines agents and tasks in Python config and orchestrates them via LangChain. It has no concept of persistent workspaces, document sharing, human approval flows, or team-level governance. CrewAI targets autonomous pipelines; AgentSpace targets human-in-the-loop organizational workflows where agents have defined owners and operate with governance constraints.

**vs. Temporal** -- Temporal is a workflow orchestration engine with durable execution, retry logic, and long-running state. AgentSpace borrows the queue-based task lifecycle idea but is purpose-built for AI agent execution rather than general distributed workflows. Temporal has no agent-specific concepts (tool approval, harness detection, session resume); AgentSpace has no generic workflow DAG primitives.

**vs. Airplane / Retool (internal tooling platforms)** -- These platforms provide UI-driven automation for human operators. AgentSpace differs in that the agents themselves are the primary executors, with humans in an oversight and approval role rather than the primary operators. The permission model is agent-centric (what tools can this agent use?) rather than human-centric (what operations can this user trigger?).

AgentSpace's positioning: a self-hosted, open-source organizational layer that wraps existing agent CLIs with team governance, shared workspace context, and a unified execution harness -- without requiring changes to the underlying agent providers.

---

## Appendix: Selected Code Snippets

**AgentRouter harness detection and dispatch** (`packages/daemon/src/agent-router/router.ts`)

```typescript
export async function runAgentRouter(
  request: AgentRouterRunRequest,
  observer: AgentRouterObserver
): Promise<AgentRouterRunResult> {
  const adapter = getAdapter(request.harness)
  const detected = await adapter.detect(request.executablePath)
  if (!detected.found) {
    return { status: "error", diagnostics: detected.diagnostics, ... }
  }
  const plan = adapter.buildLaunch(request)
  const capDiagnostics = await runCapabilityDiagnostics(
    request.runtimeToolCapabilities ?? [], adapter.id
  )
  return adapter.run(plan, observer, capDiagnostics)
}
```

**Claude bidirectional stdin approval bridge** (`packages/daemon/src/agent-router/adapters/claude.ts`)

```typescript
// Prompt delivered via stdin as JSON
const stdinPayload = JSON.stringify({
  type: "user",
  message: { role: "user", content: [{ type: "text", text: request.prompt }] }
})
controller.writeStdin(stdinPayload + "\n")

// Approval bridge: intercepts control_request events
if (event.type === "control_request" && request.handleControlRequests) {
  const decision = await request.onApprovalRequest(event)
  controller.writeStdin(JSON.stringify({
    type: "control_response",
    decision: decision.allow ? "allow" : "deny",
    reason: decision.reason
  }) + "\n")
}
```

**Task context assembly** (`packages/daemon/src/task-context.ts`)

```typescript
// RouterSession continuation mode resolution
if (routerSession?.conversationKey === currentConversationKey) {
  if (routerSession.providerName === agentProfile.provider) {
    continuationMode = "same_provider_resume"
  } else {
    continuationMode = "cold_rebuild"  // provider changed, rebuild from transcript
  }
} else {
  continuationMode = "fallback"  // no prior session for this conversation
}
```

**RuntimeToolCapability → allowed-tool injection** (`packages/daemon/src/agent-router/capabilities.ts`)

```typescript
export function buildCapabilityAllowedTools(
  capabilities: RuntimeToolCapability[]
): string[] {
  return capabilities.flatMap(cap =>
    (cap.allowedShellPatterns ?? []).map(pattern => `Bash(${pattern})`)
  )
}
// Result injected into ClaudeRunRequest.temporaryAllowedTools
```
