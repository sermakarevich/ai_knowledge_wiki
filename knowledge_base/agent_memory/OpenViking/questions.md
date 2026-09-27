---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: volcengine/OpenViking

### Q1. What is OpenViking and how do agents and humans interact with its context?
> [!tip]- Answer
> OpenViking is an open-source context database for AI agents that unifies knowledge, memory, and skills as one browsable virtual filesystem under `viking://`. Agents work it with file operations (`ls`, `tree`, `read`, `write`, `grep`) while humans can open any directory to inspect and edit what the agent knows, including via OpenViking Studio in the browser. See [[wiki/01-overview|Overview]].

### Q2. How is the `viking://` filesystem organized and how does scoped retrieval differ from a flat vector pool?
> [!tip]- Answer
> The filesystem holds three context types — resources (documents/code), memories (preferences/experience), and skills (task procedures) — laid out as subtrees such as `resources/my_project/` and `user/{user_id}/{memories, resources, skills, peers}`, each addressable by a `viking://` URI. Retrieval is scoped to a directory subtree, where `find` runs a query directly and `search` plans retrieval from session context. See [[wiki/01-overview|Overview]].

### Q3. What are the L0/L1/L2 loading tiers and what happens when a session is committed or compiled?
> [!tip]- Answer
> Directories carry generated summaries so agents scan before reading: L0 Abstract for one-sentence relevance checks, L1 Overview for structure and usage planning, and L2 Details for full content loaded only on demand via `.abstract.md` / `.overview.md` files. Committing a session archives the conversation and extracts inspectable Markdown memories, while `ov compile` organizes source material into a wiki, knowledge graph, or report when VikingBot is enabled. See [[wiki/01-overview|Overview]].

### Q4. What benchmarks justify OpenViking and what is the minimal quick-start setup?
> [!tip]- Answer
> Version 0.3.22 was evaluated on LoCoMo (long-conversation memory) and tau2-bench (multi-turn tasks), reaching 80–83% memory accuracy versus 24–57% native and lifting task success by +6.87pp retail / +11.87pp airline, with repro scripts in `./benchmark`. Quick start needs Python 3.10+ plus an embedding model and a VLM, installed via `pip install openviking` and configured with `openviking-server init` (writes `~/.openviking/ov.conf`) and `doctor`, then used through the `ov` CLI and Python/Go/TypeScript SDKs. See [[wiki/01-overview|Overview]].

### Q5. What do the root formatting, ignore, packaging, and proxy files enforce?
> [!tip]- Answer
> `.clang-format` pins C++ style to Google base with width 2 and an 80-column limit; `.dockerignore` and the 251-line `.gitignore` keep build contexts and the repo clean, excluding artifacts plus OpenViking paths like `/data/*` and `.openviking/media/`. `MANIFEST.in` grafts `src`, vendored `third_party/*`, and `crates/ragfs*` into a source-only sdist while pruning binaries, and the `Caddyfile` keeps only a legacy `:1934` reverse-proxy while new deployments use port 1933 with Studio at `/studio`. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. How are PR review, contributions, releases, and security handled at the repository root?
> [!tip]- Answer
> The 355-line `.pr_agent.toml` configures Qodo PR-Agent with a Doubao code model, 8 max findings, OpenViking custom labels, and rules R1–R11 covering async discipline, memory completeness, and API compatibility. Chinese/Japanese `CONTRIBUTING` mirrors route modules to owners and require small Conventional-Commit PRs, `RELEASE.md`/`RELEASE_CN.md` define tag conventions (`vX.Y.Z`, `python-sdk@`, `cli@`, ClawHub dates) across many artifacts, and 12-line `SECURITY.md` routes reports privately to the ByteDance security center. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Should a team running file-centric coding agents adopt OpenViking for shared project memory, and why?
> [!tip]- Answer
> Yes, if the team needs inspectable, scoped agent memory rather than a black-box vector store, because the `viking://` filesystem with L0/L1 summaries plus archived session memories fits browse-then-read agent workflows and shows strong LoCoMo and tau2-bench gains. The trade-off is operational cost — embedding model plus VLM, server setup, and a polyglot release surface — so a team without persistent-memory needs should defer adoption. See [[wiki/01-overview|Overview]].
