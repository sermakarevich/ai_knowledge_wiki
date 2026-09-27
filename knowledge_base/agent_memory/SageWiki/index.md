---
type: index
title: xoai/sage-wiki — folder index
description: Index to the sage-wiki knowledge-base summary, digest, wiki pages, explainer, critical analysis, and retrieval questions.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:04:55Z
sources:
  - id: original
    resource: https://github.com/xoai/sage-wiki
  - id: local-copy
    resource: source/source.md
tags: [knowledge-graph, mcp, rag, obsidian, go]
---

# xoai/sage-wiki

sage-wiki is a graph memory and knowledge base where an LLM compiler turns dropped-in documents into an interlinked markdown wiki plus an opt-in evidenced knowledge graph. Agents query the same data through 19 MCP tools while humans browse it as Obsidian-native markdown via a TUI and web UI. This folder holds the summary, digest, two wiki pages, plain-language explainer, critical analysis, and retrieval questions for the repo.

## How to work through this

1. Start with [summary](summary.md) (~2 min) for the full technical picture: architecture, evidenced graph, compile pipeline, files, dependencies, CLI, and limitations.
2. Move to [digest](digest.md) (~10 min) for the compressed per-page takeaways plus the five-move system narrative.
3. Go deep in the wiki pages ([01-overview](wiki/01-overview.md), [02-top-level-files](wiki/02-top-level-files.md)) for grounded detail, then check [explainer](explainer.md) for plain language, [critical thinking](critical_thinking.md) for claims-vs-evidence scrutiny, and [questions](questions.md) for retrieval practice.

## Read This Folder

- [summary](summary.md) — full technical analysis (overview, architecture, graph, pipeline, files, deps, CLI, extensibility, gotchas).
- [digest](digest.md) — compressed per-page takeaways with verbatim key points and the five-move narrative.
- [explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works, where to use it, jargon decoder.
- [critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, weaknesses, applicability, verdict (trial).
- [questions](questions.md) — seven retrieval-practice Q&As covering both wiki pages.

## Wiki table

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README.md (purpose, graph memory, guides index, install/quickstart, source-format table truncated at CSV row); docs/translations, docs/guides, docs/webhooks.md, docs/security.md, CONTRIBUTING.md as referenced |
| [02-top-level-files](wiki/02-top-level-files.md) | .dockerignore, .gitattributes, .gitignore, .golangci.yml, go.sum (truncated in chunk), integration_test.go (TestIntegrationM1) |

## Original Source

- Upstream repo: [xoai/sage-wiki on GitHub](https://github.com/xoai/sage-wiki)
- Local copy: [source/source.md](source/source.md)
