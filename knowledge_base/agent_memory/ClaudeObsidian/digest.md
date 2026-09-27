> [[index|Wiki]] | [[summary|Summary]]
# AgriciDaniel/claude-obsidian — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** claude-obsidian is a local-first knowledge system that turns source material into linked, source-cited Obsidian pages and answers from vault evidence under explicit, recoverable transactions.
## Key points
- Turns source material into linked, source-cited Obsidian pages and answers from evidence already in the vault, with explicit workflows for research, retrieval, maintenance, and visual mapping (README:33-37).
- Keeps the vault as a normal directory of Markdown, JSON, and source files, never hidden in a plugin cache, locked in a cloud database, or silently uploaded to a model (README:39-41).
- Organizes work as a loop — retain the source, ground the claims, connect the knowledge, then put it back to work — with content-addressed copies before synthesis (README:47-54).
- Retains authority, freshness, support, contradiction, confidence, and review state in source and claim ledgers so unsupported and contradictory claims remain visible (README:55-56).
- Prevents parallel-agent races by having workers return drafts while one orchestrator inspects and applies one recoverable transaction (README:88-89).
- Selects a vault explicitly via `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`, or one unambiguous initialized ancestor, exiting without writing when selection is uncertain (README:226-230).
- Applies one logical knowledge operation as one recoverable transaction: record expected SHA-256, merge drafts into one bundle, inspect, apply once, report operation ID and changed paths (README:232-238).
## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The 13 root files define the agent contract, vault schema, privacy/security boundaries, provenance metadata, and byte-identical reproducibility guards for the claude-obsidian product source.
## Key points
- `AGENTS.md` declares the repo is product source (not the user vault) and fixes vault resolution as explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`, then unambiguous ancestor, failing closed (AGENTS.md:11-25).
- All shared mutations use one inspected `claude-obsidian.transaction.v1` bundle applied once via `scripts/claude-obsidian.py`; parallel workers return drafts only and direct shared writes, `wiki-lock.sh`, and auto-commits are banned (AGENTS.md:49-62; GEMINI.md:19-21; ZCODE.md:25-27).
- `WIKI.md` fixes the user-vault layout (`inbox/`, `.raw/`, `wiki/`, `.vault-meta/`, `.obsidian/`) with `.raw/` payloads create-only and `inbox/` never auto-deleted (WIKI.md:9-33,42-45).
- `PRIVACY.md` and `SECURITY.md` make the core local-first with no telemetry, SessionStart injection opt-in via `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1` (plus `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` for external vaults), and untrusted vault/web content that never authorizes commands, egress, or destruction (PRIVACY.md:1-20; SECURITY.md:27-38).
- `.gitattributes:4` pins `* -text` so frontmatter `---\n` and content hashes stay byte-identical cross-platform, while `.gitignore` excludes runtime/secret/personal state (`.vault-meta/` locks/caches, `.mcp.json`, `*.pem`, `.env*`) but keeps `wiki/meta/dashboard.base` and plugin `data.json` exceptions (`.gitignore:4-8,38-49,80-81,134-169`).
- `RELEASE_MANIFEST.json` plus `SHA256SUMS` pin the deterministic public artifact (path, mode `0644`, `sha256`, `size` per entry), and `CITATION.cff:11-12`, `CODEOWNERS:2`, `ATTRIBUTION.md` record version `2.2.0` (2026-09-10), default owner `@AgriciDaniel`, and third-party/community provenance (RELEASE_MANIFEST.json:2-8; CITATION.cff:11-12; CODEOWNERS:2).
- `GEMINI.md` and `ZCODE.md` are thin host adapters that defer to `AGENTS.md` and install skill links via `scripts/setup-multi-agent.sh --host <gemini|zcode>` preview-then-`--apply` (GEMINI.md:1-12; ZCODE.md:1-18).
## The system in five moves
1. Start from a local-first promise: the vault stays ordinary user-owned files, never a plugin cache, cloud database, or silent upload.
2. Capture sources with context into a visible inbox with immutable content-addressed copies before any synthesis.
3. Ground every important claim in source and claim ledgers that keep authority, support, contradiction, and review state visible.
4. Connect knowledge into linked pages, indexes, Maps of Content, and Canvas views under a fixed vault schema and filing modes.
5. Reuse the vault via query, retrieval, lint, and rollup workflows instead of starting each conversation from zero.
6. Guard every mutation as one inspected, recoverable transaction — drafts from workers, one orchestrator apply — with explicit vault selection, privacy/egress boundaries, and byte-identical reproducibility checks.
