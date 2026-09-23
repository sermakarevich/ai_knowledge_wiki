# StepAudio 3 Realtime Technical Report
Source: https://arxiv.org/abs/2609.14005
Kind: pdf
Fetched: 2026-09-22T09:29:43.175971+00:00
Tool: pdftotext

                                                                              StepAudio 3 Realtime Technical Report

                                                                                                                    StepFun-Audio Team

                                                                                                                                    Project Page

                                                                                                                                     Abstract
                                                     Realtime spoken interaction demands deep reasoning, prompt responses, and ﬂuid




arXiv:2609.14005v2 [cs.SD] 19 Sep 2026
                                                     turn-taking. We present StepAudio 3 Realtime, an audio-language foundation
                                                     model organized around a continuous listen-converse-think-act loop. Deep Percep-
                                                     tion captures rich acoustic cues to interpret user intent, while Seamless Duplex mod-
                                                     els synchronized audio streams to handle pauses, backchannels, and interruptions
                                                     naturally. Crucially, we resolve the tension between deep deliberation and latency
                                                     via Think-While-Speaking, executing private reasoning in parallel with spoken de-
                                                     livery. In reasoning mode, StepAudio 3 reaches a 73.0 macro average on StepAu-
                                                     dioChat. With Think-While-Speaking, it achieves dialogue and reasoning perfor-
                                                     mance comparable to dedicated reasoning models while speaking in real time. Fur-
                                                     thermore, an integrated Voice Agent handles asynchronous tool execution without
                                                     disrupting the dialogue ﬂow. StepAudio 3 Realtime achieves top-tier performance
                                                     across key dimensions: an exceptional 90.6 on the MMSU benchmark, 98.9 Overall
                                                     on the Artiﬁcial Analysis Full-Duplex Bench, and a 56.0% macro task-success rate
                                                     on τ -Voice.
                                                    StepAudio 3 Realtime
                                                 Audio Understanding                                                                                                                                                  Score (%) · Higher is better ↑

                                                   AudioMultiChallenge                                         MMSU                                                  MMAR
                                                        StepAudio 3 Realtime                            49.3     StepAudio 3 Realtime                        90.6      StepAudio 3 Realtime                                                   86.5
                                                        Doubao 2.0 Lite                                 48.5     Doubao 2.0 Lite                             80.0      Doubao 2.0 Lite                                                        75.9
                                                        Gemini 3 Flash                                  56.6     Gemini 3 Flash                              77.0      Gemini 3 Flash                                                         75.4
                                                        Gemini 3.1 Pro                                  67.0     Gemini 3.1 Pro                              83.6      Gemini 3.1 Pro                                                         81.7
                                                                               0                  100                                    65             95                                     65                                       90



                                                 Interactive Intelligence                                                                                                                                             Score (%) · Higher is better ↑

                                                   StepAudioChat                                    Dialogue   AA Full-Duplex Bench                    Full Duplex   τ-Voice                                                                 Agentic

                                                        StepAudio 3 Realtime (Interactive)*             70.4     StepAudio 3 Realtime                        98.9      StepAudio 3 Realtime                                                   56.0
                                                        Doubao 2.0 Lite (Reasoning)                     70.5     GPT-realtime-2 (High)                       95.3      Grok Voice Think Fast 2.0 High                                         56.5
                                                        DeepSeek-V4-Flash (Reasoning)                   71.4     Qwen Audio 3.0 Realtime Plus                98.4      Qwen Audio 3.0 Realtime Plus                                           54.6
                                                        Kimi K3 (Reasoning)                             77.1     Grok Voice Think Fast 2.0 high              95.1      GPT-Realtime-2.1 High                                                  45.7
                                                                                              0   100                                             90   100                                              0                              100


                                                 * Realtime mode test.


                                                 General Text                                                                                                                                                         Score (%) · Higher is better ↑

                                                   HMMT 2026 Feb                                               GPQA Diamond                                          MultiChallenge
                                                        StepAudio 3 Realtime                            86.8     StepAudio 3 Realtime                        83.0      StepAudio 3 Realtime                                                   59.7
                                                        Doubao 2.0 Lite                                 73.9     Doubao 2.0 Lite                             82.4      Doubao 2.0 Lite                                                        60.8
                                                        Gemini 3 Flash                                  85.9     Gemini 3 Flash                              90.3      Gemini 3 Flash                                                         68.1
                                                                               60                  90                                    0             100                                     0                                       100




                                                    StepAudio 3 ASR Max                                                                                                                                     ASR · Error rate (%) · Lower is better ↓


                                                   LibriSpeech clean                                           WenetSpeech meeting                                   AISHELL-1
                                                        StepAudio 3 ASR Max                             1.18     StepAudio 3 ASR Max                         4.35      StepAudio 3 ASR Max                                                    0.49
                                                        Doubao 2.0 ASR                                  2.94     Doubao 2.0 ASR                              5.09      Doubao 2.0 ASR                                                         2.07
                                                        Seed 2.0 Lite                                   1.47     Seed 2.0 Lite                               4.80      Seed 2.0 Lite                                                          1.66
                                                        HY3.0 ASR Preview                               1.38     HY3.0 ASR Preview                           4.12      HY3.0 ASR Preview                                                      1.22
                                                                               0                    4                                    0               6                                     0                                         6




                                         Figure 1: Benchmark results for StepAudio 3 ASR Max and StepAudio 3 Realtime (blue), compared with baselines (gray). Lower
                                         is better for ASR error rates, and higher is better elsewhere. Dialogue averages eight dimensions, full duplex reports Overall, and
                                         τ -Voice averages three domains. See Tables 1 and 10.
                                                                                  StepFun-Audio Team



1 Introduction

Natural spoken interaction requires a system to follow the user while managing its own response.
A pause may occur before a request is complete, and an utterance during model speech may be
an acknowledgment or a substantive interruption. Complex requests introduce another challenge:
the model must reason carefully while keeping the conversation responsive. Tool use extends this
challenge because an external task may outlast the spoken exchange that initiated it.
Advances in speech recognition have combined acoustic representations with the linguistic knowl-
edge of large language models [1–3]. Audio-language models now support broader acoustic un-
derstanding and direct speech generation [4–8]. Streaming and full-duplex systems further allow
listening and speaking to overlap [9–12]. Together, these capabilities allow responses to account
for linguistic content, vocal delivery, and conversational timing.
StepAudio 3 Realtime builds on the Step-Audio series’ shared audio-language foundation [13–16].
Its focus is the coordination of perception, reasoning, and action as a conversation unfolds. We
organize these functions as a listen, converse, think, and act loop. Deep Perception captures lin-
guistic and nonverbal acoustic evidence. Seamless Duplex uses user and model speech to manage
the conversational ﬂoor. Think-While-Speaking [17] coordinates reasoning with spoken delivery,
supported by Adaptive Thinking and multi-token prediction. A streaming Voice Agent carries con-
versational intent into tool execution and incorporates the results into subsequent dialogue. These
functions operate concurrently as needed, with new user input shaping the ongoing interaction.
Figure 1 summarizes ASR results for StepAudio 3 ASR Max and the capability evaluations of
StepAudio 3 Realtime. The realtime model leads the reported baselines on four of eight audio-
understanding benchmarks and achieves the highest reported Overall score on the Artiﬁcial Analy-
sis Full-Duplex Bench. The results also identify remaining gaps in multi-turn constraint following
and retail tool-use tasks. Section 8 presents the protocols and domain-level analysis.


2 Realtime Conversational Loop

StepAudio 3 Realtime coordinates listening, speaking, reasoning, and action through an evolving
conversational context. User speech, model speech, and tool results can arrive while other parts of
the interaction remain in progress. Figure 2 gives an overview of these coupled functions.

2.1 Shared Conversational Context

The conversational context includes acoustic and linguistic evidence, dialogue history, the current
speaking turn, reasoning progress, and tool-execution status. Perception retains cues about what
the user says and how it is said. Model-side speech provides additional context for interpreting
user utterances that overlap with a response.
This context informs whether to continue listening or speaking, whether to reason further, and
whether a request is ready for external action. Newly observed speech and returned tool results can
change these decisions as the conversation proceeds.




                                                 2
                                                                                                                    StepFun-Audio Team




        Realtime Conversational Loop



                                    DEEP PERCEPTION
                                    ASR · AUDIO UNDERSTANDING                              SEAMLESS DUPLEX
                                                                                           LISTEN · SPEAK · YIELD
           USER STREAM




 LEXICAL · EMOTION · ACOUSTIC CONTEXT                                                                               STREAMING SPEECH
                                                                      STEP-AUDIO 3
                                                                       Realtime
          MODEL STREAM                                              CONVERSATIONAL STATE




    SPEECH · OVERLAP · TURN STATE


                                                                                               THINK WHILE SPEAKING
                                                                                               ADAPTIVE THINKING
                                     STREAMING ACTION                                          MEDUSA MTP
                                     INTENT · TOOL CALL· FEEDBACK




Figure 2: Conversational loop of StepAudio 3 Realtime. User and model speech inform perception and ﬂoor management. Rea-
soning supports spoken responses and tool use, while returned tool results update the context for subsequent interaction.

2.2 Coordinating Speech, Reasoning, and Action

Conversational timing and reasoning progress need not advance at the same pace. Seamless Duplex
handles pauses, user backchannels, and substantive interruptions. Think-While-Speaking allows
spoken delivery to begin before the full reasoning trace is complete. Adaptive Thinking selects
when explicit reasoning is useful, and MTP accelerates private reasoning. Sections 5 and 6.3
describe these capabilities.
The Voice Agent extends the interaction to tasks that require tools. It resolves the request and
required arguments before execution, then incorporates returned evidence into the conversation.
The user can continue speaking while a task is in progress. This coordination lets external work
proceed alongside dialogue, as described in Section 7.


3 Model Architecture and Foundation Training

3.1 System Architecture

StepAudio 3 Realtime uses a mixture-of-experts architecture. The audio frontend uses the Audio
Transformer (AuT) encoder from Qwen3-Omni [8]. An adapter maps the encoder outputs into the
representation space of the language model.
Figure 3 summarizes the system architecture. The full-duplex input path incorporates user and
model audio streams. Audio representations pass through the encoder and adapter to the LLM
decoder. Text tokens enter the decoder through a separate input path, allowing it to jointly condition
on acoustic information and textual context. The generator produces streaming model audio, which

                                                                            3
                                                                                                         StepFun-Audio Team



