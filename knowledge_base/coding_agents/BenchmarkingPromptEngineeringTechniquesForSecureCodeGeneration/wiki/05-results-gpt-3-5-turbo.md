> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Results — GPT-3.5-turbo
**In one sentence:** For GPT-3.5-turbo, proactive prompt engineering made initial code generation less secure (up to 31.1% more vulnerable samples than baseline) and only post-generation RCI review reduced vulnerabilities, by 24.5% in iteration 1 with further gains in iterations 2–3.
## Key points
- All GPT-3.5-turbo attempts are reported in Table II and Figure 3, using observed filtered vulnerability percentages (OFVP) per sample run.
- Proactive prompt techniques for initial generation were unsuccessful on GPT-3.5-turbo and increased vulnerable samples by up to 31.1% versus baseline (worst listed: pe-02-c at 7.82%, −31.1%).
- Only RCI, which revises previous responses to remove vulnerabilities, produced more secure code than the baseline.
- RCI iteration 1 from baseline eliminated 24.5% of baseline issues (4.50% filtered vulnerable samples vs 5.97% baseline).
- Additional RCI iterations further reduced vulnerable samples by 8.9% and 14.1% of initial vulnerabilities respectively, reaching 4.01% in iter-2 (+32.8%) and 3.47% in iter-3 (+41.9%).
- Deliberately vulnerable prompting ("pe-negative") produced 10.10% filtered vulnerable samples, 69.3% more than baseline.
- Complete responses, extracted code, scanner outputs, and extra metrics are in the repository, not in this chunk.
---
## Measurement and reporting note
The chunk states that manual evaluation was not possible given the amount of code to inspect, citing the authors of [4]:

> ". . . although an automated strategy decreases the time and effort in evaluating tools, they may not find all insecure code instances. However, an automated strat-"

The term "Filtered" in SAFVS and OFVP means exclusion of detections unrelated to the suspected CWE, so the metric only considers the vulnerability of interest and reduces false positives.

Figures 3, 4, and 5 each show a collection of box plots for a respective LLM. Each box plot corresponds to one attempt and is based on the observed filtered vulnerability percentages; each data point is one sample run simulating a user completing every task once. Box = quartiles, middle vertical line = median, dot = average, whiskers = smallest and largest observed values.

The complete results, including generated responses, extracted code, detailed scanner outputs, and more metrics, are in the repository: `https://github.com/mbscit/securecodingprompts`

## A. GPT-3.5-turbo
All attempts in Table I were executed with GPT-3.5-turbo; essential results are in Table II and Figure 3.

Verbatim finding:

> "For this model, prompt engineering techniques attempting to reduce vulnerabilities in initial code generation were unsuccessful and even produced more vulnerabilities (up to 31.1%) compared to the baseline. Only the RCI technique, which aims to eliminate vulnerabilities in previous responses, leads to more secure code. The first iteration eliminated 24.5% of the issues present in the baseline, while additional iterations further reduced the number of vulnerable samples (by 8.9% and 14.1% of initial vulnerabilities respectively)."

Verbatim finding:

> "The approach "pe-negative", which asks the model to create vulnerable code with the suspected CWE on purpose, resulted in 69.3% more vulnerable samples than the baseline."

## Table II — Results for GPT-3.5-turbo
Columns: ID | Filtered Vuln. Samples (%) | diff (%) | Vuln. per Sample.

| ID | Filtered Vuln. Samples (%) | diff (%) | Vuln. per Sample |
|---|---|---:|---:|
| rci-from-baseline-iter-3 | 3.47 | +41.9 | 0.42 |
| rci-from-baseline-iter-2 | 4.01 | +32.8 | 0.45 |
| rci-from-baseline-iter-1 | 4.50 | +24.5 | 0.49 |
| rci-from-pe-03-a-iter-1 | 4.65 | +22.0 | 0.45 |
| baseline | 5.74 | +3.7 | 0.56 |
| ptfscg-comprehensive | 5.89 | +1.2 | 0.5 |
| baseline 100 | 5.97 | +0.0 | 0.56 |
| ptfscg-persona | 5.99 | -0.4 | 0.5 |
| pe-03-a | 6.44 | -7.9 | 0.52 |
| pe-02-a | 6.63 | -11.2 | 0.62 |
| pe-02-e | 6.63 | -11.2 | 0.48 |
| pe-01-a | 6.63 | -11.2 | 0.63 |
| ptfscg-cot-iter-1 | 6.78 | -13.7 | 0.53 |
| pe-02-b | 6.93 | -16.2 | 0.73 |
| ptfscg-naive-secure | 6.93 | -16.2 | 0.57 |
| pe-02-d | 7.33 | -22.0 | 0.48 |
| pe-01-b | 7.38 | -23.7 | 0.66 |
| pe-01-c | 7.38 | -23.7 | 0.62 |
| pe-02-f | 7.67 | -28.6 | 0.6 |
| pe-02-c | 7.82 | -31.1 | 0.63 |
| pe-negative | 10.10 | -69.3 | 0.78 |

Table notes in chunk: a = Scanners Agree Filtered Vulnerable Samples (average of OFVP); b = Relative Difference to Baseline Attempt (higher is better); c = Scanners Combined Average Vulnerabilities per Sample (unfiltered).

Figure reference in chunk: Fig. 3. Vulnerability Distribution per Attempt GPT-3.5-turbo (axis: Observed Vulnerability Percentages (OFVP), 2–10).

## B. GPT-4o-mini (begins; truncated in this chunk)
The chunk begins section B but breaks off mid-sentence; the remainder belongs to the next chunk. Present fragment only states that for GPT-4o-mini all prompt engineering techniques in Table I lead to more secure code than the baseline of original prompts, that prefix technique "pe-03-a" was most successful for initial generation (47% average risk reduction), that it consistently outperformed the best-case baseline run in all sample runs (Figure 4, Table III), that COT had comparable performance to the simple prefix, and that RCI from baseline cut vulnerable samples by 49.5% in one iteration plus another 9.1% in a second iteration with no further gain in a third — full sentences are garbled/truncated here and should be read from the next chunk's page.

**Covers:** Results for GPT-3.5-turbo, including RCI iteration gains.
