[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Figure 1: A Capability Taxonomy for Full-Duplex Spoken Dialogue
**In one sentence:** The paper organizes spoken steerability into three families — natural-language steering, acoustic understanding and adaptation, and duplex interaction — connecting what the model says, how it sounds, and how it participates, and motivates SteerBench/SteerDuplex from low baseline audio-steering pass rates.
## Key points
- The taxonomy has three families — natural-language steering, acoustic understanding and adaptation, and general duplex interaction — linking requested content, vocal delivery, and conversational participation.
- Full-duplex systems listen and speak simultaneously, enabling turn taking, backchanneling, and interruption handling; fluent turn taking alone does not guarantee following instructions about tone, persona, or delivery.
- Steerability is defined as "the reliable shift of such behavior in response to user instructions," distinguished from ordinary instruction following per text-model research.
- SteerBench tests requested content and delivery across tone, persona, style/accent, and speed/length with 390 spoken prompts and 1,067 human-authored rubrics using separate text and audio rubrics plus fixed reference clips.
- Under matched items and the same judge, MOSHI and PERSONAPLEX reach audio-steering average pass rates of only 20.55% and 16.44%, respectively.
- Duplex benchmarks assess pauses, interruptions, and backchannels as distinct behaviors, so task compliance and floor management require separate checks alongside intelligibility, timing, and task capability.
- SteerDuplex (built on the public MOSHI backbone) is fine-tuned on recorded conversations plus synthetic speech/text examples covering instruction following, requested delivery, reasoning, safety, and duplex interaction, followed by two-stage RL with programmatic interaction rewards and judge-based transcript rubrics.
---
## Figure 1 caption (verbatim substance)
> "Figure 1. A capability taxonomy for full-duplex spoken dialogue. The taxonomy distinguishes natural-language steering, acoustic understanding and adaptation, and general duplex interaction. Examples are schematic, not model outputs or latency measurements. The taxonomy describes a broader design space than the present benchmark: STEERBENCH tests requested content and delivery across tone, persona, style/accent, and speed/length; AudioMC, VoiceBench, and FDB provide complementary task and interaction evaluations."

## Background: why steerability is separate from fluency
Full-duplex systems listen and speak simultaneously, enabling turn taking, backchanneling, and interruption handling within an ongoing conversation. Early systems established joint two-channel modeling while later work improved synchronization and stream interleaving. Role- and voice-conditioned models make tone, persona, and delivery explicit control inputs. Controllable-generation methods range from explicit control codes to broader adaptation approaches. Speech assessment distinguishes lexical content from speech quality and paralinguistic features, so evaluating control in speech requires acoustic evidence.

## The three families
The chunk states: "We organize spoken steerability into a capability taxonomy (Figure 1). Its three families connect what the model says, how it sounds, and how it participates: natural-language steering, acoustic understanding and adaptation, and duplex interaction."
- What the model says → natural-language steering (requested content).
- How it sounds → acoustic understanding and adaptation (requested delivery, grounded by audio references).
- How it participates → duplex interaction (pauses, interruptions, backchannels, floor management).
The taxonomy guides training and evaluation by assessing requested content and delivery alongside intelligibility, timing, and task capability.

## SteerBench as the taxonomy's measurement
To measure steerability, the paper introduces STEERBENCH: 390 spoken prompts combining concrete tasks with steering requests, assessed with separate text and audio rubrics for content and delivery, with fixed reference clips anchoring the requested acoustic style. Contributions list restates it as 390 spoken prompts and 1,067 human-authored rubrics across tone, persona, style/accent, and speed/length. Baseline result: MOSHI 20.55% and PERSONAPLEX 16.44% audio-steering average pass rates, motivating post-training that preserves general conversational capability.

## How the taxonomy connects to SteerDuplex training (as stated in chunk)
STEERDUPLEX is built on the MOSHI backbone; supervised fine-tuning uses recorded conversations and synthetic speech/text examples covering instruction following, requested delivery, reasoning, safety, and duplex interaction. Continuing from that checkpoint, two-stage RL combines programmatic interaction rewards with judge-based transcript rubrics to optimize sampled speech continuations, with response-continuity and waveform-validity checks, a continuation-duration bonus, and dedicated user-backchannel sampling. Reward design keeps content and delivery separate because text rubrics judge task content while audio-reference rubrics plus timing/waveform checks judge prosody, rate, premature responses, silence, and invalid speech. Related systems cited: PERSONAPLEX (voice/role conditioning), F-ACTOR (supervised instruction-controlled behavior), ASPIRin (speaking decisions vs. token selection), and Ohashi et al. (interaction + semantic rewards).

**Covers:** Figure 1 steerability taxonomy (tone, persona, style, duplex); chunk Sections 1–3.1 context
