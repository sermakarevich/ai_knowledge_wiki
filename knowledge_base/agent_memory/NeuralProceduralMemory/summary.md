# Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering

**Paper:** [Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering (Zhao et al., 2026)](https://arxiv.org/abs/2606.29824)

## Human Readable TL;DR

Imagine telling a new employee "follow the checklist" versus quietly nudging their instincts so they *just know* what to do next. Most AI agents today rely on the first approach: they read a text checklist (retrieved instructions) before acting, but often forget steps or misread the checklist mid-task. This paper does the second: it extracts a "feel" for how a task should go from past successful and failed attempts, turns that feel into a small numeric nudge, and injects it directly into the AI's internal "thought signals" while it works -- no text, no retraining, just a steering nudge baked into its reasoning at each step.

## TL;DR

The paper introduces Neural Procedural Memory (NPM), a training-free framework that represents an LLM agent's procedural memory as steering vectors in activation space rather than as retrieved text. Vectors are distilled from dual-granularity contrastive experience pairs (inter-trajectory: successful vs. failed full trajectories; intra-trajectory: effective vs. degenerate steps within one failed trajectory) and injected into the residual stream at inference time via `h̃ = h + α·v(q)`. Across four agent benchmarks (ALFWorld, WebShop, ScienceWorld, BabyAI) on MiniCPM3-4B, Qwen3-4B, and Qwen3-8B, NPM matches explicit textual-memory baselines and combines with them (NPM + Workflows) for the best overall scores, e.g. Qwen3-8B hybrid reaches 66.42% ALFWorld success and 41.89 average.

---

## Problem & Motivation

Turning static LLMs into autonomous agents requires persistent memory of *how* to act, not just *what* is true. Declarative memory (facts) is well served by RAG, but procedural memory (skills, workflows) is inherently implicit and hard to verbalize -- compressing sequential reasoning into text tokens loses information. Agents can retrieve and even understand a textual workflow yet still fail to execute it faithfully, a "text-action disconnect": they omit intermediate steps or drift from retrieved instructions during long execution horizons. Parametric approaches (fine-tuning, RL) bake procedures into weights but are costly and cannot adapt in real time. This motivates memory represented directly in the model's activation space, where cognitive neuroscience suggests procedural memory actually lives (non-verbalizable, expressed through neural activity modulation rather than declarative recall).

---

## Main Original Ideas

1. **Neural Procedural Memory (NPM)** -- a training-free framework that stores agent procedural memory as continuous steering vectors in activation space instead of retrieved text, and injects them into the residual stream at inference time to modulate reasoning without touching model weights or the context window.
2. **Dual-granularity contrastive experience construction** -- *inter-trajectory* contrasts pair a full successful trajectory against a full failed one for the same task (captures global behavioral shift); *intra-trajectory* contrasts split a single failed trajectory into "effective" vs. "degenerate" step sets (via redundancy/invalidity heuristics) to extract local corrective signal even when no full success exists yet, mitigating the cold-start problem of sparse successful demonstrations.
3. **Retrieval-Synthesis-Intervention pipeline** -- at inference, a dense retriever finds the top-K historical tasks most similar to the new query, their precomputed contrastive representation sets are pooled into a memory pool `M_l(q)`, a synthesis function `ψ(·)` derives a task-specific steering vector `v_l(q)`, and the vector is added (scaled by `α`) to the hidden state at each generation step: `h̃_{l,t} = h_{l,t} + α·v_l(q)`.
4. **Interpretability of steering vectors via sparse dictionary learning** -- decomposing steering vectors into basis directions shows they encode identifiable behavioral primitives (e.g. "initial planning," "systematic cabinet searching," "premature task completion") whose activation timing differs meaningfully between inter- and intra-trajectory steering.

---

## Key Findings

**Main results (Table 1, selected rows):**

| Model | Method | ALFWorld | WebShop | ScienceWorld | BabyAI | Avg |
|---|---|---|---|---|---|---|
| MiniCPM3-4B | No Memory | 23.88 | 32.21 | 7.29 | 27.00 | 22.60 |
| MiniCPM3-4B | NPM (Implicit, Ours) | 31.34 | 43.53 | 8.70 | 31.91 | 28.87 |
| MiniCPM3-4B | **NPM + Workflows (Hybrid)** | **38.81** | 51.21 | **10.97** | **36.90** | **34.47** |
| Qwen3-4B | No Memory | 30.60 | 44.81 | 18.40 | 18.75 | 28.14 |
| Qwen3-4B | NPM (Implicit, Ours) | 40.30 | **48.00** | 18.16 | 17.82 | 31.39 |
| Qwen3-4B | **NPM + Workflows (Hybrid)** | **61.19** | 47.84 | **21.97** | **19.38** | **37.60** |
| Qwen3-8B | No Memory | 39.55 | 46.25 | 24.98 | 11.74 | 30.63 |
| Qwen3-8B | NPM (Implicit, Ours) | 56.72 | 44.26 | 25.32 | 8.71 | 36.32 |
| Qwen3-8B | **NPM + Workflows (Hybrid)** | **66.42** | 53.94 | **31.89** | 15.31 | **41.89** |

- NPM (implicit-only) consistently beats implicit baselines CAA and Mass-Mean, which use fixed, dataset-wide mean-difference vectors instead of dynamically synthesized, task-specific ones.
- NPM is competitive with (and on WebShop/Qwen3-4B, beats: 48.00 vs. 45.73) explicit textual-memory baselines (Insights, Workflows), despite using zero context-window tokens.
- Hybrid (NPM + Workflows) is the best configuration across all three backbones -- explicit text supplies high-level symbolic plans, implicit steering enforces adherence to them during long execution.
- **Dual-granularity ablation:** intra-trajectory steering helps most in step-intensive environments (ALFWorld, by correcting local action errors); inter-trajectory steering helps most where macro-level planning dominates (WebShop). Combining both reduces variance across benchmarks.
- **Representational analysis:** PCA projections of hidden states (Layer 18, Qwen3-4B/ALFWorld) show successful vs. degenerate representations form distinct, separable clusters; a linear classifier trained on this space achieves high separation accuracy.
- **Vector consistency:** cosine-similarity heatmaps show steering vectors cluster by task type (e.g., `LookAt` vs. `Pick*` family) and by interaction target (e.g., `DeskLamp`, `Drawer`), indicating the extraction process captures shared procedural structure rather than noise.
- **Case study (PickHeat task):** unsteered baseline produces a bloated 33-step trajectory; inter-trajectory steering shortens it to 14 steps by boosting early-planning and object-placement features; intra-trajectory steering instead amplifies search/container-interaction features and suppresses premature-termination signals.
- **Retrieval pool size (K):** general behavioral features (basic exploration, redundant observation) scale monotonically with pool size; task-specific features (placement, systematic search, premature completion) peak at a moderate K and degrade at very large K due to cross-task interference -- justifying constrained, dynamic retrieval over using the full historical dataset.

---

## Suggestions & Future Directions

1. **Requires open/white-box models** -- NPM needs direct access to and intervention on the residual stream, so it cannot be applied to closed/API-only LLMs.
2. **Cold-start dependency** -- building the contrastive repository still relies on the agent occasionally producing successful trajectories; in very hard environments this remains a bottleneck despite the intra-trajectory contrast mitigation.
3. **Heuristic degenerate-step detection** -- identifying "degenerate" steps via redundancy/invalidity heuristics cannot catch implicit logical fallacies that don't manifest as explicit environment errors.
4. **Static intervention** -- the synthesized steering vector is applied as a single, constant modulation throughout generation; the authors propose exploring *dynamic* interventions that adapt across different execution stages as future work.

---

## Authors & Institutions

Chengfeng Zhao¹²﹡, Yuqiao Tan¹², Shizhu He¹², Yequan Wang³, Jun Zhao¹², Kang Liu¹²﹡ (﹡ corresponding) — ¹Institute of Automation, Chinese Academy of Sciences (CAS); ²University of Chinese Academy of Sciences; ³Beijing Academy of Artificial Intelligence.
