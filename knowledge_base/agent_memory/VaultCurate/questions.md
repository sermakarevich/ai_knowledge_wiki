---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: notoriouslab/vault-curate

### Q1. What is Vault Curate and which three capabilities work with zero setup?
> [!tip]- Answer
> Vault Curate is an Obsidian plugin whose job is "Find, connect, and rediscover your notes" via semantic search and connection-finding across local notes. Find (semantic search), Connect (relation graphs and semantic paths), and Rediscover (Hot/Cold surfacing) work out of the box, while AI curation stays off until explicitly enabled. See [[wiki/01-overview|Overview]].

### Q2. How does Vault Curate's fused search find a note by meaning rather than literal characters?
> [!tip]- Answer
> Each query runs Keyword (exact phrases), Semantic (different wording, same meaning), and Fuzzy-title (typos and spelling variants) searches at once and merges them into one ranking. The built-in model reads long notes in full up to 60,000 characters, and frontmatter tags plus synonym lists further shape ranking. See [[wiki/01-overview|Overview]].

### Q3. How do you read a relation-graph Canvas and turn suggestions into real links?
> [!tip]- Answer
> The center note sits amid semantic neighbors with similarity-scored edges: purple means close but unlinked, gray with arrows means already wikilinked, cyan nodes are Cold notes, and green edges mark query relevance. Checking pairs in the promote dialog writes them as wikilinks into notes' Related sections, while ✕ dismissal hides a pair permanently across renames and rebuilds. See [[wiki/01-overview|Overview]].

### Q4. How does Hot/Cold tiering decide which notes Discover resurfaces?
> [!tip]- Answer
> Notes are auto-tiered by internal links plus recency: Hot notes are linked or recently created/edited, while Cold notes are orphans untouched beyond the tunable Hot-window cutoff, with edits (not mere opens) counting as use. Current-note Discover surfaces Cold notes related to the open file and global Discover surfaces forgotten notes related to recent focus, exportable as a topic-grouped MOC. See [[wiki/01-overview|Overview]].

### Q5. What are Vault Curate's local-first privacy guarantees and its Chinese/mobile story?
> [!tip]- Answer
> Nothing leaves the machine by default: the ~110 MB embedding model downloads once, needs no API key, and data goes out only if the user points optional AI curation at a cloud service. The built-in model is strong on Chinese names and colloquial phrases with Traditional-to-Simplified matching under the hood, and phones reuse the desktop-built index via sync with no re-indexing. See [[wiki/01-overview|Overview]].

### Q6. How does the two-stage esbuild bundle ship Vault Curate as a single Obsidian plugin?
> [!tip]- Answer
> The build first bundles the embedding worker and the k-NN worker, then bundles the main plugin from src/main.ts with both worker sources inlined, so Community-store installs of main.js plus manifest and styles still run workers at runtime. Plugin identity is pinned as id vault-curate version 1.11.0 with minAppVersion 1.7.2 and isDesktopOnly false, and compiler/test behavior is fixed by tsconfig (ES2018, strict) and vitest (happy-dom, obsidian stub). See [[wiki/02-top-level-files|Top-level files]].

### Q7. Would you recommend Vault Curate for a large bilingual vault with many forgotten notes, and why?
> [!tip]- Answer
> Yes for that profile: fused semantic search plus Traditional/Simplified matching helps retrieval across languages, and Hot/Cold Discover with MOC export directly targets forgotten-note rediscovery. The main caveats are the one-time ~110 MB model download, desktop-first indexing, and the suggestion-only workflow that still needs manual yes/no verdicts on every connection. See [[wiki/01-overview|Overview]].
