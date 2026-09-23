# A frontend-backend architecture for tool calls in full-duplex speech models
Source: https://arxiv.org/pdf/2609.19334
Kind: pdf
Fetched: 2026-09-20T10:29:59.579340+00:00
Tool: pdftotext

                                         A FRONTEND-BACKEND ARCHITECTURE FOR TOOL CALLS IN FULL-DUPLEX SPEECH
                                                                      MODELS

                                                            Ke Hu, Slyne Deng, Chen Chen, Elena Rastorgueva, Edresson Casanova,
                                                     Punit Kumar, Dharmendra Choudhary, Nikhil Srihari, Ameya Sunil Mahabaleshwarkar,
                                                                 Viet Anh Trinh, Slim Essid, Oluwatobi Olabiyi, Zhehuai Chen

                                                                                                          NVIDIA, USA

                                                                      ABSTRACT                                        ters and context budget that text-only LLMs can devote to factual




arXiv:2609.19334v1 [cs.CL] 16 Sep 2026
                                                                                                                      knowledge, instruction following, and tool-call capabilities [26].
                                         Full-duplex speech-to-speech (S2S) models provide natural, low-              In contrast, a delegation-style backend agent is more modular and
                                         latency conversational interaction and would benefit from the ability        consumes little modeling capacity from a frontend speech model.
                                         to use external tools and complete voice-agent tasks. We propose                  In this direction, hybrid approaches that keep an S2S frontend
                                         a frontend-backend architecture where a duplex speech-to-text fron-          for interaction and delegating tool calling and reasoning to a text
                                         tend learns to emit a delegation token and forwards streaming ASR            backend appear in several concurrent designs: KAME [26] injects
                                         transcripts to a text-based backend LLM for tool calls. Tool-call re-        backend “oracle” tokens into a Moshi-style [4] S2S frontend for
                                         sults from the backend are injected back into the frontend through a         knowledge integration; MoshiRAG [27] augments Moshi with re-
                                         lightweight prefill-and-repeat mechanism and then synthesized us-            trieval; Thinking Machines [28] proposes an interaction-background
                                         ing streaming TTS to the user. Our approach largely preserves reg-           framework for user queries requiring deeper reasoning, tool calls,
                                         ular duplex turn-taking, interruption handling, and low-latency in-          or long-horizon work. More recently, Qwen-audio-agent [29] and
                                         teraction as it requires minimal modifications to the frontend model.        GPT-Live [30] also adopt similar frameworks. However, it remains
                                         In a single-turn tool-call evaluation, our system achieves 92-97%            unclear how the delegation signal in [28, 29, 30] is designed and
                                         tool-call recall, competitive tool-call prediction performance, and          background model interacts with the duplex frontend.
                                         81.2% accuracy in rejecting irrelevant calls. When equipped with                  In this work, we propose a frontend-backend architecture for ex-
                                         a larger backend (e.g., Qwen3-235B-A22B), our system achieves                ecuting tool calls and agentic tasks for a full-duplex speech model.
                                         competitive results on Full-Duplex-Bench-V3 compared to open and             Our S2S model consists of a duplex speech-to-text (STT) component
                                         closed source models, and significantly outperforms GPT-realtime-            (based on [6, 31]) and a streaming TTS [32]. The duplex STT model
                                         mini and Qwen3-Omni-30B-A3B-Instruct on EVA-Bench. These                     takes user speech encoding, agent text and streaming user ASR tran-
                                         results demonstrate that backend delegation is an effective and mod-         script as inputs [31]. We use the duplex STT model as the frontend:
                                         ular approach for combining natural duplex speech interaction with           it predicts a delegation token for voice queries involving tool calls,
                                         strong agentic tool-call capabilities.                                       and then sends the streaming ASR transcripts to the backend LLM,
                                                                                                                      which handles the tool call in a LangGraph framework [33]. The
                                                                 1. INTRODUCTION                                      backend’s natural-language result is then sent back to the frontend
                                                                                                                      agent text channel via a prefill mechanism and the frontend is then
                                         Full duplex speech-to-speech (S2S) models are natural and desirable          trained to repeat the result. The frontend remains silent during the
                                         interfaces for conversational AI [1, 2, 3, 4, 5, 6, 7, 8, 9]. By operating   tool calls and resumes its normal duplex behavior after the tool call is
                                         directly in the speech modality, these models eliminate cascade la-          completed. Our design imposes minimal changes on the frontend du-
                                         tency, preserve paralinguistic cues, and produce natural turn-taking         plex STT model by adding a tool-call control token to its prediction
                                         and barge-in behavior [10, 11, 12, 13]. While duplex speech mod-             targets. In a single-turn tool-call evaluation based on a speech ver-
                                         els excel in natural conversation based on internal intelligence, text-      sion of BFCL [34], our experiments show that the frontend-backend
                                         based LLMs now serve as reliable tool-using agents: Instruction-             architecture reliably predicts the tool-call token with 92% to 97%
                                         tuned models decide when and how to invoke external tools, query             recall, and rejects irrelevant calls up to 81.2%. On more natural-
                                         knowledge bases, and act on the world [14, 15, 16, 17, 18, 19].              istic user queries with pauses, hesitations, and self-corrections in
                                              Although there is increasing effort enabling spoken tool calls in       Full-Duplex-Bench-V3 [35], our model based on the Qwen3-235B-
                                         speech LLMs [20, 21, 22, 1, 23], tool-call capabilities in voice agents      A22B backend achieves response quality similar to GPT-realtime-
                                         remain substantially behind those of text-based agents. As shown             mini. On the more challenging EVA-Bench voice-agent task eval-
                                         in τ -Voice [24], leading commercial duplex voice models complete            uation [36], which involves multi-turn conversations and tool calls,
                                         only 31−51% of grounded customer-service tasks under clean con-              our model significantly outperforms GPT-realtime-mini and Qwen3-
                                         ditions, whereas text agents such as GPT-5 achieve 85% on the cor-           Omni-30B-A3B-Instruct [37], and performs similarly to Gemini 3.1
                                         responding text-mode tasks; the gap widens further under realistic           Flash Lite [38]. Demos of our frontend-backend system can be found
                                         noise and accented speech. This disparity suggests that natural spo-         online.1
                                         ken interaction and strong tool-call intelligence remain largely sep-
                                         arate strengths of current systems. A natural question is therefore                                 2. RELATED WORK
                                         whether duplex speech models should directly internalize tool-call
                                         capabilities or instead delegate such capabilities to a backend text         Cascaded frontend–backend systems, such as NVIDIA’s Nemotron
                                         agent that already benefits from mature instruction following, tool          Voice Agent [39] and LiveKit’s EXA Deep Researcher [40], com-
                                         calls, and long-horizon reasoning abilities.                                 bine ASR, LLM, and TTS into a frontend and use a separate back-
                                              Recent work investigates tool-call capabilities directly inside         end for planning and tool execution. Recent systems increasingly
                                         Moshi-style [4] duplex speech models by placing tool calls in a              explore tool use and backend agents into real-time voice interaction.
                                         separate channel [25]. However, audio-native modeling imposes
                                         a fundamental capacity tradeoff: audio tokens consume parame-                   1 https://huggingface.co/spaces/frontend-backend-duplex/demo
                     Agent Speech
                                                                                               performed by the backend, and we just prefill the tool call response
                                                                                               in the training data into the agent text channel and train the frontend
                Streaming TTS                                                                  to reproduce it exactly. The tool-call tokens, filler, and reproduced
          Agent Text                                                                           regions are used for loss computation in the same way as for regular
                                                              Prefill
          <turn-1>      <silence>     <turn-2>                                                 agent text, while prefill regions are masked and excluded from loss
       No (<agent_bos>)                                                                        computation. During inference, we send the streaming ASR tran-
                                        Yes (<tc_bos>)
                       Tool Call?                                                              script to the backend for tool call execution when <tc eos> fires.
                                                                Backend LLM
                                                                                               The backend returns the acutual natural-language text to the fron-
                                                                             User text         tend to prefill (see Sect. 3.2 for details). Our frontend is connected to
                       Text head                          <silence>     <turn_1>   <silence>   VoiceChat-TTS [32] to generate agent speech, which accepts explicit
                                                                                               turn start and interruption control tokens and incrementally generates
             Decoder-only LLM                                        ASR head                  codec-based speech tokens.

                        Pooling
                                                                                               3.2. Backend agent
         <turn-1>         <silence>       <turn-2>    Agent text
         <silence>        <turn-1>        <silence>      User text                             We use LangGraph [33], a tool-augmented ReAct agent [16], as
         <silence>        <turn-1>        <silence>                                            our backend. Our graph is a state machine over a running message
                                                                                               list, comprising an agent node that employs an instruction-following
          Streaming Speech Encoder                                                             LLM and a tools node that executes the model’s tool calls. The two
                                                                                               nodes are linked by a conditional edge that routes to tool execution
                               User speech                                                     whenever the model emits calls and terminates the turn once the turn
                                                                                               contains no tool calls. When the user query requires a tool call, e.g.,
