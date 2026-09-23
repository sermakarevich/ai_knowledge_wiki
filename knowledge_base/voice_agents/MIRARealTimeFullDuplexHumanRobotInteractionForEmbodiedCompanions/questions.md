---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions

### Q1. Why does real-time embodied companionship break decoupled dialogue-plus-offline-gesture pipelines?

> [!tip]- Answer
> A companion must infer intent from streaming speech, start moving before full response audio exists, and stay continuous with prior motion under uncertain turn boundaries. Decoupled systems generate motion offline from complete audio, so content, prosodic timing, and physical safety fall out of sync, and committed trajectories cannot be revised as freely as text. See [[wiki/01-mira-overview-and-contributions|MIRA Overview and Contributions]].

### Q2. What are the four components of MIRA (MIRA, CORTEX, ROSCO, RHPC) and how do they divide the work?

> [!tip]- Answer
> MIRA treats physical behavior as part of the interaction policy: CORTEX arbitrates turns and emits streaming text plus a symbolic embodiment cue routing discrete acts to validated libraries or speaking to ROSCO. ROSCO is the prefix-conditioned diffusion generator of joint trajectories from streaming audio and motion history, and RHPC is its inference scheme releasing only a short prefix of a longer predicted window. See [[wiki/01-mira-overview-and-contributions|MIRA Overview and Contributions]].

### Q3. What is the Audio Interaction Model (AIM) loop, and what does MIRA add to it?

> [!tip]- Answer
> AIM formalizes streaming interaction as an always-on perceive-decide-respond loop that updates context and responds without stopping perception. MIRA extends that paradigm from auditory response timing to physical embodiment: every verbal response gets an explicit embodiment decision, discrete behaviors route to validated libraries, and speaking uses streaming co-speech motion under bounded interruptible commitment. See [[wiki/02-related-work-streaming-dialogue-and-companions|Related Work — Streaming Dialogue and Embodied Companions]].

### Q4. What is the physical-commitment problem, and how does MIRA's answer differ from ProAct?

> [!tip]- Answer
> Delayed gestures, stale motion packets, and wrongly cancelled responses stay physically visible and socially disruptive after the dialogue state has moved on. ProAct decouples behavioral streaming from cognitive planning but targets one-way intention steering and leaves barge-in commitment open, while MIRA bounds commitment via RHPC plus a robot-side execution bridge and an inspectable symbolic cue interface. See [[wiki/02-related-work-streaming-dialogue-and-companions|Related Work — Streaming Dialogue and Embodied Companions]].

### Q5. What are CORTEX's three functional stages and its dual-timescale policy?

> [!tip]- Answer
> The stages are CORTEX turn-level interaction policy, embodiment routing to a validated library or ROSCO, and robot-side execution with session validation, joint/collision checks, and dispatch. CORTEX runs a fast 450 ms VAD interruption gate for immediate physical preemption alongside a deliberative arbiter and reactive generator sharing response-identity state σ. See [[wiki/03-cortex-interaction-policy-and-architecture|CORTEX Interaction Policy and Architecture]].

### Q6. What inputs and outputs define the Deliberative Turn Arbiter (Parb)?

> [!tip]- Answer
> Parb first applies deterministic rules for empty, hesitation-only ("um"/"hmm"), and stop/exit inputs, then queries a non-streaming LM with transcript, vocal affect, dialogue history, playback status, dialogue-active state, and current robot speech. It returns Parb ∈ {IGNORE, REPLY, INTERRUPT_AND_REPLY}, where IGNORE declines a turn, REPLY admits one, and INTERRUPT_AND_REPLY preempts output before generating a replacement. See [[wiki/03-cortex-interaction-policy-and-architecture|CORTEX Interaction Policy and Architecture]].

### Q7. How are embodiment cues serialized, parsed, and defaulted?

> [!tip]- Answer
> The cue is a compact prefix `<motion: m>; response text` with m ∈ M, selected from utterance, affect, intent, and history rather than one-to-one affect mapping. A parser strips the prefix before TTS so control metadata is never spoken, and missing or malformed cues fall back to `speak` for non-empty responses and `idle` for empty ones. See [[wiki/04-embodiment-cue-routing-and-execution|Embodiment Cue, Routing, and Execution]].

### Q8. How does the robot-side execution layer keep streaming motion safe and interruptible on the Astribot S1?

