# Technical Analysis: QwenAudio/qwen-audio-agent

**Repository:** https://github.com/QwenAudio/qwen-audio-agent
**Version analyzed:** 1.11.0
**Date:** 2026-09-22
**Wiki:** [[index]]

Scope note: the wiki at read time contains two component pages covering `README.md` and top-level config/toolchain files. Statements below are restricted to what those pages attest; server internals (`server/src/**`, Gateway session/task state machines, ACP bridge code) are not covered by the wiki and are not described beyond the README-level contract.

## 1. Overview / What Problem It Solves

Problem space: realtime voice assistants stall when the agent looks something up, calls a tool, or runs a sustained task — the user waits mid-conversation or the dialogue halts (README.md:19-21). Long-running tool/file/code work and full-duplex interruption, progress queries, and cancellation do not fit a single blocking turn.

What the repo does: `qwen-audio-agent` is a realtime voice runtime split into a foreground voice frontend (realtime conversation, interruption, multi-turn dialogue) and a background Agent that executes tool use and sustained tasks asynchronously (README.md:25-31, README.md:74-81). Directly answerable questions are answered immediately in the foreground; only tool or sustained work is delegated to the backend, and task results return into the current conversation for follow-up (README.md:96-98, README.md:79). The frontend and background tasks run in parallel with status tracking, progress queries, and cancellation (README.md:76-78). Primary user: a desktop operator who talks continuously while delegating file work, code changes, lookups, and long-running tasks (README.md:219-221).

## 2. High-Level Architecture

```
User audio/video ──► Voice frontend (realtime provider) ──► Gateway core
                          │                                      │
                          │ immediate answer                     ▼
                          │                                Backend Agent (ACP/adapter)
                          │                                      │ async task status
                          ▼                                      ▼
                   Conversation stream ◄── task result ── Task domain
                          │
                          ▼
              Clients: WebUI │ TUI │ desktop orb │ mobile (via Gateway Client)
```

Data flow (README-level contract, README.md:96-98, README.md:76-81):

1. Audio (and bounded camera frames on visual-capable frontends, README.md:186-187) enters the configured realtime voice frontend, which owns the live conversation (README.md:104-105).
2. The Gateway routes each turn: directly answerable content is answered in the foreground; tool-dependent or sustained work is dispatched as one or more independent backend tasks (README.md:96-98, README.md:76-78).
3. The backend Agent executes tasks asynchronously via its own model configuration, tools, MCP, Skills, and authentication (README.md:76-78), with continuous status tracking (README.md:76-78).
4. The user keeps talking to the same assistant in parallel, can ask about progress, or cancel at any time (README.md:74-77).
5. On completion the foreground announces readiness ("It's ready." / `已经好了。`, README.md:25-31, README_ZH.md:10-19) and the task result re-enters the current conversation for follow-up questions and modifications (README.md:79).

Persistent state: default memory lives on the Gateway host at `~/.config/qwaudio/`, logs at `~/.config/qwaudio/logs/` with redacted credentials and no audio/transcript/reply/task bodies (PRIVACY.md:3-29). Gateway listens on localhost only by default; `--lan` is plaintext LAN, cross-network requires Tailscale Tailnet/HTTPS-serve or a trusted-cert reverse proxy (PRIVACY.md:3-29, SECURITY.md:4-38). Uninstall never deletes data/logs (PRIVACY.md:3-29).

## 3. The Foreground–Background Split

Representation: the central abstraction is a two-plane runtime. The foreground plane is a replaceable realtime voice frontend plus three client surfaces; the background plane is a pluggable coding-agent backend reached over ACP or a bridge/adapter. The Gateway core (voice-session + backend-task logic) sits between them and is explicitly decoupled from any single provider: a custom voice service connects via the Realtime Provider interface "without changing the Gateway's core voice-session or backend-task logic" (README.md:119-121).

Named kinds/types attested in the wiki:

- Voice frontends (README.md:109-117): `Qwen Audio 3.0 Realtime` (cloud, default), `GPT-Live / OpenAI Realtime` (cloud), `Google Gemini Live` (cloud), `Qwen3.5-Omni Realtime` (cloud, video input), `StepAudio 3 Realtime` (cloud, preview), `Hugging Face Speech-to-Speech` (local), `MiniCPM-o 4.5` (local or cloud, backend delegation not yet supported).
- Backend agents (README.md:125-140): `None` (frontend-only), `Qwen Code` / `OpenCode` / `OpenClaw` / `Qoder` / `MiniMax Code` / `Kimi Code` / `Hermes` / `CodeBuddy` (native ACP), `Codex` / `Claude Code` / `Pi` (external ACP adapter), `DeepSeek Harness` (native ACP), `Muse Code` (native MSP adapter).
- Client surfaces (README.md:80-81): `WebUI`, terminal `TUI`, desktop floating orb (macOS/Windows/Linux).
- Provider selectors (`.env.example:1-7`, `.env.example:34-61`): `dashscope`, `stepfun`, `gpt-live`, `google-live`, `speech-to-speech` (plus `MINICPM_O_*` overrides).

Key query (verbatim, README.md:119-121):

```md
> To connect another voice service, implement the Realtime Provider interface (`docs/voice-frontends/custom-provider.md`) without changing the Gateway's core voice-session or backend-task logic.
```

## 4. LLM / External Service Integration

The repo calls external realtime/model services; there is no self-contained LLM. The foreground always requires exactly one selected realtime provider; the backend requires credentials only when a backend agent is configured (frontend-only mode needs no backend config, README.md:125-140).

| Provider / service | Required vs optional | Env vars (`.env.example`) |
| --- | --- | --- |
| DashScope Qwen Audio Realtime (default frontend) | Required when `QWEN_AUDIO_REALTIME_PROVIDER=dashscope` (default) | `DASHSCOPE_API_KEY`, `QWEN_AUDIO_REALTIME_BASE_URL` / `QWEN_AUDIO_REALTIME_URL`, `QWEN_AUDIO_REALTIME_MODEL` (default `qwen-audio-3.0-realtime-plus`), `QWEN_AUDIO_REALTIME_VOICE`, `QWEN_OMNI_REALTIME_VOICE` (`.env.example:1-7`, `.env.example:24-32`) |
| StepFun StepAudio 3 Realtime | Required when provider `stepfun` | `STEPFUN_API_KEY`, `STEPFUN_REALTIME_URL`, `STEPFUN_REALTIME_MODEL`, `STEPFUN_REALTIME_VOICE` (`.env.example:34-39`) |
| OpenAI Realtime (GPT-Live) | Required when provider `gpt-live` | `OPENAI_API_KEY`, `GPT_LIVE_REALTIME_URL`, `GPT_LIVE_REALTIME_MODEL`, `GPT_LIVE_REALTIME_VOICE` (`.env.example:41-46`) |
| Google Gemini Live | Required when provider `google-live` | `GOOGLE_API_KEY`, `GOOGLE_LIVE_REALTIME_URL`, `GOOGLE_LIVE_REALTIME_MODEL`, `GOOGLE_LIVE_REALTIME_VOICE` (`.env.example:48-53`) |
| Self-hosted speech-to-speech / MiniCPM-o | Required when provider `speech-to-speech` | `SPEECH_TO_SPEECH_REALTIME_URL`, `SPEECH_TO_SPEECH_AUTH_TOKEN`, or `MINICPM_O_REALTIME_URL` / `MINICPM_O_AUTH_TOKEN` (`.env.example:55-61`) |
| Backend agent (OpenClaw default; Qwen Code, OpenCode, Qoder, Kimi, Hermes, CodeBuddy, MiniMax, Codex, Claude, DeepSeek, Pi, Muse) | Optional; omit for frontend-only mode | `AGENT_PROTOCOL` (default `openclaw`, `.env.example:67`), `QWEN_AUDIO_AGENT_BACKEND_MODEL` (e.g. `qwen3.7-max`; empty reuses Agent config, README.md:162-176), `QWEN_AUDIO_AGENT_BACKEND_PERMISSION_MODE`, `OPENCODE_BASE_URL`, `OPENCLAW_BASE_URL`/`OPENCLAW_GATEWAY_TOKEN`, per-agent blocks plus generic `ACP_COMMAND`/`ACP_ARGS`/`ACP_LABEL`/`ACP_WORKSPACE` (`.env.example:69-154`) |
| Web search (foreground tool) | Optional | `QWEN_AUDIO_WEB_SEARCH_PROVIDER` (`bailian`/`none`/custom), `QWEN_AUDIO_WEB_SEARCH_MCP_URL` + `QWEN_AUDIO_WEB_SEARCH_MCP_TOKEN` + `QWEN_AUDIO_WEB_SEARCH_MCP_TOOL` (`.env.example:9-15`) |

