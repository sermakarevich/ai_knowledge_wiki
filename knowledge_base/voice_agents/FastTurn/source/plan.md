# FastTurn — wiki plan

Source: FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection (pdf, https://arxiv.org/abs/2604.01897)

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-fastturn-unifying-acoustic-and-streaming-semanti | 01-overview-and-problem.md | Paper framing: full-duplex turn-taking problem, VAD vs ASR baselines, FastTurn contribution summary |
| 02-arxiv-2604-01897v6-cs-sd-13-jul-2026-modules | 02-architecture-variants.md | FastTurn-Cascaded / Semantic / Unified architecture: CTC streaming, Conformer encoder, LLM adapter, fusion detector |
| 03-asr-data-text-data-asr-data | 03-training-and-test-set.md | Four-stage training pipeline plus FastTurn real-dialogue test set construction and splits |
| 04-capabilities-table-3-shows-results-for | 04-main-results-and-latency.md | Turn-detection accuracy/latency vs baselines across FastTurn, Smart Turn, Easy Turn test sets |
| 05-3-5-asr-results-4-conclusion-this | 05-asr-ablation-and-conclusion.md | ASR decoding results, ablation of semantic/acoustic fusion, conclusions and future work |
