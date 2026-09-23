# ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue
Source: https://arxiv.org/abs/2609.17360
Kind: pdf
Fetched: 2026-09-22T09:31:21.193607+00:00
Tool: pdftotext

                                                     ECHO: A MATCHED-CONTRAST BENCHMARK FOR CONTEXT-SENSITIVE
                                                                TURN-TAKING IN FULL-DUPLEX DIALOGUE

                                                          Shuofeng Zhao∗ , Hongwei Cai† , Wenke Fan, Qingxiang Guo,Dawei Yang,
                                                   Zhou Wang, Zhiyang Zhou, Yingxin Shang, Weixu Wang, Lin Yang, Shuran Zhou, Yang Song

                                                                                Zuoyebang Education Technology, Beijing, China


                                                                       ABSTRACT                                      semantic evidence for turn management [8, 9, 10, 11], alongside




arXiv:2609.17360v1 [cs.CL] 15 Sep 2026
                                                                                                                     end-to-end full-duplex architectures [12, 13, 14] and dedicated in-
                                         Full-duplex spoken dialogue systems must distinguish interruptions
                                                                                                                     teraction corpora [15].
                                         that require yielding the floor from backchannels that permit con-
                                                                                                                          These benchmarks measure independently occurring events
                                         tinued speaking. Existing benchmarks typically evaluate events
                                                                                                                     drawn from natural conversation (e.g., [16]) or scenario scripts,
                                         independently and may therefore reward fixed action preferences
                                                                                                                     so the inserted utterance and its preceding dialogue vary together.
                                         rather than context-sensitive decisions. We introduce ECHO, a
                                                                                                                     They also sample non-interruptive feedback narrowly, leaving that
                                         paired diagnostic benchmark for Chinese full-duplex turn-taking.
                                                                                                                     class lexically closed (Table 2). In SID-Bench [7], 81.8% of non-
                                         ECHO pairs examples with the same overlap transcript but con-
                                                                                                                     interruptive instances consist entirely of the fifteen most frequent
                                         trasting preceding multi-turn dialogue contexts, with one requiring
                                                                                                                     characters; in the Easy Turn [17] test set the backchannel and turn-
                                         Y IELD and the other K EEP. It additionally includes off-talk ex-
                                                                                                                     taking vocabularies are disjoint, so the two classes are distinguish-
                                         amples for diagnosing unnecessary yielding. We introduce pair
                                                                                                                     able by vocabulary membership alone. Such items are separable
                                         accuracy, which requires correct decisions on both members of a
                                                                                                                     by lexical form alone and leave untested whether a system recovers
                                         pair and assigns no credit to constant-action policies. Experiments
                                                                                                                     non-floor-claiming intent from dialogue context. Substantive feed-
                                         on multiple full-duplex systems show that most exhibit a pronounced
                                                                                                                     back of this kind is less frequent than canonical tokens, but it is
                                         bias toward Y IELD, performing substantially better on interruptions
                                                                                                                     exactly where context is indispensable. The utterance “This pen has
                                         than on backchannels, while another system remains comparatively
                                                                                                                     run out of ink again” is an affiliative completion when the assistant
                                         balanced. These findings demonstrate that interruption-only evalua-
                                                                                                                     is already complaining about the pen, but a genuine interruption
                                         tion can overestimate practical turn-taking reliability. ECHO and its
                                                                                                                     when a faulty pen blocks a form the user was asked to fill in (Fig. 1),
                                         metadata will be publicly released.
                                                                                                                     so lexical content alone does not determine the correct action. This
                                             Index Terms— full-duplex spoken dialogue, turn taking, inter-           raises our central question: can a full-duplex system produce the
                                         ruption detection, overlapping speech, diagnostic evaluation                correct action across context-rewritten instances that share exactly
                                                                                                                     the same insertion text?
                                                                    1. INTRODUCTION                                       We introduce ECHO (Evaluating Context-conditioned Handling
                                                                                                                     of Overlaps), a paired evaluation set of Chinese multi-turn dialogues
                                         Full-duplex spoken dialogue systems are expected to listen while            in which the inserted utterance is held lexically fixed while the pre-
                                         speaking and to yield when a user claims the conversational floor.          ceding dialogue is rewritten to change its interactional role. Be-
                                         Overlapping speech, however, does not by itself constitute an in-           cause a system with a constant action preference scores well on any
                                         terruption: users also produce acknowledgments and affective feed-          interruption-only test, we pair this design with metrics that require
                                         back that invite the assistant to continue, as well as speech directed at   joint correctness across both members of a linked pair. Evaluating
                                         themselves or at a third party. Treating every overlap as an interrup-      four speech systems and a text-conditioned semantic reference, we
                                         tion yields fragmented, oversensitive interactions, whereas ignoring        find that moderate interruption accuracy does not translate into re-
                                         genuine floor-claiming speech leaves users unable to correct or redi-       liable turn taking: three of the four speech systems respond to a
                                         rect the system. Reliable full-duplex interaction therefore hinges on       substantial share of interruptions yet yield to most backchannels, an
                                         deciding whether overlapping speech warrants a Y IELD or a K EEP,           action-level Yield bias that interruption accuracy alone conceals and
                                         not on detecting that speech occurred.                                      that limited context access does not explain.
                                              Recent benchmarks have advanced this evaluation considerably.
                                         Full-Duplex-Bench and its extensions cover interruption handling,
                                                                                                                                 2. ECHO DATASET CONSTRUCTION
                                         backchannels, pauses, non-target speech, and multi-turn interac-
                                         tion quality [1, 2, 3]; the ICASSP 2026 HumDial Challenge tests
                                                                                                                     ECHO follows an insertion-text-matched contrastive design inspired
                                         acceptance of genuine interruptions against non-interruptive feed-
                                                                                                                     by minimal-pair testing, a strategy also used to probe whether audio
                                         back [4]; TurnBench examines false interruptions across conver-
                                                                                                                     language models genuinely attend to the acoustic evidence they are
                                         sation types [5]; and recent work targets robustness to third-party
                                                                                                                     given [18].
                                         speech [6] and semantic-aware interruption detection on real dia-
                                         logues [7]. In parallel, semantic VAD, streaming state prediction,
                                         and context-aware dialogue management combine acoustic and                  2.1. Interaction Roles and System Actions
                                            ∗ Equal contribution.                                                    ECHO defines three interaction roles by intended addressee and tar-
                                            † Equal contribution.                                                    get floor action. An interruption is directed to the assistant and
                                                                          context; we do not force every insertion to realize all three roles.
                                                                               Given a selected insertion, Claude-3.5-Sonnet [21] rewrites the
                                                                          dialogue history up to and including the assistant utterance being
                                                                          overlapped while keeping the insertion text unchanged, under a
                                                                          prompt that enforces the role definitions of Sec. 2.1. Writing ui for
                                                                                                                          (a)       (b)
                                                                          the insertion shared by two context variants ci and ci , the con-
                                                                                           (a)       (b)            (a)     (b)
                                                                          trast satisfies ui = ui = ui with yi ̸= yi , and each linked
                                                                                                           (k)     (k)
                                                                          instance is represented as (ci , ui , yi ). A group may contain
                                                                          two or all three role variants. The equality constraint applies to the
                                                                          insertion text, not to its synthesized waveform.
                                                                               Candidates are then screened by DeepSeek-V4-Pro for consis-
                                                                          tency between the rewritten history, the target insertion, and the re-
                                                                          quested role, followed by a manual consistency review over all can-
                                                                          didates. Examples whose history and insertion are incompatible with
                                                                          the requested label are discarded. Human evaluation on the retained
                                                                          instances achieves 97.45% accuracy, confirming that the rewritten
                                                                          contexts successfully induce the intended interactional roles.

                                                                          2.3. Speech Synthesis and Overlap Rendering
                                                                          All dialogue turns are independently synthesized with IndexTTS2
                                                                          [22] and rendered as speaker-separated dual-channel audio. We ap-
                                                                          ply the same synthesis and post-processing pipeline to all examples,
                                                                          including speaker-prompt RMS normalization, bounded speaking-
                                                                          rate normalization, forced-alignment-based overlap placement, and
                                                                          role-dependent overlap rendering.
                                                                               Within each linked group, the insertion text, emotion condition,
                                                                          and TTS inference configuration are held fixed, while the preceding
