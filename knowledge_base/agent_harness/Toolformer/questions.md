---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# Toolformer — Retrieval Practice

## 1. Approach and tool set

### Q1 (core recall): What is the Toolformer sampling → filtering → finetuning loop, with exact thresholds and markers?

<details>
<summary>Answer</summary>

- Base model: GPT-J with 6.7B parameters; only a handful of human-written demonstrations per API seed in-context sampling over a large pretraining-style corpus.
- Markers: `<API> a_c(i_c) </API>` without result, `<API> a_c(i_c) -> r </API>` with result (implemented as `[`, `]`, `->`, so no vocabulary change).
- Sampling: keep positions where P(`<API>`) exceeds τ_s; keep top-k positions; sample up to m calls per position ending with `</API>`.
- Defaults: τ_s = 0.05, τ_f = 1.0, top k = 5 positions, up to m = 5 calls per position; calculator and MT use τ_s = 0.0, k = 20, m = 10, τ_f = 0.5 to compensate for heuristic pre-filtering.
- Filtering: keep a call only if L_i(−) − L_i(+) ≥ τ_f — i.e. call plus result lowers weighted cross-entropy over future tokens versus no call or call-without-result.
- Finetune on C* (same texts as C plus inserted useful calls), preserving general LM ability while teaching when/which/how to call.
- Five tools: Atlas-based factoid QA, BM25 Wikipedia search over KILT, four-operation calculator (rounded to 2 decimals), NLLB-600M translation into English (200 languages, fastText detection), input-free calendar returning current date.
- Inference: decode normally until the model emits `->`, pause, execute the API, insert response + `</API>`, continue.

</details>

### Q2 (elaboration): Why filter candidate calls by future-token loss reduction — what breaks if you keep every sampled call?

<details>
<summary>Answer</summary>

- Sampling from a few demonstrations over-generates: many candidate calls are irrelevant, wrong, or distracting.
- The loss test (L_i(−) − L_i(+) ≥ τ_f) keeps only calls whose result actually makes future tokens more predictable, i.e. genuinely informative calls.
- Without it, finetuning would teach the model to emit plausible-looking but useless API calls (wrong position, wrong tool, wrong argument), adding noise tokens that hurt both tool precision and base perplexity.
- Comparing against both no-call and call-without-result isolates the value of the *result*: a call only survives if the returned information — not just the call syntax — helps prediction.

</details>

## 2. Experiments, analysis, limits

### Q3 (core recall): What zero-shot scores and tool-use rates does the 6.7B Toolformer report on factual, math, and open-QA tasks?

<details>
<summary>Answer</summary>

- LAMA (SQuAD / Google-RE / T-REx): 33.8 / 11.5 / 53.5 — beating the best same-size baseline by +11.7 / +5.2 / +18.6 and beating OPT-66B and GPT-3-175B; QA tool called in 98.1% of cases.
- Math (ASDiv / SVAMP / MAWPS): 40.4 / 29.4 / 44.0 versus ~7–10 for GPT-J baselines and 14.0 / 10.0 / 19.8 for GPT-3; calculator used in 97.9% of cases, more than doubling its own disabled-tool score.
- Open QA with QA tool disabled (WebQS / NQ / TriviaQA), Wikipedia Search used in 99.3%: 26.3 / 17.7 / 48.8 — beats all GPT-J baselines but trails GPT-3-175B (29.0 / 22.6 / 65.9).
- Temporal: 16.3 on TempLAMA, 27.3 on Dateset (baselines ~13–14 / ~1–6); Dateset gains from calendar (54.8% use), TempLAMA gains from search/QA, calendar only 0.2%.
- LM quality preserved: perplexity on WikiText / CCNet-valid 10.3 / 10.5 for Toolformer-disabled and GPT-J+CC, versus 9.9 / 10.6 for base GPT-J.
- Scale/decoding: tool gains emerge around 775M parameters (GPT-2 124M/355M gain nothing); decoding threshold k=10 forces near-100% use (WebQS: 8.5% at k=1 vs 100% at k=10).

</details>

