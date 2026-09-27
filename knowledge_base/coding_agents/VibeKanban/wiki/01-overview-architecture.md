> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Architecture Overview: Local-First Kanban for Parallel Coding Agents

**In one sentence:** Vibe Kanban is a local-first web app where one Rust backend binary (web server plus agent runner) serves a TypeScript kanban UI (visual task board) and runs many coding agents in parallel, each in its own isolated copy of the code.

## Key points

- The repo is a split workspace (a set of related packages built together): about 30 Rust packages (called crates) in `Cargo.toml:3` plus 5 TypeScript packages under `pnpm-workspace.yaml:1`, with Rust for the backend and TypeScript/React for the frontend.
- The default product is local-first (your data stays on your machine): a single `server` binary opens two ports on startup, one for the main app and one for live app previews, per `crates/server/src/main.rs:117`.
- Launch path is `npx vibe-kanban`: the npm (Node package manager) entry `package.json:5` points at the CLI (command-line interface) in `npx-cli/src/cli.ts:1`, which downloads the matching server binary and starts it.
- Backend and frontend share one contract: the `api-types` crate holds row types, request types, and shared enums used by both local and remote backends, per `crates/api-types/src/lib.rs:1`.
- Persistence (saved data) is SQLite (a lightweight file-based relational database): `DBService` wraps a SQLite pool in `crates/db/src/lib.rs:71` and migrates plus opens `db.v2.sqlite` in `crates/db/src/lib.rs:15` and `crates/db/src/lib.rs:79`.
- Business logic is factored behind a `Deployment` trait (an interface describing what any backend must do), defined in `crates/deployment/src/lib.rs:80` and implemented locally by `LocalDeployment` in `crates/local-deployment/src/lib.rs:52`, with about 20 service modules wired in `crates/services/src/services/mod.rs:1`.
- Cloud and remote access are a separate track: `crates/remote` is excluded from the main Cargo workspace in `Cargo.toml:35` and ships its own server (`crates/remote/src/main.rs`), while the `relay-*` crates listed in `Cargo.toml:4` provide tunneling and live links (WebSocket, a two-way live connection; WebRTC, a browser peer-to-peer protocol) back to a local instance.

---

## Backend: one Rust binary, many small crates

The backend is a single deployable binary whose `tokio::main` entry (the async startup function) lives in `crates/server/src/main.rs:32`. Startup follows a fixed order in that file: install the TLS (Transport Layer Security, encrypted networking) provider in `crates/server/src/main.rs:34`, create the asset directory and migrate the old database copy in `crates/server/src/main.rs:52`, build the deployment object in `crates/server/src/main.rs:72`, clean up orphan agent runs in `crates/server/src/main.rs:74`, bind the main plus preview-proxy listeners in `crates/server/src/main.rs:117`, build the router in `crates/server/src/main.rs:142`, and spawn relay registration in `crates/server/src/main.rs:183`.

HTTP (the web request protocol) routing is assembled in one function in `crates/server/src/routes/mod.rs:36`. It nests three layers: signed relay routes in `crates/server/src/routes/mod.rs:37`, the `/api` group with origin checking in `crates/server/src/routes/mod.rs:70`, and the outer router that serves the bundled frontend for `/` and every other path in `crates/server/src/routes/mod.rs:80`. Route modules cover workspaces, execution processes (single agent runs), containers, terminals, approvals, sessions, search, preview, and remote control, as listed in `crates/server/src/routes/mod.rs:9`.

The `server` crate itself stays thin by design: `crates/server/src/lib.rs:1` only declares modules (`error`, `middleware`, `relay_pairing`, `routes`, `runtime`, `startup`) and aliases `DeploymentImpl` to the local backend in `crates/server/src/lib.rs:11`. All behavior comes from dependency crates: `db` for storage, `services` for logic, `executors` for agent adapters (one adapter per supported coding agent, e.g. Claude, Codex files visible under `crates/executors/src/executors/`), `worktree-manager` plus `workspace-manager` for isolated code copies, `git` plus `git-host` for version control, `preview-proxy` for app previews, and `local-deployment` for process and PTY (pseudo-terminal, the virtual terminal agents type into) handling in `crates/local-deployment/src/lib.rs:52`.

## Frontend: TypeScript packages served by the backend

There are 5 frontend packages in `packages/` (directory listing: `local-web`, `remote-web`, `web-core`, `ui`, `public`), registered as a pnpm (Node package manager) workspace in `pnpm-workspace.yaml:1`. The local app is `@vibe/local-web` per `packages/local-web/package.json:1`, built with Vite (a fast web build tool) per the `vite.config.ts` in that directory; shared screens and logic live in `@vibe/web-core` per `packages/web-core/package.json:1`, and shared visual components live in `packages/ui/`. The dev command starts backend and frontend together with assigned ports in `package.json:16`, while the backend serves the built web files itself in production through the frontend fallback routes in `crates/server/src/routes/mod.rs:80`.

