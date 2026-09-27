> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Preview Browser and Dev Server: See the Agent's Work Live
**In one sentence:** Each workspace runs its dev servers as ordinary `run_reason='devserver'` execution processes whose framework-printed `localhost:PORT` URL is scraped from logs and loaded in a sandboxed iframe through a dedicated subdomain-routed preview-proxy server that injects navigation, inspect, and Eruda (a mobile-friendly in-page developer-tools console) instrumentation while keeping untrusted app content on a separate origin and port from the main application.

## Key points
- There are exactly two proxy ingress paths to a workspace dev server: the iframe path through a standalone proxy listener keyed by subdomain (`{devPort}.localhost:{proxyPort}`) and the programmatic path `GET /api/preview/{target_port}/{*tail}`, both ultimately forwarding plain HTTP/WebSocket to `localhost:{target_port}` (`crates/preview-proxy/src/lib.rs:384-400`, `crates/server/src/routes/preview.rs:13-17`, `crates/preview-proxy/src/proxy_common.rs:37-55`).
- Dev-server ports are never allocated or stored by the backend: the backend only auto-assigns its own main and proxy ports at boot (`bind(...:0)` semantics, `PREVIEW_PROXY_PORT` override), while the dev port is whatever the user's framework binds, discovered by regex-scanning streamed process logs (`crates/server/src/main.rs:96-140`, `packages/web-core/src/shared/hooks/usePreviewUrl.ts:151-220`).
- Starting a dev server kills every running dev server in the workspace and spawns one `ExecutionProcess` with `run_reason='devserver'` per repo that has a non-empty `dev_server_script`, executed with `working_dir=<repo_name>`; there is no port reservation, health check, or auto-restart (`crates/server/src/routes/workspaces/execution.rs:38-137`, `crates/db/src/models/execution_process.rs:50-59`).
- The built-in browser is an iframe plus toolbar (`PreviewBrowser`) with back/forward/refresh/goto driven by `postMessage`, three device viewports (desktop, 390x844 mobile phone frame, draggable responsive defaulting to 800x600), per-workspace URL-override and viewport persistence, click-to-component inspect mode, and an embedded Eruda console (`packages/ui/src/components/PreviewBrowser.tsx:46-92`, `packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:272-325`, `packages/web-core/src/shared/hooks/usePreviewSettings.ts:33-36`).
- Every proxied HTML response gets up to four script injections (React DevTools bippy hook after `<head>`, Eruda CDN plus init plus navigation bridge plus click-to-component before `</body>`), and every navigation/ready event returns over `postMessage` with source tag `vibe-devtools` (`crates/preview-proxy/src/lib.rs:591-618`, `packages/web-core/src/shared/types/previewDevTools.ts:1-47`).
- The security boundary is origin and process isolation, not authentication: the proxy is a separate `TcpListener`/router with `validate_origin`, the iframe carries a restrictive `sandbox` attribute, framing-related response headers are stripped, relay signing headers are never forwarded upstream, and loopback `Location`/`Refresh`/Next.js-redirect targets are rewritten back into the proxy origin (`crates/server/src/main.rs:161-170`, `packages/ui/src/components/PreviewBrowser.tsx:32-33`, `crates/preview-proxy/src/lib.rs:77-86`, `crates/preview-proxy/src/proxy_common.rs:3-26`, `crates/preview-proxy/src/lib.rs:234-364`).

---
## 1. The two request paths

### 1.1 Path A: iframe via the standalone subdomain proxy (primary)

The backend boots two `TcpListener`s, one for the app and one for previews (`crates/server/src/main.rs:117-131`):

```rust
let main_listener = tokio::net::TcpListener::bind(format!("{host}:{port}")).await?;
let actual_main_port = main_listener.local_addr()?.port();

let proxy_listener = tokio::net::TcpListener::bind(format!("{host}:{proxy_port}")).await?;
let actual_proxy_port = proxy_listener.local_addr()?.port();
```

The proxy router is a bare fallback with only origin validation (`crates/server/src/main.rs:161-162`):

```rust
let proxy_router: Router = routes::preview::subdomain_router(deployment.clone())
    .layer(ValidateRequestHeaderLayer::custom(validate_origin));
```

The same construction exists for the Tauri/desktop handle (`crates/server/src/startup.rs:54-56`). The module contract is stated at the top of the crate (`crates/preview-proxy/src/lib.rs:1-8`):

