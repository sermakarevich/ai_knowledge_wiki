**Figure 1 — two-panel result plot for Meta‑Harness.**

**Left panel — "Harness Optimizer Search Progress."**
- *Axes:* Y = best performance (%) (≈30–55); X = number of harness evaluations (0–40).
- *Curves:* Meta‑Harness (red), TTD‑Discover, OpenEvolve, ACE, plus reference lines for few‑shot and zero‑shot baselines near the bottom.
- *Trend:* Meta‑Harness climbs sharply within the first handful of evaluations to the top of the chart (≈50–55%) and plateaus there. The existing optimizers (TTD‑Discover, OpenEvolve) rise more slowly to a lower ceiling (≈45%), and ACE stays lowest of the learned methods (≈40%), only slightly above the zero/few‑shot references.
- *Meaning:* on text classification, Meta‑Harness reaches the best prior method's *final* accuracy after only a few evaluations, i.e., it finds a strong harness much faster than hand‑designed (ACE) or existing text‑optimizing methods.

**Right panel — "TerminalBench‑2 Harness Performance."**
- *Axes:* Y = pass rate (%) (≈20–40); X = harness name (categorical).
- *Bars:* Meta‑Harness (ours, red) is the tallest (≈38%), followed by the human‑written harnesses Goose (≈35%), Terminal‑KIRA (≈33%), Mini‑SWE‑Agent (≈30%), Terminal‑2 (≈28%), Claude Code (≈27%). Legend distinguishes human‑written (blue) vs. model‑optimized (ours, red).
- *Trend:* a single descending ladder with the model‑optimized harness on top.
- *Meaning:* on agentic coding, the discovered harness beats every reported Claude Haiku‑based human‑written harness.

**Overall takeaway:** giving the optimizer richer access to prior experience (source code, scores, execution traces) yields automated harness engineering that (i) matches the best final accuracy of prior optimizers in a fraction of the evaluations and (ii) surpasses hand‑engineered baselines on agentic coding — i.e., the harness, not just the model weights, is a lever that can be optimized automatically.