returns to the model audio stream for subsequent interaction. Section 5 describes conversational-
ﬂoor management.


                                                             Text

                                                                                 LLM decoder               Generator

         Full-duplex           Audio encoder               Adapter



                                                       User audio stream



                                                      Model audio stream




Figure 3: System architecture of StepAudio 3 Realtime. The LLM decoder receives audio representations through the audio
encoder and adapter, together with a separate text input. User and model audio form the two full-duplex streams, with generator
output returning to the model audio stream. Waveforms are schematic.

The speech generator produces incremental output with context-appropriate tone and rhythm. Nat-
ural delivery includes expressive cues such as pauses and hesitation, connecting the content of a
response with its communicative intent.

3.2 Three-Stage Pretraining

Data curation. Pretraining data are prepared through an automated large-scale audio curation
pipeline [16]. Raw audio is ﬁltered with sound event detection and voice activity detection, then
merged and resegmented into samples of suitable duration that preserve semantic completeness.
The pipeline assigns audio-level metadata such as quality, synthetic-speech likelihood, and speaker
count. It also uses multiple recognition systems for transcription and language identiﬁcation, cross-
checks their outputs, and grades samples by acoustic and semantic quality. These annotations
support quality-aware sampling across training stages. For StepAudio 3 Realtime, the pipeline
is extended to broaden language coverage and support the sustained perception and interaction
demands of realtime dialogue.
Training stages. Pretraining is organized into modality alignment, multimodal mixed training,
and cooldown stages. The modality-alignment stage establishes the interface between acoustic
representations and the language model. Multimodal mixed training then develops joint audio-text
modeling at scale. The cooldown stage places greater weight on high-quality data to reﬁne the
resulting foundation. Across the three stages, StepAudio 3 Realtime uses a ﬁxed sequence length
of 32K and processes 1.2T training tokens.
Pretraining mixture. The pretraining mixture increases the proportion of pure text to preserve
the general capabilities of the base language model and support subsequent reasoning and agent
training.




                                                              4
                                                                                 StepFun-Audio Team



3.3 Midtraining for Realtime Interaction

Context extension. Midtraining uses perception, synthetic conversational, and voice-agent data.
The context length is extended to 128K to accommodate longer dialogue histories, earlier user
requirements, and intermediate tool results.
Midtraining mixture. This stage substantially increases the share of audio-understanding and
agent-interaction data. The former broadens coverage of speech, music, environmental sound, and
audio-grounded reasoning, while the latter trains the model to carry user intent through planning,
tool use, and spoken follow-up. Sections 4.2 and 7 describe the corresponding data construction
and training procedures.


4 Deep Perception: Speech Recognition and Audio Understanding

Perception combines lexical understanding with cues about the speaker, vocal delivery, acoustic
events, and temporal structure. StepAudio 3 ASR Max is specialized for transcription, while
StepAudio 3 Realtime is trained for broader audio understanding and spoken interaction. We
describe the ASR specialization ﬁrst, followed by audio-understanding data construction and post-
training. Section 8 compares capabilities across benchmarks.

4.1 StepAudio 3 ASR Max

4.1.1   Training and Data Construction

StepAudio 3 ASR Max and StepAudio 3 Realtime share the same pretraining and midtraining
stages. They diverge only during supervised ﬁne-tuning, where the ASR branch is specialized for
transcription and the realtime branch is tuned for spoken interaction.
Supervised ﬁne-tuning. The ASR-specialized model is ﬁne-tuned with examples packed into se-
quences of up to 32K tokens. We apply time-frequency masking following the augmentation princi-
ple of SpecAugment [18], while keeping the audio encoder frozen and updating the audio-language
adapter and language decoder to produce normalized transcripts. For context-aware recognition, an
example may additionally provide dialogue history, a preceding model response, a scenario descrip-
tion, or task-speciﬁc terminology as optional evidence. The target transcript remains grounded in
the input waveform, allowing the model to use relevant context without simply copying unrelated
terms.
Short- and long-form ASR data. The ASR mixture combines short labeled utterances with long
pseudo-labeled recordings. Multiple recognition systems transcribe segmented audio, and their
hypotheses are aligned and fused with Recognizer Output Voting Error Reduction (ROVER) [19].
Agreement-based ﬁltering selects reliable segments for recomposition into longer sessions. LLM
then restores punctuation and improves consistency across each session.
Long-tail terminology augmentation. Rare names and technical terms are often confused with
common words that sound similar. We therefore build targeted synthetic training examples for
these cases. An LLM expands a knowledge taxonomy to identify categories rich in homophones,
uncommon characters, abbreviations, and product identiﬁers. We enumerate candidate terms, re-
move duplicates, and place the terms in natural carrier sentences. These sentences are converted


                                                5
                                                                                                            StepFun-Audio Team


Table 1: ASR evaluation on standard public benchmarks and ContextASR-Bench (lower is better). English subsets report WER and
Mandarin subsets report CER. Bold marks the best result in each row, and underlining marks the second-best result. ContextASR-
Bench results use the Contextless setting without external context injection.

       Test set                         StepAudio 3 ASR Max          Doubao 2.0 ASR   Seed 2.0 Lite   HY3.0 ASR Preview
       LibriSpeech test-clean                    1.18                     2.94             1.47                1.38
       LibriSpeech test-other                    2.28                     5.98             2.67                2.80
       AISHELL-1                                 0.49                     2.07             1.66                1.22
       WenetSpeech test-net                      3.99                     4.03             4.71                3.71
       WenetSpeech test-meeting                  4.35                     5.09             4.80                4.12
       ContextASR-Bench
         - ContextASR-Speech-EN                  7.91                    12.04             9.48                8.53
         - ContextASR-Dialogue-EN                3.43                    9.09              3.65                4.66
         - ContextASR-Speech-ZH                  1.43                    2.80              2.15                1.74
         - ContextASR-Dialogue-ZH                1.02                    10.47             4.15                1.63

to speech and retained only when their pronunciation is consistent with the target text.1 For acous-
tically confusable terms, selected examples may also include dialogue history or entity hints. This
teaches the model to use relevant context while avoiding unrelated lexical substitutions.

4.1.2      Evaluation

Benchmarks. We evaluate StepAudio 3 ASR Max on ﬁve standard public test sets: LibriSpeech
test-clean and test-other [21], AISHELL-1 [22], and WenetSpeech test-net and test-meeting [23].
English results use word error rate (WER), while Mandarin results use character error rate (CER).
To assess the linguistic knowledge targeted by our long-tail terminology augmentation, we ad-
ditionally use the publicly released ContextASR-Bench [24], which provides long-form, multi-
domain, entity-rich speech in English and Mandarin. We use its Contextless setting without do-
main labels, entity lists, or external hotword injection; English subsets are evaluated with WER
and Mandarin subsets with CER.
Results. Table 1 compares ASR performance across benchmark subsets. StepAudio 3 ASR
Max leads on all three standard benchmark families: it is best on both LibriSpeech subsets and
AISHELL-1, and it remains ahead of Doubao 2.0 ASR and Seed 2.0 Lite on both WenetSpeech
subsets while trailing HY3.0 ASR Preview only by a small margin. On ContextASR-Bench,
StepAudio 3 ASR Max is the best-performing model on all four subsets, covering both English
and Mandarin and both Speech and Dialogue settings. Its macro-average error rate is 5.67% on the
English subsets and 1.23% on the Mandarin subsets, compared with 6.60% and 1.69% for HY3.0
ASR Preview. This consistent lead indicates strong overall transcription accuracy on the bench-
mark’s long-form, multi-domain, entity-rich speech without external context injection. Note that
these results characterize the ASR-specialized model, not the transcription behavior of the realtime
model.

4.2 Audio Understanding

Data construction. A hierarchical taxonomy covers lexical content, paralinguistics, acoustic
events, speaker and temporal structure, music, and audio-grounded reasoning. Sampling con-
trols balance duration and language coverage while removing duplicates and unsuitable recordings.
Each recording is ﬁrst described and mapped to the capabilities supported by its content. These
   1
       For related model- and data-centric methods, including synthetic speech augmentation for code-switching ASR, see [20].


                                                                 6
                                                                                                                                            StepFun-Audio Team


Table 2: Audio-understanding results on eight benchmarks and their unweighted macro average. Scores use a 0–100 scale (higher
is better). Bold marks the best result in each row, and underlining marks the second-best result.

             Benchmark                        StepAudio 3 Realtime                Doubao 2.0 Lite              Gemini 3 Flash        Gemini 3.1 Pro
             Big Bench Audio                                98.1                           98.8                          99.4             99.6
             AudioMultiChallenge                            49.3                           48.5                          56.6             67.0
             MMSU                                           90.6                           80.0                          77.0             83.6
             MMAU                                           79.0                           77.5                          77.6             80.5
             WildSpeech                                     77.1                           73.9                          74.4             77.7
             MMAR                                           86.5                           75.9                          75.4             81.7
             Step-Caption                                   78.2                           76.8                          67.8             74.8
             MTalk-Bench                                    91.7                           89.9                          88.5             89.1
             Macro Average                                  81.3                           77.7                          77.1             81.8

annotations guide the construction of one or more clip-speciﬁc questions. Multiple models then in-
dependently label each audio–question pair, and their outputs are consolidated through agreement
and quality checks. Figure 4 summarizes the construction process.

                   Sampling controls                                              Self-defined sub-capability space
                   what audio is allowed in                                               what may be asked about it




               1                              2                             3                              4                          5



                       Sampling                    Description               Capability tagging           Query construction              Labelling
                duration and language             a caption of what              which aspects              one or more questions     the answers, grounded
                    quotas, dedup                  the clip contains            the clip supports            tailored to each clip         in the audio




                              Training example         the clip, the constructed questions, and their grounded answers




Figure 4: Construction pipeline for audio-understanding training examples. Sampling controls select suitable recordings. De-
scription and capability tagging identify what each clip contains and which aspects it supports. Query construction, multi-model
labeling, and agreement ﬁltering then produce candidate training examples.

