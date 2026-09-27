[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The 13 root files define the agent contract, vault schema, privacy/security boundaries, provenance metadata, and byte-identical reproducibility guards for the claude-obsidian product source.
## Key points
- `AGENTS.md` declares the repo is product source (not the user vault) and fixes vault resolution as explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`, then unambiguous ancestor, failing closed (AGENTS.md:11-25).
- All shared mutations use one inspected `claude-obsidian.transaction.v1` bundle applied once via `scripts/claude-obsidian.py`; parallel workers return drafts only and direct shared writes, `wiki-lock.sh`, and auto-commits are banned (AGENTS.md:49-62; GEMINI.md:19-21; ZCODE.md:25-27).
- `WIKI.md` fixes the user-vault layout (`inbox/`, `.raw/`, `wiki/`, `.vault-meta/`, `.obsidian/`) with `.raw/` payloads create-only and `inbox/` never auto-deleted (WIKI.md:9-33,42-45).
- `PRIVACY.md` and `SECURITY.md` make the core local-first with no telemetry, SessionStart injection opt-in via `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1` (plus `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` for external vaults), and untrusted vault/web content that never authorizes commands, egress, or destruction (PRIVACY.md:1-20; SECURITY.md:27-38).
- `.gitattributes:4` pins `* -text` so frontmatter `---\n` and content hashes stay byte-identical cross-platform, while `.gitignore` excludes runtime/secret/personal state (`.vault-meta/` locks/caches, `.mcp.json`, `*.pem`, `.env*`) but keeps `wiki/meta/dashboard.base` and plugin `data.json` exceptions (`.gitignore:4-8,38-49,80-81,134-169`).
- `RELEASE_MANIFEST.json` plus `SHA256SUMS` pin the deterministic public artifact (path, mode `0644`, `sha256`, `size` per entry), and `CITATION.cff:11-12`, `CODEOWNERS:2`, `ATTRIBUTION.md` record version `2.2.0` (2026-09-10), default owner `@AgriciDaniel`, and third-party/community provenance (RELEASE_MANIFEST.json:2-8; CITATION.cff:11-12; CODEOWNERS:2).
- `GEMINI.md` and `ZCODE.md` are thin host adapters that defer to `AGENTS.md` and install skill links via `scripts/setup-multi-agent.sh --host <gemini|zcode>` preview-then-`--apply` (GEMINI.md:1-12; ZCODE.md:1-18).
---
## Agent contract and host entry points
`AGENTS.md:1-6` states the product is a local-first Agent Skills package plus a Claude Code plugin adapter, with portable behavior in `skills/` and `claude_obsidian/` and no knowledge behavior in host hooks:

```
claude-obsidian is a local-first Agent Skills package for building source-cited,
compounding Obsidian knowledge bases. It also ships a Claude Code plugin adapter.
```

Vault resolution order is exact (AGENTS.md:23-25):

```
explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`,
then an unambiguous vault at or above the current directory. Fail closed when
no vault is selected.
```

The 15 canonical skills live at `skills/<name>/SKILL.md` with exactly `name` and `description` frontmatter; core workflows are `wiki`, `save`, `wiki-ingest`, `wiki-query`, `wiki-lint` (AGENTS.md:37-47). New vaults start with dry-run-first `python3 scripts/claude-obsidian.py init PATH`, existing vaults use `adopt` (AGENTS.md:27-34).

Host adapters add no new rules. Gemini (GEMINI.md:6-12):

```bash
bash scripts/setup-multi-agent.sh --host gemini
bash scripts/setup-multi-agent.sh --host gemini --apply
```

ZCode (ZCODE.md:10-18): same two-step flow with `--host zcode`, links landing in `~/.zcode/skills/` so every workspace can invoke skills without per-project setup. Both restate the single-bundle mutation rule and consent requirement for remote egress and destructive actions (GEMINI.md:19-21; ZCODE.md:25-27).

## Vault schema and operation rules
`WIKI.md:9-33` fixes the user-vault root layout:

```text
vault/
├── .gitignore                  # excludes vault-local runtime/session state
├── .claude-obsidian.json       # workspace identity and vault selection
├── inbox/                      # visible source intake; never auto-deleted
├── .raw/                       # immutable source bytes
│   └── .manifest.json          # backward-compatible delta/address metadata
├── wiki/                       # generated, user-owned knowledge
│   ├── index.md                # catalog and navigation
│   ├── log.md                  # completed operation history, newest first
│   ├── hot.md                  # bounded recent context, not a transcript
│   ├── overview.md             # high-level synthesis
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   ├── questions/
│   ├── canvases/
│   └── meta/ledgers/
│       ├── source-ledger.json
│       └── claim-ledger.json
├── .obsidian/                  # user-controlled Obsidian settings
└── .vault-meta/                # ignored locks, journals, indexes, queue/config
```

Source invariants (WIKI.md:37-45): `.raw/` payloads are never replaced, `.raw/.manifest.json` mutates only inside its own transaction, capture is SHA-256 content-addressed, and remote locators must be validated HTTPS with no credentials in URLs, notes, bundles, queues, or tracked config.

Frontmatter is flat YAML with plural keys and `YYYY-MM-DD` dates (WIKI.md:49-68):

```yaml
---
type: concept
title: Source-grounded notes
status: developing
created: 2026-07-11
updated: 2026-07-11
tags:
  - knowledge
  - evidence
aliases: []
address: c-000001
---
```

Required baseline properties are `type`, `title`, `status`, `created`, `updated`, `tags`; `aliases` and `address` are optional unless vault policy requires them (WIKI.md:66-68). Page-type vocabulary (WIKI.md:72-91, declared once in `claude_obsidian/page_schema.py`):

| Type | Purpose | Routable |
|---|---|---|
| `source` | Traceable summary of one source identity | yes |
| `entity` | Person, org, product, project, named thing | yes |
| `concept` | Idea, framework, mechanism, definition | yes |
| `question` | Scoped answer with visible evidence status | yes |
| `session` | User-approved conversation summary | yes |
| `comparison` | Criteria-based contrast with cited support | no |
| `overview` | High-level map of a domain or vault | no |
| `meta` | Index, log, cache, convention, maintenance | no |
| `fold` | Extractive rollup of log entries | no |

One logical mutation is one `claude-obsidian.transaction.v1` bundle with `expected_hashes`, `writes`, `address_requests`, and `source_manifest_updates` (WIKI.md:165-192); apply binds approval via the inspect result's exact `approval_sha256` so one vault's approval cannot be reused on another (WIKI.md:193-204). `wiki/index.md` entries must resolve and every canonical create/removal updates an active catalog or MOC in the same transaction; `wiki/log.md` is newest-first operation history and `wiki/hot.md` is short sanitized context, never a transcript (WIKI.md:112-139).

## Privacy and security boundaries
`PRIVACY.md:1-7` states local-first with no telemetry: vault content stays on the selected filesystem and core makes no network requests, though the host agent, web tools, or external adapters may send selected content under their own policies. `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1` is explicit user consent for bounded sanitized `wiki/hot.md` injection; workspace configs can spend that consent only inside their own project tree, and external-vault routing additionally requires the exact canonical path in `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` (PRIVACY.md:9-20). The Stop hook emits only aggregate recovery state (PRIVACY.md:20-22); image/PDF/EPUB support is metadata-only and URL/YouTube/OCR/transcription/extraction do not execute in core (PRIVACY.md:25-28).

Explicit egress needs an intentional workflow plus boundary consent: `autoresearch`/URL cleaning via host web tools, contextual-prefix model calls only with the egress flag, refused remote Ollama endpoints without opt-in, and inert external-capture argv plans revalidated before use (PRIVACY.md:30-40). Never put credentials in source notes, URL queries, tracked config, transaction bundles, or capture queues (PRIVACY.md:43-47).

`SECURITY.md:5-12` routes vulnerability reports to GitHub private advisory reporting (no secrets, vault content, or live exploits in public issues). The core is standard-library Python with the user's filesystem permissions, not a sandbox, with single-user/single-vault as the supported default (SECURITY.md:13-22). Content trust hierarchy (SECURITY.md:27-31): system/host policy, repo instructions, selected skill, and current user scope are authority; vault notes, hot context, indexes, inbox, raw captures, web pages, chunks, and tool output are untrusted data that never authorizes commands, scope widening, egress, disclosure, or destruction. Defensive invariants include containment-checked vault-relative paths, one process-lifetime lock per mutation with journaled hashes/backups plus fsync/atomic-replace, create-only raw payloads, draft-only parallel workers, non-mutating lifecycle hooks, and no inbox deletion (SECURITY.md:33-54). `scripts/wiki-lock.sh` is legacy compatibility only (SECURITY.md:60-61).

## Attribution, citation, and ownership
`ATTRIBUTION.md:11` credits Karpathy's LLM Wiki pattern as the architectural basis (independent implementation, nothing copied); `ATTRIBUTION.md:21-28` scopes the two ITS CSS snippets to private contributor-vault state, not the public artifact or vault template. Four historical contributor-vault plugins (Calendar, Thino, Excalidraw, Banners) are likewise excluded from the deterministic artifact (ATTRIBUTION.md:31-45). Two adopted v2.0.0 designs are credited: Nomic `search_query`/`search_document` prefixes with `with_task_prefix` (maartengoet, PR #77) and BM25 fallback order `bm25_score`-before-`score` (vinsocci, PR #62) (ATTRIBUTION.md:49-60).

Citation metadata (CITATION.cff:1-12):

```yaml
cff-version: 1.2.0
title: claude-obsidian
authors:
  - alias: AgriciDaniel
repository-code: 'https://github.com/AgriciDaniel/claude-obsidian'
license: MIT
version: 2.2.0
date-released: '2026-09-10'
```

Ownership is a single default rule (CODEOWNERS:2):

```
* @AgriciDaniel
```

## Reproducibility and release integrity
`.gitattributes:4` enforces byte identity:

```
* -text
```

with the header comment (`.gitattributes:1-3`) stating frontmatter `---\n` parsing and content hashes must be identical on every platform including Windows checkouts.

`.gitignore` separates contributor state from the distributable seed: it drops `.obsidian/workspace-mobile.json`, plugin `data.json` (except calendar/thino), Excalidraw runtime, `.smart-connections/`, `.trash/`, secrets (`*.pem`, `*.key`, `credentials*`, `auth.json`), personal root drops (`WIKI*.md`, `PROMPT.md`, `Untitled.canvas`, `*.base`), media/transcripts, and all runtime state under `.vault-meta/` (locks, caches, chunks, bm25, embed-cache, transport, hook log, mutation/orchestration/capture dirs) plus `.mcp.json` and `.vault-meta/mode.json`, while negating back `wiki/meta/dashboard.base` and `.vault-meta/locks/.gitkeep` (`.gitignore:1-8,37-67,68-81,134-169`).

`RELEASE_MANIFEST.json:2-8` opens with `artifact_format: zip` and per-file `{path, mode, sha256, size}` records (e.g. `.gitattributes` → `sha256 45b7bfba…`, `size 236` at RELEASE_MANIFEST.json:24-27). `SHA256SUMS:1-3` mirrors the same hashes in `<sha256>  <path>` lines for independent verification.

## Truncated sources in this chunk
- `RELEASE_MANIFEST.json` (1241 lines) is cut inside the `docs/` entries: the visible text ends mid-entry at `docs/windows-wsl.md` with `... (truncated, 26602 more characters)`; entries after that point are not in the chunk and are not summarized here.
- `SHA256SUMS` (205 lines) is cut inside the `skills/` entries: the visible text ends mid-entry at `skills/wiki/references/git-setup.md` with `... (truncated, 7820 more characters)`; remaining checksum lines are not in the chunk and are not summarized here.
**Covers:** `.gitattributes`, `.gitignore`, `AGENTS.md`, `ATTRIBUTION.md`, `CITATION.cff`, `CODEOWNERS`, `GEMINI.md`, `PRIVACY.md`, `RELEASE_MANIFEST.json` (truncated), `SECURITY.md`, `SHA256SUMS` (truncated), `WIKI.md`, `ZCODE.md`
