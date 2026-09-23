# SteerDuplex: Steerable Duplex Speech Dialogue Models
Source: https://arxiv.org/abs/2609.12623
Kind: pdf
Fetched: 2026-09-22T09:29:45.768601+00:00
Tool: pdftotext

                                         S TEER D UPLEX: Steerable Duplex Speech
                                         Dialogue Models
                                         Utkarsh Tyagi1*† , Ramaneswaran Selvakumar2* , Advait Gosai1 , Sonal Kumar2 , Nikhil Barhate1 ,
                                         Isabell Sagar1 , Steven Li1 , Miheer Bavare1 , Daniel Quigley1 , Fabiola Tapia Carrillo1 , Jose M Patron
                                         E1 , Diego Macías Gutiérrez1 , Paul Song1 , Ramani Duraiswami2 , Dinesh Manocha2 , Yunzhong He1




arXiv:2609.12623v1 [cs.AI] 11 Sep 2026
                                         1 Scale AI, 2 University of Maryland, * Equal contribution. † Project lead.


                                            utkarsh.tyagi@scale.com | https://github.com/Utkarsh4430/SteerDuplex




                                            Abstract
                                            Full-duplex spoken dialogue models support low-latency turn taking, interruption handling, and
                                            backchanneling, yet a key capability remains underexplored: steerability, the ability to reliably
                                            shift conversational behavior along attributes such as tone, persona, speaking rate, and voice style
                                            in response to user instructions. We introduce a taxonomy of text- and audio-based steerability
                                            that identifies substantial gaps in current full-duplex models. To address this gap, we introduce
                                            S TEER D UPLEX, a Moshi-based full-duplex speech model fine-tuned on natural conversations and
                                            synthetic dialogues targeting instruction following, vocal delivery, reasoning, and duplex inter-
                                            action. We further apply two-stage reinforcement learning (RL) with hybrid rewards, combining
                                            verifiable interaction checks and judge-based semantic feedback to improve timing and response
                                            continuity. To evaluate full-duplex spoken steerability, we introduce S TEER B ENCH, a benchmark
                                            with 390 spoken prompts and 1,067 human-authored binary audio and text rubrics spanning tone,
                                            persona, style/accent, and speed/length. On S TEER B ENCH, supervised training improves audio-
                                            steering average pass rate by 44.5 percentage points over the strongest evaluated open baseline. On
                                            Audio MultiChallenge, task average pass rate improves by 7 points over its strongest evaluated
                                            open baseline. RL further raises source-clean interruption response from 72.5% to 82.5% and reduces
                                            synthetic pause barge-in from 26.5% to 9%. Steering and aggregate task scores remain comparable
                                            or higher, while reward probes reveal reward hacking through incomplete responses. Our model
                                            and benchmark support systematic research on spoken steerability, with reward analysis showing
                                            why timing gains must be evaluated alongside response completeness.




                                         1 Introduction
                                         Spoken dialogue conveys emotion, accent, and timing cues that text transcripts alone do not preserve.
                                         End-to-end models process this acoustic information directly [8], but useful conversational partners
                                         must also manage when to speak and follow instructions about content and vocal delivery.


                                                                                                           1
                                                                                                                                                                        Scale AI Research



  1 TEXT-BASED STEERABILITY                                           2 AUDIO-BASED STEERABILITY                                         3 GENERAL DUPLEX CAPABILITIES
     Steer the assistant via natural language instructions              Steerability through audio cues and voice adaptation               Foundational full-duplex interaction abilities

                                          Be sarcastic for the rest      Paralinguistic
      Tone Control                                                                                           (User sighs heavily)                                            (User finishes)
                                          of this call.                  Understanding
      Adopt and sustain a                                                                                                                   Turn-Taking
                                                                         Detect non-lexical cues
      requested emotional            Sure, adopting a                                                                                       Detect when to start and
                                                                         (laughter, sighs,
      tone across the                sarcastic tone for the                                             You sound stressed.                 stop speaking.              (Responds within ~500
                                                                         emotion) and respond
      conversation.                  remainder of our                                                   Want to talk about it?                                          ms)
                                                                         appropriately.
                                     conversation.

                                          You are a 70-year-old          Speech
                                          retired literature             Understanding from                  (User whispers)                                                 (User interrupts)
      Persona Control                     professor.                                                                                        Graceful Interruption
                                                                         Acoustics
      Maintain a specified role,                                                                                                            Handling
                                     Ah, an excellent                    Infer details from
      identity, or character                                                                            You're speaking softly,             Yield immediately when
                                     question. Let us consider           acoustics (accent, age,                                                                        (Stops speaking
      consistently.                                                                                     I'll whisper back to                the user interrupts.
                                     the nuances of the text             environment) and adapt                                                                         immediately)
                                                                                                        match.
                                     carefully.                          responses.

                                          One-sentence answers                                               Speak louder, I'm in a
      Speed & Length                                                     Voice / Style Editing                                              Backchanneling                   (User speaking…)
                                          only, please.                                                      noisy room.
      Control                                                            Modify how the assistant                                           Use short
      Adjust speaking pace                                               sounds (volume, pace,                                              acknowledgments
                                     Quantum entanglement                pitch, warmth, etc.) on                                            ("mm-hmm", "I see") at
      and response length
                                     is correlated particle              request.                       (Speaks louder)                     the right moments.          Mm-hmm, I see.
      (verbosity) as requested.
                                     behavior.

                                          (mid-conv) Be more
      Dynamic Mid-Conv.                                                                                      What was my flight
                                          empathetic - having a          Audio-Context                                                                                       (Long pause)
      Steering                                                                                               number again?                  Pause Handling
                                          bad day.                       Memory
      User steering in the                                                                                                                  Handle natural pauses,
                                                                         Remember and reason
      middle of the conv. from       Sorry to hear. I will adapt                                                                            hesitations, and silence
                                                                         over details present only      Your flight number is UA
      the next turn onward           my tone to be more                                                                                     appropriately.              Take your time.
                                                                         in earlier audio.              1247.
      without losing context.        supportive.


                                                                         Self-Coherence Over                 (User interrupts multiple      Mid-Utterance                    Set an alarm for 7 — no
      Graceful Refusal /                  Now speak as a man.
                                                                         Audio                               times, changes topics)         Corrections                      wait, 8 AM.
      Failure
                                                                         Consistent voice, tone,                                            Maintain coherence
      Decline unsupported or
                                     Can't change my voice               and style across turns,                                            across mid-utterance
      unsafe steering requests                                                                          (Continues in the same
                                     mid-conv., but I can still          interruptions, and topic                                           corrections and topic       Okay, alarm set for 8 AM.
      instead of silently failing.                                                                      voice and tone)
                                     help.                               shifts.                                                            shifts.



Figure 1. A capability taxonomy for full-duplex spoken dialogue. The taxonomy distinguishes natural-language
steering, acoustic understanding and adaptation, and general duplex interaction. Examples are schematic, not
model outputs or latency measurements. The taxonomy describes a broader design space than the present bench-
mark: S TEER B ENCH tests requested content and delivery across tone, persona, style/accent, and speed/length;
AudioMC, VoiceBench, and FDB provide complementary task and interaction evaluations.

Full-duplex systems listen and speak simultaneously, enabling turn taking, backchanneling, and inter-
ruption handling within an ongoing conversation [8, 15, 37]. Early systems established joint two-channel
modeling [25] while later work improved synchronization and stream interleaving [36, 39]. Fluent turn
taking does not guarantee that systems follow user instructions about tone, persona, or delivery.
Hence, a useful interactive system must also be steerable along such attributes. Recent role- and
voice-conditioned models make these attributes explicit control inputs [29]. We use steerability to mean
the reliable shift of such behavior in response to user instructions. Text-model research distinguishes
steerability from ordinary instruction following [3], with controllable-generation methods ranging from
explicit control codes [17] to broader adaptation approaches [19]. Evaluating this control in speech
requires acoustic evidence, since speech-assessment studies distinguish lexical content from speech
quality and paralinguistic features [24].
We organize spoken steerability into a capability taxonomy (Figure 1). Its three families connect what
the model says, how it sounds, and how it participates: natural-language steering, acoustic understanding
and adaptation, and duplex interaction. The distinction matters because task compliance and floor
management require separate checks: duplex benchmarks assess pauses, interruptions, and backchannels
as distinct behaviors [22]. The taxonomy guides training and evaluation by assessing requested content
and delivery alongside intelligibility, timing, and task capability.
To measure how steerable current full-duplex models are, we introduce S TEER B ENCH. Its 390 spoken
prompts combine concrete tasks with steering requests and use separate text and audio rubrics to assess
content and delivery. Fixed reference clips anchor the requested acoustic style. Under matched items and


                                                                                                    2
                                                                                              Scale AI Research