```rust
//! Provides a separate HTTP server for serving preview iframe content.
//! This isolates preview content from the main application for security.
//!
//! The proxy listens on a separate port and routes requests based on the
//! Host header subdomain. A request to `{port}.localhost:{proxy_port}/path`
//! is forwarded to `localhost:{port}/path`.
```

Dispatch extracts the target from the `Host` subdomain, supporting an optional remote-host token (`crates/preview-proxy/src/lib.rs:366-382`):

```rust
fn extract_target_from_host(headers: &HeaderMap) -> Option<PreviewTarget> {
    let host = headers.get(header::HOST)?.to_str().ok()?;
    let subdomain = host.split('.').next()?;
    let (port_str, relay_host_id) = match subdomain.split_once("--") {
        Some((port_str, host_id_str)) => {
            let host_id = Uuid::parse_str(host_id_str).ok()?;
            (port_str, Some(host_id))
        }
        None => (subdomain, None),
    };

    let port = port_str.parse::<u16>().ok()?;
    Some(PreviewTarget {
        port,
        relay_host_id,
    })
}
```

Entry point returns `400` when no valid port is present (`crates/preview-proxy/src/lib.rs:384-400`):

```rust
pub async fn proxy_subdomain_request(
    service: &PreviewProxyService,
    backend_addr: SocketAddr,
    proxy_port: u16,
    request: Request,
) -> Response {
    let target = match extract_target_from_host(request.headers()) {
        Some(port) => port,
        None => {
            return (StatusCode::BAD_REQUEST, "No valid port in Host subdomain").into_response();
        }
    };

    let path = normalized_proxy_path(request.uri().path()).to_string();

    proxy_impl(service, backend_addr, proxy_port, target, path, request).await
}
```

The frontend builds exactly this URL (`packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:309-314`):

```rust
// Subdomain-based routing: the proxy extracts the port from the Host header
const hostToken =
  hostId != null ? `${devServerPort}--${hostId}` : devServerPort;
const proxyUrl = new URL(
  `http://${hostToken}.localhost:${previewProxyPort}${path}`
);
```

Full chain for a local preview:

| Step | Component | Mechanism |
|---|---|---|
| 1 | `PreviewBrowserContainer.iframeUrl` | Detected or overridden dev URL is rewritten to `http://{devPort}.localhost:{proxyPort}{path}?_refresh=N` (`packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:272-325`) |
| 2 | Browser iframe | Loads the proxy origin in a sandboxed iframe (`packages/ui/src/components/PreviewBrowser.tsx:32-33`) |
| 3 | `subdomain_router` fallback | `subdomain_proxy_request` reads server addr and proxy port from `client_info` (`crates/server/src/routes/preview.rs:112-139`) |
| 4 | `proxy_subdomain_request` | Parses `{devPort}` (and optional `--{hostId}`) from `Host`, upgrades WebSocket if requested, else runs the HTTP forwarder (`crates/preview-proxy/src/lib.rs:402-453`) |
| 5 | `http_proxy_handler` | Rebuilds `http://localhost:{devPort}/{path}?{query}` (or a relay `ws`/`http` target for remote hosts), forwards allow-listed headers, injects scripts into HTML (`crates/preview-proxy/src/lib.rs:455-492`, `crates/preview-proxy/src/lib.rs:591-618`) |

### 1.2 Path B: programmatic `/api/preview` on the main server

The main router mounts the preview API under `/api` alongside all other API routes (`crates/server/src/routes/preview.rs:13-17`, `crates/server/src/routes/mod.rs:52`):

```rust
pub(super) fn api_router() -> Router<DeploymentImpl> {
    Router::new()
        .route("/preview/{target_port}", any(proxy_preview_request_no_tail))
        .route("/preview/{target_port}/{*tail}", any(proxy_preview_request))
}
```

Semantics differ deliberately from Path A: this path performs no HTML rewriting and no redirect surgery; it relays status, non-hop-by-hop headers, and a byte stream (`crates/preview-proxy/src/api.rs:116-135`):

```rust
fn relay_http_response(response: reqwest::Response) -> Response {
    let status = response.status();
    let response_headers = response.headers().clone();
    let body = Body::from_stream(response.bytes_stream());

    let mut builder = Response::builder().status(status);
    for (name, value) in &response_headers {
        if !is_hop_by_hop_header(name.as_str()) {
            builder = builder.header(name, value);
        }
    }
    ...
}
```

