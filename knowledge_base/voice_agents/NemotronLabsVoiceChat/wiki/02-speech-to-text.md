> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 2.1. Speech-to-Text (STT) — The STT Component
**In one sentence:** The STT component pairs a causal streaming perception module with the NVIDIA Nemotron-Nano-9B-v2-Base LLM to predict agent-text and function-call outputs on a shared 80-ms timeline, while an auxiliary RNN-T branch on the same encoder states produces incremental user transcription without feeding the LLM.
## Key points
- Architecture is a perception module plus a decoder-only LLM (NVIDIA Nemotron-Nano-9B-v2-Base), following the architecture in [16, 17]; the perception module encodes streaming user speech and the LLM predicts agent-text and function-call outputs.
- Audio front end converts 16-kHz user waveform into 128-bin log-Mel features using a 25-ms Hann window and 10-ms stride.
- Streaming encoder is 600M parameters with 24 cache-aware FastConformer layers and hidden dimension 1,024; causal depthwise-striding subsampling reduces the sequence by 8x, producing one encoder state every 80 ms.
- Streaming is strictly causal: self-attention uses a 70-frame left context and no right context, and convolutional modules are also causal, so no future audio is required for the current state.
- The perception module is run once and exposes two representations: raw FastConformer states go to the auxiliary RNN-T branch, while an identity modality adapter and projection map the same 1,024-dimensional states into the LLM hidden dimension, avoiding a second ASR encoder and keeping transcription synchronized with response context.
- Frame-level turn-taking supervision uses ordinary agent-text BOS/EOS tokens on the 80-ms timeline: BOS at response onset, response subwords in consecutive frames, EOS as stop target after a brief overlap when a subsequent user turn begins (no EOS for a final agent turn), padding elsewhere; BOS = begin, EOS = stop, padding = remain silent.
- Auxiliary RNN-T (two-layer 640-dimensional recurrent prediction network + 640-dimensional joint network, 1,024-unit BPE vocabulary plus blank, decoded incrementally) is exposed as an auxiliary output rather than fed into the LLM, preserving a direct speech-conditioned response path.
---
## Architecture overview
The STT component "comprises a perception module and a decoder-only LLM, similar to the architecture in [16, 17]." The backbone is stated verbatim as:

> "We use NVIDIA Nemotron-Nano-9B-v2-Base [18] as the LLM backbone."

Roles:

| Part | Role per chunk |
|---|---|
| Perception module | Encodes streaming user speech |
| LLM | Predicts agent-text and function-call outputs |
| Auxiliary RNN-T branch (attached to perception module) | Produces incremental user transcription |

## Audio preprocessor and streaming encoder
> "Within the perception module, an audio preprocessor converts the 16-kHz user waveform into 128-bin log-Mel features using a 25-ms Hann window and a 10-ms stride."

| Item | Value |
|---|---|
| Input waveform | 16 kHz |
| Feature | 128-bin log-Mel |
| Window / stride | 25-ms Hann window, 10-ms stride |
| Encoder size | 600M parameters |
| Encoder layers | 24 cache-aware FastConformer layers [19] |
| Hidden dimension | 1,024 |
| Subsampling | Causal depthwise-striding, factor of 8 |
| Encoder state rate | One state every 80 ms |
| Self-attention context | 70-frame left context, no right context |
| Convolution | Causal; no future audio required for current state |

## One encoder, two representations
> "The perception module processes the waveform once and exposes two representations."

| Representation | Destination | Transform |
|---|---|---|
| Raw FastConformer states | Auxiliary RNN-T branch | None (raw states) |
| Same 1,024-dimensional states | LLM | Identity modality adapter + projection into LLM hidden dimension |

Stated benefit: "Sharing the encoder avoids running a second ASR encoder and keeps transcription synchronized with the acoustic context used for response generation."

## Frame-level agent-text and turn-taking supervision
Training represents the agent response "on the same 80-ms timeline as the encoder output":

| Timeline rule | Detail |
|---|---|
| Initialization | Each example initialized with padding tokens |
| Response onset | Ordinary agent-text BOS token placed at response onset |
| Response body | Response subword tokens in consecutive frames |
| Stop | When a subsequent user turn begins, agent EOS token serves as stop target after a brief overlap |
| Final turn | A final agent turn without a subsequent user turn has no EOS target |
| Gaps | Frames without agent-text target, including gap between last response token and EOS, remain padding |

> "BOS and EOS therefore serve as frame-level turn-taking targets: BOS teaches when the model should begin responding, EOS teaches when it should stop, and padding teaches it to remain silent."

These are "the normal agent-text BOS and EOS tokens and are distinct from the function-channel boundaries <SOTC>, <EOTC>, and <EOTR> described in Section 2.2."

## Auxiliary RNN-T transcription branch
> "The raw encoder states additionally feed an RNN-T comprising a two-layer, 640-dimensional recurrent prediction network and a 640-dimensional joint network."

| Item | Value |
|---|---|
| Prediction network | Two-layer, 640-dimensional recurrent network |
| Joint network | 640-dimensional |
| Vocabulary | 1,024-unit BPE plus transducer blank |
| Decoding | Incremental, as audio frames arrive |
| Use | Resulting user transcript exposed as auxiliary output, not fed into the LLM |

Stated reason: "preserving a direct speech-conditioned response path."

**Covers:** Section 2.1 (chunk 02-2-1-speech-to-text-stt-the-stt-component)
