# Technical Analysis: Nishal77/Pipeline

**Repository:** https://github.com/Nishal77/Pipeline
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: solo plumbers in the US miss revenue when they cannot answer the phone while on a job; they need call answering, booking intake, and owner-side follow-up without hiring office staff. The repository addresses this with PipeLine, described as an "AI phone-office for solo US plumbers" (`README:9` per `wiki/01-overview.md:14`). Direction is sourced from `PRD.pdf` v2.0 via `/claude.md` (roadmap) and `spec/` (per-phase specs) (`README:9-10` per `wiki/01-overview.md:5`). At the analyzed state the repo is a Phase 1 scaffold: monorepo, CI, Supabase schema v1, agent tool contracts, and a voice benchmark harness are in place, while live-credential decisions (benchmark run against real keys and sample audio, Option A vs B, Twilio vs Telnyx, US entity filing, Stripe test mode, A2P 10DLC, carrier forwarding verification) remain open per `spec/phase-1-foundations.md` (`README:31-36` per `wiki/01-overview.md:11`). The primary user is the solo US plumber operating as owner-dispatcher-technician.

## 2. High-Level Architecture

```
                        ┌─ apps/voice ─────────────────┐
                        │ voice pipeline + Option A/B  │
                        │ latency benchmark harness    │
                        └──────────────┬───────────────┘
                                       │
Caller ─► Carrier (Twilio / Telnyx, ─► STT ─► LLM ─► TTS ─► Caller
          forwarding matrix in                 │
          docs/forwarding.md)                  ▼
                               packages/shared (DB row types +
                               agent tool contract, PRD §14.2)
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          ▼                          │
                    │              apps/api (Fastify + Supabase           │
                    │              client + health checks; grows          │
                    │              into booking/owner-app API)            │
                    │                          │                          │
                    │                          ▼                          │
                    │              Supabase / supabase/migrations         │
                    │              (schema v1, PRD §13, per-account RLS)  │
                    └──────────────────────────┬──────────────────────────┘
                                               │
                    apps/web (Next.js PWA; owner app ships Phase 4,
                    currently placeholder) ─► reads/writes via apps/api
```

Component roles per `wiki/01-overview.md:18-24`: `apps/api` is the Fastify backend (Supabase client, health checks); `apps/voice` holds the voice pipeline plus the Phase 1 benchmark; `apps/web` is the Next.js PWA placeholder; `packages/shared` holds DB row types plus the agent tool contract shared by `voice` and `api`; `supabase/migrations` holds schema v1 with per-account RLS; `docs/adr` holds architecture decisions from `001-voice-stack.md` and `docs/forwarding.md` holds the carrier forwarding test matrix (A5).

Data-flow narrative:

1. An inbound caller dials the plumber's number; carrier forwarding (Twilio or Telnyx, decision pending in `docs/adr/001-voice-stack.md`) routes the call into `apps/voice` (`README:15,20-21` per `wiki/01-overview.md:6-9`).
2. `apps/voice` transcribes and responds through one of two paths under benchmark: Option A realtime speech-to-speech, or Option B pipelined STT → LLM → TTS (`.env.example:22-29` per `wiki/02-top-level-files.md:6`).
3. Tool-using turns dispatch through the single agent tool contract in `packages/shared` (PRD §14.2), so voice and API paths share one schema (`README:17-18` per `wiki/01-overview.md:8`).
4. Booking and account state persist in Supabase under schema v1 with per-account RLS (`README:19` per `wiki/01-overview.md:9`); `apps/api` mediates access via its Supabase client (`README:13-14` per `wiki/01-overview.md:6`).
5. The owner reviews and manages work through `apps/web` (Phase 4 owner app; placeholder at this state) backed by `apps/api` (`README:16` per `wiki/01-overview.md:8`).
6. Phase 1 validation closes the loop offline: the benchmark harness plus `docs/forwarding.md` matrix verify latency and carrier behavior before any live cutover (`README:32-36` per `wiki/01-overview.md:11`).

