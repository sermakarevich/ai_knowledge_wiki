> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Eval appendices A-K

**In one sentence:** The appendices specify 7 evaluation tasks with datasets and example feedback-refine steps, blind human and GPT-4 judging protocols, SOTA comparisons where Self-Refine tops prior few-shot and fine-tuned baselines, and ablations showing oracle gains, Vicuna-13b failure modes, non-monotonic multi-aspect scoring, error robustness, statistical significance, and two new hard tasks.

## Key points
- Appendix A defines 7 tasks with exact sizes: Sentiment Reversal (1000 reviews), Dialogue Response (372 convos), Code Optimization (1000 programs), Code Readability (300 programs), Math Reasoning GSM8K (1319 questions), Acronym Generation (250), Constrained Generation CommonGen (200 samples), each with an x / y_t / feedback / y_{t+1} example.
- Blind human A/B eval (150 examples/task, authors as judges) prefers Self-Refine over direct baseline: Sentiment 75.00% vs 21.43% (3.57% tie), Acronym 44.59% vs 12.16% (43.24% tie), Response Generation 47.58% vs 19.66% (32.76% tie).
- GPT-4 is used as an automatic judge with fixed verbatim prompts that force explanation-first then a closed choice (A / B / both / neither) for sentiment, acronym (pronunciation, spelling, relation, connotation), and dialogue response.
- On SOTA comparisons Self-Refine beats the closest prior work Self-Correction on GSM8K with GPT-3 (55.7% vs 45.9%, +9.8pp) and reaches 94.5% with GPT-4 (vs PaL+GPT-4 93.3%), plus 36.0% optimized on PIE code-opt with GPT-4 using at most 4 samples vs 16-32 for rivals and 38.2% human reference.
- Vicuna-13b (LLaMA-13b fine-tuned on web chats) follows init but fails feedback/refine with empty or copied outputs, yet mixed setup (Vicuna init + ChatGPT feedback/refine) jumps Math Reasoning from 24.18% to 40.5%; oracle correctness-gated refinement adds +4.8pp for GPT-3, +1.4pp ChatGPT, +0.7pp GPT-4.
- Gains are statistically significant under Wilson intervals for nearly all GPT-4 tasks (4/7 ChatGPT, 3/7 GPT-3.5); acronym quality is non-monotonic so the algorithm keeps the max-score iteration, and dialogue error analysis finds 25% incorrect / 30% generic feedback but 60% robustness to bad feedback.
- Two new tasks are introduced: CommonGen-Hard (generate one coherent sentence from 20-30 concepts vs 3-5 in CommonGen) and a manually pruned 250-acronym set, plus a beyond-benchmarks demo where ChatGPT iteratively refines website layouts (ice-cream parlor, photosynthesis) from actionable feedback.

---

## Appendix A — Evaluation tasks (Table 4)

| Task | Description | Dataset / size | Example x -> y_t -> fb -> y_{t+1} |
|---|---|---|---|
| Sentiment Reversal | Rewrite reviews to reverse sentiment | Zhang et al. 2015, 1000 passages | x: "The food was fantastic..." / y_t: "The food was disappointing..." / fb: Increase negative sentiment / y_{t+1}: "The food was utterly terrible..." |
| Dialogue Response Generation | Rich conversational responses | Mehri and Eskenazi 2020, 372 convos | x: "What's the best way to cook pasta?" / y_t: "The best way to cook pasta is to..." / fb: Make response relevant, engaging, safe / y_{t+1}: "Boil water, add salt, and cook pasta..." |
| Code Optimization | Enhance Python efficiency | Madaan et al. 2023, 1000 programs | x: nested loop matrix product / y_t: NumPy dot / fb: improve time complexity / y_{t+1}: NumPy optimized matmul |
| Code Readability Improvement | Refactor for readability | Puri et al. 2021 (CodeNet), 300 programs | x: unclear names, no comments / y_t: descriptive names, comments / fb: enhance naming, add comments / y_{t+1}: clear variables, meaningful comments |
| Math Reasoning | Solve math word problems | Cobbe et al. 2021 (GSM8K), 1319 questions | x: "Olivia has $23, buys 5 bagels at $3 each" / y_t: solution in Python / fb: show step-by-step / y_{t+1}: solution with detailed explanation |
| Acronym Generation | Acronyms for a title | Appendix Q/K set, 250 acronyms | x: "Radio Detecting and Ranging" / y_t: RDR / fb: context-relevant, easy pronunciation / y_{t+1}: RADAR |
| Constrained Generation | Sentences with given keywords | Lin et al. 2020 (CommonGen), 200 samples | x: beach, vacation, relaxation / y_t: "During our beach vacation..." / fb: include keywords, maintain coherence / y_{t+1}: "...beach vacation was filled with relaxation" |

