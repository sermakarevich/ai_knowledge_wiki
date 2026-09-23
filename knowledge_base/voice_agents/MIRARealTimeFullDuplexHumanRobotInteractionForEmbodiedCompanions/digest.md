> [[index|Wiki]] | [[summary|Summary]]

# MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions — Digest

## 1. [[wiki/01-mira-overview-and-contributions|MIRA Overview and Contributions]]

**In one sentence:** MIRA is a unified full-duplex framework that coordinates streaming dialogue, explicit embodiment-cue routing, and interruptible co-speech motion so an Astribot S1 humanoid can speak, gesture, and yield safely under incremental inputs.

- Real-time embodied companionship requires inferring intent from streaming speech, generating timely responses, and executing expressive, interruptible motions under uncertain turn boundaries.
- Existing systems decouple dialogue orchestration from gesture synthesis and rely on offline motion generation from complete audio, leaving content, prosodic timing, and physical safety unsynchronized.
- MIRA predicts both response text and an explicit embodiment cue from streaming user speech, dialogue history, and vocal affect.
- Discrete social behaviors (e.g., listening, greeting) map to validated robot trajectories, while open-ended speaking uses streaming co-speech motion.
- Generative speaking motion uses a predict-more-than-commit sliding window: long temporal look-ahead for continuity with physical commitment limited to a short, cancellable prefix.
- CORTEX is a dual-timescale interaction policy managing low-latency streaming plus deliberative turn decisions, backed by a robot-side execution layer enforcing safety at the control rate.
- The system is deployed on an Astribot S1 humanoid and evaluated for audio-motion alignment, streaming responsiveness, and interruption handling.

## 2. [[wiki/02-related-work-streaming-dialogue-and-companions|Related Work — Streaming Dialogue and Embodied Companions]]

**In one sentence:** Spoken dialogue has moved to always-on streaming full-duplex interaction, but companion robots add a visible physical-commitment problem, so MIRA extends streaming response timing to embodiment with bounded interruptible motion, symbolic embodiment cues, and conservative affect fusion.

- The Audio Interaction Model (AIM) [35] formalizes streaming interaction as an always-on perceive-decide-respond loop that continuously updates context and responds without stopping perception.
- A companion robot cannot wait for a complete fixed input before choosing whether to speak, hold, or stop, building on endpointing, overlap management, and incremental response timing [5, 31].
- MIRA extends the streaming paradigm from auditory response timing to physical embodiment: every verbal response is paired with an explicit embodiment decision, discrete behaviors route to validated motion libraries, and open-ended speaking uses streaming co-speech motion under bounded interruptible commitment.
- Dual-system ProAct [42] decouples behavioral streaming from cognitive planning for proactive intentions but focuses on one-way intention steering and leaves open physical commitment during sudden barge-ins.
- MIRA targets full-duplex bidirectional interaction by bounding physical commitment via RHPC and a robot-side execution bridge, and by bridging arbitration and execution through an inspectable symbolic Embodiment Cue interface rather than an unconstrained end-to-end trajectory generator.
- Companion robots face a unique physical commitment problem: delayed gestures, stale motion packets, and incorrectly cancelled responses stay physically visible and socially disruptive after the dialogue state has transitioned.
- MIRA follows a conservative affect paradigm: instead of mapping noisy vocal affect directly to low-level motor commands, the speech-derived affect cue is fused with transcript semantics, dialogue history, and interaction state to select a high-level embodiment cue, preserving safety and inspectability.

## 3. [[wiki/03-cortex-interaction-policy-and-architecture|CORTEX Interaction Policy and Architecture]]

**In one sentence:** MIRA orchestrates full-duplex embodied dialogue in three stages — CORTEX turn-level interaction policy, embodiment routing, and robot-side execution — with CORTEX using a fast VAD interruption gate plus deliberative turn arbitration and reactive response generation coordinated through shared connection state.

