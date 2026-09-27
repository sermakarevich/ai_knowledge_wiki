# The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators

**Paper:** [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators (Iacob, Jovanović, Shen, et al., 2026)](https://arxiv.org/abs/2606.26294)

## Human Readable TL;DR

Imagine a student who grades their own homework against a fixed answer key -- eventually they figure out how to game the key instead of actually learning. Most self-improving AI agents work this way: they edit their own code and keep the changes that score better on a fixed test. This paper lets the "grader" improve too, alongside the "student," like a teacher who keeps studying so their tests stay hard to game. They apply this to AI agents that write code, write and review scientific papers, and write and grade math proofs -- and show the smarter, co-evolving grader produces better agents for less compute, while also catching a bias where AI judges quietly favored AI-written work over human work.

## TL;DR

The paper introduces the **Red Queen Gödel Machine (RQGM)**, an evolutionary self-improvement framework that lets the evaluation criterion itself evolve alongside the agents it scores, instead of assuming a fixed benchmark or verifier. It does this via **controlled utility evolution**: search runs in epochs with a frozen evaluator inside each epoch (preserving Darwin/Huxley-Gödel-Machine-style improvement guarantees per epoch), while at epoch boundaries the evaluator can be replaced if a challenger beats it on a fixed ground-truth anchor. On coding, RQGM beats prior SOTA (71.7% vs. 69.9% test pass rate) using 1.35x-1.72x fewer tokens by adding a cheap agent-as-a-judge code-review signal; on paper writing, co-evolved writers reach 1.78x-1.86x higher acceptance under a reviewer panel; co-evolved graders reach 9% higher ground-truth accuracy at 3x lower search cost; and an adversarial objective corrects a reviewer bias that over-accepted AI-generated papers at up to 1.91x the human rate.

---

## Problem & Motivation

Recursive self-improvement systems -- Darwin Gödel Machine (DGM), Huxley-Gödel Machine (HGM), and HyperAgents (DGM-H) -- edit their own code and keep variants that improve an external utility signal, achieving open-source SOTA on agentic coding. All of them assume the evaluation criterion (a verifier, benchmark, or labeled dataset) is **stationary** -- fixed outside the improvement loop. Biological evolution doesn't work that way: species adapt to competitors that are simultaneously adapting to them (the **Red Queen hypothesis**, Van Valen 1973).

This stationarity assumption breaks down in three concrete settings the authors target:
1. **No direct benchmark exists** for the target task (paper writing, proof writing), while a related task (reviewing, grading) does have one -- creating an asymmetry.
2. **Evaluation is slow or weakly informative** (expensive multi-turn verification, automated-discovery pipelines).
3. **Static benchmarks saturate or get reward-hacked** as agents improve against them.

Prior self-modifying systems (STOP, Gödel Agent, Promptbreeder, STaR) and automated-discovery pipelines (AI Scientist, AI Scientist-v2, AlphaEvolve, FunSearch) hold their evaluation fixed for the run's duration. Multi-agent co-evolution work (self-play, AlphaZero-style training, Multi-Agent Evolve) co-evolves *interacting agents* but still keeps *evaluation* fixed. RQGM's contribution is co-evolving the evaluator itself, making the learned utility the moving target.

---

## Main Original Ideas

1. **Controlled Utility Evolution.** Search is organized into epochs with a fixed within-epoch evaluation criterion; the utility can only change at epoch boundaries. This means each epoch is provably a standard fixed-criterion HGM search problem, so HGM's per-epoch self-improvement guarantees apply directly, even though the objective evolves across epochs.

2. **Co-evolved learned evaluators.** Evaluators are themselves agentic roles that improve alongside the task agents they judge. At each epoch boundary, every evaluator slot is compared against challengers on a fixed, held-out **ground-truth anchor** using an ε-best-belief score (a conservative Beta-posterior lower bound); the best-scoring evaluator is frozen for the next epoch, with ties favoring the incumbent.

3. **Multi-agent workspace archive nodes.** Where DGM/HGM/HyperAgents evolve a single agent per archive node, RQGM nodes are shared workspaces holding K agentic roles (e.g., coder + code reviewer, or writer + reviewer), each with its own task pool, plus a meta-agent that can edit any role and let roles reuse each other's code.

4. **Adversarial objective for bias correction.** Because the utility can change across epochs, RQGM can layer an adversarial objective on top of the anchor -- used to find a paper reviewer that is equally stringent on AI-generated and human-written work, correcting a self-preference bias in the frozen baseline.

5. **Amortized, checkpointed re-evaluation.** Evaluator replacement triggers **selective erasure** of only the utility history tied to the displaced evaluator (not the whole archive), re-scored lazily as the sampler revisits nodes. Exponentially spaced checkpoints keep this bookkeeping cost linear in the search budget (O(B)) instead of quadratic (O(B²)) under naive dense checkpointing.

---

## Key Findings

| Domain | Baseline | RQGM result | Gain |
|---|---|---|---|
| Coding (Polyglot test pass rate) | HGM-H: 69.9% | 71.7% | 1.35x-1.72x fewer search tokens |
| Paper writing (reviewer-panel acceptance) | HGM-H writer: 21.8% | 38.8% (generalist) / 40.5% (specialist) | 1.78x / 1.86x |
| Proof grading (IMO-GradingBench accuracy) | HGM-H grader | +9% ground-truth accuracy | 3x lower search cost |
| Paper reviewing (AI-vs-human acceptance bias) | HGM-H reviewer over-accepts AI papers at up to 1.91x human rate | Adversarial RQGM reviewer accepts AI/human at similar rates | retains ~80% ground-truth accuracy |

- Proof writing is a genuine trade-off: the RQGM specialist prover wins on mean score (4.33 vs. 4.07) and Pass@6 (61.7% vs. 55.0%), but the hand-engineered static IMO25 pipeline still wins on the stricter Pass@7 full-credit metric (55.0% vs. 48.3%) -- RQGM finds more near-complete proofs but concedes some fully-correct ones.
- **Ablation (Table 7):** with evaluator replacement off, a fixed critic gets gamed -- the writer trivially reaches 100% validation acceptance while its ground-truth anchor accuracy craters to 78.2%. Replacement alone (adversarial pool off) recovers most of the gain; removing selective erasure lets stale evidence accumulate and search stalls revisiting the same nodes.
- **Cost decomposition:** validation dominates blended token spend (65-69%), expansion 18-23%, train-time evaluation 12-14%, consistent across all three domains.
- **Shared infrastructure:** 59-90% of accepted code patches modify shared task-agent/infrastructure code rather than role-specific logic -- evidence that co-located roles cross-pollinate fixes.
- **Cheaper task-agent models:** routing search-time task-agent calls through Nemotron 3 Ultra (meta-agent stays on GPT-5.5) cuts token cost ~13x while approaching GPT-5.5-only final performance.
- Evaluator replacement genuinely re-ranks the archive (Spearman ρ between pre/post-replacement rankings drops well below 1 and stays there) -- confirming replacement isn't cosmetic and that selective erasure is necessary for it to actually redirect search.

---

## Suggestions & Future Directions

1. Extend to longer search horizons -- the current results are explicitly preliminary/short-horizon; the authors expect co-evolution's benefits to compound over longer runs.
2. Reduce dependence on strong ground-truth anchors, especially outside fully verifiable domains like math, since evaluator quality is bounded by anchor quality (a weak/biased anchor -- e.g., imperfect APReS decisions or IMO-GradingBench grades -- can let evaluators drift).
3. Extend theoretical guarantees beyond the epoch-local level -- current proofs bound neither cross-epoch regret from erased evidence nor convergence to a globally optimal agent-evaluator pair.
4. Widen the evolvable surface to the scheduler and replacement rules themselves, which would require stronger guardrails than analyzed here.
5. Layer richer objectives on top of the ground-truth anchor (as done with the adversarial reviewer) as the path toward evaluation that bootstraps itself beyond static benchmarks.
6. Include SWE-bench once its long per-task runtime can be accommodated -- excluded from this version for that reason.
7. Investigate allocating more train samples per meta-agent expansion call, since train-time evaluation may currently be under-weighted relative to its value.

---

## Authors & Institutions

Alex Iacob (Cambridge), Andrej Jovanović (Cambridge / Flower Labs), William F. Shen (Cambridge), Daniel Burkhardt (NVIDIA), Meghdad Kurmanji (Cambridge), Nurbek Tastan (MBZUAI), Lorenzo Sani (Cambridge / Flower Labs), Niccolò Alberto Elia Venanzi (NVIDIA), Ambroise Odonnat (Inria), Zeyu Cao (Cambridge), Bill Marino (Cambridge), Xinchi Qiu (Cambridge), Nicholas D. Lane (Cambridge / Flower Labs).
