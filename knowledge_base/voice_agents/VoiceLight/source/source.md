# Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation
Source: https://arxiv.org/abs/2609.20995
Kind: pdf
Fetched: 2026-09-22T09:29:50.492515+00:00
Tool: pdftotext

                                                      Voice-Light: A Full-Duplex Cascaded Voice Agent with
                                                         Causal Turn-Taking and Speculative Generation
                                                                                                       Bertil Braun
                                                                                                   contact@bertil-braun.de


                                                                                                           Abstract
                                                  Natural spoken interaction requires more than streaming ASR, language generation, and speech synthesis: a system must react to
                                              overlap without canceling on every acknowledgment, prepare a response before a turn is certain, and ensure canceled audio cannot
                                              enter conversation history. We present Voice-Light, a full-duplex cascaded voice agent that combines immediate acoustic onset, a
                                              causal adapter sharing a streaming ASR encoder, reversible playback control, and private speculative response generation. Structured
                                              tool calls execute concurrently with audible bridge speech, while browser acknowledgments make rendered audio authoritative for




arXiv:2609.20995v1 [cs.SD] 17 Sep 2026
                                              durable history. Locked evaluation on 1,673 real-conversation silence candidates found that an earlier learned completion checkpoint
                                              preserved a 2.70% false-cutoff rate but reached only 12.53% end-of-turn recall, compared with 95.60% for a Silero timing policy.
                                              The deployed system therefore retains a hybrid controller rather than claiming a learned-policy replacement. Across three unscripted
                                              operator-run microphone sessions, 36 measured response turns had a 758 ms median from final VAD endpoint to first server audio;
                                              21 turns were below 800 ms. These sessions are an instrumented case study, not a controlled user evaluation. We release the
                                              synthetic data, model artifacts, evaluation code and summaries, source code, and deployment configuration supporting the result.

                                         Keywords: streaming voice agents, turn-taking, synthetic data, causal streaming inference, speech synthesis, tool use, deployment


                                         1 Introduction                                                               interruption, backchannel resumption, stale-generation re-
                                         A conventional voice assistant is often drawn as a serial                    jection, and audible-only history;
                                         pipeline: automatic speech recognition (ASR), then a lan-                  • private speculative generation integrated with streaming
                                         guage model, then text-to-speech (TTS). That abstraction                     ASR, Qwen, Kyutai TTS, and sequential tool rounds in a
                                         hides the interaction problem. A usable conversational sys-                  public scale-to-zero deployment; and
                                         tem must decide whether a silence is a completed turn or a
                                                                                                                    • released synthetic tool-use and turn-taking corpora, trained
                                         within-turn hesitation; react immediately when speech begins
                                                                                                                      artifacts, evaluation code and result summaries, and an
                                         during playback without canceling on every short acknowledg-
                                                                                                                      instrumented 36-turn latency case study.
                                         ment; ensure canceled audio cannot reappear; and distinguish
                                         generated text from speech that actually reached the listener.               The contributions are systems and evaluation contributions.
                                            Here, full duplex means that microphone ingestion contin-              The paper does not claim that the adapter is a new state of the art,
                                         ues during assistant playback, playback can react reversibly to           that synthetic evaluation measures general tool competence,
                                         detected user speech, and generation, synthesis, and acknowl-             or that the microphone sessions estimate population-level
                                         edged audio are managed concurrently.                                     interaction quality.
                                            Voice-Light retains a cascaded architecture because its
                                         boundaries expose typed tools, playback state, and cancella-              2 Related work
                                         tion. Its central design rule is that uncertain work may begin            Turn-taking and endpointing. TurnGPT predicts turn com-
                                         early, but it may become audible or durable only after explicit           pletion from text [3]; Voice Activity Projection (VAP) predicts
                                         causal checks. This rule connects three otherwise separate                future speaker activity directly from conversational audio [4];
                                         problems: turn inference must not inspect future audio, spec-             and acoustic–language-model fusion shows that lexical and
                                         ulative generation must remain private until promotion, and               prosodic evidence can be complementary [5]. Recent turn
                                         conversation history must contain only speech acknowledged                benchmarks further emphasize that endpointing, backchannels,
                                         by the listener’s browser.                                                and interruption vary with conversation type [6, 7]. Voice-
                                            The study asks three questions. First, can a small causal              Light does not propose a general turn-taking architecture. It
                                         adapter reuse features from a persistent streaming ASR en-                asks whether a small causal adapter can share the encoder
                                         coder and improve turn commitment over deployable timing                  already used for streaming ASR and whether its evidence
                                         baselines? Second, can a reversible controller exploit uncertain          remains useful after a locked comparison with complete de-
                                         evidence without turning every VAD onset into cancellation?               ployable policies.
                                         Third, how much response latency can private speculation hide
                                         in a deployed ASR–LLM–TTS cascade?
                                            The paper makes four scoped contributions:                             Full-duplex spoken agents. End-to-end systems such as
                                                                                                                   Moshi jointly model user and assistant speech and avoid ex-
                                          • a shared-encoder causal turn-taking adapter, together with             plicit ASR–LLM–TTS boundaries [8]. A cascade instead
                                            locked evaluations that report both the learned signal and             exposes intermediate text, typed tools, playback state, and
                                            its failure to replace stronger timing baselines;                      component failures. Voice-Light uses those boundaries to
                                          • a typed hybrid controller for reversible ducking, floor-taking         make overlap reversible, reject stale work, and construct history


                                                                                                               1
                                                                                                                         Tool providers
                                                                                                                           and search
                                                                                                                          summarizer

      Browser mi-                                               Streaming               Hybrid commitment
                                   Silero onset                                                                           Qwen3-4B
       crophone                                              Nemotron ASR                  and specula-
                                 reversible duck                                                                          typed tools
     16 kHz PCM                                            shared encoder taps              tion policy

                                                                                                                        Dedicated GPU
                                                              Causal adapter                Browser play-
                                                                                                                         Kyutai TTS
                                                               completion /                  back clock
                                                             floor / feedback               and acknowl-
                                                                                              edgments