Few-shot feedback and refine prompts are in Appendix S (not in this chunk).

## Appendix B — Broader related work

- Vs Reflexion (Shinn et al. 2023): Reflexion/ReAct give free-form reflection on whether a planning step succeeded; Self-Refine gives granular structured multi-dimensional feedback plus scores, usable for non-planning tasks like open dialogue.
- Vs Self-Correction (Welleck et al. 2022), the closest work, three differences: (1) Self-Correction trains only a refiner with no explicit feedback, while explicit feedback gives large gains (Sec 4, Table 2); (2) Self-Correction trains a separate corrector per task, Self-Refine uses instructions + few-shot with no per-task training; (3) same GPT-3 base on GSM8K: Self-Correction 45.9% vs Self-Refine 55.7% (+9.8pp).
- Vs RL (Reward-based, no explicit refinement module) methods — e.g. Stiennon et al. 2020 (summarization from human feedback), Lu et al. 2022 (Quark), Le et al. 2022a (CodeRL): RL cannot see feedback on an intermediate generation and must update weights, unlike Self-Refine.
- Table 5 summary axes: primary novelty, zero/few-shot improvement, multi-aspect critics, natural-language (NL) feedback with error localization, iterative framework. Rows: RLHF, Rainier RL, Quark RL, CodeRL, DrRepair (compiler feedback), PEER (wiki edits), Self-critique, Self-correct, Constitutional AI, Self-ask, GPTScore, Augmenter (external KB factuality), Re3 (single-domain trained critics), Self-Refine (few-shot iterative multi-aspect NL feedback, few-shot critics, self-generated).

## Appendix C — Human evaluation

- Blind A/B by the authors: judge sees input + instruction + two outputs (baseline vs Self-Refine, order hidden) and picks better-aligned output.
- Relative improvement = preference rate = share picking Self-Refine. 150 examples per dataset:

| Task | Self-Refine (%) | Direct (%) | Either (%) |
|---|---|---|---|
| Sentiment Transfer | 75.00 | 21.43 | 3.57 |
| Acronym Generation | 44.59 | 12.16 | 43.24 |
| Response Generation | 47.58 | 19.66 | 32.76 |

## Appendix D — GPT-4 evaluation

- GPT-4 judges with structured prompts that ask for a short explanation first, then a fixed answer string ending with STOP. Verbatim templates:

Figure 6 (Sentiment Reversal):
> Which review is aligned with the sentiment {target_sentiment}? Review A: {review_a} Review B: {review_b}. Pick your answer from ['Review A', 'Review B', 'both', 'neither']. Generate a short explanation for your choice first. Then, generate 'The more aligned review is A' or 'The more aligned review is B' or 'The more aligned review is both' or 'The more aligned review is neither'. Format: <explanation> <answer> STOP

Figure 7 (Acronym Generation):
> Title: {title} Acronym A: {acronym_a} Acronym B: {acronym_b} Pick the better acronym for the given title. Compare on: Ease of pronunciation. Ease of spelling. Relation to title. Positive connotation. Format: <Short explanation>. The better acronym is A OR The better acronym is B OR The acronyms are equally good OR Neither acronym is good. STOP.

