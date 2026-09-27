> [[index|Wiki]] | [[summary|Summary]]

# Toolformer — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-approach-tools|Approach and tool set (intro-3)]]

**In one sentence:** Toolformer teaches a language model (in this paper, GPT-J with 6.7B parameters) to use external tools by sampling candidate API calls via in-context learning from a handful of demonstrations, keeping only calls that reduce next-token loss by at least a filtering threshold, and finetuning on the augmented texts so the model itself decides when, which, and how to call each tool.

- Toolformer targets four inherent LM weaknesses — stale knowledge/hallucination, low-resource languages, imprecise arithmetic, and no sense of time — by giving the model callable tools instead of relying on further scaling.
- Learning is self-supervised from only a handful of human-written demonstrations per API: the LM annotates a large pretraining-style corpus with candidate calls, and a loss-based filter decides which calls are actually useful.
- API calls use special markers `<API> a_c(i_c) </API>` without the result and `<API> a_c(i_c) -> r </API>` with the result (implemented as `[`, `]`, `->` so no vocabulary change is needed), seamlessly interleaved into plain text.
- Sampling keeps positions where P(`<API>`) exceeds threshold tau_s (top-k kept), then samples up to m calls per position ending with `</API>`; filtering keeps a call only if L_i(-) - L_i(+) >= tau_f, i.e. the call plus its result lowers weighted cross-entropy over future tokens versus no call or call-without-result.
- The augmented dataset C* contains exactly the same texts as C plus inserted useful calls, so finetuning on C* preserves general language modeling ability while teaching the model where and how to use tools.
- Five tools are covered: Atlas-based factoid QA, BM25 Wikipedia search over the KILT dump, four-operation calculator (rounded to 2 decimals), NLLB-600M translation into English for 200 languages with fastText language detection, and an input-free calendar returning the current date.
- After finetuning, inference decodes normally until the model emits `->`, at which point decoding pauses, the API is executed, and the response plus `</API>` is inserted before continuing.

## 2. [[wiki/02-experiments-analysis|Experiments, analysis, limits (4-7)]]

**In one sentence:** Toolformer finetuned on self-annotated API calls lets a 6.7B GPT-J decide by itself when to call tools in zero-shot tests, beating same-size baselines and often much larger OPT-66B / GPT-3-175B on factual, math and temporal tasks without hurting base language-model quality, but tool use only emerges at scale and chaining / interactive use remain unsupported.

- On LAMA (SQuAD / Google-RE / T-REx) Toolformer scores 33.8 / 11.5 / 53.5, beating the best same-size baseline by +11.7 / +5.2 / +18.6 points and beating OPT-66B and GPT-3-175B, calling the QA tool in 98.1% of cases.
- On math reasoning (ASDiv / SVAMP / MAWPS) Toolformer scores 40.4 / 29.4 / 44.0 versus ~7-10 for GPT-J baselines and 14.0 / 10.0 / 19.8 for GPT-3, using the calculator in 97.9% of cases and more than doubling even its own disabled-tool score.
- On open QA (WebQS / NQ / TriviaQA) with the QA tool disabled, Toolformer using Wikipedia Search in 99.3% of cases scores 26.3 / 17.7 / 48.8, beating all GPT-J baselines but still trailing GPT-3-175B (29.0 / 22.6 / 65.9).
- On multilingual MLQA, translating non-English questions helps in every language (MT tool used 63.8-94.9% except Hindi at 7.3%), but CCNet finetuning hurts some languages so Toolformer (e.g. Es 20.6, De 13.5) does not consistently beat vanilla GPT-J.
- On temporal tasks Toolformer scores 16.3 on TempLAMA and 27.3 on Dateset versus ~13-14 / ~1-6 for baselines; Dateset gains come from the calendar tool (54.8% use) while TempLAMA gains come from search/QA, not calendar (0.2% use), because single-call-per-input blocks date-then-lookup chains.
- Language-model quality is preserved: perplexity on WikiText / CCNet-valid is 10.3 / 10.5 for both Toolformer-disabled and GPT-J+CC, versus 9.9 / 10.6 for base GPT-J, so API-call training adds no perplexity cost when calls are disabled.
- Tool ability emerges around 775M parameters (GPT-2 124M/355M gain nothing from tools), decoding threshold k=10 forces near-100% API use and is needed on WebQS (8.5% use at k=1 vs 100% at k=10), and hard limits are no chained calls, no interactive search refinement, prompt sensitivity, sample inefficiency, and no cost-awareness.

## 3. [[wiki/03-conclusion-appendices|Conclusion and training appendices]]

**In one sentence:** Toolformer learns self-supervised tool use via perplexity-filtered API calls, letting a 6.7B GPT-J model beat much larger models zero-shot, with appendices giving exact sampling thresholds, per-tool implementations and prompts, training setup, evaluation prompts, and the Dateset construction.

- Toolformer is finetuned on large numbers of sampled API calls filtered by whether they reduce perplexity on future tokens, covering search engines, calculators, and translation systems via simple API calls.
- A 6.7B-parameter GPT-J-based Toolformer considerably improves zero-shot performance and can outperform a much larger GPT-3 model on a range of downstream tasks.
- Default API sampling/filtering uses τ_s = 0.05, τ_f = 1.0, top k = 5 positions, up to m = 5 sampled calls per position; calculator and MT use τ_s = 0.0, k = 20, m = 10, τ_f = 0.5 to compensate for heuristic pre-filtering.
- Tool implementations are Atlas-large for data creation / Atlas-xxl at inference for QA, a +/-/×// Python calculator with number-window heuristics, URL-date calendar keeping ~18% of docs, and 600M NLLB MT with fastText language detection.
- Training uses up to 25k examples per API, max length 1,024, batch size 128, DeepSpeed ZeRO-3 on 8× A100 40GB with BF16, up to 2k steps with dev-perplexity selection every 500 steps on 1,000 CCNet examples.
- Zero-shot evaluation uses fixed prompts: "Please complete the following text so that it is factually correct: x" for LAMA/TempLAMA, "x q The answer is" for math, "Answer the following question:" for QA, and a paragraph-grounded English-answer prompt for MLQA.
- Dateset contains 9,400 calendar-reasoning queries built from 500 random current dates paired with past/future dates within four years, using 7 template families plus US federal-holiday templates.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Language models fail on factuality, arithmetic, low-resource languages, and time because these exceed fixed weights.
2. A handful of demonstrations per tool lets the model sample candidate API calls across a large corpus.
3. Only calls that reduce next-token loss beyond a threshold are kept as useful training signal.
4. Finetuning on the augmented corpus teaches the model itself when, which, and how to call each tool.
5. At inference the model emits calls zero-shot, pausing decoding to execute APIs and insert results.
6. A 6.7B Toolformer thus beats same-size baselines and often 10–25× larger models without harming perplexity, though tool use emerges only at scale and chaining remains unsupported.
<!-- FIVE_MOVES_END -->
