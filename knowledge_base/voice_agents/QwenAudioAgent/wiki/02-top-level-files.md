[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
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
---
## Configuration template (.env.example)
Full 181-line template; key excerpts verbatim (.env.example:1-7):
```dotenv
# 默认前台使用 Qwen Audio Realtime，此时需要填写 DashScope API Key。
QWEN_AUDIO_REALTIME_PROVIDER=dashscope
# Provider-owned credentials remain supported; only the selected provider uses its key.
# DASHSCOPE_API_KEY=
# STEPFUN_API_KEY=
# DashScope endpoint aliases: QWEN_AUDIO_REALTIME_BASE_URL / QWEN_AUDIO_REALTIME_URL.
# DashScope Audio and Omni voices are configured independently.
```
Provider blocks (verbatim keys, all commented unless selected):
| Provider | Selector | Key / URL / model / voice vars |
| --- | --- | --- |
| DashScope (default) | `QWEN_AUDIO_REALTIME_PROVIDER=dashscope` | `DASHSCOPE_API_KEY`, `QWEN_AUDIO_REALTIME_BASE_URL` / `QWEN_AUDIO_REALTIME_URL` (.env.example:1-7) |
| Web search | `QWEN_AUDIO_WEB_SEARCH_PROVIDER` | `bailian`, `none`, or custom `QWEN_AUDIO_WEB_SEARCH_MCP_URL` + `QWEN_AUDIO_WEB_SEARCH_MCP_TOKEN` + `QWEN_AUDIO_WEB_SEARCH_MCP_TOOL=web_search` (.env.example:9-15) |
| Realtime model/voice | — | `QWEN_AUDIO_REALTIME_MODEL` (supports `qwen3.5-omni-flash-realtime`, `qwen3.5-omni-plus-realtime`, `qwen-audio-3.0-realtime-flash`, default `qwen-audio-3.0-realtime-plus`), `QWEN_AUDIO_REALTIME_VOICE`, `QWEN_OMNI_REALTIME_VOICE` (.env.example:24-32) |
| StepFun | `QWEN_AUDIO_REALTIME_PROVIDER=stepfun` | `STEPFUN_API_KEY`, `STEPFUN_REALTIME_URL=wss://api.stepfun.com/v1/realtime`, `STEPFUN_REALTIME_MODEL=stepaudio-3-realtime-preview`, `STEPFUN_REALTIME_VOICE` (.env.example:34-39) |
| GPT-Live | `QWEN_AUDIO_REALTIME_PROVIDER=gpt-live` | `OPENAI_API_KEY`, `GPT_LIVE_REALTIME_URL=wss://api.openai.com/v1/realtime`, `GPT_LIVE_REALTIME_MODEL=gpt-realtime-2.1`, `GPT_LIVE_REALTIME_VOICE` (.env.example:41-46) |
| Google Live | `QWEN_AUDIO_REALTIME_PROVIDER=google-live` | `GOOGLE_API_KEY`, `GOOGLE_LIVE_REALTIME_URL=wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent`, `GOOGLE_LIVE_REALTIME_MODEL=gemini-3.8-live`, `GOOGLE_LIVE_REALTIME_VOICE` (.env.example:48-53) |
| speech-to-speech / MiniCPM-o | `QWEN_AUDIO_REALTIME_PROVIDER=speech-to-speech` | `SPEECH_TO_SPEECH_REALTIME_URL=ws://127.0.0.1:8765/v1/realtime`, `SPEECH_TO_SPEECH_AUTH_TOKEN`, or `MINICPM_O_REALTIME_URL` / `MINICPM_O_AUTH_TOKEN` (.env.example:55-61) |
Background agent defaults verbatim (.env.example:67):
```dotenv
AGENT_PROTOCOL=openclaw
```
Related backend flags: `QWEN_AUDIO_AGENT_BACKEND_PERMISSION_MODE` (`native` vs `full`), `QWEN_AUDIO_AGENT_BACKEND_AGENT`, `QWEN_AUDIO_AGENT_BACKEND_MODEL`, `OPENCODE_BASE_URL`, `OPENCLAW_BASE_URL`/`OPENCLAW_GATEWAY_TOKEN`/`OPENCLAW_GATEWAY_TOKEN_FILE`/`OPENCLAW_ACP_BIN`, plus per-agent blocks for Qoder, Qwen Code, MiniMax, Kimi, Hermes, CodeBuddy, Codex, Claude, Pi, Muse (`MUSE_CODE_BIN`/`MUSE_CODE_ARGS`/`MUSE_CODE_HOST_WORKSPACE`), and generic `ACP_COMMAND`/`ACP_ARGS`/`ACP_LABEL`/`ACP_WORKSPACE` (.env.example:69-154). Foreground tool visibility flags are `QWEN_AUDIO_SCHEDULE_TOOL_ENABLED`, `QWEN_AUDIO_WEB_TOOLS_ENABLED`, `QWEN_AUDIO_KNOWLEDGE_TOOL_ENABLED`, `QWEN_AUDIO_NOTES_TOOL_ENABLED`, `QWEN_AUDIO_RECALL_TOOL_ENABLED` (.env.example:17-21). Remote/memory flags: `QWEN_AUDIO_GATEWAY_TAILNET`, `QWEN_AUDIO_GATEWAY_PUBLIC_URL`, `QWEN_AUDIO_AGENT_ALLOWED_ORIGINS`, and the three default-off memory toggles `QWEN_AUDIO_PREFERENCE_LEARNING`, `QWEN_AUDIO_SESSION_DIGEST`, `QWEN_AUDIO_DOMAIN_LIBRARY` (.env.example:156-180).
## Ignore files and toolchain pins
`.gitignore` (47 lines) excludes at minimum (.gitignore:1-15):
```
node_modules/
output/playwright/browser-webui-smoke/
web/dist/
dist/
.venv/
.qwen-audio/
__pycache__/
*.py[cod]
.env
.env.*
!.env.example
/runtime/
*.log
.DS_Store
```
It further excludes keys/certs (`*.pem`, `*.p12`, `*.key`, `*.cer`), agent workspaces (`config/opencode-workspace/*`, `config/openclaw-workspace/*` except `AGENTS.md`), `testws/`, generated OpenCode packaging files, `bun.lock`, `sidecars/tsnet/bin|dist`, and VitePress build output `docs/.vitepress/dist|cache|.site` (.gitignore:16-40). `.npmignore` (8 lines) excludes `**/test/`, `**/*.test.mjs`, the generated `config/opencode/` packaging files, and `/runtime/` (.npmignore:1-7). Pins are exact text: `.node-version:1` and `.nvmrc:1` both contain `22.22.2`; `.npmrc:1` contains `registry=https://registry.npmjs.org/`.
## Lint and executable architecture boundaries (eslint.config.mjs)
145 lines; scope and base rules verbatim in part (eslint.config.mjs:1-33):
```js
const sourceFiles = ['**/*.{js,mjs,cjs,jsx}']
// ignores: node_modules, dist, coverage, docs/.vitepress/cache|.site,
// examples/!(lightrag|x-omni), tui/native, mobile android/ios assets
// rules: no-constant-condition, no-dupe-else-if, no-fallthrough,
// no-irregular-whitespace, no-loss-of-precision, no-self-assign,
// no-unreachable, no-unsafe-finally, no-unused-vars (^_ ignore),
// no-useless-catch, no-useless-escape, no-with, valid-typeof
```
Enforced boundaries (each a `no-restricted-imports` error) (eslint.config.mjs:101-135):
| Scope | Forbidden imports | Rationale message |
| --- | --- | --- |
| `mobile/src/**` | `server/**`, `desktop/**` | `Mobile must use public Gateway Client and web presentation boundaries` |
| `shared/**` | `../server/**`, `../../server/**`, `../../../server/**` | `shared modules must not depend on the Gateway server` |
| `server/src/task/**` | `../agent/**`, `../../agent/**`, `../voice/**`, `../../voice/**` | `the task domain must not depend on voice or backend adapters` |
| `server/src/voice/**` | `../agent/**`, `../../agent/**`, `../../../agent/**` | `the realtime frontend must use injected work/backend ports` |
Also: `**/*.cjs` forced to CommonJS; `gateway-client-transport`, `frontend-runtime`, `realtime-session-runtime`, `orchestration/*` get `no-undef: error`; frontend dirs (`web/src`, `mobile/src`, `examples/x-omni/client`) enforce `react-hooks/rules-of-hooks` and `exhaustive-deps` (eslint.config.mjs:34-82).
## Dependency lockfile (package-lock.json)
11638 lines; the chunk is truncated mid-`node_modules` listing (cut at chunk `... (truncated, 404006 more characters)`), so only the root `packages.""` block plus early `node_modules` entries are visible. Root identity verbatim (package-lock.json:1-12):
```json
{"name": "qwen-audio-agent", "version": "1.11.0", "lockfileVersion": 3,
 "workspaces": ["server", "web", "tui", "desktop", "cli", "mobile"],
 "bin": {"qwenaudio": "cli/bin/qwenaudio.mjs"}}
```
Runtime deps: `@a2a-js/sdk 1.1.0`, `@agentclientprotocol/sdk 1.4.0`, `@modelcontextprotocol/sdk 1.30.0`, `@qwen-code/open-computer-use ^0.2.3`, `electron-updater 6.8.9`, `express ^4.22.2`, `qrcode 1.5.4`, `sherpa-onnx 1.13.7`, `tar-stream 3.2.1`, `unbzip2-stream 1.4.3`, `ws ^8.21.3`, `yaml 2.9.0`, `zod ^4.5.4`; dev deps include `concurrently`, `electron-builder 26.16.0`, `eslint 10.9.1`, `eslint-plugin-react-hooks 7.1.1`, `globals 17.12.0`, `playwright ^1.63.0`, `vitepress ^1.6.4`; engines `node ^22.22.2 || ^24.15.0 || >=26.0.0`, `npm >=10` (package-lock.json:13-50). Files beyond the truncation point were cut instead of guessed.
## Privacy, security, and product notices
`PRIVACY.md` (55 lines): orchestration runtime is user-deployed with no built-in telemetry, ad analytics, or auto crash reporting; mic audio/transcripts go to DashScope Qwen Audio Realtime by default (or the configured compatible service); WebUI camera JPEG frames are sent only when the user opens the camera and only while realtime vision is on, never written to history/status/files; background-agent instructions go to the chosen agent via ACP/A2A/custom; MCP/search/web-fetch params go to the respective tool; default memory lives on the Gateway host at `~/.config/qwaudio/` with logs at `~/.config/qwaudio/logs/` (redacted credentials, no audio/transcript/reply/task bodies), and uninstall never deletes data/logs; Gateway listens on localhost only, `--lan` is plaintext LAN-only, cross-network uses Tailscale private Tailnet/HTTPS-serve or a trusted-cert reverse proxy (PRIVACY.md:3-29). `SECURITY.md` (40 lines): fixes go to the latest release first; report via GitHub Security advisories (never public issues with exploit details/keys), include version/repro/impact/mitigation; Gateway localhost-only, LAN needs `--lan`, cross-network needs `--tailnet` or trusted-cert proxy, remote clients need pairing credentials/access tokens, `QWEN_AUDIO_AGENT_AUTH_SECRET` is a signing key not a password; production high/critical vulns block release, with a time-boxed exception to **2026-11-30** for four VitePress 1.6.4 dev-server transitive GHSA IDs (`GHSA-67mh-4wv8-2f99`, `GHSA-4w7w-66w2-5vf9`, `GHSA-v6wh-96g9-6wx3`, `GHSA-fx2h-pf6j-xcff`) maintained by `scripts/audit-dependencies.mjs` (SECURITY.md:4-38). `NOTICE` (6 lines) verbatim (NOTICE:1-6):
```
qwen-audio-agent
Copyright 2026 qwen-audio-agent contributors
This product includes software developed by third-party open-source projects.
See THIRD_PARTY_NOTICES.md for the primary component notices.
```
`THIRD_PARTY_NOTICES.md` (38 lines): project itself is Apache-2.0 with third parties under their own licenses; main table lists Electron, React/React DOM, Express, ws, Vite, react-markdown, remark-gfm, node-qrcode, electron-builder (MIT), A2A JS SDK / ACP TS SDK / Codex ACP adapter / Claude Code ACP adapter (Apache-2.0), MCP TS SDK / Zod / concurrently (MIT); reproducible versions in `package-lock.json`; optional Muse Code SDK 0.1.1 (MIT) downloads only when Muse backend is installed (THIRD_PARTY_NOTICES.md:1-38).
## Chinese README (README_ZH.md)
238 lines; product tagline section `Agent，始终在场` frames a realtime voice runtime that keeps talking/working/present and announces `已经好了。` on completion (README_ZH.md:10-19). News lists v0.9.0 open-source/ACP through v1.0.0 GA, v1.3.0 speech-to-speech, v1.5.0 timers/wake-word/Linux, v1.7.0 orb skins, v1.9.0 task cards/Omni, v1.11.0 embeddable Gateway/Skills/multimodal TUI, v2.0.0 in development (README_ZH.md:20-37). Core-features bullets, reference-architecture images (`docs/architecture-overview.png`, `docs/qwen-audio-agent-three-layer-architecture.png`), 7-row voice-frontend table and 14-row backend-agent table (with `★★★★★`/`★★★★☆` ratings), install (`npm install -g qwen-audio-agent`, Node 22.22.2+/npm 10+), quick-start (`qwenaudio config`, `DASHSCOPE_API_KEY`, `QWEN_AUDIO_REALTIME_MODEL=qwen-audio-3.0-realtime-plus`, `AGENT_PROTOCOL=openclaw`), Gateway+TUI start (`qwenaudio`, `qwenaudio tui`, `qwenaudio webui`), desktop builds (`npm run desktop:build:local|win|linux`), scenario table (桌面办公/智能座舱/X-Omni/AI Passport/客服助手 provided; 具身智能/直播助手 planned), and contribution links (`CONTRIBUTING.md`, `SECURITY.md`, `PRIVACY.md`, `THIRD_PARTY_NOTICES.md`, Apache-2.0 `LICENSE`) (README_ZH.md:58-137).
**Covers:** .env.example, .gitignore, .node-version, .npmignore, .npmrc, .nvmrc, eslint.config.mjs, NOTICE, package-lock.json (truncated), PRIVACY.md, README_ZH.md, SECURITY.md, THIRD_PARTY_NOTICES.md
