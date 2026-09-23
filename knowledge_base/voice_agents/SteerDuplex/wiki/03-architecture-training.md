> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Architecture and Training
**In one sentence:** SteerDuplex jointly generates audio/text streams under a masked system-prompt prefix and trains with SFT followed by two GDPO-based RL stages that reward response continuity and continuation through listener feedback, gated by timing, transcript-judge, and waveform-validity rewards.
## Key points
- Joint audio/text streams generate at 12.5 Hz after a silent prefix-audio and masked system-prompt prefix, with temporal plus depth transformers predicting text and 8 hierarchical RVQ audio codebooks.
- RL samples continuations from interaction windows (turns, interruptions, pauses, backchannels, noise, speech-mirror scenarios) built from filtered CANDOR material with aligned audio, history, transcripts, timing targets, and grading metadata.
- GDPO normalizes each reward component separately within a rollout group sharing one context before combining with weights, so raw scale cannot dominate and a constant component contributes no signal.
- Stage 1 (response continuity) starts from the SFT checkpoint as frozen KL reference, adds a continuity term (weight 0.5, 4-second first-response target) to discourage short timing-satisfying but non-sustained answers.
- Stage 2 (continuation after listener feedback) re-initializes policy and KL reference from the stage-1 checkpoint, retains continuity, and adds a continuation-duration bonus (weight 2.0, 4-second target) on noise and user-backchannel events with dedicated backchannel sampling.
- Policy loss covers text-stream actions only (including sampled padding tokens for pause/onset timing); audio-codebook actions get no direct policy loss, using an adaptive sampled-action KL penalty instead of exact full-distribution KL.
- RL objective combines interaction timing rewards (weight 1.0), continuity terms, a Gemini 3.6 Flash transcript judge on turn/interruption groups (weight 0.75), and a waveform-integrity gate rejecting silence, clipping, and invalid outputs.
- SFT establishes steering and task capability (65.10 ± 1.13% audio-steering APR; VoiceBench mean 40.87 ± 0.27; FDB-v2 4.17 slow examiner) before RL improves interruption/pause handling.
---
## Architecture (Figure 2)
**Covers:** Figure 2 (a)–(d)

Masked system-prompt prefix conditions joint audio/text streams: user acoustic, user semantic, agent acoustic, agent semantic, and agent text streams, with 300 s context and silent prefix audio with joint generation at 12.5 Hz. Temporal and depth transformers predict hierarchical audio codes (8 hierarchical RVQ codebooks); text plus audio codes are predicted with waveform-validity checks for silence, clipping, and invalid audio.

Verbatim caption: "Figure 2. SteerDuplex architecture and training. (a) A masked system-prompt prefix conditions joint audio/text streams. (b) Temporal and depth transformers predict hierarchical audio codes. (c) Grouped continuations receive component-normalized rewards and waveform validity checks. (d) SFT initializes RL stages rewarding response continuity, then continuation after listener feedback. Each RL stage freezes its initial model as the KL reference."

Training flow per panel (d): "SFT followed by hybrid RL" — supervised fine-tuning on natural conversations plus requested steering, RL stage 1 on semantic response plus timing plus continuity, RL stage 2 on continuation after listener feedback; depth-transformer rollout groups are normalized within groups then combined.

## Two-stage reinforcement learning
**Covers:** Section 3.2

GDPO update (Eq. 1):

| Symbol | Meaning per chunk |
|---|---|
| Rᵢ⁽ᵏ⁾ | reward component k for rollout i |
| Âᵢ | combined advantage: Σₖ wₖ (Rᵢ⁽ᵏ⁾ − mean(R⁽ᵏ⁾)) / (std(R⁽ᵏ⁾) + ε) |

Stage 1 response continuity: weight 0.5, 4-second first-response target; stage 2 continuation after listener feedback: weight 2.0, 4-second target on noise and user-backchannel events. Moshi's temporal transformer "processes joint audio/text history and supplies both text logits and the representation used by the audio decoder, so text-action gradients can change subsequent speech generation." Sampled padding tokens are included because "they encode frames without a new text token, making their timing relevant to pauses and speech onset; excluding them would remove credit from these decisions."

## Rewards and audio validity
**Covers:** Section 3.3

Weights: interaction timing 1.0, continuity terms as above, Gemini 3.6 Flash transcript judge 0.75 on turn and interruption groups, plus waveform-integrity gate. Timing rewards distinguish responding, yielding, waiting, and continuing; interruption credit requires assistant speech before the interruption, preventing silence from earning yielding credit. Reference-audio rubrics (requested delivery, prosody, rate, articulation, naturalness, task success; speaker identity only when explicitly requested) evaluate steerability but "do not enter the reported RL objective."

## SteerBench and evaluation setup
**Covers:** Sections 4–5

SteerBench: 390 prompts across tone, persona, style/accent, speed/length with 1,067 human-authored binary rubrics (438 audio, 629 text), disjoint from training; audio-in/audio-out inference under shared system prompt. Aggregation levels: audio-steering APR (% examples passing every applicable audio rubric), sample APR (additionally every text rubric), rubric pass rate (mean of binary decisions). SFT results: 65.10 ± 1.13% audio-steering APR vs 20.55% MOSHI and 16.44% PERSONAPLEX; sample APR 32%–51.11%; rubric pass rates 63.10%–77.03%. Category sample vs rubric rates: tone 49.7 / 71.5, persona 51.1 / 77, style/accent 48.4 / 69.8, speed/length 32 / 63.1.

Evaluation: Audio MultiChallenge, VoiceBench, Full-Duplex-Bench (FDB-v1 single events, v1.5 interruption/overlap, v2 multi-turn sessions) vs MOSHI and PERSONAPLEX; repeated runs report means and population SDs across three decodes. Source overlap: some FDB-v1 turn-taking/pause examples reuse CANDOR training conversations (diagnostic only); generalization via FDB-v2, the 498-example FDB-v1.5 split without Fisher/CANDOR, and source-clean synthetic interruption/pause/backchannel tasks. Checkpoint selected on a separate dev set and frozen before test evaluation.

## Multi-turn and spoken capability (SFT reference)
**Covers:** Section 6–6.1

Supervised model: Audio MultiChallenge 13.64 ± 0.28% APR and 37.17 ± 1.33% ARS vs 6.64% / 20.56% for PERSONAPLEX; FDB-v2 4.17 (slow examiner) vs MOSHI 2.59 and PERSONAPLEX 2.65; VoiceBench mean 40.87 ± 0.27 vs MOSHI 38.55 and PERSONAPLEX 30.51.
