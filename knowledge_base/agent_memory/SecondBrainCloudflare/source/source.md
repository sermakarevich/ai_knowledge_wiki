PDF-Location: https://github.com/rahilp/second-brain-cloudflare (no local source.pdf; kind repo via git-clone)
# rahilp/second-brain-cloudflare
Source: https://github.com/rahilp/second-brain-cloudflare
Kind: repo
Fetched: 2026-09-26T13:43:41.015325+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# rahilp/second-brain-cloudflare

Commit: 8a29b7352a62d2b7be9757d8431e5a5f994169ee

## README

<p align="center">
  <a href="https://www.thesecondbrain.dev"><img src="https://www.thesecondbrain.dev/logos/sb-lockup.svg" alt="Second Brain" width="400"></a>
</p>

**Private memory for you. Shared memory for your team. Available to every MCP-compatible AI tool you use.**

Now with **Team Edition** — private personal layers plus a shared team layer, in one Worker.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built with Cloudflare Workers](https://img.shields.io/badge/Built%20with-Cloudflare%20Workers-F38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-8B5CF6)](https://modelcontextprotocol.io/)
[![MCP Toplist](https://mcptoplist.com/badge/glama%2Frahilp%2Fsecond-brain-cloudflare.svg)](https://mcptoplist.com/server/glama%2Frahilp%2Fsecond-brain-cloudflare)

Claude, ChatGPT, Cursor, Codex, and the other AI tools you use do not naturally share context. You end up repeating the same projects, decisions, and preferences in every app.

Second Brain gives those tools one persistent memory system. It runs in your own Cloudflare account, stays under your control, and retrieves the right context by meaning rather than exact wording.

---

The desktop app is the easiest way to start. It builds your Second Brain and connects your AI tools in about two minutes—no terminal or Cloudflare setup required.



### [Download for Mac or Windows](releases/latest)

---

[Deploy to Cloudflare](https://deploy.workers.cloudflare.com/?url=https://github.com/rahilp/second-brain-cloudflare) · [Read the documentation](wiki)




## What it does

- **Recalls by meaning.** Ask a natural-language question and find the right memory even when you used different words when saving it.
- **Works across tools and devices.** Every client talks to the same Worker, so there is nothing to copy or synchronize between apps.
- **Keeps you in control.** Browse, edit, append, connect, share, export, or permanently remove any memory from the dashboard.
- **Builds useful context.** Automatic classification, duplicate detection, relationships, time-aware ranking, and optional weekly insights help the brain stay useful as it grows.
- **Captures from where you already work.** Use MCP clients, the CLI, browser extension, Obsidian, Notion, calendars, email, iOS Shortcuts, or the web dashboard.
- **Acts on what matters next.** Add dates to memories, review overdue and upcoming commitments, and let the installed PWA proactively push a reminder when something becomes due. See the [Reminders and Push guide](https://github.com/rahilp/second-brain-cloudflare/wiki/Reminders-and-Push).
- **Stays in your account.** Memories, vectors, credentials, and application resources live in your own Cloudflare account.



## Team Edition

Second Brain can now be a team's memory without stopping being yours.

- Every person gets a **Personal** workspace that nobody else can read, plus a **Shared** layer visible to the team.
- Memories are private by default and only enter the Shared layer when someone deliberately shares them.
- Sharing moves one canonical memory rather than making a copy. Its author remains visible, and only the author or an admin can edit, delete, or un-share it.
- Admins can manage members, access, capture defaults, and integrations without gaining access to anyone's personal workspace.
- Existing v2 memories become the owner's private memories during upgrade. Nothing is exposed to a team automatically.

| Layer | Who can read it | Who can edit or delete it |
| --- | --- | --- |
| Personal | Only you | Only you |
| Shared | Everyone on the team | The author or an admin |

The same Worker supports personal and team use; there is no separate team deployment. In the API, CLI, and MCP tools, the Shared layer is represented by the stable workspace value `company`. See the [Team Setup guide](https://github.com/rahilp/second-brain-cloudflare/wiki/Team-Setup) for member management, capture policies, sharing, and upgrades.

**v3.0.0 scope:** each brain has **one** shared team. The API and MCP layer include optional `team` parameters and a `list_teams` tool so multi-team support can ship later without breaking changes; the dashboard and admin flows do not create or switch between multiple teams yet. See [CHANGELOG.md](CHANGELOG.md).



## How it works

Second Brain runs as a Cloudflare Worker backed by D1, Vectorize, Workers AI, and KV. Every app and AI client connects to that Worker through REST or the Model Context Protocol (MCP).

1. **Capture:** Save a decision, preference, project update, note, or source from any connected client.
2. **Organize:** Second Brain classifies it, checks for duplicates and contradictions, creates relationships, and indexes it for semantic search.
3. **Recall:** Ask in natural language. Second Brain retrieves relevant memories, follows useful connections, and returns source-backed context to the tool you are using.

If Vectorize is unavailable, captures and keyword recall continue working. Your memories remain usable while semantic indexing is restored. The shipped embedding models read English best; the desktop app's Settings can switch a brain to a multilingual reading.

Search now finds the hard things: exact names, ticket numbers, versions, and phrases in any language, even when they sit in old memories, and finding them is dramatically faster and cheaper, staying that way as the brain grows, which keeps the free plan comfortable. It does this with a full-text index that ranks matches by relevance instead of scanning every memory. The upgrade is automatic: new installs use the index immediately, existing brains build it over nightly runs, and no client needs updating.



### Memory tools

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

On a team brain, memory tools accept a `workspace` of `personal` or `company` when you want to choose a layer explicitly. `company` is the wire value for the Shared team layer. Without `workspace`, captures use the member and team defaults, while recall searches everything that person is allowed to see.

Optional `team` (workspace id) and MCP `list_teams` / `GET /team/workspaces` are wired for a future multi-team release. **In v3.0.0 you can omit them** — each brain has one shared team and the primary team is used automatically.



### Projects

Memories live on four axes: **workspace** = who can see it (personal / company / team) — tenancy, unchanged. **project** = what it's about — a named, managed container. **tags** = free-form facets, unchanged. **source** = where it came from, unchanged. Call `list_projects` to discover projects in scope and pass `project` on remember to group related memories. A memory can belong to one or more projects; use projects to organize by topic, initiative, or context rather than bare topic tags.

CLI example:

```bash
brain remember --workspace company "We ship on Thursdays"
brain recall --workspace company "when do we ship?"
brain recall --project website "what did we decide about hosting?"
```



### Prompt Capsules

Prompt Capsules are deterministic, read-only projections for gateways and
custom agents that can place stable context before a changing user request.
They complement query-specific `recall`; they do not inject every memory into
every prompt.

A Capsule entry is an ordinary canonical memory with one target tag and one
slot tag. Core entries use `capsule:core`; project entries use
`capsule:project:<project-slug>`. Slots are emitted in this fixed order:

- Core: `identity`, `preferences`, `constraints`, `principles`
- Project: `current-state`, `decisions`, `open-questions`

Tag the slot as `capsule-slot:<slot>` and keep at most one canonical entry per
slot. Draft and deprecated entries are ignored. Ambiguous slots are omitted
without choosing a winner; malformed rows are skipped. The response reports
`duplicate_slots` and `invalid_entries`, and `complete` is false. Other valid
slots remain available, including on the shared layer.

An entry must carry `status:canonical` to be part of a Capsule. The easiest way
is to include `status:canonical` in the tags at remember or capture time (it is
stored after whitespace trimming, and the classifier then leaves it alone);
otherwise the definition starts as draft and requires `set_status canonical`.
Classification, including `/classify-pending`, never publishes a capsule. A
write that contradicts a protected memory is demoted to draft even when the
caller requested canonical. To take an entry out of a Capsule, set its
status to draft or deprecated. MCP `update` accepts an optional `tags` array:
pass the complete replacement definition, for example
`["capsule:core", "capsule-slot:preferences"]`, along with the entry id and
content. Naming either capsule namespace replaces both namespaces; a lone
slot tag is not a complete definition. Omit `tags` to preserve existing tags.
MCP and REST capture/update accept at most 64 tags of 128 characters each.

**Shared-layer recovery:** members can publish their own shared definitions,
but cannot edit a teammate's entry. Check the reported ids, ask the author or
an admin to re-slot or unpublish them with `update` or `set_status`, and do not
interpret an incomplete response as the full team policy. The dashboard hides
bookkeeping tags; use MCP for this recovery. No teammate content-edit permission
is added.

Authenticated clients can use `GET|HEAD /prompt-capsules/core`,
`GET|HEAD /prompt-capsules/projects/<project-slug>`, or the
`get_prompt_capsule` MCP tool. Responses include a strong `ETag`, a SHA-256 of
the exact prompt-ready `text`, and whole-slot omission metadata for the
12,000-character budget. Validation happens before serialization: shared invalid,
duplicate, or individually oversized definitions are excluded and reported, so
later healthy slots may still appear. The result is an ordered subset of the
defined slots, not necessarily their prefix. Among the remaining valid slots,
once the cumulative budget is exceeded, that slot and every later slot are omitted. A single
entry longer than the whole serialized budget (including JSON escaping) returns
`409 invalid_prompt_capsule` with reason `content-too-large` in a personal
capsule, even if earlier slots would fit; no partial text is returned. In a shared capsule it is skipped
and reported, so it cannot hide unrelated slots. Empty responses have
`populated: false` and `complete: false`. The 200-candidate resource limit still
returns `409 too_many_candidates`; an author or admin must reduce definitions. Timestamps, entry ids, and ETags are excluded from
`text`, so unrelated changes do not alter the reusable prefix. Provider cache
keys, breakpoints, token budgets, and cache-hit measurement remain the
gateway's responsibility.

Capsu

... (truncated, 12495 more characters)

## package.json

```
{
  "name": "second-brain",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "wrangler dev",
    "dev:demo": "wrangler dev -c wrangler.demo.jsonc --port 8799",
    "predeploy": "node scripts/predeploy-guard.mjs",
    "check:scope": "node scripts/check-scope.mjs",
    "deploy": "wrangler deploy",
    "deploy:worker": "node scripts/release.mjs worker",
    "deploy:app": "node scripts/release.mjs app",
    "deploy:all": "node scripts/release.mjs all",
    "deploy:tag": "node scripts/release.mjs tag",
    "db:create": "wrangler d1 create second-brain-db",
    "db:migrate": "wrangler d1 execute second-brain-db --file=db/schema.sql",
    "db:migrate:remote": "wrangler d1 execute second-brain-db --remote --file=db/schema.sql",
    "vectors:create": "wrangler vectorize create second-brain-vectors --dimensions=384 --metric=cosine",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:eval:local-models": "EVAL_LOCAL_MODELS=1 vitest run test/eval/local-ai.smoke.test.ts test/eval/legacy-rerank.test.ts",
    "test:eval:full": "EVAL_FULL=1 EVAL_WORKERD=1 vitest run test/eval",
    "test:eval:workerd": "EVAL_WORKERD=1 vitest run test/eval/d1.workerd.test.ts test/eval/baseline-lock.workerd.test.ts test/eval/runner.test.ts",
    "test:eval:scale-guards": "EVAL_SCALE_GUARDS=1 vitest run test/eval/router-guards.scale.test.ts",
    "test:eval:public-download": "EVAL_PUBLIC_DOWNLOAD=1 vitest run test/eval/public/download.test.ts",
    "eval:recall": "node scripts/eval-run-ts.mjs test/eval/cli.ts",
    "cf-typegen": "wrangler types",
    "typecheck": "wrangler types && tsc --noEmit"
  },
  "dependencies": {
    "@cloudflare/workers-oauth-provider": "^0.8.2",
    "@modelcontextprotocol/client": "^2.0.0",
    "@modelcontextprotocol/sdk": "^1.30.0",
    "@modelcontextprotocol/server": "^2.0.0",
    "agents": "^0.20.1",
    "ical.js": "^2.2.1",
    "postal-mime": "^2.7.5",
    "zod": "^4.4.3"
  },
  "devDependencies": {
    "@huggingface/transformers": "^4.3.0",
    "@types/node": "^26.1.2",
    "@vitest/coverage-v8": "^4.1.10",
    "esbuild": "^0.28.1",
    "typescript": "^7.0.2",
    "vitest": "^4.1.10",
    "wrangler": "^4.114.0"
  },
  "overrides": {
    "undici": "7.29.0"
  },
  "cloudflare": {
    "bindings": {
      "AUTH_TOKEN": {
        "description": "Your authentication token. Use a memorable phrase (like 'coffee-lover-2026') or generate a secure token with: openssl rand -base64 32. Save it - you'll need this for AI client connections!"
      }
    }
  }
}

```

## Top-level layout

- .codex/ (dir, 1 files, ~31 lines)
- .cursor/ (dir, 1 files, ~52 lines)
- .dev.vars.example (~1 lines)
- .gitattributes (~23 lines)
- .github/ (dir, 5 files, ~657 lines)
- .gitignore (~55 lines)
- .mcp.json (~8 lines)
- .npmrc (~1 lines)
- AI_Instructions/ (dir, 4 files, ~324 lines)
- assets/ (dir, 1 files, ~0 lines)
- CHANGELOG.md (~290 lines)
- db/ (dir, 1 files, ~325 lines)
- docs/ (dir, 1 files, ~296 lines)
- installer/ (dir, 84 files, ~39425 lines)
- integrations/ (dir, 12 files, ~1216 lines)
- LICENSE (~21 lines)
- package-lock.json (~6515 lines)
- package.json (~60 lines)
- public/ (dir, 55 files, ~21483 lines)
- README.md (~356 lines)
- scripts/ (dir, 10 files, ~2944 lines)
- src/ (dir, 129 files, ~26845 lines)
- test/ (dir, 446 files, ~187026 lines)
- tsconfig.json (~15 lines)
- vitest.config.ts (~25 lines)
- vitest.global-setup.ts (~17 lines)
- vitest.setup.ts (~60 lines)
- wrangler.jsonc (~76 lines)

