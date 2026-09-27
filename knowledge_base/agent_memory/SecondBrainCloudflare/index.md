---
type: index
title: rahilp/second-brain-cloudflare
description: Folder index for the Second Brain Cloudflare Worker research — summary, digest, explainer, critical analysis, retrieval questions, and wiki pages.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:15:38Z
sources:
  - id: original
    resource: https://github.com/rahilp/second-brain-cloudflare
  - id: local-copy
    resource: source/source.md
tags: [cloudflare-workers, mcp, semantic-memory, d1-vectorize, personal-knowledge-management]
---

# rahilp/second-brain-cloudflare

Second Brain is a persistent semantic memory layer running as a Cloudflare Worker (D1, Vectorize, Workers AI, KV) so every MCP-compatible AI tool shares one personal-plus-team store. Memories stay private by default and reach the team only as deliberately moved canonical entries, with recall by meaning plus full-text relevance ranking. Start with the summary, then the digest, then the wiki pages for deployment and configuration detail.

## How to work through this

1. Read [summary.md](summary.md) (~2 min) for the full technical picture: architecture, memory model, pipeline, tools, and limits.
2. Read [digest.md](digest.md) (~10 min) for the compressed per-page brief plus the five-move system narrative.
3. Work through the wiki pages in order for grounded detail, then [explainer.md](explainer.md) for plain language, [critical_thinking.md](critical_thinking.md) for claims-vs-evidence, and [questions.md](questions.md) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — full technical analysis (architecture, pipeline, tools, deps, gotchas).
- [Digest](digest.md) — per-page compressed brief with verbatim key points and five-move narrative.
- [Explainer](explainer.md) — plain-language introduction for non-specialists.
- [Critical thinking](critical_thinking.md) — claims vs. evidence and open risks.
- [Questions](questions.md) — retrieval-practice questions with answers covering every wiki page.

## Wiki

| Page | Covers |
| --- | --- |
| [01](wiki/01-overview.md) | Repo overview: positioning, Team Edition layers, Worker architecture, capture/organize/recall pipeline, memory-tool table, projects axes, Prompt Capsules |
| [02](wiki/02-top-level-files.md) | Root config: wrangler.jsonc bindings and five crons, secrets template, git hygiene, packaging, TypeScript and vitest harness |

## Original Source

- Upstream repository: [rahilp/second-brain-cloudflare](https://github.com/rahilp/second-brain-cloudflare)
- Local copy: [source/source.md](source/source.md)
