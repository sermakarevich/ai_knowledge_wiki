# Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement

**Paper:** [Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement (Cho, Chawla, Cai, Liu, Zhu, Zhang, Sahu, 2026)](https://arxiv.org/abs/2606.27226)

## Human Readable TL;DR

Instead of asking an AI judge to slap one overall grade on a summary or chatbot reply ("this is a 4 out of 5"), this paper has it answer a checklist of small yes/no questions ("Does it mention the right entities?", "Any fabricated facts?", "Is it fluent?") and averages the answers into a score. It's like grading an essay with a detailed rubric instead of a single gut-feel letter grade -- you get the score AND a clear list of exactly what went wrong, which also lets you use that checklist to coach the essay-writer (or the grader) to do better next time.

## TL;DR

BinEval decomposes any evaluation criterion into a set of atomic binary (yes/no) questions via an LLM meta-prompt, has an evaluator LLM answer each question independently with an explanation, and aggregates the verdicts into interpretable per-dimension and overall scores. Across SummEval, Topical-Chat, and QAGS, BinEval matches or beats strong baselines (G-Eval, UniEval), especially on factual consistency, while avoiding the score-ceiling effects that plague holistic LLM judges. The same question-level disagreement signal drives a five-step iterative loop that updates evaluator prompts (cross-model / self-update) and generation prompts (tested on IFBench).

---

## Problem & Motivation

Evaluating LLM outputs is a bottleneck: human evaluation is slow and expensive, lexical metrics (ROUGE, BLEU, METEOR) correlate poorly with human judgment on open-ended generation, and holistic LLM-as-judge methods (G-Eval, UniEval, MT-Bench-style judges) return a single opaque score. A mediocre summary rating doesn't tell you *why* -- factual error, missing content, poor fluency, or low relevance are all invisible behind one number. This is especially costly in iterative development, where comparing prompts/models/decoding strategies needs feedback that is both accurate and actionable, not just a scalar.

---

## Main Original Ideas

1. **Binary Question Generation (meta-prompt decomposition).** A task-agnostic meta-prompt `M` maps a task prompt `T` to a question set `Q = F_LLM(T; M) = {q1, ..., qN}` in two steps: (1) *Summarize* `T` into explicit requirements `R = {r1, ..., rK}`; (2) *Decompose* each requirement into one or more binary yes/no questions, each paired with a concise violation example to disambiguate the "no" case. Questions partition into evaluation dimensions `D` (coherence, consistency, fluency, relevance, etc.); the same meta-prompt works for summarization, dialogue, or instruction-following by only changing `T`.

2. **Binary Evaluation and Scoring.** Given input `x`, output `y`, and question `qi`, the evaluator LLM produces `f_E(x,y,qi) ∈ {0,1}` plus a natural-language explanation. Per-dimension score is the mean over that dimension's questions; overall score is the mean over all `N` questions. Scores lie in [0,1] and can be affine-scaled to any target interval (e.g., 1-5 Likert) for comparison with existing frameworks.

3. **Cross-Model Prompt Update.** A five-step loop aligns a weaker target evaluator's prompt to a stronger source evaluator using question-level disagreement as the improvement signal (rather than holistic score gaps, which don't say *which* criterion is being judged inconsistently): (1) **Evaluate** both models on each case; (2) **Identify disagreements** `Δj` -- questions where source and target verdicts differ; (3) **Extract lessons** via a note-taker LLM that analyzes each disagreement in context, with semantic deduplication/merging of similar lessons; (4) **Update prompt** -- an updater LLM finds the relevant substring in the current prompt and rewrites it to incorporate the lesson; loop terminates when the target's per-dimension scores are within tolerance `ε` of the source's.

4. **Self Prompt Update (generation-side).** The same machinery improves a *generator*, not just an evaluator: generate outputs with the current prompt, evaluate them and collect the binary questions that failed (with explanations), extract generalized lessons via the note-taker LLM, deduplicate, and rewrite the generation prompt. Terminates when no evaluation errors remain or a max-iteration budget is hit.

---

## Key Findings

**SummEval (summary-level Spearman ρ / Kendall τ, Table 1):**

| Method | Coherence | Consistency | Fluency | Relevance | Average |
|---|---|---|---|---|---|
| UniEval (T5) | 0.575/0.442 | 0.446/0.371 | 0.449/0.371 | 0.426/0.325 | 0.474/0.377 |
| G-Eval (GPT-4) | 0.582/0.457 | 0.507/0.425 | 0.506/0.455 | **0.547/0.433** | 0.514/0.418 |
| BinEval (gpt-oss) | 0.523/0.448 | 0.585/0.548 | 0.252/0.235 | 0.428/0.366 | 0.447/0.399 |
| **BinEval (Claude)** | **0.652/0.541** | **0.655/0.615** | 0.540/0.470 | 0.404/0.339 | **0.563/0.491** |

