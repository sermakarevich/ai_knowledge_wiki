PDF-Location: https://github.com/kdsz001/OpenWiki (no source.pdf in run dir; see Source line below)
# kdsz001/OpenWiki
Source: https://github.com/kdsz001/OpenWiki
Kind: repo
Fetched: 2026-09-26T13:47:13.290256+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# kdsz001/OpenWiki

Commit: 0e675dd2aa482a76993ab51cc2e4a0ae59044434

## README

<p align="center">
  <img src="docs/banner.svg" alt="OpenWiki Banner" width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/kdsz001/OpenWiki/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-F97316?style=flat-square" alt="License"></a>
  <a href="https://github.com/kdsz001/OpenWiki/releases"><img src="https://img.shields.io/github/v/release/kdsz001/OpenWiki?style=flat-square&color=F97316" alt="Release"></a>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows-F97316?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/PRs-welcome-F97316?style=flat-square" alt="PRs Welcome">
</p>

<p align="center">
  Copy anything → popup appears on desktop → choose to keep → AI organizes it into a knowledge base<br>
  <b>You decide what to keep. AI makes sense of it.</b>
</p>

<p align="center">
  Privacy first — all data stored in local SQLite database.
</p>

> **Network transparency:** URL reading can send the full URL to Jina Reader, and the Chinese UI can send foreign-language page text to Google Translate. Both are enabled by default for compatibility and can be disabled independently in Settings. Platform-specific readers may still contact the source platform or its API.

<p align="center">
  <a href="https://openwiki.pages.dev">🌐 Website</a> · <a href="README.zh-CN.md">中文文档</a>
</p>



### 📋 Capture Popup
- A popup appears on your desktop when you copy something (auto-dismisses after 10 seconds)
- **Only content you actively choose to keep gets saved** — no silent hoarding
- Supports text, images, and URLs with automatic source app detection
- Fetches full article content from WeChat, X/Twitter, and other URLs
- `⌘⇧C` on macOS or `Ctrl+Shift+C` on Windows to manually trigger the capture window



### 📂 Content Management
- Filter by type (text / image / link) and time range
- Global search across content and knowledge base
- One-click export to Markdown



### 🧠 AI Knowledge Base
- AI automatically compiles captured content into Wiki pages (concepts, entities, topics)
- Knowledge graph visualization — see how ideas connect
- **Ask sidebar** — ask questions about your knowledge base, AI answers based on your content
- Auto-detect orphaned pages, broken links, and structural issues



### 📊 Insight Reports
- One-click AI weekly report summarizing captured content
- **Attention analysis** — 7-dimension insights into your information habits:
    - At a Glance / Subconscious / Graveyard / Blind Spots / Hot Topics / Heatmap / Action Items
- Like or dismiss report items — AI learns your preferences



### ⚙️ AI Providers
- Supports **Anthropic (Claude)** / **OpenAI** / **Google Gemini**
- API Key or OAuth login — two ways to connect
- Choose different models for each provider



### 🖥 Desktop Experience
- System tray — closing the window keeps the app running
- `⌘⇧Y` on macOS or `Ctrl+Shift+Y` on Windows to show the main window
- Dark / Light / System theme
- MCP protocol integration — connect to Claude Desktop



## Download

- macOS (Apple Silicon): download `OpenWiki_X.Y.Z_aarch64.dmg`
- macOS (Intel): download `OpenWiki_X.Y.Z_x64.dmg`
- Windows (x64): download `OpenWiki_X.Y.Z_x64-setup.exe` (recommended) or `OpenWiki_X.Y.Z_x64_en-US.msi`

