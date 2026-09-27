# AgriciDaniel/claude-obsidian
PDF-Location: https://github.com/AgriciDaniel/claude-obsidian
Source: https://github.com/AgriciDaniel/claude-obsidian
Kind: repo
Fetched: 2026-09-26T13:42:14.056973+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# AgriciDaniel/claude-obsidian

Commit: 32ac5a02c4e082e4a5628ca810776375e134708e

## README

<p align="center">
  <img src="assets/cover.png" alt="claude-obsidian cover featuring an astronaut, the Obsidian crystal, and a connected knowledge graph" width="100%">
</p>

<h1 align="center">claude-obsidian</h1>

<p align="center">
  <strong>Build an Obsidian knowledge base that becomes more useful every time you use it.</strong><br>
  Capture sources, create connected notes, retrieve grounded answers, and keep the vault healthy—without giving up ownership of your files.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb.svg" alt="MIT license"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-2563eb" alt="Agent Skills compatible"></a>
  <a href="https://code.claude.com/docs/en/plugins"><img src="https://img.shields.io/badge/Claude%20Code-plugin-7c3aed" alt="Claude Code plugin"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/release-v2.2.0-d97745" alt="Release v2.2.0"></a>
</p>

<p align="center">
  <a href="#from-source-to-living-knowledge">See the workflow</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#15-skills-one-system">Explore the skills</a> ·
  <a href="docs/install-guide.md">Installation guide</a> ·
  <a href="docs/windows-wsl.md">Windows &amp; WSL</a>
</p>

