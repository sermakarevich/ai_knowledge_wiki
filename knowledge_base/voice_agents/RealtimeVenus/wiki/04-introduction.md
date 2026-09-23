> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction: natural interaction with asynchronous delegation
**In one sentence:** Realtime-Venus is a proactive full-duplex system that pairs two native conversational frontends with an asynchronous harness so live interaction continues while background tasks execute and their results are re-integrated into the ongoing dialogue.
## Key points
- Natural interaction requires interpreting ongoing observations while deciding when and how to respond, including initiating without an explicit user request.
- Built on MiniCPM-o 4.5, the system provides two separately trained 9B models: Realtime-Venus-Omni for audio–visual interaction and Realtime-Venus-Audio for spoken interaction.
- Each frontend is a complete conversational frontend with continuous perception, conversational control, and native speech generation, jointly predicting interaction-control tokens, response text, and private delegation requests.
- A unified streaming formulation aligns user observations, model outputs, private delegation requests, and background results on a shared causal timeline.
- Realtime-Venus-Harness runs in a dual-loop runtime: the frontend maintains live interaction while the harness executes registered capabilities asynchronously, binding each request to its originating session plus an evidence snapshot.
- Freshness checks determine result eligibility and playback-aware delivery governs when results re-enter the conversation; the frontend then interprets returned information against possibly changed user intent.
- The data pipeline combines scenario planning, speech realization, and temporal alignment, distinguishing backchannels and other-directed speech from interruptions requiring stop, repair, or redirect, and coupling delegation requests with background execution and continuations.
- Realtime-Venus-Omni leads on six of eight video benchmarks, Realtime-Venus-Audio leads several audio understanding and spoken QA comparisons, and full-duplex tests show high continuation rates under non-interruptive speech.
---
## Motivation: different timescales in one session
**Covers:** Section 1, paragraphs on prior models and timescale mismatch

Continuous interaction and external computation operate on different timescales within the same session. A background task needs a stable record of the request and supporting evidence, but its result must be interpreted in a conversation that may have changed during execution.

Prior context cited in the chunk:

| System | Capability noted |
|---|---|
| Moshi (Défossez et al., 2024) | Concurrent speech modeling |
| Qwen2.5-Omni and Qwen3-Omni (Xu et al., 2025a,b) | Multimodal perception with native streaming speech generation |
| MiniCPM-o 4.5 (Cui et al., 2026) | Proactive full-duplex video interaction |
| Spoken-agent work (Chien et al., 2026; Huang et al., 2026; OpenAI, 2026; Zhang et al., 2026) | Retrieval, tool calls, asynchronous external computation during dialogue |

> "Coordinating task capture with conversational result delivery is essential to maintaining coherent interaction."

## System framing: frontends plus harness
**Covers:** Section 1, system description paragraphs

- Two frontends: Realtime-Venus-Omni (audio–visual) and Realtime-Venus-Audio (spoken), each a complete conversational frontend.
- Shared policy supports: maintaining a response during user backchannels; revising its unspoken continuation after a correction; initiating background work when a request requires external capabilities.
- Realtime-Venus-Harness: shared framework for asynchronous capability execution and result delivery; routes each delegation request to a registered capability, returns eligible results as private context.
- Design goal: "preserves stable context for background execution while allowing the frontend to adapt its response to subsequent changes in user intent."

## Training data and post-training recipe
**Covers:** Section 1, training paragraphs

- Unified pipeline combines scenario planning, speech realization, and temporal alignment.
- Duplex scenarios distinguish backchannels and other-directed speech from interruptions that require stopping, repairing, or redirecting.
- Proactive trajectories supervise when to initiate a response versus continue listening; delegation scenarios link private requests, background execution, returned information, and subsequent responses.
- Shared post-training recipe mixes offline understanding, proactive duplex interaction, and delegation workflows; Omni uses audio–visual plus audio-only data, Audio uses the audio-only subset.
- Supervision covers interaction-control transitions and subsequent generation, linking listen / speak / delegate decisions to the following response.

## Contributions
**Covers:** Section 1, contributions list

- Proactive full-duplex interaction models: two separately trained 9B models integrating continuous perception, conversational control, native speech generation, and private delegation; Realtime-Venus-Omni claimed as "the first full-duplex omni model to support asynchronous backend invocation for reasoning and tool execution while maintaining video interaction," with hour-scale video understanding via memory augmentation.
- Asynchronous capability execution with Realtime-Venus-Harness: binds tasks to evidence at the request boundary, executes asynchronously, returns results to the originating session while preserving frontend control over responses.
- Coupled duplex and delegation data pipeline: scenario planning, speech realization, and temporal alignment to couple conversational events with delegation requests, background results, and response continuations.

## Related work (partial, as present in chunk)
**Covers:** Section 2 start through tool-use paragraph fragment

- Omni-modal understanding: Gemini, GPT-4o, Baichuan-Omni-1.5, MiniCPM-o 2.6, Qwen2.5-Omni (time-aligned audio–visual representations, Thinker–Talker), Qwen3-Omni (mixture-of-experts, multi-codebook speech); noted limitation: "full-duplex interaction requires incoming observations to influence an ongoing response."
- Audio understanding and speech generation: SALMONN (window-level Q-Former), Qwen-Audio (hierarchical task tags), Qwen2-Audio, SpeechGPT (discrete speech representations), Kimi-Audio, MiMo-Audio, Fun-Audio-Chat, Step-Audio 2; audio frontend aim: "retain acoustic and semantic competence while jointly learning conversational control and delegation."
- Proactive and full-duplex interaction: Moshi (parallel streams, Inner Monologue), Freeze-Omni (chunk-level dialogue-state classifier), Fun-Audio-Chat, JoyAI-Talker (Joy-Duplex), MiniCPM-o 4.5 (Omni-Flow), LiveStar (response–silence decoding), MMDuet2 (multi-turn RL); this work places "conversational control, response generation, and private delegation within a shared policy and timeline."
- Tool use and asynchronous delegation: ReAct (interleaved reasoning/actions), DuplexSLA (structured action channel), MoshiRAG (selective asynchronous retrieval), DuplexOmni (pluggable asynchronous thinking layer), JoyAI-VL-Interaction (proactive visual interaction to background delegation).

**Covers:** Section 1 Introduction through Section 2 Related Work fragment present in chunk 04
