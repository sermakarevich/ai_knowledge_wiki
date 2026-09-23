# Decoupling Conversational Dynamics in Full-Duplex Spoken Models through Reinforcement Learning
Source: https://arxiv.org/abs/2607.07148
Kind: pdf
Fetched: 2026-09-22T09:32:59.952945+00:00
Tool: pdftotext

                                           Decoupling Conversational Dynamics in Full-Duplex
                                            Spoken Models through Reinforcement Learning


                                                  Yuxin Li1         Donghang Wu1 Guan-Ting Lin2 Hung-yi Lee2                 Chengwei Qin3
                                                                              Zhehuai Chen4 Chen Chen4
                                                                1
                                                                 Nanyang Technological University 2 National Taiwan University
                                                            3
                                                                The Hong Kong University of Science and Technology 4 NVIDIA



                                                                                          Abstract

                                                      Recent full-duplex spoken dialogue models have demonstrated compelling progress




arXiv:2607.07148v1 [eess.AS] 8 Jul 2026
                                                      toward human-like interaction, enabling agents to respond with low latency, pro-
                                                      duce backchannels, and handle user barge-ins. Yet these improvements in conver-
                                                      sational dynamics often come with weaker reasoning and instruction-following
                                                      abilities, revealing a potential tension between interactive dynamics and intelligence
                                                      capability. In this paper, we argue that such an intelligence–dynamics trade-off is
                                                      not fundamental: conversational dynamics can instead be learned as a separate real-
                                                      time decision policy from human dialogue data. To this end, we propose DuplexPO,
                                                      a reinforcement learning (RL) framework that decouples when to speak from what
                                                      to say. It preserves the semantic response capability of an instruction-tuned assis-
                                                      tant, while optimizing its temporal interaction behavior over selected high-impact
                                                      windows from long human conversations. To quantitatively optimize these dy-
                                                      namics, we formulate the Factorized Conversational Dynamics Reward (FCDR)
                                                      to enable fine-grained temporal credit assignment for turn initiation, backchannel-
                                                      ing, yielding, and regularized participation. The policy is then optimized with a
                                                      GRPO-style objective. Experiments show that DuplexPO substantially improves
                                                      full-duplex behaviors, including timely backchannels, smooth turn-taking, and
                                                      barge-in handling, while maintaining strong reasoning and instruction-following
                                                      performance. Moreover, improvements in dynamics-oriented metrics are reflected
                                                      in better user experience, suggesting that optimizing conversational timing as a
                                                      standalone objective can promote more natural full-duplex interaction.


                                          1    Introduction
                                          Speech is widely regarded as the most natural modalities for human-computer interaction, making
                                          spoken dialogue systems a long-standing focus in both academia and industry. In recent years,
                                          advances in neural modeling and large-scale data have substantially accelerated progress in this area
                                          [Cui et al., 2024]. In particular, end-to-end spoken dialogue models have emerged as an increasingly
                                          important paradigm for building interactive and helpful voice agents [Nguyen et al., 2023].
                                          More recently, full-duplex spoken dialogue models have gained increasing attention in the research
                                          community due to their ability to support simultaneous listening and speaking [Défossez et al., 2024,
                                          Yu et al., 2025]. By allowing the model to process incoming user speech while generating responses,
                                          this paradigm enables real-time agent behaviors such as handling user barge-ins and producing
                                          timely backchannels. As a result, full-duplex modeling offers a more responsive and human-like
                                          conversational experience compared to traditional turn-based approaches [Wu et al., 2025b].
                                          However, such gains in conversational dynamics may come at the expense of model intelligence: full-
                                          duplex models perform substantially worse on instruction-following and reasoning benchmarks than

                                          Preprint.
their half-duplex counterparts [Hu et al., 2025, Jain et al., 2025], suggesting a potential intelligence–
dynamics trade-off. We analyze this trade-off from two complementary perspectives. First, at the
modeling level, deep logical deduction and fine-grained temporal coordination impose different
demands on autoregressive generation. Strong reasoning often requires long and structured decoding
trajectories that support multi-step inference [Wei et al., 2022, Xie et al., 2025], while natural full-
duplex interaction requires the model to continuously process fragmented, rapidly changing contexts
and make local real-time decisions about whether to speak, pause, or remain silent. Such temporal
control may bias the model toward short-range interaction states, making it harder to preserve the
stable long-range dependencies needed for complex reasoning. Second, at the data level, training
conversational behaviors often relies on human dialogue corpora such as Fisher [Cieri et al., 2004]
during supervised fine-tuning (SFT). Although such data are useful for learning interaction patterns,
they are dominated by casual or non-goal-oriented exchanges and are therefore not necessarily aligned
with the goal of building a helpful, instruction-following assistant.
Based on these analyses, we argue that the above conflict largely stems from coupling “what to say”
and “when to speak” in a single learning objective. These decisions are fundamentally different:
the former concerns semantic content generation and is the primary target of supervised instruction
tuning, while the latter governs temporal behaviors essential to full-duplex interaction, such as
turn-taking, backchanneling, and barge-in handling [Lin et al., 2025a]. This distinction suggests that
full-duplex conversational dynamics need not be relearned by imitating complete natural dialogue
responses, which are dominated by casual, non-goal-oriented exchanges that diverge from assistant-
style interaction. Instead, an instruction-tuned spoken language model can preserve its semantic
competence while selectively adapting its policy at the moments where timing decisions about
turn-taking, backchanneling, and yielding actually matter. This motivates our central hypothesis:
by optimizing only real-time floor-control decisions, a full-duplex spoken language model can
improve conversational dynamics while preserving its instruction-following and reasoning abilities.
This follows the broader principle of targeted speech-specific alignment, where auxiliary speech
capabilities are learned without replacing the model’s general language capability [Chen et al., 2025b].
To operationalize this separation, we propose DuplexPO, an RL framework that treats conversational
dynamics as an independent optimization target for full-duplex spoken dialogue models. Concretely,
DuplexPO samples dynamic-critical windows from long multi-turn human conversations, focusing
optimization on informative full-duplex events such as turn transitions, backchannels, and barge-ins.
Since trajectories are sampled from the model itself, the policy is improved under its own response
distribution rather than forced to imitate heterogeneous conversational corpora. It then computes
a Factorized Conversational Dynamics Reward (FCDR) from the sampled windows and uses it as
the reward signal for RL. Importantly, we show that optimizing these reward maps translates into an
improved user experience: higher dynamics scores lead to interactions that users perceive as more
natural, responsive, and temporally well-coordinated. Finally, the GRPO-style objective regularizes
the updated policy toward the reference SFT model, limiting policy drift and retaining the semantic
behaviors acquired during instruction tuning [Schulman et al., 2017, Ouyang et al., 2022, Shao et al.,
2024].
Empirically, DuplexPO improves turn-taking, backchanneling, and barge-in handling across multiple
conversational-dynamics evaluations, while maintaining comparable performance on factual QA,
instruction following, speech understanding, and reasoning benchmarks. We also provide a demo
page at https://liyuxin44.github.io/DuplexPO/.


2     Related Work

2.1   Full-Duplex Dialogue: Systems vs. Models

Traditional spoken dialogue systems usually decompose real-time interaction into recognition, dia-
logue management, incremental processing, and synthesis modules [Moritz et al., 2020, He et al.,
2019, Schlangen and Skantze, 2011, Chiba and Higashinaka, 2025, Skerry-Ryan et al., 2018]. Full-
duplexity is therefore best understood as a functional property rather than a single architecture. A
system can obtain it through external orchestration, such as VAD or dialogue-management control
[Yamamoto et al., 2025, Shi et al., 2023, Zhang et al., 2025], while a model can internalize it as
part of its own generation process [Yan et al., 2026a, Veluri et al., 2024, Wang et al., 2024a]. In


                                                   2
                                            DuplexPO

                    Backchannel                               Turn Taking & Barge in

                                                                                             Streaming Speech Encoder
 User                                                                           ③
                                                              ②
                                                                                                 Decoder-only LLM
                        ①
 Agent                                          ...                                               (Policy Model)

 Text                                           ...                                                Text Projector
                      <bos> T1 T <eos>                        <bos>T1 T2 T3 T4 <PAD> <eos>
Channel                         2

                                                                                                Dynamics-critical Window
                                         Reward Calculation
                                                                                                Prediction Waveform
                                  R1            ...                             Rn
                                                                                                Backpropagation
                                            Optimization
                                                                                                Streaming Speech Synthesis


Figure 1: Overview of the DuplexPO for full-duplex spoken dialogue models. The red shadows
indicate dynamics-critical windows that may include important conversational behaviors, such as: ⃝
                                                                                                 1
backchanneling, ⃝ 2 turn-taking, and 3⃝ user barge-in. For each window, the policy model generates
multiple rollouts for reward calculation and is optimized with RL.


system-level designs, auxiliary control can determine when to speak while the core model focuses on
response generation.
Model-level full duplex follows a different formulation. Models such as Moshi, SALMONN-omni,
SALM-Duplex, and related latent-reasoning variants expose turn-taking, backchanneling, and barge-
in behavior directly to the model [Défossez et al., 2024, Yu et al., 2025, Hu et al., 2025, Wu et al.,
2026]. Recent full-duplex benchmarks similarly treat these behaviors as explicit model capabilities
rather than peripheral interface features [Lin et al., 2025a, 2026b,a]. This paper therefore focuses
on model-level full-duplex dialogue, where the key challenge is not only generating an appropriate
answer, but learning a temporally coordinated policy for deciding when that answer should enter,
pause, or leave the shared speech stream.



2.2      Reinforcement Learning for Dialogue Agents


RL is well suited to dialogue policy optimization, where actions often have delayed effects beyond
next-token likelihood [Sutton and Barto, 2018]. Prior work has applied RL to task-oriented dialogue,
turn-taking, conversational reasoning, retrieval-augmented QA, and AI-feedback-based response
optimization [Raux and Eskenazi, 2012, Khouzaimi et al., 2016, Acikgoz et al., 2026, Lupart et al.,
2025, Arora et al., 2026, Rakib et al., 2026]. This direction has also begun to reach end-to-end
spoken language models. Align-SLM uses AI-feedback preference optimization to improve semantic
coherence in textless SLMs, while user-interaction alignment constructs large-scale preference pairs
from raw multi-turn speech conversations for full-duplex speech-to-speech models [Lin et al., 2025b,
Wu et al., 2025a]. These studies show that reward-based learning is useful when the desired behavior
is sequential, context-dependent, or only weakly specified by supervised targets.
Full-duplex dynamics pushes this view into a more local temporal regime. Yielding after user barge-
in, producing a brief backchannel, or delaying a turn start are decisions whose quality depends on
a narrow acoustic and conversational context, yet whole-dialogue objectives can blur their credit
assignment [Zhao et al., 2025]. Recent spoken-dialogue RL and reward-modeling work has begun
to explicitly optimize interaction behaviors such as turn-taking and backchanneling by learning
dialogue-level policies or reward models over entire conversations [Chen et al., 2025a, 2026]. In
contrast, our approach focuses on fine-grained temporal credit assignment, restricting policy updates
to short, interaction-critical windows rather than optimizing over full dialogues. ASPIRin shows that
raw-token RL for full-duplex timing can degrade semantic quality, and addresses this by projecting
the action space into active-speech versus inactive-silence states before GRPO-style optimization
[Hsiao et al., 2026]. DuplexPO instead keeps the original action space and changes the optimization
unit, updating only dynamic-critical windows rather than the full dialogue.


                                                                  3