Fig. 1. One insertion, three required actions. All three ECHO             multi-turn context and the intended interaction role are changed. The
branches share the same user insertion transcript, glossed “This pen      role determines the rendered interaction: backchannel and off-talk
has run out of ink again”. In each branch, the insertion is placed        speech is overlaid without modifying the assistant track, whereas an
at the annotated overlap position located by forced alignment, while      interruption receives onset emphasis and causes the assistant track
the preceding multi-turn dialogue context is rewritten. The rewrite       to fade to silence after a short reaction interval. Speaker-reference
changes the interactional role from backchannel to interruption to        audio may differ across paired instances, and all utterances are syn-
off-talk, and with it the target action from K EEP to Y IELD to K EEP.    thesized independently; paired insertions are therefore controlled
Lexical form is therefore uninformative, and a system must decide         in lexical and selected synthesis conditions, but are not waveform-
before the assistant track terminates.                                    identical or fully acoustically matched. The faded assistant wave-
                                                                          form is excluded from evaluated model inputs, so post-decision floor
                                                                          release cannot serve as a label cue.
introduces a request, correction, task obstacle, condition change, or
control instruction that requires immediate handling, so its target ac-   2.4. Dataset Organization and Scope
tion is Y IELD. A backchannel is also assistant-directed but does
not claim the floor; we use the term broadly for acknowledgments,         ECHO distinguishes three metadata units: a sample id identifies
affective feedback, affiliative responses, and brief collaborative com-   one instance with a specific context, waveform, and role label; a
pletions, and its target action is K EEP. Off-talk is generated with an   group id links instances sharing the same insertion text and gen-
intended self- or third-party-directed role and is likewise assigned      eration source; and a pair id identifies a two-role contrast derived
K EEP; the stage directions used during generation are never exposed      from a group.
to the evaluated models. We retain the original three-way labels               The release contains 266 groups, 549 unique audio instances,
alongside the binary action labels because the two K EEP roles dif-       and 300 pair relations, distributed over two-role and three-role
fer downstream: off-talk should generally not be committed to the         groups as reported in Table 1. The three roles are balanced at the
dialogue state as a system-directed user turn.                            instance level (183 each), and pair relations are balanced by con-
                                                                          struction with 100 pairs for each of the interruption–backchannel,