the same judge, M OSHI and P ERSONA P LEX reach audio-steering average pass rates of only 20.55% and
16.44%, respectively (Section 4). These results motivate our central question: can targeted post-training
make full-duplex models more steerable while preserving their general conversational capability?
To study this question, we fine-tune S TEER D UPLEX, built on the public M OSHI backbone [8], on recorded
conversations and synthetic speech/text examples covering instruction following, requested delivery,
reasoning, safety, and duplex interaction (Section 3.1). Continuing from this checkpoint, two-stage RL
combines programmatic interaction rewards with judge-based transcript rubrics to optimize sampled
speech continuations. Outcome-based and multi-signal rewards have proved useful in broader post-
training [18, 33]; recent work extends them to speech timing and interaction [14, 26]. Our design couples
these objectives with incentives to sustain an answer until the user takes the floor.
Our reward design keeps content and delivery separate, since each requires different evidence. Text
rubrics can judge whether an answer addresses a task, but cannot establish its prosody or speaking
rate; audio-reference rubrics make delivery criteria concrete, and timing and waveform checks identify
premature responses, silence, or invalid speech. The first RL stage pairs these timing and transcript
rewards with response-continuity and waveform-validity checks; a second stage adds a continuation-
duration bonus and dedicated user-backchannel sampling. This design is motivated by a recurring
failure mode in our experiments, where a model improves interruption metrics by yielding too readily,
including when it should continue speaking (Section 7).
P ERSONA P LEX supports voice and role conditioning [29], while F-A CTOR learns instruction-controlled
conversational behavior through supervised training [40]. ASPIRin isolates speaking decisions from
token selection [14], and Ohashi et al. [26] combine interaction rewards with semantic feedback. Our
contribution couples a steerability taxonomy with S TEER B ENCH, which checks requested content and
reference-grounded vocal delivery separately. We combine targeted supervised steering with continuity-
aware, two-stage RL and evaluate both alongside general task performance. Reward probes show how
timing gains can mask incomplete responses.
Taken together, our contributions are fourfold: (i) We propose S TEER D UPLEX, a full-duplex speech
model built around a taxonomy that connects instruction-based steering, acoustic delivery, and con-
versational interaction (Figure 1). (ii) We introduce S TEER B ENCH, with 390 spoken prompts and 1,067
human-authored rubrics that assess content and reference-grounded delivery across tone, persona,
style/accent, and speed/length (Section 4). (iii) We combine supervised fine-tuning, which establishes
steering and task capability, with continuity-aware RL, which improves interruption response and pause
handling while maintaining comparable or higher steering and aggregate task scores (Section 6). (iv) We
characterize reward hacking: isolated rewards admit empty speech, while interruption optimization can
weaken continuation after listener feedback (Section 7).

2 Related Work
Full-duplex speech models. Early two-channel dialogue modeling [25] and subsequent synchronization
and stream-interleaving methods [36, 39] established the basis for simultaneous listening and speaking.
M OSHI combines parallel user and assistant audio streams with a time-aligned text channel [8]; later
systems extend real-time duplex interaction [15, 37]. P ERSONA P LEX introduces role and voice condition-
ing [29], and F-A CTOR studies interactional control through supervised imitation [40]. We build on this
model family to study requested content and delivery alongside conversational timing.
Steering and audio understanding. Controllable text generation conditions outputs on style, sentiment,
or persona [7, 17, 19]. Steerability studies distinguish reliable behavioral control from ordinary instruction


                                                      3
                                                                                           Scale AI Research



following [3], using supervised adaptation [4] or consistency rewards [1]. Extending this control to
speech requires grounding instructions in acoustic information. Audio-language models have developed
broader understanding and reasoning capabilities [9], while compositional and multi-task benchmarks
test whether they can reason about relations and events in audio [10, 30]. These abilities help models
interpret acoustic context; controlling their own delivery remains a separate problem.
Evaluating spoken interaction. Voice-assistant evaluations cover spoken instruction following [5], the
integration of paralinguistic and visual cues [31], and retention of instructions and revisions across
turns [13]. Adversarial audio-grounding tests additionally show that standard task scores can conceal
responses unsupported by the input [32]. Duplex benchmarks complement these evaluations with event
timing and multi-turn task completion [20, 22]. S TEER B ENCH adds content and delivery rubrics for
explicit steering requests, alongside measures of task success and interaction.
Reinforcement learning for speech. GRPO and component-normalized variants optimize sampled
outputs with multiple rewards [16, 23, 33]. Speech applications include alignment from annotated
conversations [2, 38], timing optimization [14], and joint alignment of duplex interaction behaviors [26].
Reinforcement learning with verifiable rewards (RLVR) uses answer and constraint checks [18]; qualita-
tive criteria require other forms of feedback. Policy-aware rubric weighting [35] and rubric-conditioned
self-distillation without a training-time verifier [28] study these signals in general model post-training.
For speech RL, the corresponding design problem also includes acoustic validity and timing: semantic
feedback must reward responsiveness without encouraging incomplete answers.

3 SteerDuplex: Post-Training for Speech Control
S TEER D UPLEX builds on the M OSHI architecture [8]. Supervised fine-tuning produces the model,
S TEER D UPLEX-SFT. Two-stage RL with hybrid rewards then refines its interaction behavior (Figure 2).
We call the resulting checkpoint S TEER D UPLEX-RL (“+ RL” in tables); S TEER D UPLEX alone denotes
the supervised model. The hybrid objective combines verifiable programmatic interaction rewards
(RLVR-style) with judge-based semantic rewards.

3.1 Supervised Fine-Tuning
The model retains Moshi’s temporal transformer, depth transformer, and hierarchical audio codec. A
natural-language system prompt prefixes the assistant-text stream; both audio streams remain silent
during the prefix, and a delimiter marks its end. We mask the prompt tokens in the training loss and use
the same conditioning format throughout training and inference. We split conversations at alignment
boundaries and cap context and response at 300 seconds, subject to shorter benchmark limits.
The supervised training mixture combines natural conversations with targeted examples of instruction
following, steering, duplex interaction, safety, and reasoning. Natural speech supplies variation in
prosody, overlap, and turn structure; targeted examples supply explicit steering instructions and com-
plete conversation state. The mixture contains 504,416 audio records and 65,675 text records, sampled at
88% and 12% of the training mass, respectively. Audio durations sum to 8,510.9 hours of audio records;
repeated source material means this is not a count of unique recording hours. Fixed sampling weights
keep smaller targeted subsets represented without allowing synthetic examples to dominate. Quality
checks cover semantic consistency, audio validity, provenance, privacy, and safety. We use word-level
alignment from Qwen3-ForcedAligner-0.6B [34] and turn-aware loss masks. Appendix G gives
data composition and Appendix A gives training settings.



                                                    4
                                                                                                                                           Scale AI Research



 a     Conditioning and speech streams                                        b       RQ-Transformer               c     Hybrid rewards

                                                                                    Previous text + audio codes
                System-prompt prefix · masked in loss                                                                  Verifiable timing                       1.0

                          prefix              joint sequence                          Temporal transformer             Transcript rubric                   0.75

       user · acoustic                                                                  Causal · joint streams         Response continuity                     0.5
      user · semantic                                                                      300 s context
                                                                                                                       Continuation (stage 2)                  2.0
     agent · acoustic
     agent · semantic                                                                  Depth transformer           Normalize within rollout groups,
                                                                                                                   then combine components.
          agent · text                                                                      8 hierarchical
                                                                                           RVQ codebooks
                                                                     t                                                        Waveform validity
  Silent prefix audio; joint generation at 12.5 Hz.                                   Predict text + audio codes          Silence · clipping · invalid audio



 d     SFT followed by hybrid RL

           Supervised fine-tuning                                          RL stage 1                                          RL stage 2
     Natural conversations + requested steering                Semantic response + timing + continuity             Continuation after listener feedback



Figure 2. SteerDuplex architecture and training. (a) A masked system-prompt prefix conditions joint audio/text
streams. (b) Temporal and depth transformers predict hierarchical audio codes. (c) Grouped continuations receive
component-normalized rewards and waveform validity checks. (d) SFT initializes RL stages rewarding response
continuity, then continuation after listener feedback. Each RL stage freezes its initial model as the KL reference.

3.2 Two-Stage Reinforcement Learning
RL optimizes sampled continuations from interaction windows spanning turns, interruptions, pauses,
backchannels, noise, and speech-mirror scenarios. We filter CANDOR material to remove identified
overlap with evaluation conversations. Each window contains aligned user audio, assistant history,
transcripts, timing targets, and semantic grading metadata. Each rollout group shares one context.
For speech-text rollouts sharing a context, Group reward-Decoupled Normalization Policy Optimization
(GDPO) [23] normalizes each reward separately before combining components:
                                                                              (k)
                                                                            Ri      − mean(R(k) )
                                                          Âi = ∑ wk                              .                                                                  (1)
                                                                    k             std(R(k) ) + ϵ
          (k)
Here Ri is reward component k for rollout i. This normalization prevents a component’s raw scale from
dominating the update. A component that is constant within a group contributes no learning signal.
Stage 1: response continuity. The first stage starts from the supervised checkpoint and uses it as a frozen
KL reference. In addition to interaction timing and transcript rewards, it includes a response-continuity
term with weight 0.5 and a 4-second first-response target. This term discourages short responses that
satisfy a timing event but fail to sustain an answer.
Stage 2: continuation after listener feedback. The second stage initializes both policy and KL reference
from the first-stage checkpoint. It retains the continuity term and adds a continuation-duration bonus of
weight 2.0, with a 4-second target, on noise and user-backchannel events. Dedicated user-backchannel
sampling emphasizes these events. This stage rewards continuing through listener feedback that does not
request the floor. Both stages use a policy loss over text-stream actions and an adaptive sampled-action
KL penalty, rather than the exact full-distribution KL of Ohashi et al. [26]. Moshi’s temporal transformer
processes joint audio/text history and supplies both text logits and the representation used by the audio
decoder, so text-action gradients can change subsequent speech generation. We include sampled padding
tokens because they encode frames without a new text token, making their timing relevant to pauses

                                                                                  5
                                                                                                               Scale AI Research



and speech onset; excluding them would remove credit from these decisions. Audio-codebook actions
receive no direct policy loss. Appendix A gives the training settings.

3.3 Rewards and Audio Validity
The RL objective combines interaction timing rewards (weight 1.0), the continuity terms above, a Gemini
3.6 Flash transcript judge on turn and interruption groups (weight 0.75), and a waveform-integrity
gate. Timing rewards distinguish responding, yielding, waiting, and continuing; the judge assesses
semantic response quality. Waveform checks reject silence, clipping, and invalid outputs. Interruption
credit requires assistant speech before the interruption, preventing silence from earning yielding credit.
Appendix A.1 lists the weights; Section 7 examines reward shortcuts and trade-offs.
Reference-audio rubrics evaluate steerability but do not enter the reported RL objective. Given a
target clip, generated speech, and both transcripts, the judge assesses requested delivery, prosody, rate,
articulation, naturalness, and task success. Speaker identity matters only when explicitly requested by
the rubric. Fixed references give acoustic criteria a concrete target, although audio presentation and
prompting can influence judge reliability [24].