Persistent state lives in Supabase (schema v1, `supabase/migrations`, per-account RLS). No other durable store is documented in the analyzed pages; local planning and QA artifacts (`spec/`, `PRD.pdf`, `claude.md`, `docs/`, `apps/voice/qa/results/`) are explicitly excluded from git (`.gitignore:1-17` per `wiki/02-top-level-files.md:52-69`).

## 3. The Shared Tool Contract

The central abstraction is the shared agent tool contract in `packages/shared`: DB row types plus the tool-call schema from PRD §14.2, consumed by both `apps/voice` and `apps/api` so both pipelines dispatch through one schema (`README:17-18` per `wiki/01-overview.md:8,21`).

Representation: TypeScript row types mirroring the Supabase v1 schema plus a tool-call contract (tool names, argument schemas, result shapes). The analyzed component pages do not enumerate the individual type or tool names, so no named kind list with per-symbol `file:line` can be grounded here; the finest-grained citations available are `README:17-18` for the contract's existence and location, and `pnpm-lock.yaml:210-233` for the package's pinned dependencies (`zod ^3.24.1 → 3.25.76`, `@supabase/supabase-js ^2.47.10 → 2.110.3`, `web-push ^3.6.7 → 3.6.7`) per `wiki/02-top-level-files.md:116`.

Key queries against this abstraction follow the same pattern in both consumers: validate the tool call with the shared schema, execute against Supabase, return the typed result. Verbatim contract source is not quoted in the analyzed wiki pages; the closest verbatim artifact is the dependency pin block placing `@pipeline/shared workspace:*` as a dependency of `apps/api` and `apps/voice` (`pnpm-lock.yaml:105-165` per `wiki/02-top-level-files.md:113-114`):

```
apps/api:   @pipeline/shared workspace:*  (pnpm-lock.yaml:105-131)
apps/voice: @pipeline/shared workspace:*  (pnpm-lock.yaml:133-165)
```

## 4. LLM / External Service Integration

Providers declared via `.env.example` placeholders (`.env.example:1-47` per `wiki/02-top-level-files.md:5,14-50`):

| Provider | Env vars | Role |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | Voice AI Option A: realtime speech-to-speech (`.env.example:22-29`) |
| Deepgram | `DEEPGRAM_API_KEY` | Voice AI Option B: STT (`.env.example:22-29`) |
| Anthropic | `ANTHROPIC_API_KEY` | Voice AI Option B: LLM (`.env.example:22-29`) |
| Cartesia | `CARTESIA_API_KEY` | Voice AI Option B: TTS (`.env.example:22-29`) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Voice AI Option B: alternate TTS (`.env.example:22-29`) |
| Twilio | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_TEST_NUMBER` | Voice benchmark + `apps/api` |
| Telnyx | `TELNYX_API_KEY` | Benchmark comparison endpoint (PRD Q3) |
| Supabase | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY` | Database, auth, RLS enforcement |
| Sentry | `SENTRY_DSN` | Error observability |
| PostHog | `POSTHOG_API_KEY`, `POSTHOG_HOST=https://app.posthog.com` | Product analytics |
| Lemon Squeezy | `LEMONSQUEEZY_API_KEY`, `LEMONSQUEEZY_STORE_ID`, `LEMONSQUEEZY_WEBHOOK_SECRET` | Merchant-of-record billing |
| Google | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | Google API (OAuth) |

Required vs optional: no call works live without real keys — `.env` must be filled with real keys before running anything live (`README:25` per `wiki/01-overview.md:10,32`). The Phase 1 benchmark specifically requires real API keys plus sample audio to execute (`README:32-36` per `wiki/01-overview.md:11`). Carrier choice (Twilio vs Telnyx) and voice-stack choice (Option A vs B) are explicitly undecided in `docs/adr/001-voice-stack.md`, so all voice-provider keys are currently evaluation inputs rather than committed production dependencies. Supabase keys are required for any persisted path; Sentry/PostHog, Lemon Squeezy, and Google credentials are supporting integrations staged for later phases.

## 5. The Voice Intake and Benchmark Pipeline

Primary workflow: inbound call handling with a Phase 1 latency benchmark comparing Option A against Option B before committing to a stack or carrier. The analyzed wiki pages provide no function-level inventory, so per-function `file:line` citations cannot be grounded; the steps below carry the finest citations the pages support. (Note: the repo is TypeScript, not Python; there are no `file.py` units.)