Figure 1: Production runtime. Immediate acoustic reaction and learned interaction evidence meet at a typed controller. Tool calls and results
use a structured loop; acknowledged browser playback is authoritative for durable assistant history.


from acknowledged audio. Its latency results are system mea-             4.1 Synthetic spoken tool use
surements and are not directly comparable with model-internal            Spoken tool use was treated as a data and protocol
latency reported for end-to-end architectures. Speculative end-          problem rather than a prompt-only feature. A pinned
turn detection has also combined local and remote detectors              Qwen3.6-27B-FP8 teacher generated provider-neutral records
[9]; here, speculation means privately preparing downstream              for natural conversation, drafting, brainstorming, search, cal-
text and PCM before a final turn commitment.                             culation, time queries, sequential calls, and correction or
                                                                         recovery. The published corpus contains 3,999 conversations,
                                                                         11,810 user messages, 15,308 assistant messages, and 3,498
Synthetic tool use. Toolformer and ToolLLM construct su-
                                                                         structured calls across search, calculate, and get time.
pervision for API selection and multi-step execution [10, 11].
                                                                         It is available through the project collection on Hugging Face
The Voice-Light tool branch addresses a narrower spoken
                                                                         [27].
protocol: short audible bridges, causally ordered call/result
                                                                             Generation used a causal conversation state machine. The
records, sequential calls, and suppression of protocol markup.
                                                                         teacher produced a user turn and then either assistant speech
Its shared-generator holdout measures acquisition of that pro-
                                                                         or speech followed by a typed call. The controller executed
tocol, not general tool use or factual retrieval.
                                                                         or synthesized the result, appended the linked call and result,
                                                                         and only then requested the next assistant step. Calculator
3 System overview                                                        and time results were deterministic. Synthetic search results
Figure 1 shows the deployed data path. The browser streams               came from the teacher, not the live web; consequently, the
16 kHz microphone PCM over one WebSocket and acknowl-                    corpus teaches call ordering and grounding to supplied text,
edges rendered audio ranges. Silero provides the earliest                not factual retrieval quality.
acoustic onset signal. A persistent Nemotron worker produces                 The canonical JSONL is semantic rather than tokenized. It
streaming transcripts and exposes selected encoder layers to             stores runtime tool definitions, audible assistant text, typed
the causal adapter without loading a second speech backbone.             calls, stable identifiers, outcomes, later turns, split metadata,
The controller combines those signals with transcript revisions,         provenance, and hashes. The run pins the teacher revision,
playback state, and conservative deadlines. Qwen generates               prompt revision, source commit, scenario seeds, quantization,
speech and typed calls; Kyutai TTS [17] synthesizes only text            and time anchor. Structural checks retained schema validity,
released by the controller.                                              causal call/result order, deterministic tool checks, spoken-
   Four invariants define the system. All learned turn features          length limits, and protocol-leak detection. Subjective teacher-
are causal and share the ASR stream. Speech onset may duck or            based rejection was disabled after manual review found its
pause playback immediately, but only stronger lexical, learned,          false positives counterproductive.
or timeout evidence commits cancellation. Speculative text
and PCM carry generation identifiers and remain private until            4.2 Synthetic conversational turn-taking audio
transcript and turn checks promote them. Finally, generated              The second generator models coherent conversation timelines
assistant text becomes durable conversation context only to              rather than isolated completion utterances. Typed plans dis-
the extent that browser acknowledgments show it was audible.             tinguish five semantic conditions: genuine user completion,
                                                                         a HOLD pause followed by continuation, non-floor feedback
4 Training data                                                          during assistant speech, a response after the assistant yields,
                                                                         and deliberate interruption. The plan also contains ordinary
The project produced two model-training branches. The
                                                                         event-free user, assistant, and silence spans.
language-model branch generated typed spoken-tool conversa-
                                                                            Only user audio is synthesized. Virtual assistant text keeps
tions for a Qwen adapter. The turn-taking branch combined
                                                                         the scenario coherent and estimates assistant duration, but
