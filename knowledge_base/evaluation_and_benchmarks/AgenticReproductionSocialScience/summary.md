# Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results

**Paper:** [Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results (Kohler, Zollikofer, Einsiedler, Hoyle, Ash, 2026)](https://elliottash.com/wp-content/uploads/2026/04/Kohler-Zollikofer-Einsiedler-Hoyle-Ash-Read-Paper-Write-Code-Agentic-Reproduction-Social-Science-Results.pdf)

## Human Readable TL;DR

Imagine you hand a very smart research assistant only a published journal article and the raw data -- but not the spreadsheets or scripts the original authors used -- and ask them to re-derive all the numbers in the paper. That's exactly what this study tests, but with AI instead of a human. The AI agents succeeded surprisingly often: the best one matched the direction of findings more than 90% of the time and landed within statistically equivalent territory for most numbers. Crucially, when things went wrong, it was usually because the paper's own text wasn't specific enough about what the authors actually did -- not because the AI was incompetent.

## TL;DR

This paper develops a four-step agentic pipeline -- extraction, reimplementation, evaluation, and error diagnosis -- to reproduce empirical social science results from paper text and raw data alone, without any original code. Evaluating four LLMs and four agent scaffolds across 48 human-verified reproducible papers, the best agent (OpenCode + GPT-5.4) achieves 91% sign agreement and places >80% of coefficients within the original 95% CI. Deterministic cell-level grading reveals that the dominant failure mode is paper underspecification, not agent error.

---

## Problem & Motivation

Prior agentic reproducibility work gave agents access to the original analysis code -- essentially asking "can the AI re-run what someone already wrote?" This paper asks the harder question: **can agents reproduce results from the published methods description alone?** This matters because scientific papers -- not code -- are the official record of research. If results cannot be reconstructed from the paper's text, the paper fails its core communicative purpose. The reproduction gap in social science is well-documented, but scale makes human re-checking infeasible.

---

## Main Original Ideas

1. **Paper-derived reproduction pipeline** -- A four-step system: (1) extract structured methods from the PDF with numerical results masked, (2) task an autonomous coding agent to reimplement from scratch, (3) compare reproduced and original outputs deterministically at the cell level, (4) diagnose discrepancies by tracing them back through the chain.

2. **Strict information isolation** -- Agents receive only the methods description, blank result templates, and raw data. They are explicitly prohibited from accessing the original code, paper PDF, or numerical results. A dual audit (regex path scan + LLM hardcoding check) verifies no leakage.

3. **Deterministic, cell-level grading** -- Unlike prior work relying on LLM-as-judge, each reproduced cell receives a letter grade (A--F) based on exact percentage deviation from the original, with sign mismatch automatically yielding an E. Aggregation proceeds cell → table → paper.

4. **Error attribution framework** -- A diagnostic agent (GPT-5.4 + Codex CLI) traces each failing cell back to one of: agent error, extractor error, original paper underspecification, or missing data. This separates what the AI got wrong from what the paper failed to specify.

5. **Scaffold × model interaction analysis** -- Benchmarks four scaffolds (Claude Code, Codex CLI, mini-SWE-Agent, OpenCode) crossed with four LLMs (GPT-5.4, GPT-5.3 Codex, Claude Opus 4.6, GLM-5), revealing that scaffold choice and token budget explain as much variance as model capability.

---

## Key Findings

| Agent | Sign Agreement | Within 95% CI | Cost/Paper |
|-------|---------------|---------------|-----------|
| **OpenCode GPT-5.4** | **91.2%** | **>80%** | **$7.54** |
| Codex CLI GPT-5.4 | 85.1% | ~70% | ~$3.62 |
| Claude Code Opus 4.6 | 85.2% | ~70% | ~$2.10 |
| Codex CLI GPT-5.3 | 84.9% | ~68% | -- |
| OpenCode GLM-5 | 80.1% | ~60% | ~$0.93 |
| SWE-Agent GLM-5 | 79.2% | ~55% | ~$1.11 |
| SWE-Agent GPT-5.4 | 78.0% | ~50% | -- |

- Best agents match >43% of coefficients exactly (within 2% deviation, grade A)
- Completion rates: 92--100% of papers, 82--97% of tables, 52--72% of individual cells
- Descriptive statistics are easier to reproduce than regression results tables
- **Primary failure mode is human underspecification** (paper vs. code mismatches), not agent error; for strongest agents, agent errors become a minor fraction of total discrepancies
- Results are stable across repeated runs: >80% of tables show grade spread ≤ 1 across three independent runs
- No evidence of pre-training leakage: performance on post-knowledge-cutoff papers is not lower than pre-cutoff papers
- OpenCode GPT-5.4 uses ~5.6M tokens/paper and takes ~35 min/paper -- roughly 2.5× the token budget of competing agents; its performance advantage is partly attributable to greater computational investment

---

## Suggestions & Future Directions

1. **Improve methods extraction quality** -- The extraction step is occasionally responsible for downstream failures; more reliable extraction of structured methods from PDFs would directly improve reproduction rates.

2. **Better paper writing standards** -- The primary bottleneck is underspecification in papers (variable coding, filter choices, estimator details). Requiring more explicit, structured method descriptions would improve both human and automated reproducibility.

3. **Code as the authoritative source** -- The authors propose a clearer division: code specifies *what* was done; the paper explains *why*. Agentic systems can then flag mismatches between the two representations as a diagnostic tool for journals.

4. **Harder variants of agentic science** -- Sequential extensions: reproduce without shared data (agents must collect/reconstruct data), infer methods from research question alone, actively refine analysis (robustness, falsification), and ultimately replicate (new data, same hypothesis).

5. **New validity criteria for agentic research** -- If agents participate in active research generation, the field needs new standards for assessing identification, robustness, and reliability of conclusions produced without direct human oversight.

---

## Authors & Institutions

Benjamin Kohler (ETH Zurich), David Zollikofer (ETH Zurich), Johanna Einsiedler (University of Basel), Alexander Hoyle (ETH Zurich), Elliott Ash (ETH Zurich)

Code: [github.com/benjamin-kohler/social_science_replicability](https://github.com/benjamin-kohler/social_science_replicability)
