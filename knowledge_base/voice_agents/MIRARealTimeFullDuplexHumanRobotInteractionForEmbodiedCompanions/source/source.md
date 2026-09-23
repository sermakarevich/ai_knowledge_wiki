# MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions
Source: http://arxiv.org/abs/2609.24547v1
Kind: pdf
Fetched: 2026-09-22T08:12:06.196342+00:00
Tool: pdftotext

                                             MIRA: Real-Time Full-Duplex Human-Robot
                                             Interaction for Embodied Companions
                                             Lijian Lin1 , Ye Zhu1 , Fan Zhang1 , Yunfei Liu1 , Baofeng Li2 , Xianwen Zeng2 , Jianan Wang2 , Yu Li1
                                             1
                                                 International Digital Economy Academy, 2 Astribot

                                            Real-time embodied companion interaction requires a robot to infer user intent from streaming speech, generate
                                            timely responses, and execute expressive, interruptible motions. Existing systems typically decouple dialogue
                                            orchestration from gesture synthesis, relying on offline motion generation from complete audio. This separation
                                            leaves open how a deployed robot can dynamically synchronize response content, prosodic timing, and physical
                                            safety under incremental inputs and uncertain turn boundaries. We present MIRA, a unified framework




arXiv:2609.24547v1 [cs.RO] 21 Sep 2026
                                            for full-duplex embodied companion interaction. Given streaming user speech, dialogue history, and vocal
                                            affect, MIRA predicts both the response text and an explicit embodiment cue. Discrete social behaviors
                                            (e.g., listening, greeting) are mapped to validated robot trajectories, while open-ended speaking is paired
                                            with streaming, co-speech motion. This generative motion is governed by a predict-more-than-commit sliding
                                            window that provides temporal look-ahead for motion continuity while limiting physical commitment to a short,
                                            cancellable prefix. Crucially, we design CORTEX, a dual-timescale interaction policy that manages low-latency
                                            streaming and deliberative turn decisions, backed by a robot-side execution layer that enforces physical safety
                                            constraints at the control rate. We deploy MIRA on an Astribot S1 humanoid robot. Quantitative evaluations
                                            demonstrate competitive audio-motion alignment relative to state-of-the-art motion-generation baselines, while
                                            real-robot deployment measurements characterize streaming responsiveness and interruption handling.

                                             Homepage: https://gagajian.github.io/MIRA/




                                         1. Introduction
                                         A companion robot is not only expected to answer a user’s questions, but also to participate in an ongoing
                                         interaction through speech, listening, and physical behavior. A greeting may call for a brief, recognizable
                                         action, and an explanation may call for gestures that follow the rhythm and duration of unfolding speech. As
                                         the conversation evolves, the robot must continuously decide which behavior is appropriate, when to speak,
                                         how to accompany its speech with motion, and how to respond when the user pauses, asks for clarification, or
                                         interrupts. These requirements make companion interaction a continuous embodied process rather than a
                                         sequence of isolated speech responses. On a physical robot, this process is further constrained by the fact that
                                         motion already released for execution cannot be changed as freely as uncommitted text or audio.
                                         This coordination becomes particularly challenging when speaking behavior must be generated online. Unlike
                                         offline co-speech synthesis, the complete response audio may not yet be available when the robot needs to begin
                                         moving. The robot must therefore generate motion from incremental audio while maintaining continuity with
                                         its own previously generated motion. Meanwhile, the conversational state may change before the response is
                                         complete: a user may interrupt, request clarification, or redirect the interaction. A practical companion system
                                         must consequently handle two coupled processes: deciding what the robot should do next at the interaction
                                         level, and continuously generating how that behavior should be expressed at the motion level. The generated
                                         trajectories must additionally satisfy robot-specific kinematic and execution constraints.
                                         Prior work has established the importance of coordinating speech, gesture, and conversational state in
                                         embodied interaction [5, 31]. Co-speech motion generation has subsequently achieved increasingly expressive
                                         and realistic behavior [11, 2, 21, 37, 20], while recent systems have begun to consider streaming behavior
                                         generation and robot embodiment. ProAct [42] combines streaming behavior generation with deliberative social
                                         reasoning, PhysDrift [18] studies robot-native generation under embodiment constraints, and RoboGesture [34]
                                         generates streaming, semantically aligned co-speech gestures on a physical humanoid. Building on these
                                         advances, we investigate the coordination of discrete social behaviors and streaming co-speech motion under
Human Expression                                                          Social Behaviors         Embodied Response
                                                                          Greet / Listen / Dance
                             CORTEX
                             Dialogue and Behavior                          Streaming Speech
                             Decisions

                             Intent + interaction context                          If speak
 “Can you
 explain that?”
                                                      ROSCO
 Words + vocal affect
                                                      Streaming Co-Speech
                                                      Motion Generation
“Actually, wait…”
                                                                                                        Astribot S1
 User Interruption
                                                       Cancel Active Speech + Motion               Constrained Execution

Figure 1 - Real-time embodied companion interaction in MIRA. Given user speech containing
linguistic content and vocal affect, CORTEX infers conversational intent and context. Responses are routed
into two parallel pathways: discrete social behaviors (e.g., greeting, listening) execute pre-validated action
libraries, while open-ended speaking drives ROSCO to generate streaming, speech-synchronized motion.
When a user barge-in occurs (red dashed path), active speech and joint trajectories are immediately preempted
and cancelled at the execution boundary, enabling safe physical halting while retaining conversational context
for subsequent turn arbitration.


changing conversational state. We focus on explicit behavior selection, continuity across motion updates, and
response-level control of outputs awaiting execution.
We present a Full-Duplex Embodied Companion for Natural Human–Robot Interaction (MIRA), for real-time
embodied companion interaction that integrates dialogue control, behavior routing, and robotic streaming co-
speech generation. MIRA treats physical behavior as part of the interaction policy rather than as a downstream
rendering step. At the interface between dialogue and embodiment, MIRA introduces an embodiment cue, a
compact symbolic label that specifies how an admitted response should be physically expressed. The cue
routes the response to either a set of validated social behaviors, such as greeting and listening, or the generative
speaking pathway. This explicit routing allows social behaviors with well-defined physical requirements to
remain reliable while open-ended speech can be accompanied by generative motion. The interaction controller,
CORTEX, combines streaming response generation with deliberative turn admission and a local interruption
gate, allowing the robot to continuously arbitrate between speaking, listening, and changing conversational
turns. Fig. 1 presents the full MIRA framework.
For open-ended speaking behavior, we present ROSCO (Robotic Streaming Co-speech Generator),
which generates robot joint trajectories from streaming audio and recent motion history. ROSCO is designed
for recurrent streaming generation, where motion must remain temporally coherent while adapting to newly
arriving speech. To connect generation with physical execution, we introduce Receding-Horizon Prefix
Commitment (RHPC), which separates the prediction horizon from the physical emission stride: the model
looks ahead over a longer motion window while releasing only a short prefix for execution. This bounded
commitment preserves a longer temporal context for generation while keeping the physically committed
motion short enough to remain responsive to interruptions and changes in conversational state.
We deploy MIRA on an Astribot S1 humanoid robot and evaluate ROSCO on retargeted co-speech motion
dataset BEAT [21]. Our evaluation combines motion-quality comparisons, streaming timing measurements,
and interruption analysis. ROSCO achieves competitive speech-motion alignment while meeting the streaming
emission budget under the evaluated deployment configuration. These results, together with qualitative
real-robot demonstrations of streaming co-speech motion and barge-in handling, demonstrate the feasibility of
MIRA for real-time embodied companion interaction.
The contributions of this work are:
    • We propose MIRA, a real-time full-duplex human-robot interaction framework that coordinates dialogue
      decisions, social behaviors, and streaming co-speech motion through an explicit embodiment-cue protocol


                                                                 2
     and unified response-lifecycle management.
   • We introduce CORTEX, a comprehensive interaction architecture bridging high-level cognition to
     low-level motor control: it actively generates streaming verbal responses and embodiment cues, manages
     dual-timescale turn arbitration, and is grounded by a robot-side execution layer enforcing high-rate
     collision checks, joint constraints, and safe physical halting.
   • We propose ROSCO, a prefix-conditioned diffusion model for streaming audio-to-joint motion generation,
     together with RHPC, an inference scheme that balances a sufficiently long temporal context for motion
     prediction with bounded, interruptible physical commitment.
   • We present a system-level evaluation of motion quality, streaming performance, and interruption
     handling, demonstrating these capabilities on a physical Astribot S1 humanoid robot.


2. Related Work
2.1 Streaming and Full-Duplex Spoken Dialogue Systems
Recent advancements in spoken dialogue systems have shifted from offline, cascade-based perception toward
reactive, streaming interaction. The Audio Interaction Model (AIM) [35] formalizes this shift as an always-on
perceive-decide-respond loop, where a model continuously updates context, decides whether intervention is
warranted, and responds without stopping perception. This direction builds on longstanding work on conver-
sational agents and human–robot turn-taking, including endpointing, overlap management, and incremental
response timing [5, 31]. Related multimodal conversational-agent research also treats speech, visual context,
and social behavior as jointly evolving signals rather than isolated pipeline stages [4, 26]. This framing is
closely related to our setting: a companion robot cannot wait for a complete, fixed input before choosing
whether to speak, hold, or stop. MIRA extends this streaming paradigm from purely auditory response
timing to physical embodiment, where every verbal response is paired with an explicit embodiment decision,
discrete social behaviors are routed to validated motion libraries, and open-ended speaking is accompanied by
streaming co-speech motion under a bounded, interruptible commitment.
Embodied social agents face an inherent temporal tension between high-level cognitive reasoning and low-
latency motor control. While dual-system frameworks such as ProAct [42] decouple behavioral streaming from
cognitive planning to inject proactive intentions, they primarily focus on one-way intention steering and leave
open the physical commitment problem during sudden conversational barge-ins. In contrast, MIRA targets
full-duplex, bi-directional interaction. Beyond proactive turn decisions, MIRA explicitly bounds physical
commitment via RHPC and a robot-side execution bridge to enable safe, low-latency preemption, while
bridging dialogue arbitration and execution through an inspectable, symbolic Embodiment Cue interface
rather than an unconstrained end-to-end trajectory generator.

