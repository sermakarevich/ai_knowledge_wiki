# Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement

**Paper:** [Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement (Cho et al., 2026)](https://arxiv.org/abs/2606.27226)

## Human Readable TL;DR

Grading an essay with a single 1-10 score tells you nothing about *why* it got that score. This paper's fix: instead of asking an AI judge "how good is this, 1-5?", ask it a checklist of yes/no questions -- "does this avoid made-up facts?", "does it stay on topic?" -- and average the answers into a score. Because each yes/no answer comes with a reason, you can see exactly which checklist item failed, and even feed that failure back to automatically rewrite the instructions given to the judge or to the AI doing the original task, making both better over time.

## TL;DR

BINEVAL replaces holistic LLM-judge scoring with a two-step pipeline: a meta-prompt decomposes a task's evaluation criteria into atomic binary (yes/no) questions, and an evaluator LLM answers each independently, averaging verdicts into calibrated per-dimension and overall scores. Across SummEval, Topical-Chat, and QAGS, BINEVAL (with Claude Sonnet 4 as evaluator) matches or beats UniEval and G-Eval on correlation with human judgments, tracks human score distributions more faithfully (avoiding ceiling effects), and is especially strong on factual-consistency (QAGS). The same disagreement signal from binary verdicts drives an iterative prompt-optimization loop that improves evaluator prompts (SummEval) and generation prompts (IFBench) under both self-update and cross-model settings, though gains are capped: iteration helps when the model has the capability but needs clearer guidance, and can degrade performance (via prompt bloat) when the failure is a genuine capability gap.

---

## Problem & Motivation

LLM generation has outpaced LLM evaluation. Human evaluation is slow and expensive; lexical metrics (ROUGE, BLEU, BERTScore) correlate poorly with human judgment on open-ended text; and holistic "LLM-as-judge" methods (G-Eval, Chatbot Arena-style judges) return a single opaque score that is hard to debug -- if a summary gets a mediocre rating, there's no way to tell whether the cause is factual inconsistency, weak relevance, missing content, or poor fluency. This is especially costly during iterative development, where comparing prompts/models/decoding strategies needs feedback that is both accurate *and* actionable.

The paper's core premise: instead of asking a model for one broad judgment, ask it a set of small, checkable questions. Decomposing evaluation criteria into atomic yes/no questions turns a black-box verdict into a structured diagnostic signal usable for both inspection and optimization.

---

## Main Original Ideas

1. **Binary question decomposition (BinEval).** A meta-prompt performs two steps on a task prompt T: (a) *Summarize* T into explicit requirements R = {r1...rK}; (b) *Decompose* each requirement into one or more binary questions, each paired with a concise violation example. The meta-prompt is task-agnostic -- the same prompt generates questions for summarization, dialogue, or instruction-following by only changing T.

2. **Score aggregation via averaged verdicts.** An evaluator LLM answers each binary question independently (with an explanation), giving f(x,y,qi) in {0,1}. Per-dimension score = mean of verdicts in that dimension's question set; overall score = mean across all N questions. Both lie in [0,1] and can be affine-scaled to any target range (e.g. 1-5 Likert) for comparison with other frameworks.

3. **Cross-model prompt update via disagreement.** When a stronger source evaluator and a weaker target evaluator disagree on specific binary questions, that disagreement is a fine-grained, per-criterion improvement signal (unlike a holistic score gap). A note-taker LLM extracts generalized "lessons" from disagreements, deduplicates them semantically, and an updater LLM rewrites the target's prompt to incorporate each lesson -- iterating until the target's per-dimension scores converge to the source's within tolerance ε.

4. **Self prompt update for generation.** The same disagreement-free version of the loop (evaluator vs. own failing outputs) is applied to a *generator's* prompt: generate → evaluate against binary questions → extract lessons from failing questions → dedupe → rewrite the generation prompt. Iterates until no failures remain or a max-iteration budget is hit.

5. **Decomposition mechanism analysis.** The paper attributes BinEval's gains to three measurable mechanisms: complexity reduction (one property per question vs. one multi-faceted judgment), variance reduction via averaging weakly-correlated binary classifiers, and coverage of otherwise-missed failure modes -- quantified per-dimension via yes-rate spread and pairwise phi-coefficient correlation between questions.

---

## Key Findings

**Correlation with human judgment (Spearman ρ / Kendall τ, higher is better), averaged across dimensions:**

| Method | SummEval | Topical-Chat | QAGS (r/ρ/τ avg) |
|---|---|---|---|
| UniEval (T5) | 0.474 / 0.377 | 0.552 / 0.417 | 0.571 / 0.575 / 0.465 |
| G-Eval (GPT-4) | **0.514** / **0.418** | 0.575 / 0.588 | 0.599 / 0.611 / 0.525 |
| G-Eval (gpt-oss-120b) | 0.436 / 0.392 | 0.541 / 0.478 | 0.140 / 0.132 / 0.131 |
| UniEval (gpt-oss-120b) | 0.254 / 0.235 | 0.144 / 0.132 | 0.452 / 0.436 / 0.424 |
| BinEval (gpt-oss-120b) | 0.447 / 0.399 | 0.539 / 0.450 | 0.543 / 0.563 / 0.492 |
| **BinEval (Claude Sonnet 4)** | 0.563 / 0.491 | **0.632** / **0.525** | **0.604** / **0.620** / **0.534** |

- BinEval (Claude) is best overall on SummEval and Topical-Chat and best average on QAGS (its strongest benchmark, targeting hallucination detection); G-Eval (GPT-4) narrowly leads only on SummEval relevance (0.547 vs 0.404 Spearman).
- BinEval better matches human *score distributions* (violin plots) and avoids the ceiling effects that flatten UniEval/G-Eval scores near the top of the scale, giving better discrimination between borderline and clearly-flawed outputs.
- On a worked example, a summary with 3 real factual errors got Human=2.0, BinEval(Claude)=1.57 (catches 4/7 error-relevant questions), while G-Eval(gpt-oss) and UniEval(gpt-oss) both scored it 5.0 -- a holistic judge that "looks consistent" at a glance misses errors a decomposed checklist catches.

**Iterative prompt optimization:**

| Task | Mode | Base → Best | Δ |
|---|---|---|---|
| SummEval evaluator prompt (avg. Spearman) | Self-update | .440 → .515 | +.075 |
| SummEval evaluator prompt (avg. Spearman) | Cross-model | .451 → .520 | +.070 |
| IFBench generation prompt (strict accuracy %) | Self-update | 34.6 → 38.0 (iter 3), then collapses to 26.1 (iter 4) | +3.4 pp (peak) |
| IFBench generation prompt (strict accuracy %) | Cross-model | 35.9 → 33.8, then stops (declines) | 0.0 pp |

- Self-update's biggest single-dimension SummEval gain: fluency (+0.119). Cross-model's biggest gain: consistency (+0.136, "the largest improvement in our experiments") -- Claude correctly separated *omission* from *contradiction*, a distinction gpt-oss conflated.
- SummEval relevance did not improve under either mode (Δ = 0.000); a failure case in the appendix shows relevance Spearman actually *dropping* from .505 to .357 after over-strict lessons made the evaluator penalize summaries humans rated fine -- "decomposing an inherently holistic, tolerant criterion into strict atomic checks produces a harsher evaluator that diverges from human behavior."
- IFBench shows a sharp promptable/computational split: format (+17pp: 52→69) and sentence (+17pp: 25→42) constraints improve with clearer instructions; count, ratio, words, repeat barely move or degrade, because they require precise computation during generation that better prompting cannot supply. The generation meta-prompt grew from 22 characters to 6,248 characters over 4 iterations, and the accumulated (largely ineffective) computational instructions eventually degraded even the previously-improved format category -- a "carrying capacity" for prompt-based optimization.

**Why decomposition works (mechanistic analysis):** consistency shows the *weakest* variance reduction and failure-mode coverage (questions are highly correlated, mean φ=0.58) yet the *largest* gain over UniEval (+0.195 Spearman) -- suggesting complexity reduction (breaking one holistic judgment into targeted sub-checks) alone can dominate, even without diverse/independent questions.

---

## Suggestions & Future Directions

1. Extend atomic binary decomposition to **agentic and multi-turn settings**, where fine-grained, claim-level feedback is especially valuable for pinpointing where and why a system goes wrong.
2. Practitioners can inspect generated questions' yes-rate spread, inter-question correlation, and pairwise coverage *before* deploying BinEval, to anticipate where decomposition will help most and where the question set needs refinement.
3. Explicitly acknowledged limitations: (a) the method depends on question quality -- missing criteria produce a blind score; (b) it assumes fraction-of-satisfied-questions maps roughly linearly to overall quality, which "need not always hold"; (c) it trades efficiency for diagnostic value (more model calls, more text processed than a single holistic judgment); (d) decomposition helps most for concrete, checkable criteria (e.g. factual consistency) and less for subjective, holistic qualities; (e) prompt-update loops fix guidance problems but cannot fix underlying model capability gaps, and can make things worse via instruction bloat; (f) evaluator models can inherit the biases of their underlying LLM, so high-stakes deployments should pair BinEval with human oversight.

---

## Authors & Institutions

Sangwoo Cho, Kushal Chawla, Pengshan Cai, Zefang Liu, Chenyang Zhu, Shi-Xiong Zhang, Sambit Sahu -- Capital One, AI Foundations, McLean, VA, USA. Accepted to the 2nd Workshop on Compositional Learning at ICML 2026, Seoul, South Korea.
