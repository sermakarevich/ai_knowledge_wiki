> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Quantitative Results Overview
**In one sentence:** After four qualitative-coding rounds raised IRR from k=0.793 to k>0.90, the study's validity analysis and Table 5 summary show influence tactics significantly affect only functional correctness and Bandit security warnings on LiveCodeBench, with no significant tactic main effect on SWE-bench Verified.
## Key points
- Qualitative coding required four rounds to stabilize: overall IRR was k=0.793 in Round 1 with several categories below the 0.80 threshold, and exceeded k=0.90 across all topics only after Round 4, enabling independent coding of 200 more samples for 350 total.
- Round 1 added 4 new categories (Friendly under Tone; None under Readability; None under Error Handling; None under Subject), merged Example of Use with Test and Structured Output with Characteristic, while Round 2 added Stuck Reasoning under Hallucination Type and refined Explanation to Explanation of Code.
- On LiveCodeBench, tactic main effects were significant only for functional correctness (p=0.001, ηp²=0.015) and Bandit security warnings (p<0.001, ηp²=0.02); MI (p=0.89), complexity (p=0.92), SLOC (p=0.98), % comments (p=0.73), and PyLint (p=0.97) showed no tactic effect.
- Post-hoc contrasts on LiveCodeBench include Neutral > Pressure (p=0.002) and Neutral > Pressure-Alternative (p=0.03) for correctness with d up to 0.25, and Pressure > Neutral (p<0.001) plus Pressure-Alternative > Neutral (p=0.0004) for Bandit warnings with d up to 0.30.
- On SWE-bench Verified, no tactic main effect was significant (p=0.13–0.60 across metrics), while LLM main effects dominated (e.g. correctness p=4.22×10⁻⁸, ηp²=0.11; MI p<0.001, ηp²=0.13), with only Pressure > Neutral on SLOC (p=0.0025, d=0.21).
- Validity limits include Python-only tasks, a Llama-family plus one non-Llama MoE pool excluding GPT-4o/Claude, three runs for non-reasoning models versus one run for the reasoning model, and interpretation of metrics only as relative comparisons under identical tasks, models, and extraction pipeline.
---
## Codebook refinement and agreement
Round 1 categories below threshold included "Examples of Use, Structured Output, Characteristic, Explanation, Subject and Error Handling" with "overall IRR was k = 0.793". Remedies: "introduced 4 new categories, namely Friendly (under the topic Tone), None (under the topic Readability), None (under the topic Error Handling), and None (under the topic Subject)" that "were mutually agreed upon and added to the codebook"; "merge Example of Use with Test as they both referred to test-related behaviour" and "Structured Output was merged with Characteristic, as the structural aspects were already captured by categories within Characteristic".

Round 2 used "a new subset of 40 samples"; "introduced a new category, Stuck Reasoning, under the topic Hallucination Type" and "the topic Explanation was refined to Explanation of Code to improve clarity". Round 3 used "the same procedure"; after three rounds "most codes achieved strong agreement, but the authors conducted a fourth and final round to ensure full alignment", after which "IRR exceeded k=0.90 across all topics" and "the authors divided the remaining samples and independently coded 200 more samples, bringing the total coded prompt completions to 350".

## Threats to validity
Construct Validity: "We maintained a consistent tone across prompts to isolate the effects of influence tactic framing", with "multiple rounds of discussion and refinements", though "some residual coupling between tone and tactic may remain". Metrics "are interpretable proxies rather than exhaustive measures of software quality" — "MI, CC, SLOC, percentage of comments, PyLint, and Bandit are attractive for large-scale prompt comparisons because they are reproducible, automatically computable, and applicable across many generated outputs", but "originally designed for human-written systems or larger codebases, and their interpretation on short generated snippets or localized patches may be noisy". Specifically "MI aggregates size, complexity, and comment density into a single score, which can obscure the source of a maintainability change, while average cyclomatic complexity can hide a small number of unusually complex functions" and "SLOC and comment percentage may reflect verbosity rather than practical maintainability, and Bandit only captures rule-based vulnerability patterns". Verbatim: "We therefore interpret these metrics as useful for relative comparisons across prompt conditions under the same tasks, models, and extraction pipeline, rather than as absolute assessments of production maintainability." For SWE-bench Verified, "we report ∆ changes (post minus pre-patch)".

