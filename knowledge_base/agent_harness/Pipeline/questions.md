---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Nishal77/Pipeline

### Q1. What is PipeLine, who is it for, and where do its roadmap and specs live?

> [!tip]- Answer
> PipeLine is an AI phone-office for solo US plumbers that answers calls and handles booking work while the owner is on a job. Direction lives in `/claude.md` for the roadmap and `spec/` for per-phase specs, both sourced from `PRD.pdf` v2.0. See [[wiki/01-overview|Overview]].

### Q2. What are the six tracks of the PipeLine monorepo and what does each one hold?

> [!tip]- Answer
> The repo splits into `apps/api` (Fastify backend with Supabase client and health checks), `apps/voice` (voice pipeline plus the Option A/B latency benchmark), and `apps/web` (Next.js PWA placeholder until Phase 4). It is rounded out by `packages/shared` (DB row types plus the PRD §14.2 agent tool contract), `supabase/migrations` (schema v1 with per-account RLS), and `docs/` (ADRs plus the carrier forwarding matrix). See [[wiki/01-overview|Overview]].

### Q3. What is done in Phase 1 versus still open, and what is the exact setup sequence?

> [!tip]- Answer
> Scaffolded in Phase 1 are the repo, CI, Supabase schema, agent tool contracts, and the voice benchmark harness. Still open are running the benchmark on real keys plus sample audio, the Option A/B and Twilio/Telnyx ADR decisions, and business gates (US entity, Stripe test mode, A2P 10DLC, carrier forwarding). Setup is `cp .env.example .env` with real keys, then `pnpm install` and `pnpm typecheck && pnpm lint && pnpm test`. See [[wiki/01-overview|Overview]].

### Q4. Which two voice-AI paths does `.env.example` declare side by side, and which keys select each?

> [!tip]- Answer
> Option A is realtime speech-to-speech selected by `OPENAI_API_KEY`, while Option B is a Deepgram STT → LLM → TTS chain using `DEEPGRAM_API_KEY`, `ANTHROPIC_API_KEY`, `CARTESIA_API_KEY`, and `ELEVENLABS_API_KEY`. The same template also declares Supabase, Twilio/Telnyx, Sentry/PostHog observability, Lemon Squeezy, and Google OAuth placeholders. See [[wiki/02-top-level-files|top-level-files]].

### Q5. What does `.gitignore` exclude and why, and what defines pnpm workspace membership?

> [!tip]- Answer
> `.gitignore` excludes build outputs and secrets (`node_modules/`, `dist/`, `.next/`, `.env`, logs, coverage) plus planning artifacts (`spec/`, `PRD.pdf`, `claude.md`, `docs/`, `apps/voice/qa/results/`), keeping generated and local files out of git. Workspace membership comes from just two globs in `pnpm-workspace.yaml` — `apps/*` and `packages/*` — with four importers (`apps/api`, `apps/voice`, `apps/web`, `packages/shared`) pinned in the lockfile. See [[wiki/02-top-level-files|top-level-files]].

### Q6. What shared TypeScript baseline, lint rules, and pinned dependencies lock the four packages together?

> [!tip]- Answer
> The shared baseline in `tsconfig.base.json` sets `ES2022`, `NodeNext` module and resolution, `strict`, `declaration`, and `sourceMap`. Lint enforces flat recommended JS/TS rules ignoring only `dist/`, `.next/`, and `node_modules/`, with `@typescript-eslint/no-unused-vars` downgraded to `warn` ignoring `_`-prefixed args. Visible lockfile pins include Fastify 5.10.0 and Supabase JS 2.110.3 for `apps/api`, Deepgram SDK 3.13.0 for `apps/voice`, and Next 16.2.10 with React 19.2.4 for `apps/web`. See [[wiki/02-top-level-files|top-level-files]].

### Q7. (Evaluation) With Phase 1 scaffolded but all open items gated on live credentials or legal steps, what should the maintainer do first and why?

> [!tip]- Answer
> The maintainer should run the voice benchmark on real API keys with sample audio and record the Option A/B and Twilio/Telnyx decision in `docs/adr/001-voice-stack.md` first, since that unblocks the telephony and forwarding work. In parallel they should start the slow business tracks (US entity, Stripe test mode, A2P 10DLC) because those gate any live pilot and no further code scaffolding removes them. See [[wiki/01-overview|Overview]].
