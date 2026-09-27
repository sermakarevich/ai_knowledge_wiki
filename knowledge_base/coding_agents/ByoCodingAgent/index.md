---
type: Codebase
title: ByoCodingAgent
description: ByoCodingAgent (byo-coding-agent) is a small, teachable Go coding-agent harness — agent loop, provider seam (Anthropic/OpenAI/mock), compaction, session memory, MCP tool bridge, and a Bubble Tea TUI — wrapped in a bilingual course of lessons, recipes, and graded exercises.
generated: { by: claude, at: 2026-09-12T06:57:00Z }
sources:
  - id: original
    resource: https://github.com/betta-tech/byo-coding-agent
  - id: local-copy
    resource: source/provenance.md
tags: [agent-harness, go, coding-agent, mcp, teaching, tui]
---

# ByoCodingAgent

**Repository:** https://github.com/betta-tech/byo-coding-agent @ 77aa4db

ByoCodingAgent is a small, teachable coding-agent harness written in Go: a single `Agent` runs a Send→loop tool-use cycle capped by `MaxTurns`, talking to LLMs only through a narrow `Provider` interface (Anthropic, OpenAI, or a scripted mock), trimming context per-turn with a tool-pair-safe compaction strategy, persisting session summaries to markdown, bridging local tools and remote MCP servers into one registry with diff-gated writes, and presenting it all through a Bubble Tea terminal UI. Around the ~7k-line codebase sits a bilingual (English/Spanish) course — a 20-chapter narrative, three copy-paste recipes, and six graded exercises — that teaches harness engineering by having the reader extend this exact codebase.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~N min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-agent-loop\|Agent loop and entrypoint]] | The root `Agent` runs a `Send`→`loop` tool-use cycle capped by `MaxTurns`, wired in `main.go` to a Bubble Tea runner that routes `/`-commands inline and everything else into the loop. |
| [[wiki/02-provider\|Provider seam: Anthropic/OpenAI/mock]] | The `Provider` interface (`Send`/`Model`/`SetModel`) decouples the agent loop from LLM backends, with `AnthropicProvider` and `OpenAIProvider` translating generic messages/tools to vendor SDK calls plus per-model cost tracking, and `MockProvider` serving canned responses for tests. |
| [[wiki/03-compaction-memory\|Compaction strategies and session memory]] | Short-term context is truncated per-turn by a `CompactionStrategy` snapped to tool-pair-safe boundaries, while long-term context persists across sessions through a `memory.Store` whose default file-backed implementation writes one markdown file per session plus a JSON index. |
| [[wiki/04-tools-mcp\|Tool surface, diffs, MCP client]] | External MCP servers are bridged into the agent's local tool registry with per-server clients, and shared types plus a unified-diff preview define the common tool surface. |
| [[wiki/05-ui\|TUI: program, input, styles, compaction view]] | The `internal/ui` package implements the Bubble Tea terminal UI — a `harness` model with conversation viewport, input box, debug panel, approval modals, banner animation, and stdout helpers for spinner, highlight, and compaction views. |
| [[wiki/06-course-map\|Course structure: lessons, exercises, how-tos]] | The repo teaches harness engineering through three parallel tracks — a 20-chapter narrative (`follow_along/`), three copy-paste recipes (`how-to/`), and six graded extension exercises (`exercises/`), all bilingual in English and Spanish. |

## Original Source

- [source/provenance.md](source/provenance.md) — provenance pin (commit 77aa4db, shallow clone, 2026-09-11), local read-only clone at `/tmp/byo-coding-agent`
- [source/delegation_report.md](source/delegation_report.md) — extraction/verify/synth delegation trail
