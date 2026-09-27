> [[index|Wiki]] | [[summary|Summary]]
# notoriouslab/vault-curate — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Vault Curate is an Obsidian plugin for semantic search and connection-finding across local notes, strong on Chinese/CJK, with relation graphs, semantic paths, and Hot/Cold rediscovery, where nothing leaves the machine by default (01-overview.md:22, 01-overview.md:24, 01-overview.md:51).
## Key points
- Vault Curate's whole job is "Find, connect, and rediscover your notes" via semantic search and connection-finding for Obsidian notes (01-overview.md:22, 01-overview.md:24).
- Three capabilities work out of the box with zero setup — Find, Connect, Rediscover — while the fourth, AI curation, is off until turned on (01-overview.md:62).
- Every suggested connection waits for user verdict: one click turns it into a real wikilink, or ✕ dismisses the pair permanently even across renames or index rebuilds (01-overview.md:69).
- The built-in model is about 110 MB, downloads once, needs no API key, and AI curation only sends data out if the user points it at a cloud service (01-overview.md:51).
- Search fuses three engines — Keyword, Semantic, Fuzzy title — into one ranking, and the built-in model reads long notes in full up to 60,000 characters (01-overview.md:77, 01-overview.md:88).
- Relation graphs render as editable Obsidian Canvas files with purple (unlinked), gray (wikilinked), cyan (Cold), and green (query-relevance) edges/nodes, each run writing a fresh timestamped `.canvas` (01-overview.md:102, 01-overview.md:104, 01-overview.md:109).
- Notes are auto-tiered Hot/Cold by internal links plus recency, where editing counts as use but merely opening does not, with the cutoff tunable under Advanced → Hot window (days) (01-overview.md:126).
## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** Top-level files define the plugin's build, identity, dependencies, docs, and shared styles — a two-stage esbuild bundle (workers + main), manifests, lockfile, README, styles.css, and compiler/test configs (02-top-level-files.md:5).
## Key points
- The component covers 9 source files at the repo root, led by `esbuild.config.mjs` (266 lines), `styles.css` (492 lines), and `README.zh-TW.md` (307 lines) (02-top-level-files.md:5, 02-top-level-files.md:50, 02-top-level-files.md:764, 02-top-level-files.md:1075).
- `esbuild.config.mjs` runs a three-step bundle: embedding worker from `src/workers/embeddingWorker.ts`, k-NN worker from `src/workers/knnWorker.ts`, then the main plugin from `src/main.ts` with both worker sources inlined (02-top-level-files.md:216, 02-top-level-files.md:258, 02-top-level-files.md:280).
- Plugin identity is pinned in both `manifest.json` and `manifest-beta.json` as `id: vault-curate`, `version: 1.11.0`, `minAppVersion: 1.7.2`, `isDesktopOnly: false` (02-top-level-files.md:320, 02-top-level-files.md:335).
- The dependency lockfile pins `vault-curate 1.11.0` with one runtime dependency (`hdbscan-ts 1.0.17`) and dev dependencies on transformers, esbuild, sql.js, typescript, and vitest, but its body is truncated in the chunk (02-top-level-files.md:354, 02-top-level-files.md:363, 02-top-level-files.md:761).
- `README.zh-TW.md` documents the user-facing surface — semantic search, relation graph, Hot/Cold Discover, optional AI curation, desktop/mobile matrix, commands, settings, and privacy (02-top-level-files.md:812, 02-top-level-files.md:896, 02-top-level-files.md:947, 02-top-level-files.md:1008).
- Shared UI styling lives in `styles.css` under the `.vault-curate-*` / `.vc-result-dismiss` class family covering modal, sidebar, tabs, promote list, onboarding, and dismiss controls (02-top-level-files.md:1081, 02-top-level-files.md:1225, 02-top-level-files.md:1510).
- Compiler and test behavior are fixed by `tsconfig.json` (`target ES2018`, `strict`, `include src/**/*.ts`) and `vitest.config.ts` (`happy-dom`, `test/**/*.test.ts`, `obsidian` aliased to a stub) (02-top-level-files.md:1571, 02-top-level-files.md:1595).
## The system in five moves
1. Vault Curate starts from the user's local Obsidian vault, promising Find/Connect/Rediscover with nothing leaving the machine and a Chinese-strong local model.
2. Find fuses keyword, semantic, and fuzzy-title search over full long-note content so meaning, not just literal characters, retrieves notes.
3. Connect surfaces unlinked-but-related notes as suggestion-only relation graphs, semantic paths, and in-place canvas expansion awaiting a yes/no verdict.
4. Rediscover auto-tiers notes Hot/Cold by links plus recency and resurfaces forgotten Cold notes via current-note and global Discover plus MOC export.
5. The whole surface ships as one plugin identity (vault-curate 1.11.0, desktop+mobile) built by a two-stage esbuild bundle inlining both workers, styled by a shared stylesheet, and documented bilingually.
