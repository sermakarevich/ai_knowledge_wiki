# Wiki plan — AVTR-1: Open Stack for Real-Time Interactive Avatars

Source: `source/source.md` (local copy of http://arxiv.org/abs/2609.22913v1; PDF not copied, 3.5 MB > 2 MB limit).
Target wiki pages live in `wiki/`.

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-avtr-1-o-pen-s-tack-for | 01-avtr-1-overview-and-introduction.md | Covers paper framing, contributions, and the interactive-avatar problem statement. |
| 02-motion-parameters-liveportrait-implements-this-d | 02-motion-representation-and-model-architecture.md | Covers the LivePortrait motion representation and the flow-matching Transformer architecture. |
| 03-speaker-separation-the-source-audio-contains | 03-data-pipeline-and-training-procedure.md | Covers the dyadic data pipeline, speaker separation, and the training procedure. |
| 04-self-distillation-adapting-a-pretrained-bidirect | 04-chunk-based-audio-encoder-and-distillation.md | Covers the streaming chunk-based HuBERT audio encoder via self-distillation. |
| 05-streamer-stream-clock-avatar-speech-conversation | 05-streamer-architecture-and-stream-clock.md | Covers the streamer serving architecture, worklets, and the shared stream clock. |
| 06-rendering-worklet-the-rendering-worklet-generate | 06-renderer-and-rendering-worklet.md | Covers the renderer inference component and the rendering worklet loop. |
| 07-short-the-scheduler-then-blocks-until | 07-speech-schedulers-and-latency-model.md | Covers speech schedulers and the response/interruption latency analysis. |
| 08-protocol-we-evaluate-on-184-speaker-listener | 08-evaluation-protocol-and-r-dgg-metric.md | Covers the evaluation protocol and the Reference-Based Directed Granger Gain metric. |
| 09-quantitative-comparisons-are-presented-in-tables | 09-quantitative-results.md | Covers quantitative comparisons on visual quality, lip sync, and listening motion. |
| 10-17-zexu-pan-gordon-wichern-yoshiki | 10-references-and-further-reading.md | Covers cited references and pointers for further reading. |
| 11-table-9-conventional-motion-based-metrics-comput | 11-appendix-additional-evaluation.md | Covers appendix tables and additional evaluation details. |
