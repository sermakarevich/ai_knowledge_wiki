---
type: Video
title: Build-Time vs. Run-Time: Why Dev Tools Fail in Production
description: A Google MCP Toolbox talk on why build-time (developer-assistant) database tools are unsafe when reused at runtime, and how to progressively harden agent tools into a zero-trust design.
generated: { by: claude/claude-sonnet-5, at: 2026-09-09T18:20:00Z }
sources:
  - id: original
    resource: https://www.youtube.com/watch?v=9R--1tg45Jg&list=PLcfpQ4tk2k0X1DNKK3SyZ2Qbl3QxBfHr3
  - id: local-copy
    resource: source/transcript.md
tags: [mcp, agent-tools, ai-security, database-security, tool-design]
---

# Build-Time vs. Run-Time: Why Dev Tools Fail in Production

A ~20-minute AI Engineer conference talk by Averi Kitsch and Prerna Kakkar (Google), the tech leads behind MCP Toolbox for Databases and Eval Bench. The central claim: tools built for a developer to drive interactively (build-time) are dangerous when handed to an autonomous agent in production (runtime), and the fix is a step-by-step hardening path — from a fully model-controlled superuser tool down to a "zero trust" tool that only accepts a single harmless parameter.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-mcp-toolbox-background\|MCP Toolbox Background & Tool Patterns]] | Speaker intros, MCP Toolbox for Databases history/stats, and the three common database tool patterns (control-plane, NL2SQL, structured SQL) |
| [[wiki/02-build-time-vs-runtime\|Build-Time vs. Runtime Tools]] | The core distinction, the table-deletion failure demo, and the (failed-to-load) runtime travel-chatbot demo |
| [[wiki/03-security-guardrails\|Security Guardrails: From Confused Deputy to Zero Trust]] | Confused deputy attack, the lethal trifecta, identity/parameter separation, and the step-by-step tool-hardening evolution |
| [[wiki/04-tool-quality-best-practices\|Tool-Quality Best Practices]] | Outcome-focused tools, lean descriptions, read/write separation, actionable errors, simple inputs, and closing pointers (docs, GitHub, Eval Bench) |

## Original Source

- [source/transcript.md](source/transcript.md) — full timestamped transcript, retrieved 2026-09-09
