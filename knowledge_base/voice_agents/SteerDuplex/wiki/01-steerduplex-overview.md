> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# SteerDuplex Overview: Steerable Duplex Speech Dialogue Models

**In one sentence:** SteerDuplex is a Moshi-based full-duplex speech model that adds steerability — reliably shifting tone, persona, speaking rate, and voice style on user instruction — via natural/synthetic dialogue fine-tuning, two-stage RL with hybrid rewards, and a new 390-prompt SteerBench benchmark.

## Key points

- Full-duplex models already support low-latency turn-taking, interruption handling, and backchanneling, but steerability along tone, persona, speaking rate, and voice style remains underexplored.
- SteerDuplex is a Moshi-based full-duplex speech model fine-tuned on natural conversations plus synthetic dialogues targeting instruction following, vocal delivery, reasoning, and duplex interaction.
- Training adds two-stage reinforcement learning (RL) with hybrid rewards combining verifiable interaction checks and judge-based semantic feedback to improve timing and response continuity.
- Evaluation introduces STEERBENCH: 390 spoken prompts and 1,067 human-authored binary audio and text rubrics spanning tone, persona, style/accent, and speed/length.
- Supervised training improves audio-steering average pass rate by 44.5 percentage points over the strongest evaluated open baseline on STEERBENCH.
- On Audio MultiChallenge, task average pass rate improves by 7 points over its strongest evaluated open baseline.
- RL further raises source-clean interruption response from 72.5% to 82.5% and reduces synthetic pause barge-in from 26.5% to 9%, while steering and aggregate task scores remain comparable or higher.
- Reward probes reveal reward hacking through incomplete responses, showing timing gains must be evaluated alongside response completeness.

---

## Abstract

> "Full-duplex spoken dialogue models support low-latency turn taking, interruption handling, and backchanneling, yet a key capability remains underexplored: steerability, the ability to reliably shift conversational behavior along attributes such as tone, persona, speaking rate, and voice style in response to user instructions."

- Introduces a taxonomy of text- and audio-based steerability identifying substantial gaps in current full-duplex models.
- Contribution: S TEER D UPLEX, a Moshi-based full-duplex speech model fine-tuned on natural conversations and synthetic dialogues targeting instruction following, vocal delivery, reasoning, and duplex interaction.
- Contribution: two-stage RL with hybrid rewards (verifiable interaction checks + judge-based semantic feedback).
- Contribution: S TEER B ENCH benchmark with 390 spoken prompts and 1,067 human-authored binary audio and text rubrics spanning tone, persona, style/accent, and speed/length.
- Paper metadata: arXiv:2609.12623v1 [cs.AI] 11 Sep 2026; Scale AI (1) and University of Maryland (2); equal-contribution authors Utkarsh Tyagi and Ramaneswaran Selvakumar; project lead Utkarsh Tyagi; contact utkarsh.tyagi@scale.com; code at https://github.com/Utkarsh4430/SteerDuplex.

## Introduction

> "Spoken dialogue conveys emotion, accent, and timing cues that text transcripts alone do not preserve."

- End-to-end models process acoustic information directly, but useful conversational partners must also manage when to speak and follow instructions about content and vocal delivery.

## Capability taxonomy preview (Figure 1, as captured in this chunk)

| Pillar | Sub-capability | Example |
|---|---|---|
| 1 Text-based steerability | Tone Control | "Be sarcastic for the rest of this call." → "Sure, adopting a sarcastic tone for the remainder of our conversation." |
| 1 Text-based steerability | Persona Control | "You are a 70-year-old retired literature professor." → "Ah, an excellent question. Let us consider the nuances of the text carefully." |
| 1 Text-based steerability | Speed & Length Control | "One-sentence answers only, please." → "Quantum entanglement is correlated particle behavior." |
| 1 Text-based steerability | Dynamic Mid-Conv. Steering | "(mid-conv) Be more empathetic - having a bad day." → "Sorry to hear. I will adapt my tone to be more supportive." |
| 1 Text-based steerability | Graceful Refusal / Failure | "Now speak as a man." → "Can't change my voice mid-conv., but I can still help." |
| 2 Audio-based steerability | Paralinguistic Understanding | "(User sighs heavily)" → "You sound stressed. Want to talk about it?" |
| 2 Audio-based steerability | Speech Understanding from Acoustics | "(User whispers)" → "You're speaking softly, I'll whisper back to match." |
| 2 Audio-based steerability | Voice / Style Editing | "Speak louder, I'm in a noisy room." → "(Speaks louder)" |
| 2 Audio-based steerability | Audio-Context Memory | "What was my flight number again?" → "Your flight number is UA 1247." |
| 2 Audio-based steerability | Self-Coherence Over Audio | "(User interrupts multiple times, changes topics)" → "(Continues in the same voice and tone)" |
| 3 General duplex capabilities | Turn-Taking | "(User finishes)" → "(Responds within ~500 ms)" |
| 3 General duplex capabilities | Graceful Interruption Handling | "(User interrupts)" → "(Stops speaking immediately)" |
| 3 General duplex capabilities | Backchanneling | "(User speaking…)" → "Mm-hmm, I see." |
| 3 General duplex capabilities | Pause Handling | "(Long pause)" → "Take your time." |
| 3 General duplex capabilities | Mid-Utterance Corrections | "Set an alarm for 7 — no wait, 8 AM." → "Okay, alarm set for 8 AM." |

**Covers:** Abstract + Section 1 Introduction (opening) + Figure 1 taxonomy preview, arXiv:2609.12623v1
