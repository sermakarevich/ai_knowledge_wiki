> [[index|Wiki]] | [[summary|Summary]]
# katipally/openlive — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** OpenLive is the open, on-device voice and vision loop (ears, mouth, eyes) around any AI brain you bring, as a local alternative to ElevenLabs Agents, Gemini Live, and OpenAI Realtime.
## Key points
- OpenLive is the open voice and vision layer for AI agents: your AI thinks, OpenLive gives it ears, a mouth, and eyes, running the whole voice loop on your own machine (README.md:13-17).
- The core problem it solves is wiring an AI into real conversation — voice activity detection, end-of-turn detection, streaming STT, model turn, streaming TTS, barge-in, plus camera/screen — without renting that pipeline per minute from a hosted cloud (README.md:41-45).
- It accepts any brain: a model you hold a key for (Anthropic, OpenAI, Google, xAI, DeepSeek, Groq, Ollama fully local, and more) or a coding agent you already use (Claude Code, Codex, Cursor, OpenCode, Hermes) driven locally over Agent Client Protocol JSON-RPC over stdio (README.md:50-57).
- Privacy model: listening, speaking, and watching run on-device (WebGPU); nothing spoken leaves the machine except the final transcript (plus camera/screen frames only if enabled) to whichever brain was picked (README.md:59-62).
- Architecturally it is a cascaded pipeline (speech to text to model to speech), not a full-duplex speech-to-speech model — the trade that makes "any brain, all local, no audio fees" possible (README.md:64-68).
- The on-device voice loop is Silero VAD, Whisper STT, Smart-Turn end-of-turn, and a choice of Kokoro (28 voices, light) or Supertonic (10 voices, 44.1 kHz) TTS, all in-app on WebGPU, with barge-in and custom instructions/speaking speed (README.md:74-89).
- Coding-agent integration is voice-driven per conversation with mid-call model/mode switching over ACP, native session placement (e.g. `~/.claude/projects/…`), voice permission relay, narrated progress, live plan checklist, cost chip, CLI install/auth management, mini mode, markdown transcripts, and AES-256-GCM encrypted keys (README.md:93-114).
## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root defines a pnpm monorepo (`apps/*`, `packages/*`, `services/*`) with shared TypeScript strictness, one pinned `@huggingface/transformers` copy, a single root test runner, and tag-driven releases.
## Key points
- The monorepo layout is `packages/*`, `apps/*`, and `services/*` workspaces declared in `pnpm-workspace.yaml:438-441`.
- Exactly one `@huggingface/transformers` copy (4.2.0) is forced across the tree via `overrides` in `pnpm-workspace.yaml:443-446` and `pnpm-lock.yaml:44-45` to avoid two clashing onnxruntime envs and segfaults.
- Native-module builds are allow-listed (`electron`, `electron-builder`, `esbuild`, `onnxruntime-node`, `protobufjs`, `sharp`) while `electron-winstaller` is explicitly disabled in `pnpm-workspace.yaml:449-457`.
- All packages share one strict base config: `ES2022` target, `Bundler` module resolution, `strict: true` plus `noUncheckedIndexedAccess: true` in `tsconfig.base.json:500-511`.
- One root vitest runner executes every package's colocated tests via `include: ["{apps,services,packages}/*/src/**/*.test.ts"]` with `environment: "node"` in `vitest.config.ts:527-529`.
- Releases are one tag with no manual version bump (`git tag v0.2.0 && git push origin v0.2.0`), and CI typechecks every push/PR then builds macOS/Windows/Linux installers from the tag in `RELEASING.md:481-489`.
- Generated, secret, and large/binary artifacts are never committed: `node_modules`, `.next`, `dist`, `data`, `.env`, `*.log`, `*.tsbuildinfo`, `release/`, `*.mp4`, and vendored `apps/web/public/vad/` are ignored in `.gitignore:9-30`.
## The system in five moves
1. OpenLive frames the product as the open, on-device ears-mouth-eyes loop around any brain you bring, instead of a per-minute hosted voice pipeline.
2. A cascaded local pipeline (Silero VAD → Whisper STT → Smart-Turn → Kokoro/Supertonic TTS on WebGPU, with barge-in and vision frames) carries each turn, sending only transcripts to the chosen brain.
3. Any brain plugs in — keyed model providers, fully local Ollama, or ACP-driven coding agents with mid-call switching, native sessions, permission relay, and narrated plans.
4. The repo backs this with a pnpm monorepo (`apps/*`, `packages/*`, `services/*`) under one strict TypeScript base, one pinned transformers copy, and one root vitest runner.
5. Hygiene and shipping stay lean: generated/secrets/large artifacts ignored, native builds allow-listed, and one git tag drives CI-built installers for all three desktop platforms.
