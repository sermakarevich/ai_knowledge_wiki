> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Memory, Skills, and the Learning Loop
**In one sentence:** Hermes Agent remembers with two tiny curated files (MEMORY.md for facts, USER.md for user profile) plus searchable session history, learns procedures as on-demand skills it writes itself, and improves after every turn through a background review loop with optional human approval.
## Key points
- Built-in memory is two files in `~/.hermes/memories/` — MEMORY.md (agent notes: environment facts, conventions, lessons, 2,200 chars) and USER.md (user profile: preferences, style, 1,375 chars) — injected as a frozen snapshot into the system prompt at session start.
- The agent manages memory itself with the `memory` tool (`add`, `replace`, `remove` via unique-substring matching, no `read` action since memory is already in context), and writes that would overflow the limit fail loudly so the agent consolidates entries instead of silently dropping them.
- Session search (`session_search` tool, SQLite FTS5 over `~/.hermes/state.db`) gives unlimited recall of past conversations at ~20ms per query with zero token cost until searched, complementing the small always-loaded memory.
- After each turn a background self-improvement review replays the conversation and may save memories or patch skills, announced by a `💾 Memory updated` line; it can run on a cheaper model, be deferred on local-GPU machines, disabled, or gated behind approval.
- `memory.write_approval: true` stages every memory write for review (`/memory pending`, `/memory approve`, `/memory reject`), and the `/journey` timeline (`hermes journey`) visualizes everything learned with list/edit/delete pruning.
- Skills are on-demand knowledge documents in `~/.hermes/skills/` following progressive disclosure (index ~3k tokens, full content only when needed), usable as slash commands, stackable up to 5 per message, and groupable into YAML bundles.
- The agent creates and patches its own skills via `skill_manage` (procedural memory: lessons not logs), installable from 8 hub sources (official, skills.sh, well-known endpoints, GitHub taps, ClawHub, LobeHub, browse.sh, direct URL) with security scanning, and background-maintained by the Curator; 8 external memory providers (Mem0, Honcho, OpenViking, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) add deeper recall alongside built-in memory.
---
## Built-in memory: two small files
Hermes memory is bounded and curated by design. Two files in `~/.hermes/memories/`:

| File | Purpose | Limit |
|------|---------|-------|
| MEMORY.md | Agent's personal notes — environment facts, conventions, tool quirks, completed-work diary, techniques that worked | 2,200 chars (~800 tokens) |
| USER.md | User profile — name, role, timezone, communication preferences, pet peeves, skill level | 1,375 chars (~500 tokens) |

Both load into the system prompt once at session start as a frozen block (header shows store name plus usage like `[67% — 1,474/2,200 chars]`, entries separated by `§`). Frozen is intentional: it preserves the LLM (Large Language Model) prefix cache. Writes during a session persist to disk immediately but appear in context only next session.

One agent per Hermes home: two processes sharing one home compound each other's entries. Give a second agent its own profile; share via an external provider instead. Memory is scoped per profile by design.

## The memory tool
The agent uses the `memory` tool with `add`, `replace`, `remove` (targets `memory` or `user`). No `read` — content is already in context. `replace`/`remove` use short unique-substring matching via `old_text`; ambiguous matches error out. Exact duplicates are rejected automatically. Entries are security-scanned (injection, exfiltration, backdoor patterns, invisible Unicode) before acceptance since they enter the system prompt.

Save proactively (user prefs → `user`; environment facts, corrections, conventions, completed work → `memory`); skip trivia, re-discoverable facts, raw dumps, session ephemera, and anything already in SOUL.md/AGENTS.md.

When memory is full the tool errors with current usage and entries, and the agent consolidates (merge/remove, then retry) in the same turn. Above ~80% it should consolidate before adding. Config in `~/.hermes/config.yaml` under `memory:` (`memory_enabled`, `user_profile_enabled`, char limits, `write_approval`); setting both enables off hides the tool entirely.

## Session search vs memory
All CLI and messaging sessions persist in `~/.hermes/state.db` with FTS5 (Full-Text Search v5, SQLite's built-in search index) full-text search. `session_search` returns actual messages — no LLM summarization — and can scroll inside any session. Browse with `hermes sessions list`.

| | Memory | Session search |
|---|---|---|
| Capacity | ~1,300 tokens | Unlimited |
| Cost | Token cost every prompt | Free until searched |
| Use | Key facts always in context | "Did we discuss X last week?" |

## The learning loop: background review and journey
After each turn a background review fork replays the conversation and may save a memory or update a skill — repeated corrections and durable lessons become compact entries or procedures. Knobs under `auxiliary.background_review`: run on a cheaper model (digest replay, ~3–5x cheaper), `defer: auto` on managed local GPU (queue until idle), `enabled: false` to skip auto-forks (`/refine` still works), `extra_tools` whitelist. `display.memory_notifications` controls the chat line (`off`/`on`/`verbose`).

Approval gates: `memory.write_approval: true` stages all memory writes (`/memory pending|approve|reject`); `skills.write_approval: true` stages all skill writes (`/skills pending|diff|approve|reject`, diffs live under `~/.hermes/pending/skills/`).

`/journey` (`hermes journey`, aliases `/learning`, `/memory-graph`) renders the timeline of learned skills and memories with a playable constellation scrubber; `journey list|delete|edit` prunes nodes (skills archive, memory chunks delete). Same data powers CLI, TUI (Terminal User Interface), and Desktop Star Map.

## Skills: on-demand knowledge
Every skill in `~/.hermes/skills/` is a slash command (`/gif-search funny cats`), stackable (up to 5 leading `/skill` tokens), and loadable via `skills_list()` → `skill_view(name)` → `skill_view(name, path)` progressive disclosure. SKILL.md front-matter carries name, description, version, optional `platforms`, conditional activation (`fallback_for_toolsets`, `requires_toolsets` — e.g. DuckDuckGo search appears only when the `web` toolset is unavailable), required env vars (secure setup on load), and config settings.

Authoring: `/learn` turns anything (SDK dir, URL, workflow, notes, whole book → knowledge-base skill with `references/` per chapter) into a skill; the agent saves via `skill_manage` (`create/patch/edit/delete/write_file/remove_file`, `patch` preferred). Skill content rule: lessons not logs — generalizable rules with mechanism, no incident narration. Bundles (`~/.hermes/skill-bundles/<slug>.yaml`) group skills under one command. Project-local skills (`.hermes/skills/` or `.agents/skills/` in a repo, trust via `hermes skills trust`) outrank global ones; external dirs (`skills.external_dirs`) and `skills.create_dir` redirect scanning/creation.

Hub: `hermes skills browse|search|inspect|install|check|update|audit|uninstall` across official, skills.sh, well-known endpoints, GitHub taps (openai, anthropics, huggingface, NVIDIA, gstack), ClawHub, LobeHub, browse.sh, and direct URLs — all security-scanned (dangerous verdicts un-overridable, others with `--force`), trust levels builtin > official > trusted > community. The Curator passively maintains agent-created skills (usage tracking, staleness, archival, LLM review).

## External memory providers
Eight plugins — Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory — run alongside (never replacing) built-in memory for knowledge graphs, semantic search, auto fact extraction, cross-session modeling. `hermes memory setup` / `hermes memory status`.

**Covers:** docs `user-guide/features/memory`, `memory-providers`, `skills`, `curator`, `context-files`, `personality` (SOUL.md), `user-guide/sessions` (session search), `user-guide/profiles` (memory scoping).
