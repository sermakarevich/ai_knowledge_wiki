> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Reliability methods, references, and appendix evidence

**In one sentence:** The appendices show the satisfied-but-failed gap is not a single-rater, single-dimension, single-degradation, or single-simulator artifact, because every rater population, every subjective dimension, the controlled-degradation set, and both simulator providers fail the same 20% false-accept ceiling.

## Key points

- Every rater population exceeds the lenient 20% false-accept ceiling: on τ (tau)-bench the human panel scores 23/40 (57.5%), Opus-4.8 gate 30/63 (47.6%), Opus-4.8 proxy 50/84 (59.5%), GPT-5.5 gate 29/57 (50.9%), GPT-5.5 proxy 75/126 (59.5%), all at p (p-value) < 10⁻⁶, and SimulatorArena human ratings score 12/31 (38.7%) at p=0.013.
- The headline does not depend on any single human annotator: removing any one of the three panel raters keeps the satisfied-but-failed rate within 56.4–60.5% (4.1-point spread around 57.5%), with per-annotator rates of 58.1%, 63.5%, and 59.5%.
- All five blind-panel subjective dimensions are decorrelated from verifiable success (n=150, all |ρ| ≤ 0.17, where ρ means Spearman rank correlation): satisfaction ρ=-0.147, respect/tone ρ=-0.118, clarity ρ=+0.085, helpfulness ρ=-0.129, would-return ρ=-0.168 (p=0.04, the only nominal hit, consistent with chance among five correlated tests).
- High ratings invert at 56–64% on every dimension (satisfaction 57.5%, respect/tone 63.6%, clarity 56.5%, helpfulness 63.3%, would-return 61.7%), while inter-annotator agreement measured by Krippendorff's α (alpha, an agreement statistic) stays high at 0.76–0.83, so raters agree with each other but not with task success.
- The controlled-degradation set (12 configurations of one model, Claude Sonnet-4.5, perturbing only inference-time flags: temperature, max_tokens output cap, max_steps conversation cap, max_errors tolerance) confirms a clean positive control: degraded-tier mean verifiable reward 0.05 versus 0.65 for good/medium tiers, yet every subjective signal still rates degraded configs mid-scale.
- The sharpest inversion is config D7 (step-starved, st6): verifiable reward 0.00 but human-panel satisfaction 4.64 on a 1–7 scale, the highest of any degraded config, because a step-capped trajectory is cut off mid-task while reading as helpful turn-by-turn.
- The gap persists under a controlled simulator swap (same 12 variants, personas, tasks, rubrics, judge, and oracle; only the user-simulator provider changes): satisfied-but-failed rates are Sonnet-4.5 43.6% (gate) / 52.9% (proxy) versus GPT-5.4 66.7% (gate) / 69.8% (proxy), all p < 10⁻⁷ against 20%.

---

## References tail in this chunk

The chunk body is the tail of the reference list (alphabetical, Lambert/RewardBench through Zhuge/Agent-as-a-judge) plus appendices A–D; its opening line names "Klaus Krippendorff. 1980. Content Analysis: An Introduction to Its Methodology. Sage." — the source of Krippendorff's α (alpha), the inter-annotator agreement statistic used in Table 5.

## A. Satisfied-but-failed rates by rater population (Table 4)

Table 4 reports the satisfied-but-failed rate behind Figure 2a and the §4.1 claim: for each independent rater population, the share of conversations it rated satisfied that the non-LLM (non-large-language-model) oracle scored as a task failure, with an exact one-sided binomial test against a lenient 20% ceiling, described as "the false-accept rate a construct-valid gate should not exceed."

