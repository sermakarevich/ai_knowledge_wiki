> [[index|Wiki]] | [[summary|Summary]]

# Nishal77/Pipeline — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** PipeLine is an AI phone-office for solo US plumbers, scaffolded as a pnpm monorepo with voice, API, web, shared-contract, Supabase, and docs tracks whose Phase 1 foundations are in place but await live-credential decisions.

## Key points

- PipeLine's job is an AI phone-office for solo US plumbers, with the roadmap in `/claude.md` and per-phase specs in `spec/` sourced from `PRD.pdf` v2.0 (README:9-10).
- `apps/api` is the Fastify backend holding the Supabase client and health checks, slated to grow into the booking/owner-app API in later phases (README:13-14).
- `apps/voice` holds the voice pipeline plus the Phase 1 Option A/B latency benchmark (README:15).
- `apps/web` is the Next.js PWA whose owner app ships in Phase 4 and is currently a placeholder, while `packages/shared` holds DB row types plus the agent tool contract (PRD §14.2) shared by `voice` and `api` so both pipelines dispatch through one schema (README:16-18).
- `supabase/migrations` holds schema v1 (PRD §13) with per-account RLS, and `docs/` holds `adr` architecture decisions starting with `001-voice-stack.md` plus `forwarding.md` with the carrier forwarding test matrix (A5) (README:19-21).
- Setup is `cp .env.example .env` with real keys, then `pnpm install` and `pnpm typecheck && pnpm lint && pnpm test` (README:24-28).
- Phase 1 scaffolded state covers repo, CI, Supabase schema, agent tool contracts, and the voice benchmark harness, while still open per `spec/phase-1-foundations.md` are running the benchmark against real API keys plus sample audio, deciding Option A vs B and Twilio vs Telnyx in `docs/adr/001-voice-stack.md`, filing the US entity, opening Stripe test mode, submitting A2P 10DLC, and verifying carrier forwarding (README:31-36).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** Top-level files define the monorepo's environment variables, workspace membership, build/lint configuration, and pinned dependencies.

## Key points

- Declares all external integrations via `.env.example` placeholders for Supabase, Twilio, Telnyx, voice-AI providers, observability, Lemon Squeezy, and Google OAuth (`.env.example:1-3,14-16,20,23-29,32-38,45-47`).
- Supports two voice-AI paths side by side: Option A realtime speech-to-speech via `OPENAI_API_KEY` and Option B Deepgram STT → LLM → TTS via `DEEPGRAM_API_KEY`, `ANTHROPIC_API_KEY`, `CARTESIA_API_KEY`, `ELEVENLABS_API_KEY` (`.env.example:22-29`).
- Excludes build outputs, secrets, logs, and planning artifacts from git, including `node_modules/`, `dist/`, `.next/`, `.env`, `spec/`, `docs/`, and `apps/voice/qa/results/` (`.gitignore:1-8,13-17`).
- Enforces flat recommended TypeScript/JS lint rules with `js.configs.recommended` plus `tseslint.configs.recommended`, ignoring only `dist/`, `.next/`, and `node_modules/` (`.eslint.config.js:8-10`).
- Downgrades `@typescript-eslint/no-unused-vars` to `warn` and ignores unused args starting with `_` via `argsIgnorePattern: "^_"` (`.eslint.config.js:14-16`).
- Declares a pnpm workspace covering `apps/*` and `packages/*` with four importers (`apps/api`, `apps/voice`, `apps/web`, `packages/shared`) pinned in the lockfile (`.pnpm-workspace.yaml:1-3`, `pnpm-lock.yaml:101-233`).
- Sets shared strict TypeScript baseline (`ES2022`, `NodeNext` module/resolution, `strict`, `declaration`, `sourceMap`) in `tsconfig.base.json` (`.tsconfig.base.json:2-11`).
- `pnpm-lock.yaml` content was truncated in the source chunk (5893 lines total, body cut after the `@esbuild/openbsd-arm64` entry), so dependency-package claims below cover only the visible `importers` block (`.pnpm-lock.yaml:92-233`).

## The system in five moves

1. PipeLine is framed as an AI phone-office for solo US plumbers, with the roadmap and per-phase specs sourced from PRD v2.0.
2. The vision is scaffolded as a pnpm monorepo splitting voice, API, web, shared contracts, Supabase schema, and docs/ADR tracks.
3. Top-level files declare every external integration up front (Supabase, Twilio/Telnyx, dual voice-AI paths, observability, Lemon Squeezy, Google OAuth) while keeping secrets and build outputs out of git.
4. Workspace membership, a strict shared TypeScript baseline, recommended lint rules, and pinned lockfile importers lock the four packages into one reproducible toolchain.
5. Setup reduces to env copy plus install plus typecheck/lint/test, and Phase 1 foundations (repo, CI, schema, contracts, benchmark harness) are declared done.
6. The remaining arc is explicitly non-code: run the voice benchmark on real keys, decide Option A vs B and Twilio vs Telnyx, and clear business/legal gates (US entity, Stripe test mode, A2P 10DLC, carrier forwarding).
