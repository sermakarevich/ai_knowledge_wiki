# Technical Analysis: kdsz001/OpenWiki

**Repository:** https://github.com/kdsz001/OpenWiki
**Version analyzed:** 0.3.25
**Date:** 2026-09-26
**Wiki:** [[index]]

> Coverage note: the wiki snapshot under analysis contains two component pages (overview of `README.md`/`README.zh-CN.md`, and top-level config/entry files). Statements below are grounded in those pages and their citations. Backend internals (Rust commands, SQLite schema, capture pipeline code) are not covered by the available pages and are therefore described only as far as the README discloses behavior, not implementation.

## 1. Overview

Problem space: clipboard content is high-volume and ephemeral — users copy text, images, and links across apps all day and lose most of it, while general note apps require manual filing and expose data to cloud sync. The primary user is a desktop info worker (the design doc scopes it to Mac desktop capture plus AI knowledge tooling for Chinese info workers) who wants to retain selected fragments and retrieve them as structured knowledge.

How the repo addresses it: OpenWiki is a Tauri 2 desktop app (React 19 frontend, Rust + SQLite backend) built around an explicit opt-in capture loop: "Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base" (`README.md:19`). The copy event raises a 10-second auto-dismissing popup; nothing persists unless the user keeps the item (`README.md:36`, `README.md:37`). Kept items land in a local SQLite store (`README.md:24`) and are compiled by LLM providers into wiki pages, a knowledge graph, an Ask sidebar, and weekly insight reports (`README.md:52`, `README.md:53`, `README.md:54`, `README.md:60`).

## 2. High-Level Architecture

```
Clipboard / URL copy ─► Capture popup (Tauri, 10s auto-dismiss) ─► Keep / Discard decision
        │                                                                  │
        │ (manual: ⌘⇧C / Ctrl+Shift+C)                                      ▼
        │                                                        Local SQLite store
        │                                                                  │
        ▼                                                                  ▼
Source-app detection + URL full-text fetch ───────────────► React 19 UI (content list, wiki, graph, Ask, reports)
(WeChat / X-Twitter / generic URLs)                                    │
                                                                       ▼
                                                            LLM providers (Anthropic / OpenAI / Gemini)
                                                            via API key or OAuth (Settings → AI)
```

Data-flow narrative:

1. A system copy event (or manual `⌘⇧C` / `Ctrl+Shift+C`, `README.md:40`) raises the capture popup with detected type (text / image / link) and source app (`README.md:38`).
2. For URLs the app fetches full article content, including platform-specific handling for WeChat and X/Twitter (`README.md:39`).
3. The user keeps or ignores the item; the popup auto-dismisses after 10 seconds and only kept content is saved (`README.md:36`, `README.md:37`).
4. Kept content persists in a local SQLite database (`README.md:24`) and is searchable, filterable (type / time range), and exportable to Markdown (`README.md:45`, `README.md:46`, `README.md:47`).
5. On demand, LLM calls compile captures into wiki pages, graph edges, Ask-sidebar answers, structure checks, and weekly reports (`README.md:52`, `README.md:53`, `README.md:54`, `README.md:55`, `README.md:60`, `README.md:61`).
6. Two documented network exceptions bypass the local-only baseline: full URLs may go to Jina Reader and foreign-language text in the Chinese UI may go to Google Translate, both on by default and independently disableable (`README.md:27`).

Persistent state lives in the local SQLite database (`README.md:24`); OAuth/API credentials live in `.env` (templated by `.env.example:4-9`) and are excluded from version control (`.gitignore:54-57`).

## 3. The Kept Capture

The central concept is the kept capture: a copied fragment (text, image, or link) the user explicitly elects to retain. Representation per the available pages is behavioral, not schema-level: the README distinguishes captures by type and time range for filtering (`README.md:45`), by full-text searchability across content and knowledge base (`README.md:46`), and by Markdown exportability (`README.md:47`). No table or struct definition is visible in the two wiki pages, so field-level representation is not stated here.

Named kinds/types, as disclosed:

- `text` / `image` / `link` capture types for filtering (`README.md:45`)
- Wiki pages of concepts, entities, and topics compiled from captures (`README.md:52`)
- Knowledge-graph nodes/edges visualizing how ideas connect (`README.md:53`)
- Report feedback signals: liked vs dismissed items that train preferences (`README.md:63`)
- Attention-analysis dimensions (7 fixed): At a Glance / Subconscious / Graveyard / Blind Spots / Hot Topics / Heatmap / Action Items (`README.md:61`)

Key queries (verbatim positioning):

> Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base<br>
> **You decide what to keep. AI makes sense of it.** (`README.md:19`, `README.md:20`)

> **Network transparency:** URL reading can send the full URL to Jina Reader, and the Chinese UI can send foreign-language page text to Google Translate. Both are enabled by default for compatibility and can be disabled independently in Settings. Platform-specific readers may still contact the source platform or its API. (`README.md:27`)

## 4. LLM / External Service Integration

Providers: Anthropic (Claude), OpenAI, Google Gemini; connection via API Key or OAuth login with per-provider model selection under Settings → AI (`README.md:68`, `README.md:69`, `README.md:70`, `README.md:102`).

Required vs optional calls: no call is required for capture and local storage to function; LLM calls are required only for AI features (wiki compilation, graph, Ask sidebar, structure checks, weekly reports) and therefore fail closed to a working local capture store when unconfigured. The two non-LLM external calls (Jina Reader for URL reading, Google Translate for foreign-language text in the Chinese UI) are enabled by default and independently disableable in Settings (`README.md:27`).

Environment variables (`.env.example:1-9`):

| Variable | Required for | Status |
|---|---|---|
| `GEMINI_CLIENT_ID` | Gemini OAuth AI features | placeholder, user-supplied |
| `GEMINI_CLIENT_SECRET` | Gemini OAuth AI features | placeholder, user-supplied |
| `OPENAI_OAUTH_CLIENT_ID` | OpenAI/Codex OAuth features | placeholder, user-supplied |

Secrets convention: copy `.env.example` to `.env` (`.env.example:2`); `.env` and `.env.*` are git-ignored with `!.env.example` re-allowed (`.gitignore:54-57`). No Anthropic OAuth variables are templated in the excerpt — Anthropic connects via API key per the README flow.

## 5. The Copy → Keep → Organize Pipeline

Primary workflow, step by step (behavioral level; per-function code mapping is not available in the two wiki pages, so each step cites the disclosing README line rather than a function symbol):

1. Copy event captured (any app) — popup raised on desktop (`README.md:19`, `README.md:36`). Manual fallback: `⌘⇧C` macOS / `Ctrl+Shift+C` Windows (`README.md:40`).
2. Content typed and attributed — text / image / URL with automatic source-app detection (`README.md:38`).
3. URL enrichment — full article content fetched; WeChat, X/Twitter, and generic URLs handled (`README.md:39`). Exception path: full URL may be sent to Jina Reader (`README.md:27`).
4. Keep / discard decision — user keeps the item or lets the 10-second timer dismiss it; only kept content is saved (`README.md:36`, `README.md:37`).
5. Local persistence and retrieval — stored in SQLite (`README.md:24`); filtered by type/time, globally searched, exported to Markdown (`README.md:45`, `README.md:46`, `README.md:47`).
6. AI organization — captures compiled into wiki pages (`README.md:52`), graph view (`README.md:53`), Ask-sidebar Q&A grounded in user content (`README.md:54`), orphan/broken-link/structure checks (`README.md:55`).
7. Insight reporting — one-click weekly report over captures with the 7-dimension attention analysis (`README.md:60`, `README.md:61`); like/dismiss feedback trains preferences (`README.md:63`).