### Q4 (elaboration): Why does the calendar tool help Dateset (54.8% use) but sit unused on TempLAMA (0.2%) — what breaks?

<details>
<summary>Answer</summary>

- TempLAMA questions typically need a chain: find today's date *then* look up a fact relative to it — but Toolformer allows only one API call per input, so date-then-lookup chains are structurally blocked.
- The model therefore solves TempLAMA via search/QA instead of the calendar, since a single search call is more informative than a lone date.
- Dateset questions are pure calendar arithmetic (dates within four years of a given current date), so one calendar call suffices and the tool is used in 54.8% of cases.
- General lesson: single-call-per-input plus no interactive search refinement means any task requiring chained or refined calls fails even when each individual tool works.

</details>

## 3. Conclusion and training appendices

### Q5 (core recall): What are the exact training setup and Dateset construction numbers?

<details>
<summary>Answer</summary>

- Data: up to 25k examples per API; max sequence length 1,024; batch size 128.
- Hardware/schedule: DeepSpeed ZeRO-3 on 8× A100 40GB with BF16; up to 2k steps with dev-perplexity selection every 500 steps on 1,000 CCNet examples.
- Tools at data/inference time: Atlas-large for data creation, Atlas-xxl at inference for QA; Python +/-/×/÷ calculator with number-window heuristics; URL-date calendar keeping ~18% of docs; 600M NLLB MT with fastText language detection.
- Evaluation prompts (zero-shot, fixed): "Please complete the following text so that it is factually correct: x" for LAMA/TempLAMA; "x q The answer is" for math; "Answer the following question:" for QA; paragraph-grounded English-answer prompt for MLQA.
- Dateset: 9,400 calendar-reasoning queries from 500 random current dates paired with past/future dates within four years, using 7 template families plus US federal-holiday templates.

</details>

### Q6 (transfer): You add a new unit-conversion tool to a Toolformer-style pipeline. How do you apply the paper's method?

<details>
<summary>Answer</summary>

- Write a handful of demonstrations showing `<API>` conversion calls interleaved in text (e.g. "The 5-mile run [miles_to_km(5) -> 8.05] 8.05 km took...").
- Sample candidate calls over a large corpus at positions with high P(`<API>`), using the lenient calculator-style settings (τ_s = 0.0, larger k/m) if numeric pre-filtering applies.
- Filter with the loss test L_i(−) − L_i(+) ≥ τ_f (≈0.5–1.0): keep only calls whose returned conversion lowers future-token loss.
- Finetune on the augmented corpus C* (same texts plus useful calls) with the standard setup (1,024 length, batch 128, dev-perplexity selection), then at inference pause decoding at `->`, execute the converter, insert the result + `</API>`.
- Expect the known limits: single call per input (no convert-then-lookup chains), gains only at sufficient scale (~775M+), and decoding threshold k may need raising to force use on tasks where the model under-calls.

</details>

## 4. Evaluation

### Q7 (evaluation): Toolformer's abstract frames it as "the model decides for itself when, which, and how to call each tool." Where does [[critical_thinking|the critical analysis]] show this framing is narrower than it sounds?

<details>
<summary>Answer</summary>

- The decoding threshold k that controls tool-use rate is tuned per task in the appendix (k=10 forces near-100% use vs. 8.5% at k=1 on WebQS) — a knob set by the experimenter, not a purely emergent decision.
- TempLAMA shows the calendar tool used only 0.2% of the time because the task needs a chained call (date, then lookup) that the single-call-per-input architecture cannot express — the model isn't "choosing" not to use the calendar, it structurally cannot chain it with a follow-up lookup.
- On MLQA, the MT tool is used 63.8–94.9% of the time yet Toolformer still fails to consistently beat vanilla GPT-J, because CCNet finetuning side effects offset the tool's benefit in some languages — tool-use rate and tool-use *benefit* diverge.
- Net effect: "the model decides" is accurate for tasks that map onto one well-defined call (LAMA, math), but for tasks needing chaining, interactivity, or where finetuning has its own side effects, the framing overstates how much of the behavior is a learned decision versus a structural or decoding-time artifact.

</details>
