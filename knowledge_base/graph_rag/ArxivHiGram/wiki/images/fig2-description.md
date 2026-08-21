**Figure 2 — Ablation of Memory Organization & Evidence Localization (LoCoMo)**

**What it shows.** A three‑panel ablation comparing three model configurations: the full system (*Ours‑full*), a variant with the MicroGraph memory organization removed (*w/o MicroGraph*), and a variant with the localized support subgraph removed (*w/o Support Subgraph*). The first two panels measure answer quality (F1 and an LLM‑judge score, "LLM‑J") across question types; the third panel measures inference cost in token length.

**Axes.**
- *Panel 1 (F1):* y‑axis ≈ 20–65; x‑axis = Single‑Hop / Multi‑Hop / Temporal.
- *Panel 2 (LLM‑J):* y‑axis ≈ 66–90; x‑axis = same three categories.
- *Panel 3 (Token Length):* y‑axis ≈ 3,000–5,000; x‑axis = Full / w/o MG / w/o SS.

**Trends (approximate values).**
- *Quality (F1, LLM‑J):* The full model is best or near‑best in every category. Removing the **Support Subgraph** hurts most on **Multi‑Hop** F1 (full ≈ 33 vs. ≈ 19), indicating this component is critical for multi‑hop evidence localization; its impact is smaller on Single‑Hop and Temporal. Removing **MicroGraph** costs the most on **Single‑Hop** (F1 ≈ 61→≈ 48; LLM‑J ≈ 88→≈ 84) with a milder effect on Temporal/Multi‑Hop.
- *Cost (Token Length):* The full system is by far the most token‑efficient (≈ 2.9k). Dropping MicroGraph is the most expensive (≈ 4.9k), and dropping the Support Subgraph is intermediate (≈ 3.9k).

**Takeaway.** Both components are load‑bearing: MicroGraph organization primarily drives token efficiency and single‑hop accuracy, while the localized support subgraph is key to multi‑hop reasoning. The full architecture delivers the highest quality at the lowest inference cost, so neither ablation (which trade quality for higher token usage) is preferable.