> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments, analysis, limits (4-7)

**In one sentence:** Toolformer finetuned on self-annotated API calls lets a 6.7B GPT-J decide by itself when to call tools in zero-shot tests, beating same-size baselines and often much larger OPT-66B / GPT-3-175B on factual, math and temporal tasks without hurting base language-model quality, but tool use only emerges at scale and chaining / interactive use remain unsupported.

## Key points
- On LAMA (SQuAD / Google-RE / T-REx) Toolformer scores 33.8 / 11.5 / 53.5, beating the best same-size baseline by +11.7 / +5.2 / +18.6 points and beating OPT-66B and GPT-3-175B, calling the QA tool in 98.1% of cases.
- On math reasoning (ASDiv / SVAMP / MAWPS) Toolformer scores 40.4 / 29.4 / 44.0 versus ~7-10 for GPT-J baselines and 14.0 / 10.0 / 19.8 for GPT-3, using the calculator in 97.9% of cases and more than doubling even its own disabled-tool score.
- On open QA (WebQS / NQ / TriviaQA) with the QA tool disabled, Toolformer using Wikipedia Search in 99.3% of cases scores 26.3 / 17.7 / 48.8, beating all GPT-J baselines but still trailing GPT-3-175B (29.0 / 22.6 / 65.9).
- On multilingual MLQA, translating non-English questions helps in every language (MT tool used 63.8-94.9% except Hindi at 7.3%), but CCNet finetuning hurts some languages so Toolformer (e.g. Es 20.6, De 13.5) does not consistently beat vanilla GPT-J.
- On temporal tasks Toolformer scores 16.3 on TempLAMA and 27.3 on Dateset versus ~13-14 / ~1-6 for baselines; Dateset gains come from the calendar tool (54.8% use) while TempLAMA gains come from search/QA, not calendar (0.2% use), because single-call-per-input blocks date-then-lookup chains.
- Language-model quality is preserved: perplexity on WikiText / CCNet-valid is 10.3 / 10.5 for both Toolformer-disabled and GPT-J+CC, versus 9.9 / 10.6 for base GPT-J, so API-call training adds no perplexity cost when calls are disabled.
- Tool ability emerges around 775M parameters (GPT-2 124M/355M gain nothing from tools), decoding threshold k=10 forces near-100% API use and is needed on WebQS (8.5% use at k=1 vs 100% at k=10), and hard limits are no chained calls, no interactive search refinement, prompt sensitivity, sample inefficiency, and no cost-awareness.

---

## 4.1 Experimental setup

- Base data `C`: subset of CCNet; base model `M`: GPT-J (6.7B).
- To save compute, candidate texts are pre-filtered per tool by heuristics (e.g. calculator texts must contain at least three numbers; full heuristics in Appendix A).
- `C*` = `C` annotated with API calls per Section 2, then all examples where every API call was filtered out are dropped. Authors assume remaining distribution is close enough to preserve LM ability (validated in 4.3).
- Position weighting: `w_t = tilde{w}_t / sum_s tilde{w}_s` with `tilde{w}_t = max(0, 1 - 0.2 * t)`, so calls stay close to where the returned info helps.
- Thresholds `tau_s`, `tau_f` chosen per tool to keep enough examples; dataset sizes:

| API | tau_f=0.5 | tau_f=1.0 | tau_f=2.0 |
|---|---|---|---|
| Question Answering | 51,987 | 18,526 | 5,135 |
| Wikipedia Search | 207,241 | 60,974 | 13,944 |
| Calculator | 3,680 | 994 | 138 |
| Calendar | 61,811 | 20,587 | 3,007 |
| Machine Translation | 3,156 | 1,034 | 229 |

- Finetuning: batch 128, LR 1e-5 with linear warmup for first 10% (details Appendix B).
- Baselines: GPT-J (no finetune), GPT-J+CC (finetuned on `C` without calls), Toolformer (finetuned on `C*`), Toolformer-disabled (same weights but `<API>` probability forced to 0), plus OPT-66B and GPT-3 davinci-175B (no instruction tuning).

## 4.2 Zero-shot downstream protocol

- All tasks zero-shot with natural-language prompts, no in-context tool-use demos — harder than prior few-shot tool work.
- Greedy decoding modified: emit `<API>` whenever it is among top-k tokens (k=10 used; k=1 = plain greedy). At most one API call per input to avoid call loops. Effect studied in Section 5.

## 4.2.1 LAMA (SQuAD, Google-RE, T-REx)

- Task: complete a short factual statement (date/place). Mask-not-final examples removed for left-to-right decoding; lenient scoring: correct word within first five predicted words.
- Wikipedia Search disabled for Toolformer to avoid unfair advantage (LAMA statements come from Wikipedia).

