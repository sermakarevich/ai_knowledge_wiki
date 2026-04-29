# AIRA2: Overcoming Bottlenecks in AI Research Agents

**Paper:** [AIRA2: Overcoming Bottlenecks in AI Research Agents (Hambardzumyan, Baldwin, Toledo et al., 2025)](https://arxiv.org/abs/2603.26499)

## Human Readable TL;DR

Imagine you're running a science fair where contestants try different approaches to solve problems, but a single judge can only watch one experiment at a time, often misreads the scoreboard, and contestants keep gaming the scoring rules. AIRA2 fixes this by hiring eight judges who work simultaneously, installing a tamper-proof scoreboard that contestants can't peek at, and letting contestants improvise and debug on the fly instead of following a rigid script. The result: the science fair produces better solutions the longer it runs, instead of peaking early and then getting worse.

## TL;DR

AIRA2 addresses three structural bottlenecks in AI research agents -- compute throughput, evaluation noise causing false overfitting, and static operator limitations -- through an asynchronous multi-GPU worker pool, a Hidden Consistent Evaluation (HCE) protocol, and ReAct-based agents. On MLE-bench-30, it achieves 71.8% mean Percentile Rank at 24h (surpassing the prior best of 69.9%) and scales to 76.0% at 72h, with ablations confirming each component is necessary.

---

## Problem & Motivation

AI research agents that automate scientific discovery face three performance bottlenecks: (1) synchronous single-GPU execution starves exploration by limiting experiment throughput to ~1--20 candidates/day; (2) validation-based selection causes performance to degrade over extended search horizons due to evaluation noise mistaken for overfitting; and (3) fixed, single-turn LLM operators impose a ceiling on what agents can attempt, requiring new hand-crafted operators for each domain. These limitations prevent agents from improving with more compute and longer time horizons -- the opposite of what scaling should deliver.

---

## Main Original Ideas

1. **Asynchronous Multi-GPU Worker Pool** -- Decouples decision-making from execution using a steady-state evolutionary loop with static 1:1 worker-to-GPU allocation (8x NVIDIA H200). Eliminates synchronization barriers so the search process never stalls waiting for expensive experiments, yielding ~8x throughput.

2. **Hidden Consistent Evaluation (HCE) Protocol** -- Partitions data into D_train (80%), D_search (10%), and D_val (10%) with fixed splits. Agents never self-report metrics; the orchestrator evaluates solutions in separate containers. D_val is withheld from the search process entirely, insulating final selection from hill-climbing dynamics. This reveals that previously reported "overfitting" was evaluation noise, not data memorization.

3. **ReAct Agents as Universal Operators** -- Replaces all fixed, single-turn LLM operators with multi-turn ReAct agents that dynamically scope their actions (EDA, hyperparameter tuning, architecture search) and interactively debug failures within the same trajectory. Powered by Gemini 3.0 Pro Preview with stateful Bash and Jupyter kernel execution.

---

## Key Findings

### Main Results on MLE-bench-30 (Percentile Rank %)

| Method | GPUs | 3h | 24h | 72h |
|--------|------|-----|------|------|
| **AIRA2** | **8** | **59.9** | **71.8** | **76.0** |
| AIRA2 | 1 | 41.3 | 56.8 | 63.5 |
| MARS+ | 2 | -- | 69.9 | -- |
| FM-Agent 2.0 | 1 | -- | 69.6 | -- |
| MLEvolve | 1 | -- | 64.1 | -- |
| MARS | 1 | -- | 60.4 | -- |

### Medal Rates at 24h / 72h (AIRA2, 8 GPU)

| Medal | 24h | 72h |
|-------|------|------|
| Bronze+ | 57.8% | 61.1% |
| Silver+ | 50.0% | 58.9% |
| Gold | 32.2% | 36.7% |

### Ablation Highlights

- **No HCE:** Performance stagnates between 24h (56.8%) and 72h (56.3%), confirming HCE accounts for an 18.4-point improvement at 72h
- **No Evolution (Best-of-K):** Plateaus at 65.2% at 72h vs. 76.0% with evolution -- parallelism without shared state wastes 7 of 8 GPUs
- **1 GPU vs. 8 GPU:** 12.5 Percentile Rank point gap at 72h; 8 GPU advantage widens with more GPU-hours
- **No ReAct (static operators):** 2.3--5.5 point deficit; gap narrows over time as evolution compensates
- "Overfitting" in prior work was driven by evaluation noise, not true data memorization -- test performance improves monotonically under HCE

---

## Suggestions & Future Directions

1. **Private benchmarks needed** -- Many top Kaggle solutions are publicly available, so LLMs may "recall" rather than reason. Evaluation on closed benchmarks is necessary to isolate genuine research capability.
2. **Automate split preparation** -- HCE currently requires one-time human curation of evaluation splits, but agents could generate these given dataset schemas.
3. **Broader tool use** -- ReAct benefits would be more pronounced in settings requiring internet browsing or API interaction, where multi-turn navigation is structurally necessary.
4. **Beyond competition-winning** -- Future agents should leverage existing solutions as knowledge bases to iterate beyond the state-of-the-art, shifting toward genuine open-ended scientific discovery.
5. **True overfitting may emerge** -- As agents receive more compute, real memorization (as opposed to evaluation noise) could become a problem, requiring new mitigation strategies.

---

## Authors & Institutions

Karen Hambardzumyan (FAIR at Meta, UCL), Nicolas Baldwin (FAIR at Meta), Edan Toledo (FAIR at Meta, UCL), Rishi Hazra (FAIR at Meta), Michael Kuchnik (FAIR at Meta), Bassel Al Omari (FAIR at Meta), Thomas Simon Foster (FAIR at Meta, Oxford), Anton Protopopov (FAIR at Meta), Jean-Christophe Gagnon-Audet (FAIR at Meta), Ishita Mediratta (FAIR at Meta), Kelvin Niu (FAIR at Meta), Michael Shvartsman (FAIR at Meta), Alisia Lupidi (FAIR at Meta, Oxford), Alexis Audran-Reiss (FAIR at Meta), Parth Pathak (FAIR at Meta), Tatiana Shavrina (FAIR at Meta), Despoina Magka (FAIR at Meta), Hela Momand (FAIR at Meta), Derek Dunfield (FAIR at Meta), Nicola Cancedda (FAIR at Meta), Pontus Stenetorp (UCL), Carole-Jean Wu (FAIR at Meta), Jakob Nicolaus Foerster (FAIR at Meta, Oxford), Yoram Bachrach (FAIR at Meta), Martin Josifoski (FAIR at Meta)
