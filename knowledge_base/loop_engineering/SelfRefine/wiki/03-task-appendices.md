> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Task appendices L-R
**In one sentence:** Self-Refine improves code readability, dialogue quality, code speed, math accuracy, sentiment transfer, acronym quality, and hard constrained generation through iterated natural-language critique and refinement.
## Key points
- Code readability (App. L): on 300 CodeNet snippets with text-davinci-003 critique/editor over N=5 iterations, all three heuristic metrics rise with iteration, and at T=0.7 Self-Refine beats 60-example human rewrites (meaningful-variable ratio 0.700 vs 0.653, comments/line 0.25 vs 0.24, function units 1.33 vs 0.70).
- Dialogue response generation (App. M): few-shot init/feedback/iterate with k=3 iterations and 10-aspect scoring (relevant, informative, interesting, consistent, helpful, engaging, specific, safe, understanding, fluent) lets Self-Refine beat init by wide margins on FED (342 auto + 100 human instances), e.g. human "Self-Refine wins" 36/48/54% vs "init wins" 23/18/16% across GPT-3.5/ChatGPT/GPT-4 judges.
- Code optimization (App. N): on PIE, Self-Refine with introspective feedback reaches 15.3–15.6% optimized and 2.90–3.74x speedup versus ~9.7–10.4% and ~3.0x for direct generation or ablated no-feedback refinement, proving multi-faceted feedback is load-bearing.
- Math reasoning (App. O): writing GSM-8k solutions as Python and using correctness-gated looping, Self-Refine accuracy climbs 71.34% → 73.39% → 75.06% → 75.74% → 76.19% over iterations 0–4 by catching errors like equating cup cost to plate cost.
- Sentiment reversal (App. P): few-shot k=4 loop until target sentiment reached achieves 100% Vader positive accuracy for both baselines but 93.6% vs 92% on negative targets, and pinpointed chain-of-thought feedback is critical (preference 85%→73% sentiment, 80.09%→58.92% dramatic when ablated to "something is wrong").
- Acronym generation (App. Q): on 250 pruned Wikipedia acronyms, 5-dimension feedback (pronunciation, spelling, title relation, connotation, well-knownness with CoT reasoning) plus human eval shows e.g. "Sequence to Sequence Learning with Neural Networks" improving STSLWN (5/25) to Seq2Seq (20/25).
- Constrained generation (App. R): CommonGen-Hard scales CommonGen from 3–5 to 20–30 concepts per sentence, and Self-Refine with GPT-3.5 wins on concept coverage, commonsense, and overall quality versus direct generation (Figure 18 winning-ratio bars ~35 vs ~10 and ~32 vs ~5).
---
## L. Code readability
### L.1 Method
- Goal orthogonal to correctness: improve usability, upgradability, ease of maintenance.
- Setup mirrors Self-Refine with `init` as no-op; loop starts directly at critique:
  - `feedback`: prompt LLM with the code + instruction to give free-text readability feedback, freely choosing enhancement types.
  - `refine`: prompt code-generator LLM with code + feedback + fix instruction; output is one loop iteration.
- Recursion: from `y_0`, `c_1 = critique(y_0)`, `y_1 = editor(y_0, c_1)`; generally `c_{k+1} = critique(y_k)`, `y_{k+1} = editor(y_k, c_{k+1})`, repeated N times.
### L.2 Experiments
- Dataset: CodeNet (Puri et al. 2021, IBM Project_CodeNet) competitive-programming snippets, hard-to-read multi-line code; random 300-example subset for Self-Refine plus 60-example subset with human-annotator rewrites for comparison.
- Implementation: critique and editor both InstructGPT text-davinci-003; critique decoded at T=0.0 (greedy) and T=0.7 (sampling); editor always T=0.0; N=5 iterations (budget constraint); exact prompts in Figures 25–26.
- Metrics (heuristic, automatic):
  - Meaningful Variable Names: distinct meaningful-named variables / total distinct variables, extracted via few-shot LM.
  - Comments: average comment pieces per code line.
  - Function Units: count of modular functional units (long functions refactored into smaller units).
### Results
- Figure 14(a)(b)(c): all three metrics averaged over examples grow across iterations 0–5 for both temperatures.
- Temperature effect: T=0.7 (diverse) yields more edits for meaningful names and comments; T=0.0 (greedy) suggests more modularization refactoring.
- Figure 15 example: dense `print((int((int(eval(input()))+1)/2)))` → first indented across lines → rewritten into atomic lines with `num_input`, `num_result`.
- Table 14 (60-example subset, last iteration vs human):

| Setup | Meaningful Variable Ratio | Comment Per Line | Function Units |
|---|---|---|---|
| Human Annotator Rewrites | 0.653 | 0.24 | 0.70 |
| Self-Refine (T=0.0) | 0.628 | 0.12 | 1.41 |
| Self-Refine (T=0.7) | 0.700 | 0.25 | 1.33 |

- Conclusion: Self-Refine reaches similar or better metric performance than human rewrites.
## M. Dialogue response generation
- Task: open-domain response generation; Self-Refine adds automatic multifaceted feedback + iterative refinement.
- Figure 16 worked example (table-tennis context): initial response scored 20/30 across aspects; refined response adds hobby info and YouTube-tutorial suggestion.
### M.1 Modules
- `init`: dialogue context → draft response.
- `feedback`: 6 in-context examples; scores response on 10 aspects (Mehri and Eskenazi 2020 review):
  - Relevant, Informative, Interesting, Consistent, Helpful, Engaging, Specific, Safe, User understanding, Fluent — each with 1–3 score + reason.