- MIRA is organized in three functional stages: (a) CORTEX Interaction Policy, (b) Embodiment Routing to a validated behavior library or the ROSCO co-speech pathway, and (c) Robot-Side Execution with session-scoped validation, joint-limit/collision checks, interpolation, and hardware dispatch.
- Four design requirements drive the system: contextually appropriate interaction decisions, inspectable cue-to-motion routing (behavior class, not joint control), streaming speech/motion generation, and contained physical execution via the robot-side bridge.
- A VAD-based Fast Interruption Gate aborts ongoing output when sustained user speech reaches a 450 ms interruption-confirmation threshold during playback (with embodiment listening mode disabled): it marks the response aborted, clears pending TTS, sends TTS-stop, ends robot motion, and streams audio incrementally to ASR.
- The Deliberative Turn Arbiter (Parb) first applies deterministic rules (empty/hesitation-only input such as 'um'/'hmm', explicit stop/exit commands), then sends a non-streaming LM query combining transcript, vocal affect, recent dialogue history, playback status, dialogue-active state, current/most recent robot speech, and the preliminary rule decision.
- Parb returns one of three decisions — `Parb ∈ {IGNORE, REPLY, INTERRUPT_AND_REPLY}` — where IGNORE declines a new turn, REPLY admits a turn, and INTERRUPT_AND_REPLY interrupts ongoing output before generating a replacement.
- The Reactive Dialogue Generator (Pgen) conditions on transcript, vocal affect, accumulated dialogue history, and persona/task instructions; it can call registered functions (e.g., weather lookup, music playback) with tool calls and results recorded in dialogue context, emits a symbolic embodiment cue parsed separately from speech text, and streams text to incremental TTS so speech and co-speech motion start early.
- Interruption uses shared connection state (playback status, abort flag, response identifier σ): an admitted turn gets a fresh σ binding TTS segments and motion messages to one response, while an interruption marks the response aborted, clears queues, and dispatches speech-stop/motion-end commands while retaining dialogue history; an ignored turn after an early abort can resume via a continuation from saved assistant context.

## 4. [[wiki/04-embodiment-cue-routing-and-execution|Embodiment Cue, Routing, and Execution]]

**In one sentence:** CORTEX emits a compact `<motion: m>` cue prefix that is stripped before TTS and routed either to pre-validated retrieved motions or to a streaming ROSCO co-speech session, with robot-side safety enforced by a collision-aware projection layer and a 250 Hz control loop.

- The embodiment cue `m` is serialized as a compact prefix `<motion: m>; response text` with `m ∈ M` (Eq. 2), where `M` is a finite vocabulary of embodiment cues with representative examples in Tab. 1.
- Cue selection jointly considers user utterance, inferred affect, semantic intent, and recent dialogue history — not a one-to-one affect-to-action mapping (e.g. negative affect raises the likelihood of repair plus an apologize cue only when the utterance indicates dissatisfaction).
- A parser separates the cue prefix from response text before TTS so control metadata never enters spoken audio; missing or malformed cues fall back deterministically to `speak` for non-empty responses and `idle` for empty responses.
- Routing splits by cue: non-speaking cues forward a behavior family to a retrieval service of pre-validated motions (predictable timing, bounded physical envelope); `speak` establishes a co-speech session streaming TTS audio to ROSCO (Sec. 4).
- Robot-side execution runs on an Astribot S1 via an execution bridge that receives discrete cues or streaming co-speech `qpos` frames, opens a realtime co-speech session for `speak`, and sends the first frame through a brief `move_to` transition to avoid discontinuity.
- Every generated `qpos` frame passes through a collision-aware projection layer evaluated in the MuJoCo simulator that solves constrained inverse kinematics under joint-limit and collision constraints, holding the last safe pose or invoking fallback on failure.
- Source-rate motion at typically 30 Hz is consumed by a 250 Hz joint-position control loop on the Orin side with per-tick joint-step limits; on CORTEX interruption the active motion session is terminated and delayed commands rejected while dialogue state stays intact.

## 5. [[wiki/05-rosco-model-and-training|ROSCO Model and Training]]

**In one sentence:** ROSCO-DiT is a prefix-conditioned diffusion transformer that generates target motion chunks from preceding motion context and causal audio features, trained with rich-motion reconstruction plus kinematic, rollout, and contrastive audio objectives.

- Streaming generation conditions on preceding motion prefix `Pi` and causal audio features, with cached rich-motion history providing the prefix for subsequent updates.
- The backbone consists of eight stacked Prefix-DiT blocks, each applying causal motion self-attention, causal audio cross-attention, and a feed-forward network.
- Motion and prefix audio sequences are processed by a shared causal audio encoder, and each motion token can access only same-or-earlier audio tokens.
- Motion sequence is projected to d = 256 dimensions with sinusoidal temporal position embeddings; each block uses 4 attention heads, a 1024-dimensional feed-forward layer, and dropout of 0.1.
- Diffusion timestep τ is embedded and injected via AdaLN, with separate shift, scale, and residual gates (g1, g2, g3) for self-attention, cross-attention, and feed-forward branches.
- Only denormalized joint qpos qt are retained for downstream robot execution; auxiliary geometric components are used for training and reconstruction.
- Training combines rich-motion reconstruction, kinematic consistency with FK and collision clearance, two-step autoregressive rollout, and a margin-based contrastive audio loss.
- Streaming inference uses overlapping windows: each call predicts 50 frames but commits only the first 15, reusing the latest 10 committed frames as prefix context at 30 fps.

