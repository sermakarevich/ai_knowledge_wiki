---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: AgriciDaniel/claude-obsidian

### Q1. What is the four-step knowledge loop at the heart of claude-obsidian, and what must happen before any synthesis?
> [!tip]- Answer
> The loop is retain the source, ground the claims, connect the knowledge, then put it back to work. Before any synthesis, sources pass through a visible inbox and get immutable, content-addressed copies in `.raw/`. See [[wiki/01-overview|Overview]].

### Q2. How does claude-obsidian prevent parallel agents from racing when mutating the vault?
> [!tip]- Answer
> Parallel workers return drafts and evidence only; a single orchestrator merges them into one operation bundle, inspects it, and applies it once as a recoverable transaction. A changed target is treated as a conflict, never silently overwritten, with journaled backups enabling restore. See [[wiki/01-overview|Overview]].

### Q3. How does vault selection work, and what happens when it is ambiguous?
> [!tip]- Answer
> Selection resolves via explicit `--vault`, then `CLAUDE_OBSIDIAN_VAULT`, then the nearest `.claude-obsidian.json`, then one unambiguous initialized ancestor. When selection is uncertain it fails closed, exiting without writing rather than guessing a vault. See [[wiki/01-overview|Overview]].

### Q4. Which skills handle the core wiki lifecycle versus retrieval and maintenance, and what are their roles?
> [!tip]- Answer
> The core lifecycle uses `wiki` for init/adopt/routing, `wiki-ingest` for turning sources into linked pages, `wiki-query` for read-only answers from vault evidence, `save` for scoped insights, and `wiki-lint` for dead links, orphans, and metadata gaps. Retrieval and reuse come from `wiki-retrieve` with BM25 plus optional reranking, `wiki-fold` rollups, `autoresearch` bounded web research, and `canvas` mapping. See [[wiki/01-overview|Overview]].

### Q5. What are the stated capability boundaries and non-goals of claude-obsidian?
> [!tip]- Answer
> Local filesystem capture and BM25 retrieval are fully implemented, while PDF/EPUB give metadata only and URL, YouTube, OCR, and remote-model calls need explicit egress consent plus a configured external runner. It is explicitly not an automatic transcript recorder, cloud sync service, factual oracle, or substitute for backups. See [[wiki/01-overview|Overview]].

### Q6. What is the fixed user-vault layout and which invariants protect sources and history?
> [!tip]- Answer
> The vault root holds `inbox/`, `.raw/`, `wiki/`, `.vault-meta/`, and `.obsidian/`, with `wiki/` containing `index.md`, `log.md`, `hot.md`, `overview.md`, sources, entities, concepts, questions, canvases, and `meta/ledgers/`. Payloads in `.raw/` are create-only and content-addressed, `inbox/` is never auto-deleted, `log.md` is newest-first history, and `hot.md` is bounded context, never a transcript. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Should a privacy-conscious team adopt claude-obsidian as its shared team knowledge base, and why or why not?
> [!tip]- Answer
> Recommend it only if the team accepts local-first, single-user/single-vault operation with explicit transactions and no built-in cloud sync or multi-user sandboxing. Its strengths are no telemetry, opt-in session injection, create-only evidence, and inspected bundles, but shared use needs external git discipline and explicit egress consent for web or model calls. See [[wiki/02-top-level-files|top-level-files]].
