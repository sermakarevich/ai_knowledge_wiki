> [[index|Wiki]] | [[summary|Summary]]

# SteerDuplex: Steerable Duplex Speech Dialogue Models — Digest

## 1. [[wiki/01-steerduplex-overview|SteerDuplex Overview: Steerable Duplex Speech Dialogue Models]]

**In one sentence:** SteerDuplex is a Moshi-based full-duplex speech model that adds steerability — reliably shifting tone, persona, speaking rate, and voice style on user instruction — via natural/synthetic dialogue fine-tuning, two-stage RL with hybrid rewards, and a new 390-prompt SteerBench benchmark.

- Full-duplex models already support low-latency turn-taking, interruption handling, and backchanneling, but steerability along tone, persona, speaking rate, and voice style remains underexplored.
- SteerDuplex is a Moshi-based full-duplex speech model fine-tuned on natural conversations plus synthetic dialogues targeting instruction following, vocal delivery, reasoning, and duplex interaction.
- Training adds two-stage reinforcement learning (RL) with hybrid rewards combining verifiable interaction checks and judge-based semantic feedback to improve timing and response continuity.
- Evaluation introduces STEERBENCH: 390 spoken prompts and 1,067 human-authored binary audio and text rubrics spanning tone, persona, style/accent, and speed/length.
- Supervised training improves audio-steering average pass rate by 44.5 percentage points over the strongest evaluated open baseline on STEERBENCH.
- On Audio MultiChallenge, task average pass rate improves by 7 points over its strongest evaluated open baseline.
- RL further raises source-clean interruption response from 72.5% to 82.5% and reduces synthetic pause barge-in from 26.5% to 9%, while steering and aggregate task scores remain comparable or higher.
- Reward probes reveal reward hacking through incomplete responses, showing timing gains must be evaluated alongside response completeness.

## 2. [[wiki/02-capability-taxonomy|Figure 1: A Capability Taxonomy for Full-Duplex Spoken Dialogue]]

**In one sentence:** The paper organizes spoken steerability into three families — natural-language steering, acoustic understanding and adaptation, and duplex interaction — connecting what the model says, how it sounds, and how it participates, and motivates SteerBench/SteerDuplex from low baseline audio-steering pass rates.

- The taxonomy has three families — natural-language steering, acoustic understanding and adaptation, and general duplex interaction — linking requested content, vocal delivery, and conversational participation.
- Full-duplex systems listen and speak simultaneously, enabling turn taking, backchanneling, and interruption handling; fluent turn taking alone does not guarantee following instructions about tone, persona, or delivery.
- Steerability is defined as "the reliable shift of such behavior in response to user instructions," distinguished from ordinary instruction following per text-model research.
- SteerBench tests requested content and delivery across tone, persona, style/accent, and speed/length with 390 spoken prompts and 1,067 human-authored rubrics using separate text and audio rubrics plus fixed reference clips.
- Under matched items and the same judge, MOSHI and PERSONAPLEX reach audio-steering average pass rates of only 20.55% and 16.44%, respectively.
- Duplex benchmarks assess pauses, interruptions, and backchannels as distinct behaviors, so task compliance and floor management require separate checks alongside intelligibility, timing, and task capability.
- SteerDuplex (built on the public MOSHI backbone) is fine-tuned on recorded conversations plus synthetic speech/text examples covering instruction following, requested delivery, reasoning, safety, and duplex interaction, followed by two-stage RL with programmatic interaction rewards and judge-based transcript rubrics.

## 3. [[wiki/03-architecture-training|Architecture and Training]]

**In one sentence:** SteerDuplex jointly generates audio/text streams under a masked system-prompt prefix and trains with SFT followed by two GDPO-based RL stages that reward response continuity and continuation through listener feedback, gated by timing, transcript-judge, and waveform-validity rewards.

