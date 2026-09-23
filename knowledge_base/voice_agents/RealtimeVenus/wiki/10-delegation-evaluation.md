> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Delegation Behavior Taxonomy and Evaluation Protocol
**In one sentence:** Each trajectory links an observed event to a duplex target (immediate conversational action) and a delegation target (computational handling) joined by the event's effect on user intent, and Realtime-Venus evaluates both frontends on video/audio understanding, spoken QA, Full-Duplex-Bench v1.5 overlap handling, FDB-v3 tool use, and an internal delegate benchmark under fixed sampling and audio settings.
## Key points
- The aligned session preserves overlap intervals, response boundaries, and the affected portion of assistant output, materialized as audio-only data for Realtime-Venus-Audio or video data for Realtime-Venus-Omni.
- Both modalities share one trajectory and supervision: a compact model-visible vocabulary encodes online interaction-control actions, while non-audible delegation requests, background results, and execution metadata stay in the structured event stream.
- The duplex target is one of continue speaking, await input, yield the floor, stop queued output, or revise the response, selected on conversational meaning rather than acoustic overlap alone.
- The delegation target keeps simple or latency-sensitive acts with the frontend, may invoke a registered capability when additional perceptual evidence, broader context, or substantial replanning is needed, and routes external-information or executable-action requests to tools or specialized components, with longer operations able to run alongside a cancellable local acknowledgment.
- Supervision specifies whether active work is retained, canceled, revised, reconciled with another result, retried, or replaced by a fallback; a stable-intent interruption may stop playback while retaining the semantic plan, while an intent-changing correction cancels dependent work and triggers replanning.
- Evaluation covers Realtime-Venus-Omni on streaming and offline video understanding, both frontends on audio understanding, spoken QA, and Full-Duplex-Bench v1.5 overlap handling, plus both frontends within Realtime-Venus on FDB-v3 tool use and the internal delegate benchmark.
- Full-Duplex-Bench v1.5 uses response categories C_RESPOND, C_RESUME, UNCERTAIN, and UNKNOWN, with responding desired for user interruptions and continuing the preceding response preferred for backchannels, talking to others, and background speech.
- Default evaluation settings sample video at 1 frame per second with at most 128 frames at approximately 448 × 448 pixels, convert input waveforms to mono at 16 kHz, process full-duplex audio in one-second chunks with perception active during generation, and generate speech output at 24 kHz.
---
## Function, intended addressee, and associated system
The chunk opens mid-sentence on "function, intended addressee, and associated system behavior." It states:
> "The aligned session preserves overlap intervals, response boundaries, and the portion of assistant output affected by an interaction event."
> "It is then materialized as audio-only data for Realtime-Venus-Audio or video data for Realtime-Venus-Omni."
> "Both modalities share the underlying trajectory and supervision: a compact model-visible vocabulary encodes online interaction-control actions, while non-audible delegation requests, background results, and execution metadata remain in the structured event stream."

## Coupling duplex and delegation behaviors (§6.2)
Each trajectory links an observed event to two complementary targets:
- Duplex target (immediate conversational action): "continue speaking, await input, yield the floor, stop queued output, or revise the response." Selection "reflects conversational meaning, not acoustic overlap alone."
- Delegation target (computational handling): "Simple or latency-sensitive conversational acts remain with the frontend. Requests requiring additional perceptual evidence, broader context, or substantial replanning may invoke a registered capability; those involving external information or executable actions are routed to tools or specialized components. Longer operations can run alongside a cancellable local acknowledgment."
- Supervision: "specifies whether active work is retained, canceled, revised, reconciled with another result, retried, or replaced by a fallback."

Intent-effect mapping (verbatim claims):
- "Backchannels, other-directed speech, and unrelated background speech generally preserve the active response, whereas floor-taking interruptions stop queued audio."
- "Hesitation may pause responses; intent-changing corrections trigger recovery."
- "A backchannel preserves speech and computation; other-directed and background speech create no new route."
- "A stable-intent interruption may stop playback while retaining the semantic plan; an intent-changing correction cancels dependent work and triggers replanning."
- "Tool-dependent requests pair immediate feedback with asynchronous execution."
- "Each trajectory connects observable context, interaction control, computation management, and execution outcomes on a shared timeline."

