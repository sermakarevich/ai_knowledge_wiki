---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models

### Q1. What problem does this paper address, and why is the source for the framing page limited?

> [!tip]- Answer
> > Full-duplex S2S models allow simultaneous listening and speaking but lack explicit streaming user transcription, which the paper addresses with a dedicated parallel ASR head rather than conflating transcription with reasoning. The framing wiki page is limited because its source chunk contains only the title, authors (Hu et al., NVIDIA), and the first two lines of the abstract before breaking off mid-sentence. See [[wiki/01-enabling-streaming-user-transcription|Enabling Streaming User Transcription in Full-Duplex]].

### Q2. How is the parallel streaming ASR head integrated into the SALM-Duplex backbone?

> [!tip]- Answer
> > The backbone pairs a 600M-parameter Parakeet streaming encoder (80ms frames) with the 9B-parameter Nemotron-Nano-9B-v2-Base decoder-only LLM, fusing time-aligned user and agent embeddings. The ASR module adds a separate embedding layer and prediction head in parallel to the agent text head, initialized from backbone LLM layers and sharing one decoding pass so user transcription and agent text are produced jointly. See [[wiki/02-model-architecture-and-streaming-asr-head|Model Architecture and Streaming ASR Head]].

### Q3. How does on-the-fly forced alignment work, and what do the `du`/`da` delays control?

> [!tip]- Answer
> > During training, a torchaudio CTC forced-alignment API with the MMS-FA acoustic model produces word-level timestamps, with left (word-start) alignment beating right alignment and `<pad>` tokens filling inter-word frames. The user text delay `du` shifts transcription targets forward in time to trade latency against accuracy, while the agent text delay `da` helps the agent learn reliable response timing for turn-taking. See [[wiki/02-model-architecture-and-streaming-asr-head|Model Architecture and Streaming ASR Head]].

### Q4. What streaming ASR accuracy does the integrated duplex model achieve, and how is it configured?

> [!tip]- Answer
> > With `du = 1.2s` and `da = 0.16s`, chosen to balance ASR quality with immediate agent response, the duplex model with integrated ASR head reaches 10.21% average WER across the Open ASR Leaderboard sets (e.g., LS-clean 3.9, AMI 18.36). This beats the dedicated streaming baselines FastConformer-80ms (11.71%) and FastConformer-multi (11.27%) despite simultaneously generating agent responses. See [[wiki/03-experiments-turn-taking-and-asr-results|Experiments: Turn-Taking and ASR Results]].

### Q5. Does adding the streaming ASR head hurt turn-taking, barge-in, or intelligence scores?

> [!tip]- Answer
> > No meaningful degradation: on the internal set the model keeps 90% precision / 95% recall at 431ms latency with 100% barge-in accuracy at 374ms, versus the no-ASR baseline's 86.1% / 96.9% at 410ms and 100% at 393ms. On FDB-v1 it improves smooth turn-taking TOR (96.12% vs. 94% Moshi) and pause handling (44.4% vs. 98% false takeovers) with a far better interruption GPT score (3.99 vs. 0.77), while OpenbookQA rises from 66.59% to 69.01%, suggesting the text modality helps QA. See [[wiki/03-experiments-turn-taking-and-asr-results|Experiments: Turn-Taking and ASR Results]].

### Q6. What does the standalone streaming ASR variant achieve, and what explains its gap to the best baselines?

> [!tip]- Answer
> > The same architecture trained without agent text heads scores 8.47% average WER at 1.6s delay, improving to 7.73% after adding YODAS and YTC data, with ablations of 7.99% at 1.2s latency and 8.64% with a smaller Qwen 2.5-1.5B backbone. The remaining gap to Nemotron-Speech-0.6B (7.16%) is attributed to using only Granary subsets unavailable in full at training time, while Qwen3-ASR and Kyutai STT comparisons are confounded by undisclosed training data and higher latencies. See [[wiki/04-standalone-asr-conclusions-and-references|Standalone Streaming ASR, Conclusions and References]].

### Q7. Evaluation: should a team building an accessible live-captioned voice agent adopt this parallel ASR head?

> [!tip]- Answer
> > Yes, recommend it when the agent already uses a duplex S2S backbone, since it adds real-time user transcription (10.21% WER) with minimal extra parameters and preserved turn-taking/barge-in, directly enabling conversation logging and accessibility features. Require a latency check first, because smooth turn-taking latency rises on FDB-v1 (477ms vs. 265ms Moshi) and standalone WER still trails SOTA systems such as Qwen3-ASR/Kyutai STT despite its lower streaming latency. See [[wiki/04-standalone-asr-conclusions-and-references|Standalone Streaming ASR, Conclusions and References]].