synthetic interaction timelines with automatically prepared
                                                                         assistant waveform never becomes an input artifact. The
human conversations for a causal speech adapter. Figure 2
                                                                         runtime-relevant assistant-speaking probability is compiled as
shows where the branches remain separate and where they
                                                                         a causal state curve with ramps, dips, and bounded noise. This
meet the deployed system.


                                                                     2
            Pinned 27B teacher              3,999 canonical                Qwen3-1.7B
            and typed scenarios          tool-use conversations          LoRA experiment



          Typed interaction plans
                                          Dense causal frames
             and synthesized
                                               at 80 ms
               user speech



           Licensed two-speaker         ASR, VAD, alignment,             Frozen Nemotron                   Locked evaluation
           human conversations            regions, review                 causal adapter                  and deployed hybrid

Figure 2: Two model-training branches feed one evaluated deployment. The turn-taking branch combines synthetic interaction timelines with
separately prepared human evidence; the language-model branch uses synthetic typed conversations.


prevents future assistant state or clean synthetic timing from         Table 1: Human conversational material in the locked corpus manifest.
leaking into the adapter.                                              Source audio remains subject to its original access terms; only derived
   The accepted rendering route used Qwen VoiceDesign                  manifests and code are distributed by the project.
references to condition CosyVoice 3 zero-shot voices [19, 18].
                                                                        Material                                     Conversations    Hours
Each user unit was rendered and trimmed independently; the
compiler then measured its active speech, assembled the final           MagicHub                                                 8     2.77
                                                                        TurnBench                                               37     7.31
timeline, and rasterized 20-second views into 250 frames at             Additional authorized material                          62    26.22
80 ms. A planned pause became HOLD supervision only if
                                                                        Total                                                  107    36.30
the rendered unit contained at least 500 ms of silence followed
by resumed speech.
   The public synthetic repository [30] stores lossless speech
units and reconstruction metadata rather than duplicating              corpus quality was tracked through the automated evidence
every composed waveform. Plans, voice provenance, trim                 pipeline.
measurements, composition seeds, split assignments, and
checksums allow conversation audio and training crops to               5 Model adaptation
be rebuilt. The retained V4 and V5 manifests contain 1,092
and 1,097 timelines, approximately 21.84 and 21.80 hours of            5.1 A language adapter for spoken tools
source timeline respectively. These counts describe retained           The tool-use experiment fine-tuned Qwen/Qwen3-1.7B [13]
run manifests, not a claim that synthetic interaction validation       with a BF16 rank-16 LoRA [12]. Two source records from each
substitutes for natural conversation.                                  combination of eight behavior families and five speech styles
                                                                       formed a balanced 80-record validation split; the remaining
4.3 Automatic preparation of human conversations                       3,919 records were training data. Across 16 deterministic
The human pipeline separates three artifact layers: authorized         passes, every record appeared once per pass. Intact short
source audio, recording-level evidence, and materialized train-        segments were regrouped into histories with 8–16 user turns,
ing windows. Each complete speaker track is stored once                producing 14,391 training histories and 17.84 million rendered
as lossless FLAC. Typed Parquet rows reference bounded                 tokens, of which 6.86 million were assistant targets.
20-second intervals and contain aligned inputs, targets, and              The native Qwen chat template rendered the canonical
masks; they do not duplicate the recording.                            records with thinking disabled. The loss mask retained or-
   Ingestion registers and hashes both channels, reuses exact          dinary assistant speech, the spoken bridge preceding a call,
cached transcripts, transports only missing material, applies          structured call tokens, post-result continuation, and later as-
a reviewed inter-speaker offset, and persists a full-duration          sistant turns. System text, tool definitions, user messages,
annotation and quality result transactionally. Multiple ASR and        tool results, padding, and non-assistant protocol tokens were
activity systems provide independent evidence for consensus            masked. The adapter targeted all attention and MLP projec-
alignment, channel-aware crosstalk filtering, conversation             tions, trained 17.43 million parameters, and completed 904
regions, and quality flags. Supplied TurnBench annotations             optimizer steps in 47 minutes on an RTX 4090.
remain an independent evidence source rather than being                   The public deployment uses Qwen3-4B Instruct [14]; the
copied into model-output fields to manufacture agreement.              trained 1.7B LoRA remains a released experimental artifact
   The completed preparation pass accepted eight MagicHub              [28, 29]. Section 6 reports why the synthetic protocol result
conversations (about 2.77 hours) [20] and 37 Mundo Turn-               was not treated as evidence of general conversational quality.
Bench conversations (about 7.31 hours) [6]; a silent TurnBench
recording was excluded. These additions joined previously              5.2 A causal adapter on shared Nemotron features
prepared authorized conversational material. The locked cor-           The turn-taking model attaches approximately 183,000 train-
pus manifest records 107 accepted conversations totaling 36.3          able parameters to the frozen Nemotron Speech Streaming
hours across conversation-disjoint train, validation, and test         0.6B encoder [16]. Nemotron is a cache-aware streaming
splits. A manual pipeline-validation audit reviewed 12 dataset-        FastConformer-RNNT. Its activation caches allow new non-
stratified recordings and applied targeted exclusions; broader         overlapping chunks to reuse prior work [1, 2]. This property


                                                                   3
