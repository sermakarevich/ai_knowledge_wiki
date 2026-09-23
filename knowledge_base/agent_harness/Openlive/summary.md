# Technical Analysis: katipally/openlive

**Repository:** https://github.com/katipally/openlive
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: wiring an AI into real conversation requires voice activity detection, end-of-turn detection, streaming STT, model turn, streaming TTS, barge-in, plus camera/screen input, without renting that pipeline per minute from a hosted cloud (README.md:41-45). The primary user is an individual who already holds a model key or uses a coding agent and wants a local voice/vision front end on their own machine.

How the repo addresses it: OpenLive is the open voice and vision layer for AI agents: the AI thinks, OpenLive supplies ears, mouth, and eyes, running the voice loop on-device (README.md:13-17). It is described as "that pipeline, open and local" for listening, speaking, and watching around a brain the user supplies (README.md:47-48). The user pays no per-minute audio fees, only the model costs they would pay anyway; with a coding agent as brain there is nothing extra since it runs under the existing login (README.md:50-52, README.md:132-135). Privacy model: listening, speaking, and watching run on-device on WebGPU; nothing spoken leaves the machine except the final transcript, plus camera/screen frames only if enabled, to whichever brain was picked (README.md:59-62). No audio ever uploads and API keys are encrypted at rest with only the last four digits shown (README.md:113-114).

## 2. High-Level Architecture

```
mic ─▶ VAD ──────────▶ streaming STT ─▶ end-of-turn ─▶ your AI ──────────▶ streaming TTS ─▶ speaker
(Silero) │              (Whisper)         (Smart-Turn)   (BYO model /        (Kokoro / Supertonic /
         │                                  ▲           coding agent over    cloned voice)
         │              camera / screen ────┘           ACP on local stdio)
         │              frames (vision)
         ▼
renderer (on-device voice engine) ── warm local WebSocket ──► agent server (Hono + ws) ──► provider / ACP child process
         ▲                                                                                     │
         └──────────────────────────────── sentence-by-sentence speech ◄────────────────────────┘

apps/desktop (Electron shell) ─ spawns local servers, holds window / mini mode / tray
apps/web (Next.js UI + src/lib/live/* + /api routes) ─ on-device loop + settings/agents/history
packages/db (JSON-file store) ─ encrypted keys, settings, conversations
```

Derived from the verbatim pipeline diagram (README.md:139-145), the renderer/server split (README.md:147-150), and the layout map (README.md:173-184).

Data-flow narrative:

1. Capture and detect: microphone input passes through Silero VAD; Whisper performs streaming STT; Smart-Turn decides end-of-turn (README.md:74-89, README.md:139-145).
2. Attach vision (optional): camera/screen frames ride each turn, or the `look` tool grabs a hi-res frame on demand; a text-only model can borrow a separate vision model's eyes (README.md:74-89).
3. Route the turn: everything outside "your AI" runs locally in the renderer; the turn goes over a warm local WebSocket to a small agent server (README.md:147-150).
4. Execute the brain: the server streams a provider reply or drives the coding agent's ACP adapter as a child process over Agent Client Protocol JSON-RPC over stdio (README.md:50-57, README.md:147-150).
5. Speak incrementally: the app speaks sentence by sentence while the reply streams; barge-in stops output mid-word on user interruption (README.md:74-89, README.md:147-150).
6. Persist: agent identity comes from a shared registry; conversations, settings, and encrypted keys land in the JSON-file store; coding-agent calls land in the agent's native session location (e.g. `~/.claude/projects/…`) and appear in History (README.md:93-114, README.md:173-184).

Persistent state lives in `packages/db`, a JSON-file store holding encrypted keys, settings, and conversations (README.md:173-184). Coding-agent session state additionally lives in the agent's own native placement (e.g. `~/.claude/projects/…` where `claude --resume` finds it) (README.md:93-114). Voice models downloaded from Hugging Face on first talk are cached locally after first use (README.md:154-169).

## 3. The On-Device Voice Loop

Representation: a cascaded pipeline (speech to text to model to speech), not a full-duplex speech-to-speech model; that trade is what makes "any brain, all local, no audio fees" possible (README.md:64-68). All loop stages except the brain run in-app on WebGPU (README.md:74-89).

Named kinds/types, all from the loop description (README.md:74-89):

