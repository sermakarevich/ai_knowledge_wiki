**Figure 5 — Technical Summary**

**What it shows.** A two-panel bar chart comparing the rubric-judge performance of three systems — baseline **Codex**, **Codex with an in-context prompt-optimised prompt**, and **Faraday** — on the task of replicating scientific figures. The left panel aggregates mean scores over two splits; the right panel breaks the same comparison out per individual task (a mix of original and counterfactual variants drawn from ten papers).

**Axes and encoding.**
- *Y-axis (both panels):* "Score" (mean rubric score), spanning roughly 0.3–0.95. Bars carry error bars of ±1 SEM.
- *Left panel X-axis:* two groups, **ML (train)** and **AI-for-science (test)**; each group has three bars (Codex solid, prompt-optimised Codex hatched, Faraday green).
- *Right panel X-axis:* individual tasks (e.g., Adams, Autoencoder, Exec-grounded, SQA, Social-influence in the ML/train region; Aurora, CLOUD, Coulomb, Eff-discovery, PINV in the AI-for-science/test region), each shown as a Codex/Faraday pair.

**Trends.**
- In the left panel, Faraday is highest in both splits (≈0.86 on train, ≈0.79 on test), while the two Codex variants are lower and nearly identical to each other (≈0.80 train, ≈0.73 test).
- In the right panel, Faraday is at or above Codex in almost every task, with the advantage widening on several test-split tasks (most pronounced on PINV, where Faraday reaches ≈0.95 vs ≈0.85 for Codex). A few train-split tasks show Codex ahead, but the overall pattern favors Faraday.

**Takeaway.** Automating prompt optimisation does not close the gap: the prompt-optimised Codex performs no meaningfully better than the baseline Codex, leaving Faraday's lead intact. Faraday also generalises well to the counterfactual/innovation tasks (test split), leading in nearly all cases — evidence that its advantage comes from post-training rather than from prompting.