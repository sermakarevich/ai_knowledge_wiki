---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# SelfRefine — Retrieval Practice

## Section 1: Method and evaluation (1-7)

### Q1 (core recall): What is the Self-Refine loop — the three steps, the model setup, and the headline gain?

<details>
<summary>Answer</summary>

One frozen model M (LLM — a large neural network trained on text that generates outputs word by word) plays generator, feedback-giver, and refiner in a loop with few-shot prompts: initial generation y0 = M(p_gen || x), self-feedback fbt = M(p_fb || x || yt), refinement yt+1 = M(p_refine || x || history), stopping after up to 4 iterations or a stop signal in the feedback. Across 7 tasks it lifts strong models (GPT-3.5, ChatGPT, GPT-4) by ~20% absolute on average with no extra training.

</details>

### Q2 (core recall): What numbers prove feedback must be targeted, that gains hold across models, and that early iterations matter most?

<details>
<summary>Answer</summary>

Targeted vs generic with ChatGPT/GPT-3.5: replacing actionable specific feedback with generic feedback drops Sentiment Reversal 43.2 to 31.2 and Acronym Generation 56.4 to 48.0; removing feedback entirely collapses Sentiment Reversal to 0. Cross-model gains (GPT-4 + Self-Refine over base GPT-4): Code Optimization +8.7 points (27.3% to 36.0%), Dialogue Response preference +49.2 points (25.4% to 74.6%), Constrained Generation +30.0 points (15.0% to 45.0%). Early-iteration curve (averaged over models): Constrained Generation 29.0 (y0) to 40.3 (y1) to 46.7 (y2) to 49.7 (y3); Code Optimization 22.0 to 28.8 and Sentiment Reversal 33.9 to 36.8 over three iterations — diminishing returns.

</details>

### Q3 (elaboration): Why does Math Reasoning barely move under Self-Refine, and what breaks if the model cannot spot its own errors?

<details>
<summary>Answer</summary>

Math Reasoning gains only +0.0 to +0.2 points because the model cannot spot its own errors — ChatGPT says "everything looks good" on 94% of math instances, so the loop stops with no correction. Failure analysis on 70 Code Optimization and Math samples confirms feedback is the bottleneck: of failures, 33% mislocalize the error and 61% suggest a wrong fix, with only 6% caused by the refiner botching good feedback. If error detection fails, iteration is wasted; an external correctness signal restores 5%+ gains. Conversely the refiner is robust — it fixes the output even from partially wrong feedback in 33% of successes.

</details>

## Section 2: Eval appendices A-K

### Q4 (core recall): What are the 7 evaluation tasks and sizes, the blind human A/B results, and the SOTA comparison numbers?

<details>
<summary>Answer</summary>

Appendix A sizes: Sentiment Reversal (1000 reviews), Dialogue Response (372 convos), Code Optimization (1000 programs), Code Readability (300 programs), Math Reasoning GSM8K (1319 questions), Acronym Generation (250), Constrained Generation CommonGen (200 samples). Blind human A/B (150 examples/task, authors as judges) prefers Self-Refine: Sentiment 75.00% vs 21.43% (3.57% tie), Acronym 44.59% vs 12.16% (43.24% tie), Response Generation 47.58% vs 19.66% (32.76% tie). GPT-4 auto-judge uses fixed verbatim prompts forcing explanation-first then closed choice (A / B / both / neither). SOTA: beats Self-Correction on GSM8K with GPT-3 (55.7% vs 45.9%, +9.8pp), reaches 94.5% with GPT-4 (vs PaL+GPT-4 93.3%), and 36.0% optimized on PIE code-opt with GPT-4 using at most 4 samples vs 16-32 for rivals (38.2% human reference).

</details>

## Section 3: Task appendices L-R

### Q5 (core recall): What per-task numbers show Self-Refine working across readability, dialogue, code speed, math, sentiment, acronyms, and hard constrained generation?

<details>
<summary>Answer</summary>

