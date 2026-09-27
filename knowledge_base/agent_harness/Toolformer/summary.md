# Toolformer: Language Models Can Teach Themselves to Use Tools

**Paper:** [Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., 2023)](https://arxiv.org/abs/2302.04761)

## Human Readable TL;DR

Imagine a very well-read student who has memorized whole libraries but still makes things up when asked for today's date, botches simple arithmetic, and can't read a letter written in a rare language. Toolformer is like giving that student a phone with five trusted contacts — a librarian who answers facts, a search engine, a pocket calculator, a translator, and a calendar — plus a habit: only call when the answer genuinely helps finish the sentence. The student practices on ordinary text with just a few examples of when to call, tries out calls everywhere, and keeps only the ones that actually make the next words easier to guess. After this practice, the student knows on their own when to pick up the phone, whom to call, and what to ask — and this modestly sized student then beats far bigger students who rely on memory alone.

## TL;DR

Toolformer is a self-supervised recipe for teaching a language model (GPT-J, 6.7B parameters) to call external APIs. From a handful of human-written demonstrations per tool, the model samples candidate calls (`<API> a_c(i_c) </API>`, implemented with `[`, `]`, `->` so no vocabulary change is needed) at positions in a CCNet corpus where P(`<API>`) exceeds a sampling threshold τ_s, executes them, and keeps only calls whose result lowers weighted cross-entropy on future tokens by at least a filtering threshold τ_f versus no call or a call without its result. Finetuning on the resulting augmented corpus C* — identical content to C plus only useful inserted calls — teaches the model to invoke five tools (Atlas-based QA, BM25 Wikipedia search, four-operation calculator, NLLB translation into English, input-free calendar) zero-shot at inference, pausing decoding at `->` to execute the call and insert the result. It beats same-size baselines and often much larger OPT-66B / GPT-3-175B on LAMA, math word problems, and temporal tasks, without raising perplexity when tools are disabled.

---

## Problem & Motivation

Large language models (LMs) show strong zero- and few-shot results at scale, yet keep basic gaps that scaling only partly fixes: no access to up-to-date information, hallucinated facts, poor understanding of low-resource languages, weak precise calculation, and no awareness of time passing. Existing tool-use approaches either demand large human annotation efforts or restrict tool use to narrow task-specific settings, which blocks widespread adoption.

Toolformer addresses this with two goals: (1) tool use learned self-supervised without large human annotations — also because what humans find useful can differ from what a model finds useful; (2) the LM keeps full generality and decides itself when, which, and how to use each tool, rather than being tied to specific tasks. Because the method is dataset-agnostic, it can run on the model's own pretraining-style data, preserving general language modeling ability.

---

## Main Original Ideas

1. **Self-supervised API-call annotation from a few demos** — Per API, a prompt with only a handful of human-written examples teaches the model to propose calls on a large plain-text corpus: candidate positions are kept where P(`<API>`) exceeds τ_s (capped at top-k), then up to m calls are sampled per position ending with `</API>`. No large labeled tool-use dataset is needed.
2. **Loss-based filtering of useful calls** — Every candidate call is executed to get a text response r, and a call is kept only if `L_i(-) - L_i(+) >= τ_f`, i.e. supplying the call plus its result as a prefix lowers weighted cross-entropy over future tokens (with decaying weights favoring nearby tokens) versus no call or the call without its result. This lets the model's own prediction gain decide what is useful.
3. **Augmented-corpus finetuning that preserves generality** — Surviving calls across all tools are interleaved into the original texts to form C*, which holds exactly the same content as C plus inserted calls, and the model is finetuned on C* with a standard LM objective. The model thus sees familiar content while learning from its own feedback where and with what inputs to use each tool.
4. **Autonomous zero-shot tool use at inference** — After finetuning, the model decodes normally until it emits `->`, signaling it expects an API response; decoding pauses, the API is executed, and the response plus `</API>` is inserted before continuing. No in-context tool demos are needed at test time, and at most one call per input is allowed to avoid loops.
5. **Five-tool coverage with text-only interfaces** — QA via Atlas (retrieval-augmented LM finetuned on Natural Questions), BM25 Wikipedia search over the KILT dump (richer snippets the model must sift itself), a four-operation calculator rounded to two decimals, NLLB-600M translation into English for 200 languages with fastText language detection, and an input-free calendar returning the current date.

---

## Key Findings

| Task | Toolformer | Same-size baselines (GPT-J / +CC / disabled) | Larger models (OPT-66B / GPT-3-175B) | Tool use rate |
|---|---|---|---|---|
| LAMA SQuAD / Google-RE / T-REx | 33.8 / 11.5 / 53.5 | 17.8–22.1 / 4.9–6.3 / 31.9–34.9 | 21.6 / 2.9 / 30.1 and 26.8 / 7.0 / 39.8 | QA 98.1% |
| Math ASDiv / SVAMP / MAWPS | 40.4 / 29.4 / 44.0 | 7.5–14.8 / 5.0–6.3 / 9.3–15.0 | 6.0 / 4.9 / 7.9 and 14.0 / 10.0 / 19.8 | Calculator 97.9% |
| Open QA WebQS / NQ / TriviaQA (search only) | 26.3 / 17.7 / 48.8 | 18.4–18.9 / 12.2–12.8 / 43.9–46.7 | 18.6 / 11.4 / 45.7 and 29.0 / 22.6 / 65.9 | WikiSearch 99.3% |
| Temporal TempLAMA / Dateset | 16.3 / 27.3 | 12.7–13.7 / 2.9–5.9 | 14.5 / 1.3 and 15.5 / 0.8 | Calendar 0.2% / 54.8% |
| Perplexity WikiText / CCNet (disabled) | 10.3 / 10.5 | base GPT-J 9.9 / 10.6; GPT-J+CC 10.3 / 10.5 | — | — |

- Multilingual MLQA: translating non-English questions helps in every language (MT used 63.8–94.9% except Hindi at 7.3%), but CCNet finetuning shifts distribution so Toolformer (e.g. Spanish 20.6, German 13.5) does not consistently beat vanilla GPT-J; OPT/GPT-3 collapse mostly by answering in the question language instead of English.
- TempLAMA gains come from search/QA, not the calendar (0.2% use), because the ideal date-then-lookup chain is banned by the one-call-per-input limit and absent from training; Dateset gains come directly from the calendar (54.8% use).
- Language-model quality is preserved: Toolformer-with-tools-disabled matches GPT-J+CC perplexity (10.3 / 10.5), so API-call training adds no cost when calls are off; finetuning on CCNet alone slightly helps CCNet and slightly hurts WikiText.
- Tool ability emerges around 775M parameters (GPT-2 124M/355M gain nothing from tools; Wikipedia Search is the easiest exception), and both raw and tool-augmented scores keep growing with size.
- Decoding threshold matters: k=10 forces near-100% API use and is needed on WebQS (8.5% use at k=1 vs 100% at k=10); at k=1 the model is somewhat calibrated (it skips calls it does not need), a calibration lost at high k.
- Data-quality check: high filter scores look intuitively useful (e.g. WikiSearch on Flodden Window, QA on Nile length, calculator divisions) while low/negative scores look useless (calculator in wrong context, stray calendar dates, unanswerable QA); residual noise is argued to keep the model from blindly trusting every result.

---

## Suggestions & Future Directions

1. **Support chained tool use** — call outputs never feed another call because per-tool calls are sampled independently, so date-then-lookup chains (needed for TempLAMA-style questions) are impossible; sample and train on multi-call chains.
2. **Enable interactive use** — the model cannot browse many search hits, reformulate queries, or page through results, which caps open-QA gains versus GPT-3; add query refinement and multi-hit browsing.
3. **Reduce prompt sensitivity** — the decision to call is sensitive to exact input wording, consistent with known zero-/few-shot fragility; study robust prompting and calibration across thresholds k.
4. **Improve sample efficiency for rare tools** — over 1M documents yield only thousands of useful calculator/MT examples even after heuristic pre-filtering; try iterative re-application of the method as in related bootstrapping work (e.g. STaR-style loops).
5. **Add tool-cost awareness** — API latency and compute are currently ignored at decision time; teach the model to weigh the benefit of a call against its cost.
6. **Scale and combine** — tool benefit persists at GPT-J scale and grows with size, so test larger models, richer tools (e.g. code execution, browsers), and combined/chained tool portfolios.

---

## Authors & Institutions

Timo Schick et al., Meta AI Research (per paper citation; author details not stated in the verified wiki pages).
