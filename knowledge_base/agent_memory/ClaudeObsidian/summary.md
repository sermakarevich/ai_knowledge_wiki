# Technical Analysis: AgriciDaniel/claude-obsidian

**Repository:** https://github.com/AgriciDaniel/claude-obsidian
**Version analyzed:** 2.2.0 (CITATION.cff:11-12, date-released 2026-09-10)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: personal and team knowledge decays when sources are detached from notes, claims lack provenance, parallel editors race shared files, and retrieval restarts from zero each session (README:47-60, README:84-89). Secondary problems are vault lock-in (cloud databases, plugin caches, silent model uploads) and unverifiable automation (simulated capabilities, silent overwrites) (README:39-41, README:90-91).

How the repo addresses it: a local-first Agent Skills package plus Claude Code plugin adapter that keeps the vault as ordinary Markdown/JSON/source files and organizes work as a retain-ground-connect-reuse loop with content-addressed source copies before synthesis (README:39-41, README:47-54). Authority, freshness, support, contradiction, confidence, and review state persist in source and claim ledgers so unsupported and contradictory claims stay visible (README:55-56). Mutation discipline is one logical operation applied as one recoverable, inspected transaction; parallel workers return drafts and a single orchestrator applies the bundle once (README:88-89, README:232-238). Fifteen skills share one evidence, vault-selection, and mutation rule set (README:176-177).

Primary user: an individual Obsidian vault owner/operator who captures local sources, curates linked notes, and queries accumulated evidence from a file-owned vault.

Explicit non-goals: not an automatic transcript recorder, cloud sync service, factual oracle, or substitute for backups and source control (README:93-94).

## 2. High-Level Architecture

```
                    ┌─ host agents (Claude Code, Codex, OpenCode,
                    │   Gemini, ZCode, Cursor, Windsurf)
                    │   invoke skills; may egress under own policy
                    ▼
┌──────────┐   ┌────────────┐   ┌──────────────────┐   ┌───────────────┐
│ inbox/   │──►│ .raw/ +    │──►│ wiki/ + ledgers  │──►│ query/retrieve│
│ intake   │   │ .manifest  │   │ + index/log/hot  │   │ lint/fold/    │
└──────────┘   └────────────┘   └──────────────────┘   │ canvas/bases  │
     │                │                  │             └───────────────┘
     │         create-only,              │                    │
     │         SHA-256 addressed         ▼                    ▼
     │                │          ┌───────────────┐   ┌───────────────┐
     └────────────────┴─────────►│ single txn    │──►│ .vault-meta/  │
              provenance         │ bundle apply  │   │ locks/journals│
              preserved          │ (inspect once)│   │ indexes/queue │
                                 └───────────────┘   └───────────────┘
```

Data-flow narrative:

1. Select vault. Resolution order is explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`, then one unambiguous initialized ancestor; selection exits without writing when uncertain (README:226-230, AGENTS.md:11-25).
2. Capture. Local sources enter through visible `inbox/`; immutable content-addressed byte copies land in `.raw/` before any synthesis, with `.raw/` payloads create-only and `inbox/` never auto-deleted (README:47-54, WIKI.md:9-33, WIKI.md:37-45).
3. Ground and connect. Source and claim ledgers record authority, freshness, support, contradiction, confidence, and review state; ingest builds linked pages, indexes, Maps of Content, methodology-aware structures, and Canvas views (README:55-56, README:47-60).
4. Transact. One logical mutation becomes one `claude-obsidian.transaction.v1` bundle: record expected SHA-256 of every target, merge worker drafts into one bundle, inspect, apply once, report operation ID and changed paths (README:232-238, WIKI.md:165-204). A changed target is a conflict, never a silent overwrite; prior state restores if apply cannot finish (README:240-242).
5. Reuse. Query, research, retrieve (BM25 local/deterministic, optional cosine rerank), lint, fold of the operation log, and Canvas/bases views operate on accumulated evidence instead of starting from zero (README:47-60, README:86-87, README:266-269).

Persistent state lives in the user vault directory itself: `inbox/`, `.raw/` plus `.manifest.json`, `wiki/` (index, log, hot, overview, sources/entities/concepts/questions/canvases, meta/ledgers `source-ledger.json` and `claim-ledger.json`), `.obsidian/` settings, `.claude-obsidian.json` identity, and ignored `.vault-meta/` runtime state (locks, journals, indexes, queue/config) (WIKI.md:9-33, .gitignore:134-169). Product source and user vault are separate directories; the checkout is not the vault (README:112, AGENTS.md:11-25).

## 3. The Vault and Transaction Bundle

Representation: the vault is a plain directory of Markdown with flat-YAML frontmatter, JSON ledgers, and source bytes — never a plugin cache or cloud database (README:39-41, WIKI.md:9-33). Every page carries flat YAML with plural keys and `YYYY-MM-DD` dates; required baseline properties are `type`, `title`, `status`, `created`, `updated`, `tags`, with `aliases` and `address` optional unless vault policy requires them (WIKI.md:49-68). One mutation is one `claude-obsidian.transaction.v1` bundle with `expected_hashes`, `writes`, `address_requests`, and `source_manifest_updates`; apply binds approval via the inspect result's exact `approval_sha256` so one vault's approval cannot be reused on another (WIKI.md:165-204). `wiki/index.md` entries must resolve and every canonical create/removal updates an active catalog or MOC in the same transaction; `wiki/log.md` is newest-first operation history and `wiki/hot.md` is short sanitized context, never a transcript (WIKI.md:112-139).

Named kinds/types (page-type vocabulary, declared once in `claude_obsidian/page_schema.py`, documented WIKI.md:72-91):

- `source` (WIKI.md:72-91) — traceable summary of one source identity; routable.
- `entity` (WIKI.md:72-91) — person, org, product, project, named thing; routable.
- `concept` (WIKI.md:72-91) — idea, framework, mechanism, definition; routable.
- `question` (WIKI.md:72-91) — scoped answer with visible evidence status; routable.
- `session` (WIKI.md:72-91) — user-approved conversation summary; routable.
- `comparison` (WIKI.md:72-91) — criteria-based contrast with cited support; not routable.
- `overview` (WIKI.md:72-91) — high-level map of a domain or vault; not routable.
- `meta` (WIKI.md:72-91) — index, log, cache, convention, maintenance; not routable.
- `fold` (WIKI.md:72-91) — extractive rollup of log entries; not routable.

Filing modes routing new notes without bulk-moving old ones (README:275-276, README:285-286): Generic (sources, concepts, entities, sessions; default), LYT (Maps of Content, atomic notes), PARA (Projects, Areas, Resources, Archives), Zettelkasten (stable identifiers, atomic notes, dense links).

Key queries operate on vault evidence: `wiki-query` answers read-only from relevant vault evidence; `wiki-retrieve` provides contextual prefixes, BM25, and optional cosine reranking; `wiki-lint` reports dead links, orphans, metadata gaps, stale indexes, and empty sections (README:176-177 skill tables). Vault-selection rule, verbatim (AGENTS.md:23-25):

```
explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`,
then an unambiguous vault at or above the current directory. Fail closed when
no vault is selected.
```

## 4. LLM / External Service Integration

The core calls no LLM or external API. `PRIVACY.md:1-7` states local-first with no telemetry: vault content stays on the selected filesystem and core makes no network requests. Image/PDF/EPUB support is metadata-only and URL/YouTube/OCR/transcription/extraction do not execute in core (PRIVACY.md:25-28).

All model and network activity is optional, explicit, and outside core:

- Host agent and web tools may send selected content under their own policies; autoresearch and URL cleaning via host web tools require an intentional workflow plus boundary consent (PRIVACY.md:1-7, PRIVACY.md:30-40).
- Contextual-prefix model calls occur only with the egress flag; model-based retrieval falls back to deterministic BM25 when embedding/reranking cannot be trusted (PRIVACY.md:30-40, README:266-269).
- URL and YouTube require validated consent plans plus a configured external runner; OCR requires a local-file consent plan plus a configured external runner; remote Ollama endpoints are refused without opt-in; external-capture argv plans are inert until revalidated before use (overview capability table, PRIVACY.md:30-40).
- Obsidian CLI is optional for reads/search; filesystem transport remains available (overview capability table).
- `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1` is explicit user consent for bounded sanitized `wiki/hot.md` injection; external-vault routing additionally requires the exact canonical path in `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` (PRIVACY.md:9-20).

Environment variables: `CLAUDE_OBSIDIAN_VAULT` (vault selection), `CLAUDE_OBSIDIAN_SESSION_CONTEXT` (opt-in hot-context injection), `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` (external-vault routing), plus `GENERATED_AT` and `OPERATION_ID` as caller-supplied init parameters in the documented flow (README:126-127). No model API keys are defined in the covered pages; credentials must never appear in notes, URL queries, tracked config, bundles, or capture queues (PRIVACY.md:43-47).

## 5. The Capture-Ground-Connect-Reuse Pipeline

Primary workflow is the knowledge loop — capture with context, ground claims, connect knowledge, reuse the vault — executed through skills under the single-transaction rule (README:47-60, README:176-177).

