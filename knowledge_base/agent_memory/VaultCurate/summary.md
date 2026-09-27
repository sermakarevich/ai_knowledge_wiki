# Technical Analysis: notoriouslab/vault-curate

**Repository:** https://github.com/notoriouslab/vault-curate
**Version analyzed:** 1.11.0
**Date:** 2026-09-26
**Wiki:** [[index]]

> Coverage note: the wiki completed two component pages at analysis time — `01-overview.md` (user-facing behavior) and `02-top-level-files.md` (root files, build, dependencies). No `src/` internals pages exist yet, so sections 3 and 5 cite behavior-level evidence rather than implementation functions, and per-file internals below the root are not described.

## 1. Overview / What Problem It Solves

The problem space is three documented failures of plain Obsidian vaults: keyword-only search misses paraphrased content, related notes stay scattered because manual linking does not scale, and old notes become unrecoverable memory (01-overview.md:38, 01-overview.md:40, 01-overview.md:43). The repo addresses it as an Obsidian plugin — Vault Curate — providing semantic search and connection-finding over local notes, with explicit strength on Chinese/CJK text, relation graphs, semantic paths, and Hot/Cold rediscovery (01-overview.md:3, 01-overview.md:51). Four capability layers exist: Find (fused keyword/semantic/fuzzy search), Connect (relation graph, semantic path, expand-in-place), Rediscover (Hot/Cold tiering plus Discover and MOC export), and an optional, off-by-default AI curation layer (01-overview.md:6, 01-overview.md:49). The governing design constraint is local-first operation: the ~110 MB embedding model downloads once, no API key is required, and nothing leaves the machine unless the user explicitly configures a cloud service (01-overview.md:8, 01-overview.md:15). The primary user is an Obsidian vault owner with a large, long-lived, substantially Chinese-language note collection who wants suggestion-only assistance — the plugin never edits notes automatically and every connection requires a verdict (01-overview.md:16, 01-overview.md:17).

## 2. High-Level Architecture

```
Obsidian vault (.md notes + frontmatter)
        │
        ▼
Index builder (desktop; embeddings via ~110 MB local model,
  BM25 + vectors in sql.js store, up to 60,000 chars/note)
        │
        ├───► Find: Keyword ─┐
        │    Semantic ────────┼─► fused ranking (RRF k=60) ─► modal / sidebar results
        │    Fuzzy title ─────┘         │
        │                               ▼
        ├───► Connect: relation graph / semantic path / expand-in-place
        │              ─► timestamped .canvas files ─► verdict dialog ─► wikilinks
        │
        └───► Rediscover: Hot/Cold tiering ─► Discover (current-note / global)
                       ─► MOC export / similar-notes
        │
        ▼ (optional, off by default)
AI curation (Ollama / OpenAI-compatible / cloud; manual trigger only)
```

Data flow: (1) On desktop, notes are indexed into a local store combining BM25 keyword data with embeddings from the built-in `bge-small-zh-v1.5` q8 model; long notes are read in full up to 60,000 characters (01-overview.md:88, 02-top-level-files.md:52). (2) At query time the three search engines — Keyword, Semantic, Fuzzy title — run concurrently and merge into one fused ranking, with frontmatter tags fused into similarity scoring in Find Similar, relation graph, and Discover (01-overview.md:20, 01-overview.md:31). (3) Connection surfaces render as Obsidian Canvas files: each run writes a fresh timestamped `.canvas` into the configured folder (default `Vault Curate Canvases`), never overwriting prior graphs (01-overview.md:37). (4) Every suggestion resolves through an explicit verdict — accept writes real wikilinks into notes' Related sections, dismiss suppresses the pair persistently across renames and index rebuilds (01-overview.md:7, 01-overview.md:41). (5) Hot/Cold tiers are derived live at query time from internal links plus recency, so tiering reflects current vault state without a separate tiering pass (01-overview.md:43). (6) The desktop-built index is portable: carried over iCloud, Obsidian Sync, or Syncthing, it is read directly on mobile with no re-indexing or model download (01-overview.md:18).

