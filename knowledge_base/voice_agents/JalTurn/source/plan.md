# JalTurn — wiki plan

Source: JAL-Turn: Joint Acoustic-Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialog (pdf, https://arxiv.org/abs/2603.26515)

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-jal-turn-joint-acoustic-linguistic-modeling-for | 01-overview-and-problem.md | Paper framing: full-duplex turn-taking problem, acoustic-vs-semantic cue limits, JAL-Turn contribution summary |
| 02-arxiv-2603-26515v1-cs-cl-27-mar-2026-ai | 02-background-and-data-pipeline.md | Motivation plus scalable VAD future-window labeling and context/dataset construction pipeline |
| 03-high-level-semantic-and-linguistic-elements-the | 03-architecture-dual-encoder-and-fusion.md | Dual-encoder design (SenseVoice + CPC), cross-attention fusion, transformer, pooling, classification head |
| 04-4-experiments-4-2-1-comparison-with-slm-based | 04-experiments-slm-and-audio-baselines.md | Experimental setups plus results vs SLM-based and audio-only baselines on Easy-Turn and STurn |
| 05-4-2-3-comparison-with-llm-based-methods-removing | 05-llm-comparison-and-ablations.md | Results vs LLM-based detectors on in-house Japanese corpus plus component ablation studies |
| 06-automatic-extraction-of-reliable-turn-taking-lab | 06-analysis-and-conclusion.md | Encoder/temporal attribution analysis, conclusions, and references |
