[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo root files define the Worker's deployment bindings and schedules, the Node/TypeScript/test harness configuration, and the git/secret hygiene rules that keep memories and credentials out of version control.
## Key points
- `wrangler.jsonc` declares the Worker entry `src/index.ts` with D1, Vectorize, AI, and KV bindings plus five cron triggers that are the free-plan maximum (wrangler.jsonc:53, wrangler.jsonc:58-77, wrangler.jsonc:596-623).
- `wrangler.jsonc` requires the `AUTH_TOKEN` secret and sets `VECTORIZE_GRACE_MS` to `"300000"` (wrangler.jsonc:578-582).
- `.dev.vars.example` shows the only local secret shape: `AUTH_TOKEN=your_memorable_token_here` (.dev.vars.example:9).
- `.gitignore` deliberately uses slashless `node_modules`, `docs/*`, and `.cursor/**` patterns with re-inclusions so symlinks, nested rules, and the two tracked docs/memory files behave correctly (.gitignore:45-66).
- `.gitignore` blocks all `*.sql` except `db/schema.sql`, all SQLite artifacts, D1 exports, `.eval-cache/`, `devharness/`, and per-environment `wrangler.*.jsonc` (`.gitignore`:70-97).
- `.gitattributes` forces LF line endings via `* text=auto eol=lf` and marks binary extensions (png/jpg/pdf/zip/exe/so and others) as binary (.gitattributes:16, .gitattributes:19-37).
- `package-lock.json` pins `second-brain@1.0.0` with 8 runtime deps (workers-oauth-provider, MCP client/sdk/server, agents, ical.js, postal-mime, zod) and 7 dev deps (transformers, types/node, coverage-v8, esbuild, typescript, vitest, wrangler); full listing was truncated in the chunk (package-lock.json:123-149).
- The vitest harness fails the run on leaked temp dirs at both run level (`vitest.global-setup.ts`) and per-file level (`vitest.setup.ts`), and stubs `agents/mcp`, `cloudflare:sockets`, and `@cloudflare/workers-oauth-provider` so Worker-only imports load under node (vitest.global-setup.ts:470-478, vitest.setup.ts:507-544).
---
## Secrets template (.dev.vars.example)
Verbatim content:
```
AUTH_TOKEN=your_memorable_token_here
```
This is the local-dev counterpart of the required secret declared in `wrangler.jsonc:582` (`"secrets": {"required": ["AUTH_TOKEN"]}`); the example file itself is tracked while `.dev.vars` is ignored (`.gitignore`:67).
## Git line endings and binaries (.gitattributes)
Verbatim head:
```
* text=auto eol=lf
```
Binary block (verbatim list): `*.png *.jpg *.jpeg *.gif *.ico *.webp *.woff *.woff2 *.ttf *.eot *.pdf *.zip *.gz *.tar *.7z *.exe *.dll *.so *.dylib` each flagged `binary` (.gitattributes:19-37).
## Ignore rules (.gitignore)
Slashless-vs-slashed distinctions with verbatim rationale from the file:
- `node_modules` (no trailing slash) so a worktree symlink (mode-120000 blob) is still matched; guard is `test/unit/repo-hygiene.test.ts` (.gitignore:45-50).
- `docs/*` (not `docs/`) so the negations `!docs/dashboard-architecture.md` can re-include; same pattern for `.cursor/**` + `!.cursor/rules/` + `!.cursor/rules/second-brain-memory.mdc` (.gitignore:55-66).
- Ignored local-only items: `coverage/`, `.wrangler/`, `.wrangler-dry-run/`, `.worktrees/`, `.claude/`, `.dev.vars`, `.env`, `worker-configuration.d.ts`, `wrangler.*.jsonc`, `deploy-personal.sh`, `devharness/` (.gitignore:51-77).
- Memory-safety block: `*.sql` except `!db/schema.sql`; `*.sqlite *.sqlite3 *.db *.db-wal *.db-shm`; `.eval-cache/` (.gitignore:79-97).
## MCP and npm config (.mcp.json, .npmrc)
Verbatim `.mcp.json`:
```json
{
  "mcpServers": {
    "gw": {
      "command": "gw",
      "args": ["mcp"]
    }
  }
}
```
Verbatim `.npmrc`:
```
legacy-peer-deps=true
```
## Packaging (package.json data via package-lock.json)
Exact pinned dependencies (chunk lines 131-149):
| Scope | Package | Range |
|---|---|---|
| dependencies | @cloudflare/workers-oauth-provider | ^0.8.2 |
| dependencies | @modelcontextprotocol/client | ^2.0.0 |
| dependencies | @modelcontextprotocol/sdk | ^1.30.0 |
| dependencies | @modelcontextprotocol/server | ^2.0.0 |
| dependencies | agents | ^0.20.1 |
| dependencies | ical.js | ^2.2.1 |
| dependencies | postal-mime | ^2.7.5 |
| dependencies | zod | ^4.4.3 |
| devDependencies | @huggingface/transformers | ^4.3.0 |
| devDependencies | @types/node | ^26.1.2 |
| devDependencies | @vitest/coverage-v8 | ^4.1.10 |
| devDependencies | esbuild | ^0.28.1 |
| devDependencies | typescript | ^7.0.2 |
| devDependencies | vitest | ^4.1.10 |
| devDependencies | wrangler | ^4.114.0 |
Package identity: `"name": "second-brain", "version": "1.0.0", "lockfileVersion": 3` (package-lock.json:123-126). The chunk truncates the lockfile body at chunk line 407 (`... (truncated, 212459 more characters)`); per-file resolved/integrity entries beyond the head were cut, so they are not summarised here.
## TypeScript config (tsconfig.json)
Verbatim options:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ES2022",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "allowJs": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["worker-configuration.d.ts", "src/**/*.ts", "test/**/*.ts", "vitest.setup.ts"],
  "exclude": ["node_modules"]
}
```
## Test harness (vitest.config.ts, vitest.global-setup.ts, vitest.setup.ts)
Exact settings in `vitest.config.ts`: `environment: "node"`, `globals: true`, `testTimeout: 30_000`, `globalSetup: ["./vitest.global-setup.ts"]`, `setupFiles: ["./vitest.setup.ts"]`, `exclude: [...configDefaults.exclude, ".worktrees/**"]`, coverage `provider: "v8"`, `include: ["src/**/*.ts", "public/utils.js"]`, `reporter: ["text", "html", "json-summary", "json"]`, `reportsDirectory: "coverage"` (vitest.config.ts:436-456). The 30 s timeout comment notes sqlite-backed corpus / eval CLI tests timed out at 5 s on CI (vitest.config.ts:439-441).
Temp-leak guards (verbatim error strings):
- Run level: `the test run leaked ${left.length} temp entries (first: ...)` via `SB_TEST_TMP_ROOT` + `TMPDIR` override (vitest.global-setup.ts:470-478).
- File level: `this file leaked ${left.length} temp entries (first: ...); remove what a test creates in afterEach/afterAll or a finally` (vitest.setup.ts:498-504).
Module stubs in `vitest.setup.ts` (verbatim targets): `vi.mock("agents/mcp", ...)` returning `() => new Response("mcp")`; `vi.mock("cloudflare:sockets", ...)` whose `connect()` throws `cloudflare:sockets connect() is not available in tests`; `vi.mock("@cloudflare/workers-oauth-provider", ...)` with a minimal `OAuthProvider` router gating `apiRoute` on `resolveExternalToken` and returning 401 `{"error": "Unauthorized"}` otherwise (vitest.setup.ts:507-544).
## Worker deployment config (wrangler.jsonc)
Exact identity and entry: `"name": "second-brain"`, `"main": "src/index.ts"`, `"compatibility_date": "2026-06-17"`, `"compatibility_flags": ["nodejs_compat"]` (wrangler.jsonc:552-557).
Bindings table:
| Type | Binding | Target |
|---|---|---|
| d1_databases | DB | second-brain-db |
| vectorize | VECTORIZE | second-brain-vectors |
| ai | AI | (binding only) |
| kv_namespaces | OAUTH_KV | (binding only) |
| vars | VECTORIZE_GRACE_MS | "300000" |
| secrets.required | AUTH_TOKEN | (required) |
| assets.directory | — | ./public |
Cron triggers (verbatim, five entries — the free-plan maximum):
| Cron | Purpose per inline comments |
|---|---|
| `0 1 * * *` | Nightly maintenance: compression, graph pass, staleness pass |
| `30 * * * *` | Integrations (hourly; one provider per run; offset to :30) |
| `45 1 * * *` | Insight candidate accrual (`INSIGHT_ACCRUAL_CRON` in src/insight/schedule.ts must match) |
| `15 2 * * SUN` | Weekly insight reasoning (`INSIGHT_WEEKLY_CRON` must match; `SUN` not `0` — Cloudflare rejects numeric form) |
| `45 2 * * SUN` | Weekly TEAM insight reasoning (`INSIGHT_TEAM_WEEKLY_CRON` must match; off by default via TEAM_INSIGHTS) |
The two-budget rationale is verbatim in the file: a free-plan invocation gets 50 D1 queries and 10 ms CPU; the nightly pass spends ~30, so the mirror sync needs its own invocation; `scheduled()` in `src/index.ts` routes on the cron string and `INTEGRATION_SYNC_CRON` in `src/integrations/mirror.ts` must match the second entry exactly, guarded by `test/unit/cron-triggers.test.ts` (wrangler.jsonc:587-594).
**Covers:** .dev.vars.example, .gitattributes, .gitignore, .mcp.json, .npmrc, package-lock.json (truncated in chunk), tsconfig.json, vitest.config.ts, vitest.global-setup.ts, vitest.setup.ts, wrangler.jsonc