made it possible to share one streaming backbone between                        Table 3: Balanced synthetic holdout for Qwen3-1.7B. The same 160
ASR and turn inference rather than re-encoding a rolling                        states were decoded with three seeds. Expected calls, no-tool states,
waveform or loading a second 0.6-billion-parameter model.                       and continuations contribute 210, 90, and 180 repeated predictions
                                                                                respectively; percentages therefore do not represent independent
   The adapter taps encoder layers 6, 12, 18, and 24. Each
                                                                                tasks.
1,024-dimensional tap is normalized and projected to 32 di-
mensions; the streams are fused to 64 dimensions, processed by                   Behavior                                                     Base    Fine-tuned
residual causal depthwise-separable convolutions, combined
                                                                                 Correct tool decision                                    80.0%            95.2%
with assistant-speaking state, and passed through a single-layer                 Exact tool name                                          78.6%            94.3%
64-dimensional unidirectional GRU. Separate heads emit com-                      Valid argument schema                                    80.0%            95.2%
                                                                                 Concise 1–12-word bridge                                  7.6%            94.3%
pletion/yield evidence, interaction events including floor take                  Correctly avoided a tool                                 70.0%           100.0%
and non-floor feedback, and future activity. Convolution and                     Valid post-tool continuation                             98.3%           100.0%

recurrent state persist incrementally and reset with the ASR
stream.                                                                                              1.2
   Synthetic pretraining selected step 2,250. Human fine-

                                                                                   Validation loss
tuning warm-started those weights with a fresh optimizer, 15%
synthetic replay, and 1,884 human boundaries: 1,038 HOLD                                              1
                                                                                                                   loss minimum
and 846 end-of-turn (EOT) examples. The resulting 750-step
checkpoint was selected on human validation.                                                         0.8
   The final adapter-best.pt is step 750, with the pinned
Nemotron revision listed in Table 6, one lookahead token,                                                  2   4      6      8     10    12          14     16
80 ms encoder frames, and the four taps above. Human                                                                Completed training pass
validation selected it; synthetic validation could not. At
runtime, forward hooks capture the exact features produced                      Figure 3: Recorded assistant-token validation loss after each logical
by persistent streaming ASR. A bounded latest-value queue                       pass. The directly comparable zero-update loss was 4.5398 and is
supersedes stale adapter work, and loading or inference failure                 omitted to preserve resolution. Loss bottomed after pass 4, then rose
degrades the predictor without stopping ASR or the voice                        even while free-generation protocol metrics improved.
session.
   The offline protocols evaluate several checkpoints with
                                                                                post-result continuations. These descriptive gains demonstrate
different roles. Section 6 keeps those roles explicit rather than
                                                                                acquisition of the generator’s conversational protocol. They
transferring results between artifacts.
                                                                                do not establish factual accuracy, robust web search, or general
                                                                                tool intelligence because evaluation points share the training
6 Offline evaluation                                                            generator and schema.
6.1 Protocols and checkpoint lineage
                                                                                6.3 Causal turn-completion results
The project uses separate evaluation protocols for separate
claims. Tool-use evaluation measures behavior on held-out                       Synthetic pretraining exposed the transfer problem directly.
synthetic conversation states. Turn completion has two non-                     Completion AUROC was 0.9260 on 893 held-out synthetic
comparable protocols: the original V1 benchmark scores                          examples but 0.5646 on 789 clean human validation labels.
future silence under a yield-oriented target and opens a locked                 Human fine-tuning raised human AUROC to 0.5972. At its
test split only after policy selection on validation, whereas                   selected validation policy, the deployed step-750 checkpoint
V2 scores semantic completion at speech boundaries. V2                          reached 65.04% EOT recall (426/655), 3.73% false cutoffs
stopped at validation because no detector met its predefined                    (5/134 HOLD cases), and 2.0 s p95 commitment latency.
deployment gate, so its test split remained sealed. Deployment                  These are validation results, not locked-test results, and the
evidence is an operator-run microphone case study, not a                        head remained a poor standalone probability estimator.
substitute for a controlled conversational study.                                  For the policy metrics below, a HOLD candidate is a silence
                                                                                followed by continuation from the same speaker, while EOT
Table 2: Turn-adapter checkpoint lineage. Parenthesized values                  denotes a completed user turn. False cutoff is the fraction of
are training steps. “Validation” and “test” name distinct locked                HOLD candidates committed as EOT; EOT recall counts com-
inventories; evidence is not transferred between artifacts.                     pleted turns committed before the timeout. Latency measures
                                                                                the causal delay from the candidate boundary to commitment,
Checkpoint (step)             Role and evidence                                 capped by the earlier of the timeout or the observed opportunity
Synthetic (2,250)             Pretraining seed; synthetic and human vali-       end.
                              dation                                               The locked V1 test contains 1,673 causal silence candidates