2.2. Context-Rewritten Contrast Generation                                interruption–off-talk, and backchannel–off-talk contrasts. We re-
                                                                          lease the audio, model-observable dialogue text, original scenario
We first randomly sample Chinese multi-turn dialogue skele-               labels, binary action labels, event timestamps, and group/pair meta-
tons from the synthesized dialogue data constructed in Duplex-            data.
Drama [19], which covers diverse interlocutor relationships, loca-             Non-interruptive feedback in prior test sets is separable by lex-
tions, everyday tasks, and conversational situations. DeepSeek-           ical form alone, and ECHO removes that shortcut by construction.
V4-Pro [20] then selects candidate overlap positions and generates        All 100 interruption–backchannel pairs carry identical insertion text,
initial backchannel or off-talk insertions according to the dialogue      each of the 183 backchannel instances is lexically unique, none is
state and character roles. We retain only insertions that can plausibly   built only from the fifteen most frequent characters, and the three
receive an alternative interactional interpretation under a rewritten     roles have matched length distributions (6.3, 6.2, and 6.6 characters
                                                                                                                     is end-to-end multimodal; we force-aligned the final assistant utter-
Table 1. ECHO dataset statistics. Groups, unique samples, and                                                        ance and teacher-forced its text up to the target event while stream-
pair relations are counted separately so that three-role groups are not                                              ing the user audio. We assessed whether the model correctly stopped
counted multiple times at the instance level. Each of the 17 three-                                                  for an interruption and continued speaking for a backchannel or off-
role groups induces all three pair contrasts.                                                                        talk event. Gemini-3.1-Pro-Preview [23] predicts one of the three
 Group type                                        Groups           Unique samples            Pair relations         ECHO roles from text alone. It receives no audio, stage directions,
 Interruption–Backchannel only                             83                        166                     83      unspoken assistant content, or post-event reference responses, and
 Interruption–Off-talk only                                83                        166                     83      serves as a semantic reference rather than a modality-matched base-
 Backchannel–Off-talk only                                 83                        166                     83
                                                                                                                     line or an upper bound.
 Three-role groups                                         17                         51                     51
 Total                                                   266                         549                   300
                                                                                                                     3.2. Action Alignment and Metrics
                                                                                                                     We map interruption to Y IELD and backchannel and off-talk to
         Table 2. Lexical closure of non-interruptive feedback.                                                      K EEP (Sec. 2.1), over all unique instances. For speech models with-
          Set                            Inst.        Char. voc.            Top-15-char only                         out an explicit off-talk state, an off-talk instance counts as correct
                                                                                                                     whenever the system continues its current turn, so no fine-grained
          SID-Bench (zh)                  494                    124                            81.8                 off-talk recognition is required. Gemini’s three-way predictions are
          Easy Turn                       100                     67                            26.0
          ECHO (ours)                     183                    400                             0.0                 mapped to the same binary space before action metrics are com-
                                                                                                                     puted; predicting off-talk for a backchannel is therefore wrong in
                                                                                                                     the three-way analysis but right in the binary one. We additionally
                                                                                                                     evaluate Gemini in the original three-way role space to test whether
Table 3. Native input interfaces and event-level decision rules. The                                                 the intended roles can be recovered from explicit textual context.
amount and representation of dialogue context differ across systems;                                                      We report action accuracy over unique samples, separately for
assistant-side context is provided only where supported by the cor-                                                  each original label: AccI is the correct Y IELD rate on interruptions,
responding interface.                                                                                                and AccB and AccO the correct K EEP rates on backchannel and off-
 Model           User-side input                  Assistant-side text                Decision rule
 Easy Turn       Target insertion                 None                               Native state during insertion
                                                                                                                     talk. Macro accuracy averages the three, and each unique sample is
 SoulX-Duplug
 Lychee-FD
                 Last 2 user turns + insertion
                 Up to 5 user turns + insertion
                                                  None
                                                  History + planned utterance
                                                                                     Hit over insertion + 1 s
                                                                                     Stop event during insertion
                                                                                                                     counted once even when it belongs to a three-role group.
 MiniCPM-o 4.5   Full history + insertion         Teacher-forced planned utterance   Stop event during insertion          Sample-level accuracy can overstate reliability when a model
 Gemini          Insertion transcript             History + spoken prefix only       Prompted three-way prediction
                                                                                                                     prefers one action, so we define Pairwise Action Success Rate
                                                                                                                     (PASR) over the linked pairs whose target actions differ, Pflip =
                                                                                                                     PI-B ∪ PI-O :
on average), so the insertion text carries no discriminative informa-
tion within a pair (Table 2).                                                                                                              1       X
                                                                                                                              PASR =                       ⊮[âp = ap ∧ âq = aq ].     (1)
                                                                                                                                        |Pflip |
                                                                                                                                               (p,q)∈Pflip
                                     3. EXPERIMENTS
                                                                                                                     By Eq. (1) a pair succeeds only if the model yields to the interruption