Fig. 1. The proposed frontend-backend system for a duplex speech-                              “what is the weather in New York?”, the user ASR transcript is sent
to-speech model with tool-call capability.                                                     to the graph as a message, and the agent is invoked to call tools to
                                                                                               respond. Multi-turn context is maintained automatically by a thread-
Commercial systems [30, 1, 41] expose tool calls inside an end-to-                             keyed checkpointer that persists and restores the accumulating con-
end voice API, but their architectures are not disclosed. Recent work                          versation state across turns, so each turn only takes the current user
focuses on pairing a low-latency full-duplex speech frontend with a                            ASR transcript as input.
more capable text backend. KAME [26] runs a Moshi-style fron-                                        If the backend generates a syntactically invalid tool-call request
tend and conditions its output on “oracle” tokens streamed from a                              or a regular text response, we return the text directly to the fron-
backend LLM updated every 100–500 ms; the frontend is explicitly                               tend as prefill. This means the frontend may have misfired a tool-
trained to anchor its speech on these oracle tokens. MoshiRAG [27]                             call request, while the larger backend reliably falls back to natural-
augments Moshi with retrieval, injecting retrieved context into the                            language explanations for irrelevant queries.
inner-monologue stream. Thinking Machines adopts an interaction-
background style system to delegate deep reasoning, tool calls, or
longer-horizon jobs to the background model [28]. Recently, Qwen-                                              4. TRAINING AND INFERENCE
audio-agent [29] is proposed as a realtime voice model with backend
agents which can execute various tasks while the frontend is in a con-                         For the frontend duplex STT model, our training includes a pretrain-
versation with the user. However, in [28, 29], it is unclear how the                           ing stage followed by supervised fine-tuning (SFT) [42]. To enable
delegation signal is designed or backend results are integrated into                           tool-call token prediction in the frontend, we generate multi-turn
the frontend duplex model.                                                                     conversation data with tool calls for SFT. First, we use various LLMs
     Compared to the aforementioned approaches, we propose a                                   (e.g., Nemotron 3 Nano [45], Gemma-4-31B-IT [46], and Qwen3.5-
straightforward approach to predict a delegation token in the agent                            397B-A17B [47]) to generate user, agent, tool call and tool response
text channel to assign tool calls to a backend. The backend exe-                               turns in text, and use LLM judges to filter conversations with in-
cutes multiple rounds of tool calls, and then prefills the response                            consistent turns or incorrect tool invocations. These textual conver-
text to the frontend as context for further generation. The pro-                               sations are then synthesized into audio conversations using a data
posed frontend-backend framework is modular and does not need                                  pipeline involving filtering (e.g., removing math-heavy and code-
significant architecture changes for the frontend.                                             heavy conversations not suitable for audio), TTS (VoiceChat-TTS
                                                                                               [32] with diverse voices), ASR (Parakeet-tdt-0.6b-v2 [48]) based
                                                                                               quality filtering using WER/CER. The multi-turn tool call data has
                               3. ARCHITECTURE                                                 variants targeting voice-agent decisions about when to call a tool,
                                                                                               when to ask follow-up questions, and when not to call an unavailable
