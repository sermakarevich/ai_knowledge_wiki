> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Prompt Structure and Execution Setup (Fig. 2)
**In one sentence:** Prompts share a common structure (with `*` components only for SWE-bench Verified) and were executed at large scale (~123k LiveCodeBench and ~57k SWE-bench generations) with fixed decoding parameters, scripted code/diff extraction, official evaluation harnesses, and mixed-model statistical analysis.
## Key points
- Fig. 2 shows the prompt structure for testing psychological tactics, where components marked `*` were included only in SWE-bench Verified prompts.
- Total scale was ~123,435 generations for LiveCodeBench (1,055 problems × 9 tactics) and ~56,745 for SWE-bench Verified (485 problems × 9 tactics), each over 4 models × 3 runs plus 1 model × 1 run.
- All models used Temperature 0.2, Top-p 0.95, and max 8,192 generated tokens, per LiveCodeBench and SWE-bench defaults.
- LiveCodeBench code blocks were extracted with a custom script (200 responses manually validated with no errors; most recent block kept when multiple existed); SWE-bench diffs used official repository utilities.
- Correctness evaluation used official harnesses with 12 workers: LiveCodeBench on 128 GB RAM / 32-core CPU with 6 s timeout, SWE-bench Verified on 64 GB RAM / 16-core CPU with 1,800 s timeout and default patch application.
- Quantitative analysis used the first trial per condition (DeepSeek R1 Distill Llama 70B had only one run), Linear Mixed Models for continuous outcomes and GLMM (negative binomial, log-link) for binary outcomes, with ProblemID as random intercept and neutrality as baseline.
- Cross-trial variation averaged 0.059% (1.23% absolute) for LiveCodeBench versus 10.31% (26.56% absolute) for SWE-bench; 38 LiveCodeBench points lacking difficulty ratings and 2,038 / 2,833 non-Python generations were excluded.
---
## Prompt structure (Fig. 2)
**Covers:** Fig. 2 caption and method framing

> "Fig. 2: Structure of prompt used for evaluating the influence of psychological tactics in LLM code generation. Components marked with an '*' were included only in prompts for the SWE-bench verified benchmark."

> "This setup enables a controlled and fully reproducible comparison of how influence tactic prompt framings affect LLM-generated code across both structured algorithmic tasks and real-world software maintenance scenarios."

Inference scripts, prompt templates, and data processing utilities are documented in replication package [16].

## Generation scale and parameters
**Covers:** generation counts and decoding settings

- LiveCodeBench: 1,055 problems × 9 tactics × (4 models × 3 runs + 1 model × 1 run) ≈ 123,435 total generations
- SWE-bench Verified: 485 problems × 9 tactics × (4 models × 3 runs + 1 model × 1 run) ≈ 56,745 total generations
- Temperature: 0.2, Top-p: 0.95; max generated tokens: 8,192.

## Code extraction
**Covers:** extraction and validation procedure

- LiveCodeBench: custom script extracts code blocks; one author randomly sampled and validated 200 responses plus extracted files with no errors reported.
- When a response contained multiple code blocks (model optimizing or correcting itself), the script kept the most recent response.
- SWE-bench Verified: git diffs extracted using utilities from the official GitHub repository.

## Code evaluation environment
**Covers:** evaluation framework and hardware

| Setting | LiveCodeBench | SWE-bench Verified |
|---|---|---|
| Framework | Official LiveCodeBench repo harness | Official SWE-bench repo harness, default patch application |
| Machine | Linux, ~128 GB RAM, 32-core CPU | Linux, ~64 GB RAM, 16-core CPU |
| Workers | 12 | 12 |
| Timeout | 6 seconds (default) | 1,800 seconds (default) |

After correctness evaluation, generated code was analyzed for maintainability, quality, and security using Section 3.4 metrics.

## Quantitative analysis setup (Section 3.6)
**Covers:** Section 3.6 trial variation, filtering, and models

- Mean percentage difference across three repeated trials: 0.059% (LiveCodeBench) and 10.31% (SWE-bench); in absolute terms 1.23% and 26.56%.
- Inferential analysis used the first trial per condition; DeepSeek R1 Distill Llama 70B had only a single run due to computational cost, so its cross-run stability cannot be verified.
- Removed 38 LiveCodeBench points with missing/undefined difficulty ratings; excluded non-Python generations (2,038 and 2,833 data points, respectively).

Table 3 values as given:

| Benchmark | Mean Var. | Std. Dev. | Avg. % Diff. | Abs. % Change |
|---|---|---|---|---|
| LiveCodeBench | 0.00021 | 0.014 | 0.059% | 1.23% |
| SWE-Bench | 0.087 | 0.294 | 10.31% | 26.56% |

Statistical models (verbatim structure):

```text
Yijk = β0 + β1 Tactici + β2 LLMj + β3 Difficultyk
     + β4 (Tactici × LLMj) + β5 (Tactici × Difficultyk)              (1)
     + β6 (LLMj × Difficultyk) + β7 (Tactici × LLMj × Difficultyk)
     + u0p + εijk
```

where `u0p ~ N(0, σu²)` is the random intercept for ProblemID and `εijk ~ N(0, σε²)` is residual variance; for binary outcomes a GLMM from the negative binomial family with log-link (Eq. 2) uses the same fixed-effect structure plus `u0p`.

- LiveCodeBench adds difficulty as an independent variable alongside tactic and LLM; all analyses include ProblemID as random intercept with a full factorial fixed-effects structure.
- Analyses were run with neutrality as baseline and without it for robustness; fit via Restricted Maximum Likelihood (REML), with post hoc pairwise comparisons using estimated marginal means and Bonferroni correction.

## Qualitative sampling start (Section 3.7, partial in chunk)
**Covers:** Section 3.7 opening included in chunk

- Two-phase qualitative analysis for RQ3: (1) codebook development, (2) qualitative coding of randomly sampled outputs.
- Stratified sample of 1,600 completions from 47,466, restricted to LiveCodeBench (SWE-bench `patch.diff` outputs excluded as harder to interpret manually).
- Sampling guided by Correctness, Quality, Maintainability Index (MI), and Security (`bandit_low`, chosen because medium/high-severity samples were too few); 200 high + 200 low samples per metric (top/bottom 5%), 400 per metric.
