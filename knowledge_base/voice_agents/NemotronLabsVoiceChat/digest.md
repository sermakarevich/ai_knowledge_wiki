> [[index|Wiki]] | [[summary|Summary]]

# NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities — Digest

## 1. [[wiki/01-overview-architecture|Overview and Full-Duplex Architecture]]

**In one sentence:** NemotronLabs VoiceChat is an open unified streaming speech-to-speech model that listens, transcribes, reasons, invokes tools, and speaks concurrently via a streaming encoder, decoder-only LM with parallel agent-text and tool-call heads, an auxiliary RNN-T transcription branch, and a streaming TTS/codec decoder.

## Key points

- Unified streaming architecture combines a streaming speech encoder, a decoder-only language model, parallel specialized output streams for agent text and structured function calls, an auxiliary RNN-T branch for incremental user transcription, and a streaming TTS decoder.
- Parallel specialized streams for agent text and tool calls preserve low-latency full-duplex behavior, unlike DuplexSLA which serializes heterogeneous action-related tokens within a shared autoregressive channel.
- On Full-Duplex-Bench 1.0, the model achieves the lowest pause-handling takeover rates among evaluated open-weight systems, 100% takeover following user interruptions, and a 4.33/5 post-interruption response-quality score.
- On Full-Duplex-Bench 1.5, it resumes its response after user backchannels in 93% of cases.
- On VoiceBench it obtains a 55.1 normalized average, and on Full-Duplex-Bench 3.0 (FDB 3.0) it achieves 82.5% tool-selection F1, while argument accuracy and end-to-end tool execution remain areas for improvement.
- Motivation is the gap between half-duplex cascaded ASR + LLM + TTS stacks gated by voice-activity detection and human full-duplex dialogue with fine-grained turn-taking, backchannels, overlap, hesitation, and interruption.
- Open checkpoint is available on Huggingface; paper is arXiv:2609.21967v1 [cs.CL] 18 Sep 2026, NVIDIA, © 2026 NVIDIA.

## 2. [[wiki/02-speech-to-text|2.1. Speech-to-Text (STT) — The STT Component]]

**In one sentence:** The STT component pairs a causal streaming perception module with the NVIDIA Nemotron-Nano-9B-v2-Base LLM to predict agent-text and function-call outputs on a shared 80-ms timeline, while an auxiliary RNN-T branch on the same encoder states produces incremental user transcription without feeding the LLM.

## Key points

- Architecture is a perception module plus a decoder-only LLM (NVIDIA Nemotron-Nano-9B-v2-Base), following the architecture in [16, 17]; the perception module encodes streaming user speech and the LLM predicts agent-text and function-call outputs.
- Audio front end converts 16-kHz user waveform into 128-bin log-Mel features using a 25-ms Hann window and 10-ms stride.
- Streaming encoder is 600M parameters with 24 cache-aware FastConformer layers and hidden dimension 1,024; causal depthwise-striding subsampling reduces the sequence by 8x, producing one encoder state every 80 ms.
- Streaming is strictly causal: self-attention uses a 70-frame left context and no right context, and convolutional modules are also causal, so no future audio is required for the current state.
- The perception module is run once and exposes two representations: raw FastConformer states go to the auxiliary RNN-T branch, while an identity modality adapter and projection map the same 1,024-dimensional states into the LLM hidden dimension, avoiding a second ASR encoder and keeping transcription synchronized with response context.
- Frame-level turn-taking supervision uses ordinary agent-text BOS/EOS tokens on the 80-ms timeline: BOS at response onset, response subwords in consecutive frames, EOS as stop target after a brief overlap when a subsequent user turn begins (no EOS for a final agent turn), padding elsewhere; BOS = begin, EOS = stop, padding = remain silent.
- Auxiliary RNN-T (two-layer 640-dimensional recurrent prediction network + 640-dimensional joint network, 1,024-unit BPE vocabulary plus blank, decoded incrementally) is exposed as an auxiliary output rather than fed into the LLM, preserving a direct speech-conditioned response path.

## 3. [[wiki/03-training-recipes|Component-wise training. The full-duplex STT backbone]]

**In one sentence:** The full-duplex STT backbone and streaming TTS model are trained independently with audio-codec prediction disabled, then a frozen-encoder RNN-T transcription branch is attached, using weighted agent-text/function-channel losses plus inference-time filler, endpointing, and runtime enhancements.

## Key points

