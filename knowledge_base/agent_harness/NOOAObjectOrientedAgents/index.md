---
type: Paper
title: Native Python Object-Oriented Agents
description: NVIDIA proposes NOOA, a Python framework where an agent is a class, its methods are LLM-completable actions, and six previously scattered model-facing ideas (typed I/O, pass-by-reference, code-as-action, programmable loop engineering, explicit object state, harness APIs) are unified on one surface.
generated: { by: claude/claude-sonnet-5, at: 2026-08-03T18:05:07Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.20709
  - id: local-copy
    resource: source/2607.20709.pdf
tags: [agent-frameworks, python, code-as-action, agent-memory, harness-design]
---

# Native Python Object-Oriented Agents

NVIDIA's NOOA (NVIDIA Object-Oriented Agents) reframes agent development as ordinary Python object-orientation: an agent is a class, its methods are the actions the model can take, docstrings are prompts, type annotations are contracts, and a special method body (`...`) is completed at runtime by an LLM-driven loop while normal-bodied methods stay deterministic Python. The paper argues this unifies six model-facing ideas — typed I/O, pass-by-reference over live objects, code-as-action, programmable loop engineering, explicit object state, and harness APIs — that other frameworks implement only partially, and backs the claim with capability tests, SWE-bench Verified, Terminal-Bench 2.0, CyberGym, and an ARC-AGI-3 result where the interface collapses a multi-agent world-model system into one agent with a one-page skill.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-design-principles\|Introduction & Design Principles]] | Motivation for the framework and the "agent as Python object" design principles (Sec. 1–2) |
| [[wiki/02-agent-loop-strategies-and-context\|Agent Loop Strategies & Context]] | Programmable loop engineering and context-rendering strategies (Sec. 3.1–3.2) |
| [[wiki/03-execution-validation-and-memory\|Execution, Validation & Memory]] | Code-as-action execution, validated LLM loops, and the long-term memory system (Sec. 3.3–3.7, Appendix C) |
| [[wiki/04-capability-tests-and-stress-test-appendix\|Capability Tests & Stress-Test Appendix]] | Targeted capability tests and detailed stress-test case studies (Sec. 4.1, Appendix B) |
| [[wiki/05-swebench-terminal-bench-and-cybergym\|SWE-bench, Terminal-Bench & CyberGym]] | Results on SWE-bench Verified, Terminal-Bench 2.0, and CyberGym (Sec. 4.2–4.3) |
| [[wiki/06-arc-agi-3-and-world-models\|ARC-AGI-3 & World Models]] | Interactive-reasoning benchmark results and the single-agent world-model compression (Sec. 4.4, Appendix D) |
| [[wiki/07-comparison-to-other-frameworks\|Comparison to Other Frameworks]] | Head-to-head comparison against 14+ other agent frameworks and harnesses (Sec. 5, Appendix A) |
| [[wiki/08-related-work-and-conclusion\|Related Work & Conclusion]] | Positioning against prior agent-framework research and closing takeaways (Sec. 6–7) |

## Original Source

- [source/2607.20709.pdf](source/2607.20709.pdf) — arXiv PDF (arXiv:2607.20709v1 [cs.AI], 22 Jul 2026), retrieved 2026-08-03