Persistent state lives in: the desktop-built local index (carried to mobile via file sync, 01-overview.md:18); timestamped `.canvas` graph files in the vault (01-overview.md:37); wikilinks written into notes' Related sections on accept (01-overview.md:40); and the dismissed-pair list reviewable under Settings → Advanced → Hidden suggestions (01-overview.md:41).

## 3. The Suggested Connection

The central concept is the *suggested connection*: a ranked candidate link between two notes that remains inert until the user promotes or dismisses it (01-overview.md:7, 01-overview.md:17). Representation is behavioral rather than structural in the available pages: a suggestion carries a similarity score rendered as an edge label, a source/target note pair, and a lifecycle state of pending, promoted (real wikilink), or dismissed (01-overview.md:36, 01-overview.md:40, 01-overview.md:41).

Named kinds, all from the Canvas edge/node vocabulary (01-overview.md:36):

- **Purple edge** — semantically close but not yet wikilinked; the actionable suggestion (01-overview.md:36).
- **Gray edge (with direction arrow)** — already wikilinked; promoted state (01-overview.md:36).
- **Cyan node** — Cold note (orphan, long untouched); rediscovery marker (01-overview.md:36).
- **Green edge** — relevance to a search query; appears only on results canvases, never between two notes (01-overview.md:36).
- **Orange node** — note pointed at by two or more edges after expand-in-place; convergence marker (01-overview.md:39).
- **Hot / Cold tier** — Hot: linked, or created/edited recently (edits count, opens do not); Cold: orphan and untouched past the tunable window (01-overview.md:43).

Key queries operate on notes, not query strings, in the Rediscover layer: current-note Discover surfaces related Cold notes for the open file, and global Discover surfaces forgotten notes related to recent focus (recently edited/created notes, their topic tags, semantic centroid), grouped by top-level folder (01-overview.md:44, 01-overview.md:46). Verbatim query-surface rule:

> "Search finds a single note; this layer shows how notes relate, including the links you never drew by hand" (01-overview.md:35).

## 4. LLM / External Service Integration

Default operation calls no LLM and no external API: the built-in embedding model (~110 MB, one download, no key) plus local BM25/vectors handle Find, Connect, and Rediscover entirely on-device (01-overview.md:8, 01-overview.md:15). External calls exist only in the optional AI curation layer, which is off until enabled under Settings → AI Curation → Enable AI curation and is always manually triggered, never background (01-overview.md:49). Documented providers for that layer: Ollama or any OpenAI-compatible service for non-Chinese languages, plus user-configured cloud services — data leaves the machine only when pointed at one (01-overview.md:8, 01-overview.md:16). The single documented Curate action in the available pages is generating a description plus tags into one note's frontmatter; remaining actions are truncated in the source and not described (01-overview.md:50). No environment variables are documented in either wiki page; configuration is via plugin settings (synonym list, Hot window, graph folder, bidirectional promotion) rather than env vars (01-overview.md:32, 01-overview.md:37, 01-overview.md:40, 01-overview.md:43).

## 5. The Find–Connect–Rediscover Pipeline

The primary workflow is the Find → Connect → Rediscover loop ("Find, connect, and rediscover your notes", 01-overview.md:5). The wiki's two pages do not reach `src/` implementation functions, so steps below cite behavior-level evidence with wiki file:line per step; no implementation function signatures are asserted.

