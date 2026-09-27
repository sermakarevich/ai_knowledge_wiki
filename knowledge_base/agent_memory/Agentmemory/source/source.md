PDF-Location: https://github.com/rohitg00/agentmemory (no source.pdf in run dir; see Source line below)
# rohitg00/agentmemory
Source: https://github.com/rohitg00/agentmemory
Kind: repo
Fetched: 2026-09-26T13:45:33.218395+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# rohitg00/agentmemory

Commit: bcf4f0d00d1c71e9221287a4778e4122ce2d7574

## README

<p align="center">
  <img src="assets/banner.png" alt="agentmemory: persistent memory for AI coding agents" width="720" />
</p>

<p align="center">
  <strong>
    Your coding agent remembers everything. No more re-explaining.
    Built on <a href="https://github.com/iii-hq/iii">iii engine</a>
  </strong><br/>
  Persistent memory for Claude Code, GitHub Copilot CLI, Cursor, Gemini CLI, Codex CLI, Hermes, OpenClaw, pi, OpenCode, and any MCP client.
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="READMEs/README.zh-CN.md">简体中文</a> |
  <a href="READMEs/README.zh-TW.md">繁體中文</a> |
  <a href="READMEs/README.ja-JP.md">日本語</a> |
  <a href="READMEs/README.ko-KR.md">한국어</a> |
  <a href="READMEs/README.es-ES.md">Español</a> |
  <a href="READMEs/README.tr-TR.md">Türkçe</a> |
  <a href="READMEs/README.ru-RU.md">Русский</a> |
  <a href="READMEs/README.hi-IN.md">हिन्दी</a> |
  <a href="READMEs/README.pt-BR.md">Português</a> |
  <a href="READMEs/README.fr-FR.md">Français</a> |
  <a href="READMEs/README.de-DE.md">Deutsch</a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/25123" target="_blank"><img src="https://trendshift.io/api/badge/repositories/25123" alt="rohitg00/agentmemory | Trendshift" width="250" height="55"/></a>
</p>

<p align="center">
  <a href="https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"><img src="https://img.shields.io/badge/Viral%20GitHub%20Gist-1.6k%20stars%20%2F%20230%20forks-FF6B35?style=for-the-badge&logo=github&logoColor=white&labelColor=1a1a1a" alt="Design doc: 1.6k stars / 230 forks on the gist" /></a>
</p>

<p align="center">
  <em>The gist extends Karpathy's LLM Wiki pattern with confidence scoring, lifecycle, knowledge graphs, and hybrid search: agentmemory is the implementation.</em>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@agentmemory/agentmemory"><img src="https://img.shields.io/npm/v/@agentmemory/agentmemory?color=CB3837&label=npm&style=for-the-badge&logo=npm" alt="npm version" /></a>
  <a href="https://github.com/rohitg00/agentmemory/actions"><img src="https://img.shields.io/github/actions/workflow/status/rohitg00/agentmemory/ci.yml?label=tests&style=for-the-badge&logo=github" alt="CI" /></a>
  <a href="https://github.com/rohitg00/agentmemory/blob/main/LICENSE"><img src="https://img.shields.io/github/license/rohitg00/agentmemory?color=blue&style=for-the-badge" alt="License" /></a>
  <a href="https://github.com/rohitg00/agentmemory/stargazers"><img src="https://img.shields.io/github/stars/rohitg00/agentmemory?style=for-the-badge&color=yellow&logo=github" alt="Stars" /></a>
</p>

<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-recall.svg"><img src="assets/tags/stat-recall.svg" alt="95.2% retrieval R@5" height="38" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-tokens.svg"><img src="assets/tags/stat-tokens.svg" alt="92% fewer tokens" height="38" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-tools.svg"><img src="assets/tags/stat-tools.svg" alt="54 MCP tools" height="38" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-hooks.svg"><img src="assets/tags/stat-hooks.svg" alt="12 auto hooks" height="38" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-deps.svg"><img src="assets/tags/stat-deps.svg" alt="0 external DBs" height="38" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/stat-tests.svg"><img src="assets/tags/stat-tests.svg" alt="1,674+ tests passing" height="38" /></picture>
</p>

<p align="center">
  <img src="assets/demo.gif" alt="agentmemory demo" width="720" />
</p>