No `file.py:line`-style function citations are given because the available wiki pages do not cover the Rust/TypeScript implementation files; inventing them would be fabrication.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~160 (cited to :160) | Primary spec of behavior: capture loop, privacy, AI features, install, build |
| `README.zh-CN.md` | 164 (`README.zh-CN.md:737-902`) | Chinese landing/dev mirror of the same behavior and commands |
| `index.html` | 19 (`index.html:1-19`) | Vite shell: mounts `#root`, loads `/src/main.tsx`, sets title, font preconnects |
| `vite.config.ts` | 20 (`vite.config.ts:980-1000`) | React + Tailwind plugins, dev port 5173, ignores `src-tauri/**` to avoid HMR loop |
| `package-lock.json` | 6021 (head cited `:401-450`) | Pins `openwiki@0.3.25`, lockfileVersion 3, MIT; runtime + toolchain dependency set |
| `tsconfig.app.json` | 29 (`tsconfig.app.json:904-935`) | Frontend TS config: ES2022, strict, `react-jsx`, `include: ["src"]` |
| `tsconfig.json` | 8 (`tsconfig.json:937-947`) | Project-reference root over app + node configs |
| `tsconfig.node.json` | 27 (`tsconfig.node.json:949-978`) | Tooling TS config: ES2023, node types, covers `vite.config.ts` |
| `eslint.config.js` | 24 (`eslint.config.js:1-24`) | Flat lint config for `**/*.{ts,tsx}`: recommended JS/TS + react-hooks + react-refresh |
| `.env.example` | 9 (`.env.example:1-9`) | OAuth placeholder template for Gemini + OpenAI credentials |
| `.gitignore` | 61+ (`.gitignore:1-82`) | Ignores logs, `node_modules`, `dist`, editor dirs, `.env`, cargo artifacts, bundled binaries |
| `AGENTS.md` | ~159 (`AGENTS.md:1-159`) | Agent playbook: permissions, decision protocol, push/release flow, skill routing |
| `CLAUDE.md` | ~235 (`CLAUDE.md:1-235`) | Near-identical agent playbook (Claude-owned release flow variant) |
| `DESIGN.md` | 106+ (`DESIGN.md:1-344`) | Normative design system: Brutally Minimal + `#F97316` accent, type/color/spacing/icons/motion |
| `docs/banner.svg` | — (`README.md` cover ref) | Project banner asset referenced by both READMEs |

Line counts for chunk-embedded files use the chunk's cited numbering where the page reports it.

## 7. Dependencies

Required first; constraint strings as pinned in the lockfile head (`package-lock.json:411-450`):

| Package | Version constraint | Purpose |
|---|---|---|
| `@tauri-apps/api` | `^2` | Frontend-to-Rust bridge (commands, events, tray/clipboard plugins) |
| `@tauri-apps/plugin-autostart` | (v2 line) | Launch-on-login / tray residency support |
| `@tauri-apps/plugin-clipboard-manager` | (v2 line) | Clipboard read/listen for the copy-to-capture flow |
| `@tauri-apps/plugin-process` | (v2 line) | Process control helpers in the Tauri shell |
| `@tauri-apps/plugin-shell` | (v2 line) | Scoped shell execution from the desktop app |
| `@tauri-apps/plugin-updater` | (v2 line) | In-app auto-update channel |
| `react` / `react-dom` | `^19.2.0` | UI framework |
| `zustand` | `^5` | Client state management |
| `framer-motion` | `^11` | Minimal-functional motion |
| `d3-force` | `^3.0.0` (+ `@types/d3-force`) | Knowledge-graph layout |
| `lucide-react` | `^1.6.0` | Icon set (2px stroke, emoji→Lucide rule per `DESIGN.md:321-335`) |
| `i18next` / `react-i18next` / `i18next-browser-languagedetector` | (v-series line) | EN/ZH localization |
| `react-markdown` / `remark-gfm` | (line) | Wiki/report Markdown rendering |
| `tailwindcss` | `^4` (+ typography/vite plugins) | Styling system |
| `vite` | `^6.4.1` | Dev server + build |
| `@vitejs/plugin-react` | `^5.1.1` | React fast refresh for Vite |
| `typescript` | `~5.9.3` | Typechecking |
| `typescript-eslint` / `@eslint/js` / `eslint` / react-hooks + react-refresh plugins / `globals` | (devDeps line) | Lint stack |
| `autoprefixer` / `postcss` | (devDeps line) | CSS pipeline |
| `@tauri-apps/cli` | (devDep line) | `tauri dev` / `tauri build` |
| `rusqlite` (Rust, via `AGENTS.md:128-135` project info) | — | SQLite backend (constraint not visible in the two wiki pages) |

Build prerequisites (not packages): Node.js 18+, latest stable Rust, macOS 13+ or Windows 10/11, Xcode CLT on macOS, MSVC build tools + WebView2 on Windows (`README.md:116`, `README.md:117`, `README.md:118`, `README.md:119`, `README.md:120`).