4 SteerBench: Evaluating Spoken Steerability
S TEER B ENCH tests whether a model can satisfy a spoken steering request while completing a concrete
task. It contains 390 prompts across tone, persona, style/accent, and speed/length, with 1,067 human-
authored binary rubrics: 438 audio rubrics and 629 text rubrics. The test set is disjoint from the supervised
and RL training data. Inference is audio-in/audio-out under the shared system prompt in Appendix D.1.
Text rubrics are judged from transcripts; audio rubrics use fixed synthetic and human-sourced reference
clips. Human reviewers validate references against the requested delivery. Appendices D.2 and D.5
detail judging and human agreement.
We distinguish three aggregation levels. Audio-steering average pass rate (APR) is the percentage of
examples that satisfy every applicable audio rubric. Sample APR additionally requires every text rubric
to pass. Rubric pass rate averages the individual binary decisions. These measures distinguish delivery
control from full task compliance; passing many rubrics need not mean completing the task.1
Under matched items, rubric implementation, and the Gemini 3.6 Flash judge, the supervised model
reaches 65.10 ± 1.13% audio-steering APR, compared with 20.55% for M OSHI and 16.44% for P ERSON -
A P LEX (Figure 3). Sample APR ranges from 32% to 51.11%; individual-rubric pass rates range from
63.10% to 77.03%. Reliably satisfying every constraint remains difficult.

5 Evaluation Setup
Benchmarks and baselines. Alongside S TEER B ENCH, we evaluate multi-turn robustness with Audio
MultiChallenge [13], spoken instruction following with VoiceBench [5], and interaction with Full-Duplex-
Bench (FDB) [20, 22]. FDB-v1 tests individual events; its v1.5 extension tests interruption and overlap
handling [21]; FDB-v2 evaluates multi-turn task sessions. We compare with M OSHI and P ERSONA P LEX
to assess steerability gains alongside maintained or improved task performance and duplex interaction.
Published hosted-model results provide context, with model identities and protocol differences stated in
the tables. Repeated benchmark evaluations report means and population standard deviations across
three decoding runs. Published baseline scores retain their source protocols. See Appendix F.
  1 Passing three of four rubrics gives a 75% rubric pass rate, but the example fails an all-constraints pass criterion.




                                                               6
                                                                                                                         Scale AI Research



  a Audio-steering performance                                b Completing every constraint

                    +44.5 percentage points over Moshi                               All constraints               Individual rubrics


                                                                         Tone                          49.7                 71.5
           Moshi                20.55

                                                                      Persona                          51.1                     77
      PersonaPlex          16.44
                                                                Style / accent                     48.4                     69.8

    SteerDuplex                                   65.10
                                                                Speed / length                32                         63.1


                    0      20           40   60      80                          0           25               50           75           100
                                 Audio APR (%)                                                     Pass rate (%)


Figure 3. Steering improves, but complete task compliance remains difficult. (a) Audio-steering APR on matched
items. SFT reaches 65.10 ± 1.13% over three runs; baseline scores retain their source protocols. (b) These same
three runs supply sample APR and individual-rubric pass rates. Gemini 3.6 Flash judges both panels; see Table 10.

Source overlap. Some official FDB-v1 turn-taking and pause examples reuse CANDOR conversations
present in supervised training. We treat those scores as diagnostics. To assess generalization, we use
FDB-v2, the 498-example FDB-v1.5 split without Fisher/CANDOR material, and FDB-v1’s source-clean
synthetic interruption, synthetic pause, and backchannel tasks.
Checkpoint selection. We select the RL checkpoint on a separate development set targeting the inter-
action and task capabilities measured by the benchmarks. We freeze the checkpoint before benchmark
evaluation; benchmark test scores do not influence checkpoint choice (Appendix B).

6 Results
The supervised model establishes steering and task capability. RL then improves interruption response
and pause handling with comparable or higher steering and aggregate task means. We compare task
performance before examining these gains and costs.

6.1 Multi-Turn and General Spoken Capability
On Audio MultiChallenge, S TEER D UPLEX obtains 13.64 ± 0.28% APR and 37.17 ± 1.33% average rubric
score (ARS), compared with 6.64% and 20.56% for the strongest open baseline, P ERSONA P LEX (Table 1).
Fully successful multi-turn tasks remain uncommon, particularly those requiring spoken revisions.
On FDB-v2, the supervised model scores 4.17 under the slow examiner, exceeding M OSHI (2.59) and
P ERSONA P LEX (2.65) in every task family. Its VoiceBench mean is 40.87 ± 0.27, compared with 38.55 for
M OSHI and 30.51 for P ERSONA P LEX. Table 1 gives the task breakdowns; the same SFT runs serve as the
reference for RL within each benchmark.

6.2 RL Improves Interruption Response and Pause Handling
On source-clean FDB-v1.5, RL raises correct response after interruption from 72.5% to 82.5% (Figure 4).
Continuation after a user backchannel rises from 71.4% to 80.6%. Background-speech recovery changes
from 60% to 59%; recovery after speech directed elsewhere rises from 42% to 48%.
On synthetic pause items, barge-in falls from 26.5% to 9%, a difference of −17.5 percentage points. On
the synthetic interruption task, response rate rises from 96% to 97.7%, while semantic score changes from

                                                          7
                                                                                                                               Scale AI Research



Table 1. Supervised task performance. SteerDuplex averages three runs per benchmark; baseline scores retain
their source protocols; ± denotes population standard deviation. AudioMC scores are percentages; FDB-v2 uses
a 1–5 scale; VoiceBench retains its official scales and paired subscores. Higher is better; bold marks the best
displayed score per column, with paired subscores compared separately. AudioMC axes: instruction memory
(IM), instruction revision (IR), self-correction (SC), and voice editing (VE).
                                                       (a) Audio MultiChallenge

Model                        APR (%)             ARS (%)                     IM                     IR                    SC                    VE
M OSHI                         3.98                 14.29                  9.09                  2.50                 3.61                         0
P ERSONA P LEX                 6.64                 20.56                 10.61                  6.67                 9.64                         0
S TEER D UPLEX           13.64±0.28            37.17±1.33                 17.93                 14.17                21.69                      2.56

                                                        (b) Full-Duplex-Bench v2

Model                           Correction                  Daily                      Entity                    Safety                     Mean
M OSHI                                  2.78                  2.26                       2.63                      2.68                         2.59
P ERSONA P LEX                          3.38                  2.06                       2.51                      2.66                         2.65
S TEER D UPLEX                          4.21                  3.74                       4.07                      4.65                         4.17

                                                              (c) VoiceBench

Model               Alpaca       Common WildVoice               SD-QA                   IFEval            BBH       AdvBench            Overall
M OSHI                2.15            1.94      1.49          25.4 / 35.3              9.9 / 19.4         49.9            68.2            38.55
P ERSONA P LEX        2.45            2.29      1.56          20.6 / 27.8               9 / 17.2          48.6            5.3             30.51
S TEER D UPLEX        2.28            2.21      1.74         26.88 / 26.88             10 / 19.7          49.9            99.3         40.87±0.27



  a Waiting through a pause                       b Responding under overlap

  Barge-in rate (%) · lower is better            Success rate (%) · higher is better
                                                                                                                                 SFT       RL


     30                                                       Interruption                                                     72.5      82.5
            26.5

                                                       Background speech                                                         60        59
     20

                                                       Other conversation                                                        42        48
     10                          9
                                                        User backchannel                                                       71.4      80.6
      0
             SFT                 RL                                          0         25        50       75          100
                                                                                            Success (%)
          -17.5 pp     3 runs


Figure 4. RL improves when to wait and when to respond. (a) Source-clean synthetic pause barge-in averaged
across three runs per model; error bars show population standard deviation. (b) FDB-v1.5 success on 498 paired
examples. Table 11 reports the condition sizes and success rates.

3.94 to 3.88 and mean takeover latency increases by 40 ms (Table 5). Thus better response timing does
not imply uniform improvement in every interaction measure.

6.3 Steering, Task Scores, and Interaction Costs
The comparison (Table 2) gives comparable or higher steering and aggregate task means. VoiceBench
rises from 40.87 to 41.38, and FDB-v2 safety from 4.65 to 4.81. FDB-v2 mean task score changes by only



                                                                      8
                                                                                                                       Scale AI Research



                       Table 2. Capability and interaction. Higher is better; bold marks best displayed
                       scores, including ties. Three runs per model; full dispersion is in Table 5.

                       Metric                                                                          SFT     + RL
                       Steering and task capability
                       S TEER B ENCH rubric pass (%)                                                  63.75    65.22
                       AudioMC APR (%)                                                                13.64    14.38
                       VoiceBench overall                                                             40.87    41.38
                       FDB-v2 task mean                                                                4.17     4.17
                       Conversational behavior
                       FDB-v2 turn taking                                                              4.18     4.19
                       FDB-v2 instruction following                                                    3.67     3.81


  a Task capability after RL                                            b Task and event differences

  FDB-v2 task scores · higher is better                                 Difference between means
                                                       SFT    RL


      Correction                                    4.21     4.41                                   -0.003
                                                                                  Task mean

           Daily                                    3.74     3.41                                                           +0.153
                                                                                      Safety
          Entity                                    4.07     4.04
                                                                                                       +0.018
                                                                                 Turn taking
          Safety                                    4.65     4.81
                                                                                                                         +0.134
                                                                                  Instruction
           Mean                                     4.17     4.17                   following

                   1      2       3         4   5                                               −0.05 0.00    0.05   0.10   0.15   0.20
                              Score (1–5)                                                                Change in score


Figure 5. Task capability. (a) FDB-v2 task-family means; error bars show population standard deviation across
three runs per model. (b) Differences between means for task and event scores. Each model uses the same three
runs in both panels. Colors indicate the direction of the point difference, not statistical significance. Higher is
better. Table 5 reports dispersion.

−0.003; its per-event turn-taking and instruction-following differences are +0.018 and +0.134 (Figure 5).
These task-level means do not establish that every conversational behavior is retained.
RL also takes over the floor less often during user backchannels (4.8% versus 9.1% for SFT). However,
aggregate task scores can conceal premature yielding in other contexts. Section 7 examines this tension
between holding and yielding the floor.