3     Methodology
3.1   Overview

We propose DuplexPO, a policy optimization method that decouples when and how to engage in
conversation (turn-taking, backchanneling, yielding to user barge-ins) from what to say (semantic
content). DuplexPO improves full-duplex behavior while preserving the model’s instruction-following
and reasoning capabilities. As shown in Figure 1, the framework consists of three main components.
First, Dynamic-critical Window Sampling selects local windows around annotated agent speaking
events and restricts policy optimization to these regions. Second, the Factorized Conversational
Dynamics Reward (FCDR). Third, group-based policy optimization. Appendix D provides a token-
level example showing how DuplexPO reshapes boundary-control decisions.

3.2   Problem Formulation

We formulate full-duplex conversational dynamics learning as frame-level policy optimization over
streamed dialogue. Let x1:T denote the user audio stream and y1:T denote the agent’s real-time
interaction decisions on a uniform temporal grid with frame duration ∆. At each frame, the policy
predicts
                                        πθ (yt | y<t , x≤t ),                                      (1)
where x≤t is the causal user context and yt represents the agent’s interaction state, such as silence,
speaking, turn initiation, or yielding.
Instead of optimizing over entire conversations, DuplexPO operates on a set of local dynamics-critical
windows W = {Wi }M    i=1 extracted from long human conversations. Each window contains a short
temporal region around an interaction-critical event, together with its reference speaking interval
and event metadata, as defined in subsection 3.3. For a window Wi with temporal support [si , ei ),
the policy samples actions only inside the window while conditioning on the teacher-forced history
before si . The sampled sub-trajectory is evaluated by a window-level reward:
                                         Ri = R(Wi , y[si ,ei ) ),                                     (2)
where y[si ,ei ) denotes the agent’s sampled decisions within the window.

3.3   Dynamics-Critical Window Sampling

Prior study suggests that conversational turn transfer is often determined by local timing and prosodic
cues near possible response points, rather than by evidence uniformly distributed across the entire
dialogue [Ward and Tsukahara, 2000, Sacks et al., 1974]. Therefore, DuplexPO does not optimize
the policy over full conversations. Instead, it selects short but important local windows, such as turn
transitions, backchannels, and user barge-ins, where real-time speaking decisions are most critical.
Let (ai , bi ) denote the start and end times of the i-th annotated human agent segment, and let ci denote
its event metadata, including whether the segment is a backchannel and whether the corresponding
window contains user barge-in. Each window is defined as
                                        Wi = (si , ei , gi , hi , ci ),                                (3)
where [gi , hi ) is the discretized reference speaking interval and [si , ei ) is the sampled window. The
reference interval is
                                     gi = ⌊ai /∆⌋ ,     hi = ⌊bi /∆⌋ .                                 (4)
The sampled window includes a lead time L before the annotated segment and a buffer time B after
it:
                    si = max(ei−1 , ⌊(ai − L)/∆⌋) ,       ēi = ⌊(bi + B)/∆⌋ .                 (5)
For the first window, the previous boundary term is omitted. We further apply boundary clipping to
avoid overlap between neighboring events:
                                 ei = min(ēi , ⌊(ai+1 − L)/∆⌋ , T ) ,                                 (6)
where the next-segment boundary is omitted for the final segment.
Within each window, the history before si is teacher-forced, and the policy is optimized only on
sampled actions in [si , ei ).


                                                      4
3.4   Factorized Conversational Dynamics Reward (FCDR)

Although ORISE [Chen et al., 2025a] shows that rollout-level rewards can improve spoken interaction,
its sequence-level assignment provides coarse supervision, making it difficult to attribute success or
failure to specific real-time decisions. We therefore introduce a temporally shaped reward that assigns
fine-grained supervision at the event level. The proposed reward design is motivated by findings from
human turn-taking and backchannel behavior in conversational interaction [Sacks et al., 1974, Stivers
et al., 2009, Levinson and Torreira, 2015].
For a sampled continuation in window Wi , let Ŝi ⊆ [si , ei ] denote the frames where the agent speaks.
If Ŝi ̸= ∅, the predicted onset is ĝi = min Ŝi , and the onset delay is
                                                τi = ∆(ĝi − gi ),                                                  (7)
where τi < 0 means the agent starts too early and τi > 0 means it starts late. We derive three binary
masks from the event metadata ci : mion , mibc , and mioff , indicating whether onset timing, backchannel
timing, and barge-in yielding are active for the current window.
The final FCDR is a weighted sum of factorized event-level components:
               RFCD (Wi , Ŝi ) = λon mion Ron
                                            i
                                               + λbc mibc Rbc
                                                           i
                                                              + λoff mioff Roff
                                                                            i           i
                                                                                + λreg Rreg .                       (8)

The component definitions are summarized in Table 1. This factorized design assigns credit to local
timing decisions while keeping the reward interpretable across different conversational-dynamics
events. Figure 6 in Appendix provides an empirical analysis of the reward components. We also
compare FCDR with neural reward model alternatives in Appendix I, including designs based on
temporal state prediction and window-level dynamics scoring.

