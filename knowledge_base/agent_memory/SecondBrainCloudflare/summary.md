# Technical Analysis: rahilp/second-brain-cloudflare

**Repository:** https://github.com/rahilp/second-brain-cloudflare
**Version analyzed:** 1.0.0 (from `package-lock.json`: `"name": "second-brain", "version": "1.0.0"` per 02-top-level-files.md:67; Team Edition feature scope discussed as v3.0.0 in 01-overview.md:29,68)
**Date:** 2026-09-26
**Wiki:** [[index]]

Source scope: this summary is grounded only in `wiki/01-overview.md` and `wiki/02-top-level-files.md` (the only two component pages present). Function-level `src/**/*.ts` detail, chunk files, clone, and web were not consulted per task constraints; gaps are stated explicitly rather than inferred.

## 1. Overview / What Problem It Solves

Problem space: AI tools (Claude, ChatGPT, Cursor, Codex) are stateless across sessions and siloed per application, forcing the user to re-supply decisions, preferences, project context, and commitments in every tool (01-overview.md:20-22). Adjacent symptoms are exact-keyword-only retrieval (fails on paraphrase but must still resolve ticket numbers, names, versions), scattered capture points (browser, notes, calendar, email, phone), and no shared team memory without leaking private notes (01-overview.md:41-46, 01-overview.md:53-59).

How the repo addresses it: a single Cloudflare Worker in the user's own account, backed by D1, Vectorize, Workers AI, and KV, exposes one memory layer over REST and MCP so every client reads and writes the same store with nothing to copy or synchronize (01-overview.md:42, 01-overview.md:47, 01-overview.md:74). On capture it classifies, deduplicates, contradiction-checks, relates, and indexes each memory; on recall it retrieves by semantic similarity plus a full-text relevance-ranked index and follows connections to return source-backed context (01-overview.md:44, 01-overview.md:76-78, 01-overview.md:82). Visibility is split into a private Personal workspace and one Shared team layer (wire value `company`), private by default, shared only by deliberate move of a canonical memory (01-overview.md:55-57, 01-overview.md:106). Dated memories support overdue/upcoming review with proactive push reminders via the installed PWA; management (browse, edit, append, connect, share, export, permanent remove) is via the dashboard (01-overview.md:43, 01-overview.md:46).

Primary user: an individual developer/knowledge worker operating across multiple AI clients and devices who also participates in a small team sharing one team layer, and who wants the infrastructure (memories, vectors, credentials) to live in their own Cloudflare account rather than a vendor SaaS (01-overview.md:47, 01-overview.md:53-55).

## 2. High-Level Architecture

```
MCP clients (Claude/ChatGPT/Cursor/Codex) ─┐
CLI (`brain`) / browser ext / Obsidian /   │
Notion / calendars / email / iOS Shortcuts │
/ web dashboard / PWA                       │
                    │ REST + MCP
                    ▼
         Cloudflare Worker (`src/index.ts`)
          │ MCP+REST routing │ scheduled()
          ├──────────────────┤
    ┌─────┼─────┬────────────┼──────┐
    ▼     ▼     ▼            ▼      ▼
   D1  Vectorize Workers AI KV    Assets
 (DB)  (vectors) (embed/   (OAuth (./public
  `DB`  `VECTORIZE` reason) `OAUTH_KV` dashboard)
                    │ AI
                    ▼
         Nightly/hourly/weekly crons
         (maintenance, mirror, insights)
```

Component roles (per 01-overview.md:74, 02-top-level-files.md:94-104): `src/index.ts` is the Worker entry (`wrangler.jsonc:53`, `wrangler.jsonc:552-557`); D1 binding `DB` (`second-brain-db`) is the system of record; Vectorize binding `VECTORIZE` (`second-brain-vectors`) holds semantic indexes with degraded-mode fallback; `AI` binding provides Workers AI (embeddings/reasoning); `OAUTH_KV` holds OAuth/session state; `./public` serves dashboard assets.

Data-flow narrative:

1. **Capture.** Any connected client submits a decision, preference, update, note, or source via `remember`/`append`/`update`, CLI, or dashboard (01-overview.md:76).
2. **Organize.** The Worker classifies the memory, checks duplicates and contradictions, creates relationships, and writes D1 rows plus semantic (Vectorize) and full-text index entries (01-overview.md:76-78, 01-overview.md:82).
3. **Recall.** A natural-language query is embedded, matched semantically and by full-text relevance ranking, expanded across useful connections, and returned as source-backed context or as a deterministic Prompt Capsule projection (01-overview.md:76-78, 01-overview.md:128-131).
4. **Manage/share.** Dashboard and `share`/`set_status`/`link`/`forget` operations mutate lifecycle (draft/canonical/deprecated) and move one canonical memory between Personal and Shared layers (01-overview.md:43, 01-overview.md:56-57).
5. **Act.** Dated memories surface in overdue/upcoming review; the installed PWA pushes reminders when items become due (01-overview.md:46).
6. **Maintain.** Five cron triggers run nightly maintenance (compression, graph pass, staleness pass), hourly integration mirror (one provider per run), nightly insight accrual, and weekly personal/team insight reasoning (02-top-level-files.md:105-113).

Persistent state lives in the user's own Cloudflare account: D1 (`second-brain-db`), Vectorize (`second-brain-vectors`), KV (`OAUTH_KV`), plus local-excluded SQLite/D1-export artifacts (`*.sqlite`, `*.db`, D1 exports ignored per 02-top-level-files.md:31) (01-overview.md:47).

## 3. Memory: The Core Abstraction

Representation: a memory is a content unit with lifecycle status, tenancy/project/facet/provenance axes, timestamped updates, and explicit graph edges. Four axes are named in 01-overview.md:114: `workspace` (tenancy: who can see it — `personal` / `company` / `team`), `project` (named managed container, what it is about), `tags` (free-form facets), `source` (where it came from). Lifecycle states set via `set_status` are `canonical`, `draft`, `deprecated` (01-overview.md:49). Updates are either timestamped appends (`append`) or full replacement (`update`); explicit edges are created/removed/listed via `link` / `unlink` / `connections` (01-overview.md:38-54).

Named kinds/types with file:line-anchored evidence (citations refer to wiki chunk lines that quote the source):

- Workspace layers: `personal` (only the owner reads/edits) vs Shared (everyone on the team reads; author or admin edits/deletes/un-shares); wire value for Shared is `company` (01-overview.md:24-28, 01-overview.md:55-57, 01-overview.md:106).
- Project containers: discoverable via `list_projects` (display names, descriptions, memory counts); a memory may belong to one or more projects; projects preferred over bare topic tags (01-overview.md:45, 01-overview.md:57).
- Prompt Capsule entries: ordinary canonical memories carrying one target tag (`capsule:core` or `capsule:project:<project-slug>`) plus one slot tag of form `capsule-slot:<slot>`; core slots are `identity`, `preferences`, `constraints`, `principles`; project slots are `current-state`, `decisions`, `open-questions`; at most one canonical entry per slot (01-overview.md:133-144).
- Tag/status discipline: `status:canonical` requested via tags at capture time (whitespace-trimmed, left alone by classifier; otherwise starts as draft); writes contradicting a protected memory are demoted to draft; removal from a capsule means demotion to draft/deprecated; capture/update accept at most 64 tags of 128 characters each (01-overview.md:146-158).

Key queries: semantic `recall` ("find the right memory even when you used different words when saving it" — 01-overview.md:41) combined with a full-text relevance-ranked index for exact names/phrases without scanning every memory (01-overview.md:41, 01-overview.md:82). Verbatim pipeline statement:

> "classifies it, checks for duplicates and contradictions, creates relationships, and indexes it for semantic search." (01-overview.md:76-78)

> "Ask in natural language … retrieves relevant memories, follows useful connections, and returns source-backed context." (01-overview.md:76-78)

Layer routing verbatim: captures default per member/team settings while "recall searches everything the person may see" unless `workspace` (`personal`|`company`) is explicit (01-overview.md:106).

## 4. LLM / External Service Integration

The repo calls both a built-in LLM/embedding provider and third-party capture sources; it is not LLM-free.