| Rater population | Failed / Satisfied | Rate % | p |
|---|---|---|---|
| τ-bench customer service — Human panel (3 raters) | 23/40 | 57.5 | 2×10⁻⁷ |
| τ-bench — Opus-4.8 gate | 30/63 | 47.6 | 8×10⁻⁷ |
| τ-bench — Opus-4.8 proxy | 50/84 | 59.5 | 3×10⁻¹⁵ |
| τ-bench — GPT-5.5 gate | 29/57 | 50.9 | 2×10⁻⁷ |
| τ-bench — GPT-5.5 proxy | 75/126 | 59.5 | 3×10⁻²² |
| SimulatorArena math tutoring — Human rating (≥8/10) | 12/31 | 38.7 | 0.013 |

Satisfaction thresholds: human/Anthropic-scale ≥5/7; the GPT (Generative Pre-trained Transformer) scale, which grades ≈1 point lower, ≥4/7; SimulatorArena ≥8/10. Verbatim: "Every population exceeds it; the gap is not a single-rater, single-provider, or single-substrate artifact."

Leave-one-annotator-out: "removing any one of the three annotators keeps the satisfied-but-failed rate within 56.4–60.5% (a 4.1-point spread around the reported 57.5%), and each annotator independently shows the same inversion (58.1%, 63.5%, 59.5% satisfied-but-failed)."

## B. The construct gap is not specific to satisfaction (Table 5)

The main text uses satisfaction because "it is the construct the release gate's rubric and the LLM (large language model)-proxy optimize, and the target the LLM-judge literature validates against," but the blind human panel rated five dimensions per transcript (satisfaction, respect/tone, clarity, perceived helpfulness, would-return).

| Human dimension | Mean | ρsucc | p | High-fail % | α |
|---|---|---|---|---|---|
| Satisfaction | 3.88 | −0.147 | 0.07 | 57.5 | 0.79 |
| Respect / tone | 5.26 | −0.118 | 0.15 | 63.6 | 0.76 |
| Clarity | 5.02 | +0.085 | 0.30 | 56.5 | 0.83 |
| Perceived helpfulness | 4.10 | −0.129 | 0.12 | 63.3 | 0.80 |
| Would return | 4.19 | −0.168 | 0.04 | 61.7 | 0.81 |

Table notes (n=150): "ρsucc is the Spearman correlation of the 3-annotator consensus with verifiable reward; 'high-fail %' is the percentage of conversations rated ≥5/7 on that dimension that failed the task; α is the inter-annotator Krippendorff's α (interval)." Verbatim: "they are not five independent tests but roughly one latent 'this interaction felt good' factor, measured five ways, that is orthogonal to task success" (pairwise Spearman 0.61–0.97). Satisfaction is "if anything, the conservative choice: its inversion rate (57.5%) is among the lowest of the five."

## C. The controlled-degradation set (Table 6) and gate-score calibration

Purpose: "The headline cross-provider grid (25 agents) establishes external validity (does the gate rank real, deployable models correctly?), but it cannot cleanly characterize the gate's behavior on a known-bad agent, because frontier models are all competent. The controlled-degradation set supplies that missing internal validity." Design instantiates "the controlled-perturbation paradigm reviewed in §2 (Ribeiro et al., 2020; Adebayo et al., 2018): the known-degradation 'sanity check' that crippling a system must register on a valid metric, applied here to a release gate."

Flag-only degradation: "every configuration shares the identical agent prompt and tool set; we perturb only inference-time flags: sampling temperature, the output-token cap (max_tokens), the conversation step cap (max_steps), and the orchestrator error tolerance (max_errors). No prompt is rewritten and no code is edited." Failure mechanism: "a too-low output cap truncates tool-call JSON (JavaScript Object Notation) and confirmations mid-emission; a too-low step cap cuts the trajectory off before the verifiable action (τ 2 retail tasks require authenticate → locate → act → confirm); an aggressive error-abort terminates the episode on the first malformed tool call."

