> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Model Architecture and Streaming ASR Head
**In one sentence:** The paper adds streaming user transcription to the SALM-Duplex full-duplex S2S architecture via a dedicated parallel ASR head trained jointly with the agent text head using on-the-fly CTC forced alignment and delay tuning.
## Key points
- The backbone combines a 600M-parameter Parakeet streaming speech encoder emitting continuous embeddings at an 80ms frame rate with a 9B-parameter NVIDIA Nemotron-Nano-9B-v2-Base decoder-only LLM.
- Three input streams are processed — user speech, user transcript, and agent text — with user and agent embeddings time-aligned and added before the decoder-only LLM, plus input user speech encoding.
- A dedicated streaming ASR module in parallel to the agent text head adds a separate embedding layer and prediction head initialized from the backbone LLM layers, sharing the same LLM backbone so only a single decoding pass jointly produces user and agent texts.
- Joint training uses multi-channel next-token prediction with equal loss for user and agent text prediction, plus an ASR loss term supervising user transcription alongside agent text loss.
- Frame-level alignment uses on-the-fly torchaudio CTC-based forced alignment with the MMS-FA acoustic model producing word-level timestamps, with left alignment (tokens at word start) outperforming right alignment and `<pad>` tokens filling inter-word frames.
- Two delay hyperparameters trade latency against accuracy: user text delay `du` shifts transcription targets forward in time, and agent text delay `da` helps the agent learn reliable response timing for turn-taking.
- SFT uses a mixture of interleaved S2S data, text-to-text conversations, multi-turn conversational SFT data, multiple-choice QA, single-turn speech instruction data, and 16k hours of English ASR data (LibriSpeech, VoxPopuli, Common Voice, VCTK, SPGISpeech, plus in-house; standalone ASR adds Granary/YODAS/YTC), with background noise augmentation at 0.5 probability from 60,000+ noise files and SNR sampled between -30 dB and 60 dB.
---
## Related work context
Prior streaming ASR systems (FastConformer, Parakeet, Kyutai STT, Qwen-ASR) achieve strong recognition but are encoder/chunk-based or lack conversational full-duplex integration, while full-duplex dialogue models (Moshi, PersonaPlex, SyncLLM, OmniFlatten, Freeze-Omni, FireRedChat, FlexDuo, SALM-Duplex) enable simultaneous listening/speaking but lack explicit streaming user transcription or rely on external VAD/turn detection rather than truly simultaneous processing.

Verbatim: Moshi [27] and PersonaPlex [28] "jointly model both user and agent audio streams" but "require extensive speech-text pretraining from scratch and do not provide streaming user transcription capabilities."

Verbatim on prior transcription approach: interleaving ASR and reasoning tokens in "a single text monologue stream [31]" "conflates transcription and reasoning into a shared channel rather than treating ASR as a dedicated output."

## Full-duplex S2S backbone
As shown in Fig. 1, the extended model processes user speech, user transcript, and agent text; generated user and agent text tokens are autoregressively fed back as inputs to the backbone LLM.

| Component | Specification from chunk |
|---|---|
| Speech encoder | 600M-parameter Parakeet streaming encoder, 80ms frame rate |
| Backbone LLM | NVIDIA Nemotron-Nano-9B-v2-Base, 9B decoder-only, for reasoning and instruction-following |
| Fusion | User and agent embeddings time-aligned and added, plus user speech encoding |
| Agent output path | Agent text with turn-taking info fed to streaming TTS [41] to generate agent speech |
| Training stages | Pretraining on interleaved speech-to-text conversation data, then SFT on diverse mixture |

Agent text is predicted without word-level alignment "to give the user a preview of the agent response before speech generation finishes."

## Streaming ASR head
The ASR head takes the LLM hidden states and predicts user transcription tokens in a streaming fashion, with a separate embedding layer so user text representations are learned independently from agent text embeddings; this enables real-time recognition concurrent with agent response generation while leveraging conversational context from the shared backbone.

For the standalone streaming ASR configuration, the model is trained without the agent text heads, focusing solely on streaming speech recognition.

Main contributions quoted from chunk:
- "We propose an efficient method to add streaming ASR capabilities to a full-duplex S2S model, requiring minimal additional parameters while preserving turn-taking and barge-in performance."
- "We demonstrate that the S2S model achieves streaming ASR capability, enabling real-time user transcription alongside agent response generation."

## On-the-fly (OTF) forced alignment
Alignment pipeline: torchaudio CTC-based forced alignment API with MMS-FA acoustic model [42] runs during training on user audio plus transcripts, producing word-level timestamps used to align text tokens with speech frames at the start of each word.

| Choice | Result stated in chunk |
|---|---|
| Left vs right word alignment | Left alignment (start of word) yields better performance, "presumably because speech onset is easier to detect in this setup" |
| Inter-word frames | `<pad>` tokens fill frames with no text prediction; example "hello world" becomes "_hel lo <pad> <pad> _world <pad> <pad>" (underscore denotes word boundaries) |
| End-of-word token experiment | Tried a distinct end-of-word token instead of pad at word boundaries, "but did not observe a significant difference in performance" |
| Delays | `du` (user text delay) and `da` (agent text delay) control trade-off between streaming ASR latency and turn-taking accuracy |

## Training data (Experiments §IV.A, partial in this chunk)
Pretraining learns user/agent conversation fundamentals from interleaved speech-to-text data; SFT mixes interleaved S2S data, text-to-text conversations (to maintain language modeling), multi-turn conversational SFT data synthesized per [32], multiple-choice QA, single-turn speech instruction data, and ASR training data; noise augmentation applies in SFT only.

Evaluation sets named in chunk: streaming ASR benchmarks from HuggingFace Open ASR Leaderboard [34] including LibriSpeech test-clean and test-other, SPGISpeech, GigaSpeech, Earnings22, AMI, TED-LIUM, and VoxPopuli; conversational evaluation uses Full-Duplex-Bench V1 (FDB-v1) [49] plus an internal set of ~60 multi-turn real-world interactions (~4 turns each, varied acoustic environments/devices/headsets, scripts generated by a text LLM then recorded with natural pauses).

**Covers:** §I tail (contributions) through §II Related Work, §III.A–C Model Architecture (backbone, ASR head, OTF alignment), and §IV.A Data (training mixture and eval sets); Table I header begins but results are in chunk 03.