3.1. Speech-to-text frontend                                                                   or inappropriate tool, similar to When2Call [49] but with multi-turn
As shown in Fig. 1, our frontend model is a duplex speech-to-text                              speech user input. Our pipeline also simulates realistic multi-turn
(STT) model which consists of a streaming speech encoder and the                               interactions with backchannels, pauses, and interruptions. We have
LLM backbone (similar to [42]). The duplex STT model takes three                               also constructed domain-based multi-turn tool call data (e.g. simu-
input streams: user speech, user transcript, and agent text. User                              lated airline and retail databases) with entities distinct from evalua-
speech is encoded by a 600M-parameter Parakeet streaming speech                                tion. We generate conversation and tool-calling trajectories by hav-
encoder [43] and fed to a backbone LLM (NVIDIA Nemotron-                                       ing two text-only LLMs interact with each other (both are Qwen3.5-
Nano-9B-v2-Base [44]). The streaming ASR head consists of a                                    235B-A22B [50]) to achieve diverse user goals. Samples that failed
separate embedding layer and prediction head, and share the same                               to complete the task are discarded, and we synthesize the user turns
LLM backbone as the agent text head. A single decoding pass                                    into speech using Chatterbox [51]. In total, our training data con-
jointly produces both user and agent text.                                                     sists of around 530k hours of pretraining data, 111k hours of SFT
     To delegate tool calls to the backend, we train the frontend model                        data, around 16k hours of ASR transcription data, and 8.5k hours of
to fire a tool-call token <tc bos> in the agent text channel if the                            multi-turn conversation data with tool calls. When training the fron-
user speech naturally requires a tool call (e.g., “what is the weather in                      tend, we randomly choose either the full tool definition as the system
New York?”). We then train the model to first generate a short filler                          prompt or a partial prompt with only function name and description
followed by the special token <tc eos>. Actual tool calls will be                              for generalization.
Table 1. BFCL AST accuracy (%) and irrelevance score. UV0.6-                Table 2. FDB3 results; “–” is N/A. Boldface marks group bests.
8B and UV0.6-32B denote Ultravox-v0.6 with Llama-3.1-8B and                 Ours-235B-extASR denotes our system with the Qwen3-235B-
Qwen-3-32B backbones, respectively. Ours-7B uses Qwen2.5-7B,                A22B backend and external ASR. ∗ Judged with no timing.
Ours-30B uses Qwen3-30B-A3B.                                                Model                    Tool-acc↑ Arg-acc↑ Pass@1↑ Res-Q↑ TT↑ Inter↓ Filler↓
Model                 Simple Multiple Parallel Para. Multi. Irrelev. Avg    GPT-realtime-mini [57]       77.4     58.2    51.0    62.0 93.0 14.2 17.2
                                                                            GPT-realtime                 88.7     71.6    61.0    74.7 95.0 13.5 12.1
GPT-realtime             82.9     83.6    72.5         74.0   90.8 80.8
                                                                            Gemini-3.5 Flash [19]        97.0     72.5    65.0    88.0     –    – 1.0∗