## Evaluation protocol (§7)
> "We evaluate Realtime-Venus through complementary assessments of its two frontend models. We assess Realtime-Venus-Omni on streaming and offline video understanding. Both Realtime-Venus-Omni and Realtime-Venus-Audio are evaluated on audio understanding, spoken question answering, and overlap handling on Full-Duplex-Bench v1.5. We also evaluate both frontends within Realtime-Venus on the tool-use component of Full-Duplex-Bench v3 (FDB-v3) and compare their routing decisions on our internally developed delegate benchmark."

## Evaluation datasets and metrics (§7.1)
- Streaming and offline video understanding: "StreamingBench (Lin et al., 2024) covers 18 tasks in real-time visual, omni-source, and contextual understanding. OVO-Bench (Niu et al., 2025) covers 12 tasks in real-time visual perception, backward tracing, and forward active responding. ProactiveVideoQA (Wang et al., 2025e) reports PAUC across WEB, EGO, TV, and VAD, while OmniPro (Zhao et al., 2026) reports probe-mode accuracy and online-mode F1. For offline video understanding, we report overall accuracy on WorldSense (Hong et al., 2026), Daily-Omni (Zhou et al., 2025), OmniVideoBench (Li et al., 2026), and LVOmniBench (Tao et al., 2026). The memory study reports accuracy by duration bin on LVOmniBench, LongVideoBench (Wu et al., 2024), and CGBench (Chen et al., 2025)."
- Audio understanding: "We use MMAU (Sakshi et al., 2024), MMAU-Pro (Kumar et al., 2025), MMAR (Ma et al., 2025), and MMSU (Wang et al., 2025a)"; "MMAU covers speech, music, and sound; MMAU-Pro extends evaluation to challenging long-form, spatial, and multi-audio settings. MMAR emphasizes reasoning from contextual and acoustic evidence, while MMSU assesses spoken-language understanding, including linguistic and paralinguistic cues. We report accuracy under the task configuration used for each benchmark."
- Spoken question answering: VoiceBench AlpacaEval (Chen et al., 2024), Llama Questions (Nachmani et al., 2024), Speech TriviaQA (Défossez et al., 2024), and Speech CMMLU (Shi et al., 2026); "VoiceBench AlpacaEval uses a judge-based response-quality score; the remaining tasks use benchmark-specific measures of answer accuracy."
- Full-duplex interaction: "Full-Duplex-Bench v1.5 (Lin et al., 2026b) evaluates user interruption, user backchannel, talking to others, and background speech. Its four response categories are C_RESPOND, C_RESUME, UNCERTAIN, and UNKNOWN"; "Responding is the desired behavior for user interruptions; continuing the preceding response is preferred in the other scenarios."
- Full-duplex tool use: FDB-v3 tool-use component (Lin et al., 2026a), "which tests voice agents on human-recorded speech containing fillers, pauses, hesitations, false starts, and self-corrections. Its tasks span four application domains and require single-step or chained calls to deterministic mock APIs. Tool selection F1 compares expected and predicted tool calls, penalizing missed and extra calls. Argument accuracy measures the semantic correctness of function arguments. Pass@1 is the proportion of episodes in which all expected tools are called, no extra calls are made, and every call has correct arguments. We report these metrics as percentages."
- Full-duplex delegation: "an internally constructed delegate benchmark. It includes omni and audio-only input modes with different levels of difficulty. Its tasks span three categories: external capabilities, routine interaction, and reasoning. Overall accuracy measures agreement with reference delegation decisions across all requests within each mode. Delegation recall measures the proportion of external-capability requests correctly delegated. Non-delegation specificity measures the proportion of routine requests for which the model correctly avoids delegation. Reasoning accuracy measures correct routing on a mixture of requests requiring delegation and direct handling. We report these metrics as percentages for each input mode."