7 Reward Design and Optimization Dynamics
We examine response continuity, reward hacking, and sensitivity to training choices. Appendix C gives
the full comparisons and judge checks.

7.1 Continuity Supports Sustained Responses
Without our continuity additions, an SFT-initialized control using the original interaction recipe continues
for only 1.10 seconds after a user backchannel in the fixed development diagnostic. FDB-v2 turn taking
scores 3.93, versus 4.18 for SFT, 4.04 after stage 1, and 4.19 after stage 2. Differences in interaction pools,
optimization settings, and training budgets preclude attributing these gains solely to continuity rewards.



                                                                    9
                                                                                                                     Scale AI Research



  a Empty speech under isolated rewards                                    b Conversational usefulness

  Empty outputs / 96 · lower is better                                     Shared duplex diagnostic · higher is better


           Text rubric only                                      47                      0.055

         Audio rubric only                                  41                      0.000

        Audio quality only                                  41                      0.000

          Promptness only                         25                                0.000

         Joint composite          4                                                                                      0.371

                              0       12     24        36    48                  0.0        0.1      0.2       0.3       0.4
                                           Empty outputs                                          Duplex score


Figure 6. Isolated rewards admit empty or unresponsive speech. Separate reward probes each evaluate 96
held-out sampled rollouts. Left: empty outputs; lower is better. Right: the shared duplex diagnostic; higher
is better. The joint composite improves both diagnostics but still leaves four empty outputs. These probes are
separate from the reported RL model. Scalar training rewards use different objectives and should not be compared
across conditions. Table 9 gives the full results.

The second stage sustains longer responses: SFT, stage 1, and RL average 22.1, 20.1, and 23.0 words
per utterance across three FDB-v2 daily-task runs. Development continuation after a user backchannel
rises from SFT’s 2.60 seconds to 3.20 seconds. Yet RL ends daily-task utterances while the examiner is
speaking more often than SFT (32.3% versus 23.6%), despite longer responses.

7.2 Reward Hacking in Duplex Speech
A model that remains silent can earn interruption credit without ever yielding. Requiring speech before
the interruption closes this shortcut; continuity rewards additionally encourage sustained speech when
the user has not taken the floor.
In separate reward probes (Figure 6), promptness-only optimization attains a scalar reward of 0.670 but
scores zero on the shared duplex diagnostic, leaving 25 of 96 rollouts empty. Text-only, audio-rubric-only,
and audio-quality-only objectives leave 47, 41, and 41 empty rollouts. The joint composite improves
the duplex score to 0.371 but still leaves 4 empty outputs. Appendix E details these probes, which are
separate from the reported interaction RL runs.

7.3 Continued Optimization Can Erode Response Continuity
Further optimization can improve yielding while weakening continuation through listener feedback.
In the second stage (Figure 7), interruption reward on natural development conversations rises from 0.450
to 0.793, while continuation after a user backchannel falls from 3.20 to 2.00 seconds and noise-robustness
reward declines from 1.96 to 0.77. These measurements suggest interference between interaction objec-
tives without isolating its mechanism. Group normalization balances scales, but any component that
becomes constant within a rollout group supplies no gradient to resist other reward components.

7.4 Robustness and Behavioral Trade-offs
A training-seed replicate reaches 9% synthetic pause barge-in and 4.22 FDB-v2 turn taking. Applying the
final reward directly from SFT yields 16.8% and 4.13 with less training, so staging is not isolated.



                                                                      10
                                                                                                      Scale AI Research



  a Noise-robustness reward             b Interruption reward                c Response continuity
  Training reward                      Development score                     Seconds after listener feedback

                                         1.0                                     4
              1.96                                               0.793                   3.20
      2
                                                                                                         SFT 2.60 s

                                                 0.450                                                 2.00
                                         0.5                                     2
      1                 0.77


      0                                  0.0                                     0
              Earlier   Later                     Earlier        Later                   Earlier        Later



Figure 7. Higher interruption reward can coexist with weaker response continuity. Recorded snapshots from the
second RL stage. (a) The noise-robustness reward, which includes continuation, declines with further optimization.
(b) The interruption reward on natural development conversations rises, while (c) continuation after a user
backchannel falls below the SFT reference.

Rescoring identical generations from three runs per model gives RL-minus-SFT turn-taking differences
of −0.074 under Gemini 3.6 Flash and −0.059 under gpt-5.4-mini at low reasoning effort (Table 7).
Both judges find a loss in this common pool, which differs from the broader comparison in Table 5.
S TEER B ENCH and AudioMC use one judge.

8 Limitations
Scope and selection. S TEER B ENCH covers controlled English requests with fixed reference clips, rather
than unrestricted personalization across languages, dialects, and recording conditions. Some fine-grained
styles remain below the stronger open baseline. Repeated evaluations average the three highest-scoring
runs from pools of unequal size, potentially inflating scores; FDB-v1.5 uses one decoding pass per
checkpoint. CANDOR overlap further limits the use of official FDB-v1 turn and pause results.
Interaction trade-offs. The reported RL checkpoint yields too readily in some FDB-v2 contexts. The
single-stage comparison has fewer updates than the staged run, so it cannot establish that staging itself
causes the observed advantage. The first-stage FDB-v1.5 row omits an unavailable acoustic check; latency
distributions beyond means are unavailable.
Backbone capacity. SteerDuplex retains Moshi’s 7B model, audio codec, and streaming architecture [8].
These components constrain the reasoning, acoustic representation, and latency available to post-training.
Our results measure improvement within that backbone, rather than the ceiling of steerable speech
models. We have not isolated the effects of the backbone, training data, and reward design.
Judges and deployment. Rubric rewards are imperfect proxies: they depend on the LLM judge’s ability
to recognize the requested characteristics of a correct response. Reference-audio evaluation also depends
on the judge’s comparison with a target clip, which can favor that particular realization of a style even
after human validation. Judge errors can therefore affect both the learning signal and reported scores.
The second-judge study agrees on a turn-taking loss within its common run pool, while the broader
comparison gives a small positive difference; no such study is available for S TEER B ENCH or AudioMC.
Automated safety and audio checks also do not establish deployment safety. Appendix G.1 covers
consent, data handling, and misuse.



                                                            11
                                                                                                                Scale AI Research



9 Conclusion
Our steerability taxonomy organizes content, delivery, and interaction control. S TEER D UPLEX improves
these capabilities, and S TEER B ENCH evaluates requested content and delivery separately. Supervised
fine-tuning supplies the main steerability gains; RL refines interaction behavior. Explicit continuity
rewards reduce the tendency to obtain timing credit through short or absent responses, but do not
eliminate the conflict between yielding and continuing. Premature yielding calls for evaluation of
conversational events alongside aggregate task success.

References
 [1] M. Abdulhai, R. Cheng, D. Clay, T. Althoff, S. Levine, and N. Jaques. Consistently simulating human personas with
     multi-turn reinforcement learning. In Advances in Neural Information Processing Systems, 2025. URL https://arxiv.
     org/abs/2511.00222.
 [2] S. Arora, J. Tian, J. Shi, H. Futami, Y. Kashiwagi, E. Tsunoo, and S. Watanabe. Optimizing conversational quality in
     spoken dialogue systems with reinforcement learning from AI feedback. arXiv preprint arXiv:2601.19063, 2026. URL
     https://arxiv.org/abs/2601.19063.
 [3] T. Chang, J. Wiens, T. Schnabel, and A. Swaminathan. Measuring steerability in large language models. In NeurIPS
     Workshop on Safe Generative AI, 2024. URL https://openreview.net/forum?id=y2J5dAqcJW.
 [4] Y. Chen, Z. Wu, J. Guo, S. Huang, and X. Dai. Extroversion or introversion? Controlling the personality of your large
     language models. arXiv preprint arXiv:2406.04583, 2024. URL https://arxiv.org/abs/2406.04583.
 [5] Y. Chen, X. Yue, C. Zhang, X. Gao, R. T. Tan, and H. Li. VoiceBench: Benchmarking LLM-based voice assistants. arXiv
     preprint arXiv:2410.17196, 2024. URL https://arxiv.org/abs/2410.17196.
 [6] C. Cieri, D. Miller, and K. Walker. The Fisher corpus: A resource for the next generations of speech-to-text. In Proceedings of
     the 4th International Conference on Language Resources and Evaluation (LREC), 2004. URL https://aclanthology.org/
     L04-1500/.
 [7] S. Dathathri, A. Madotto, J. Lan, J. Hung, E. Frank, P. Molino, J. Yosinski, and R. Liu. Plug and play language models:
     A simple approach to controlled text generation. In International Conference on Learning Representations, 2020. URL
     https://arxiv.org/abs/1912.02164.
 [8] A. Défossez, L. Mazaré, M. Orsini, A. Royer, P. Pérez, H. Jégou, E. Grave, and N. Zeghidour. Moshi: A speech-text
     foundation model for real-time dialogue. arXiv preprint arXiv:2410.00037, 2024. URL https://arxiv.org/abs/2410.
     00037.
 [9] S. Ghosh, S. Kumar, A. Seth, C. K. R. Evuru, U. Tyagi, S. Sakshi, O. Nieto, R. Duraiswami, and D. Manocha. GAMA:
     A large audio-language model with advanced audio understanding and complex reasoning abilities. In Proceedings of
     the 2024 Conference on Empirical Methods in Natural Language Processing, pages 6288–6313, Miami, Florida, USA, 2024.
     Association for Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.361. URL https://aclanthology.
     org/2024.emnlp-main.361/.
[10] S. Ghosh, A. Seth, S. Kumar, U. Tyagi, C. K. Evuru, S. Ramaneswaran, S. Sakshi, O. Nieto, R. Duraiswami, and D. Manocha.
     CompA: Addressing the gap in compositional reasoning in audio-language models. In International Conference on Learning
     Representations, 2024. URL https://arxiv.org/abs/2310.08753.
[11] Google. Gemini 3.6 Flash. Google AI for Developers model documentation, 2026. URL https://ai.google.dev/
     gemini-api/docs/models/gemini-3.6-flash. Model ID gemini-3.6-flash; accessed 2026-09-01.
