# Self-Refine: Iterative Refinement with Self-Feedback

**Paper:** [Self-Refine: Iterative Refinement with Self-Feedback (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651)

## Human Readable TL;DR

Imagine a writer who drafts an article, then puts on an editor's hat to write margin notes about what is weak ("this part is boring, add an example"), then puts the writer's hat back on to fix the draft using those notes — and repeats this a few times until the piece reads well. Self-Refine does exactly this, except one computer program plays the writer, the editor, and the rewriter all by itself, with no extra schooling. Tested on seven kinds of jobs — writing replies, speeding up computer code, tidying code, solving math word problems, flipping a review from happy to angry, inventing short names, and squeezing many required words into one sentence — it made strong programs about 20% better on average. The one place it barely helped was math, because the program usually told itself "everything looks good" even when the answer was wrong.

## TL;DR

Self-Refine loops three few-shot-prompted steps with one frozen model M: initial generation y0 = M(p_gen || x), self-feedback fbt = M(p_fb || x || yt), and history-aware refinement yt+1 = M(p_refine || x || y0 || fb0 || ... || yt || fbt), stopping after up to 4 iterations or when the feedback emits a stop signal. Feedback is explicitly prompted to be actionable and specific (naming the concrete span and fix), and ablations show targeted feedback is load-bearing versus generic or no feedback. Across 7 tasks it beats the same base model (GPT-3.5, ChatGPT, GPT-4, Codex) in every cell by ~20% absolute on average — e.g. GPT-4 Dialogue Response preference 25.4% to 74.6% and Constrained Generation 15.0% to 45.0% — with most gains in early iterations, except Math Reasoning (+0.0 to +0.2) where the model cannot spot its own errors.

---

## Problem & Motivation

Large language models produce coherent first drafts but miss multifaceted requirements such as dialogue quality (engaging, helpful, specific), code efficiency and readability, or covering 20–30 required concepts in one sentence. Classic refinement approaches need domain data, trained reward or refinement models, per-task fine-tuning, or costly human labels, which limits reuse across tasks. Self-Refine asks whether the same model can generate feedback on its own output and then refine it, iteratively, using only few-shot prompting with no extra training, no supervised data, and no reinforcement learning. This matters because it promises a cheap, general, training-free way to unlock capability already latent in single-pass decoding.

---

## Main Original Ideas

1. **Single-model generate–feedback–refine loop.** One frozen model M plays all three roles via three task-specific few-shot prompts {p_gen, p_fb, p_refine}: y0 = M(p_gen || x), fbt = M(p_fb || x || yt), yt+1 = M(p_refine || x || history). No weights change; the only supervision is the few-shot examples embedded in the three prompts.
2. **Actionable, specific, multi-aspect natural-language feedback.** Feedback must name the concrete defect and fix (e.g. "slow for-loop, use n(n+1)/2") rather than generic advice ("improve efficiency"), and can cover multiple aspects at once (code efficiency/readability, 10 dialogue traits, 5 acronym dimensions). This lets the same generative model critique itself while reusing pretrained models like GPT-4.
3. **History-aware refinement with a prompted stop condition.** The refine step actually used sees all past outputs and feedback (Eq. 4 / Algorithm 1), so the model avoids repeating mistakes, and the loop stops via a per-task criterion: a fixed timestep or a stopping indicator the model is prompted to emit inside p_fb.
4. **Training-free instantiation across 7 diverse tasks plus 2 new benchmarks.** The same recipe is applied to Dialogue Response, Code Optimization, Code Readability, Math Reasoning, Sentiment Reversal, Acronym Generation, and Constrained Generation, including two newly introduced hard tasks: CommonGen-Hard (20–30 concepts per sentence vs 3–5) and a manually pruned 250-acronym set.
5. **Blind human plus GPT-4-as-judge evaluation protocol.** Where automated metrics are unavailable, outputs are compared by blind human A/B preference (150 examples/task, authors as judges) and by GPT-4 judging with fixed verbatim prompts that force explanation-first then a closed choice (A / B / both / neither), with reported human–GPT-4 correlation of 68–82%.

---

## Key Findings

| Task | GPT-3.5 Base | GPT-3.5 + Self-Refine | ChatGPT Base | ChatGPT + Self-Refine | GPT-4 Base | GPT-4 + Self-Refine |
|---|---|---|---|---|---|---|
| Sentiment Reversal | 8.8 | 30.4 (+21.6) | 11.4 | 43.2 (+31.8) | 3.8 | 36.2 (+32.4) |
| Dialogue Response | 36.4 | 63.6 (+27.2) | 40.1 | 59.9 (+19.8) | 25.4 | 74.6 (+49.2) |
| Code Optimization | 14.8 | 23.0 (+8.2) | 23.9 | 27.5 (+3.6) | 27.3 | 36.0 (+8.7) |
| Code Readability | 37.4 | 51.3 (+13.9) | 27.7 | 63.1 (+35.4) | 27.4 | 56.2 (+28.8) |
| Math Reasoning | 64.1 | 64.1 (+0.0) | 74.8 | 75.0 (+0.2) | 92.9 | 93.1 (+0.2) |
| Acronym Generation | 41.6 | 56.4 (+14.8) | 27.2 | 37.2 (+10.0) | 30.4 | 56.0 (+25.6) |
| Constrained Generation | 28.0 | 37.0 (+9.0) | 44.0 | 67.0 (+23.0) | 15.0 | 45.0 (+30.0) |

- Self-Refine beats the same base model on every model–task cell and beats prior state of the art on all tasks; nearly all GPT-4 gains are significant under Wilson intervals (4/7 for ChatGPT, 3/7 for GPT-3.5).
- Feedback quality is load-bearing: with ChatGPT/GPT-3.5, generic feedback drops Sentiment Reversal 43.2 to 31.2 and Acronym 56.4 to 54.0, and no feedback collapses Sentiment Reversal to 0 and Acronym to 48.0; pinpointed chain-of-thought feedback beats generic "something is wrong" 85% to 73% (sentiment) and 80.09% to 58.92% (dramatic).
- Most improvement comes early with diminishing returns: averaged over models, Constrained Generation rises 29.0 (y0) → 40.3 (y1) → 46.7 (y2) → 49.7 (y3); Code Optimization 22.0 → 27.0 → 27.9 → 28.8; Sentiment Reversal 33.9 → 34.9 → 36.1 → 36.8.
- The gain is from feedback-driven refinement, not extra samples: one Self-Refine output is preferred by human judges over 4 independent samples (k=4) without feedback/refine.
- Math Reasoning barely moves because error detection fails — ChatGPT says "everything looks good" on 94% of math instances — though an external oracle correctness signal restores gains (+4.8pp GPT-3.5, +1.4pp ChatGPT, +0.7pp GPT-4; iterated accuracy 71.34% → 76.19% over 0–4 steps with gating).
- Failure analysis on 70 Code Optimization and Math samples: feedback is the bottleneck — 33% mislocalize the error, 61% suggest a wrong fix, only 6% is the refiner botching good feedback; conversely the refiner still recovers from partially wrong feedback in 33% of successes. Dialogue error analysis: 25% incorrect / 30% generic feedback, yet the model ignores bad feedback 60% of the time.
- Multi-aspect quality can be non-monotonic (e.g. acronym USTACCSF 11 → TACC-SIM 17 → TACCSF 12 → TACC-SIMF 17 across pronunciation/spelling/relation/connotation subscores); the fix is explicit numeric per-aspect scores and keeping the max-score iteration.
- Strong bases unlock more: GPT-4 + Self-Refine tops smaller-model variants on all tasks even where base GPT-4 started lower, and reaches 94.5% on GSM8K (vs Self-Correction 45.9% on GPT-3, PaL+GPT-4 93.3%) and 36.0% optimized on PIE code-opt with at most 4 samples vs 16–32 for rivals (human reference 38.2%).
- Weak instruction-following models fail the loop: Vicuna-13B cannot reliably emit feedback in the required format and ignores refine prompts even given oracle feedback — yet Vicuna init + ChatGPT feedback/refine jumps Math Reasoning 24.18% to 40.5%.
- Beyond benchmarks: ChatGPT iteratively refines rudimentary website layouts (ice-cream parlor, photosynthesis page) via actionable edits (colors, font sizes, icons, dividers); code-readability Self-Refine at T=0.7 matches or beats 60-example human rewrites (meaningful-variable ratio 0.700 vs 0.653, comments/line 0.25 vs 0.24, function units 1.33 vs 0.70).

---

## Suggestions & Future Directions

1. **Require strong instruction-following base models.** The loop only works when the model can learn feedback and refinement formats in context; extend prompt engineering or lightweight tuning so smaller open models (e.g. Vicuna-13B class) can participate.
2. **Add external correctness signals for math-like tasks.** Self-detection fails on subtle operator/single-line errors; gate refinement on compilers, unit tests, or answer checkers, which already restores 5%+ gains.
3. **Score aspects numerically and keep the best iteration.** Adopt explicit per-aspect scores with max-score selection to handle non-monotonic trade-offs in multi-aspect tasks such as acronyms.
4. **Reproduce beyond closed, English-only models.** Experiments use undisclosed closed models (GPT-3.5, ChatGPT, GPT-4, Codex) at monetary cost on English-only datasets; rerun on open models and other languages (code and outputs are released for reproducibility).
5. **Guard against misuse of steering.** Prompted refinement could be misused to steer models toward more toxic or harmful text; add safety constraints to the feedback/refine prompts.
6. **Extend introspective multi-dimensional feedback to new domains.** Follow the website-generation, CommonGen-Hard, and readability case studies into further creative and real-world generation tasks demanding commonsense and coherence.

---

## Authors & Institutions

Madaan et al. (2023) — full author list and affiliations not specified in the verified wiki pages.
