[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Standalone Streaming ASR, Conclusions and References
**In one sentence:** The same architecture trained as a standalone streaming ASR model without agent text heads reaches 7.73% average WER on the HuggingFace Open ASR Leaderboard, and the paper concludes that a lightweight parallel ASR head adds real-time user transcription without significantly modifying the base full-duplex S2S model.
## Key points
- A standalone streaming ASR model uses the same architecture but without the agent text heads, focusing solely on streaming speech recognition.
- Table V compares the standalone model against state-of-the-art streaming ASR systems on the HuggingFace Open ASR Leaderboard [34].
- The base model with 1.6s streaming delay achieves 8.47% average WER, improving to 7.73% after adding YODAS and YTC data from Granary [48].
- A latency ablation achieves 7.99% average WER with 1.2s streaming latency, and a smaller Qwen 2.5-1.5B-Instruct [53] backbone achieves 8.64% average WER.
- The remaining gap to Nemotron-Speech-0.6B (7.16% vs 7.73%) is attributed to utilizing only subsets of the Granary dataset, with some portions unavailable in the training pipeline at training time.
- Compared to Qwen3-ASR and Kyutai STT (Table V), the model achieves lower streaming latency at the cost of higher WER, though direct comparison is difficult because training data differs and is not fully disclosed.
- The duplex S2S model with integrated ASR achieves 10.21% average WER while maintaining competitive turn-taking and barge-in performance, enabling conversation logging and accessibility features.
---
## Standalone streaming ASR results
**Covers:** Section C + Table V (HuggingFace Open ASR Leaderboard comparison)

- Setup: "We also train a standalone streaming ASR model using the same architecture but without the agent text heads, focusing solely on the streaming speech recognition task."
- Benchmark: "Table V compares our standalone model against state-of-the-art streaming ASR systems on the HuggingFace Open ASR Leaderboard [34]."
- Results:
  - Base model, 1.6s streaming delay: 8.47% average WER.
  - + YODAS and YTC data from Granary [48]: 7.73% average WER.
  - Latency ablation: 7.99% average WER with 1.2s streaming latency.
  - Smaller backbone Qwen 2.5-1.5B-Instruct [53]: 8.64% average WER.
- Gap analysis:
  - "the remaining gap compared to Nemotron-Speech-0.6B (7.16% vs 7.73%) is likely due to utilizing subsets of the Granary dataset."
  - "at the time of training, some portions of the Granary data were not available in our training pipeline, and we plan to incorporate the full dataset in future work."
  - "Compared to other SOTA models such as Qwen3-ASR and Kyutai STT (Table V), our model achieves a lower streaming latency, though at the cost of higher WER."
  - "A direct comparison is also difficult as the training data of these models differs from ours and is not fully disclosed."

## Conclusions
**Covers:** Section V. Conclusions

- "We presented an efficient method to add streaming ASR capabilities to a full-duplex speech-to-speech model."
- Mechanism: "By introducing a lightweight ASR head in parallel to the agent text head, our approach enables real-time user transcription without significantly modifying the base S2S architecture."
- Integrated result: "The duplex S2S model with integrated ASR achieves 10.21% average WER while maintaining competitive turn-taking, and barge-in performance."
- Applications: "This enables applications such as conversation logging and accessibility features."
- Standalone result restated: "we showed that the same architecture trained as a standalone streaming ASR model achieves 7.73% WER on the HuggingFace Open ASR Leaderboard."

## Generative AI use disclosure and references
**Covers:** Section VI + References [1]–[53]

- "Claude Opus 4.8 and Codex with GPT-5.5 are used to format tables and references and fix grammatical errors throughout all sections of the paper."
- References cited in this chunk: HuggingFace Open ASR Leaderboard [34], Granary [48], Qwen 2.5 [53].