[12] Google DeepMind. Gemini Live API overview. Google AI for Developers documentation, 2025. URL https://ai.
     google.dev/gemini-api/docs/live-api. Accessed 2026-09-09.
[13] A. Gosai, T. Vuong, U. Tyagi, S. Li, W. You, M. Bavare, A. Uçar, Z. Fang, B. Jang, B. Liu, and Y. He. Audio MultiChallenge:
     A multi-turn evaluation of spoken dialogue systems on natural human interaction. arXiv preprint arXiv:2512.14865, 2025.
     URL https://arxiv.org/abs/2512.14865.
[14] C.-Y. Hsiao, K.-H. Lu, Y.-K. Fu, G.-T. Lin, H.-T. Hung, and H.-y. Lee. ASPIRin: Action space projection for interactivity-
     optimized reinforcement learning in full-duplex speech language models. arXiv preprint arXiv:2604.10065, 2026. URL
     https://arxiv.org/abs/2604.10065.
[15] K. Hu, E. Hosseini-Asl, C. Chen, E. Casanova, S. Ghosh, P. Żelasko, Z. Chen, J. Li, J. Balam, and B. Ginsburg. SALM-
     Duplex: Efficient and direct duplex modeling for speech-to-speech language model. In Proc. Interspeech, 2025. URL
     https://arxiv.org/abs/2505.15670.



                                                                12
                                                                                                                  Scale AI Research



[16] Y. Ichihara, Y. Jinnai, T. Morimura, M. Sakamoto, R. Mitsuhashi, and E. Uchibe. MO-GRPO: Mitigating reward hacking
     of group relative policy optimization on multi-objective problems. arXiv preprint arXiv:2509.22047, 2025. URL https:
     //arxiv.org/abs/2509.22047.
[17] N. S. Keskar, B. McCann, L. R. Varshney, C. Xiong, and R. Socher. CTRL: A conditional transformer language model for
     controllable generation. arXiv preprint arXiv:1909.05858, 2019. URL https://arxiv.org/abs/1909.05858.
[18] N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, et al.
     Tülu 3: Pushing frontiers in open language model post-training. arXiv preprint arXiv:2411.15124, 2024. URL https:
     //arxiv.org/abs/2411.15124.
[19] X. Liang, H. Wang, Y. Wang, S. Song, J. Yang, S. Niu, J. Hu, D. Liu, S. Yao, F. Xiong, and Z. Li. Controllable text generation for
     large language models: A survey. arXiv preprint arXiv:2408.12599, 2024. URL https://arxiv.org/abs/2408.12599.
[20] G.-T. Lin, S.-Y. S. Kuan, J. Shi, K.-W. Chang, S. Arora, S. Watanabe, and H.-y. Lee. Full-Duplex-Bench-v2: A multi-turn
     evaluation framework for duplex dialogue systems with an automated examiner. arXiv preprint arXiv:2510.07838, 2025.
     URL https://arxiv.org/abs/2510.07838.
[21] G.-T. Lin, S.-Y. S. Kuan, Q. Wang, J. Lian, T. Li, S. Watanabe, and H.-y. Lee. Full-Duplex-Bench v1.5: Evaluating overlap
     handling for full-duplex speech models. arXiv preprint arXiv:2507.23159, 2025. URL https://arxiv.org/abs/2507.
     23159.
[22] G.-T. Lin, J. Lian, T. Li, Q. Wang, G. Anumanchipalli, A. H. Liu, and H.-y. Lee. Full-Duplex-Bench: A benchmark to
     evaluate full-duplex spoken dialogue models on turn-taking capabilities. In Proc. ASRU, 2025. URL https://arxiv.
     org/abs/2503.04721.
[23] S.-Y. Liu, X. Dong, X. Lu, S. Diao, P. Belcak, M. Liu, M.-H. Chen, H. Yin, Y.-C. F. Wang, K.-T. Cheng, Y. Choi, J. Kautz, and
     P. Molchanov. GDPO: Group reward-decoupled normalization policy optimization for multi-reward RL optimization.
     arXiv preprint arXiv:2601.05242, 2026. URL https://arxiv.org/abs/2601.05242.
[24] P. Manakul, W. H. Gan, M. J. Ryan, A. S. Khan, W. Sirichotedumrong, K. Pipatanakul, W. Held, and D. Yang. AudioJudge:
     Understanding what works in large audio model based speech evaluation. arXiv preprint arXiv:2507.12705, 2025. URL
     https://arxiv.org/abs/2507.12705.
[25] T. A. Nguyen, E. Kharitonov, J. Copet, Y. Adi, W.-N. Hsu, A. Elkahky, P. Tomasello, R. Algayres, B. Sagot, A. Mohamed,
     and E. Dupoux. Generative spoken dialogue language modeling. Transactions of the Association for Computational Linguistics,
     11:250–266, 2023. URL https://aclanthology.org/2023.tacl-1.15/.
[26] A. Ohashi, N. Zeghidour, A. Défossez, and E. Kharitonov. Multi-faceted interactivity alignment in full-duplex speech
     models. arXiv preprint arXiv:2606.11167, 2026. URL https://arxiv.org/abs/2606.11167.
[27] OpenAI. GPT-Realtime model. OpenAI Platform documentation, 2025. URL https://developers.openai.com/
     api/docs/models/gpt-realtime. Accessed 2026-09-09.
[28] M. Rezaei, A. Mahmoud, Z. Wang, U. Tyagi, A. Gosai, R.-G. Dumitru, A. Sabharwal, B. Liu, and Y. He. Rubric-
     guided self-distillation: Post-training without rubric verifiers. arXiv preprint arXiv:2606.12507, 2026. URL https:
     //arxiv.org/abs/2606.12507.
[29] R. Roy, J. Raiman, S.-g. Lee, T.-D. Ene, R. Kirby, S. Kim, J. Kim, and B. Catanzaro. PersonaPlex: Voice and role control for
     full duplex conversational speech models. arXiv preprint arXiv:2602.06053, 2026. URL https://arxiv.org/abs/2602.
     06053.
[30] S. Sakshi, U. Tyagi, S. Kumar, A. Seth, R. Selvakumar, O. Nieto, R. Duraiswami, S. Ghosh, and D. Manocha. MMAU: A
     massive multi-task audio understanding and reasoning benchmark. In International Conference on Learning Representations,
     2025. URL https://arxiv.org/abs/2410.19168.
[31] R. Selvakumar, A. Seth, N. Anand, U. Tyagi, S. Kumar, S. Ghosh, and D. Manocha. MULTIVOX: A benchmark for
     evaluating voice assistants for multimodal interactions. In Proceedings of the 2025 Conference on Empirical Methods in
     Natural Language Processing, pages 28481–28493, Suzhou, China, 2025. Association for Computational Linguistics. doi:
     10.18653/v1/2025.emnlp-main.1447. URL https://aclanthology.org/2025.emnlp-main.1447/.
[32] A. Seth, S. Kumar, R. Selvakumar, N. Anand, U. Tyagi, P. Seetharaman, R. Duraiswami, and D. Manocha. Audio
     hallucination attacks: Probing the reliability of large audio language models. arXiv preprint arXiv:2603.29263, 2026. URL
     https://arxiv.org/abs/2603.29263.
[33] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, and D. Guo. DeepSeekMath:
     Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024. URL
     https://arxiv.org/abs/2402.03300.
[34] X. Shi, X. Wang, Z. Guo, Y. Wang, P. Zhang, X. Zhang, Z. Guo, H. Hao, Y. Xi, B. Yang, J. Xu, J. Zhou, and J. Lin. Qwen3-ASR
     technical report. arXiv preprint arXiv:2601.21337, 2026. URL https://arxiv.org/abs/2601.21337.
[35] U. Tyagi, X. Guo, M. Rezaei, D. George, A. Mahmoud, J. Lee, B. Liu, and Y. He. Not every rubric teaches equally: Policy-
     aware rubric rewards for RLVR. arXiv preprint arXiv:2605.20164, 2026. URL https://arxiv.org/abs/2605.20164.



                                                                 13
                                                                                                           Scale AI Research



[36] B. Veluri, B. N. Peloquin, B. Yu, H. Gong, and S. Gollakota. Beyond turn-based interfaces: Synchronous LLMs as full-
     duplex dialogue agents. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages
     21390–21402, 2024. URL https://aclanthology.org/2024.emnlp-main.1192/.
[37] P. Wang, S. Lu, Y. Tang, S. Yan, W. Xia, and Y. Xiong. A full-duplex speech dialogue scheme based on large language
     models. In Advances in Neural Information Processing Systems, 2024. URL https://arxiv.org/abs/2405.19487.
[38] A. Wu, L. Mazaré, N. Zeghidour, and A. Défossez. Aligning spoken dialogue models from user interactions. In International
     Conference on Machine Learning, 2025. URL https://arxiv.org/abs/2506.21463.
[39] Q. Zhang, L. Cheng, C. Deng, Q. Chen, W. Wang, S. Zheng, J. Liu, H. Yu, C. Tan, Z. Du, and S. Zhang. OmniFlatten: An
     end-to-end GPT model for seamless voice conversation. arXiv preprint arXiv:2410.17799, 2024. URL https://arxiv.
     org/abs/2410.17799.
[40] M. Züfle, O. Klejch, N. Sanders, J. Niehues, A. Birch, and T. K. Lam. F-Actor: Controllable conversational behaviour in
     full-duplex models. arXiv preprint arXiv:2601.11329, 2026. URL https://arxiv.org/abs/2601.11329.



A Training Hyperparameters
Table 3 gives the training settings. The supervised run uses a Moshi-style 7B backbone, 80 H100 GPUs, and 3,600
steps; the reported SFT checkpoint is step 2,925. Both RL stages leave model parameters trainable, with policy
gradients flowing through the text head and shared temporal transformer. Decoded speech and transcripts supply
rewards; audio-codebook actions receive no direct policy loss.