3.1. Evaluated Systems and Native Interfaces                                                                         member and keeps the floor for the other, so PASR penalizes both
                                                                                                                     constant-Y IELD and constant-K EEP strategies. Backchannel–off-
We evaluate four speech systems and one text-only language model                                                     talk pairs share the target action K EEP and are instead summarized
as a semantic reference (Table 3). Each system is evaluated through                                                  by Pairwise Keep Consistency (PKC), the fraction of such pairs on
its supported interface, resulting in different amounts and represen-                                                which the system keeps the floor for both members. PASR and PKC
tations of dialogue context. Easy Turn receives only the target in-                                                  are complementary: a constant-K EEP policy maximizes PKC but
sertion, while SoulX-Duplug receives the two preceding user turns                                                    scores zero on PASR, so a system must do well on both to be non-
and the insertion. Lychee-FD receives five preceding user-side turns                                                 degenerate. For the three-way evaluation we report Pairwise Role
and the insertion, together with the assistant dialogue history and the                                              Success Rate (PRSR), which applies the same joint-correctness cri-
complete planned utterance. MiniCPM-o 4.5 receives the full user-                                                    terion to the original role labels and therefore covers all three pair
side history and insertion while the planned assistant utterance is                                                  types.
teacher-forced during streaming. Gemini receives the dialogue his-
tory and insertion in text form, but only the already-spoken prefix                                                  3.3. Results and Analysis
of the current assistant utterance. Gemini therefore serves as a text-
only semantic reference, rather than a modality-matched baseline or                                                  Finding 1: high interruption accuracy can coexist with severe
an upper bound. In particular, cross-model differences cannot iso-                                                   over-yielding on non-floor-claiming feedback. Easy Turn and
late the effects of context access, modality, model capacity, or native                                              SoulX-Duplug correctly yield on 98.91% and 91.26% of interrup-
decision interface.                                                                                                  tions, respectively, but keep the floor on only 1.09% and 6.56% of
     Easy Turn [17] is a modular turn-state predictor with four na-                                                  backchannels. Lychee-FD shows a similar imbalance, with 55.19%