Historical (3,500)            V1 locked test and V2 validation                  from 11 conversations, including only 37 HOLD cases. Thresh-
Human fine-tune (750)         Deployed adapter; human validation and run-
                              time only
                                                                                old, minimum delay, and timeout were selected on validation
Completion challenger (625)   Later experiment; V2 validation only              and frozen before test. Table 4 shows the central negative
                                                                                result: the Voice-Light checkpoint preserved a low false-cutoff
                                                                                rate but crossed its learned threshold on only 205 of 1,636
6.2 Synthetic tool-protocol results                                             EOT cases. Most turns therefore used the 800 ms timeout, and
The final adapter emitted 200/210 expected calls, 198/210 exact                 the learned policy did not beat the Silero or LiveKit timing
tool names, 200/210 schema-valid arguments, 198/210 concise                     baselines. This test evaluates historical step 3,500, not the
bridges, 90/90 correct no-tool responses, and 180/180 valid                     deployed step-750 adapter.


                                                                            4
   The detectors do not score after identical amounts of silence.          tool completion, producing a deterministic mid-preamble stall.
Voice-Light emits its boundary score at 80 ms, Smart Turn                  The final design avoids that stall but can retain a short acoustic
at 240 ms, LiveKit at 320 ms, and Silero updates a silence                 seam at the semantic boundary. Before synthesis, a narrow
proxy on 32 ms chunks. Comparisons therefore evaluate                      text-boundary filter removes Markdown formatting, quotation
complete causal policies at their native gates rather than                 marks, and emoji that Kyutai would otherwise pronounce
isolating model quality under identical acoustic evidence. The             poorly; the durable generated text remains unchanged.
implementations are pinned to Silero VAD 6.2.1, Pipecat                       A separate Qwen3-0.6B worker [15] summarizes web results
Smart Turn v3.2, and LiveKit v1-mini [21, 22, 23].                         so provider output does not occupy the main conversation
                                                                           worker. Tavily latency varied from approximately 234–408
Table 4: Locked real-conversation test under the original V1 yield-        ms in several calls to roughly 1.98–2.29 seconds in slower
target protocol. Mean latency includes timeout actions. VL is              observations. External provider time is therefore reported
historical Voice-Light step 3,500; policy values are threshold, min-
                                                                           separately from first-response latency.
imum delay, and timeout. Possible training-source overlap makes
Smart Turn contextual only.                                                7.3 Hybrid overlap policy
Metric                                  VL    Silero   Smart LiveKit       Silero remains the immediate acoustic authority. When user
False cutoff                          2.70% 2.70% 13.51% 2.70%
                                                                           speech begins during assistant playback, the browser fades
HOLD errors (𝑛 = 37)                       1      1      5      1          toward -15 dB over 450 ms and pauses by 500 ms. This
EOT recall                           12.53% 95.60% 20.72% 91.50%
Mean latency                         770 ms 656 ms 684 ms 654 ms
                                                                           response is reversible: onset alone does not discard gener-
Threshold                               0.90   0.05   0.95   0.15          ation. A floor-take probability above the configurable 0.82
Minimum delay                        560 ms 640 ms  80 ms 640 ms
Timeout                              800 ms 800 ms 800 ms 800 ms
                                                                           threshold can commit interruption and cancellation. A non-
                                                                           floor-feedback probability above 0.82 becomes actionable after
                                                                           the short speech burst ends and resumes the same generation
   The V2 semantic-completion validation inventory contains                without adding a user turn. Explicit stop, repair, question, or
1,005 soft targets and 789 clean hard labels: 134 HOLD and                 meaningful lexical evidence provides another fast path.
655 EOT examples, with 216 ambiguous cases excluded from                      Ambiguous overlap is bounded. Sustained speech commits
hard scoring. Historical step 3,500 achieved AUROC 0.6866,                 floor taking after 900 ms, while a short ended burst resolves
65.80% recall, 3.73% false cutoffs, and 2.0 s p95 latency. Its             conservatively as non-floor feedback. Empty or slow final
BCE of 0.6719 and Brier score of 0.1843 were worse than                    ASR receives a 120 ms grace rather than parking playback
the constant soft-prior baseline (0.5847 and 0.1453), despite              indefinitely. Generation and TTS budgets are held after 350
above-chance ranking. No swept detector met the joint gate                 ms of unresolved overlap, and paused audio remains resumable
of at most 5% false cutoff, at least 70% recall, and at most               for at most 800 ms. A committed interruption rejects new
800 ms p95 latency, so the V2 test split remained sealed.                  server PCM immediately and fades no more than 100 ms of
A completion-primary retrain improved calibration but still                already-buffered audio.
missed the gate; longer training reduced recall.                              The adapter catches up from bounded pre-roll after Silero
                                                                           detects user activity, using the same persistent Nemotron
7 Streaming controller and deployment                                      stream once active. This preserves one backbone and strict
7.1 Speculation and cancellation                                           causality while limiting the acoustic context available at the
                                                                           earliest overlap decision.
