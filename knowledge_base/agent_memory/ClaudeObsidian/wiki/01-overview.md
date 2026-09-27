> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** claude-obsidian is a local-first knowledge system that turns source material into linked, source-cited Obsidian pages and answers from vault evidence under explicit, recoverable transactions.
## Key points
- Turns source material into linked, source-cited Obsidian pages and answers from evidence already in the vault, with explicit workflows for research, retrieval, maintenance, and visual mapping (README:33-37).
- Keeps the vault as a normal directory of Markdown, JSON, and source files, never hidden in a plugin cache, locked in a cloud database, or silently uploaded to a model (README:39-41).
- Organizes work as a loop — retain the source, ground the claims, connect the knowledge, then put it back to work — with content-addressed copies before synthesis (README:47-54).
- Retains authority, freshness, support, contradiction, confidence, and review state in source and claim ledgers so unsupported and contradictory claims remain visible (README:55-56).
- Prevents parallel-agent races by having workers return drafts while one orchestrator inspects and applies one recoverable transaction (README:88-89).
- Selects a vault explicitly via `CLAUDE_OBSIDIAN_VAULT`, nearest `.claude-obsidian.json`, or one unambiguous initialized ancestor, exiting without writing when selection is uncertain (README:226-230).
- Applies one logical knowledge operation as one recoverable transaction: record expected SHA-256, merge drafts into one bundle, inspect, apply once, report operation ID and changed paths (README:232-238).
---
## From source to living knowledge
Loop (`README:47-60`):
- **Capture with context.** Bring local sources through a visible inbox and preserve immutable, content-addressed copies before synthesis.
- **Ground every important claim.** Source and claim ledgers retain authority, freshness, support, contradiction, confidence, and review state.
- **Connect what you learn.** Build linked pages, indexes, Maps of Content, methodology-aware structures, and Obsidian Canvas views.
- **Use the vault again.** Query, research, retrieve, lint, and fold what is already known instead of starting every conversation from zero.

Verbatim positioning (`README:14-15`):
> **Build an Obsidian knowledge base that becomes more useful every time you use it.**<br>
> Capture sources, create connected notes, retrieve grounded answers, and keep the vault healthy—without giving up ownership of your files.
## See the vault
Output is plain Markdown for portability with Obsidian for navigation and visual exploration (`README:66-67`); screenshots show linked knowledge in Graph view and a visual knowledge map in Obsidian Canvas (`README:74-76`).
## Why it feels different
- **Local by default.** The vault is user-owned and works as ordinary files. Network egress is a separate, explicit decision (README:82-83).
- **Sources survive the summary.** Notes point back to durable source evidence; unsupported and contradictory claims remain visible (README:84-85).
- **Knowledge compounds deliberately.** Ingestion, querying, linting, retrieval, research, and rollups share one provenance-aware model (README:86-87).
- **Parallel agents cannot race the vault.** Workers return drafts. One orchestrator inspects and applies one recoverable transaction (README:88-89).
- **Capabilities are stated honestly.** Optional tools are detected, maturity is declared, and missing adapters degrade clearly instead of being simulated (README:90-91).

