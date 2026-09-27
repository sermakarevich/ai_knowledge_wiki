> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Control Surface

**In one sentence:** One local Go daemon on loopback owns all state in SQLite and all domain logic, while the Electron desktop, thin CLI, and opt-in mobile clients stay thin; status is never stored but derived at read time, and every change flows to clients as replayable CDC events.

## Key points

- One Go daemon owns durable state in SQLite plus all domain logic; the Electron/React desktop, `ao` CLI, and Expo mobile clients are thin HTTP/SSE/mux clients.
- The CLI never touches the database and never launches adapters — it is a pure HTTP client that requires the desktop app (and its supervised daemon) to be running.
- Status is never stored: the daemon persists activity, termination, controller generation, and PR/check/review facts, then computes labels (working, needs input, CI failed, ready to merge) on read.
- Storage lives under `~/.ao` (`AO_DATA_DIR` / `AO_RUN_FILE` overrides are advanced-only); SQLite triggers append to `change_log` and a CDC poller broadcasts over SSE with `Last-Event-ID` replay.
- The primary listener is unauthenticated `127.0.0.1:3001` and can never be bound publicly; phone access is a second opt-in plaintext LAN listener with a bearer password, trusted-home-network only.
- The desktop supervises the daemon (discover, launch, restart); `ao status` and `ao doctor --json` diagnose daemon, config, data dir, database, Git, and tmux/conpty health.
- Schema evolution is append-only: new migrations only, never modify a merged migration.

---

## 1. Process layout

```text
Electron/React desktop ─┐
ao CLI (thin HTTP) ─────┼──► Go daemon (127.0.0.1:3001) ──► SQLite (~/.ao/data)
Expo mobile (opt-in) ───┘         │  ├─ services / managers / adapters
                                  │  ├─ tmux-conpty runtime, Chat controllers
                                  │  ├─ GitHub SCM observer, lifecycle engine
                                  └──► SSE events + terminal mux + browser bridge
```

The daemon owns the runtime, workspace, tracker, and SCM layers. There is no plugin marketplace: adapters are compiled into the binary behind port interfaces. The desktop owns the daemon process lifetime — recovery step number one in troubleshooting is "quit and reopen the desktop app", which restarts the daemon and reconnects SSE plus terminal streams.

## 2. Thin clients

| Client | Role | Notes |
|---|---|---|
| Electron/React desktop | Primary UI: kanban board (Pending / Iterating / In Review / Ready to merge / Archive), session cards with agent, branch, PR state, live activity | Supervises the daemon |
| `ao` CLI | Start/stop/status/doctor, spawn, session, send, orchestrator, pr, review, preview/browser, import | Never opens SQLite, never launches adapters |
| Expo mobile | Watch sessions and terminal, receive notifications over LAN or Tailscale | Code stays on the desktop machine; shutdown/telemetry/browser routes excluded |

Key commands: `ao status`, `ao doctor [--json]`, `ao spawn --kind worker|orchestrator [--agent …] [--mode chat|tui]`, `ao session ls/get/kill/restore/rename/cleanup/claim-pr/switch-agent`, `ao send`, `ao orchestrator ls`, `ao pr merge/resolve-comments`, `ao review ls/trigger/cancel/submit`, `ao preview`, `ao browser`, `ao project add/ls/get/set-config/rm`, `ao agent ls --refresh`.

Relevant environment variables: `AO_PORT=3001`, `AO_RUN_FILE`, `AO_DATA_DIR`, `AO_REQUEST_TIMEOUT`, `AO_SHUTDOWN_TIMEOUT`, `AO_SESSION_ID`, `AO_PROJECT_ID`.

## 3. Durable facts, derived status

The daemon stores only facts:

- Agent activity (active/idle/waiting/blocked/exited), termination records.
- Interface mode, controller handle and generation, transition checkpoints.
- PR, check, and review facts from the SCM observer.
- Notification records, reviewer-agent runs.

Display labels — working, needs input, CI failed, ready to merge — are computed when a client reads. Rationale: a stored status string always drifts from reality under failures; derivation cannot drift. A failed or unknown runtime probe is recorded as an observation, never as proof the session died; the operator reopens the session and looks before killing it.

## 4. Storage and live updates

- SQLite database under `~/.ao/data` (overridable via `AO_DATA_DIR`, advanced-only).
- SQLite triggers append every mutation to a `change_log` table.
- A CDC (Change Data Capture — reading the log of what changed) poller broadcasts invalidations over `GET /api/v1/events` as SSE (Server-Sent Events — one-way live updates from server), with `Last-Event-ID` replay so reconnecting clients resume without refetching everything.
- Migrations are append-only: new migration files only, never edit a merged one.

## 5. Networking posture

- Primary listener: unauthenticated, loopback-only `127.0.0.1:3001`; cannot be bound to a public interface.
- Connect Mobile: second, explicitly enabled listener on the LAN, plaintext HTTP with a bearer password, trusted-home-network only. Shutdown, telemetry, and browser-control routes are excluded from it.
- Tailscale is the documented path for remote phone access outside the home network; code and state never leave the desktop machine.

## 6. The eight load-bearing rules

1. Derive status, don't store it.
2. Probes are observations, not death.
3. Never force-delete a dirty worktree.
4. All state lives under `~/.ao`.
5. Loopback-only primary listener.
6. Thin CLI and UI — all logic in the daemon.
7. CDC events via triggers + change log + SSE replay.
8. Append-only migrations.

**Covers:** docs architecture page (daemon, clients, storage, CDC/SSE, networking), CLI reference (status/doctor/spawn/session/send/pr/review/project/agent), configuration env vars, troubleshooting daemon recovery.