- BinEval (Claude) is the strongest method overall and leads on coherence, consistency, and fluency; G-Eval (GPT-4) still wins on relevance.
- Largest gain is on **consistency** (factual quality): decomposing it into several targeted checks is especially effective. Relevance is the main exception -- it stays a comparatively holistic judgment that resists clean binary decomposition.
- BinEval's score distributions (violin plots) are wider and more human-like than UniEval/G-Eval, which compress scores and understate genuine variability -- this avoids the **ceiling effects** common in holistic LLM judges.

**Topical-Chat:** BinEval (Claude) achieves the best average Spearman correlation (0.632), with especially strong gains on naturalness and engagingness -- decomposition helps with subjective conversational criteria too.

**QAGS (hallucination-focused):** BinEval (Claude) best average Spearman (0.620); BinEval (gpt-oss) substantially outperforms G-Eval (gpt-oss) under the same backbone, reinforcing that decomposing factual consistency into several targeted questions beats a single holistic/Boolean judgment on hallucination-prone data.

**Iterative evaluator prompt update on SummEval (Table 2, test-set Spearman ρ, Δ = absolute improvement):**

| Dimension | Self-Update Δ | Cross-Model Δ |
|---|---|---|
| Coherence | +0.089 | +0.070 |
| Consistency | +0.091 | **+0.136** |
| Fluency | **+0.119** | +0.072 |
| Relevance | .000 | .000 |
| **Average** | **+0.075** | **+0.070** |

Self-update and cross-model update are complementary: self-update helps most on coherence/fluency, cross-model update helps most on consistency. Relevance never improves under either mode -- inspection shows lesson-driven refinements over-decompose relevance into overly granular checks (per actor/motivation/background event), making the evaluator *more severe than humans*, not better aligned.

**Generation prompt update on IFBench (Table 3, strict accuracy %):** Self-update peaks at **38.0%** at iteration 3 (+3.4pp over the 34.6% baseline) but collapses to 26.1% at iteration 4 from repeated prompt rewriting (instruction bloat). Cross-model update shows no improvement and declines after the first step -- a stricter reference judge can overcorrect rather than refine.

**IFBench per-category (Table 4):** Format (+17pp, 52→69) and Sentence (+17pp, 25→42) constraints -- *promptable* failures -- improve substantially once given clearer structural guidance. Count, Ratio, Words, and Repeat constraints -- *computational* failures requiring precise counting/tracking during generation -- show little to no improvement; lessons diagnose these failures correctly but instructions like "maintain an internal counter" don't grant new computational ability.

**Why decomposition works (phi-coefficient analysis, Section 5.6):** three mechanisms, contributing unequally by dimension:
- *Complexity reduction* -- each binary question isolates one verifiable property instead of one multi-faceted rating.
- *Variance reduction via aggregation* -- averaging N weakly-correlated binary classifiers reduces variance ~1/N (mean inter-question φ = 0.38 across dimensions).
- *Coverage of failure modes* -- low-correlation question pairs catch disjoint failures (e.g., spelling vs. punctuation in fluency, φ = 0.02).
- Consistency is the outlier: weakest variance reduction/coverage (φ up to 0.79 between related questions) yet the *largest* correlation gain over UniEval (+0.195 Spearman) -- for factual checks, complexity reduction alone is the dominant driver.

**Qualitative case study (Figure 4):** A SummEval consistency example with three factual errors (misattribution, fabricated URL, conflation of two parties). BinEval (Claude) catches 4/7 sub-questions as violations → score 1.57, close to the human rating of 2.0. G-Eval and UniEval both assign a perfect 5.0 because the summary is "surface-plausible" -- they judge global fluency/topicality, not individual claims, and miss every error.

---

## Suggestions & Future Directions

1. **Agentic and multi-turn extensions.** The authors flag fine-grained, claim-level feedback as especially valuable for diagnosing *where and why* a system fails in agentic and multi-turn settings -- named as the natural next step.
2. **Question-design dependency (limitation).** The method's final score can only reflect criteria captured by the generated questions; if the meta-prompt misses an important requirement, the score misses it too.
3. **Linearity assumption (limitation).** BinEval assumes the fraction of satisfied questions maps roughly linearly to overall quality -- shown not to hold cleanly for relevance, which stays a holistic judgment.
4. **Efficiency/diagnostic tradeoff.** BinEval trades computational cost (more model calls: question generation + per-question answering, plus note-taking and prompt-rewriting during optimization) for interpretability and actionable diagnosis.
5. **Human oversight in high-stakes settings (impact statement).** Evaluator models inherit the biases and blind spots of their underlying LLMs, so any deployment of BinEval should be paired with human oversight where stakes are high.

---

## Authors & Institutions

Sangwoo Cho, Kushal Chawla, Pengshan Cai, Zefang Liu, Chenyang Zhu, Shi-Xiong Zhang, Sambit Sahu — all Capital One, AI Foundations, McLean, VA 22102, USA. Accepted to the 2nd Workshop on Compositional Learning at ICML 2026, Seoul, South Korea.
