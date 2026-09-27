---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: rahilp/second-brain-cloudflare

### Q1. What problem does Second Brain solve for users of MCP-compatible AI tools?
> [!tip]- Answer
> It gives every MCP-compatible AI tool (Claude, ChatGPT, Cursor, Codex) one shared persistent memory, so context no longer has to be repeated per app.
> Every client talks to the same Cloudflare Worker, so there is nothing to copy or synchronize between apps and devices.
> See [[wiki/01-overview|Overview]].

### Q2. How does Second Brain's recall combine semantic search with full-text search?
> [!tip]- Answer
> Recall works by meaning, finding the right memory even when the question uses different words than were saved, plus a full-text index for exact names, ticket numbers, versions, and phrases.
> Results use relevance ranking instead of scanning every memory, and existing brains build the full-text index over nightly runs with no client update needed.
> If Vectorize is unavailable, captures and keyword recall keep working in degraded mode while semantic indexing is restored.
> See [[wiki/01-overview|Overview]].

### Q3. How do the Personal and Shared visibility layers work, including the wire value and share semantics?
> [!tip]- Answer
> Each person keeps a Personal workspace readable only by them, plus one Shared team layer whose wire value is `company`; memories stay private by default.
> Sharing deliberately moves one canonical memory (not a copy) into Shared with the author visible, and only the author or an admin can edit, delete, or un-share it.
> Without an explicit `workspace`, captures use member/team defaults while recall searches everything the person may see.
> See [[wiki/01-overview|Overview]].

### Q4. What are Prompt Capsules and what rules govern their slots and publication?
> [!tip]- Answer
> Prompt Capsules are deterministic, read-only context projections for gateways and custom agents that sit before a changing user request; core entries use `capsule:core` and project entries use `capsule:project:<project-slug>`, with fixed slot orders (core: identity, preferences, constraints, principles; project: current-state, decisions, open-questions).
> An entry must have `status:canonical` plus exactly one target tag and one `capsule-slot:<slot>` tag; drafts, deprecated entries, ambiguous slots, and malformed rows are omitted or reported via `duplicate_slots` and `invalid_entries`.
> Responses carry a strong ETag over the exact prompt text with a 12,000-character budget, and removal from a capsule means setting status to draft or deprecated.
> See [[wiki/01-overview|Overview]].

### Q5. What does `wrangler.jsonc` declare about the Worker's entry point, bindings, schedules, and secrets?
> [!tip]- Answer
> It declares the Worker entry `src/index.ts` with D1 (`DB`), Vectorize (`VECTORIZE`), AI, and KV (`OAUTH_KV`) bindings, static assets from `./public`, and the `VECTORIZE_GRACE_MS` var set to `"300000"`.
> It defines five cron triggers — the free-plan maximum — covering nightly maintenance, hourly integrations, insight accrual, and weekly team/personal insight reasoning.
> It requires the `AUTH_TOKEN` secret, whose only local shape is `AUTH_TOKEN=your_memorable_token_here` in `.dev.vars.example`.
> See [[wiki/02-top-level-files|Top-level-files]].

### Q6. How do the repo's git/secret hygiene rules and vitest harness keep memories and credentials out of version control while staying testable?
> [!tip]- Answer
> `.gitignore` uses slashless `node_modules`, `docs/*`, and `.cursor/**` patterns with re-inclusions so symlinks and the two tracked docs/memory files behave correctly, while blocking all `*.sql` except `db/schema.sql`, SQLite artifacts, D1 exports, `.eval-cache/`, `devharness/`, `.dev.vars`, and per-environment `wrangler.*.jsonc`.
> `.gitattributes` forces LF line endings and marks binary extensions as binary.
> The vitest harness fails runs on leaked temp dirs at both run and per-file level, and stubs `agents/mcp`, `cloudflare:sockets`, and the OAuth provider so Worker-only imports load under node.
> See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Would you recommend Second Brain for a small team that needs private-plus-shared memory on the Cloudflare free plan, and why?
> [!tip]- Answer
> Yes, provided the team accepts one shared team per brain and the free-plan cron/budget limits, because it offers private-by-default workspaces with deliberate canonical-move sharing, dashboard control, and broad capture sources in the members' own Cloudflare accounts.
> The main cautions are the single-team v3.0.0 scope, the degraded English-first embeddings when Vectorize is down, and the operational need to guard the single `AUTH_TOKEN` and nightly cron capacity.
> If those constraints fit, the combination of semantic plus exact-phrase recall and Prompt Capsules makes it a strong lightweight team-memory choice.
> See [[wiki/01-overview|Overview]].