Data selection and quality control. Deterministic checks ﬁrst remove empty, truncated, mal-
formed, or severely repetitive outputs. Text-only LLM judges then assess query and response qual-
ity and assign a case-value score. Case value jointly considers the query, the response, the amount
of useful information available in the audio as represented by its annotations, and the training value
of the question. These judges do not directly evaluate audio grounding. Instead, grounding reliabil-
ity is estimated from the consistency of responses independently produced by multiple models for
the same audio–question pair. Only candidates with high quality, high case value, and strong cross-
model consistency are retained as SFT candidates; broadly useful examples may enter midtraining,
while disagreements and correctable cases are routed to relabeling or further review.2
Evaluation. We evaluate the post-trained conversational model on eight audio-understanding
benchmarks covering audio-grounded reasoning, ﬁne-grained perception, nonverbal acoustic cues,
and multi-turn understanding. Results are reported in Table 2; the complete cross-capability com-
parison and evaluation protocols are provided in Section 8.
StepAudio 3 Realtime leads the reported baselines on four of the eight benchmarks, with its largest
margins on MMSU (90.6 versus 83.6) and MMAR (86.5 versus 81.7), gains of 7.0 and 4.8 points.
   2
       Related work examines modality-grounded evaluation and staged post-training in omni-modal models [25].


                                                                                    7
                                                                                                                                              StepFun-Audio Team



It also leads on Step-Caption and MTalk-Bench, and is close to Gemini 3.1 Pro on MMAU and
WildSpeech. In contrast, it trails Gemini 3.1 Pro by 17.7 points on AudioMultiChallenge, while
Big Bench Audio is nearly saturated for all systems. The results indicate broad strength in spoken-
language understanding, audio-grounded reasoning, and nonverbal acoustic perception, with main-
taining and revising constraints over natural multi-turn audio remaining a clear area for improve-
ment.
Less is more. We conduct a separate ablation in which the SFT data are the only changed factor,
comparing roughly two million randomly sampled examples with about 100K high-quality exam-
ples retained after quality control. The quality-controlled set improves MMSU from 78.78 to 89.70
and MMAR from 74.70 to 84.50. WildSpeech rises from 74.20 to 77.11, while the macro average
across the ambient, paralinguistic, and semantic subsets of MTalk-Bench increases from 88.83 to
90.84. Despite using roughly one twentieth as many examples, the quality-controlled data yield
consistent gains, highlighting the importance of data quality over raw SFT volume.


5 Seamless Duplex: Conversational Floor Management

A central challenge in full-duplex dialogue is determining when to take, retain, or yield the con-
versational ﬂoor. This requires distinguishing pauses within an unﬁnished utterance from turn
completion, and brief acknowledgments from attempts to interrupt. Resolving these ambiguities
relies on acoustic evidence interpreted in the context of the unfolding dialogue [10, 11, 26].
To support these decisions, StepAudio 3 Realtime integrates incoming user speech, ongoing model
speech, and dialogue history for context-aware conversational-ﬂoor management. Figure 5 illus-
trates the dual-stream architecture and the temporal interleaving of audio blocks with interaction-
state tokens.
                                                           Dual-Stream Full-Duplex Modeling
    A Dual-stream recurrent architecture                                                                                                  Step-Audio model
                                                                                                                                          streaming speech output

    Serialized S2T input                            Audio LLM and full-duplex interaction states

                                                                                                                                               user audio
                                                                                                                                               model audio
                                                                        Streaming                                                              state token
                                                                        audio encoder


    User audio stream

    Model audio stream

    B Time-interleaved audio and state tokens
    One state or text token follows every 320 ms audio block.
   0.00 s                                  0.32 s                                    0.64 s                              0.96 s                                     1.28 s

                                   listening:                                listening:                          listening:                                  speaking
      S     a   a     a     a   E no_voice S         a    a     a   a     E user_voice S      a   a   a   a   E user_voice S      a   a       a     a   E transition



Figure 5: Full-duplex interaction and temporal organization. (A) User speech, model-side speech, and dialogue history jointly
inform conversational-ﬂoor management. (B) Audio and interaction states are represented along a shared timeline.




                                                                                      8
                                                                                    StepFun-Audio Team



5.1 Streaming Interaction States

The system tracks its interaction state incrementally through the time-interleaved representation
illustrated in Figure 5. Audio is organized into 320 ms blocks, each followed by a state or text
token. Acoustic evidence and semantic context guide decisions to continue listening, initiate a
response, continue speaking, or yield the conversational ﬂoor. The model also uses its own ongoing
speech to interpret overlapping user utterances in the context of what the user is currently hearing.

5.2 Context-Aware Interaction Control

The conversational role of a user utterance depends on its relation to the ongoing dialogue [12].
For example, “right” may function as a backchannel acknowledging the model’s explanation or as
a preface to a correction. The system uses both audio streams and dialogue history to interpret
these context-dependent roles and guide ﬂoor-management decisions.

Pauses and turn endings. The system combines acoustic timing with semantic completeness
to distinguish within-turn pauses from turn endings. This distinction guides whether to continue
listening or initiate a response.

Backchannels and interruptions. During model speech, user backchannels are interpreted in
relation to the ongoing response. Brief acknowledgments can signal continued engagement without
requesting a ﬂoor transfer, whereas a substantive request or correction may signal an intent to
interrupt. The system uses this distinction to guide whether to continue speaking or yield to the
user.

Background speech rejection. Dialogue history provides contextual evidence for assessing
whether incoming speech is directed at the assistant. This assessment informs whether the speech
should be incorporated into the active exchange or treated as unrelated background conversation.

5.3 Training

Midtraining. Midtraining adapts the model to the time-interleaved representation used for full-
duplex interaction. This stage combines supervision for streaming ASR, voice activity detection
(VAD), and streaming prediction of utterance completeness. The training mixture includes over
10,000 hours of synthetic full-duplex interaction data. Text data are also incorporated to help
retain general language and reasoning capabilities.

Post-training. Post-training further reﬁnes conversational behavior using high-quality interac-
tion data covering turn taking, user backchannel handling, interruption handling, and background
speech rejection.

5.4 Evaluation

StepAudio 3 Realtime ranks ﬁrst in the Artiﬁcial Analysis (AA) full-duplex evaluation, achieving
an overall score of 98.9. This evaluation uses a subset of Full Duplex Bench v1 and v1.5 to assess
four aspects of conversational interaction: pause handling, turn taking, user interruption handling,
and backchannel handling.

                                                 9
                                                                                                                    StepFun-Audio Team


Table 3: Full-duplex interaction results on the Artiﬁcial Analysis subset of Full Duplex Bench v1 and v1.5. Scores use a 0–100
scale (higher is better). Bold marks the best result in each row, and underlining marks the second-best result.
 Capability                   StepAudio 3 Realtime   GPT-realtime-2 (High)   Qwen Audio 3.0 Realtime Plus   Grok Voice Think Fast 2.0 High
 Pause Handling                      98.9                    99.3                        98.0                            98.0
 Turn Taking                         100.0                   100.0                       98.0                            91.0
 User Interruption Handling          99.0                    95.0                        98.0                            97.0
 Backchannel Handling                98.0                    86.7                       100.0                            95.0
 Overall                              98.9                   95.3                        98.4                            95.1


As shown in Table 3, StepAudio 3 Realtime surpasses the strongest baseline, Qwen Audio 3.0
Realtime Plus, which scores 98.4 overall. Across individual categories, StepAudio 3 Realtime
achieves 100.0 on turn taking and 99.0 on user interruption handling, alongside scores of 98.9 on
pause handling and 98.0 on backchannel handling.
The category-level results highlight two complementary aspects of full-duplex interaction: respect-
ing within-turn pauses while responding at turn completion, and accommodating user interruptions
while continuing through backchannels. Strong performance across both pairs indicates balanced
conversational control over when to listen, speak, and yield.


6 Conversational Intelligence and Realtime Reasoning

Seamless Duplex determines when the model should respond. Conversational intelligence deter-
mines how it should engage with the user and how much reasoning the response requires. A natural
voice assistant should follow intent across turns, clarify underspeciﬁed goals, and move the con-
versation toward a useful outcome. Routine turns should avoid unnecessary deliberation, while
complex requests should retain the reasoning needed for a reliable answer.
StepAudio 3 Realtime combines dialogue and reasoning training with Think-While-Speaking,
which coordinates spoken responses with ongoing private reasoning. Adaptive Thinking controls
whether a turn uses explicit reasoning, and MTP acceleration reduces the decoding cost of that
reasoning.

6.1 StepAudioChat Benchmark

StepAudioChat is a closed, text-based benchmark for foundational conversational intelligence. It
evaluates dialogue behavior and the reasoning expressed through dialogue. Its scope isolates text-
level response quality from prosody, turn timing, interruption handling, and other properties of the
speech interface.3 The benchmark provides a common capability taxonomy and newly constructed
items to reduce reliance on public test questions.

6.1.1       Capability Taxonomy

We organize conversational abilities into a hierarchy whose leaves target observable behaviors
with deﬁned evaluation boundaries. Tasks and representative examples from public benchmarks
serve as a coverage check, without reusing their test questions. Overlapping mappings help reﬁne
capability deﬁnitions, while unmapped examples identify coverage gaps.
    3
        For complementary evaluation of emotional intelligence in multi-turn spoken dialogue, see Multi-Bench [27].




                                                                     10
                                                                                    StepFun-Audio Team



Within each capability family, we also vary factors such as the source of a constraint, its form of
expression, and its interaction with other conditions. This exposes combinations including nested
constraints and requirements that must remain consistent across turns. Each item targets a primary
capability. Only capabilities supported by validated items enter the evaluation suite.

6.1.2   Naturalistic Item Construction

Each item contains a dialogue prompt, independently checkable criteria, a valid reference response,
and a deliberately ﬂawed response. The paired responses provide positive and negative controls
for the judging criteria while allowing multiple valid phrasings.
De-identiﬁed utterances from real interactions inform prompt phrasing and local context, preserv-
ing brevity, fragmentation, colloquial wording, and transcription noise. Personal entities are re-
placed with typed placeholders. These utterances do not supply expected answers or grading cri-
teria. Except for intrinsically domain-speciﬁc capabilities, scenarios are recast across everyday
settings to broaden coverage beyond individual applications.

6.1.3   Quality Control and Difﬁculty Calibration

