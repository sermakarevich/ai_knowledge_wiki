> [[index|Wiki]] | [[summary|Summary]]

# PathRouter — Digest

The whole paper at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-related-work|Introduction and Related Work]]

**In one sentence:** Outcome-only reinforcement learning for agentic GraphRAG suffers from *answer-path reward aliasing* (correct answers can come from parametric-memory shortcuts rather than useful evidence paths, and wrong answers can occur even when key evidence is retrieved) and *search-update ambiguity* (scalar trajectory-level feedback gives no hint about which retrieval actions to adjust), and prior chunk-based RAG, entity-relation GraphRAG, and GRPO-trained retrieval agents all fail to make evidence-path quality a first-class, actionable training signal.

- RAG grounds LLM output in external evidence to reduce hallucination (Lewis et al., 2020; Gao et al., 2024; Wang et al., 2024), but standard chunk-based pipelines treat passages independently and fail to capture relational structure among entities.
- Graph-structured RAG organizes knowledge as entity-relation graphs, enabling multi-step retrieval over structured evidence paths (Edge et al., 2025; Guo et al., 2025; Chen et al., 2025; Luo et al., 2025b; Gutiérrez et al., 2025), while agentic approaches model retrieval as iterative agent–environment interactions optimized via reinforcement learning (Jin et al., 2025; Song et al., 2025; Luo et al., 2025a).
- Existing agentic GraphRAG methods rely **solely on answer correctness** for trajectory rewards, ignoring whether retrieved evidence truly supports the answer.
- This produces **two failure modes** (Figure 1): (a) *reasoning failure* — an incorrect answer despite retrieved/key evidence (F1 ≈ 0.00, EO ≈ 0.24 in the figure's NBA finals-MVP-statue example), and (b) *shortcut failure* — a correct answer produced from parametric memory after failed or unhelpful retrieval (F1 ≈ 1.00, EO ≈ 0.04). Both receive the same scalar reward, producing **answer-path reward aliasing**.
- Scalar trajectory-level feedback yields **search-update ambiguity**: it tells the agent nothing about which retrieval actions (queries, entities, relations) to adjust, leaving no actionable guidance.
- **PATHROUTER** resolves aliasing by evaluating each trajectory along two axes — answer correctness and **evidence-path overlap (EO)**, a token-level F1 between retrieved and gold evidence — building a 2×2 trajectory taxonomy (faithful success C↑P↑, shortcut success C↑P↓, evidence-retrieved-but-wrong C↓P↑, joint failure C↓P↓) and applying **differentiated route-conditioned GRPO advantage scaling** that suppresses shortcut reinforcement while preserving evidence-seeking behavior.
- For evidence-poor trajectories (C↑P↓ and C↓P↓), a **frozen gold-evidence teacher** — prompted with gold supporting passages — provides **token-level KL supervision on reasoning and search-query tokens**, with **answer tokens explicitly excluded** to avoid direct response imitation (mitigating answer-token leakage, cf. RLSD, Yang et al., 2026).
- Experiments on **six QA benchmarks across three model sizes** (3B and 7B results reported here) show consistent improvements over a strong baseline, with average **F1 gains of 3.1 on 3B and 4.9 on 7B models**, enhanced cross-dataset OOD transfer, and robust single-hop and multi-hop performance — evidence that path-aware training yields generalizable retrieval behavior rather than dataset-specific shortcuts.

## 2. [[wiki/02-pathrouter-method|PathRouter Method]]

**In one sentence:** PathRouter extends GRPO by scoring every trajectory on both answer correctness (C_i) and evidence-path overlap with the gold supporting passages (P_i), then classifying trajectories into four routes that scale the GRPO advantage so shortcut-style successes are damped and useful-but-wrong evidence-seeking is protected — and for evidence-poor trajectories, a selective teacher-KL term gives token-level guidance on top of the routed GRPO loss.

- **Multi-turn agent–environment formulation (Section 3.1):** agentic GraphRAG is formalized as a multi-turn interaction in which an LLM agent π_θ answers a query q over a knowledge graph G; at each turn it either emits a reasoning segment plus a search query, or terminates with a final answer.
- **Two diagnostic scores per trajectory:** C_i = 1[EM(a_i, a*) > 0 ∨ F1(a_i, a*) ≥ θ_C] (Eq. 1) is binary answer correctness; P_i (Eq. 2) is the average token-F1 between retrieved passages and each gold supporting passage.
- **Four-way route classification (Eq. 3):** C↑P↑ (Faithful Success), C↑P↓ (Shortcut Failure), C↓P↑ (Evidence Retrieved), C↓P↓ (Joint Failure), each with a distinct advantage weight (w_full for C↑P↑/C↓P↓, w_down for C↑P↓, w_preserve for C↓P↑).
- **Selective teacher-KL distillation (Section 3.3):** for evidence-poor trajectories (P_i < θ_P), a frozen reference model conditioned on the same response prefix plus the gold supporting passages S_gt supplies token-level KL guidance restricted to reasoning and search-query tokens, never retrieved observations or the final answer.
- **Training objective (Section 3.4):** the reward combines answer F1, evidence-path overlap, and exploration-shaping terms (Eq. 8–9); the routed GRPO loss (Eq. 10) scales each trajectory's advantage by its route weight; the overall objective adds a warmed-up teacher-KL term to routed GRPO (Eq. 11): L = L_GRPO + λ_T(s) · L_TKL.

## 3. [[wiki/03-experimental-setup-and-main-results|Experimental Setup and Main Results]]

**In one sentence:** PathRouter is evaluated on six QA benchmarks against GraphRAG, non-retrieval, chunk-based, and graph-based agentic baselines, and it delivers consistent gains over Graph-R1 at every model scale — largest on the multi-hop benchmarks where evidence-path faithfulness matters most.

- **Research questions (§4):** RQ1 — does PATHROUTER improve answer accuracy and evidence quality over existing baselines (§4.2)? RQ2 — which components drive path faithfulness, and how does routing change trajectory-level behavior (§4.3, §4.4)? RQ3 — how does teacher KL interact with model capacity, and do the learned retrieval strategies transfer across datasets (§4.5, §4.6)?
- **Datasets (§4.1):** six QA benchmarks — three multi-hop (HotpotQA, 2WikiMultiHopQA, MuSiQue) with gold supporting facts, and three single-hop (NQ, PopQA, TriviaQA).
- **Baselines (§4.1), following Graph-R1:** GPT-4o-mini-based references (GraphRAG, LightRAG, PathRAG, HippoRAG2, HyperGraphRAG), non-retrieval approaches (NaiveGeneration, SFT, R1), chunk-based retrieval (StandardRAG, Search-R1, R1-Searcher), and graph-based agentic retrieval (Graph-R1, the primary baseline).
- **Metrics (§4.1):** token-level F1, Exact Match (EM), and GPT-4o-mini evaluation (G-E) for answer quality; Supporting Fact F1 (SF-F1) and Unsupported Answer Rate (UAR, ↓) for path faithfulness.
- **Main results (§4.2):** PATHROUTER consistently outperforms Graph-R1 across all model scales — 7B average F1 improves from 57.82 to 62.74, EM from 48.57 to 53.26, G-E from 76.23 to 78.72 — and also outperforms the `w/o TKL` ablation at every scale.
- **Gains are most pronounced on multi-hop benchmarks (§4.2):** at 7B, F1 rises by 7.4 points on HotpotQA and 8.2 on MuSiQue; the pattern holds at smaller scales (average F1 +3.1 at 3B, +3.2 at 1.5B).
- **Scaling behavior (§4.2):** route conditioning is scale-robust, while TKL is more capacity-sensitive.

## 4. [[wiki/04-experiments-and-main-results|Ablation, Trajectory Quality, Teacher Scale, and Cross-Dataset Transfer]]

**In one sentence:** PathRouter (PATHROUTER) outperforms the strongest baseline (Graph-R1) across all six QA benchmarks at every model size tested (1.5B, 3B, 7B), with ablations showing the exploration bonus and lazy penalty are critical for multi-step evidence seeking and that 2D routing plus selective teacher KL drive path faithfulness, while the teacher-scale analysis shows student capacity — not teacher quality — is the bottleneck at small scale, and cross-dataset transfer reaches a 95.7% average OOD ratio.

- **Ablation (reward group):** removing the exploration bonus or lazy penalty is catastrophic — retrieval collapses to ~1 turn and all metrics degrade sharply (e.g., HotpotQA F1 drops from 70.13 to 43.51/48.23); removing the path reward mainly lowers SF-F1 while retaining answer F1.
- **Ablation (KL & routing groups):** selective KL beats uniform KL; KL warmup improves F1/UF and avoids inflated turn counts; 2D routing beats both 1D answer-only and 1D path-only variants.
- **Routing/trajectory quality:** Figure 3 shows PATHROUTER shifts trajectory mass from the P↓ column into the P↑ column on all six datasets, proving improved evidence acquisition independent of answer correctness.
- **Teacher scale:** online self-distillation is always inferior; same-size frozen teachers are best at all scales; a 7B frozen teacher supervising a 1.5B student degrades F1 to 15.83 — the bottleneck is student capacity, not teacher quality.
- **Scheduling (Table 4):** warmup λ with a frozen teacher is the best configuration on 7B; constant-λ over-constrains early training and inflates turns.
- **Cross-dataset transfer:** PathRouter achieves all off-diagonal transfer ratios above 89%, averaging **95.7%**, vs. 70.6% for Search-R1 and 85.8% for Graph-R1.

## 5. [[wiki/05-limitations-and-appendix|Limitations and Appendix]]

**In one sentence:** PathRouter trades training efficiency (extra routing/teacher hyperparameters, more exploration turns, per-step teacher forward passes) for faithfulness — a trade the appendices back up with exact metric definitions (F1, EM, SF-F1, UAR, G-E), a complete hyperparameter configuration, a KL-selection/threshold-sensitivity analysis, and case studies showing outcome-only training reaching correct answers from parametric memory or hallucinated bridge entities with near-zero path overlap.

- **Acknowledged limitations:** extra routing/teacher-scheduling hyperparameters may need re-tuning on smaller models or new domains; more exploration turns during training; frozen teacher's forward passes add per-step cost.
- **Key hyperparameters:** learning rate 1×10⁻⁶ (batch 128, 3 epochs); group size K=32; max retrieval turns T=5 in training; clip range ε=0.2; teacher KL coefficient λ̄_T=0.1 with 20 warmup steps; thresholds θ_C=0.5, θ_P=0.1; route weights 1.0/0.5/0.3.
- **KL selection:** low-P_i trajectory filtering beats content-based and uniform sampling; extending KL to answer tokens raises UAR from 39.95 to 46.23 — answer-token imitation creates shortcuts.
- **Threshold sensitivity:** performance stable for θ_P ∈ [0.05, 0.2] but degrades at θ_P=0.3, where 88% of trajectories receive teacher KL.
- **Training dynamics:** faithful (C↑P↑) trajectories grow steadily, joint failures (C↓P↓) vanish within the first 20 steps — an implicit curriculum from teacher-guided correction to on-policy reinforcement.
- **Case-study takeaway:** GRPO repeatedly produces the exact right answer (F1 up to 1.000) with near-zero path overlap (as low as 0.028) from parametric memory or a hallucinated bridge entity, while PathRouter's trajectories are shorter, evidence-grounded reasoning chains.

## The argument in five moves

1. Outcome-only RL rewards agentic GraphRAG agents purely on answer correctness, which conflates lucky/shortcut answers with genuinely evidence-grounded ones (answer-path reward aliasing) and gives no signal about which search action to fix (search-update ambiguity).
2. PathRouter adds a second diagnostic axis — evidence-path overlap P_i — and classifies every trajectory into one of four correctness×overlap routes.
3. Each route gets its own GRPO advantage weight, damping shortcut reinforcement while protecting useful-but-wrong evidence-seeking; evidence-poor trajectories additionally receive token-level KL guidance from a frozen, gold-evidence-privileged teacher, restricted to reasoning/search-query tokens.
4. Across six QA benchmarks and three model scales, this consistently beats the strongest prior agentic-GraphRAG baseline (Graph-R1), with the largest gains on multi-hop questions where evidence composition matters most.
5. The mechanism generalizes: routing decouples faithful behavior from any one dataset's shortcuts, yielding a 95.7% average cross-dataset transfer ratio — and case studies confirm outcome-only training's wins are frequently ungrounded, while PathRouter's are evidence-backed.
