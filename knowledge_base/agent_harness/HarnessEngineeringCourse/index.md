---
type: Codebase
title: HarnessEngineeringCourse
description: A 15-chapter Python teaching codebase (harnessengineering) where each chapter introduces one agent-harness primitive — model seam, instructions, context delivery, tools/approval, compaction, skills, sandbox, memory, orchestration, subagents, verification, observability, TUI — gated by an offline `verify` check plus a live-model `accept` check per chapter.
generated: { by: claude, at: 2026-09-12T07:05:00Z }
sources:
  - id: original
    resource: https://github.com/Satish137-GS/harnessengineering
  - id: local-copy
    resource: source/provenance.md
tags: [agent-harness, python, coding-agent, teaching, observability, sandbox]
---

# HarnessEngineeringCourse

**Repository:** https://github.com/Satish137-GS/harnessengineering @ edac4be

HarnessEngineeringCourse is a 15-chapter Python course (`ch-00` through `ch-14`) built around one thesis: the model only ever asks, the harness decides and executes. Each chapter adds exactly one primitive owned by one module — provider seam, conversation history, project instructions, `@path` context delivery, tools with an approval gate, tool-safe compaction, progressively disclosed skills, a hardened sandbox, durable JSON-L memory, a plan-gate-execute orchestrator, isolated subagents, nonce-guarded code verification, dual-shape (flat event + OTel span) observability, and a Textual TUI — and every chapter must clear two gates: an offline deterministic `verify` (ruff, mypy, pytest, smoke import) and a live-model `accept ch-NN`.

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
| [[wiki/01-agent-core\|Agent loop, context delivery, instructions]] | The `Agent` class drives a tool-calling chat loop over layered instructions, injected `@path` file context, and a confined workspace. |
| [[wiki/02-model-seam\|Model seam, fake provider, pricing]] | The free `chat()` function is the sole model entry point, dispatched by `Provider` config to an OpenAI-compatible HTTP path or a deterministic fake responder. |
| [[wiki/03-memory-skills\|Memory, compaction, limits, skills]] | Durable JSON-L session memory with keyword recall, middle-summarizing tool-safe compaction, per-item clamp limits, and progressively disclosed file-based skills. |
| [[wiki/04-execution\|Sandbox, orchestrator, subagents, verification]] | Sandboxed shell commands, planned-and-gated multi-step runs, parallel subagents, and nonce-guarded code verification. |
| [[wiki/05-observability-ui\|Observability, events, TUI]] | A dual-shape trace (flat `Event` plus OTel GenAI span tree) feeding a Textual two-pane terminal UI and pure print renderers. |
| [[wiki/06-gates-course\|Two-gate verification and course map]] | The offline `verify` / live-model `accept` two-gate rule, and the 15-chapter primitive-to-module map. |

## Original Source

- [source/provenance.md](source/provenance.md) — provenance pin (commit edac4be, shallow clone, 2026-09-11), local read-only clone at `/tmp/harnessengineering`
- [source/delegation_report.md](source/delegation_report.md) — extraction/verify/synth delegation trail