| Model | SQuAD | Google-RE | T-REx |
|---|---|---|---|
| GPT-J | 17.8 | 4.9 | 31.9 |
| GPT-J + CC | 19.2 | 5.6 | 33.2 |
| Toolformer (disabled) | 22.1 | 6.3 | 34.9 |
| Toolformer | 33.8 | 11.5 | 53.5 |
| OPT (66B) | 21.6 | 2.9 | 30.1 |
| GPT-3 (175B) | 26.8 | 7.0 | 39.8 |

- Toolformer calls QA tool in 98.1% of cases, another tool 0.7%, no tool 1.2%.

## 4.2.2 Math (ASDiv, SVAMP, MAWPS)

- Lenient scoring: first predicted number counts, except if prediction contains an equation like `5+3=8` then number after `=` counts.

| Model | ASDiv | SVAMP | MAWPS |
|---|---|---|---|
| GPT-J | 7.5 | 5.2 | 9.9 |
| GPT-J + CC | 9.6 | 5.0 | 9.3 |
| Toolformer (disabled) | 14.8 | 6.3 | 15.0 |
| Toolformer | 40.4 | 29.4 | 44.0 |
| OPT (66B) | 6.0 | 4.9 | 7.9 |
| GPT-3 (175B) | 14.0 | 10.0 | 19.8 |

- Calculator used in 97.9% of examples. Even disabled, Toolformer beats GPT-J baselines — authors guess exposure to call results during finetuning improves raw math.

## 4.2.3 Open QA (WebQS, NQ, TriviaQA)

- Scoring: correct answer appears within first 20 predicted words. QA tool disabled (would be trivial, and QA backend was trained on NQ).

| Model | WebQS | NQ | TriviaQA |
|---|---|---|---|
| GPT-J | 18.5 | 12.8 | 43.9 |
| GPT-J + CC | 18.4 | 12.2 | 45.6 |
| Toolformer (disabled) | 18.9 | 12.6 | 46.7 |
| Toolformer | 26.3 | 17.7 | 48.8 |
| OPT (66B) | 18.6 | 11.4 | 45.7 |
| GPT-3 (175B) | 29.0 | 22.6 | 65.9 |

- Wikipedia Search used in 99.3%. Gap to GPT-3 blamed on crude search engine and no ability to reformulate queries or page through multiple hits — flagged as future work.

## 4.2.4 Multilingual QA (MLQA)

- English context paragraph, question in Arabic / German / Spanish / Hindi / Vietnamese / Simplified Chinese; model must understand both, translating the question can help. Score: answer within first 10 generated words.

| Model | Es | De | Hi | Vi | Zh | Ar |
|---|---|---|---|---|---|---|
| GPT-J | 15.2 | 16.5 | 1.3 | 8.2 | 18.2 | 8.2 |
| GPT-J + CC | 15.7 | 14.9 | 0.5 | 8.3 | 13.7 | 4.6 |
| Toolformer (disabled) | 19.8 | 11.9 | 1.2 | 10.1 | 15.0 | 3.1 |
| Toolformer | 20.6 | 13.5 | 1.4 | 10.6 | 16.8 | 3.7 |
| OPT (66B) | 0.3 | 0.1 | 1.1 | 0.2 | 0.7 | 0.1 |
| GPT-3 (175B) | 3.4 | 1.1 | 0.1 | 1.7 | 17.7 | 0.1 |
| GPT-J (All En) | 24.3 | 27.0 | 23.9 | 23.3 | 23.1 | 23.6 |
| GPT-3 (All En) | 24.7 | 27.2 | 26.1 | 24.9 | 23.6 | 24.0 |

- Calls help in all languages; MT tool rate 63.8-94.9% except Hindi 7.3%. CCNet finetuning alone degrades some languages (distribution shift vs GPT-J pretraining), so net Toolformer does not always beat GPT-J. OPT/GPT-3 collapse mostly because they answer in the question language instead of English; GPT-J saw more multilingual data incl. EuroParl. All-English control rows confirm GPT-3 is strongest when language barrier is removed.

## 4.2.5 Temporal (TempLAMA, Dateset)

- TempLAMA: Wikidata cloze facts that change over time (e.g. "Cristiano Ronaldo plays for ___"), answers per year 2010-2020. Dateset (new, Appendix D): template questions needing today's date (e.g. "What day of the week was it 30 days ago?"). Same LAMA scoring.