👉 [Go to Releases](https://github.com/kdsz001/OpenWiki/releases)



### ⚠️ First Launch Guide (Important)

Choose the steps for your operating system.

#### macOS

The app is signed and notarized by Apple — just double-click to open, no security bypass needed:

1. Open the `.dmg` and drag OpenWiki into the Applications folder
2. Launch the app and click "Allow" in the authorization prompt
3. Go to Settings → AI to configure your AI provider

#### Windows

The Windows build is unsigned, so Microsoft Defender SmartScreen may warn on first launch:

1. Run `OpenWiki_X.Y.Z_x64-setup.exe`
2. If SmartScreen appears, choose **More info** → **Run anyway**
3. Launch OpenWiki from the Start menu or desktop shortcut
4. Go to Settings → AI to configure your AI provider



### Prerequisites
- Node.js 18+
- Rust (latest stable)
- macOS 13+ or Windows 10/11
- macOS: Xcode Command Line Tools (`xcode-select --install`)
- Windows: Microsoft C++ Build Tools / Visual Studio Build Tools and WebView2 Runtime



### Getting Started

```bash


# Clone the repo
git clone https://github.com/kdsz001/OpenWiki.git
cd OpenWiki



# Install dependencies
npm install



# Development mode
npm run tauri dev



# Build the app
npm run tauri build
```

Before creating release bundles, prepare the bundled document converter:

```bash


# macOS / Linux
./src-tauri/scripts/setup_markitdown.sh



# Windows PowerShell
./src-tauri/scripts/setup_markitdown.ps1
```



## Special Thanks

Thanks to everyone who helped spread the word:

- [@NFTCPS](https://x.com/NFTCPS)



## Author

**Ray** — [@BitcoinRui](https://x.com/BitcoinRui)

## package.json

```
{
  "name": "openwiki",
  "private": false,
  "version": "0.3.25",
  "description": "Desktop AI knowledge management tool for macOS and Windows — capture clipboard, build personal wiki, get AI insights",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/kdsz001/OpenWiki.git"
  },
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "tauri": "tauri"
  },
  "dependencies": {
    "@tauri-apps/api": "^2",
    "@tauri-apps/plugin-autostart": "^2.5.1",
    "@tauri-apps/plugin-clipboard-manager": "^2",
    "@tauri-apps/plugin-process": "^2.3.1",
    "@tauri-apps/plugin-shell": "^2.3.5",
    "@tauri-apps/plugin-updater": "^2.10.1",
    "@types/d3-force": "^3.0.10",
    "d3-force": "^3.0.0",
    "framer-motion": "^11",
    "i18next": "^26.0.4",
    "i18next-browser-languagedetector": "^8.2.1",
    "lucide-react": "^1.6.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-i18next": "^17.0.2",
    "react-markdown": "^10.1.0",
    "remark-gfm": "^4.0.1",
    "zustand": "^5"
  },
  "overrides": {
    "enhanced-resolve": "5.18.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.39.1",
    "@tailwindcss/typography": "^0.5.19",
    "@tailwindcss/vite": "^4.1.18",
    "@tauri-apps/cli": "^2",
    "@types/node": "^24.10.1",
    "@types/react": "^19.2.5",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^5.1.1",
    "autoprefixer": "^10",
    "eslint": "^9.39.1",
    "eslint-plugin-react-hooks": "^7.0.1",
    "eslint-plugin-react-refresh": "^0.4.24",
    "globals": "^16.5.0",
    "postcss": "^8",
    "tailwindcss": "^4",
    "typescript": "~5.9.3",
    "typescript-eslint": "^8.46.4",
    "vite": "^6.4.1"
  }
}

```

## Top-level layout

- .claude/ (dir, 2 files, ~12 lines)
- .env.example (~9 lines)
- .github/ (dir, 1 files, ~258 lines)
- .gitignore (~60 lines)
- AGENTS.md (~71 lines)
- CHANGELOG.md (~111 lines)
- CLAUDE.md (~71 lines)
- CODE_OF_CONDUCT.md (~40 lines)
- CONTRIBUTING.md (~99 lines)
- DESIGN.md (~105 lines)
- docs/ (dir, 6 files, ~341 lines)
- eslint.config.js (~23 lines)
- index.html (~18 lines)
- LICENSE (~21 lines)
- mockups/ (dir, 4 files, ~3315 lines)
- package-lock.json (~6020 lines)
- package.json (~62 lines)
- README.md (~163 lines)
- README.zh-CN.md (~163 lines)
- release-notes/ (dir, 34 files, ~1395 lines)
- scripts/ (dir, 1 files, ~111 lines)
- src/ (dir, 64 files, ~16066 lines)
- src-tauri/ (dir, 98 files, ~33856 lines)
- tsconfig.app.json (~28 lines)
- tsconfig.json (~7 lines)
- tsconfig.node.json (~26 lines)
- vite.config.ts (~19 lines)

