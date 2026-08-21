---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: SAGE

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. SAGE names three "core challenges" that static GraphRAG systems can't address. What is Challenge I, and why does early anchor commitment cause it?

> [!tip]- Answer
> Challenge I is global associative reading: a query may only give an episodic clue, alias, or distant conceptual hint. If the reader commits early to a small set of query-matched anchor entities, the bridge nodes actually needed to answer the question can lie outside the region the anchors activate, so the evidence chain stays disconnected even after propagation. See [[wiki/01-challenges-and-related-work|Challenges and Related Work]].

### Q2. In SAGE's formalization, what are s_h, a_h, and the graph-update operator, and which component do they belong to?

> [!tip]- Answer
> They describe the writer as a structured policy: at step h, given state s_h, the writer samples a writing action a_h ~ π_θ(· | s_h) and updates the partial graph as G_{h+1} = G_h ⊕ a_h (⊕ being the graph-update operation). This makes the writer learnable via RL-style action selection rather than a fixed construction rule. See [[wiki/01-challenges-and-related-work|Challenges and Related Work]].

### Q3. What is the writer's hybrid task reward made of, and what does the repetition penalty ρ_rep(G) prevent?

> [!tip]- Answer
> r_task = (α·r_rec + β·r_pre + γ·r_ded)/(α+β+γ), where r_rec rewards coverage of gold evidence by the reader's top-k set, r_pre penalizes irrelevant evidence expansion, and r_ded checks whether a judge can derive the answer from the retrieved evidence; an answer-level F1 auxiliary is also used. The repetition penalty in the trajectory return stops the writer's policy from inflating the graph with duplicate triples just to game recall. See [[wiki/02-method-writer-and-reader|Method: Memory Writer + Memory Reader]].

### Q4. Why does SAGE's reader use a synapse-inspired edge gate instead of uniform message passing or fixed community expansion (as in classic GraphRAG)?

> [!tip]- Answer
> The gate g_uv^[l] = 1 + δ·tanh(MLP_g^[l](z_uv^[l])) lets the reader learn, per edge, three brain-like behaviors absent from PPR/community expansion: inhibiting hub edges (so a highly connected generic node doesn't flood retrieval), preserving long-distance bridge edges (so rare but crucial connections aren't pruned like noise), and habituating (down-weighting) redundant local edges. This directly targets Challenge II — treating structure as something to learn rather than a fixed index. See [[wiki/02-method-writer-and-reader|Method: Memory Writer + Memory Reader]].

### Q5. What is SAGE's single biggest empirical result, and how does it compare to HippoRAG 2 and RAPTOR?

> [!tip]- Answer
> Trained only on multi-hop QA data (MuSiQue, HotpotQA, 2WikiMultiHopQA), SAGE achieves 82.5% Recall@2 / 91.6% Recall@5 in zero-shot transfer to Natural Questions — far above HippoRAG 2 (45.6/78.0) and RAPTOR (40.3/68.3). This is presented as evidence the writer–reader co-training produces transferable retrieval skill, not dataset-specific tricks. See [[wiki/03-experiments-and-conclusion|Experiments and Conclusion]].

### Q6. On which class of benchmark does SAGE *not* yet lead, and what does the paper attribute the gap to?

> [!tip]- Answer
> On specialized long-term-memory benchmarks (LongMemEval, HaluMem), SAGE is competitive but does not surpass the strongest system-level memory baselines (Memobase, Supermemory, MemU), though an extra self-evolution training round already beats Memobase on several metrics. The paper attributes the remaining gap to memory *updating* and high-coverage extraction, not to the core reader/writer retrieval mechanism. See [[wiki/03-experiments-and-conclusion|Experiments and Conclusion]].

### Q7. Appendix A's writer-reward ablation shows that pure recall-maximizing reward and hybrid reward diverge on one metric in particular. Which metric, and what does that divergence prove?

> [!tip]- Answer
> RL-Recall reaches high Precision/Recall (0.889/0.835) but a lower Deducible score (0.502) than RL-Hybrid (0.902/0.917 precision/recall, 0.522 deducible). This proves that matching the gold evidence set is not the same as the evidence actually being sufficient for an answer to be derived — retrieval-quality metrics and answer-deducibility can move in opposite directions. See [[wiki/04-appendix-writer-analysis-snr|Appendix A & B — Writer Analysis and SNR / Retrieval-Budget Theory]].