## Local vs cloud/relay split

Local execution is the default path: `LocalDeployment` in `crates/local-deployment/src/lib.rs:52` bundles config, database, workspace manager, git service, container service, and PTY service in one process. The abstract `Deployment` trait in `crates/deployment/src/lib.rs:80` lets other backends reuse the same route and service code without forking the server.

Remote and cloud pieces are deliberately separated. `crates/remote` has its own manifest, migrations, Dockerfile, and Compose setup (see `crates/remote/` directory: `Cargo.toml`, `migrations/`, `Dockerfile`, `docker-compose.yml`) and is excluded from the local workspace build in `Cargo.toml:35`, with its own entry and route tree under `crates/remote/src/` (including `main.rs`, `routes/`, `state.rs`, `db/`). Connectivity between a browser outside the home network and a local instance goes through the relay family (`relay-client`, `relay-control`, `relay-protocol`, `relay-ws`, `relay-hosts`, `relay-tunnel-core`, `relay-webrtc`, `ws-bridge`), all declared as workspace members in `Cargo.toml:4`. A desktop shell (Tauri, a framework wrapping web apps as native apps) exists separately in `crates/tauri-app/src/main.rs:1`, reusing the same backend services plus native notifications.

## Data flow end-to-end

A typical task-to-agent-run path through the system:

1. User launches the app (`npx vibe-kanban` ► CLI downloads/starts server binary)
   │ `package.json:5` declares the binary entry; CLI logic starts in `npx-cli/src/cli.ts:1`
   ▼
2. Browser loads UI plus live channels (HTTP API, SSE event stream, terminal WebSocket)
   │ outer router plus `/api` nesting in `crates/server/src/routes/mod.rs:80`; events router merged in `crates/server/src/routes/mod.rs:48`; terminal and SSH-session sockets in `crates/server/src/routes/mod.rs:55`
   ▼
3. User creates issue and workspace (kanban card ─ ► isolated code copy plus agent run)
   │ shared request/row types in `crates/api-types/src/lib.rs:10`; workspace plus execution-process routers in `crates/server/src/routes/mod.rs:41`; logic in `crates/services/src/services/mod.rs:5` (`container`, `execution_process`, `repo`)
   ▼
4. Agent executes in worktree with PTY, logs stream back to UI
   │ local container and PTY services in `crates/local-deployment/src/lib.rs:52` and `crates/local-deployment/src/container.rs`; process routes in `crates/server/src/routes/mod.rs:42`
   ▼
5. Results persist to SQLite and stay visible after restart
   │ models enumerated in `crates/db/src/models/mod.rs:1`; pool plus file path in `crates/db/src/lib.rs:71` and `crates/db/src/lib.rs:79`
   ▼
6. Optional: remote browser reaches the same instance through relay signing
   │ relay middleware layers in `crates/server/src/routes/mod.rs:60`; relay registration spawn in `crates/server/src/main.rs:183`

## Where persistent state lives

The local database file is `db.v2.sqlite` inside the app asset directory, opened in `crates/db/src/lib.rs:79`, with schema migrations embedded from `./migrations` in `crates/db/src/lib.rs:15`. The main tables map to the models listed in `crates/db/src/models/mod.rs:1`: projects, tasks (kanban issues), workspaces, execution processes plus their logs and repo state, sessions, merges, pull requests, files, and tags. Startup preserves downgrade safety by copying the old `db.sqlite` to the new path only when the new file is missing, per `crates/server/src/main.rs:58`. Ephemeral (short-lived) state such as running agent processes, preview-proxy ports, and relay registrations lives in memory inside the deployment object built in `crates/server/src/main.rs:72` and is rebuilt or cleaned on every boot. The remote backend keeps its own separate database and migrations under `crates/remote/` and does not share the local SQLite file.

**Covers:** `README.md`, `Cargo.toml`, `package.json`, `pnpm-workspace.yaml`, `crates/` (workspace layout), `packages/` (`local-web`, `remote-web`, `web-core`, `ui`, `public`), `crates/server/src/main.rs`, `crates/server/src/lib.rs`, `crates/server/src/routes/mod.rs`, `npx-cli/src/cli.ts`, `crates/tauri-app/src/main.rs`, `crates/api-types/src/lib.rs`, `crates/db/src/lib.rs`, `crates/db/src/models/mod.rs`, `crates/services/src/services/mod.rs`, `crates/deployment/src/lib.rs`, `crates/local-deployment/src/lib.rs`, `crates/remote/`, `crates/executors/`, `docs/`