- **Compute/inference provider:** Cloudflare Workers AI via the `ai` → `AI` binding declared in `wrangler.jsonc` (02-top-level-files.md:94-104). Roles evidenced in overview: embeddings for semantic index/recall, classification/duplicate/contradiction/relationship passes, and weekly insight reasoning (01-overview.md:44, 01-overview.md:74-78). Degraded mode is explicit: if Vectorize is unavailable, captures and keyword recall keep working while semantic indexing is restored; shipped embedding models "read English best" with a multilingual switch in the desktop app Settings (01-overview.md:80). Exact model IDs and per-call required/optional matrix are not stated in the two available component pages.
- **Vector/search/storage:** Vectorize (`VECTORIZE` → `second-brain-vectors`), D1 (`DB` → `second-brain-db`), KV (`OAUTH_KV`) (02-top-level-files.md:94-104). Full-text index upgrade is automatic for new installs; existing brains backfill over nightly runs with no client update (01-overview.md:82).
- **Auth:** `workers-oauth-provider` dependency plus `OAUTH_KV`; `cloudflare:sockets` and `agents/mcp` appear as Worker-only imports stubbed in tests (02-top-level-files.md:11-12, 02-top-level-files.md:92).
- **Capture/integration sources:** MCP clients, CLI, browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts, web dashboard (01-overview.md:45). Syntactic evidence for two: `ical.js` (calendars) and `postal-mime` (email parsing) in dependencies (02-top-level-files.md:49-66). Hourly mirror sync runs one provider per run (02-top-level-files.md:105-113).
- **Env vars / secrets:**

| Name | Required? | Purpose / evidence |
|---|---|---|
| `AUTH_TOKEN` | Required (`wrangler.jsonc` `secrets.required`, 02-top-level-files.md:6) | Bearer auth for Worker; local shape `AUTH_TOKEN=your_memorable_token_here` (02-top-level-files.md:14-19) |
| `VECTORIZE_GRACE_MS` | Set, default `"300000"` (`wrangler.jsonc` vars, 02-top-level-files.md:6) | Grace window for Vectorize degraded-mode behavior |
| `INSIGHT_*` / `TEAM_INSIGHTS` / cron-match constants | Config-level | `INSIGHT_ACCRUAL_CRON`, `INSIGHT_WEEKLY_CRON`, `INSIGHT_TEAM_WEEKLY_CRON` in `src/insight/schedule.ts` must match wrangler crons; `INTEGRATION_SYNC_CRON` in `src/integrations/mirror.ts` must match hourly entry; `TEAM_INSIGHTS` gates team reasoning off by default (02-top-level-files.md:105-113) |

## 5. Capture → Organize → Recall: The Main Pipeline

Primary workflow is Capture → Organize → Recall (plus Manage/Act/Maintain), per 01-overview.md:31-35. Function-level `src/*.ts:line` mapping is not present in the two available component pages (they cover README-level behavior and root config only), so steps below cite the pipeline and scheduling evidence that is available; exact handler/function names must be read from `src/` directly.

1. **Capture — save from any client.** "Save a decision, preference, project update, note, or source from any connected client" (01-overview.md:31-35). Entry points: `remember` (store), `append` (timestamped update), `update` (replace), plus CLI/dashboard/integrations (01-overview.md:38-54, 01-overview.md:45). Layer routing: optional `workspace` (`personal`|`company`); optional `team` workspace id wired for future multi-team; `list_teams` / `GET /team/workspaces` exist but dashboard flows do not create/switch teams in v3.0.0 scope (01-overview.md:55, 01-overview.md:68).
2. **Organize — classify, deduplicate, relate, index.** "classifies it, checks for duplicates and contradictions, creates relationships, and indexes it for semantic search" (01-overview.md:31-35). New installs index to the full-text relevance index immediately; existing brains backfill over nightly runs (`0 1 * * *` maintenance: compression, graph pass, staleness pass) (01-overview.md:82, 02-top-level-files.md:105-113). Tag/status rules (canonical-vs-draft, contradiction demotion, 64×128 tag limits) apply here (01-overview.md:146-158).
3. **Recall — semantic + full-text + graph expansion.** "Ask in natural language … retrieves relevant memories, follows useful connections, and returns source-backed context" (01-overview.md:31-35). Tools: `recall`, `get` (by ID), `list_recent`, `connections`, project-scoped recall (`--project`), and `get_prompt_capsule` deterministic projections with ETag/12,000-char budget semantics (01-overview.md:38-54, 01-overview.md:57-64).
4. **Manage — lifecycle and sharing.** `set_status` (`canonical`/`draft`/`deprecated`), `link`/`unlink`, `share` (moves one canonical memory between Personal and Shared, author-visible, author-or-admin mutable), `forget` (permanent delete), dashboard browse/edit/append/connect/share/export/remove (01-overview.md:38-54, 01-overview.md:43, 01-overview.md:56-57).
5. **Act/maintain — reminders and scheduled passes.** Dated memories feed overdue/upcoming review with PWA push (01-overview.md:46); scheduled jobs (`scheduled()` in `src/index.ts` routing on cron string) run maintenance, hourly mirror, insight accrual, and weekly reasoning, guarded by `test/unit/cron-triggers.test.ts` (02-top-level-files.md:105-113).