1. Provision credentials: `cp .env.example .env` and fill in real keys (`README:24-28` per `wiki/01-overview.md:10`; verbatim in Appendix).
2. Install and gate: `pnpm install`, then `pnpm typecheck && pnpm lint && pnpm test` (`README:24-28` per `wiki/01-overview.md:10`) under the shared strict baseline (`tsconfig.base.json:2-11`: `ES2022`, `NodeNext` module/resolution, `strict`, `declaration`, `sourceMap`) and flat recommended lint (`eslint.config.js:8-10`) per `wiki/02-top-level-files.md:8,11`.
3. Run the Option A/B latency benchmark in `apps/voice` against real API keys plus sample audio (`README:32-36` per `wiki/01-overview.md:11`); `apps/voice` pins `@deepgram/sdk ^3.11.1 → 3.13.0`, `ws ^8.18.0 → 8.21.0`, `zod-to-json-schema ^3.24.1 → 3.25.2` (`pnpm-lock.yaml:133-165` per `wiki/02-top-level-files.md:114`).
4. Record the decision in `docs/adr/001-voice-stack.md` (Option A vs B; Twilio vs Telnyx) and verify carrier forwarding against the `docs/forwarding.md` test matrix (A5) (`README:19-21,32-36` per `wiki/01-overview.md:9,11`).
5. Serve live traffic: carrier forwards to `apps/voice`, tool calls dispatch through the `packages/shared` contract, state persists via `apps/api` into Supabase v1 with per-account RLS (`README:13-19` per `wiki/01-overview.md:6-9`).
6. Clear business gates in parallel: file the US entity, open Stripe test mode, submit A2P 10DLC — stated as unblocked by code (`README:36-37` per `wiki/01-overview.md:34`).

## 6. Key Files

Line counts are not provided in the analyzed wiki pages; ordering below is by structural importance.

| File | Lines | What It Does |
|---|---|---|
| `README` | cited `README:9-41` | Purpose, monorepo layout, setup, Phase 1 status; entry-point documentation |
| `claude.md` | referenced, excluded from git | Roadmap source derived from `PRD.pdf` v2.0 |
| `spec/phase-1-foundations.md` | referenced, excluded from git | Phase 1 acceptance criteria and open live-credential items |
| `PRD.pdf` | v2.0, excluded from git | Source spec (§13 schema, §14.2 tool contract) |
| `apps/voice/` | — | Voice pipeline plus Option A/B latency benchmark harness |
| `apps/api/` | — | Fastify backend with Supabase client and health checks; future booking/owner-app API |
| `packages/shared/` | — | DB row types and agent tool contract shared by voice and API |
| `apps/web/` | — | Next.js PWA; owner app ships Phase 4, currently placeholder |
| `supabase/migrations/` | schema v1 | Versioned schema with per-account RLS |
| `docs/adr/001-voice-stack.md` | referenced, excluded from git | Pending Option A-vs-B and Twilio-vs-Telnyx decision record |
| `docs/forwarding.md` | matrix A5, excluded from git | Carrier forwarding test matrix |
| `.env.example` | `1-47` | Placeholder declarations for all external integrations |
| `pnpm-workspace.yaml` | `1-3` | Workspace membership (`apps/*`, `packages/*`) |
| `tsconfig.base.json` | `1-11` | Shared strict compiler baseline |
| `eslint.config.js` | `4-17` | Flat recommended JS/TS lint config |
| `.gitignore` | `1-17` | Excludes build outputs, secrets, logs, planning artifacts |
| `pnpm-lock.yaml` | 5893 lines, importers `101-233` visible | Pinned dependency graph; packages body truncated in source |

## 7. Dependencies

Required first (runtime/backend/voice/data), then frontend and shared/support. Constraint strings are exact specifiers from the lockfile importers block (`pnpm-lock.yaml:101-233` per `wiki/02-top-level-files.md:110-116`); the packages body beyond the importers block was truncated in source, so transitive pins are not covered.