UV0.6-8B                 61.4     63.5    48.5         43.0    0.0 43.3     UV0.6-8B                     59.1     39.0    11.0    19.0     –    – 2.0∗
UV0.6-32B                78.9     81.1    75.2         65.4   82.5 76.6     UV0.6-32B                    84.3     52.2    45.0    71.0     –    – 12.0∗
                                                                            Ours-30B-extASR              74.6     52.8    44.0    54.0 100.0 54.0 84.8
Ours-7B-intASR           80.2     79.6    69.5         52.7   76.7 71.7
                                                                            Ours-235B-extASR             71.7     55.2    48.0    67.0 100.0 51.0 83.3
Ours-30B-intASR          79.4     78.3    71.1         55.1   81.2 73.0
Ours-30B-extASR          80.1     78.7    72.0         61.1   81.2 74.6
                                                                            models, and we label the best score in bold for each group. Our sys-
     In training, if a user query leads to a tool call, we label the fol-   tem with the 7B backend substantially outperforms Ultravox-v0.6
lowing agent turn as a tool-call turn, along with the final natural-        Llama-3.1-8B in average score (71.7 vs. 43.3). For Ultravox-v0.6-
language tool-call response. We first place a <tc bos> token to re-         Llama-3.1-8B, we use post-hoc type normalization to coerce string-
place a regular <agent bos> token, which is usually 320 ms after            typed JSON arguments to their schema types. The score of 0.0 on
the end of the user turn (as in [42, 6, 31]), then followed by the filler   Irrelevance is because it invokes the single offered function on all
(∼1s duration) and then <tc eos>. The natural-language tool re-             240 prompts. For GPT-realtime, we use semantic VAD and feed the
sponse is then enclosed by <pf bos> and <pf eos> and prefilled              user speech turn to generate the tool-call request. As shown in Table
into the agent text channel around 1s after the <tc eos> to simulate        1, our 30B backend setup performs close to GPT-realtime on some
the tool call executation time, and the frontend model is trained to        subsets, however the largest gap is on Parallel-Multiple, followed by
generate the exact prefilled text starting with <agent bos>. Dur-           Irrelevance. We also compute tool-call token recall as the fraction
ing training, we insert pad tokens to the ASR channel and silence to        of positive tool-call utterances for which the frontend correctly fires
speech regions as inputs with prefilled agent text, and these regions       the delegation token. Our frontend achieves recall of 97.2%, 92.0%,
are not used for loss computation. An example training sequence             95.0%, and 93.5% on Simple, Multiple, Parallel, and Parallel Multi-
looks like:                                                                 ple, respectively.
User: What is the weather in New York?
Agent: <pad>320 ms [ <tc bos> Give me a moment. <pad>... <tc eos> ]1 s
<pad>1 s <pf bos> The weather in New York is 72 degrees <pf eos>            5.1.2. Full Duplex Bench v3
<agent bos> The weather in New York is 72 degrees <pad>...                  Whereas BFCL contains continuous and fluent TTS-generated user
    At inference, once the frontend fires the tool-call detection to-       speech, Full-Duplex-Bench v3 (FDB3) [58] consists entirely of nat-
ken, the user transcript, endpointed by <user eos>, is sent to the          uralistic real human recordings. The corpus contains 100 scenarios
backend to complete the tool-call request. The resulting natural-           from 12 speakers, recorded with everyday built-in microphones in
language response is then injected into the agent-text channel before       environments ranging from quiet rooms to mild background noise.
further generation. During the function call, we suppress the agent         Mock APIs are used to generate tool-call results. In evaluation, we
output by inserting pad tokens in the agent text channel.                   follow the official FDB3 setup to use GPT-4o as the LLM judge [35],
                                                                            along with the original system prompts and tool descriptions. In
                            5. RESULTS                                      this evaluation, we stream our user speech to the frontend chunk by
                                                                            chunk as in live conversation. Since our frontend is an STT model,
5.1. Tool Calls                                                             we use agent text for computing Res-Q, TT and Inter. We also re-
                                                                            produced other model’s results using their text outputs in Table 2.
5.1.1. Single-Turn Tool Calls                                                    Table 2 reports tool selection accuracy (Tool-acc), argument
We use the audio version of the Berkeley Function-Calling Leader-           accuracy (Arg-acc), response quality (Res-Q), end-to-end task-
board (BFCL) [52] single-turn datasets from ServiceNow-AI [34]              completion (Pass@1), turn-taking rate (TT), interruption rate (Inter),
for evaluation. The single-turn datasets include Simple, Multiple,          and filler rate (Filler). We remove end-to-end latency because our
Parallel, Parallel-multiple, and Irrelevance subsets. We use the Ab-        backends may run either as local vLLM instances or from cloud
stract Syntax Tree (AST) score to evaluate the structural correctness       APIs, and latencies are not comparable. The turn-taking latency of
of the generated tool-call request. We follow the original AST im-          our frontend model is separately evaluated in Sect. 5.3.
plementation [53], which tolerates argument order, spacing and for-              As shown in Table 2, our systems fulfill the user’s request (Res-
matting differences, and default parameters in AST scoring.                 Q) at around 54%-67%. A larger backend (Qwen3-235B-A22B)
     As shown in Table 1, we evaluate our system with backend               performs better as expected. Our model achieves 100% turn-taking.