| Model | TempLAMA | Dateset |
|---|---|---|
| GPT-J | 13.7 | 3.9 |
| GPT-J + CC | 12.9 | 2.9 |
| Toolformer (disabled) | 12.7 | 5.9 |
| Toolformer | 16.3 | 27.3 |
| OPT (66B) | 14.5 | 1.3 |
| GPT-3 (175B) | 15.5 | 0.8 |

- TempLAMA: calendar used only 0.2%; gains come from search + QA because entities are too rare for date alone to help; ideal date-then-QA chain is banned by one-call limit and absent from training (calls sampled independently).
- Dateset: calendar used 54.8%, fully explains the jump.

## 4.3 Language modeling (perplexity)

- Eval: WikiText + 10k held-out CCNet docs not seen in training. Toolformer-with-calls perplexity not computed (would require marginalizing over all possible calls at each position — intractable).

| Model | WikiText | CCNet |
|---|---|---|
| GPT-J | 9.9 | 10.6 |
| GPT-J + CC | 10.3 | 10.5 |
| Toolformer (disabled) | 10.3 | 10.5 |

- Finetuning on CCNet slightly helps CCNet, slightly hurts WikiText (GPT-J pretraining closer to WikiText). Adding API calls costs nothing extra when disabled.

## 4.4 Scaling laws

- Repeats setup on GPT-2 124M / 355M / 775M / 1.6B plus GPT-J, using only QA + calculator + Wikipedia Search (Figure 4 in paper).
- Tool benefit emerges ~775M: smaller models score the same with or without calls; Wikipedia Search is the easiest exception.
- Both raw and tool-augmented scores grow with size, so a large with/without gap persists even at GPT-J scale.

## 5 Analysis

### Decoding threshold k

- T-REx and WebQS split by call (AC) vs no-call (NC) subsets and call rate %:

| k | T-REx All | T-REx AC | T-REx NC | T-REx % | WebQS All | WebQS AC | WebQS NC | WebQS % |
|---|---|---|---|---|---|---|---|---|
| 0 (never call) | 34.9 | - | 34.9 | 0.0 | 18.9 | - | 18.9 | 0.0 |
| 1 (greedy) | 47.8 | 53.0 | 44.3 | 40.3 | 19.3 | 17.1 | 19.9 | 8.5 |
| 3 | 52.9 | 58.0 | 29.0 | 82.8 | 26.3 | 26.5 | 6.6 | 99.3 |
| 10 | 53.5 | 54.0 | 22.5 | 98.1 | 26.3 | 26.4 | - | 100.0 |

- Higher k = more calls. At k=1 the model is somewhat calibrated (NC subset 44.3 / 19.9 beats the never-call average 34.9 / 18.9, i.e. it skips calls it does not need); calibration is lost at high k.

### Data quality vs filter score

- Table 10 examples sorted by `L_i^- - L_i^+` (perplexity gain from the call): high scores look intuitively useful (Flodden Window WikiSearch 5.49; Calendar Thursday March 9 2017 → March 10 note 2.11; Nile QA 6,853 km 2.08; Venus Calculator 735/499 → 1.47, 1.59), low scores look useless (Calculator 85/23 → 3.70 in wrong context -0.02; Calendar Saturday June 25 2011 before Disneyland story -0.41; QA "Who was last time I was with?" → "The Last Time" -1.23).
- Exceptions exist (WikiSearch "Fast train success" returns chart trivia yet scores 0.92) but residual noise is argued to be useful so the model does not blindly trust every call result.

## 6 Related work

- LM pretraining with extra text (metadata, HTML tags, Wikipedia markup, retrieval-augmented pretraining like REALM / RETRO / Atlas): extra info is always given, whereas Toolformer decides itself when to ask.
- Tool use (search engines, browsers, calculators, translators, Python): prior work needs heavy human supervision or task-specific few-shot prompts with known tools; closest is TALM which shares the self-supervised perplexity objective but only for downstream finetuning with calculator + search.
- Bootstrapping / self-training (word senses, extraction, parsing, generation, few-shot classification, retrieval, reasoning e.g. STaR): Toolformer follows the same train-on-own-filtered-predictions pattern.

## 7 Limitations

- No chained tool use (call outputs never feed another call) because per-tool calls are sampled independently — no chain examples exist in `C*`.
- No interactive use: cannot browse many search hits or refine a query, unlike browser agents.
- Sensitive to exact input wording when deciding to call, consistent with known prompt sensitivity in zero/few-shot LMs.
- Sample-inefficient for rare tools: >1M documents yield only thousands of useful calculator examples; authors suggest iterative re-application as in related bootstrapping work.
- No notion of tool cost at decision time; API latency/compute is ignored.

**Covers:** chunk 02