- `iterate`: context + prior response + feedback → refined response matching feedback.
### M.2 Setup and experiments
- Baseline: `init` alone (direct, no feedback).
- Few-shot config: 3 in-context examples for init (instructed to be good on all 10 aspects); feedback uses same 3 contexts/responses including low-scoring variants with scores+explanations; iterate shows context-response-feedback → better response; max k=3 iterations; selection = highest feedback total score excluding initial response.
- Model: text-davinci-003 throughout.
- Data: FED dataset (Mehri and Eskenazi 2020), 18 fine-grained qualities, human-system and human-human conversations, no-reference evaluation.
- Evaluation: 342 instances auto-eval (zero-shot text-davinci-003 picks better of Self-Refine vs init on 10 qualities, win rate in Table 1); 100 random instances human-eval (annotators shown 10 aspects + both responses, choice Self-Refine/init/both).
- Table 15 human results (%):

| Outcome | GPT-3.5 judge | ChatGPT judge | GPT-4 judge |
|---|---|---|---|
| Self-Refine wins | 36.0 | 48.0 | 54.0 |
| init wins | 23.0 | 18.0 | 16.0 |
| Both equal | 41.0 | 50.0 | 30.0 |

- Finding: despite strong GPT-3.5 baseline, Self-Refine beats init by wide margin on auto and human eval; manual analysis: more engaging, interesting, elaborate.
## N. Code optimization
- Setting: PIE (Performance-Improving Code Edits, Madaan et al. 2023) — optimize functionally correct programs via algorithmic edits.
- Pipeline: PIE output → Self-Refine natural-language improvement feedback (Figure 23) → refine (Figure 24).
- Table 16/17 results:

| Setup | Iteration | % Optimized | Relative Speedup | Speedup |
|---|---|---|---|---|
| Direct | – | 9.7 | 62.29 | 3.09 |
| Self-Refine − feedback | 1 | 10.1 | 62.15 | 3.03 |
| Self-Refine − feedback | 2 | 10.4 | 61.79 | 3.01 |
| Self-Refine | 1 | 15.3 | 59.64 | 2.90 |
| Self-Refine | 2 | 15.6 | 65.60 | 3.74 |

- Ablation conclusion: introspective multi-faceted feedback beats direct and no-feedback refinement, which barely improve over direct.
## O. Math reasoning
- Data: GSM-8k (Grade School Math 8k, Cobbe et al. 2021); solutions written in Python per Gao et al. 2022.
- Example error caught: cups problem sets `cup_cost = plate_cost; result = cup_cost`; feedback annotates `# wrong! The cost of a cup is not the same as the cost of a plate` and computes `half_dozen_plate_cost = 6 * plate_cost; cup_cost = half_dozen_plate_cost - 1200`.
- Loop: generator → feedback scans for errors → refine new solution; iteration gating uses correct label per Welleck et al. 2022.
- Figure 17 solve-rate over iterations 0–4: 71.34% → 73.39% → 75.06% → 75.74% → 76.19% accuracy.
## P. Sentiment reversal
- Task: long-form style transfer — rewrite multi-sentence review to flip sentiment (positive↔negative); harder than sentence-level transfer (Li et al. 2018; Prabhumoye et al. 2018).
- Instantiation: full few-shot init/feedback/iterate; max k=4 iterations; loop until target sentiment reached.
### P.1 Details
- Evaluation: preference rate (% times variant preferred as better matching desired sentiment) + Vader off-the-shelf classifier accuracy.
- Classifier: positive target 100% for both GPT-3.5 (text-davinci-003) and Self-Refine; negative target 92% GPT-3.5 vs 93.6% Self-Refine.
- Auto-eval prompts: few-shot choice of which review is more positive / less boring; init/feedback/refine examples in Figures 36/37/38 contrasting bland vs colorful phrasing ("food was really bad" vs "I wouldn't eat it if they pay me").
- Pinpointed feedback ablation: replacing CoT pinpoint feedback (which phrases to alter) with generic "something is wrong" drops Self-Refine preference 85%→73% (sentiment) and 80.09%→58.92% (dramatic).
- Extra eval note: GPT-4 used as judge; ties credit win rate to either side.
## Q. Acronym generation
- Motivation: good acronyms trade off length, pronounceability, relevance; iterative refinement natural fit (like email writing).
- Data: 250 acronyms from Crawl-Wiki-For-Acronyms AcronymsFile.csv, manually pruned of offensive/uninformative entries; full list in code repo.
- Feedback: 5 dimensions each with CoT reasoning before score:
  - Ease of pronunciation, Ease of spelling, Relation to title, Positive connotation, Well-known (familiarity to audience).
- Eval: human judgment of final quality; Table 18 example input "Sequence to Sequence Learning with Neural Networks":

| Criteria | GPT-3 output: STSLWN | Self-Refine output: Seq2Seq |
|---|---|---|
| Ease of pronunciation | ess-tee-ess-ell-double-you-enn, very difficult | seq-two-seq, easy |
| Ease of spelling | Very difficult | Easy |
| Relation to title | No relation | Mentions sequence, somewhat related |
| Positive connotation | Meaningless | Positive, sense of ease |
| Well-known | Not well-known | Close to well-known word "sequence" |
| Total score | 5/25 | 20/25 |

## R. Constrained generation
- Contribution: CommonGen-Hard variant of CommonGen — 20–30 concepts per sentence vs original 3–5, demanding commonsense reasoning, contextual understanding, creative problem-solving; benchmark for LLM improvement and real-world NLG.
- Role of Self-Refine: initial outputs often lack quality/coherence/sensibility; framework gives multi-dimensional introspective feedback then refines, mimicking human creative process.
- Figure 18: GPT-3.5 Self-Refine vs direct generation winning-ratio comparison on Concept, Commonsense, Overall — Self-Refine bars (~35, ~10–32 scale) clearly exceed Direct (~3–10 range).
**Covers:** chunk 03
