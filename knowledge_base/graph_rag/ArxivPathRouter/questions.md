---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: PathRouter

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the two structural problems with outcome-only RL rewards in agentic GraphRAG that PathRouter names, and how does each one concretely hurt training?

> [!tip]- Answer
> **Answer-path reward aliasing**: a correct answer from parametric memory (no real evidence) and a correct answer from genuine evidence retrieval get the same scalar reward, so the training signal can't distinguish "lucky" from "faithful" success. **Search-update ambiguity**: even a reward that does flag a bad trajectory gives no token- or query-level signal about which specific retrieval action needs to change. See [[wiki/01-introduction-and-related-work|Introduction and Related Work]].

### Q2. In the two diagnostic scores C_i and P_i, what exactly does each measure, and why is P_i alone not enough to fix reward aliasing without also using C_i?

> [!tip]- Answer
> C_i is binary answer correctness (exact match or F1 above threshold θ_C). P_i is evidence-path overlap: the average token-level F1 between the trajectory's retrieved passages and each gold supporting passage. P_i alone can't fix aliasing because a trajectory can retrieve good evidence yet still answer wrong (a reasoning failure) — you need both axes to distinguish "faithful success," "shortcut success," "evidence retrieved but wrong," and "joint failure." See [[wiki/02-pathrouter-method|PathRouter Method]].

### Q3. Why does PathRouter's teacher-KL supervision explicitly exclude answer tokens and retrieved-observation tokens, applying only to reasoning and search-query tokens?

> [!tip]- Answer
> Applying KL to answer tokens would let the student directly imitate the teacher's final answer (an "answer-token leakage" shortcut, the risk RLSD documented) rather than learning better search behavior; excluding retrieved-observation tokens keeps the supervision on the agent's own generated actions instead of on text it didn't produce. Masking to reasoning/search-query tokens forces the guidance to shape *how the agent searches*, not what it ultimately answers. See [[wiki/02-pathrouter-method|PathRouter Method]].

### Q4. Why is the teacher-KL coefficient λ_T(s) linearly warmed up over the first W steps instead of applied at full strength from the start of training?

> [!tip]- Answer
> Early in training, most trajectories still have low evidence overlap and would all qualify for teacher KL, which would suppress the on-policy exploration the student needs to discover effective retrieval strategies on its own. Warming up lets the student first learn from GRPO reward signals before the teacher constraint gradually takes full effect. See [[wiki/02-pathrouter-method|PathRouter Method]].

### Q5. On the six-benchmark evaluation, what were PathRouter's average F1/EM/G-E gains over Graph-R1 at the 7B scale, and which benchmark category (multi-hop or single-hop) saw the largest improvement?

> [!tip]- Answer
> At 7B, average F1 rose from 57.82 to 62.74, EM from 48.57 to 53.26, and G-E from 76.23 to 78.72. Gains were largest on multi-hop benchmarks (HotpotQA +7.4 F1, MuSiQue +8.2 F1), where faithful evidence composition matters most. See [[wiki/03-experimental-setup-and-main-results|Experimental Setup and Main Results]].

### Q6. In the ablation study, what happens when the exploration bonus (r_e) or lazy penalty (r_l) is removed, and what does that reveal about what these reward terms actually control?

> [!tip]- Answer
> Removing either one is catastrophic: retrieval collapses to roughly a single turn and all metrics degrade sharply (e.g., HotpotQA F1 drops from 70.13 to 43.51/48.23). This reveals that these two terms specifically control whether the agent keeps searching multiple turns at all — they're not fine-tuning refinements but load-bearing for multi-step evidence seeking. See [[wiki/04-experiments-and-main-results|Ablation, Trajectory Quality, Teacher Scale, and Cross-Dataset Transfer]].

### Q7. The teacher-scale analysis found that supervising a 1.5B student with a larger 7B frozen teacher degrades performance rather than helping. What does the paper conclude is the bottleneck, and why would a "smarter" teacher hurt?

