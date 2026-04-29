# A Comparison of Agentic AI Systems and Human Economists

**Paper:** [A Comparison of Agentic AI Systems and Human Economists (Serafin Grundl, 2026)](https://claude-code-economist.com/data/paper.pdf)

## Human Readable TL;DR

Can AI agents do empirical economics research as well as trained human economists? A researcher gave three coding agents -- Claude Code (Opus 4.6), Codex (GPT-5.4), and Codex (GPT-5.3-Codex) -- the exact same three tasks that 146 human research teams had tackled: measure how the DACA immigration program changed employment outcomes for Mexican-born immigrants in the U.S. The AI systems produced answers whose middle values looked similar to the humans', but with far fewer wild outliers. In a blind "review tournament" where AI judges ranked all the submissions side-by-side, the AI-written analyses consistently beat the human ones, with GPT-5.4 taking first place every time.

## TL;DR

The paper benchmarks three agentic AI systems (Claude Code Opus 4.6, Codex GPT-5.4, Codex GPT-5.3-Codex) against 146 human research teams from Huntington-Klein et al. (2025) on three progressively-constrained causal-inference tasks estimating the effect of DACA eligibility on full-time employment using ACS 2006-2016 data. Each AI model ran 100 independent instances per task (900 total runs). Means and medians of AI estimates track human values closely except Opus 4.6 on Task 1 (mean 0.4 pp vs. humans' 4.4-5.3 pp); AI dispersion is smaller than humans' on standard deviation and range, but sometimes comparable on IQR. A 300-group AI review tournament (using Gemini 3.1 Pro Preview, Opus 4.6, and GPT-5.4 as reviewers) produces a consistent ranking across reviewers: (1) GPT-5.4, (2) GPT-5.3-Codex, (3) Opus 4.6, (4) Human Researchers.

---

## Problem & Motivation

Empirical research findings depend heavily on the analyst who conducts the work -- a phenomenon called "researcher degrees of freedom," "non-standard errors," or "the garden of forking paths." Agentic AI systems like Codex and Claude Code can now execute large parts of empirical economics workflows end-to-end: translating a research question into a design, writing and revising code, running analyses, inspecting results, debugging, and producing a research report. This raises the possibility of scaling empirical economics massively. But a prerequisite is knowing how AI output compares to human output on the same tasks. This paper delivers that comparison by running AI systems on the same progressively-constrained many-analysts design used with 146 human teams.

---

## Main Original Ideas

1. **First head-to-head empirical comparison.** The first systematic comparison of agentic AI systems and human economists performing identical open-ended empirical tasks at scale -- 900 AI runs matched against 146 human research teams on the DACA-employment question.

2. **Distributional characterization via repeated runs.** Running 100 independent instances per model per task exposes the stochasticity of AI research output, including runs where the sign of the estimated treatment effect flips. This reframes AI analysis as a distribution of possible answers rather than a single point.

3. **AI review tournament.** A novel evaluation protocol: 300 four-way comparison groups (one human, one Opus 4.6, one GPT-5.3-Codex, one GPT-5.4 submission each) scored by three AI reviewer models. Uses an 11-item substantive review template and a detailed prompt that weights identification strategy over polish or estimate magnitude.

4. **AI as both producer and reviewer.** The paper studies AI in two distinct research roles -- the analyst generating the empirical work and the referee evaluating competing submissions -- and finds only a slight own-submission bias in reviewers.

5. **Decomposition of dispersion sources.** Prescribing the research design (Task 1 to Task 2) substantially reduces AI dispersion, but additionally providing a cleaned dataset (Task 2 to Task 3) does not further reduce it, because AI models already construct similar datasets once the design is fixed.

---

## Key Findings

### Point estimates: central tendency (percentage points)

| Source | Task 1 mean/median | Task 2 mean/median | Task 3 mean/median |
|---|---|---|---|
| Human Unweighted (N=145) | 5.3 / 3.0 | 4.4 / 3.2 | 4.5 / 5.0 |
| Human Weighted (N=138-142) | 4.4 / 2.6 | 4.6 / 3.4 | 6.2 / 5.1 |
| **GPT-5.4** (N=100) | 4.3 / 4.1 | 4.5 / 4.7 | 3.1 / 5.2 |
| **GPT-5.3-Codex** (N=100) | 3.2 / 3.2 | 4.1 / 4.5 | 5.4 / 6.0 |
| **Opus 4.6** (N=100) | **0.4 / 0.4** | 3.8 / 4.9 | 4.8 / 5.8 |

Opus 4.6 on Task 1 is the clear outlier, far below humans and the Codex models.

### Dispersion (Task 1 SD / range, percentage points)

| Source | SD | Range |
|---|---|---|
| Human Unweighted | 5.5 | 70.9 |
| GPT-5.4 | 0.6 | 3.2 |
| GPT-5.3-Codex | 0.4 | 2.3 |
| Opus 4.6 | 0.3 | 1.3 |

Human distributions have much wider tails, but AI IQRs are sometimes wider than human IQRs.

### Sign reversals across instances

- Opus 4.6: negative preferred estimates in **44 of 100** Task 1 runs
- GPT-5.4: negative in **32 of 100** Task 3 runs
- GPT-5.3-Codex: 6/100 Task 1, 13/100 Task 3

### Effect of constraining design

Prescribing the research design (Task 1 -> Task 2) reduces AI SDs: GPT-5.4 1.0 -> 0.8 pp, GPT-5.3-Codex 2.3 -> 1.3 pp, Opus 4.6 2.7 -> 1.8 pp. Providing the cleaned dataset (Task 2 -> Task 3) produces no further reduction.

### AI review tournament -- Average ranks (lower is better, pooled across tasks)

| Reviewer | GPT-5.4 | GPT-5.3-Codex | Opus 4.6 | Human |
|---|---|---|---|---|
| GPT-5.4 | **1.15** | 1.95 | 3.08 | 3.82 |
| GPT-5.3-Codex | **1.27** | 1.87 | 3.07 | 3.80 |
| Opus 4.6 | **1.14** | 2.23 | 2.86 | 3.76 |
| Gemini 3.1 Pro Preview Pass 1 | **1.24** | 2.05 | 2.77 | 3.94 |
| Gemini 3.1 Pro Preview Pass 2 | **1.27** | 2.02 | 2.83 | 3.88 |

Ranking is stable across reviewer models: **GPT-5.4 > GPT-5.3-Codex > Opus 4.6 > Humans**. Reviewers show only minimal own-submission bias (e.g., Opus 4.6 ranks both Codex variants above itself).

---

## Suggestions & Future Directions

1. **Scaling empirical economics.** Results suggest agentic AI systems can scale empirical research without sacrificing quality, enabling many more analyses than possible with human labor alone.

2. **Use multiple models and instances.** Running multiple AI models and/or multiple instances of the same model makes it easier to detect errors and to map the space of research choices that lead to different conclusions.

3. **Stay alert to AI errors.** An earlier draft (Opus 4.5) documented two instructive errors. Newer models show no such documented errors in this study, but they cannot be ruled out. Human oversight remains necessary.

4. **Stochasticity as a first-class concern.** Different instances of the same model can reach opposite-sign conclusions. Future work should report distributions over runs, not single-run point estimates.

5. **Potential reviewer bias.** Author cannot fully rule out AI reviewers being biased against human submissions. Review prompts and templates were designed to focus on substantive issues (identification, parallel trends, etc.) to mitigate this.

6. **Open replication archive.** All replication reports, log files, and code for the 900 runs are browsable at claude-code-economist.com.

---

## Authors & Institutions

Serafin Grundl (Federal Reserve Board of Governors, 1801 K St. NW, Washington DC 20006; serafin.j.grundl@frb.gov). The analysis and conclusions are those of the author and do not indicate concurrence by other members of the staff, the Board of Governors, or the Federal Reserve Banks.
