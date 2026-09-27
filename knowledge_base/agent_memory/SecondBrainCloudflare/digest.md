> [[index|Wiki]] | [[summary|Summary]]
# rahilp/second-brain-cloudflare — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Second Brain is a persistent semantic memory system running as a Cloudflare Worker that lets every MCP-compatible AI tool share one personal-plus-team memory layer (01-overview.md:11-13, 01-overview.md:20-22).
## Key points
- Gives MCP-compatible AI tools (Claude, ChatGPT, Cursor, Codex) one persistent memory so context need not be repeated per app (01-overview.md:20-22).
- Runs in the user's own Cloudflare account on a Worker backed by D1, Vectorize, Workers AI, and KV, reached via REST or MCP (01-overview.md:47, 01-overview.md:74).
- Recalls by meaning (semantic) plus a full-text index for exact names, ticket numbers, versions, and phrases, with relevance ranking instead of scanning every memory (01-overview.md:41, 01-overview.md:82).
- Organizes on capture via automatic classification, duplicate detection, contradiction checks, relationships, and time-aware ranking, with optional weekly insights (01-overview.md:44, 01-overview.md:76-78).
- Separates visibility into a private Personal workspace and a Shared team layer (wire value `company`), private by default, shared only by deliberate move of one canonical memory (01-overview.md:55-57, 01-overview.md:106).
- Supports management from the dashboard (browse, edit, append, connect, share, export, permanently remove) and capture from MCP clients, CLI, browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts, or web dashboard (01-overview.md:43, 01-overview.md:45).
- Acts on dated memories with overdue/upcoming review and proactive push reminders via the installed PWA (01-overview.md:46).
## 2. [[wiki/02-top-level-files|Top-level-files]]
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
## The system in five moves
1. Every AI tool talks to one Cloudflare Worker in the user's own account instead of keeping its own separate memory.
2. Anything saved is classified, deduplicated, contradiction-checked, related, and indexed for semantic plus exact-phrase recall.
3. Memories stay private by default and reach the team only as one deliberately moved canonical memory on the Shared layer.
4. The Worker entry, D1/Vectorize/AI/KV bindings, five cron schedules, and the single AUTH_TOKEN secret pin the deployment shape.
5. Strict git/secret hygiene plus a leak-failing vitest harness with Worker-only stubs keeps credentials and memory dumps out of version control while keeping the pipeline testable.