Table 1: FCDR components. Each component is computed within a dynamics-critical window
Wi . Event-specific masks determine which components are active. Here Bi = [gi , hi ] denotes the
annotated backchannel interval, d(t, Bi ) denotes the frame distance from t to Bi , ℓi denotes the
duration of agent speech after user barge-in, and ei,k denotes predefined undesirable interactions.

        Component         Target behavior                           Functional form                      Range
                                                                                  τi2
                                                                                          
         i
        Ron               Turn initiation                  I[Ŝi ̸= ∅] exp −                             [0, 1]
                                                                              2σon (τi ) 2
         i                                                                         / Bi ]e−αd(t,Bi )
                                                                                                     
        Rbc              Backchanneling         I[Ŝi ̸= ∅] max I[t ∈ Bi ] + I[t ∈                       [0, 1]
                                                          t∈Ŝi
                                                                              − ℓ∗ )
                                                                                         
         i                                                       max(0, ℓi
        Roff          Yielding after barge-in            −clip                    , 0, 1                 [−1, 0]
                                                                     Hoff
                                                                P                      
         i                                                        K
        Rreg           Pattern regularization             −clip   k=1 βk I[ei,k ], 0, 1                  [−1, 0]



3.5   Group-based Optimization

DuplexPO uses a GRPO-style objective [Shao et al., 2024] to optimize sampled continuations within
each dynamics-critical window. GRPO uses group-normalized advantages over the full set of sampled
continuations, providing a denser and more stable optimization signal for dynamics-critical decisions
than DPO-style preference optimization.
For window i, we normalize rewards across its sampled continuations to obtain a clipped group
advantage:                                                    
                                              ri,k − µi
                                 Ai,k = clip            , −5, 5 ,                           (9)
                                               σi + ϵ
where ri,k is the reward of the k-th continuation, and µi , σi are the reward mean and standard
deviation within the same window group. We then apply a policy-gradient loss only to sampled
tokens inside the window, with a KL penalty toward the rollout behavior policy:
                                            LGRPO = Lpolicy + βLKL .                                               (10)

We also implement a DPO-style baseline by constructing pairwise preferences among continuations
from the same window, and report the ablation in Appendix J.


                                                          5
4     Data and Model Training
4.1   Conversational Dynamics-Aware Dialogue Data Generation

Fisher [Cieri et al., 2004] and Seamless-Naturalistic-HQ (Seamless) [Agrawal et al., 2025] provide
natural two-party conversations with word-level timing, making them suitable sources for learning
conversational dynamics. The two corpora cover complementary interaction regimes: Fisher is
closer to symmetric peer-to-peer conversation, whereas Seamless contains more role-asymmetric,
question-answer-oriented interactions. This combination enables us to test whether DuplexPO can
handle both balanced conversational exchange and assistant-like spoken interaction. All Fisher and
Seamless evaluations use held-out conversations that are split before reconstruction and window
annotation; the training conversations, derived windows, and timing annotations are disjoint from the
evaluation conversations and evaluation annotations. Reconstruction, filtering, and sampling details
for data preprocessing are given in Appendix A.

4.2   Training Pipeline

The training pipeline consists of four stages: pre-training, SFT, RL with DuplexPO, and speech-
synthesis SFT. The pre-training and SFT stages follow the setup of Nemotron-VoiceChat [NVIDIA,
2026] and we provide more training and data details in Appendix A. Then, DuplexPO is applied to
optimize conversational dynamics with explicit rewards over dynamics-critical windows. Finally, in
speech-synthesis SFT, we freeze all parameters except the speech generation module and train the
streaming TTS model on the same speech dataset [Du et al., 2024]. The implementation, optimization,
and stage-wise hyperparameters are in Appendix B.

5     Evaluation and Benchmark
We evaluate Spoken Dialogue Language Models (SDLMs) from two complementary aspects, namely
conversational dynamics and model intelligence. The former assesses full-duplex conversational
dynamics, such as turn-taking and backchanneling. The latter examines general capabilities, including
factual knowledge, instruction following, speech understanding, and reasoning.

5.1   Conversational Dynamics Evaluation

Conversational dynamics are evaluated on Fisher [Cieri et al., 2004], Seamless [Agrawal et al., 2025],
and Full-Duplex-Bench v3 (FDB-v3) [Lin et al., 2026a]. For each conversation, we evaluate all non-
overlapping windows spanning the full dialogue. On Fisher and Seamless, we report window-level
initiation rate, onset MAE, and yield rate for both full-turn and backchannel events, measuring <BOS>
occurrence, <BOS> timing error, and timely <EOS> emission, respectively. Here, <BOS> and <EOS>
denote the beginning and end of the agent’s speaking turn, respectively. Onset MAE is computed only
for initiated events. FDB-v3 tests robustness to premature agent speech during disfluent user turns
and user re-entry. We report Turn-taking Latency, Voiced Interrupt Rate (VIR), and Yield Rate. VIR
measures the percentage of agent speech onsets that overlap with voiced user speech. We exclude
onsets during internal user pauses and within the final 0.5s of a voiced user segment, where overlap
may reflect turn-transition ambiguity rather than interruption. Yield Rate measures whether the agent
releases the floor before the user resumes speaking.
Following prior pairwise preference evaluation protocols for open-ended dialogue models [Zheng
and et al., 2023, Chiang et al., 2024], we conduct a blinded matched-window LLM-as-a-Judge
evaluation with Gemini 3.0 Pro1 to compare DuplexPO with the SFT Baseline at the conversation
level. For each aligned dialogue, the judge is given the shared user timeline and two anonymized
candidate model timelines. To fit the judge’s context budget and control evaluation cost, we sample a
subset of windows per dialogue, using the same window indices for both models to ensure matched
conversational contexts. We concatenate each model’s responses over these windows into a single
conversation-level judge input. The judge selects the candidate with more natural conversational
dynamics and reports dimension-level preferences for turn-taking, backchanneling, and user barge-in
handling. The full prompts, and per-dimension results are provided in Appendix F.
    1 https://gemini.google.com/




                                                  6
Table 2: Window-level turn-taking and backchannel performance on Fisher and Seamless. Rates
(except Onset MAE) are reported in %. Best values in each column are bolded.
                                                                                    Turn-taking                       Backchannel
 Method                             Dataset          Onset MAE (↓)
                                                                           Init Rate (↑) Yield Rate (↑)      Init Rate (↑) Yield Rate (↑)
 Moshi [Défossez et al., 2024]                            1.99                87.7             76.5                83.9              66.7
 PersonaPlex [Roy et al., 2026]                           1.50                 98.6            80.3                91.4               69.2
 SFT Baseline                        Fisher               0.98                 97.8            92.1                95.7               57.1
 SFT Dynamics                                             1.14                 97.1            78.9                91.4               57.1
 DuplexPO                                                 0.69                100.0            98.7                97.8              100.0
 Moshi [Défossez et al., 2024]                            2.16                80.1             69.0                76.2              71.3
 PersonaPlex [Roy et al., 2026]                           1.77                82.8             79.6                82.3              84.0
 SFT Baseline                       Seamless              1.22                91.8             78.5                92.2              79.4
 SFT Dynamics                                             1.34                79.7             63.0                83.2              63.4
 DuplexPO                                                 1.03                98.0             93.6                99.5              93.3


Table 3: Turn-Taking Dynamics, VIR, and Yield Rate on FDB-v3. Rates are reported in %, and
Latency is reported in seconds. The results of GPT-Realtime, Gemini Live 2.5, Gemini Live 3.1,
Grok and Ultravox are taken from [Lin et al., 2026a]. Best values in each column are bolded.
                                                                   Turn-Taking Dynamics
                    Method                                                                          VIR (↓) Yield (↑)
                                                                 Turn-Take (↑) Latency (↓)
                    GPT-Realtime [OpenAI]                           96.0              2.65            –             –
                    Gemini Live 2.5 [Google, 2025]                  92.0              3.84            –             –
                    Gemini Live 3.1 [Google]                        78.0              1.59            –             –
                    Grok [x.ai]                                     94.0              3.13            –             –
                    Ultravox [fixie-ai]                              96.0             1.90            –             –
                    Moshi [Défossez et al., 2024]                   100.0             0.44           12.0          71.9
                    PersonaPlex [Roy et al., 2026]                   98.0             1.41           15.0          66.7
                    SFT Baseline                                     99.0              7.33            8.0         64.8
                    SFT Dynamics                                    100.0             14.24            4.0         93.3
                    DuplexPO                                        100.0              0.24            5.0        100.0



5.2   Model Intelligence Evaluation

To verify that conversational dynamics optimization preserves task-level capability, we evalu-
ate SDLMs on factual knowledge, instruction following, speech understanding, and reasoning
benchmarks. Factual knowledge is measured by accuracy on four quick QA sets: Llama Ques-
tions [Nachmani et al., 2023], WebQuestions [Berant et al., 2013], TriviaQA [Joshi et al., 2017], and
SDQA [Faisal et al., 2021]. Instruction following is evaluated with AlpacaEval and CommonEval
from VoiceBench [Chen et al., 2024]; the latter uses real human speech and better reflects spoken
instruction-following scenarios. Following the official VoiceBench protocol, open-ended responses
are scored by a GPT judge on a 1–5 scale. Speech understanding and reasoning are measured by
multiple-choice accuracy on OpenBookQA and MMSU [Wang et al., 2025]. For all benchmarks,
generated speech is transcribed with Whisper large v3 [Radford et al., 2022] before computing
text-based metrics under the official VoiceBench protocol.

                         A Win     B Win       Tie                                             A Win     B Win     Tie

                                           2                2                  2              10
                                                                                                             68                76


           20            20                                                   264             250
                                           22               21                                               261              237


                                                                              117             123
           6             6                                                                                                     70
                                           2                3                                                54

          Total      Turn-taking    Backchannel        User Barge-in          Total      Turn-taking     Backchannel      User Barge-in
                                                         handling                                                           handling
       (a) Pairwise Judge Evaluation on Fisher test set (n=26)         (b) Pairwise Judge Evaluation on Seamless test set (n=383)


Figure 2: Conversation-level Gemini pairwise evaluation comparing the SFT Baseline (A) with
DuplexPO (B). The judge observes timestamps, transcripts, and aggregate dynamics statistics to
assess turn-taking, backchanneling, and barge-in handling.



                                                                       7
Table 4: Model intelligence evaluation. QA, OpenBookQA, and MMSU metrics are accuracy in %;
AlpacaEval and CommonEval are GPT-scores on a 1–5 scale. Baseline results are taken from [Yu
et al., 2025, Chen et al., 2024]. FD denotes full duplex. LlamaQ, WebQ, TriQA, OBQA, AlpacaE,
and ComE denote Llama Questions, WebQuestions, TriviaQA, OpenBookQA, AlpacaEval, and
CommonEval.
    Method                             FD   LlamaQ   WebQ   TriQA   SDQA   AlpacaE   ComE   OBQA   MMSU
    Moshi [Défossez et al., 2024]      ✓     54.5    22.1   16.7    15.6    2.01     1.60   25.9   24.0
    Freeze-Omni [Wang et al., 2024b]   ✓     56.2    27.9   28.5    53.5    4.03     3.46   31.0   28.1
    SALMONN-omni [Yu et al., 2025]     ✓     73.6    43.7   56.0     -      3.22       -     -     30.0
    SALM-Duplex [Hu et al., 2025]      ✓     51.3    25.0   16.9    26.0    2.99     2.50   39.6   26.3
    GLM-4-Voice [Zeng et al., 2024]    ✗     65.7    37.0   47.5    37.0    3.97     3.42   53.4   39.8
    Qwen2-Audio [Chu et al., 2024]     ✗     69.7    45.2   40.3    35.7    3.74     3.43   49.5   35.7
    Kimi-Audio [Ding et al., 2025]     ✗     68.3    37.3   51.2    63.1    4.46     3.97   83.5   62.2
    Baichuan-Audio [Li et al., 2025]   ✗     74.0    40.7   53.0    45.8    4.41     4.08   71.7   53.2
    STITCH-R [Chiang et al., 2025]     ✗     70.0    50.3   49.6     -      2.70       -     -      -
    SFT Baseline                       ✓     72.0    44.3   48.1    47.2    3.43     3.48   72.2   54.9
    DuplexPO                           ✓     75.3    44.5   49.9    49.8    3.68     3.74   73.7   56.2



6      Results and Analysis
6.1     Conversational Dynamics

We compare DuplexPO with two SFT-only baselines. SFT Baseline is trained without dynamics-
aware dialogue data, whereas SFT Dynamics uses the same SFT recipe as DuplexPO and includes the
reconstructed dynamics-aware dialogue data.
Table 2 shows that DuplexPO consistently improves window-level turn-taking and backchannel
behavior on both Fisher and Seamless. SFT Dynamics shows that SFT alone is insufficient for
learning robust conversational coordination from natural dynamics patterns, regressing across all
dynamics metrics relative to the SFT Baseline. DuplexPO achieves the best overall performance,
with the highest initiation and yield rates for both turn-taking and backchannels, as well as the lowest
onset MAE on both datasets.
Table 3 examines whether these window-level gains transfer to ambiguous mid-turn regions where
premature responses cause barge-ins. The results reveal a latency-interruption trade-off among
existing models. Commercial models and Ultravox achieve reasonable turn-taking accuracy but
incur high latency, reflecting conservative endpointing strategies that wait for extended silence.
In contrast, open-source duplex models such as Moshi and PersonaPlex reduce latency through
always-on listening, but suffer from substantially higher VIR due to premature interruptions. Among
our ablations, SFT Dynamics attains low VIR and high Yield Rate only by adopting long latencies,
effectively trading responsiveness for caution.
DuplexPO breaks this trade-off. It preserves perfect turn-taking, achieves the highest Yield Rate
and the lowest latency among all models, and keeps VIR competitively low. These results suggest
that dynamics-aware RL learns coordinated floor control rather than simply biasing the agent toward
eagerness or caution. By using mid-turn dynamics evidence to distinguish true completion from
disfluent continuation, DuplexPO can respond promptly when the user yields while reliably yielding
when the user retains the floor. The reward curve and pairwise correlations among sub-reward
components are visualized in Appendix G.
Figure 2 evaluates whether these metric gains are reflected at the conversation level. The pairwise
judge prefers DuplexPO in 76.9% of Fisher comparisons and 69.3% of non-tie Seamless comparisons.
Dimension-level preferences are consistent with the automatic metrics for turn-taking, backchanneling,
and user barge-in handling.

6.2     Model Intelligence

Table 4 addresses the second side of the proposed intelligence–dynamics trade-off. Across factual QA,
instruction following, speech understanding, and reasoning, DuplexPO preserves the SFT Baseline’s
task-level capability and yields small but consistent improvements. Although the magnitude of these
gains is modest, their direction is important because optimizing the real-time speaking policy does
not degrade the semantic and reasoning abilities learned during SFT.


                                                        8
6.3                 Discussion and Visualization

We analyze how DuplexPO reshapes conversational behavior using two metrics defined in Appendix C:
Suppressed Intent Rate (SIR), measuring how often latent boundary intent is suppressed, and Sup-
pression Release Ratio (SRR), measuring whether suppressed intent is later released. Figure 3(b)
shows that DuplexPO releases suppressed <BOS> impulses more selectively than the SFT model,
while Figure 3(a) shows consistent <EOS> urge trajectories around user barge-ins. A token-level
qualitative comparison with the SFT Baseline is provided in Appendix K. Overall, DuplexPO does
not globally suppress speaking intent, but instead shifts behavior near boundary-control decisions,
releasing latent <BOS> and <EOS> impulses according to the local conversational state. Consistent
with this, Appendix D shows that DuplexPO attends less to the <BOS> sink and more to real-text,
recent-context, and PAD-state positions than Moshi 7B.
We further ablate three DuplexPO design choices. First, longer lead times sharply reduce mean RL
reward, whereas buffer time has a milder effect, showing that supervision must stay close to boundary
events (Appendix H; Figure 7). Second, replacing FCDR with a neural reward model based on a
learned temporal state predictor yields partial gains over SFT Dynamics but remains less reliable than
FCDR, likely because coarse teacher-derived states can disturb fine-grained SFT behaviors. This
suggests that explicit FCDR shaping provides a more direct signal for dynamics-critical decisions
(Appendix I). Third, replacing GRPO with a DPO objective based on the highest- and lowest-reward
continuations yields weaker performance on most dynamics metrics, particularly yield-oriented
metrics, suggesting that group-normalized advantages better exploit the full reward distribution rather
than only the extremes (Appendix J). Additional discussion is provided in Appendix ??.

                                                                          SFT Baseline
                                                                          DuplexPO                        <BOS> Impulses      <EOS> Impulses
                                                                                               Dataset
                                                                                                          SIR       SRR       SIR      SRR
                                                                                               Fisher     11.0      70.6      4.9     100.0
Mean 𝑝 𝐸𝑂𝑆 𝑡)
                                                                                               FDB-v3     10.8      71.9      0.9     100.0
                                                                                             (b) Suppressed-intent analysis results for <BOS> and
                                                                                                  <EOS> impulses. Values are reported in %.

                                   Time Relative to Interrupt Onset (s)

                (a) <EOS> impulse around user interruption onset.