2.2 Embodied Companion and Affective Interaction
Embodied conversational agents have established that speech, gaze, gesture, facial expression, and dialogue state
should be planned as components of a unified interactive behavior rather than as decoupled outputs [5, 6, 4].
Research on social robot gesture generation likewise shows that communicative motion influences both
the interpretation and perceived naturalness of a robot’s response [30, 40]. Turn-taking research further
demonstrates that endpointing, overlap, and barge-in are central to conversational fluency in human–robot
interaction (HRI) [31]. Companion robots, however, introduce a unique physical commitment problem: delayed
gestures, stale motion packets, and incorrectly cancelled responses remain physically visible and socially
disruptive even after the high-level dialogue state has transitioned.
Affective computing treats vocal, facial, and physiological observations as uncertain evidence about a user’s
internal state rather than direct ground truth [29]. Social robotics likewise emphasizes that emotional
expression must remain legible and appropriate to the specific interaction context [4, 26]. This concern is
also reflected in work on expressive face and body representations, which models identity, pose, and affect
as structured but uncertain components of animation [17, 9, 27, 38]. MIRA aligns with this conservative
paradigm. Instead of mapping noisy vocal affect directly to low-level motor commands, the speech-derived


                                                       3
affect cue is fused with transcript semantics, dialogue history, and interaction state to select an appropriate
high-level embodiment cue, preserving safety and inspectability.

2.3 Language-to-Behavior Interfaces
Language-conditioned robotics commonly decouples high-level reasoning from low-level joint execution. SayCan
combines language-model scores with learned affordances to select discrete robot skills from a pre-defined
library [1], while PaLM-E incorporates embodied observations directly into a multimodal foundation model
for task planning [10]. This line of work is complemented by approaches that learn cross-modal associations
between language and gesture, ground language in embodied observations, and organize robot behavior
through reusable skills [23, 1, 10]. MIRA applies this decoupling philosophy specifically to social response
behavior. The predicted embodiment cue describes how the robot should physically accompany the generated
response at a semantic level, rather than specifying the low-level joint trajectory itself. This compact interface
keeps the dialogue decision highly inspectable and allows downstream motion backends to be modified or
upgraded without altering the high-level CORTEX interaction policy.

2.4 Co-Speech Motion for Avatars and Robots
Rule-based and template-driven systems such as BEAT map linguistic structure directly to communicative ges-
ture specifications [6]. Conversely, data-driven co-speech methods learn high-dimensional motion distributions
from multi-modal inputs including audio, text, speaker identity, and prosodic features [11, 39, 2]. Semantic
and affective annotations further expose the complex one-to-many relationship between an utterance and its
possible gestures [41, 21]. Dataset and representation studies have also expanded the scope of speech-driven
behavior modeling from speaking styles and facial motion to expressive whole-body motion [8, 33, 24, 27, 19].
Related reconstruction methods provide structured estimates of body pose, shape, and expressive components
that are useful for building and evaluating motion representations [15, 14, 16]. Recent generative models
synthesize holistic face, hand, and body motion for virtual characters [37, 20, 22, 25], while speech-driven
facial animation and head-pose methods explore diffusion-based generation for expressive facial movement [32].
Physical robot deployment raises additional kinematic and safety constraints beyond virtual avatar synthesis.
Humanoid robot gesture generation highlights the value of physical embodiment and spatial presence [40, 30],
while human-body representations and general motion-retargeting methods provide important foundations for
transferring expressive motion across embodiments [24, 27, 3]. PhysDrift identifies an embodiment gap when
human-centric, SMPL-X-style motion pipelines are retargeted to robots, arguing for robot-native co-speech
generation under strict joint constraints [18]. RoboGesture further learns a streaming diffusion policy in
humanoid joint space, aligning multi-granular audio cues with co-speech motion and applying an MPC filter
for collision-aware execution on a physical humanoid [34]. MIRA shares this robot-native streaming goal, but
treats co-speech generation as one pathway inside a full-duplex interaction policy: CORTEX arbitrates turns
and barge-in, embodiment cues route between validated discrete social behaviors and generative speaking
motion, and RHPC bounds how much predicted motion may be physically committed.

2.5 Streaming Diffusion and Physical Execution
Diffusion models capture the highly multimodal distribution of plausible communicative gestures [12, 44, 7], and
continuous rotation representations help maintain stable orientation trajectories in neural motion synthesis [43].
Diffusion Transformers provide a flexible denoising backbone for streaming deployment [28], while recent work
explores faster latent or masked generation for reducing the cost of iterative synthesis [22, 36, 20]. However,
strong offline clip synthesis does not define how much motion a robot may safely commit before the current
response and turn boundaries are fully resolved. Streaming physical deployment introduces causal audio
input, generated motion history, cold-start constraints, strict emission deadlines, interruption recovery, and
robot-side safety checks.
MIRA treats these challenges as core components of the motion interface rather than mere implementation
details. Under RHPC, ROSCO predicts an overlapping future horizon from causal audio and generated motion
history, but commits only a short prefix for execution. Retrieved discrete motions and generated continuous



                                                        4
  (a) CORTEX interaction policy                                                                           (b) Embodiment routing                         (c) Robot-side execution

                                                                                                                             Cancel active sentence

                                   Finalized ASR
       Fast interruption                               Deliberative turn
              gate                                          arbiter Parb      admit
                                                                                                                   Streaming PCM audio
                                                                                 Incremental                                                                      Audio playback
       ≥ 450 ms                                                                      TTS
 during playback                                     Shared context & state
 User audio                                                                              rt                                                                   Shared sentence / session ID
                             ASR +                    Reactive dialogue           Cue parser                                       ROSCO
               VAD
                           vocal affect                  generator Pgen           strip prefix                                  Co-speech bridge
                                                       <motion:m> response                                        speak
                                                                                                 mt                             Prefix-DiT, 30 fps
                                                                                                                                                       qpos      Motion validation
                                                                                                           Cue router
                                                                                                                                                                 Session + joint limits
                                                                                                                                                                   Collision checks
    Sentence-scoped Interruption                                                                              Discrete cue
    Stop the active response before admitting the next turn                                                                                                       250 Hz control
                                                                                                                                   Validated                      + SDK dispatch
                                                                                                                                behavior library
               σ                  Clear pending queues if admitted            σ+1
                                   Reject stale packets
              Abort                                                     Admit next turn


                                  Dialogue history is retained                                                                                                 Accepted
                                                                                                                              Retrieved motion clips          commands
                                                                                                                                                                                  Astribot S1


Figure 2 - MIRA system architecture. (a) CORTEX combines the transcript, vocal affect, dialogue
history, and playback state to manage turn admission and stream responses. The cue parser separates
embodiment metadata from response text before TTS. (b) Embodiment cues route motion production to
ROSCO for audio-conditioned co-speech generation or to a validated behavior library for discrete actions. (c)
The robot-side execution layer applies configured joint and collision checks before SDK dispatch and manages
audio playback. Speech and motion share a response identity; the red dashed paths indicate cancellation
requests for the active response, allowing its pending outputs to be invalidated while retaining dialogue history.


trajectories then converge at a robot-side execution boundary that validates session identity, checks physical
constraints, converts timing, and dispatches commands.


3. MIRA System Architecture and Interaction Policy
3.1 System Overview
MIRA provides a real-time orchestration layer that coordinates user intent understanding, response generation,
and embodiment-cue selection with physical execution, with ROSCO (Sec. 4) serving as the streaming co-
speech motion generator for open-ended speaking behavior. To ensure fluid and robust interaction, the system
is designed around four requirements. First, interaction decisions must be contextually appropriate: MIRA
jointly considers the user’s current intent, vocal affect, dialogue history, and interaction state to determine
whether and how to respond, including whether to interrupt ongoing behavior and which embodied behavior
to select. Second, cue-to-motion routing must be inspectable: the dialogue model selects a behavior class
rather than directly controlling robot joints. Third, response generation and embodiment must be streaming:
speech and motion should begin before the complete response is available. Fourth, physical execution must be
contained : generated and retrieved motion are validated by the robot-side bridge for safe execution.
As illustrated in Figure 2, MIRA is organized around three primary functional stages: (a) CORTEX
Interaction Policy, which makes turn-level interaction decisions and produces the response together with an
embodiment cue; (b) Embodiment Routing, which routes the selected cue to either a validated behavior
library or the ROSCO co-speech pathway; and (c) Robot-Side Execution, which processes candidate
motion under hardware-level constraints and dispatches the resulting motion for execution. The CORTEX
Interaction Policy processes incoming user audio to obtain linguistic and vocal-affect information, maintains
conversational and interaction state, and produces a natural-language response together with a symbolic
embodiment cue. The internal decision process, including the dual-timescale policies and interruption handling,
is described in Sec. 3.2. The Embodiment Routing stage maps the selected cue to its corresponding


                                                                                                      5