> [!tip]- Answer
> An execution bridge opens a realtime co-speech session for `speak`, routes the first qpos frame through a brief `move_to` transition, then streams frames through a MuJoCo collision-aware projection solving constrained IK under joint and collision limits with hold-or-fallback on failure. Source-rate 30 Hz frames feed a 250 Hz joint-position loop with per-tick step limits, and interruption terminates the session and rejects delayed commands while dialogue state persists. See [[wiki/04-embodiment-cue-routing-and-execution|Embodiment Cue, Routing, and Execution]].

### Q9. What is the ROSCO-DiT architecture and its causality discipline?

> [!tip]- Answer
> ROSCO-DiT stacks eight Prefix-DiT blocks over concatenated clean-prefix plus noisy-target tokens (d = 256, sinusoidal positions, 4 heads, 1024-dim FFN, dropout 0.1) with binary prefix/target markers and an output head predicting only the target chunk. Each block applies causal motion self-attention then causal audio cross-attention via a shared audio encoder so each motion token sees only same-or-earlier audio, with diffusion timestep τ injected by AdaLN gates g1–g3. See [[wiki/05-rosco-model-and-training|ROSCO Model and Training]].

### Q10. What four training objectives shape ROSCO, and what does each enforce?

> [!tip]- Answer
> Rich-motion reconstruction (Lrich) supervises qpos, velocity, local positions, 6D rotations, and kinematics; Lkin adds FK Cartesian consistency plus a clearance-margin collision penalty. A two-step autoregressive rollout (Lrollout) supervises the next chunk from detached predictions to curb exposure bias, and a margin-based contrastive audio loss (Laudio) forces matched audio to reconstruct better and separate joint predictions from shuffled audio. See [[wiki/05-rosco-model-and-training|ROSCO Model and Training]].

### Q11. State the RHPC numbers (predict / commit / prefix / rates) and the three reasons for predicting more than is committed.

> [!tip]- Answer
> Each step consumes 50 audio tokens, predicts a 50-frame window, commits only the first 15 frames (0.50 s at 30 fps), and reuses the latest 10 committed frames as the next prefix. The long horizon reduces train-test mismatch versus denoising short sequences, gives downstream projection and collision checks a trajectory candidate to vet, and bounds barge-in cost since only 0.5 s must be played out or discarded. See [[wiki/06-receding-horizon-prefix-commitment|Receding-Horizon Prefix Commitment Inference]].

### Q12. What do the headline evaluation numbers say about motion quality, streaming viability, and turn arbitration?

> [!tip]- Answer
> ROSCO takes the lowest FID-G with top BC rhythmic alignment, stays competitive on BeatAlign, and collides far less than retargeted ground truth (6.51%) thanks to its collision-aware objective. Streaming holds with Tgen 195 ms over 500 ms of motion (RTF 0.390), turn startup dominated by LLM TTFT 1.62 s to first speech 2.20 s and motion 2.36 s, 466 ms barge-in preemption, and 559 traced decisions (302 REPLY, 88 INTERRUPT_AND_REPLY, 169 IGNORE) splitting rule-based fillers/wake-words from context-resolved ambiguous turns. See [[wiki/07-evaluation-motion-quality-and-streaming|Evaluation: Motion Quality, Streaming Latency, and Turn Arbitration]].

### Q13. Which cited references ground MIRA's body models, gesture synthesis, interaction framing, and diffusion backbone?

> [!tip]- Answer
> Body models rest on SMPL (2015) and SMPL-X (2019); gesture synthesis spans trimodal conditioning, diffusion gestures, semantic-aware synthesis, GestureHYDRA, RoboGesture, and ProAct. Interaction framing cites the turn-taking review, empathy survey, communicative robot gesture, affective computing, and the Audio Interaction Model, while diffusion grounding cites scalable DiTs and rotation-continuity representations. See [[wiki/09-references-and-further-reading|References and Further Reading]].

### Q14. Given MIRA's constrained vocabulary, platform-specific safety tuning, cascaded-pipeline startup latency, and lack of long-term user studies, where should the team invest next before a home deployment?

> [!tip]- Answer
> Prioritize long-term naturalistic user studies plus per-platform safety validation, since benchmarks prove throughput and containment but not sustained companion dynamics or transfer to new kinematics. In parallel, attack the ~2.2 s startup bottleneck from the ASR→LLM→TTS cascade (e.g., omni speech-to-speech models) and broaden the cue vocabulary with semantic text conditioning before promising open-ended home companionship. See [[wiki/08-discussion-limitations-and-deployment|Discussion and Limitations: System Insights]].