WebSocket handling exists on both paths and preserves subprotocols (required for Vite hot-module-reload, which checks `Sec-WebSocket-Protocol: vite-hmr` and `?token=`): the subdomain path extracts protocols before upgrade (`crates/preview-proxy/src/lib.rs:412-449`), the API path echoes the upstream-selected protocol back to the client (`crates/preview-proxy/src/api.rs:84-114`, `crates/server/src/routes/preview.rs:67-110`).

## 2. Port handling: what is allocated, what is merely detected

There is no dev-server port manager. Two ports are allocated; the third is observed:

- Main app port comes from `BACKEND_PORT`/`PORT` or `0` (OS auto-assign) (`crates/server/src/main.rs:96-108`).
- Preview proxy port comes from `PREVIEW_PROXY_PORT` or `0` (`crates/server/src/main.rs:110-113`).
- Both actual ports are published via the port file and `client_info` (`crates/server/src/main.rs:123-140`); the proxy port is also exposed to clients through the config endpoint (`crates/server/src/routes/config.rs:101`, `crates/server/src/routes/config.rs:174`).
- The dev-server port is never chosen, reserved, recorded in the database, or passed to the proxy out-of-band. It travels inside the `Host` header (Path A) or the URL path parameter (Path B).

Detection is entirely client-side log scraping. `usePreviewUrl` scans streamed process logs for loopback URLs or `host:port` tokens, normalizes `0.0.0.0`/`127.0.0.1`/private IPv4 to `localhost`, ignores Vibe Kanban's own ports, and prefers the newest localhost candidate (`packages/web-core/src/shared/hooks/usePreviewUrl.ts:151-220`, `packages/web-core/src/shared/hooks/usePreviewUrl.ts:253-312`):

```ts
const urlPatterns = [
  // Full URL pattern (e.g., http://localhost:3000, https://127.0.0.1:8080)
  /(https?:\/\/(?:\[[0-9a-f:]+\]|localhost|127\.0\.0\.1|0\.0\.0\.0|\d{1,3}(?:\.\d{1,3}){3})(?::\d{2,5})?(?:\/\S*)?)/i,
  // Host:port pattern (e.g., localhost:3000, 0.0.0.0:8080)
  /((?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[[0-9a-f:]+\]|(?:\d{1,3}\.){3}\d{1,3})):(\d{2,5})/gi,
];
```

Consequences, all user-visible in docs: the dev command must print its URL to stdout/stderr (`docs/core-features/testing-your-application.mdx:39-46`); `0.0.0.0`/`::` are converted to `localhost` for embedding (`docs/core-features/testing-your-application.mdx:211-223`); port conflicts are the user's problem to resolve with `lsof -i :3000` (`docs/browser-testing.mdx:125-127`).

Non-loopback URLs (for example Coder port-forwarded `https://4000--workspace--user.coder.example.com`) deliberately bypass the proxy and load directly, losing script injection, Eruda, inspect mode, and `postMessage` single-page-app navigation (`packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:261-284`).

## 3. Dev-server lifecycle

The per-repo command lives on the `repos` row (`crates/db/src/models/repo.rs:47`):

```rust
pub dev_server_script: Option<String>,
```

The start endpoint (`crates/server/src/routes/workspaces/execution.rs:29-35`):

```rust
pub fn router() -> Router<DeploymentImpl> {
    Router::new()
        .route("/dev-server/start", post(start_dev_server))
        .route("/cleanup", post(run_cleanup_script))
        .route("/archive", post(run_archive_script))
        .route("/stop", post(stop_workspace_execution))
}
```

`start_dev_server` implements kill-then-start (`crates/server/src/routes/workspaces/execution.rs:44-85`):

```rust
let existing_dev_servers =
    match ExecutionProcess::find_running_dev_servers_by_workspace(pool, workspace.id).await {
        ...
    };

for dev_server in existing_dev_servers {
    ...
    if let Err(e) = deployment
        .container()
        .stop_execution(&dev_server, ExecutionProcessStatus::Killed)
        .await
    ...
}

let repos = WorkspaceRepo::find_repos_for_workspace(pool, workspace.id).await?;
let repos_with_dev_script: Vec<_> = repos
    .iter()
    .filter(|r| r.dev_server_script.as_ref().is_some_and(|s| !s.is_empty()))
    .collect();
```

