> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The top-level files define OpenWiki's project entry point, build/lint/typecheck configuration, agent and design rules, and ignored/secret-file conventions for a Tauri 2 + React 19 desktop app.
## Key points
- The stack is a Tauri 2 desktop app with React 19 + Tailwind 4 + Zustand + Framer Motion frontend, Rust + SQLite (rusqlite) backend, npm and Vite 6 (`AGENTS.md:128-135`, `CLAUDE.md:204-211`).
- `index.html:11-18` is the Vite entry: mounts `<div id="root">`, loads `/src/main.tsx`, sets `<title>OpenWiki</title>`, and preloads Plus Jakarta Sans / JetBrains Mono / Cabinet Grotesk fonts.
- Secrets are templated by `.env.example:4-9`, which declares `GEMINI_CLIENT_ID`, `GEMINI_CLIENT_SECRET`, and `OPENAI_OAUTH_CLIENT_ID` as OAuth placeholders copied into `.env`.
- `.gitignore:54-57` ignores `.env` and `.env.*` while re-allowing `!.env.example`, and also ignores logs, `node_modules`, `dist`, editor dirs, and build artifacts (`src-tauri/resources/yt-dlp_macos`, `src-tauri/resources/markitdown/*`).
- `AGENTS.md:1-72` and `CLAUDE.md:1-72` are near-identical agent playbooks (permissions, decision protocol, GitHub push on "存一下"/"保存进度", Codex/Claude-owned release flow via `release-notes/README.md`, skill routing table).
- `DESIGN.md:1-106` is the normative design system (Brutally Minimal + warm accent `#F97316`, font/type scales, warm neutrals, dark mode, Lucide icons, minimal-functional motion, 2026-03-25 decisions log).
- `package-lock.json:1-9` pins `openwiki@0.3.25` (lockfileVersion 3, MIT) with Tauri plugins, React 19, i18next, d3-force, framer-motion, and Vite 6 / TS ~5.9.3 toolchain; the chunked copy is truncated after ~732 lines (`package-lock.json:732-733`).
---
## .env.example
Template for secrets; copy to `.env` (`.env.example:2`).

| Variable (` .env.example:4-9`) | Purpose |
|---|---|
| `GEMINI_CLIENT_ID` | Google Gemini OAuth client ID (required for Gemini AI features) |
| `GEMINI_CLIENT_SECRET` | Google Gemini OAuth secret |
| `OPENAI_OAUTH_CLIENT_ID` | OpenAI OAuth client ID (required for OpenAI/Codex features) |

Verbatim (`.env.example:1-9`):
```
# OpenWiki Environment Variables
# Copy this file to .env and fill in your own values.

# Google Gemini OAuth (required for Gemini AI features)
GEMINI_CLIENT_ID=your_google_client_id_here
GEMINI_CLIENT_SECRET=your_google_client_secret_here

# OpenAI OAuth (required for OpenAI/Codex features)
OPENAI_OAUTH_CLIENT_ID=your_openai_client_id_here
```

## .gitignore
61-line ignore list (`.gitignore:1-61`): `logs`, `*.log`, npm/yarn/pnpm debug logs (`.gitignore:23-30`); `node_modules`, `dist`, `dist-ssr`, `*.local` (`.gitignore:32-35`); editor files `.vscode/*` (except `!.vscode/extensions.json`), `.idea`, `.DS_Store`, VS artifacts (`.gitignore:37-52`); secrets `.env`, `.env.*` except `!.env.example` (`.gitignore:54-57`); `.claude/settings.local.json` (`.gitignore:59-60`); `src-tauri/.cargo/` (`.gitignore:62-64`); bundled `src-tauri/resources/yt-dlp_macos` 36 MB binary downloaded by `build.rs` (`.gitignore:66-68`); generated `src-tauri/resources/markitdown/bin/`, `venv/`, `VERSION.txt` (`.gitignore:70-74`); internal `docs/superpowers/` (`.gitignore:76-77`); local `outputs/`, `_design/`, `*-report-*.html` (`.gitignore:79-82`).

## AGENTS.md and CLAUDE.md
Two 72-line agent playbooks with identical structure (only the release-flow owner differs: Codex in `AGENTS.md:116-122` vs Claude in `CLAUDE.md:192-198`).

