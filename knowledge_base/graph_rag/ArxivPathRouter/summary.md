> [[index|Wiki]] | [[digest|Digest]]

# PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation

**Paper:** [PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation (Wang et al., 2026)](https://arxiv.org/abs/2606.16409)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine training a research assistant by only checking whether its final answer is right — you never check whether it actually looked at the right documents. It will quickly learn to guess from memory when guessing works, and you can't tell "got it right by actually reading the sources" from "got it right by luck." PathRouter fixes this for AI agents that search a knowledge graph to answer questions: it separately scores whether the answer is correct AND whether the agent's search trail actually covered the right evidence, then rewards the agent differently depending on which of four combinations happened. For the agent's worst search trails, it also gets extra coaching from a "teacher" that has been shown the right evidence, so the agent learns which specific searches to fix — not just "try again."

## TL;DR

Agentic GraphRAG trained with outcome-only RL (reward = "was the answer correct?") suffers from answer-path reward aliasing (lucky guesses and evidence-grounded answers get the same reward) and search-update ambiguity (a scalar reward gives no signal about which search actions to change). PathRouter scores each trajectory on answer correctness (C_i) and evidence-path overlap with gold passages (P_i), routes GRPO's advantage through four category-specific weights, and adds selective token-level teacher-KL distillation (from a frozen, gold-evidence-privileged reference model) restricted to reasoning/search-query tokens for evidence-poor trajectories. On six QA benchmarks and three Qwen2.5 scales it beats Graph-R1 at every size (7B: F1 57.82→62.74, EM 48.57→53.26), with the largest gains on multi-hop datasets, and reaches a 95.7% average cross-dataset OOD transfer ratio versus 70.6% (Search-R1) and 85.8% (Graph-R1).

---

## Problem & Motivation

Agentic GraphRAG systems (e.g., Graph-R1, Search-R1) train retrieval agents with GRPO using a single scalar reward — usually answer F1/EM. This conflates two structurally different failures, illustrated in the paper's running example ("Who developed the statue of the person with the most finals MVPs in the NBA?"): (1) a wrong answer despite retrieving useful evidence ("reasoning failure"), and (2) a correct-looking answer produced from parametric memory after retrieval failed ("shortcut failure"). Both receive the same reward under outcome-only training — **answer-path reward aliasing** — and even when the reward does distinguish good from bad trajectories, it gives no token- or query-level signal about **which** retrieval action needs fixing — **search-update ambiguity**. Left unaddressed, this lets RL-trained retrieval agents learn to "cheat" via memorized knowledge instead of building genuinely evidence-grounded search behavior, which especially hurts generalization to unfamiliar datasets/domains.

---

## Main Original Ideas

1. **Two-axis trajectory evaluation.** Every trajectory is scored on both binary answer correctness C_i (EM or F1 above a threshold) and evidence-path overlap P_i (average token-F1 between all retrieved passages and each gold supporting passage) — making evidence quality a first-class, measurable signal instead of an afterthought.
2. **Four-way route-conditioned GRPO advantage scaling.** Trajectories fall into C↑P↑ (faithful success), C↑P↓ (shortcut success), C↓P↑ (evidence retrieved but wrong), or C↓P↓ (joint failure); each route gets its own non-negative weight (w_full / w_down / w_preserve) that scales — but never flips the sign of — the group-relative GRPO advantage, damping shortcut reinforcement while protecting useful-but-currently-wrong evidence-seeking.
3. **Selective teacher-KL distillation for evidence-poor trajectories.** For trajectories with P_i below threshold, a frozen reference model conditioned on the *same* on-policy prefix plus the gold evidence passages supplies token-level KL guidance restricted to reasoning and search-query tokens (never retrieved text or the final answer) — turning a single scalar failure signal into localized, actionable retrieval guidance without teaching the model to imitate final answers.
4. **Combined training objective with KL warmup.** The final loss adds a linearly warmed-up teacher-KL term to the routed GRPO loss, so the student first learns from reward signals before the teacher constraint takes full effect — avoiding early-training over-constraint when most trajectories are still evidence-poor.

---

## Key Findings

Six QA benchmarks (HotpotQA, 2WikiMultiHopQA, MuSiQue, NQ, PopQA, TriviaQA), three Qwen2.5-Instruct scales (1.5B/3B/7B), baseline = Graph-R1 (the strongest prior agentic-GraphRAG method):

| Model size | Method | Avg EM | Avg F1 | Avg G-E |
|---|---|---|---|---|
| 1.5B | Graph-R1 | 31.90 | 40.09 | 64.38 |
| 1.5B | **PathRouter** | **35.55** | **43.31** | **67.72** |
| 3B | Graph-R1 | 42.45 | 51.26 | 72.99 |
| 3B | **PathRouter** | **44.48** | **54.32** | **75.70** |
| 7B | Graph-R1 | 48.57 | 57.82 | 76.23 |
| 7B | **PathRouter** | **53.26** | **62.74** | **78.72** |

- Gains are largest on multi-hop benchmarks where evidence composition matters most: at 7B, F1 rises 7.4 points on HotpotQA and 8.2 on MuSiQue.
- Ablation: removing the exploration bonus or lazy penalty is catastrophic (retrieval collapses to ~1 turn); 2D routing beats 1D answer-only or 1D path-only routing; selective KL beats uniform KL and content-based/uniform trajectory sampling.
- Teacher-scale analysis: same-size frozen teachers work best at every scale; a larger (7B) frozen teacher supervising a 1.5B student actually degrades performance — student capacity, not teacher quality, is the bottleneck.
- Cross-dataset transfer (train on one dataset, evaluate on all others): PathRouter reaches a **95.7%** average OOD ratio (all off-diagonal ratios > 89%), versus **70.6%** for Search-R1 and **85.8%** for Graph-R1 — the learned retrieval behavior is not tied to any one training distribution.
- Case studies show outcome-only GRPO repeatedly reaches the exact right answer (F1 up to 1.000) with near-zero path overlap (as low as 0.028) via parametric memory or a hallucinated bridge entity; PathRouter reaches the same or better answers with 3–12x higher path overlap in fewer turns.

---

## Suggestions & Future Directions

1. **Cost/tuning tradeoff acknowledged as a limitation:** routing and teacher-scheduling introduce extra hyperparameters that may need re-tuning for smaller models or new domains.
2. **More exploration turns during training** as a side effect of the path-aware reward — an efficiency cost the paper accepts in exchange for faithfulness.
3. **Per-step teacher forward-pass cost** for selective KL, which the paper does not quantify in wall-clock or FLOPs terms.
4. Implicit open question (from the teacher-scale analysis): how to close the capacity gap so smaller students can benefit from stronger (larger) frozen teachers, rather than only same-size teachers working well.

---

## Authors & Institutions

Bo Wang, Heyan Huang, Yaolin Li, Wei Tang, Yuan Zhang, Wenbo Li, Mingze Gao, Ge Shi, Chong Feng — Beijing Institute of Technology; Joy Future Academy.

## Figures

![Figure 1: Two failure modes of outcome-only training](wiki/images/01-fig1-failure-modes.png)

![Figure 2: PathRouter overview](wiki/images/02-fig2-overview.png)