## 6. Key Files

Ordered by structural importance; `src/` internals below are those named inside the two component pages — the pages do not enumerate the full tree.

| File | Lines | What It Does |
|---|---|---|
| `src/index.ts` | not stated in pages | Worker entry (`main` in `wrangler.jsonc:552-557`); REST+MCP routing and `scheduled()` cron dispatch (02-top-level-files.md:94, 02-top-level-files.md:113) |
| `wrangler.jsonc` | ~623 lines (cited to :623) | Deployment: name/main/compat, D1+D3 Vectorize+AI+KV bindings, `AUTH_TOKEN` requirement, `VECTORIZE_GRACE_MS`, assets, five cron triggers with two-budget rationale (02-top-level-files.md:4-6, 02-top-level-files.md:93-113) |
| `db/schema.sql` | not stated | Canonical D1 schema; sole tracked `*.sql` (all others ignored) (02-top-level-files.md:9, 02-top-level-files.md:31) |
| `src/insight/schedule.ts` | not stated | Insight cron constants (`INSIGHT_ACCRUAL_CRON`, `INSIGHT_WEEKLY_CRON`, `INSIGHT_TEAM_WEEKLY_CRON`) that must match wrangler entries (02-top-level-files.md:105-113) |
| `src/integrations/mirror.ts` | not stated | Integration mirror; `INTEGRATION_SYNC_CRON` must match hourly entry exactly (02-top-level-files.md:113) |
| `package-lock.json` | 212k+ chars (truncated at chunk line 407) | Pins `second-brain@1.0.0`, 8 runtime + 7 dev deps (02-top-level-files.md:11, 02-top-level-files.md:49-67) |
| `vitest.config.ts` | cited to :456 | Test harness: node env, 30 s timeout, global setup/setup files, `.worktrees/**` exclusion, v8 coverage over `src/**/*.ts` + `public/utils.js` (02-top-level-files.md:87-88) |
| `vitest.global-setup.ts` | cited to :478 | Run-level temp-leak guard (`SB_TEST_TMP_ROOT` + `TMPDIR` override) (02-top-level-files.md:12, 02-top-level-files.md:87-92) |
| `vitest.setup.ts` | cited to :544 | Per-file temp-leak guard; stubs for `agents/mcp`, `cloudflare:sockets`, `@cloudflare/workers-oauth-provider` (02-top-level-files.md:12, 02-top-level-files.md:87-92) |
| `test/unit/cron-triggers.test.ts` | not stated | Guards wrangler↔source cron-string equality (02-top-level-files.md:113) |
| `test/unit/repo-hygiene.test.ts` | not stated | Guards `.gitignore` symlink/negation behavior (02-top-level-files.md:28) |
| `public/utils.js` | not stated | Dashboard asset covered by coverage include (02-top-level-files.md:88) |
| `.dev.vars.example` | 9 lines | Local secret template (`AUTH_TOKEN`) (02-top-level-files.md:7, 02-top-level-files.md:14-19) |
| `.gitignore` | cited to :97 | Slashless matching, re-inclusions, SQLite/D1-export/`.eval-cache/`/`devharness/`/per-env wrangler hygiene (02-top-level-files.md:8-9, 02-top-level-files.md:26-31) |
| `.gitattributes` | cited to :37 | LF enforcement + binary flags (02-top-level-files.md:10, 02-top-level-files.md:20-25) |
| `tsconfig.json` | cited head | Strict TS ES2022/bundler config over `src`, `test`, setup files (02-top-level-files.md:68-86) |
| `.mcp.json` / `.npmrc` | tiny | MCP gateway (`gw mcp`) and `legacy-peer-deps=true` (02-top-level-files.md:32-47) |

