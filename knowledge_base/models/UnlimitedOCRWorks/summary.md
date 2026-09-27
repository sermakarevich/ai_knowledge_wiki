# Unlimited OCR Works

**Paper:** [Unlimited OCR Works: Welcome the Era of One-shot Long-horizon Parsing (Youyang Yin et al., 2026)](https://arxiv.org/abs/2606.23050)

## Human Readable TL;DR

Most reading machines today work like someone who can only copy one page of a book at a time before starting over -- they forget everything between pages and slow down as their notepad fills up. This paper introduces a new way for reading machines to work like a person who can copy an entire book in one sitting, keeping just the immediate context in mind while steadily moving forward without getting slower.

## TL;DR

The paper proposes Unlimited OCR, an end-to-end OCR model that replaces all attention layers in DeepSeek OCR's decoder with Reference Sliding Window Attention (R-SWA), maintaining a constant-size KV cache during decoding instead of the traditional linearly growing cache. This enables one-shot transcription of dozens of document pages within a 32K context window. Unlimited OCR achieves 93.23% on OmniDocBench v1.5 (+6.22 over DeepSeek OCR) and 93.92% on v1.6 (SOTA among end-to-end models), while gaining 12.7% TPS improvement over the baseline.

---

## Problem & Motivation

Current end-to-end OCR models (e.g., DeepSeek OCR) process documents page-by-page in a for-loop, resetting memory at each step. When decoding long sequences, the accumulated KV cache drives up memory consumption and progressively slows generation speed. This is fundamentally at odds with how humans handle long-horizon copying tasks -- we maintain a continuous state where nearby context is fresh and distant outputs fade softly from memory. No existing model can parse even 10 pages in a single forward pass.

---

## Main Original Ideas

1. **Reference Sliding Window Attention (R-SWA)** -- For each generated token, R-SWA attends to all reference tokens (visual tokens + prompt) via a fixed prefix window of size Lm, while limiting output-to-output attention to only the preceding n tokens (n=128 by default) in a causally sliding window. This keeps the KV cache upper-bounded at Lm+n regardless of decoding length, unlike standard MHA where cache grows as Lm+T.

2. **Constant KV cache during decoding** -- Implemented as a FIFO queue with capacity m+n. When a new token is generated, the (m+1)-th token in the queue is evicted. This ensures both computational cost and memory usage do not progressively increase during generation.

3. **DeepEncoder retention for ultra-high compression** -- DeepSeek OCR's encoder achieves 16x token compression (e.g., 1024x1024 PDF image -> 256 visual tokens) via cascading SAM-ViT and CLIP-ViT with token compression at the bridge. Visual tokens undergo no state transitions -- they are encoded once and remain static throughout the entire parsing process.

4. **One-shot multi-page parsing** -- By combining R-SWA's constant cache with DeepEncoder's compression, Unlimited OCR can transcribe dozens of pages in a single 32K forward pass -- 10K visual tokens can decode ~100k+ text tokens.

---

## Key Findings

- **OmniDocBench v1.5:** Unlimited OCR achieves 93.23% overall (+6.22 over DeepSeek OCR). Text edit distance drops from 0.073 to 0.038; formula CDM improves from 83.37 to 92.61; table TEDS from 84.97 to 90.93.

- **OmniDocBench v1.6:** Achieves 93.92% overall, SOTA among end-to-end models (outperforming Qianfan-OCR's 93.90%). Formula CDM: 95.79.

- **Multi-page performance:** At 20 pages, distinct-20 = 98.73%, edit distance = 0.0572. At 40+ pages, distinct-35 = 96.90%, edit distance = 0.1069. Most errors occur at small text in PDFs due to the fixed 1024x1024 "Base" resolution, not R-SWA losing direction.

- **TPS improvement:** 5580 TPS (vs DeepSeek OCR's 4951 TPS at 512 concurrency), a 12.7% speed increase on OmniDocBench. Under theoretical ceiling conditions, at 6144 tokens, Unlimited OCR reaches 7847 TPS while DeepSeek OCR drops to 5822 TPS (35% gap).

- **Subcategory consistency:** Across all 9 document types (PPT, academic paper, book, colorful textbook, exam paper, magazine, newspaper, note, research report), Unlimited OCR consistently beats both DeepSeek OCR and DeepSeek OCR 2 on text edit distance and reading order metrics.

---

## Suggestions & Future Directions

1. Train models with longer context lengths (e.g., 128K) to support prefill of more pages -- currently limited by prefill length as pages accumulate.
2. Build a prefill pool enabling the model to learn to automatically fetch prefill KV chunks, simulating a human flipping through pages for truly unlimited parsing.
3. Extend R-SWA to other reference-based tasks: ASR (audio recording transcription), translation, and other long-horizon dependency modeling tasks.
4. The model currently uses DeepEncoder "Base" mode (1024x1024) -- addressing the small-text degradation in multi-page scenarios is an open challenge.

---

## Authors & Institutions

Youyang Yin, Huanhuan Liu*, YY†, Qunyi Xie, Chaorun Liu, Shiqi Yang, Shaohua Wang, Zhanlong Liu, Hao Zou, Jinyue Chen, Shu Wei, Jingjing Wu, Mingxin Huang, Zhen Wu, Guibin Wang, Tengyu Du, Lei Jia

*All from Baidu Inc.*