physical pathway. Discrete social behaviors (e.g., greeting, listen) are retrieved from a validated behavior
library, while the speak cue opens a streaming co-speech session and routes PCM audio to ROSCO. The
resulting motion, together with retrieved behaviors, is passed to the Robot-Side Execution layer, where
session-scoped validation, joint-limit and collision checks, interpolation, and hardware dispatch are performed.

3.2 CORTEX: Dual-Timescale Interaction Policy
CORTEX orchestrates full-duplex embodied dialogue through two cooperative policies for turn admission and
response generation. The Deliberative Turn Arbiter (Parb ) determines whether an incoming utterance
warrants a response and whether ongoing output should be interrupted, while the Reactive Dialogue
Generator (Pgen ) produces spoken responses and embodiment cues for admitted turns. Both policies operate
through a shared connection state, ensuring that downstream speech and motion remain associated with a
single active response even when decisions arrive asynchronously. Moreover, to reduce latency during active
playback, we adopt a low-level, VAD-based Fast Interruption Gate that detects potential user barge-ins
before deliberative turn arbitration is completed.
Fast interruption gate. To minimize barge-in latency, MIRA uses a local VAD-based1 gate to detect
sustained user speech during robot playback. After VAD stabilization, the controller measures the duration of
the ongoing speech segment. If the segment reaches the configured 450 ms interruption-confirmation threshold
while playback is active and embodiment listening mode is disabled, the controller performs an early abort: it
marks the current response as aborted, clears pending TTS output, sends a TTS-stop control message, and
terminates the ongoing robot motion. Meanwhile, audio is sent incrementally to the ASR backend while the
user is speaking. Deliberative Turn Arbiter is triggered only after the backend returns a provider-specific final
or otherwise definitive transcription. If the turn is ignored after an early abort, the controller may generate a
continuation of the interrupted response using its saved response context.
Deliberative Turn Arbiter (Parb ). After an ASR segment is finalized, the Deliberative Turn Arbiter
Parb first applies deterministic rules to handle unambiguous cases, including empty or hesitation-only input
(e.g.,’um’, ’hmm’) and explicit stop or exit commands. For inputs that require semantic arbitration, it invokes a
non-streaming language-model query. The query combines the current transcript, vocal affect, recent dialogue
history, and interaction context, including playback status, whether the dialogue remains active, the robot’s
current or most recent speech, and the preliminary rule decision. These inputs support context-sensitive
judgments about whether an utterance addresses the robot and whether it warrants interrupting the ongoing
response. The Arbiter returns one of three semantic decisions:

                                 Parb ∈ {IGNORE, REPLY, INTERRUPT_AND_REPLY}.                                 (1)

Here, IGNORE declines to admit the input as a new user turn; REPLY admits a turn for response generation;
and INTERRUPT_AND_REPLY requests interruption of the ongoing response before generating a new one. The
controller combines this decision with deterministic rules to determine the final action.
Reactive Dialogue Generator (Pgen ). Once a turn is admitted, CORTEX invokes the Reactive Dialogue
Generator (Pgen ) to interpret the user’s request and formulate a response. Generation is conditioned on the
current transcript, vocal affect, accumulated dialogue history, and configurable persona and task instructions.
The persona and task instructions specify the assistant’s identity, conversational style, and interaction role,
supporting companion dialogue and informational presentations. Based on the inferred intent, the generator
can invoke registered functions, such as weather lookup and music playback. Tool calls and their results are
recorded in the dialogue context, and returned results inform subsequent response generation when needed.
In addition, the model is prompted to emit a symbolic embodiment cue, which is parsed separately from the
spoken text to select the corresponding embodiment route. The response text is streamed to incremental
TTS, allowing speech and associated co-speech motion to begin before the complete response is available.
State handoff and interruption semantics. CORTEX coordinates turn arbitration and response generation
through shared connection state, including playback status, an abort flag, and the current response identifier
σ. When a turn is admitted, the generator creates a response with a fresh identifier, which associates queued
TTS segments and motion-control messages with that response. An interruption marks the current response
  1 https://github.com/snakers4/silero-vad




                                                        6
Table 1 - Representative embodiment-cue vocabulary. The table shows a representative subset of the
cue vocabulary used in our system. Each cue specifies a communicative behavior family or execution route,
which is realized through either streaming co-speech generation or pre-validated robot behaviors.

 Cue              Communicative role                                          Behavior family / route
 speak            General verbal response                                     Streaming co-speech generation
 greeting/wave    Greeting or positive social opening                         Greeting / wave bank
 listen           Turn yielding or invitation to elaborate                    Attentive-listening bank
 confused         Uncertainty, misunderstanding, or failed understanding      Confusion / clarification bank
 apologize        Conversational repair or explicit apology                   Apology / repair bank
 idle             Neutral hold or fallback                                    Idle bank / default pose



as aborted, clears pending output queues, and dispatches speech-stop and motion-end commands. These
operations stop ongoing response production while retaining the dialogue history for subsequent arbitration
and generation. An IGNORE decision does not admit the triggering input as a new user turn. If the response
has already been aborted by the fast interruption gate but the subsequent arbitration does not admit the
input, the controller can use the saved assistant context to generate a continuation of the previous response.
For an INTERRUPT_AND_REPLY decision, the controller requests interruption if playback remains active, then
admits the input as a new user turn and invokes the Reactive Dialogue Generator to produce a replacement
response.

3.3 Embodiment Cue and Routing Interface
The embodiment cue m is the explicit interface between CORTEX and physical behavior. It is serialized as a
compact prefix:
                              < motion: m >; response text,    m ∈ M,                                  (2)
where M is a finite vocabulary of embodiment cues, of which representative examples are shown in Tab. 1.
Embodiment-cue selection jointly considers the user’s utterance, inferred affect, semantic intent, and recent
dialogue history (as mentioned in Reactive Dialogue Generator). These signals are integrated to select a
behavior appropriate to the conversational context, rather than applying a one-to-one mapping between affect
and action. For example, negative affect may increase the likelihood of conversational repair and an apologize
cue when the utterance indicates dissatisfaction, but does not independently determine the selected behavior.
At execution time, a parser separates the cue prefix from the response text before passing the latter to TTS,
preventing control metadata from entering spoken audio. If the cue is missing or malformed, the dispatcher
falls back deterministically to speak for non-empty responses and idle for empty responses.
Embodiment-cue routing. The parsed embodiment cue then determines the downstream embodiment
route. For non-speaking cues, CORTEX forwards the selected behavior family to a retrieval service containing
pre-validated robot motions. These motions provide predictable execution timing and a bounded physical
envelope for discrete social behaviors. For speak, CORTEX instead establishes a co-speech session and
streams the associated TTS audio to ROSCO (Sec. 4), which generates speech-synchronized motion online.
This routing separates behavioral intent from motion realization: CORTEX determines what kind of embodied
response is appropriate, while the corresponding execution module determines how that behavior is physically
realized over time.

3.4 Robot-Side Physical Execution
Robot-side execution bridge and high-rate control. MIRA is deployed on an Astribot S1 humanoid robot.
As a robot-side component of MIRA, the deployed Astribot execution bridge connects the system’s behavior-
generation modules to the robot-side Orin service. It receives either discrete embodiment cues or streaming
co-speech motion, with each motion stream represented as a sequence of qpos frames. The bridge translates
these inputs into robot-side commands and enforces the final physical execution constraints.
Discrete embodiment cues are mapped to pre-validated robot actions and dispatched to the robot. For speak,


                                                       7
the bridge opens a realtime co-speech session and receives a motion stream generated by ROSCO (Sec. 4).
The first qpos frame of the stream is sent to a brief move_to transition. This transition moves the robot
smoothly from the pose produced by the preceding action, or from its current held pose, to the initial co-speech
generated qpos frame, avoiding an abrupt discontinuity at the handoff. Subsequent qpos frames are dispatched
to the robot in realtime.
Before physical dispatch, each qpos frame in the generated motion stream is passed through a collision-aware
projection layer. The layer evaluates the frame in the MuJoCo simulator 2 and solves constrained inverse
kinematics subject to joint-limit and collision constraints. If projection fails, the bridge holds the last safe pose
or invokes the configured fallback policy. On the Orin side, source-rate motion frames, typically generated at
30 Hz, are consumed by a 250 Hz joint-position control loop. The control loop additionally enforces per-tick
joint-step limits before forwarding commands to the Astribot SDK.
The execution bridge thus serves as the final execution and safety layer for physical behavior. When CORTEX
interrupts a response, the active motion session is terminated and invalidated, causing any delayed commands
from that session to be rejected. The controller then holds the last safe pose or invokes the configured fallback
policy. This separation ensures that obsolete or unsafe motion cannot continue after an interruption, while
leaving the dialogue state intact.

3.4.1 Failure Containment and Recovery
As a streaming architecture composed of asynchronous modules and a physical execution loop, MIRA requires
explicit failure isolation across module boundaries. Recovery is therefore handled locally, with each fault
assigned a bounded scope determined by the responsible module. Language-format errors are contained
before reaching TTS; interruptions are handled at the sentence level without invalidating the dialogue session;
insufficient audio evidence prevents new motion from being committed; and collision rejection is handled
independently of speech generation. Physical execution remains subject to the constraints enforced by the
robot-side controller. The modular architecture also makes the individual service components replaceable.
Streaming speech APIs, dialogue models, and downstream behavior services can be wrapped behind the
session-scoped CORTEX interface without changing the cue-routing protocol.


