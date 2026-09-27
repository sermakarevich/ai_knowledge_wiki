[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## What is OpenViking
OpenViking replaces black-box agent memory ("text goes in, embeddings come out") with an inspectable virtual filesystem under `viking://` (README.md:45). Agents use file operations (`ls`, `tree`, `read`, `write`, `grep`) and humans can open any directory to inspect and edit what the agent knows (README.md:45). A browser-based [OpenViking Studio](https://openviking.ai/studio) allows browsing context and trying semantic search with no installation (README.md:54).
## Context model (`viking://`)
Resources, per-user memories/resources/skills, and peer contexts are laid out as filesystem subtrees, each with a `viking://` URI for browsing and retrieval (README.md:60). Verbatim layout from the chunk (README.md:68-88):
```
viking://
├── resources/              # Resources: project docs, repos, web pages, etc.
│   └── my_project/
│       ├── docs/
│       │   ├── api/
│       │   └── tutorials/
│       └── src/
└── user/
    └── {user_id}/
        ├── memories/
        │   └── preferences/
        │       ├── writing_style
        │       └── coding_habits
        ├── resources/
        │   └── private_project/
        ├── skills/
        │   ├── search_code
        │   └── analyze_data
        └── peers/
            └── web-visitor-alice/
```
The four value propositions are scoped search, summary-before-source, sessions-as-files, and the unified filesystem (README.md:60-63).
## Loading tiers L0/L1/L2
Three loading tiers control how much an agent reads (README.md:90-94):
| Tier | Name | Purpose |
|---|---|---|
| L0 | Abstract | one-sentence summary for quick relevance checks |
| L1 | Overview | core information and usage scenarios for planning |
| L2 | Details | full original data, read only when needed |
Semantically processed directories carry `.abstract.md` (L0) and `.overview.md` (L1) files alongside L2 content (README.md:96-108). Verbatim example (README.md:99-108):
```
viking://resources/my_project/
├── .abstract.md           # L0: quick relevance check
├── .overview.md           # L1: structure and key points
└── docs/
    ├── .abstract.md
    ├── .overview.md
    └── api/
        ├── auth.md         # L2: full content, loaded on demand
        └── endpoints.md
```
## Proof it works
Version 0.3.22 was evaluated on long-conversation user memory (LoCoMo) and multi-turn agent tasks (tau2-bench); reproduction scripts live in `./benchmark` (README.md:114). The memory evaluation used Doubao 2.0 Pro as the VLM and Doubao-embedding-vision-251215 as the embedding model (README.md:116). Reported results (README.md:123-124):
- User memory (LoCoMo): all three agent integrations at 80–83% accuracy vs 24–57% native, with input tokens down 34.3–91.0% and query latency down 58.45–66.10%.
- Agent experience (tau2-bench): experience memory lifts task success by +6.87pp (retail) and +11.87pp (airline).
## Quick start
Prerequisites: Python 3.10+ and access to an embedding model and a VLM, cloud or local (README.md:130). Verbatim setup (README.md:133-137):
```bash
pip install openviking --upgrade
openviking-server init      # configure providers and models
openviking-server doctor    # check configuration and connectivity
openviking-server           # start the server
```
`init` writes `~/.openviking/ov.conf`; supported options include Volcengine, OpenAI, Codex OAuth, Kimi, GLM, and local Ollama (README.md:139). The package includes the `ov` CLI; verbatim usage (README.md:144-154):
```bash
ov status
ov add-resource https://github.com/volcengine/OpenViking


# Replace TASK_ID with the returned task_id; repeat until status is completed
ov task status TASK_ID
ov ls viking://resources/
ov tree viking://resources/volcengine -L 2
ov find "what is openviking"
ov grep "openviking" --uri viking://resources/volcengine/OpenViking/docs/en
```
`ov find` returns matching context with inspectable URIs; SDKs exist for Python, Go, and TypeScript plus an HTTP API (README.md:156-158). Note: the chunk is truncated mid-table at line 201 (`<td align="cente`), so the full agent-integration list and the macro-components section (README.md:201-206) were cut and are not covered here.
**Covers:** README.md (What is OpenViking, Why OpenViking, `viking://` layout, L0/L1/L2 tiers, benchmarks, quick start, `ov` CLI); chunk notes truncation at README.md:201-206 (agent-integration table cut off)