Figure 3: Analysis of suppressed boundary intent in SFT Baseline and DuplexPO. (a) <EOS> impulse
around user interruption onset on Fisher test set (n=148 events from 20 conversations). Both policies
are evaluated on the SFT trajectory; shaded regions show 95% CI. (b) Suppressed-intent analysis.

Limitations DuplexPO’s factorized rewards enable interpretable event-level credit assignment,
but may miss subtle pragmatic factors such as user intent, discourse content, speaker style, and
culture-specific timing preferences. Human timing annotations are also not unique ground truth, since
turn initiation, backchanneling, and yielding can vary across speakers, languages, and conversational
settings. As policy updates are restricted to local dynamics-critical windows, DuplexPO may also miss
long-range dialogue effects. Future work could combine multilingual and user-adaptive evaluation,
and longer-horizon objectives for dialogue coherence.

7                  Conclusion
We identified the trade-off between conversational dynamics and model intelligence in full-duplex
spoken language models. We argue that this trade-off largely stems from coupling what to say with
when to speak, rather than from an inherent conflict between the two. We propose DuplexPO, an RL
framework that preserves instruction-tuned semantic capability while optimizing real-time speaking
decisions over dynamics-critical windows. Experiments show that DuplexPO improves turn-taking,
backchanneling, and barge-in handling without degrading instruction following, factual QA, speech
understanding, or reasoning.




                                                                                         9
References
Emre Can Acikgoz, Jinoh Oh, Jie Hao, Joo Hyuk Jeon, Heng Ji, Dilek Hakkani-Tur, Gokhan Tur,
 Xiang Li, Chengyuan Ma, and Xing Fan. Speakrl: Synergizing reasoning, speaking, and acting in
 language models with reinforcement learning. In Proceedings of the 16th International Workshop
 on Spoken Dialogue System Technology, pages 312–325, 2026.
Vasu Agrawal, Akinniyi Akinyemi, Kathryn Alvero, Morteza Behrooz, Julia Buffalini, Fabio Maria
  Carlucci, Joy Chen, Junming Chen, Zhang Chen, Shiyang Cheng, et al. Seamless interaction:
  Dyadic audiovisual motion modeling and large-scale dataset. arXiv preprint arXiv:2506.22554,
  2025.
Siddhant Arora, Jinchuan Tian, Jiatong Shi, Hayato Futami, Yosuke Kashiwagi, Emiru Tsunoo, and
  Shinji Watanabe. Optimizing conversational quality in spoken dialogue systems with reinforcement
  learning from ai feedback. arXiv preprint arXiv:2601.19063, 2026.
Evelina Bakhturina, Vitaly Lavrukhin, Boris Ginsburg, and Yang Zhang. Hi-fi multi-speaker english
  tts dataset. arXiv preprint arXiv:2104.01497, 2021.
Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. Semantic parsing on freebase from
  question-answer pairs. In Proceedings of the 2013 conference on empirical methods in natural
  language processing, pages 1533–1544, 2013.
Chen Chen, Ke Hu, Chao-Han Huck Yang, Ankita Pasad, Edresson Casanova, Weiqing Wang,
  Szu-Wei Fu, Jason Li, Zhehuai Chen, Jagadeesh Balam, et al. Reinforcement learning enhanced
  full-duplex spoken dialogue language models for conversational interactions. In Second Conference
  on Language Modeling, 2025a.
Chen Chen, Yuchen Hu, Siyin Wang, Helin Wang, Zhehuai Chen, Chao Zhang, Chao-Han Huck Yang,
  and Eng Siong Chng. Audio large language models can be descriptive speech quality evaluators.
  arXiv preprint arXiv:2501.17202, 2025b.
Yifu Chen, Shengpeng Ji, Zhengqing Liu, Qian Chen, Wen Wang, Ziqing Wang, Yangzhuo Li,
  Tianle Liang, and Zhou Zhao. Dual-axis generative reward model toward semantic and turn-taking
  robustness in interactive spoken dialogue models. arXiv preprint arXiv:2604.14920, 2026.
Yiming Chen, Xianghu Yue, Chen Zhang, Xiaoxue Gao, Robby T Tan, and Haizhou Li. Voicebench:
  Benchmarking llm-based voice assistants. arXiv preprint arXiv:2410.17196, 2024.
Cheng-Han Chiang, Xiaofei Wang, Linjie Li, Chung-Ching Lin, Kevin Lin, Shujie Liu, Zhendong
  Wang, Zhengyuan Yang, Hung-yi Lee, and Lijuan Wang. Stitch: Simultaneous thinking and talking
  with chunked reasoning for spoken language models. arXiv preprint arXiv:2507.15375, 2025.
Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle Li, Dacheng
 Li, Hao Zhang, Banghua Zhu, Michael Jordan, Joseph E Gonzalez, et al. Chatbot arena: An open
 platform for evaluating llms by human preference. arXiv preprint arXiv:2403.04132, 2024.
Yuya Chiba and Ryuichiro Higashinaka. Investigating the impact of incremental processing and
  voice activity projection on spoken dialogue systems. In Proceedings of the 31st International
  Conference on Computational Linguistics, pages 3687–3696, 2025.
Yunfei Chu, Jin Xu, Qian Yang, Haojie Wei, Xipin Wei, Zhifang Guo, Yichong Leng, Yuanjun Lv,
  Jinzheng He, Junyang Lin, et al. Qwen2-audio technical report. arXiv preprint arXiv:2407.10759,
  2024.
C. Cieri, D. Miller, and K. Walker. The fisher corpus: A resource for conversational speech. LDC,
  2004.
Wenqian Cui, Dianzhi Yu, Xiaoqi Jiao, Ziqiao Meng, Guangyan Zhang, Qichao Wang, Yiwen
 Guo, and Irwin King. Recent advances in speech language models: A survey. arXiv preprint
 arXiv:2410.03751, 2024.
Alexandre Défossez, Laurent Mazaré, Manu Orsini, Amélie Royer, Patrick Pérez, Hervé Jégou,
  Edouard Grave, and Neil Zeghidour. Moshi: a speech-text foundation model for real-time dialogue.
  arXiv preprint arXiv:2410.00037, 2024.


                                                10
Ding Ding, Zeqian Ju, Yichong Leng, Songxiang Liu, Tong Liu, Zeyu Shang, Kai Shen, Wei Song,
  Xu Tan, Heyi Tang, et al. Kimi-audio technical report. arXiv preprint arXiv:2504.18425, 2025.
Zhihao Du, Yuxuan Wang, Qian Chen, Xian Shi, Xiang Lv, Tianyu Zhao, Zhifu Gao, Yexin Yang,
  Changfeng Gao, Hui Wang, et al. Cosyvoice 2: Scalable streaming speech synthesis with large
  language models. arXiv preprint arXiv:2412.10117, 2024.
Fahim Faisal, Sharlina Keshava, Md Mahfuz Ibn Alam, and Antonios Anastasopoulos. Sd-qa: Spoken
  dialectal question answering for the real world. In Findings of the Association for Computational
  Linguistics: EMNLP 2021, 2021.
fixie-ai. ultravox. URL https://github.com/fixie-ai/ultravox.
Eduardo Fonseca, Jordi Pons Puig, Xavier Favory, Frederic Font Corbera, Dmitry Bogdanov, Andres
  Ferraro, Sergio Oramas, Alastair Porter, and Xavier Serra. Freesound datasets: a platform for the
  creation of open audio datasets. 2017.
Google. gemini3.1-flash-live-preview. https://ai.google.dev/gemini-api/docs/models/g
  emini3.1-flash-live-preview.
Google. gemini2.5-flash-native-audio-preview-12-2025. https://ai.google.dev/gemini-api
 /docs/models/gemini2.5-flash-native-audio-preview-12-2025, 2025.
Yanzhang He, Tara N Sainath, Rohit Prabhavalkar, Ian McGraw, Raziel Alvarez, Ding Zhao, David
  Rybach, Anjuli Kannan, Yonghui Wu, Ruoming Pang, et al. Streaming end-to-end speech recog-
  nition for mobile devices. In ICASSP 2019-2019 IEEE International Conference on Acoustics,
  Speech and Signal Processing (ICASSP), pages 6381–6385. IEEE, 2019.
Chi-Yuan Hsiao, Ke-Han Lu, Yu-Kuan Fu, Guan-Ting Lin, Hsiao-Tsung Hung, and Hung-yi Lee.
  Aspirin: Action space projection for interactivity-optimized reinforcement learning in full-duplex
  speech language models. arXiv preprint arXiv:2604.10065, 2026.
Ke Hu, Ehsan Hosseini-Asl, Chen Chen, Edresson Casanova, Subhankar Ghosh, Piotr Żelasko,
  Zhehuai Chen, Jason Li, Jagadeesh Balam, and Boris Ginsburg. Efficient and direct duplex
  modeling for speech-to-speech language model. arXiv preprint arXiv:2505.15670, 2025.
Dhruv Jain, Harshit Shukla, Gautam Rajeev, Ashish Kulkarni, Chandra Khatri, and Shubham Agarwal.
  Voiceagentbench: Are voice assistants ready for agentic tasks? arXiv preprint arXiv:2510.07978,
  2025.
Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly
 supervised challenge dataset for reading comprehension. arXiv preprint arXiv:1705.03551, 2017.
Hatim Khouzaimi, Romain Laroche, and Fabrice Lefèvre. Reinforcement learning for turn-taking
  management in incremental spoken dialogue systems. In IJCAI, pages 2831–2837, 2016.
Nithin Rao Koluguri, Monica Sekoyan, George Zelenfroynd, Sasha Meister, Shuoyang Ding, Sofia Ko-
  standian, He Huang, Nikolay Karpov, Jagadeesh Balam, Vitaly Lavrukhin, et al. Granary: Speech
  recognition and translation dataset in 25 european languages. arXiv preprint arXiv:2505.13404,
  2025.
Oleksii Kuchaiev, Jason Li, Huyen Nguyen, Oleksii Hrinchuk, Ryan Leary, Boris Ginsburg, Samuel
  Kriman, Stanislav Beliaev, Vitaly Lavrukhin, Jack Cook, et al. Nemo: a toolkit for building ai
  applications using neural modules. arXiv preprint arXiv:1909.09577, 2019.
