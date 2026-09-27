# Chapter 11 — literature notes: benchmark contamination, saturation, error bars

This chapter runs GSM8K + IFEval ourselves; the points below are the *reported*
numbers in the literature we cite when discussing what those scores mean.
No GSM1k / LiveCodeBench runs were performed in this chapter (spec: literature
only). All citations come from `research/SOURCES_papers.md`.

## 1. How good are public math benchmarks really? (contamination)

| Reported number | Source | What it shows |
|---|---|---|
| Up to **8-point drop** for several model families (Phi, Mistral, some Llama) on a fresh, matched-difficulty GSM8K-style set vs the original GSM8K; little/no drop for Gemini, GPT, Claude | Zhang et al. 2024, **GSM1k**, arXiv 2405.00332 | Direct evidence of benchmark-specific overfitting/contamination, correlated with memorization probability. The gap is model-family dependent, not uniform. |
| GSM8K now treated as **near-saturated/contaminated** by frontier labs | 2026 industry leaderboard set (SOURCES_papers) | Labs report HLE, FrontierMath, GPQA Diamond, SWE-bench Verified, τ²-bench instead of MMLU/GSM8K. |

Practical rule of thumb for this tutorial: a high GSM8K score only says
"the model did well on these 50–1319 school problems, which it may have
seen in training" — always ask "could this model have seen this benchmark?".

## 2. When does a benchmark stop being useful? (saturation)

| Reported number | Source | What it shows |
|---|---|---|
| ~**48%** of 60 widely used benchmarks show high/very-high saturation | 2026 systematic saturation study, arXiv 2602.16763 | Benchmarks have a "shelf life"; no agreed threshold for "saturated". |
| Older benchmarks saturate faster: **54.5%** of >60-month-old benchmarks saturated vs **42.9%** of <24-month-old ones | same | Age matters — replacement should happen on a cadence, not ad hoc. |
| SWE-bench Verified (the 2024–25 default coding metric) — OpenAI itself stated by 2026 it "no longer discriminates between frontier models" | 2026 (SOURCES_papers) | Real-time saturation: a benchmark retired by its own community inside ~2 years. |

## 3. Every number needs an error bar

| Reported number | Source | What it shows |
|---|---|---|
| Most reported score **deltas between models are within measurement noise** | Miller 2024, *Adding Error Bars to Evals*, arXiv 2411.00640 | Point estimates without CIs mislead. Use clustered SEs / bootstrap over samples. This chapter reports a bootstrap 95% CI on every score, and paired bootstrap for the prompt-sensitivity study. |
| Prompt formatting, few-shot choice, and answer-extraction regexes swing results by **double digits** | lm-evaluation-harness paper, arXiv 2405.14782 | Always report harness + version + prompt template + extractor next to the score. This chapter's sensitivity table (0-shot vs 5-shot vs CoT vs plain) reproduces exactly this effect locally. |

## 4. Why we chose these two tasks

| Benchmark | Citation | Why it fits the chapter |
|---|---|---|
| **GSM8K** — grade-school math word problems | Cobbe et al. 2021, arXiv 2110.14168 | Deterministic exact-match on an extracted final number: we can control prompt, few-shot count and extractor ourselves and see each lever move the score. Also the archetypal "contaminated benchmark" — ties into §1. |
| **IFEval** — verifiable instruction-following ("answer in exactly 3 bullet points") | Zhou et al. 2023, arXiv 2311.07911 | Scored by **deterministic checkers, not an LLM judge** — a clean contrast to chapters 5/6 where the judge is the system under test. |

## 5. What this chapter deliberately did NOT run

- **GSM1k / LiveCodeBench** — live, contamination-resistant math/code sets (arXiv 2405.00332, 2403.07974). Mentioned in §1 as the "what to use instead" answer; not executed.
- **Frontier replacements** (HLE, GPQA Diamond, ARC-AGI-2, τ²-bench) — listed as the 2026 leaderboard set in §2; out of scope for a local 27B demo.
- **SWE-bench Verified** — 500 human-reviewed instances (SOURCES_tools §5 suggests 3–5 instances for pipeline demos); that is chapter-13 territory.

## Local-reproduction caveat

The three local models in this chapter (qwen3.8:27b, gemma4, 110M tiny-qwen35)
are *not* frontier models, so their GSM8K/IFEval scores are intentionally not
comparable to the leaderboard numbers above. The value of the numbers here is
the **mechanics** — harness plumbing, CIs, prompt sensitivity — not the
absolute score level.
