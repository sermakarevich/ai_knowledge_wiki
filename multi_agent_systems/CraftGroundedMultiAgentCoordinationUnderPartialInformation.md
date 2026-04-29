# CRAFT: Grounded Multi-Agent Coordination Under Partial Information

**Paper:** [CRAFT: Grounded Multi-Agent Coordination Under Partial Information (Nath, VanderHoeven, Krishnaswamy, 2026)](https://arxiv.org/abs/2603.25268v1)

## Human Readable TL;DR

Imagine three people each looking at a different side of a Lego sculpture, and they have to describe what they see to a fourth person who has to rebuild it -- but none of them can see the whole thing. This paper tests whether AI language models can do this kind of teamwork. The surprising finding is that bigger, fancier AI models are not necessarily better teammates -- they tend to overthink and issue too many "undo" instructions, wasting their limited turns. Smaller models that keep things simple often build more of the sculpture correctly.

## TL;DR

CRAFT is a multi-agent benchmark where three LLM "director" agents, each holding a private 2D projection of a 3D target structure, must coordinate via natural language to guide a builder agent in reconstructing the structure. Formalized as a multi-sender Bounded Pragmatic Speaker (BPS) problem, the benchmark reveals that frontier models score higher on individual communication quality metrics yet achieve lower task progress than smaller open-weight models (7B--9B), because their superior perspective-taking drives over-correction behavior that exhausts the turn budget without advancing construction.

---

## Problem & Motivation

LLMs are increasingly deployed in multi-agent systems, yet their ability to coordinate under **partial observability** -- where each agent holds complementary private information -- remains fragile and largely untested. Existing benchmarks either evaluate single-agent reasoning or study multi-agent interaction in symmetric, abstract settings. The critical missing capability is **pragmatic communication**: deciding what to say, how much to say, and when to say it based on other agents' knowledge and needs. CRAFT addresses this gap by providing a grounded, spatially constrained environment where communication quality directly determines task success, and where failures can be diagnosed at the level of spatial grounding, belief modeling, and pragmatic sufficiency.

---

## Main Original Ideas

1. **CRAFT Benchmark.** A multi-agent construction task where three director agents each observe a private 2D wall projection of a 3D target structure on a 3x3 grid and must guide a builder agent through natural language. The benchmark features procedurally generated structures across three complexity tiers (simple, medium, complex), a physics-constrained game engine, and fine-grained per-turn trajectory logging. An oracle-assisted builder interface isolates director communication quality from builder execution ability.

2. **Multi-Sender Bounded Pragmatic Speaker (BPS) Framework.** A theoretical extension of the single-sender BPS model to multi-agent settings, where each director is modeled as a bounded pragmatic speaker whose Theory-of-Mind listener must account for what all other directors have already communicated. This formalizes the Gricean Maxim of Quantity in a grounded multi-agent setting and identifies four failure modes: limited search (F1), flawed pragmatics (F2), inefficient inference (F3), and a novel group-level failure where individually competent directors collectively fail to specify a correct move.

3. **Three-Judge Diagnostic Framework.** An LLM-based automatic grading system with three diagnostically independent judges -- Spatial Grounding (SG) evaluating private reasoning, Mind Modeling (MM) evaluating public message calibration, and Pragmatic Sufficiency (PS) evaluating whether the collective director output enables a rational builder to identify a correct move. This decomposition enables scalable per-turn diagnostics across thousands of dialogue turns.

4. **Correction Spiral Taxonomy.** Identification of a behavioral failure mode where directors issue excessive removal instructions beyond what the oracle prescribes, consuming the limited turn budget without advancing progress. This pattern is particularly pronounced in frontier models and is causally linked to their stronger unique perspective utilization -- the very reasoning that makes them better individual communicators drives over-correction at the group level.

---

## Key Findings

| Model | Progress | Completion | Pos. Acc. | Dist. | Fail Rate | REMOVE | Gap |
|---|---|---|---|---|---|---|---|
| **Gemini-3-Flash** | **0.675** | **0.716** | **0.594** | **0.817** | 0.625 | 0.196 | 0.018 |
| GPT-4o | 0.588 | 0.633 | 0.500 | 0.753 | 0.421 | 0.280 | 0.056 |
| **Mistral-7B** | **0.631** | **0.673** | **0.539** | **0.793** | 0.500 | 0.124 | -0.124 |
| **Qwen-7B** | **0.612** | **0.665** | **0.517** | **0.778** | 0.556 | 0.205 | -0.116 |
| Llama-8B | 0.586 | 0.630 | 0.506 | 0.741 | 0.684 | 0.277 | 0.080 |
| Gemma-9B | 0.578 | 0.628 | 0.483 | 0.751 | 0.600 | 0.122 | -0.084 |
| GPT-4.1-Mini | 0.312 | 0.352 | 0.233 | 0.481 | 0.500 | 0.463 | 0.388 |
| Claude-Sonnet-4.6 | 0.285 | 0.332 | 0.189 | 0.479 | 0.350 | 0.395 | 0.265 |

- **Frontier models do not uniformly outperform open-weight models.** Mistral-7B and Qwen-7B outperform the majority of frontier systems. Only Gemini-3-Flash matches or exceeds the best open-weight models.
- **Higher individual communication quality does not translate to better collaboration.** GPT-4.1-Mini achieves the highest SG (0.937) and MM (0.787) scores of any model yet only reaches 0.312 progress -- less than half of Mistral-7B's 0.631.
- **Layer errors are the dominant failure mode** across nearly all models, confirming that 3D layer inference from 2D projections is the primary bottleneck.
- **Remove gap strongly predicts task failure.** The gap between attempted and oracle-prescribed removals is negatively correlated with oracle adherence (rho = -0.543, p < 0.001), which in turn drives task progress (r = 0.962, p < 0.001).
- **Pragmatic Sufficiency (PS) is the only judge that discriminates successful from unsuccessful turns** -- SG and MM scores are nearly identical regardless of outcome, while PS scores drop sharply on failed turns.
- **Mediation analysis confirms the causal chain:** unique perspective utilization leads to correction-oriented instructions, which drives over-removal in frontier models, consuming the turn budget without advancing progress.

---

## Suggestions & Future Directions

1. **Multimodal inputs.** CRAFT is text-only; incorporating visual inputs could improve individual spatial grounding, though it remains unclear whether such gains would transfer to multi-agent coordination where communication and conflict resolution are critical.

2. **Removing oracle assistance.** The current fixed builder with oracle-verified candidate moves isolates director communication but does not reflect real-world settings where agents must act without ground-truth guidance or explore moves via simulation tools.

3. **Heterogeneous director models.** Mixing open-weight and proprietary models within a single game could reveal how differences in alignment algorithms, pretraining data, and post-training methods influence collaborative performance and partner-aware coordination.

4. **Training for collective coordination.** The results suggest that current RLHF and reasoning training improve individual communication but may actively harm group coordination -- future work could develop training objectives that explicitly optimize for multi-agent pragmatic sufficiency rather than individual quality.

5. **Scaling turn budgets and repair mechanisms.** The 20-turn limit constrains recovery from early errors; investigating adaptive turn allocation or explicit repair-tracking protocols could improve performance.

---

## Authors & Institutions

Abhijnan Nath, Hannah VanderHoeven, Nikhil Krishnaswamy -- Situated Grounding and Natural Language (SIGNAL) Lab, Department of Computer Science, Colorado State University, Fort Collins, CO, USA.