4. ROSCO: Robotic Streaming Co-Speech Generation
The <motion:speak> route requires robot motion to remain synchronized with the temporal structure of
speech, including its rhythm, pauses, and prosodic emphasis. Unlike retrieved behavior families, whose
durations and trajectories are fixed in advance, co-speech motion must unfold continuously with the generated
utterance, while future audio is not yet available. This makes online synchronization particularly challenging:
motion must begin before the complete utterance is synthesized while remaining temporally consistent as new
audio arrives. To address this challenge, we present ROSCO (Robotic Streaming Co-speech generator), a
prefix-conditioned model that generates temporally coherent motion from streaming speech while preserving
continuity across successive output chunks. The overview of ROSCO is presented in Fig. 3.

4.1 Motion Representation and Data Construction
Training samples for ROSCO are retargeted from co-speech dataset BEAT [21] to Astribot S1 joint trajectories
at 30 fps using GMR [3]. Each sample consists of a motion prefix of C = 10 frames and a target motion chunk
of K = 100 frames, together with temporally aligned audio sequences.
To provide richer geometric supervision for motion reconstruction, we represent each motion frame using a rich
motion representation comprising joint qpos, joint velocities, local-body positions, and local link rotations:

                                       xt = [qt , ∆qt , plocal
                                                         t     , Rt6D ] ∈ R460 ,                                  (3)

where qt ∈ R32 denotes the joint qpos sequence, ∆qt ∈ R32 the joint velocity, plocal
                                                                               t     ∈ R132 the Cartesian
positions of 44 tracked body segments, and Rt ∈ R
                                              6D     264
                                                         the local link rotations in the continuous 6D
  2 https://mujoco.org/




                                                          8
 (a) Streaming generation
                                                                                                                                                      (b) Prefix-DiT block
  C = 10        K = 100 (train)
                                                  Causal audio                                            τ                                              τ        Modulation MLP
                                                    encoder
         Previous + current audio                                                                                              Robot motion                              hℓ

                                                                                                                                                                       AdaLN
       Motion prefix + noisy chunk                                                                             X̂i                                              Motion self-attention
                                                Embedding
                                                                      ROSCO-DiT                                                                                           ×      g1
                                                                       8 Prefix-DiT blocks                                                                                +
    Pi                X̃i τ                                                                           Clean current chunk
                                                                                                                                                      Audio            AdaLN
                                                        Latest committed prefix
                                                                                                                                                                Audio cross-attention
                                                                                                                                                        K, V
                                                                                                                                                                          ×      g2
 (c) Training objectives
                                                                                                                                                                          +
         Ai +
                                                                             Reconstruction + FK
                       ROSCO-DiT                X̂i +                              Lrich
                                                                                                               Build next      Next-chunk audio                        AdaLN
                                                                                                                prefix          + noisy motion                 Feed-forward network
                               Shared weights                                                                         P i+1
         Ai −                                                                                                                                                             ×      g3
                                                                            Audio contrast + separation
                       ROSCO-DiT                X̂i −                                                         ROSCO-DiT          X̂i+1                                    +
                                                                                      Laudio
                                                                                                              Shared weights               GT X i+1
                                                                                                                                                                        hℓ+1
 Matched / shuffled audio                                                                                                       Rollout
                                                                                                                                Lrollout                       Causal SA / CA
 Same noisy motion, prefix and diffusion step                                                                                                                  key time ≤ query time



Figure 3 - Overview of ROSCO. (a) Streaming generation. ROSCO-DiT predicts a clean motion
window conditioned on the preceding motion context and causal audio features. The cached rich-motion
history provides the prefix for subsequent updates. (b) Prefix-DiT block. ROSCO-DiT consists of stacked
Prefix-DiT blocks, each applying causal motion self-attention, causal audio cross-attention, and a feed-forward
network. A modulation MLP conditioned on the diffusion timestep τ generates the AdaLN shifts and scales,
together with residual gates g1 , g2 , and g3 . (c) Training objectives. Matched and shuffled audio conditions
share the same noisy motion, motion prefix, and diffusion timestep. The matched prediction is supervised by
the rich-motion reconstruction objective, including kinematic consistency and collision constraints, while a
margin-based audio loss contrasts matched and shuffled conditions through reconstruction loss and joint-qpos
prediction separation. For autoregressive rollout, the matched prediction is detached, its joint velocities are
recomputed from the predicted qpos, and the latest C frames are retained to form the next prefix Pi+1 . The
shared model then predicts the next chunk for rollout supervision.


representation [43]. Joint qpos and local-body positions are normalized using statistics computed over the
training split, with the same statistics reused during inference. Joint velocities are computed from the
unnormalized trajectories and scaled by the joint-position standard deviation. The auxiliary geometric
components are used for training and reconstruction, while only the denormalized joint qpos qt are retained
for downstream robot execution.

4.2 ROSCO-DiT: Prefix-Conditioned Diffusion Transformer
ROSCO employs a prefix-conditioned Diffusion Transformer, termed ROSCO-DiT, to generate each target
motion chunk conditioned on preceding motion and temporally aligned audio. The ROSCO-DiT backbone
consists of eight stacked Prefix-DiT blocks, which extend the standard Diffusion Transformer architecture
with explicit conditioning on preceding motion and its temporally aligned audio. Let Xi ∈ RK×Dm denote the
target rich-motion chunk, Pi ∈ RC×Dm the preceding motion prefix, Ai ∈ RK×Da the audio features aligned
with the target chunk, and Aprev
                              i   ∈ RC×Da the audio features aligned with the prefix. Following the standard
diffusion formulation, Gaussian noise is added to the target motion Xi at diffusion timestep τ :
                                         √        √
                                   X̃iτ = ᾱτ Xi + 1 − ᾱτ ϵ, ϵ ∼ N (0, I).                               (4)

The model then reconstructs the clean target motion conditioned on the motion prefix and aligned audio:

                                                                           X̂i = fθ (X̃iτ , Pi , Ai , Aprev
                                                                                                       i    , τ ),                                                                      (5)


                                                                                                      9
where τ is the diffusion timestep. The noisy target tokens X̃iτ and clean prefix tokens Pi are concatenated
along the temporal dimension and marked with a binary type indicator distinguishing prefix frames from target
frames. The resulting motion sequence is projected to d = 256 dimensions and augmented with sinusoidal
temporal position embeddings. To support streaming inference, temporal information flow is constrained to
be causal at both the audio encoding and motion generation stages. Specifically, the prefix and target audio
sequences are processed by a shared causal audio encoder, producing Eiprev and Ei . Each transformer block
then applies causally masked self-attention over motion tokens, followed by causal audio cross-attention to
the encoded audio, where each motion token can access only audio tokens at the same or earlier temporal
positions, and a feed-forward network. The model uses eight transformer blocks with four attention heads, a
1024-dimensional feed-forward layer, and dropout of 0.1. The output head removes the prefix portion and
predicts only the denoised target chunk X̂i .
The diffusion timestep τ is embedded and injected into each block through adaptive LayerNorm (AdaLN).
Separate modulation parameters are used for the self-attention, audio cross-attention, and feed-forward
branches, including shift, scale, and residual gates.

4.3 Joint Training Objectives and Contrastive Loss
The training objective combines rich-motion reconstruction, kinematic consistency, autoregressive rollout, and
acoustic conditioning. For clarity, we omit the batch and chunk index i in the following formulation.
The model is trained with a global reconstruction loss over the rich motion representation, together with
component-wise losses that explicitly emphasize the joint configuration, velocity, local-body position, and
rotation components, as well as additional kinematic constraints:

                      Lrich =λx MSE(X̂, X) + λq MSE(q̂, q) + λ∆q MSE( c
                                                                     ∆q, ∆q)
                                                                                                             (6)
                              + λp MSE(p̂local , plocal ) + λR MSE(R̂6D , R6D ) + λkin Lkin ,
where λx weights the reconstruction of the complete rich-motion representation, while λq , λ∆q , λp , λR , and
λkin control the contributions of joint qpos, joint velocities, local-body positions, local link rotations, and
kinematic constraints, respectively. ˆ· denotes the predicted component. To constrain the predicted joint qpos,
we incorporate robot-specific kinematic and collision constraints by mapping the predictions to Cartesian
positions through forward kinematics (FK) and explicitly penalizing close-proximity self-collisions. Let FK(q̂t )
denote the forward kinematics function that maps the predicted joint qpos to the Cartesian positions of the
tracked body segments, and let pFKt     = FK(q̂t ) denote its output. We define:
                                                               1X                           2
                    Lkin = λFK-pos MSE(pFK , plocal ) + λcol        [mcol − Clearance(q̂t )]+ ,              (7)
                                                               T t

where Clearance(q̂t ) denotes the minimum pairwise clearance between the collision proxies of the body
segments induced by the predicted qpos. The first term enforces Cartesian consistency through forward
kinematics, while the second encourages a minimum clearance and penalizes potential self-collisions.
Moreover, to mitigate exposure bias during recurrent inference, we additionally perform a two-step autore-
gressive rollout during training. The first predicted chunk is detached and used as the motion prefix for a
subsequent target chunk X ′ , with joint velocities recomputed from the predicted qpos. The rollout loss uses
the same rich-motion objective:
                                            Lrollout = Lrich (X̂ ′ , X ′ ),                               (8)
