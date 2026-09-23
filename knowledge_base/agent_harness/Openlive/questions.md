---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: katipally/openlive

### Q1. In one sentence, what is OpenLive, and what hard pipeline problem does it solve?

> [!tip]- Answer
> OpenLive is the open, on-device voice and vision loop — ears, mouth, and eyes — around any AI brain you bring, as a local alternative to ElevenLabs Agents, Gemini Live, and OpenAI Realtime. It solves wiring an AI into real conversation (VAD, end-of-turn detection, streaming STT, model turn, streaming TTS, barge-in, plus camera/screen) without renting that pipeline per minute from a hosted cloud. See [[wiki/01-overview|Overview]].

### Q2. What are the stages of the on-device voice loop, and which models fill each slot?

> [!tip]- Answer
> The loop runs Silero VAD, Whisper streaming STT, Smart-Turn end-of-turn detection, and a choice of Kokoro (28 voices, light) or Supertonic (10 voices, 44.1 kHz) TTS, all in-app on WebGPU. Barge-in lets the user interrupt mid-word, and the turn flows mic → VAD → STT → end-of-turn → brain → streaming TTS → speaker. Everything outside the brain runs locally, so no audio ever uploads. See [[wiki/01-overview|Overview]].

### Q3. Why is OpenLive a cascaded pipeline rather than a full-duplex speech-to-speech model, and what does that trade buy?

> [!tip]- Answer
> The cascade (speech to text to model to speech) is what makes "any brain, all local, no audio fees" possible, since any text-capable model or coding agent can plug in. The cost is giving up native full-duplex speech-to-speech behavior with its lower turn latency. Only the final transcript (plus camera/screen frames if enabled) leaves the machine for the chosen brain. See [[wiki/01-overview|Overview]].

### Q4. How does bring-your-own-brain work, including voice-driven coding agents?

> [!tip]- Answer
> Any keyed model works (Anthropic, OpenAI, Google, xAI, DeepSeek, Groq, fully local Ollama, and more), or a coding agent — Claude Code, Codex, Cursor, OpenCode, Hermes — driven locally over Agent Client Protocol JSON-RPC over stdio. A call with Claude Code lands in its native session location (e.g. `~/.claude/projects/…`) with voice permission relay, narrated progress, a live plan checklist, and mid-call model/mode switching. API keys are AES-256-GCM encrypted at rest with only the last four digits shown. See [[wiki/01-overview|Overview]].

### Q5. How is the pnpm monorepo laid out, and why is exactly one copy of `@huggingface/transformers` forced?

> [!tip]- Answer
> The root declares `packages/*`, `apps/*`, and `services/*` workspaces (`apps/desktop` Electron shell, `apps/web` Next.js UI plus on-device voice engine, `services/agent` Hono/ws live server and ACP driver, `packages/shared`, `packages/harness`, `packages/db`). The `overrides` entry pins `@huggingface/transformers` to 4.2.0 because kokoro-js pulls 3.8.1 and two copies mean two clashing onnxruntime envs that segfault. Native-module builds are allow-listed while `electron-winstaller` is disabled since the project ships NSIS, not Squirrel.Windows. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What shared strictness, test, ignore, and release conventions hold the repo together?

> [!tip]- Answer
> All packages share one strict base (`ES2022` target, `Bundler` resolution, `strict` plus `noUncheckedIndexedAccess`), and one root vitest runner executes every colocated `*.test.ts` file under `node` environment. Generated, secret, and large artifacts (`node_modules`, `.next`, `dist`, `.env`, `*.log`, `release/`, `*.mp4`, vendored `apps/web/public/vad/`) are never committed. Releases are a single tag (`git tag v0.2.0 && git push origin v0.2.0`) with CI typechecking every push/PR and building signed macOS, Windows, and Linux installers from the tag. See [[wiki/02-top-level-files|Top-level files]].

### Q7. (Evaluation) Should you recommend OpenLive as the voice layer for a local-first coding-agent setup, and what is the main caveat?

> [!tip]- Answer
> Yes when the priorities are privacy, zero per-minute audio fees, and driving an existing coding-agent login by voice with vision attached, since the whole loop runs on-device and only transcripts leave the machine. The main caveat is the cascaded turn-based design, so expect higher turn latency than true full-duplex speech-to-speech and verify barge-in behavior against the use case before committing. The monorepo hygiene (single transformers pin, strict TS, tag-driven releases) further suggests a maintainable base to build on. See [[wiki/01-overview|Overview]].
