> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# MIRA Overview and Contributions
**In one sentence:** MIRA is a unified full-duplex framework that coordinates streaming dialogue, explicit embodiment-cue routing, and interruptible co-speech motion so an Astribot S1 humanoid can speak, gesture, and yield safely under incremental inputs.
## Key points
- Real-time embodied companionship requires inferring intent from streaming speech, generating timely responses, and executing expressive, interruptible motions under uncertain turn boundaries.
- Existing systems decouple dialogue orchestration from gesture synthesis and rely on offline motion generation from complete audio, leaving content, prosodic timing, and physical safety unsynchronized.
- MIRA predicts both response text and an explicit embodiment cue from streaming user speech, dialogue history, and vocal affect.
- Discrete social behaviors (e.g., listening, greeting) map to validated robot trajectories, while open-ended speaking uses streaming co-speech motion.
- Generative speaking motion uses a predict-more-than-commit sliding window: long temporal look-ahead for continuity with physical commitment limited to a short, cancellable prefix.
- CORTEX is a dual-timescale interaction policy managing low-latency streaming plus deliberative turn decisions, backed by a robot-side execution layer enforcing safety at the control rate.
- The system is deployed on an Astribot S1 humanoid and evaluated for audio-motion alignment, streaming responsiveness, and interruption handling.
---
## Motivation: companion interaction as continuous embodied process
**Covers:** Title, abstract, Section 1 Introduction (pp. 1–2)

A companion robot must answer questions and participate through speech, listening, and physical behavior: "A greeting may call for a brief, recognizable action, and an explanation may call for gestures that follow the rhythm and duration of unfolding speech."

Core demands from the chunk:

| Requirement | Detail from source |
|---|---|
| Continuous decisions | Which behavior is appropriate, when to speak, how to accompany speech with motion, how to respond to pauses, clarifications, or interruptions |
| Online speaking constraint | Complete response audio may not yet exist when the robot must begin moving; motion must be generated from incremental audio while staying continuous with prior motion |
| Coupled processes | (1) deciding what the robot should do next at the interaction level; (2) continuously generating how that behavior is expressed at the motion level |
| Physical constraint | "Motion already released for execution cannot be changed as freely as uncommitted text or audio"; trajectories must satisfy kinematic and execution constraints |

Prior work context cited in the chunk: ProAct [42] (streaming behavior generation with deliberative social reasoning), PhysDrift [18] (robot-native generation under embodiment constraints), RoboGesture [34] (streaming, semantically aligned co-speech gestures on a physical humanoid).

Verbatim framing quote:

> "Real-time embodied companion interaction requires a robot to infer user intent from streaming speech, generate timely responses, and execute expressive, interruptible motions."

## Framework: MIRA, CORTEX, ROSCO, and RHPC
**Covers:** Abstract + Introduction framework description + Figure 1

Full title and source facts:

- Title: "MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions"
- Authors: Lijian Lin, Ye Zhu, Fan Zhang, Yunfei Liu, Baofeng Li, Xianwen Zeng, Jianan Wang, Yu Li; affiliations: 1 International Digital Economy Academy, 2 Astribot
- Identifier: arXiv:2609.24547v1 [cs.RO] 21 Sep 2026
- Homepage: https://gagajian.github.io/MIRA/
- Deployment robot: Astribot S1 humanoid; motion dataset: retargeted co-speech motion dataset BEAT [21]

Expanded name given in the chunk: "Full-Duplex Embodied Companion for Natural Human–Robot Interaction (MIRA)".

Architecture as described:

- MIRA treats "physical behavior as part of the interaction policy rather than as a downstream rendering step."
- Interface: an embodiment cue, "a compact symbolic label that specifies how an admitted response should be physically expressed," routing to validated social behaviors (greeting, listening) or the generative speaking pathway.
- CORTEX "combines streaming response generation with deliberative turn admission and a local interruption gate, allowing the robot to continuously arbitrate between speaking, listening, and changing conversational turns."
- ROSCO (Robotic Streaming Co-speech Generator) "generates robot joint trajectories from streaming audio and recent motion history" for "recurrent streaming generation, where motion must remain temporally coherent while adapting to newly arriving speech."
- RHPC (Receding-Horizon Prefix Commitment) "separates the prediction horizon from the physical emission stride: the model looks ahead over a longer motion window while releasing only a short prefix for execution."

Figure 1 behavior (verbatim summary from caption): "Given user speech containing linguistic content and vocal affect, CORTEX infers conversational intent and context. Responses are routed into two parallel pathways: discrete social behaviors (e.g., greeting, listening) execute pre-validated action libraries, while open-ended speaking drives ROSCO to generate streaming, speech-synchronized motion." On barge-in ("Actually, wait…", red dashed path), "active speech and joint trajectories are immediately preempted and cancelled at the execution boundary, enabling safe physical halting while retaining conversational context for subsequent turn arbitration."

## Contributions
**Covers:** Contribution list (p. 2)

Verbatim contributions:

- "We propose MIRA, a real-time full-duplex human-robot interaction framework that coordinates dialogue decisions, social behaviors, and streaming co-speech motion through an explicit embodiment-cue protocol and unified response-lifecycle management."
- "We introduce CORTEX, a comprehensive interaction architecture bridging high-level cognition to low-level motor control: it actively generates streaming verbal responses and embodiment cues, manages dual-timescale turn arbitration, and is grounded by a robot-side execution layer enforcing high-rate collision checks, joint constraints, and safe physical halting."
- "We propose ROSCO, a prefix-conditioned diffusion model for streaming audio-to-joint motion generation, together with RHPC, an inference scheme that balances a sufficiently long temporal context for motion prediction with bounded, interruptible physical commitment."
- "We present a system-level evaluation of motion quality, streaming performance, and interruption handling, demonstrating these capabilities on a physical Astribot S1 humanoid robot."

Evaluation claim in this chunk: "ROSCO achieves competitive speech-motion alignment while meeting the streaming emission budget under the evaluated deployment configuration," supported by "motion-quality comparisons, streaming timing measurements, and interruption analysis" plus "qualitative real-robot demonstrations of streaming co-speech motion and barge-in handling."

**Covers:** MIRA motivation, full-duplex embodied companion framing, and the paper's contributions (chunk 01).
