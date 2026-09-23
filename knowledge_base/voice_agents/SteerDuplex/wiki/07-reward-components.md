> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Table 4. Reward Components and Evaluation
**In one sentence:** The reported RL run (interactivity-v2 with response-continuity term, plus a stage-2 continuation-duration bonus) combines weighted timing, rubric, backchannel, continuity, noise-robustness, and interruption rewards normalized within rollout groups, with waveform integrity as hard validity and safety/capability held out, while retention tables show small capability deltas and control/snapshot tables show staging and judge effects.
## Key points
- Pause timing, backchannel timing, noise robustness/speech mirror, and interruption yield plus recovery each carry component reward weight 1.0, while turn timing (1.0) pairs with a transcript rubric judge reward (0.75, pre-boundary transcript shown).
- Response continuity for the first response carries weight 0.5 with a 4.0 s target on turn, interruption, paired pause, and paired backchannel groups; stage 2 adds a continuation-duration term with weight 2.0 and 4 s target on noise-robustness and user-backchannel groups.
- Component rewards are normalized within rollout groups; waveform integrity is hard rollout validity, malformed or incomplete judge results invalidate a rollout, and safety plus broad capability (AudioMC / STEERBENCH / VoiceBench) are held-out frozen-checkpoint evaluation.
- Capability retention (Table 5, three-run means ± population SD): AudioMC APR +0.74, ARS +0.80, interruption response +1.67, FDB-v2 safety +0.153, STEERBENCH rubric pass +1.47, VoiceBench overall +0.51, with FDB-v2 mean −0.003 and interruption semantics −0.069.
- RL controls (Table 6, differences vs SFT mean): STEERDUPLEX-RL gives FDB-v2 mean −0.003, turn taking +0.018, VoiceBench +0.505, versus single-stage (−0.177 / −0.050 / −0.363) and training-seed replicate (+0.155 / +0.048 / +0.227); data and training-budget differences prevent single-variable ablation reading.
- Judge sensitivity (Table 7, identical generations): RL-minus-SFT headline mean −0.083 (Gemini 3.6 Flash) and −0.098 (gpt-5.4-mini); second-stage snapshots (Table 8) show training noise-robustness reward 1.96 → 0.77 and development interruption reward 0.450 → 0.793 while continuation after user backchannel falls 3.20 → 2.00 s (SFT reference 2.60 s).
- Isolated single-family probes (Table 9, 96 held-out rollouts each) each leave empty-rollout rate ≥ 26% and duplex-FDB score ≤ 0.055, while the joint composite reaches duplex 0.371 with 4 empty rollouts and MOS 0.631.
---
## Table 4. Reward components and evaluation roles
**Covers:** Table 4 (interactivity-v2 with response-continuity term; stage 2 adds continuation-duration bonus)

| Component | Weight / role |
|---|---|
| Pause timing | component reward (1.0) |
| Turn timing + transcript rubric judge | component rewards (1.0 timing; 0.75 rubric, pre-boundary transcript shown) |
| Backchannel timing | component reward (1.0) |
| Response continuity (first response) | component term (0.5, target 4.0 s) on turn, interruption, paired pause, and paired backchannel groups |
| Continuation duration (stage 2) | component term (2.0, target 4 s) on noise-robustness and user-backchannel groups |
| Noise robustness / speech mirror | component rewards (1.0) |
| Interruption yield + recovery | component rewards (1.0 each) |
| Waveform integrity | hard rollout validity |
| Malformed or incomplete judge result | invalid rollout |
| Safety and broad capability | held-out evaluation |
| AudioMC / STEERBENCH / VoiceBench | frozen-checkpoint evaluation |

> "Component rewards are normalized within rollout groups; hard validity checks and held-out metrics never substitute for missing reward variation."
## Appendix C.1 Complete retention results (Table 5)
**Covers:** Section C.1 / Table 5 (three runs per model and benchmark; same runs supply every subscore)

| Metric | SFT | + RL | ∆ |
|---|---|---|---|
| AudioMC APR (%) | 13.64±0.28 | 14.38±0 | +0.74 |
| AudioMC ARS (%) | 37.17±1.33 | 37.97±0.44 | +0.80 |
| Interruption response (%) | 96±0.4 | 97.7±0.2 | +1.67 |
| Interruption semantics | 3.94±0.03 | 3.88±0.03 | −0.069 |
| FDB-v2 mean | 4.17±0.02 | 4.17±0.03 | −0.003 |
| FDB-v2 safety | 4.65±0.05 | 4.81±0.05 | +0.153 |
| FDB-v2 turn taking | 4.18±0.13 | 4.19±0.07 | +0.018 |
| FDB-v2 instruction following | 3.67±0.13 | 3.81±0.26 | +0.134 |
| STEERBENCH rubric pass (%) | 63.75±1.59 | 65.22±0.47 | +1.47 |
| VoiceBench overall | 40.87±0.27 | 41.38±0.02 | +0.51 |

Higher is better; bold marks the larger displayed mean, including ties; differences computed before rounding; rates and differences use percentages and percentage points. The synthetic pause probe supplies the continuation needed for the waiting-followed-by-response measurement; the source-clean FDB-v1.5 comparison uses 498 examples.
## Appendix C.2 Training controls (Tables 6–8)
**Covers:** Sections C.2–C.3 / Tables 6–8