LLMs of two different sizes: Qwen2.5-7B [54] and Qwen3-30B-                 Our high Filler rate is by design: the frontend emits a short hold
A3B [37]. We also compare two methods for transcribing user                 phrase (“Let me pull that up”) before the backend executes the tool
speech: our internal ASR (intASR) transcripts and an external ASR           call. Our high Inter rate has a different cause: the frontend typically
(extASR) model [43]. For external ASR, we transcribe the user               responds at pauses during the user’s disfluency with a backchannel
speech once the streaming ASR detects the user end. As shown in             (e.g., “Okay, I am here.”) before any tool call. Because it keeps
Table 1, we first find that the two Qwen3 backends with intASR              listening while speaking, the eventual tool call usually still sees the
perform similarly on Simple and Multiple, and the larger backend            complete user request (Res-Q up to 67.0).
performs better on Parallel and Parallel Multiple subsets, and rejects           We compare our systems to open-source and closed-source mod-
irrelevant speech more reliably. When we switch to external ASR             els in Table 2, where the Ultravox and Gemini models are grouped
transcripts for the Qwen3-30B-A3B, the average score improves               into a section representing turn-based speech models, and therefore
from 73.0% to 74.6%, with the biggest gain on Parallel-Multiple             the TT and Inter metrics are not applicable. Our models perform
(55.1% → 61.1%) due to more accurate ASR transcripts. We will               signficantly better than Ultravox-v0.6 Llama-3.1-8B since the model
use the external ASR setup in later experiments.                            produced no response in many scenarios. Ultravox-v0.6 Qwen-3-
     We also compre to GPT-realtime [1], Ultravox-v0.6 with Llama-          32B performs better than our systems since it is a turned based model
3.1-8B [55] and Qwen-3-32B [56] backbones in Table 1. We orga-              and will not emit premature tool calls. For GPT-realtime and mini
nize Ultravox models in a different section since they are turn-based       we use the semantic VAD and take their text output for evaluation.
Table 3. EVA-Bench [36] results. Values are percentages except            Table 4. Turn-taking and barge-in (BI) on our internal benchmark.
TT (ms). Q3O-30B and G3.1-FL denote Qwen3-Omni-30B-A3B-                   Model               Pr↑/Rec↑ (%)      Lat.↓ (ms)      BI Acc.↑/Lat.↓ (%/ms)
Instruct and Gemini 3.1 Flash Lite, respectively.                         Baseline (no TC)        85/94            423                100/403
Model            EVA-A↑ EVA-X↑ Task↑ Faith↑ Prog.↑ Concise↑ Speak↑ TT↓    Ours (frontend)         82/91            438                 99/395
GPT-5.2 (text)      63.3   80.8 78.4 48.1 73.2         77.6    91.6   –
GPT-RT-mini         33.1   71.2 37.1 29.1 46.5         77.5    89.7 535   Table 5. Spoken-language intelligence. Scores are in a 5-point scale.
GPT-RT2             59.4   75.7 68.1 50.7 63.9         72.7    90.5 435
Q3O-30B             29.1   72.7 32.5 25.7 46.9         77.5    93.7   –       Model                 OpenbookQA (%)↑          AE (/5)↑   CE (/5)↑
G3.1-FL             45.6   75.3 57.1 34.2 53.1         78.9    93.8   –       Baseline (no TC)            65.0                3.54       2.87
UV0.6-8B [55]        8.3   58.8 11.8    4.7 16.5       68.5    91.5   –       Ours (frontend)             64.7                3.61       2.36
UV0.6-32B [56]      31.2   54.5 36.2 26.3 55.2         68.2    40.1   –
Ours-30B-extASR     32.4   63.5 40.4 24.4 39.2         65.7    85.6 151
Ours-235B-extASR    46.6   74.7 57.3 35.9 53.5         77.6    93.0 352     Table 6. ASR word error rate for the Open ASR Leaderboard.
                                                                          Model            LS-C LS-O TED Vox Earn AMI Giga SPGI Avg
Compared to them, our results with Qwen3-235B-A22B backend are            Baseline (no TC) 3.93 8.59 5.89 8.90 20.00 20.45 13.45 5.15 10.80
similar to GPT-realtime-mini based on Pass@1 and Res-Q metrics,           Ours (frontend)  4.16 8.18 6.71 9.90 21.52 21.66 14.64 4.98 11.47
while GPT-realtime performs best on almost all metrics.
                                                                          Table 7. Full-Duplex-Bench v1 [10] results. Pause reports Candor
5.2. Voice Agent Tasks                                                    TOR. GPT score is out of 5.
                                                                                            Smooth TT (Candor)   Pause         User Interruption
