> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
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
---
## Environment template (.env.example)
Verbatim excerpt:
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
| Variable(s) | Purpose noted in chunk (`.env.example:9-47`) |
|---|---|
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY` | Supabase |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_TEST_NUMBER` | Twilio (voice benchmark + apps/api) |
| `TELNYX_API_KEY` | Telnyx (benchmark comparison, PRD Q3) |
| `OPENAI_API_KEY` | Voice AI Option A: realtime speech-to-speech |
| `DEEPGRAM_API_KEY`, `ANTHROPIC_API_KEY`, `CARTESIA_API_KEY`, `ELEVENLABS_API_KEY` | Voice AI Option B: Deepgram STT -> LLM -> TTS |
| `SENTRY_DSN`, `POSTHOG_API_KEY`, `POSTHOG_HOST` | Observability (`POSTHOG_HOST=https://app.posthog.com`) |
| `LEMONSQUEEZY_API_KEY`, `LEMONSQUEEZY_STORE_ID`, `LEMONSQUEEZY_WEBHOOK_SECRET` | Lemon Squeezy (merchant-of-record) |
| `NODE_ENV=development` | Default environment |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | Google API |
## Git ignore (.gitignore)
Verbatim excerpt (`.gitignore:1-17`):
```
node_modules/
dist/
.next/
.env
.env.local
*.log
.DS_Store
coverage/
.turbo/
spec/
PRD.pdf
claude.md
docs/
apps/voice/qa/results/
```
Build/secret entries (`node_modules/`, `dist/`, `.next/`, `.env`, `.env.local`, `*.log`, `.DS_Store`, `coverage/`, `.turbo/`) keep generated and local files out of git; planning entries (`spec/`, `PRD.pdf`, `claude.md`, `docs/`, `apps/voice/qa/results/`) exclude specs and voice QA results.
## Lint config (eslint.config.js)
Verbatim excerpt (`.eslint.config.js:4-17`):
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
Exact parameters: `ignores` covers `**/dist/**`, `**/.next/**`, `**/node_modules/**`; rule `@typescript-eslint/no-unused-vars` is `["warn", { argsIgnorePattern: "^_" }]`.
## Workspace membership (pnpm-workspace.yaml)
Verbatim excerpt (`.pnpm-workspace.yaml:1-3`):
```yaml
packages:
  - "apps/*"
  - "packages/*"
```
Only these two globs define workspace membership.
## Shared TypeScript base (tsconfig.base.json)
Verbatim excerpt (`.tsconfig.base.json:1-11`):
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
## Pinned dependencies (pnpm-lock.yaml, truncated)
`lockfileVersion: '9.0'` with `autoInstallPeers: true` and `excludeLinksFromLockfile: false` (`pnpm-lock.yaml:95-99`); root importer is empty (`.`) (`pnpm-lock.yaml:103`). Visible importer pins:
| Importer | Notable dependencies (specifier → pinned) |
|---|---|
| `apps/api` | `fastify ^5.2.0 → 5.10.0`, `@supabase/supabase-js ^2.47.10 → 2.110.3`, `zod ^3.24.1 → 3.25.76`, `@sentry/node ^8.47.0 → 8.55.2`, `@pipeline/shared workspace:*` (`pnpm-lock.yaml:105-131`) |
| `apps/voice` | `@deepgram/sdk ^3.11.1 → 3.13.0`, `ws ^8.18.0 → 8.21.0`, `zod-to-json-schema ^3.24.1 → 3.25.2` plus shared/supabase/zod (`pnpm-lock.yaml:133-165`) |
| `apps/web` | `next 16.2.10`, `react 19.2.4`, `react-dom 19.2.4`, `@supabase/ssr ^0.5.2 → 0.5.2`, `tailwindcss ^4 → 4.3.2` (`pnpm-lock.yaml:167-208`) |
| `packages/shared` | `web-push ^3.6.7 → 3.6.7`, `@supabase/supabase-js ^2.47.10 → 2.110.3`, `zod ^3.24.1 → 3.25.76` (`pnpm-lock.yaml:210-233`) |
Truncation note: `pnpm-lock.yaml` has 5893 lines but the chunk cuts the `packages:` body after `@esbuild/openbsd-arm64` ("truncated, 186503 more characters"), so per-package integrity/engine entries beyond that point are not covered here.
**Covers:** `.env.example`, `.gitignore`, `eslint.config.js`, `pnpm-lock.yaml` (importers block visible; packages body truncated), `pnpm-workspace.yaml`, `tsconfig.base.json`