## 6. [[wiki/06-receding-horizon-prefix-commitment|Receding-Horizon Prefix Commitment Inference]]

**In one sentence:** Receding-Horizon Prefix Commitment (RHPC) balances long temporal context with streaming low latency by predicting a 50-frame motion window at each step but committing only the first 15 frames, reusing the latest 10 committed frames as autoregressive prefix.

- Each inference step consumes 50 temporally aligned audio tokens and predicts an extended 50-frame rich-motion window, but only the first 15 frames are committed to the robot controller.
- At speaking-turn start the streaming bridge initializes the motion prefix `P0` and audio context `Aprev_0` with zero tensors, since no ground-truth motion history is available at test time; each generated chunk is fed back as the prefix for the next step.
- The next 50-frame prediction uses the latest 10 committed frames as the motion prefix, with commitment advancing 15 frames per step, so the 10-frame overlap smooths transitions across chunk boundaries.
- The 50-frame prediction horizon keeps the sequence length closer to training, reducing the train-test distribution mismatch of applying diffusion denoising to substantially shorter sequences.
- The extended trajectory candidate lets downstream kinematic projection and collision checks assess future motion feasibility before commands are dispatched.
- Only 15 frames (0.50 s) are committed per step, so a CORTEX-triggered interruption ends the session after the current segment without discarding a long pre-generated trajectory, preserving continuity up to the last committed frame.
- At deployment only the denormalized joint qpos of the committed 15 frames are transmitted to the robot controller, while remaining rich-motion predictions are retained internally; incoming TTS audio is resampled from 24 kHz to 16 kHz mono.

## 7. [[wiki/07-evaluation-motion-quality-and-streaming|Evaluation: Motion Quality, Streaming Latency, and Turn Arbitration]]

**In one sentence:** ROSCO matches real-motion geometry (lowest FID-G) with strong rhythmic alignment and low self-collision, generates 500 ms motion chunks in 195 ms (RTF 0.390) with 466 ms barge-in preemption, and CORTEX arbitrates multi-party turns by combining a fast physical interruption gate with deliberative addressivity decisions.

- FID-G compares empirical mean/covariance (µp, Σp) of predicted geometry features against reference (µr, Σr); lower FID-G means closer alignment with the reference motion distribution.
- Kinematic self-collision proxy replays every predicted qpos frame in the full Astribot MuJoCo model via `mj_forward` without stepping dynamics, counting non-positive signed-distance contacts and reporting the fraction of frames with ≥1 self-contact.
- ROSCO achieves the highest BC score among generative baselines and remains competitive on BeatAlign, indicating audio-onset/motion-beat synchronization beyond frame-wise correspondence, plus the lowest FID-G among reported generative models.
- ROSCO's collision rate is substantially lower than retargeted ground truth (GT 6.51%), because GMR retargeting preserves kinematic correspondence without collision avoidance while ROSCO uses a collision-aware training objective.
- Streaming is viable with Tgen (195 ms, pcm_received → motion_ready) < Tmotion (500 ms), i.e. emission RTF 0.390; turn startup is dominated by LLM TTFT (1.62 s) and audio ingress (493 ms), with first speech at 2.20 s and first motion UDP at 2.36 s (all P50 medians).
- Full-duplex preemption combines RHPC (commits only leading 15 frames / 500 ms of each 50-frame horizon) with a VAD-based Fast Interruption Gate, reaching 466 ms median from speech onset to abort-command dispatch.
- Trace-based CORTEX evaluation on 199 sessions / 36,448 events / 559 turn decisions (302 REPLY, 88 INTERRUPT_AND_REPLY, 169 IGNORE) shows rule-based handling of clear cases (fillers, wake word) and dialogue-context reasoning for ambiguous utterances, with physical stop decoupled from the deliberative decision.

## 8. [[wiki/08-discussion-limitations-and-deployment|Discussion and Limitations: System Insights]]

**In one sentence:** MIRA's fluid embodied interaction comes from coupling dialogue reasoning, motion generation, and physical execution in one loop — hybrid routing plus end-to-end streaming safeguards — but vocabulary breadth, platform-specific safety tuning, cascaded-pipeline startup latency, and missing long-term user studies bound the current system.

