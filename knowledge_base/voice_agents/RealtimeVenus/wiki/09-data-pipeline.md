> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 6.1 Unified Data Construction
**In one sentence:** As illustrated in Figure 8, unified data construction builds full-duplex interaction data through a three-stage pipeline — scenario and interaction planning, paralinguistic and acoustic realization, and temporal alignment with model-specific materialization.
## Key points
- The pipeline contains exactly three stages: scenario and interaction planning, paralinguistic and acoustic realization, and temporal alignment with model-specific materialization.
- Each session begins with a structured scenario seed specifying setting, participants, user goal, language profile, acoustic environment, and target interaction conditions, expanded into an event-level plan covering semantic progression, speaker and addressee, floor ownership, and whether each event preserves or changes the active user intent.
- Compositional sampling covers daily communication, information seeking, collaborative tasks, decision making, service interactions, and multi-party conversations, including ordinary turn-taking plus pauses, backchannels, interruptions, corrections, other-directed speech, and background speech.
- Planned turns are converted into speech and arranged on the session timeline by intended boundaries and overlaps, with hesitation, filled pauses, repetition, self-correction, incomplete utterances, laughter, and breathing added for realism and turn-taking cues.
- Foreground dialogue is mixed with scene-matched secondary speakers and environmental audio with varied event onset and duration to produce different overlap conditions, covering Chinese, English, and code-switching.
- Audio, video, text, and system actions are mapped to a common monotonic session clock (shared session clock shown spanning 00:00–00:10), with audio–visual instances synchronizing composed audio with video while retaining interaction structure and delegation annotations.
- Figure 8 reports corpus scale of ≈72,200 total corpus sessions and ≈1,600 h aligned audio, split ≈36,100 Chinese sessions and ≈36,100 English sessions under "One trajectory, two training modalities" with "SHARED SUPERVISION" for AUDIO-ONLY (RT-Venus-Audio) and AUDIO-VISUAL (RT-Venus-Omni).
---
## Scenario and interaction planning
**Covers:** Section 6.1, stage 1 (Figure 8, column 1)

Each session begins with a structured scenario seed specifying the setting, participants, user goal, language profile, acoustic environment, and target interaction conditions. The seed is expanded into an event-level plan that determines "the semantic progression, speaker and addressee, floor ownership, and whether each incoming event preserves or changes the active user intent."

Compositional sampling covers:

| Sampling dimension | Values in chunk |
|---|---|
| Task domains | daily communication, information seeking, collaborative tasks, decision making, service interactions, multi-party conversations |
| Interaction phenomena | ordinary turn-taking, pauses, backchannels, interruptions, corrections, other-directed speech, background speech |
| Plan event types (Fig. 8) | request, backchannel, overlap, correction, pause, laugh, breath |

## Paralinguistic and acoustic realization
**Covers:** Section 6.1, stage 2 (Figure 8, column 2)

Planned turns are converted into speech and arranged on the session timeline according to their intended boundaries and overlaps. Paralinguistic additions verbatim: "Hesitation, filled pauses, repetition, self-correction, incomplete utterances, laughter, and breathing are added to improve conversational realism and expose cues relevant to turn-taking."

Foreground dialogue is mixed with scene-matched secondary speakers and environmental audio, with event onset and duration varied to produce different overlap conditions. Language coverage: "The corpus covers Chinese, English, and code-switching." For audio–visual instances, "the composed audio is synchronized with the associated video while retaining the interaction structure and delegation annotations specified by the plan."

## Temporal alignment and materialization
**Covers:** Section 6.1, stage 3 (Figure 8, column 3; chunk text truncates here)

"Temporal alignment and materialization. Audio, video, text, and system actions are mapped to a common monotonic session clock. Each event records its source, temporal span, conversational" — [chunk text ends mid-sentence at this point; remainder unavailable].

Figure 8 timeline details present in chunk:

| Lane | Content shown |
|---|---|
| USER / ASSISTANT / BACKGROUND AUDIO / VIDEO | Aligned session lanes under "Shared session clock" (00:00–00:10) |
| Annotated events | Backchannel, Other-directed, Interruption, Correction |
| Output branches | "One trajectory, two training modalities": AUDIO-ONLY → "RT-Venus-Audio", AUDIO-VISUAL → "RT-Venus-Omni", under "SHARED SUPERVISION" |

Corpus scale from Figure 8 (exact strings):

| Metric | Value |
|---|---|
| total corpus sessions | ≈72,200 |
| aligned audio | ≈1,600 h |
| Chinese sessions | ≈36,100 |
| English sessions | ≈36,100 |

Quality-control and supervision labels visible in Figure 8: "Media / Temporal", "Semantic / Interaction", duplex behavior "CONTINUE / HOLD / YIELD / STOP / RECOVER" (keep speaking, wait for input, give the floor, stop queued audio, resume/revise), delegate behavior "Routing / Coordination / Recovery" with "Retain · Cancel", "Bounded retry · Clarification", "Revise · Reconcile", "Degraded response · Fallback".