Explicit non-goals (`README:93-94`): not an automatic transcript recorder, a cloud sync service, a factual oracle, or a substitute for backups and source control.
## Quick start
Safest first run uses a source checkout and a separate user vault; every mutating setup command previews its exact operation before it can apply (`README:100-101`).
### 1. Get the product
```bash
git clone https://github.com/AgriciDaniel/claude-obsidian.git
cd claude-obsidian
```
The checkout contains the product. It is not your knowledge vault (README:112).
### 2. Initialize a separate vault
```bash
export GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
export OPERATION_ID="init-reviewed"

python3 scripts/claude-obsidian.py init "$HOME/Documents/MyKnowledgeVault" \
  --generated-at "$GENERATED_AT" --operation-id "$OPERATION_ID"
```
Review the JSON plan and copy its `approved_plan_sha256`, then apply that exact operation (README:126-127):
```bash
python3 scripts/claude-obsidian.py init "$HOME/Documents/MyKnowledgeVault" \
  --generated-at "$GENERATED_AT" --operation-id "$OPERATION_ID" \
  --approved-plan-sha256 "<sha256-from-the-plan>" --apply
```
Exact parameter names: `--generated-at`, `--operation-id`, `--approved-plan-sha256`, `--apply`. For an existing Obsidian vault, use the non-destructive `adopt` workflow (README:135-136).
### 3. Start from the vault
```bash
cd "$HOME/Documents/MyKnowledgeVault"
claude --plugin-dir /absolute/path/to/claude-obsidian
```
Start with `/claude-obsidian:wiki`, place a source in `inbox/` and invoke `/claude-obsidian:wiki-ingest`; save with `/claude-obsidian:save`; ask with `/claude-obsidian:wiki-query` (README:150-158). Other hosts (Codex, OpenCode, Gemini, ZCode) use `bash scripts/setup-multi-agent.sh --host codex` preview then `--apply` (README:160-166); Cursor and Windsurf use workspace-local skill discovery (README:168-170).
## 15 skills, one system
Skills share the same evidence, vault-selection, and mutation rules (README:176-177). Claude Code exposes namespaced invocations such as `/claude-obsidian:wiki-lint`; other hosts use native Agent Skills invocation; trigger phrases and exact contracts live in each `skills/<name>/SKILL.md` (README:215-218).
### Build and use the wiki
| Skill | What it does |
|---|---|
| `wiki` | Initializes or adopts a vault, diagnoses readiness, and routes work |
| `save` | Saves one scoped answer or insight—never an automatic transcript |
| `wiki-ingest` | Turns captured sources into linked pages and provenance records |
| `wiki-query` | Answers read-only from relevant vault evidence |
| `wiki-lint` | Reports dead links, orphans, metadata gaps, stale indexes, and empty sections |
### Extend the workflow
| Skill | What it adds |
|---|---|
| `autoresearch` | Bounded web research with explicit egress and a separate canonical merge |
| `canvas` | Wiki-scoped Obsidian Canvas creation and maintenance |
| `defuddle` | Clean, readable web content before ingestion |
| `wiki-fold` | Extractive, traceable rollups of the operation log |
| `wiki-mode` | Generic, LYT, PARA, or Zettelkasten filing conventions |
| `wiki-retrieve` | Contextual prefixes, BM25, and optional cosine reranking |
| `wiki-cli` | Obsidian CLI reads and search with transaction-safe writes |
### Reference skills
| Skill | What it provides |
|---|---|
| `obsidian-markdown` | Correct Obsidian Flavored Markdown, links, embeds, and callouts |
| `obsidian-bases` | Native `.base` tables, cards, filters, formulas, and summaries |
| `think` | A structured observe, listen, connect, create, and grow review loop |
## Trust is part of the architecture
One logical knowledge operation is one recoverable transaction (README:232-238):
1. Read every target and record its expected SHA-256.
2. Let parallel workers return drafts and evidence only.
3. Merge the complete change into one operation bundle.
4. Inspect the bundle, then apply it once.
5. Report the operation ID and exact changed paths.

The core holds one process-lifetime vault lock, journals backups, uses atomic replacement, and restores the prior state if an apply cannot finish; a changed target is a conflict, never a silent overwrite (README:240-242). Git checkpoints, destructive repairs, network egress, and canonical research merges remain explicit operations (README:242-244).
## Honest capability boundaries
| Input or capability | Current support |
|---|---|
| Local filesystem sources | Implemented bounded, content-addressed byte capture |
| Images | Metadata, hash, size, and bounded dimensions when available |
| PDF and EPUB | Metadata, hash, and size; no built-in semantic extraction |
| URL and YouTube | Validated consent plans; a configured external runner is required |
| OCR | Local-file consent plan; a configured external runner is required |
| BM25 retrieval | Local and deterministic |
| Contextual prefixes or remote models | Optional and gated by explicit egress consent |
| Obsidian CLI | Optional for reads/search; filesystem transport remains available |

High-risk accepted claims require two independent sources; unsupported or contradictory evidence stays visible; grounded refusal is preferred over invented citation; model-based retrieval falls back to deterministic BM25 when embedding/reranking cannot be trusted (README:266-269).
## Shape the vault to the way you think
`wiki-mode` routes new notes using four methodologies without bulk-moving existing knowledge (README:275-276):
| Mode | Filing principle |
|---|---|
| Generic | Sources, concepts, entities, and sessions |
| LYT | Maps of Content and linked atomic notes |
| PARA | Projects, Areas, Resources, and Archives |
| Zettelkasten | Stable identifiers, atomic notes, and dense links |

Generic is the default when no mode is configured; switching modes changes how new notes are routed, not old ones (README:285-286).
## Operator reference
Wrapper is `python3 scripts/claude-obsidian.py` (README:296).
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

Note: the source chunk truncates the operator-reference block mid-table (the `capture apply --vault PATH [SOURCE ...]` row has no Effect cell) and ends with an unexpanded `Macro components` stub listing only `top-level-files/`; contents beyond that cut were not summarized.
---
**Covers:** README (repo overview, knowledge loop, skills tables, trust/transaction model, capability boundaries, vault modes, operator CLI reference)