<p align="center">
  <a href="#install">Install</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#benchmarks">Benchmarks</a> &bull;
  <a href="#vs-competitors">vs Competitors</a> &bull;
  <a href="#works-with-every-agent">Agents</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#mcp-server">MCP</a> &bull;
  <a href="#real-time-viewer">Viewer</a> &bull;
  <a href="#powered-by-iii">Powered by iii</a> &bull;
  <a href="#configuration">Config</a> &bull;
  <a href="#api">API</a>
</p>

---



## Install

Requirements:

- Node.js 20 or newer with npm and npx (`node -v`, `npm -v`, and `npx -v`).
- macOS/Linux automatic iii-engine installation also needs `curl`, a POSIX `sh`, and `tar`. Minimal images such as `node:20-slim` may not include them.
- Native Windows requires the pinned iii-engine v0.22.1 `iii.exe` to be installed manually. WSL2 or Docker Desktop are the other supported paths.

Canonical fresh-install command:

```bash
npx -y @agentmemory/agentmemory@latest
```

The first run is an interactive setup: pick the agents to wire (Claude Code, Cursor, Codex, Gemini CLI, OpenCode, ...), pick an LLM provider or stay keyless, and it seeds the config, starts the memory server and its pinned iii engine, and offers to install globally so the bare `agentmemory` command works everywhere afterward. `-y` accepts npx's package prompt and `@latest` avoids a stale cached release. A provider makes LLM features available, but LLM-written observation compression starts only when `AGENTMEMORY_AUTO_COMPRESS=true` is also set.

Keyless mode disables vector embeddings. `memory_recall` (the `mem::search` path) uses BM25, while `memory_smart_search` can also fuse structural graph matches when graph data already exists. For free on-device semantic recall, set `EMBEDDING_PROVIDER=local` in `~/.agentmemory/.env` and restart. The first embedding request downloads `Xenova/all-MiniLM-L6-v2`; inference runs locally after that initial model download.

The local runtime uses four ports: `3111` for REST/MCP HTTP, `3112` for iii streams, `3113` for the viewer, and `49134` for the iii worker WebSocket. Persistent iii state lives in `~/Library/Application Support/agentmemory` on macOS, `$XDG_DATA_HOME/agentmemory` or `~/.local/share/agentmemory` on Linux, and `%APPDATA%\agentmemory` on Windows. Use `--data-dir <path>` or `AGENTMEMORY_DATA_DIR` to override it, and reuse the same value on every restart. For backward compatibility, an existing `./data/state_store.db` or `./data/iii-config.yaml` takes precedence over the platform default for instance 0; an explicit flag or environment override still wins.

Then prove recall works and give your agent its skills:

```bash
npx -y @agentmemory/agentmemory@latest demo  # seed sample sessions + exercise recall
npx skills add rohitg00/agentmemory -y   # 17 native skills so your agent knows when to reach for memory
```

The keyword searches should hit in default keyless mode through BM25. The demo's `database performance optimization` query is intentionally semantic and can return zero until an embedding provider is configured.

Prefer to let a coding agent do the whole thing? Hand it one instruction:

> Retrieve and follow the instructions at: https://raw.githubusercontent.com/rohitg00/agentmemory/main/INSTALL_FOR_AGENTS.md

