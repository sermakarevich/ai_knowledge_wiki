> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Unified Runtime Abstraction — Both Frontends
**In one sentence:** Both Realtime-Venus frontends share one causal per-second runtime transition that maps retained state, media input, newly admitted background replies, and playback feedback to control, foreground, delegation, and speech outputs, implemented by a MiniCPM-o 4.5-derived omni/audio streaming stack with in-stream delegation and, for Omni, a training-free long-video memory.
## Key points
- Both frontends run the same 1-second-chunk causal transition `(s_{k+1}, O_k) = F_m(s_k, x^m_k, b_k; η_k)` (Eq. 1), where only foreground text `Y_k` and speech tokens `S_k` of `O_k = (c_k, Y_k, D_k, S_k)` are user-facing.
- Media inputs are `x^{audio}_k = u_k` (causal audio features) and `x^{omni}_k = (u_k, v_k)` (plus aligned visual features), with `v_k = ∅` when no frame is available.
- Retained state `s_k` carries model context, partial output spans, and previously admitted reply text, so old replies stay deliverable without a new background message every chunk; `b_k` carries only newly admitted reply text and `η_k` carries playback acknowledgments.
- Delegation text `D_k` may span chunks; a completed request commits a work item whose evidence boundary was fixed at request start, and its prepared reply can be admitted at a later input boundary and spoken using current interaction state.
- Both frontends adapt MiniCPM-o 4.5 (open-source 9B): SigLIP2 + Whisper-Medium encoders for Omni, audio-only (no ViT branch) for Audio, Qwen3-8B backbone, discrete S3 speech tokens, and a streaming flow-matching decoder using system-prompt reference audio.
- Each 1-second unit predicts `<|listen|>` or `<|speak|>`; speaking units generate text conditioning S3 tokens, `<|chunk_eos|>` closes a speech chunk and `<|turn_eos|>` ends a turn, keeping perception concurrent and the unspoken continuation revisable for omni-proactive (Omni only) and full-duplex (both) behavior.
- The Omni-only long-video memory is training-free and decoupled: motion-compensated gating decides archival, MaxSim + MAD-weighted relevance plus MMR-style novelty score retrieval, then chronological reassembly of retrieved frames with adjacent audio plus the recent short-term window.
---
## 3.2 Unified runtime abstraction
**Covers:** Sec. 3.2, Eq. (1)

Both frontends follow the same runtime structure: "they receive media and newly returned replies, update retained session state, and determine interaction behavior and output."

| Symbol | Meaning in chunk |
|---|---|
| `σ`, `m ∈ {audio, omni}` | Session, frontend selector (session superscripts omitted) |
| `k` | One-second chunk index |
| `x^{audio}_k = u_k` | Causal audio features |
| `x^{omni}_k = (u_k, v_k)` | Causal audio + aligned visual features; `v_k = ∅` when no frame is available |
| `s_k` | Frontend state retained before chunk `k`, including model context, partial output spans, and previously admitted reply text awaiting delivery |
| `b_k` | Background input: private reply text newly admitted before assistant generation in that chunk |
| `η_k` | Runtime feedback recording causal events such as playback acknowledgments |
| `O_k = (c_k, Y_k, D_k, S_k)` | Interaction-control tokens, foreground text, delegation text, speech tokens; only `Y_k` and `S_k` are user-facing |

> "(s_{k+1}, O_k) = F_m(s_k, x^m_k, b_k; η_k)." (1)

Per chunk: "`F_m` summarizes streaming decoding and runtime scheduling while preserving the causal input–output order within each chunk, as specified in Section 4.3." "Delegation text `D_k` may extend across multiple chunks." "A completed request commits a work item whose evidence boundary was fixed when the request began, and its prepared reply can be admitted at a later input boundary." "For delegated replies, the frontend uses the current interaction state to schedule speech output of the text prepared by the harness." "Section 5 details task capture, capability execution, and reply delivery." "Previously received replies remain available through the retained state, so their delivery does not require a new background message in every chunk."

## Figure 5 — Omni architecture
**Covers:** Fig. 5 caption and diagram labels

> "Figure 5 Architecture of Realtime-Venus-Omni for audio-visual perception, full-duplex interaction, and asynchronous delegation."

Diagram stages as labeled: streaming perception (Vision encoder, Audio encoder) → long-term / short-term audio-visual memory (Construct/Write via Frame filter, Vision encoder, Audio encoder; Retrieve via Query, Relevance, Novelty; Assemble Retrieved + Recent) → model context (Omni LLM, Delegate Harness, Task, Result) → streaming output (Text, Speech decoder, Speech, Recall). Retrieval illustration ranks candidates (e.g. relevance 1/4/3/2, novelty 1/2) and marks rejected/distinct/repeated-scene content.

## 4 Model Design — both frontends
**Covers:** Sec. 4 intro

> "Realtime-Venus-Omni and Realtime-Venus-Audio are the omni-modal and audio-only streaming frontends of Realtime-Venus, respectively."

Each "continuously processes incoming signals, decides whether and when to respond, and generates speech within a single autoregressive interaction loop." "We develop both frontends by adapting MiniCPM-o 4.5 (Cui et al., 2026), an open-source 9B model." "Both incorporate an in-stream delegation protocol that connects the latency-sensitive foreground loop to the Delegate Harness described in Section 5, enabling complex requests to execute asynchronously while perception and speech generation continue." "Realtime-Venus-Omni additionally integrates a training-free long-video memory module that retains relevant visual context across hour-long sessions."

