> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Final Round Selection
**In one sentence:** A final-round candidate is admissible only if it passes the noise-adjusted floor, the applicable complexity-aware branch, and all domain guards, with the highest-scoring admissible candidate selected (otherwise the incumbent is retained) and the running best updated as 𝑆★ ← max(𝑆★, 𝑆ˆ(𝐻𝑡+1)).
## Key points
- Admissibility requires all three conditions jointly: the noise-adjusted floor, the appropriate branch of the complexity-aware rule, and all active domain guards.
- Among admissible candidates the selector picks the one with the largest measured score; if none is admissible, the incumbent is retained.
- The running best score is updated as 𝑆★ ← max(𝑆★, 𝑆ˆ(𝐻𝑡+1)).
- Hyperparameters are selected using only the evolve environment and operational considerations; held-out and OOD benchmarks are not used for tuning, and the noise tolerance 𝛿 is calibrated from repeated evaluations of the unchanged base harness.
- Scores 𝑆ˆ are fractions in [0, 1] and Δ𝐶 is the relative change in policy tokens per trial: 𝛿 is 0.017 (coding, 3 passes out of 89 × 𝑘 = 178 trials), 0.004 (agentic workspace, 60 criteria out of ~14,100 verdicts), and 0.020 (engineering design, 5 passes out of 61 × 𝑘 = 244 trials).
- Cost trade-off parameters (𝛽0, 𝛽1) are (0.10, 44.5) coding, (0.10, 35.4) agentic workspace, (0.15, 24.4) engineering design, corresponding to a 25% token allowance per additional pass (coding), per 100 additional criteria (agentic workspace), and a 10% allowance per additional pass (engineering design).
- Case-study trajectories show selection is not score alone: Coding R0-A accepted (+3.93 points) while similar R0-B rejected by cost rule (+1.69 points, +26.1% cost); Coding R8-B rejected by floor (−2.81 points despite −13.6% cost); Engineering R2 accepted (122/244 → 128/244 passes, +1.6% tokens) as a small reusable control-flow fix.
---
## Final-round selection rule
A candidate is admissible only if it satisfies the noise-adjusted floor, the appropriate branch of the complexity-aware rule, and all active domain guards. Among admissible candidates, the selector chooses the one with the largest measured score; if none is admissible, the incumbent is retained. The running best score is then updated as 𝑆★ ← max(𝑆★, 𝑆ˆ(𝐻𝑡+1)).
## D.1 Hyperparameter Setting
RRSI hyperparameters control update sparsity, exploration, pruning, and the cost–performance trade-off. They are selected using only the evolve environment and operational considerations; held-out and OOD benchmarks are not used for tuning. The noise tolerance 𝛿 is calibrated from repeated evaluations of the unchanged base harness. The edit-budget parameters (𝑏min, 𝑏max) determine how many independent changes can be bundled into one candidate, while 𝑤 and 𝑚draft control when and how strongly the search explores underused components. The pruning window 𝑛prune determines how much recent evidence is required before a component is treated as unproductive. Finally, (𝛽0, 𝛽1) encode the allowed trade-off between measured gain and additional inference cost. Table 5 lists the values used in each instance.

| Hyperparameter | Role | Coding | Agentic workspace | Engineering design |
|---|---|---:|---:|---:|
| 𝑇 | evolution rounds | 20 | 20 | 40 |
| 𝑘 | trials per task per evaluation | 2 | 2 | 4 |
| 𝛿 | empirical noise tolerance | 0.017 | 0.004 | 0.020 |
| 𝑏min | final-round edit budget | 1 | 1 | 1 |
| 𝑏max | initial edit budget | 4 | 3 | 4 |
| 𝑤 | stall-detection window | 3 | 3 | 3 |
| 𝑚draft | reserved exploratory proposals | 1 | 1 | 1 |
| 𝑛prune | pruning window | 4 | 4 | 5 |
| 𝛽0 | base cost allowance | 0.10 | 0.10 | 0.15 |
| 𝛽1 | gain-dependent cost allowance | 44.5 | 35.4 | 24.4 |

Table 5 | Hyperparameters used by RRSI in each evolution setting. All choices are fixed without consulting held-out or OOD benchmarks.
## E. Qualitative Case Study
To complement the aggregate results, representative decisions made during RRSI evolution are inspected; Table 6 summarizes several examples from the released trajectories, with complete round-by-round records (proposals, critic decisions, acceptance decisions, exact harness diffs) available on the project website.

> "These examples provide a more concrete view of the regularization behavior. In particular, the two candidates from the first coding round are superficially similar, yet only the candidate with a sufficiently large measured improvement survives the cost-aware selection rule. Conversely, the round-8 candidate reduces inference cost but is still rejected because its performance falls below the admissible floor. The engineering example shows the complementary case: a small and reusable control-flow correction is retained with little resource growth. Together, these trajectories suggest that RRSI does not simply accumulate edits that improve the evolve-set score, but selectively retains changes whose measured benefit is sufficiently robust relative to their complexity."

| Domain / Round | Harness change | Outcome | What it illustrates |
|---|---|---|---|
| Coding, R0-A | Adds a bounded pre-completion verification audit and guidance for non-blocking polling of long-running jobs. | Accepted: +3.93 points on the evolve set. | A reusable behavioral mechanism can justify a relatively broad early-round update when the gain exceeds the noise threshold. |
| Coding, R0-B | Adds a similar verification reminder and long-running-work guidance, but with a smaller measured gain and additional inference cost. | Rejected by cost rule: +1.69 points, +26.1% cost. | An apparent improvement is not automatically retained when it lies within the noise band and requires substantial additional computation. |
| Coding, R8-B | Pins the original task instruction into the completion gate so that the policy re-checks the literal specification before submission. | Rejected by floor: −2.81 points despite −13.6% cost. | Lower cost alone cannot compensate for a candidate whose performance falls below the noise-adjusted acceptance floor. |
| Engineering, R2 | Adds a bounded recovery hint for the recurring "workdir must be an existing directory" tool-use error. | Accepted: 122/244 → 128/244 passes, +1.6% tokens. | The search can retain small, task-agnostic control-flow fixes that improve reliability with little added complexity. |

Table 6 | Representative harness-evolution decisions from RRSI. The examples show that evolution is not driven by score alone: candidate specificity, evaluation stability, and inference cost jointly determine whether a change is retained.
**Covers:** Final-round selection rule; §D.1 Hyperparameter Setting; §E Qualitative Case Study (Tables 5–6)
