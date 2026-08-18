**Figure 3** is a three‑panel figure comparing GoAgent against a set of baseline topologies on (a) token cost on MMLU, (b) token cost on GSM8K, and (c) robustness under a prompt‑injection attack.

**Panels (a) & (b) – Token cost vs. accuracy (bubble/scatter plots).**
- **X‑axis:** Accuracy (%) (roughly the low‑80s to mid‑90s).
- **Y‑axis:** Token consumption, scaled ×10⁵ (MMLU ≈ 0.2–1.0; GSM8K ≈ 0.4–1.4).
- Each bubble is one method (e.g., LLM‑Debate, Complete/Chain, Random, SC, EIB‑LEARNER, ARG‑Designer, GoAgent), with bubble color/size encoding a secondary attribute.
- **Trend:** There is a clear trade‑off frontier. Dense, node‑centric topologies (LLM‑Debate, Complete, Chain, Random) cluster in the *upper‑left* — high token consumption for only moderate accuracy. Sparse/graph‑learning baselines (ARG‑Designer, EIB‑LEARNER) sit lower but still above the ideal region. **GoAgent** lands in the *lower‑right* corner: among the highest accuracy while using one of the lowest token budgets, i.e., it dominates the cost‑accuracy Pareto front on both benchmarks.

**Panel (c) – Robustness under attack (grouped bar chart).**
- **X‑axis:** Method (Full, Random, Tree, Debate, Prune, G‑Designer, EIB‑LEARNER, ARG‑Designer, GoAgent/"Ours").
- **Y‑axis:** Accuracy (%), roughly 70–90.
- Two bars per method: *Before attack* (blue) and *After attack* (red).
- **Trend:** Every baseline suffers a noticeable post‑attack accuracy drop (e.g., Full, Tree, Debate, Prune all lose on the order of ~5–10 points). GoAgent starts at the highest pre‑attack accuracy (≈90%) and retains the highest post‑attack accuracy (≈89%), showing by far the smallest degradation.

**Takeaway.** GoAgent achieves a favorable efficiency/accuracy Pareto position — top accuracy with minimal inference tokens on both MMLU and GSM8K — and remains the most robust method to prompt‑injection attacks, outperforming all baselines on all three axes (token cost on two benchmarks and attack robustness). This supports the paper's claim that group‑level generation plus structural noise filtering yields a model that is simultaneously more efficient, more accurate, and more attack‑resistant than node‑centric alternatives.