- Full-duplex backbone and streaming TTS model are trained independently: direct audio-codec prediction is disabled in CPT/SFT (audio-loss weight 0.0) and agent speech is synthesized by the separately trained VoiceChat-TTS decoder, so no gradients flow between backbone and TTS.
- After backbone training, RNN-T prediction (decoder) and joint networks are attached to the shared cache-aware streaming speech encoder; the speech encoder, LLM backbone, agent-text head, function head, and TTS model are frozen and only the RNN-T prediction and joint networks are optimized with standard transducer loss for user transcription.
- STT loss is `ℒSTT = (1 − λT2T)(λtext ℒtext + λFC ℒFC) + λT2T ℒT2T`: SFT uses λtext = 1.0, λFC = 1.0, λT2T = 0.5 (ℒSTT = 0.5(ℒtext + ℒFC) + 0.5ℒT2T); CPT uses λtext = 3.0, λFC = 1.0, λT2T = 0.0 (ℒCPT = 3ℒtext + ℒFC), with the CPT function channel supervised to predict padding despite no tool-calling examples.
- Token-weighted cross-entropy uses SFT agent-text weights 12.5 (beginning-of-turn), 7.5 (end-of-turn), 5.0 (text content), 1.0 (padding) and CPT weights 10.0, 10.0, 1.0, 0.5; function-channel SFT weights are 64.0 (`<TOOLCALL>` content), 6.0 each (`<SOTC>`, `<EOTC>`), 3.0 (`<EOTR>`), 0.3 (padding), with the function mask zero on injected tool-response tokens.
- Optimization runs on 64 GPUs (8 nodes × 8 GPUs) with full data parallelism and bf16 precision, AdamW (β1 = 0.9, β2 = 0.98, zero weight decay), learning rate 5 × 10⁻⁵ with inverse-square-root schedule, 2,500 warmup steps, minimum 5 × 10⁻⁶, and gradient clipping 2.0 (CPT) / 5.0 (SFT).
- Inference-time enhancements in the chunk are per-tool filler messages that mask tool latency, an RNN-T-transcript endpointing fallback that force-injects BOS/EOS tokens for turn start/barge-in stop, and an optimized low-latency real-time inference runtime (details in Appendix B).
- On Full-Duplex-Bench 1.0 the chunk's Table 1 / text reports V-Model at 15.3% synthetic and 25.5% CANDOR pause TOR, 81.5% smooth-turn TOR (448 ms latency), 100% user-interruption TOR (480 ms latency) with 4.33/5 GPT-4o response quality; on FDB 1.5 user-backchannel it reports 93% Resume vs 80% Freeze-Omni and 70% GPT-4o Realtime.

## 4. [[wiki/04-backchannel-evaluation|Respond Resume Uncertain Unknown Model (↓)]]

**In one sentence:** Among open full-duplex models V-Model ties Freeze-Omni on VoiceBench (55.1 vs 55.2) with strong knowledge-task gains but weaker open-ended/IFEval scores, and it leads open models on FDB 3.0 tool-selection F1 (82.5%) while trailing on argument accuracy and Pass@1, within a design whose limitations include a ~2-minute audio context window and imperfect multi-tool use.

## Key points

- V-Model obtains a normalized VoiceBench average of 55.1, improving over Moshi by 25.6 points and PersonaPlex by 24.5 points, and effectively tying Freeze-Omni at 55.2.
- Relative to Freeze-Omni, V-Model scores substantially higher on OpenBookQA (61.3 vs 31.0), MMSU (46.1 vs 28.1), and AdvBench safety (100.0 vs 97.3), offset by weaker SD-QA, open-ended response-quality subsets, and IFEval.
- The cascaded DuplexCascade system averages 65.4 while omni-modal MiniCPM-o 4.5 averages 76.1 in the independent Raon-Speech evaluation with a different judge, serving only as a system-level reference across full-duplex design choices.
- On FDB 3.0 spoken tool use with disfluent human speech and chained API calls, the model achieves 82.5% tool-selection F1, outperforming Gemini Live 2.5 (78.6%) and Gemini Live 3.1 (81.7%).
- Argument accuracy (42.2%) and Pass@1 (33.0%) trail both Gemini Live baselines, and because Pass@1 requires exactly the expected tools with perfect arguments, the gap shows routing is stronger than argument extraction and end-to-end execution.
- The model uses parallel specialized streams for agent text, function calls, and user transcription plus a streaming TTS decoder and an RNN-T branch sharing the speech encoder, enabling continuous listen/speak/transcribe/tool-invoke behavior.
- Limitations include at most ~2-minute audio context windows, degraded tool use with many tools (recommendation: no more than five per session), unreliable simultaneous multi-tool invocation, invented arguments, answering from internal knowledge instead of invoking tools, delayed speech after long tool responses, no barge-in during tool execution, and limited robustness in noisy/reverberant conditions with competing speech.

## 5. [[wiki/05-references-background|References Background — Prior Full-Duplex Work [4]–[38] and CPT Data Construction]]

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

## 6. [[wiki/06-sft-data-construction|SFT Data Construction. Like the CPT]]

**In one sentence:** Like CPT, the SFT stage builds its corpora by rendering text turns into speech with TTS onto a two-channel duplex timeline, retaining a large share of pretraining-style data while adding conversational, instruction-tuning, tool-calling, and text-only knowledge buckets plus online full-duplex augmentations.

## Key points

