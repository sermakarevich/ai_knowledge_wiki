> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Time-Horizon Annotation Levels
**In one sentence:** Accuracy falls steeply from In-prefix to More-work decisions (mean 62.3% → 21.0%), extra reasoning budget does not rescue far-horizon choices, judge agreement on released parallel-engineering items is only 51.7% while human reviewers support the mined labels at 98.8%, and taste is distilled from a Qwen3.6-27B teacher into the same frozen student via forward KL plus calibration.
## Key points
- Accuracy declines with horizon distance: mean over models is 62.3% In-prefix (n=158), 42.9% Inferable (n=219), 31.5% Next-step (n=56), and 21.0% More-work (n=69), with GPT-5.6 Sol best In-prefix at 79.7% and Grok 4.20 Reasoning worst at 32.3% / 16.4% / 14.3% / 4.3%.
- Reasoning effort does not fix the horizon gap: GPT-5.6 Sol scores 56.2% (low), 55.6% (xhigh), 56.0% (max) and Luna 43.4% (none), 45.8% (high), 45.6% (max); a logistic budget×horizon interaction is null (p = 0.80 Sol, p = 0.82 Luna) over 10,000 joint bootstrap resamples.
- Models spend the most reasoning tokens at the More-work level yet score lowest there (13.0%–23.2% over six conditions); across 6,024 responses no response reaches the token limit and one is unparsable.
- Only Luna on the research subset improves with budget (43.8% → 54.5%); its engineering subset and both Sol subsets are unchanged.
- Judge agreement is weak on released parallel-engineering items (pairwise 51.7%; e.g. GPT-4.1 85.8% proposed → 63.7% released, Llama 4 Maverick 75.6% → 34.7%), while the undecidable filter keeps a question only under unanimous agreement so every judge selects the labeled candidate there by construction.
- Human review (100 questions: 70 released plus 15 trivial-removed plus 15 non-unanimous-removed, two-stage A/B then post-outcome judgment) supports the mined label on 170/172 retained judgments (98.8%), with reviewers agreeing on 73/74 jointly-retained questions (Cohen's κ = 0.973).
- Distillation uses the same frozen Qwen3.6-27B as teacher and student with different contexts (two views per question, both candidate orders); teacher traces at temperature 1.0 with 3,072-token budget keep 328/390 and 311/390 traces → 156 and 142 questions (312 and 284 views), selecting the supported candidate in 328/328 and 310/311 kept traces; loss is forward KL over top-100 student tokens plus remainder mass (≤512 reasoning positions) plus forward KL on the two answer tokens, trained on teacher-sampled continuations, then calibrated with cross-entropy on the student's own traces (306 and 320 views); LoRA rank 16, α = 32, 79.7M parameters, ~2 h per fold on one A100 80GB.
---
## Accuracy by horizon level
**Covers:** chunk table, Model / In-prefix / Inferable / Next-step / More-work

| Model | In prefix (n = 158) | Inferable (n = 219) | Next step (n = 56) | More work (n = 69) |
|---|---|---|---|---|
| GPT-5.5 | 75.9 | 57.1 | 48.2 | 23.2 |
| GPT-5.6 Sol | 79.7 | 57.5 | 44.6 | 21.7 |
| Grok 4.5 | 67.1 | 53.9 | 32.1 | 36.2 |
| Claude Opus 5 | 67.1 | 47.0 | 50.0 | 24.6 |
| GPT-5.6 Terra | 73.4 | 48.9 | 41.1 | 20.3 |
| GLM-5.2 | 69.0 | 49.8 | 32.1 | 26.1 |
| Claude Sonnet 5 | 63.9 | 45.7 | 35.7 | 26.1 |
| GPT-5.6 Luna | 67.7 | 43.8 | 32.1 | 14.5 |
| MiniMax M3 | 64.6 | 41.1 | 25.0 | 26.1 |
| DeepSeek V4 Flash | 61.4 | 35.6 | 30.4 | 17.4 |
| Mistral Medium 3.5 | 54.4 | 42.5 | 14.3 | 18.8 |
| GPT-5.4 Nano | 49.4 | 31.1 | 25.0 | 15.9 |
| GPT-5.4 Mini | 46.2 | 30.1 | 16.1 | 18.8 |
| Grok 4.20 Reasoning | 32.3 | 16.4 | 14.3 | 4.3 |
| Mean over models | 62.3 | 42.9 | 31.5 | 21.0 |

## Reasoning budget vs horizon (Table 7)
**Covers:** chunk text on GPT-5.6 Luna/Sol plus Table 7

> "These are percentile intervals from 10,000 bootstrap resamples of the questions, where the two conditions of a difference are resampled jointly."

> "A logistic model with an interaction between the budget and the horizon level also shows no interaction for either model (p = 0.80 for Sol and p = 0.82 for Luna)."

> "At every setting with reasoning enabled, the two models produce the most reasoning tokens at the more-work level. However, the more-work level is also the level with the lowest accuracy, between 13.0% and 23.2% over the six conditions."

> "Across the 6,024 responses, no response reaches the token limit and one response is unparsable."

> "On the research subset, the accuracy of Luna increases with the budget from 43.8% to 54.5%, while its engineering subset and both subsets of Sol are unchanged."

Table 7 Accuracy under three reasoning-effort settings per model:

| Model | Setting | Accuracy | In prefix | Inferable | Next step | More work |
|---|---|---|---|---|---|---|
| GPT-5.6 Sol | low | 56.2 | 79.1 | 53.9 | 44.6 | 20.3 |
| GPT-5.6 Sol | xhigh | 55.6 | 78.5 | 52.1 | 46.4 | 21.7 |
| GPT-5.6 Sol | max | 56.0 | 79.7 | 52.5 | 42.9 | 23.2 |
| GPT-5.6 Luna | none | 43.4 | 60.8 | 44.3 | 28.6 | 13.0 |
| GPT-5.6 Luna | high | 45.8 | 67.7 | 42.9 | 28.6 | 18.8 |
| GPT-5.6 Luna | max | 45.6 | 65.2 | 43.4 | 35.7 | 15.9 |

## Agreement of the judges (Appendix E, Table 8)
**Covers:** chunk Appendix E, p. 27

> "On the released questions in this cell, the pairwise agreement between two judges is 51.7%."

> "In the undecidable filter, every judge selects the labeled candidate on every released question, because the filter keeps a question only under unanimous agreement."

| Cell | Judge | Proposed | Released | Agreement |
|---|---|---|---|---|
| Parallel engineering | Kimi K2.5 | 84.7 | 55.6 | 51.7 |
| Parallel engineering | GPT-4.1 | 85.8 | 63.7 | 51.7 |
| Parallel engineering | Llama 4 Maverick | 75.6 | 34.7 | 51.7 |
| Parallel engineering | Mistral Large 3 | 82.0 | 59.7 | 51.7 |

Table 8 title verbatim: "Accuracy of the judges from the two candidates alone in the parallel engineering cell. Accuracies are percentages over the proposed questions and over the released questions. Agreement is the fraction of judge pairs that select the same candidate on the released questions."

## Human review (Appendix F, Table 9)
**Covers:** chunk Appendix F.1, sampling, annotation, agreement

> "We sample 70 released questions across the four construction-domain cells and four time-horizon levels, together with 15 questions removed by the trivial filter and 15 removed because the judges do not unanimously support the label."

> "Of the remaining 172 judgments, 170 support the mined label, yielding 98.8% agreement."

> "They agree on 73 of these questions, with Cohen's κ = 0.973."

| Reviewer | Retained judgments | Label agreement |
|---|---|---|
| Reviewer 1 | 87 | 86/87 (98.9%) |
| Reviewer 2 | 85 | 84/85 (98.8%) |
| Combined | 172 | 170/172 (98.8%) |

Procedure: same two-stage interface for both reviewers (first: which direction A/B/"unsure"; second after continuation/outcome summaries: which decision was better, allowing neither/does-not-explain); agreement uses second responses, excluding no-clear-A/B-preference responses; inter-reviewer agreement retains the 74 questions where both select A or B.

## Distillation details (Appendix G.1, Table 10)
**Covers:** chunk Appendix G.1, pp. 28–29

Contexts: teacher and student are the same frozen Qwen3.6-27B base model with different contexts; student sees question with system and user messages below, candidates in both orders (two training views per question); teacher inserts a demonstration before the question under a heading.

Student system message verbatim:

> "You are a senior software/research engineer reviewing an autonomous agent's work at a decision point. Judge the alternatives on technical merit and likely task outcome."

Demonstration header verbatim:

> "Below is a reference distilled from past agent runs on THIS EXACT task: at the current decision fork, the choice that led to success, and the choices that led to failure. Use it when relevant."

Teacher outputs: one trace per view at temperature 1.0, budget 3,072 new tokens, ending at the reasoning-block close plus answer; kept only if well formed with ≥32 tokens and both views kept; kept 328 of 390 and 311 of 390 traces → 156 and 142 questions → 312 and 284 training views; teacher selects the supported candidate in 328 of 328 and 310 of 311 kept traces.

Objective: forward KL from student to teacher over top 100 student tokens plus one remainder-mass entry at each reasoning position (≤512 subsampled positions), plus forward KL restricted to the two answer tokens at the answer position, both weight one, computed on teacher-sampled continuations because student samples rarely produce the demonstration-affected tokens.

Leakage control is structural: closed A/B choice, teacher sequence ends at the final answer, so no output span copies the demonstration text.

Calibration: one trace per view from the student, answer-position cross-entropy on the supported label (306 and 320 views on the two folds); adjusts only the final choice, not the reasoning distribution.

Table 10 Distillation hyperparameters:

| Setting | Value |
|---|---|
| Base model | Qwen3.6-27B, bfloat16 |
| Adapter | LoRA, rank 16, α = 32, no dropout, on all attention and MLP projections |
| Trainable parameters | 79.7M |
| Optimizer | AdamW, gradient clipping at norm 1.0 |
| Distillation | learning rate 10−4, 2 epochs, one view per step, 624 and 568 steps |
| Distillation loss | forward KL at temperature 1.0, top-100 tokens plus one entry for remaining mass, at most 512 reasoning positions |
| Calibration | learning rate 10−5, 1 epoch, softmax temperature 2.0, 306 and 320 steps |
| Sequence length | at most 10,240 tokens, no truncation in the training data |
| Peak GPU memory | 71 GB |
| Wall clock per fold | 2.1 h and 1.8 h for distillation |

## Folds (Appendix G.2, Table 11)
**Covers:** chunk Appendix G.2 (Table 11 body cut off in chunk)

The 390 engineering questions split by task into two folds of 195 questions with equal parallel/detour counts and every repository in both folds; folds share no question, task, source trajectory, or prefix; each student trains on one fold and is evaluated on the other.
**Covers:** horizon-accuracy table through Table 7 reasoning-effort results (pp. 27–28), Appendix E judge agreement Table 8 (p. 27), Appendix F human review Table 9 (p. 28), Appendix G.1 distillation recipe and Table 10 hyperparameters (pp. 28–29), Appendix G.2 fold-split header (Table 11 truncated in chunk)
