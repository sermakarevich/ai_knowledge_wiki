# From Model Scaling to System Scaling: Scaling the Harness in Agentic AI

**Paper:** [From Model Scaling to System Scaling: Scaling the Harness in Agentic AI (Shangding Gu, 2026)](https://arxiv.org/abs/2605.26112)

## Human Readable TL;DR

Imagine you hire a brilliant consultant (the AI model), but they keep forgetting what was discussed last week, lose track of which expert they called for what, and can't cross-check their own conclusions. Giving that consultant an even bigger brain won't fix those problems -- you need better notebooks, filing systems, checklists, and coordinators around them. This paper argues that AI agents have hit exactly that wall: the "office infrastructure" around the AI (memory, context management, tool use, verification) is now the bottleneck, not the AI itself. The author proposes a framework to design, measure, and improve that infrastructure systematically.

## TL;DR

The paper argues that the next major bottleneck in agentic AI is **system scaling** -- optimizing the structured execution layer (the "harness") surrounding a foundation model -- rather than further model scaling alone. It introduces a six-component framework (Reasoning, Memory, Context Constructor, Skill-Routing, Orchestration, Verification/Governance) and identifies three core system bottlenecks: context governance, trustworthy memory, and dynamic skill routing with verification. A new evaluation agenda focused on process-level and longitudinal metrics is proposed, alongside the release of CheetahClaws, a Python-native reference harness.

---

## Problem & Motivation

Current agentic AI evaluation is **model-centric**: benchmarks reduce agent performance to final-task success, treating memory, retrieval, tool use, orchestration, and governance as secondary implementation details. This is increasingly inadequate because:

- Agent performance emerges from the *interaction* among a foundation model and its surrounding components, not from the model alone.
- Even with fixed models, better tool schemas and harness design yield large benchmark gains (e.g., SWE-agent).
- Larger context windows don't solve attention dilution or positional bias -- those are context governance problems.
- Multi-agent systems introduce coordination failures that single-agent success metrics can't capture.
- Frontier models still fail at reliability over repeated long-horizon interactions.

---

## Main Original Ideas

1. **System Scaling Framing** -- Defines "scaling the harness" as the design, evaluation, and optimization of auditable, persistent, modular, and verifiable architectures *around* foundation models. Future progress will depend as much on this as on stronger models.

2. **Six-Component Agent Framework** -- An agent is modeled as P_H = Φ(R, M, C, S, O, G):
   - **R** (Reasoning Substrate): the foundation model
   - **M** (Memory Store): precision, durability, retrievability, verifiability
   - **C** (Context Constructor): relevance, compactness, traceability, refresh policy
   - **S** (Skill-Routing Layer): specificity, selectivity, composability, verifiability
   - **O** (Orchestration Loop): control flow and task scheduling
   - **G** (Verification & Governance Layer): safety, auditability, post-condition checks

3. **Three Temporal Layers** -- Prompt (local, single-turn), Skill (task-level, reusable capability), and Memory (longitudinal, cross-session) operate at distinct timescales and have different failure modes and intervention points.

4. **Context Governance as Policy** -- Reframes context assembly not as "fit more tokens" but as a dynamic policy optimizing relevance, compactness, traceability, and timely refresh. The key failure mode is "exposure without access" -- the model sees tokens but fails to attend to them.

5. **Trustworthy Memory** -- Proposes treating memory trust as a runtime decision: every stored entry carries staleness penalties and confidence scores, and memory is periodically re-verified against the live environment. The failure mode to prevent is "stale-but-confident."

6. **Routing as a Learned Policy** -- Skill routing should be adaptive (like OS scheduling), not a fixed rule set. Routing policy (S) and verification (G) are tightly coupled: scaling skill quality without scaling verification produces faster but *less reliable* progress.

7. **CheetahClaws Reference Harness** -- A Python-native open-source harness released alongside the paper that operationalizes the framework; compared against Claude Code and OpenClaw to make harness-level design choices explicit.

---

## Key Findings

The paper is primarily theoretical/analytical (no new empirical benchmarks), but its key claims are:

| System Component | Failure Mode | Proposed System Move |
|---|---|---|
| Context (C) | Exposure without access | Treat assembly as a dynamic policy; just-in-time refresh |
| Memory (M) | Stale-but-confident | Runtime trust scores; staleness penalties; periodic re-verification |
| Skill Routing (S+G) | Confident-but-unchecked | Learned routing policy; explicit post-condition checks at every step |

- A multi-agent system (Claude Opus 4 lead + Claude Sonnet 4 subagents) outperformed single-agent Claude Opus 4 by **90.2%** on Anthropic's internal research evaluation -- illustrating why longitudinal, multi-agent evaluation matters.
- Current benchmarks (SWE-bench, AgentBench, WebArena, Terminal-Bench) are necessary but insufficient: they mix model capability with harness design and capture only outcome metrics, not process-level costs.
- Different harness designs around the *same* foundation model produce qualitatively distinct agent behaviors, validating that the harness is a first-class variable.

---

## Suggestions & Future Directions

1. **Process + outcome reporting** -- Benchmarks should jointly report token usage, tool calls, retries, failed edits, human interventions, and auditability alongside task success.
2. **Longitudinal evaluation** -- Multi-session benchmarks measuring memory hygiene, context efficiency, communication fidelity across subagents, and drift over time.
3. **Standards for safe agent evolution** -- Define what persists, what updates, what is measured (including reward hacking detection), and what is auditable as agents adapt across sessions.
4. **Adaptive skill-routing research** -- Online estimation of subtask type, confidence-aware escalation, mixture-style composition, and policies optimized for verified (not merely fluent) intermediate outputs.
5. **Memory trust mechanisms** -- Develop confidence-gated risk terms, staleness penalties, and hybrid designs (persistent project context + just-in-time environment access).
6. **Harness-level benchmarks** -- New metrics for trajectory quality, memory precision, minimal-context efficiency, verification cost, and safety under tool access and autonomous execution.

---

## Authors & Institutions

Shangding Gu (UC Berkeley)