Code readability (300 CodeNet snippets, text-davinci-003, N=5 iterations, T=0.7): beats 60-example human rewrites on meaningful-variable ratio 0.700 vs 0.653, comments/line 0.25 vs 0.24, function units 1.33 vs 0.70. Dialogue (k=3 iterations, 10-aspect scoring, FED 342 auto + 100 human): human "Self-Refine wins" 36/48/54% vs "init wins" 23/18/16% across GPT-3.5/ChatGPT/GPT-4. Code optimization (PIE, introspective feedback): 15.3–15.6% optimized and 2.90–3.74x speedup vs ~9.7–10.4% and ~3.0x for direct/no-feedback. Math (GSM-8k Python, correctness-gated): 71.34% → 73.39% → 75.06% → 75.74% → 76.19% over iterations 0–4. Sentiment (k=4): 100% Vader positive accuracy both baselines, 93.6% vs 92% on negative targets. Acronym (250 pruned): e.g. "Sequence to Sequence Learning with Neural Networks" STSLWN (5/25) to Seq2Seq (20/25) on the 5-dimension rubric. Constrained (CommonGen-Hard, 20–30 concepts vs 3–5): GPT-3.5 Self-Refine wins on coverage, commonsense, overall quality (bars ~35 vs ~10 and ~32 vs ~5).

</details>

### Q6 (elaboration): Why does Vicuna-13B fail at Self-Refine while a mixed Vicuna + ChatGPT setup works — and what breaks if acronym scoring is treated as monotonic?

<details>
<summary>Answer</summary>

Self-Refine needs a strong instruction-following model: Vicuna-13B (LLaMA-13b fine-tuned on web chats) follows init but fails feedback/refine with empty or copied outputs, and even given oracle feedback repeats outputs or hallucinates conversations instead of refining. The mixed setup (Vicuna init + ChatGPT feedback/refine) jumps Math Reasoning from 24.18% to 40.5%, proving the bottleneck is critique-and-repair ability, not the draft — similarly oracle correctness-gated refinement adds +4.8pp GPT-3, +1.4pp ChatGPT, +0.7pp GPT-4. For acronyms, quality is non-monotonic across iterations, so always taking the last output breaks results; the algorithm keeps the max-score iteration. Dialogue error analysis shows the same robustness logic: 25% incorrect / 30% generic feedback is tolerated with 60% robustness to bad feedback.

</details>

## Section 4: Prompt appendix S (verbatim prompts)

### Q7 (transfer): You must build a Self-Refine loop for a new code-review bot using only the Appendix S prompt patterns. What three prompts do you write, and what task-specific rubric/feedback shapes do you copy?

<details>
<summary>Answer</summary>

Copy the three-prompt template from Figures 19–38: p_gen over input-output pairs, p_fb over input-output-feedback triples, p_refine over input-output-feedback-refined quadruples. For the review bot, mirror Code Readability (Figs 25–26): split into two turns — first "give one suggestion, don't fix the code" on {code}, then {code} + {suggestion} + "Now fix the code". Borrow rubric shapes: Acronym's 5-dimension scored rubric (each /5, total /25, with 3 scored-and-improved examples) or Dialogue's 10-trait rubric (each /3, total /30, e.g. 17/30 for a weak response rewritten to 30/30); for code-opt reuse slow/fast pairs plus explanations (e.g. brute-force square-root loop over range(n)). For constrained outputs use the Concept Feedback (missing concepts) plus Commonsense Feedback (NONE or a reason) split and the "Okay, improve the sentence using the feedback" refine loop, and for math use Python def solution(): programs with block-by-block error analysis.

</details>

## Section 5: Evaluation

### Q8 (evaluation): Per [[critical_thinking|Critical Analysis]], why is Self-Refine structurally blind to its own Math Reasoning failure, and what does the paper's fix concede about self-feedback alone?

<details>
<summary>Answer</summary>

Because the same frozen model both drafts and grades its own output, it shares its blind spots with its own judgment — on GSM8K it says "everything looks good" on 94% of instances, so the loop stops without correcting real errors. The paper's fix (an external correctness/oracle signal recovering 5%+ gains) quietly concedes that self-feedback alone is insufficient whenever the model's generation errors and evaluation errors overlap — self-critique needs a source of ground truth outside the model for verifiable-correctness tasks, not just more iterations.

</details>
