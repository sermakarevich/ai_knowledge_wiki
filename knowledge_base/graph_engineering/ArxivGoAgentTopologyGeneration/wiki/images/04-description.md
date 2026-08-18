**Figure 5 — Heatmap of model performance vs. bottleneck hyperparameters (MMLU dataset).**

The figure presents two side‑by‑side 6×6 heatmaps over the same hyperparameter grid: the x‑axis is β_e (edge‑prediction KL strength) and the y‑axis is β_g (group‑prediction KL strength), each spanning roughly 0.0–1.0 (with non‑uniform ticks at 0.0, 0.1, 0.2, 0.3, 0.5, 1.0). Panel (a) reports **Accuracy (%)** (colorbar ≈ 86–90), and panel (b) reports **Token cost in K** (colorbar ≈ 160–220).

**Trends**
- *Accuracy (a):* Relatively flat across the grid, mostly in the high‑80s (≈ 86–90). The leftmost column (β_e ≈ 0) is slightly higher (≈ 88–89), with a gentle decline toward larger β_e and β_g (≈ 86–87). Overall, accuracy is only weakly sensitive to the bottleneck parameters.
- *Token cost (b):* Strong gradient. The lowest β_e (left column) is the most expensive (≈ 210–220 K), and cost steadily **decreases as β_e grows**, reaching the cheapest values (≈ 160–190 K) at moderate/high β_e. Larger β_g also tends to raise cost within a column.

**Takeaway:** There is a clear cost/robustness trade‑off governed by the CIB strength. A too‑weak bottleneck (e.g., β_e ≈ 0) lets historical noise through, inflating token cost, while increasing β_e trims token cost substantially with only minor accuracy change. Accuracy is comparatively stable, so the dominant sensitivity of the model to these hyperparameters is in **token cost**, which can be reduced by raising β_e.