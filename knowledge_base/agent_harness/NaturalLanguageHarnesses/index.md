---
type: Paper
title: Natural-Language Agent Harnesses
description: Externalizes agent-harness policy from coupled controller code into editable Natural-Language Agent Harness (NLAH) documents run by a shared Intelligent Harness Runtime (IHR), matching code-harness task scores on coding/terminal/computer-use benchmarks with ~20x smaller inspectable policies, while exposing parent-child handoff as the main bottleneck.
generated: { by: claude, at: 2026-09-12T06:54:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2603.25723
  - id: local-copy
    resource: source/full.md
tags: [agent-harness, llm-agents, orchestration, ablation, natural-language-policy]
---

# Natural-Language Agent Harnesses

Agent performance is strongly shaped by the harness around the model, but harness logic is usually buried in tightly coupled controller code — hard to inspect, compare, transfer, or ablate. This paper proposes Natural-Language Agent Harnesses (NLAHs): editable documents carrying run-level harness policy (stages, roles, state, verification, recovery, stopping), executed by a shared Intelligent Harness Runtime (IHR) that turns the document into agent calls, handoffs, state updates, and validation gates. Across SWE-bench Verified/Live-SWE, Terminal-Bench 2.0/MHTBA, and OSWorld/SeeAct, IHR-executed NLAHs are competitive with native code harnesses while compressing static policy roughly 20x, and module ablations show file-backed state and evidence-backed answering help while multi-candidate search and context compression hurt. The main disclosed weakness is parent-child information handoff, and an appendix shows a code harness tuned for one model porting poorly to another as a cautionary contrast.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-intro-method\|Intro, preliminaries, NLAH methodology]] | Harness definition, NLAH+IHR design, four-layer stack, five writing principles, three evaluation questions |
| [[wiki/02-experiments\|Experimental design and results]] | RQ1 code/prompt/IHR head-to-head, static-policy compression, RQ2 mechanism audits, RQ3 module ablations |
| [[wiki/03-appendices\|Appendices and limits]] | NL/code boundary tables, LinguaClaw replication package, MHTBA cross-model portability failure, limitations |

## Original Source

- [source/full.md](source/full.md) — full paper text, retrieved from arXiv:2603.25723