Each qualifying repo becomes one script execution tagged `DevServer` with its working directory set to the repo name (`crates/server/src/routes/workspaces/execution.rs:103-125`):

```rust
let executor_action = ExecutorAction::new(
    ExecutorActionType::ScriptRequest(ScriptRequest {
        script: repo.dev_server_script.clone().unwrap(),
        language: ScriptRequestLanguage::Bash,
        context: ScriptContext::DevServer,
        working_dir: Some(repo.name.clone()),
    }),
    None,
);

let execution_process = deployment
    .container()
    .start_execution(
        &workspace,
        &session,
        &executor_action,
        &ExecutionProcessRunReason::DevServer,
    )
    .await?;
```

The `DevServer` variant is one of five run reasons (`crates/db/src/models/execution_process.rs:50-59`):

```rust
pub enum ExecutionProcessRunReason {
    SetupScript,
    CleanupScript,
    ArchiveScript,
    CodingAgent,
    DevServer,
}
```

Liveness queries filter on the serialized `'devserver'` value: running dev servers (`crates/db/src/models/execution_process.rs:311-342`), workspaces-with-dev-servers for sidebar badges (`crates/db/src/models/execution_process.rs:661`), and the complementary "anything running except dev servers" guard used by cleanup/archive/stop flows (`crates/db/src/models/execution_process.rs:292-309`). The frontend mirrors this split with `filterRunningDevServers` / `filterDevServerProcesses` plus working-directory deduplication, and start/stop mutations against `POST .../dev-server/start` and per-process stop (`packages/web-core/src/features/workspace/model/hooks/usePreviewDevServer.ts:19-94`). Dev servers do not survive restarts and must be started again (`docs/workspaces/interface.mdx:80`, `docs/browser-testing.mdx:26-38`).

## 4. The built-in browser: what it can do

The presentational component declares the full control surface as props (`packages/ui/src/components/PreviewBrowser.tsx:46-92`): `url`, `autoDetectedUrl`, URL-bar state and submit/clear/copy/open/refresh handlers, `onStart`/`onStop` with `isStarting`/`isStopping`/`isServerRunning`, `showIframe`, `screenSize` plus responsive dimensions and resize handlers, `repos` plus edit/fix-script handlers, `iframeRef`, `navigation` state with back/forward, `isInspectMode` toggle, `isErudaVisible` toggle, and iframe-load callbacks.

### 4.1 Navigation without reloads

Because the iframe is cross-origin (proxy host), the parent cannot touch `iframe.contentWindow.location` directly. Instead the injected `devtools_script.js` maintains a history stack in `sessionStorage` keyed by a `_refresh` query param, reports `navigation`/`ready` messages, and obeys `navigate` commands (`crates/preview-proxy/src/devtools_script.js:1-15`, `packages/web-core/src/shared/types/previewDevTools.ts:36-43`):

```ts
export interface NavigationCommand {
  source: PreviewDevToolsSource;
  type: 'navigate';
  payload: {
    action: 'back' | 'forward' | 'refresh' | 'goto';
    url?: string; // for 'goto' action
  };
}
```

The parent side is `PreviewDevToolsBridge`, which accepts messages only from the known iframe window and only with `source === 'vibe-devtools'`, and sends commands via `postMessage(command, '*')` (`packages/web-core/src/shared/lib/previewDevToolsBridge.ts:36-70`). The container documents the wiring explicitly (`packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:344-347`):

```ts
// The Rust proxy injects devtools_script.js into every iframe response.
// That script reports navigation events (URL changes, page ready) via postMessage.
// PreviewDevToolsBridge wraps the postMessage protocol for type-safe communication.
```

The toolbar exposes back/forward, URL bar with manual override, copy/open/refresh, and pause/resume (`docs/browser-testing.mdx:40-54`).

### 4.2 Device emulation

Three modes, persisted per workspace as scratch (`PREVIEW_SETTINGS`) data (`packages/web-core/src/shared/hooks/usePreviewSettings.ts:38-74`, `packages/web-core/src/shared/hooks/usePreviewSettings.ts:33-36`):