### Q8. What does Theorem B.13's retrieval-budget bound say the top-k budget B_ρ(q,G) depends on, and why does the paper stress that SAGE's advantage doesn't need "perfect edge-wise classification"?

> [!tip]- Answer
> B_ρ(q,G) ≤ m_ρ + (m_ρ K_A)/(c_ρ S_L)·(1/SNR_L) + m_ρ·ζ_A/(c_ρ S_L) — the budget needed for a given evidence-coverage level grows with 1/SNR_L, the inverse of the aggregate signal-to-noise ratio at the final layer. Propositions 2–5 show the bound only requires *aggregate* (or high-probability) evidence-retention dominance — the per-layer ratios B_l/A_l and C_l/A_l being sufficiently small — so the design doesn't rely on every single edge gate being classified correctly, only on the aggregate tendency to suppress noise and retain signal. See [[wiki/04-appendix-writer-analysis-snr|Appendix A & B — Writer Analysis and SNR / Retrieval-Budget Theory]].

### Q9. Appendix C's context–schema decomposition theorem (Thm C.4) bounds the reader's error as R_G ≤ 2ε_sch + 2ε_ctx. What does each term represent, and what happens if the reader uses *only* the schema part?

> [!tip]- Answer
> ε_sch is how well a schema class approximates the shared structural rule across graphs; ε_ctx is how well a context class approximates the residual specific to the current target graph. A schema-only reader (dropping the context channel) retains an irreducible bias exactly equal to the squared L² distance between the true context-conditioned reading function and the schema hypothesis class (Proposition 6) — it can't fully adapt to graph-specific structure no matter how much data it sees. See [[wiki/05-appendix-calibration-stability-theory|Appendix C–F — Calibration, Stability, and the Writer–Reader Loop Theory]].

### Q10. Appendix F's "irreducible bottlenecks" result (Proposition 9) says reader-only or writer-only updates each hit a hard floor. What is that floor, in words?

> [!tip]- Answer
> With total error E = E_write(θ) + E_read(ϕ;θ) + ε_int, updating only the reader can never push total error below E_write(θ) (the writer's own error term is untouched), and updating only the writer can never push it below E_read(ϕ;θ′) (the reader's error given the new graph is still there). The two update mechanisms are complementary, not substitutable — which is why the alternating self-evolution loop, rather than fixing one side and endlessly retraining the other, is necessary. See [[wiki/05-appendix-calibration-stability-theory|Appendix C–F — Calibration, Stability, and the Writer–Reader Loop Theory]].

### Q11. In the Appendix G/H reader ablations (Table 8), how much does removing the structural gate cost on HotpotQA R@2, and how does that compare to switching to fully uniform message passing?

> [!tip]- Answer
> Full SAGE gets 65.1 R@2 on HotpotQA. Removing the structural gate drops it to 60.4 (−4.7); switching to uniform message passing drops it further to 58.9 (−6.2). Both variants still outperform a vanilla GNN reader (57.2), showing structural gating is the single largest lever among the reader's components, and that even "un-gated but still graph-structured" beats no graph structure at all. See [[wiki/06-appendix-ablations-and-implementation|Appendix G–O — Ablations and Implementation]].

### Q12. In the Appendix P HotpotQA case study, how does SAGE connect "the 2022 FIFA World Cup bid" to a specific birth date, and what retrieval capability does this demonstrate?

> [!tip]- Answer
> SAGE follows the inverse relation "was one of the representatives of"⁻¹ from the World Cup bid entity to "Frank Lowy," then an "equivalent" (alias) edge to "Sir Frank P. Lowy," whose birth date (22 October 1930) satisfies the question's second constraint; a second, reverse path verifies the same chain starting from the date. This demonstrates SAGE's ability to align different surface forms of the same entity (alias resolution) while jointly satisfying multiple question constraints within a single retrieval pass — directly answering Challenge I (global associative reading) with an inspectable, interpretable path. See [[wiki/07-appendix-additional-results-case-studies|Appendix P–R — Additional Results and Case Studies]].
