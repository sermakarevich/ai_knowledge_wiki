[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation: Motion Quality, Streaming Latency, and Turn Arbitration
**In one sentence:** ROSCO matches real-motion geometry (lowest FID-G) with strong rhythmic alignment and low self-collision, generates 500 ms motion chunks in 195 ms (RTF 0.390) with 466 ms barge-in preemption, and CORTEX arbitrates multi-party turns by combining a fast physical interruption gate with deliberative addressivity decisions.
## Key points
- FID-G compares empirical mean/covariance (µp, Σp) of predicted geometry features against reference (µr, Σr); lower FID-G means closer alignment with the reference motion distribution.
- Kinematic self-collision proxy replays every predicted qpos frame in the full Astribot MuJoCo model via `mj_forward` without stepping dynamics, counting non-positive signed-distance contacts and reporting the fraction of frames with ≥1 self-contact.
- ROSCO achieves the highest BC score among generative baselines and remains competitive on BeatAlign, indicating audio-onset/motion-beat synchronization beyond frame-wise correspondence, plus the lowest FID-G among reported generative models.
- ROSCO's collision rate is substantially lower than retargeted ground truth (GT 6.51%), because GMR retargeting preserves kinematic correspondence without collision avoidance while ROSCO uses a collision-aware training objective.
- Streaming is viable with Tgen (195 ms, pcm_received → motion_ready) < Tmotion (500 ms), i.e. emission RTF 0.390; turn startup is dominated by LLM TTFT (1.62 s) and audio ingress (493 ms), with first speech at 2.20 s and first motion UDP at 2.36 s (all P50 medians).
- Full-duplex preemption combines RHPC (commits only leading 15 frames / 500 ms of each 50-frame horizon) with a VAD-based Fast Interruption Gate, reaching 466 ms median from speech onset to abort-command dispatch.
- Trace-based CORTEX evaluation on 199 sessions / 36,448 events / 559 turn decisions (302 REPLY, 88 INTERRUPT_AND_REPLY, 169 IGNORE) shows rule-based handling of clear cases (fillers, wake word) and dialogue-context reasoning for ambiguous utterances, with physical stop decoupled from the deliberative decision.
---
## Motion-quality metrics: FID-G and kinematic self-collision proxy
**Covers:** FID-G definition through kinematic feasibility proxy (p. 14)

FID-G is defined over geometry features:

> "where µp and Σp denote the empirical mean vector and covariance matrix of the predicted geometry features, respectively, and µr and Σr denote those of the reference features. Lower FID-G indicates closer alignment with the reference motion distribution."

Kinematic self-collision proxy procedure:
- Replay every predicted qpos frame in the full Astribot MuJoCo model and call `mj_forward` without stepping the dynamics.
- The trajectory is thus "evaluated kinematically, without modification by gravity, contacts, or actuators."
- Count contacts with non-positive signed distance; distinguish self-collisions from environment collisions using MuJoCo body identifiers.
- Report the self-collision frame rate, "defined as the fraction of frames containing at least one self-contact."

Caveat, verbatim:

> "This simulator-based measure serves as a proxy for physical executability, but does not by itself guarantee successful hardware execution."

## Motion-quality results: ROSCO vs baselines and retargeted ground truth
**Covers:** Evaluation Results, Table 2 summary (p. 14)

- ROSCO "achieves the highest BC score among the generative baselines, indicating stronger rhythmic synchronization between the detected audio onsets and generated motion beats."
- It "remains competitive on BeatAlign, where a higher score indicates better temporal alignment between motion dynamics and the rhythmic structure of the input audio," suggesting "audio-driven motion timing beyond simple frame-wise correspondence."
- ROSCO "obtains the lowest FID-G among the reported generative models, indicating that its generated motion better matches the geometric distribution of real motion."
- ROSCO "achieves a low collision rate, substantially lower than the retargeted ground-truth motions"; GT collision rate is 6.51%.
- Explanation: "the GMR retargeting process primarily aims to preserve the kinematic correspondence between the source and target embodiments, without explicitly optimizing for collision avoidance," so "the retargeted reference motions can still contain physically undesirable configurations."
- In contrast, "ROSCO incorporates a collision-aware training objective that explicitly penalizes physically implausible motions during generation," encouraging motions that "balance audio-motion alignment with the physical constraints of the target robot, rather than simply reproducing the potentially colliding retargeted trajectories."

## Real-time generation and full-duplex responsiveness
**Covers:** §5.3, Table 3 — runtime latency on Astribot S1 across multi-turn sessions, median (P50) (pp. 14–15)

Three temporal requirements for continuous interaction: "(i) Streaming Efficiency: motion synthesis must run faster than physical playback"; "(ii) Turn Responsiveness: the system should minimize the delay before speech and motion begin"; "(iii) Full-Duplex Preemption: ongoing speech and physical execution must be promptly interruptible upon user barge-in."

Table 3 — Runtime latency and full-duplex responsiveness of MIRA on Astribot S1 (median P50; user_turn denotes committed user transcript post-ASR):

| Pipeline Stage / Metric | Measurement Window | Median (P50) |
|---|---|---|
| Streaming ASR Endpointing | speech_end → user_turn | 10.0 ms |
| LLM First-Token Latency (TTFT) | user_turn → llm_first_token | 1.62 s |
| Streaming Audio Ingress | llm_first_token → pcm_received | 493 ms |
| ROSCO Chunk Inference Time (Tgen) | pcm_received → motion_ready | 195 ms |
| Emission Real-Time Factor (RTF) | Tgen / Tmotion (Tmotion = 500 ms) | 0.390 |
| First Synthesized Speech | user_turn → tts_first_audio | 2.20 s |
| Co-Speech Motion Synchronization | user_turn → first_motion_udp | 2.36 s |
| Deterministic Interruption Preemption | speech_started → abort_cmd_sent | 466 ms |

Streaming viability condition: "Tgen < Tmotion or equivalently RTF < 1.0"; with "Tmotion = 500 ms committed motion duration, ROSCO completes prefix-conditioned diffusion inference in only 195 ms (pcm_received → motion_ready), yielding an emission RTF of 0.390," leaving "sufficient runtime margin to sustain continuous trajectory execution."

Turn startup: "startup latency is dominated by upstream cognitive processing rather than motion synthesis"; "Local ASR endpointing introduces only 10.0 ms (speech_end → user_turn), while LLM first-token generation (1.62 s) and initial audio streaming to PCM ingress (493 ms) contribute most of the latency before first speech emission (tts_first_audio at 2.20 s)"; "Once audio becomes available, ROSCO generates the initial joint trajectory within 195 ms of audio ingress, with motion dispatched to the hardware bridge at 2.36 s (first_motion_udp)."

Preemption: "MIRA combines RHPC with a dedicated VAD-based interruption gate (i.e., Fast Interruption Gate)"; "RHPC commits only the leading 15 frames (500 ms) of each 50-frame prediction horizon, thereby strictly bounding the amount of motion committed ahead of physical execution"; on barge-in "the interruption gate requests active-audio cancellation and dispatches an asynchronous abort command"; "the preemption latency is 466 ms at the median, measured from speech onset (speech_started) to abort-command dispatch (abort_cmd_sent)."

## Multi-party turn arbitration and addressivity
**Covers:** §5.4, Table 4 — CORTEX trace-corpus evaluation and representative cases (p. 15)

Corpus: "a production trace corpus containing 199 active sessions, 36,448 recorded events, and 559 completed turn decisions. Among these decisions, 302 resulted in REPLY, 88 in INTERRUPT_AND_REPLY, and 169 in IGNORE." The evaluation examines "whether CORTEX can distinguish speech addressed to the robot from concurrent third-party speech and decide whether an ongoing response should be continued or interrupted."

Table 4 — Representative multi-party turn-arbitration cases:

| Case Family | User Utterance | Decision Basis | Decision |
|---|---|---|---|
| Case A | "Just sent the location to them." | Dialogue context | IGNORE |
| Case B | "No, that will not work." | Dialogue context | INTERRUPT_AND_REPLY |
| Case C | "Um." | Predefined rule | IGNORE |
| Case D | "MIRA." | Predefined rule | INTERRUPT_AND_REPLY |

- Case A (non-addressed speech / false-alarm recovery): bystander utterance exceeds the 450 ms threshold during robot presentation; "the Fast Interruption Gate triggers an early_barge_in_abort, temporarily pausing active speech and holding the robot motion"; once finalized ASR arrives, "the Deliberative Turn Arbiter evaluates the preceding conversational context and determines the utterance was not addressed to the robot, returning IGNORE"; "CORTEX retrieves the saved response context and seamlessly generates a continuation from the interrupted breakpoint."
- Case B (context-dependent interruption): "No, that will not work" is ambiguous alone, so the arbiter "uses the preceding dialogue context to infer the user's intent and returns INTERRUPT_AND_REPLY"; "the physical preemption does not wait for this decision" — the gate "emitted an early_barge_in_abort event before the finalized ASR transcript reached Parb."
- Case C (rule-based filler): brief hesitation filler ("Um", duration < 450 ms) does not engage the Fast Interruption Gate for lack of "the sustained 450 ms confirmation threshold"; the arbiter "matches the filler rule and returns IGNORE within ∼10 ms, allowing continuous robot playback to proceed completely undisturbed."
- Case D (rule-based wake word): explicit "MIRA" — "The Fast Interruption Gate initiates the hardware abort at 450 ms, and the arbiter confirms the addressivity via wake-word detection, returning INTERRUPT_AND_REPLY only 2 ms after the gate's decision."

Design takeaway: "CORTEX combines rule-based decisions with context-based reasoning within the Deliberative Turn Arbiter"; "Clear inputs, such as fillers and explicit wake-word commands, can be handled directly by predefined rules, while short or ambiguous utterances can be interpreted using the preceding dialogue context"; "The Fast Interruption Gate handles the time-critical physical stop separately, allowing the robot to stop promptly without waiting for the dialogue-level decision."

**Covers:** FID-G / self-collision proxy through §5.4 multi-party arbitration; Tables 2–4 (pp. 14–15)
