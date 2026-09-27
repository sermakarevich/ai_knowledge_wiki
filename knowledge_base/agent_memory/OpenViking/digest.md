> [[index|Wiki]] | [[summary|Summary]]
# volcengine/OpenViking — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** OpenViking is an open-source context database for AI agents that organizes knowledge, memory, and skills as a browsable virtual filesystem under `viking://` with layered summaries and scoped semantic search.
## Key points
- OpenViking is "an open-source context database for AI agents — one filesystem for everything an agent knows: knowledge, memory, and skills" (README.md:43).
- Context is navigated like files — `ls`, `tree`, `read`, `write`, `grep` — under `viking://`, and every directory carries a generated summary for scan-before-read (README.md:45).
- One filesystem holds three context types: resources (documents/code), memories (preferences/experience), and skills (task procedures), each addressable by a `viking://` URI (README.md:60).
- Retrieval is scoped to a directory subtree: `find` runs a query directly while `search` plans retrieval from session context, instead of scanning a flat vector pool (README.md:61).
- Directories carry generated abstracts (L0) and overviews (L1) so agents judge relevance before opening full content (L2) (README.md:62, README.md:92-94).
- Committing a session archives the conversation and extracts inspectable/editable Markdown memories, and `ov compile` organizes source material into a wiki, knowledge graph, or report when VikingBot is enabled (README.md:63).
- Evaluated on LoCoMo and tau2-bench, OpenViking integrations reach 80–83% memory accuracy (from 24–57% native) and lift agent task success by +6.87pp retail / +11.87pp airline (README.md:114, README.md:123-124).
- Quick start requires Python 3.10+ plus an embedding model and a VLM, installed via `pip install openviking` and configured with `openviking-server init` / `doctor` (README.md:130, README.md:133-139).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repository root defines code formatting, build/sync ignore rules, packaging, legacy proxy entrypoint, PR-review automation, contribution/release/security policy, and the multilingual project front door.
## Key points
- `.clang-format` pins C++ style to Google base with `IndentWidth: 2`, `ColumnLimit: 80`, and `PointerAlignment: Left` (`.clang-format:1-9` [chunk:9-36]).
- `.dockerignore` keeps the build context small by excluding `.git`, `__pycache__`, `target/`, `node_modules`, and `web-studio/dist` (`.dockerignore:3-16` [chunk:48-63]).
- `.gitignore` (251 lines) excludes Python/Rust/Node artifacts plus OpenViking-specific paths `/data/*`, `.openviking/media/`, `.openviking/downloads/`, and `.beads/` / `.loopx/` state (`.gitignore:207-218,310-317` [chunk:207-218,310-317]).
- `.gitattributes` marks only directory-installed memory-plugin shared copies as `linguist-generated=true`, while the rest are built at pack time and gitignored (`.gitattributes:4-6` [chunk:74-76]).
- `MANIFEST.in` grafts `src`, vendored `third_party/*`, and `crates/ragfs*` into the sdist while pruning `openviking/bin`, `openviking/lib`, and all `*.so/*.dylib/*.dll/*.exe` binaries (`MANIFEST.in:1-12` [chunk:1182-1204]).
- `Caddyfile` retains only a `:1934` legacy reverse-proxy to `openviking:{$OPENVIKING_SERVER_PORT:1933}` and directs new deployments at port 1933 plus `/studio` (`Caddyfile:23-25` [chunk:613-615]).
- `.pr_agent.toml` (355 lines) configures Qodo PR-Agent with `model = "openai/doubao-seed-2-0-code-preview-260215"`, 8 max findings, and OpenViking-specific custom labels and review rules (`.pr_agent.toml:6-24` [chunk:355-373]).
- `README_CN.md` / `README_JA.md` (337 lines each), `CONTRIBUTING_CN.md` (267 lines) / `CONTRIBUTING_JA.md` (286 lines), `RELEASE.md` (196 lines) / `RELEASE_CN.md` (184 lines), and `SECURITY.md` (12 lines) carry the project pitch, contributor routing, multi-artifact release flows, and private security reporting path (`README_CN.md:1-5`, `RELEASE.md:1-13`, `SECURITY.md:1-2` [chunk:1211-1223,1656-1675,2044-2046]).

## The system in five moves
1. OpenViking reframes everything an agent knows — documents, memories, skills — as one browsable `viking://` filesystem worked with file operations instead of a black-box vector pool.
2. Retrieval stays scoped to a directory subtree and tiered through L0 abstracts and L1 overviews before full L2 content is ever opened.
3. Sessions become files: conversations archive into inspectable Markdown memories, and source material compiles into wikis, knowledge graphs, or reports.
4. Benchmarks justify the shape, with LoCoMo memory accuracy at 80–83% and tau2-bench task lifts in retail and airline.
5. The repository root enforces the engineering shell around that system — formatting, ignore rules, source-only packaging, and the legacy proxy entrypoint.
6. Project governance closes the arc — PR-review automation, contribution routing, multi-artifact releases, private security reporting, and the multilingual front door.