> [!tip]- Answer
> The paper concludes the bottleneck is student capacity, not teacher quality — the 7B teacher's distribution is too complex/fine-grained for a 1.5B student to usefully track, so forcing the smaller model toward a bigger model's token distribution actively hurts rather than helps (F1 degrades to 15.83, UAR rises above 63%). Same-size frozen teachers work best at every scale tested. See [[wiki/04-experiments-and-main-results|Ablation, Trajectory Quality, Teacher Scale, and Cross-Dataset Transfer]].

### Q8. PathRouter reaches a 95.7% average cross-dataset OOD transfer ratio versus 70.6% (Search-R1) and 85.8% (Graph-R1). What does this experiment actually test, and what does the gap suggest about what each method's training signal is rewarding?

> [!tip]- Answer
> The experiment trains a model on one dataset and evaluates it on all five others (a 6×6 train×eval matrix), measuring how well retrieval behavior transfers to unseen data distributions. The large gap suggests outcome-only RL (Search-R1) lets the model overfit to dataset-specific answer patterns/shortcuts, while PathRouter's evidence-path-conditioned reward shapes retrieval behavior that isn't tied to any one dataset's quirks. See [[wiki/04-experiments-and-main-results|Ablation, Trajectory Quality, Teacher Scale, and Cross-Dataset Transfer]].

### Q9. In the case studies (Appendix E), what specific behavior let GRPO (outcome-only training) reach the exact correct answer in Case 3 with essentially no supporting evidence?

> [!tip]- Answer
> GRPO's agent repeated a failed search query ("governor of Mississippi salary") for several turns, found nothing useful, and then emitted the exact figure $122,160 anyway — a value that never appeared in any retrieved passage (path overlap = 0.028). This is a parametric-memory hallucination that outcome-only F1/EM scoring rewards fully because it happens to be correct. See [[wiki/05-limitations-and-appendix|Limitations and Appendix]].

### Q10. The paper acknowledges three concrete costs of its own method. What are they, and which one does the paper leave unquantified?

> [!tip]- Answer
> The three acknowledged costs are: extra routing/teacher-scheduling hyperparameters that may need re-tuning for smaller models or new domains, more exploration turns during training, and per-step teacher forward-pass cost from selective KL. The paper never quantifies any of these in wall-clock time, GPU-hours, or memory overhead versus the Graph-R1 baseline. See [[wiki/05-limitations-and-appendix|Limitations and Appendix]] and [[critical_thinking|Critical Analysis]].

### Q11. If you wanted to apply PathRouter's core idea to a coding agent that is trained via RL to fix bugs (reward = "did the test suite pass?"), what would the analogue of C_i and P_i be, and what's the analogue of the "shortcut failure" route?

> [!tip]- Answer
> C_i would be whether the tests pass; P_i would need to measure whether the agent's actual code changes/diagnostic steps overlap with the "real" root cause (e.g., overlap with a reference fix's changed lines, or with files a human diagnosis flagged as relevant). "Shortcut failure" (C↑P↓) would be a patch that makes tests pass without addressing the underlying bug — e.g., deleting/weakening a test, hardcoding an expected output, or a change unrelated to the actual defect that happens to satisfy the test suite by coincidence. This is a transfer question — the paper doesn't cover coding agents.

### Q12. Per the critical analysis, what is the weakest link in PathRouter's evidence, and why does it matter more than it might first appear?

> [!tip]- Answer
> The teacher-KL ablations (trajectory-selection strategy and token-masking choice in Table 7, and the θ_P threshold sensitivity in Table 8) are run on a single dataset (MuSiQue) at a single model size (7B), even though these design choices are central to the paper's second main contribution. It matters because the headline results are aggregated across six datasets and three scales, but the specific mechanism justifying *why* selective, token-masked KL is the right design is only validated in one narrow setting — so it's unclear whether that specific configuration (vs. some other selection/masking choice) would still be best elsewhere. See [[critical_thinking|Critical Analysis]].