After 80 ms of low Silero speech probability, the adapter
receives another 80 ms opportunity to open a speculative                   7.4 Two GPUs and scale to zero
response candidate. If learned evidence is not ready, a Silero
                                                                           Production requests a co-located pair of A10 GPUs, with an
fallback may start at 160 ms. Candidate text and PCM remain
                                                                           L40S pair as the capacity fallback. GPU 0 runs Nemotron, the
private until final ASR and transcript-revision checks permit
                                                                           adapter, Qwen3-4B, and the small search summarizer. GPU
promotion. Revisions limited to case, punctuation, whitespace,
                                                                           1 is reserved for Kyutai. Moving Nemotron beside Kyutai
or apostrophes preserve work; lexical change invalidates it.
                                                                           improved Qwen first-delta latency by roughly 25–30 ms but
   The system uses generation identifiers, cancellation barriers,
                                                                           regressed Kyutai first-word-to-PCM in small warm traces:
and rebased sample positions to reject stale text or PCM.
                                                                           346–353 ms with dedicated TTS (𝑛 = 3) versus 459–486
Playback clocks and boundary acknowledgements return every
                                                                           ms in the alternate placement (𝑛 = 5). Because first audible
80 ms. Durable assistant history is constructed only from
                                                                           speech dominates perceived response time, the dedicated-TTS
audio ranges that the browser confirms it rendered; generated
                                                                           topology was retained; the traces are engineering placement
but canceled words remain diagnostic evidence rather than
                                                                           checks rather than statistical tests.
conversation content.
                                                                              Modal [24] is a thin wrapper around the provider-neutral
7.2 Tool execution and speech boundaries                                   compute application. Model revisions and the adapter are
                                                                           pinned; Hugging Face and Torch caches live on a persistent
Structured tools support calculation, current time, and web
                                                                           volume; serving operates offline after initialization. Model
search, including sequential rounds. Tool execution can overlap
                                                                           subprocesses persist inside a warm container.
with bridge audio already buffered in the browser. Kyutai,
                                                                              The final topology loads Nemotron, Qwen, Kyutai, and the
however, requires text lookahead. The bridge must therefore
                                                                           search summarizer concurrently after the small VAD is ready.
be closed before awaiting a tool result, and the result begins
                                                                           Cached weights prevent downloads but not image scheduling,
a second TTS utterance within the same assistant generation.
                                                                           imports, CUDA initialization, or framework startup. Observed
Reusing one uninterrupted TTS session was implemented and
                                                                           cold readiness remains approximately 32–55 seconds. GPU
reverted because it could strand the last bridge words until


                                                                       5
snapshots failed for the multi-process CUDA layout, and an                p95 claims or independently quantify interruption, duck, or
import-only CPU snapshot added about 30 seconds. Keeping                  backchannel-resume latency.
a container warm was rejected for the expected low visit
frequency and cost.                                                       9 Observability and reproducibility
                                                                          The browser’s diagnostic stream separates model evidence from
8 End-to-end latency case study                                           durable conversation. Its rolling 20-second view records user-
The deployment case study comprises three unscripted mi-                  speech and assistant-audible lanes, raw adapter outputs, Silero
crophone sessions run by one operator from a browser in                   state, applicability, causal audio time, age, inference latency,
Germany against the scale-to-zero service in Modal’s Euro-                policy decisions, and browser acknowledgments. The adapter
pean region. Measurements begin after the service reported                heads were not independently calibrated as probabilities of
readiness and therefore exclude cold start. Prompts covered               observable conversational behavior; their values are therefore
ordinary conversation, longer responses, interruptions, short             retained as engineering telemetry rather than presented as
acknowledgments, calculations, current information, and se-               behavioral results. Figure 4 limits the paper view to directly
quential tool use. The final VAD endpoint is the last speech              observable speech and playback activity.
boundary used for turn commitment; first server audio is the                 Concrete reproducibility artifacts accompany each bound-
first PCM packet sent for the response.                                   ary: immutable serialized schemas reject extra fields; manifests
   Across 36 measured response turns, the median final-VAD-               retain seeds, input hashes, configuration, metrics, and check-
to-first-server-audio latency was 758 ms; 21/36 turns were                point identity; locked evaluation files carry content hashes
below 800 ms, and the range was 528–1,652 ms. One session                 and detector provenance; and build and test commands are
exported the complete telemetry trace for 13 turns. In that               recorded with pinned model revisions. Deployment packages
subset, median endpoint commitment was 502 ms, LLM first                  the final adapter and mounts persistent model caches without
word 336 ms after generation start, TTS first PCM 444 ms                  committing credentials. Table 6 identifies the final runtime
after its first word, and server-to-browser render 95 ms. These           snapshot and principal pins.
component intervals overlap and must not be added.                           The public artifacts include the tool-use dataset, LoRA,
   Nine of the 13 fully traced turns promoted speculative                 merged 1.7B checkpoint, and synthetic turn-taking audio [27,
work. Their median final-VAD-to-first-server- audio latency               28, 29, 30]. Human conversational audio remains restricted by
was 667 ms, compared with 1,513 ms for the four turns                     its source terms. The source repository contains generation,
without promotion. This observational split is consistent with            preparation, training, and evaluation code; narrative result
speculation hiding downstream work, but candidate success is              summaries; the runtime and browser; and Modal deployment
confounded with transcript stability and turn difficulty; it is not       runbooks. Large prediction inventories and restricted source
a causal estimate of an 846 ms speedup. Kyutai’s fixed first-             audio are not public artifacts.
frame computation remained the largest warm downstream
cost.