## Evaluation settings (§7.2)
> "By default, we sample videos at 1 frame per second, retain at most 128 frames, and resize frames to approximately 448 × 448 pixels while preserving the original aspect ratio."
> "Streaming predictions are conditioned on observations available at the corresponding query or response time, while offline tasks permit access to the sampled evaluation clip before answering."
> "For both Realtime-Venus-Omni and Realtime-Venus-Audio, input waveforms are converted to mono and resampled to 16 kHz."
> "During full-duplex evaluation, incoming audio is processed in one-second chunks, with perception remaining active during speech generation."
> "When speech output is required, waveforms are generated at 24 kHz."
> "We report offline and online baselines separately in the summary table. In all tables, bold and underlined values indicate the best and second-best distinct scores, respectively."

## Omni results — Table 2 start (§7.3)
> "Streaming and offline understanding. Table 2 compares Realtime-Venus-Omni with offline and online baselines across eight benchmarks."

Table 2 values present in this chunk (0–100 scale; StreamingBench, OVO-Bench, WorldSense, Daily-Omni, OmniVideoBench, LVOmniBench report accuracy; ProactiveVideoQA reports PAUC; OmniPro reports probe-mode accuracy):

| Model | Size | StreamingBench | OVO-Bench | ProactiveVideoQA | OmniPro | WorldSense | Daily-Omni | OmniVideoBench | LVOmniBench |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| InternVL3.5 | 8B | 60.8 | 53.8 | 37.5 | 12.1 | 39.2 | 53.4 | 35.7 | 38.1 |
| Qwen3-VL | 8B | 53.5 | 49.8 | 43.4 | 19.5 | 44.0 | 45.6 | 30.7 | 30.2 |
| Qwen3.5 | 9B | 57.0 | 55.0 | 47.3 | 22.7 | 45.5 | 47.5 | 31.1 | 32.1 |
| Qwen3-Omni | 30B | 64.3 | 61.4 | 44.1 | 22.6 | 49.6 | 72.6 | 38.4 | 39.7 |
| video-SALMONN 2+ | 7B | 59.9 | 46.8 | 40.4 | 22.1 | 49.8 | 66.1 | 35.8 | 38.7 |
| AV-Flamingo | 7B | 58.5 | 51.5 | 34.6 | 18.6 | 53.2 | 69.4 | 39.9 | 38.0 |
| Gemini-3.5-Flash | – | 77.3 | 71.6 | 56.5 | 52.4 | 67.2 | 82.3 | 64.6 | 58.2 |
| LiveStar | 8B | 60.2 | 38.0 | 25.0 | 8.3 | 36.1 | 44.7 | 29.3 | 32.5 |
| MMDuet2 | 3B | 58.1 | 47.6 | 34.9 | 7.6 | 36.9 | 50.6 | 30.4 | 32.1 |
| JoyAI-VL-Interaction | 8B | 63.3 | 56.7 | 39.1 | 18.2 | 43.0 | 54.1 | 36.7 | 36.3 |
| MiniCPM-o 4.5 | 9B | 67.9 | 60.7 | 47.5 | 25.6 | 54.2 | 79.4 | 37.7 | 36.7 |
| Realtime-Venus-Omni | 9B | 70.2 | 64.7 | 46.2 | 29.0 | 54.0 | 81.3 | 39.2 | 38.9 |

Note: the chunk ends mid-table-notes at "All scores are shown on a 0–100 scale; offline models are shown for reference." Full interpretation of Table 2 belongs to the understanding-evaluation chunk; values are reproduced here only because they appear in this chunk's text.

**Covers:** §6 tail (function, intended addressee, and associated system) through §6.2 Coupling duplex and delegation behaviors, §7 Evaluation Protocol, §7.1 Evaluation datasets and metrics, §7.2 Evaluation settings, and §7.3 Table 2 start
