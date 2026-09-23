[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# ASR Results and Conclusion
**In one sentence:** CTC greedy decoding beats the tested LLM-based autoregressive decoding variants on recognition error rates, and the paper concludes that FastTurn — fast CTC decoding plus integrated acoustic features — delivers low-latency, robust turn detection in full-duplex systems.
## Key points
- CTC greedy decoding achieves 7.06% WER on LibriClean, 9.52% on TestNet, and 2.33% CER on AISHELL-1, the best error rates among the Table 4 rows in this chunk.
- LLM decoding with a 2-layer MLP adapter is the worst in the table: 14.09% on LibriClean, 16.80% on TestNet, and 6.45% on AISHELL-1.
- Replacing the MLP adapter with a 2-layer Transformer adapter improves LLM decoding to 7.19% (LibriClean), 10.74% (TestNet), and 5.31% (AISHELL-1).
- A 4-layer Transformer adapter further improves LLM decoding to 5.56% (LibriClean) and 3.69% (AISHELL-1), with TestNet unchanged at 10.74%.
- The LLM decoding variants in Table 4 differ only in the LLM adapter architecture, per the table caption.
- The conclusion attributes FastTurn's low latency to fast CTC decoding and its robustness to integrating acoustic features.
- The authors release a comprehensive test set capturing realistic interaction dynamics (turn-taking and speech overlap, including echo signals and speech overlap) and propose future work on optimizing performance and extending to more dynamic conversational scenarios.
---
## 3.5. ASR results
Table 4 reports recognition performance on evaluation sets: Chinese CER (%) and English WER (%); for LLM decoding, variants differ only in the LLM adapter architecture.

| Decoding | LLM Adapter | LibriClean | TestNet | AISHELL-1 |
|---|---|---|---|---|
| CTC greedy | – | 7.06 | 9.52 | 2.33 |
| LLM | 2L MLP | 14.09 | 16.80 | 6.45 |
| LLM | 2L Transformer | 7.19 | 10.74 | 5.31 |
| LLM | 4L Transformer | 5.56 | 10.74 | 3.69 |

Chunk text introducing the table: "As shown in Table 4, LLM-based autoregressive decoding" (sentence continues outside this chunk).
## 4. Conclusion
Verbatim conclusion claims in this chunk:
- "This paper presents FastTurn, a framework for efficient turn detection in full-duplex systems."
- "By utilizing fast CTC decoding and integrating acoustic features, FastTurn reduces latency and enhances robustness."
- "We release a comprehensive test set to promote research on conversational turn-taking and speech overlap phenomena, specifically designed to capture realistic interaction dynamics."
- "FastTurn effectively handles complex conversational patterns, such as echo signals and speech overlap, while maintaining high accuracy and low latency."
- "Experimental results demonstrate that FastTurn exhibits strong robustness under challenging acoustic conditions, making it a promising solution for real-time, scalable turn detection."
- "Future work will focus on optimizing the model's performance and extending its application to more dynamic conversational scenarios."
## References in this chunk
The chunk also contains the reference list ([1]–[30]), covering full-duplex dialogue systems, ASR corpora (AISHELL-1/2, WenetSpeech, LibriSpeech, GigaSpeech, MLS), and models (Conformer, Paraformer, CTC, Qwen, DeepSeek, AudioGPT and related dialogue systems); no reference-derived factual claims are added beyond noting their presence.
**Covers:** Section 3.5 (ASR results, Table 4) through Section 4 (Conclusion)
