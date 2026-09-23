> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix — Corpus Statistics
**In one sentence:** The appendix consolidates MSI-Bench's corpus, cloned-voice pool, and audio-asset counts, Mandarin-split metrics, overlay-SNR behavior composition, and the exact compute/serving configuration used for evaluation.
## Key points
- The corpus has 576 two-speaker cases (288 + 288) and 576 three-speaker cases (288 + 288), with 6–12 visible dialogue lines per case.
- The cloned voice pool totals 96 voices (48 + 48): 48 female and 48 male; by age, 16 teen, 48 young adult, 26 middle-aged, and 6 senior.
- Base assets comprise 8,849 base dialogue clips totaling 23.15 h, 10,408 rendered artifacts in 24 kHz PCM16 WAV format, and 74 background assets.
- Speaker voices are cloned from CC0 Common Voice 17.0 reference clips with planner-assigned gender and age buckets; the Mandarin split has no senior-tagged voice because Common Voice 17.0 contributes no qualifying Mandarin reference clip in that age band.
- Speak-time probes add one injected-utterance clip per case, while hear-time probes cover the two patterns scored by PRR (selective disclosure and background speech retrieval) and reference the base line audio, adding no files of their own.
- Figure 6 pools background-speech-retrieval responses over three configurations (n = 288 per bar): as overlay SNR gets harder, capture falls and both failure modes grow, with answers reporting the salient foreground fact instead of the overheard one rising from 6.9% at +8 dB to 18.4% at −8 dB.
- All open-weight configurations run on one server with eight NVIDIA A100-SXM4-40GB GPUs, two Intel Xeon Platinum 8352Y CPUs (64 physical cores, 128 threads), 1 TiB memory, Ubuntu 22.04.3 LTS (kernel 5.15, driver 535.183.01), served as OpenAI-compatible `vllm serve` endpoints from pinned Docker images via Slurm and enroot.
---
## A — Dataset statistics
**Covers:** Appendix A / Table 3: corpus, voice, and audio statistics.

Table 3 as given in the chunk:

| Item | Numbers as printed |
|---|---|
| Two-speaker cases | 288, 288, 576 |
| Three-speaker cases | 288, 288, 576 |
| Visible dialogue lines | 6–12 |
| Cloned voices | 48, 48, 96 |
| Female | 24, 24, 48 |
| Male | 24, 24, 48 |
| Teen | 8, 8, 16 |
| Young adult | 22, 26, 48 |
| Middle-aged | 12, 14, 26 |
| Senior | 6, 0, 6 |
| Base dialogue clips | 8,849 |
| Duration | 23.15 h |
| Rendered artifacts | 10,408 |
| Format | 24 kHz, PCM16 WAV |
| Background assets | 74 |

Verbatim mechanisms from the chunk:
- "Speaker voices are cloned from CC0 Common Voice 17.0 reference clips, and the planner assigns each speaker a gender and an age bucket that select the pool a line is rendered from; the Mandarin split has no senior-tagged voice because Common Voice 17.0 contributes no qualifying Mandarin reference clip in that age band."
- "Speak-time probes add one injected-utterance clip per case; hear-time probes cover the two patterns scored by PRR (selective disclosure and background speech retrieval) and reference the base line audio, adding no files of their own."

## B — Mandarin results
**Covers:** Appendix B / Table 4: Mandarin split under APR, ARS, tool execution, BIR, and PRR.

- "Table 4 reports the Mandarin split under the metrics defined in the main paper: APR, ARS, tool execution, bystander interference robustness (BIR), and premature response rate (PRR)."
- Selected rows as printed (APR / ARS / Tool / BIR / PRR): Gemini 3.1 Pro 52.8 / 69.9 / 58.8 / 74.6 / 32.5; GPT Realtime 2.1 (xhigh) 54.5 / 76.4 / 54.1 / – / 37.8; GPT Audio 1.5 42.5 / 59.6 / 51.0 / 53.3 / 70.2; Qwen3-Omni-30B 19.3 / 41.8 / 26.3 / 43.3 / 99.5; Gemma 4-12B 4.5 / 28.3 / 0.0 / 60.0 / 92.6; Qwen2-Audio-7B 0.5 / 12.4 / 0.0 / – / 0.0.
- "Dashes mark configurations for which the mid-answer probe could not be run, or which never produced a valid prediction."
- "Open-weight models use the same schema-constrained decoding as in the main paper; as there, Qwen2-Audio-7B's PRR is not highlighted because it reflects near-total silence."

## C — Overlay-SNR behavior composition
**Covers:** Appendix C / Figure 6: four-way behavior composition per overlay-SNR level.

- "Figure 6 decomposes every judged background speech retrieval response into the four exclusive behaviors defined in the main paper, pooled over the three configurations (n = 288 per bar)."
- "As the overlay becomes harder to hear, capture falls and both failure modes grow, but they grow differently: the share answered with the salient foreground fact rather than the overheard one rises from 6.9% at +8 dB to 18.4% at −8 dB, so models do not merely miss more, they increasingly report the wrong, louder fact."
- Figure caption as printed: "Four-way behavior composition per overlay-SNR level, over all cases and pooled over Gemini 3.1 Pro, GPT Audio 1.5, and GPT Realtime 2.1 (medium)."

## D — Computing infrastructure
**Covers:** Appendix D / Table 5: hardware, serving builds, and harness.

- "All open-weight configurations are evaluated on a single server with eight NVIDIA A100-SXM4-40GB GPUs, two Intel Xeon Platinum 8352Y CPUs (64 physical cores, 128 threads), and 1 TiB of system memory, running Ubuntu 22.04.3 LTS (Linux kernel 5.15, NVIDIA driver 535.183.01)."
- "Each model is served as an OpenAI-compatible vllm serve endpoint (Python 3.12 inside the container) from a pinned Docker image executed through Slurm and enroot, so a serving configuration is fully determined by its image tag."
- "Gemma 4-12B requires a Transformers version that recognizes its checkpoint architecture and is therefore served from a pinned vLLM source build (commit f52870f26); its endpoint raises the audio multimodal limit to 12 clips per request, the maximum clip count in the benchmark."
- "Gemma 4-12B and MiMo-Audio-7B serve one checkpoint for both thinking variants, with thinking toggled per request through chat_template_kwargs.enable_thinking."
- Table 5 as printed (Model / vLLM build / TP): Qwen3-Omni-30B / 0.19.0+cu130 / 2; Gemma 4-12B / source build f52870f26 / 1; MiMo-Audio-7B / 0.18.0 / 1; Qwen2.5-Omni-7B / 0.19.0+cu130 / 1; Phi-4-Multimodal / 0.19.0+cu130 / 1; Qwen2-Audio-7B / 0.19.0+cu130 / 1.
- "Hosted systems and the DeepSeek V4 Pro judge are accessed through their public APIs. The evaluation harness runs on the same server under Python 3.11 with locked dependencies and issues all model and judge requests through OpenAI-compatible clients."