A.1 Reward Weights
Table 4 separates rewards with within-group variation from hard validity checks and held-out evaluation metrics.
In the stage-1 run the transcript rubric judge is active on the turn and interruption strata only, with within-group
standard deviations of 0.14–0.43 and no parse failures in the recorded rollouts.

A.2 Compute Resources
The first RL stage ran on four nodes with eight H100 80 GB GPUs each; the second used one eight-GPU H100
80 GB node. From run initialization to saving the checkpoints used in the paper, the recorded intervals were 5.08
and 4.01 hours, respectively, corresponding to approximately 162.7 and 32.1 allocated GPU-hours. These estimates
include rollout generation, reward computation, optimization, and checkpoint writes within each interval. They
exclude queueing, prior setup, benchmark evaluation, and hosted-model compute. Preliminary runs and training
beyond these checkpoints used additional compute, so this subtotal does not represent the full project.




                                                             14
                                                                                                    Scale AI Research



          Table 3. Training settings. RL stages inherit the preceding policy and freeze a copy as reference.

Setting                                          Value
Base model                               M OSHI [8]
SFT execution                            80 H100 GPUs; batch 8/GPU; global batch 640
SFT budget                               3,600 steps; 2.304M fixed sample draws
Reported model checkpoint                step 2,925 (1.872M draws)
SFT optimizer                            AdamW; lr 2.828×10−6 ; wd 0.1
Depth-former lr                          5.657×10−6
SFT warmup / gradient clip               500 steps / 3.0
Audio/text sampling mass                 0.88/0.12
First-codebook / text-pad weight         100/0.5
Turn / backchannel onset weight          1.5/3.0
Context and response ceiling             300 s
RL learning rate                         5×10−7
RL algorithm                             component-normalized GDPO (weighted sum; final batch
                                         normalization)
RL KL coefficient / target               0.05/0.01 (adaptive, minimum coefficient 0.02; bounded k3
                                         estimator; both stages)
RL clip / gradient clip                  0.2/1.0
RL response-continuity term              weight 0.5, target 4.0 s (both stages)
RL continuation-duration bonus (stage 2) weight 2.0, target 4 s, on noise-robustness and
                                         user-backchannel events
RL reward weights                        interactivity 1.0; transcript rubric judge 0.75 (Gemini 3.6
                                         Flash)
RL event context / max response          30 s / 30 s
RL policy stream                         text stream incl. padding actions
Parameter dtype                          bfloat16 (fp32 master persisted for RL); weight-delta gate
                                         (≥ 5% of elements changed, median ≥ 1 ULP) in both stages
Gradient checkpointing                   on

B Evaluation and Checkpoint Selection
B.1 Judges and Checkpoint Selection
SteerBench and FDB-v2 use Gemini 3.6 Flash. AudioMC, VoiceBench, and FDB-v1 interruption ratings use gpt-5.4-
mini at medium reasoning effort; VoiceBench uses three judge samples per item. FDB-v1/v2 transcription uses
parakeet-tdt-0.6b-v2. Judge identity and scoring conventions are checked before aggregation. The judge-sensitivity
study uses the same generations under both judges; it does not change the reported checkpoint.
The development set is separate from benchmark test sets and targets the same capabilities. We select and freeze
the checkpoint using development performance alone, then report benchmark results.

B.2 Overlap and Pause Measurement
An overlap check found strong transcript n-gram overlap between 100 of 216 CANDOR pause transcripts and 96
supervised conversations. CANDOR turn and pause tasks are therefore diagnostic for the entire training lineage.
Official pause clips also end only 0.02–0.11 seconds after the user’s last word, so they cannot measure successful




                                                         15
                                                                                               Scale AI Research



Table 4. Reward components and evaluation roles in the reported RL run (interactivity-v2 with the response-
continuity term; stage 2 adds the continuation-duration bonus). Component rewards are normalized within rollout
groups; hard validity checks and held-out metrics never substitute for missing reward variation.

Component                                    Weight
Pause timing                         component reward (1.0)
Turn timing + transcript rubric judgecomponent rewards (1.0 timing; 0.75 rubric, pre-boundary
                                     transcript shown)
Backchannel timing                   component reward (1.0)
Response continuity (first response) component term (0.5, target 4.0 s) on turn, interruption, paired
                                     pause, and paired backchannel groups
Continuation duration (stage 2)      component term (2.0, target 4 s) on noise-robustness and
                                     user-backchannel groups
Noise robustness / speech mirror     component rewards (1.0)
Interruption yield + recovery        component rewards (1.0 each)
Waveform integrity                   hard rollout validity
Malformed or incomplete judge result invalid rollout
Safety and broad capability          held-out evaluation
AudioMC / S TEER B ENCH / VoiceBench frozen-checkpoint evaluation

Table 5. Capability comparison. Means ± population standard deviations over three runs per model and
benchmark. The same runs supply every subscore. Higher is better; bold marks the larger displayed mean,
including ties. Differences are computed before rounding. Rates and their differences use percentages and
percentage points; other scores retain their native scales.

                      Metric                                 SFT          + RL        ∆
                      AudioMC APR (%)                 13.64±0.28      14.38±0     +0.74
                      AudioMC ARS (%)                 37.17±1.33   37.97±0.44     +0.80
                      Interruption response (%)           96±0.4     97.7±0.2     +1.67
                      Interruption semantics           3.94±0.03    3.88±0.03    −0.069
                      FDB-v2 mean                      4.17±0.02    4.17±0.03    −0.003
                      FDB-v2 safety                    4.65±0.05    4.81±0.05    +0.153
                      FDB-v2 turn taking               4.18±0.13    4.19±0.07    +0.018
                      FDB-v2 instruction following     3.67±0.13    3.81±0.26    +0.134
                      S TEER B ENCH rubric pass (%)   63.75±1.59   65.22±0.47     +1.47
                      VoiceBench overall              40.87±0.27   41.38±0.02     +0.51

waiting followed by a response. The synthetic pause probe supplies the continuation needed for that measurement.
The source-clean FDB-v1.5 comparison uses 498 examples.


C RL Controls and Robustness
C.1 Complete Retention Results
Table 5 reports three-run means, population standard deviations, and differences for the compact main-text
comparison. It also includes semantic quality, safety, and AudioMC ARS.




                                                      16
                                                                                                   Scale AI Research



Table 6. RL controls. Differences between each model’s three-run mean and the corresponding SFT mean.
Higher is better; bold marks the largest point estimate per column. Data and training-budget differences prevent
interpreting these as single-variable ablations.

                        Variant                   FDB-v2 mean FDB-v2 turn taking VoiceBench
                        Original timing recipe        -0.115          -0.244             +0.049
                        Stage 1                       +0.107          -0.140             +0.444
                        S TEER D UPLEX-RL             -0.003         +0.018              +0.505
                        Training-seed replicate       +0.155         +0.048              +0.227
                        Single-stage                  -0.177          -0.050             -0.363

Table 7. Judge sensitivity. FDB-v2 differences on identical generations from three runs per model; higher is better.
Columns use Gemini 3.6 Flash (canonical) and gpt-5.4-mini (low reasoning). Both judges score the same runs from
the common rescored pool. The broader comparison is in Table 5.

                        Comparison           Metric                             Gemini       GPT
                        Stage 1 minus SFT    headline mean                      +0.057    −0.058
                        Stage 1 minus SFT    per-event turn taking              −0.278    −0.106
                        Stage 1 minus SFT    per-event instruction following    −0.065    −0.009
                        RL minus SFT         headline mean                      −0.083    −0.098
                        RL minus SFT         per-event turn taking              −0.074    −0.059
                        RL minus SFT         per-event instruction following    −0.124    +0.001

Table 8. Second-stage optimization snapshots. Each row compares earlier and later observations on its own scale.
The SFT continuation reference is 2.60 seconds.

                            Measurement                                    Earlier     Later
                            Training noise-robustness reward                    1.96    0.77
                            Development interruption reward                    0.450   0.793
                            Continuation after user backchannel (s)             3.20    2.00

C.2 Training Controls
The original-recipe control starts from SFT with the original interaction recipe and no continuity additions. Stage
1 starts from SFT with continuity weight 0.5 and a 4-second target; its trained checkpoint initializes stage 2.
Stage 2 adds a continuation bonus (weight 2.0, target 4 seconds) and dedicated user-backchannel sampling. The
single-stage variant applies the final reward directly from SFT with a smaller training budget. The training-seed
replicate changes the random seed of the reported configuration. These controls differ in training budget and, for
the original recipe, additional configuration choices, so they do not isolate every reward component.

C.3 Reward and Continuation Snapshots
Table 8 lists the snapshots in Figure 7. Training and development observations were recorded separately within
one run; no intermediate measurements or confidence intervals are available.


D Prompts and Judges
D.1 System Prompts
This section lists the two prompt templates used by S TEER D UPLEX, the constant training system prompt and the
shared inference system prompt, and describes the multi-turn context wrapper that surfaces dialogue history.




                                                               17
                                                                                                                 Scale AI Research



Table 9. Single-family reward probes vs. the joint composite. Endpoint diagnostics on 96 held-out sampled
rollouts per condition. Scalar rewards use different objectives; the common behavioral diagnostics show that every
isolated probe leaves the empty-rollout rate ≥ 26% and the duplex-FDB score at or near zero (≤ 0.055).

                           Probe                       Scalar↑ Empty/96↓ Duplex↑ MOS↑
                           Text-rubric only              0.329          47          0.055      0.512
                           Audio-rubric only             0.336          41          0.000      0.571
                           Audio-quality only            0.522          41          0.000      0.561
                           Promptness only               0.670          25          0.000      0.626
                           Joint composite probe         0.554          4           0.371      0.631

The training-time system prompt below is prepended to the agent-text channel of every RL rollout; per-scenario
steering instructions are inserted on the user side via the dialogue history.

      You are a helpful full-duplex voice assistant. Your voice and identity are fixed. Stay kind, safe, and constructive.
      Follow the user’s spoken instructions about tone, persona flavor, speaking style, speed, and length when those
      instructions are allowed.

