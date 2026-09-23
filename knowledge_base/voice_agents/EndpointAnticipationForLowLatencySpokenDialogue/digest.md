> [[index|Wiki]] | [[summary|Summary]]
# Endpoint Anticipation for Low-Latency Spoken Dialogue — Digest
## 1. [[wiki/01-endpoint-anticipation-for-low-latency-spoken-dia|Endpoint Anticipation for Low-Latency Spoken Dialogue]]
**In one sentence:** The source chunk for this page is truncated/garbled, containing only the paper title, author/affiliation header, and a cut-off fragment of the Abstract, so no substantive claim can be faithfully summarized.
## Key points
- The chunk contains only the paper title "Endpoint Anticipation for Low-Latency Spoken Dialogue" and nothing else substantive.
- The chunk lists authors Sathvik Udupa, Shinji Watanabe, Petr Schwarz, and Jan Cernocky with affiliations Brno University of Technology (Czechia) and Carnegie Mellon University (United States).
- The chunk lists contact emails {udupa, schwarzp, cernocky}@fit.vut.cz and shinjiw@ieee.org.
- The Abstract fragment states only "While low-latency interaction is critical for spoken dialogue," before breaking off.
- A second Abstract fragment mentions "generating initial hypotheses and pre-fetching audio frames during the user's speech" to "'pipeline' ongoing speech," but the sentence is incomplete.
- Because the chunk text ends mid-sentence, no complete argument, method, number, or result can be extracted without inventing content.
## 2. [[wiki/02-arxiv-2606-13450v1-eess-as-11-jun-2026-the|Endpoint Anticipation: method, experiments, and Unmute integration]]
**In one sentence:** The chunk proposes Endpoint Anticipation — proactive speech-only forecasting of end-of-turn up to 2.56 s ahead to enable speculative LLM-TTS execution — with new latency-vs-redundancy metrics, EPA-S/EPA-M models that beat VAP baselines, and a Unmute integration cutting average latency by 505 ms at 28.4% extra compute.
## Key points
- Shifts from reactive endpoint detection to proactive forecasting of end-of-turn (EOT) signals, anticipating endpoints up to 2.56 seconds in advance to speculatively execute LLM and TTS pipelines on partial context.
- Introduces four metrics separating success from waste: Median Realized Anticipation (MRA), Premature Anticipation Rate (PAR), Expected Redundant Computation (ERC), and Horizon Entry Accuracy (HEA).
- Formulates anticipation as independent binary classification over horizons H = {320, 640, …, 2560} ms at 12.5 Hz frame rate, with trigger threshold θ (Eq. 3) tuning latency reduction versus premature predictions.
- Trains two variants — EPA-S (|H| independent single-horizon models) and EPA-M (shared dual-stream backbone with horizon-specific heads) — with comparable accuracy, but EPA-M avoids horizon-specific retraining.
- At h = 640 ms and ≈33% ERC on SpokenWOZ, EPA-M achieves 640 ms MRA and 67.0% HEA versus VAP's 160 ms MRA and 19.2% HEA; at h = 1280 ms and ≈15% ERC, EPA-M achieves 480 ms MRA and 22.1% HEA versus VAP's 80 ms MRA and 7.2% HEA.
- Anticipation is easier on structured task-oriented SpokenWOZ than spontaneous Switchboard conversation, yielding higher MRA at fixed PAR and higher HEA at fixed ERC for both h = 960 ms and h = 2560 ms.
- Unmute integration (EPA-M, h = 960 ms) reduces average latency from 1195 ms to 690 ms (505 ms saving) with 28.4% ERC, masking ASR-LLM-TTS sequential bottlenecks via trigger-fork, pre-synthesis cache, and verification.
## 3. [[wiki/03-2-a-de-fossez-l-mazare-m|References [2]–[33]: speech dialogue, endpointing, and turn-taking bibliography]]
**In one sentence:** This chunk is the references tail [2]–[33], listing cited works on full-duplex speech dialogue systems, endpoint/turn-taking prediction, dialogue benchmarks, and supporting methods.
## Key points
- Entries [2]–[9] cite full-duplex and real-time spoken dialogue systems: Moshi (arXiv:2410.00037, 2024), Interspeech 2025 duplex modeling (pp. 2715–2719), Personaplex (arXiv:2602.06053, 2026), ChipChat (arXiv:2509.00078, 2025), SALMONN-Omni (NeurIPS 2025, arXiv:2505.17060), ICLR 2026 listen/look/speak/act (arXiv:2510.16756), GLM-4-Voice (arXiv:2412.02612, 2024), and F-actor (arXiv:2601.11329, 2026).
- Entries [10]–[13] cite endpointing and turn-taking prediction: grid LSTM endpoint detection (Interspeech 2017, pp. 3812–3816), voice activity projection turn-taking (arXiv:2401.04868, 2024), streaming endpointer with neural audio codecs and label-delayed training (ASRU 2025, arXiv:2506.07081), and Easy Turn acoustic-linguistic turn-taking (arXiv:2509.23938, 2025).
- Entries [14]–[16] cite turn-taking foundations and real-time speech-to-speech work: PNAS vol. 106, no. 26, pp. 10 587–10 592 (2009), Frontiers in Psychology vol. 6, p. 136034 (2015), and Kame tandem architecture (arXiv:2510.02327, 2025).
- Entries [20]–[25] cite predictive recognition, voice activity projection, and streaming dialogue reasoning: predictive ASR and end-of-utterance detection (arXiv:2409.19990, 2024), VAP (Interspeech 2022, pp. 5190–5194), multilingual turn-taking prediction (LREC-COLING 2024, pp. 11 873–11 883), thinking-while-listening speech LLMs (arXiv:2510.07497, 2025), chain-of-thought training for open E2E spoken dialogue (Interspeech 2025, pp. 4833–4837), and Stream RAG with streaming tool usage (arXiv:2510.02044, 2025).
- Entries [26]–[28] cite benchmarks and data: SpokenWOZ (NeurIPS, vol. 36, pp. 39 088–39 118, 2023), Switchboard telephone speech corpus (ICASSP, vol. 1, 1992, pp. 517–520), and Silero VAD (github.com/snakers4/silero-vad, 2024).
- Entries [29]–[33] cite modeling and serving infrastructure: "Attention is all you need" (NeurIPS, vol. 30, 2017), RoFormer / rotary position embedding (Neurocomputing, vol. 568, p. 127063, 2024), streaming sequence-to-sequence learning with delayed streams modeling (arXiv:2509.08753, 2025), PagedAttention (SOSP 2023), and Full-Duplex-Bench (arXiv:2503.04721, 2025).
## The argument in five moves
1. Low-latency spoken dialogue is bottlenecked by reactive endpoint detection that serializes ASR, LLM, and TTS after turn completion, far above human ~250 ms gaps.
2. The paper reframes the problem as proactive speech-only endpoint anticipation over fixed horizons (320–2560 ms), triggering speculative LLM-TTS execution during the user's speech.
3. It formalizes the latency-vs-waste tradeoff with MRA, PAR, ERC, and HEA metrics and a dual-stream EPA-S/EPA-M architecture operating directly on acoustic signal without ASR.
4. Experiments show EPA strongly beats adapted VAP baselines on both structured SpokenWOZ and spontaneous Switchboard, with multi-target EPA-M matching single-target EPA-S while avoiding per-horizon retraining.
5. Integrated into the Unmute cascaded system with trigger-fork, pre-synthesis cache, and verification, EPA-M cuts average latency 1195 ms to 690 ms at 28.4% redundant compute.
6. The bibliography grounds the work in full-duplex dialogue systems, endpointing/turn-taking prediction, SpokenWOZ/Switchboard benchmarks, and streaming Transformer and serving infrastructure.