## 7. Dependencies

Exact constraint strings from `package-lock.json:131-149` via 02-top-level-files.md:49-66. Required (runtime) first, then dev.

| Package | Version constraint | Purpose |
|---|---|---|
| @cloudflare/workers-oauth-provider | ^0.8.2 | OAuth gating for Worker API routes (stubbed in tests) |
| @modelcontextprotocol/client | ^2.0.0 | MCP client interop |
| @modelcontextprotocol/sdk | ^1.30.0 | MCP protocol SDK |
| @modelcontextprotocol/server | ^2.0.0 | MCP server (memory tools surface) |
| agents | ^0.20.1 | Cloudflare Agents runtime integration |
| ical.js | ^2.2.1 | Calendar ingest (capture source) |
| postal-mime | ^2.7.5 | Email parsing (capture source) |
| zod | ^4.4.3 | Schema validation |
| @huggingface/transformers | ^4.3.0 (dev) | Local/test embedding-related harness |
| @types/node | ^26.1.2 (dev) | Node typings for tests/tooling |
| @vitest/coverage-v8 | ^4.1.10 (dev) | Coverage provider |
| esbuild | ^0.28.1 (dev) | Build/bundling |
| typescript | ^7.0.2 (dev) | Typechecking (`tsconfig.json` strict ES2022) |
| vitest | ^4.1.10 (dev) | Test runner (30 s timeout, leak guards) |
| wrangler | ^4.114.0 (dev) | Worker deploy/config tooling |

Resolved-version/integrity rows beyond the lockfile head were truncated in the chunk and are not reproduced here (02-top-level-files.md:67).

## 8. CLI / Usage Surface

Entry points: Worker over REST and MCP (01-overview.md:74); CLI `brain`; web dashboard + installed PWA (push reminders); capture integrations (browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts) (01-overview.md:43-46).

Memory-tool commands (01-overview.md:38-54):

| Command/tool | Args/notes | Effect |
|---|---|---|
| `remember` | `project`, `workspace` (`personal`\|`company`), `team`, tags | Store idea/decision/preference/context |
| `append` | memory ID + text | Timestamped update to existing memory |
| `update` | memory ID; optional complete-replacement `tags` array | Replace memory; omitting `tags` preserves them |
| `recall` | natural-language query; `workspace`, `project` filters | Semantic + full-text relevance retrieval |
| `list_recent` | scope filters | Browse recently saved memories |
| `list_teams` | — | List shared teams (one team in v3.0.0) |
| `list_projects` | — | Projects with names/descriptions/counts |
| `get_prompt_capsule` | core or `project:<slug>` | Deterministic prompt-prefix projection |
| `get` | ID | Read one memory |
| `forget` | ID | Permanent delete |
| `set_status` | `canonical`\|`draft`\|`deprecated` | Lifecycle transition (incl. capsule publish/unpublish) |
| `link` / `unlink` | two memory IDs | Add/remove explicit relationship |
| `connections` | memory ID | List connected memories |
| `share` | memory ID + layer | Move canonical memory Personal↔Shared |

CLI examples (01-overview.md:57-62):

```bash
brain remember --workspace company "We ship on Thursdays"
brain recall --workspace company "when do we ship?"
brain recall --project website "what did we decide about hosting?"
```

REST surface named in pages: `GET|HEAD /prompt-capsules/core`, `GET|HEAD /prompt-capsules/projects/<project-slug>` (strong `ETag` over exact prompt-ready `text`; 12,000-char budget; `409 invalid_prompt_capsule` / `409 too_many_candidates` semantics), `GET /team/workspaces` (01-overview.md:64, 01-overview.md:55). Full route table is not in the available pages.

Env-var table: see §4 (`AUTH_TOKEN` required; `VECTORIZE_GRACE_MS="300000"`; insight/team cron constants).