tive outputs; we map complete and incomplete to Y IELD and                                                           interruption accuracy but only 12.02% backchannel Keep accuracy.
backchannel and offtalk to K EEP, since the first two indicate                                                       Consistent with these class-conditioned results, the interruption–
that the user is claiming the floor. Receiving only the insertion, it                                                backchannel PASR is 0.00% for Easy Turn and only 4.00% for
is a context-free local baseline. SoulX-Duplug [10] is a streaming                                                   both SoulX-Duplug and Lychee-FD. Over the balanced ECHO con-
state predictor on 160-ms chunks and Lychee-FD [13] a full-duplex                                                    struction, Easy Turn and SoulX-Duplug predict Y IELD on 99.09%
dialogue model with a dedicated control head at 400-ms resolution;                                                   and 89.80% of all instances, respectively. These results reveal a
Interruptions were correct if speech stopped, whereas backchannels                                                   strong Y IELD preference that would be obscured by reporting in-
and off-talk were correct if speech continued. MiniCPM-o 4.5 [14]                                                    terruption accuracy alone. The aggregate predicted-action rates
Table 4. Binary system-action evaluation on ECHO. Input interfaces are given in Table 3. All sample-level accuracies are computed over
unique instances. Gemini’s three-way predictions are mapped to Y IELD/K EEP before computing this table.
  Model                      Int. Yield       BC Keep         OT Keep†          Macro        Overall        PASRI−B           PASRI−O              PKCB−O
  Easy Turn                       98.91             1.09             0.55         33.52         33.52              0.00              0.00             1.00
  SoulX-Duplug                    91.26             6.56            15.30         37.71         37.71              4.00             12.00             2.00
  Lychee-FD                       55.19            12.02             8.20         25.14         25.14              4.00              6.00             0.00
  MiniCPM-o 4.5                   63.39            65.57            53.55         60.84         60.84             54.00             53.00            49.00
  Gemini reference                90.71            86.34            71.58         82.88         82.88             79.00             52.00            70.00
  Three-way role prediction (same reference, original role labels; PRSR in place of PASR/PKC)
  Gemini reference        90.71       85.25         71.04     82.33      82.33             66.00 (PRSR)
  † Keep rate on scenario-labeled off-talk, interpreted as a scenario-based action diagnostic rather than an unambiguous false-trigger estimate.




describe ECHO’s balanced diagnostic distribution and should not be                is therefore how floor decisions use available context, not how much
interpreted as estimates under naturally occurring event prevalence.              context is available. Reporting class-conditioned Keep rates along-
Finding 2: the bias is not explained by limited context. Lychee-                  side interruption accuracy is necessary for meaningful turn-taking
FD receives up to five preceding dialogue turns and the complete                  evaluation. We release the ECHO audio, observable dialogue text,
planned assistant utterance, and still keeps the floor on only 12.02%             labels, and pair metadata.
of backchannels and 8.20% of off-talk, with 4.00% PASRI−B .                       Limitations. ECHO is a paired diagnostic set rather than an es-
The text-conditioned reference, which observes the same dialogue                  timate of performance in naturally occurring dialogue: synthesis
but only the assistant prefix already spoken, reaches 86.34% on                   is what allows one insertion to recur across rewritten histories, at
backchannels. The low off-talk rate is consistent with the diffi-                 the cost of the ecological validity of real-speech benchmarks [7].
culty on incidental side-talk reported in the original Lychee-FD                  Furthermore, interruption waveforms receive label-dependent RMS
study [13]; the comparably low backchannel rate shows that over-                  scaling and onset emphasis. The design therefore controls insertion
yielding extends to system-directed feedback that does not claim                  text, emotion condition, and TTS inference configuration, but does
the floor. Among the speech systems, MiniCPM-o 4.5 is the only                    not fully isolate dialogue context from speaker-reference variation
balanced one (63.39%/65.57%, 54.00% PASRI−B ). Since the fail-                    or other acoustic factors. A waveform-reuse condition and a gain-
ing systems observe at least as much assistant-side context as the                free interruption ablation would be required for strict acoustic con-
reference that succeeds, the limiting factor is how floor decisions               trol. Off-talk is scenario-labeled and its intended addressee is not
use available context rather than how much context is available.                  always explicit, so we treat backchannel as the primary evidence for
Finding 3: pair-level metrics expose what sample-level accuracy                   Yield bias and off-talk as a supporting diagnostic. Finally, the evalu-
hides. Evaluated in the original three-way role space (Table 4, last              ated systems differ in modality, streaming latency, and native output
row), the text-conditioned reference reaches 82.33% macro accuracy                space, so the results are a behavioral audit under supported interfaces
but only 66.00% PRSR, so correct predictions on individual samples                rather than a modality-matched ranking.
do not imply consistent predictions across linked context variants.
The same gap appears in the binary space, where 82.88% overall
accuracy corresponds to 52.00% PASRI−O .                                          5. ACKNOWLEDGMENTS AND DISCLOSURE OF AI USE
     Label ambiguity affects all evaluated systems identically. The
                                                                                  Generative AI is used in this work in two capacities, both disclosed