Table 5: Deployment case-study measurements. Aggregate response
latency covers three sessions; component medians come from the
13-turn fully exported trace and overlap in time.

 Measurement                                   Observed value
 Sessions / measured turns                              3 / 36
 Final VAD to first server audio, median               758 ms
 Final VAD to first server audio, mean                 932 ms
 Final VAD to first server audio, range          528–1,652 ms
 Turns below 800 ms                                    21 / 36
 Fully traced turns                                         13
 Final VAD to endpoint commitment, me-                 502 ms
 dian
 Generation start to LLM first word, me-                336 ms
 dian
 TTS first word to first PCM, median                    444 ms
 Server audio send to browser render,                    95 ms
 median
 Final VAD to browser render, median                    836 ms


  The original 250–600 ms engineering target was not met
consistently. The 800 ms line became a practical develop-
ment reference, not a population target. The sessions were
neither scripted nor blinded, involved one operator, and omit
users, acoustic conditions, accents, and networks outside the
development setting. They do not justify population p50 or


                                                                      6
Figure 4: Observable activity during a 20-second excerpt from an interactive microphone session. Green spans show detected user speech and
gold spans show acknowledged assistant playback. The session exercised short backchannels and a floor-taking interruption, but the lanes
intentionally do not assign semantic labels to individual overlaps.


10 Discussion and limitations                                              The negative result is equally central: the historical learned
The principal result is not a learned endpointer that replaces          completion policy did not beat simple deployable timing
silence timing. It is a bounded way to integrate uncertain              baselines on the locked real-conversation test. Instrumentation
learned evidence into a streaming controller. Immediate onset           therefore changed the design rather than being used to justify
remains acoustic, early reactions are reversible, private work          the original model. The resulting contribution is a reproducible
is discarded safely, and a deadline provides progress when the          hybrid system and a set of explicit evidence boundaries for
learned model is late or unavailable. This separation allowed           future controlled turn-taking evaluation.
the adapter to remain an optional signal after its standalone
completion policy failed the locked gate.                               References
   The experiments also expose two transfer failures. Syn-               [1] D. Rekesh et al., “Fast Conformer with Linearly Scalable
thetic turn pretraining produced strong in-domain ranking but                Attention for Efficient Speech Recognition,” arXiv:2305.05084,
transferred weakly to human completion labels. Synthetic                     2023.
tool fine-tuning improved a shared-generator protocol holdout            [2] V. Noroozi et al., “Stateful Conformer with Cache-based
but did not establish general reasoning or retrieval quality.                Inference for Streaming Automatic Speech Recognition,”
Qwen3-4B was selected for deployment after an engineering                    arXiv:2312.17279, 2023.
integration review, not a controlled model-quality comparison.           [3] E. Ekstedt and G. Skantze, “TurnGPT: A Transformer-based
Together, these results argue for measuring learned compo-                   Language Model for Predicting Turn-taking in Spoken Dialog,”
nents at the boundary where they will be used rather than                    Findings of EMNLP, 2020.
inferring deployment value from training-domain metrics.                 [4] E. Ekstedt and G. Skantze, “Voice Activity Projection: Self-
   Several limitations constrain the evidence. The locked                    supervised Learning of Turn-taking Events,” Interspeech, 2022.
V1 turn test contains 11 conversations and only 37 HOLD
                                                                         [5] J. Wang et al., “Turn-taking and Backchannel Predic-
cases, so one error changes false cutoff by 2.70 percentage                  tion with Acoustic and Large Language Model Fusion,”
points and candidates within a conversation are correlated.                  arXiv:2401.14717, 2024.
Possible training-source overlap prevents a clean Smart Turn
                                                                         [6] A. Jiang et al., “TurnBench: A Benchmark for Turn-Taking in
superiority comparison. V2 excludes 216 ambiguous cases
                                                                             Spoken Dialogue Systems,” arXiv:2608.25218, 2026.
and lacks the planned independent human label audit. Most
importantly, the deployed step-750 adapter was not evaluated             [7] G.-T. Lin et al., “Full-Duplex-Bench v1.5: Evaluating Overlap
on the locked V1 test, and its floor-take and backchannel heads              Handling for Full-Duplex Speech Models,” arXiv:2507.23159,
                                                                             2025.
have not been calibrated against an independently annotated
natural-conversation test set.                                           [8] A. Défossez et al., “Moshi: A Speech-Text Foundation Model
   The deployment study adds only three unscripted sessions                  for Real-Time Dialogue,” arXiv:2410.00037, 2024.
