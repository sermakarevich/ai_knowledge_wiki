**Figure 2 & Figure 3 — Technical Summary**

**What they show.** The two panels evaluate RAG systems on the Natural Questions (NQ) benchmark along two relevance dimensions: **Context Relevance** (Fig. 2) and **Answer Relevance** (Fig. 3). Each panel compares three scoring sources per framework — the LLM‑judge metric **ARES** (blue), the reference metric **RAGAS** (orange), and **Ground Truth** (green) — with vertical error bars on ARES denoting its confidence interval.

**Axes.** The y‑axis is *RAG System Accuracy*, scaled 0.0–1.0. The x‑axis is the *RAG Framework*, organized as a grid of retriever (BM25, OpenAI, ColBERT) × generator (MPT, GPT‑3.5, GPT‑4.0), plus a Facebook RAG baseline.

**Trends.**
- *Monotonic improvement across configurations.* Accuracy is lowest for the BM25 + MPT combination (roughly 0.2–0.4) and rises steadily as both retriever and generator are upgraded, peaking at **ColBERT + GPT‑4.0** (≈0.8–0.9 for ARES/Ground Truth).
- *Retriever matters as much as generator.* At a fixed generator, ColBERT > OpenAI > BM25; at a fixed retriever, GPT‑4.0 > GPT‑3.5 > MPT.
- *ARES tracks Ground Truth closely* in most configurations, with the green and blue markers often overlapping or within ARES's error bars.
- *RAGAS tends to score below Ground Truth*, especially on Context Relevance for BM25 and OpenAI‑MPT setups, indicating it is more conservative/penalizing in those regimes.
- *Confidence intervals* are moderate in width and tighten somewhat as accuracy rises.

**Takeaway.** ARES behaves as a faithful, low‑variance proxy for human ground‑truth relevance judgments, whereas RAGAS systematically under‑scores relative to ground truth. System quality is driven jointly by retrieval and generation, with ColBERT + GPT‑4.0 as the strongest configuration — i.e., relevance accuracy is a function of both the retriever and the LLM, not either alone.