| Mode | Rendering | Source |
|---|---|---|
| Desktop | Full-width iframe | `packages/ui/src/components/PreviewBrowser.tsx:150-160` switch |
| Mobile | Fixed 390x844 phone frame with chrome and scaling | `packages/ui/src/components/PreviewBrowser.tsx:28-29` (`MOBILE_WIDTH = 390`, `MOBILE_HEIGHT = 844`) |
| Responsive | Draggable edges, default 800x600, min 320x480 | `packages/web-core/src/shared/hooks/usePreviewSettings.ts:33-36`, `packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:33-34` |

Docs describe the same three modes (`docs/browser-testing.mdx:56-76`, `docs/workspaces/interface.mdx:180-192`).

### 4.3 Inspect (click-to-component)

Inspect state is global Zustand (a lightweight React state container) store state (`packages/web-core/src/features/workspace-chat/model/store/useInspectModeStore.ts:1-23`):

```ts
export const useInspectModeStore = create<InspectModeState>((set) => ({
  isInspectMode: false,
  setInspectMode: (active) => set({ isInspectMode: active }),
  toggleInspectMode: () => set((s) => ({ isInspectMode: !s.isInspectMode })),
  pendingComponentMarkdown: null,
  ...
}));
```

The injected `click_to_component_script.js` arms a hover overlay and posts `source: 'click-to-component'` messages (`crates/preview-proxy/src/click_to_component_script.js:8-21`); selecting a component exits inspect mode and delivers component markdown into the chat as agent context. Framework adapters cover React, Vue, Svelte, Astro with an HTML fallback showing tag names when dev-build metadata is absent (`docs/browser-testing.mdx:78-87`, `docs/browser-testing.mdx:129-133`). The older companion-package flow (install `vibe-kanban-web-companion`, click the floating button, pick component depth) is the legacy variant of the same idea (`docs/core-features/testing-your-application.mdx:48-125`, `docs/core-features/testing-your-application.mdx:175-209`).

### 4.4 DevTools (Eruda)

Toggling the terminal icon shows an in-iframe Eruda panel with Console, Elements, Network, Resources, Sources, and Info tabs (`docs/browser-testing.mdx:88-107`). The proxy injects the CDN plus two local scripts before `</body>` (`crates/preview-proxy/src/lib.rs:603-618`); the init script starts Eruda dark-themed and hidden, hides its floating entry button, and listens for parent toggle commands (`crates/preview-proxy/src/eruda_init.js:16-30`). Because Eruda runs inside the iframe, it observes exactly what the app sees, including cookies and storage for the proxy origin.

## 5. Proxy transform details

Upstream URL construction strips the leading slash and reattaches path and query (`crates/preview-proxy/src/proxy_common.rs:37-55`):

```rust
pub(crate) fn build_local_upstream_url(
    scheme: &str,
    target_port: u16,
    path: &str,
    query: &str,
) -> String {
    let normalized_path = normalized_proxy_path(path);
    if normalized_path.is_empty() {
        if query.is_empty() {
            format!("{scheme}://localhost:{target_port}/")
        } else {
            format!("{scheme}://localhost:{target_port}/?{query}")
        }
    } else if query.is_empty() {
        format!("{scheme}://localhost:{target_port}/{normalized_path}")
    } else {
        format!("{scheme}://localhost:{target_port}/{normalized_path}?{query}")
    }
}
```

Request forwarding drops hop-by-hop and security-sensitive headers (`crates/preview-proxy/src/proxy_common.rs:3-26`):

```rust
pub(crate) const SKIP_REQUEST_HEADERS: &[&str] = &[
    "host",
    "connection",
    "transfer-encoding",
    "upgrade",
    "proxy-connection",
    "keep-alive",
    "te",
    "trailer",
    "sec-websocket-key",
    "sec-websocket-version",
    "sec-websocket-extensions",
    "accept-encoding",
    "origin",
    // Relay signing headers must not leak into preview dev servers. ...
    "x-vk-relayed",
    "x-vk-sig-session",
    "x-vk-sig-ts",
    "x-vk-sig-nonce",
    "x-vk-sig-signature",
];
```

Response processing strips framing-busters so the app can actually load in the iframe, at the cost of delegating framing policy to the proxy origin (`crates/preview-proxy/src/lib.rs:77-86`):

