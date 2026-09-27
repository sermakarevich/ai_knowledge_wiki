---
type: Paper
title: "SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence"
description: Fully automated framework that invents multi-agent teams from scratch and jointly optimizes roles and workflows via language-driven Particle Swarm Optimization, beating seed-based baselines everywhere tested with a headline 261.8% relative gain over ADAS on TravelPlanner.
generated: { by: fleet-65xe, at: 2026-09-15T00:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2506.15672
  - id: local-copy
    resource: source/full.md
tags: [llm-agents, multi-agent-systems, swarm-intelligence, automated-design, self-optimization]
---

# SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence

SwarmAgentic (Yao Zhang et al.) builds whole teams of AI assistants from nothing more than a task description and a scoring rule: several candidate teams are tested, their failures diagnosed in words, and roles plus workflows reshuffled through language-driven swarm search until the best team wins. Across TravelPlanner, Natural Plan, Creative Writing, and Multilingual Grade School Math it leads every baseline column, most strikingly on constraint-dense travel planning, and publishes the discovered teams as runnable programs — though inference cost is never measured and training samples are small.

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
| [[wiki/01-swarmagentic-overview\|SwarmAgentic overview]] | Autonomy gap and Table 1, PSO background, system representation, initialization, flaw identification, failure-aware velocity and position updates, TravelPlanner/Natural Plan results, transferability, ablation, trajectory |
| [[wiki/02-autonomy-setup-and-implementation\|Autonomy setup and implementation]] | Three autonomy properties, seven-framework evaluations, MODEL SWARMS comparison, dataset splits and metrics, six baselines, Role/Team code, Algorithm 1 pseudocode, eleven-operator prompt repository |
| [[wiki/03-optimization-prompts-case-study-and-discovered-systems\|Optimization prompts, case study and discovered systems]] | Global-best, personal-best, velocity and position prompts, travel-planning case study with per-signal fixes, best-discovered systems for MGSM/Creative Writing/meeting scheduling/TravelPlanner, ADAS comparison |

## Original Source

- [SwarmAgentic (Yao Zhang et al., 2025)](https://arxiv.org/abs/2506.15672) — original paper on arXiv
- [source/full.md](source/full.md) — full paper text, retrieved from arXiv:2506.15672