Stephen C Levinson and Francisco Torreira. Timing in turn-taking and its implications for processing
  models of language. Frontiers in psychology, 6:136034, 2015.
Tianpeng Li, Jun Liu, Tao Zhang, Yuanbo Fang, Da Pan, Mingrui Wang, Zheng Liang, Zehuan Li,
  Mingan Lin, Guosheng Dong, et al. Baichuan-audio: A unified framework for end-to-end speech
  interaction. arXiv preprint arXiv:2502.17239, 2025.
Xinjian Li, Shinnosuke Takamichi, Takaaki Saeki, William Chen, Sayaka Shiota, and Shinji Watanabe.
  Yodas: Youtube-oriented dataset for audio and speech. In 2023 IEEE Automatic Speech Recognition
  and Understanding Workshop (ASRU), pages 1–8. IEEE, 2023.


                                                11
Guan-Ting Lin, Jiachen Lian, Tingle Li, Qirui Wang, Gopala Anumanchipalli, Alexander H Liu, and
  Hung-yi Lee. Full-duplex-bench: A benchmark to evaluate full-duplex spoken dialogue models on
  turn-taking capabilities. arXiv preprint arXiv:2503.04721, 2025a.
Guan-Ting Lin, Prashanth Gurunath Shivakumar, Aditya Gourav, Yile Gu, Ankur Gandhe, Hung-yi
  Lee, and Ivan Bulyko. Align-slm: Textless spoken language models with reinforcement learning
  from ai feedback. In Proceedings of the 63rd Annual Meeting of the Association for Computational
 Linguistics (Volume 1: Long Papers), pages 20395–20411, 2025b.
Guan-Ting Lin, Chen Chen, Zhehuai Chen, and Hung-yi Lee. Full-duplex-bench-v3: Benchmarking
  tool use for full-duplex voice agents under real-world disfluency. arXiv preprint arXiv:2604.04847,
  2026a.
Guan-Ting Lin, Shih-Yun Shan Kuan, Qirui Wang, Jiachen Lian, Tingle Li, Shinji Watanabe, and
  Hung-yi Lee. Full-duplex-bench v1. 5: Evaluating overlap handling for full-duplex speech models.
  In ICASSP 2026-2026 IEEE International Conference on Acoustics, Speech and Signal Processing
 (ICASSP), pages 19447–19451. IEEE, 2026b.
Simon Lupart, Mohammad Aliannejadi, and Evangelos Kanoulas. Chatr1: Reinforcement learn-
  ing for conversational reasoning and retrieval augmented question answering. arXiv preprint
  arXiv:2510.13312, 2025.
Niko Moritz, Takaaki Hori, and Jonathan Le. Streaming automatic speech recognition with the
  transformer model. In ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech
  and Signal Processing (ICASSP), pages 6074–6078. IEEE, 2020.
Eliya Nachmani, Alon Levkovitch, Roy Hirsch, Julian Salazar, Chulayuth Asawaroengchai, Soroosh
  Mariooryad, Ehud Rivlin, RJ Skerry-Ryan, and Michelle Tadmor Ramanovich. Spoken question an-
  swering and speech continuation using spectrogram-powered llm. arXiv preprint arXiv:2305.15255,
  2023.
Tu Anh Nguyen, Eugene Kharitonov, Jade Copet, Yossi Adi, Wei-Ning Hsu, Ali Elkahky, Paden
  Tomasello, Robin Algayres, Benoit Sagot, Abdelrahman Mohamed, et al. Generative spoken
  dialogue language modeling. Transactions of the Association for Computational Linguistics, 11:
  250–266, 2023.
Vahid Noroozi, Zhehuai Chen, Somshubra Majumdar, Steve Huang, Jagadeesh Balam, and Boris
  Ginsburg. Instruction data generation and unsupervised adaptation for speech language models.
  arXiv preprint arXiv:2406.12946, 2024a.
Vahid Noroozi, Somshubra Majumdar, Ankur Kumar, Jagadeesh Balam, and Boris Ginsburg. Stateful
  conformer with cache-based inference for streaming automatic speech recognition. In ICASSP
  2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
  pages 12041–12045. IEEE, 2024b.
NVIDIA. Nemotron 3 VoiceChat Model Card. https://build.nvidia.com/nvidia/nemotron
 -voicechat/modelcard, 2026. Accessed: 2026-05-07.
OpenAI. gptrealtime-1.5. https://developers.openai.com/api/docs/models/gptrealtim
  e-1.5.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong
  Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow
  instructions with human feedback. Advances in neural information processing systems, 35:27730–
  27744, 2022.
Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever.
  Robust speech recognition via large-scale weak supervision, 2022. URL https://arxiv.org/
  abs/2212.04356.
Tazeek Bin Abdur Rakib, Ambuj Mehrish, Lay-Ki Soon, Wern Han Lim, and Soujanya Poria.
  Dialogxpert: Driving intelligent and emotion-aware conversations through online value-based
  reinforcement learning with llm priors. In Proceedings of the AAAI Conference on Artificial
  Intelligence, volume 40, pages 29967–29975, 2026.


                                                 12
Antoine Raux and Maxine Eskenazi. Optimizing the turn-taking behavior of task-oriented spoken
  dialog systems. ACM Transactions on Speech and Language Processing (TSLP), 9(1):1–23, 2012.

Dima Rekesh, Nithin Rao Koluguri, Samuel Kriman, Somshubra Majumdar, Vahid Noroozi,
  He Huang, Oleksii Hrinchuk, Krishna Puvvada, Ankur Kumar, Jagadeesh Balam, et al. Fast
  conformer with linearly scalable attention for efficient speech recognition. In 2023 IEEE Automatic
  Speech Recognition and Understanding Workshop (ASRU), pages 1–8. IEEE, 2023.

Rajarshi Roy, Jonathan Raiman, Sang-gil Lee, Teodor-Dumitru Ene, Robert Kirby, Sungwon Kim,
  Jaehyeon Kim, and Bryan Catanzaro. Personaplex: Voice and role control for full duplex conversa-
  tional speech models. arXiv preprint arXiv:2602.06053, 2026.

Harvey Sacks, Emanuel A Schegloff, and Gail Jefferson. A simplest systematics for the organization
  of turn-taking for conversation. language, 50(4):696–735, 1974.

David Schlangen and Gabriel Skantze. A general, abstract model of incremental dialogue processing.
  Dialogue & Discourse, 2(1):83–111, 2011.

John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
  optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.

Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathemat-
  ical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

Mohan Shi, Yuchun Shu, Lingyun Zuo, Qian Chen, Shiliang Zhang, Jie Zhang, and Li-Rong
 Dai. Semantic vad: Low-latency voice activity detection for speech interaction. arXiv preprint
 arXiv:2305.12450, 2023.

RJ Skerry-Ryan, Eric Battenberg, Ying Xiao, Yuxuan Wang, Daisy Stanton, Joel Shor, Ron Weiss,
  Rob Clark, and Rif A Saurous. Towards end-to-end prosody transfer for expressive speech synthesis
  with tacotron. In international conference on machine learning, pages 4693–4702. PMLR, 2018.

David Snyder, Guoguo Chen, and Daniel Povey. Musan: A music, speech, and noise corpus. arXiv
  preprint arXiv:1510.08484, 2015.

Tanya Stivers, Nicholas J Enfield, Penelope Brown, Christina Englert, Makoto Hayashi, Trine
  Heinemann, Gertie Hoymann, Federico Rossano, Jan Peter De Ruiter, Kyung-Eun Yoon, et al.
  Universals and cultural variation in turn-taking in conversation. Proceedings of the National
  Academy of Sciences, 106(26):10587–10592, 2009.

Dan Su, Kezhi Kong, Ying Lin, Joseph Jennings, Brandon Norick, Markus Kliegl, Mostofa Patwary,
  Mohammad Shoeybi, and Bryan Catanzaro. Nemotron-cc: Transforming common crawl into
  a refined long-horizon pretraining dataset. In Proceedings of the 63rd Annual Meeting of the
  Association for Computational Linguistics (Volume 1: Long Papers), pages 2459–2475, 2025.

R. Sutton and A. Barto. Reinforcement learning: An introduction. 2018.

Qwen Team. Qwen2.5: A party of foundation models, September 2024. URL https://qwenlm.g
 ithub.io/blog/qwen2.5/.

Bandhav Veluri, Benjamin N Peloquin, Bokai Yu, Hongyu Gong, and Shyamnath Gollakota. Be-
  yond turn-based interfaces: Synchronous llms as full-duplex dialogue agents. arXiv preprint
  arXiv:2409.15594, 2024.

Dingdong Wang, Jincenzi Wu, Junan Li, Dongchao Yang, Xueyuan Chen, Tianhua Zhang, and Helen
  Meng. Mmsu: A massive multi-task spoken language understanding and reasoning benchmark.
  arXiv preprint arXiv:2506.04779, 2025.

Peng Wang, Songshuo Lu, Yaohua Tang, Sijie Yan, Wei Xia, and Yuanjun Xiong. A full-duplex speech
  dialogue scheme based on large language model. Advances in Neural Information Processing
  Systems, 37:13372–13403, 2024a.


                                                 13
Xiong Wang, Yangze Li, Chaoyou Fu, Yunhang Shen, Lei Xie, Ke Li, Xing Sun, and Long Ma.
  Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm. arXiv
  preprint arXiv:2411.00774, 2024b.
Nigel Ward and Wataru Tsukahara. Prosodic features which cue back-channel responses in english
  and japanese. Journal of pragmatics, 32(8):1177–1207, 2000.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
  Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in
  neural information processing systems, 35:24824–24837, 2022.
Anne Wu, Laurent Mazaré, Neil Zeghidour, and Alexandre Défossez. Aligning spoken dialogue
  models from user interactions. arXiv preprint arXiv:2506.21463, 2025a.
Donghang Wu, Haoyang Zhang, Chen Chen, Tianyu Zhang, Fei Tian, Xuerui Yang, Gang Yu, Hexin
  Liu, Nana Hou, Yuchen Hu, et al. Chronological thinking in full-duplex spoken dialogue language
  models. arXiv preprint arXiv:2510.05150, 2025b.
Donghang Wu, Tianyu Zhang, Yuxin Li, Hexin Liu, Chen Chen, Eng Siong Chng, and Yoshua Bengio.
  The silent thought: Modeling internal cognition in full-duplex spoken dialogue models via latent
  reasoning. arXiv preprint arXiv:2603.17837, 2026.
x.ai. grok-voice-agent-api. https://x.ai/news/grok-voice-agent-api.
Zhifei Xie, Mingbao Lin, Zihang Liu, Pengcheng Wu, Shuicheng Yan, and Chunyan Miao. Audio-
  reasoner: Improving reasoning capability in large audio language models. arXiv preprint
  arXiv:2503.02318, 2025.
Kenta Yamamoto, Ryu Takeda, and Kazunori Komatani. Analysis of voice activity detection errors
  in api-based streaming asr for human-robot dialogue. In Proceedings of the 15th International
 Workshop on Spoken Dialogue Systems Technology, pages 245–253, 2025.
