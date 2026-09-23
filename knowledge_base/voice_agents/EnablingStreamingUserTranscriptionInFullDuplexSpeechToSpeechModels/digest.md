> [[index|Wiki]] | [[summary|Summary]]
# Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models — Digest

## 1. [[wiki/01-enabling-streaming-user-transcription|Enabling Streaming User Transcription in Full-Duplex]]
**In one sentence:** The source chunk for this page is truncated (title, authors, and the first two lines of the abstract only), so the full argument cannot be recovered from it.
## Key points
- The chunk contains only the paper title "Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models" and author list (Hu et al., NVIDIA).
- The only body text present is the start of the abstract: "Full-duplex speech-to-speech (S2S) models enable natural conversational AI by allowing simultaneous listening".
- The abstract fragment breaks off mid-sentence at "rather than simultaneous process-", so no complete claim about the method or results is present.
- No mechanisms, numbers, tables, or verbatim complete quotes beyond the fragment above can be extracted from this chunk.
- The planned scope of this page (per plan.md) is the paper framing: the missing-user-transcription problem and the proposed parallel ASR head, but that content is not present in the chunk text provided.

## 2. [[wiki/02-model-architecture-and-streaming-asr-head|Model Architecture and Streaming ASR Head]]
**In one sentence:** The paper adds streaming user transcription to the SALM-Duplex full-duplex S2S architecture via a dedicated parallel ASR head trained jointly with the agent text head using on-the-fly CTC forced alignment and delay tuning.
## Key points
- The backbone combines a 600M-parameter Parakeet streaming speech encoder emitting continuous embeddings at an 80ms frame rate with a 9B-parameter NVIDIA Nemotron-Nano-9B-v2-Base decoder-only LLM.
- Three input streams are processed — user speech, user transcript, and agent text — with user and agent embeddings time-aligned and added before the decoder-only LLM, plus input user speech encoding.
- A dedicated streaming ASR module in parallel to the agent text head adds a separate embedding layer and prediction head initialized from the backbone LLM layers, sharing the same LLM backbone so only a single decoding pass jointly produces user and agent texts.
- Joint training uses multi-channel next-token prediction with equal loss for user and agent text prediction, plus an ASR loss term supervising user transcription alongside agent text loss.
- Frame-level alignment uses on-the-fly torchaudio CTC-based forced alignment with the MMS-FA acoustic model producing word-level timestamps, with left alignment (tokens at word start) outperforming right alignment and `<pad>` tokens filling inter-word frames.
- Two delay hyperparameters trade latency against accuracy: user text delay `du` shifts transcription targets forward in time, and agent text delay `da` helps the agent learn reliable response timing for turn-taking.
- SFT uses a mixture of interleaved S2S data, text-to-text conversations, multi-turn conversational SFT data, multiple-choice QA, single-turn speech instruction data, and 16k hours of English ASR data (LibriSpeech, VoxPopuli, Common Voice, VCTK, SPGISpeech, plus in-house; standalone ASR adds Granary/YODAS/YTC), with background noise augmentation at 0.5 probability from 60,000+ noise files and SNR sampled between -30 dB and 60 dB.

