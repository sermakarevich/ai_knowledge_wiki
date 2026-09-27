[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Second Brain is a persistent semantic memory system running as a Cloudflare Worker that lets every MCP-compatible AI tool share one personal-plus-team memory layer (01-overview.md:11-13, 01-overview.md:20-22).
## Key points
- Gives MCP-compatible AI tools (Claude, ChatGPT, Cursor, Codex) one persistent memory so context need not be repeated per app (01-overview.md:20-22).
- Runs in the user's own Cloudflare account on a Worker backed by D1, Vectorize, Workers AI, and KV, reached via REST or MCP (01-overview.md:47, 01-overview.md:74).
- Recalls by meaning (semantic) plus a full-text index for exact names, ticket numbers, versions, and phrases, with relevance ranking instead of scanning every memory (01-overview.md:41, 01-overview.md:82).
- Organizes on capture via automatic classification, duplicate detection, contradiction checks, relationships, and time-aware ranking, with optional weekly insights (01-overview.md:44, 01-overview.md:76-78).
- Separates visibility into a private Personal workspace and a Shared team layer (wire value `company`), private by default, shared only by deliberate move of one canonical memory (01-overview.md:55-57, 01-overview.md:106).
- Supports management from the dashboard (browse, edit, append, connect, share, export, permanently remove) and capture from MCP clients, CLI, browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts, or web dashboard (01-overview.md:43, 01-overview.md:45).
- Acts on dated memories with overdue/upcoming review and proactive push reminders via the installed PWA (01-overview.md:46).
---
## What it does
Recalls by meaning, works across tools and devices through a single Worker, keeps user control via the dashboard, builds context automatically, captures from existing tools, acts on dated commitments, and stays in the user's own account (01-overview.md:41-47):
- **Recalls by meaning.** "Ask a natural-language question and find the right memory even when you used different words when saving it." (01-overview.md:41)
- **Works across tools and devices.** "Every client talks to the same Worker, so there is nothing to copy or synchronize between apps." (01-overview.md:42)
- **Keeps you in control.** "Browse, edit, append, connect, share, export, or permanently remove any memory from the dashboard." (01-overview.md:43)
- **Builds useful context.** "Automatic classification, duplicate detection, relationships, time-aware ranking, and optional weekly insights" (01-overview.md:44)
- **Captures from where you already work.** "MCP clients, the CLI, browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts, or the web dashboard." (01-overview.md:45)
- **Acts on what matters next.** "Add dates to memories, review overdue and upcoming commitments, and let the installed PWA proactively push a reminder when something becomes due." (01-overview.md:46)
- **Stays in your account.** "Memories, vectors, credentials, and application resources live in your own Cloudflare account." (01-overview.md:47)
## Team Edition
One Worker serves both personal and team use with no separate team deployment; each person keeps an unreadable-by-others Personal workspace plus one Shared layer (01-overview.md:53-55, 01-overview.md:66). Memories are private by default and enter Shared only by deliberate share, which moves one canonical memory (not a copy) with the author visible; only the author or an admin can edit, delete, or un-share it (01-overview.md:56-57). Admins manage members, access, capture defaults, and integrations without gaining access to personal workspaces, and v2 memories upgrade into the owner's private memories with nothing auto-exposed (01-overview.md:58-59).
| Layer | Who can read it | Who can edit or delete it |
| --- | --- | --- |
| Personal | Only you | Only you |
| Shared | Everyone on the team | The author or an admin |
(01-overview.md:61-64)
**v3.0.0 scope:** each brain has **one** shared team; the API/MCP layer carries optional `team` parameters and a `list_teams` tool for future multi-team support, but dashboard/admin flows do not create or switch teams yet (01-overview.md:68).
## How it works
Cloudflare Worker backed by D1, Vectorize, Workers AI, and KV; apps and AI clients connect through REST or MCP (01-overview.md:74). Pipeline (01-overview.md:76-78):
1. **Capture:** "Save a decision, preference, project update, note, or source from any connected client."
2. **Organize:** "classifies it, checks for duplicates and contradictions, creates relationships, and indexes it for semantic search."
3. **Recall:** "Ask in natural language … retrieves relevant memories, follows useful connections, and returns source-backed context."
Degraded mode: if Vectorize is unavailable, captures and keyword recall keep working while semantic indexing is restored; shipped embedding models "read English best" with a multilingual switch in the desktop app Settings (01-overview.md:80). Search upgrade is automatic — new installs use the full-text relevance-ranked index immediately, existing brains build it over nightly runs, no client update needed (01-overview.md:82).
## Memory tools
| Tool | What it does |
| --- | --- |
| `remember` | Store ideas, decisions, preferences, and project context |
| `append` | Add a timestamped update to an existing memory |
| `update` | Replace an existing memory |
| `recall` | Find memories by meaning rather than exact wording |
| `list_recent` | Browse recently saved memories |
| `list_teams` | List shared teams you belong to (names and ids). In v3.0.0 this is one team; used by MCP clients for future multi-team support |
| `list_projects` | List projects in scope, with display names, descriptions, and memory counts |
| `get_prompt_capsule` | Read a deterministic core or project context projection for a gateway-controlled prompt prefix |
| `get` | Read one memory by ID |
| `forget` | Permanently delete a memory |
| `set_status` | Mark a memory `canonical`, `draft`, or `deprecated` |
| `link` | Add an explicit relationship between two memories |
| `unlink` | Remove a relationship between two memories |
| `connections` | List the memories connected to a memory |
| `share` | Move a memory between the Personal and Shared layers |
(01-overview.md:88-104)
Layer selection: memory tools accept `workspace` of `personal` or `company` for an explicit layer choice; `company` is the wire value for the Shared team layer; without `workspace`, captures use member/team defaults while recall searches everything the person may see (01-overview.md:106). Optional `team` (workspace id) and `list_teams` / `GET /team/workspaces` are wired for a future multi-team release and may be omitted in v3.0.0 (01-overview.md:108).
## Projects
Memories live on four axes: `workspace` (who can see it: personal / company / team — tenancy), `project` (what it is about — named, managed container), `tags` (free-form facets), `source` (where it came from) (01-overview.md:114). Discovery and grouping: call `list_projects`, pass `project` on remember; a memory may belong to one or more projects; prefer projects over bare topic tags for topic/initiative/context organization (01-overview.md:114). CLI example (01-overview.md:118-122):
```bash
brain remember --workspace company "We ship on Thursdays"
brain recall --workspace company "when do we ship?"
brain recall --project website "what did we decide about hosting?"
```
## Prompt Capsules
Deterministic, read-only projections for gateways/custom agents that place stable context before a changing user request; they complement query-specific `recall` and do not inject every memory into every prompt (01-overview.md:128-131). A Capsule entry is an ordinary canonical memory with one target tag plus one slot tag: core entries use `capsule:core`, project entries use `capsule:project:<project-slug>`; fixed slot order is core `identity`, `preferences`, `constraints`, `principles` and project `current-state`, `decisions`, `open-questions` (01-overview.md:133-138). Slot tag form is `capsule-slot:<slot>` with at most one canonical entry per slot; draft/deprecated entries are ignored, ambiguous slots omitted without picking a winner, malformed rows skipped; the response reports `duplicate_slots` and `invalid_entries` with `complete` false (01-overview.md:140-144). An entry needs `status:canonical` (easiest via `status:canonical` in tags at remember/capture time, whitespace-trimmed, left alone by the classifier; otherwise starts as draft and needs `set_status canonical`); classification including `/classify-pending` never publishes a capsule, and a write contradicting a protected memory is demoted to draft even when canonical was requested (01-overview.md:146-152). Removal from a capsule means setting status to draft or deprecated; MCP `update` takes an optional complete-replacement `tags` array such as `["capsule:core", "capsule-slot:preferences"]`; naming either capsule namespace replaces both; a lone slot tag is incomplete; omitting `tags` preserves tags; MCP/REST capture/update accept at most 64 tags of 128 characters each (01-overview.md:153-158). Shared-layer recovery: members publish their own shared definitions but cannot edit a teammate's entry — check reported ids, ask author/admin to re-slot or unpublish via `update`/`set_status`; dashboard hides bookkeeping tags, so use MCP (01-overview.md:160-165). Access via `GET|HEAD /prompt-capsules/core`, `GET|HEAD /prompt-capsules/projects/<project-slug>`, or `get_prompt_capsule` MCP tool; responses carry a strong `ETag` (SHA-256 of exact prompt-ready `text`) and whole-slot omission metadata for the 12,000-character budget; shared invalid/duplicate/oversized definitions are excluded and reported; over-budget slots and all later slots are omitted; a personal-capsule entry longer than the whole serialized budget returns `409 invalid_prompt_capsule` (`content-too-large`) with no partial text, while in a shared capsule it is skipped/reported; empty responses have `populated: false` and `complete: false`; the 200-candidate limit returns `409 too_many_candidates` (01-overview.md:167-181). Timestamps, entry ids, and ETags are excluded from `text`; provider cache keys, breakpoints, token budgets, and cache-hit measurement stay the gateway's responsibility (01-overview.md:181-184).
> Truncation note: the chunk ends mid-word at "Capsu" (01-overview.md:186), so Prompt Capsule content beyond that point is not covered here; the chunk's macro-component list is also cut, showing only `top-level-files/` (01-overview.md:188-190).
**Covers:** repo overview (README positioning, feature list, Team Edition layers, Worker architecture, capture/organize/recall pipeline, memory-tool table, projects axes, Prompt Capsules) as given in 01-overview.md:1-190
