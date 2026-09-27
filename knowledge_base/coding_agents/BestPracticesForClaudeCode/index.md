---
type: Documentation
title: Best practices for Claude Code - Claude Code Docs
description: Anthropic Engineering's best practices for Claude Code — managing context as the scarcest resource, verifying with runnable checks, explore-plan-implement-commit workflow, specific rich prompts, concise CLAUDE.md, and non-interactive claude -p scripting.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-24T05:05:17Z }
sources:
  - id: original
    resource: https://www.anthropic.com/engineering/claude-code-best-practices
  - id: local-copy
    resource: source/source.md
tags: [claude-code, agentic-coding, context-management, prompt-engineering]
---

# Best practices for Claude Code - Claude Code Docs

This folder distills Anthropic Engineering's best-practices guide for Claude Code: treat the context window as the scarcest resource, give Claude a runnable verification check, and separate explore/plan from implementation. Use it to write specific prompts with rich content, keep a concise checked-in CLAUDE.md, and script one-off work with `claude -p`.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[Summary](summary.md)** (~2 min) — the whole guide, shallow: TL;DR, motivation, main ideas, findings.
2. **[Digest](digest.md)** (~10 min) — the whole guide, medium: every section's headline and key points, plus the argument in five moves.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the topic? Start with [the plain-language explainer](explainer.md) instead. Coming back after a break? Read [the digest](digest.md), then [self-test](questions.md) — do not re-read the wiki._

## Read This Folder

- [Summary](summary.md) — rung 1: the whole source, shallow
- [Digest](digest.md) — rung 2: the whole source at medium depth; the file to re-read on review
- [Plain-Language Explainer](explainer.md) — no-jargon explanation, applications, conclusions
- [Critical Analysis](critical_thinking.md) — claims vs. evidence, applicability, what it changes, verdict
- [Retrieval Practice](questions.md) — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [01](wiki/01-documentation-index.md) | Documentation index pointer and context-window constraint framing the guide |
| [02](wiki/02-claude-md-code-style-and-workflow.md) | CLAUDE.md code-style rules and workflow conventions (typecheck, focused test runs) |
| [03](wiki/03-non-interactive-mode-output-formats.md) | Non-interactive `claude -p` one-off queries with text, JSON, and streaming JSON output |

## Original Source

- [Best practices for Claude Code - Claude Code Docs](https://www.anthropic.com/engineering/claude-code-best-practices) — the original Anthropic Engineering article this folder summarizes
- [Local copy](source/source.md) — full retrieved source text used by the other workers in this folder