Mic audio/transcripts go to the configured realtime service (DashScope by default); camera JPEG frames are sent only while the user has the camera open and realtime vision is on; backend instructions go to the chosen agent via ACP/A2A/custom; MCP/search/web-fetch params go to the respective tool (PRIVACY.md:3-29).

## 5. The Foreground Conversation + Background Delegation Pipeline

Primary workflow as attested at README/`.env.example` level (no per-function code pages exist in the wiki; steps cite the contract lines, not implementation functions):

1. Configure (`README.md:162-176`, `.env.example:1-7`, `.env.example:67`): run `qwenaudio config`, set `DASHSCOPE_API_KEY` (or the selected provider key), optionally `QWEN_AUDIO_REALTIME_MODEL` and `AGENT_PROTOCOL`/`QWEN_AUDIO_AGENT_BACKEND_MODEL`.
2. Start Gateway + client (`README.md:189-194`): `qwenaudio` in one terminal, `qwenaudio tui` (or `qwenaudio webui`) in another; desktop orb embeds the Gateway (README.md:203-204).
3. Converse in the foreground (README.md:74-77): full-duplex audio with interruption over the selected realtime frontend (README.md:104-105, README.md:109-117).
4. Route each turn (README.md:96-98): answer immediately if directly answerable; otherwise dispatch one or more independent backend tasks reusing the Agent's model/tools/MCP/Skills/auth (README.md:76-78).
5. Track in parallel (README.md:76-78): monitor status, ask about progress, or cancel while the conversation continues.
6. Reintegrate (README.md:79): completed results return to the current conversation; the assistant announces completion and accepts follow-ups/modifications.

## 6. Key Files

| File | Lines | What It Does |
| --- | --- | --- |
| `README.md` | attested to ~232 (truncated mid-row at 233) | Product contract: presence goal, feature list, architecture pointer, frontend/backend tables, install/quick-start, desktop, scenarios |
| `.env.example` | 181 | Full Gateway/frontend/backend config template: provider selectors, model/voice overrides, backend ACP blocks, foreground tool flags, Gateway exposure, memory toggles |
| `package-lock.json` | 11638 (truncated in chunk) | Locks `qwen-audio-agent@1.11.0`, six workspaces (`server`, `web`, `tui`, `desktop`, `cli`, `mobile`), `qwenaudio` bin, engines and runtime/dev deps |
| `eslint.config.mjs` | 145 | Lint scope plus executable layer boundaries (`shared`/`task`/`voice`/`mobile` import restrictions) |
| `README_ZH.md` | 238 | Chinese product entrypoint: tagline, version news, feature/frontend/backend tables, install, builds, scenarios, contribution links |
| `PRIVACY.md` | 55 | Data-flow privacy contract: no telemetry, where audio/transcripts/frames/instructions go, local memory/log paths, network posture |
| `SECURITY.md` | 40 | Vulnerability reporting, localhost/LAN/Tailnet posture, auth-secret handling, release-blocking policy with VitePress exception to 2026-11-30 |
| `THIRD_PARTY_NOTICES.md` | 38 | License table (Apache-2.0 product; MIT/Apache-2.0 third parties) and reproducible-version pointer |
| `NOTICE` | 6 | Copyright and third-party notice pointer |
| `.gitignore` | 47 | Excludes `node_modules/`, `dist/`, `.env`, `/runtime/`, logs, keys/certs, agent workspaces, docs build output |
| `.npmignore` | 8 | Excludes tests, generated `config/opencode/` packaging files, `/runtime/` from the published package |
| `.node-version` / `.nvmrc` / `.npmrc` | 1 each | Pins Node `22.22.2`; pins registry to `https://registry.npmjs.org/` |

