> [[index|Wiki]] | [[summary|Summary]]

# SelfRefine — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-method-evaluation|Method and evaluation (1-7)]]

**In one sentence:** Self-Refine uses a single large language model (LLM — a large neural network trained on text that generates outputs word by word) as its own generator, feedback-giver, and refiner in a loop, and across 7 tasks it lifts strong models like GPT-3.5, ChatGPT, and GPT-4 by ~20% absolute on average without any extra training.

- Self-Refine loops three few-shot-prompted steps with one frozen model M: initial generation y0 = M(p_gen || x), self-feedback fbt = M(p_fb || x || yt), and refinement yt+1 = M(p_refine || x || history), stopping after up to 4 iterations or when the feedback contains a stop signal.
- Feedback must be actionable and specific (e.g. "slow for-loop, use n(n+1)/2" rather than "improve efficiency"): with ChatGPT/GPT-3.5, replacing targeted feedback with generic feedback drops Sentiment Reversal 43.2 to 31.2 and Acronym Generation 56.4 to 48.0, and removing feedback entirely collapses Sentiment Reversal to 0.
- Gains hold across all base models and all 7 tasks: GPT-4 + Self-Refine improves over base GPT-4 by 8.7 points on Code Optimization (27.3% to 36.0%), 49.2 points on Dialogue Response preference (25.4% to 74.6%), and 30.0 points on Constrained Generation (15.0% to 45.0%).
- Most improvement comes in early iterations with diminishing returns: averaged over models, Constrained Generation rises 29.0 (y0) to 40.3 (y1) to 46.7 (y2) to 49.7 (y3), while Code Optimization rises 22.0 to 28.8 and Sentiment Reversal 33.9 to 36.8 over three iterations.
- Math Reasoning barely moves (+0.0 to +0.2 points) because the model cannot spot its own errors — ChatGPT says "everything looks good" on 94% of math instances — though an external correctness signal restores 5%+ gains.
- Failure analysis on 70 Code Optimization and Math samples shows feedback is the bottleneck: of failures, 33% mislocalize the error and 61% suggest a wrong fix, with only 6% caused by the refiner botching good feedback; conversely the refiner fixes the output even from partially wrong feedback in 33% of successes.
- The method needs a strong instruction-following model: Vicuna-13B cannot reliably emit feedback in the required format and, even given oracle feedback, repeats outputs or hallucinates conversations instead of refining.

## 2. [[wiki/02-evaluation-appendices|Eval appendices A-K]]

**In one sentence:** The appendices specify 7 evaluation tasks with datasets and example feedback-refine steps, blind human and GPT-4 judging protocols, SOTA comparisons where Self-Refine tops prior few-shot and fine-tuned baselines, and ablations showing oracle gains, Vicuna-13b failure modes, non-monotonic multi-aspect scoring, error robustness, statistical significance, and two new hard tasks.

- Appendix A defines 7 tasks with exact sizes: Sentiment Reversal (1000 reviews), Dialogue Response (372 convos), Code Optimization (1000 programs), Code Readability (300 programs), Math Reasoning GSM8K (1319 questions), Acronym Generation (250), Constrained Generation CommonGen (200 samples), each with an x / y_t / feedback / y_{t+1} example.
- Blind human A/B eval (150 examples/task, authors as judges) prefers Self-Refine over direct baseline: Sentiment 75.00% vs 21.43% (3.57% tie), Acronym 44.59% vs 12.16% (43.24% tie), Response Generation 47.58% vs 19.66% (32.76% tie).
- GPT-4 is used as an automatic judge with fixed verbatim prompts that force explanation-first then a closed choice (A / B / both / neither) for sentiment, acronym (pronunciation, spelling, relation, connotation), and dialogue response.
- On SOTA comparisons Self-Refine beats the closest prior work Self-Correction on GSM8K with GPT-3 (55.7% vs 45.9%, +9.8pp) and reaches 94.5% with GPT-4 (vs PaL+GPT-4 93.3%), plus 36.0% optimized on PIE code-opt with GPT-4 using at most 4 samples vs 16-32 for rivals and 38.2% human reference.
- Vicuna-13b (LLaMA-13b fine-tuned on web chats) follows init but fails feedback/refine with empty or copied outputs, yet mixed setup (Vicuna init + ChatGPT feedback/refine) jumps Math Reasoning from 24.18% to 40.5%; oracle correctness-gated refinement adds +4.8pp for GPT-3, +1.4pp ChatGPT, +0.7pp GPT-4.
- Gains are statistically significant under Wilson intervals for nearly all GPT-4 tasks (4/7 ChatGPT, 3/7 GPT-3.5); acronym quality is non-monotonic so the algorithm keeps the max-score iteration, and dialogue error analysis finds 25% incorrect / 30% generic feedback but 60% robustness to bad feedback.
- Two new tasks are introduced: CommonGen-Hard (generate one coherent sentence from 20-30 concepts vs 3-5 in CommonGen) and a manually pruned 250-acronym set, plus a beyond-benchmarks demo where ChatGPT iteratively refines website layouts (ice-cream parlor, photosynthesis) from actionable feedback.

## 3. [[wiki/03-task-appendices|Task appendices L-R]]

**In one sentence:** Self-Refine improves code readability, dialogue quality, code speed, math accuracy, sentiment transfer, acronym quality, and hard constrained generation through iterated natural-language critique and refinement.