| Package | Version constraint | Purpose |
|---|---|---|
| fastify | `^5.2.0 → 5.10.0` | `apps/api` HTTP server |
| @supabase/supabase-js | `^2.47.10 → 2.110.3` | Supabase client in `apps/api` and `packages/shared` |
| zod | `^3.24.1 → 3.25.76` | Schema validation in `apps/api`, `apps/voice`, `packages/shared` |
| @deepgram/sdk | `^3.11.1 → 3.13.0` | Option B speech-to-text in `apps/voice` |
| ws | `^8.18.0 → 8.21.0` | WebSocket transport in `apps/voice` |
| zod-to-json-schema | `^3.24.1 → 3.25.2` | Tool-schema conversion in `apps/voice` |
| @pipeline/shared | `workspace:*` | Internal contract dependency of `apps/api` and `apps/voice` |
| next | `16.2.10` | `apps/web` PWA framework |
| react | `19.2.4` | `apps/web` UI |
| react-dom | `19.2.4` | `apps/web` rendering |
| @supabase/ssr | `^0.5.2 → 0.5.2` | Supabase auth in `apps/web` |
| tailwindcss | `^4 → 4.3.2` | `apps/web` styling |
| web-push | `^3.6.7 → 3.6.7` | Push notifications in `packages/shared` |
| @sentry/node | `^8.47.0 → 8.55.2` | Error tracking in `apps/api` |

## 8. CLI / Usage Surface

Entry points: `apps/api` (Fastify service), `apps/voice` (voice pipeline and benchmark harness), `apps/web` (Next.js PWA), `packages/shared` (library, no CLI). No command/flag table beyond the documented setup gates exists in the analyzed pages.

| Command | Purpose |
|---|---|
| `cp .env.example .env` | Create local env file; fill in real keys before running anything live (`README:24-28`) |
| `pnpm install` | Install workspace dependencies |
| `pnpm typecheck && pnpm lint && pnpm test` | Verification gate over the monorepo |

Environment variables (all placeholders in `.env.example:1-47`, verbatim in Appendix):

| Variable(s) | Required when |
|---|---|
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY` | Any persisted or authenticated path |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_TEST_NUMBER` | Twilio benchmark leg or telephony path |
| `TELNYX_API_KEY` | Telnyx comparison leg |
| `OPENAI_API_KEY` | Option A realtime evaluation |
| `DEEPGRAM_API_KEY`, `ANTHROPIC_API_KEY`, `CARTESIA_API_KEY`, `ELEVENLABS_API_KEY` | Option B pipeline evaluation |
| `SENTRY_DSN`, `POSTHOG_API_KEY`, `POSTHOG_HOST` | Observability |
| `LEMONSQUEEZY_API_KEY`, `LEMONSQUEEZY_STORE_ID`, `LEMONSQUEEZY_WEBHOOK_SECRET` | Billing |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | Google API integration |
| `NODE_ENV=development` | Default environment |

Config files:

| File | Role |
|---|---|
| `pnpm-workspace.yaml:1-3` | Workspace membership: `apps/*`, `packages/*` |
| `tsconfig.base.json:1-11` | Strict shared compiler baseline |
| `eslint.config.js:4-17` | Recommended JS/TS rules; `no-unused-vars` downgraded to `warn` with `argsIgnorePattern: "^_"`; ignores `dist`, `.next`, `node_modules` |
| `.gitignore:1-17` | Excludes generated, secret, and planning artifacts from git |
| `pnpm-lock.yaml` (`lockfileVersion: '9.0'`, `autoInstallPeers: true`) | Reproducible installs |

## 9. Extensibility Points

- New voice provider or model swap: extend `apps/voice`; add the key to `.env.example`, wire the SDK call beside the existing Option A/B legs, and re-run the latency benchmark before updating `docs/adr/001-voice-stack.md`.
- New booking or owner-app endpoint: extend `apps/api` (Fastify routes using its Supabase client); validate payloads with the existing `zod` setup.
- New agent capability: extend the tool contract in `packages/shared` (PRD §14.2 shapes) so `apps/voice` and `apps/api` inherit it through `@pipeline/shared workspace:*` without duplicating schemas.
- New persistent entity or policy: add a migration under `supabase/migrations` following the v1 per-account RLS pattern.
- New owner-app surface: extend `apps/web` (Next.js PWA, Tailwind, `@supabase/ssr`).
- New architecture decision or carrier case: add a record under `docs/adr/` or a row in `docs/forwarding.md` following `001-voice-stack.md` and matrix A5.

