# 2026-9-21 NemotronLabs VoiceChat: An Open Full-duplex Overview and Architecture

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview and Full-Duplex Architecture
**In one sentence:** NemotronLabs VoiceChat is an open unified streaming speech-to-speech model that listens, transcribes, reasons, invokes tools, and speaks concurrently via a streaming encoder, decoder-only LM with parallel agent-text and tool-call heads, an auxiliary RNN-T transcription branch, and a streaming TTS/codec decoder.
## Key points
- Unified streaming architecture combines a streaming speech encoder, a decoder-only language model, parallel specialized output streams for agent text and structured function calls, an auxiliary RNN-T branch for incremental user transcription, and a streaming TTS decoder.
- Parallel specialized streams for agent text and tool calls preserve low-latency full-duplex behavior, unlike DuplexSLA which serializes heterogeneous action-related tokens within a shared autoregressive channel.
- On Full-Duplex-Bench 1.0, the model achieves the lowest pause-handling takeover rates among evaluated open-weight systems, 100% takeover following user interruptions, and a 4.33/5 post-interruption response-quality score.
- On Full-Duplex-Bench 1.5, it resumes its response after user backchannels in 93% of cases.
- On VoiceBench it obtains a 55.1 normalized average, and on Full-Duplex-Bench 3.0 (FDB 3.0) it achieves 82.5% tool-selection F1, while argument accuracy and end-to-end tool execution remain areas for improvement.
- Motivation is the gap between half-duplex cascaded ASR + LLM + TTS stacks gated by voice-activity detection and human full-duplex dialogue with fine-grained turn-taking, backchannels, overlap, hesitation, and interruption.
- Open checkpoint is available on Huggingface; paper is arXiv:2609.21967v1 [cs.CL] 18 Sep 2026, NVIDIA, © 2026 NVIDIA.
---
## Abstract
**Covers:** Abstract (arXiv:2609.21967v1 [cs.CL] 18 Sep 2026)

The chunk states:

> "We introduce NemotronLabs VoiceChat, an open full-duplex speech-to-speech model with native tool-calling capabilities."

Design components named in the abstract:

- streaming speech encoder and decoder-only language model
- parallel specialized output streams for agent text and structured function calls
- auxiliary RNN-T branch for incremental user transcription
- streaming TTS decoder

Claimed behavior: the design enables the model to "listen, transcribe, reason, invoke tools, and speak within a unified streaming architecture while preserving the temporal behavior required for natural conversation."

Reported results (verbatim numbers):

| Benchmark | Metric | Value |
|---|---|---|
| Full-Duplex-Bench 1.0 | pause-handling takeover | lowest among evaluated open-weight systems |
| Full-Duplex-Bench 1.0 | takeover following user interruptions | 100% |
| Full-Duplex-Bench 1.0 | post-interruption response quality | 4.33/5 |
| Full-Duplex-Bench 1.5 | resume response after user backchannels | 93% |
| VoiceBench | normalized average | 55.1 |
| Full-Duplex-Bench 3.0 (FDB 3.0) | tool-selection F1 | 82.5% |

Stated limitation: "argument accuracy and end-to-end tool execution remain areas for improvement."

Stated conclusion: "full-duplex interaction, speech recognition and generation, general language capabilities, and external tool use can be integrated in a single open speech-to-speech model without sacrificing real-time conversational behavior."

## 1. Introduction — from cascaded half-duplex to full-duplex with tools
**Covers:** Section 1, Introduction

Conventional cascaded architecture described in the chunk: automatic speech recognition (ASR) connected to a large language model (LLM) used in a chat function, plus a text-to-speech (TTS) system translating the LLM response into audio. More recent unified speech language models enable direct speech-conditioned reasoning and speech generation, but low-latency speech-to-speech generation alone "does not reproduce the dynamics of human conversation."

Half-duplex characterization (verbatim mechanism): "the system relies on a voice activity (VAD) detection module to detect when the user stops speaking, and only then begins producing its response." Human dialogue, by contrast, "is inherently full-duplex. Speakers continuously listen while speaking, take turns with fine temporal precision, produce backchannels, overlap, hesitate, and interrupt one another."

Prior full-duplex work cited in the chunk spans:

- explicit dialogue-state control
- synchronous or parallel listening–speaking architectures
- end-to-end models that jointly represent user and assistant audio streams
- modular adaptation, controllable conversational behavior, and multimodal realtime interaction

Chunk's assessment of that prior work: "their contributions are primarily centered on the dynamics of realtime interaction itself. Enabling such agents to seamlessly invoke external tools while preserving these full-duplex properties remains much less explored."

Proprietary realtime tool calling noted in the chunk:

- OpenAI Realtime API "can emit structured function calls during a realtime session"
- Gemini Live "similarly supports function invocation and the asynchronous return of tool results"

Open-research adjacent work discussed in the chunk:

- DuplexSLA: introduces "a rate-limited textual action channel alongside user and assistant speech, through which the model autoregressively produces planning tokens and structured actions on the same temporal timeline as the conversation." Footnote in chunk: "At the time of writing the model has still not been made publicly available."
- MoshiRAG: "does not perform general-purpose tool calling in the conventional sense, but demonstrates an important adjacent capability: a full-duplex speech model can detect that an utterance requires external knowledge, asynchronously trigger retrieval, and incorporate the retrieved information into its response without suspending the conversational flow."

VoiceChat differentiation claims (verbatim contrast):

- "Unlike traditional cascaded stacks, this model achieves full duplex, real-time, seamless voice interaction in one unified architecture, eliminating the need for multiple models or API handoffs, thus reducing end-to-end latency."
- "Unlike DuplexSLA, which serializes heterogeneous action-related tokens within a shared autoregressive channel, NemotronLabs VoiceChat maintains parallel, specialized streams, preserving the low-latency behavior required for full-duplex interaction."
- "Our model achieves an unprecedented trade-off between general 'intelligence', conversational naturalness, user-speech transcription accuracy and tool calling capabilities, while being completely open." Footnote in chunk: "Checkpoint available on Huggingface."

## 2. Model Architecture — overview and Figure 1
**Covers:** Section 2 opening + Figure 1

Opening architecture statement: "extends a streaming full-duplex speech-to-speech architecture with integrated user transcription and tool-calling capabilities. A streaming speech encoder continuously processes the user audio, while a decoder-only language model tracks the evolving conversation and generates both the agent" response and structured function calls.

Downstream/transcription path stated in the chunk: "The generated response is converted into speech by a streaming speech and codec decoder, and an auxiliary RNN-T decoder predicts the user transcription from the shared input speech representation."

Figure 1 elements visible in the chunk text layer:

- Agent Audio Stream with Streaming Codec Decoder producing agent speech across `<turn-1>`, `<silence>`, `<turn-2>`
- Speech Decoder producing agent text tokens and tool call across the same turn/silence timeline
- Agent text head and Tool calling head feeding a Softmax into the decoder-only LM
- Input Pooling over tool call, agent text, and user speech turn/silence segments
- Streaming Speech Encoder over the User Stream with barge-in (user) and turn-taking (agent) markers
- RNN-T decoder path with Pred network and Joiner network producing User Transcription across `<silence>`, `<turn-2>`, `<silence>`

Figure caption in chunk: "Figure 1 | NemotronLabs VoiceChat Architecture Overview."

**Covers:** Abstract, Section 1 (Introduction), Section 2 opening and Figure 1; arXiv:2609.21967v1 [cs.CL] 18 Sep 2026.