Table 6. RL controls (differences between each model's three-run mean and corresponding SFT mean):

| Variant | FDB-v2 mean | FDB-v2 turn taking | VoiceBench |
|---|---|---|---|
| Original timing recipe | -0.115 | -0.244 | +0.049 |
| Stage 1 | +0.107 | -0.140 | +0.444 |
| STEERDUPLEX-RL | -0.003 | +0.018 | +0.505 |
| Training-seed replicate | +0.155 | +0.048 | +0.227 |
| Single-stage | -0.177 | -0.050 | -0.363 |

Table 7. Judge sensitivity (FDB-v2 differences on identical generations from three runs per model; Gemini 3.6 Flash canonical, gpt-5.4-mini low reasoning):

| Comparison | Metric | Gemini | GPT |
|---|---|---|---|
| Stage 1 minus SFT | headline mean | +0.057 | −0.058 |
| Stage 1 minus SFT | per-event turn taking | −0.278 | −0.106 |
| Stage 1 minus SFT | per-event instruction following | −0.065 | −0.009 |
| RL minus SFT | headline mean | −0.083 | −0.098 |
| RL minus SFT | per-event turn taking | −0.074 | −0.059 |
| RL minus SFT | per-event instruction following | −0.124 | +0.001 |

Table 8. Second-stage optimization snapshots (SFT continuation reference 2.60 seconds):

| Measurement | Earlier | Later |
|---|---|---|
| Training noise-robustness reward | 1.96 | 0.77 |
| Development interruption reward | 0.450 | 0.793 |
| Continuation after user backchannel (s) | 3.20 | 2.00 |

- The original-recipe control starts from SFT with the original interaction recipe and no continuity additions; stage 1 starts from SFT with continuity weight 0.5 and a 4-second target, and its trained checkpoint initializes stage 2.
- Stage 2 adds a continuation bonus (weight 2.0, target 4 seconds) and dedicated user-backchannel sampling; the single-stage variant applies the final reward directly from SFT with a smaller training budget; the training-seed replicate changes the random seed of the reported configuration.
- "These controls differ in training budget and, for the original recipe, additional configuration choices, so they do not isolate every reward component."
- "Training and development observations were recorded separately within one run; no intermediate measurements or confidence intervals are available."
## Appendix D. Prompts and judges (Table 9)
**Covers:** Sections D.1–D.3 / Table 9 (96 held-out sampled rollouts per condition)

| Probe | Scalar↑ | Empty/96↓ | Duplex↑ | MOS↑ |
|---|---|---|---|---|
| Text-rubric only | 0.329 | 47 | 0.055 | 0.512 |
| Audio-rubric only | 0.336 | 41 | 0.000 | 0.571 |
| Audio-quality only | 0.522 | 41 | 0.000 | 0.561 |
| Promptness only | 0.670 | 25 | 0.000 | 0.626 |
| Joint composite probe | 0.554 | 4 | 0.371 | 0.631 |

Scalar rewards use different objectives; every isolated probe leaves the empty-rollout rate ≥ 26% and the duplex-FDB score at or near zero (≤ 0.055).

Training-time system prompt (prepended to the agent-text channel of every RL rollout):
> "You are a helpful full-duplex voice assistant. Your voice and identity are fixed. Stay kind, safe, and constructive. Follow the user's spoken instructions about tone, persona flavor, speaking style, speed, and length when those instructions are allowed."

Shared inference/benchmark assistant prompt:
> "You are a helpful voice assistant. Your voice and identity are fixed. Listen carefully, follow the user's instructions, and respond naturally."

For multi-turn RL scenarios with stitched user audio, the system prompt includes a plain "Conversation so far" transcript alternating user and assistant lines, marking assistant-generated text and ending with the latest user turn, which the model is instructed to respond to using the preceding context. Per-scenario steering instructions are inserted on the user side via the dialogue history.

Reference-audio rubric judge (receives Audio 1 target style, Audio 2 model output, plus transcripts; returns per-criterion JSON scores):
> "You are judging audio steerability for a full-duplex voice assistant. Audio 1 is the reference target. Audio 2 is the model-generated answer. Compare delivery / style / prosody / speaking rate / articulation / affect against the reference. Do NOT require identical speaker timbre or voice identity unless the rubric explicitly asks for it. Use the transcript only to verify content; judge audio qualities from the audio."

Benchmark judge (daily, correction, safety, entity-tracking, factual, AudioMC with per-task rubric daily/correction/entity-tracking/safety/alpaca/factual/ifeval/default):
> "You judge spoken-assistant transcripts. Given the user's request, any scenario-specific rubric, and the assistant's transcript, FIRST write a ONE-SENTENCE explanation of how the assistant performed (referencing concrete details from the transcript), THEN give a 1..5 integer score (5 = best)."
> "Be calibrated. A typical OK-but-imperfect response is a 3. A 5 requires the response to actually accomplish the task as a competent human would. Always reason FIRST, score AFTER - never invert the order."

**Covers:** Table 4 reward roles, Tables 5–9, Sections C.1–C.3 and D.1–D.3 as present in chunk 07 (pp. 16–18)
