# Forecasting Scientific Progress with Artificial Intelligence

**Paper:** [Forecasting Scientific Progress with Artificial Intelligence (Wu et al., 2026)](https://arxiv.org/abs/2605.22681)

## Human Readable TL;DR

Imagine asking a very well-read person to predict next year's Nobel Prize winners -- not by guessing names, but by predicting what scientific breakthrough will occur and when. This paper tests whether today's most powerful AI systems can do exactly that: predict real, verifiable scientific discoveries before they happen, using only information available at the time. The researchers built a quiz of nearly 5,000 real scientific milestones and asked AI systems to forecast them without peeking at the answers. The surprising result: even the best AI systems perform barely better than random chance at predicting whether a discovery will happen, and they're systematically overconfident about their wrong guesses. Knowing a lot about science, it turns out, does not mean you can predict where science is going.

## TL;DR

This paper introduces CUSP (Cutoff-conditioned Unseen Scientific Progress), a benchmark of 4,760 verifiable scientific milestones (2024--2026) with strict temporal knowledge cutoffs, designed to evaluate AI's ability to forecast scientific progress across four task types: binary feasibility, MCQ mechanistic reasoning, free-response solution design, and date prediction. Evaluated across six frontier LLMs, the study finds that models approach chance-level on feasibility prediction, exhibit strong response biases, are systematically overconfident, and cannot close the gap to full-information performance even with augmented pre-cutoff retrieval -- revealing a fundamental disconnect between scientific knowledge access and genuine forward-looking forecasting.

---

## Problem & Motivation

Scientific progress follows recognizable patterns (Moore's Law, deep learning scaling laws), and AI is increasingly embedded in the scientific process. Yet no evaluation framework tests whether AI can genuinely *predict* unknown future scientific milestones under strict temporal constraints. Existing benchmarks either evaluate retrospective reasoning (ground truth already known) or general-event forecasting without scientific grounding. CUSP fills this gap by enforcing hard knowledge cutoffs aligned to publication dates and requiring predictions of concrete, verifiable scientific events.

---

## Main Original Ideas

1. **CUSP Benchmark** -- A multi-disciplinary, event-level benchmark of 4,760 scientific milestones sourced from Nature/Science/Cell (natural sciences) and community leaderboards/Hugging Face (AI). Each milestone has a verified knowledge cutoff date derived from the earliest DOI appearance across Crossref, Semantic Scholar, OpenAlex, Europe PMC, arXiv, and bioRxiv/medRxiv.

2. **Four-Dimensional Task Decomposition** -- Scientific forecasting is decomposed into: (a) binary feasibility (will this claim be achieved?), (b) MCQ mechanistic reasoning (which technical approach enabled it?), (c) free-response solution design (propose a concrete solution), and (d) date prediction (forecast the month/year). This yields 17,429 structured tasks.

3. **Bias-Corrected Binary Evaluation (Merged Score)** -- A perturbed variant of each binary question replaces the real advance with a plausible-but-unrealized alternative. The "merged" score averages original and perturbed accuracy to correct for directional response bias, exposing that most models near chance-level performance is driven by systematic Yes/No bias rather than predictive signal.

4. **Knowledge Gap vs. Forecasting Gap Decomposition** -- On a 500-event subset, models are run under three conditions: base, web-search restricted to pre-cutoff info, and unrestricted web search. This cleanly separates how much performance is limited by missing knowledge (knowledge gap) vs. a deeper inability to forecast from available evidence (forecasting gap).

5. **CUSP Time Capsule** -- A prospective subset of tasks whose real-world outcomes are not yet known at evaluation time (beyond April 2026), used to study cross-model consistency and implicit world models rather than accuracy. Models converge on similar expectations for AI benchmark saturation and CO2 growth through 2027.

6. **LLM-as-Judge with Leakage Detection for FRQ** -- Free-response proposals are scored by GPT-5.4-mini augmented with agentic web search that detects post-cutoff information leakage. Non-contaminated responses are scored 0--10 across alignment, specificity, novelty, and feasibility, with human expert correlation validation.

---

## Key Findings

| Task | Best Model | Best Score | Chance/Baseline | Key Observation |
|------|-----------|-----------|----------------|-----------------|
| MCQ (mechanistic) | GPT-5.4 | **0.819** | 0.25 | Well above chance; models identify plausible approaches |
| Binary feasibility (merged) | GPT-4o | **0.519** | 0.50 | Near chance; driven by response bias |
| FRQ (solution design) | GPT-5.4 | **5.04 / 60.3% pass** | -- | High specificity but poor alignment with actual methods |
| Date prediction | LLaMA 3.3 | **0.500** | -- | Systematic late-bias; exact match <4% |

- **Feasibility prediction is universally near-chance** -- no model across any domain can reliably assess whether a scientific advance will be realized.
- **Response bias dominates binary tasks** -- LLaMA 3.3 says "Yes" 93.2% of the time; GPT-4o says "No" 81% of the time. Both reach ~0.51 merged score by different failure modes.
- **Specificity-alignment gap** -- Models write technically detailed FRQ proposals (high specificity) that do not match the actual method used (alignment gap up to +3.0 points). They sound credible but are systematically wrong.
- **Date prediction is systematically late** -- all models predict events later than they occurred; AI timeline prediction (0.461) is substantially more accurate than other domains (0.18--0.28).
- **Performance is insensitive to training cutoff** -- models do not degrade meaningfully for post-cutoff events, suggesting limitations are not primarily due to knowledge gaps.
- **Forecasting gap > knowledge gap** -- adding pre-cutoff web search helps, but a large unexplained gap to full-information hindsight remains, growing with citation count of the discovery.
- **Overconfidence is pervasive** -- Binary ECE ranges from 0.167 (DeepSeek R1) to 0.309 (LLaMA 3.3); calibration is worse in open-ended settings.

---

## Suggestions & Future Directions

1. **Improve temporal reasoning under uncertainty** -- Models need capabilities beyond knowledge retrieval: reasoning about how scientific discoveries unfold over time, not just what has been discovered.
2. **Better calibration mechanisms** -- Current models' confidence estimates are unreliable in forecasting contexts; targeted calibration training on forward-looking tasks is needed.
3. **Reduce response bias** -- Structured prompting or training interventions to address systematic Yes/No biases in feasibility assessment.
4. **Close the forecasting gap for high-impact advances** -- The gap is largest for high-citation discoveries, which are precisely the ones most valuable to predict; targeted work on reasoning about breakthrough science is warranted.
5. **Longitudinal CUSP Time Capsule evaluation** -- As Time Capsule outcomes become known, re-evaluating models will provide a true prospective benchmark for scientific forecasting.
6. **Extend to non-text scientific modalities** -- Current evaluation is text-based; incorporating experimental data, figures, and molecular structures could better capture scientific reasoning.

---

## Authors & Institutions

Sean Wu (University of Oxford), Pan Lu (Stanford University), Yupeng Chen (University of Oxford), Jonathan Bragg (Allen Institute for AI), Yutaro Yamada (Sakana AI), Peter Clark (Allen Institute for AI), David Clifton (University of Oxford), Philip Torr (University of Oxford), James Zou (Stanford University), Junchi Yu (University of Oxford)