where X̂ ′ denotes the prediction conditioned on the generated motion prefix.
To prevent the model from over-relying on motion history and ignoring acoustic cues, we construct negative
conditions by cyclically shuffling the current and prefix audio across each training batch. Let L+     rich and
L−
 rich denote the rich-motion reconstruction losses under  matched  and   shuffled audio conditions, respectively.
We encourage the model to assign a higher reconstruction loss to mismatched audio while requiring the
corresponding motion predictions to respond differently:
                                                                  −
                                 Laudio = sg(L+
                                                                     
                                               rich ) + maudio − Lrich +
                                                                                                             (9)
                                          + λsep msep − mean |q̂ + − q̂ − | + ,
                                                                          


                                                       10
  Predict-more-than-commit streaming inference
  50-frame prediction / 15-frame commitment / 10-frame prefix / 30 fps

  Motion frame   -10            0                  15                    30                   45   50                   65              80
                                                            Predict 50

     Calli             Prefix       Commit 15                 Revisable prediction (35)

                                              last 10
                                                                                 Predict 50

     Calli+1                              Prefix        Commit 15                  Revisable prediction (35)

                                                                  last 10
                                                                                                        Predict 50

     Calli+2                                                  Prefix          Commit 15                   Revisable prediction (35)


                                                                                                                                      time
  Only committed rich frames enter the next prefix; joint-angle slices are sent to the controller.
Figure 4 - Overlapping-window streaming inference. Each call predicts 50 frames but commits only
the first 15. The next call advances by 15 frames, reuses the latest 10 committed frames as prefix context,
and predicts an overlapping future horizon.


where q̂ + and q̂ − denote the predicted joint qpos under matched and shuffled audio conditions, respectively.
The margin maudio encourages a margin between the reconstruction losses under matched and mismatched
audio, with matched audio expected to yield a lower loss. In contrast, msep encourages a minimum difference
between the corresponding motion predictions in joint qpos space. The stop-gradient operator sg(·) prevents
the matched-condition loss from being optimized through this comparison. The complete training objective is:

                                          L = λrich Lrich + λroll Lrollout + λaudio Laudio .                                             (10)


4.4 Receding-Horizon Prefix Commitment Inference
To balance the need for a sufficiently long temporal context with the low-latency requirements of streaming
robot execution, we design Receding-Horizon Prefix Commitment (RHPC), as shown in Fig. 4. Rather
than generating and committing short motion chunks independently, RHPC maintains a longer prediction
horizon while committing only a short leading segment at each inference step. Since no ground-truth motion
history is available at test time, inference in ROSCO differs from offline clip prediction. Specifically, at the
start of a speaking turn, the streaming bridge initializes the motion prefix P0 ∈ RC×Dm and corresponding
audio context Aprev
                 0    with zero tensors. The generated motion chunk is then fed back as the prefix for the
subsequent inference step, enabling autoregressive streaming generation.
At each inference step, the model consumes 50 temporally aligned audio tokens and predicts an extended
50-frame rich-motion window, but only the first 15 frames are committed to the robot controller. At the next
inference step, the model predicts the next 50-frame window using the latest 10 committed frames as the
motion prefix, with the commitment progressing by 15 frames at each step. The 10-frame overlap improves
continuity between newly generated and previously committed motion, resulting in smoother transitions
across chunk boundaries. Maintaining this 50-frame prediction horizon serves two practical purposes. First, it
preserves a temporal sequence length closer to that used during training, reducing the train-test distribution
mismatch that would arise from applying diffusion denoising to substantially shorter sequences. Second, it
provides an extended trajectory candidate that allows downstream kinematic projection and collision checks
to assess future motion feasibility before commands are dispatched.
The 15-frame commitment also bounds the amount of motion exposed to the robot at each inference step,
which is beneficial for full-duplex interaction. Since only 15 frames (0.50 s) are committed at a time, an
interruption triggered by CORTEX does not require discarding a long pre-generated trajectory. Instead, the
active motion session can be terminated after the currently committed segment, while continuity is preserved
up to the last committed frame and the system remains responsive to user barge-in.



                                                                       11
5. Experiments
We evaluate MIRA as an end-to-end embodied interaction system along three complementary dimensions:
(i) co-speech motion quality, (ii) real-time streaming performance, (iii) contextual turn arbitration on real
interaction traces. The evaluation combines component-level measurements with end-to-end experiments on a
physical humanoid platform.
We conduct all physical experiments on an Astribot S1 deployment integrating CORTEX, the validated
behavior service, the ROSCO co-speech bridge, and the robot-side controller. Unless otherwise specified, all
experiments use the same trained model and deployment configuration. We visualize several representative
robot motions from the embodiment-cue vocabulary in Fig. 5.

5.1 Implementation Details
ROSCO operates at 30 fps with 16 kHz mono audio. Each training sample contains a C = 10-frame motion
prefix and a K = 100-frame target chunk, corresponding to approximately 0.33 s and 3.33 s, respectively.
Samples near the beginning of a clip are left-padded with the initial motion frame to obtain a fixed-length prefix.
The rich-motion representation has dimension Dm = 460, comprising 32 joint qpos, 32 joint velocities, 132
local-body position values, and 264 local link rotations represented using the continuous 6D representation [43].
Only the denormalized joint qpos are used for downstream robot execution.
For each motion frame, the audio descriptor consists of 80 log-mel channels and four low-latency prosodic
features—log energy, delta log energy, positive onset strength, and zero-crossing rate—giving Da = 84. The
audio features are processed by a causal dilated encoder with dilation rates [1, 2, 4, 8, 16], shared between
the prefix and target audio streams. The ROSCO-DiT projects motion tokens to d = 256 dimensions and
uses eight Prefix-DiT blocks with four attention heads and a 1024-dimensional feed-forward layer. Sinusoidal
temporal position embeddings are applied to the motion tokens, while the diffusion timestep is injected into
each transformer block through AdaLN. The diffusion process follows the standard DDPM noise schedule [12].
To improve robustness to the incomplete and self-generated context encountered during streaming inference,
we apply condition corruption during training and perform a two-step autoregressive rollout. Audio conditions
are independently masked, while the motion prefix is randomly removed, truncated, or perturbed with
Gaussian noise. In the autoregressive rollout, the motion generated in the first prediction is detached and
reused as the prefix for the second prediction, with joint velocities recomputed from the generated joint qpos.
The second-step rollout loss is weighted by λroll = 0.5. These procedures expose the model to the imperfect
conditioning states that arise during streaming deployment.
At deployment, ROSCO performs causal inference using a 50-frame temporal window with a 15-frame
commitment. Incoming TTS audio is resampled from 24 kHz to 16 kHz mono before entering the inference
stream. The inference procedure follows the Receding-Horizon Prefix Commitment strategy described in
Sec. 4.4. Only the denormalized joint qpos of the committed 15 frames are transmitted to the robot controller,
while the remaining rich-motion predictions are retained internally for subsequent inference.

5.2 ROSCO Motion Quality Evaluation
Dataset and Comparison Methods. We evaluate the algorithmic motion quality of ROSCO on the
retargeted BEAT [21] test set. We compare against representative co-speech motion generation methods,
including GestureLSM [22] and MIBURI [25]. For all comparison methods, the generated motions are
retargeted to the Astribot S1 using the same retargeting protocol as described in Sec. 4.1, i.e., GMR [3]. We
evaluate three complementary aspects of generated motion: audio-motion synchronization, motion-distribution
fidelity, and physical executability. All metrics are computed from robot kinematic states (i.e., FK positions)
obtained by applying mj_forward to the predicted or retargeted qpos trajectories.
Audio-Motion Synchronization. For audio-motion synchronization, we report two complementary beat-
level synchronization metrics: Beat Consistency (BC) [22] and BeatAlign [13]. Since the two metrics use
different beat extraction and alignment procedures, we report them separately rather than treating their
scores as directly interchangeable. For BC, let A = {ai } denote the audio-onset timestamps detected from the
input waveform, where each ai marks the temporal location of a detected audio onset. Let pt,j ∈ R3 denote


                                                        12
 Wave




 Wiggle




 Dance




Figure 5 - Visualization of representative robot motions in the embodiment-cue vocabulary.
Each embodiment cue is associated with multiple pre-authored motion chunks, from which one is randomly
selected during interaction.


the FK position of the j-th selected joint at frame t. We compute the frame-to-frame speed of each selected
joint and detect local minima using an order of seven frames. We then retain local minima with normalized
speed above 0.3, producing an independent motion-beat set Mj for each joint. For each audio onset a ∈ A,
we find its nearest motion beat in Mj and apply a Gaussian temporal weighting:
                                             d(a, Mj )2
                                                       
                              1 X
                      BCj =          exp −         2      ,  d(a, Mj ) = min |a − m|,                  (11)
                             |A|                 2σE                     m∈Mj
                                 a∈A

where σE = 0.3 s. The final BC score is obtained by averaging the per-joint scores over the J selected joints:
                                                             J
                                                       1X
                                                BC =         BCj .                                        (12)
                                                       J j=1

Thus, BC measures audio-to-motion temporal alignment independently for each selected joint, without merging
motion beats across joints. For BeatAlign, we instead construct a single global motion signal by averaging the
frame-difference speed over the J selected joints:
                                                   J
                                                1X
                                         ut =         ∥pt+1,j − pt,j ∥2 .                                 (13)
                                                J j=1