Structural validation checks that prompts are complete and self-contained. The valid response must
satisfy every judging criterion, and the ﬂawed response must violate at least one. A semantic audit
then checks the premise, reference response, and judging logic. Automated checks provide broad
coverage, with targeted human review of semantic failures and anomalous cases.
Difﬁculty is calibrated using responses from two reference systems with different capability levels.
Their observed successes and failures guide the mixture of baseline, discriminative, and difﬁcult
examples. The judge is calibrated separately using the valid and ﬂawed controls and a trusted
labeled sample. These checks help distinguish capability demands from ambiguous wording or
inconsistent grading.

6.2 Multi-Turn Dialogue Data

We train StepAudio 3 Realtime to follow user intent and constraints across turns, clarify under-
speciﬁed requests, and adapt responses to the conversational context. Joint training on dialogue
and reasoning examples supports deliberation on difﬁcult requests and concise responses to rou-
tine turns. Training examples span diverse topics, personas, and interaction lengths. Open-ended
requests can admit multiple valid responses without requiring a single canonical wording. Fig-
ure 6 summarizes the construction pipeline for multi-turn dialogue examples that support these
objectives.

Factorized construction. Generation follows four axes: topics and their concrete discussion
points; participant personas that specify roles, backgrounds, and interaction styles; turn depth;
and target capabilities such as contextual recall, logical reasoning, and instruction use. A stratiﬁed
rotation schedule coordinates these choices within topics, extending coverage beyond their global
marginal distributions.




                                                 11
                                                                                                                                             StepFun-Audio Team




                                          Persona corpus                                              Capability injection
                                           user personas and                                              optional requirements
                                           interaction styles                                               for the final turn


              1                       2                                3                              4                              5
                                                                                                                   ?

               Discussion points              Case plan                       Self-play                   Final-turn query                  Labelling
                  topic-classified        topic, scene, persona,           two models; N−1               the user asks; no                this one answer
                   source points              and turn plan                 turns of context          answer is produced here            is the only target




                          Training example       the first N−1 turns as context, the final query, and the labelled response with its reasoning




Figure 6: Construction of multi-turn dialogue training examples through discussion-point selection, case planning, self-play, ﬁnal-
turn query construction, and labeling.

Turn depth is an explicit construction variable. Longer dialogues progress through deeper engage-
ment with discussion points, allowing later turns to reﬁne constraints, resolve ambiguity, revisit
evidence, or change direction while remaining consistent with the history.

Quality assessment and routing. Quality control separates three concerns into independent
stages. First, a context–query review evaluates the depth and informativeness of the dialogue
history, whether the opening is self-contained, and whether the ﬁnal query is substantive and prop-
erly connected to the preceding conversation. Second, when capabilities are injected into the ﬁnal
turn, a capability-speciﬁc review checks both whether the query instantiates each requested capa-
bility and whether the response actually satisﬁes its requirement. Third, response review evaluates
answer quality, persona and style consistency, and naturalness as spoken dialogue.
Deterministic checks handle defects such as empty output, malformed tokens, severe repetition,
and role confusion. Only examples that pass these checks and receive high scores in all three
quality-control stages are retained for supervised ﬁne-tuning; all other examples are rejected.

Reasoning-model evaluation. We evaluate StepAudio 3 in reasoning mode on the eight StepAu-
dioChat dimensions. This evaluation isolates the model’s conversational and reasoning capability;
here we focus only on its dialogue results. The results in this subsection directly evaluate the
reasoning-mode model. By contrast, the overall comparison in Section 8 evaluates the realtime
system, which additionally applies Think-While-Speaking, Adaptive Thinking, and MTP acceler-
ation, as described in Section 6.3. Table 4 compares the reasoning checkpoint with the dialogue
baselines.
StepAudio 3 achieves a macro average of 73.0, above Doubao 2.0 Lite at 70.5 and DeepSeek-V4-
Flash at 71.4, but below Kimi K3 at 77.1. It ranks second on reasoning, memory, knowledge,
conversational pragmatics, and persona and role consistency. Kimi K3 leads six of the eight di-
mensions, including reasoning at 81.9, memory at 77.6, and safety and reliability at 84.8, while
Doubao 2.0 Lite leads instruction following and persona and role consistency. These category-level
differences show that strong aggregate reasoning does not imply uniformly stronger instruction fol-
lowing or role consistency.




                                                                             12
                                                                                                             StepFun-Audio Team


Table 4: Dialogue and reasoning evaluation of StepAudio 3 Realtime in reasoning mode and baseline models. The reasoning-mode
results isolate the model capability before realtime interaction; the complete realtime system is evaluated separately in Section 8.
Scores use a 0–100 scale (higher is better). Bold marks the best result in each row, and underlining marks the second-best result.

     Capability                     StepAudio 3 Realtime (Reasoning)        Doubao 2.0 Lite   DeepSeek-V4-Flash      Kimi K3
     Instruction Following                                           66.3              72.9                   71.4       68.9
     Faithfulness                                                    72.4              67.5                   75.3       78.4
     Reasoning                                                       73.0              72.7                   64.8       81.9
     Memory                                                          72.0              71.3                   71.5       77.6
     Knowledge                                                       73.1              59.9                   71.6       78.6
     Safety & Reliability                                            79.0              75.9                   79.9       84.8
     Conversational Pragmatics                                       67.2              61.5                   62.9       70.3
     Persona & Role Consistency                                      80.9              82.6                   73.6       76.5
     Macro Average                                                   73.0              70.5                   71.4       77.1

6.3 Think-While-Speaking

Think-While-Speaking coordinates realtime reasoning in StepAudio 3 Realtime. It builds on the
two-process design of Mind-Paced Speaking [17]. Two concurrent calls to the same audio model
act as a Formulation Brain and an Articulation Brain. The Formulation Brain generates a private
reasoning trace. The Articulation Brain produces short response segments conditioned on the
reasoning available so far and on the response already spoken.
Playback-aware scheduling releases response segments according to the progress of the streaming
output audio while formulation continues in parallel. Once formulation ﬁnishes, the remaining
response can use the complete reasoning state. A ﬁnal continuation can supplement or correct an
answer that began from incomplete reasoning. The system uses Speak-First by default, starting
the response without waiting for an initial reasoning preﬁx. Think-First waits for a short reasoning
preﬁx before beginning the response.
Adaptive Thinking controls whether a turn uses explicit reasoning. For turns that do, MTP ac-
celeration speeds up the private thinking stream, following speculative and multi-token decoding
approaches that reduce sequential target-model steps [28–31]. Together, these mechanisms coordi-
nate reasoning effort, decoding efﬁciency, and spoken delivery.

6.3.1     Adaptive Thinking

Motivation. Different conversational turns warrant different deliberation budgets. Explicit rea-
soning consumes decoding compute and can delay a routine response. Adaptive Thinking aims to
reduce unnecessary reasoning while retaining it on turns that beneﬁt from deliberation.

Reasoning-selection policy. Adaptive Thinking constructs supervision at the assistant-turn level.
For each turn, we collect the dialogue context, target answer, original reasoning trace, and task-type
features. A ﬁxed probe model, trained without the adaptive-thinking data transformation, receives
an empty think block and regenerates the answer under a no-think condition.
A blind judge scores the original and no-think trajectories against the target answer, without know-
ing which is which, and labels the turn by whether reasoning changed the answer’s quality. This
paired judgment provides the primary evidence, with consistency across repeated judgments and
the coherence between a reasoning trace and the answer it produces, together with a task-type prior,
informing how conservatively to retain reasoning supervision.


                                                                13
                                                                                                                      StepFun-Audio Team



    A Adaptive Thinking routing



                                          Adaptive Thinking                      NO · DIRECT ROUTE             Immediate response
                                          Does this turn need                                                    empty think block
      User turn                           explicit reasoning?
    audio + context

                                                       YES · DELIBERATE ROUTE
    B Think-While-Speaking with MTP
                      TIME STEP i                    Current
                                                      Think


    Formulation                              LLM Decoder
       Brain
                           user context          thought stream              Same                  MTP
                                                                             Model               Decoding
                                          Previous   Current   Previous    Current              Acceleration
                                           Think      Think    Response   Response


     Articulation                            LLM Decoder
        Brain


                             Audio Adapter
        Input Token
        Think Token
        Response Token       Audio Encoder




                              Input Audio                                            Streaming Output Audio

Figure 7: Overview of realtime thinking in StepAudio 3 Realtime. Adaptive Thinking routes each turn to an immediate or deliberate
response, while MTP acceleration speeds up the private thinking used by deliberate turns.

Within each domain, turns labeled reasoning-unnecessary are the candidates for replacement, and a
per-domain budget on the no-think rate decides how many are taken while the remaining turns keep
their original reasoning. Rather than spending that budget uniformly, we stratify retention by ﬁne-
grained topic and cap the drop rate within each capability, so that reasoning-intensive capabilities
are not disproportionately stripped of supervision.

Adaptive Thinking evaluation. Table 5 compares three conﬁgurations on StepAudioChat, cov-
ering 46 benchmark members in eight capability categories. Direct SFT and forced no-think share
baseline weights, with explicit reasoning enabled or disabled at inference time. Adaptive Thinking
is trained separately with reasoning-selection supervision, so its comparison also includes the effect
of training. Within each category, scores and think rates are unweighted means over benchmark
members. Evaluation uses temperature zero and no system prompt.
Adaptive Thinking invokes explicit reasoning at rates from 51.5% to 82.0% across the eight cat-
egories. Full thinking provides its largest gain over forced no-think in Reasoning (11.37 points),
followed by Persona and Role Consistency (8.37 points) and Knowledge (5.94 points). Relative
to Direct SFT, Adaptive Thinking improves Dialogue Pragmatics from 63.59 to 65.87, but reduces
Reasoning from 71.89 to 66.80.
The category rates expose a limitation of the selection policy. Reasoning has a think rate of 59.5%
despite beneﬁting most from full thinking. Faithfulness has a higher rate of 79.2%, but gains only


                                                                      14
                                                                                                               StepFun-Audio Team


