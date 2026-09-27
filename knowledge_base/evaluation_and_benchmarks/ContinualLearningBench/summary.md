# Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments

**Paper:** [Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments (Asawa et al., 2026)](https://arxiv.org/abs/2606.05661)

## Human Readable TL;DR

Imagine hiring an assistant who starts fresh every single day, never remembering what they learned yesterday. Some AI systems work this way, even though they claim to "learn over time." This paper creates a tough test to find out which AI systems can actually get better at their jobs through experience -- like a database analyst learning the quirks of a database after many queries, or a game player figuring out an opponent's strategy over many matches. The surprising finding: the fanciest "memory" systems don't outperform the simple approach of just keeping a running chat history, and even the best system only captures about a quarter of its potential improvement from experience.

## TL;DR

CL-BENCH is the first expert-validated benchmark for measuring genuine continual learning in LLM-based agents across six real-world domains. It introduces a novel *gain metric* that isolates online learning from underlying model capability by comparing stateful vs. stateless performance on identical instances. Frontier evaluation reveals that naive in-context learning (full conversation history) outperforms dedicated memory systems (Mem0, ACE, ICL Notepad) in both reward and gain, and even the top system (ICL + Claude Sonnet 4.6) achieves only 25.4% normalized gain, showing that reliable online adaptation remains an open problem.

---

## Problem & Motivation

Existing benchmarks for LLM memory and continual learning measure recall fidelity, context compaction quality, or new-task accuracy -- but none directly test whether a system improves online by learning *environment-specific latent structure* across related tasks. A benchmark gap exists: there is no way to distinguish a generically strong model from one that genuinely learns from sequential experience. CL-BENCH fills this gap by constructing tasks where the latent structure (e.g., obfuscated database schema conventions, opponent strategies, transmitter channel maps) is hidden, task-specific, and not recoverable from pretraining -- so performance improves *only* when prior experience is correctly exploited.

---

## Main Original Ideas

1. **CL-BENCH framework** -- A benchmark of six expert-validated tasks spanning software engineering, signal processing, disease outbreak forecasting, database querying, strategic game-playing, and demand forecasting. Each task is a sequence of instances in a shared environment with exploitable latent structure that a stateless agent cannot recover.

2. **Gain metric** -- For each instance t, gain g_t = r_sf_t − r_sl_t, where r_sf is the stateful system's reward and r_sl is the same system run statelessly on the same instance. This isolates the contribution of accumulated state to performance, controlling for instance-level difficulty variation.

3. **Normalized gain with headroom denominator** -- g̃ = (r̄_sf − r̄_sl) / (r_max − r̄_sl). The denominator is the system's own learning headroom, preventing tasks where the stateless baseline is already near maximum from contributing negligible signal regardless of actual learning.

4. **Concept drift variants** -- Tasks include environment perturbations mid-schedule (e.g., a database migration, a new transmitter appearing) requiring agents to detect stale beliefs and re-explore, not just accumulate state.

5. **Plasticity--stability decomposition** -- Gain is partitioned into a *plasticity* term (within-variant adaptation via in-variant feedback) and a *stability* term (transfer of prior knowledge across variant boundaries without in-variant feedback), revealing that different systems fail in qualitatively different ways.

---

## Key Findings

| Rank | System | Model | Norm. Reward (%) | Norm. Gain (%) | Cost ($) |
|------|--------|-------|-----------------|----------------|---------|
| 1 | ICL | Claude Sonnet 4.6 | 22.3 ± 4.1 | **25.4 ± 3.6** | 30.4 |
| 2 | ICL | GPT-5.4 | 20.1 ± 9.1 | 20.1 ± 9.1 | 18.4 |
| 3 | Claude Code | Sonnet 4.6 | 19.0 ± 7.1 | 23.9 ± 5.7 | 38.6 |
| 4 | Mem0 | GPT-5.4 | 15.1 ± 6.4 | 20.2 ± 5.9 | 18.3 |
| 5 | ICL | Claude Opus 4.7 | 10.2 ± 4.4 | 19.5 ± 4.1 | 49.6 |
| 9 | ACE | GPT-5.4 | 4.6 ± 2.7 | 8.6 ± 2.5 | **62.8** |

- **Naive ICL dominates dedicated memory systems.** Full-context ICL with Claude Sonnet 4.6 achieves the highest normalized reward and gain of any evaluated system.
- **Dedicated memory systems often hurt.** ACE ranks 9th in gain while incurring the highest cost ($62.8/run). ICL Notepad (same Sonnet 4.6 model) ranks 10th in reward at only 3.5%.
- **Cost efficiency favors ICL.** Gemini 3 Flash + ICL offers best cost efficiency: 16.4% gain at $7.6/run. No dedicated memory system dominates ICL on the Pareto frontier.
- **Claude Code is a notable exception** -- it is the one non-ICL system on the cost-efficient frontier, achieving 23.9% gain at moderate cost, with per-task gains of 65.1% on Sales Prediction and 43.6% on Database Exploration that no ICL configuration matches on those tasks individually.
- **Learning is highly task-dependent.** Sales Prediction and Blind Spectrum Monitoring show the largest and earliest-forming stateful vs. stateless gaps. Cohort Studies shows near-zero learning for all systems, with expert-validated structure no current system extracts.
- **Memory systems show different deficit profiles.** ICL Notepad shows the most stability (knowledge retention across variant boundaries) but low plasticity; ICL and Claude Code show the most plasticity (fast in-variant adaptation). ACE and GPT-5.4 ICL show almost no stability, indicating performance gains evaporate after concept-drift switches.

---

## Suggestions & Future Directions

1. **Extend task diversity.** CL-BENCH's six domains are a starting point; community contributions of additional expert-validated tasks with hidden latent structure are explicitly solicited, with clear admission criteria defined in the paper.
2. **Longer horizons.** Current schedules are on the order of tens of instances. Benchmarking over longer deployment horizons (hundreds or thousands of instances) is a natural extension, despite higher cost and validation difficulty.
3. **Parametric/test-time training approaches.** Current evaluation focuses on context-based memory paradigms. Methods like test-time training and self-distillation are not evaluated and are a priority for future inclusion as they become practical for realistic settings.
4. **Smaller model failure modes.** CL-BENCH requires frontier capability for non-trivial performance; smaller models' failure modes are not surfaced and warrant separate investigation.
5. **Addressing stability failure.** The consistent finding that memory modules introduce stale beliefs and spurious generalizations suggests the need for explicit mechanisms for belief revision and uncertainty-aware memory curation.

---

## Authors & Institutions

Parth Asawa (UC Berkeley), Christopher M. Glaze (Snorkel AI), Gabriel Orlanski (University of Wisconsin-Madison), Ramya Ramakrishnan (Snorkel AI), Benji Xu (UC Berkeley), Asim Biswal (UC Berkeley), Vincent Sunn Chen (Snorkel AI), Frederic Sala (University of Wisconsin-Madison / Snorkel AI), Matei Zaharia (UC Berkeley), Joseph E. Gonzalez (UC Berkeley)
