> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repository root defines packaging, build, distribution, and agent-integration metadata for the `@docsagent/mcp-zotero` 4.0.0 package rather than runtime logic.
## Key points
- The root package is named `@docsagent/mcp-zotero` at version `4.0.0` with license `Apache-2.0` and `lockfileVersion: 3` (`package-lock.json:21-30`).
- The published CLI entry is the `docsagent` bin mapped to `dist/cli.js`, requiring Node `>=18` (`package-lock.json:35-44`).
- Runtime dependencies are only `@modelcontextprotocol/sdk@^1.29.0` and `ajv@^8.17.0`, with `tsup@^8.0.0` and `typescript@^5.0.0` as devDependencies (`package-lock.json:31-41`).
- TypeScript compiles `src/**/*` to `dist/` with `strict: true`, `target/module/lib` set to `ESNext`/`NodeNext`, and `skipLibCheck: true` (`tsconfig.json:1-17`).
- Build output, dependencies, temp files, and tarballs are excluded from version control via `dist/`, `node_modules/`, `tmp/`, `.qwen/`, `*.tgz`, `.DS_Store` (`.gitignore:1-6`).
- Distribution spans four channels — npm tarball, PyPI wheel/sdist, MCP Registry payload `mcp-registry/server.json`, and Smithery via `smithery.yaml` — plus web-form directory submissions (`PUBLISH.md:1-56`).
- The agent skill contract (`SKILL.md:1-87`) exposes local-first `add` / `search` / `list` / `status` / `stop` CLI workflows over private PDF, PPTX, and DOCX files with no web dependency.
- Smithery launches the server over stdio with `npx -y @docsagent/mcp-zotero` and optional `zoteroDataDir` / `enableWrites` config (`smithery.yaml:1-23`).
---
## .gitignore — untracked paths
Excludes build output and local artefacts from git:
```gitignore
dist/
node_modules/
tmp/
.qwen/
*.tgz
.DS_Store
```
(`.gitignore:1-6`; chunk header reports 7 lines.)
## package-lock.json — package identity and dependency pin
Root package block (`package-lock.json:21-45`):
```json
{
  "name": "@docsagent/mcp-zotero",
  "version": "4.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "@docsagent/mcp-zotero",
      "version": "4.0.0",
      "hasInstallScript": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.29.0",
        "ajv": "^8.17.0"
      },
      "bin": {
        "docsagent": "dist/cli.js"
      },
      "devDependencies": {
        "tsup": "^8.0.0",
        "typescript": "^5.0.0"
      },
      "engines": {
        "node": ">=18"
      }
    }
  }
}
```
Remainder of the file (platform-scoped optional `@esbuild/*` entries such as `@esbuild/aix-ppc64:0.27.7`, `@esbuild/darwin-arm64:0.27.7`, `@esbuild/linux-x64:0.27.7` at `package-lock.json:46-440`) was cut in the chunk: chunk notes `... (truncated, 74946 more characters)` at chunk line 441, so their full contents are not summarised here.
## tsconfig.json — compiler contract
Verbatim (`tsconfig.json:1-17`):
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ESNext"],
    "outDir": "dist",
    "strict": true,
    "declaration": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