text-conditioned reference recovers the intended role for 82.33% of
                                                                                  in accordance with IEEE policy. As construction tools, the models
instances from the same observable context, which bounds the share
                                                                                  named in Sec. 2 generate the ECHO material: dialogue skeletons,
of the observed gap that residual ambiguity can explain; the three
                                                                                  context rewrites, and synthesized audio; all retained items passed
systems exhibiting Yield bias reach at most 35.70% overall accuracy,
                                                                                  the human review of Sec. 2.2. In manuscript preparation, the authors
far below that bound.
                                                                                  used llm for language polishing and assisted drafting. No AI sys-
                                                                                  tem contributed to the experimental design, the reported results, or
                          4. CONCLUSION                                           the scientific claims, and the authors take full responsibility for the
                                                                                  content of this publication.
We presented ECHO, a paired diagnostic set for Chinese full-duplex
turn taking that holds the inserted utterance lexically fixed while
                                                                                                             6. REFERENCES
rewriting the preceding dialogue, together with pair-level metrics
that require correct actions on both members of a linked pair. Under
                                                                                   [1] Guan-Ting Lin et al., “Full-Duplex-Bench: A Benchmark to
this protocol, three of the four evaluated speech systems show a pro-
                                                                                       Evaluate Full-Duplex Spoken Dialogue Models on Turn-taking
nounced action-level Yield bias that single-number interruption ac-
                                                                                       Capabilities,” in 2025 IEEE Automatic Speech Recognition and
curacy conceals. Limited context does not explain the bias: Lychee-
                                                                                       Understanding Workshop (ASRU), 2025, pp. 1–8.