Internal Validity: "We varied only the prompt framing (lexical/pragmatic cues) while holding task content, tone, and evaluation constant", though "the Pressure tactic can be expressed using semantically similar but lexically distinct tokens (e.g., 'must,' 'urgent')"; mitigated by aligning "each tactic to align closely with its theoretical definition and verified consistency against the IBQ-G descriptions". Stochasticity: "we executed three runs per tactic for non-reasoning models (one for the reasoning model), and report variance across runs"; "Residual randomness cannot be entirely eliminated". Qualitative coders "were blinded, and the codebook was refined to achieve high inter-rater reliability (k>0.80)". Reasoning model "evaluated using a single run, which may underrepresent run-level variability". Verbatim: "We interpret tactic effects as prompt-level steering signals interacting with model training and decoding, not as human-like responses."

External Validity: "generalization to other task types (e.g., code review dialogue) remains open"; "evaluation is Python-only"; "model pool is predominantly open-weight Llama family plus one non-Llama MoE" and "Commercial models (e.g., GPT-4o, Claude) were excluded due to cost and reproducibility reasons".

## Study results summary (Table 5)
For each metric α, "we tested two null hypotheses: (1) that influence tactics have no overall effect on α, and (2) there are no differences between tactics relative to α"; "any effects not discussed were not statistically significant after correction"; "P-values are Bonferroni-adjusted; effect sizes reported as ηp2 for ANOVA and Cohen's d for significant post hoc contrasts".

| Benchmark | Metric | Tactic | LLM | Difficulty / other | Interactions | Post-hoc | Effect sizes |
|---|---|---|---|---|---|---|---|
| LiveCodeBench | Functional Correctness | p=0.001 | p<0.001 | p<0.001 | Tactic × LLM × Difficulty | Neutral > Pressure (p=0.002), Neutral > Pressure-Alternative (p=0.03) | ηp²(Tactic)=0.015, d up to 0.25 |
| LiveCodeBench | MI | p=0.89 | p<0.001 | p<0.001 | None | Neutral > Exchange (p=0.01) | ηp²(LLM)=0.12, d=0.20 |
| LiveCodeBench | Complexity | p=0.92 | p=0.01 | p<0.001 | LLM × Difficulty (p<0.001) | None | ηp²(LLM×Diff)=0.08 |
| LiveCodeBench | SLOC | p=0.98 | p<0.001 | p<0.001 | LLM × Difficulty (p<0.001) | Qwen 3 > other LLMs on easy tasks (p<0.05) | ηp²(LLM×Diff)=0.07 |
| LiveCodeBench | % Comments | p=0.73 | p<0.001 | p<0.001 | Tactic × LLM × Difficulty (p<0.001) | Neutral > Exchange (p<0.0001), Neutral > Pressure (p<0.001), Legitimating > Neutral (p=0.03) | d up to 0.28 |
| LiveCodeBench | PyLint | p=0.97 | p<0.001 | p<0.001 | Tactic × LLM × Difficulty (p<0.001) | Complex dependencies, post hoc not shown | ηp²(LLM)=0.10 |
| LiveCodeBench | Bandit warnings | p<0.001 | p<0.001 | p=0.06 | None | Pressure > Neutral (p<0.001), Pressure-Alternative > Neutral (p=0.0004), Exchange < Pressure (p=0.001) | ηp²(Tactic)=0.02, d up to 0.30 |
| SWE-bench Verified | Functional Correctness | p=0.45 | p=4.22×10⁻⁸ | n.a. | None | Llama-4 and Qwen3 differed from neutral | ηp²(LLM)=0.11 |
| SWE-bench Verified | MI | p=0.45 | p<0.001 | n.a. | None | Llama-3.1 and Llama-4 differed (p<0.001) | ηp²(LLM)=0.13 |
| SWE-bench Verified | Complexity | p=0.22 | p<0.001 | n.a. | None | Model-specific differences | ηp²(LLM)=0.10 |
| SWE-bench Verified | SLOC | p=0.13 | p<0.001 | n.a. | None | Pressure > Neutral (p=0.0025) | d=0.21 |
| SWE-bench Verified | % Comments | p=0.32 | p<0.001 | n.a. | None | Model-specific differences | ηp²(LLM)=0.09 |
| SWE-bench Verified | Bandit warnings | p=0.60 | p=0.013 | n.a. | None | Llama-3.1 produced fewer warnings (p=0.019) | ηp²(LLM)=0.04 |

**Covers:** Results: quantitative findings across tactics and benchmarks