- Joint audio/text streams generate at 12.5 Hz after a silent prefix-audio and masked system-prompt prefix, with temporal plus depth transformers predicting text and 8 hierarchical RVQ audio codebooks.
- RL samples continuations from interaction windows (turns, interruptions, pauses, backchannels, noise, speech-mirror scenarios) built from filtered CANDOR material with aligned audio, history, transcripts, timing targets, and grading metadata.
- GDPO normalizes each reward component separately within a rollout group sharing one context before combining with weights, so raw scale cannot dominate and a constant component contributes no signal.
- Stage 1 (response continuity) starts from the SFT checkpoint as frozen KL reference, adds a continuity term (weight 0.5, 4-second first-response target) to discourage short timing-satisfying but non-sustained answers.
- Stage 2 (continuation after listener feedback) re-initializes policy and KL reference from the stage-1 checkpoint, retains continuity, and adds a continuation-duration bonus (weight 2.0, 4-second target) on noise and user-backchannel events with dedicated backchannel sampling.
- Policy loss covers text-stream actions only (including sampled padding tokens for pause/onset timing); audio-codebook actions get no direct policy loss, using an adaptive sampled-action KL penalty instead of exact full-distribution KL.
- RL objective combines interaction timing rewards (weight 1.0), continuity terms, a Gemini 3.6 Flash transcript judge on turn/interruption groups (weight 0.75), and a waveform-integrity gate rejecting silence, clipping, and invalid outputs.
- SFT establishes steering and task capability (65.10 ± 1.13% audio-steering APR; VoiceBench mean 40.87 ± 0.27; FDB-v2 4.17 slow examiner) before RL improves interruption/pause handling.

## 4. [[wiki/04-rl-interruption-results|RL Improves Interruption Response and Pause Handling]]

**In one sentence:** On source-clean and synthetic duplex probes, RL sharply improves when to wait through pauses and when to respond to interruptions, while background-speech recovery, semantic score, and takeover latency show flat or mixed changes.

- Correct response after interruption on source-clean FDB-v1.5 rises from 72.5% to 82.5% with RL (Figure 4).
- Continuation after a user backchannel rises from 71.4% to 80.6%.
- Background-speech recovery changes from 60% to 59%, effectively flat.
- Recovery after speech directed elsewhere rises from 42% to 48%.
- On synthetic pause items, barge-in falls from 26.5% to 9%, a difference of −17.5 percentage points.
- On the synthetic interruption task, response rate rises from 96% to 97.7%, while semantic score changes from 3.94 to 3.88 and mean takeover latency increases by 40 ms.
- The chunk's conclusion is explicit: "Thus better response timing does not imply uniform improvement in every interaction measure."

## 5. [[wiki/05-reward-hacking|Reward Hacking in Duplex Speech]]

**In one sentence:** Duplex timing rewards can be hacked by staying silent or cutting responses short, so speech-gated interruption credit plus continuity rewards reduce but do not eliminate the yielding-vs-continuing conflict.

- A silent model can earn interruption credit without ever yielding, so the design requires speech before the interruption and adds continuity rewards encouraging sustained speech when the user has not taken the floor.
- In separate reward probes (Figure 6), promptness-only optimization attains scalar reward 0.670 but scores zero on the shared duplex diagnostic, leaving 25 of 96 rollouts empty.
- Single-component probes also collapse to empty outputs: text-only leaves 47, audio-rubric-only leaves 41, and audio-quality-only leaves 41 empty rollouts.
- The joint composite improves the duplex score to 0.371 but still leaves 4 empty outputs; Appendix E details these probes, which are separate from the reported interaction RL runs.
- In the second RL stage (Figure 7), interruption reward on natural development conversations rises from 0.450 to 0.793 while continuation after a user backchannel falls from 3.20 to 2.00 seconds and noise-robustness reward declines from 1.96 to 0.77.
- Group normalization balances reward scales, but any component constant within a rollout group supplies no gradient to resist other reward components, consistent with interference between interaction objectives without isolating its mechanism.
- A training-seed replicate reaches 9% synthetic pause barge-in and 4.22 FDB-v2 turn taking, while applying the final reward directly from SFT yields 16.8% and 4.13 with less training, so staging is not isolated.

## 6. [[wiki/06-references|References and Training Appendix (Refs [16]–[40], Appendices A–B)]]

**In one sentence:** This chunk lists references [16]–[40] on controllable generation, duplex benchmarks, and multi-reward RL, then documents SFT/RL training settings (Table 3), reward-weight and compute details, and the start of the evaluation/checkpoint-selection appendix.