- Permissions (`AGENTS.md:90-97`, `CLAUDE.md:167-173`): free shell/dev commands (`npm run dev`, `npm run build`, `cargo build`, `cargo check`, `cargo tauri dev`), install packages/crates, run tests, create/delete/modify project files.
- Decision protocol (`AGENTS.md:99-104`, `CLAUDE.md:175-180`): routine tasks autonomous; architecture/dependency/data-model/scope decisions need 2–3 options with a marked recommendation; 3-minute no-reply means proceed with recommendation; explain in plain Chinese for a beginner user.
- GitHub (`AGENTS.md:106-110`, `CLAUDE.md:182-186`): repo `https://github.com/kdsz001/OpenWiki`; on "存一下"/"保存进度" commit + push; conventional messages (`feat/fix/refactor`).
- Release workflow (`AGENTS.md:112-126`, `CLAUDE.md:188-202`): user never maintains `release-notes/` manually; on "发版"/"发 release"/"打 tag"/"发个新版本" the agent reads `release-notes/README.md`, picks version, writes `release-notes/vX.Y.Z.md` from `TEMPLATE.md`, bumps three version files, runs `cargo check`, commits/tags/pushes, and reports the Actions URL; never paste raw commits — rewrite as short user-facing "优化了 X"/"修复了 X" sentences.
- Project info (`AGENTS.md:128-135`, `CLAUDE.md:204-211`): Tauri 2 (Rust + React/TypeScript), React 19 / Tailwind 4 / Zustand / Framer Motion, Rust + SQLite via rusqlite, npm, Vite 6.
- Design system (`AGENTS.md:136-140`, `CLAUDE.md:212-216`): always read `DESIGN.md` before visual/UI decisions; no deviation without approval; in QA mode flag mismatches.
- Skill routing (`AGENTS.md:142-159`, `CLAUDE.md:218-235`): Skill tool first when matched — `office-hours` (ideas), `investigate` (bugs), `ship` (deploy/PR), `qa`, `review` (diffs), `document-release`, `retro`, `design-consultation`, `design-review`, `plan-eng-review`.

## DESIGN.md
106-line design system (`DESIGN.md:1-106`): Mac desktop capture + AI knowledge tool for Chinese info workers; competes with Paste/CleanClip/Maccy (`DESIGN.md:242-246`).

- Aesthetic (`DESIGN.md:248-253`): Brutally Minimal + warm accents; layout does the work, only subtle flat background layering; bans purple gradients, floating orbs, emoji icons, decorative blobs, uniform bubbly radius.
- Typography (`DESIGN.md:255-272`): Display Cabinet Grotesk 700/800; Body/UI Plus Jakarta Sans; Data/Code JetBrains Mono; Google Fonts + Fontshare URLs verbatim in chunk (`DESIGN.md:261-263`); scale 3xl 56px → 2xs 9px.
- Color (`DESIGN.md:274-302`): accent `#F97316`, hover `#EA580C`, soft `#FFF7ED`; warm neutrals Background `#FAFAF8` / Surface `#FFFFFF` / raised `#F5F5F0` / Border `#E7E5E4` / text `#1C1917`, `#57534E`, `#A8A29E`, `#D6D3D1`; semantic Success `#16A34A`, Warning `#CA8A04`, Error `#DC2626`, Info `#2563EB`; dark mode Background `#0C0A09`, Surface `#1C1917`, accent `#FB923C`, soft `#431407`.
- Spacing/layout (`DESIGN.md:304-319`): 8px base, Comfortable density, card padding 16px / gap 12px / section gap 32px; max content width 640px; radius sm 6px / md 12px / lg 16px / full 9999px.
- Icons/motion (`DESIGN.md:321-335`): Lucide `lucide-react`, 2px stroke, 16/20/24px sizes, emoji→Lucide rule; minimal-functional motion micro 50–100ms / short 150–200ms / medium 200–300ms / long 400ms; no floating/breathing/gradient animation.
- Decisions log (`DESIGN.md:337-344`): 2026-03-25 rows — warm orange over blue/purple for differentiation; Cabinet Grotesk over Inter; Lucide over emoji; warm grays; Minimal over AI-slop gradients.

## eslint.config.js
24-line flat config (`eslint.config.js:1-24`): imports `@eslint/js`, `globals`, `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`, `typescript-eslint`, `defineConfig, globalIgnores` (`eslint.config.js:1-6`); `globalIgnores(['dist'])` (`eslint.config.js:8`); `files: ['**/*.{ts,tsx}']` extends `js.configs.recommended`, `tseslint.configs.recommended`, `reactHooks.configs.flat.recommended`, `reactRefresh.configs.vite`, with `ecmaVersion: 2020` and `globals: globals.browser` (`eslint.config.js:9-23`).

## index.html
19-line Vite shell (`index.html:1-19`): `<!doctype html>`, `<html lang="en">`, charset/viewport, `/vite.svg` favicon, Google/Fontshare preconnect + font CSS links (`index.html:6-11`), `<title>OpenWiki</title>` (`index.html:12`), transparent-background `<style>` (`index.html:13`), `<div id="root">` and `<script type="module" src="/src/main.tsx">` (`index.html:15-18`).