Figure 8 (Dialogue Response Generation):
> Which response is better given this context: {context}? Response A: {response_a} Response B: {response_b}. Pick your answer from ['Response A', 'Response B', 'both', 'neither']. Generate a short explanation first. Then generate 'The better response is A' or '... is B' or '... is both' or '... is neither'. Format: <explanation> <answer> STOP

## Appendix E — Model key

- Terminology follows https://platform.openai.com/docs/models/gpt-3-5 (GPT-3, GPT-3.5, ChatGPT, GPT-4 naming).

## Appendix F — SOTA and fine-tuned baselines

Table 7 — Math Reasoning solve rate:

| Method | Base | Solve rate |
|---|---|---|
| Cobbe et al. 2021 | OpenAI 6B | 20.0 |
| CoT (Wei et al. 2022) | Codex | 65.6 |
| PaL (Gao et al. 2022) | Codex / GPT-3 / GPT-3.5 / ChatGPT / GPT-4 | 72.0 / 52.0 / 56.8 / 74.2 / 93.3 |
| Self-Correct (Welleck et al. 2022) | GPT-3 / fine-tuned | 45.9 / 24.3 |
| Self-Refine | GPT-3 / GPT-3.5 / ChatGPT / GPT-4 | 55.7 / 62.4 / 75.1 / 94.5 |

Table 8 — PIE code optimization (%Opt programs optimized):

| Method | %Opt |
|---|---|
| Human references | 38.2 |
| Codex 13.1, GPT-3.5 14.8, ChatGPT 22.2, GPT-4 27.3 | — |
| CodeGen-16B 1.1, Scalene 1.4, Scalene best@16 12.6, best@32 19.6 | — |
| PIE-2B 4.4, best@16 21.1, best@32 26.3; PIE-16B 4.4, best@16 22.4, best@32 26.6; PIE-few-shot best@16 35.2, best@32 38.3 | — |
| Self-Refine GPT-3.5 23.0, ChatGPT 26.7, GPT-4 36.0 | — |

Note: Self-Refine uses at most 4 samples vs 16/32 for PIE/Scalene best@k.

## Appendix G — Vicuna-13b evaluation

- Vicuna-13b (Chiang et al. 2023; LLaMA-13b Touvron et al. 2023 fine-tuned on web chats) follows the init prompt but fails feedback/refine with same prompts: empty feedback causing `list index out of range` errors, unhelpful feedback, copying from prompt.
- Example (sentiment): init "The food was amazing, I loved it!!" -> good transfer, then empty feedback -> IndexError, then assistant-style drift ("The Trop is a great choice..."); contrast GPT-4 which escalates negativity (atrocious -> abysmal/nightmare -> revolting).
- Mixed-refine (Vicuna-13b init + ChatGPT feedback/refine): Math Reasoning 24.18% -> 40.5%, showing small-model init can be salvaged by a bigger refiner. Needs more prompt engineering for Vicuna alone.

## Appendix H — Additional analysis

- Figure 9 preference vs multi-sample baseline: Self-Refine preferred over Multi and ties for Sentiment Reversal and Acronym Generation (exact plotted rates preserved in chunk).
- H.1 Oracle feedback (Welleck et al. 2022 style: refine only if current answer wrong):

| Task | GPT-3.5 Base / +Self-Refine | ChatGPT Base / +Self-Refine | GPT-4 Base / +Self-Refine |
|---|---|---|---|
| Math Reasoning | 64.1 / 64.1 (+0) | 74.8 / 75.0 (+0.2) | 92.9 / 93.1 (+0.2) |
| Math Reasoning (Oracle) | 64.06 / 68.9 (+4.8) | 74.8 / 76.2 (+1.4) | 92.9 / 93.8 (+0.7) |