Ruiqi Yan, Wenxi Chen, Zhanxun Liu, Ziyang Ma, Haopeng Lin, Hanlin Wen, Hanke Xie, Jun Wu,
  Yuzhe Liang, Yuxiang Zhao, et al. Soulx-duplug: Plug-and-play streaming state prediction module
  for realtime full-duplex speech conversation. arXiv preprint arXiv:2603.14877, 2026a.
Ruiqi Yan, Wenxi Chen, Zhanxun Liu, Ziyang Ma, Haopeng Lin, Hanlin Wen, Hanke Xie, Jun Wu,
  Yuzhe Liang, Yuxiang Zhao, et al. Soulx-duplug: Plug-and-play streaming state prediction module
  for realtime full-duplex speech conversation. arXiv preprint arXiv:2603.14877, 2026b.
Wenyi Yu, Siyin Wang, Xiaoyu Yang, Xianzhao Chen, Xiaohai Tian, Jun Zhang, Guangzhi Sun,
 Lu Lu, Yuxuan Wang, and Chao Zhang. Salmonn-omni: A standalone speech llm without codec
 injection for full-duplex conversation. arXiv preprint arXiv:2505.17060, 2025.
Heiga Zen, Viet Dang, Rob Clark, Yu Zhang, Ron J Weiss, Ye Jia, Zhifeng Chen, and Yonghui Wu.
  Libritts: A corpus derived from librispeech for text-to-speech. arXiv preprint arXiv:1904.02882,
  2019.
Aohan Zeng, Zhengxiao Du, Mingdao Liu, Kedong Wang, Shengmin Jiang, Lei Zhao, Yuxiao Dong,
  and Jie Tang. Glm-4-voice: Towards intelligent and human-like end-to-end spoken chatbot. arXiv
  preprint arXiv:2412.02612, 2024.
Hao Zhang, Weiwei Li, Rilin Chen, Vinay Kothapally, Meng Yu, and Dong Yu. Llm-enhanced
  dialogue management for full-duplex spoken dialogue systems. arXiv preprint arXiv:2502.14145,
  2025.
Yue Zhao, Xiaoyu Wang, Dan Wang, Zhonglin Jiang, Qingqing Gu, Teng Chen, Ningyuan Xi, Jinxian
  Qu, Yong Chen, and Luo Ji. Dream to chat: Model-based reinforcement learning on dialogues
  with user belief modeling. In Findings of the Association for Computational Linguistics: EMNLP
  2025, pages 4764–4781, 2025.
L. Zheng and et al. Judging llm-as-a-judge with mt-bench and chatbot arena. arXiv preprint, 2023.



                                               14
A     Data Details
In this chapter, we illustrate all the synthetic and real data we used in this work. In pre-training, we use
the speech-continuation data to make the model understand speech input under full-duplex modeling.
Then, all other data is used in SFT to improve the reasoning ability and build a helpful speech agent.
The broader data-construction recipe follows the released Nemotron-VoiceChat materials [NVIDIA,
2026].

1. Speech-continuation data. Speech-continuation pre-training uses 530K hours of examples
derived from large text corpora [Su et al., 2025]. Each continuous passage is converted into a
two-party pseudo-dialogue by assigning successive sentences to the user and agent streams. Turn
lengths are randomized: a turn stops after one sentence with probability 0.8, while longer turns are
formed by appending additional sentences with a decaying continuation probability; turns longer
than 200 words are handed to the other speaker. The resulting turns are synthesized with two speaker
profiles, aligned in time, and packed into synchronized two-stream full-duplex examples. We also
swap user and agent roles to increase coverage of both conversational directions.

2. Instruction-following QA data. The instruction-following mixture contributes 70K hours of
spoken QA data. Within this set, 10K hours are single-turn examples spanning broad topics, and the
remaining multi-turn examples train the assistant to maintain conversations lasting up to four minutes.
Dialogue generation uses a helpful-assistant prompt and is conditioned on heterogeneous textual
contexts, including Wikipedia pages.2 The generated turns are then rendered with the multi-speaker
TTS pipeline.

3. Synthetic user interruption. We augment multi-turn examples with simulated barge-ins. When
an agent utterance lasts more than four seconds, a user interruption is inserted with probability
0.1, and its onset is sampled uniformly from the 20%–80% span of the agent utterance. After the
interruption begins, the agent stream is given an 8-token reaction delay (≈ 0.64 s) before it is forced
to emit an end-of-sequence (<EOS>) token. At inference time, an <EOS> on the text channel masks
the corresponding audio channel to silence.

4. ASR-QA data. ASR-QA examples expose the model to real recording conditions. We use
speech segments from the open-source corpora aggregated in NeMo ASRSET [Noroozi et al., 2024b]
as acoustic contexts. Following Noroozi et al. [2024a], an LLM writes questions grounded in the ASR
transcripts. These clips are shorter and less knowledge-dense than the synthetic QA conversations,
but they add real speaker variation, channel effects, and background noise to the full-duplex training
mixture.

Model diversity and prompt speaker pool. The synthetic portions of our training mixture are
generated with several text and acoustic models rather than a single generator. Text responses
are sampled from a pool of instruction-tuned LLMs, including GPT-OSS-120B,3 Qwen2.5-72B
Instruct,4 and Llama3.1-70B-Instruct.5 Speech rendering is performed with multiple TTS backends,
including Chatterbox,6 Magpie-TTS,7 and Mooncast.8 For voice conditioning, we build a prompt
pool from all 5–10 s speech segments in LibriTTS [Zen et al., 2019], YODAS [Li et al., 2023], and
Hifi-TTS [Bakhturina et al., 2021]. This pool contains more than 100K prompt segments and covers
over 20K speakers.

Dynamics-aware dialogue reconstruction. Fisher [Cieri et al., 2004] and Seamless-Naturalistic-
HQ (Seamless) [Agrawal et al., 2025] provide the natural timing signals used for rhythm-aware
training. Starting from word-level alignments, we recover utterance segments by merging nearby
words while keeping short lexical acknowledgments as standalone backchannels. For Seamless, we
    2 https://huggingface.co/datasets/wikimedia/wikipedia
    3 https://huggingface.co/openai/gpt-oss-120b
    4 https://huggingface.co/Qwen/Qwen2.5-72B-Instruct
    5 https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct
    6 https://github.com/resemble-ai/chatterbox
    7 https://docs.nvidia.com/nemo-framework/user-guide/latest/speech_ai/magpietts.html
    8 https://github.com/jzq2000/MoonCast




                                                    15
remove non-dialogue sessions and low-quality utterance fragments before sampling. The processed
training set contains 24.6K Fisher samples and 43.1K Seamless samples. Splits are fixed at the
conversation or session level before reconstruction, so no evaluation conversation contributes SFT
examples, RL windows, reward targets, or timing annotations. Fisher evaluation uses a held-out
Fisher test SHAR view, while Seamless evaluation uses a held-out eval-clean view rather than the
naturalistic training split. During training, a randomized round-robin sampler balances the two
sources, and each sample is truncated at 210 seconds.

Acoustic augmentation. Acoustic robustness is improved with both feature-level and waveform-
level augmentation. User speech features are augmented with SpecAugment, and the waveform
stream is mixed with a curated set of 10K noise clips from Freesound [Fonseca et al., 2017] and
MUSAN [Snyder et al., 2015]. Noise is added with probability 0.5, with the signal-to-noise ratio
sampled uniformly between 0 dB and 60 dB.

B     Training Details
Implementation. The implementation builds on the released Nemotron-VoiceChat recipe [NVIDIA,
2026] and is trained with the NeMo Toolkit [Kuchaiev et al., 2019]. We select a smaller language
backbone Qwen2.5-7B-Instruct [Team, 2024] than Nemotron-VoiceChat. Streaming speech is
encoded by a 600M-parameter Parakeet-based encoder with causal convolutional context,9 followed
by a 1024-dimensional Transformer modality adapter that maps acoustic features into the LLM
embedding space [Koluguri et al., 2025, Rekesh et al., 2023]. The speech codec and the streaming
flow-matching generator follow CosyVoice2 [Du et al., 2024]. The speech encoder and codec remain
frozen during training. The speech encoder and LLM advance at 12.5 Hz, whereas the audio codec
runs at 25 Hz; each LLM frame therefore predicts two speech tokens to keep the text and audio
streams temporally aligned. All runs use 64 A800 80 GB GPUs.

Supervised fine-tuning. SFT is applied after speech-continuation pre-training to adapt the model
to assistant-style spoken interaction. The base SFT mixture uses the instruction-following QA data in
Appendix A, together with ASR-QA and synthetic-interruption examples that expose the model to real
acoustics and basic barge-in handling. SFT Baseline uses this mixture and excludes dynamics-aware
dialogue data. SFT Dynamics keeps the same schedule but adds the reconstructed dynamics-aware
dialogue data from Section 4.1, making it the data-matched SFT control for DuplexPO.

Optimization. Pre-training, SFT, and RL use AdamW. For pre-training and SFT, we use β =
(0.9, 0.98), a weight decay of 0, and an inverse-square-root learning-rate schedule. Pre-training uses
a peak learning rate of 5 × 10−4 after a 2,500-step warm-up, while the SFT stages use a peak learning
rate of 5 × 10−5 . These stages are trained with bfloat16 mixed precision, and gradients are clipped to
a maximum norm of 1.0. Additional RL and reward hyperparameters are summarized in Table 5.

C     Definition of Suppressed Intent Rate (SIR) and Suppression Release Ratio
      (SRR)
To quantify a full-duplex agent’s ability to start speaking when appropriate and to stop speaking
when the user takes the floor, we introduce two complementary metrics. Both are computed at
the frame level on the agent’s text head and are defined symmetrically for the two control actions
a⋆ ∈ {<BOS>, <EOS>}.
Let πSFT and πRL denote the SFT and DuplexPO policies. Let pSFT                       RL
                                                                        t (a) and pt (a) denote the
probability each policy assigns to token a at frame t. To isolate differences attributable to the policy
head rather than to trajectory divergence, both quantities are evaluated on a single shared context,
namely the SFT-generated trajectory. Let ŷtSFT and ŷtRL denote the corresponding arg max tokens.
We say that the SFT policy has an intent for action a⋆ at frame t when pSFT      ⋆
                                                                           t (a ) > τ , with τ a fixed
threshold (we use τ = 0.1 throughout).
For each action we restrict attention to a frame set Fa⋆ in which the corresponding intent is mean-
ingful. We define F<BOS> = {t | ŷtSFT = PAD} as the set of frames at which the SFT model
    9 https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b




                                                  16