## package-lock.json (truncated in chunk)
6021-line lockfile, chunk shows only the head (`package-lock.json:398-733`): root `openwiki@0.3.25`, `lockfileVersion: 3`, MIT (`package-lock.json:401-410`); runtime deps `@tauri-apps/api ^2`, `plugin-autostart`, `plugin-clipboard-manager`, `plugin-process`, `plugin-shell`, `plugin-updater`, `@types/d3-force`, `d3-force ^3.0.0`, `framer-motion ^11`, `i18next`, `i18next-browser-languagedetector`, `lucide-react ^1.6.0`, `react`/`react-dom ^19.2.0`, `react-i18next`, `react-markdown`, `remark-gfm`, `zustand ^5` (`package-lock.json:411-430`); devDeps `@eslint/js`, Tailwind typography/vite, Tauri CLI, node/react types, `@vitejs/plugin-react ^5.1.1`, `autoprefixer`, `eslint`, react-hooks/refresh plugins, `globals`, `postcss`, `tailwindcss ^4`, `typescript ~5.9.3`, `typescript-eslint`, `vite ^6.4.1` (`package-lock.json:431-450`); then per-package entries from `@babel/code-frame@7.29.0` onward resolved via `registry.npmmirror.com` (`package-lock.json:452-732`). Chunk truncates here with "`... (truncated, 202884 more characters)`" (`package-lock.json:732-733`); remaining ~6000 lines were cut, so their contents are not covered.

## README.zh-CN.md
164-line Chinese landing/dev doc (`README.zh-CN.md:737-902`): banner `docs/banner.svg`, MIT/release/platform/PRs shields (`README.zh-CN.md:739-748`); tagline "复制任何内容 → 桌面弹出浮窗 → 选择收藏 → AI 自动整理成知识库" + local-SQLite privacy note + Jina Reader/Google Translate networking disclosure (`README.zh-CN.md:750-759`); screenshots table (content/wiki/graph/insights under `docs/screenshots/`) (`README.zh-CN.md:765-773`); features — 10s capture popup saving only chosen items (`⌘⇧C`/`Ctrl+Shift+C`), type/time filtering + global search + Markdown export, AI wiki/graph/Ask sidebar/structure checks, weekly + 7-dimension attention reports, Anthropic/OpenAI/Gemini via key or OAuth, tray app with `⌘⇧Y`/`Ctrl+Shift+Y` + themes + MCP (`README.zh-CN.md:775-810`); DMG/EXE install + macOS signed vs Windows SmartScreen first-run steps (`README.zh-CN.md:812-839`); dev prereqs Node 18+/Rust/macOS 13+ or Win 10-11 plus `npm install`, `npm run tauri dev/build`, and `setup_markitdown.sh/.ps1` (`README.zh-CN.md:841-875`); CONTRIBUTING link, Karpathy LLM-Wiki credit, `@NFTCPS` thanks, author Ray `@BitcoinRui`, MIT, Star History (`README.zh-CN.md:877-901`).

## tsconfig.* (app / root / node)
- `tsconfig.app.json:904-935` (29 lines): `target ES2022`, `lib [ES2022, DOM, DOM.Iterable]`, `types [vite/client]`, bundler `moduleResolution`, `allowImportingTsExtensions`, `verbatimModuleSyntax`, `moduleDetection force`, `noEmit`, `jsx react-jsx`, strict + `noUnusedLocals/Parameters`, `erasableSyntaxOnly`, `noFallthroughCasesInSwitch`, `noUncheckedSideEffectImports`; `include: ["src"]`.
- `tsconfig.json:937-947` (8 lines): project-reference root with `files: []` and references to `./tsconfig.app.json` and `./tsconfig.node.json`.
- `tsconfig.node.json:949-978` (27 lines): same strict/bundler flags with `target ES2023`, `lib [ES2023]`, `types [node]`; `include: ["vite.config.ts"]`.

## vite.config.ts
20-line config (`vite.config.ts:980-1002`): `defineConfig` with `plugins: [react(), tailwindcss()]`, `clearScreen: false`, dev `server: { port: 5173, strictPort: true }` (`vite.config.ts:988-992`); `watch.ignored: ["**/src-tauri/**"]` so Vite ignores the tens of thousands of rustdoc HTML files `cargo build` generates under `src-tauri/target/doc`, avoiding infinite HMR reload that would leave the Tauri window on its transparent background (`vite.config.ts:993-1000`).

**Covers:** `.env.example`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `eslint.config.js`, `index.html`, `package-lock.json` (head only — remainder truncated in chunk), `README.zh-CN.md`, `tsconfig.app.json`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`
