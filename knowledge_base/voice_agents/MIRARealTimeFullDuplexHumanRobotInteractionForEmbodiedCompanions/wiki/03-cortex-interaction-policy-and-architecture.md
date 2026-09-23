> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# CORTEX Interaction Policy and Architecture
**In one sentence:** MIRA orchestrates full-duplex embodied dialogue in three stages — CORTEX turn-level interaction policy, embodiment routing, and robot-side execution — with CORTEX using a fast VAD interruption gate plus deliberative turn arbitration and reactive response generation coordinated through shared connection state.
## Key points
- MIRA is organized in three functional stages: (a) CORTEX Interaction Policy, (b) Embodiment Routing to a validated behavior library or the ROSCO co-speech pathway, and (c) Robot-Side Execution with session-scoped validation, joint-limit/collision checks, interpolation, and hardware dispatch.
- Four design requirements drive the system: contextually appropriate interaction decisions, inspectable cue-to-motion routing (behavior class, not joint control), streaming speech/motion generation, and contained physical execution via the robot-side bridge.
- A VAD-based Fast Interruption Gate aborts ongoing output when sustained user speech reaches a 450 ms interruption-confirmation threshold during playback (with embodiment listening mode disabled): it marks the response aborted, clears pending TTS, sends TTS-stop, ends robot motion, and streams audio incrementally to ASR.
- The Deliberative Turn Arbiter (Parb) first applies deterministic rules (empty/hesitation-only input such as 'um'/'hmm', explicit stop/exit commands), then sends a non-streaming LM query combining transcript, vocal affect, recent dialogue history, playback status, dialogue-active state, current/most recent robot speech, and the preliminary rule decision.
- Parb returns one of three decisions — `Parb ∈ {IGNORE, REPLY, INTERRUPT_AND_REPLY}` — where IGNORE declines a new turn, REPLY admits a turn, and INTERRUPT_AND_REPLY interrupts ongoing output before generating a replacement.
- The Reactive Dialogue Generator (Pgen) conditions on transcript, vocal affect, accumulated dialogue history, and persona/task instructions; it can call registered functions (e.g., weather lookup, music playback) with tool calls and results recorded in dialogue context, emits a symbolic embodiment cue parsed separately from speech text, and streams text to incremental TTS so speech and co-speech motion start early.
- Interruption uses shared connection state (playback status, abort flag, response identifier σ): an admitted turn gets a fresh σ binding TTS segments and motion messages to one response, while an interruption marks the response aborted, clears queues, and dispatches speech-stop/motion-end commands while retaining dialogue history; an ignored turn after an early abort can resume via a continuation from saved assistant context.
---
## System overview
CORTEX "combines the transcript, vocal affect, dialogue history, and playback state to manage turn admission and stream responses," and "the cue parser separates embodiment metadata from response text before TTS." Embodiment cues route to "ROSCO for audio-conditioned co-speech generation or to a validated behavior library for discrete actions." The robot-side execution layer "applies configured joint and collision checks before SDK dispatch and manages audio playback." "Speech and motion share a response identity; the red dashed paths indicate cancellation requests for the active response, allowing its pending outputs to be invalidated while retaining dialogue history."
Discrete social behaviors (e.g., greeting, listen) are retrieved from the validated library, while the speak cue opens a streaming co-speech session routing PCM audio to ROSCO; motion trajectories "converge at a robot-side execution boundary that validates session identity, checks physical constraints, converts timing, and dispatches commands."
## CORTEX dual-timescale policy
"CORTEX orchestrates full-duplex embodied dialogue through two cooperative policies for turn admission and response generation. The Deliberative Turn Arbiter (Parb) determines whether an incoming utterance warrants a response and whether ongoing output should be interrupted, while the Reactive Dialogue Generator (Pgen) produces spoken responses and embodiment cues for admitted turns." Both operate through shared connection state so speech and motion stay associated with a single active response under asynchronous decisions.
## Fast interruption gate
After VAD stabilization the controller measures the ongoing speech segment; at the 450 ms threshold during active playback it performs an early abort (mark response aborted, clear pending TTS, send TTS-stop, terminate robot motion). Audio goes incrementally to ASR while the user speaks, and the Deliberative Turn Arbiter is triggered only after the backend returns a provider-specific final or otherwise definitive transcription. "If the turn is ignored after an early abort, the controller may generate a continuation of the interrupted response using its saved response context."
## Deliberative Turn Arbiter (Parb)
Verbatim decision set:
> Parb ∈ {IGNORE, REPLY, INTERRUPT_AND_REPLY}. (1)
"IGNORE declines to admit the input as a new user turn; REPLY admits a turn for response generation; and INTERRUPT_AND_REPLY requests interruption of the ongoing response before generating a new one. The controller combines this decision with deterministic rules to determine the final action."
## Reactive Dialogue Generator (Pgen)
Generation is conditioned on current transcript, vocal affect, accumulated dialogue history, and configurable persona/task instructions specifying "the assistant's identity, conversational style, and interaction role, supporting companion dialogue and informational presentations."
## State handoff and interruption semantics
"When a turn is admitted, the generator creates a response with a fresh identifier, which associates queued TTS segments and motion-control messages with that response." Interruption operations "stop ongoing response production while retaining the dialogue history for subsequent arbitration and generation." "An IGNORE decision does not admit the triggering input as a new user turn." "For an INTERRUPT_AND_REPLY decision, the controller requests interruption if playback remains active, then admits the input as a new user turn and invokes the Reactive Dialogue Generator to produce a replacement response."
## Representative embodiment-cue vocabulary (Table 1)
| Cue | Communicative role | Behavior family / route |
|---|---|---|
| speak | General verbal response | Streaming co-speech generation |
| greeting/wave | Greeting or positive social opening | Greeting / wave bank |
| listen | Turn yielding or invitation to elaborate | Attentive-listening bank |
| confused | Uncertainty, misunderstanding, or failed understanding | Confusion / clarification bank |
| apologize | Conversational repair or explicit apology | Apology / repair bank |
| idle | Neutral hold or fallback | Idle bank / default pose |
**Covers:** Covers the MIRA system architecture and CORTEX dual-timescale interaction policy (turn arbitration, interruption).