```
| Option | Value |
|---|---|
| `target` / `lib` | `ESNext` |
| `module` / `moduleResolution` | `NodeNext` |
| `outDir` | `dist` |
| `include` | `src/**/*` |
| `strict` / `declaration` / `skipLibCheck` / `forceConsistentCasingInFileNames` / `esModuleInterop` / `allowSyntheticDefaultImports` | `true` |
## PUBLISH.md — release channels
Artifact table (`PUBLISH.md:3-9`):
| File | What |
|---|---|
| `docsagent-mcp-zotero-4.0.0.tgz` | npm tarball (includes `bin/` with all-platform core binaries) |
| `python/dist/docsagent_mcp_zotero-4.0.0-py3-none-any.whl` (+ sdist) | PyPI wheel (same bundled core) |
| `mcp-registry/server.json` | official MCP Registry submission payload |
| `smithery.yaml` | Smithery config |
Steps (`PUBLISH.md:11-56`):
1. npm: `npm login` then `npm publish docsagent-mcp-zotero-4.0.0.tgz`; create `@docsagent` scope at `https://www.npmjs.com/org/new` if missing.
2. PyPI: `~/.pypirc` holds only `[testpypi]` credentials; `twine upload --repository testpypi python/dist/*` for validation, `twine upload -u __token__ -p <pypi-token> python/dist/*` for production.
3. MCP Registry (`registry.modelcontextprotocol.io`): publish npm + PyPI first, then submit `mcp-registry/server.json` via `https://github.com/modelcontextprotocol/registry`; name `io.github.docsagent/zotero` verified through the `docsagent` GitHub organization.
4. Smithery: `npx @smithery/cli publish` using `./smithery.yaml`.
5. Directory web forms: PulseMCP (`https://www.pulsemcp.com/submit`), Glama (`https://glama.ai/mcp/servers`), mcp.so (`https://mcp.so`), Cursor directory (`https://cursor.directory/submit`), Cline MCP Marketplace (PR to `cline/mcp-marketplace`).
## SKILL.md — agent-facing skill contract
Frontmatter (`SKILL.md:1-4`):
```yaml
name: docsagent
description: Search and manage private, local document collections (PDF, PPTX, DOCX) offline. Use when you need to find information within your private files, not for web research.
```
Claims: local-first engine doing lightning-fast hybrid (text + semantic) search 100% locally with zero data leakage (`SKILL.md:7-24`); supported formats PDF, PPTX, DOCX (`SKILL.md:19`); install via `npm install -g @docsagent/docsagent` (`SKILL.md:31-33`).
| Command | Purpose |
|---|---|
| `docsagent add ./documents/manuals` (multi-path allowed) | Index folders/files for searchability (`SKILL.md:40-49`) |
| `docsagent search "how to configure local encryption"` | Hybrid search returning snippets with source paths and scores; index via `add` first (`SKILL.md:51-61`) |
| `docsagent list` | List indexed/monitored files (`SKILL.md:63-67`) |
| `docsagent status` | Show indexing progress and service health (`SKILL.md:69-73`) |
| `docsagent stop` | Stop the indexing service (`SKILL.md:75-79`) |
Workflow (`SKILL.md:81-86`): check index → `search` with a query derived from the request → synthesize snippets → cite file path and page number. Error handling (`SKILL.md:88-91`): on "No results found" offer to `add` a directory; on missing path during `add`, verify the path before retrying.
## smithery.yaml — Smithery launch config
Verbatim core (`smithery.yaml:1-23`):
```yaml
startCommand:
  type: stdio
  configSchema:
    type: object
    title: DocsAgent Zotero MCP Server
    description: Search, read, and write a local Zotero library through a resident C++ search engine. The core must be running (docsagent-mcp-zotero core start or the JS CLI equivalent).
    properties:
      zoteroDataDir:
        type: string
        title: Zotero data directory
        description: Path to the Zotero data directory the engine indexes.
        default: ~/Zotero
      enableWrites:
        type: boolean
        title: Enable write tools
        description: Register the write tools (import_item, add_note, batch_modify).
        default: false
  commandFunction: |-
    (config) => ({
      "command": "npx",
      "args": ["-y", "@docsagent/mcp-zotero"],
      "env": config.zoteroDataDir ? { "DOCSAGENT_ZOTERO_DATA_DIR": config.zoteroDataDir } : {}
    })
```
| Parameter | Type | Default | Effect |
|---|---|---|---|
| `zoteroDataDir` | `string` | `~/Zotero` | Maps to env `DOCSAGENT_ZOTERO_DATA_DIR` when set |
| `enableWrites` | `boolean` | `false` | Registers write tools `import_item`, `add_note`, `batch_modify` |
**Covers:** `.gitignore`, `package-lock.json`, `PUBLISH.md`, `SKILL.md`, `smithery.yaml`, `tsconfig.json`