Table 5: Adaptive Thinking ablation on the StepAudioChat dialogue benchmark. Scores are reported in the native percentage-based
scale. Higher scores are better. Think rates are percentages. Category values average benchmark members equally. The ﬁrst two
conditions share baseline weights; Adaptive Thinking uses a separately trained model. Bold and underlining mark the best and
second-best scores in each row; think rates are not ranked.

                                                 Direct SFT         Direct SFT (forced no think)     Adaptive Thinking
           Domain                            Think Rate   Score     Think Rate        Score          Think Rate    Score
           Instruction Following               100.0      64.15        0.0            61.98             60.0       62.12
           Faithfulness                        100.0      72.35        0.0            70.63             79.2       72.42
           Reasoning                           100.0      71.89        0.0            60.52             59.5       66.80
           Memory                              100.0      67.99        0.0            63.86             51.5       65.99
           Knowledge                           100.0      74.59        0.0            68.65             80.4       71.55
           Safety and Reliability              100.0      78.46        0.0            74.95             56.9       77.90
           Dialogue Pragmatics                 100.0      63.59        0.0            62.41             58.9       65.87
           Persona and Role Consistency        100.0      77.17        0.0            68.80             82.0       74.62

Table 6: MTP evaluation on StepAudioChat with a repetition penalty of 1.05. Quality, acceptance, and wall-clock measurements
use their respective evaluation settings. Wall-clock ratios are speciﬁc to each timing conﬁguration. Bold marks the best result in
each row, and underlining marks the second-best result.

                 Domain                        Baseline   MTP3      MTP3 (Medusa)      MTP5        MTP5 (Medusa)
                 Instruction Following          64.15     61.21          62.71         61.25           62.73
                 Faithfulness                   72.35     72.29          70.46         72.49           72.03
                 Reasoning                      70.76     74.30          73.74         73.14           72.73
                 Memory                         67.99     69.29          68.97         70.85           71.36
                 Knowledge                      74.59     75.07          75.34         75.31           74.33
                 Safety & Reliability           81.41     81.07          81.59         81.23           81.17
                 Conversational Pragmatics      63.59     66.04          63.17         66.22           66.15
                 Persona & Role                 77.17     77.99          75.92         77.19           77.56
                 Accepted/Step                     0      1.231          1.801         1.353           2.153
                 Wall-clock Speedup             1.00×     1.76×          2.05×         1.49×           1.72×

1.72 points from full thinking. Lower thinking frequency alone therefore does not demonstrate
that reasoning is allocated to the turns that beneﬁt most. These aggregate comparisons also do not
establish the optimal decision for individual turns.

6.3.2     Accelerating Private Reasoning with MTP

Adaptive Thinking reduces how often explicit reasoning is invoked. To reduce the decoding cost
of the remaining private thinking, we use MTP3 with three prediction heads, drafting up to three
future tokens at each target-model step [30, 31].
Strict veriﬁcation follows the target model’s standard speculative-decoding rule. Medusa-style typ-
ical acceptance uses an entropy-adaptive conﬁdence threshold to accept plausible draft tokens that
strict veriﬁcation may reject. This increases acceptance while allowing the generated distribution
to change. A repetition penalty of 1.05 discourages repeated tokens and reduces the risk of repeti-
tion loops under permissive acceptance. We apply typical acceptance and the repetition penalty to
private reasoning, while retaining strict veriﬁcation for the spoken response.

MTP evaluation. Table 6 reports StepAudioChat scores, accepted draft tokens per target-model
step, and wall-clock speedup for MTP3 and MTP5. All conﬁgurations use a repetition penalty of
1.05. The measurements retain the aggregation and runtime settings of their respective evaluations.
The tested MTP conﬁgurations improve Reasoning and Memory over the baseline, while Instruc-
tion Following declines.

                                                               15
                                                                                                             StepFun-Audio Team


Table 7: Marginal acceptance rate at each draft position on StepAudioChat under the acceptance-evaluation settings. All conﬁgu-
rations use a repetition penalty of 1.05. Bold and underlining mark the best and second-best result, respectively, within each head
column.

                              Depth    Veriﬁcation   Head 1    Head 2    Head 3    Head 4    Head 5
                                       Strict        65.0%     37.2%     20.8%      N/A       N/A
                              MTP3
                                       Typical       82.4%     58.2%     39.4%      N/A       N/A
                                       Strict         63.7%    35.5%     19.6%     10.7%      5.7%
                              MTP5
                                       Typical        80.6%    55.7%     37.6%     24.9%     16.4%

Under typical acceptance, MTP5 accepts more drafts per step than MTP3 (2.153 versus 1.801).
Table 7 shows similar acceptance rates for the ﬁrst three heads at both depths. The fourth and
ﬁfth heads add accepted drafts, but their strict marginal acceptance rates fall to 10.7% and 5.7%,
respectively. The additional heads therefore provide diminishing gains in accepted drafts per step.
Acceptance alone does not determine net efﬁciency, which also depends on reasoning length and
decoding costs. The reported wall-clock ratios therefore should not be interpreted as a controlled
comparison of draft depth. Keeping strict veriﬁcation for spoken output does not eliminate errors
arising from incomplete private reasoning.

6.4 Model Merging for Capability Integration

Specialized teacher training. We train multiple compatible teacher checkpoints from a common
base model, using a different data composition for each teacher. The mixtures emphasize comple-
mentary capabilities, including multi-turn dialogue, audio understanding, general text reasoning
and knowledge, and targeted mixed-domain behavior. This produces teachers that are individu-
ally strong in different regions of the capability space while preserving parameter alignment for
merging.

Weighted parameter merging. We integrate the specialized teachers by∑     directly averaging their
parameters.
    ∑        For teacher parameters θi , the merged model is θmerge =       i αi θi , where αi ≥ 0
and i αi = 1. The coefﬁcients control the contribution of each teacher and are selected against
held-out evaluations spanning dialogue, audio understanding, and general text capabilities. The
reported model uses four teachers with a normalized 3:1:1:1 weighting. Because integration occurs
in parameter space, it introduces neither additional model components nor inference-time routing.

Capability integration. Weighted merging is intended to retain complementary strengths rather
than make the merged model identical to the best teacher on every metric. The evaluation therefore
considers both capability-speciﬁc scores and their overall balance. This also allows teacher data
mixtures to be developed independently and then recombined without retraining a single model on
the full union of data.
Model merging results. Table 8 compares the four specialized teachers with their weighted merge
across audio understanding, general text, and dialogue. The Dialogue results are measured with
the model in reasoning mode. On audio understanding, the merge reaches a macro average of 81.3,
tying the best teacher macro average while leading on MMAU and WildSpeech. On general text, it
achieves the highest macro average of 76.5, with the best HMMT 2026 Feb and GPQA Diamond
scores and a tie on MultiChallenge. On dialogue, it has a macro average of 73.0, exceeding Teach-
ers 2, 3, and 4, while remaining below the strongest dialogue teacher at 74.2. These results support
model merging as a low-cost mechanism for combining complementary capabilities, while show-

                                                               16
                                                                                                                StepFun-Audio Team


Table 8: Capability comparison for four teachers trained with different data compositions and their 3:1:1:1 weighted merge. Results
cover audio understanding, general text, and dialogue. Domain macro averages give equal weight to the listed rows. Higher is better.
Bold marks the best result in each row, and underlining marks the second-best result.

         Domain                   Benchmark                    Merged       Teacher 1   Teacher 2   Teacher 3     Teacher 4
                                  BigBench Audio                     98.1       96.1        98.1         98.4         98.5
                                  AudioMultiChallenge                49.3       49.1        49.8         50.2         47.6
                                  MMSU                               90.6       85.5        85.5         90.4         90.9
                                  MMAU                               79.0       78.5        78.8         77.8         77.7
         Audio Understanding      WildSpeech                         77.1       76.5        76.4         75.9         76.1
                                  MMAR                               86.5       85.4        86.4         87.3         86.5
                                  Step-Caption                       78.2       75.8        78.3         79.6         79.4
                                  MTalk-Bench                        91.7       91.8        90.3         90.9         90.7
                                  Macro Average                      81.3       79.8        80.5         81.3         80.2
                                  HMMT 2026 Feb                      86.8       44.0        82.2         81.3         79.8
                                  GPQA Diamond                       83.0       73.1        81.9         80.1         80.1
         General Text
                                  MultiChallenge                     59.7       54.6        51.3         50.6         59.7
                                  Macro Average                      76.5       57.2        71.8         70.7         73.2
                                  Instruction Following              66.3       64.2        64.5         69.3         64.2
                                  Faithfulness                       72.4       74.0        65.6         67.1         73.6
                                  Reasoning                          73.0       75.2        67.0         67.2         67.8
                                  Memory                             72.0       73.4        70.0         68.3         71.5
         Dialogue                 Knowledge                          73.1       75.1        63.7         62.0         75.6
                                  Safety & Reliability               79.0       79.2        75.7         75.6         78.0
                                  Conversational Pragmatics          67.2       67.8        62.4         63.4         64.5
                                  Persona & Role                     80.9       84.7        79.5         76.9         83.0
                                  Macro Average                      73.0       74.2        68.6         68.7         72.3

ing that it provides a balanced trade-off rather than uniform improvement over every specialized
teacher. These measurements evaluate the underlying reasoning model and are separate from the
system-level evaluations that additionally use the realtime reasoning mechanisms described above.


7 Full-Duplex Voice Agent

StepAudio 3 Realtime extends its full-duplex interaction capabilities to tool-grounded task execu-
tion. The model selects among direct responses, lightweight tool calls, and asynchronous back-
end execution based on the requirements of each request. Asynchronous execution allows longer-
running tasks to proceed alongside the conversation, enabling the user to ask about progress or
provide additional requirements while work is underway.

7.1 Request Routing and Clariﬁcation

The model handles routine conversation and questions about stable knowledge directly. Requests
for up-to-date public information are routed to lightweight tools such as weather lookup or web
search. Requests involving private context, multi-step processing, or work extending beyond the
current conversational turn are delegated to the backend. This routing strategy determines whether
and how to invoke external capabilities, drawing on prior work in tool-augmented language mod-
eling [32, 33].
A grammatically complete phrase may still leave a spoken request incomplete or open to revision.
Spoken responses can be extended or explicitly corrected in subsequent segments, whereas tool

                                                                17
                                                                                                             StepFun-Audio Team


