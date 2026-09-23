> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction
**In one sentence:** Existing benchmarks test whether a voice model stops when interrupted, but this paper targets what it says next — recovering a structured workflow after mid-sentence barge-ins.
## Key points
- Real-time voice agents (GPT Realtime, Gemini, Moshi) are moving to production in customer service, healthcare, and enterprise workflows, where interruption (corrections, impatience, topic switches, backchannels like "mm-hm") is the norm, not an edge case.
- Existing benchmarks (Full-Duplex-Bench, FLEXI topic-shift score, SID-Bench semantic detection, HumDial respond/resume) answer whether the model detects and reacts to an interruption in real time: stopping, yielding the floor, distinguishing backchannels.
- The unanswered question is post-interruption recovery: e.g. an insurance-claim agent cut off mid-sentence by "Actually, it was my work address, not home" must (1) stop, (2) recognize a correction, (3) integrate it, (4) not repeat already-heard content, and (5) resume at the correct workflow step — existing benchmarks cover only step (1).
- Failure modes differ qualitatively: failing to stop yields awkward but recoverable overlap, while stopping correctly but re-reading the whole sentence, ignoring the correction, or losing workflow place creates a fundamentally broken interaction.
- Current models, including frontier ones, show gaps invisible to existing benchmarks: all evaluated GPT-family audio models continue correctly after a backchannel less than a third of the time (filler pass rate 7%–31%), Gemini 2.5 is markedly better (62%–68%) while the newer Gemini 3.x line regresses sharply (13%–32%).
- The authors frame these as undertrained rather than inherently difficult behaviors, so targeted evaluation surfaces actionable training gaps, with degradation-by-depth, audio-vs-text modality, judge-agreement, and AudioMultiChallenge comparison verified in Section 5.
- Contributions: define post-interruption recovery as a distinct axis (six interruption types, two-axis scoring via LLM judges with type-specific criteria); introduce IHBench (synthetic multi-turn conversations grounded in state-machine workflows across 10 enterprise domains with controlled interruptions and per-interruption rubrics); evaluate 27 audio-language model configurations.
---
## 1 Introduction: two questions
**Covers:** Section 1 up to insurance-claim example

Real-time voice agents are moving from prototypes to production (GPT Realtime [28], Gemini [12], Moshi [7]). Interruption sharply distinguishes spoken conversation from text chat. In structured workflows interruptions are the norm.

| Question | Content | Status |
|---|---|---|
| Q1 | Can the model detect and react to an interruption in real time? | Answered by Full-Duplex-Bench [23] and successors [21, 20, 38] (stop, yield floor, backchannel vs genuine), FLEXI [10] (topic-shift), SID-Bench [41] (semantic detection), HumDial [39] (respond/resume) |
| Q2 | What does the model say next? | Largely unanswered for structured workflows; the subject of this paper (steps 2–5) |

Insurance-claim example: agent mid-sentence on required documentation, user cuts in: "Actually, it was my work address, not home." Required: "(1) stop speaking, (2) recognize this as a correction of previously provided information, (3) integrate the correction, (4) not repeat the part of its explanation the user already heard, and (5) resume the workflow at the correct step."

## Good vs. bad recovery (Figure 1)
**Covers:** Section 1, Figure 1 Examples A–B

Example A — filler interruption (backchannel): assistant ". . . and there is elevator access from the garage. Back —", user: "mm-hm". Bad response: "Before we continue, I just want to . . ." — starts over after a simple backchannel and jumps to a different workflow stage. Good response: "to your registration, we still need to schedule your first appointment. Is now a good time?" — continues exactly from where it was cut off.

Example B — correction interruption: assistant "Got it, I'll use john.smith@example-company.com. Reading that back —", user: "Oh wait, sorry, no hyphen. It should be examplecompany as one word." Bad response: "Sure, it's john.smith@examplecompany.com. I'll use that for the email." — accepts correction but drops the workflow (was about to send summary). Good response: "Got it, I'll use john.smith@examplecompany.com. I'm sending the brief summary now with Jane Doe's direct contact and scheduling link." — integrates correction and resumes the workflow. "—" marks where the user interrupted mid-utterance.

## Preview of findings
**Covers:** Section 1, findings paragraph

- "A model that fails to stop speaking produces an awkward overlap, annoying but recoverable. A model that stops correctly but then re-reads its entire interrupted sentence, ignores the user's correction, or loses its place in the workflow creates a fundamentally broken interaction."
- All evaluated GPT-family audio models continue an utterance correctly after a backchannel less than a third of the time (filler pass rate between 7% and 31%); Gemini 2.5 family markedly better (62%–68%) although newer Gemini 3.x regresses sharply (13%–32%).
- "These are not inherently difficult behaviors; rather, they appear to be undertrained, suggesting that targeted evaluation can surface actionable training gaps."

## Contributions
**Covers:** Section 1, Contributions 1–3

1. "We define post-interruption recovery as a distinct evaluation axis for voice agents, decomposed into six interruption types, and propose a two-axis scoring for it: comparative task fulfillment judging and absolute recovery quality assessment, both powered by LLM judges with type-specific criteria (Sections 3.2 and 4)."
2. "We introduce IHBench, a benchmark of synthetically generated multi-turn conversations grounded in state-machine workflows across 10 enterprise domains. Each conversation includes controlled interruptions with per-interruption evaluation rubrics generated alongside the data (Section 3)."
3. "We evaluate 27 audio-language model configurations along several axes (overall scores, per-interruption-type breakdown, degradation with conversation depth, and audio-versus-text input modality), and verify our findings through inter-judge and human-judge agreement studies and a cross-benchmark comparison with AudioMultiChallenge [15] (Section 5)."

## Related work captured in this chunk
**Covers:** Section 2 opening (full-duplex and workflow-recovery benchmarks)

- FDB [23]: single-turn audio input, interruption handling judged by semantic relevance; v1.5 [22] expands overlap scenarios; FLEXI [10] single-turn, topic shift; SID-Bench [41] interruption vs backchannel; HumDial [39] respond vs resume; Talking Turns [3] timing via trained judge; INSTRUCT-FD [38] explicit turn-taking instructions — all characterize local overlap, "but do not evaluate post-interruption recovery within a structured workflow."
- FDB v2 [21] uses GPT-Realtime [28] as examiner for multi-turn evaluation, closest in spirit, but interruptions sit at VAD-detected pauses (model's own turn boundaries) and center on correction; this pipeline scripts interruptions mid-utterance at controlled positions, spans six types beyond correction with per-interruption rubrics. MTR-DuplexBench [47] tests detection/stopping in free dialogue; FDB v3 [20] tests tool use under self-corrections rather than user barge-ins.
**Covers:** Sections 1–2 (Introduction through related-work contrast on mid-speech barge-in recovery)
