> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Component-wise training. The full-duplex STT backbone
**In one sentence:** The full-duplex STT backbone and streaming TTS model are trained independently with audio-codec prediction disabled, then a frozen-encoder RNN-T transcription branch is attached, using weighted agent-text/function-channel losses plus inference-time filler, endpointing, and runtime enhancements.
## Key points
- Full-duplex backbone and streaming TTS model are trained independently: direct audio-codec prediction is disabled in CPT/SFT (audio-loss weight 0.0) and agent speech is synthesized by the separately trained VoiceChat-TTS decoder, so no gradients flow between backbone and TTS.
- After backbone training, RNN-T prediction (decoder) and joint networks are attached to the shared cache-aware streaming speech encoder; the speech encoder, LLM backbone, agent-text head, function head, and TTS model are frozen and only the RNN-T prediction and joint networks are optimized with standard transducer loss for user transcription.
- STT loss is `ℒSTT = (1 − λT2T)(λtext ℒtext + λFC ℒFC) + λT2T ℒT2T`: SFT uses λtext = 1.0, λFC = 1.0, λT2T = 0.5 (ℒSTT = 0.5(ℒtext + ℒFC) + 0.5ℒT2T); CPT uses λtext = 3.0, λFC = 1.0, λT2T = 0.0 (ℒCPT = 3ℒtext + ℒFC), with the CPT function channel supervised to predict padding despite no tool-calling examples.
- Token-weighted cross-entropy uses SFT agent-text weights 12.5 (beginning-of-turn), 7.5 (end-of-turn), 5.0 (text content), 1.0 (padding) and CPT weights 10.0, 10.0, 1.0, 0.5; function-channel SFT weights are 64.0 (`<TOOLCALL>` content), 6.0 each (`<SOTC>`, `<EOTC>`), 3.0 (`<EOTR>`), 0.3 (padding), with the function mask zero on injected tool-response tokens.
- Optimization runs on 64 GPUs (8 nodes × 8 GPUs) with full data parallelism and bf16 precision, AdamW (β1 = 0.9, β2 = 0.98, zero weight decay), learning rate 5 × 10⁻⁵ with inverse-square-root schedule, 2,500 warmup steps, minimum 5 × 10⁻⁶, and gradient clipping 2.0 (CPT) / 5.0 (SFT).
- Inference-time enhancements in the chunk are per-tool filler messages that mask tool latency, an RNN-T-transcript endpointing fallback that force-injects BOS/EOS tokens for turn start/barge-in stop, and an optimized low-latency real-time inference runtime (details in Appendix B).
- On Full-Duplex-Bench 1.0 the chunk's Table 1 / text reports V-Model at 15.3% synthetic and 25.5% CANDOR pause TOR, 81.5% smooth-turn TOR (448 ms latency), 100% user-interruption TOR (480 ms latency) with 4.33/5 GPT-4o response quality; on FDB 1.5 user-backchannel it reports 93% Resume vs 80% Freeze-Omni and 70% GPT-4o Realtime.
---
## Component-wise training strategy
**Covers:** Section 3 opening (component-wise training)

The chunk states:

> "Component-wise training. The full-duplex STT backbone and streaming TTS model are trained independently. We first optimize the full-duplex backbone through CPT and SFT to predict the agent-text and function channels from streaming user speech."

Mechanisms named in the chunk:

- Direct audio-codec prediction is disabled in these stages (audio-loss weight 0.0); agent speech is instead synthesized by the separately trained VoiceChat-TTS decoder described in Section 2.3.
- "Consequently, gradients are not propagated between the full-duplex backbone and TTS model."
- After backbone training, "we attach the RNN-T prediction (decoder) and joint networks to the shared cache-aware streaming speech encoder."
- "We freeze the speech encoder, LLM backbone, agent-text head, function head, and TTS model, and optimize only the RNN-T prediction and joint networks using the standard transducer loss for user transcription."
- "At inference time, the independently trained full-duplex backbone, RNN-T branch, and TTS model operate together as the system shown in Figure 1."

## 3.2 Training details — objective
**Covers:** Section 3.2, Training objective, equations (1)–(2)

Loss combination (equation 1, verbatim):

> "ℒSTT = (1 − λT2T) (λtext ℒtext + λFC ℒFC) + λT2T ℒT2T."