## 7. Dependencies

Exact constraint strings from the root manifest block as reported by the wiki (package-lock.json:13-50). Required runtime first, then dev/toolchain.

| Package | Version constraint | Purpose |
| --- | --- | --- |
| `express` | `^4.22.2` | Gateway HTTP server |
| `ws` | `^8.21.3` | Realtime WebSocket transport |
| `yaml` | `2.9.0` | Config parsing |
| `zod` | `^4.5.4` | Schema validation |
| `@modelcontextprotocol/sdk` | `1.30.0` | MCP tool integration |
| `@agentclientprotocol/sdk` | `1.4.0` | Native ACP backend-agent integration |
| `@a2a-js/sdk` | `1.1.0` | A2A backend-agent path |
| `@qwen-code/open-computer-use` | `^0.2.3` | Open computer-use capability |
| `qrcode` | `1.5.4` | Pairing/terminal QR (client auth) |
| `sherpa-onnx` | `1.13.7` | Local speech (e.g. wake-word) runtime |
| `tar-stream` | `3.2.1` | Packaging/streaming |
| `unbzip2-stream` | `1.4.3` | Packaging/streaming |
| `electron-updater` | `6.8.9` | Desktop auto-update |
| `concurrently` | dev (versioned in lockfile) | Multi-workspace dev orchestration |
| `electron-builder` | `26.16.0` | Desktop packaging (macOS/Windows/Linux) |
| `eslint` | `10.9.1` | Lint with architecture boundaries |
| `eslint-plugin-react-hooks` | `7.1.1` | Frontend hooks rules |
| `globals` | `17.12.0` | Lint globals |
| `playwright` | `^1.63.0` | WebUI smoke/e2e tests |
| `vitepress` | `^1.6.4` | Docs site (dev-only; has time-boxed audit exception, SECURITY.md:4-38) |

Engines: `node ^22.22.2 || ^24.15.0 || >=26.0.0`, `npm >=10` (package-lock.json:13-50); default toolchain pin Node `22.22.2` (`.node-version:1`, `.nvmrc:1`).

## 8. CLI / Usage Surface

Entry points: global install exposes the `qwenaudio` bin (`cli/bin/qwenaudio.mjs`, package-lock.json:1-12); workspaces are `server`, `web`, `tui`, `desktop`, `cli`, `mobile` (package-lock.json:1-12).

| Command | Effect |
| --- | --- |
| `npm install -g qwen-audio-agent` | One-click install (README.md:153-155) |
| `qwenaudio config` | Create/interactive config (README.md:162-176) |
| `qwenaudio` | Start Gateway (Terminal 1, README.md:189-194) |
| `qwenaudio tui` | Start terminal TUI client (Terminal 2, README.md:189-194) |
| `qwenaudio webui` | Browser-UI alternative (README.md:189) |
| `npm run desktop:build:local` | Build desktop orb, macOS (README.md:208-212) |
| `npm run desktop:build:win` | Build desktop orb, Windows (README.md:208-212) |
| `npm run desktop:build:linux` | Build desktop orb, Linux AppImage + deb, no signing (README.md:208-212) |

Env-var surface (`.env.example`, all opt-in except the selected provider key):