## 8. CLI / Usage Surface

Entry points:

| Entry | Command / artifact | Notes |
|---|---|---|
| Dev run | `npm run tauri dev` (`README.md:141`) | After `git clone …OpenWiki.git` (`README.md:130`) + `npm install` (`README.md:136`) |
| Prod build | `npm run tauri build` (`README.md:146`) | Preceded by document-converter setup below |
| Doc converter (macOS/Linux) | `./src-tauri/scripts/setup_markitdown.sh` (`README.md:155`) | Required before release bundles (`README.md:149`) |
| Doc converter (Windows) | `./src-tauri/scripts/setup_markitdown.ps1` (`README.md:160`) | PowerShell variant |
| Desktop artifacts | `OpenWiki_X.Y.Z_aarch64.dmg` (`README.md:84`), `OpenWiki_X.Y.Z_x64.dmg` (`README.md:85`), `OpenWiki_X.Y.Z_x64-setup.exe` or `…_x64_en-US.msi` (`README.md:86`) | macOS signed+notarized; Windows unsigned (SmartScreen **More info → Run anyway**, `README.md:106`) |
| Installed app shortcuts | `⌘⇧C` / `Ctrl+Shift+C` manual capture (`README.md:40`); `⌘⇧Y` / `Ctrl+Shift+Y` show main window (`README.md:76`) | Tray residency, Dark/Light/System themes, MCP link to Claude Desktop (`README.md:75`, `README.md:77`, `README.md:78`) |
| Agent release flow | natural-language triggers "发版"/"发 release"/"打 tag"/"发个新版本" → agent writes `release-notes/vX.Y.Z.md` from `TEMPLATE.md`, bumps three version files, `cargo check`, tags/pushes (`AGENTS.md:112-126`) | User never edits `release-notes/` manually |

Env-var and config tables:

| Variable | Source | Purpose |
|---|---|---|
| `GEMINI_CLIENT_ID` / `GEMINI_CLIENT_SECRET` | `.env.example:4-9` | Gemini OAuth |
| `OPENAI_OAUTH_CLIENT_ID` | `.env.example:4-9` | OpenAI/Codex OAuth |
| AI provider + model selection | Settings → AI (`README.md:102`) | Per-provider model choice for key or OAuth connections |
| Jina Reader / Google Translate toggles | Settings (`README.md:27`) | Independently disableable network exceptions |
| Dev server port | `vite.config.ts:988-992` | `port: 5173, strictPort: true` |
| Design tokens | `DESIGN.md:248-344` | Accent `#F97316`, warm neutrals, type scales, 8px spacing, Lucide-only icons |

## 9. Extensibility Points

- New capture sources / URL readers: extend wherever the WeChat/X-Twitter/generic fetch dispatch lives (behavior specified at `README.md:39`; implementation file not covered by the available pages — locate the Rust command handling URL enrichment before adding a platform).
- New AI providers or models: extend the Settings → AI provider registry (surfaced at `README.md:68-70`, `README.md:102`); add OAuth placeholders alongside `.env.example:4-9` and wire the provider's key/OAuth path.
- New report dimensions or feedback signals: extend the weekly-report generator and the like/dismiss preference loop (`README.md:60`, `README.md:61`, `README.md:63`); the 7-dimension list is currently fixed.
- New wiki/graph structure checks: extend the orphan/broken-link/structure detection behind `README.md:55`.
- New themes or visual language: read `DESIGN.md:1-106` first — deviation requires approval (`AGENTS.md:136-140`); tokens are accent `#F97316` (`DESIGN.md:274-302`), Cabinet Grotesk / Plus Jakarta Sans / JetBrains Mono (`DESIGN.md:255-272`), Lucide icons (`DESIGN.md:321-335`).
- New agent skills or release steps: extend the skill routing table (`AGENTS.md:142-159`) and the `release-notes/` flow (`AGENTS.md:112-126`); keep `AGENTS.md` and `CLAUDE.md` in sync (they differ only in release-flow owner, `AGENTS.md:116-122` vs `CLAUDE.md:192-198`).

## 10. Limitations and Gotchas