Hyperparameters (verbatim):

- "For SFT, λtext = 1.0, λFC = 1.0, and λT2T = 0.5, giving ℒSTT = 0.5(ℒtext + ℒFC) + 0.5ℒT2T."
- "For CPT, λtext = 3.0, λFC = 1.0, and λT2T = 0.0, giving ℒCPT = 3ℒtext + ℒFC."
- "Although CPT contains no tool-calling examples, the function channel is supervised to predict padding, discouraging spurious tool activation."

Token-weighted cross-entropy (equation 2, verbatim form in chunk):

> "ℒc = −(1/N) Σt mₜ⁽ᶜ⁾ w_c(yₜ⁽ᶜ⁾) log pθ(yₜ⁽ᶜ⁾ | hₜ), c ∈ {text, FC}."

Channel weights (verbatim):

- "For the agent-text channel, the SFT weights are 12.5 for beginning-of-turn, 7.5 for end-of-turn, 5.0 for text content, and 1.0 for padding; the corresponding CPT weights are 10.0, 10.0, 1.0, and 0.5."
- "For the function channel, the SFT weights are 64.0 for `<TOOLCALL>` content, 6.0 each for `<SOTC>` and `<EOTC>`, 3.0 for `<EOTR>`, and 0.3 for padding."
- "The function mask mₜ⁽ᶠᶜ⁾ is zero on injected tool-response tokens, so those tokens provide context without contributing loss."
- "Upweighting the sparse boundary and content tokens teaches turn-taking and the complete tool protocol, while the padding losses discourage emissions on inactive output channels."
- "The RNN-T and TTS objectives are optimized separately and are not included in ℒSTT."

## 3.2 Training details — optimization
**Covers:** Section 3.2, Optimization

Exact settings from the chunk:

- "Both CPT and SFT are performed on 64 GPUs (8 nodes with 8 GPUs each) using full data parallelism and bf16 precision."
- "We use AdamW with β1 = 0.9, β2 = 0.98, zero weight decay, and a learning rate of 5 × 10⁻⁵."
- "The learning rate follows an inverse-square-root schedule with 2,500 warmup steps and a minimum value of 5 × 10⁻⁶."
- "The gradient-clipping threshold is 2.0 during CPT and 5.0 during SFT."

## 4. Inference-time enhancements
**Covers:** Section 4 (Filler messages, Improved turn-taking, Optimized Inference)

Filler messages during tool calling (verbatim rationale):

> "We have chosen a practical solution to ensure the voice agent does not remain silent, potentially for a long time, when tools are being called."

Mechanism in the chunk:

- "For each tool a specific filler message can be defined that will be spoken by the agent as soon as the LLM generates the text that will trigger the tool call and response."
- "This message needs to be defined along with the tool specification in the system prompt, following the example given in Section D.1 of the appendix."
- "Such messages can be defined such that their duration 'masks' the delay that would be experienced by the user while the tool response is being generated."
- "For fast executing tools with short responses, they can be completely skipped. For tools with long execution time and long responses they should be long enough. A trade-off is needed in-between."

Improved turn-taking (verbatim mechanism):

> "When the model fails to natively handle turn-taking/barge-in scenarios, we introduce a simple endpointing mechanism as a fallback, using the RNN-T transcript output."

- "A set of heuristics based on user speech/silence activity is combined with the current response generation state, to forcefully inject BOS/EOS tokens into the model."
- "This helps to steer the model to start a new turn or stop in case of user barge-in."

Optimized inference:

> "We designed an optimized inference runtime for low-latency, real-time conversation, whose details can be found in Appendix B."

## 5. Experiments & Results — turn management (Table 1, FDB 1.0 / 1.5)
**Covers:** Section 5 opening, Table 1, Turn-taking discussion, Table 2 header

Evaluation framing (verbatim): "We evaluate NemotronLabs VoiceChat across complementary dimensions. Full-Duplex-Bench v1 [26] and v1.5 [27] assess real-time turn management; VoiceBench [28] measures single-turn response intelligence; and Full-Duplex-Bench v3 [29] evaluates tool calling under naturalistic speech conditions."

Table 1 as given in the chunk (behavioral rates in percent, latency in seconds, GPT-4o quality 0–5; TOR = Takeover Rate):

