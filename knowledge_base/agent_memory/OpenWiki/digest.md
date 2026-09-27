> [[index|Wiki]] | [[summary|Summary]]

# kdsz001/OpenWiki — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** OpenWiki is a privacy-first desktop app where anything you copy raises a capture popup, content you choose to keep is stored in a local SQLite database, and AI organizes it into a wiki, knowledge graph, and insight reports.

## Key points

- Copy-to-knowledge flow is explicit opt-in: "Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base" and "Only content you actively choose to keep gets saved" (`README.md:19`, `README.md:37`).
- Capture popup handles text, images, and URLs with automatic source-app detection, auto-dismisses after 10 seconds, and fetches full article content from WeChat, X/Twitter, and other URLs (`README.md:36`, `README.md:38`, `README.md:39`).
- All data is stored in a local SQLite database, with two disclosed network exceptions: URL reading can send the full URL to Jina Reader and the Chinese UI can send foreign-language page text to Google Translate, both enabled by default and independently disableable (`README.md:24`, `README.md:27`).
- The AI knowledge base auto-compiles captures into Wiki pages (concepts, entities, topics), renders a knowledge-graph visualization, offers an Ask sidebar grounded in the user's content, and auto-detects orphans, broken links, and structural issues (`README.md:52`, `README.md:53`, `README.md:54`, `README.md:55`).
- One-click AI weekly reports summarize captures with a 7-dimension attention analysis (At a Glance / Subconscious / Graveyard / Blind Spots / Hot Topics / Heatmap / Action Items), and liking or dismissing items trains preferences (`README.md:60`, `README.md:61`, `README.md:63`).
- AI connectivity supports Anthropic (Claude), OpenAI, and Google Gemini via API Key or OAuth login, with per-provider model selection configured under Settings → AI (`README.md:68`, `README.md:69`, `README.md:70`, `README.md:102`).
- Desktop app targets macOS and Windows with system-tray residency, `⌘⇧C` / `Ctrl+Shift+C` manual capture, `⌘⇧Y` / `Ctrl+Shift+Y` main-window shortcut, Dark / Light / System themes, and MCP integration with Claude Desktop (`README.md:40`, `README.md:75`, `README.md:76`, `README.md:77`, `README.md:78`).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** The top-level files define OpenWiki's project entry point, build/lint/typecheck configuration, agent and design rules, and ignored/secret-file conventions for a Tauri 2 + React 19 desktop app.

## Key points

- The stack is a Tauri 2 desktop app with React 19 + Tailwind 4 + Zustand + Framer Motion frontend, Rust + SQLite (rusqlite) backend, npm and Vite 6 (`AGENTS.md:128-135`, `CLAUDE.md:204-211`).
- `index.html:11-18` is the Vite entry: mounts `<div id="root">`, loads `/src/main.tsx`, sets `<title>OpenWiki</title>`, and preloads Plus Jakarta Sans / JetBrains Mono / Cabinet Grotesk fonts.
- Secrets are templated by `.env.example:4-9`, which declares `GEMINI_CLIENT_ID`, `GEMINI_CLIENT_SECRET`, and `OPENAI_OAUTH_CLIENT_ID` as OAuth placeholders copied into `.env`.
- `.gitignore:54-57` ignores `.env` and `.env.*` while re-allowing `!.env.example`, and also ignores logs, `node_modules`, `dist`, editor dirs, and build artifacts (`src-tauri/resources/yt-dlp_macos`, `src-tauri/resources/markitdown/*`).
- `AGENTS.md:1-72` and `CLAUDE.md:1-72` are near-identical agent playbooks (permissions, decision protocol, GitHub push on "存一下"/"保存进度", Codex/Claude-owned release flow via `release-notes/README.md`, skill routing table).
- `DESIGN.md:1-106` is the normative design system (Brutally Minimal + warm accent `#F97316`, font/type scales, warm neutrals, dark mode, Lucide icons, minimal-functional motion, 2026-03-25 decisions log).
- `package-lock.json:1-9` pins `openwiki@0.3.25` (lockfileVersion 3, MIT) with Tauri plugins, React 19, i18next, d3-force, framer-motion, and Vite 6 / TS ~5.9.3 toolchain; the chunked copy is truncated after ~732 lines (`package-lock.json:732-733`).

## The system in five moves

1. Anything copied on the desktop raises a capture popup, and only content the user actively keeps enters the system.
2. Kept text, images, and links land in a local SQLite store with type/time filtering, global search, and Markdown export.
3. AI compiles the captures into wiki pages of concepts, entities, and topics, visualized as a knowledge graph with an Ask sidebar and structural issue detection.
4. One-click weekly reports with 7-dimension attention analysis summarize what was captured, and likes/dismissals train the AI's preferences.
5. The whole product ships as a Tauri 2 + React 19 desktop app (macOS/Windows, tray-resident, themed, MCP-connected) whose root files pin the entry point, build/lint/typecheck config, agent playbooks, design system, and secret/ignore conventions.