```rust
const STRIP_RESPONSE_HEADERS: &[&str] = &[
    "content-security-policy",
    "content-security-policy-report-only",
    "x-frame-options",
    "x-content-type-options",
    "transfer-encoding",
    "connection",
    "content-encoding",
];
```

`content-length` is additionally dropped for rewritten HTML (`crates/preview-proxy/src/lib.rs:106-127`); duplicate headers such as multiple `Set-Cookie` are preserved entry-wise (`crates/preview-proxy/src/lib.rs:104-127`).

Redirect handling keeps the user inside the proxy origin: absolute loopback `Location`/`Content-Location`/`Refresh`/any `*redirect*`/`*rewrite*` header pointing at the same dev port is rewritten to `{port}.localhost:{proxyPort}` (or `{port}--{hostId}.localhost` for relay targets), relative redirects pass through, non-loopback targets are untouched, and `Refresh: 0; url=...` is parsed and rewritten segment-wise (`crates/preview-proxy/src/lib.rs:234-364`). Next.js (a React full-stack framework) single-page-app redirects get two extra interceptions: a `200 + x-nextjs-redirect` on an `rsc` (React Server Components flight) request becomes a `307` with a `Location` header, and `NEXT_REDIRECT;{type};{url};{status};` digests embedded in flight-data bodies (capped at 1MB) become native redirect responses (`crates/preview-proxy/src/lib.rs:556-589`, `crates/preview-proxy/src/lib.rs:762-830`).

## 6. Security boundaries

| Boundary | Mechanism | Files |
|---|---|---|
| Process/origin isolation | Separate listener, port, and router for preview traffic; iframe loads `*.localhost:{proxyPort}`, never the app origin | `crates/server/src/main.rs:117-170`, `crates/server/src/startup.rs:19-56` |
| Cross-origin request policy | `validate_origin` layer on both the main API router and the proxy router; relay-signed requests bypass origin checks via their own session auth | `crates/server/src/routes/mod.rs:70-78`, `crates/server/src/middleware/origin.rs:41-82` |
| WebSocket auth shape | `/api/preview` WS upgrades go through `SignedWsUpgrade`, which is plain-local by default and relay-signed (or `401` on missing session) when a relay signature context is present | `crates/server/src/middleware/signed_ws.rs:33-72`, `crates/server/src/routes/preview.rs:25-65` |
| Iframe capability cap | `sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox allow-modals"` — scripts run, but top-navigation and most privilege escalation stays blocked | `packages/ui/src/components/PreviewBrowser.tsx:32-33` |
| Upstream credential hygiene | Relay `x-vk-sig-*` headers stripped before forwarding so a nested Vibe Kanban preview target does not mistake a preview fetch for a relay control request | `crates/preview-proxy/src/proxy_common.rs:17-26` |
| Framing policy trade-off | Upstream `Content-Security-Policy` (Content Security Policy, the page's allow-list for scripts/frames) / `X-Frame-Options` removed so arbitrary dev servers frame correctly; the proxy itself relies on subdomain-per-port isolation instead | `crates/preview-proxy/src/lib.rs:77-86` |
| Navigation confinement | Redirect/refresh rewrites pin loopback navigation to the proxy origin; self-port guards in the container refuse to proxy Vibe Kanban's own app or proxy ports (infinite-loop prevention) | `crates/preview-proxy/src/lib.rs:234-364`, `packages/web-core/src/pages/workspaces/PreviewBrowserContainer.tsx:289-305` |

Known limits worth stating plainly: `postMessage(command, '*')` trusts any parent/child holding a reference (`packages/web-core/src/shared/lib/previewDevToolsBridge.ts:65-70`, `crates/preview-proxy/src/devtools_script.js:9-15`); the Eruda CDN script loads from `cdn.jsdelivr.net` at injection time (`crates/preview-proxy/src/lib.rs:603-618`), so offline or CDN-compromised environments degrade or risk the preview context (not the app origin); stripped framing headers mean a malicious dev server renders with fewer browser guardrails inside its own isolated origin.

**Covers:** subdomain vs `/api/preview` request paths; main/proxy port allocation and log-scraped dev-port detection; kill-then-start dev-server lifecycle and `devserver` run-reason queries; PreviewBrowser toolbar, device modes, and per-workspace settings; navigation bridge, click-to-component inspect, and Eruda DevTools injection; header, redirect, and Next.js-RSC transforms; origin/sandbox/relay-signing security boundaries and known limits.
