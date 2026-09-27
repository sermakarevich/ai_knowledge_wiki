> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** OpenWiki is a privacy-first desktop app where anything you copy raises a capture popup, content you choose to keep is stored in a local SQLite database, and AI organizes it into a wiki, knowledge graph, and insight reports.
## Key points
- Copy-to-knowledge flow is explicit opt-in: "Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base" and "Only content you actively choose to keep gets saved" (`README.md:19`, `README.md:37`).
- Capture popup handles text, images, and URLs with automatic source-app detection, auto-dismisses after 10 seconds, and fetches full article content from WeChat, X/Twitter, and other URLs (`README.md:36`, `README.md:38`, `README.md:39`).
- All data is stored in a local SQLite database, with two disclosed network exceptions: URL reading can send the full URL to Jina Reader and the Chinese UI can send foreign-language page text to Google Translate, both enabled by default and independently disableable (`README.md:24`, `README.md:27`).
- The AI knowledge base auto-compiles captures into Wiki pages (concepts, entities, topics), renders a knowledge-graph visualization, offers an Ask sidebar grounded in the user's content, and auto-detects orphans, broken links, and structural issues (`README.md:52`, `README.md:53`, `README.md:54`, `README.md:55`).
- One-click AI weekly reports summarize captures with a 7-dimension attention analysis (At a Glance / Subconscious / Graveyard / Blind Spots / Hot Topics / Heatmap / Action Items), and liking or dismissing items trains preferences (`README.md:60`, `README.md:61`, `README.md:63`).
- AI connectivity supports Anthropic (Claude), OpenAI, and Google Gemini via API Key or OAuth login, with per-provider model selection configured under Settings → AI (`README.md:68`, `README.md:69`, `README.md:70`, `README.md:102`).
- Desktop app targets macOS and Windows with system-tray residency, `⌘⇧C` / `Ctrl+Shift+C` manual capture, `⌘⇧Y` / `Ctrl+Shift+Y` main-window shortcut, Dark / Light / System themes, and MCP integration with Claude Desktop (`README.md:40`, `README.md:75`, `README.md:76`, `README.md:77`, `README.md:78`).
---
## Capture popup
Popup appears on copy and auto-dismisses after 10 seconds; nothing is saved unless the user actively keeps it (`README.md:36`, `README.md:37`).

Verbatim positioning:

> Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base<br>
> **You decide what to keep. AI makes sense of it.** (`README.md:19`, `README.md:20`)

Capabilities:

- Supports text, images, and URLs with automatic source app detection (`README.md:38`)
- Fetches full article content from WeChat, X/Twitter, and other URLs (`README.md:39`)
- Manual trigger: `⌘⇧C` on macOS or `Ctrl+Shift+C` on Windows (`README.md:40`)

## Content management
Filter by type (`text` / `image` / `link`) and time range, search globally across content and knowledge base, and export to Markdown in one click (`README.md:45`, `README.md:46`, `README.md:47`).

## AI knowledge base
AI automatically compiles captured content into Wiki pages of concepts, entities, and topics, plus a knowledge-graph view of how ideas connect (`README.md:52`, `README.md:53`).

- **Ask sidebar** — ask questions about the knowledge base; AI answers based on the user's content (`README.md:54`)
- Auto-detects orphaned pages, broken links, and structural issues (`README.md:55`)

## Insight reports
One-click AI weekly report summarizing captured content (`README.md:60`).

Attention analysis covers exactly 7 dimensions (`README.md:61`):

| # | Dimension |
|---|---|
| 1 | At a Glance |
| 2 | Subconscious |
| 3 | Graveyard |
| 4 | Blind Spots |
| 5 | Hot Topics |
| 6 | Heatmap |
| 7 | Action Items |

Liking or dismissing report items teaches the AI the user's preferences (`README.md:63`).

## AI providers and privacy
Supported providers: **Anthropic (Claude)** / **OpenAI** / **Google Gemini**; connection via API Key or OAuth login; different models selectable per provider (`README.md:68`, `README.md:69`, `README.md:70`).

> **Network transparency:** URL reading can send the full URL to Jina Reader, and the Chinese UI can send foreign-language page text to Google Translate. Both are enabled by default for compatibility and can be disabled independently in Settings. Platform-specific readers may still contact the source platform or its API. (`README.md:27`)

Privacy baseline: "Privacy first — all data stored in local SQLite database." (`README.md:24`)

## Desktop experience and distribution
System tray keeps the app running when the window closes; `⌘⇧Y` (macOS) or `Ctrl+Shift+Y` (Windows) shows the main window; Dark / Light / System theme; MCP protocol integration connects to Claude Desktop (`README.md:75`, `README.md:76`, `README.md:77`, `README.md:78`).

| Platform | Artifact |
|---|---|
| macOS (Apple Silicon) | `OpenWiki_X.Y.Z_aarch64.dmg` (`README.md:84`) |
| macOS (Intel) | `OpenWiki_X.Y.Z_x64.dmg` (`README.md:85`) |
| Windows (x64) | `OpenWiki_X.Y.Z_x64-setup.exe` (recommended) or `OpenWiki_X.Y.Z_x64_en-US.msi` (`README.md:86`) |

First launch: macOS build is signed and notarized (open `.dmg`, drag to Applications, click "Allow", then Settings → AI); Windows build is unsigned so SmartScreen needs **More info** → **Run anyway** before launching and configuring Settings → AI (`README.md:98`, `README.md:100`, `README.md:106`, `README.md:108`).

## Build prerequisites and commands
Prerequisites: Node.js 18+, latest stable Rust, macOS 13+ or Windows 10/11, Xcode Command Line Tools on macOS (`xcode-select --install`), Microsoft C++ / Visual Studio Build Tools and WebView2 Runtime on Windows (`README.md:116`, `README.md:117`, `README.md:118`, `README.md:119`, `README.md:120`).

```bash
git clone https://github.com/kdsz001/OpenWiki.git
cd OpenWiki
npm install
npm run tauri dev
npm run tauri build
```
(`README.md:130`, `README.md:136`, `README.md:141`, `README.md:146`)

Before release bundles, prepare the bundled document converter (`README.md:149`):

```bash
# macOS / Linux
./src-tauri/scripts/setup_markitdown.sh
# Windows PowerShell
./src-tauri/scripts/setup_markitdown.ps1
```
(`README.md:155`, `README.md:160`)

**Covers:** README.md, README.zh-CN.md, docs/banner.svg