Table 9: Agentic task-completion results on τ -Voice. Scores are task-success rates on a 0–100 scale, with higher values indicating
better performance. The macro average assigns equal weight to the airline, retail, and telecom domains. Bold marks the best result
in each row, and underlining marks the second-best result.
 Domain           StepAudio 3 Realtime    Grok Voice Think Fast 2.0 High   Qwen Audio 3.0 Realtime Plus    GPT-Realtime-2.1 High
 Airline                   60.0                        56.0                            61.3                         62.0
 Retail                    37.7                        49.7                            49.0                         45.6
 Telecom                   70.2                        63.7                            53.5                         29.4
 Macro Average             56.0                        56.5                            54.6                         45.7


execution requires sufﬁciently speciﬁed intent and arguments. Before committing to an external
action, the model is therefore trained to gather missing information through clariﬁcation with the
user or context retrieval using an appropriate tool, and to obtain any required conﬁrmation.

7.2 Conversation During Asynchronous Execution

Backend tasks execute asynchronously while the conversation continues. During execution, the
user may request progress updates, provide additional requirements, or shift to another topic. The
model is trained to associate task-related user input with the ongoing task while distinguishing it
from unrelated dialogue. As results become available, they are incorporated into the conversational
context to inform subsequent spoken responses.
For complex requests, reasoning supports constraint resolution and task planning, while tool and
backend outputs provide evidence of what has actually been completed. This evidence guides
subsequent reasoning and action, consistent with the interleaved interaction pattern of ReAct [34].
Think-While-Speaking supports spoken responses during deliberation, while asynchronous execu-
tion allows the conversation to continue during external task execution.

7.3 Training for Conversational Tool Use

Training combines targeted voice-agent dialogues with real multi-step agent trajectories. The tar-
geted dialogues cover request routing, clariﬁcation, private-context retrieval, conﬁrmation before
consequential actions, execution-time updates, progress queries, and result reporting. These dia-
logues train the model to ground claims about private information and completed work in user-
provided context or evidence returned by tools. Negative examples discourage unnecessary tool
invocation and unsupported claims of successful execution.
The multi-step trajectories complement these dialogues by exposing the model to longer sequences
of reasoning and tool use. We ﬁlter and normalize these trajectories, focusing on tool-call structure,
argument consistency, evidence grounding, and suitability for spoken interaction.

7.4 Evaluation

We evaluate StepAudio 3 Realtime using the Artiﬁcial Analysis (AA) implementation of τ -
Voice [35]. The benchmark assesses tool-grounded task completion in full-duplex spoken inter-
action under challenging conversational and acoustic conditions, including interruptions in which
users revise their requests, backchannels, and diverse forms of background noise. These condi-
tions require agents to track evolving requests and coordinate spoken interaction with tool use.
The benchmark covers customer-service tasks in the airline, retail, and telecom domains, with


                                                                18
                                                                                    StepFun-Audio Team



task success determined by whether the ﬁnal database state matches the target state. We report
task-success rates for each domain and their equally weighted macro average.
As shown in Table 9, StepAudio 3 Realtime achieves a macro task-success rate of 56.0%, close to
Grok’s 56.5% and above Qwen’s 54.6% and GPT’s 45.7%. Across domains, StepAudio 3 Realtime
achieves the highest telecom score among the evaluated models at 70.2%, exceeding Grok by 6.5
percentage points. Its airline score of 60.0% is within 2.0 percentage points of the highest reported
score of 62.0%. Retail performance leaves room for further improvement, with a score of 37.7%
compared with 49.7% for Grok. Overall, StepAudio 3 Realtime achieves competitive performance
on end-to-end task completion, with the highest telecom score among the evaluated models and an
airline score close to the best reported result.


8 Evaluation

We evaluate the StepAudio 3 family along six capability domains: speech recognition, audio under-
standing, dialogue and reasoning, full-duplex interaction, agentic task completion, and general text.
Together, these domains measure the progression from recognizing an utterance to understanding
its context, managing the conversational ﬂoor, and completing an external task. We ﬁrst describe
the benchmarks and comparison models, then analyze the results within each domain.

8.1 Benchmarks

The ASR benchmarks and their task-speciﬁc setup are described with the ASR model and results
in Section 4.1.2; the paragraphs below cover the remaining evaluation domains.

Audio understanding. We use Big Bench Audio [36], MMSU [37], MMAU [38], MMAR [39],
WildSpeech-Bench [40], AudioMultiChallenge [41], Step-Caption [42], and MTalk-Bench [43] to
cover audio-grounded reasoning, ﬁne-grained perception, and multi-turn understanding.

Dialogue and reasoning. StepAudioChat covers eight dimensions of foundational conversational
intelligence. Its construction is described in Section 6.1.

Full-duplex interaction. We use the Artiﬁcial Analysis subset of Full Duplex Bench v1 and
v1.5 [35], covering pause handling, turn taking, user interruptions, and backchannels.

Agentic task completion. The Artiﬁcial Analysis implementation of τ -Voice [35] evaluates tool-
grounded customer-service tasks in airline, retail, and telecom environments.

General text. HMMT February 2026 [44], GPQA Diamond [45], and MultiChallenge [46] assess
competition mathematics, scientiﬁc question answering, and multi-turn conversational reliability,
respectively.

8.2 Baselines

For ASR, we compare against Doubao 2.0 ASR, Seed 2.0 Lite [47], and HY3.0 ASR Preview [48].
All ASR baselines are rerun under the same evaluation setup as StepAudio 3 ASR Max, using the
same test audio and scoring procedure. For audio understanding, we use Doubao 2.0 Lite [47],

                                                 19
                                                                                 StepFun-Audio Team



Gemini 3 Flash [49], and Gemini 3.1 Pro [50]. Dialogue baselines include Doubao 2.0 Lite,
DeepSeek-V4-Flash [51], and Kimi K3 [52]. General text uses Doubao 2.0 Lite and Gemini 3
Flash.
Full-duplex baselines are GPT-realtime-2 (High) [53], Qwen Audio 3.0 Realtime Plus [54], and
Grok Voice Think Fast 2.0 High [55]. Agentic evaluation uses the same Qwen and Grok variants,
with GPT-Realtime-2.1 High [56] replacing GPT-realtime-2. Model versions and effort labels
follow the corresponding evaluation records.

8.3 Evaluation Protocols and Metrics

The following conventions apply to the main comparison in Table 10. All scores are expressed on
a 0–100 scale, with higher values indicating better performance; ASR error rates are the exception
and are deﬁned separately in Section 4.1.2.
The ASR scoring protocol is speciﬁed alongside the ASR results in Section 4.1.2; the paragraphs
below cover the non-ASR domains.

Audio understanding. We retain each benchmark’s reported accuracy or normalized evaluation
score. Step-Caption uses judge-based scoring against annotated speaker attributes, with sample
scores averaged over the evaluation set [42]. The MTalk-Bench entry includes only the Paralin-
guistic Information and Ambient Sound components, reported as one aggregate.

Dialogue and reasoning. Each StepAudioChat dimension is the unweighted mean of its vali-
dated capability line scores. We report both the reasoning-mode result and the realtime Think-
While-Speaking result; component-ablation scores are not used to ﬁll these entries.

Full-duplex interaction. Category scores measure the percentage of samples satisfying the cor-
responding interaction criterion [35]. We use the source-reported Overall score, preserving the
benchmark’s aggregation rather than averaging the four displayed category scores.

Agentic task completion. A τ -Voice task succeeds when the ﬁnal database state matches its
target. Domain task-success rates average three trials where available, and the reported macro
average gives equal weight to Airline, Retail, and Telecom [35].

General text. We report the recorded accuracy percentages for HMMT February 2026, GPQA Di-
amond, and MultiChallenge separately. MultiChallenge evaluates responses with instance-speciﬁc
rubrics [46]. No average is taken across these three benchmarks.

8.4 Results

Across the reported capability domains, StepAudio 3 Realtime combines broad audio under-
standing with strong dialogue, reasoning, and interaction control. It leads four of eight audio-
understanding benchmarks and reaches a macro average of 81.3, within 0.5 points of Gemini 3.1
Pro. Its clearest gains appear on MMSU and MMAR, while the leading Step-Caption and MTalk-
Bench results show strength beyond lexical content, including speaker attributes, paralinguistic
cues, ambient sound, and multi-turn audio context. In reasoning mode, StepAudio 3 reaches a
73.0 macro average on StepAudioChat, above Doubao 2.0 Lite and DeepSeek-V4-Flash and below

                                               20
                                                                                                                                           StepFun-Audio Team


Table 10: Capability evaluation of StepAudio 3 Realtime and domain-speciﬁc baselines. Scores use a 0–100 scale (higher is
better), with protocols and aggregation speciﬁed in Section 8.3. For Dialogue and Reasoning evaluation, StepAudio 3 Realtime
uses realtime mode while others use reasoning mode. Bold and underlining mark the best and second-best results in each row.
Audio Understanding (Score ↑)            StepAudio 3 Realtime                  Doubao 2.0 Lite                  Gemini 3 Flash                  Gemini 3.1 Pro
Big Bench Audio                                  98.1                                98.8                            99.4                             99.6
AudioMultiChallenge                              49.3                                48.5                            56.6                             67.0
MMSU                                             90.6                                80.0                            77.0                             83.6
MMAU                                             79.0                                77.5                            77.6                             80.5
WildSpeech                                       77.1                                73.9                            74.4                             77.7
MMAR                                             86.5                                75.9                            75.4                             81.7
Step-Caption                                     78.2                                76.8                            67.8                             74.8
MTalk-Bench                                      91.7                                89.9                            88.5                             89.1
Dialogue and Reasoning (Score ↑)   StepAudio 3 Realtime (Interactive)    Doubao 2.0 Lite (Reasoning)     DeepSeek-V4-Flash (Reasoning)       Kimi K3 (Reasoning)
Instruction Following                            54.1                                72.9                            71.4                             68.9
Faithfulness                                     71.9                                67.5                            75.3                             78.4
Reasoning                                        73.6                                72.7                            64.8                             81.9
Memory                                           71.8                                71.3                            71.5                             77.6
Knowledge                                        70.4                                59.9                            71.6                             78.6
Safety and Reliability                           75.1                                75.9                            79.9                             84.8
Conversational Pragmatics                        68.2                                61.5                            62.9                             70.3
Persona and Role Consistency                     78.3                                82.6                            73.6                             76.5
Macro Average                                    70.4                                70.5                            71.4                             77.1
General Text (Accuracy ↑)                StepAudio 3 Realtime                  Doubao 2.0 Lite                  Gemini 3 Flash
HMMT 2026 Feb                                    86.8                                73.9                            85.9                              –
GPQA Diamond                                     83.0                                82.4                            90.3                              –
MultiChallenge                                   59.7                                60.8                            68.1                              –
Full Duplex (Score ↑)                    StepAudio 3 Realtime               GPT-realtime-2 (High)        Qwen Audio 3.0 Realtime Plus    Grok Voice Think Fast 2.0 high
AA Full-Duplex Bench                             98.9                                95.3                            98.4                             95.1
Agentic (Success ↑)                      StepAudio 3 Realtime           Grok Voice Think Fast 2.0 High   Qwen Audio 3.0 Realtime Plus       GPT-Realtime-2.1 High
τ -Voice                                         56.0                                56.5                            54.6                             45.7