## 10. Limitations and Gotchas

- **No live validation yet:** the benchmark has not been run against real API keys and sample audio, and the Option A-vs-B plus Twilio-vs-Telnyx decisions are still open, so no latency or cost claim can be treated as measured (`README:32-36` per `wiki/01-overview.md:11`).
- **Business gates block launch, not code:** US entity filing, Stripe test mode, A2P 10DLC submission, and carrier forwarding verification are outstanding prerequisites for production telephony and billing (`README:32-37` per `wiki/01-overview.md:11,34`).
- **Thin analyzed surface:** the wiki pages available here cover only top-level layout and configuration; per-function behavior in `apps/voice`, `apps/api`, `packages/shared`, and the Supabase migrations is not quotable from these pages, and `pnpm-lock.yaml` beyond the importers block (`pnpm-lock.yaml:101-233`) is truncated, so dependency conclusions stop at direct pins (`wiki/02-top-level-files.md:12,117`).
- **Planning sources are git-excluded:** `spec/`, `PRD.pdf`, `claude.md`, `docs/`, and `apps/voice/qa/results/` are ignored (`.gitignore:1-17`), so a fresh clone without those artifacts loses the roadmap, specs, ADRs, and QA evidence (`.gitignore:13-17` per `wiki/02-top-level-files.md:7,69`).
- **Owner app is a placeholder:** `apps/web` ships no owner functionality until Phase 4, so end-to-end owner workflows cannot be exercised at this state (`README:16` per `wiki/01-overview.md:8`).

## 11. How It Compares to Alternatives

- **Retell AI:** managed voice-agent platform with telephony, low-latency pipeline, and dashboard; PipeLine differs by self-hosting the stack (Fastify, Supabase, pluggable STT/LLM/TTS) and benchmarking Option A against Option B before committing.
- **Vapi:** API-first voice-agent builder with provider abstraction; PipeLine differs by narrowing to one vertical (solo plumbing shops) and co-owning the booking data model in Supabase rather than treating voice as a standalone widget.
- **Bland AI:** hosted phone-call automation with batch and inbound flows; PipeLine differs by keeping the tool contract (`packages/shared`, PRD §14.2) inside the same monorepo as the booking API, so voice actions and owner-app actions share one schema.
- **Housecall Pro / Jobber:** field-service SaaS with scheduling, dispatch, and payments but no AI phone-office core; PipeLine positions as the call-answering front end that could sit ahead of such systems, with Lemon Squeezy staged as its own merchant-of-record path.

Positioning: PipeLine is a vertical, self-hosted AI receptionist scaffold for solo plumbers rather than a general voice-agent platform or a full field-service suite; its differentiator at this state is the single shared tool contract plus the explicit Option A/B and carrier benchmark before any vendor commitment.

## Appendix: Selected Code Snippets

1. Environment template (`.env.example`, full placeholder set):

```
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_ANON_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_TEST_NUMBER=
TELNYX_API_KEY=
OPENAI_API_KEY=
DEEPGRAM_API_KEY=
ANTHROPIC_API_KEY=
CARTESIA_API_KEY=
ELEVENLABS_API_KEY=
SENTRY_DSN=
POSTHOG_API_KEY=
POSTHOG_HOST=https://app.posthog.com
LEMONSQUEEZY_API_KEY=
LEMONSQUEEZY_STORE_ID=
LEMONSQUEEZY_WEBHOOK_SECRET=
NODE_ENV=development
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
```

2. Setup gate (`README:24-28`):

```
cp .env.example .env   # fill in real keys before running anything live
pnpm install
pnpm typecheck && pnpm lint && pnpm test
```

3. Lint config (`.eslint.config.js:4-17`):

```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { ignores: ["**/dist/**", "**/.next/**", "**/node_modules/**"] },
  { rules: { "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }] } },
);
```

4. Shared TypeScript baseline (`tsconfig.base.json:1-11`):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true
  }
}
```