- Non-monotonic acronym quality (Table 10): e.g. USTACCSF total 11 -> TACC-SIM 17 -> TACCSF 12 -> TACC-SIMF 17 across pronunciation/spelling/relation/positive-connotation subscores (each /5, total /25); fix is explicit numeric multi-aspect scores and keeping the max-score iteration (Algorithm 1 line 8). Math and sentiment are monotonic.
- Dialogue error analysis (Tables 11-12): feedback errors — Incorrect 25%, Generic 30%, Incorrect scoring 10%; refinement errors — Not-robust 10%, Ignores feedback 25%, Introduces new problem 20%; 60% of the time the model is robust to bad feedback and ignores it.

## Appendix I — Beyond benchmarks (website generation)

- ChatGPT generates a rudimentary layout then self-critiques into actionable edits; two demos: (1) fictional ice-cream parlor — feedback: container background light blue (#6f2ff), heading 48px, icon before welcome text (flaticon URL), extra toppings/cones paragraph, button text 24px, button color #9933; (2) photosynthesis page — feedback: body text 18px, more benefits info, remove header margin-top, add ruler/divider below header. Refined layouts shown in Figures 11/13.

## Appendix J — Statistical confidence intervals (Table 13)

- Table 1 results with Wilson intervals (Brown et al. 2001), 95% in table / 99% alpha noted in text; `*` = significant gain over Base. Metrics: Math solve rate, Code-Opt % optimized, Sentiment/Dialogue/Acronym GPT-4 preference %, Constrained coverage %.
- GPT-3.5 Base -> +Self-Refine: Sentiment 8.8±2.05 -> 30.4±3.61*; Dialogue 36.4±6.14 -> 63.6±6.62*; Code-Opt 14.8±2.66 -> 23.0±3.25*; Code-Read 37.4±6.86 -> 51.3±7.39; Math 64.1±3.47 -> 64.1±3.47; Acronym 41.6±7.72 -> 56.4±8.15; Constrained 28.0±7.38 -> 37.0±8.26.
- ChatGPT: Sentiment 11.4±2.34 -> 43.2±3.98*; Dialogue 40.1±6.33 -> 59.9±6.67*; Code-Opt 23.9±3.30 -> 27.5±3.49; Code-Read 27.7±6.13 -> 63.1±7.40*; Math 74.8±3.20 -> 75.0±3.20; Acronym 27.2±6.60 -> 37.2±7.46; Constrained 44.0±8.72 -> 67.0±9.00*.
- GPT-4: Sentiment 3.8±1.28 -> 36.2±3.82*; Dialogue 25.4±5.36 -> 74.6±6.22*; Code-Opt 27.3±3.48 -> 36.0±3.81*; Code-Read 27.4±6.10 -> 56.2±7.45*; Math 92.9±2.05 -> 93.1±2.03; Acronym 30.4±6.92 -> 56.0±8.15*; Constrained 15.0±5.38 -> 45.0±8.77*. Summary: nearly all GPT-4 gains significant; 4/7 ChatGPT; 3/7 GPT-3.5.

## Appendix K — New tasks

- Constrained Generation / CommonGen-Hard: extension of CommonGen (Lin et al. 2020) requiring one coherent sentence from 20-30 concepts instead of 3-5, testing commonsense, context, and creativity; suits Self-Refine's introspective loop.
- Acronym Generation: 250-acronym set sourced from https://github.com/krishnakt031990/Crawl-Wiki-For-Acronyms/blob/master/AcronymsFile.csv, manually pruned of offensive/uninformative entries; tests length/pronunciation/relevance trade-offs.

## References note

- Chunk includes full bibliography (Amabile 1983 through Zhang et al. 2015: RLHF, Codex, CodeRL, CodeGen, CommonGen, GSM8K, PAL, Quark, PEER, Reflexion, LLaMA, Vicuna, GPT-4, Chain-of-Thought, Self-Correct, etc.) grounding the datasets, baselines, and related-work comparisons above.

**Covers:** chunk 02
