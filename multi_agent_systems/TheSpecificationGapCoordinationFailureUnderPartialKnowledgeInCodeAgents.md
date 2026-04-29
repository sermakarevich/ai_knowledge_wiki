# The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents

**Paper:** [The Specification Gap: Coordination Failure Under Partial Knowledge in Code Agents (Chacon Sartori, 2025)](https://arxiv.org/abs/2603.24284v1)

## Human Readable TL;DR

Imagine two builders constructing different rooms of the same house, but neither has the full blueprint -- one builds doorways 3 feet wide while the other builds doors 4 feet wide. This paper studies what happens when multiple AI coding assistants each build separate parts of the same program without seeing the whole plan. The researchers found that even small gaps in the shared instructions cause the pieces to clash when put together. The single most effective fix is simply giving everyone a complete, detailed blueprint upfront -- not trying to patch things after the fact.

## TL;DR

This paper empirically investigates coordination failures in multi-agent LLM code generation when agents operate under partial specifications. Using a controlled benchmark (AmbigClass, 204 task-specification pairs), the authors show that integration success degrades monotonically as specification detail is removed, and a persistent 30--35 pp "coordination tax" separates multi-agent from single-agent performance at all specification levels. Recovery experiments demonstrate that restoring the full specification is both necessary and sufficient for resolving integration failures, while AST-based conflict reports alone provide no measurable benefit to a merger agent.

---

## Problem & Motivation

When multiple LLM-based code agents independently implement different parts of the same software artifact (e.g., methods of a class), they must implicitly agree on shared internal data representations. If one agent stores data as a list while another expects a dictionary, their individually correct code will fail upon integration. This "specification gap" -- the mismatch between what each agent knows and what it needs to know for compatibility -- is a distinct class of error that does not arise in single-agent settings. Classical software engineering principles (Parnas's information-hiding, Meyer's Design by Contract) predict that precise interface specifications are essential for independent module development, but no prior work had empirically quantified this effect for LLM agents.

---

## Main Original Ideas

1. **Specification-Ablation Protocol** -- A nested hierarchy of four specification levels (L0 full spec down to L3 bare signatures) that progressively removes information, enabling controlled measurement of how specification completeness affects coordination outcomes.

2. **AmbigClass Benchmark** -- A reusable benchmark of 204 task-specification pairs derived from 51 ClassEval tasks, designed specifically to study multi-agent coordination rather than individual agent capability.

3. **Controlled Bias Injection** -- Deliberately biasing split agents toward lists vs. dictionaries as a proxy for natural stylistic divergence, isolating structural incompatibility from stochastic variation.

4. **AST-Based Zero-Cost Conflict Detector** -- A lightweight static analysis tool that identifies type, state, and protocol conflicts between independently generated code segments before integration, requiring no additional LLM inference.

5. **Factorial Decomposition of Recovery** -- A 2x2 experiment crossing specification quality with conflict report availability, cleanly separating the contribution of each factor to integration recovery.

6. **Coordination vs. Information Asymmetry Decomposition** -- An additional 2x2 experiment crossing agent mode (single vs. split) with constructor visibility, showing that coordination difficulty and hidden information contribute approximately additively to the specification gap.

---

## Key Findings

| Condition | L0 (Full) | L1 | L2 | L3 (Bare) |
|---|---|---|---|---|
| **Single Agent** | 88.6% | 79.5% | 68.6% | 55.8% |
| **Split Agents** | 58.2% | 47.9% | 37.3% | 24.6% |
| **Coordination Gap** | 30.4 pp | 31.6 pp | 31.3 pp | 31.2 pp |

- The coordination tax (29.5--34.8 pp for Sonnet, 25.5--38.8 pp for Haiku) is statistically significant at every specification level (Wilcoxon p < 0.001) and does not shrink as specifications improve -- richer specs raise both ceilings equally.
- AST conflict detector precision rises from 43.5% at L0 to 96.7% at L3, making it most reliable precisely when specifications are weakest. Type conflicts account for 60.6% of all detections.
- **Recovery experiment:** Providing the full L0 spec to a merger agent restored performance to 88.9% (matching the single-agent ceiling of 88.3%). Conflict reports alone added 0.0 pp improvement. Combining both spec and reports actually decreased performance slightly (-6.6 pp interaction effect).
- **Init-visibility experiment:** Coordination cost (+15.7 pp) exceeds information asymmetry cost (+11.2 pp), and the effects are approximately additive.
- All qualitative patterns replicated with Claude Haiku 4.5 across three independent runs (SD <= 2 pp).

---

## Suggestions & Future Directions

1. **Specification-first orchestration** -- Multi-agent systems should invest in generating rich, data-structure-explicit specifications before distributing work to agents, rather than relying on post-hoc conflict resolution.

2. **Conflict detection as monitoring, not resolution** -- AST-based conflict detectors are best used as diagnostic signals to flag inadequate specifications, not as direct inputs to merger agents lacking full context.

3. **Account for inherent coordination cost** -- System architects should expect a persistent performance penalty from task decomposition and prefer single-agent generation when specification enrichment is infeasible.

4. **Richer conflict representations** -- Future work should explore semantic diffs, iterative inter-agent negotiation, and richer conflict encodings that might partially compensate for specification gaps.

5. **Broader generalization** -- The current findings are bounded by Python class generation, explicit bias injection, and the Claude model family; extension to other languages, implicit biases, and diverse model architectures is needed.

6. **Scaling studies** -- Investigating how the coordination tax scales with the number of agents, task complexity, and codebase size remains an open question.

---

## Authors & Institutions

Camilo Chacon Sartori -- Catalan Institute of Nanoscience and Nanotechnology (ICN2), CSIC and BIST, Campus UAB, Bellaterra, Barcelona, Spain.
