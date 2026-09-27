> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conclusion and training appendices

**In one sentence:** Toolformer learns self-supervised tool use via perplexity-filtered API calls, letting a 6.7B GPT-J model beat much larger models zero-shot, with appendices giving exact sampling thresholds, per-tool implementations and prompts, training setup, evaluation prompts, and the Dateset construction.

## Key points

- Toolformer is finetuned on large numbers of sampled API calls filtered by whether they reduce perplexity on future tokens, covering search engines, calculators, and translation systems via simple API calls.
- A 6.7B-parameter GPT-J-based Toolformer considerably improves zero-shot performance and can outperform a much larger GPT-3 model on a range of downstream tasks.
- Default API sampling/filtering uses τ_s = 0.05, τ_f = 1.0, top k = 5 positions, up to m = 5 sampled calls per position; calculator and MT use τ_s = 0.0, k = 20, m = 10, τ_f = 0.5 to compensate for heuristic pre-filtering.
- Tool implementations are Atlas-large for data creation / Atlas-xxl at inference for QA, a +/-/×// Python calculator with number-window heuristics, URL-date calendar keeping ~18% of docs, and 600M NLLB MT with fastText language detection.
- Training uses up to 25k examples per API, max length 1,024, batch size 128, DeepSpeed ZeRO-3 on 8× A100 40GB with BF16, up to 2k steps with dev-perplexity selection every 500 steps on 1,000 CCNet examples.
- Zero-shot evaluation uses fixed prompts: "Please complete the following text so that it is factually correct: x" for LAMA/TempLAMA, "x q The answer is" for math, "Answer the following question:" for QA, and a paragraph-grounded English-answer prompt for MLQA.
- Dateset contains 9,400 calendar-reasoning queries built from 500 random current dates paired with past/future dates within four years, using 7 template families plus US federal-holiday templates.

---

## Conclusion

Toolformer is a language model that learns in a self-supervised way how to use different tools such as search engines, calculators, and translation systems via simple API calls.

Method recap:

- Finetune on a large number of sampled API calls.
- Filter calls based on whether they reduce perplexity on future tokens.

Claimed result:

- Considerably improves zero-shot performance of a 6.7B parameter GPT-J model.
- Enables it to even outperform a much larger GPT-3 model on a range of different downstream tasks.

## Appendix A — API details

### Sampling and filtering thresholds

Default values for sampling and filtering API calls:

- τ_s = 0.05 — only make API calls at positions where P(`<API>`) ≥ 5%.
- τ_f = 1.0 — keep API calls if they reduce loss by at least 1.0.
- Keep only top k = 5 such positions per text.
- Sample up to m = 5 API calls per identified position.

Special settings for calculator and machine translation (because heuristic pre-filtering is applied to only a small subset of C):

- τ_s = 0.0, k = 20, m = 10.
- τ_f = 0.5 (resulting sets still comparably small).

### A.1 Implementation

| Tool | Implementation |
|------|----------------|
| Question Answering | Atlas model of Izacard et al. (2022) finetuned on Natural Questions (Kwiatkowski et al., 2019); Atlas-large for creating C* to process millions of calls efficiently; larger Atlas-xxl during inference. |
| Calculator | Simple Python script supporting only `+`, `-`, `*`, `/`; no result for syntactically invalid equations. Heuristic CCNet filters: (i) ≥3 numbers in 100-token window where one is the result of an operation on two others, (ii) one of `=`, `equals`, `equal to`, `total of`, `average of` followed by a number, or (iii) ≥3 numbers — texts matching only (iii) kept at 1% random subset. |
| Calendar | Assumes calendar date = document creation date, approximated by extracting date from URL; filters out texts with no extractable date, leaving ~18% of documents. |
| Machine Translation | 600M-parameter NLLB (Costa-jussà et al., 2022) for train and inference; source auto-detected with fastText classifier (Joulin et al., 2016), target always English. Keeps only paragraphs with non-English 10-token chunks preceded and followed by English text (fastText confidence > 0.8, drop number/symbol-only chunks). Removes training cases where MT input appears after but not before the call, since lookahead is possible in data generation but not at inference. |

### A.2 Prompts for sampling API calls

Question Answering — `Your task is to add calls to a Question Answering API to a piece of text. The questions should help you get information required to complete the text. You can call the API by writing "[QA(question)]" where "question" is the question you want to ask. Here are some examples of API calls:` plus examples:

