> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References Background — Prior Full-Duplex Work [4]–[38] and CPT Data Construction
**In one sentence:** This chunk lists the paper's cited prior work on full-duplex speech-to-speech models, benchmarks, and infrastructure (references [4]–[38]) and specifies the Appendix A.1 CPT pseudo-dialogue data construction procedure.
## Key points
- Reference [4] (Veluri et al., EMNLP 2024, pp. 21390–21402) is cited for synchronous LLMs as full-duplex dialogue agents beyond turn-based interfaces.
- References [5]–[11] cite contemporary full-duplex / omni speech models: duplex listening-while-speaking, Moshi, OmniFlatten, SALMONN-omni, Freeze-Omni, Personaplex, and MiniCPM-o 4.5.
- References [12]–[13] cite commercial realtime APIs (OpenAI Realtime, Google Vertex AI Live), both accessed 2026-08-20.
- References [18]–[20] ground VoiceChat components: Nemotron-Nano-9B-v2-Base (9B), Nemotron streaming ASR (0.6B FastConformer-RNNT, ~530k hours, released March 13, 2026), and V-Model-TTS (anonymous manuscript under review, 2026).
- References [26]–[30] cite evaluation benchmarks: Full-Duplex-Bench (2025), v1.5 (ICASSP 2026, pp. 19447–19451), v3 tool-use under disfluency (arXiv:2604.04847), VoiceBench (TACL 14:378–398), and DuplexCascade (arXiv:2603.09180).
- References [34]–[38] cite serving and measurement infrastructure: PagedAttention (SOSP 2023), Triton Inference Server, FastAPI, TorchAudio-SQUIM, and the Open ASR Leaderboard.
- Appendix A.1 states CPT data is built by segmenting plain-text passages into sentences, alternately assigning them to user and agent, and synthesizing each turn independently with TTS voice-cloning conditioned on two distinct speaker prompts.
- Appendix A.1 states user and agent turns are placed on a shared timeline in dialogue order and concatenated within their respective channels to produce synchronized two-stream audio paired with agent-side text targets for CPT.
---
## Cited full-duplex and omni speech models [4]–[17]
**Covers:** references [4]–[17]

| Ref | Work | Venue / detail in chunk |
|---|---|---|
| [4] | Veluri, Peloquin, Yu, Gong, Gollakota — Beyond turn-based interfaces: Synchronous LLMs as full-duplex dialogue agents | EMNLP 2024, pp. 21390–21402, Miami |
| [5] | Ma et al. — Language model can listen while speaking | AAAI 2025, vol. 39, pp. 24831–24839 |
| [6] | Défossez et al. — Moshi: a speech-text foundation model for real-time dialogue | Kyutai tech report, Sept 2024 |
| [7] | Zhang et al. — OmniFlatten: end-to-end GPT for seamless voice conversation | ACL 2025, pp. 14570–14580, Vienna |
| [8] | Yu et al. — SALMONN-omni | NeurIPS 2025 |
| [9] | Wang et al. — Freeze-Omni with frozen LLM | ICML 2025, vol. 267, pp. 63345–63354 |
| [10] | Roy et al. — Personaplex: voice and role control | ICASSP 2026 |
| [11] | Cui et al. — MiniCPM-o 4.5 | 2026 |
| [14] | Zhang et al. — DuplexSLA | arXiv:2605.20755, 2026 |
| [15] | Chien et al. — MoshiRAG: asynchronous knowledge retrieval | ICML 2026 |
| [16]–[17] | Hu / Casanova et al. — SALM-duplex; Open full-duplex voice agent | arXiv:2505.15670; ASRU 2025 |

## Base models and components [18]–[25]
**Covers:** references [18]–[25]

- [18] NVIDIA Nemotron-Nano-9B-v2-Base: 9B-parameter language model for reasoning and instruction following (Hugging Face, 2025).
- [19] NVIDIA Nemotron streaming ASR: 600M-parameter Cache-Aware FastConformer-RNNT, streaming English ASR trained on "~530k hours of audio", released March 13, 2026.
- [20] V-Model-TTS described verbatim as "A low-latency continuous speech synthesis model for interactive agents, 2026. Anonymous manuscript under review."
- [21]–[25] cite Audio Flamingo 3 (NeurIPS 2025), Gemma 3 Technical Report (arXiv:2503.19786), RVQ-based generative modeling (ICML 2025, pp. 30609–30630), Nemotron Nano 2 hybrid Mamba-Transformer (arXiv:2508.14444), and Nemotron-CC dataset (ACL 2025, pp. 2459–2475).

## Benchmarks, data, and infrastructure [26]–[38]
**Covers:** references [26]–[38]

- Full-Duplex-Bench [26] (ASRU 2025, pp. 1–8) for turn-taking; v1.5 [27] (ICASSP 2026, pp. 19447–19451) for overlap handling; v3 [29] (arXiv:2604.04847) for tool use under disfluency; VoiceBench [28] (TACL 14:378–398).
- DuplexCascade [30] (arXiv:2603.09180): "VAD-free cascaded ASR–LLM–TTS pipeline and micro-turn optimization"; Raon-Speech [31] (arXiv:2605.23912).
- Noise corpora [32]–[33]: ICASSP 2023 Deep Noise Suppression Challenge; DEMAND database (Proc. Meetings on Acoustics 19(1):035081, 2013).
- Serving [34]–[36]: PagedAttention (SOSP 2023); Triton Inference Server; FastAPI. Measurement [37]–[38]: TorchAudio-SQUIM (ICASSP 2023); Open ASR Leaderboard (arXiv:2510.06961).

## Appendix A.1 — CPT data construction
**Covers:** Appendix A, A.1 Data construction

Verbatim mechanism from the chunk:

> "Each plain-text passage is segmented into sentences, which are alternately assigned to the user and agent to form a pseudo-dialogue. The TTS system operates in voice-cloning mode, conditioned on two distinct speaker prompts to maintain a consistent voice for each role. User and agent turns are synthesized independently, placed on a shared timeline in dialogue order, and concatenated within their respective channels. This produces synchronized two-stream audio with separate user and agent speech, which is paired with the agent-side text targets for CPT."

**Covers:** references [4]–[38] (pp. 11–13) and Appendix A.1 CPT Data Construction
