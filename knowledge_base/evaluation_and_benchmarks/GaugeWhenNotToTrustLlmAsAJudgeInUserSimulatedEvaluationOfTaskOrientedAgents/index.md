---
type: Paper
title: 'GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents'
description: GAUGE audits the offline simulator-plus-judge release gate for task-oriented agents against a verifiable non-LLM reward, showing broad ranking agreement yet decorrelated satisfaction and 31% wrong promotions on close pairs.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-15T07:35:33Z }
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.12191
  - id: local-copy
    resource: source/source.md
tags: [llm-as-a-judge, task-oriented-agents, user-simulation, evaluation-validity]
---

# GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents

GAUGE (Grounded Audit of User-simulator-and-judge Gate Evaluation) audits the de facto offline release gate in which persona-conditioned LLM user-simulators converse with candidate agents and an LLM-as-a-judge scores the transcripts. Across 25 agents from six providers, four judges, two substrates (tau2-bench retail/airline plus SimulatorArena tutoring), and about 3,700 transcripts, the gate's ranking matches the verifiable reward broadly (rho=0.94) yet satisfaction is decorrelated from task success (57.5% satisfied-but-failed, rho=-0.147) and close-pair decisions disagree 31% of the time. The remedy is calibrate-then-trust: use the cheap gate only inside a verifiably audited operating region.

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
| [[wiki/01-gauge-overview\|GAUGE: When Not to Trust LLM-as-a-Judge]] | Title block only (authors, Amazon affiliation); no substantive claims |
| [[wiki/02-introduction-and-positioning\|Introduction and Positioning]] | De facto offline gate, ranking vs. construct validity, satisfaction gap, calibrate-then-trust |
| [[wiki/03-judge-biases-and-method\|Judge Biases and Method]] | Known judge biases, misaligned satisfaction anchor, GAUGE formalism, substrates and ladder |
| [[wiki/04-satisfaction-success-gap\|Satisfaction Matches the Base — Only the Policy-Aware Gate Helps]] | 57.5% satisfied-but-failed vs. base rate, policy-aware gate vs. process-blind proxy |
| [[wiki/05-judge-robustness-and-self-preference\|Judge robustness and self-preference]] | Cross-judge agreement, capability-artifact control, +0.75/7 self-preference, rerun stability |
| [[wiki/06-reliability-methods-and-references\|Reliability methods, references, and appendix evidence]] | Rater populations, dimensions, controlled degradation (D7 inversion), simulator robustness |
| [[wiki/07-simulator-swap-control\|Controlled second-provider simulator swap (Table 7)]] | Sonnet-4.5 to GPT-5.4 simulator swap, preserved gap and ranking (rho=0.93) |
| [[wiki/08-decision-disagreement-rate\|Table 9: Decision-disagreement rate by signal]] | 31.0% near-equal vs. 0.9% wide disagreement, signal-specific flips, no ensemble fix |
| [[wiki/09-annotation-and-prompt-instructions\|Annotation and Prompt Instructions: Entire Conversation, Personas, and Evaluation Substrates]] | Personas S1–S5/S8, dataset statistics, oracle patch, process-blind prompts |
| [[wiki/10-release-gate-judge-rubric\|Release-gate judge (policy-aware) and three satisfied-but-failed cases]] | Policy-aware rubric, retail/airline/tutoring satisfied-but-failed cases |

## Original Source

- [https://arxiv.org/pdf/2609.12191](https://arxiv.org/pdf/2609.12191) — original paper PDF
- [source/source.md](source/source.md) — local copy of the source text