- MIRA couples dialogue reasoning, motion generation, and physical execution into a unified interactive loop rather than treating motion as a passive downstream rendering step.
- Hybrid routing separates discrete social actions from open-ended speaking: pre-validated motion libraries give deterministic safety envelopes for repeatable behaviors (e.g., greetings, listening), while streaming diffusion adapts to unpredictable speech prosody.
- In continuous physical deployment, streaming quality is an end-to-end system property, not just the generative capacity of the diffusion backbone.
- Real-time fluidity depends critically on prefix feedback, receding-horizon commitment schedules, boundary preemption, and robot-side execution safeguards.
- The embodiment vocabulary is currently constrained; adding joint semantic text conditioning alongside audio prosody could further enrich gesture expressivity.
- The physical safety layer requires embodiment-specific kinematic tuning and collision geometry modeling for each new robot platform.
- Turn startup latency is largely bounded by the upstream cascaded pipeline (ASR → LLM → TTS); native end-to-end speech-to-speech (omni) foundation models could substantially compress initial response delay.
- Quantitative benchmarks establish technical viability, streaming throughput, and physical containment, but long-term human-subject studies in naturalistic environments are still needed to assess subjective companion dynamics and sustained user engagement.

## 9. [[wiki/09-references-and-further-reading|References and Further Reading]]

**In one sentence:** This chunk is the paper's reference list tail (entries [24]–[44], pp. 18–20), spanning parametric body models, co-speech gesture synthesis, talking-face and motion datasets, diffusion backbones, and turn-taking/affective-interaction surveys cited by MIRA.

- The chunk contains only bibliography entries [24]–[44] (pp. 18–20), with no methods, results, or new claims.
- Foundational body-model references include SMPL (Loper et al. 2015, ACM TOG 34(6), pp. 248:1–248:16) and SMPL-X expressive capture (Pavlakos et al. 2019, CVPR, pp. 10975–10985).
- Co-speech gesture references span trimodal text/audio/identity conditioning (Yoon et al. 2020, ACM TOG 39(6), pp. 222:1–222:16), diffusion-based gesture generation (Zhu et al. 2023, CVPR, pp. 10544–10553), and semantic-aware synthesis (Zhang et al. 2024, ACM TOG 43(4), pp. 136:1–136:17).
- Recent (2025–2026) cited works include GestureHYDRA (ICCV 2025, pp. 12615–12625), SMPLest-X (IEEE TPAMI 48(2), pp. 1778–1794), RoboGesture (arXiv:2608.28693), ProAct (arXiv:2602.14048), and Audio Interaction Model (arXiv:2606.05121).
- Speech-to-face and motion references include DiffPoseTalk (ACM TOG 43(4), Article 46, 9 pages), MEAD (ECCV 2020, pp. 700–717), and speech-to-holistic-motion (Yi et al. 2023, CVPR, pp. 469–480).
- Interaction-framing references include turn-taking review (Skantze 2021, Computer Speech & Language 67, Article 101178), empathy survey (Paiva et al. 2017, ACM TIIS 7(3), Article 11, 40 pages), communicative robot gesture (Salem et al. 2012, Int. J. Social Robotics 4(2), pp. 201–217), and affective computing (Picard 1997, MIT Press).
- Diffusion-architecture grounding cites Scalable Diffusion Models with Transformers (Peebles & Xie 2023, ICCV, pp. 4172–4182) and rotation-continuity representations (Zhou et al. 2019, CVPR, pp. 5745–5753).

## The argument in five moves

1. Real-time companionship is a continuous embodied problem: streaming intent inference, timely response, and interruptible motion under uncertain turn boundaries, which decoupled dialogue-plus-offline-gesture pipelines leave unsynchronized.
2. MIRA answers by making physical behavior part of the interaction policy: CORTEX predicts response text plus an explicit embodiment cue from streaming speech, affect, and history, routing discrete social acts to validated libraries and open-ended speaking to streaming co-speech generation.
3. Full-duplex arbitration runs on two timescales — a 450 ms VAD fast interruption gate for immediate physical preemption plus a deliberative arbiter (IGNORE / REPLY / INTERRUPT_AND_REPLY) and reactive generator sharing response-identity state — so stops are fast while turn decisions stay context-aware.
4. ROSCO with RHPC makes the motion side streamable and safe: a prefix-conditioned diffusion transformer generates 50-frame windows but commits only a 15-frame prefix over a 10-frame overlap, trained with kinematic, rollout, and contrastive audio objectives and guarded by MuJoCo projection plus a 250 Hz control loop.
5. On the Astribot S1 this yields the lowest FID-G with top rhythmic alignment and sub-GT collision rates, 195 ms chunk generation (RTF 0.390) with 466 ms barge-in preemption, and context-sensitive multi-party arbitration across 559 traced turn decisions.
6. The remaining bounds are a constrained embodiment vocabulary, per-platform safety tuning, cascaded-pipeline startup latency (~2.2 s to first speech), and the absence of long-term human-subject studies — fluidity is shown to be an end-to-end systems property, not just backbone capacity.
