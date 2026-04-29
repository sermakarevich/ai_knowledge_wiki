# I Tested Meta Muse Spark Against 4 Frontier Models

**Paper:** [I Tested Meta Muse Spark Against 4 Frontier Models (Ritesh Khanna, 2026)](https://www.riteshkhanna.com/blog/muse-spark-arena)

## Human Readable TL;DR

Imagine you gave five students the same exam with three very different sections -- reading a messy handwritten menu, doing stock market homework, and building a snow globe diorama. The newest student (Meta Muse Spark) aced the reading and homework but built a snow globe you couldn't see inside. The one everyone expected to win at coding (GPT-5.4) made the only snow globe that actually looked good but fumbled the other tests. The takeaway: no single student is best at everything, and the way each one messes up tells you more than their grades.

## TL;DR

A practical, non-benchmark evaluation of five frontier models (Meta Muse Spark, Claude Opus 4.6, GPT-5.4, Gemini 3.1, Grok 4.2) across three real-world tasks: multimodal menu reading, tool-augmented stock analysis, and 3D code generation. Meta Muse Spark won overall (75/100) with zero hallucinations on vision and best-sourced analysis, but rendered a black screen on the code task. The key finding: code quality metrics inversely correlated with functional output, and hallucination failure modes are model-specific diagnostics, not random noise.

---

## Problem & Motivation

Benchmark scores dominate model comparisons but rarely reflect real-world usability. The author sought to test frontier models on practical, messy tasks -- a handwritten restaurant menu with glass reflections, live stock data requiring tool use and arithmetic, and complex 3D scene generation -- to see how models actually perform when benchmarks are removed from the equation. Single-shot, identical prompts, zero retries.

---

## Main Original Ideas

1. **Consensus-Based Ground Truth for Vision** -- Rather than human-annotated labels, correctness was determined by 4+/5 model agreement on menu items, creating a pragmatic ground truth from the models themselves.

2. **Hallucination Pattern Taxonomy** -- Each model's failure mode was classified as a diagnostic signature: Meta stays silent under uncertainty, Grok invents plausible alternatives, GPT-5.4 states wrong numbers confidently, Gemini smooths gaps with generic substitutes, Claude misreads fundamentally.

3. **Code Quality vs. Functional Output Inversion** -- Static code analysis scores were inversely correlated with actual rendering results. Meta's code was the most technically correct Three.js but produced a black screen; GPT-5.4's simplest code was the only watchable output.

4. **Task-Specific Model Selection Framework** -- Rather than ranking models globally, the evaluation argues for choosing models per-task, since no model dominated all three categories.

---

## Key Findings

### Menu Reading (Vision / Hallucination)

| Model | Items Found (of 17) | Hallucinations | Failure Mode |
|---|---|---|---|
| **Meta Muse Spark** | **17/17** | **0** | -- |
| Gemini 3.1 | 17/17 | 2-3 | Plausible substitutions |
| GPT-5.4 | 15/17 | 3-4 | Confident fabrication |
| Grok 4.2 | 17/17 | 5+ | Creative invention |
| Claude Opus 4.6 | 8/17 | 5+ | Fundamental misreads |

### Stock Analysis (Tool Use & Reasoning)

| Model | NVDA P/E | Analysis Score | Key Differentiator |
|---|---|---|---|
| **Meta Muse Spark** | **36.3x** | **7+** | Best sourcing, forward P/E, same-day news |
| Claude Opus 4.6 | 36.3x | 7 | Correct data, proper sources, noted caveats |
| Grok 4.2 | 37.1x | 6 | Exact timestamps, showed formula, no sources |
| GPT-5.4 | 37.0x | 6 | Right answer, bad sourcing |
| Gemini 3.1 | 36.3x | 5.5 | Good analysis, zero sources cited |

### Snow Globe (Code Generation)

| Model | Code Quality (Static) | Rendering Rank | Notes |
|---|---|---|---|
| Meta Muse Spark | 12.5 (best) | 4th | Black screen -- lighting couldn't penetrate glass |
| Claude Opus 4.6 | 12.0 | 2nd | -- |
| Gemini 3.1 | 11.0 | 5th | Clock bug froze snow completely |
| Grok 4.2 | 10.0 | 3rd | -- |
| **GPT-5.4** | **9.5 (worst)** | **1st** | Only watchable result |

### Overall Composite (0-100)

| Rank | Model | Score | Wins |
|---|---|---|---|
| 1 | **Meta Muse Spark** | **75** | 2 |
| 2 | GPT-5.4 | 58 | 1 |
| 3 | Claude Opus 4.6 | 50 | 0 |
| 4 | Grok 4.2 | 42 | 0 |
| 5 | Gemini 3.1 | 25 | 0 |

- "In coding, 'it works' beats 'it's correct' every time."
- Meta's victory was marginal -- two first-place finishes in vision/analysis carried it past poor code performance.
- All five models unanimously recommended NVIDIA as best value; differentiation was in analysis depth and sourcing.

---

## Suggestions & Future Directions

1. **Task-specific model selection** -- No single model dominates; practitioners should match models to task types rather than relying on aggregate rankings.
2. **Hallucination failure modes as diagnostics** -- The way a model fails reveals its internal biases and can inform which model to avoid for which task.
3. **Functional testing over static analysis** -- Code benchmarks that measure quality without executing output miss the most important signal.

Limitations: single-shot testing (no retries), consensus-based ground truth (not independent human verification), small sample size (3 tests), time-specific stock data (April 8, 2026), Chrome-only rendering.

---

## Authors & Institutions

Ritesh Khanna, independent researcher (@treadon on X)