- **Network exceptions are on by default despite "privacy first" framing.** URL reading can exfiltrate the full URL to Jina Reader and the Chinese UI can send foreign text to Google Translate; both must be disabled independently in Settings, and platform-specific readers may still contact source platforms (`README.md:27`).
- **Windows build is unsigned.** SmartScreen blocks first launch until **More info → Run anyway**; macOS is signed and notarized, so the two platforms have asymmetric install friction (`README.md:98`, `README.md:100`, `README.md:106`, `README.md:108`).
- **Release-bundle builds need an extra converter step.** `npm run tauri build` alone is insufficient for bundled output — `setup_markitdown.sh` / `.ps1` must run first (`README.md:149`, `README.md:155`, `README.md:160`).
- **Vite dev loop breaks without the `src-tauri` watch exclusion.** `cargo build` generates tens of thousands of rustdoc HTML files under `src-tauri/target/doc`; removing the `watch.ignored: ["**/src-tauri/**"]` line (`vite.config.ts:993-1000`) causes infinite HMR reload and strands the window on its transparent background.
- **Wiki coverage itself is truncated.** `package-lock.json` is cut after ~732 lines (`package-lock.json:732-733`), so the full transitive dependency set is unknown from these pages; and no Rust/SQLite implementation files are covered, so schema, command, and error-handling claims cannot be verified here.

## 11. How It Compares to Alternatives

- **Paste / CleanClip / Maccy** — clipboard-history managers named in `DESIGN.md:242-246` as direct competitors. They optimize recall of recent copies; OpenWiki adds the keep-decision plus AI wiki/graph/report organization layer on top of capture.
- **Notion / Obsidian Web Clipper-style collectors** — browser-first clippers that file into cloud or local vaults. OpenWiki is desktop-clipboard-first (any source app, `README.md:38`), local-SQLite by default (`README.md:24`), and compiles rather than merely files.
- **Readwise / Reader-style read-it-later pipelines** — URL/article-centric ingestion with resurfacing. OpenWiki overlaps on URL full-text fetch (`README.md:39`) and weekly attention reports (`README.md:60-61`) but starts from the OS clipboard instead of a browser/queue and keeps an explicit 10-second keep-or-drop gate (`README.md:36-37`).
- **Claude Desktop + MCP note setups** — general AI chat over user files (OpenWiki itself integrates with Claude Desktop via MCP, `README.md:78`). Standalone MCP notes lack OpenWiki's capture popup, source attribution, and fixed 7-dimension attention analysis (`README.md:61`).

Positioning: OpenWiki occupies the narrow intersection of clipboard manager, local-first store, and AI knowledge compiler — its differentiator is the explicit keep-gate on every copy feeding a provider-agnostic (Claude/OpenAI/Gemini) organization layer, at the cost of desktop-only distribution and default-on third-party readers that weaken the local-first claim.

## Appendix: Selected Code Snippets

1. Dev/build command sequence (`README.md:130-146`):

```bash
git clone https://github.com/kdsz001/OpenWiki.git
cd OpenWiki
npm install
npm run tauri dev
npm run tauri build
```

2. Document-converter setup before release bundles (`README.md:149-160`):

```bash
# macOS / Linux
./src-tauri/scripts/setup_markitdown.sh
# Windows PowerShell
./src-tauri/scripts/setup_markitdown.ps1
```

3. OAuth placeholder template (`.env.example:1-9`):

```
# OpenWiki Environment Variables
# Copy this file to .env and fill in your own values.

# Google Gemini OAuth (required for Gemini AI features)
GEMINI_CLIENT_ID=your_google_client_id_here
GEMINI_CLIENT_SECRET=your_google_client_secret_here

# OpenAI OAuth (required for OpenAI/Codex features)
OPENAI_OAUTH_CLIENT_ID=your_openai_client_id_here
```

4. Vite watch exclusion that prevents the HMR loop (`vite.config.ts:993-1000`, per page description):

```ts
watch: {
  ignored: ["**/src-tauri/**"]
}
```

Reconstructed from the page's verbatim description (`vite.config.ts:993-1000`); the full 20-line config also sets `plugins: [react(), tailwindcss()]`, `clearScreen: false`, and `server: { port: 5173, strictPort: true }` (`vite.config.ts:980-992`).
