**Figure overview.** The scatter plot, titled *"Cost–Accuracy Trade-off on LongMemEval‑S,"* compares many long‑memory agent frameworks (baselines, light‑blue dots) against the authors' method, **SodaMem** (large dark‑blue dot), on two axes: query cost versus benchmark accuracy. A shaded top‑left region (bounded by dashed lines through SodaMem) is labeled the preferred zone: *high accuracy at low cost*.

**Axes.**
- **X‑axis** — Estimated API cost per question, in USD, on a **log scale**, spanning roughly 10⁻³ to 10⁻¹.
- **Y‑axis** — LongMemEval‑S accuracy, in percent, linear from ~20% to 100%.

**Trends / layout of points.**
- A cluster of low‑cost methods (≲10⁻³ USD) achieves only mid‑range accuracy (~35–80%): e.g., MemU, A MEM, Zep, Memobase, MemOS variants.
- SodaMem sits at the top of the low‑cost side: ~90+% accuracy at a cost on the order of 10⁻³–10⁻² USD, placing it inside the shaded "better cost & accuracy" region.
- A second group of high‑cost methods (10⁻²–10⁻¹ USD) reaches comparable or only marginally higher accuracy (~82–98%) — e.g., Cersei Embed/Hybrid, AgentOS, LCGraph, EmergenceMem, Mem0 (2026i), agentmemory V4 — i.e., they spend ~10–100× more for little or no accuracy gain.
- Some mid‑cost systems land in the low‑accuracy band (MemoryOS, Fact‑Mem0 read, MemoryBank), showing cost alone does not guarantee accuracy.

**Takeaway.** SodaMem delivers near‑state‑of‑the‑art LongMemEval‑S accuracy at a fraction of the per‑query cost of the strongest baselines, occupying the favorable high‑accuracy / low‑cost corner of the trade‑off curve; pushing cost higher beyond its point buys, at best, only marginal accuracy improvement. (All values read off the plot are approximate.)