Config surface (`wrangler.jsonc`): Worker `second-brain`, entry `src/index.ts`, compat `2026-06-17` + `nodejs_compat`, bindings D1/`DB`, Vectorize/`VECTORIZE`, AI/`AI`, KV/`OAUTH_KV`, assets `./public`, five crons (`0 1 * * *`, `30 * * * *`, `45 1 * * *`, `15 2 * * SUN`, `45 2 * * SUN`) (02-top-level-files.md:93-113). Test config: `vitest.config.ts` node env, 30 s timeout, leak-guard setup, v8 coverage (02-top-level-files.md:87-88).

## 9. Extensibility Points

Each item names the file/class area to extend; detail is limited to what the two pages evidence — consult `src/` for signatures.

- **New capture source / sync provider:** hourly mirror path — `src/integrations/mirror.ts` (`INTEGRATION_SYNC_CRON` must keep matching the `30 * * * *` wrangler entry); one provider per run by design (02-top-level-files.md:105-113). Dependency precedents: `ical.js` for calendars, `postal-mime` for email (02-top-level-files.md:49-66).
- **New scheduled/maintenance pass:** `src/index.ts` `scheduled()` router + `wrangler.jsonc` cron list; nightly `0 1 * * *` covers compression/graph/staleness, but free-plan ceiling is five triggers and the two-budget D1/CPU rationale constrains packing more work into one invocation (02-top-level-files.md:105-113).
- **New insight/reasoning cadence:** `src/insight/schedule.ts` constants (`INSIGHT_ACCRUAL_CRON`, `INSIGHT_WEEKLY_CRON`, `INSIGHT_TEAM_WEEKLY_CRON`) plus `TEAM_INSIGHTS` gate; any cron-string change must update both sides, enforced by `test/unit/cron-triggers.test.ts` (02-top-level-files.md:105-113).
- **New memory tool / MCP surface:** MCP server layer (deps `@modelcontextprotocol/server`, `agents`); routing lives under the Worker entry `src/index.ts` (02-top-level-files.md:49-66, 02-top-level-files.md:94). Multi-team readiness hook already exists: optional `team` params + `list_teams` (01-overview.md:29, 01-overview.md:55).
- **New Prompt Capsule slot or namespace:** capsule convention (`capsule:core` / `capsule:project:<slug>` + `capsule-slot:<slot>`; fixed slot orders; canonical-only; duplicate/invalid reporting) — extension means adding a slot name and teaching the projection/validation path that enforces single-canonical-per-slot, budget omission, and ETag semantics (01-overview.md:63-64).
- **New project axis behavior / tag taxonomy:** `project` container + `tags`/`source`/`workspace` axes with `list_projects` discovery; prefer projects over bare topic tags (01-overview.md:57). Classifier interaction matters: it leaves explicit `status:canonical` tags whitespace-trimmed and alone, and `/classify-pending` never publishes a capsule (01-overview.md:64).
- **Test-harness-safe Worker-only imports:** extend stubs in `vitest.setup.ts` (`agents/mcp`, `cloudflare:sockets`, `@cloudflare/workers-oauth-provider`) and respect temp-leak guards (`vitest.global-setup.ts`, `vitest.setup.ts`) when adding file-creating tests (02-top-level-files.md:87-92).

## 10. Limitations and Gotchas

