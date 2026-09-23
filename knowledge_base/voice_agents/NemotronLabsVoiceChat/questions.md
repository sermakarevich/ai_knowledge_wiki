---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities

### Q1. What is the unified streaming architecture of NemotronLabs VoiceChat, and how does its tool-calling design differ from DuplexSLA?

> [!tip]- Answer
> VoiceChat combines a streaming speech encoder, a decoder-only LLM with parallel specialized agent-text and function-call heads, an auxiliary RNN-T transcription branch, and a streaming TTS/codec decoder for concurrent listen, transcribe, reason, invoke, and speak. Unlike DuplexSLA, which serializes planning and action tokens in one shared autoregressive channel, VoiceChat keeps parallel specialized streams to preserve low-latency full-duplex behavior. See [[wiki/01-overview-architecture|Overview and Full-Duplex Architecture]].

### Q2. What are the exact front-end and streaming-encoder specifications of the STT perception module?

> [!tip]- Answer
> The front end converts 16-kHz waveforms into 128-bin log-Mel features with a 25-ms Hann window and 10-ms stride. The 600M-parameter encoder has 24 cache-aware FastConformer layers (hidden 1,024) with causal depthwise-striding subsampling by 8x, emitting one state every 80 ms using 70-frame left context and no right context. See [[wiki/02-speech-to-text|2.1. Speech-to-Text (STT) — The STT Component]].

### Q3. How does frame-level turn-taking supervision work on the 80-ms timeline, and what is the role of the auxiliary RNN-T branch?

> [!tip]- Answer
> Ordinary agent-text BOS marks response onset, subwords fill consecutive frames, EOS is the stop target after brief overlap when a user turn begins (no EOS on a final turn), and padding teaches silence elsewhere. The raw encoder states also feed a two-layer 640-dim RNN-T predictor plus 640-dim joint network with 1,024-unit BPE vocabulary, decoded incrementally as an auxiliary output not fed to the LLM. See [[wiki/02-speech-to-text|2.1. Speech-to-Text (STT) — The STT Component]].

### Q4. What is the component-wise training strategy and the STT loss with its CPT/SFT weights?

> [!tip]- Answer
> The full-duplex STT backbone trains via CPT/SFT with audio-codec loss weight 0.0 while VoiceChat-TTS trains separately, so no gradients flow between them; afterwards only the RNN-T prediction and joint networks train with transducer loss while encoder, LLM, heads, and TTS stay frozen. The loss is ℒSTT = (1−λT2T)(λtextℒtext + λFCℒFC) + λT2TℒT2T, with SFT λtext/λFC/λT2T = 1.0/1.0/0.5 and CPT = 3.0/1.0/0.0, plus heavy upweighting of sparse boundary tokens such as 64.0 for `<TOOLCALL>` content. See [[wiki/03-training-recipes|Component-wise training. The full-duplex STT backbone]].

### Q5. What inference-time enhancements support tool calling and turn-taking, and what turn-management results do they achieve?

> [!tip]- Answer
> Per-tool filler messages mask tool latency, an RNN-T-transcript endpointing fallback force-injects BOS/EOS tokens for turn start and barge-in stop, and an optimized real-time runtime runs the system. V-Model reports 15.3%/25.5% pause TOR (synthetic/CANDOR), 81.5% smooth-turn TOR, 100% interruption TOR at 480 ms with 4.33/5 quality, and 93% Resume on FDB 1.5 backchannels. See [[wiki/03-training-recipes|Component-wise training. The full-duplex STT backbone]].

### Q6. How does V-Model compare on VoiceBench intelligence and FDB 3.0 tool calling, and what are its stated limitations?

> [!tip]- Answer
> V-Model ties Freeze-Omni on VoiceBench (55.1 vs 55.2) with gains on OpenBookQA, MMSU, and AdvBench but weaker SD-QA, open-ended, and IFEval scores; on FDB 3.0 it leads tool-selection F1 at 82.5% yet trails Gemini Live on argument accuracy (42.2%) and Pass@1 (33.0%). Limitations include a ~2-minute audio context window, degraded many-tool and simultaneous multi-tool use, invented arguments, no barge-in during tool execution, and noise fragility. See [[wiki/04-backchannel-evaluation|Respond Resume Uncertain Unknown Model (↓)]].

### Q7. Which prior works and benchmarks does the paper cite, and how is CPT pseudo-dialogue data constructed?

> [!tip]- Answer
> Citations span full-duplex models (Moshi, OmniFlatten, SALMONN-omni, Freeze-Omni, Personaplex, MiniCPM-o 4.5), realtime APIs, the Nemotron-Nano-9B-v2-Base and 0.6B streaming ASR backbones, and benchmarks including Full-Duplex-Bench v1/v1.5/v3 and VoiceBench. CPT data segments plain-text passages into sentences, alternately assigns them to user and agent, synthesizes each turn with TTS voice-cloning from two speaker prompts, and concatenates turns within channels on a shared timeline. See [[wiki/05-references-background|References Background — Prior Full-Duplex Work [4]–[38] and CPT Data Construction]].

### Q8. How is SFT data mixed and augmented for full-duplex behavior?

> [!tip]- Answer
> SFT retains pretraining-style data and adds conversational, instruction-tuning, and multi-agent-pipeline tool-calling buckets plus text-only knowledge at 0.5 T2T weight, with normalized sampler shares near 46.8% retention, 23.8% conversational, 26.0% tool calling, and 3.4% safety. Online augmentations add early interruptions (p=0.1, 640 ms overlap), backchannel injection (p=0.05 per sample), 160 ms text-channel delay, plus DNS5/DEMAND noise (p=0.5), room/microphone IRs, and codec augmentation. See [[wiki/06-sft-data-construction|SFT Data Construction. Like the CPT]].

### Q9. What does standalone evaluation show for VoiceChat-TTS quality, speaker drift, streaming ASR, and inference efficiency?

> [!tip]- Answer
> Unseen-speaker first-turn quality reaches 2.00% WER and 4.380 SQuIM-MOS, beating its Audio Flamingo 3-Chat base, with stable multi-turn intelligibility but zero-shot speaker drift (SECS 0.757 to 0.685 over four turns; seen speakers stay near 0.785 to 0.778). Streaming ASR averages 9.02% WER at 80 ms chunks versus 8.28% at 160 ms, and four concurrent streams run at 118 ms p95 per 160-ms chunk (1.36x real-time) on one H100. See [[wiki/07-tts-decoder-evaluation|We evaluate the VoiceChat-TTS speech decoder]].

### Q10. Would you recommend NemotronLabs VoiceChat as the starting point for a team building an open full-duplex voice agent with tool calling, and why?

> [!tip]- Answer
> Yes for interaction-first prototypes: it is the rare open system unifying barge-in handling, backchannel resume, transcription, and tool routing with leading open tool-selection F1 and a public checkpoint. The caveat is execution depth, since argument accuracy, multi-tool reliability, context length, and noisy conditions still lag, so the team should budget for argument validation and tool-scoping work. See [[wiki/04-backchannel-evaluation|Respond Resume Uncertain Unknown Model (↓)]].
