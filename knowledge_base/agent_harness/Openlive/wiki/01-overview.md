> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** OpenLive is the open, on-device voice and vision loop (ears, mouth, eyes) around any AI brain you bring, as a local alternative to ElevenLabs Agents, Gemini Live, and OpenAI Realtime.
## Key points
- OpenLive is the open voice and vision layer for AI agents: your AI thinks, OpenLive gives it ears, a mouth, and eyes, running the whole voice loop on your own machine (README.md:13-17).
- The core problem it solves is wiring an AI into real conversation — voice activity detection, end-of-turn detection, streaming STT, model turn, streaming TTS, barge-in, plus camera/screen — without renting that pipeline per minute from a hosted cloud (README.md:41-45).
- It accepts any brain: a model you hold a key for (Anthropic, OpenAI, Google, xAI, DeepSeek, Groq, Ollama fully local, and more) or a coding agent you already use (Claude Code, Codex, Cursor, OpenCode, Hermes) driven locally over Agent Client Protocol JSON-RPC over stdio (README.md:50-57).
- Privacy model: listening, speaking, and watching run on-device (WebGPU); nothing spoken leaves the machine except the final transcript (plus camera/screen frames only if enabled) to whichever brain was picked (README.md:59-62).
- Architecturally it is a cascaded pipeline (speech to text to model to speech), not a full-duplex speech-to-speech model — the trade that makes "any brain, all local, no audio fees" possible (README.md:64-68).
- The on-device voice loop is Silero VAD, Whisper STT, Smart-Turn end-of-turn, and a choice of Kokoro (28 voices, light) or Supertonic (10 voices, 44.1 kHz) TTS, all in-app on WebGPU, with barge-in and custom instructions/speaking speed (README.md:74-89).
- Coding-agent integration is voice-driven per conversation with mid-call model/mode switching over ACP, native session placement (e.g. `~/.claude/projects/…`), voice permission relay, narrated progress, live plan checklist, cost chip, CLI install/auth management, mini mode, markdown transcripts, and AES-256-GCM encrypted keys (README.md:93-114).
---
## What this is
OpenLive is "that pipeline, open and local" for the listening, speaking, and watching around a brain you supply (README.md:47-48). You pay no per-minute audio fees, only the model costs you would pay anyway; with a coding agent as brain there is nothing extra since it runs under your existing login (README.md:50-52, README.md:132-135). No audio ever uploads and API keys are encrypted at rest with only the last four digits shown (README.md:113-114).
## Voice loop (ears / mouth / eyes)
The core loop components, verbatim (README.md:74-89):
- **On-device voice loop.** Silero VAD, Whisper STT, Smart-Turn end-of-turn, Kokoro (28 voices, light) or Supertonic (10 voices, 44.1 kHz) TTS on WebGPU.
- **Speak as yourself.** Settings → Clone Voice records 5 to 30 seconds (seekable listen-back before save); zero-shot cloning via ZipVoice (Apache-2.0) locally, ~208 MB optional install, deletable; profiles preview with any text, rename, export/import.
- **It can see.** Camera or screen frames ride each turn; the `look` tool grabs a hi-res frame on demand; a text-only model can borrow a separate vision model's eyes.
- **Barge-in.** Interrupt any time; it stops mid-word.
- **Your assistant, your way.** Custom instructions in Settings → General apply to every brain; speaking speed and spoken progress narration live there too.
## Agent integrations
Integration features, verbatim in structure (README.md:93-114):
| Capability | Behavior |
|---|---|
| Voice-drive coding agent | Pick Claude Code / Codex / Cursor / OpenCode / Hermes per conversation plus project folder; model, mode (`ask` / `accept edits` / `bypass`), and other options switch mid-call, reported by the agent over ACP |
| Sessions are the agent's own | Call with Claude Code lands in `~/.claude/projects/…` where `claude --resume` finds it; existing CLI sessions appear in OpenLive History; resume from either side |
| Permission relay | Agent command/file-edit asks are spoken; answer by voice ("yes" / "no") or tap |
| Narrated progress | Optional spoken plan steps ("Step 2 of 4 — refactor the store") |
| Live plans and costs | Working plan renders as checklist; context/cost chip tracks session |
| Manage agents | Install, sign in, update, uninstall each agent CLI from Settings → Agents; status self-updates; fallback exact command if terminal cannot open |
| Mini mode | Always-on-top pill keeps listening; menu-bar tray and notifications |
| Transcript | Agent replies as markdown with copy buttons on code blocks; full export to Markdown |
## How it works
Verbatim pipeline diagram (README.md:139-145):
```
mic ─▶ VAD ─▶ streaming STT ─▶ end-of-turn ─▶ your AI ──────────▶ streaming TTS ─▶ speaker
     (Silero)  (Whisper)        (Smart-Turn)  (BYO model, or a     (Kokoro / Supertonic /
                                    ▲          coding agent over    your cloned voice)
                camera / screen ────┘          ACP on local stdio)
                frames (vision)
```
Everything outside "your AI" runs locally in the renderer; the turn goes over a warm local WebSocket to a small agent server that streams a provider reply or drives the coding agent's ACP adapter as a child process, and the app speaks sentence by sentence while the reply streams (README.md:147-150).
## Get started
Verbatim commands (README.md:154-169):
- **Just use it:** installer from the latest release, paste a model key or pick an installed coding agent (Settings → Agents if needed), start a call; voice models download from Hugging Face on first talk (~200 MB with Kokoro, more with Supertonic/bigger Whisper), then cached.
- **Build from source:**
```bash
pnpm install
pnpm desktop:dev      # runs the web + agent servers and opens the app window
```
- Browser dev alternative: `pnpm dev`, then open `localhost:3000`; tests via `pnpm test`.
## Repo layout
Verbatim layout map (README.md:173-184):
```
apps/desktop     Electron shell: spawns the local servers, media perms, window,
                 mini mode, tray + notifications
apps/web         Next.js UI + the on-device voice engine (src/lib/live/*) + /api routes
                 (agents install/auth, history discovery, settings)
services/agent   Hono + ws: the /live WebSocket, the ACP agent driver (acp-agent.ts,
                 supervisor.ts), voice cloning (voice/*), the built-in provider turn loop
packages/shared  the agent registry (single source of agent identity), wire protocol,
                 shared types
packages/harness provider-neutral model adapters, live model listing, cost/effort
packages/db      JSON-file store: encrypted keys, settings, conversations
```
Cross-reference: the ACP driver, voice loop, resume, and delegate/worker tool flow are detailed in `docs/ARCHITECTURE.md` (README.md:186-187). Contributions start at `CONTRIBUTING.md`; license is MIT (README.md:189-197).
**Covers:** README.md (project tagline, What this is, Features, Screenshots, Why on-device voice matters, How it works, Get started, Repo layout, Contributing, License); chunk notes no truncated files.