We detect local minima of ut , requiring adjacent motion beats to be at least 0.25 s apart, yielding a single
global motion-beat set M . BeatAlign then computes the audio-to-motion alignment as
                                                   d(a, M )2
                                                            
                                     1 X
               BeatAlign(A, M ) =           exp −       2      ,   d(a, M ) = min |a − m|,               (14)
                                    |A|              2σB                      m∈M
                                        a∈A

where σB = 3 motion frames = 0.1 s at FPS = 30. This score averages over audio onsets and therefore
measures how well the generated robot motion covers the detected audio onsets.


                                                        13
Table 2 - Quantitative evaluation of ROSCO. BC and BeatAlign measure audio-motion synchronization,
FID-G measures geometric motion-distribution discrepancy, and Collision Rate measures the rate of kinematic
self-collision. Bold values indicate the best performance among generative baselines.

 Method                       BC ↑              BeatAlign ↑             FID-G ↓             Collision Rate (%) ↓
 Ground Truth (GT)           0.2536                0.5600                  –                      6.51%
 GestureLSM [22]             0.0049                0.5849               0.3420                    3.09%
 MIBURI [25]                 0.0766                0.5552               0.2427                    3.01%
 ROSCO (Ours)                0.3039                0.5726               0.1111                    2.61%



Motion-Distribution Fidelity. To measure motion-distribution fidelity, we compute FID-G distance. For
each prediction-reference pair, we first truncate both trajectories to their common duration and resample them
to a common frame rate. We remove global translation by expressing each selected body position relative
to the root body. For each clip, we summarize each root-local position dimension over time using its mean,
standard deviation, 5-th percentile, and 95-th percentile, yielding a fixed-dimensional geometry feature vector.
We then compute the Fréchet distance between the predicted and reference feature distributions:
                                                                                
                             FID-G = ∥µp − µr ∥22 + Tr Σp + Σr − 2(Σp Σr )1/2 ,                            (15)

where µp and Σp denote the empirical mean vector and covariance matrix of the predicted geometry features,
respectively, and µr and Σr denote those of the reference features. Lower FID-G indicates closer alignment
with the reference motion distribution.
Kinematic self-collision proxy. To assess simulation-based feasibility, we replay every predicted qpos
frame in the full Astribot MuJoCo model and call mj_forward without stepping the dynamics. Thus, the
supplied trajectory is evaluated kinematically, without modification by gravity, contacts, or actuators. We
count contacts with non-positive signed distance and distinguish self-collisions from environment collisions
using MuJoCo body identifiers. We report the self-collision frame rate, defined as the fraction of frames
containing at least one self-contact. This simulator-based measure serves as a proxy for physical executability,
but does not by itself guarantee successful hardware execution.
Evaluation Results. As shown in Table 2, ROSCO achieves the highest BC score among the generative
baselines, indicating stronger rhythmic synchronization between the detected audio onsets and generated
motion beats. It also remains competitive on BeatAlign, where a higher score indicates better temporal
alignment between motion dynamics and the rhythmic structure of the input audio. This suggests that ROSCO
can effectively capture audio-driven motion timing beyond simple frame-wise correspondence. In addition,
ROSCO obtains the lowest FID-G among the reported generative models, indicating that its generated motion
better matches the geometric distribution of real motion.
Notably, ROSCO also achieves a low collision rate, substantially lower than the retargeted ground-truth
motions. This difference is expected because the GMR retargeting process primarily aims to preserve the
kinematic correspondence between the source and target embodiments, without explicitly optimizing for
collision avoidance. As a result, the retargeted reference motions can still contain physically undesirable
configurations, as reflected by the relatively high collision rate of 6.51% for GT. In contrast, ROSCO
incorporates a collision-aware training objective that explicitly penalizes physically implausible motions during
generation. This encourages the model to learn motions that balance audio-motion alignment with the physical
constraints of the target robot, rather than simply reproducing the potentially colliding retargeted trajectories.
Together with its strong BeatAlign and BC scores, the results suggest that ROSCO can preserve audio-driven
rhythmic and temporal correspondence while producing motion that is more compatible with robot execution.

5.3 Real-Time Generation and Full-Duplex Responsiveness
Continuous human-robot interaction imposes three temporal requirements on the embodied system: (i)
Streaming Efficiency: motion synthesis must run faster than physical playback to support continuous
motion execution; (ii) Turn Responsiveness: the system should minimize the delay before speech and
motion begin; and (iii) Full-Duplex Preemption: ongoing speech and physical execution must be promptly


                                                       14
Table 3 - Runtime latency and full-duplex responsiveness of MIRA on Astribot S1. Evaluated
across multi-turn interaction sessions. user_turn denotes the committed user transcript post-ASR. All metrics
report the median (P50).

 Pipeline Stage / Metric                                  Measurement Window                 Median (P50)
 Upstream Cognitive Breakdown
  Streaming ASR Endpointing                               speech_end → user_turn                 10.0 ms
  LLM First-Token Latency (TTFT)                          user_turn → llm_first_token             1.62 s
  Streaming Audio Ingress                                 llm_first_token → pcm_received         493 ms
 Streaming Motion Generation
   ROSCO Chunk Inference Time (Tgen )                     pcm_received → motion_ready            195 ms
   Emission Real-Time Factor (RTF)                        Tgen /Tmotion (Tmotion = 500 ms)        0.390
 Interactive Responsiveness
   First Synthesized Speech                               user_turn → tts_first_audio             2.20 s
   Co-Speech Motion Synchronization                       user_turn → first_motion_udp            2.36 s
 Full-Duplex Preemption
   Deterministic Interruption Preemption                  speech_started → abort_cmd_sent        466 ms


interruptible upon user barge-in. We benchmark these three aspects on the physical Astribot S1 platform across
continuous multi-turn interaction sessions. Table 3 summarizes the median (P50) runtime measurements.
Streaming Motion Generation Efficiency. Streaming viability requires that the time to generate a
motion chunk, denoted by Tgen , be shorter than the physical duration of the committed motion, denoted by
Tmotion , i.e., Tgen < Tmotion or equivalently RTF < 1.0. With a Tmotion = 500 ms committed motion duration,
ROSCO completes prefix-conditioned diffusion inference in only 195 ms (pcm_received → motion_ready),
yielding an emission RTF of 0.390. This indicates that motion generation operates substantially faster than
physical playback, leaving sufficient runtime margin to sustain continuous trajectory execution under the
evaluated deployment conditions.
Turn Startup and Audio–Motion Coupling. In conversational turn transitions, the component breakdown
shows that startup latency is dominated by upstream cognitive processing rather than motion synthesis. Local
ASR endpointing introduces only 10.0 ms (speech_end → user_turn), while LLM first-token generation
(1.62 s) and initial audio streaming to PCM ingress (493 ms) contribute most of the latency before first
speech emission (tts_first_audio at 2.20 s). Once audio becomes available, ROSCO generates the initial
joint trajectory within 195 ms of audio ingress, with motion dispatched to the hardware bridge at 2.36 s
(first_motion_udp).
Full-Duplex Interruption Preemption. MIRA combines RHPC with a dedicated VAD-based interruption
gate (i.e., Fast Interruption Gate) to support prompt barge-in handling. RHPC commits only the leading
15 frames (500 ms) of each 50-frame prediction horizon, thereby strictly bounding the amount of motion
committed ahead of physical execution. When user vocalization is detected during robot speech, the
interruption gate requests active-audio cancellation and dispatches an asynchronous abort command. As
reported in Table 3, the preemption latency is 466 ms at the median, measured from speech onset (speech_-
started) to abort-command dispatch (abort_cmd_sent). This bounded commitment mechanism limits the
amount of precomputed motion that can remain committed after a user barge-in, while enabling subsequent
turn arbitration to proceed without waiting for the ongoing motion sequence to complete.

5.4 Multi-Party Turn Arbitration and Addressivity
We evaluate CORTEX in unconstrained multi-party interaction using a production trace corpus containing 199
active sessions, 36,448 recorded events, and 559 completed turn decisions. Among these decisions, 302 resulted
in REPLY, 88 in INTERRUPT_AND_REPLY, and 169 in IGNORE. Rather than evaluating isolated interruption
examples, this trace-based evaluation examines whether CORTEX can distinguish speech addressed to the
robot from concurrent third-party speech and decide whether an ongoing response should be continued or
interrupted. Four representative cases are summarized in Table 4.


                                                     15
Table 4 - Representative multi-party turn-arbitration cases. The examples show how the arbiter uses
dialogue context for unclear cases and predefined rules for clear cases. The Fast Interruption Gate provides a
separate fast path for physical interruption.

 Case Family              User Utterance             Decision Basis               Decision
   Case A        “Just sent the location to them.”   Dialogue context             IGNORE
   Case B            “No, that will not work.”       Dialogue context             INTERRUPT_AND_REPLY
   Case C                     “Um.”                  Predefined rule              IGNORE
   Case D                    “MIRA.”                 Predefined rule              INTERRUPT_AND_REPLY