Table 5: DuplexPO RL and reward hyperparameters used for the reported run. Time values are in
seconds unless otherwise noted.
 Group          Hyperparameter                            Value            Role
 Windowing      Frame duration ∆                          0.08             LLM decision grid.
 Windowing      Training lead time L                      1.0              Context before annotated
                                                                           agent onset.
 Windowing      Training buffer B                         2.0              Rollout region after anno-
                                                                           tated agent offset.
 Windowing      Validation lead / buffer                  2.0 / 2.0        Wider evaluation context for
                                                                           testing early starts and yield-
                                                                           ing behavior.
 Windowing      Full-turn windows per conversation        3                Maximum sampled non-
                                                                           backchannel segments.
 Windowing      Backchannel windows per conversation      1                Maximum               sampled
                                                                           backchannel segments.
 Windowing      Full-turn windows per conversation        3                Maximum number of sam-
                                                                           pled non-backchannel win-
                                                                           dows.
 Windowing      Backchannel windows per conversation      1                Maximum number of sam-
                                                                           pled backchannel windows.
 Rollout        Samples per window                        4                GRPO group size for reward
                                                                           normalization.
 Rollout        Temperature / top-p                       1.0 / 0.9        Sampling policy for continu-
                                                                           ations.
 Rollout        Maximum rollout steps                     200              Maximum generated frames
                                                                           inside a window.
 Rollout        Rollout chunk size                        128              Chunk size for rollout pro-
                                                                           cessing.
 Optimization   RL learning rate                          1 × 10−5         AdamW learning rate.
 Optimization   Warm-up / minimum LR                      100 / 1 × 10−6   Inverse-square-root schedule.
 Optimization   KL coefficient β                          0.2              Regularization strength to-
                                                                           ward the reference policy.
 Optimization   Advantage clipping                        [−5, 5]          Clip range for group-
                                                                           normalized advantages.
 Reward         Missed-event penalty                      −0.5             Penalty for failing to initiate
                                                                           a target event.
 Reward         False-alarm penalty                       −0.5             Penalty for unwarranted
                                                                           starts.
 Reward         Backchannel overlong penalty              −0.5             Penalty for floor-grabbing
                                                                           backchannels.
 Reward         No-<EOS> penalty scale                    0.75             Scale for failure to stop after
                                                                           user takeover.
 Reward         Observable margin                         0.16             Margin for determining ob-
                                                                           servable turn-end evidence.
 Reward         Interrupt grace                           0.16             Grace period around user in-
                                                                           terruption.
 Reward         Stop tolerance                            0.24             Allowed delay for yielding af-
                                                                           ter target stop time.
 Reward         Explicit <EOS> bonus                      0.05             Small bonus for explicit
                                                                           yielding.
 Reward         Near-target PAD penalty                   −0.02            Penalty for silence near a tar-
                                                                           get start.
 Reward         Early / late stop penalties               −0.15 / −0.10    Penalties for mistimed turn
                                                                           offset.




remains silent, where the intent is the impulse to start speaking. We define F<EOS> = {t | ŷtSFT ̸=
<EOS> and the agent is mid-utterance at t} as the set of frames at which the SFT model continues
speaking, where the intent is the impulse to stop speaking.


                                                     17
Suppressed Intent Rate (SIR). SIR is the fraction of frames in Fa⋆ at which the SFT policy holds
a latent intent for a⋆ but is overridden by a different action,
                                                           ⋆
                                           {t ∈ Fa⋆ | pSFT
                                                       t (a ) > τ }
                              SIRa⋆ =                               .                             (11)
                                                     Fa⋆
A higher SIRa⋆ indicates that the SFT model has internalised the relevant action intent at the
representational level, yet its decision boundary fails to translate that intent into behaviour.

Suppression Release Ratio (SRR).        SRR is a paired metric defined on exactly the suppressed-intent
frames identified by SIR. Let
                                                      ⋆
                                Sa⋆ = {t ∈ Fa⋆ | pSFT
                                                  t (a ) > τ }.                                   (12)
On this same frame set, SRR measures how often the RL policy actually takes action a⋆ ,
                                              {t ∈ Sa⋆ | ŷtRL = a⋆ }
                               SRRa⋆ =                                .                           (13)
                                                       Sa⋆
A higher SRRa⋆ indicates that RL’s behavioural change is concentrated precisely on frames where
the SFT model already exhibited a latent intent, rather than reflecting an indiscriminate shift toward
more action-taking.

D    Attention Analysis
This appendix provides additional analysis for the model behaviour analysed in Section 5. The
attention statistics in Figure 4 and Table 6 should be read as supporting evidence about context usage,
not as a mechanistic proof of the learned timing policy.




Figure 4: Attention mass distribution across token categories. Attention mass is averaged across
layers and grouped by token category, including the <BOS> token, early positions, PAD positions,
real-text tokens, and recent-context tokens. In our streaming representation, PAD positions encode
non-speech or waiting states that can inform speaking and yielding decisions. Compared with Moshi
7B, DuplexPO assigns less mass to the initial <BOS> sink and more mass to real-text, recent-context,
and PAD-state positions.

                 Table 6: Attention mass distribution (%) across token categories.

                  Metric                 Moshi 7B [Défossez et al., 2024]   DuplexPO
                  <BOS> sink (pos. 0)                   70.2                  14.5
                  First 4 positions                     74.2                  37.9
                  PAD positions                         28.0                  77.5
                  Real-text positions                    1.8                  22.5
                  Last 16 tokens                        13.5                  33.4
                  Attention entropy                     1.63                  3.19



E    Judge Calibration with Synthetic Timing Perturbations
To assess whether the pairwise LLM judge is sensitive to conversational timing rather than transcript
content alone, we conduct a controlled timing-perturbation sanity check on Fisher. For each conversa-
tion, we keep the user timeline and the agent transcript unchanged, but shift the agent timestamps by


                                                   18
Table 7: Judge calibration under synthetic timing perturbations on Fisher. The transcript content is
identical across candidates; only the agent timestamps are shifted. Candidate order is randomized.
Win rates are computed over non-tie judgments. p-values are computed using a two-sided binomial
sign test.

 Perturbation          # Conv.   Original Wins     Perturbed Wins      Ties       Original Win Rate     p-value
 Delayed by +1.0s           26         18                 8             0              69.2%            0.076
 Advanced by −1.0s          26         21                 5             0              80.8%            0.002



±1.0 seconds. A +1.0s shift makes agent responses and backchannels systematically late, while a
−1.0s shift makes agent speech more likely to occur prematurely during ongoing user speech. The
judge is then asked to compare the original timeline with the perturbed timeline using the same
blinded pairwise protocol as in Appendix F. Candidate order is randomized across examples.
Importantly, in this calibration experiment, we remove aggregate dynamics statistics from the judge
input. Thus, the judge must rely on the aligned timestamps and transcripts rather than precomputed
automatic metrics. Win rates are computed over non-tie judgments, and statistical significance is
evaluated with a two-sided binomial sign test.
As shown in Table 7, the judge prefers the original timing over both delayed and advanced perturba-
tions. The effect is significant for advanced perturbations and marginal for delayed ones. Because
the transcript content is identical across candidates, the results indicate a timing preference aligned
with human conversational perception, with stronger sensitivity to premature turn entry than to
comparable response delays [Sacks et al., 1974, Stivers et al., 2009, Levinson and Torreira, 2015].
This asymmetry also supports the design of FCDR’s onset reward, which applies a narrower tolerance
to early initiation than to delayed responses.

F     LLM Pairwise Judge for Full-Duplex Dialogue Naturalness
The pairwise judge is designed to evaluate conversational dynamics rather than semantic answer
quality. Table 9 gives the system instruction, and Table 10 gives the user-prompt template used
to present aligned candidate timelines. We used Gemini 3.0 Pro and counted a result only when
the returned JSON matched the requested schema and contained no error. Candidate labels were
anonymized in the prompt, and in these runs candidate A is the SFT Baseline and candidate B is
DuplexPO. Table 8 reports both overall and dimension-level preferences. Win rates are computed over
non-tie judgments, and the p-values use a two-sided binomial sign test over the non-tie preferences.

Table 8: Conversation-level LLM pairwise judge results. Candidate B is DuplexPO; candidate A is
the SFT Baseline. Win rates exclude ties.
    Dataset     Criterion             Total      B wins       A wins    Ties        B win rate        p-value
    Fisher      Overall                 26          20            6           0           76.9          0.009
    Fisher      Turn-taking             26          20            6           0           76.9          0.009
    Fisher      Backchannel             26          22            2           2           91.7        < 10−4
    Fisher      Barge-in handling       26          21            3           2           87.5        < 10−3
    Seamless    Overall                383         264          117          2            69.3    < 10−13
    Seamless    Turn-taking            383         250          123         10            67.0    < 10−10
    Seamless    Backchannel            383         261           54         68            82.9    < 10−32
    Seamless    Barge-in handling      383         237           70         76            77.2    < 10−21



G     Reward Visualisation
As shown in Figure 5, the reward curve increases monotonically and then stabilises, suggesting
that training is robust and generalises across dialogue contexts. The pairwise correlation analysis in
Figure 6 highlights the specialisation of reward signals: the stop reward provides the strongest signal


                                                   19
    Table 9: System prompt for LLM pairwise judging of full-duplex dialogue dynamics.
System prompt

You are an expert evaluator for full-duplex spoken dialogue rhythm.

Your role:
- Compare two candidate system turns from the same local dialogue context.
- Evaluate ONLY three interaction abilities: turn-taking, backchanneling,
  and user barge-in handling.
- Use only the observable local dialogue context and candidate turns
  provided in the prompt. Do NOT assume access to any hidden annotations,
  target response, target timing interval, or dataset label.
- Do NOT evaluate factual correctness, knowledge, helpfulness,
  informativeness, or whether the answer fully solves the user's question.
- Do NOT prefer a candidate merely because it is more detailed, more
  informative, or more semantically complete.
- If both candidates are similar on these three interaction abilities,
  output "tie".

Evaluation dimensions:
1. turn_taking: Which candidate starts at a more natural time and yields
   smoothly for the local conversation state. Do not reward a candidate
   for being longer or more substantive.
2. backchannel: Which candidate better uses short listener feedback when
   appropriate, without being stale, too long, or floor-grabbing.
3. user_barge_in_handling: Which candidate better avoids talking over
   the user or better yields/gets out of the way when the user starts or
   continues speaking.

Important judgment rules:
- Judge from timing and local dialogue behaviour, not answer quality.
- A short response can be better if it functions as a natural backchannel.
- A longer response should not be preferred just because it holds the
  floor or gives more content.
- Penalise competitive interruption, awkward delayed feedback, excessive
  overlap with the user, and failure to yield when the user appears to
  take the floor.
- If one dimension is hard to determine from the visible context and
  candidate timestamps, mark that dimension as "tie".

You MUST:
1. Read the shared local context first.
2. Infer the local turn-taking state: user_holding_floor,
   user_yielding_floor, backchannel_opportunity, full_turn_opportunity,
   or uncertain.
3. Compare candidate A and candidate B on the three dimensions.
4. State preferred_candidate as "A", "B", or "tie".
5. Give concise reasons focused only on turn-taking, backchanneling,
   and user barge-in handling.
6. Give confidence from 0 to 1.