- Code readability (App. L): on 300 CodeNet snippets with text-davinci-003 critique/editor over N=5 iterations, all three heuristic metrics rise with iteration, and at T=0.7 Self-Refine beats 60-example human rewrites (meaningful-variable ratio 0.700 vs 0.653, comments/line 0.25 vs 0.24, function units 1.33 vs 0.70).
- Dialogue response generation (App. M): few-shot init/feedback/iterate with k=3 iterations and 10-aspect scoring (relevant, informative, interesting, consistent, helpful, engaging, specific, safe, understanding, fluent) lets Self-Refine beat init by wide margins on FED (342 auto + 100 human instances), e.g. human "Self-Refine wins" 36/48/54% vs "init wins" 23/18/16% across GPT-3.5/ChatGPT/GPT-4 judges.
- Code optimization (App. N): on PIE, Self-Refine with introspective feedback reaches 15.3–15.6% optimized and 2.90–3.74x speedup versus ~9.7–10.4% and ~3.0x for direct generation or ablated no-feedback refinement, proving multi-faceted feedback is load-bearing.
- Math reasoning (App. O): writing GSM-8k solutions as Python and using correctness-gated looping, Self-Refine accuracy climbs 71.34% → 73.39% → 75.06% → 75.74% → 76.19% over iterations 0–4 by catching errors like equating cup cost to plate cost.
- Sentiment reversal (App. P): few-shot k=4 loop until target sentiment reached achieves 100% Vader positive accuracy for both baselines but 93.6% vs 92% on negative targets, and pinpointed chain-of-thought feedback is critical (preference 85%→73% sentiment, 80.09%→58.92% dramatic when ablated to "something is wrong").
- Acronym generation (App. Q): on 250 pruned Wikipedia acronyms, 5-dimension feedback (pronunciation, spelling, title relation, connotation, well-knownness with CoT reasoning) plus human eval shows e.g. "Sequence to Sequence Learning with Neural Networks" improving STSLWN (5/25) to Seq2Seq (20/25).
- Constrained generation (App. R): CommonGen-Hard scales CommonGen from 3–5 to 20–30 concepts per sentence, and Self-Refine with GPT-3.5 wins on concept coverage, commonsense, and overall quality versus direct generation (Figure 18 winning-ratio bars ~35 vs ~10 and ~32 vs ~5).

## 4. [[wiki/04-prompts|Prompt appendix S (verbatim prompts)]]

**In one sentence:** Appendix S publishes the complete few-shot prompts for all seven SelfRefine tasks (Figures 19–38), showing the exact generation, 5-point/10-trait rubric feedback, and feedback-conditioned refine templates used for each task.

- Appendix S covers Figures 19–38 with three prompts per task where applicable: a generation prompt `p_gen` over input-output pairs, a feedback prompt `p_fb` over input-output-feedback triples, and a refine prompt `p_refine` over input-output-feedback-refined quadruples.
- Acronym Generation (Figs 19–21) uses 15 (title, acronym) few-shot examples for `p_gen` plus a 5-dimension rubric (pronunciation, spelling, title relation, positive connotation, well-known, each /5, total /25), with 3 scored-and-improved examples for feedback/refine.
- Code Optimization (Figs 22–24) pairs slow/fast programs from Madaan et al. (2023) for `p_gen` and reuses their explanations for feedback/refine, e.g. diagnosing a brute-force square-root loop over `range(n)` that checks `i**2 == n`.
- Code Readability (Figs 25–26) splits feedback and refinement into two turns: first "give one suggestion, don't fix the code" on `{code}`, then `{code} + {suggestion} + Now fix the code`.
- Constrained Generation (Figs 27–29) uses 10 concept-sentence examples for `p_gen`, six incoherent/missing-concept variants for feedback with `Concept Feedback` (missing concepts) and `Commonsense Feedback` (NONE or a reason), and an iterative "Okay, improve the sentence using the feedback" refine loop.
- Dialogue Response Generation (Figs 30–32) uses six dialogue examples for `p_gen` with 10 desired traits (Relevant, Informative, Interesting, Consistent, Helpful, Engaging, Specific, Safe, User understanding, Fluent, each /3, total /30), scored feedback (e.g. 17/30 for "That's just the way it is"), and a refine step that rewrites to a 30/30 response.
- Math Reasoning (Figs 33–35) sources `p_gen` from PaL (Gao et al., 2022) Python `def solution():` programs and builds feedback/refine from two Codex-failing training examples with block-by-block error analysis (e.g. `cup_cost = plate_cost` is wrong; correct is `(plate_cost * plates) - 1200` divided over 240 cups).
- Sentiment Reversal (Figs 36–38) builds positive/negative variants of one review with hand-written conversion descriptions, where feedback explains intensity levels (Very positive vs Positive vs Neutral vs Negative vs Very negative) via trigger words ("magical/top-notch" vs "good/fun" vs "questionable/subpar") and refine retries with "Okay, let's try again".

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. One frozen LLM loops generate, self-critique, and refine with no extra training.
2. Actionable, specific feedback is the load-bearing step, not the rewrite.
3. Early iterations capture most gains (~20 points average across 7 tasks and models).
4. Self-critique fails where the model can't spot its own errors (math barely moves).
5. Appendices confirm blind-judged wins, SOTA beats, and significance with ablations.
6. The loop only works on strong instruction-following models, with verbatim prompts published.
<!-- FIVE_MOVES_END -->