Kimi K3, with particularly competitive results in reasoning, memory, knowledge, conversational
pragmatics, and persona consistency. In realtime interaction, StepAudio 3 Realtime reaches a 70.41
macro average on StepAudioChat, comparable to Doubao 2.0 Lite at 70.5 and DeepSeek-V4-Flash
at 71.4. Together with Think-While-Speaking, this shows that the model can deliberate while pro-
ducing speech and retain dialogue and reasoning performance comparable to dedicated reasoning
models, rather than providing only low-latency surface responses. This capability is paired with
robust conversational timing. The model ranks ﬁrst on Full Duplex Bench with an Overall score of
98.9, including 100.0 on turn taking and 99.0 on interruption handling, while remaining strong on
pauses and backchannels. This balanced proﬁle suggests that it can preserve conversational ﬂow
without treating every user sound as an interruption. The agentic and general-text results further
demonstrate solid performance in tool use and text-based capabilities. The model reaches 56.0 on
τ -Voice, close to the best reported 56.5, and leads HMMT with 86.8, although GPQA Diamond
and MultiChallenge remain below Gemini 3 Flash.


9 Conclusion

StepAudio 3 Realtime brings perception, conversational timing, reasoning, and tool use into a
continuous spoken interaction. It allows deliberation and external tasks to proceed alongside the
conversation, with new user input and returned evidence informing subsequent responses. Eval-
uations show strong audio understanding and conversational-ﬂoor management, while revealing
variation across reasoning and tool-use tasks. Adaptive Thinking reduces the frequency of explicit
reasoning, with uneven effects on answer quality. Multi-turn constraint handling and retail task
completion remain areas for improvement. These ﬁndings motivate more effective allocation of
reasoning effort and more reliable task execution over extended conversations.



                                                                                  21
                                                                               StepFun-Audio Team



Contributors

The listing of authors is in alphabetical order based on their ﬁrst names.

Bin Lin,                  Bo Zhao,                    Boyang Zhang,          Boyong Wu,
Chao Yan,                 Chen Geng,                  Chen Wu,               Cheng Yi,
Chengli Feng,             Chenglin Zhu,               Chengting Feng,        Chengyuan Yao,
Daijiao Liu,              DanNi Wan,                  Daxin Jiang,           Dongjian Li,
Dongqing Pang,            Fei Tian,                   Feng Tian,             Future Li,
Gang Yu,                  Guanglong Yang,             Haoyang Zhang,         Hongyuan Wang,
Jia Peng,                 Jiahao Song,                Jialong Xue,           Jiamin Fan,
Jiangjie Zhen,            Jianzheng Gao,              Jincheng Wen,          Jinghua Liang,
Jinglan Gong,             Jun Chen,                   Li Xie,                Liang Zhao,
Lifang Zhang,             Lingli Ji,                  Lun Cai,               Min Xu,
Peilin Li,                Peng Yang,                  Pengfei Tan,           Qingjian Lin,
Qinxin Du,                Ruijie Xiong,               Runze Li,              Shenghua Hu,
Shengqian Qin,            Shi Qiu,                    Siqi Tu,               Siyi Zhou,
Tianjiao Deng,            Wanying Lu,                 Weiming Niu,           Wen Sun,
WenWen Qu,                Xiangyu Zhang,              Xianwei Zhang,         Xiaosu Su,
Xing Chen,                Xinyu Liu,                  Xuerui Yang,           Yan Wu,
Yang Li,                  Yang Yang,                  Yechang Huang,         Yibo Zhu,
Yifan Zhang,              Yinuo Yan,                  Youjun Chen,           Yu Fu,
Yu Luo,                   Yu Zhou,                    Yujie Chen,            Yumang Wang,
Yunzhou Ju,               Yuxiang Yang,               Yuxin Li,              Yuxin Zhang,
Zekai Liu,                Zengwei Yao,                Zhaoxin Yuan,          Zhenwei Mou,
Zhiquan Zhang,            Zhiyue Wu,                  Zichao Li,             Zichao Zhou,
Ziqi Ren,                 Zixuan Wang,


References

 [1] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya
     Sutskever. Robust speech recognition via large-scale weak supervision. In International
     conference on machine learning, pages 28492–28518. PMLR, 2023.
 [2] Ye Bai, Jingping Chen, Jitong Chen, Wei Chen, Zhuo Chen, Chuang Ding, Linhao Dong,
     Qianqian Dong, Yujiao Du, Kepan Gao, et al. Seed-asr: Understanding diverse speech and
     contexts with llm-based speech recognition. arXiv preprint arXiv:2407.04675, 2024.
 [3] Qingjian Lin, Yuxin Li, Haoyang Zhang, Jun Chen, Yechang Huang, Feng Tian, Xie Li,
     Xiangyu Tony Zhang, Daijiao Liu, Yuxin Zhang, Jinglan Gong, Bo Zhao, Fei Tian, Xuerui
     Yang, Gang Yu, Xiangyu Zhang, and Daxin Jiang. ParaASR: Multi-Token Prediction for Fast
     and Long-Context LLM-Based Speech Recognition. arXiv preprint arXiv:2607.29279, 2026.
     URL https://arxiv.org/abs/2607.29279.




                                                 22
                                                                                StepFun-Audio Team



 [4] Zalán Borsos, Raphaël Marinier, Damien Vincent, Eugene Kharitonov, Olivier Pietquin, Matt
     Shariﬁ, Dominik Roblek, Olivier Teboul, David Grangier, Marco Tagliasacchi, et al. Audiolm:
     a language modeling approach to audio generation. IEEE/ACM transactions on audio, speech,
     and language processing, 31:2523–2533, 2023.
 [5] Changli Tang, Wenyi Yu, Guangzhi Sun, Xianzhao Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma,
     and Chao Zhang. Salmonn: Towards generic hearing abilities for large language models. In
     International Conference on Learning Representations, volume 2024, pages 16607–16629,
     2024.
 [6] Heeseung Kim, Soonshin Seo, Kyeongseok Jeong, Ohsung Kwon, Soyoon Kim, Jungwhan
     Kim, Jaehong Lee, Eunwoo Song, Myungwoo Oh, Jung-Woo Ha, et al. Paralinguistics-aware
     speech-empowered large language models for natural conversation. Advances in Neural In-
     formation Processing Systems, 37:131072–131103, 2024.
 [7] Boyong Wu, Chao Yan, Chen Hu, Cheng Yi, Chengli Feng, Fei Tian, Feiyu Shen, Gang
     Yu, Haoyang Zhang, Jingbei Li, et al. Step-audio 2 technical report. arXiv preprint
     arXiv:2507.16632, 2025.
 [8] Jin Xu, Zhifang Guo, Hangrui Hu, Yunfei Chu, Xiong Wang, Jinzheng He, Yuxuan Wang,
     Xian Shi, Ting He, Xinfa Zhu, et al. Qwen3-omni technical report. arXiv preprint
     arXiv:2509.17765, 2025.
 [9] Xiong Wang, Yangze Li, Chaoyou Fu, Yunhang Shen, Lei Xie, Ke Li, Xing Sun, and Long
     Ma. Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm.
     arXiv preprint arXiv:2411.00774, 2024.
[10] Alexandre Défossez, Laurent Mazaré, Manu Orsini, Amélie Royer, Patrick Pérez, Hervé Jé-
     gou, Edouard Grave, and Neil Zeghidour. Moshi: a speech-text foundation model for real-
     time dialogue. arXiv preprint arXiv:2410.00037, 2024.
[11] Donghang Wu, Haoyang Zhang, Chen Chen, Tianyu Zhang, Fei Tian, Xuerui Yang, Gang
     Yu, Hexin Liu, Nana Hou, Yuchen Hu, et al. Chronological thinking in full-duplex spoken
     dialogue language models. In Proceedings of the 27th Annual Meeting of the Special Interest
     Group on Discourse and Dialogue, pages 473–485, 2026.
[12] Haoyang Zhang, Jun Chen, Donghang Wu, Yuxin Li, Yuxin Zhang, Xiangyu Tony Zhang,
     Che Liu, Qingjian Lin, Yizhou Peng, Hexin Liu, et al. Duplexsla: A full-duplex spo-
     ken language model with synchronized speech, language, and action. arXiv preprint
     arXiv:2605.20755, 2026.
[13] Ailin Huang, Boyong Wu, Bruce Wang, Chao Yan, Chen Hu, Chengli Feng, Fei Tian, Feiyu
     Shen, Jingbei Li, Mingrui Chen, et al. Step-Audio: Uniﬁed Understanding and Generation
     in Intelligent Speech Interaction. arXiv preprint arXiv:2502.11946, 2025. URL https://
     arxiv.org/abs/2502.11946.
[14] Fei Tian, Xiangyu Tony Zhang, Yuxin Zhang, Haoyang Zhang, Yuxin Li, Daijiao Liu, Yayue
     Deng, Donghang Wu, Jun Chen, Liang Zhao, et al. Step-audio-r1 technical report. arXiv
     preprint arXiv:2511.15848, 2025.
[15] Yuxin Zhang, Xiangyu Tony Zhang, Daijiao Liu, Fei Tian, Yayue Deng, Jun Chen, Qingjian
     Lin, Haoyang Zhang, Yuxin Li, Jinglan Gong, et al. Step-audio-r1. 5 technical report. arXiv

                                              23
                                                                                StepFun-Audio Team



     preprint arXiv:2604.25719, 2026.