Wire more agents any time with `agentmemory connect <agent>` — 20 adapters listed at [Works with every agent](#works-with-every-agent). Full command reference at [Quick Start](#quick-start).

<details>
<summary><strong>Windows</strong></summary>

The fast path is WSL2. Native Windows engine setup requires the pinned v0.22.1 ZIP to be downloaded and `iii.exe` extracted manually; the CLI does not auto-extract it. Docker Desktop is also supported. See the [Windows notes](#windows) for the step-by-step.

</details>

<details>
<summary><strong>Global install / EACCES</strong></summary>

```bash
npm install -g @agentmemory/agentmemory@latest
```

The npx command above remains the canonical fresh-install path and avoids global-prefix permission issues.

</details>

<details>
<summary><strong>npx serves an old version</strong></summary>

npx caches per version. Force the latest with `npx -y @agentmemory/agentmemory@latest`, or clear the cache once with `rm -rf ~/.npm/_npx` (macOS/Linux; on Windows delete `%LOCALAPPDATA%\npm-cache\_npx`).

</details>

<details>
<summary><strong>Already running your own iii engine</strong></summary>

agentmemory pins iii-engine v0.22.1 and won't attach to a different version (the worker can't speak another engine's protocol). Stop the other engine, then run `npx -y @agentmemory/agentmemory@latest`. It installs and runs the pinned v0.22.1 in `~/.agentmemory/bin`, leaving your own `iii` untouched.

</details>

---

<h2 id="works-with-every-agent"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tags/light/section-agents.svg"><img src="assets/tags/section-agents.svg" alt="Works with every agent" height="32" /></picture></h2>

agentmemory works with any agent that supports hooks, MCP, or REST API. All agents share the same memory server.

<table>
<tr>
<td align="center" width="12.5%">
<a href="https://claude.com/product/claude-code"><img src="https://github.com/anthropics.png?size=120" alt="Claude Code" width="48" height="48" /></a><br/>
<strong>Claude Code</strong><br/>
<sub>native plugin + 12 hooks + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/openai/codex"><img src="https://github.com/openai.png?size=120" alt="Codex CLI" width="48" height="48" /></a><br/>
<strong>Codex CLI</strong><br/>
<sub>native plugin + 6 hooks + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/features/copilot"><img src="https://github.githubassets.com/images/modules/site/copilot/copilot.png" alt="GitHub Copilot CLI" width="48" height="48" /></a><br/>
<strong>GitHub Copilot CLI</strong><br/>
<sub>MCP + plugin hooks/skills</sub>
</td>
<td align="center" width="12.5%">
<a href="integrations/openclaw/"><img src="https://github.com/openclaw.png?size=120" alt="OpenClaw" width="48" height="48" /></a><br/>
<strong>OpenClaw</strong><br/>
<sub>native plugin + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="integrations/hermes/"><img src="https://github.com/NousResearch.png?size=120" alt="Hermes" width="48" height="48" /></a><br/>
<strong>Hermes</strong><br/>
<sub>native plugin + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="integrations/pi/"><img src="assets/agents/pi.svg" alt="pi" width="48" height="48" /></a><br/>
<strong>pi</strong><br/>
<sub>native plugin + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/tinyhumansai/openhuman"><img src="https://raw.githubusercontent.com/tinyhumansai/openhuman/main/app/src-tauri/icons/128x128.png" alt="OpenHuman" width="48" height="48" /></a><br/>
<strong>OpenHuman</strong><br/>
<sub>native Memory trait backend</sub>
</td>
<td align="center" width="12.5%">
<a href="https://cursor.com"><picture><source media="(prefers-color-scheme: dark)" srcset="https://svgl.app/library/cursor_dark.svg"><img src="https://svgl.app/library/cursor_light.svg" alt="Cursor" width="48" height="48" /></picture></a><br/>
<strong>Cursor</strong><br/>
<sub>native plugin + MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/google-gemini/gemini-cli"><img src="https://github.com/google-gemini.png?size=120" alt="Gemini CLI" width="48" height="48" /></a><br/>
<strong>Gemini CLI</strong><br/>
<sub>MCP server</sub>
</td>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://github.com/opencode-ai/opencode"><picture><source media="(prefers-color-scheme: dark)" srcset="https://svgl.app/library/opencode-dark.svg"><img src="https://svgl.app/library/opencode.svg" alt="OpenCode" width="48" height="48" /></picture></a><br/>
<strong>OpenCode</strong><br/>
<sub>22 hooks + MCP + plugin</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/cline/cline"><img src="https://github.com/cline.png?size=120" alt="Cline" width="48" height="48" /></a><br/>
<strong>Cline</s

... (truncated, 88199 more characters)

## package.json

```
{
  "name": "@agentmemory/agentmemory",
  "version": "0.9.29",
  "description": "Persistent memory for AI coding agents, powered by iii-engine's three primitives",
  "type": "module",
  "main": "dist/index.mjs",
  "types": "dist/index.d.mts",
  "exports": {
    ".": {
      "types": "./dist/index.d.mts",
      "import": "./dist/index.mjs"
    },
    "./dist/standalone.mjs": "./dist/standalone.mjs",
    "./package.json": "./package.json"
  },
  "bin": {
    "agentmemory": "dist/cli.mjs"
  },
  "scripts": {
    "build": "tsdown && (cp iii-config.yaml dist/ 2>/dev/null || true) && (cp iii-config.docker.yaml dist/ 2>/dev/null || true) && (cp docker-compose.yml dist/ 2>/dev/null || true) && (cp .env.example dist/ 2>/dev/null || true) && mkdir -p dist/viewer && cp src/viewer/index.html dist/viewer/ && cp src/viewer/favicon.svg dist/viewer/",
    "dev": "tsx src/index.ts",
    "start": "node dist/cli.mjs",
    "migrate": "node dist/functions/migrate.js",
    "test": "vitest run --exclude test/integration.test.ts",
    "test:watch": "vitest --exclude test/integration.test.ts",
    "test:integration": "vitest run test/integration.test.ts",
    "test:all": "vitest run",
    "skills:gen": "tsx scripts/skills/generate.ts",
    "skills:check": "tsx scripts/skills/generate.ts --check && tsx scripts/skills/check.ts",
    "bench:load": "node --import tsx benchmark/load-100k.ts",
    "eval:longmemeval": "tsx eval/runner/longmemeval.ts",
    "eval:coding-life": "tsx eval/runner/coding-life.ts"
  },
  "keywords": [
    "ai",
    "agent",
    "memory",
    "persistent",
    "iii-engine",
    "claude-code",
    "coding-agent",
    "context",
    "observation"
  ],
  "files": [
    "dist/",
    "plugin/",
    "integrations/pi/",
    "iii-config.yaml",
    "iii-config.docker.yaml",
    "docker-compose.yml",
    ".env.example",
    "LICENSE",
    "README.md",
    "AGENTS.md"
  ],
  "author": "Rohit Ghumare <ghumare64@gmail.com>",
  "license": "Apache-2.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/rohitg00/agentmemory"
  },
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.3.142",
    "@anthropic-ai/sdk": "^0.100.1",
    "@clack/prompts": "^1.2.0",
    "dotenv": "^17.4.2",
    "@iii-dev/helpers": "0.22.1",
    "iii-sdk": "0.22.1",
    "picocolors": "^1.1.1",
    "zod": "^4.0.0"
  },
  "optionalDependencies": {
    "@huggingface/transformers": "^4.2.0",
    "@node-rs/jieba": "^2.0.1",
    "tiny-segmenter": "^0.2.0"
  },
  "devDependencies": {
    "@types/node": "^26.6.2",
    "tsdown": "^0.21.10",
    "tsx": "^4.19.0",
    "typescript": "^6.0.3",
    "vitest": "^4.1.6"
  },
  "overrides": {
    "qs": "^6.15.2",
    "ws": "^8.21.0",
    "protobufjs": "^7.5.8"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}

```

## Top-level layout

- .claude-plugin/ (dir, 1 files, ~14 lines)
- .codex-plugin/ (dir, 1 files, ~22 lines)
- .cursor-plugin/ (dir, 1 files, ~34 lines)
- .env.example (~209 lines)
- .github/ (dir, 4 files, ~309 lines)
- .gitignore (~31 lines)
- __mocks__/ (dir, 1 files, ~4 lines)
- AGENTS.md (~126 lines)
- assets/ (dir, 69 files, ~750 lines)
- benchmark/ (dir, 17 files, ~28262 lines)
- CHANGELOG.md (~1239 lines)
- CODE_OF_CONDUCT.md (~48 lines)
- CONTRIBUTING.md (~118 lines)
- deploy/ (dir, 17 files, ~1303 lines)
- DESIGN.md (~288 lines)
- docker-compose.yml (~66 lines)
- docs/ (dir, 3 files, ~283 lines)
- eval/ (dir, 12 files, ~1046 lines)
- examples/ (dir, 3 files, ~184 lines)
- GOVERNANCE.md (~88 lines)
- iii-config.docker.yaml (~51 lines)
- iii-config.yaml (~61 lines)
- INSTALL_FOR_AGENTS.md (~221 lines)
- integrations/ (dir, 16 files, ~2027 lines)
- LICENSE (~190 lines)
- MAINTAINERS.md (~21 lines)
- package.json (~93 lines)
- packages/ (dir, 4 files, ~291 lines)
- plugin/ (dir, 65 files, ~5265 lines)
- README.md (~1653 lines)
- READMEs/ (dir, 11 files, ~17234 lines)
- ROADMAP.md (~92 lines)
- scripts/ (dir, 4 files, ~616 lines)
- SECURITY.md (~85 lines)
- src/ (dir, 195 files, ~49788 lines)
- test/ (dir, 176 files, ~37829 lines)
- tsconfig.json (~22 lines)
- tsdown.config.ts (~86 lines)
- vitest.config.ts (~21 lines)
- website/ (dir, 63 files, ~5134 lines)