1. **Index (desktop, once).** Notes are embedded with the local model and keyword-indexed (BM25+) into the portable local store; Traditional-Chinese text is normalized Traditional→Simplified for matching while stored text, keyword search, and snippets stay Traditional (01-overview.md:30, 02-top-level-files.md:52).
2. **Find.** Three engines (Keyword for exact phrases, Semantic for paraphrase, Fuzzy title for typos) run concurrently and merge into one fused ranking; synonyms configured under Advanced → Synonym list expand queries silently (01-overview.md:20, 01-overview.md:32). Results show matched passages with highlights; modal Alt+Enter inserts a link at the cursor instead of navigating (01-overview.md:27).
3. **Connect.** Relation graph lays the center note with radial semantic neighbors and scored edges; semantic path chains stepping-stone notes between two endpoints judged by weakest hop, with an honest not-connected notice when no strong chain exists; expand-in-place grows an existing canvas into free space without duplicating edges (01-overview.md:36, 01-overview.md:38, 01-overview.md:39).
4. **Verdict.** Accept via the canvas checkbox dialog writes checked purple-edge pairs into notes' Related sections as wikilinks (both notes by default; source-only via Advanced → Bidirectional promotion), turning edges gray in place; dismiss via per-pair Don't suggest or hover ✕ removes the pair from all surfaces and refills the slot with the next candidate (01-overview.md:40, 01-overview.md:41, 01-overview.md:48).
5. **Rediscover.** Hot/Cold tiers derive live from links plus recency; Discover (current-note and global) surfaces related Cold notes; Generate MOC exports a topic-grouped Map of Content, falling back to flat layout when results are too few or similar (01-overview.md:43, 01-overview.md:45, 01-overview.md:47).
6. **Curate (optional).** With AI curation enabled, manually triggered actions such as frontmatter description-plus-tags generation run against the configured provider (01-overview.md:49, 01-overview.md:50).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `esbuild.config.mjs` | 266 | Three-step bundle: embedding worker, k-NN worker, then main plugin with both worker sources inlined (02-top-level-files.md:6, 02-top-level-files.md:16) |
| `styles.css` | 492 | Shared UI styling under `.vault-curate-*` / `.vc-result-dismiss` for modal, sidebar, tabs, promote list, onboarding, dismiss controls (02-top-level-files.md:6, 02-top-level-files.md:54) |
| `README.zh-TW.md` | 307 | Traditional-Chinese user docs: features, desktop/mobile matrix, commands, settings, privacy, tech stack, dev commands (02-top-level-files.md:6, 02-top-level-files.md:52) |
| `manifest.json` | — | Plugin identity: `vault-curate`, 1.11.0, minAppVersion 1.7.2, desktop+mobile (02-top-level-files.md:30) |
| `manifest-beta.json` | — | Beta-track copy of the same identity block (02-top-level-files.md:30) |
| `package-lock.json` | — | Pinned tree: root 1.11.0, lockfileVersion 3; body truncated in source past the header (02-top-level-files.md:42, 02-top-level-files.md:50) |
| `tsconfig.json` | 20 | Compiler settings: ES2018 target, strict, `src/**/*.ts` include (02-top-level-files.md:56) |
| `vitest.config.ts` | 19 | Test settings: happy-dom, `test/**/*.test.ts`, `obsidian` aliased to a stub (02-top-level-files.md:56) |
| `.gitignore` | 40 | Ignores build outputs, `node_modules/`, `data.json`, patch artefacts, agent configs, private drafts (02-top-level-files.md:57) |
| `src/main.ts` | n/a in wiki | Main plugin bundle entry (referenced as build entry; internals not covered) (02-top-level-files.md:20) |
| `src/workers/embeddingWorker.ts` | n/a in wiki | Embedding worker entry, bundled to `worker.js` with transformers/ORT aliases (02-top-level-files.md:18) |
| `src/workers/knnWorker.ts` | n/a in wiki | Pure-math k-NN worker entry, bundled to `knn-worker.js`; bundle must not contain `obsidian` (02-top-level-files.md:19) |

Structural note: Community-store installs receive only `main.js` plus manifests and styles, so workers are inlined at build time and WASM ships as sibling release assets fetched via `wasmPaths` (02-top-level-files.md:14).

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `hdbscan-ts` | `1.0.17` | Only runtime dependency; density clustering (topic grouping behind Discover/MOC) (02-top-level-files.md:47) |
| `@huggingface/transformers` | `^4.0.1` | Local embedding inference in the worker bundle (02-top-level-files.md:48, 02-top-level-files.md:18) |
| `sql.js` | `^1.14.1` | Local index store (SQLite/WASM); `sql-wasm.wasm` copied as release asset (02-top-level-files.md:48, 02-top-level-files.md:25, 02-top-level-files.md:52) |
| `onnxruntime` (web bundle `ort.wasm.bundle.min.mjs`) | via alias, version cut in source | Embedding runtime; main-bundle alias redirects `onnxruntime-node` to the WASM bundle; `ort-wasm-simd-threaded.wasm` copied as release asset (02-top-level-files.md:27, 02-top-level-files.md:25) |
| `esbuild` | `^0.28.0` | Two-stage production/dev bundling (02-top-level-files.md:48) |
| `typescript` | `^5.7.0` | Compilation per `tsconfig.json` (02-top-level-files.md:48) |
| `vitest` | `^4.1.6` | Test runner per `vitest.config.ts` (02-top-level-files.md:48) |
| `obsidian` | `^1.13.1` | Plugin API types; external at bundle time, stubbed in tests (02-top-level-files.md:48, 02-top-level-files.md:20, 02-top-level-files.md:56) |
| `@types/node` | `^22.0.0` | Node type surface for build scripts (02-top-level-files.md:48) |
| `@types/sql.js` | `^1.4.11` | Types for the sql.js store (02-top-level-files.md:48) |
| `happy-dom` | `^20.9.0` | DOM environment for tests (02-top-level-files.md:48, 02-top-level-files.md:56) |