Finally, we evaluate on EVA-Bench [36], an end-to-end frame-              Model            TOR (%)↑ Lat. (ms)↓ TOR (%)↓ TOR (%)↑ GPT score↑ Lat. (ms)↓
work for evaluating voice agent tasks on grounded, multi-domain           Baseline (no TC)    93        221       53.2    95.5       3.94        590
customer-service tasks. Our model’s EVA results are generated             Ours (frontend)     100        92       68.2    89.5       4.04        349
using the following setup. We simulate the caller using EVA’s
LiteLLMClient and use GPT-5.2 to role-play the caller. To                 performs in the ITSM (56.3% vs. 75%) and Medical HR (49.4%
adapt to our infrastructure and improve inference availability, we        vs. 69.9%) domains. In the latter two scenarios, the model needs
synthesize user text turns with Chatterbox-TTS [59], and the syn-         a chain of up to 6–8 successful tool calls to complete a task. This
thesized user speech is streamed chunk-by-chunk to the frontend           requires reliable tool-call detection from the frontend over a long
implemented using Triton Inference Server [60]. We use GPT-5.2 as         conversation.
the LLM judge for all metrics. To focus on evaluating our frontend
STT text output quality and also compare to other text and STT            5.3. Turn-Taking and Intelligence
models, we directly return agent text to the simulated user instead of    Lastly, we measure whether adding tool-call prediction abilities to
transcribed synthesized speech for our models and compared models         the frontend model impacts regular duplex conversation quality. We
in Table 3.                                                               evaluate the frontend on an internal multi-turn conversation set [42],
      For metrics, we report all 213 EVA-Bench scenarios across the       VoiceBench tasks [62], the Open ASR Leaderboard [63], and FDB-
airline, ITSM, and medical HR domains. Since we use text outputs          v1 [10]. In Tables 4, 5, 6, and 7, we compare the proposed model’s
from the agent, we adapt EVA-A and EVA-X metrics for evaluation.          performance on turn-taking, intelligence, streaming ASR, and FDB-
EVA-A is the average of Task and Faith(fulness), and we remove            v1 against baseline models without tool-call (TC) training. We fol-
Speech Fidelity, which measures TTS quality, since our frontend out-      low [42] for computing the metrics for the internal set. Overall, our
puts agent text. EVA-X is the average of Prog(ress), Concise(ness),       frontend model performs slightly worse in turn-taking precision and
and Speak(ability). We add Speakability to measure how friendly the       recall while performing similarly on the other metrics in Table 4.
agent text is as input to the TTS model. We also report Turn-Taking       It performs similarly on OpenbookQA and AlpacaEval (AE) while
separately as the last column in Table 3, but it is not used to compute   degrades a little on CommonEval (CE) as shown in Table 5. The
EVA-X because different backends and models use different imple-          streaming ASR WER degrades from 10.80% to 11.47% (Table 6),
mentations and their latencies are not strictly comparable.               presumably because the added tool-call training data are mostly syn-
      In Table 3, we compare EVA performance across the text-only         thetic. On FDB-v1 in Table 7, the model generally becomes more
model (GPT 5.2), GPT-realtime-mini [57], GPT realtime2 [61], turn-        responsive, with a higher TOR rate for smooth TT and lower la-
based speech models, and our frontend–backend systems. GPT-5.2            tency, but it also performs worse on pause handling. This can be
text-only is presented as a topline model, where we directly pass user    addressed by adding more training data with natural pauses, which
text to the model to obtain the agent text response. This ideal set-      are not present in the current SFT training.
ting performs best, with the highest EVA-A and EVA-X scores and a
task-completion ratio of 78.4%. We also run GPT-realtime-mini and                                  6. CONCLUSION
GPT-realtime2 in streaming mode using the semantic VAD setup and          We propose a frontend-backend architecture that enables a full-
return text outputs directly to the simulated user. GPT realtime2 per-    duplex model to perform tool calls and agentic tasks. Our frontend
forms significantly better than the mini on EVA-A. Our model with         model is trained to emit a tool-call token that signals the need for
Qwen3-30B-A3B backend performs similarly to GPT-realtime-mini             backend delegation, and the tool-response text from the backend
on EVA-A, and the Qwen3-235B-A22B backend achieves signifi-               is prefilled to the frontend as context for the further conversation.
cantly better EVA-A and EVA-X scores than GPT-realtime-mini but           Our results show that this architecture works with different back-
still lags behind GPT realtime2 on EVA-A.                                 end LLMs and achieves competitive results on tool-calling and
      For turn-based speech models in Table 3, we directly use the        voice-agent benchmarks.
full user speech as input. Our system with the Qwen3-235B-A22B
backend performs similarly to Gemini 3.1 Flash Lite and signif-
icantly outperforms Ultravox-v0.6 Qwen-3-32B [56]. Compared
                                                                          Acknowledgment
