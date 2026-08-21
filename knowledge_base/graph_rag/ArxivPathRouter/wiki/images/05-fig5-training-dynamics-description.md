**Figure 5 — Training dynamics on HotpotQA (Owen 2.5‑B), two panels.**

**Panel (a) "Route category proportions."** A stacked‑area plot with *Route Proportion* (0–1.0) on the y‑axis and *Training Step* (≈0–120) on the x‑axis. The four route categories (legend: C↑P↑, C↑P↓, C↓P↑, C↓P↓) sum to 1.0 at every step. All proportions rise steeply during the first ~10–20 steps and then plateau with minor oscillation. The two "P↑" categories dominate: C↑P↑ (green, bottom band) settles around ~0.5–0.6, and C↓P↑ (blue, large upper band) occupies roughly the 0.6–0.9 range; the two "P↓" categories remain thin slivers near the top. Net effect: routing mass concentrates quickly and stably on the P↑ routes.

**Panel (b) "Training metrics."** Line plot of *Value* (0–1.0) vs. *Training Step* (~0–120) for four quantities: Train F1 (solid teal), Path Overlap (dashed brown), Avg Route Weight (dash‑dot orange), and KL Token Ratio (normalized; dotted purple). Trends:
- *Train F1* climbs sigmoidally from ~0 to ~0.5–0.6 within the first ~30 steps, then drifts slowly higher to a ~0.6 plateau.
- *Path Overlap* rises from ~0 to a low plateau (~0.15–0.2) and stays flat.
- *Avg Route Weight* starts near ~0.9, decays to ~0.7 by step ~20, and holds there with small wiggles.
- *KL Token Ratio* starts near 1.0, drops sharply to ~0.2 by step ~20, and keeps falling toward ~0.05 by the end.

**Takeaway.** The model converges fast: within roughly the first 20–30 training steps the route distribution saturates (dominated by the P↑ categories), task quality (F1) and path overlap reach a plateau, and the regularization‑type signals (KL token ratio) and average route weight decrease and stabilize. Beyond ~30–40 steps there is only slow, marginal improvement—indicating a quick, stable convergence of both routing behavior and performance.