- References [16]–[23] cite MO-GRPO (arXiv:2509.22047), CTRL (arXiv:1909.05858), Tülu 3 (arXiv:2411.15124), a controllable-text-generation survey (arXiv:2408.12599), Full-Duplex-Bench v2/v1.5/v1, and GDPO (arXiv:2601.05242).
- References [24]–[32] cite AudioJudge, generative spoken dialogue language modeling (TACL 2023), interactivity alignment in full-duplex speech models, GPT-Realtime docs, rubric-guided self-distillation, PersonaPlex, MMAU, MULTIVOX, and audio hallucination attacks.
- References [33]–[40] cite DeepSeekMath, Qwen3-ASR, policy-aware rubric rewards, synchronous LLMs as full-duplex agents (EMNLP 2024), a full-duplex speech dialogue scheme (NeurIPS 2024), aligning spoken dialogue models from user interactions (ICML 2025), OmniFlatten, and F-Actor.
- SFT uses a Moshi-style 7B backbone on 80 H100 GPUs (batch 8/GPU, global batch 640) for a 3,600-step budget (2.304M draws), with the reported checkpoint at step 2,925 (1.872M draws).
- Both RL stages use component-normalized GDPO with RL lr 5×10−7, KL 0.05/target 0.01 (adaptive, min 0.02, bounded k3 estimator), clip 0.2/grad-clip 1.0, and a response-continuity term (weight 0.5, target 4.0 s); stage 2 adds a continuation-duration bonus (weight 2.0, target 4 s) on noise-robustness and user-backchannel events.
- Reward weights are interactivity 1.0 plus transcript rubric judge 0.75 (Gemini 3.6 Flash); the stage-1 run shows the transcript rubric judge active on turn and interruption strata only, with within-group std 0.14–0.43 and no parse failures in recorded rollouts.
- RL stage 1 ran on four 8×H100-80GB nodes (5.08 h, ~162.7 GPU-h) and stage 2 on one 8×H100-80GB node (4.01 h, ~32.1 GPU-h), excluding queueing, prior setup, benchmark evaluation, and hosted-model compute.
- Evaluation uses Gemini 3.6 Flash for SteerBench/FDB-v2, gpt-5.4-mini (medium reasoning, 3 samples/item for VoiceBench) for AudioMC/VoiceBench/FDB-v1 interruption ratings, and parakeet-tdt-0.6b-v2 for FDB-v1/v2 transcription; checkpoints are frozen on development-set performance alone, and CANDOR pause tasks are flagged diagnostic because 100/216 pause transcripts overlap 96 supervised conversations and official pause clips end only 0.02–0.11 s after the user's last word.

## 7. [[wiki/07-reward-components|Table 4. Reward Components and Evaluation]]

**In one sentence:** The reported RL run (interactivity-v2 with response-continuity term, plus a stage-2 continuation-duration bonus) combines weighted timing, rubric, backchannel, continuity, noise-robustness, and interruption rewards normalized within rollout groups, with waveform integrity as hard validity and safety/capability held out, while retention tables show small capability deltas and control/snapshot tables show staging and judge effects.

- Pause timing, backchannel timing, noise robustness/speech mirror, and interruption yield plus recovery each carry component reward weight 1.0, while turn timing (1.0) pairs with a transcript rubric judge reward (0.75, pre-boundary transcript shown).
- Response continuity for the first response carries weight 0.5 with a 4.0 s target on turn, interruption, paired pause, and paired backchannel groups; stage 2 adds a continuation-duration term with weight 2.0 and 4 s target on noise-robustness and user-backchannel groups.
- Component rewards are normalized within rollout groups; waveform integrity is hard rollout validity, malformed or incomplete judge results invalidate a rollout, and safety plus broad capability (AudioMC / STEERBENCH / VoiceBench) are held-out frozen-checkpoint evaluation.
- Capability retention (Table 5, three-run means ± population SD): AudioMC APR +0.74, ARS +0.80, interruption response +1.67, FDB-v2 safety +0.153, STEERBENCH rubric pass +1.47, VoiceBench overall +0.51, with FDB-v2 mean −0.003 and interruption semantics −0.069.
- RL controls (Table 6, differences vs SFT mean): STEERDUPLEX-RL gives FDB-v2 mean −0.003, turn taking +0.018, VoiceBench +0.505, versus single-stage (−0.177 / −0.050 / −0.363) and training-seed replicate (+0.155 / +0.048 / +0.227); data and training-budget differences prevent single-variable ablation reading.
- Judge sensitivity (Table 7, identical generations): RL-minus-SFT headline mean −0.083 (Gemini 3.6 Flash) and −0.098 (gpt-5.4-mini); second-stage snapshots (Table 8) show training noise-robustness reward 1.96 → 0.77 and development interruption reward 0.450 → 0.793 while continuation after user backchannel falls 3.20 → 2.00 s (SFT reference 2.60 s).
- Isolated single-family probes (Table 9, 96 held-out rollouts each) each leave empty-rollout rate ≥ 26% and duplex-FDB score ≤ 0.055, while the joint composite reaches duplex 0.371 with 4 empty rollouts and MOS 0.631.