Non-addressed speech. Case A demonstrates CORTEX’s ability to handle multi-party overhearing and
recover gracefully from false-alarm early aborts. While the robot is presenting, a bystander says “Just sent
the location to them” to another person, with vocalization exceeding the 450 ms threshold. Because physical
preemption prioritizes low-latency halting, the Fast Interruption Gate triggers an early_barge_in_abort,
temporarily pausing active speech and holding the robot motion. Once the finalized ASR transcript arrives,
the Deliberative Turn Arbiter evaluates the preceding conversational context and determines the utterance
was not addressed to the robot, returning IGNORE. Rather than discarding interaction progress or terminating
awkwardly, CORTEX retrieves the saved response context and seamlessly generates a continuation from the
interrupted breakpoint, successfully recovering from the environmental false-alarm.
Context-dependent interruption. Case B demonstrates how CORTEX handles a short utterance whose
intent is unclear from the utterance alone. The user says “No, that will not work” while the robot is presenting
a proposal. The utterance itself does not provide enough information to determine the appropriate response,
so the Deliberative Turn Arbiter uses the preceding dialogue context to infer the user’s intent and returns
INTERRUPT_AND_REPLY. Importantly, the physical preemption does not wait for this decision. In this trace, the
Fast Interruption Gate emitted an early_barge_in_abort event before the finalized ASR transcript reached
Parb . This separation allows the robot to stop promptly while the Deliberative Turn Arbiter continues to
determine how to respond to the interruption.
Rule-based decisions. Cases C and D show that clear inputs can be handled directly by predefined rules in
the Deliberative Turn Arbiter. In Case C, the user produces a brief hesitation filler (“Um”, duration < 450 ms)
during playback. Because the utterance does not satisfy the sustained 450 ms confirmation threshold, the
Fast Interruption Gate is not engaged. Upon ASR finalization, the arbiter matches the filler rule and returns
IGNORE within ∼10 ms, allowing continuous robot playback to proceed completely undisturbed. In Case D,
the user issues an explicit wake word (“MIRA”). The Fast Interruption Gate initiates the hardware abort at
450 ms, and the arbiter confirms the addressivity via wake-word detection, returning INTERRUPT_AND_REPLY
only 2 ms after the gate’s decision.
Together, these cases demonstrate how CORTEX combines rule-based decisions with context-based reasoning
within the Deliberative Turn Arbiter. Clear inputs, such as fillers and explicit wake-word commands, can be
handled directly by predefined rules, while short or ambiguous utterances can be interpreted using the preceding
dialogue context. The Fast Interruption Gate handles the time-critical physical stop separately, allowing the
robot to stop promptly without waiting for the dialogue-level decision. This design enables CORTEX to avoid
unnecessary interruptions while responding quickly when an interruption is clearly required.


6. Discussion and Limitations
System Insights: Hybrid Embodiment and Streaming Quality. MIRA couples dialogue reasoning,
motion generation, and physical execution into a unified interactive loop. Rather than treating motion as
a passive downstream rendering step, our hybrid routing separates discrete social actions from open-ended
speaking: pre-validated motion libraries provide deterministic safety envelopes for repeatable behaviors
(e.g., greetings, listening), while streaming diffusion dynamically adapts to unpredictable speech prosody.
In continuous physical deployment, streaming quality emerges as an end-to-end system property. Beyond


                                                      16
the generative capacity of the diffusion backbone, real-time fluidity depends critically on prefix feedback,
receding-horizon commitment schedules, boundary preemption, and robot-side execution safeguards.
Limitations and Future Scope. The current framework has several practical limitations that outline
avenues for future investigation: (1) the embodiment vocabulary is currently constrained, where incorporating
joint semantic text conditioning alongside audio prosody could further enrich gesture expressivity; (2) the
physical safety layer requires embodiment-specific kinematic tuning and collision geometry modeling for new
robot platforms; and (3) turn startup latency remains largely bounded by the upstream cascaded pipeline
(ASR → LLM → TTS), where integrating native end-to-end speech-to-speech (omni) foundation models
represents a promising avenue to substantially compress initial response delay. Finally, while our quantitative
benchmarks establish the essential technical viability, streaming throughput, and physical containment required
for embodied interaction, long-term human-subject studies in naturalistic environments remain an important
next step to fully assess subjective companion dynamics and sustained user engagement.


7. Conclusion
We presented MIRA, a unified framework for real-time embodied companion interaction. MIRA links user-
intent understanding, response generation, embodiment-cue prediction, and robot motion within a single
streaming architecture. CORTEX maintains the interaction state, starts streaming responses, manages
deliberative turn decisions, and handles bounded-latency interruption. Validated behavior families provide
discrete social actions, while a prefix-conditioned diffusion model ROSCO generates open-ended co-speech
motion from incremental audio and generated motion history. During streaming inference, RHPC maintains a
long prediction horizon for smooth streaming motion while limiting physical commitment to a short leading
segment. Finally, a robot-side bridge provides a final safety layer, enforcing timing and physical constraints
for safe execution. Together, these components form an extensible architecture that translates companion
responses and embodiment cues into timely, expressive, and physically contained robot behavior.


References
 [1] Michael Ahn, Anthony Brohan, Noah Brown, et al. 2023. Do As I Can, Not As I Say: Grounding
     Language in Robotic Affordances. In Conference on Robot Learning (CoRL), Vol. 205. PMLR, Auckland,
     New Zealand, 287–318.
 [2] Tenglong Ao, Qingzhe Gao, Yuke Lou, Baoquan Chen, and Libin Liu. 2022. Rhythmic Gesticulator:
     Rhythm-Aware Co-Speech Gesture Synthesis with Hierarchical Neural Embeddings. ACM Transactions
     on Graphics (TOG) 41, 6 (2022), 209:1–209:19.
 [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. 2025. Retargeting Matters: General
     Motion Retargeting for Humanoid Motion Tracking. arXiv preprint arXiv:2510.02252 (2025).
 [4] Cynthia Breazeal. 2003. Emotion and Sociable Humanoid Robots. International Journal of Human-
     Computer Studies 59, 1–2 (2003), 119–155. doi:10.1016/S1071-5819(03)00018-1
 [5] Justine Cassell, Joseph Sullivan, Scott Prevost, and Elizabeth Churchill (Eds.). 2000. Embodied Conver-
     sational Agents. MIT Press, Cambridge, MA, USA.
 [6] Justine Cassell, Hannes Hogni Vilhjalmsson, and Timothy W. Bickmore. 2001. BEAT: The Behavior
     Expression Animation Toolkit. In ACM SIGGRAPH. ACM, New York, NY, USA, 477–486.
 [7] Junming Chen, Yunfei Liu, Jianan Wang, Ailing Zeng, Yu Li, and Qifeng Chen. 2024. DiffSHEG: A
     Diffusion-Based Approach for Real-Time Speech-Driven Holistic 3D Expression and Gesture Generation.
     In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). IEEE, Los Alamitos,
     CA, USA, 7352–7361.
 [8] Daniel Cudeiro, Timo Bolkart, Cassidy Laidlaw, Anurag Ranjan, and Michael J. Black. 2019. Capture,
     Learning, and Synthesis of 3D Speaking Styles. In Proceedings of the IEEE/CVF Conference on Computer
     Vision and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 10101–10111.


                                                      17
 [9] Radek Danecek, Michael J. Black, and Timo Bolkart. 2022. EMOCA: Emotion Driven Monocular Face
     Capture and Animation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
     Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 20311–20322.
[10] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, et al. 2023. PaLM-E: An Embodied Multimodal Language
     Model. In International Conference on Machine Learning (ICML), Vol. 202. PMLR, Honolulu, Hawaii,
     USA, 8469–8488.
[11] Shiry Ginosar, Amir Bar, Gefen Kohavi, Caroline Chan, Andrew Owens, and Jitendra Malik. 2019.
     Learning Individual Styles of Conversational Gesture. In IEEE/CVF Conference on Computer Vision
     and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 3497–3506.
[12] Jonathan Ho, Ajay Jain, and Pieter Abbeel. 2020. Denoising Diffusion Probabilistic Models. In Advances
     in Neural Information Processing Systems (NeurIPS), Vol. 33. Curran Associates, Inc., Red Hook, NY,
     USA, 6840–6851.
[13] Siqiao Huang, Kun-Ying Lee, Dongming Qiao, Guanqi He, Zhenyu Wang, Yitang Li, Shaoting Zhu,
     and Hang Zhao. 2026. OMG: Omni-Modal Motion Generation for Generalist Humanoid Control. arXiv
     preprint arXiv:2606.10340 (2026).
[14] Muhammed Kocabas, Chun-Hao P. Huang, Otmar Hilliges, and Michael J. Black. 2021. PARE: Part
     Attention Regressor for 3D Human Body Estimation. In Proceedings of the IEEE/CVF International
     Conference on Computer Vision (ICCV). IEEE, Los Alamitos, CA, USA, 11127–11137.
[15] Nikos Kolotouros, Georgios Pavlakos, Michael J. Black, and Kostas Daniilidis. 2019. Learning to
     Reconstruct 3D Human Pose and Shape via Model-Fitting in the Loop. In Proceedings of the IEEE/CVF
     International Conference on Computer Vision (ICCV). IEEE, Los Alamitos, CA, USA, 2252–2261.
[16] Nikos Kolotouros, Georgios Pavlakos, Dinesh Jayaraman, and Kostas Daniilidis. 2021. Probabilistic
     Modeling for Human Mesh Recovery. In Proceedings of the IEEE/CVF International Conference on
     Computer Vision (ICCV). IEEE, Los Alamitos, CA, USA, 11605–11614.
[17] Tianye Li, Timo Bolkart, Michael J. Black, Hao Li, and Javier Romero. 2017. Learning a model of facial
     shape and expression from 4D scans. ACM Transactions on Graphics (Proc. SIGGRAPH Asia) 36, 6
     (2017), 194:1–194:17. doi:10.1145/3130800.3130813