[16] Bin Lin, Bo Zhao, Boyong Wu, Chao Yan, Chen Wu, Cheng Yi, Chengyuan Yao, Daijiao Liu,
     Fei Tian, Feng Tian, et al. Stepaudio 2.5 technical report. arXiv preprint arXiv:2605.23463,
     2026.
[17] Donghang Wu, Haoyang Zhang, Jun Chen, Hexin Liu, Eng Siong Chng, Fei Tian, Xuerui
     Yang, Xiangyu Zhang, Daxin Jiang, Gang Yu, et al. Mind-paced speaking: A dual-brain ap-
     proach to real-time reasoning in spoken language models. arXiv preprint arXiv:2510.09592,
     2025.
[18] Daniel S Park, William Chan, Yu Zhang, Chung-Cheng Chiu, Barret Zoph, Ekin D Cubuk,
     and Quoc V Le. Specaugment: A simple data augmentation method for automatic speech
     recognition. arXiv preprint arXiv:1904.08779, 2019.
[19] Jonathan G Fiscus. A post-processing system to yield reduced word error rates: Recognizer
     output voting error reduction (rover). In 1997 IEEE workshop on automatic speech recogni-
     tion and understanding proceedings, pages 347–354. IEEE, 1997.
[20] Hexin Liu, Haoyang Zhang, Qiquan Zhang, Xiangyu Zhang, Dongyuan Shi, Eng Siong Chng,
     and Haizhou Li. Code-Switching Speech Recognition Under the Lens: Model- and Data-
     Centric Perspectives. IEEE Transactions on Audio, Speech and Language Processing, 34:
     1853–1865, 2026. doi: 10.1109/TASLPRO.2026.3675776.
[21] Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur. Librispeech: an
     asr corpus based on public domain audio books. In 2015 IEEE international conference on
     acoustics, speech and signal processing (ICASSP), pages 5206–5210. IEEE, 2015.
[22] Hui Bu, Jiayu Du, Xingyu Na, Bengu Wu, and Hao Zheng. Aishell-1: An open-source
     mandarin speech corpus and a speech recognition baseline. In 2017 20th conference of the
     oriental chapter of the international coordinating committee on speech databases and speech
     I/O systems and assessment (O-COCOSDA), pages 1–5. IEEE, 2017.
[23] Binbin Zhang, Hang Lv, Pengcheng Guo, Qijie Shao, Chao Yang, Lei Xie, Xin Xu, Hui Bu,
     Xiaoyu Chen, Chenchen Zeng, et al. Wenetspeech: A 10000+ hours multi-domain mandarin
     corpus for speech recognition. In ICASSP 2022-2022 IEEE International Conference on
     Acoustics, Speech and Signal Processing (ICASSP), pages 6182–6186. IEEE, 2022.
[24] He Wang, Linhan Ma, Dake Guo, Xiong Wang, Lei Xie, Jin Xu, and Junyang Lin.
     ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark. arXiv preprint
     arXiv:2507.05727, 2025. URL https://arxiv.org/abs/2507.05727.
[25] Che Liu, Lichao Ma, Xiangyu Tony Zhang, Yuxin Zhang, Haoyang Zhang, Xuerui Yang,
     and Fei Tian. Boosting Omni-Modal Language Models: Staged Post-Training with Visually
     Debiased Evaluation. arXiv preprint arXiv:2605.12034, 2026. URL https://arxiv.org/
     abs/2605.12034.
[26] Qingkai Fang, Shoutao Guo, and Yang Feng. Bayling-duplex: Native full-duplex speech
     dialogue with a single autoregressive llm. arXiv preprint arXiv:2606.14528, 2026.
[27] Yayue Deng, Guoqiang Hu, Haiyang Sun, Xiangyu Zhang, Haoyang Zhang, Fei Tian, Xuerui
     Yang, Gang Yu, and Eng Siong Chng. Multi-bench: A multi-turn interactive benchmark


                                               24
                                                                                 StepFun-Audio Team



     for assessing emotional intelligence ability of spoken dialogue models.      arXiv preprint
     arXiv:2511.00850, 2025.
[28] Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre,
     and John Jumper. Accelerating large language model decoding with speculative sampling.
     arXiv preprint arXiv:2302.01318, 2023.
[29] Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via
     speculative decoding. In International conference on machine learning, pages 19274–19286.
     PMLR, 2023.
[30] Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D Lee, Deming Chen, and Tri
     Dao. Medusa: Simple llm inference acceleration framework with multiple decoding heads.
     arXiv preprint arXiv:2401.10774, 2024.
[31] Fabian Gloeckle, Badr Youbi Idrissi, Baptiste Rozière, David Lopez-Paz, and Gabriel Syn-
     naeve. Better & faster large language models via multi-token prediction. arXiv preprint
     arXiv:2404.19737, 2024.
[32] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Ham-
     bro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language mod-
     els can teach themselves to use tools. Advances in neural information processing systems, 36:
     68539–68551, 2023.
[33] Shishir G Patil, Tianjun Zhang, Xin Wang, and Joseph E Gonzalez. Gorilla: Large language
     model connected with massive apis. Advances in Neural Information Processing Systems, 37:
     126544–126565, 2024.
[34] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and
     Yuan Cao. React: Synergizing reasoning and acting in language models. arXiv preprint
     arXiv:2210.03629, 2022.
[35] Artiﬁcial Analysis. Speech to speech benchmarking methodology, 2026. URL https://
     artificialanalysis.ai/methodology/speech-to-speech-benchmarking/.
[36] Artiﬁcial Analysis. Evaluating audio reasoning with big bench audio. Hugging Face Blog,
     2024. URL https://huggingface.co/blog/big-bench-audio-release.
[37] Dingdong Wang, Junan Li, Jincenzi Wu, Dongchao Yang, Xueyuan Chen, Tianhua Zhang,
     and Helen Meng. Mmsu: A massive multi-task spoken language understanding and reasoning
     benchmark. In International Conference on Learning Representations, volume 2026, pages
     31374–31410, 2026.
[38] Sakshi Sakshi, Utkarsh Tyagi, Sonal Kumar, Ashish Seth, Ramaneswaran Selvakumar, Oriol
     Nieto, Ramani Duraiswami, Sreyan Ghosh, and Dinesh Manocha. Mmau: A massive multi-
     task audio understanding and reasoning benchmark. In International Conference on Learning
     Representations, volume 2025, pages 84929–84964, 2025.
[39] Ziyang Ma, Yinghao Ma, Yanqiao Zhu, Chen Yang, Yi-Wen Chao, Ruiyang Xu, Wenxi Chen,
     Yuanzhe Chen, Zhuo Chen, Jian Cong, et al. Mmar: A challenging benchmark for deep
     reasoning in speech, audio, music, and their mix. Advances in Neural Information Processing
     Systems, 38, 2026.


                                               25
                                                                               StepFun-Audio Team



[40] Linhao Zhang, Jian Zhang, Bokai Lei, Chuhan Wu, Aiwei Liu, Wei Jia, and Xiao Zhou.
     Wildspeech-bench: Benchmarking end-to-end speechllms in the wild. arXiv preprint
     arXiv:2506.21875, 2025.
[41] Advait Gosai, Tyler Vuong, Utkarsh Tyagi, Steven Li, Wenjia You, Miheer Bavare, Arda Uçar,
     Zhongwang Fang, Brian Jang, Bing Liu, et al. Audio multichallenge: A multi-turn evaluation
     of spoken dialogue systems on natural human interaction. In Proceedings of the 64th Annual
     Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages
     35740–35770, 2026.
[42] StepFun.    Step-caption: Benchmark and evaluation protocol, 2026.                    URL
     https://github.com/stepfun-ai/Step-Audio-R1/tree/main/benchmarks/
     Step-Audio-R1.5/step_caption.
[43] Yuhao Du, Qianwei Huang, Guo Zhu, Zhanchen Dai, Shunian Chen, Qiming Zhu, Le Pan,
     Minghao Chen, Yuhao Zhang, Li Zhou, et al. Mtalk-bench: Evaluating speech-to-speech
     models in multi-turn dialogues via arena-style and rubrics protocols. arXiv preprint
     arXiv:2508.18240, 2025.
[44] HMMT. Archive of february 2026, 2026. URL https://www.hmmt.co/www/archive/292.
[45] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang,
     Julien Dirani, Julian Michael, and Samuel R Bowman. Gpqa: A graduate-level google-proof
     q&a benchmark. arXiv preprint arXiv:2311.12022, 2023.
[46] Kaustubh Deshpande, Ved Sirdeshmukh, Johannes Baptist Mols, Lifeng Jin, Ed-Yeremai
     Hernandez-Cardona, Dean Lee, Jeremy Kritz, Willow E Primack, Summer Yue, and Chen
     Xing. Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging
     to frontier llms. In Findings of the Association for Computational Linguistics: ACL 2025,
     pages 18632–18702, 2025.
[47] ByteDance Seed. Seed2.0, 2026. URL https://seed.bytedance.com/en/seed2.
[48] Tencent Cloud. Intelligent Subtitles: Hy ASR 3.0 Preview Integration, 2026. URL https:
     //cloud.tencent.cn/document/product/862/135605.
[49] Google DeepMind. Gemini 3 Flash Model Card, 2025. URL https://deepmind.google/
     models/model-cards/gemini-3-flash/.
[50] Google DeepMind. Gemini 3.1 Pro Model Card, 2026. URL https://deepmind.google/
     models/model-cards/gemini-3-1-pro/.
[51] DeepSeek. DeepSeek-V4-Flash Update, 2026. URL https://api-docs.deepseek.com/
     updates/#deepseek-v4-flash-update.
[52] Moonshot AI. Kimi K3: Open Frontier Intelligence, 2026. URL https://github.com/
     MoonshotAI/Kimi-K3.
[53] OpenAI. GPT-Realtime-2, n.d..      URL https://developers.openai.com/api/docs/
     models/gpt-realtime-2.
[54] Alibaba Cloud. Speech-to-Speech Models, n.d. URL https://docs.qwencloud.com/
     developer-guides/speech/s2s-models.


                                              26
                                                                    StepFun-Audio Team



[55] SpaceXAI. Introducing Grok Voice Think Fast 2.0, 2026. URL https://x.ai/news/
     grok-voice-think-fast-2.
[56] OpenAI. GPT-Realtime-2.1, n.d.. URL https://developers.openai.com/api/docs/
     models/gpt-realtime-2.1.




                                        27