- **Single shared team in v3.0.0.** Each brain has one shared team; `team` params and `list_teams` / `GET /team/workspaces` are wired for a future multi-team release but dashboard/admin flows neither create nor switch teams yet (01-overview.md:29, 01-overview.md:55).
- **Vectorize outage degrades recall; embeddings skew English.** If Vectorize is unavailable, capture and keyword recall continue but semantic indexing waits for restoration; shipped embedding models "read English best" (multilingual switch lives in the desktop app Settings) (01-overview.md:35).
- **Free-plan ceilings shape scheduling.** Five cron triggers is the free-plan maximum and the file documents a two-invocation budget rationale (50 D1 queries / 10 ms CPU per invocation; nightly pass spends ~30, so mirror sync needs its own run) — adding jobs means merging or upgrading, not appending (02-top-level-files.md:4, 02-top-level-files.md:105-113).
- **Prompt Capsule budgets and strict validation lose data silently-by-design.** 12,000-character budget with whole-slot omission (over-budget slot plus all later slots dropped); 200-candidate cap returns `409 too_many_candidates`; oversized personal entry returns `409 invalid_prompt_capsule` while shared oversized entries are skipped/reported; draft/deprecated, ambiguous-slot, and malformed entries are ignored or omitted with `complete: false` (01-overview.md:64).
- **Sharing and capsule edits have sharp edges.** `share` moves one canonical memory (not a copy) with author visible; only author or admin can edit/delete/un-share; members cannot edit a teammate's shared capsule entry (must ask author/admin to re-slot or unpublish); dashboard hides bookkeeping tags so capsule debugging requires MCP; `update` without `tags` preserves tags while naming a capsule namespace replaces both (01-overview.md:23, 01-overview.md:64).
- **Cron-string coupling is brittle.** `scheduled()` routes on literal cron strings; `INSIGHT_*` / `INTEGRATION_SYNC_CRON` constants must match `wrangler.jsonc` exactly, including `SUN` instead of numeric `0` which Cloudflare rejects; the guard is `test/unit/cron-triggers.test.ts` (02-top-level-files.md:105-113).
- **Tag/status discipline is unforgiving.** At most 64 tags of 128 chars on capture/update; writes contradicting a protected memory are demoted to draft even when canonical was requested; lone slot tags are incomplete; `/classify-pending` never publishes (01-overview.md:64).
- **Coverage gap in this summary's sources.** Only root config and README-level overview pages were available; `src/` handler names, D1 schema columns, embedding model IDs, and the full REST route table are not evidenced here and must be verified in the repo before building on them.

## 11. How It Compares to Alternatives

- **Mem0 (mem0ai/mem0).** Hosted + self-hostable memory layer with entity/graph extraction APIs for agents. Second-brain differs by running entirely on the user's Cloudflare primitives (Worker+D1+Vectorize+KV) with a Personal/Shared tenancy model and a dashboard/PWA surface instead of a vendor-hosted memory API.
- **Zep / Graphiti (getzep/zep).** Temporal knowledge-graph memory with hybrid search for agents. Second-brain overlaps on semantic+full-text+graph-expansion recall but centers on cross-tool MCP reuse, dated commitments with push reminders, and deterministic Prompt Capsule projections rather than a standalone temporal-graph service.
- **Letta (letta-ai/letta, formerly MemGPT).** Agent framework with self-editing archival/recall memory inside the agent loop. Second-brain is client-agnostic infrastructure: memory lives outside any single agent framework and is shared across Claude/ChatGPT/Cursor/Codex via MCP/REST.
- **Obsidian / Notion (as personal knowledge bases).** File/database-centric note systems with plugins and AI features. Second-brain treats them as capture sources (Obsidian, Notion listed as inputs) and adds cross-client semantic recall, team-layer sharing, and scheduled insight passes on top, at the cost of operating a Worker + Cloudflare bindings instead of plain local files.

Positioning: second-brain is the self-hosted-on-Cloudflare, MCP-first shared memory substrate for people already spread across many AI tools — narrower than a full PKM suite, more deployment-coupled than a memory API, chosen when one tenancy-aware semantic layer with dashboard control and push-acted commitments matters more than framework-embedded memory or plain notes.

## Appendix: Selected Code Snippets

1. Local secret template — `.dev.vars.example` (verbatim, 02-top-level-files.md:14-19):

```
AUTH_TOKEN=your_memorable_token_here
```

Range: `.dev.vars.example:9` (single meaningful line; tracked example while `.dev.vars` is git-ignored).

2. Line-ending + binary policy — `.gitattributes` head and binary list (verbatim, 02-top-level-files.md:20-25):

```
* text=auto eol=lf
```

Binary block flags each of `*.png *.jpg *.jpeg *.gif *.ico *.webp *.woff *.woff2 *.ttf *.eot *.pdf *.zip *.gz *.tar *.7z *.exe *.dll *.so *.dylib` as `binary` (`.gitattributes:19-37`).

3. MCP and npm config — `.mcp.json` and `.npmrc` (verbatim, 02-top-level-files.md:32-47):

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

```
legacy-peer-deps=true
```

Ranges: `.mcp.json` full file; `.npmrc` full file.

4. TypeScript strict config — `tsconfig.json` (verbatim options, 02-top-level-files.md:68-86):

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

Range: `tsconfig.json` full file as quoted in 02-top-level-files.md:68-86.