## 3. [[wiki/03-experiments-turn-taking-and-asr-results|Experiments: Turn-Taking and ASR Results]]
**In one sentence:** With `du = 1.2s` and `da = 0.16s`, the duplex S2S model with integrated streaming ASR head achieves 10.21% average WER while keeping turn-taking/barge-in competitive (90% precision, 95% recall, 100% barge-in accuracy) and improving OpenbookQA to 69.01%.
## Key points
- Delay hyperparameters are `du = 1.2s` (user text) and `da = 0.16s` (agent text), chosen "to achieve a balance between reasonable ASR performance and immediate agent response."
- The duplex model with streaming ASR head achieves 10.21% average WER (LS-clean 3.9, LS-other 8.48, SPGI 4.95, Giga 14.22, Earn22 16.87, AMI 18.36, Tedlium 5.98, Voxpop 8.9), beating dedicated streaming models FastConformer-80ms (11.71%) and FastConformer-multi (11.27%).
- On the internal test set, turn-taking is 90% precision / 95% recall at 431ms latency versus baseline (noASR) 86.1% / 96.9% at 410ms, with 100% barge-in accuracy at 374ms latency versus baseline 393ms.
- Intelligence scores (VoiceBench) are OpenbookQA 69.01%, AlpacaEval 3.83/5, CommonEval 3.11/5, versus baseline 66.59%/3.71/3.24, versus Qwen2-Audio 67.91%/4.11/3.77 and Moshi 26.15%/2.01/1.60.
- FDB-v1 shows better smooth turn-taking TOR (96.12% vs. Moshi 94%), worse user-interruption TOR (94% vs. 100%) but far higher interruption GPT score (3.99 vs. 0.77), and fewer pause-handling false takeovers (TOR 44.4% vs. 98%) at the cost of higher smooth-TT latency (477ms vs. 265ms).
- Adding the streaming ASR head "does not significantly change the turn taking results compared to the baseline model (i.e., no ASR)" except increased smooth turn-taking latency on FDB-v1, while OpenbookQA improves from 66.59% to 69.01%, "which indicates that the model may benefit from the text modality to answer questions."
- Standalone streaming ASR (Table V) gives Ours (1.6s) 8.47% average WER, improving to 7.73% with "+ YODAS and YTC", versus Nemotron-Speech-0.6B 7.16%, Qwen3-ASR-1.7B 5.76%, Qwen3-ASR-0.6B 6.42%, and Kyutai STT-2.6B 6.40%.

## 4. [[wiki/04-standalone-asr-conclusions-and-references|Standalone Streaming ASR, Conclusions and References]]
**In one sentence:** The same architecture trained as a standalone streaming ASR model without agent text heads reaches 7.73% average WER on the HuggingFace Open ASR Leaderboard, and the paper concludes that a lightweight parallel ASR head adds real-time user transcription without significantly modifying the base full-duplex S2S model.
## Key points
- A standalone streaming ASR model uses the same architecture but without the agent text heads, focusing solely on streaming speech recognition.
- Table V compares the standalone model against state-of-the-art streaming ASR systems on the HuggingFace Open ASR Leaderboard [34].
- The base model with 1.6s streaming delay achieves 8.47% average WER, improving to 7.73% after adding YODAS and YTC data from Granary [48].
- A latency ablation achieves 7.99% average WER with 1.2s streaming latency, and a smaller Qwen 2.5-1.5B-Instruct [53] backbone achieves 8.64% average WER.
- The remaining gap to Nemotron-Speech-0.6B (7.16% vs 7.73%) is attributed to utilizing only subsets of the Granary dataset, with some portions unavailable in the training pipeline at training time.
- Compared to Qwen3-ASR and Kyutai STT (Table V), the model achieves lower streaming latency at the cost of higher WER, though direct comparison is difficult because training data differs and is not fully disclosed.
- The duplex S2S model with integrated ASR achieves 10.21% average WER while maintaining competitive turn-taking and barge-in performance, enabling conversation logging and accessibility features.

## The argument in five moves
1. Full-duplex S2S models allow simultaneous listening and speaking but lack explicit streaming user transcription, motivating a dedicated transcription channel rather than conflating ASR with reasoning.
2. The paper extends SALM-Duplex (Parakeet streaming encoder plus Nemotron-Nano-9B-v2-Base LLM) with a lightweight parallel streaming ASR head sharing one decoding pass, aligned by on-the-fly CTC forced alignment with left word alignment and `du`/`da` delay tuning.
3. With `du = 1.2s` and `da = 0.16s`, the integrated duplex model reaches 10.21% average WER — beating dedicated FastConformer streaming baselines — while preserving turn-taking and barge-in (90% precision, 95% recall, 100% barge-in accuracy).
4. The ASR head leaves conversational behavior essentially unchanged except higher smooth turn-taking latency on FDB-v1, while improving OpenbookQA (66.59% to 69.01%) and delivering better interruption response quality and pause handling than Moshi at a latency cost.
5. The same architecture as a standalone streaming ASR model reaches 7.73% average WER (8.47% base, plus YODAS/YTC), trading lower latency for higher WER against Qwen3-ASR/Kyutai STT, with the residual gap to Nemotron-Speech-0.6B attributed to partial Granary data.
6. Therefore a minimal parallel ASR head adds real-time user transcription without significantly modifying the base full-duplex S2S model, enabling conversation logging and accessibility features.
