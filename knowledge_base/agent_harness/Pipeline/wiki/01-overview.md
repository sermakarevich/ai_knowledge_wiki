> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** PipeLine is an AI phone-office for solo US plumbers, scaffolded as a pnpm monorepo with voice, API, web, shared-contract, Supabase, and docs tracks whose Phase 1 foundations are in place but await live-credential decisions.
## Key points
- PipeLine's job is an AI phone-office for solo US plumbers, with the roadmap in `/claude.md` and per-phase specs in `spec/` sourced from `PRD.pdf` v2.0 (README:9-10).
- `apps/api` is the Fastify backend holding the Supabase client and health checks, slated to grow into the booking/owner-app API in later phases (README:13-14).
- `apps/voice` holds the voice pipeline plus the Phase 1 Option A/B latency benchmark (README:15).
- `apps/web` is the Next.js PWA whose owner app ships in Phase 4 and is currently a placeholder, while `packages/shared` holds DB row types plus the agent tool contract (PRD §14.2) shared by `voice` and `api` so both pipelines dispatch through one schema (README:16-18).
- `supabase/migrations` holds schema v1 (PRD §13) with per-account RLS, and `docs/` holds `adr` architecture decisions starting with `001-voice-stack.md` plus `forwarding.md` with the carrier forwarding test matrix (A5) (README:19-21).
- Setup is `cp .env.example .env` with real keys, then `pnpm install` and `pnpm typecheck && pnpm lint && pnpm test` (README:24-28).
- Phase 1 scaffolded state covers repo, CI, Supabase schema, agent tool contracts, and the voice benchmark harness, while still open per `spec/phase-1-foundations.md` are running the benchmark against real API keys plus sample audio, deciding Option A vs B and Twilio vs Telnyx in `docs/adr/001-voice-stack.md`, filing the US entity, opening Stripe test mode, submitting A2P 10DLC, and verifying carrier forwarding (README:31-36).
---
## Purpose
PipeLine is an "AI phone-office for solo US plumbers" (README:9). Direction lives in `/claude.md` for the roadmap and `spec/` for per-phase specs, both sourced from `PRD.pdf` v2.0 (README:9-10).
## Monorepo layout
| Path | Role |
|---|---|
| `apps/api` | Fastify backend (Supabase client, health checks; grows into the booking/owner-app API in later phases) (README:13-14) |
| `apps/voice` | Voice pipeline + the Phase 1 Option A/B latency benchmark (README:15) |
| `apps/web` | Next.js PWA (owner app ships Phase 4; currently a placeholder) (README:16) |
| `packages/shared` | DB row types + the agent tool contract (PRD §14.2), shared by `voice` and `api` so both pipelines dispatch through one schema (README:17-18) |
| `supabase/migrations` | Schema v1 (PRD §13) with per-account RLS (README:19) |
| `docs/adr` | Architecture decisions (start with `001-voice-stack.md`) (README:20) |
| `docs/forwarding.md` | Carrier forwarding test matrix (A5) (README:21) |
## Setup
Verbatim from the chunk (README:24-28):
```
cp .env.example .env   # fill in real keys before running anything live
pnpm install
pnpm typecheck && pnpm lint && pnpm test
```
The `.env` must be filled with real keys before running anything live (README:25).
## Phase 1 status
Scaffolded: repo, CI, Supabase schema, agent tool contracts, and the voice benchmark harness (README:31-32). Still open per `spec/phase-1-foundations.md` (README:32-36): run the benchmark against real API keys + sample audio, decide Option A vs B and Twilio vs Telnyx in `docs/adr/001-voice-stack.md`, file the US entity, open Stripe test mode, submit A2P 10DLC, and verify carrier forwarding (`docs/forwarding.md`). The chunk states those four are business/legal or require live credentials this environment doesn't have — no code blocks them (README:36-37).
> Truncation note: the chunk's `## Macro components` list is cut off after its first entry, `top-level-files/` (README:39-41); no further component entries were provided, so they are not described here.
**Covers:** `README` (purpose, monorepo layout, setup, Phase 1 status); referenced-but-not-quoted `claude.md`, `spec/`, `PRD.pdf` v2.0, `apps/api`, `apps/voice`, `apps/web`, `packages/shared`, `supabase/migrations`, `docs/adr/001-voice-stack.md`, `docs/forwarding.md`
