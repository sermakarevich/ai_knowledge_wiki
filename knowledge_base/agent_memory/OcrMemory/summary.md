# OCR-Memory: Optical Context Retrieval for Long-Horizon Agent Memory

**Paper:** [OCR-Memory: Optical Context Retrieval for Long-Horizon Agent Memory (Li et al., 2026)](https://arxiv.org/abs/2604.26622)

## Human Readable TL;DR

Imagine an AI assistant that needs to remember everything you've shown it over hundreds of interactions, but its "working memory" can only hold a few pages at a time. Instead of writing notes (which lose detail) or keeping every page open (which fills the memory instantly), OCR-Memory takes a photo of each page and stores it as a highly compressed thumbnail. When it needs something, it scans the thumbnails like a detective looking at a photo wall -- pointing at the relevant spots and reading back the exact original words. This gives the AI near-perfect recall of long histories while barely using any of its limited working memory.

## TL;DR

OCR-Memory proposes storing LLM agent interaction histories as compressed visual images rather than raw text, achieving ~10× token compression while preserving full fidelity. Retrieval uses a *Locate-and-Transcribe* paradigm: a fine-tuned DeepSeek-OCR model scans Set-of-Mark annotated memory images, predicts which segment indices are relevant, then deterministically fetches verbatim text -- achieving 100% retrieval faithfulness and zero hallucination. On Mind2Web and AppWorld long-horizon benchmarks, OCR-Memory achieves state-of-the-art Task Success Rate (4.8% and 58.1% average, respectively), outperforming all text-based memory baselines.

---

## Problem & Motivation

LLM agents operating over extended interactions accumulate trajectories containing reasoning traces, tool calls, and environmental feedback. The finite context window makes it infeasible to store these in full. Existing approaches either:

- **Summarize/abstract** history -- fast but destroys structural, temporal, and procedural details needed for debugging, error analysis, or multi-step planning.
- **Retrieve text chunks** -- token-efficient but similarity matching is brittle; retrieved snippets may be topically related yet logically irrelevant for causal or long-range dependencies.

The key insight: visual tokens can encode dense textual content at far lower context cost than raw text, while preserving full information fidelity.

---

## Main Original Ideas

1. **Visual Memory Bank** -- Store agent trajectories as rendered images using DeepSeek-OCR's optical compression. Interaction logs are rendered into marked images with Set-of-Mark (SoM) bounding boxes and numerical IDs, compressed to as few as 64 latent tokens per frame (vs. thousands for raw text). This decouples storage from the reasoning agent's context window entirely.

2. **Locate-and-Transcribe Retrieval** -- Instead of asking the model to *generate* retrieved text (which hallucinates), the OCR-Memory model acts as a pure *relevance extractor*: it outputs only binary segment indices (0/1 per SoM anchor), and the actual text is fetched deterministically from stored logs. This achieves 100% content-level retrieval faithfulness vs. 84.3% for free-form generative retrieval, and reduces inference latency from 5.3 s to 1.7 s per step.

3. **Multi-Resolution Active Recall** -- Mimics human "vivid-to-fuzzy" memory decay. The 5 most recent interaction steps are stored at high resolution (1024×1024, 256 tokens/frame); all earlier history is downsampled to 512×512 thumbnails (65 tokens/frame). When a low-resolution memory is identified as relevant during retrieval, it is instantly upscaled on-demand to full fidelity before being injected into context. The dynamic strategy matches high-res performance (46.1% Step SR) while consuming only 82 avg tokens/frame vs. 256 for static high-res.

4. **Recall-Biased Fine-tuning on HotpotQA** -- The retrieval backbone (DeepSeek-OCR 3B) is fine-tuned discriminatively on HotpotQA rendered as SoM-annotated images. A weighted BCE loss with w+ > w- (specifically w+/w- = 2.0/1.0) penalizes missed evidence more than false positives. Only the language decoder is updated (LoRA), keeping the visual encoder frozen to preserve optical recognition.

5. **Resolution Curriculum Training** -- To bridge the domain gap between high-fidelity HotpotQA training images and the degraded thumbnails seen at deployment, training randomly samples resolution tiers (Categorical distribution over {1024×1024, 512×512}). This forces the retriever to rely on coarse semantic cues when fine details are unavailable.

---

## Key Findings

| Method | Ele Acc (%) | F1 Score | Step SR (%) | Task SR (%) | AppWorld Avg SR (%) |
|---|---|---|---|---|---|
| Zero-Shot | 40.1 | 46.2 | 37.9 | 2.2 | 41.9 |
| Retrieval (Text-RAG) | 41.3 | 48.2 | 38.9 | 2.7 | 46.2 |
| MemoryBank | 43.8 | 49.5 | 39.2 | 3.3 | 52.1 |
| AWM | 49.1 | 55.7 | 42.6 | 4.3 | 55.0 |
| ACON | 48.2 | 54.1 | 41.4 | 4.1 | 56.2 |
| **OCR-Memory** | **53.8** | **59.2** | **46.1** | **4.8** | **58.1** |

- **Retrieval faithfulness:** OCR-Memory 100% vs. generative variant 84.3% (content-level faithfulness on Mind2Web subset)
- **Retrieval ranking:** Recall@1 = 78.6%, Recall@5 = 93.4%, MRR = 0.84 vs. Dense Text-RAG (52.7%, 74.3%, 0.61)
- **Token efficiency:** 596 reasoning tokens/step vs. 3,980 for Text-RAG -- a **6.7× reduction** -- at the cost of higher disk usage (1.47 MB vs. 18 KB per episode) and retrieval latency (1.7 s vs. 0.3 s)
- **Needle-in-a-Haystack (NIAH):** Retrieval accuracy 98.5% at 4k tokens and 94.1% at 32k, with consistent ~10× compression ratio across all context lengths
- **Backbone generalization:** Gains hold under Qwen3-32B (48.6% Ele Acc, 42.3% Step SR) vs. GPT-4, confirming the advantage is from the memory mechanism, not the backbone
- **SoM ablation:** Removing SoM (text generation variant) drops Step SR from 46.1% to 39.2% and increases latency 3× (1.7 s → 5.3 s)

---

## Suggestions & Future Directions

1. **Reducing training overhead** -- The current framework requires fine-tuning a specialized optical retrieval model; future work could explore training-free visual retrieval approaches.
2. **Reducing storage costs** -- Rendering and storing visual histories consumes substantially more disk space (1.47 MB vs. 18 KB per episode) and imposes an extra vision encoder memory footprint; more efficient visual compression could address this.
3. **Extension to richer modalities** -- Current work encodes text-based interaction logs; extending to native GUI screenshots (visual layouts, icons, spatial structure) could improve retrieval for GUI-heavy tasks.
4. **Embodied and robotic agents** -- The visual memory paradigm could generalize to robotics and embodied settings where observations are already visual.
5. **Eliminating the image-rendering step** -- A direct mapping from raw logs to visual tokens without explicit rendering would reduce computational overhead and latency.

---

## Authors & Institutions

Jinze Li (The University of Hong Kong), Yang Zhang (University of North Texas), Xin Yang (University of Tsukuba), Jiayi Qu (Yonsei University), Jinfeng Xu (The University of Hong Kong), Shuo Yang (The University of Hong Kong), Junhua Ding (University of North Texas), Edith Cheuk-Han Ngai (The University of Hong Kong)

*Accepted to ACL 2026 (Main Conference)*