- SFT renders text turns into speech with TTS and assembles them onto a two-channel duplex timeline with user and agent on separate channels and realistic inter-turn timing.
- CPT trains almost entirely on TTS-rendered pretraining data, while SFT retains a large share of it and adds instruction-tuning, conversational, and tool-calling corpora.
- The extract-knowledge pretraining subset is kept in text form, contributing a text-to-text loss at weight 0.5 in SFT versus 0 in CPT, preserving text-domain competence.
- Tool-calling data is the exception: text tool-calling transcripts contain URLs, markdown, and code with no spoken realization and train poorly on tool relevance, so it is built by a multi-agent pipeline instead of TTS rendering.
- SFT raw sampler weights sum to 1.175 (retention 0.55, conversational 0.28, tool calling 0.305, safety 0.04), normalizing to ~46.8%, ~23.8%, ~26.0%, and ~3.4%.
- SFT adds three online dialogue transformations: early interruption (p = 0.1, truncate mid-utterance + 8 frames / 640 ms overlap), backchannel injection (p = 0.05 per sample, 0.5 per agent turn, loudness-matched), and text-channel delay (agent text targets shifted 2 frames / 160 ms; function channel unshifted).
- Acoustic robustness is raised in the same pass: additive DNS5 and DEMAND noise probability goes from p = 0.1 in CPT to p = 0.5 in SFT at SNR −30 to 60 dB, plus room impulse responses (p = 0.8), microphone impulse responses (p = 0.6), and codec augmentation (p = 0.1), all disabled in CPT.

## 7. [[wiki/07-tts-decoder-evaluation|We evaluate the VoiceChat-TTS speech decoder]]

**In one sentence:** VoiceChat-TTS, evaluated standalone, delivers competitive first-turn quality (2.00% WER, 4.380 SQuIM-MOS unseen) with stable multi-turn intelligibility but zero-shot speaker drift, while supporting the persistent silence-and-interruption behavior the full-duplex system requires.

## Key points

- Standalone protocol isolates the decoder from the upstream full-duplex model, testing unseen speakers on LibriTTS test-clean and seen speakers from training, with WER (intelligibility), SECS (speaker similarity), and SQuIM-MOS (predicted overall quality) as metrics.
- First unseen-speaker turn reaches 2.00% WER and 4.380 SQuIM-MOS, beating its streaming-decoder base Audio Flamingo 3-Chat (4.51% WER, 3.600 SQuIM-MOS) with similar first-turn SECS (0.761 vs 0.757).
- Over four consecutive unseen-speaker turns, intelligibility and quality stay stable (WER 2.00% to 2.20%, SQuIM-MOS 4.380 to 4.376) while speaker similarity drifts (SECS 0.757 to 0.685).
- Seen speakers show comparatively stable identity (SECS 0.785 to 0.778 first-to-fourth turn), so the drift is attributed to zero-shot speaker conditioning rather than general persistent-decoding degradation.
- Chatterbox-TTS and Qwen3-TTS-12Hz-1.7B-Base score stronger conventional isolated-response WER, but those results do not test the interaction functionality VoiceChat needs.
- VoiceChat-TTS stays active over the conversation timeline, generates silence under upstream PAD control, and responds to explicit interruption signals without resetting cached state; end-to-end turn-taking is evaluated separately in Table 1.
- The same chunk also reports streaming ASR (80 ms vs 160 ms chunks, average WER 9.02% to 8.28%) and inference efficiency (118 ms per-stream p95 per 160-ms chunk, 1.36x real-time with four concurrent streams on one H100).

## The argument in five moves

1. Human dialogue is full-duplex — continuous listening, fine turn-taking, backchannels, overlap, and interruption — which half-duplex cascaded ASR+LLM+TTS stacks gated by VAD cannot reproduce, and prior full-duplex work plus proprietary realtime APIs leave open tool-calling while preserving full-duplex behavior largely unexplored.
2. VoiceChat answers with one unified streaming architecture: a causal streaming speech encoder feeding a decoder-only LLM with parallel specialized agent-text and function-call streams, an auxiliary RNN-T branch for incremental user transcription off the same encoder states, and a streaming TTS/codec decoder — with BOS/EOS/padding on an 80-ms timeline supervising begin/stop/remain-silent.
3. The system is built component-wise: CPT/SFT train the full-duplex backbone with weighted agent-text and function-channel losses (audio-codec prediction disabled, TTS trained separately), then a frozen-encoder RNN-T branch is attached with transducer loss, using TTS-rendered pseudo-dialogue CPT data, mixed SFT buckets with multi-agent tool-calling data and online interruption/backchannel/delay/noise augmentations, plus inference-time filler messages, RNN-T endpointing fallback, and an optimized runtime.
4. Empirically, the design preserves conversational behavior — lowest open-weight pause-takeover rates, 100% interruption takeover at 4.33/5 quality, 93% backchannel resume — while matching Freeze-Omni on VoiceBench intelligence (55.1) and leading on FDB 3.0 tool-selection F1 (82.5%), with TTS holding stable multi-turn quality and streaming ASR/inference meeting real-time budgets.
5. The remaining gap is execution depth, not routing or fluency: argument accuracy (42.2%) and Pass@1 (33.0%) trail Gemini Live, multi-tool and many-tool use is unreliable, context is capped near two minutes with no barge-in during tool execution and noise fragility — so full-duplex interaction, recognition, generation, language competence, and tool use coexist in one open model, but precise end-to-end tool execution still needs work.