claude-obsidian is a local-first knowledge system for Claude Code and compatible
[Agent Skills](https://agentskills.io) hosts. It turns source material into
linked, source-cited Obsidian pages; answers from the evidence already in the
vault; and provides explicit workflows for research, retrieval, maintenance,
and visual mapping.

Your vault remains a normal directory of Markdown, JSON, and source files. It is
not hidden in a plugin cache, locked in a cloud database, or silently uploaded
to a model.



## From source to living knowledge

Most AI note workflows stop after saving text. claude-obsidian is organized
around a repeatable loop: retain the source, ground the claims, connect the
knowledge, then put it back to work.

![The claude-obsidian compounding knowledge loop](assets/diagrams/knowledge-loop.svg)

- **Capture with context.** Bring local sources through a visible inbox and
  preserve immutable, content-addressed copies before synthesis.
- **Ground every important claim.** Source and claim ledgers retain authority,
  freshness, support, contradiction, confidence, and review state.
- **Connect what you learn.** Build linked pages, indexes, Maps of Content,
  methodology-aware structures, and Obsidian Canvas views.
- **Use the vault again.** Query, research, retrieve, lint, and fold what is
  already known instead of starting every conversation from zero.



## See the vault

The output is meant to remain useful with or without an agent: plain Markdown
for portability, Obsidian for navigation and visual exploration.

<p align="center">
  <img src="assets/screenshots/graph-view.png" alt="Example claude-obsidian vault in Obsidian Graph view" width="49%">
  <img src="assets/screenshots/wiki-map-view.png" alt="Example claude-obsidian knowledge map in Obsidian Canvas" width="49%">
</p>

<p align="center">
  <sub>Linked knowledge in Graph view · A visual knowledge map in Obsidian Canvas</sub>
</p>



## Why it feels different

- **Local by default.** The vault is user-owned and works as ordinary files.
  Network egress is a separate, explicit decision.
- **Sources survive the summary.** Notes point back to durable source evidence;
  unsupported and contradictory claims remain visible.
- **Knowledge compounds deliberately.** Ingestion, querying, linting, retrieval,
  research, and rollups share one provenance-aware model.
- **Parallel agents cannot race the vault.** Workers return drafts. One
  orchestrator inspects and applies one recoverable transaction.
- **Capabilities are stated honestly.** Optional tools are detected, maturity
  is declared, and missing adapters degrade clearly instead of being simulated.

This is not an automatic transcript recorder, a cloud sync service, a factual
oracle, or a substitute for backups and source control.



## Quick start

The safest first run uses a source checkout and a separate user vault. Every
mutating setup command previews its exact operation before it can apply.



### 1. Get the product

```bash
git clone https://github.com/AgriciDaniel/claude-obsidian.git
cd claude-obsidian
```

The checkout contains the product. It is not your knowledge vault.



### 2. Initialize a separate vault

```bash
export GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
export OPERATION_ID="init-reviewed"

python3 scripts/claude-obsidian.py init "$HOME/Documents/MyKnowledgeVault" \
  --generated-at "$GENERATED_AT" --operation-id "$OPERATION_ID"
```

Review the JSON plan and copy its `approved_plan_sha256`, then apply that exact
operation:

```bash
python3 scripts/claude-obsidian.py init "$HOME/Documents/MyKnowledgeVault" \
  --generated-at "$GENERATED_AT" --operation-id "$OPERATION_ID" \
  --approved-plan-sha256 "<sha256-from-the-plan>" --apply
```

For an existing Obsidian vault, use the non-destructive `adopt` workflow
described in the [installation guide](docs/install-guide.md#adopt-an-existing-vault).



### 3. Start from the vault

Open the new directory in Obsidian, then run Claude Code from that directory
with the local plugin:

```bash
cd "$HOME/Documents/MyKnowledgeVault"
claude --plugin-dir /absolute/path/to/claude-obsidian
```

Start with:

```text
/claude-obsidian:wiki
```

Then place a source in `inbox/` and invoke
`/claude-obsidian:wiki-ingest`. Save an answer explicitly with
`/claude-obsidian:save`; ask the vault with `/claude-obsidian:wiki-query`.

For Codex, OpenCode, Gemini, or ZCode, preview and then apply the portable
skill links from the product checkout:

```bash
bash scripts/setup-multi-agent.sh --host codex
bash scripts/setup-multi-agent.sh --host codex --apply
```

Cursor and Windsurf use workspace-local skill discovery. Marketplace setup,
every supported host, vault adoption, upgrades, and uninstall steps are covered
in the [full installation guide](docs/install-guide.md).



## 15 skills, one system

The skills are small enough to invoke directly and coordinated enough to share
the same evidence, vault-selection, and mutation rules.



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

Claude Code exposes namespaced invocations such as
`/claude-obsidian:wiki-lint`; other hosts use their native Agent Skills
invocation. Trigger phrases and exact contracts live in each
`skills/<name>/SKILL.md`.



## Trust is part of the architecture

![The claude-obsidian product and vault trust boundary](assets/diagrams/product-vault-boundary.svg)

The product never treats a source checkout, plugin cache, or contributor state
as the default vault. A vault is selected explicitly, through
`CLAUDE_OBSIDIAN_VAULT`, by the nearest `.claude-obsidian.json`, or by one
unambiguous initialized ancestor. If selection is uncertain, the command exits
without writing.

One logical knowledge operation is one recoverable transaction:

1. Read every target and record its expected SHA-256.
2. Let parallel workers return drafts and evidence only.
3. Merge the complete change into one operation bundle.
4. Inspect the bundle, then apply it once.
5. Report the operation ID and exact changed paths.

The core holds one process-lifetime vault lock, journals backups, uses atomic
replacement, and restores the prior state if an apply cannot finish. A changed
target is a conflict, never a silent overwrite. Git checkpoints, destructive
repairs, network egress, and canonical research merges remain explicit
operations.

Read the [transaction contract](skills/wiki/references/operation-transactions.md),
[provenance contract](skills/wiki/references/provenance.md), and
[Compound Vault architecture](docs/compound-vault-guide.md) for the
machine-facing detail.



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

High-risk accepted claims require two independent sources. Unsupported or
contradictory evidence stays visible, and a grounded refusal is preferred over
an invented citation. Model-based retrieval falls back to deterministic BM25
when the embedding or reranking stage cannot be trusted.



## Shape the vault to the way you think

`wiki-mode` can route new notes using four methodologies without bulk-moving
existing knowledge:

| Mode | Filing principle |
|---|---|
| Generic | Sources, concepts, entities, and sessions |
| LYT | Maps of Content and linked atomic notes |
| PARA | Projects, Areas, Resources, and Archives |
| Zettelkasten | Stable identifiers, atomic notes, and dense links |

Generic is the default when no mode is configured. Switching modes changes how
new notes are routed; it does not silently reorganize old ones. See the
[methodology modes guide](docs/methodology-modes-guide.md).



## Operator reference

<details>
<summary><strong>Portable CLI</strong></summary>

The wrapper is `python3 scripts/claude-obsidian.py`.

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
| `capture apply --vault PATH [SOURCE ...]`

... (truncated, 5061 more characters)

## Top-level layout

- .claude-plugin/ (dir, 2 files, ~50 lines)
- .cursor/ (dir, 1 files, ~32 lines)
- .gitattributes (~4 lines)
- .github/ (dir, 6 files, ~288 lines)
- .gitignore (~155 lines)
- .windsurf/ (dir, 1 files, ~15 lines)
- agents/ (dir, 3 files, ~311 lines)
- AGENTS.md (~97 lines)
- assets/ (dir, 5 files, ~246 lines)
- ATTRIBUTION.md (~69 lines)
- CHANGELOG.md (~393 lines)
- CITATION.cff (~20 lines)
- claude_obsidian/ (dir, 22 files, ~19458 lines)
- CODE_OF_CONDUCT.md (~22 lines)
- CODEOWNERS (~2 lines)
- config/ (dir, 5 files, ~1149 lines)
- CONTRIBUTING.md (~62 lines)
- docs/ (dir, 5 files, ~770 lines)
- examples/ (dir, 13 files, ~178 lines)
- GEMINI.md (~24 lines)
- hooks/ (dir, 2 files, ~66 lines)
- LICENSE (~21 lines)
- Makefile (~66 lines)
- PRIVACY.md (~47 lines)
- README.md (~397 lines)
- RELEASE_MANIFEST.json (~1240 lines)
- scripts/ (dir, 16 files, ~5475 lines)
- SECURITY.md (~71 lines)
- SHA256SUMS (~204 lines)
- skills/ (dir, 34 files, ~3230 lines)
- templates/ (dir, 11 files, ~146 lines)
- tests/ (dir, 60 files, ~19711 lines)
- WIKI.md (~260 lines)
- ZCODE.md (~30 lines)