FD observes up to five preceding dialogue turns and the complete
planned assistant utterance but maintains the floor on only 12.02% of              [2] Guan-Ting Lin, Shih-Yun Shan Kuan, Qirui Wang, Jiachen
backchannels, whereas a text-conditioned reference that sees strictly                  Lian, Tingle Li, and Hung-yi Lee, “Full-Duplex-Bench v1.5:
less assistant-side information reaches 86.34%. The limiting factor                    Evaluating Overlap Handling for Full-Duplex Speech Models,”
     in IEEE International Conference on Acoustics, Speech and      [17] Guojian Li et al., “Easy Turn: Integrating Acoustic and Lin-
     Signal Processing (ICASSP), 2026.                                   guistic Modalities for Robust Turn-Taking in Full-Duplex Spo-
                                                                         ken Dialogue Systems,” 2025.
 [3] Guan-Ting Lin et al., “Full-Duplex-Bench-v2: A Multi-Turn
     Evaluation Framework for Duplex Dialogue Systems with an       [18] Jiaqi Xiong et al., “DEAF: A Benchmark for Diagnostic Eval-
     Automated Examiner,” 2026.                                          uation of Acoustic Faithfulness in Audio Language Models,”
                                                                         ArXiv, vol. abs/2603.18048, 2026.
 [4] Chengyou Wang et al., “Full-Duplex Interaction in Spoken
     Dialogue Systems: A Comprehensive Study from the ICASSP        [19] Qingxiang Guo, Wenke Fan, Shuofeng Zhao, Dawei Yang,
     2026 HumDial Challenge,” in IEEE International Conference           Zhiyang Zhou, Yingxin Shang, Hongwei Cai, Zhou Wang,
     on Acoustics, Speech and Signal Processing (ICASSP), 2026,          Weixu Wang, Lin Yang, Shuran Zhou, and Yang Song, “Du-
     arXiv:2604.21406.                                                   plexdrama: A synthesized dialogue dataset with scenarios,
                                                                         full-duplex behaviors, expressive speech, and sound events,”
 [5] Freeman Jiang et al., “TurnBench: A Multi-Domain Bench-             2026.
     mark for Turn-Taking Dynamics in Spoken Dialogue,” 2026.
                                                                    [20] DeepSeek-AI, “DeepSeek-V4: Towards Highly Efficient
 [6] Dongwook Lee, Eunwoo Song, Che Hyun Lee, Heeseung                   Million-Token Context Intelligence,” 2026.
     Kim, and Sungroh Yoon, “Still Between Us? Evaluating
     and Improving Voice Assistant Robustness to Third-Party In-    [21] Anthropic, “Model Card Addendum: Claude 3.5 Haiku and
     terruptions,” in Proceedings of the 64th Annual Meeting of          Upgraded Claude 3.5 Sonnet,” Tech. Rep., Anthropic, October
     the Association for Computational Linguistics (ACL), 2026,          2024.
     arXiv:2604.17358.                                              [22] Siyi Zhou et al., “IndexTTS2: A Breakthrough in Emo-
 [7] Bingshen Mu, Jin Xu, Kangxiang Xia, et al., “Semantic-Aware         tionally Expressive and Duration-Controlled Auto-Regressive
     Interruption Detection in Spoken Dialogue Systems: Bench-           Zero-Shot Text-to-Speech,” 2025.
     mark, Metric, and Model,” in Proceedings of the IEEE Inter-    [23] Google DeepMind, “Gemini 3.1 Pro Model Card,” Tech. Rep.,
     national Conference on Multimedia and Expo (ICME), 2026,            Google DeepMind, February 2026.
     arXiv:2603.24144.
 [8] Chengyou Wang et al., “FastTurn: Unifying Acoustic and
     Streaming Semantic Cues for Low-Latency and Robust Turn
     Detection,” ArXiv, vol. abs/2604.01897, 2026.
 [9] Weijie Wu et al., “Phoenix-VAD: Streaming Semantic End-
     point Detection for Full-Duplex Speech Interaction,” ArXiv,
     vol. abs/2509.20410, 2025.
[10] Ruiqi Yan et al., “SoulX-Duplug: Plug-and-Play Stream-
     ing State Prediction Module for Realtime Full-Duplex Speech
     Conversation,” 2026.
[11] Hao Zhang, Weiwei Li, Rilin Chen, Vinay Kothapally, Meng
     Yu, and Dong Yu, “LLM-Enhanced Dialogue Management
     for Full-Duplex Spoken Dialogue Systems,” ArXiv, vol.
     abs/2502.14145, 2025.
[12] Wenyi Yu et al., “SALMONN-omni: A Standalone Speech
     LLM without Codec Injection for Full-duplex Conversation,”
     2025.
[13] Zhenyu Liu et al., “Hierarchical Acoustic-Semantic Modeling:
     Modality Separation and Semantic Coherence for Full-Duplex
     SLMs,” 2026.
[14] Junbo Cui et al., “MiniCPM-o 4.5: Towards Real-Time Full-
     Duplex Omni-Modal Interaction,” ArXiv, vol. abs/2604.27393,
     2026.
[15] Yifu Chen, Shengpeng Ji, Ziqing Wang, Hanting Wang, and
     Zhou Zhao, “InteractSpeech: A Speech Dialogue Interaction
     Corpus for Spoken Dialogue Model,” in Findings of the Asso-
     ciation for Computational Linguistics: EMNLP 2025, Suzhou,
     China, 2025, pp. 8024–8033, Association for Computational
     Linguistics.
[16] Christopher Cieri, David Miller, and Kevin Walker, “The
     Fisher Corpus: A Resource for the Next Generations of
     Speech-to-Text,” in Proceedings of the Fourth International
     Conference on Language Resources and Evaluation (LREC),
     2004.