from one operator. It is not a user study and does not establish         [9] H. Ok, S. Yoo, and J. Lee, “Speculative End-Turn Detector for
naturalness, interruption accuracy, or latency distributions                 Efficient Speech Chatbot Assistant,” ACL, 2026.
across users, accents, noise, echo, networks, or GPU types.             [10] T. Schick et al., “Toolformer: Language Models Can Teach
The system is English-first, human audio remains restricted                  Themselves to Use Tools,” arXiv:2302.04761, 2023.
by source terms, and factual generation depends on a small
                                                                        [11] Y. Qin et al., “ToolLLM: Facilitating Large Language Models
language model and external retrieval. A stronger evaluation                 to Master 16000+ Real-world APIs,” arXiv:2307.16789, 2023.
would use conversation-disjoint human labels, participant-level
confidence intervals, controlled overlap scenarios, and final-          [12] E. Hu et al., “LoRA: Low-Rank Adaptation of Large Language
                                                                             Models,” arXiv:2106.09685, 2021.
topology action latencies. A learned policy should replace the
hybrid controller only if it improves the latency-versus-false-         [13] A. Yang et al., “Qwen3 Technical Report,” arXiv:2505.09388,
cancel frontier on that evidence.                                            2025.
                                                                        [14] Qwen Team, “Qwen3-4B-Instruct-2507,” model card, 2025.
11 Conclusion                                                           [15] Qwen Team, “Qwen3-0.6B,” model card, 2025.
Voice-Light demonstrates an artifact-backed path from causal            [16] NVIDIA, “Nemotron Speech Streaming English 0.6B,” model
conversational data to a public full-duplex cascaded agent                   card, 2026.
[25, 26]. The system shares streaming ASR features with a               [17] Kyutai, “TTS 1.6B English/French,” model card, 2025.
small turn adapter, prepares responses speculatively, executes
                                                                        [18] Z. Du et al., “CosyVoice 3: Towards In-the-wild Speech Gen-
typed tools, controls playback reversibly, and records only
                                                                             eration via Scaling-up and Post-training,” arXiv:2505.17589,
acknowledged audio as durable assistant history. Its three-                  2025.
session case study shows sub-second median server response
while retaining scale-to-zero deployment.                               [19] H. Hu et al., “Qwen3-TTS Technical Report,” arXiv:2601.15621,
                                                                             2026.


                                                                    7
[20] MagicHub, “Multi-stream Spontaneous Conversation Training          [26] B. Braun, “Voice-Light source code, data-generation pipelines,
     Datasets (English),” dataset description.                               evaluation records, and deployment documentation,” 2026.
[21] Silero Team, “Silero VAD,” software and model documentation.       [27] B. Braun, “Voice-Light synthetic tool-use dataset.”
[22] Pipecat AI, “Smart Turn v3,” model card.                           [28] B. Braun, “Voice-Light Qwen3-1.7B tool-use LoRA.”
[23] LiveKit, “Turn Detector,” documentation.                           [29] B. Braun, “Voice-Light Qwen3-1.7B merged tool-use check-
[24] Modal Labs, “Modal Documentation.”                                      point.”

[25] B. Braun, “Voice-Light live demo.”                                 [30] B. Braun, “Voice-Light synthetic turn-taking audio.”




                                                                    8
A Reproducibility snapshot

Table 6: Principal revisions, hashes, and recorded validation for the final runtime. Full commands and additional hashes are recorded in the
repository runbooks [26].

Artifact                           Revision, hash, or recorded result
Report source                      Committed TeX, figure assets, and build instructions in the source repository
Runtime source snapshot            e2f79adc on master; evaluated two-GPU deployment d78115d2
Qwen3-4B-Instruct-2507             cdbee75f17c01a7cc42f958dc650907174af0554
Qwen3-0.6B summarizer              c1899de289a04d12100db370d81485cdf75e47ca
Nemotron Streaming 0.6B            ebe59e5a817142986528bbbee5dba8db7b38ed50
Kyutai TTS 1.6B                    f65439609986c392cb12df63938abcc550c3fb15
Deployed adapter step 750          SHA-256 d5c8e02c61dc9c230eac57992278383b81f14e3b71935b8dc684fe5da4171011
Release engineering checks         630 Python tests (1 skipped, 1 integration deselected), 38 browser tests, Ruff clean; not scientific evaluation


A.1 Build and validation commands
The release PDF is built from the committed source. From the repository root on Windows, the recorded validation sequence is:

.\.venv\Scripts\ruff.exe format --check --exclude .cache .
.\.venv\Scripts\ruff.exe check --exclude .cache .
.\.venv\Scripts\python.exe -m pytest tests\voice_agent tests\training\turn_taking
    -m "not integration" --import-mode=importlib
node --test tests\browser\*.test.mjs
tectonic --outdir output\pdf docs\technical-report\voice-light-technical-report.tex

  Model-dependent integration tests and the deployed microphone acceptance session require the documented external services,
GPU environment, and uncommitted credentials; they are not implied by the local command sequence above.




                                                                          9