Output MUST be valid JSON matching this schema, with no markdown and no
extra text:
{
  "interaction_id": "string",
  "pair_id": "string",
  "candidate_a_id": "string",
  "candidate_b_id": "string",
  "inferred_turn_state": "user_holding_floor|user_yielding_floor|
                           backchannel_opportunity|full_turn_opportunity|
                           uncertain",
  "preferred_candidate": "A|B|tie",
  "preference_reason": "string",
  "dimension_preferences": {
     "turn_taking":            {"preferred_candidate": "A|B|tie",
                                "reason": "string"},
     "backchannel":            {"preferred_candidate": "A|B|tie",
                                "reason": "string"},
     "user_barge_in_handling": {"preferred_candidate": "A|B|tie",
                                "reason": "string"}
  },
  "major_rhythm_issues": ["string"],         20
  "content_quality_ignored_note": "string",
  "confidence": 0.0-1.0
}
      Table 10: User-prompt template for conversation-level pairwise dynamics judging.
User prompt template

Compare candidate A and candidate B for overall full-duplex
spoken-dialogue rhythm across this conversation sample. Ignore factual
correctness, answer completeness, and informativeness. Output only valid
JSON matching the schema.

## Interaction ID
{interaction_id}

## Shared user timeline
- [user] ({user_turn_1_start_s:.2f}s--{user_turn_1_end_s:.2f}s)
  {user_turn_1_text}
- [user] ({user_turn_2_start_s:.2f}s--{user_turn_2_end_s:.2f}s)
  {user_turn_2_text}
...

## Candidate A assistant timeline
- [candidate] ({candidate_a_turn_1_start_s:.2f}s--
                {candidate_a_turn_1_end_s:.2f}s)
  {candidate_a_turn_1_text}
- [candidate] ({candidate_a_turn_2_start_s:.2f}s--
                {candidate_a_turn_2_end_s:.2f}s)
  {candidate_a_turn_2_text}
...

## Candidate A observable rhythm summary
- n_turns:                      {candidate_a_n_turns}
- total_speech_ms:              {candidate_a_total_speech_ms}
- total_user_overlap_ms:        {candidate_a_total_user_overlap_ms}
- n_user_overlaps:              {candidate_a_n_user_overlaps}
- n_interrupted_by_user:        {candidate_a_n_interrupted_by_user}
- median_pause_after_user_ms:   {candidate_a_median_pause_after_user_ms}

## Candidate B assistant timeline
- [candidate] ({candidate_b_turn_1_start_s:.2f}s--
                {candidate_b_turn_1_end_s:.2f}s)
  {candidate_b_turn_1_text}
- [candidate] ({candidate_b_turn_2_start_s:.2f}s--
                {candidate_b_turn_2_end_s:.2f}s)
  {candidate_b_turn_2_text}
...

## Candidate B observable rhythm summary
- n_turns:                      {candidate_b_n_turns}
- total_speech_ms:              {candidate_b_total_speech_ms}
- total_user_overlap_ms:        {candidate_b_total_user_overlap_ms}
- n_user_overlaps:              {candidate_b_n_user_overlaps}
- n_interrupted_by_user:        {candidate_b_n_interrupted_by_user}
- median_pause_after_user_ms:   {candidate_b_median_pause_after_user_ms}




                                            21
Figure 5: Training dynamics of the total reward and its individual components across optimisation
steps. The total reward rises monotonically and then plateaus, indicating stable optimisation.




Figure 6: Pairwise correlations between reward components and the behavioural events they shape.
Stop and start rewards specialise on yielding and turn initiation respectively, with low cross-talk.


specifically for backchannel yielding, while start rewards drive the timing of turn initiation. These
correlations indicate that the model decomposes conversational dynamics into distinct, actionable
components, effectively addressing both when to yield and when to participate.


H    Ablation Study: Effect of Window Boundary Size

We separately ablate window lead time L and window buffer time B, as shown in Figure 7. The two
parameters affect the RL reward differently. Varying Window Lead Time produces a clear ordering
in mean reward, with overly long lead times causing a substantial performance drop. In contrast,
varying Window Buffer Time yields no significant separation, with the mean rewards differing by at
most 0.02. These results suggest that dynamics-critical window sampling is primarily sensitive to
the amount of anticipatory context required for committing to a speaking decision, rather than to the
amount of post-event context retained in the window.


                                                 22
                                  (a) Varying lead time (buffer = 2s)     (b) Varying buffer time (lead = 2s)




         Mean RL Reward




                                            Lead time                              Buffer time

Figure 7: Ablation of dynamics-critical window lead and buffer times. Bars show the mean RL
reward across checkpoints every 10 training steps. Error bars show ±1 standard deviation across
checkpoints.


I   Ablation Study: Neural Reward Model
The neural reward model teacher is SoulX-Duplug [Yan et al., 2026b], denoted fϕ . This method does
not use assistant ground-truth. For each training sample, the user waveform u and its aligned word
sequence {(wj , tsj , tej , temit
                             j    )}j are fed to fϕ , producing a chunk-level teacher timeline

                          T = {(am , bm , sm )}M
                                               m=1 ,         sm ∈ {idle, nonidle, speak, blank}.                (14)
The neural reward model first converts the SoulX-Duplug timeline into a state st for each frame. A
prescription prior pT (d | s, c) scores whether the agent decision dt is appropriate under teacher state
st and transition type ci ∈ {yield, interrupt}. For a predicted sequence d in window Wi , we compute
the salience-weighted teacher score
                                          Pni
                                                wi,t log pT (dt | si,t , ci )
                                Ai (d) = t=1        Pni                       ,                     (15)
                                                       t=1 wi,t

where blank frames have wi,t = 0, frames within ∼160 ms of a SoulX-Duplug transition are weighted
1.0 and other non-blank frames 0.5. The core reward subtracts a per-window frozen-reference
baseline:
                                                       K0
                             core                   1 X          ref
                           ri,k   = Ai (g(zi,k )) −       Ai (g(zi,l )).                     (16)
                                                    K0
                                                                        l=1

Table 11 shows that NRM provides a useful but less reliable dynamics signal than FCDR. Although
NRM improves over SFT Dynamics on several metrics, it does not consistently surpass the original
SFT Baseline. This suggests that teacher-derived state supervision can recover some temporal
coordination cues, but may also disturb behaviors already learned during SFT, especially for fine-
grained decisions such as backchannel yielding and ambiguous turn transitions. One likely reason
is that the neural teacher provides coarse temporal states rather than direct feedback on whether a
specific <BOS> or <EOS> decision is appropriate within the current dynamics-critical window. In
contrast, FCDR directly rewards target floor-control decisions, leading to more stable improvements
across turn-taking, backchanneling, and barge-in handling.

J   Ablation Study: Optimization Methods
Holding the FCDR-based reward calculation and the dynamics-critical window sampler fixed, we
ablate the preference-optimization objective by comparing GRPO with a DPO-style variant. In the
DPO-style variant, the highest- and lowest-reward continuations within each sampled window are
used as the preferred and dispreferred pair. Table 12 reports the resulting dynamics metrics on Fisher,
Seamless, and FDB-v3.


                                                                23
Table 11: Comparison with SFT controls and reward calculation ablation. SFT Baseline and SFT
Dynamics are non-RL controls without reward optimization. NRM and FCDR use the same dynamics-
critical window sampler and GRPO-style optimization, and differ only in the reward calculation
method. Rates are in %; Onset MAE is in seconds. Best values in each column are bolded.

 Dataset      Training setting Onset MAE (↓)         Turn-taking         Backchannel             Barge-in
                                                Init (↑) Yield (↑) Init (↑) Yield (↑) VIR (↓) Yield (↑)
              SFT Baseline         1.22          91.8          78.5     92.2     79.4        –              –
 Fisher       SFT Dynamics         1.34          79.7          63.0     83.2     63.4        –              –
              NRM reward           1.22          96.4          81.6     89.2     50.0        –              –
              FCDR reward          0.69         100.0          98.7     97.8     100.0       –              –
          SFT Baseline             1.22          91.8          78.5     92.2     79.4        –              –
 Seamless SFT Dynamics             1.34          79.7          63.0     83.2     63.4        –              –
          NRM reward               1.32          84.5          67.6     93.5     74.0        –              –
          FCDR reward              1.03          98.0          93.6     99.5     93.3        –              –
              SFT Baseline             –             –             –        –        –    8.0           64.8
 FDB-v3       SFT Dynamics             –             –             –        –        –    4.0           93.3
              NRM reward               –             –             –        –        –    4.0           93.3
              FCDR reward              –             –             –        –        –    5.0          100.0

Table 12: Optimization method ablation. Both variants use the same FCDR and dynamics-critical
window sampler, and differ only in the preference-optimization objective. Rates are reported in %;
Onset MAE is reported in seconds. The best result in each column is bolded.

    Dataset    Optimization Onset MAE (↓)        Turn-taking            Backchannel          Barge-in
                                               Init (↑) Yield (↑) Init (↑) Yield (↑) VIR (↓) Yield (↑)

    Fisher     DPO               0.81          100.0          93.6     91.4     71.4     –              –
               GRPO              0.69          100.0          98.7     97.8     100.0    –              –

    Seamless DPO                 1.00           95.1          77.8     95.8     84.7     –              –
             GRPO                1.03           98.0          93.6     99.5     93.3     –              –

    FDB-v3     DPO                 –             –             –        –        –       4.0          93.3
               GRPO                –             –             –        –        –       5.0         100.0


The results show that GRPO outperforms the DPO-style objective on most window-level dynamics
metrics, especially yield rate and backchannel behavior. This suggests that reducing each window to
only the highest- and lowest-reward continuations discards useful ranking information. In contrast,
GRPO uses group-normalized advantages over the full set of sampled continuations, providing a
denser and more stable optimization signal for dynamics-critical decisions. Although DPO achieves
slightly better Onset MAE on Seamless and a lower VIR on FDB-v3, GRPO achieves higher
yield rates across all datasets, indicating better recovery and response behavior in dynamics-critical
scenarios.

K      Example of a Conversational Pattern
Figure 8 contrasts the token-level conversational pattern of DuplexPO with that of the SFT baseline.
DuplexPO maintains and releases <BOS>/<EOS> impulses around user speech instead of remaining
near PAD, which is consistent with the attention statistics in Appendix D and the suppression metrics
defined in Appendix C.

L     Broader Impacts
This work improves the naturalness of full-duplex spoken dialogue models. Positively, this can
significantly enhance accessible interfaces and conversational assistants. Negatively, highly human-
like voice dynamics (e.g., natural backchanneling and interruption) could be misused for deceptive
practices like realistic vishing (voice phishing). Future deployments should consider appropriate
safeguards, such as watermarking or identity disclosure, to mitigate these risks.




                                                         24
                                        (a) SFT Baseline




     Probability


                                         (b) DuplexPO




     Probability



                                              Time (s)

Figure 8: Example token-level conversational pattern. Compared with the SFT baseline, DuplexPO
maintains and releases <BOS>/<EOS> impulses around user speech instead of staying near PAD.




                                              25

