[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** qwen-audio-agent is a realtime voice runtime that keeps full-duplex conversation flowing in the foreground while delegating tool use and long-running work to a backend Agent (README.md:25-31).
## Key points
- Realtime voice runtime keeps the Agent talking, working, and present, announcing completion with "It's ready." instead of stalling on lookup, tool calls, or tasks (README.md:25-31).
- Full-duplex realtime voice supports natural interruption and sustained multi-turn conversation, with frontend conversation and background tasks running in parallel, progress queries, and cancellation (README.md:74-77).
- Replaceable realtime voice frontends (cloud and local options) integrate independently of the backend and combine as needed (README.md:104-105, README.md:109-117).
- One-click backend-Agent integration reuses the Agent's model configuration, tools, MCP, Skills, and authentication, executing multiple independent tasks asynchronously with continuous status tracking (README.md:76-78).
- Task results automatically return to the current conversation for follow-up questions and modifications; directly answerable questions are answered immediately and only tool/sustained work is delegated (README.md:79-79, README.md:96-98).
- Three client surfaces are offered: WebUI, terminal TUI, and desktop floating orb on macOS / Windows / Linux, plus long-term per-user personalization and cross-session memory (README.md:80-81).
- Custom voice services connect via the Realtime Provider interface without changing Gateway core voice-session or backend-task logic (README.md:119-121).
---
## Agent presence
Conversation should not leave you waiting after a single sentence, nor grind to a halt while the Agent looks something up, calls a tool, or works on a task (README.md:19-21). The design goal is that conversation keeps flowing and the Agent stays present whether chatting, thinking, or working (README.md:23-28).
## Core features
Verbatim feature list (README.md:74-81):
- Full-duplex realtime voice interaction, natural interruption, and sustained multi-turn conversation
- Replaceable realtime voice frontends, with cloud services and local deployment options
- One-click integration with your preferred Agent, reusing its model configuration, tools, MCP, Skills, and authentication
- Frontend conversation and background tasks run in parallel; ask about progress or cancel at any time
- Create multiple independent tasks executed asynchronously by the backend Agent, with continuous status tracking
- Task results automatically return to the current conversation, supporting follow-up questions and modifications
- WebUI, terminal TUI, and desktop floating orb (macOS / Windows / Linux)
- Long-term per-user personalization and cross-session memory
## Architecture
Direct questions are answered immediately; tool or sustained processing is delegated to the backend Agent, while the user always faces the same assistant (README.md:96-98). Full design and module breakdown live in `docs/architecture/deep-dive.md` (README.md:100). Diagrams referenced: `docs/architecture-overview-en.png` and `docs/qwen-audio-agent-three-layer-architecture-en.png` (README.md:85-94).
## Voice frontends
The voice frontend handles realtime conversation (README.md:104-105). Verbatim table (README.md:109-117):

| Voice frontend | Deployment | Setup | Features |
| --- | --- | --- | --- |
| Qwen Audio 3.0 Realtime | Cloud | Bailian API Key | Default frontend |
| GPT-Live / OpenAI Realtime | Cloud | OpenAI API Key | OpenAI GA Realtime dialect |
| Google Gemini Live | Cloud | Google API Key | Native Gemini Live WebSocket |
| Qwen3.5-Omni Realtime | Cloud | Bailian API Key | Video input |
| StepAudio 3 Realtime | Cloud | StepFun API Key | Preview model |
| Hugging Face Speech-to-Speech | Local | Start the service and set its URL | Configurable components |
| MiniCPM-o 4.5 | Local or cloud | Compatible service URL | Backend delegation not yet supported |

Extension point (README.md:119-121):
> To connect another voice service, implement the Realtime Provider interface (`docs/voice-frontends/custom-provider.md`) without changing the Gateway's core voice-session or backend-task logic.
## Backend agents
The backend Agent executes tasks (README.md:104-105). Verbatim table (README.md:125-140):

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

Ratings reflect integration completeness, compatibility, and verification level: five stars = thoroughly tested recommended integration; four stars = active development or not yet fully verified (README.md:142-144). Details in `docs/backends/overview.md` and `docs/configuration.md` (README.md:145-147).
## Installation and quick start
Requires Node.js 22.22.2+ or 24.15.0+, npm 10+ (README.md:151). One-click install (README.md:153-155):
```bash
npm install -g qwen-audio-agent
```
Building from source, GitHub install, and DashScope API Key acquisition are in `docs/getting-started/install.md` (README.md:157-158). Config creation (README.md:162-176):
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
Keys come from the Bailian API Key page; new-user free quota and usage pages apply per official Bailian docs (README.md:178-181). Start commands (README.md:189-194):
```bash
qwenaudio        # Terminal 1: Gateway
qwenaudio tui    # Terminal 2: TUI
```
`qwenaudio webui` is the browser-UI alternative (README.md:189). With a visual-capable Realtime frontend, WebUI can explicitly stream bounded camera frames alongside live audio; see `docs/configuration/frontend.md` (README.md:186-187).
## Desktop app and scenarios
The desktop app provides a persistent floating voice orb with built-in Gateway, automatic idle sleep, local voice wake, and customizable appearance (README.md:203-204). Build commands (README.md:208-212):
```bash
npm run desktop:build:local      # macOS
npm run desktop:build:win        # Windows
npm run desktop:build:linux      # Linux (AppImage + deb, no signing)
```
Visuals, orb behavior, and builds are in `docs/desktop/overview.md` (README.md:214-215). The framework focuses on desktop productivity — talking in realtime while delegating tool use, file work, code changes, and long-running tasks (README.md:219-221). The "foreground conversation + background task" design also expands beyond desktop (README.md:223-225); listed scenarios include Desktop, Smart cockpit, X-Omni, and AI Passport (README.md:227-232).

Note on truncation: the chunk is cut mid-row at chunk line 233 (`| C`) inside the scenarios table, and the `## Macro components` section lists only `top-level-files/` with no further detail, so any scenarios or components beyond that point are not covered here.
**Covers:** README.md (repo overview, features, architecture, frontend/backend tables, install/quick-start, desktop, scenarios)
