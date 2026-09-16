---
type: Paper
title: Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures
description: A 41-mode taxonomy that labels agent failures by which interaction edge (User, Harness, or Environment) they occur on and which endpoint is at fault, validated with an agent-as-a-judge protocol.
generated: { by: claude/claude-sonnet-5, at: 2026-08-04T09:23:57Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.28802
  - id: local-copy
    resource: source/2607.28802.pdf
tags: [agents, failure-taxonomy, llm-evaluation, agent-as-judge, fault-attribution]
---

# Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures

A Scale AI Research paper (arXiv:2607.28802, submitted 2026-07-30) arguing that knowing an agent failed is not enough — you need to know *which interaction* it failed on (with its user, its harness, or its environment) and *which side* of that interaction is at fault, because that determines whether the fix is model post-training, harness engineering, or something outside the model entirely. It builds a 41-failure-mode taxonomy organized around a "mechanism axis" (the model as hub, with edges to User/Harness/Environment families) and validates that the labels are recoverable in practice using four LLM judges in a three-turn protocol, plus a catalog of 40 worked examples. Worth ingesting because it gives a reusable vocabulary for triaging agent failures encountered in real agentic-systems work, not just a benchmark leaderboard result.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-problem-and-related-work\|Problem and Related Work]] | Poses the "repair-assignment problem" and positions the taxonomy against benchmark-specific, module-based, flat-list, security, and trace-localization prior work (§1-§2). |
| [[wiki/02-mechanism-and-methodology\|Mechanism Axis and Categorization Methodology]] | The model-as-hub interaction-edge representation, the fault-side attribution rule, and the iterative methodology used to build the taxonomy (§3-§4). Figures 1-2. |
| [[wiki/03-taxonomy-user-and-context-memory\|Taxonomy: Users, Context, and Memory]] | Owner/Grader/Third-party edges plus the Context/Memory harness edges — 23 failure modes with fault-side attributions and verbatim Appendix B definitions (§5.1, part of §5.2). |
| [[wiki/04-taxonomy-tool-and-environment\|Taxonomy: Tool, Multi-Agent, and Environment]] | Model-Tool, Model-Model (multi-agent), and Model-Environment edges — tool-call failures, delegation/communication failures, service/state/recovery failures (part of §5.2). |
| [[wiki/05-agent-as-judge-validation\|Validating the Taxonomy with an Agent-as-a-Judge]] | The 4-judge, 3-turn validation protocol, agreement metrics (κ up to 0.76), the precision/coverage tradeoff, and the Harbor-Mix case study where a judge misattributes a harness bug to the model (§6, Appendix A). Figures 3-5. |
| [[wiki/06-discussion-and-limitations\|Discussion and Limitations]] | Why fault localization matters practically, why the taxonomy skews model-side, and the paper's acknowledged descriptive-scope and judge-deployment limitations (§7). |
| [[wiki/07-worked-examples-catalog\|Worked Examples Catalog]] | All 40 worked examples (E1-E40) from Appendix C with a full summary table, 12 detailed walkthroughs, and the OWASP/MAST risk-category mapping. |

## Original Source

- [source/2607.28802.pdf](source/2607.28802.pdf) — arXiv PDF, retrieved 2026-08-04