- Input: `Joe Biden was born in Scranton, Pennsylvania.` → Output: `Joe Biden was born in [QA("Where was Joe Biden born?")] Scranton, [QA("In which state is Scranton?")] Pennsylvania.`
- Input: `Coca-Cola, or Coke, is a carbonated soft drink manufactured by the Coca-Cola Company.` → Output: `Coca-Cola, or [QA("What other name is Coca-Cola known by?")] Coke, is a carbonated soft drink manufactured by [QA("Who manufactures Coca-Cola?")] the Coca-Cola Company.`
- Input: `x` → Output: (model completes)

Calculator — `Your task is to add calls to a Calculator API to a piece of text. The calls should help you get information required to complete the text. You can call the API by writing "[Calculator(expression)]" where "expression" is the expression to be computed. Here are some examples of API calls:` plus examples such as:

- `18 + 12 x 3 = [Calculator(18 + 12 * 3)] 54.`
- `[Calculator(658,893 / 11.4%)] 5,763,868`, `[Calculator(723 / 252)] 2.87`, `[Calculator(723 - 20)] 703`, `[Calculator(2011 - 1994)] 17`, `[Calculator(4 * 30)] 120`.
- Input: `x` → Output: (model completes)

Wikipedia Search — `Your task is to complete a given piece of text. You can use a Wikipedia Search API to look up information. You can do so by writing "[WikiSearch(term)]" where "term" is the search term you want to look up. Here are some examples of API calls:` plus examples:

- `... red is for [WikiSearch("Ghana flag red meaning")] the blood of martyrs ...`
- `... nanomaterials? [WikiSearch("nanomaterial production risks")] Some nanomaterials ...`
- `Metformin is the first-line drug for [WikiSearch("Metformin first-line drug")] patients ...`
- Input: `x` → Output: (model completes)

Machine Translation — `Your task is to complete a given piece of text by using a Machine Translation API. You can do so by writing "[MT(text)]" where text is the text to be translated into English. Here are some examples:` plus examples:

- `O homem suprimido [MT(O homem suprimido)] ("The Supressed Man")`
- `der klassische jüdische Mann [MT(der klassische jüdische Mann)]`
- `[MT(南京高淳县住房和城乡建设局 城市新区设计)] a plane of reference ...`
- Input: `x` → Output: (model completes)

Calendar — `Your task is to add calls to a Calendar API to a piece of text. The API calls should help you get information required to complete the text. You can call the API by writing "[Calendar()]" Here are some examples of API calls:` plus examples:

- `Today is the first [Calendar()] Friday of the year.`
- `The president of the United States is [Calendar()] Joe Biden.`
- `The current day of the week is [Calendar()] Wednesday.`
- `The number of days from now until Christmas is [Calendar()] 30.`
- `... so today [Calendar()] it is closed.`
- Input: `x` → Output: (model completes)

## Appendix B — Toolformer training

- Up to 25k examples per API.
- Max sequence length 1,024.
- Effective batch size 128.
- DeepSpeed ZeRO-3; 8× NVIDIA A100 40GB GPUs with BF16.
- Train up to 2k steps; evaluate perplexity every 500 steps on a 1,000-example CCNet dev set; pick best checkpoint.

## Appendix C — Zero-shot prompts

### C.1 LAMA and TempLAMA

Given input text x: `Please complete the following text so that it is factually correct: x.`

### C.2 Math benchmarks

Given context x and question q: `x q The answer is` (prompt is `x q The answer is .` per chunk).

### C.3 Question answering

All QA datasets including Dateset: prefix question with `Answer the following question: `; append `?` if not already present.

### C.4 Multilingual QA

Given context x and question q (MLQA): `Your task is to answer a question based on the following paragraph: x Now answer the following question in English: q.`

## Appendix D — Dateset

Construction:

- Randomly select 500 "current dates".
- For each, select another past/future date within a four-year range; fill query templates in Table 11.
- Example: "How many days ago was August 14, 2020?" with Calendar returning e.g. "Today is Sunday, November 20, 2020".
- Federal holidays in the United States (e.g., Thanksgiving) used for holiday templates.

| Template | Size |
|----------|------|
| How many days {ago was, are there until} {past_date, future_date}? | 400 |
| What {day of the week, day of the month, month, year} was it (current_date – past_date) {days, weeks, months, years} ago? | 800 |
| What {day of the week, day of the month, month, year} will it be in (future_date – current_date) days? | 800 |
| What day of the week {is, was} it on {past_date, future_date}? | 400 |
| What {day of the week, day of the month, month, year} {is, was} it {the day before yesterday, yesterday, today, tomorrow, the day after tomorrow}? | 4,000 |
| What {day of the week, day of the month} {is, was} holiday this year? | 1,800 |
| How many {days, weeks, months, years} {ago was, are there until} holiday this year? | 1,200 |
| Total | 9,400 |

**Covers:** chunk 03