- `Silero VAD` — voice activity detection entry stage.
- `Whisper STT` — streaming speech-to-text.
- `Smart-Turn` — end-of-turn detection.
- `Kokoro` — TTS option, 28 voices, light.
- `Supertonic` — TTS option, 10 voices, 44.1 kHz.
- `ZipVoice (Apache-2.0)` — zero-shot voice cloning backend for Settings → Clone Voice (5–30 s sample, ~208 MB optional install, deletable; profiles support preview, rename, export/import).
- `look tool` — on-demand hi-res frame grab; camera/screen frames otherwise ride each turn.

Key queries: the loop is parameterized per the Features structure (README.md:93-114) — per-conversation agent pick plus project folder; model, mode (`ask` / `accept edits` / `bypass`), and other options switchable mid-call and reported by the agent over ACP; custom instructions in Settings → General applied to every brain; speaking speed and spoken progress narration stored in settings.

Verbatim snippet (README.md:139-145):

```
mic ─▶ VAD ─▶ streaming STT ─▶ end-of-turn ─▶ your AI ──────────▶ streaming TTS ─▶ speaker
     (Silero)  (Whisper)        (Smart-Turn)  (BYO model, or a     (Kokoro / Supertonic /
                                    ▲          coding agent over    your cloned voice)
                camera / screen ────┘          ACP on local stdio)
                frames (vision)
```

## 4. LLM / External Service Integration

Providers: any brain the user holds a key for — Anthropic, OpenAI, Google, xAI, DeepSeek, Groq, Ollama fully local, and more — or a coding agent already in use (Claude Code, Codex, Cursor, OpenCode, Hermes) driven locally over Agent Client Protocol JSON-RPC over stdio (README.md:50-57).

Required vs optional calls:

- Required: one brain per conversation — either a provider reply streamed through the built-in provider turn loop, or a coding-agent turn through the ACP driver (`acp-agent.ts`, `supervisor.ts`) (README.md:147-150, README.md:173-184).
- Optional: separate vision model eyes for a text-only model; camera/screen frames only if enabled (README.md:59-62, README.md:74-89).
- Optional first-talk download: voice models from Hugging Face (~200 MB with Kokoro, more with Supertonic/bigger Whisper), then cached (README.md:154-169).
- Optional cloning payload: ZipVoice ~208 MB optional install, deletable (README.md:74-89).

Env vars: no provider env-var names are documented in the analyzed wiki pages. Key handling is via encrypted storage at rest with only the last four digits shown, managed through Settings → Agents install/sign-in flow (README.md:93-114, README.md:113-114). Build/release secrets documented are Mac signing secrets `MAC_CSC_LINK`, `MAC_CSC_KEY_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID` (RELEASING.md:491-493).

## 5. The Live Turn Pipeline

Step by step, each function tied to its file location as given in the wiki pages:

1. `mic capture → Silero VAD` in `apps/web` on-device voice engine (`src/lib/live/*`) (README.md:74-89, README.md:173-184) — detects speech locally on WebGPU.
2. `streaming STT (Whisper)` in `apps/web` (`src/lib/live/*`) (README.md:74-89, README.md:139-145) — produces the transcript; nothing spoken leaves the machine except this transcript (README.md:59-62).
3. `end-of-turn (Smart-Turn)` in `apps/web` (`src/lib/live/*`) (README.md:74-89, README.md:139-145) — decides when to hand the turn to the brain.
4. `attach vision frames` in `apps/web` (`src/lib/live/*`) (README.md:74-89, README.md:139-145) — camera/screen frames ride the turn or are pulled via the `look` tool.
5. `warm local WebSocket (/live)` in `services/agent` (Hono + ws) (README.md:147-150, README.md:173-184) — transports the turn from renderer to the small agent server.
6. `provider turn loop OR ACP agent driver (acp-agent.ts, supervisor.ts)` in `services/agent` as child process over local stdio (README.md:50-57, README.md:147-150, README.md:173-184) — executes the model or coding-agent turn; permission asks are relayed back for voice/tap answer ("yes"/"no") (README.md:93-114).
7. `streaming TTS (Kokoro / Supertonic / cloned voice)` in `apps/web` (`src/lib/live/*`) plus `services/agent` `voice/*` cloning path (README.md:74-89, README.md:173-184) — speaks sentence by sentence while the reply streams (README.md:147-150); barge-in interrupts mid-word (README.md:74-89).
8. `persist + render` via `packages/db` JSON-file store (keys, settings, conversations) and `apps/web` `/api routes` (history discovery, settings) plus agent-native session files (README.md:93-114, README.md:173-184) — markdown transcript with code-block copy buttons and full Markdown export; working plan renders as checklist; context/cost chip tracks the session (README.md:93-114).