[18] Zhangzhao Liang, Xiaofen Xing, Mingyue Yang, Wenlve Zhou, and Xiangmin Xu. 2026. PhysDrift:
     Bridging the Embodiment Gap in Humanoid Co-Speech Motion Generation. arXiv:2606.19935 [cs.AI]
[19] Jing Lin, Ailing Zeng, Haoqian Wang, Lei Zhang, and Yu Li. 2023. One-Stage 3D Whole-Body Mesh
     Recovery with Component Aware Transformer. In Proceedings of the IEEE/CVF Conference on Computer
     Vision and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 21159–21168.
[20] Haiyang Liu, Zihao Zhu, Giorgio Becherini, Yichen Peng, Mingyang Su, You Zhou, Xuefei Zhe, Naoya
     Iwamoto, Bo Zheng, and Michael J. Black. 2024. EMAGE: Towards Unified Holistic Co-Speech Gesture
     Generation via Expressive Masked Audio Gesture Modeling. In IEEE/CVF Conference on Computer
     Vision and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 1144–1154.
[21] Haiyang Liu, Zihao Zhu, Naoya Iwamoto, Yichen Peng, Zhengqing Li, You Zhou, Elif Bozkurt, and Bo
     Zheng. 2022. BEAT: A Large-Scale Semantic and Emotional Multi-Modal Dataset for Conversational
     Gestures Synthesis. In European Conference on Computer Vision (ECCV). Springer, Cham, Switzerland,
     612–630.
[22] Pinxin Liu, Luchuan Song, Junhua Huang, Haiyang Liu, and Chenliang Xu. 2025. Gesturelsm: La-
     tent shortcut based co-speech gesture generation with spatial-temporal modeling. In 2025 IEEE/CVF
     International Conference on Computer Vision (ICCV). IEEE, 10929–10939.
[23] Xian Liu, Qianyi Wu, Hang Zhou, Yinghao Xu, Rui Qian, Xinyi Lin, Xiaowei Zhou, Wayne Wu, Bo Dai,
     and Bolei Zhou. 2022. Learning Hierarchical Cross-Modal Association for Co-Speech Gesture Generation.
     In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
     IEEE, Los Alamitos, CA, USA, 10462–10472.



                                                    18
[24] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J. Black. 2015.
     SMPL: A Skinned Multi-Person Linear Model. ACM Transactions on Graphics (Proc. SIGGRAPH Asia)
     34, 6 (2015), 248:1–248:16.
[25] M. Hamza Mughal, Rishabh Dabral, Vera Demberg, and Christian Theobalt. 2026. MIBURI: Towards
     Expressive Interactive Gesture Synthesis. In Proceedings of the IEEE/CVF Conference on Computer
     Vision and Pattern Recognition (CVPR).
[26] Ana Paiva, Iolanda Leite, Hana Boukricha, and Ipke Wachsmuth. 2017. Empathy in Virtual Agents and
     Robots: A Survey. ACM Transactions on Interactive Intelligent Systems 7, 3, Article 11 (2017), 40 pages.
     doi:10.1145/2912150
[27] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed A. A. Osman, Dimitrios
     Tzionas, and Michael J. Black. 2019. Expressive Body Capture: 3D Hands, Face, and Body from a
     Single Image. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
     (CVPR). IEEE, Los Alamitos, CA, USA, 10975–10985.
[28] William Peebles and Saining Xie. 2023. Scalable Diffusion Models with Transformers. In IEEE/CVF
     International Conference on Computer Vision (ICCV). IEEE, Los Alamitos, CA, USA, 4172–4182.
[29] Rosalind W. Picard. 1997. Affective Computing. MIT Press, Cambridge, MA, USA.
[30] Maha Salem, Stefan Kopp, Ipke Wachsmuth, Katharina Rohlfing, and Frank Joublin. 2012. Generation
     and Evaluation of Communicative Robot Gesture. International Journal of Social Robotics 4, 2 (2012),
     201–217. doi:10.1007/s12369-011-0124-9
[31] Gabriel Skantze. 2021. Turn-Taking in Conversational Systems and Human-Robot Interaction: A Review.
     Computer Speech & Language 67 (2021), 101178. doi:10.1016/j.csl.2020.101178
[32] Zhiyao Sun, Tian Lv, Sheng Ye, Matthieu Lin, Jenny Sheng, Yu-Hui Wen, Minjing Yu, and Yong-Jin Liu.
     2024. DiffPoseTalk: Speech-Driven Stylistic 3D Facial Animation and Head Pose Generation via Diffusion
     Models. ACM Transactions on Graphics (TOG) 43, 4, Article 46 (2024), 9 pages. doi:10.1145/3658221
[33] Kaisiyuan Wang, Qianyi Wu, Linsen Song, Zhuoqian Yang, Wayne Wu, Chen Qian, Ran He, Yu Qiao,
     and Chen Change Loy. 2020. MEAD: A Large-scale Audio-visual Dataset for Emotional Talking-face
     Generation. In Computer Vision – ECCV 2020. Springer, Cham, Switzerland, 700–717. doi:10.1007/
     978-3-030-58589-1_42
[34] Zifan Wang, Ziang Ren, Pengyang Shi, Zirui Wang, Chenghuai Lin, Tianze Wang, Zekun Qi, Liangliang
     Zhao, He Wang, and Li Yi. 2026. RoboGesture: Real-Time Semantic-aligned Co-Speech Gestures
     Generation for Humanoid Interaction. arXiv:2608.28693 [cs.RO]
[35] Zhifei Xie, Zihang Liu, Ze An, Xiaobin Hu, Yue Liao, Ziyang Ma, Dongchao Yang, Mingbao Lin, Deheng
     Ye, Shuicheng Yan, and Chunyan Miao. 2026. Audio Interaction Model. arXiv:2606.05121 [cs.SD]
[36] Quanwei Yang, Luying Huang, Kaisiyuan Wang, Jiazhi Guan, Shengyi He, Fengguo Li, Hang Zhou,
     Lingyun Yu, Yingying Li, Haocheng Feng, and Hongtao Xie. 2025. GestureHYDRA: Semantic Co-speech
     Gesture Synthesis via Hybrid Modality Diffusion Transformer and Cascaded-Synchronized Retrieval-
     Augmented Generation. In Proceedings of the IEEE/CVF International Conference on Computer Vision
     (ICCV). IEEE, Honolulu, HI, USA, 12615–12625.
[37] Hongwei Yi, Hualin Liang, Yifei Liu, Qiong Cao, Yandong Wen, Timo Bolkart, Dacheng Tao, and
     Michael J. Black. 2023. Generating Holistic 3D Human Motion from Speech. In IEEE/CVF Conference
     on Computer Vision and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 469–480.
[38] Wanqi Yin, Zhongang Cai, Ruisi Wang, Ailing Zeng, Chen Wei, Qingping Sun, Haiyi Mei, Yanjun Wang,
     Hui En Pang, Mingyuan Zhang, Lei Zhang, Chen Change Loy, Atsushi Yamashita, Lei Yang, and Ziwei Liu.
     2026. SMPLest-X: Ultimate Scaling for Expressive Human Pose and Shape Estimation. IEEE Transactions
     on Pattern Analysis and Machine Intelligence 48, 2 (2026), 1778–1794. doi:10.1109/TPAMI.2025.3618174
[39] Youngwoo Yoon, Bok Cha, Joo-Haeng Lee, Minsu Jang, Jaeyeon Lee, Jaehong Kim, and Geehyuk Lee.



                                                     19
    2020. Speech Gesture Generation from the Trimodal Context of Text, Audio, and Speaker Identity. ACM
    Transactions on Graphics (TOG) 39, 6 (2020), 222:1–222:16.
[40] Youngwoo Yoon, Woo-Ri Ko, Minsu Jang, Jaeyeon Lee, Jaehong Kim, and Geehyuk Lee. 2019. Robots
     Learn Social Skills: End-to-End Learning of Co-Speech Gesture Generation for Humanoid Robots. In
     IEEE International Conference on Robotics and Automation (ICRA). IEEE, Piscataway, NJ, USA,
     4303–4309. doi:10.1109/ICRA.2019.8793720
[41] Zeyi Zhang, Tenglong Ao, Yuyao Zhang, Qingzhe Gao, Chuan Lin, Baoquan Chen, and Libin Liu. 2024.
     Semantic Gesticulator: Semantics-Aware Co-Speech Gesture Synthesis. ACM Transactions on Graphics
     (TOG) 43, 4 (2024), 136:1–136:17.
[42] Zeyi Zhang, Zixi Kang, Ruijie Zhao, Yusen Feng, Biao Jiang, and Libin Liu. 2026. ProAct: A Dual-System
     Framework for Proactive Embodied Social Agents. arXiv:2602.14048 [cs.RO]
[43] Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. 2019. On the Continuity of Rotation
     Representations in Neural Networks. In IEEE/CVF Conference on Computer Vision and Pattern
     Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 5745–5753.
[44] Lingting Zhu, Xian Liu, Xuanyu Liu, Rui Qian, Ziwei Liu, and Lequan Yu. 2023. Taming Diffusion
     Models for Audio-Driven Co-Speech Gesture Generation. In IEEE/CVF Conference on Computer Vision
     and Pattern Recognition (CVPR). IEEE, Los Alamitos, CA, USA, 10544–10553.




                                                    20