1. Provision vault with dry-run-first plan. `init PATH` plans or creates a separate vault; `adopt PATH` does the same non-destructively for an existing Obsidian vault; both require copying the plan's `approved_plan_sha256` and re-invoking with `--apply` (README:126-127, README:135-136, AGENTS.md:27-34).
2. Route and diagnose. `wiki` skill initializes or adopts a vault, diagnoses readiness, and routes work; `contracts --verify --vault PATH` executes capability readiness contracts; `doctor --vault PATH` shows selection and readiness (README:176-177 skill tables; operator table README:296ff).
3. Capture with preflight. `capture plan --vault PATH [SOURCE ...]` runs a local capture preflight without writes; bounded content-addressed byte capture lands immutable copies in `.raw/` with SHA-256 addressing; remote locators must be validated HTTPS with no credentials (operator table README:296ff; WIKI.md:37-45).
4. Ingest into linked, provenance-recorded pages. `wiki-ingest` turns captured sources into linked pages plus source/claim ledger entries; `wiki-mode` routes new notes per Generic/LYT/PARA/Zettelkasten convention; Canvas and Bases skills maintain visual and tabular views (README:176-177 skill tables, README:275-276).
5. Apply as one inspected bundle. Parallel workers return drafts and evidence only; direct shared writes, `wiki-lock.sh`, and auto-commits are banned (AGENTS.md:49-62, GEMINI.md:19-21, ZCODE.md:25-27). The orchestrator merges drafts into one bundle, runs `transaction inspect BUNDLE --vault PATH`, then `transaction apply BUNDLE --vault PATH --approved-plan-sha256 HASH`; the core holds one process-lifetime lock, journals backups, uses atomic replacement with fsync, and restores prior state on incomplete apply (README:232-242, operator table README:296ff).
6. Reuse and maintain. `wiki-query` (read-only answers from evidence), `wiki-retrieve` (prefixes/BM25/optional cosine rerank), `wiki-lint` plus `lint --vault PATH` findings deterministic for the declared UTC date, `wiki-fold` (extractive traceable rollups of the operation log), `save` (one scoped answer or insight, never automatic transcript), `canvas`, `defuddle` (clean web content before ingestion), `autoresearch` (bounded web research with explicit egress and separate canonical merge) (README:150-158, README:176-177, operator table README:296ff).
7. Recover and checkpoint explicitly. `transaction recover --vault PATH [--force-stale-lock]` restores interrupted operations; git checkpoints, destructive repairs, network egress, and canonical research merges remain explicit operations (operator table README:296ff, README:242-244).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README` | overview pp. README:14-296 | Product contract: loop, 15 skills, transaction model, capability boundaries, modes, operator CLI reference |
| `AGENTS.md` | AGENTS.md:1-62 | Agent contract: product-vs-vault boundary, vault resolution, skill layout, single-bundle mutation ban on direct writes |
| `WIKI.md` | WIKI.md:9-204 | Vault schema: directory layout, source invariants, frontmatter, page types, transaction bundle and approval binding |
| `PRIVACY.md` | PRIVACY.md:1-47 | Local-first/no-telemetry statement, session-context consent vars, egress and credential rules |
| `SECURITY.md` | SECURITY.md:5-61 | Trust hierarchy (vault/web as untrusted data), lock/journal/atomic-replace invariants, legacy lock note |
| `scripts/claude-obsidian.py` | wrapper (README:296) | Single CLI wrapper for init/adopt/migrate/transaction/lint/contracts/capture |
| `skills/<name>/SKILL.md` (15 skills) | per-skill contracts (README:215-218) | Canonical skill definitions; core workflows `wiki`, `save`, `wiki-ingest`, `wiki-query`, `wiki-lint` (AGENTS.md:37-47) |
| `GEMINI.md` / `ZCODE.md` | GEMINI.md:1-21, ZCODE.md:1-27 | Thin host adapters deferring to AGENTS.md; `setup-multi-agent.sh --host` install flow |
| `CITATION.cff` | CITATION.cff:1-12 | Citation metadata: title, author alias, license MIT, version 2.2.0, released 2026-09-10 |
| `RELEASE_MANIFEST.json` | 1241 lines, truncated in chunk | Deterministic artifact manifest: per-file path, mode 0644, sha256, size |
| `SHA256SUMS` | 205 lines, truncated in chunk | Independent hash verification lines mirroring the manifest |
| `.gitattributes` | .gitattributes:1-4 | `* -text` byte-identity guard for frontmatter and content hashes cross-platform |
| `.gitignore` | .gitignore:1-169 | Excludes runtime/secret/personal state while negating back dashboard base and lock gitkeep |
| `CODEOWNERS` | CODEOWNERS:2 | Single default owner `@AgriciDaniel` |
| `ATTRIBUTION.md` | ATTRIBUTION.md:11-60 | Architectural credit (Karpathy LLM Wiki pattern), excluded contributor-vault state, two adopted v2.0.0 designs |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| (standard library only) | no constraint string in covered pages | Entire core runtime; `SECURITY.md:13-22` describes core as standard-library Python with user filesystem permissions |
| Obsidian CLI | version string not in covered pages; optional | Optional reads/search; filesystem transport remains available |
| External runner (URL/YouTube/OCR/transcription/extraction) | version string not in covered pages; required only for those paths | Executes consent-planned remote or heavy extraction core refuses to run |
| Remote embedding/rerank model behind egress flag | version string not in covered pages; optional | Contextual prefixes and cosine reranking; falls back to deterministic BM25 |

No required third-party package and no exact constraint string appears in the two covered component pages. `RELEASE_MANIFEST.json` and `SHA256SUMS` pin artifact file hashes, not package versions, and both are truncated in the chunk (top-level-files p. 144-146).

## 8. CLI / Usage Surface

Entry points: `python3 scripts/claude-obsidian.py` wrapper (README:296); skill invocations `/claude-obsidian:<name>` on Claude Code (e.g. `/claude-obsidian:wiki`, `:wiki-ingest`, `:save`, `:wiki-query`, `:wiki-lint`) and native Agent Skills invocation on other hosts; `bash scripts/setup-multi-agent.sh --host <codex|gemini|...>` for Codex/OpenCode/Gemini/ZCode and workspace-local skill discovery for Cursor/Windsurf (README:150-170). `init` requires `--generated-at`, `--operation-id`, then `--approved-plan-sha256` with `--apply` (README:126-127).

Commands:

| Command | Effect |
|---|---|
| `doctor --vault PATH` | Show vault selection and readiness |
| `init PATH [--approved-plan-sha256 HASH --apply]` | Plan or create a separate vault |
| `adopt PATH [--approved-plan-sha256 HASH --apply]` | Plan or adopt an existing Obsidian vault |
| `migrate --vault PATH [--approved-plan-sha256 HASH --apply]` | Add v1 ledgers and configuration without rewriting legacy data |
| `transaction inspect BUNDLE --vault PATH` | Validate a write bundle without mutation |
| `transaction apply BUNDLE --vault PATH --approved-plan-sha256 HASH` | Apply one inspected, recoverable operation |
| `transaction recover --vault PATH [--force-stale-lock]` | Restore an interrupted operation |
| `lint --vault PATH [--as-of YYYY-MM-DD] [--exclude GLOB]...` | Emit findings deterministic for the declared UTC date |
| `contracts --verify --vault PATH` | Execute capability readiness contracts |
| `capture plan --vault PATH [SOURCE ...]` | Run a local capture preflight without writes |
| `capture apply --vault PATH [SOURCE ...]` | Effect cell truncated in source chunk; row exists but effect not summarized |

Environment variables:

| Variable | Role |
|---|---|
| `CLAUDE_OBSIDIAN_VAULT` | Explicit vault selection (highest precedence after `--vault`) |
| `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1` | Opt-in bounded sanitized `wiki/hot.md` injection |
| `CLAUDE_OBSIDIAN_SESSION_CONTEXT_VAULT` | Exact canonical path required for external-vault session routing |
| `GENERATED_AT` / `OPERATION_ID` | Caller-supplied init parameters in documented flow |

Configuration: `.claude-obsidian.json` (workspace identity and vault selection, nearest-ancestor lookup); vault-local `.obsidian/` settings remain user-controlled; `.vault-meta/` holds ignored locks, journals, indexes, queue/config (WIKI.md:9-33, .gitignore:134-169). Capabilities are stated via detection with declared maturity and clear degradation (README:90-91).

## 9. Extensibility Points

- New workflow skill: add `skills/<name>/SKILL.md` with exact `name` and `description` frontmatter under the shared evidence, vault-selection, and mutation rules (AGENTS.md:37-47, README:176-177, README:215-218).
- New host adapter: mirror `GEMINI.md`/`ZCODE.md` thin pattern — defer to `AGENTS.md`, install skill links via `scripts/setup-multi-agent.sh --host <name>` preview-then-`--apply`, restate single-bundle and egress-consent rules (GEMINI.md:1-21, ZCODE.md:1-27).
- New filing convention: extend `wiki-mode` routing (Generic/LYT/PARA/Zettelkasten) so new notes route differently without bulk-moving existing knowledge (README:275-276, README:285-286).
- New page kind or frontmatter rule: extend the vocabulary declared once in `claude_obsidian/page_schema.py` and documented in `WIKI.md:72-91`, keeping flat YAML, plural keys, and `YYYY-MM-DD` dates (WIKI.md:49-68).
- New retrieval or preprocessing path: add under `wiki-retrieve` (prefixes/BM25/cosine), `defuddle` (web cleaning before ingestion), or `autoresearch` (bounded egress plus separate canonical merge) rather than inside core, preserving core's no-network invariant (README:176-177 skill tables, PRIVACY.md:1-7).
- New view: extend `canvas` (Canvas creation/maintenance) or `obsidian-bases` (native `.base` tables/cards/filters/formulas) and reference outputs (`obsidian-markdown` for OFM links/embeds/callouts) (README:176-177 skill tables).
- New readiness gate: extend `contracts --verify` capability contracts so missing adapters degrade clearly instead of being simulated (README:90-91, operator table README:296ff).

## 10. Limitations and Gotchas

- **PDF and EPUB have metadata only, no built-in semantic extraction.** Hash, size, and metadata are retained; content understanding needs an external path (overview capability table, PRIVACY.md:25-28).
- **URL, YouTube, OCR, and transcription do not run in core.** Each needs a validated consent plan and a configured external runner; without one the workflow stops rather than simulating results (overview capability table, PRIVACY.md:25-28, PRIVACY.md:30-40).
- **Every shared mutation pays the inspect-then-apply price.** Workers return drafts only; direct shared writes, `wiki-lock.sh` (legacy compatibility only, SECURITY.md:60-61), and auto-commits are banned, and `transaction apply` requires the exact `approval_sha256` — cross-vault approval reuse fails (AGENTS.md:49-62, WIKI.md:193-204).
- **Vault selection fails closed.** Ambiguous resolution writes nothing; operators must set `--vault`, `CLAUDE_OBSIDIAN_VAULT`, or ensure one unambiguous initialized ancestor (README:226-230, AGENTS.md:23-25).
- **Remote-model retrieval is gated and fallback-prone by design.** Contextual prefixes and cosine reranking require explicit egress consent and fall back to deterministic BM25 when embeddings cannot be trusted; high-risk accepted claims require two independent sources and grounded refusal is preferred over invented citation (README:266-269, PRIVACY.md:30-40).
- **Source-chunk truncation limits this analysis.** The operator-reference block cuts mid-table (`capture apply` effect cell missing) and `RELEASE_MANIFEST.json`/`SHA256SUMS` are cut inside `docs/` and `skills/` entries respectively; entries past the cut were not summarized and are not covered here (overview p. 135, top-level-files pp. 144-146).

## 11. How It Compares to Alternatives

- **Obsidian (native app and vault format).** The repo does not replace Obsidian; output is plain Markdown for portability with Obsidian navigation and visual exploration including Graph view and Canvas (README:66-67, README:74-76). Positioning: agent-side discipline and provenance layer on top of user-owned Obsidian files.
- **Karpathy LLM Wiki pattern (architectural basis).** Credited as the pattern's origin with independent implementation and nothing copied (ATTRIBUTION.md:11). Positioning: this repo is the operationalization — ledgers, transactions, and skills — rather than the pattern sketch.
- **Nomic embedding prefix convention (`search_query`/`search_document` with `with_task_prefix`).** Adopted v2.0.0 design credited to maartengoet PR #77, alongside BM25 fallback order `bm25_score`-before-`score` from vinsocci PR #62 (ATTRIBUTION.md:49-60). Positioning: standards-compatible retrieval defaults with deterministic BM25 fallback instead of embedding-only recall.
- **Contributor-vault plugins (Calendar, Thino, Excalidraw, Banners) and ITS CSS snippets.** Explicitly scoped to private contributor state and excluded from the deterministic public artifact (ATTRIBUTION.md:21-45). Positioning: the distributable stays a minimal reproducible seed while personal visualization state stays out of the release.

Positioning sentence: against file-based notes tools, RAG-pattern sketches, embedding providers, and personal plugin setups, this repo competes as a provenance-first, transaction-guarded operating layer that keeps knowledge as ordinary Obsidian files with every claim traceable and every write recoverable.

## Appendix: Selected Code Snippets

1. Vault resolution order — `AGENTS.md:23-25`:

```
explicit `--vault`, `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`,
then an unambiguous vault at or above the current directory. Fail closed when
no vault is selected.
```

2. User-vault root layout — `WIKI.md:9-33`:

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

3. Page frontmatter convention — `WIKI.md:49-68`:

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

4. Byte-identity guard — `.gitattributes:4` (header comment `.gitattributes:1-3`):

```
* -text
```