| Model | Pause TOR synth. (↓) | Pause TOR CANDOR (↓) | Smooth-turn TOR (↑) | Smooth latency s (↓) | Interruption TOR (↑) | Response quality GPT-4o (↑) | Interruption latency s (↓) |
|---|---|---|---|---|---|---|---|
| Moshi | 98.5 | 98.0 | 94.1 | 0.265 | 100.0 | 0.77 | 0.257 |
| Freeze-Omni | 64.2 | 48.1 | 33.6 | 0.953 | 86.7 | 3.62 | 1.409 |
| PersonaPlex | 35.8 | 43.1 | 90.8 | 0.170 | 95.0 | 4.29 | 0.240 |
| MoshiRAG† | 32.0 | 56.0 | 83.0 | 0.180 | 85.0 | 3.75 | 1.020 |
| V-Model | 15.3 | 25.5 | 81.5 | 0.448 | 100.0 | 4.33 | 0.480 |
| Gemini Live 2.0 | 25.5 | 31.0 | 65.5 | 1.301 | 89.1 | 3.38 | 1.183 |
| GPT-Realtime | 1.0 | 12.0 | 100.0 | 1.470 | 97.0 | 3.85 | 1.500 |

Table notes in chunk: "Moshi, Freeze-Omni, Gemini Live, and GPT-Realtime scores are from the public FDB results. Gemini Live 2.0 denotes the gemini-2.0-flash-live-001 endpoint. PersonaPlex denotes the publicly released checkpoint evaluated by its authors [10]. MoshiRAG† scores are reported by its authors [15]; this separate evaluation was not part of the controlled FDB run."

Turn-taking protocol definitions in the chunk:

- FDB 1.0 pause tracks measure whether a model refrains from taking the floor during within-turn pauses (synthetic + CANDOR); lower TOR preferred.
- Smooth-turn-taking measures whether the model takes the floor after the user completes a turn (higher TOR preferred).
- User-interruption measures whether the model takes the turn after interruption, latency, and GPT-4o-scored post-interruption quality (coherence, relevance, adaptability, 0–5).
- FDB 1.5 user-backchannel ("uh-huh" while model speaks) is classified Respond / Resume / Uncertain / Unknown; "Resume is therefore the desired outcome."

Headline comparisons stated in the chunk:

- "Among the reported open-weight systems, V-Model achieves the lowest FDB 1.0 pause-handling TOR on both the synthetic (15.3%) and CANDOR (25.5%) subsets."
- "It also reaches a 100% user-interruption TOR and the highest response-quality score (4.33) in the comparison."
- "Its smooth-turn TOR is 81.5%, with smooth-turn and interruption latencies of 448 and 480 ms, respectively."
- "PersonaPlex, however, achieves a higher smooth-turn TOR (90.8% versus 81.5%) and lower latency (170 versus 448 ms)."
- "On the FDB 1.5 user-backchannel condition, V-Model achieves the highest Resume rate among the open-weight baselines: its 93% rate exceeds the next-best result, Freeze-Omni's 80%, by 13 percentage points, while it responds unnecessarily in only 1% of examples."
- "Relative to closed-API systems, V-Model outperforms Gemini Live 2.0 on every reported FDB 1.0 metric, including lower smooth-turn and interruption latencies by 853 and 703 ms, respectively."
- "GPT-Realtime achieves lower pause TOR and higher smooth-turn TOR, whereas V-Model responds faster and obtains higher user-interruption TOR and response quality."
- "On the FDB 1.5 user-backchannel condition, V-Model exactly matches Gemini Live 2.0 across all four behavior categories."
- "Compared with GPT-4o Realtime, it achieves a higher Resume rate (93% versus 70%) and a lower Unknown rate (4% versus 25%)."

Table 2 header present in chunk: "Table 2 | FDB 1.5 behavioral response distribution for the user-backchannel condition. Values are percentages. A listener backchannel does not claim the floor, so Resume is the desired behavior." (Row values cut off in this chunk.)

**Covers:** Component-wise training intro, Section 3.2 (training objective + optimization), Section 4 (inference-time enhancements), Section 5 opening with Table 1 and FDB 1.0/1.5 turn-taking discussion (V-Model numbers as above).
