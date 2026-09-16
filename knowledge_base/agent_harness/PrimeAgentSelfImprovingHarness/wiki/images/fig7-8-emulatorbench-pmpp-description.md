**What the figures show.** The page presents two benchmark comparisons of the *Prime Agent* harness against native harnesses (Codex, Claude Code, Kimi‑Code). Figure 7 reports *EmulatorBench* runs (retro‑hardware emulation in Rust); Figure 8 reports *PMPP‑Hard* GPU‑kernel solve rates under a fixed wall‑clock budget.

**Figure 7 (EmulatorBench).** Two step‑function line plots, one per console — (a) Sega Genesis, (b) Game Boy Color.
- **Axes:** x = estimated cost in dollars (Genesis ≈ $0–$16; GBC ≈ $0–$7); y = stepwise verifier score (0.0–1.0).
- **Encoding:** hue = model (orange = Sol, purple = Opus 5); line style = harness (solid = Prime Agent, dashed/dotted = Codex / Claude Code).
- **Trend:** The Sol‑based harnesses (orange) climb quickly to a high plateau and hold it — roughly a ~0.6 score on Genesis and near ~1.0 on Game Boy Color — at low cost. The Opus‑based harnesses (purple) remain flat at a ~0.0 score across the entire cost range on both consoles.

**Figure 8 (PMPP‑Hard).** Grouped bar charts of GPU‑kernel solve‑rate (%) (y‑axis 0–80), comparing Prime Agent (solid fill) to the native harness (hatched) within each model, at a fixed budget (GPT‑5.6 Sol @ 1500 s; Kimi‑K3 @ 4500 s).
- **Trend:** Prime Agent is close to the native harness in both model groups, with the ordering flipping — Prime Agent is slightly ahead on Sol (~62% vs ~59%) and slightly behind on Kimi (~68% vs ~71%).

**Takeaway.** Harness choice is competitive: Prime Agent matches or exceeds the native harness on PMPP‑Hard at the same budget. On EmulatorBench the *model* dominates the outcome — Sol‑backed runs succeed at low cost while Opus‑backed runs fail entirely (≈0 score) despite comparable spend, indicating the harness does not compensate for a weak model on these long‑context tasks.