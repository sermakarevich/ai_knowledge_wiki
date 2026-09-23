# QwenAudio/qwen-audio-agent
Source: https://github.com/QwenAudio/qwen-audio-agent
Kind: repo
Fetched: 2026-09-22T14:37:30.399021+00:00
Tool: git-clone
PDF: https://github.com/QwenAudio/qwen-audio-agent

# QwenAudio/qwen-audio-agent

Commit: 0d9372ffde0699bc77cd2a474797ea1f7746a195

## README

# Qwen Audio Agent

[中文](README_ZH.md) | [English](README.md) | [User Guide](https://qwenaudio.github.io/qwen-audio-agent/) | [Quickstart](https://qwenaudio.github.io/qwen-audio-agent/getting-started/quickstart)

[![CI](https://github.com/QwenAudio/qwen-audio-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/QwenAudio/qwen-audio-agent/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/qwen-audio-agent)](https://www.npmjs.com/package/qwen-audio-agent)
[![node](https://img.shields.io/badge/node-%E2%89%A522.22.2-brightgreen)](https://nodejs.org/)
[![license](https://img.shields.io/github/license/QwenAudio/qwen-audio-agent)](LICENSE)
[![WeChat](https://img.shields.io/badge/WeChat-join_chat-07C160?logo=wechat&logoColor=white)](#community)

## Agent Presence

Real conversation should not leave you waiting after a single sentence, nor
should it grind to a halt just because the Agent is looking something up,
calling a tool, or working on a task.

Conversation should keep flowing, and the Agent should always be present.

That is why we built **qwen-audio-agent**—a realtime voice runtime that keeps
Agents talking, working, and present. Whether chatting with you, thinking
through a problem, or working on a task, your Agent remains in the
conversation. It listens, responds, and when the task is complete, naturally
tells you:

"It's ready."

## News

- **2026-08-27 · v2.0.0 (In development)**
  🚧 The next major version is under active development, with ongoing work on the Agent architecture, task lifecycle, multimodal input, memory, and extensibility.
- **2026-08-20 · [v1.11.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.11.0)**
  🧩 Adds embeddable Gateway and Realtime Provider extensions; 🛠️ supports installing and managing Agent Skills; 📎 adds multimodal input to the TUI; 🎨 links pet animations to runtime states.
- **2026-08-13 · [v1.9.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.9.0)**
  🧩 Desktop task cards show live Agent progress; 🔎 backend Agent selection is clearer and searchable; 🎙️ supports Qwen3.5-Omni Realtime frontend integration.
- **2026-08-07 · [v1.7.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.7.0)**
  🎨 The orb opens up custom skins — import your own look, compatible with pet packs from the [Awesome Codex Pet](https://codexpet.top/) community gallery; 🪟 improved Windows backend Agent startup.
- **2026-08-05 · [v1.5.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.5.0)**
  ⏰ Adds scheduled reminders and progress reporting; 🗣️ adds the voice wake word ("你好千问"); 🐧 desktop build support for Linux; the desktop app now uses a data directory isolated from the CLI.
- **2026-08-03 · [v1.3.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.3.0)**
  🎙️ Adds [🤗 speech-to-speech](https://github.com/huggingface/speech-to-speech) frontend integration, supporting fully local VAD, STT, LLM, and TTS.
- **2026-07-30 · [v1.0.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.0.0)**
  🚀 First stable release, introducing a macOS desktop app with a built-in Gateway.
- **2026-07-28 · [v0.9.0](https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v0.9.0)**
  🌍 Project officially open-sourced; backend Agents unified under the ACP architecture.

## Conversation Continues, Tasks Too

Conversation doesn't stop for background tasks; when a task completes, the
result naturally returns to the current conversation:

<table>
  <tr>
    <th width="50%">Office</th>
    <th width="50%">Smart Cockpit</th>
  </tr>
  <tr>
    <td width="50%">
      <video src="https://github.com/user-attachments/assets/ab570531-8da9-4af4-93fa-244bb6614c05" controls width="100%"></video>
    </td>
    <td width="50%">
      <video src="https://github.com/user-attachments/assets/29375a62-d5d0-46e8-a963-e00118688002" controls width="100%"></video>
    </td>
  </tr>
</table>

### Core Features

- Full-duplex realtime voice interaction, natural interruption, and sustained multi-turn conversation
- Replaceable realtime voice frontends, with cloud services and local deployment options
- One-click integration with your preferred Agent, reusing its model configuration, tools, MCP, Skills, and authentication
- Frontend conversation and background tasks run in parallel; ask about progress or cancel at any time
- Create multiple independent tasks executed asynchronously by the backend Agent, with continuous status tracking
- Task results automatically return to the current conversation, supporting follow-up questions and modifications
- WebUI, terminal TUI, and desktop floating orb (macOS / Windows / Linux)
- Long-term per-user personalization and cross-session memory

## Architecture

<table>
  <tr>
    <td width="50%">
      <img src="docs/architecture-overview-en.png" alt="qwen-audio-agent architecture">
    </td>
    <td width="50%">
      <img src="docs/qwen-audio-agent-three-layer-architecture-en.png" alt="qwen-audio-agent reference architecture">
    </td>
  </tr>
</table>

Questions that can be answered directly are answered immediately; when tools
or sustained processing are needed, the task is delegated to the backend Agent.
Throughout, the user always faces the same assistant.

For the full design and module breakdown, see the [architecture document](docs/architecture/deep-dive.md).

## Frontend and Backend Support

The voice frontend handles realtime conversation; the backend Agent executes
tasks. They integrate independently and can be combined as needed.

### Voice Frontends

| Voice frontend | Deployment | Setup | Features |
| --- | --- | --- | --- |
| [Qwen Audio 3.0 Realtime](docs/voice-frontends/qwen-audio-realtime.md) | Cloud | Bailian API Key | Default frontend |
| [GPT-Live / OpenAI Realtime](docs/voice-frontends/gpt-live.md) | Cloud | OpenAI API Key | OpenAI GA Realtime dialect |
| [Google Gemini Live](docs/voice-frontends/google-live.md) | Cloud | Google API Key | Native Gemini Live WebSocket |
| [Qwen3.5-Omni Realtime](docs/voice-frontends/qwen-omni-realtime.md) | Cloud | Bailian API Key | Video input |
| [StepAudio 3 Realtime](docs/voice-frontends/stepfun.md) | Cloud | StepFun API Key | Preview model |
| [Hugging Face Speech-to-Speech](docs/voice-frontends/speech-to-speech.md) | Local | Start the service and set its URL | Configurable components |
| [MiniCPM-o 4.5](docs/voice-frontends/minicpm-o.md) | Local or cloud | Compatible service URL | Backend delegation not yet supported |

To connect another voice service, implement the
[Realtime Provider interface](docs/voice-frontends/custom-provider.md) without
changing the Gateway's core voice-session or backend-task logic.

### Backend Agents

| Backend Agent | Integration | Setup | Rating |
| --- | --- | --- | --- |
| None | N/A | Frontend-only mode, no backend config needed | ★★★★★ |
| Qwen Code | Native ACP | One-click install, user config required | ★★★★★ |
| OpenCode | Native ACP | One-click install + Bailian config | ★★★★★ |
| OpenClaw | Built-in ACP bridge | One-click install + Bailian config | ★★★★★ |
| Qoder | Native ACP | One-click install, user config required | ★★★★★ |
| MiniMax Code | Native ACP | One-click install, user config required | ★★★★☆ |
| Kimi Code | Native ACP | One-click install, user config required | ★★★★★ |
| Hermes | Native ACP | One-click install, user config required | ★★★★☆ |
| CodeBuddy | Native ACP | One-click install, user config required | ★★★★☆ |
| Codex | External ACP adapter | One-click install (base + adapter), user config required | ★★★★☆ |
| Claude Code | External ACP adapter | One-click install (base + adapter), user config required | ★★★★☆ |
| DeepSeek Harness | Native ACP | One-click install, DeepSeek API key required | ★★★★☆ |
| Pi | External ACP adapter | One-click install (base + adapter), user config required | ★★★★☆ |
| Muse Code | Native MSP adapter | Install Muse and its optional SDK on demand; user config required | ★★★☆☆ |

Ratings reflect current integration completeness, compatibility, and
verification level: five stars indicate a thoroughly tested recommended
integration; four stars indicate active development or not yet fully verified.
For detailed configuration and capability boundaries, see the
[backend Agent documentation](docs/backends/overview.md) and
[configuration guide](docs/configuration.md).

## Installation

Requires Node.js 22.22.2+ or 24.15.0+, npm 10+. One-click install (recommended):

```bash
npm install -g qwen-audio-agent
```

For building from source, installing from GitHub, and obtaining a DashScope
API Key, see the [installation guide](docs/getting-started/install.md).

## Quick Start

1. Create your config and fill in the API Key:

```bash
qwenaudio config
```

```dotenv
DASHSCOPE_API_KEY=your-key
# Voice frontend model: optional, defaults to Qwen Audio 3.0 Realtime Plus
QWEN_AUDIO_REALTIME_MODEL=qwen-audio-3.0-realtime-plus
# Backend Agent: optional, leave empty or set to none for frontend-only mode
AGENT_PROTOCOL=openclaw
# Backend model: optional; explicit values use standard ACP, empty reuses Agent config
QWEN_AUDIO_AGENT_BACKEND_MODEL=qwen3.7-max
```

Before starting, create a key from the [Bailian API Key page](https://bailian.console.aliyun.com/?tab=model#/api-key).
Eligible new users can review the [new-user free quota](https://help.aliyun.com/zh/model-studio/new-free-quota)
and check remaining usage on the [model usage page](https://help.aliyun.com/zh/model-studio/model-usage-statistics).
Quota and billing rules are subject to the current official Bailian documentation.

> The example above uses the default DashScope voice frontend. See
> [Voice Frontends](#voice-frontends) for other cloud and self-hosted options.

With a visual-capable Realtime frontend, WebUI can explicitly stream bounded
camera frames alongside live audio. See [Realtime frontend configuration](docs/configuration/frontend.md).

2. Start the Gateway, then open another terminal to start the TUI (or use `qwenaudio webui` for the browser UI):

```bash
qwenaudio        # Terminal 1: Gateway
qwenaudio tui    # Terminal 2: TUI
```

For full configuration options, local voice frontend setup, and TUI platform
notes, see [quick start](docs/getting-started/quickstart.md),
[voice frontends](docs/configuration/frontend.md), and
[TUI notes](docs/getting-started/tui.md).

## Desktop App

The desktop app provides a persistent floating voice orb with a built-in
Gateway, automatic idle sleep, local voice wake, and customizable appearance.
Download the installer for your platform from the releases page, or build from
source:

```bash
npm run desktop:build:local      # macOS
npm run desktop:build:win        # Windows
npm run desktop:build:linux      # Linux (AppImage + deb, no signing)
```

For visuals, orb behavior, and build instructions, see the
[desktop documentation](docs/desktop/overview.md).

## Examples and Scenario Expansion

The current qwen-audio-agent framework focuses on desktop productivity: users
can keep talking with the Agent in realtime while delegating tool use, file
work, code changes, and long-running tasks to the backend Agent.

This "foreground conversation + background task" design is not limited to
desktop use. It can also expand to more scenarios where the Agent can both
chat naturally and get real work done.

| Scenario | Description | Link | Status |
| --- | --- | --- | --- |
| Desktop | Voice chat, progress follow-up, tools, and background tasks. | [Docs][desktop-docs] | Available |
| Smart cockpit | Vehicle control, navigation, music, weather, and services. | [Example][smart-cockpit-example] | Available |
| X-Omni | Visual conversation, on-demand capture, optional observation and narration. | [Example](https://github.com/QwenAudio/qwen-audio-agent/tree/main/examples/x-omni/README.md) | Available |
| AI Passport | Qwen Voice Bean on a hardware card, with voice conversation and backend tasks. Currently half-duplex only. | [Example][ai-passport-example] | Available |
| C

... (truncated, 1498 more characters)

## package.json

```
{
  "name": "qwen-audio-agent",
  "desktopName": "qwen-audio-agent.desktop",
  "version": "1.11.0",
  "description": "A realtime voice runtime that keeps AI agents talking, working, and present.",
  "author": "qwen-audio-agent contributors",
  "license": "Apache-2.0",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/QwenAudio/qwen-audio-agent.git"
  },
  "bugs": {
    "url": "https://github.com/QwenAudio/qwen-audio-agent/issues"
  },
  "homepage": "https://github.com/QwenAudio/qwen-audio-agent#readme",
  "keywords": [
    "qwen",
    "audio",
    "voice",
    "agent",
    "opencode",
    "openclaw",
    "qoder",
    "kimi-code",
    "claude-code",
    "deepseek",
    "minimax-code"
  ],
  "type": "module",
  "exports": {
    "./package.json": "./package.json",
    "./electron": "./shared/electron-host.cjs",
    "./gateway-protocol": "./server/src/core/gateway-protocol.mjs",
    "./gateway-setup": "./shared/gateway/setup.mjs",
    "./gateway-process": "./shared/gateway/process.mjs",
    "./gateway-lease": "./shared/gateway/lease.mjs",
    "./runtime-paths": "./shared/runtime-paths.mjs",
    "./realtime-events": "./shared/protocol/realtime-events.mjs",
    "./gateway-events": "./shared/protocol/gateway-events.mjs",
    "./gateway-client-protocol": "./shared/protocol/gateway-client-protocol.mjs",
    "./gateway-client-sdk": "./shared/gateway/client-sdk.mjs",
    "./gateway-client-profiles": "./shared/gateway/client-profiles.mjs",
    "./gateway-access-client": "./shared/gateway/access-client.mjs",
    "./gateway-remote-access": "./shared/gateway/remote-access.mjs",
    "./gateway-connection-profiles": "./shared/gateway/connection-profiles.mjs",
    "./gateway-file-credential-store": "./shared/gateway/file-credential-store.mjs",
    "./gateway-websocket-auth": "./shared/gateway/websocket-auth.mjs",
    "./client-events": "./server/src/client/client-event-router.mjs",
    "./client-actions": "./server/src/client/client-action-port.mjs",
    "./agent-delivery": "./server/src/delivery/agent-delivery.mjs",
    "./ag-ui-events": "./shared/protocol/agui-events.mjs",
    "./session-events": "./shared/session-events.mjs",
    "./session-journal": "./server/src/session/session-journal.mjs",
    "./session-replay": "./server/src/session/session-replay.mjs",
    "./conversation-history": "./shared/conversation-history.mjs",
    "./gateway-client-state": "./shared/gateway/client-state.mjs",
    "./gateway-application": "./server/src/app/gateway-application.mjs",
    "./backend-adapter-sdk": "./server/src/backend/backend-adapter-sdk.mjs",
    "./a2a-backend-adapter": "./server/src/backend/adapters/a2a/backend-adapter.mjs",
    "./realtime-provider": "./server/src/voice/realtime-provider-extension.mjs",
    "./web-retrieval": "./server/src/frontend/retrieval/providers/web-retrieval.mjs",
    "./knowledge-provider": "./server/src/knowledge/provider.mjs",
    "./memory-provider": "./server/src/memory/provider.mjs",
    "./voicemem-provider": "./server/src/memory/providers/voicemem/provider.mjs",
    "./settings": "./desktop/src/settings-store.mjs",
    "./skin-store": "./desktop/src/skin-store.mjs",
    "./orb/main": "./desktop/src/orb-shell.mjs",
    "./orb/window": "./desktop/src/orb-window.mjs",
    "./orb/placement": "./desktop/src/orb-placement.mjs",
    "./orb/presence": "./desktop/src/desktop-presence.mjs",
    "./orb/preload": "./desktop/src/preload.cjs",
    "./orb/url": "./desktop/src/orb-url.mjs",
    "./web-dist/*": "./web/dist/*"
  },
  "bin": {
    "qwenaudio": "cli/bin/qwenaudio.mjs"
  },
  "files": [
    "cli/bin/",
    "cli/src/",
    "cli/package.json",
    "config/frontend-agent/",
    "config/backends/openclaw/openclaw.json5",
    "config/backends/deepseek-harness/cordis.yml",
    "examples/ai-passport/",
    "examples/webrtc/",
    "docs/architecture/overview.md",
    "docs/architecture/overview.zh.md",
    "docs/architecture/deep-dive.md",
    "docs/architecture/deep-dive.zh.md",
    "docs/architecture-overview.png",
    "docs/architecture-overview-en.png",
    "docs/desktop-fluid-orb-thinking.gif",
    "docs/desktop-goo-orb-thinking.gif",
    "docs/qwen-audio-agent-three-layer-architecture.png",
    "docs/qwen-audio-agent-three-layer-architecture-en.png",
    "docs/qwen-audio-agent-three-layer-architecture.svg",
    "docs/qwen-audio-agent-two-layer-architecture.png",
    "docs/voice-agent-architecture-presentation.zh.md",
    "docs/configuration.md",
    "docs/configuration.zh.md",
    "docs/configuration/frontend.md",
    "docs/configuration/frontend.zh.md",
    "docs/configuration/backend.md",
    "docs/configuration/backend.zh.md",
    "docs/configuration/advanced.md",
    "docs/configuration/advanced.zh.md",
    "docs/contract.md",
    "docs/contract.zh.md",
    "docs/extensions.md",
    "docs/extensions.zh.md",
    "docs/gateway-protocol.md",
    "docs/gateway-protocol.zh.md",
    "docs/gateway-webrtc-client.md",
    "docs/gateway-webrtc-client.zh.md",
    "docs/roadmap/gateway-client-protocol.md",
    "docs/roadmap/gateway-client-protocol.zh.md",
    "docs/roadmap/gateway-remote-access.md",
    "docs/roadmap/gateway-remote-access.zh.md",
    "docs/backends/overview.md",
    "docs/backends/overview.zh.md",
    "docs/backends/configuration.md",
    "docs/backends/configuration.zh.md",
    "docs/backends/extend.md",
    "docs/backends/extend.zh.md",
    "docs/desktop/overview.md",
    "docs/desktop/overview.zh.md",
    "docs/desktop/pet-skin-spec.md",
    "docs/desktop/pet-skin-spec.zh.md",
    "docs/desktop/examples/firefly.pet.json",
    "docs/getting-started/install.md",
    "docs/getting-started/install.zh.md",
    "docs/getting-started/quickstart.md",
    "docs/getting-started/quickstart.zh.md",
    "docs/getting-started/concepts.md",
    "docs/getting-started/concepts.zh.md",
    "docs/getting-started/tui.md",
    "docs/getting-started/tui.zh.md",
    "docs/getting-started/webui.md",
    "docs/getting-started/webui.zh.md",
    "docs/getting-started/mobile.md",
    "docs/getting-started/mobile.zh.md",
    "docs/guides/",
    "docs/operations/",
    "docs/reference/memory.md",
    "docs/reference/memory.zh.md",
    "docs/reference/memory-provider.md",
    "docs/reference/memory-provider.zh.md",
    "docs/reference/preference-learning.md",
    "docs/reference/preference-learning.zh.md",
    "docs/reference/desktop-animations.md",
    "docs/reference/desktop-animations.zh.md",
    "docs/reference/personalization.md",
    "docs/reference/personalization.zh.md",
    "docs/reference/knowledge.md",
    "docs/reference/knowledge.zh.md",
    "docs/reference/frontend-evaluations.md",
    "docs/reference/frontend-evaluations.zh.md",
    "docs/reference/frontend-mcp.md",
    "docs/reference/frontend-mcp.zh.md",
    "docs/reference/frontend-openapi.md",
    "docs/reference/frontend-openapi.zh.md",
    "docs/reference/frontend-profile.md",
    "docs/reference/frontend-profile.zh.md",
    "docs/reference/cli.md",
    "docs/reference/cli.zh.md",
    "docs/reference/backend-adapter-sdk.md",
    "docs/reference/backend-adapter-sdk.zh.md",
    "docs/reference/a2a-backend-adapter.md",
    "docs/reference/a2a-backend-adapter.zh.md",
    "docs/voice-frontends/speech-to-speech.md",
    "docs/voice-frontends/stepfun.md",
    "docs/voice-frontends/stepfun.zh.md",
    "docs/voice-frontends/speech-to-speech.zh.md",
    "docs/voice-frontends/minicpm-o.md",
    "docs/voice-frontends/minicpm-o.zh.md",
    "docs/voice-frontends/custom-provider.md",
    "docs/voice-frontends/custom-provider.zh.md",
    "docs/voice-frontends/qwen-audio-realtime.md",
    "docs/voice-frontends/qwen-audio-realtime.zh.md",
    "docs/voice-frontends/qwen-omni-realtime.md",
    "docs/voice-frontends/qwen-omni-realtime.zh.md",
    "docs/voice-frontends/gpt-live.md",
    "docs/voice-frontends/gpt-live.zh.md",
    "docs/voice-frontends/google-live.md",
    "docs/voice-frontends/google-live.zh.md",
    "docs/scenarios/smart-cockpit.md",
    "docs/scenarios/index.md",
    "d

... (truncated, 10500 more characters)
```

## Top-level layout

- .env.example (~180 lines)
- .github/ (dir, 9 files, ~710 lines)
- .gitignore (~46 lines)
- .gitlab/ (dir, 5 files, ~439 lines)
- .node-version (~1 lines)
- .npmignore (~7 lines)
- .npmrc (~1 lines)
- .nvmrc (~1 lines)
- CHANGELOG.md (~411 lines)
- cli/ (dir, 22 files, ~7289 lines)
- config/ (dir, 4 files, ~214 lines)
- CONTRIBUTING.md (~77 lines)
- desktop/ (dir, 88 files, ~14253 lines)
- docs/ (dir, 170 files, ~17201 lines)
- eslint.config.mjs (~144 lines)
- examples/ (dir, 379 files, ~73703 lines)
- LICENSE (~201 lines)
- mobile/ (dir, 81 files, ~2292 lines)
- NOTICE (~5 lines)
- package-lock.json (~11637 lines)
- package.json (~369 lines)
- packages/ (dir, 5 files, ~973 lines)
- PRIVACY.md (~54 lines)
- README.md (~256 lines)
- README_ZH.md (~237 lines)
- scripts/ (dir, 28 files, ~3139 lines)
- SECURITY.md (~39 lines)
- server/ (dir, 397 files, ~77869 lines)
- shared/ (dir, 52 files, ~8749 lines)
- test/ (dir, 49 files, ~5884 lines)
- THIRD_PARTY_NOTICES.md (~37 lines)
- tui/ (dir, 19 files, ~4829 lines)
- web/ (dir, 60 files, ~10746 lines)