Registry-level versions beyond the manifest header are truncated in the source chunk (88,878 further characters cut) and are not asserted here (02-top-level-files.md:50).

## 8. CLI / Usage Surface

No shell CLI exists; the usage surface is Obsidian commands, sidebar/modal UI, a scripting API, and settings. Dev commands `npm run dev`, `npm run build` (`production` arg), and `npm test` are documented (02-top-level-files.md:52, 02-top-level-files.md:28).

| Command (palette / context menu) | What it does |
|---|---|
| `Vault Curate: Semantic search (modal)` | Quick-jump fused search via Cmd/Ctrl+P (01-overview.md:26) |
| Sidebar **Search** tab | Persistent search results surface (01-overview.md:26) |
| `VC: Find similar notes` (right-click `.md`) | Similar-note ranking to sidebar; rows draggable to Canvas (01-overview.md:30) |
| `VC: Generate relation graph` (palette, right-click, Discover **Graph** button) | Writes fresh timestamped `.canvas` with radial neighbors (01-overview.md:37) |
| Semantic path builder | Chain-of-notes path between two notes over a background-built semantic map (cancellable, non-blocking) (01-overview.md:38) |
| `VC: Expand in this graph` (canvas node right-click) | In-place neighborhood expansion preserving layout and manual colors (01-overview.md:39) |
| `Generate MOC` | Topic-grouped Map of Content export from Discover results (01-overview.md:47) |
| `search(query, { scope? })` (Obsidian-CLI) | Scripted search for automation (02-top-level-files.md:52) |

| Setting | Effect |
|---|---|
| Advanced → Synonym list (e.g. `Amy = Amy Chen`) | Query-time alias expansion, including mobile keyword mode (01-overview.md:32) |
| Advanced → Hot window (days) | Recency cutoff for Hot/Cold tiering, applied instantly (01-overview.md:43) |
| Advanced → Relation graph folder (default `Vault Curate Canvases`) | Output folder for generated canvases (01-overview.md:37) |
| Advanced → Bidirectional promotion | Accept writes both notes by default; source-only when set (01-overview.md:40) |
| Settings → Advanced → Hidden suggestions | Review dismissed pairs with open-note link and copy-path (01-overview.md:41) |
| Settings → AI Curation → Enable AI curation | Unlocks the three manual AI actions (01-overview.md:49) |

No environment variables are documented; providers and toggles are configured through these settings (01-overview.md:32, 01-overview.md:49).

## 9. Extensibility Points

The wiki covers user-level extension only; no `src/` class or module extension points are documented in the two available pages. Per-surface extension mapping:

- **Query vocabulary** — Advanced → Synonym list; add alias groups without touching code (01-overview.md:32).
- **Tiering policy** — Advanced → Hot window (days); retunes Hot/Cold without rebuilds (01-overview.md:43).
- **Graph output location and promotion direction** — Advanced → Relation graph folder and Bidirectional promotion (01-overview.md:37, 01-overview.md:40).
- **Embedding provider for non-Chinese vaults** — switch the model path to Ollama or any OpenAI-compatible service per the documented guidance (01-overview.md:16).
- **Build pipeline** — `esbuild.config.mjs` plugin hooks (`inlineSourcePlugin`, `nativeStubPlugin`, `stripNodeBuiltinsPlugin`, main-bundle alias) are the code-level seam for bundling changes, e.g. stubbing additional native modules or redirecting runtimes (02-top-level-files.md:27).
- **Programmatic access** — the Obsidian-CLI `search(query, { scope? })` API is the scripting seam (02-top-level-files.md:52).
- **Dismissal lifecycle** — Hidden suggestions store is the review/audit seam for suggestion quality work (01-overview.md:41).