For inference and benchmark evaluation, the shared default assistant prompt is:

      You are a helpful voice assistant. Your voice and identity are fixed. Listen carefully, follow the user’s instructions,
      and respond naturally.

For multi-turn RL scenarios with stitched user audio, the system prompt includes a plain “Conversation so far”
transcript. It alternates user and assistant lines, marks assistant-generated text, and ends with the latest user turn.
The model is instructed to respond to that turn using the preceding context.

D.2 Reference-Audio Rubric Judge
The reference-audio rubric judge (§3.3) receives two clips (Audio 1: target style; Audio 2: model output) and
their transcripts, then returns per-criterion JSON scores. The template below is simplified for presentation; the
executable prompt accompanies the evaluation code.

  You are judging audio steerability for a full-duplex voice assistant.
  Audio 1 is the reference target.
  Audio 2 is the model-generated answer.
  Compare delivery / style / prosody / speaking rate / articulation / affect against the
      reference. Do NOT require identical speaker timbre or voice identity unless the
      rubric explicitly asks for it. Use the transcript only to verify content; judge
      audio qualities from the audio.
  Scenario category: <category>
  User request/context: <user_text>
  Reference transcript: <ref_text>
  Generated transcript: <gen_text>
  Audio rubrics:
  <numbered list of rubric items>
  Return ONLY valid JSON with numeric scores in [0,1]:
  {"reason": "<one sentence>", "score": 0.0,
   "style_match": 0.0, "prosody_match": 0.0, "speech_rate_length": 0.0,
   "articulation": 0.0, "naturalness": 0.0, "task_success": 0.0,
   "criteria": [{"title": "...", "category": "...",
                 "rating": "No Issues|Minor Issues|Major Issues",
                 "score": 0.0, "reason": "..."}]}




                                                                 18
                                                                                                       Scale AI Research



D.3 Benchmark Judge
For benchmark-aligned scenarios (daily, correction, safety, entity-tracking, factual, AudioMC), the benchmark judge
is conditioned with the following system prompt and a per-task rubric (one of: daily, correction, entity-tracking,
safety, alpaca, factual, ifeval, default):

  You judge spoken-assistant transcripts. Given the user’s request, any
      scenario-specific rubric, and the assistant’s transcript, FIRST write a
      ONE-SENTENCE explanation of how the assistant performed (referencing concrete
      details from the transcript), THEN give a 1..5 integer score (5 = best). If a list
      of criteria is provided, evaluate each one independently with a one-sentence reason
      and a boolean flag.
  Return ONLY valid JSON with this exact key ORDER (reasoning first, scores last) and no
      other text:
  {"reason": "<ONE sentence, <= 220 chars>",
   "criteria_reasons": ["...", ...], "criteria_met": [<bool>, ...],
   "task_score": <int 1..5>}
  Be calibrated. A typical OK-but-imperfect response is a 3. A 5 requires the response
      to actually accomplish the task as a competent human would. Always reason FIRST,
      score AFTER - never invert the order.


D.4 Text Rubric Judge
The text rubric judge (Section 3.3) scores one criterion at a time as “No Issues,” “Minor Issues,” or “Major Issues,”
explaining its decision before rating. It receives criterion metadata (title, category, type, weight, and description),
the latest user request, and the assistant transcript. Explicit criteria require direct answers; implicit criteria may be
inferred from context. Objective criteria concern factual correctness, while subjective criteria concern quality. The
judge ignores criterion weights and tolerates minor formatting or phrasing differences. For speech, content takes
priority over delivery polish. Output is JSON with reasoning before the rating.

D.5 Agreement with Human Annotations
We assess reference-audio judging by comparing 200 LLM-generated labels with 200 corresponding human
annotations. Agreement, measured as the fraction of matching labels, is approximately 76% with reference
audio and 62% without it. The approximately 14-percentage-point gain supports reference conditioning in this
comparison, while agreement remains imperfect.


E Reward-Integrity Diagnostic
The diagnostic compares four isolated reward families with a joint composite on 96 held-out sampled rollouts per
condition (Table 9). The composite includes semantic, audio, quality, interaction, instruction-following, safety, and
promptness components. These small probes are separate from the reported RL checkpoint. Their endpoint scores
establish failure modes within this study, not a general necessity result for a particular reward combination.


F Baseline Systems
F.1 Configurations
Open models. We use M OSHI’s public moshiko-pytorch-bf16 checkpoint [8] and P ERSONA P LEX’s personaplex-7b-v1
checkpoint through its official inference server [29]. Both are 7B full-duplex speech models.
Proprietary context. The AudioMC comparison reproduces Gemini 2.5 Flash with text output and GPT Realtime
with audio output from Gosai et al. [13]. GPT Realtime (gpt-realtime) is distinct from the older GPT-4o Realtime
model [27]. VoiceBench reports separate hosted-API comparisons; Gemini Live refers to Google’s streaming
API [12]. Imported scores retain their original evaluation protocols.


                                                           19
                                                                                                                 Scale AI Research



Table 10. Exact S TEER B ENCH results underlying Figure 3. Matched items, rubric implementation, and Gemini 3.6
Flash judge. SFT averages three runs; ± denotes population standard deviation. Audio APR requires every audio
rubric to pass; sample APR requires every text and audio rubric to pass. Rubric pass rate averages individual
decisions. All values are percentages; higher is better. Bold marks the best displayed score in each column.
                                                                          S TEER D UPLEX steering profile
      Matched system comparison
                                                         Axis                   Sample APR (%)             Rubric pass (%)
System                    Audio APR (%)
                                                         Tone                                     49.67              71.51
M OSHI [8]                            20.55
                                                         Persona                                  51.11              77.03
P ERSONA P LEX [29]                   16.44
                                                         Style / accent                           48.40              69.83
S TEER D UPLEX (ours)            65.10±1.13
                                                         Speed / length                              32              63.10

Table 11. Source-clean interruption and overlap handling (FDB-v1.5). Success rates (%) on 498 paired examples.
Bold marks the highest success rate in each column. All checkpoints use the frozen behavior scorer and Gemini 3.6
Flash judge. The stage-1 row is behavior-only because its user-backchannel acoustic check was unavailable. Other
checkpoints pass silence, clipping, and duration checks.

                                      Interruption      Background          Talking to              User
                     Checkpoint           response         recovery           another        backchannel
                     Examples                   200               100                100                  98
                     SFT                       72.5                60                 42                71.4
                     RL stage 1                80.5                53                 45                65.3
                     + RL                      82.5                59                 48                80.6

Table 12. Expanded FDB-v2 task comparison. Slow-examiner scores on 200 sessions per pass, judged by Gemini
3.6 Flash (1–5; higher is better). Each model averages three runs; the same runs supply all categories. Bold marks
the higher displayed score (both for ties).

                        System                          Corr.     Daily      Entity    Safety      Mean
                        Three runs per model
                        S TEER D UPLEX (matched ref.)    4.21      3.74       4.07         4.65     4.17
                           + RL                          4.41      3.41       4.04         4.81     4.17

Table 13. Hosted-API AudioMC context. Scores from Gosai et al. [13], in percent; higher is better. Gemini 2.5
Flash uses text output; GPT Realtime uses audio output. Axes follow Table 1. Bold marks the best displayed score.
Different protocols limit comparisons with open models.

                                                   Overall                  Per-Axis APR (%)
                          System
                                              APR (%)    ARS (%)      IM        IR         SC      VE
                          Proprietary
                          Gemini 2.5 Flash     26.11      65.42      19.70     29.17   31.33      26.50
                          GPT Realtime         20.35      63.03      19.70      20     26.51      17.09


F.2 Benchmark Breakdowns
Tables 10 and 11 provide the exact values behind Figures 3 and 4. Tables 12, 13, and 14 supplement Table 1 with
expanded RL comparisons and hosted-API context.


G Data and Responsible Development
The supervised mixture contains 504,416 audio and 65,675 text records, with 8,510.9 hours of audio records and a
fixed 2.304M sample-draw budget. Audio and text have sampling masses 0.88 and 0.12. Targeted subsets include


                                                             20
                                                                                                                 Scale AI Research



Table 14. Additional VoiceBench scores. Gray rows provide hosted-API context. The matched comparison
averages three runs per model, with three judge samples per item. The subscore breakdown includes only the
judged SD-QA score. Bold marks the best displayed subscore within each comparison block, including ties.

      Model                           AlpacaEval CommonEval WildVoice     SD-QA        IFEval      BBH AdvBench Overall
      Proprietary
      Gemini Live                       3.69        3.52          3.26   53.5 / 40.6 17 / 25.9     62.8   94.1       63.01
      GPT-4o Realtime                   4.65        4.33          4.38   88.9 / 75.9 24.3 / 37.3   62.9   98.8       78.42
      Three runs per model
      S TEER D UPLEX (matched ref.)     2.28        2.21          1.74   26.88 / –        –         –     99.3       40.87
         + RL                           2.44        2.28          1.77   28.27 / –        –         –     99.2       41.38


20,000 multi-turn instruction-following records from 5,000 sessions, 25,000 steering records from 5,000 sessions,
1,200 duplex records, and 1,300 six-turn mathematics conversations. Dataset splits are fixed at the record-list level;
duplicate paths are removed and long examples are split at turn boundaries. The duration total counts training
records, not unique source recordings.
Interaction RL data. The proprietary interaction pool covers turns, interruptions, pauses, backchannels, noise,
and speech-mirror scenarios. CANDOR filtering removes identified overlap with evaluation conversations; official
test prompts and labels are excluded from optimization. The second stage emphasizes continued speech after
listener feedback through dedicated user-backchannel sampling.

G.1 Contributor Consent and Data Handling
Contributors received training on task design, rubric writing, audio quality, allowed content, and speaker consent.
They submitted prompts, recordings, transcripts, reference answers, and rubrics for independent review. Screening
rejected audio corruption, transcript mismatches, personal information, inappropriate content outside designated
safety tasks, and missing speaker permission.
Recordings were restricted to contributors’ own voices or explicitly consenting participants. Instructions prohib-
ited bystander speech, identifying personal information, and imitation of private individuals or public figures;
fictional entities were used where needed. Contributors were paid $25–$40 per hour, and were informed of
training, evaluation, and consent-dependent research release uses. The collection protocol obtained the applicable
permissions and ethics approval. Raw audio release follows contributor consent and source terms.

