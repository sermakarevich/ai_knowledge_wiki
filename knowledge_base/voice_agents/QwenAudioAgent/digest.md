> [[index|Wiki]] | [[summary|Summary]]
# QwenAudio/qwen-audio-agent — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** qwen-audio-agent is a realtime voice runtime that keeps full-duplex conversation flowing in the foreground while delegating tool use and long-running work to a backend Agent (README.md:25-31).
## Key points
- Realtime voice runtime keeps the Agent talking, working, and present, announcing completion with "It's ready." instead of stalling on lookup, tool calls, or tasks (README.md:25-31).
- Full-duplex realtime voice supports natural interruption and sustained multi-turn conversation, with frontend conversation and background tasks running in parallel, progress queries, and cancellation (README.md:74-77).
- Replaceable realtime voice frontends (cloud and local options) integrate independently of the backend and combine as needed (README.md:104-105, README.md:109-117).
- One-click backend-Agent integration reuses the Agent's model configuration, tools, MCP, Skills, and authentication, executing multiple independent tasks asynchronously with continuous status tracking (README.md:76-78).
- Task results automatically return to the current conversation for follow-up questions and modifications; directly answerable questions are answered immediately and only tool/sustained work is delegated (README.md:79-79, README.md:96-98).
- Three client surfaces are offered: WebUI, terminal TUI, and desktop floating orb on macOS / Windows / Linux, plus long-term per-user personalization and cross-session memory (README.md:80-81).
- Custom voice services connect via the Realtime Provider interface without changing Gateway core voice-session or backend-task logic (README.md:119-121).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** Top-level files define the repo's runtime configuration template, toolchain pins, lint-enforced architecture boundaries, dependency lockfile, and privacy/security/product notices plus the Chinese README.
## Key points
- `.env.example` (181 lines) is the full Gateway/frontend/backend configuration template, defaulting the foreground to `QWEN_AUDIO_REALTIME_PROVIDER=dashscope` with `AGENT_PROTOCOL=openclaw` for the background agent (.env.example:1-2, .env.example:67).
- Realtime provider selection covers DashScope, StepFun, GPT-Live, Google Live, self-hosted speech-to-speech, and MiniCPM-o via provider-specific URL/model/voice keys, with DashScope endpoint aliases and independent Audio/Omni voices (.env.example:5-7, .env.example:24-61).
- Optional foreground tools, realtime model/voice overrides, backend ACP model override, permission mode, Gateway Tailnet/public-URL exposure, and three foreground memory/library toggles are all opt-in env flags (.env.example:17-21, .env.example:24-32, .env.example:72-74, .env.example:156-180).
- Toolchain is pinned to Node `22.22.2` via `.node-version`/`.nvmrc` with `registry=https://registry.npmjs.org/`, while `.gitignore`/`.npmignore` exclude `node_modules/`, `dist/`, `.env`, `/runtime/`, logs, keys, agent workspaces, and docs build output (.node-version:1, .nvmrc:1, .npmrc:1, .gitignore:1-15, .npmignore:1-7).
- `eslint.config.mjs` (145 lines) lints `**/*.{js,mjs,cjs,jsx}` with strict correctness rules plus executable architecture boundaries: shared must not import server, task must not import agent/voice, voice must not import agent, mobile must stay behind Gateway Client boundaries (eslint.config.mjs:1-33, eslint.config.mjs:101-135).
- `package-lock.json` (11638 lines, truncated in chunk) locks `qwen-audio-agent@1.11.0` with `server`, `web`, `tui`, `desktop`, `cli`, `mobile` workspaces, `qwenaudio` bin, Node `^22.22.2 || ^24.15.0 || >=26.0.0` engines, and express/ws/yaml/zod/MCP/ACP/A2A runtime deps (package-lock.json:1-50).
- `PRIVACY.md`, `SECURITY.md`, `NOTICE`, and `THIRD_PARTY_NOTICES.md` state no built-in telemetry, localhost-only Gateway default, private vulnerability reporting, Apache-2.0 product license, and third-party license tables with a time-boxed VitePress dev-only audit exception (PRIVACY.md:3-5, SECURITY.md:8-22, NOTICE:1-6, THIRD_PARTY_NOTICES.md:3-10).
- `README_ZH.md` (238 lines) is the Chinese product entrypoint documenting full-duplex voice, replaceable frontends, backend agents, install/quick-start, desktop builds, and scenario extensions (README_ZH.md:1-12, README_ZH.md:58-82).
## The system in five moves
1. Stay present in voice: keep a full-duplex foreground conversation flowing with interruption and multi-turn continuity instead of stalling on work.
2. Split foreground from background: answer direct questions immediately in the voice frontend while delegating tool use and sustained tasks to a backend Agent running in parallel.
3. Plug in either side independently: choose among replaceable realtime voice frontends and one-click backend-Agent integrations via provider interfaces without changing Gateway core logic.
4. Return work to conversation: track async tasks with progress/cancel, then bring results back into the same session for follow-ups across WebUI, TUI, and desktop orb with memory.
5. Pin it down at the repo root: encode the whole split in configuration template, toolchain pins, lint-enforced module boundaries, locked workspaces, and privacy/security notices.