## 10. Limitations and Gotchas

- **Only two wiki pages exist, so `src/` behavior is unverified.** Ranking fusion details (RRF k=60), clustering use, and the semantic-map implementation are named but not traced to functions; treat any claim below the root-file level as unconfirmed (01-overview.md:51, 02-top-level-files.md:50).
- **AI curation documentation is truncated.** Only frontmatter description-plus-tags generation is described; the remaining Curate actions are cut mid-line in the source, so the full optional surface cannot be enumerated from the wiki (01-overview.md:50).
- **Mobile is read-only by architecture.** Search works on the phone against the synced desktop index, but index construction and the ~110 MB model download are desktop tasks — a mobile-only user gets no index (01-overview.md:18).
- **Suggestion state can surprise.** Dismissed pairs stay suppressed even across renames and index rebuilds, and every graph run mints a new timestamped canvas instead of updating in place — expect canvas accumulation and check Hidden suggestions before assuming a missing suggestion is a ranking failure (01-overview.md:37, 01-overview.md:41).
- **Tiering semantics are narrow.** Hot/Cold derives only from internal links plus recency, and merely opening a note does not count as use — recently read but unedited orphans still surface as Cold (01-overview.md:43).
- **Language asymmetry is explicit.** The built-in model is tuned for Chinese personal names, proper nouns, and colloquial phrasing; other languages are directed to Ollama or OpenAI-compatible services, and Traditional-Chinese matching normalizes to Simplified under the hood (01-overview.md:16, 01-overview.md:30).

## 11. How It Compares to Alternatives

- **Obsidian core search** — built-in keyword and backlink panes with no semantic ranking; Vault Curate layers fused semantic/fuzzy search and unlinked-connection discovery on top while leaving core search untouched.
- **Omnisearch** — local-first vault search with BM25-style relevance and PDF/image indexing; Vault Curate overlaps on local-first fused search but adds the verdict-driven connection workflow (Canvas graphs, promotion to wikilinks) and Hot/Cold rediscovery rather than search alone.
- **Smart Connections / Smart Second Brain** — embedding-based similar-note surfacing with chat-oriented AI features; Vault Curate shares the semantic-similarity core but inverts the default: no background AI, no auto-edits, suggestions-only with persistent dismiss, and AI curation strictly opt-in.
- **Obsidian Copilot / various AI assistants** — cloud-LLM chat over vault content requiring API keys; Vault Curate's default path needs no key and sends nothing out, reserving external providers for explicitly enabled curation actions.

Positioning: Vault Curate occupies the local-first, suggestion-only niche — a privacy-preserving discovery layer (search, unlinked-link proposals, forgotten-note surfacing) for large CJK-heavy vaults, rather than an AI organizer or chat interface.

## Appendix: Selected Code Snippets

1. Production/dev mode switch, `esbuild.config.mjs` (02-top-level-files.md:23):

```
const prod = process.argv[2] === 'production';
```

2. Bundle banner stamped into built output, `esbuild.config.mjs` (02-top-level-files.md:24):

```
THIS IS A GENERATED/BUNDLED FILE BY ESBUILD / Source: https://github.com/notoriouslab/vault-curate
```

3. WASM release-asset copies, `esbuild.config.mjs` (02-top-level-files.md:25):

```
copyFileSync(ortWasmSrc, path.join(PLUGIN_ROOT, 'ort-wasm-simd-threaded.wasm'));
copyFileSync(sqlJsWasmSrc, path.join(PLUGIN_ROOT, 'sql-wasm.wasm'));
```

4. Verbatim plugin description, `manifest.json` / `manifest-beta.json` (02-top-level-files.md:41):

```
Find, connect, rediscover your notes. Local semantic search (BM25 + embeddings), relation graph + semantic paths for unlinked related notes, Hot/Cold surfacing of forgotten ones, strong Chinese/CJK. Mobile reads your desktop-built index. No API keys.
```