Cross-reference for the ACP driver, voice loop, resume, and delegate/worker tool flow: `docs/ARCHITECTURE.md` (README.md:186-187).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| README.md | 13-17, 41-68, 74-184 | Project definition, problem statement, loop components, pipeline diagram, layout map |
| docs/ARCHITECTURE.md | cited at README.md:186-187 | ACP driver, voice loop, resume, delegate/worker tool flow detail |
| apps/desktop (dir) | README.md:173-184 | Electron shell: spawns local servers, media perms, window, mini mode, tray + notifications |
| apps/web (dir) | README.md:173-184 | Next.js UI + on-device voice engine (`src/lib/live/*`) + `/api` routes |
| apps/web/src/lib/live/* | README.md:173-184 | On-device voice engine: VAD/STT/end-of-turn/TTS loop |
| services/agent (dir) | README.md:173-184 | Hono + ws `/live` WebSocket, ACP driver, provider turn loop, voice cloning |
| services/agent/acp-agent.ts | README.md:173-184 | ACP agent driver (coding-agent child process) |
| services/agent/supervisor.ts | README.md:173-184 | ACP supervision alongside the agent driver |
| services/agent/voice/* | README.md:173-184 | Voice cloning path (ZipVoice) |
| packages/shared (dir) | README.md:173-184 | Agent registry (single source of agent identity), wire protocol, shared types |
| packages/harness (dir) | README.md:173-184 | Provider-neutral model adapters, live model listing, cost/effort |
| packages/db (dir) | README.md:173-184 | JSON-file store: encrypted keys, settings, conversations |
| pnpm-workspace.yaml | 438-446, 449-471 | Workspace globs, single transformers override, native-build allow-list |
| pnpm-lock.yaml | 38-62, 64-255 | Lockfile v9, peer settings, pinned importer dependency sets |
| tsconfig.base.json | 499-516 | Shared strict TS base (ES2022, Bundler resolution, `noUncheckedIndexedAccess`) |
| vitest.config.ts | 522-531 | Single root runner for colocated `*.test.ts` |
| RELEASING.md | 479-493 | Tag-driven release procedure and Mac signing secrets |
| CONTRIBUTING.md | README.md:189-197 | Contribution entry point; license is MIT |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| @huggingface/transformers | `4.2.0` (override) | Single on-device ML runtime; override avoids two onnxruntime envs that clash and segfault |
| typescript | `^5.7.3` | Shared strict compilation (root dev dep) |
| vitest | `^3.2.4` | Root test runner for colocated tests |
| concurrently | `^9.1.0` | Multi-server dev orchestration (root dev dep) |
| cross-env | `^10.0.0` | Cross-platform env handling (root dev dep) |
| electron | `^43.1.1` | Desktop shell |
| electron-builder | `^25.1.8` | macOS/Windows/Linux installer builds |
| esbuild | `^0.28.1` | Bundling / native-build allow-listed |
| next | `^16.2.9` | Web app framework (`apps/web`) |
| react | `^19.2.0` | Web UI |
| kokoro-js | `^1.2.0` | Light Kokoro TTS option (pulls transformers 3.8.1, hence the override) |
| @ricky0123/vad-web | `^0.0.29` | Silero VAD in browser |
| onnxruntime-web | `^1.22.0` | WebGPU inference for on-device loop |
| hono | `^4.12.27` | Agent service HTTP framework |
| @hono/node-server | `^1.13.8` | Node adapter for Hono service |
| sherpa-onnx-node | `^1.13.4` | Native speech runtime in agent service |
| tar | `^7.5.20` | Archive handling in agent service |
| proper-lockfile | `^4.1.2` | File locking for JSON-file store (`packages/db`) |
| zod | `^3.24.1` | Shared types / wire-protocol validation (`packages/shared`) |
| onnxruntime-node | allow-listed `true` | Native inference backend (build allow-list) |
| protobufjs | allow-listed `true` | Native-build allow-listed serialization dep |
| sharp | allow-listed `true` | Native-build allow-listed image dep |

Constraint strings and allow-list values from `pnpm-lock.yaml:44-62`, `pnpm-lock.yaml:64-255`, and `pnpm-workspace.yaml:449-457`. Lockfile per-package resolution entries beyond the importers section were truncated in the source chunk (noted at chunk line 432), so only importer-level constraints are listed here.

## 8. CLI / Usage Surface

Entry points: installer from the latest release for end use; source dev via `apps/desktop` Electron shell and `apps/web` Next.js app; agent turn backend in `services/agent` (README.md:154-169, README.md:173-184).

| Command | Purpose |
|---|---|
| installer from latest release, then paste model key or pick installed coding agent, start a call | End-user path; voice models download from Hugging Face on first talk (~200 MB Kokoro), then cached (README.md:154-169) |
| `pnpm install` | Install monorepo workspaces (README.md:154-169) |
| `pnpm desktop:dev` | Runs web + agent servers and opens the app window (README.md:154-169) |
| `pnpm dev` + open `localhost:3000` | Browser dev alternative (README.md:154-169) |
| `pnpm test` | Run root vitest suite over `{apps,services,packages}/*/src/**/*.test.ts` (README.md:154-169, vitest.config.ts:522-531) |
| `git tag v0.2.0 && git push origin v0.2.0` | Maintainer release; tag drives version, CI builds and publishes all three installers (RELEASING.md:483-489) |

| Env var / secret | Required? | Purpose |
|---|---|---|
| Model API key (per provider) | Required iff using a keyed brain | Pasted in app; stored encrypted, only last four digits shown (README.md:113-114, README.md:154-169) |
| Coding-agent login | Required iff using agent brain | Runs under existing login, no extra cost (README.md:50-52) |
| `MAC_CSC_LINK` | Release-only | macOS signing (RELEASING.md:491-493) |
| `MAC_CSC_KEY_PASSWORD` | Release-only | macOS signing (RELEASING.md:491-493) |
| `APPLE_ID` | Release-only | macOS notarization (RELEASING.md:491-493) |
| `APPLE_APP_SPECIFIC_PASSWORD` | Release-only | macOS notarization (RELEASING.md:491-493) |
| `APPLE_TEAM_ID` | Release-only | macOS signing identity (RELEASING.md:491-493) |

| Config surface | Location | Purpose |
|---|---|---|
| Settings → General | `apps/web` + `packages/db` | Custom instructions for every brain; speaking speed; spoken progress narration (README.md:74-89) |
| Settings → Clone Voice | `services/agent` `voice/*` | 5–30 s sample, listen-back, ZipVoice profile management (README.md:74-89) |
| Settings → Agents | `apps/web` `/api` routes | Install, sign in, update, uninstall each agent CLI; status self-updates (README.md:93-114) |
| Per-conversation picker | app UI | Agent + project folder + mid-call model/mode (`ask`/`accept edits`/`bypass`) switch (README.md:93-114) |
| Mini mode / tray | `apps/desktop` | Always-on-top pill, menu-bar tray, notifications (README.md:93-114) |

## 9. Extensibility Points

- New model provider: extend the provider-neutral adapters and live model listing in `packages/harness` (README.md:173-184); brain choice is BYO-key by design (README.md:50-57).
- New coding agent: extend the agent registry (single source of agent identity) in `packages/shared` and the install/auth `/api` routes in `apps/web`, reusing the ACP driver pattern (`acp-agent.ts`, `supervisor.ts`) in `services/agent` (README.md:93-114, README.md:173-184).
- Voice-loop stage swap (VAD/STT/end-of-turn/TTS): extend the on-device engine in `apps/web` `src/lib/live/*`; the two TTS options (Kokoro 28 voices vs Supertonic 10 voices at 44.1 kHz) show the intended seam (README.md:74-89, README.md:173-184).
- New voice/clone backend: extend `services/agent` `voice/*` alongside the ZipVoice path (README.md:173-184, README.md:74-89).
- Wire-protocol change: extend shared types/protocol in `packages/shared` (zod-validated) consumed by both `apps/web` and `services/agent` (README.md:173-184, `pnpm-lock.yaml:202-206`).
- Persistence field: extend the JSON-file store in `packages/db` (encrypted keys, settings, conversations) with `proper-lockfile` locking (README.md:173-184, `pnpm-lock.yaml:171-178`).
- Desktop capability (window, tray, mini mode, media perms): extend the Electron shell in `apps/desktop` (README.md:173-184).

## 10. Limitations and Gotchas

- **Cascaded, not full-duplex:** the pipeline is speech→text→model→speech rather than a full-duplex speech-to-speech model, so turn latency and prosody are bounded by the STT→LLM→TTS chain even though barge-in stops output mid-word (README.md:64-68, README.md:74-89).
- **First-talk model download:** voice models fetch from Hugging Face on first talk (~200 MB with Kokoro, more with Supertonic/bigger Whisper) before caching, so first-run latency and disk use are higher than subsequent runs (README.md:154-169).
- **Single pinned transformers copy:** exactly one `@huggingface/transformers` 4.2.0 is forced because kokoro-js pulls 3.8.1 and "two copies = two onnxruntime-node envs that clash and segfault" (`pnpm-workspace.yaml:443-444`, `pnpm-lock.yaml:44-45`); bumping either side without the override risks native crashes.
- **Only the transcript (plus opted-in frames) reaches the brain:** on-device privacy means the cloud model never hears raw audio — it receives the final transcript and, only if enabled, camera/screen frames — so audio-grounded reasoning is unavailable server-side (README.md:59-62).
- **Generated/large artifacts are git-ignored, not vendored:** `node_modules`, `.next`, `dist`, `data`, `.env`, `release/`, `*.mp4`, and `apps/web/public/vad/` are never committed (`.gitignore:9-30`); the VAD assets must be rebuilt via `copy-voice-assets.mjs` and demo videos live only as hosted GitHub assets (`.gitignore:25`, `.gitignore:28`).
- **Releases are tag-driven with platform-specific signing gaps:** one tag builds all installers with no manual version bump (RELEASING.md:483-489), but Mac signing/notarization only runs when all five Apple secrets are set, and Linux ships as an unsigned AppImage (RELEASING.md:487-493).

## 11. How It Compares to Alternatives

- **ElevenLabs Agents:** hosted voice-agent platform with per-minute audio + hosted pipeline; OpenLive is positioned as the open, on-device voice/vision loop alternative with no per-minute audio fees — only the user's own model costs (README.md:13-17, README.md:50-52).
- **Gemini Live:** closed full-duplex multimodal live API tied to one vendor's brain; OpenLive is cascaded rather than speech-to-speech but accepts any brain including fully local Ollama (README.md:50-57, README.md:64-68).
- **OpenAI Realtime:** closed low-latency speech-to-speech API tied to OpenAI models and usage billing; OpenLive keeps VAD/STT/end-of-turn/TTS local on WebGPU and sends only the transcript (plus opted-in frames) to the chosen brain (README.md:59-68).

Positioning sentence: where the three incumbents sell a hosted, single-vendor voice stack billed per minute, OpenLive unbundles the loop — local ears/mouth/eyes, bring-your-own brain over keys or local ACP coding agents — trading full-duplex fidelity for vendor independence, on-device privacy, and zero audio fees (README.md:41-68).

## Appendix: Selected Code Snippets

1. Live-turn pipeline diagram (`README.md:139-145`):

```
mic ─▶ VAD ─▶ streaming STT ─▶ end-of-turn ─▶ your AI ──────────▶ streaming TTS ─▶ speaker
     (Silero)  (Whisper)        (Smart-Turn)  (BYO model, or a     (Kokoro / Supertonic /
                                    ▲          coding agent over    your cloned voice)
                camera / screen ────┘          ACP on local stdio)
                frames (vision)
```

2. Workspace pinning (`pnpm-workspace.yaml:438-446`):

```
packages:
  - "packages/*"
  - "apps/*"
  - "services/*"
overrides:
  "@huggingface/transformers": "4.2.0"
```

3. Shared strict base (`tsconfig.base.json:499-516`):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "moduleDetection": "force",
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "verbatimModuleSyntax": false,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true,
    "declaration": true,
    "isolatedModules": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

4. Root test runner (`vitest.config.ts:522-531`):

```ts
import { defineConfig } from "vitest/config";

// One root runner for every package's colocated *.test.ts files (they existed
// before this config but had no framework to run them).
export default defineConfig({
  test: {
    include: ["{apps,services,packages}/*/src/**/*.test.ts"],
    environment: "node",
  },
});
```