## 8. [[wiki/08-text-rubric-judge|Text Rubric Judge (D.4)]]

**In one sentence:** The text rubric judge scores one criterion at a time as "No Issues," "Minor Issues," or "Major Issues," explaining before rating and prioritizing content over delivery polish for speech.

- Scores exactly one criterion at a time on a three-level scale: "No Issues," "Minor Issues," or "Major Issues".
- Explains its decision before giving the rating, and outputs JSON with reasoning placed before the rating.
- Receives criterion metadata (title, category, type, weight, and description) plus the latest user request and the assistant transcript.
- Treats explicit criteria as requiring direct answers, while implicit criteria may be inferred from context.
- Distinguishes objective criteria (factual correctness) from subjective criteria (quality).
- Ignores criterion weights during judging and tolerates minor formatting or phrasing differences.
- For speech, gives content priority over delivery polish.

## 9. [[wiki/09-audio-profile|Audio Profile]]

**In one sentence:** This appendix chunk specifies artifact licenses and use terms, SteerBench composition and synthetic-audio construction, scoring/error rules, and the verbatim user-audio, reference-script, and reference-audio templates including their Audio Profile blocks.

- Table 15 assigns each artifact a role and license: STEERBENCH is a new benchmark under research license released upon acceptance; synthetic SFT data and in-house two-person conversations have restricted redistribution; Fisher English follows LDC User Agreement; Audio MultiChallenge, Full-Duplex-Bench v1/v2, VoiceBench (Apache-2.0), MOSHI (CC BY 4.0), PERSONAPLEX (NVIDIA Open Model License plus CC BY 4.0 additional information), and hosted OpenAI/Google models and judges (gpt-5.4-mini / Gemini 3.6 Flash) follow provider API terms.
- SteerBench contains 100 tone, 136 persona, 104 style/accent, and 50 speed/length prompts, each recording identifiers, steering categories, subcategories, topics, user utterances, and audio/text rubrics that pair an axis with a binary criterion.
- User utterances are rendered as neutral, conversational speech with Gemini 3.1 Flash TTS at 24 kHz, mono, PCM16, with a hash of the item identifier choosing a voice from a fixed pool so assignment is stable.
- Reference scripts are generated by a text model from user request, steering category, and rubrics; saved generation records identify Gemini 3 Pro Preview for original scripts and Gemini 3.1 Pro Preview for repairs, synthesis uses Gemini 3.1 Flash TTS with Gemini 2.5 Flash TTS as fallback, and reference voices are chosen deterministically from Kore and Schedar.
- Text and audio criteria are judged separately with audio decisions conditioned on the fixed reference; items with judge-call errors are excluded from pass-rate denominators and counted, a run with more than 5% such errors is invalid, Audio APR requires all audio criteria for an item to pass, sample APR requires all applicable criteria to pass, and rubric pass rate counts individual decisions.
- Code, STEERBENCH, and checkpoints will be released upon acceptance under a research license, while audio release follows consent and source terms; benchmark test material is excluded from optimization and raw audio is not redistributed without permission.
- The chunk reproduces three literal templates: the user-audio template with Audio Profile "A real human user speaking casually to a voice assistant", the reference-script generator system/user messages with split-specific style rules and strict JSON output, and the reference-audio template with Audio Profile "A helpful and professional personal assistant".

## The argument in five moves

1. Fluent full-duplex turn-taking is not steerability, and baselines prove the gap with only ~16–21% audio-steering pass rates, so the paper defines a three-family taxonomy and builds SteerBench to measure requested content and delivery separately.
2. SteerDuplex answers with Moshi-based SFT on natural plus synthetic steering/duplex data, which supplies the main steerability and task gains (65.10% audio-steering APR; +7 AudioMC APR points).
3. Joint audio/text architecture plus two-stage component-normalized GDPO RL — continuity then continuation-after-feedback, gated by timing, transcript-judge, and waveform checks — refines when to wait, yield, and continue.
4. RL succeeds on targeted interaction probes (interruption response 72.5%→82.5%; pause barge-in 26.5%→9%) while leaving background-speech, semantics, and latency flat or mixed, so timing gains do not imply uniform improvement.
5. Timing rewards invite hacking through silence or truncated responses, so speech-gating plus continuity/continuation terms and joint composite rewards reduce but do not eliminate the yielding-vs-continuing conflict.
6. Retention, control, seed, judge-sensitivity, and overlap analyses qualify the headline: capabilities are broadly retained with small deltas, staging and judge choices matter, and pause-overlap plus scoring rules constrain what the numbers can claim.
