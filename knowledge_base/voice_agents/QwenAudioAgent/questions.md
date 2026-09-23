---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: QwenAudio/qwen-audio-agent

### Q1. What is qwen-audio-agent's foreground/background split and how does it keep the agent present?
> [!tip]- Answer
> It is a realtime voice runtime that keeps a full-duplex foreground conversation flowing with natural interruption and multi-turn continuity instead of stalling on lookups, tool calls, or long tasks. Directly answerable questions are answered immediately in the voice frontend, while tool use and sustained work are delegated to a backend Agent running in parallel. The agent announces completion with "It's ready." and results return into the same conversation for follow-ups. See [[wiki/01-overview|Overview]].

### Q2. Which voice frontends are offered and how is a custom voice service added?
> [!tip]- Answer
> Five cloud frontends are offered (Qwen Audio 3.0 Realtime as default, GPT-Live/OpenAI Realtime, Gemini Live, Qwen3.5-Omni with video input, StepAudio 3 preview) alongside local options (Hugging Face speech-to-speech with configurable components, MiniCPM-o 4.5 which lacks backend delegation). The frontend handles realtime conversation independently of the backend and options can be combined as needed. A custom service connects by implementing the Realtime Provider interface without changing Gateway voice-session or backend-task logic. See [[wiki/01-overview|Overview]].

### Q3. How does backend-Agent integration work and what do the star ratings mean?
> [!tip]- Answer
> Integration is mostly one-click via Native ACP (plus a built-in ACP bridge, external ACP adapters, or MSP adapter), reusing the agent's model configuration, tools, MCP, Skills, and authentication for multiple parallel async tasks with status tracking. Listed backends include Qwen Code, OpenCode, OpenClaw, Qoder, Kimi Code, Claude Code, Codex, DeepSeek Harness, Pi, Muse Code, and others, plus a frontend-only None mode. Five stars mark thoroughly tested recommended integrations while four or three stars mark active development or unverified ones. See [[wiki/01-overview|Overview]].

### Q4. What are the install, start, client-surface, and memory basics?
> [!tip]- Answer
> It requires Node.js 22.22.2+ or 24.15.0+ with npm 10+, installed via `npm install -g qwen-audio-agent` and configured with `qwenaudio config` (DashScope key, realtime model default, optional backend protocol). The Gateway starts with `qwenaudio` plus `qwenaudio tui` or `qwenaudio webui`, and clients span WebUI, terminal TUI, and a desktop floating orb on macOS/Windows/Linux. Long-term per-user personalization and cross-session memory persist across sessions. See [[wiki/01-overview|Overview]].

### Q5. What does `.env.example` configure for realtime providers and backend agents?
> [!tip]- Answer
> The 181-line template defaults the foreground to `QWEN_AUDIO_REALTIME_PROVIDER=dashscope` with `AGENT_PROTOCOL=openclaw`, covering DashScope, StepFun, GPT-Live, Google Live, self-hosted speech-to-speech, and MiniCPM-o via provider-specific key/URL/model/voice vars. Realtime model/voice overrides, web-search provider, and foreground tool flags (schedule, web, knowledge, notes, recall) are opt-in env vars. Backend flags include the ACP model override, permission mode, per-agent blocks (Qoder, Qwen Code, MiniMax, Kimi, Hermes, CodeBuddy, Codex, Claude, Pi, Muse), Gateway Tailnet/public-URL exposure, and three default-off memory toggles. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What toolchain pins, lint boundaries, and privacy/security notices guard the repo?
> [!tip]- Answer
> The toolchain pins Node `22.22.2` via `.node-version`/`.nvmrc` with the npm registry set, while ignore files exclude `node_modules/`, `dist/`, `.env`, `/runtime/`, logs, keys, and agent workspaces; the lockfile pins `qwen-audio-agent@1.11.0` across six workspaces. The 145-line eslint config enforces architecture boundaries: shared must not import server, task must not import agent/voice, voice must not import agent, and mobile must stay behind Gateway Client boundaries. Privacy/security state no built-in telemetry, localhost-only Gateway default, private vulnerability reporting, Apache-2.0 licensing, and a time-boxed VitePress dev-only audit exception to 2026-11-30. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Your team wants hands-free voice coding with long async builds on reliable internet: which frontend/backend setup would you recommend and why?
> [!tip]- Answer
> I would recommend the default Qwen Audio 3.0 Realtime cloud frontend with a five-star Native ACP backend such as Qwen Code or OpenCode, run via the Gateway plus TUI or desktop orb. This keeps full-duplex conversation alive while parallel async builds run with progress checks, cancellation, and results returned into the same session for follow-ups. I would avoid frontend-only mode (no background execution) and MiniCPM-o here (no backend delegation yet) since both defeat the parallel voice-plus-build goal. See [[wiki/01-overview|Overview]].