## 4.1 Model Architecture
**Covers:** Sec. 4.1

"The model family inherits the Omni-Flow architecture of MiniCPM-o 4.5, as shown in Figure 5." "Realtime-Venus-Omni encodes aligned visual and audio streams with SigLIP2 (Tschannen et al., 2025) and Whisper-Medium (Radford et al., 2023), whereas Realtime-Venus-Audio removes the ViT-based visual branch and processes only streaming audio." "The projected features are consumed by a Qwen3-8B language backbone, whose generated text and hidden states condition discrete S3 speech-token prediction." "A streaming flow-matching decoder converts these tokens into waveform chunks using reference audio from the system prompt (Du et al., 2024b)."

Streaming schedule: "Streaming is organized into one-second units." "Each Realtime-Venus-Omni unit interleaves visual tokens from the current frame with temporally aligned audio features, while each Realtime-Venus-Audio unit contains only audio features." "At each unit, the language model predicts `<|listen|>` or `<|speak|>`. For speaking units, response text is generated and used to condition aligned S3 speech-token generation." "The token `<|chunk_eos|>` closes a speech chunk, while `<|turn_eos|>` marks the end of an assistant turn." "This chunk-wise schedule keeps perception concurrent with speaking and the unspoken continuation revisable, supporting two interaction capabilities: Realtime-Venus-Omni can respond omni-proactively—watching and listening continuously and initiating speech when a new event warrants it—while both models conduct full-duplex conversation, distinguishing backchannels from interruptions to stop, repair, or redirect the unspoken continuation." "These capabilities are supervised by the proactive and full-duplex data in Section 4.5."

## 4.2 Training-Free Long-Video Memory
**Covers:** Sec. 4.2 (construction, retrieval, reassembly)

Motivation: "Streaming audio-visual input grows continuously, while the base model can maintain only a bounded rolling context window." "As a session extends to tens of minutes or even hours, earlier content gradually falls outside the window, making historical information inaccessible to subsequent queries." "We therefore attach an external long-term memory module to the streaming pipeline." "The module requires no additional training or parameter updates and remains decoupled from the fine-tuned dialogue policy."

Memory construction: "Storing the visual representation of every sampled frame would cause the memory size and subsequent retrieval cost to grow continuously over time." "Inspired by the predictive visual coding criterion of AdaCodec (Hou et al., 2026), we introduce a visual memory gating mechanism based on motion-compensated prediction cost." "Each sampled frame is compared with the preceding sampled frame through lightweight block-level motion matching, and the resulting prediction residual and motion cost are used to estimate visual changes between them." "To reduce the risk of discarding short-lived visual events, we further introduce local-change protection and a maximum consecutive-dropping constraint." "The gating mechanism only determines whether a sampled frame is archived into long-term memory and does not affect its normal processing within the short-term context." "Retained frames are stored together with their visual representations and timestamps, while audio is preserved independently and aligned with the video timeline."

Memory retrieval: "Inspired by the MaxSim operator (Khattab and Zaharia, 2020; Wu et al., 2026), the module performs fine-grained matching between query tokens and the visual tokens of each stored historical frame." "For each query token, we take its maximum cosine similarity over the visual tokens within a frame as its token-level matching score." "To emphasize query tokens whose matching scores vary more across historical frames, we compute the median absolute deviation (MAD) of these scores and normalize the resulting values into token weights." "The weighted token-level scores are then aggregated to obtain the semantic relevance score of each frame." "Based on the semantic relevance scores, we first identify a set of candidate frames and rank them by relevance." "For each candidate, we compare it with higher-ranked candidates to estimate its visual novelty." "Inspired by the relevance-diversity principle of Maximal Marginal Relevance (MMR), we combine semantic relevance and visual novelty into a final retrieval score." "These scores are computed once based on the initial relevance ranking and remain fixed during selection." "The highest-scoring candidates are selected as historical evidence, aiming to preserve query-relevant information while reducing redundant visual content."

Context reassembly: "For each retrieved frame, the module retrieves its temporally adjacent audio segments and merges overlapping temporal intervals." "The selected historical frames and their associated audio are then arranged chronologically together with the recent short-term audio-visual window and the current query to form the context for answer generation." "In this way, the model can recover relevant historical information beyond its rolling context window without continuously retaining the complete input history."

## 4.3 Unified stream serialization (start; truncated in chunk)
**Covers:** Sec. 4.3 opening through Fig. 6 caption fragment

"Realtime-Venus-Omni and Realtime-Venus-Audio represent streaming interaction as a sequence of one-second chunks, with temporal boundary `t_k = k s` and chunk `k` covering `[t_{k−1}, t_k)`." "Each chunk aligns three logical streams—the user stream, assistant stream, and background stream—on a shared conversational clock, as illustrated in Figure 6." The chunk then shows Figure 6 fragments (Streaming Whisper, LLM Decoder, Speech Talker, low-latency playback, full-duplex interaction timeline, example user turn "Can you check the latest news right now and tell me whether there have been any major developments in the Israel ?", Video Stream, Audio Stream) and truncates there; no further 4.3 claims are in this chunk.

**Covers:** Sec. 3.2 (Eq. 1) + Fig. 5 + Sec. 4 intro + Sec. 4.1 + Sec. 4.2 + Sec. 4.3 opening (chunk truncates mid-Fig. 6); pp. 6–8 in chunk pagination.
