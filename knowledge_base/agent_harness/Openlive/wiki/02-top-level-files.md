> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root defines a pnpm monorepo (`apps/*`, `packages/*`, `services/*`) with shared TypeScript strictness, one pinned `@huggingface/transformers` copy, a single root test runner, and tag-driven releases.
## Key points
- The monorepo layout is `packages/*`, `apps/*`, and `services/*` workspaces declared in `pnpm-workspace.yaml:438-441`.
- Exactly one `@huggingface/transformers` copy (4.2.0) is forced across the tree via `overrides` in `pnpm-workspace.yaml:443-446` and `pnpm-lock.yaml:44-45` to avoid two clashing onnxruntime envs and segfaults.
- Native-module builds are allow-listed (`electron`, `electron-builder`, `esbuild`, `onnxruntime-node`, `protobufjs`, `sharp`) while `electron-winstaller` is explicitly disabled in `pnpm-workspace.yaml:449-457`.
- All packages share one strict base config: `ES2022` target, `Bundler` module resolution, `strict: true` plus `noUncheckedIndexedAccess: true` in `tsconfig.base.json:500-511`.
- One root vitest runner executes every package's colocated tests via `include: ["{apps,services,packages}/*/src/**/*.test.ts"]` with `environment: "node"` in `vitest.config.ts:527-529`.
- Releases are one tag with no manual version bump (`git tag v0.2.0 && git push origin v0.2.0`), and CI typechecks every push/PR then builds macOS/Windows/Linux installers from the tag in `RELEASING.md:481-489`.
- Generated, secret, and large/binary artifacts are never committed: `node_modules`, `.next`, `dist`, `data`, `.env`, `*.log`, `*.tsbuildinfo`, `release/`, `*.mp4`, and vendored `apps/web/public/vad/` are ignored in `.gitignore:9-30`.
---
## Build ignores (`.gitignore`)
Verbatim entries (`.gitignore:9-30`):
```
node_modules
.next
dist
data
.env
.DS_Store
*.log
*.tsbuildinfo
next-env.d.ts
release/
apps/desktop/dist/
*.mp4
apps/web/public/vad/
assets/milestone-200.png
assets/milestone-200.svg
```
`*.mp4` is excluded because demo videos are hosted as GitHub assets, not committed (100MB limit + no inline playback) (`.gitignore:25`); `apps/web/public/vad/` is excluded because it is vendored voice-runtime assets copied from `node_modules` by `copy-voice-assets.mjs` (`.gitignore:28`).
## Workspace layout and dependency pinning (`pnpm-workspace.yaml`, `pnpm-lock.yaml`)
`pnpm-workspace.yaml:438-446`:
```
packages:
  - "packages/*"
  - "apps/*"
  - "services/*"
overrides:
  "@huggingface/transformers": "4.2.0"
```
The override comment states the reason verbatim: kokoro-js pulls 3.8.1 while the repo uses 4.2.0 and "two copies = two onnxruntime-node envs that clash and segfault" (`pnpm-workspace.yaml:443-444`).

| Setting | Value |
|---|---|
| `lockfileVersion` | `'9.0'` (`pnpm-lock.yaml:38`) |
| `settings.autoInstallPeers` | `true` (`pnpm-lock.yaml:41`) |
| `settings.excludeLinksFromLockfile` | `false` (`pnpm-lock.yaml:42`) |
| `@huggingface/transformers` override | `4.2.0` (`pnpm-lock.yaml:45`) |
| Root dev deps | `concurrently ^9.1.0`, `cross-env ^10.0.0`, `typescript ^5.7.3`, `vitest ^3.2.4` (`pnpm-lock.yaml:50-62`) |

Importers pinned in the lockfile: `apps/desktop` (electron `^43.1.1`, electron-builder `^25.1.8`, esbuild `^0.28.1`) (`pnpm-lock.yaml:64-81`); `apps/web` (next `^16.2.9`, react `^19.2.0`, `kokoro-js ^1.2.0`, `@ricky0123/vad-web ^0.0.29`, `onnxruntime-web ^1.22.0`, workspace links to `@openlive/db`, `@openlive/harness`, `@openlive/shared`) (`pnpm-lock.yaml:83-150`); `packages/db` (`proper-lockfile ^4.1.2`, workspace link to `@openlive/shared`) (`pnpm-lock.yaml:171-178`); `packages/shared` (`zod ^3.24.1`) (`pnpm-lock.yaml:202-206`); `services/agent` (`hono ^4.12.27`, `@hono/node-server ^1.13.8`, `sherpa-onnx-node ^1.13.4`, `tar ^7.5.20`, workspace links to all three `@openlive/*` packages) (`pnpm-lock.yaml:212-255`).
> Note: `pnpm-lock.yaml` content in the source chunk was truncated after the `packages:` section header (chunk line 432, "206824 more characters" remaining), so per-package resolution entries beyond that point are not covered here.
## Native builds and release-age guard (`pnpm-workspace.yaml`)
Verbatim allow-list (`pnpm-workspace.yaml:449-457`):
```
allowBuilds:
  electron: true
  electron-builder: true
  electron-winstaller: false
  esbuild: true
  onnxruntime-node: true
  protobufjs: true
  sharp: true
```
`electron-winstaller` is skipped with the comment "Squirrel.Windows binary fetcher — unused (we ship NSIS), skip its build script" (`pnpm-workspace.yaml:452`). `minimumReleaseAgeExclude` exempts `@anthropic-ai/sdk@0.107.0`, `@tailwindcss/node@4.3.2`, eight `@tailwindcss/oxide-*@4.3.2` platform builds, `@tailwindcss/postcss@4.3.2`, and `tailwindcss@4.3.2` (`pnpm-workspace.yaml:459-471`).
## Shared TypeScript base (`tsconfig.base.json`)
Verbatim (`tsconfig.base.json:499-516`):
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
## Test runner (`vitest.config.ts`)
Verbatim (`vitest.config.ts:522-531`):
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
## Releasing (`RELEASING.md`)
Maintainer-only notes, "not linked from the README on purpose" (`RELEASING.md:479`). Release command verbatim (`RELEASING.md:483-485`):
```bash
git tag v0.2.0 && git push origin v0.2.0
```
"The tag drives the version. CI builds the macOS (universal, signed and notarized), Windows, and Linux (unsigned AppImage) installers on their native runners, uploads them, and publishes the release with all three downloads" (`RELEASING.md:487-489`). Mac signing runs only when repo secrets `MAC_CSC_LINK`, `MAC_CSC_KEY_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID` are set, with details in `apps/desktop/README.md` (`RELEASING.md:491-493`).
**Covers:** `.gitignore`, `pnpm-lock.yaml` (importers section; packages resolution section truncated in source), `pnpm-workspace.yaml`, `RELEASING.md`, `tsconfig.base.json`, `vitest.config.ts`
