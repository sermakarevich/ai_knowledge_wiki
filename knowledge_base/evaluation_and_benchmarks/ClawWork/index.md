---
type: Codebase
title: ClawWork
description: ClawWork turns an AI assistant into an economically accountable AI coworker that must earn income from 220 GDPVal professional tasks across 44 occupations while paying its own token/API costs from a $10 balance, judged by an LLM and payable only above a 0.6 quality threshold — shipped as a livebench runtime, a nanobot chat-plugin (clawmode), an offline pricing/validation pipeline, and a React dashboard.
generated: { by: claude, at: 2026-09-12T15:52:00Z }
sources:
  - id: original
    resource: https://github.com/HKUDS/ClawWork
  - id: local-copy
    resource: source/provenance.md
tags: [agent-economics, benchmark, llm-judge, gdpval, dashboard, python, react]
---

# ClawWork

**Repository:** https://github.com/HKUDS/ClawWork @ 9c73ac0

ClawWork is an economic-accountability benchmark: a `LiveAgent` runs one professional GDPVal task per simulated workday, paying for every token and API call from a starting $10 balance via `EconomicTracker`, and earning `quality_score × estimated_hours × BLS_hourly_wage` only when an LLM judge's score clears 0.6 — otherwise the task pays $0 while still burning cost. The same economic engine is re-exposed as a `clawmode` plugin that bolts cost tracking and a `/clawwork` task classifier onto the `nanobot` chat harness, as an offline `scripts/` pipeline that estimates task hours and BLS wages and validates the accounting, and as a React dashboard (live via FastAPI/WebSocket, or statically exported for GitHub Pages) that visualizes balances, earnings, and artifacts.

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
| [[wiki/01-concept-economics\|Concept: AI-coworker economic benchmark]] | The core premise — $10 starting balance, 220 GDPVal tasks across 44 occupations, `quality_score × estimated_hours × BLS_wage` payment, GPT-5.2 LLM-judge rubrics, and the work-or-learn daily loop. |
| [[wiki/02-agent-runtime\|Live agent runtime and economic tracking]] | `LiveAgent`'s daily session loop, `EconomicTracker`'s real-time cost deduction and pay gating at the 0.6 threshold, survival-status bands, and the `WrapUpWorkflow` timeout fallback. |
| [[wiki/03-clawmode-tools\|ClawMode integration: loop, tools, classifier]] | `ClawWorkAgentLoop` subclassing nanobot's `AgentLoop`, six shared-state economic/artifact tools, `TaskClassifier`'s `/clawwork` instruction pricing, and per-call cost-tracking provider wrappers. |
| [[wiki/04-scheduler-api\|Scheduler, API server, run configs]] | The empty `scheduler/` placeholder, `api/server.py`'s FastAPI REST + WebSocket data layer, and `configs/default_config.json`'s date/economic/agent settings. |
| [[wiki/05-economics-scripts\|Economics pipeline scripts]] | Offline hour estimation, BLS wage matching, historical payment rescaling, and the `validate_economic_system.py` audit of `EconomicTracker`'s threshold/channel logic. |
| [[wiki/06-frontend-dashboard\|Dashboard: static data + web UI]] | The React dashboard's live/static data-source split (`VITE_STATIC_DATA`), WebSocket updates, and per-view JSON generation for GitHub Pages export. |

## Original Source

- [source/provenance.md](source/provenance.md) — provenance pin (commit 9c73ac0, shallow clone, 2026-09-12), local read-only clone at `/tmp/clawwork`
- [source/delegation_report.md](source/delegation_report.md) — extraction/verify/synth delegation trail