with Qwen3-Omni-30B-A3B-Instruct, our system with the Qwen3-              We thank Lily Lee, Nourchene Ferchichi, Harishchandra Dubey,
30B-A3B backend achieves higher EVA-A and task completion.                Yuanhang Su, Aditya Malte, Zijia Chen, Travis Bartley, Praise
For Qwen3-235B-A22B, the conciseness and speakability scores              Manzi, Hayley Ross, and Yoshi Suhara for their efforts, contribu-
are better than GPT realtime2, but task completion and faithfulness       tions, and support throughout this project.
lag behind. Actually in a more detailed analysis, we find that the            Claude Opus 4.8 and Codex with GPT-5.5 are only used to for-
Qwen3-235B-A22B backend achieves higher task completion in                mat tables and references and to fix grammatical errors throughout
the airline domain than GPT realtime2 (72% vs. 54%) but under-            the paper.
                       7. REFERENCES                                        tation, 2026, Accessed: 2026-09-15.
                                                                       [31] Edresson Casanova et al., “Open full-duplex voice agent with
                                                                            speech-to-speech language model,” in Proc. IEEE ASRU,
 [1] OpenAI, “Introducing gpt-realtime and realtime api updates
                                                                            2025.
     for production voice agents,” OpenAI, 2025, Accessed: 2026-
                                                                       [32] Edresson Casanova et al., “VoiceChat-TTS: A low-latency
     06-05.
                                                                            continuous speech synthesis model for interactive agents,”
 [2] Google, “Gemini Live API overview,” Google AI documenta-
                                                                            2026, arXiv:2608.13831.
     tion, 2026, Accessed: 2026-06-09.
                                                                       [33] LangChain, Inc., “LangGraph,” GitHub, 2024.
 [3] xAI, “Grok: Truth-seeking ai chatbot with voice and image
                                                                       [34] ServiceNow-AI, “BFCL v3 audio dataset,” Hugging Face,
     generation,” xAI, 2026, Accessed: 2026-06-09.
                                                                            2025.
 [4] A. Défossez et al., “Moshi: a speech-text foundation model for
                                                                       [35] Daniel Lin et al., “Full-duplex-bench v3,” GitHub, 2025.
     real-time dialogue,” 2024, arXiv:2410.00037.
                                                                       [36] T. Bogavelli et al., “EVA-Bench: A new end-to-end framework
 [5] NVIDIA et al., “PersonaPlex: Voice and role control for full
                                                                            for evaluating voice agents,” 2026, arXiv:2605.13841.
     duplex conversational speech models,” in Proc. ICASSP, 2026.
                                                                       [37] Qwen Team, “Qwen3-30B-A3B,” Hugging Face, 2025.
 [6] Ke Hu et al., “SALM-duplex: Efficient and direct duplex mod-
                                                                       [38] Google DeepMind, “Gemini 3.1 Flash-Lite model card,”
     eling for speech-to-speech language model,” in Proc. Inter-
                                                                            Google DeepMind, Mar. 2026, Accessed: 2026-09-11.
     speech, 2025.
                                                                       [39] NVIDIA,        “Frontend/backend agent cascaded example,”
 [7] Wenfu Wang et al., “Covo-Audio technical report,” 2026,
                                                                            GitHub, Accessed: 2026-09-11.
     arXiv:2602.09823.
                                                                       [40] LiveKit, “EXA Deep Researcher,” GitHub, Accessed: 2026-
 [8] NVIDIA, “Nemotron 3 VoiceChat,” NVIDIA model card, Mar.
                                                                            09-11.
     2026, Accessed: 2026-09-11.
                                                                       [41] Neel Joshi, “Turn your voice into action with new productivity
 [9] NVIDIA, “NVIDIA NemotronLabs VoiceChat 11B,” Hugging
                                                                            features in Gemini Live,” Google Blog, Aug. 2026, Accessed:
     Face, Aug. 2026, Accessed: 2026-09-11.
                                                                            2026-09-11.
[10] G.-T. Lin et al., “Full-Duplex-Bench: A benchmark to evalu-
                                                                       [42] Ke Hu et al., “Enabling streaming user transcription in full-
     ate full-duplex spoken dialogue models on turn-taking capabil-
                                                                            duplex speech-to-speech models,” 2026, arXiv:2609.15759.
     ities,” in Proc. IEEE ASRU, 2025.
                                                                       [43] NVIDIA NeMo Team, “Parakeet-TDT-0.6B-v3: A multi-
[11] G.-T. Lin et al., “Full-Duplex-Bench v2: A multi-turn evalua-
                                                                            lingual streaming speech recognition model,” Hugging Face,
     tion framework for duplex dialogue systems with an automated
                                                                            2025.
     examiner,” in Proc. ACL, 2026.
                                                                       [44] NVIDIA, “Nemotron-Nano-9B-v2-Base: A 9B Parameter
[12] Guojian Li et al., “Easy Turn: Integrating acoustic and lin-
                                                                            Language Model for Reasoning and Instruction Following,”
     guistic modalities for robust turn-taking in full-duplex spoken
                                                                            2025, Hugging Face Model Hub.
     dialogue systems,” 2025, arXiv:2509.23938.
                                                                       [45] NVIDIA et al., “Nemotron 3 Nano: Open, efficient mixture-
[13] HumDial Organizers, “The ICASSP 2026 HumDial chal-
                                                                            of-experts hybrid mamba-transformer model for agentic rea-
     lenge: Benchmarking human-like spoken dialogue systems in
                                                                            soning,” 2025, arXiv:2512.20848.
     the LLM era,” in Proc. ICASSP, 2026.
                                                                       [46] Google DeepMind, “Gemma-4-31B-it,” Hugging Face, 2026,