| Variable group | Key examples | Default / note |
| --- | --- | --- |
| Provider select + credentials | `QWEN_AUDIO_REALTIME_PROVIDER`, `DASHSCOPE_API_KEY`, `STEPFUN_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `SPEECH_TO_SPEECH_AUTH_TOKEN` | `dashscope` default (`.env.example:1-7`); only the selected provider uses its key |
| Model/voice overrides | `QWEN_AUDIO_REALTIME_MODEL`, `QWEN_AUDIO_REALTIME_VOICE`, `QWEN_OMNI_REALTIME_VOICE` | Default `qwen-audio-3.0-realtime-plus` (`.env.example:24-32`) |
| Backend agent | `AGENT_PROTOCOL`, `QWEN_AUDIO_AGENT_BACKEND_MODEL`, `QWEN_AUDIO_AGENT_BACKEND_PERMISSION_MODE`, `OPENCODE_BASE_URL`, `OPENCLAW_*`, `MUSE_CODE_BIN`/`MUSE_CODE_ARGS`, `ACP_COMMAND`/`ACP_ARGS` | `AGENT_PROTOCOL=openclaw` (`.env.example:67`); empty backend model reuses Agent config (README.md:162-176) |
| Foreground tools | `QWEN_AUDIO_SCHEDULE_TOOL_ENABLED`, `QWEN_AUDIO_WEB_TOOLS_ENABLED`, `QWEN_AUDIO_KNOWLEDGE_TOOL_ENABLED`, `QWEN_AUDIO_NOTES_TOOL_ENABLED`, `QWEN_AUDIO_RECALL_TOOL_ENABLED` | Opt-in flags (`.env.example:17-21`) |
| Gateway exposure | `QWEN_AUDIO_GATEWAY_TAILNET`, `QWEN_AUDIO_GATEWAY_PUBLIC_URL`, `QWEN_AUDIO_AGENT_ALLOWED_ORIGINS` | Opt-in (`.env.example:156-180`) |
| Memory/library | `QWEN_AUDIO_PREFERENCE_LEARNING`, `QWEN_AUDIO_SESSION_DIGEST`, `QWEN_AUDIO_DOMAIN_LIBRARY` | All default-off (`.env.example:156-180`) |

Canonical minimal config (README.md:162-176):

```dotenv
DASHSCOPE_API_KEY=your-key
# Voice frontend model: optional, defaults to Qwen Audio 3.0 Realtime Plus
QWEN_AUDIO_REALTIME_MODEL=qwen-audio-3.0-realtime-plus
# Backend Agent: optional, leave empty or set to none for frontend-only mode
AGENT_PROTOCOL=openclaw
# Backend model: optional; explicit values use standard ACP, empty reuses Agent config
QWEN_AUDIO_AGENT_BACKEND_MODEL=qwen3.7-max
```

## 9. Extensibility Points

- New realtime voice service: implement the Realtime Provider interface per `docs/voice-frontends/custom-provider.md`; Gateway voice-session and backend-task logic are unchanged (README.md:119-121).
- New backend agent: add a native ACP integration, an external ACP adapter (pattern used by Codex/Claude Code/Pi), or an MSP-style adapter (pattern used by Muse Code), wired through `AGENT_PROTOCOL` plus the per-agent block or generic `ACP_COMMAND`/`ACP_ARGS`/`ACP_LABEL`/`ACP_WORKSPACE` (README.md:125-140, `.env.example:69-154`).
- Foreground tools and retrieval: toggle/extend via `QWEN_AUDIO_SCHEDULE_TOOL_ENABLED`, `QWEN_AUDIO_WEB_TOOLS_ENABLED`, `QWEN_AUDIO_KNOWLEDGE_TOOL_ENABLED`, `QWEN_AUDIO_NOTES_TOOL_ENABLED`, `QWEN_AUDIO_RECALL_TOOL_ENABLED`, and the web-search triplet `QWEN_AUDIO_WEB_SEARCH_MCP_URL`/`TOKEN`/`TOOL` (`.env.example:17-21`, `.env.example:9-15`).
- Clients and form factors: WebUI, TUI, desktop orb, and scenario extensions (Desktop, Smart cockpit, X-Omni, AI Passport per README.md:227-232) sit behind Gateway client boundaries that `mobile` must respect (`mobile must use public Gateway Client`, eslint.config.mjs:101-135).
- Layering constraints (enforced by lint, eslint.config.mjs:101-135): `shared` must not import `server`; `server/src/task` must not import `agent`/`voice`; `server/src/voice` must not import `agent` (use injected work/backend ports). Any extension crossing these layers should go through the Gateway client/ports, not direct imports.

## 10. Limitations and Gotchas

- **MiniCPM-o 4.5 does not support backend delegation.** It is usable as a local/cloud voice frontend, but tool/sustained backend work is unavailable on it (README.md:109-117).
- **Frontend-only mode (`AGENT_PROTOCOL=none`/empty) has no backend tools.** Delegation, async tasks, and status tracking require a configured backend agent (README.md:125-140, README.md:162-176).
- **Backend maturity varies by the star rating.** Five-star integrations are thoroughly tested; four-star entries (MiniMax, Hermes, CodeBuddy, Codex, Claude, DeepSeek, Muse) are under active development or not fully verified (README.md:142-144).
- **Localhost-only by default; remote access needs explicit setup.** `--lan` is plaintext LAN-only; cross-network requires Tailnet/HTTPS-serve or a trusted-cert reverse proxy plus pairing credentials/tokens (PRIVACY.md:3-29, SECURITY.md:4-38).
- **Camera frames leave the host while vision is on.** WebUI JPEG frames are sent only when the user opens the camera and realtime vision is on, and are never written to history/status/files — but they are transmitted (PRIVACY.md:3-29).
- **Wiki/contract coverage is partial.** The available wiki pages attest README-level behavior and top-level files only; `docs/architecture/deep-dive.md`, per-provider/backend docs, and all `server/*` implementation details are referenced but not covered, so capacity, retry, and failure-mode behavior cannot be stated from the wiki.

## 11. How It Compares to Alternatives

The wiki names no competing projects directly (backend-agent table entries are integrations, not alternatives). Positioning against known realtime voice-agent runtimes:

- **Pipecat (Daily):** open-source framework for building realtime voice/multimodal agents with pluggable transports and pipeline components. `qwen-audio-agent` is narrower: a fixed foreground/background runtime with prebuilt Gateway + TUI/WebUI/orb clients rather than a component toolkit.
- **LiveKit Agents:** programmable realtime voice/video agent framework over LiveKit WebRTC with worker-based dispatch. `qwen-audio-agent` instead centers on delegating to existing coding agents over ACP/bridges and reusing their tools/MCP/Skills/auth.
- **OpenAI Realtime API reference agents / console demos:** single-provider full-duplex starters on the OpenAI Realtime dialect. `qwen-audio-agent` abstracts the frontend behind a Realtime Provider interface supporting Qwen/StepFun/OpenAI/Google/local options plus video input on Omni.
- **Mycroft / OVOS / generic local voice assistants:** local-first intent/skill voice stacks. `qwen-audio-agent` keeps the realtime frontend possibly local (speech-to-speech, MiniCPM-o) but delegates heavy work to a full coding agent with cross-session memory and parallel background tasks.

Positioning sentence: `qwen-audio-agent` occupies the "voice shell over your coding agent" niche — foreground realtime conversation decoupled from background ACP-agent execution — rather than competing as a general voice-agent SDK or a single-provider demo.

## Appendix: Selected Code Snippets

1. Global install and start (`README.md:153-155`, `README.md:189-194`):

```bash
npm install -g qwen-audio-agent
```

```bash
qwenaudio        # Terminal 1: Gateway
qwenaudio tui    # Terminal 2: TUI
```

2. Minimal backend/frontend config (`README.md:162-176`):

```dotenv
DASHSCOPE_API_KEY=your-key
# Voice frontend model: optional, defaults to Qwen Audio 3.0 Realtime Plus
QWEN_AUDIO_REALTIME_MODEL=qwen-audio-3.0-realtime-plus
# Backend Agent: optional, leave empty or set to none for frontend-only mode
AGENT_PROTOCOL=openclaw
# Backend model: optional; explicit values use standard ACP, empty reuses Agent config
QWEN_AUDIO_AGENT_BACKEND_MODEL=qwen3.7-max
```

3. Root package identity (`package-lock.json:1-12`):

```json
{"name": "qwen-audio-agent", "version": "1.11.0", "lockfileVersion": 3,
 "workspaces": ["server", "web", "tui", "desktop", "cli", "mobile"],
 "bin": {"qwenaudio": "cli/bin/qwenaudio.mjs"}}
```

4. Executable layer boundaries (`eslint.config.mjs:101-135`, paraphrased scope table; rationale strings verbatim): `shared/**` must not import `server/**` ("shared modules must not depend on the Gateway server"); `server/src/task/**` must not import `agent/**` or `voice/**` ("the task domain must not depend on voice or backend adapters"); `server/src/voice/**` must not import `agent/**` ("the realtime frontend must use injected work/backend ports"); `mobile/src/**` must not import `server/**` or `desktop/**` ("Mobile must use public Gateway Client and web presentation boundaries").