G.2 Demographic and Linguistic Coverage
We evaluate English spoken dialogue only. We collect speaker-gender and native-accent metadata when contrib-
utors voluntarily provide it, and we use those fields for aggregate coverage checks rather than for individual
profiling. AudioMC metadata covers 2,998 user speakers with a 51.3% female, 47.1% male, and 1.6% other gender
split, and includes General American, African (non-South African), British, Canadian, Southern American, North-
eastern U.S., Midwestern U.S., European, Indian, East Asian, Australian, Latin American, Middle Eastern, New
Zealand, and Irish accent labels. We do not claim coverage of non-English languages, code-switching, children,
clinical speech, or all regional dialects.

G.3 Artifact Licenses and Terms
Table 15 summarizes the terms governing training and evaluation artifacts. Restricted corpora and benchmark
assets are not redistributed with the paper.

G.4 Misuse Risks
Steerable dialogue models can enable impersonation, manipulation, or unsafe persuasion. Training excludes
non-consensual voice cloning, and the system prompt specifies a fixed assistant identity. Safety rubrics and refusal
data reduce but do not eliminate misuse risks; deployment still requires identity, consent, abuse-monitoring, and
content-safety controls. Our English-only evaluation does not establish safety across languages or accents.


                                                             21
                                                                                                                    Scale AI Research



Artifact          Role             License / terms            Use in this work
S TEER B ENCH       New benchmark Research license; release   Steerability evaluation; evaluation prompts and labels excluded from
                                  upon acceptance             optimization; audio release follows contributor consent terms.
Synthetic SFT data Training       Author-generated            SFT; release limited to artifacts whose source-data and generated-audio
                                  internal artifact           terms permit redistribution.
In-house            Training      Contributor agreement       Training after quality, PII, and speaker-permission checks; raw recordings
two-person                        and consent terms           not redistributed without explicit permission.
conversations
Proprietary duplex RL training    Project-specific data-use   Gradient-side development examples only; benchmark test material
development data                  permission                  excluded; raw audio not redistributed.
Fisher English [6] Training       LDC User Agreement          Licensed conversational speech; not redistributed.
Audio MultiChal- Evaluation /     Open-source release;        Multi-turn spoken evaluation and coverage analysis.
lenge [13]          analysis      contributor consent terms
Full-Duplex-        Evaluation    Public research release;    Duplex interaction metrics through the official harnesses.
Bench                             no third-party
v1/v2 [20, 22]                    redistribution
VoiceBench [5]      Evaluation    Apache-2.0 dataset/code     Spoken instruction following, reasoning, safety, and QA evaluation.
                                  release
M OSHI [8]          Base model /  CC BY 4.0 model release     Base architecture and open-weight baseline.
                    baseline
P ERSONA P LEX [29] Baseline      NVIDIA Open Model           Open-weight full-duplex baseline.
                                  License; CC BY 4.0
                                  additional information
OpenAI / Google Baselines         Provider API terms          Hosted APIs; no model weights redistributed.
hosted models
gpt-5.4-mini /      Judges        Provider API terms          Hosted APIs; scores only; no model outputs redistributed.
Gemini 3.6
Flash [11]

Table 15. Licenses and use terms for major artifacts. When a third-party artifact has more restrictive redistribution
terms than research use terms, we report results but do not redistribute the underlying asset.

G.5 Writing Assistance
The authors used AI tools for language editing, LaTeX cleanup, and writing assistance. They reviewed and edited
all assisted text and take responsibility for the paper’s research, claims, correctness, originality, and integrity.


H SteerBench Documentation
Contents and intended use. The evaluation set contains 100 tone, 136 persona, 104 style/accent, and 50
speed/length prompts. Items record identifiers, steering categories, subcategories, topics, user utterances, and
audio/text rubrics. Rubrics pair an axis with a binary criterion; item identifiers link user audio, reference audio,
and transcripts. The benchmark measures single-turn English steering under explicit requests; it does not test
long-term personalization or coverage across languages.
Synthetic audio construction. User utterances are rendered as neutral, conversational speech with Gemini 3.1
Flash TTS at 24 kHz, mono, PCM16. A hash of the item identifier chooses a voice from a fixed pool, so the voice
assignment is stable. For synthetic references, a text model converts the user request, steering category, and rubrics
into a transcript and delivery instructions. The saved generation records identify Gemini 3 Pro Preview for the
original scripts and Gemini 3.1 Pro Preview for repairs; synthesis uses Gemini 3.1 Flash TTS with Gemini 2.5 Flash
TTS as a fallback. Reference voices are chosen deterministically from Kore and Schedar. Human review validates
the requested delivery. Fixed reference clips are reused across models; regeneration can change the target.
Scoring and error handling. Text and audio criteria are judged separately, with audio decisions conditioned on
the fixed reference. The scoring implementation excludes items with judge-call errors from pass-rate denominators
and records their count; a run with more than 5% such errors is invalid. Audio APR requires all audio criteria
for an item to pass, sample APR requires all applicable criteria to pass, and rubric pass rate counts individual
decisions. These definitions apply within each reported category as well as to the pooled set.




                                                                22
                                                                                                 Scale AI Research



Access and reuse. Code, S TEER B ENCH, and checkpoints will be released upon acceptance under a research
license. Audio release follows consent and source terms (Appendix G.3).

H.1 Synthetic User-Audio Template
The literal request template is reproduced below; utterance is the item’s user request.
Read the following user utterance naturally, like a real person talking to a voice assistant.

# Audio Profile
A real human user speaking casually to a voice assistant.

# Director’s note
Style: Natural. Pace: Conversational. Accent: American (Gen).

## Scene:
A user speaking into a phone or laptop microphone.

## Transcript:
{utterance}


H.2 Synthetic Reference-Script Template
The generator uses the following system message. The user message supplies the item identifier, category,
subcategory, user utterance, and rubric list, as shown afterward. The request specifies JSON output; the generator
does not set an explicit sampling temperature.
You generate REFERENCE audio scripts for a voice-assistant steerability benchmark.

For each bench sample you receive: a user utterance, the steering sub_axis the
model is supposed to exhibit, and the rubric items the model will be scored on.

You output a short response that an *ideal* steerable assistant would produce
for this turn -- content that engages the user, in the requested style -- plus a
director’s note describing exactly how the line should be spoken.

The script will be sent to a TTS model. Your transcript and director’s note
together MUST produce audio that clearly exhibits the target sub_axis. The
content is secondary -- the audio’s job is to anchor STYLE/TONE/PERSONA/ACCENT/
PACE for a judge model.

Style rules by split:

- A3_tone_controlled: the sub_axis is a TONE (angry, playful, sad, etc.).
  Transcript should be plain, natural prose engaging the user’s topic.
  DO NOT add bracket prefixes. Put the entire tone signal in ‘tts_instruct‘ as
  a vivid director’s note (e.g. "Sharp, irritated, clipped pacing; voice tight
  with frustration; short bitten-off phrases.").

- A4_persona_controlled: the sub_axis is a PERSONA (pirate_captain, doctor,
  noir_detective, etc.). Transcript SHOULD start with the inline tag
  ‘[like a <persona>]‘ (substituting the persona name with spaces, e.g.
  ‘[like a noir detective]‘) and use vocabulary/phrasing matching that persona.
  ‘tts_instruct‘ should describe the persona’s vocal style (cadence, register,
  mannerisms).

- A5_style_accent: the sub_axis is either ‘style=<X>‘ or ‘accent=<X>‘.
  * For style=<X>: bake the style INTO the words (e.g. for pirate_speak,
    write "Arr, matey..."; for poetic, use poetic phrasing; for whispered,
    keep sentences short and intimate). ‘tts_instruct‘ should match the
    style ("hushed, breathy, intimate" for whispered, etc.).
  * For accent=<X>: keep content plain English but ‘tts_instruct‘ must
    explicitly name the accent ("Spoken with a clear British Received
    Pronunciation accent, crisp consonants and rounded vowels.").

- A6_speed_length: the sub_axis is either ‘speed=<X>‘ or ‘length=<X>‘.
  * For speed=<X>: prepend the bracket tag (‘[slow]‘, ‘[fast]‘, ‘[very fast]‘,
    ‘[very slow]‘) to the transcript. ‘tts_instruct‘ should describe the pace
    ("Rapid, breathless rattle of words" / "Measured, unhurried, room to


                                                       23
                                                                                                 Scale AI Research



    breathe").
  * For length=<X>: write the response at the requested length (very_brief
    = 1 short sentence; very_detailed = ~5-6 sentences). No bracket tag.
    ‘tts_instruct‘ can stay neutral ("Natural pace, conversational.").

Length: aim for ~3-6 short sentences (target audio ~15-20s), shorter for
length=very_brief / length=brief, longer for length=detailed / very_detailed.

Return STRICT JSON:
{
  "transcript": "...spoken response, including any required bracket prefix...",
  "tts_instruct": "...natural-language director’s note..."
}
Sample: {sample_id}
Split: {split}
sub_axis: {sub_axis}
sub_axis_group: {sub_axis_group}

User utterance:
{user_utterance}

Rubric items the response must satisfy (these tell you what behaviour the
judge will look for):
{rubrics_block}

Generate the reference script now.


H.3 Synthetic Reference-Audio Template
The returned delivery instructions fill sample_context, and the reference transcript, after removing parenthetical
non-speech cues and normalizing whitespace, fills transcript. The audio request specifies PCM16 output.
Generation metadata retain the transcript, delivery instructions, voice, model identifiers, and sample rate.
Read the following transcript based on the audio profile and director’s note.
# Audio Profile
A helpful and professional personal assistant.
# Director’s note
Style: Empathetic. Pace: Natural. Accent: American (Gen).
## Scene:
A quiet, professional remote workspace.
## Sample Context:
{sample_context}
## Transcript:
{transcript}




                                                       24

