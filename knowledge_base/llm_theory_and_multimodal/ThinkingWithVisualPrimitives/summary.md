# Thinking with Visual Primitives

**Paper:** [Thinking with Visual Primitives (DeepSeek-AI, Ruijie Lu, Yiyang Ma et al., 2026)](https://www.alphaxiv.org/abs/visual-primitives)
**GitHub:** [deepseek-ai/Thinking-with-Visual-Primitives](https://github.com/deepseek-ai/Thinking-with-Visual-Primitives)

## Human Readable TL;DR

Imagine asking someone to describe where objects are in a photo using only words -- they might say "the big bear on the left near the tree," which gets confusing fast. This paper teaches AI to "point" as it thinks, dropping actual coordinates and boxes directly into its thought process, like saying "bear at position (452, 23) to (804, 411)" instead of a vague description. This anchors the AI's reasoning to exact physical locations, so it never loses track of where things are. The result is a model that counts, navigates mazes, and traces paths far better than much larger systems -- while also being far cheaper to run because it uses far fewer image tokens.

## TL;DR

DeepSeek introduces a framework where points and bounding boxes are embedded directly into the chain-of-thought reasoning trajectory of a Multimodal LLM, addressing what they call the "Reference Gap" -- the failure of language descriptions to precisely anchor spatial concepts during reasoning. Combined with 7,056× image token compression via spatial downsampling and Compressed Sparse Attention (CSA), the system achieves state-of-the-art results on counting, spatial reasoning, and topological navigation benchmarks, matching or surpassing GPT-5.4 and Gemini-3-Flash with a smaller activated parameter count (13B vs. much larger).

---

## Problem & Motivation

Current Multimodal LLMs (MLLMs) can see images but struggle to "think clearly" about them. During chain-of-thought reasoning, models describe object locations in natural language ("the large red object near the center"), but such descriptions are inherently ambiguous in dense scenes. This causes **reasoning drift** -- the model's attention gradually degrades as it loses precise track of which object is which, leading to wrong conclusions on tasks requiring precise spatial tracking.

The authors call this the **Reference Gap**: there is no grounding mechanism connecting abstract language reasoning tokens to concrete image coordinates, so spatial references accumulate errors over reasoning steps.

---

## Main Original Ideas

1. **Visual Primitives as Reasoning Tokens** -- Points `(x, y)` and bounding boxes `[x1, y1, x2, y2]` are embedded directly into the reasoning trajectory as atomic units of thought, interleaved with text. The model outputs chains like `<|ref|>bear<|/ref|><|box|>[[452,23,804,411]]<|/box|>` mid-reasoning, grounding every logical step to physical coordinates.

2. **Extreme Visual Compression** -- A three-stage compression pipeline reduces image token counts by 7,056×: (1) ViT encodes a 756×756 image into 2,916 tokens, (2) 3×3 spatial pooling compresses to 324 tokens, (3) Compressed Sparse Attention (CSA) further reduces the KV cache by 4×, yielding ~90 effective entries. This makes the model dramatically cheaper than competitors (~90 KV entries vs. Claude's ~870).

3. **Specializing First, Then Unifying** -- Training follows a two-phase strategy: first train specialist expert models (FTwG for bounding-box grounding, FTwP for point-based reasoning) independently, then merge them via unified reinforcement fine-tuning (GRPO algorithm with format, quality, and precision rewards) followed by on-policy distillation into a single model.

4. **Diverse Spatial Reasoning Curriculum** -- The training set covers four task families designed to stress-test spatial grounding: coarse and fine-grained counting, spatial relation reasoning (GQA, CLEVR), maze navigation (DFS/Prim/Kruskal algorithms; rectangular/circular/hexagonal topologies; 460K samples), and path tracing with Bezier curves and cross-ambiguity resolution (125K samples).

---

## Key Findings

| Benchmark | DeepSeek TVP | GPT-5.4 | Gemini-3-Flash | Qwen3-VL |
|---|---|---|---|---|
| Pixmo-Count (coarse counting) | **89.2%** | 76.6% | 88.2% | -- |
| Fine-grained counting | **88.7%** | -- | -- | 87.2% |
| MIHBench (spatial reasoning) | **85.3%** | -- | -- | -- |
| SpatialMQA | **69.4%** | -- | -- | -- |
| Maze navigation | **66.9%** | 50.6% | 49.4% | -- |
| Path tracing | **56.7%** | 46.5% | 41.4% | -- |

- The largest performance gaps appear on **topological reasoning** tasks (maze, path tracing), where precise spatial tracking matters most -- consistent with the Reference Gap hypothesis.
- Visual compression allows the model to operate with only ~90 KV cache entries for image content, compared to ~870 for Claude, enabling much lower inference cost.
- The "specializing first" phase is essential: skipping it and training a unified model directly yields substantially worse results (shown in ablation).
- Using both points and boxes together outperforms either primitive alone across all task types.

---

## Suggestions & Future Directions

1. **Richer primitive vocabulary** -- The authors suggest extending beyond points and boxes to other geometric primitives (masks, polylines, depth maps) for even finer spatial grounding.
2. **Dynamic compression rates** -- Current CSA uses a fixed 4× reduction; adaptive compression that varies by image complexity could preserve more information where needed.
3. **Video and 3D extensions** -- Visual primitives in temporal sequences (video) and volumetric inputs (3D point clouds) are identified as natural next steps.
4. **Broader task coverage** -- The current curriculum focuses on counting, spatial, and topological tasks; extending to fine-grained manipulation, medical imaging, and robotics are listed as open problems.
5. **Grounding faithfulness** -- Ensuring the emitted coordinates are genuinely used in downstream reasoning steps (not just decorative) is an open measurement and training challenge.

---

## Authors & Institutions

Ruijie Lu (DeepSeek / Peking University), Yiyang Ma (DeepSeek), and collaborators at DeepSeek-AI, Peking University, and Tsinghua University.