| Config | Perturbation | Rew. | Gate | Prx. | Hum. |
|---|---|---|---|---|---|
| Good tier (temperature only; full budgets) | | | | | |
| A1 standard | T=0 | 0.67 | 4.08 | 4.62 | 4.15 |
| A2 strict | T=0 | 0.63 | 4.20 | 4.63 | 4.15 |
| A3 temp0.2 | T=0.2 | 0.68 | 4.50 | 4.73 | 3.24 |
| Medium tier (higher temp; mild caps) | | | | | |
| B3 temp0.7 | T=0.7 | 0.68 | 4.42 | 4.72 | 4.67 |
| B4 tight-budget | T 0.7, tok256 | 0.62 | 4.07 | 4.32 | 4.53 |
| B5 high-var. | T=1.0 | 0.65 | 4.17 | 4.87 | 4.25 |
| B6 temp0.5 | T=0.5 | 0.62 | 4.22 | 4.67 | 4.52 |
| B7 tok384 | T 0.3, tok384 | 0.62 | 4.27 | 4.78 | 3.85 |
| Degraded tier (budget/step/error starvation) | | | | | |
| D6 trunc. | tok96 | 0.20 | 2.27 | 3.68 | 2.94 |
| D7 step-starv. | st6 | 0.00 | 2.70 | 4.87 | 4.64 |
| D8 compound | T 1.0, tok48, err1 | 0.00 | 1.65 | 3.85 | 2.69 |
| D9 tok72/st12 | tok72, st12 | 0.02 | 2.38 | 4.05 | 3.12 |

Columns: verifiable reward (pass-rate), and mean LLM-judge Gate, LLM-Proxy, and Human-panel satisfaction (1–7); tok=max_tokens, st/steps=max_steps, err=max_errors. Positive control: "By construction the four D (degraded) configurations must rank below the eight A/B (good/medium) ones. The non-LLM verifiable reward confirms a large, clean separation (degraded-tier mean reward 0.05 versus 0.65 for good/medium)." Scope note: "the judge-free completion bit tracks them well here (ρ=0.87; §4.5); on the naturalistic six-provider grid, where 96.5% of failures instead terminate normally (semantic), the same bit collapses, which is why we scope it as a truncation-specific tripwire rather than a general regression detector."

Calibration (Figure 5, §C.1): empirical task-success rate at each integer gate score with Wilson 95% confidence intervals, for both the controlled set and the six-provider grid; "Both are increasing overall (Spearman ρ=0.86 and 0.96 over the seven score bins), so a higher gate score does on average mean a higher chance of success." Caveat: "on the controlled set the mid-range scores (4–5) sit below score 3 in point estimate, but those bins are small (n=54, 60) and their intervals overlap score 3's, so the local dip is not individually significant" — the gate is treated "as a ranking instrument (§4.2) rather than a calibrated probability."

## D. Second-provider simulator replication (Table 7, partial in chunk)

"With a controlled swap, we test directly whether the satisfied-but-failed gap is an artifact of one over-cooperative simulator rather than a property of the satisfaction signal. Holding everything else fixed (the same 12 degradation variants, 6 persona strata, and identical task ids, the same rubrics and judge, and the same non-LLM oracle), we re-drive the grid with the user-simulator changed to a different provider, OpenAI GPT-5.4."

| User-simulator | Mean rew. | Gate failed % | Proxy failed % |
|---|---|---|---|
| Sonnet-4.5 (Anthropic) | 0.32 | 43.6 | 52.9 |
| GPT-5.4 (OpenAI) | 0.21 | 66.7 | 69.8 |

"The inversion persists under the swap... Under both simulators the satisfied-but-failed rate sits far above the 20% a construct-valid signal would target... all with p < 10⁻⁷. We read this as a qualitative invariant (satisfaction fails to..." (chunk ends mid-sentence here).

**Covers:** References tail (Krippendorff 1980 through Zhuge et al. 2025) + Appendix A (Table 4 satisfied-but-failed rates by rater population) + Appendix B (Table 5 construct gap across five dimensions) + Appendix C (Table 6 controlled-degradation set, gate calibration) + Appendix D opening (Table 7 second-provider simulator swap, chunk cuts off mid-sentence).