[14] T. Schick et al., “Toolformer: Language models can teach
                                                                            Accessed: 2026-09-14.
     themselves to use tools,” in Proc. NeurIPS, 2023.
                                                                       [47] Qwen Team, “Qwen3.5-397B-A17B,” Hugging Face, 2026,
[15] S. G. Patil et al., “Gorilla: Large language model connected
                                                                            Accessed: 2026-09-14.
     with massive APIs,” in Proc. NeurIPS, 2024.
                                                                       [48] NVIDIA, “Parakeet TDT 0.6B V2,” Hugging Face, 2025, Ac-
[16] S. Yao et al., “ReAct: Synergizing reasoning and acting in
                                                                            cessed: 2026-09-14.
     language models,” in Proc. ICLR, 2023.
                                                                       [49] NVIDIA, “When2Call Dataset,” Hugging Face, Accessed:
[17] S. Yao et al., “τ -bench: A benchmark for tool-agent-user in-
                                                                            2026-06-09.
     teraction in real-world domains,” 2024, arXiv:2406.12045.
                                                                       [50] Qwen Team, “Qwen3-235B-A22B,” Hugging Face, 2025.
[18] OpenAI, “GPT-5.5 model,” OpenAI documentation, 2026, Ac-
                                                                       [51] Resemble AI, “Chatterbox-TTS,” GitHub, 2025.
     cessed: 2026-06-09.
                                                                       [52] S. G. Patil et al., “Berkeley function calling leaderboard,”
[19] Google, “Gemini 3.5 Flash model,” Google AI documentation,
                                                                            BFCL leaderboard, 2024.
     2026, Accessed: 2026-06-09.
                                                                       [53] Shishir G. Patil et al., “Berkeley function calling leaderboard,”
[20] Ramit Pahwa et al., “Audio2Tool: Speak, call, act – a dataset
                                                                            GitHub, 2024.
     for benchmarking speech tool use,” 2026, arXiv:2604.22821.
                                                                       [54] Qwen Team, “Qwen2.5-7B-Instruct,” Hugging Face, 2024.
[21] Kimi Team et al., “Kimi-Audio technical report,” 2025,
                                                                       [55] Fixie.ai, “Ultravox-v0.6 Llama-3.1-8B,” Hugging Face, 2025,
     arXiv:2504.18425.
                                                                            Accessed: 2026-09-09.
[22] Qwen Team,           “Qwen3-Omni technical report,” 2025,
                                                                       [56] Fixie.ai, “Ultravox-v0.6 Qwen-3-32B,” Hugging Face, 2025,
     arXiv:2509.17765.
                                                                            Accessed: 2026-09-09.
[23] Google, “Gemini 3.1 Flash Live Preview,” Google AI docu-
                                                                       [57] OpenAI, “GPT-Realtime mini Model,” OpenAI documenta-
     mentation, 2026, Accessed: 2026-06-09.
                                                                            tion, Accessed: 2026-06-09.
[24] S. Ray et al., “τ -Voice: Benchmarking full-duplex voice agents
                                                                       [58] Guan-Ting Lin et al., “Full-Duplex-Bench-v3: Benchmarking
     on real-world domains,” 2026, arXiv:2603.13686.
                                                                            tool use for full-duplex voice agents under real-world disflu-
[25] Haoyang Zhang et al., “DuplexSLA: A full-duplex spoken lan-
                                                                            ency,” 2026, arXiv:2604.04847.
     guage model with synchronized speech, language, and action,”
                                                                       [59] Deokjin Seo, Gangin Park, and Kihyun Nam, “Chatterbox-
     2026, arXiv:2605.20755.
                                                                            Flash: Prior-calibrated block diffusion for streaming zero-shot
[26] S. Kuroki et al., “KAME: Tandem architecture for enhancing
                                                                            TTS,” 2026, arXiv:2605.30748.
     knowledge in real-time speech-to-speech conversational AI,”
                                                                       [60] NVIDIA Corporation, “Triton Inference Server: An optimized
     2025, arXiv:2510.02327.
                                                                            cloud and edge inferencing solution,” GitHub, 2026, Accessed:
[27] Chung-Ming Chien et al., “MoshiRAG: Asynchronous knowl-
                                                                            2026-06-08.
     edge retrieval for full-duplex speech language models,” 2026,
                                                                       [61] OpenAI, “GPT-Realtime-2 Model,” OpenAI documentation,
     arXiv:2604.12928.
                                                                            Accessed: 2026-06-09.
[28] Thinking Machines, “Interaction models: A scalable approach
                                                                       [62] Y. Chen et al., “VoiceBench: Benchmarking LLM-based voice
     to human-ai collaboration,” Thinking Machines, 2026, Ac-
                                                                            assistants,” 2024, arXiv:2410.17196.
     cessed: 2026-06-09.
                                                                       [63] Vaibhav Srivastav et al., “Open ASR Leaderboard: Towards re-
[29] Qwen Audio Team, “Qwen Audio Agent: A real-time voice
                                                                            producible and transparent multilingual and long-form speech
     runtime for AI agents,” GitHub, 2026, Accessed: 2026-09-11.
                                                                            recognition evaluation,” 2025, arXiv:2510.06961.
[30] OpenAI, “Getting started with GPT-Live,” OpenAI documen-

