# IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows
Source: https://arxiv.org/abs/2606.19595
Kind: pdf
Fetched: 2026-09-22T07:24:04.576624+00:00
Tool: pdftotext

                                             IHBench: Evaluating Post-Interruption Recovery
                                             in Voice Agents with Structured Workflows
                                             Ahmad Salimi        Wentao Ma              Yuzhi Tang         Dongming Shen        Mu Li               Alex Smola
                                             Boson AI                                                      Boson AI
                                             Toronto, ON, Canada                                           Santa Clara, CA, USA
                                             {ahmad,wentao,yuzhi}@boson.ai                                 {dongming,mu,smola}@boson.ai




arXiv:2606.19595v1 [cs.LG] 17 Jun 2026
                                             Voice agents deployed in structured workflows (customer service, healthcare scheduling, account management) must
                                             handle frequent user interruptions while maintaining progress through multi-step procedures. Existing benchmarks for
                                             speech-capable models focus on the timing of interruptions: barge-in detection, endpointing, and turn-taking dynamics.
                                             They leave unmeasured what happens after the interruption: does the agent resume the workflow at the correct step?
                                             Does it address the user’s interjection? Does it avoid re-delivering content the user already heard?
                                             We introduce IHB ENCH (Interruption Handling Benchmark), a benchmark that evaluates post-interruption recovery
                                             in voice agents executing state-machine-driven workflows across 10 enterprise domains. Six interruption types are
                                             injected at controlled points mid-utterance, with per-interruption evaluation rubrics generated alongside the data. Each
                                             interruption is scored on two axes: task fulfillment and recovery quality.
                                             We evaluate 27 audio-language model configurations from OpenAI, Google, and the open-weight community. Models
                                             vary widely, and recovery quality depends strongly on the interruption type. Across our experiments, closed-weight
                                             models are consistently more robust to interruptions than open-weight ones: they win far more often on task fulfillment,
                                             degrade roughly 3.3× more slowly as conversations grow longer, and show no audio-versus-text modality gap, whereas
                                             the open-weight models lose ground on all three. A human study validates the LLM judge against human annotators, and
                                             a cross-benchmark analysis against AudioMultiChallenge indicates that recovery quality is a largely distinct capability
                                             axis.
                                                                                               Blog    § Code         Data




                                         1   Introduction                                                       These benchmarks answer an important question: can the
                                                                                                                model detect and react to an interruption in real time? How-
                                                                                                                ever, a second question remains largely unanswered, espe-
                                         Real-time voice agents are rapidly moving from research                cially in the context of structured task workflows: what does
                                         prototypes to production deployments. Models such as GPT               the model say next?
                                         Realtime [28], Gemini [12], and Moshi [7] can now process
                                         and generate speech natively, enabling voice-first applications        Consider a voice agent guiding a user through an insurance
                                         in customer service, healthcare, and enterprise workflows. A           claim. The agent is mid-sentence explaining the required doc-
                                         defining characteristic of natural spoken conversation, one            umentation when the user cuts in: “Actually, it was my work
                                         that sharply distinguishes it from text chat, is interruption.         address, not home.” The agent must now (1) stop speaking,
                                         Users cut in mid-sentence to correct information, express              (2) recognize this as a correction of previously provided in-
                                         impatience, switch topics, or simply acknowledge with a                formation, (3) integrate the correction, (4) not repeat the part
                                         backchannel like “mm-hm.” In structured workflows, these               of its explanation the user already heard, and (5) resume the
                                         interruptions are not edge cases; they are the norm.                   workflow at the correct step. Existing benchmarks evaluate
                                                                                                                step (1). Steps (2)–(5) are the subject of this paper.
                                         A growing body of work evaluates how well speech models
                                         handle the mechanics of interruption. Full-Duplex-Bench                The distinction matters because the failure modes are qualita-
                                         [23] and its successors [21, 20, 38] measure whether mod-              tively different. A model that fails to stop speaking produces
                                         els stop speaking when interrupted, how quickly they yield             an awkward overlap, annoying but recoverable. A model
                                         the floor, and whether they distinguish genuine interruptions          that stops correctly but then re-reads its entire interrupted
                                         from backchannels. FLEXI [10] adds a topic-shift score.                sentence, ignores the user’s correction, or loses its place in
                                         SID-Bench [41] focuses on semantic-aware interruption de-              the workflow creates a fundamentally broken interaction. Fig-
                                         tection. HumDial [39] classifies post-overlap behavior into            ure 1 contrasts good and bad post-interruption recovery on
                                         respond/resume categories.                                             two such cases. In our evaluation, we find that current mod-
   Example A: Filler interruption (backchannel)                                               breakdown, degradation with conversation depth, and
                                                                                              audio-versus-text input modality), and verify our findings
   Æ Assistant: “. . . and there is elevator access from the                                  through inter-judge and human-judge agreement studies
   garage. Back —”                                                                            and a cross-benchmark comparison with AudioMultiChal-
      User (interrupts): “mm-hm”                                                              lenge [15] (Section 5).
   ✗ Bad response: “Before we continue, I just want to . . . ”
   Starts over after a simple backchannel, and jumps to a different workflow stage.       2    Related Work
   ✓ Good response: “to your registration, we still need to
   schedule your first appointment. Is now a good time?”                                  Full-duplex and turn-taking benchmarks. Recent bench-
   Continues exactly from where it was cut off.                                           marks evaluate speech-native models on real-time conversa-
                                                                                          tional dynamics. Full-Duplex-Bench (FDB) [23] evaluates
   Example B: Correction interruption                                                     user pause handling, interruption handling, model backchan-
                                                                                          neling, and smooth turn-taking. For interruption handling, it
   Æ Assistant: “Got it, I’ll use john.smith@example-                                     uses a single-turn audio input and mainly assesses whether
   company.com. Reading that back —”                                                      the model’s response is semantically relevant to the inter-
      User (interrupts): “Oh wait, sorry, no hyphen. It should be
                                                                                          ruption. FDB v1.5 [22] expands the test space to additional
   examplecompany as one word.”
                                                                                          overlap scenarios, but still uses single-turn audio inputs and
                                                                                          evaluates user interruption by whether the model responds to
   ✗ Bad response:                                                                        the interruption. FLEXI [10] also uses a single-turn interrup-
   “Sure, it’s john.smith@examplecompany.com. I’ll use that                               tion setup and evaluates whether the model shifts topic after a
   for the email.”                                                                        user interruption. SID-Bench [41] focuses on distinguishing
   Accepts correction but drops the workflow (was about to send summary).                 user interruptions from backchannels, HumDial [39] clas-
   ✓ Good response:                                                                       sifies post-overlap behavior as respond or resume, Talking
   “Got it, I’ll use john.smith@examplecompany.com. I’m                                   Turns [3] benchmarks turn-taking timing using a trained turn-
   sending the brief summary now with Jane Doe’s direct contact                           taking model as judge, and INSTRUCT-FD [38] tests whether
   and scheduling link.”                                                                  a full-duplex system follows explicit turn-taking instructions.
   Integrates correction and resumes the workflow.                                        These benchmarks characterize whether a model detects, re-
                                                                                          sponds to, shifts after, times, or follows instructions about
Figure 1: Good vs. bad post-interruption recovery on two                                  local overlap, but do not evaluate post-interruption recovery
IHB ENCH cases: a filler backchannel (A) and a correction                                 within a structured workflow.
(B). “—” marks where the user interrupted mid-utterance.                                  FDB v2 [21] uses GPT-Realtime [28] as an examiner for
                                                                                          multi-turn full-duplex evaluation, and is closest in spirit to
els, including frontier ones, exhibit gaps in post-interruption
                                                                                          our setting. Its interruptions are interjected at pauses sur-
recovery that are not captured by existing benchmarks. For
                                                                                          faced by a voice-activity detector, which keeps the interac-
example, all evaluated GPT-family audio models continue an
                                                                                          tion natural but places the cut-in at the model’s own turn
utterance correctly after a backchannel less than a third of the
                                                                                          boundaries rather than at controlled points mid-utterance;
time (filler pass rate between 7% and 31%), and the Gemini
                                                                                          the disruptions it studies also center on the correction case.
2.5 family is markedly better (62%–68%) although the newer
                                                                                          Our pipeline is complementary: because interruptions are
Gemini 3.x line regresses sharply (13%–32%). These are
                                                                                          scripted into the conversation rather than triggered by a voice-
not inherently difficult behaviors; rather, they appear to be
                                                                                          activity detector, they are not confined to detected pauses and
undertrained, suggesting that targeted evaluation can surface
                                                                                          can be injected at controlled positions partway through an
actionable training gaps.
                                                                                          utterance; it also spans six interruption types beyond cor-
Contributions. We make the following contributions:                                       rection, with per-interruption rubrics that make the result-
                                                                                          ing post-interruption recovery directly measurable. MTR-
1. We define post-interruption recovery as a distinct evalua-                             DuplexBench [47] also evaluates multi-turn interruption han-
   tion axis for voice agents, decomposed into six interrup-                              dling, but focuses on whether the model detects user inter-
   tion types, and propose a two-axis scoring for it: com-                                ruptions and stops speaking in free dialogue. FDB v3 [20]
   parative task fulfillment judging and absolute recovery                                evaluates tool-use accuracy under speech disfluencies, but
   quality assessment, both powered by LLM judges with                                    focuses on user self-corrections rather than user-initiated in-
   type-specific criteria (Sections 3.2 and 4).                                           terruptions of the agent. In contrast, our benchmark evaluates
2. We introduce IHB ENCH, a benchmark of synthetically                                    whether a voice agent can recover a structured workflow af-
   generated multi-turn conversations grounded in state-                                  ter disruptive mid-speech barge-ins, assessing type-specific
   machine workflows across 10 enterprise domains. Each                                   recovery behavior.
   conversation includes controlled interruptions with per-
   interruption evaluation rubrics generated alongside the                                Voice agents and workflow recovery benchmarks. A par-
   data (Section 3).                                                                      allel line of work evaluates task-oriented voice agents on
3. We evaluate 27 audio-language model configurations                                     end-to-end task completion: EVA-Bench [4], VoiceAgent-
   along several axes (overall scores, per-interruption-type                              Bench [16], VoiceBench [5], and SpokenWOZ [35] measure


                                                                                      2
     Prerequisites                                     Conversation Synthesis                                                                               Verification                                    Aui d o 
                                                                                                                                                                                                                                             va uation Sa                e
                                                                                                                                                                                                     
                                                                                                                                                                                                               Synthesis                  E     l                 mpl




                                                      assistant
                                                           Round Planner                Assistant 
                                                                                         Simulator                           Use
                                                                                                                              Simulator
                                                                                                                                         r 
                                                                                                                                                                         Verifier
                                                                                                                                                                                                                                   system: Y

                                                                                                                                                                                                                                 [   instructions
                                                                                                                                                                                                                                                  ou are a support ag
                                                                                                                                                                                                                                                       state mac ine
                                                                                                                                                                                                                                                     +            h
                                                                                                                                                                                                                                                                         ... 

                                                                                                                                                                                                                                                                         ]


        Domains                   Goal Generator                    plan                                                                                       list of issues with fix procedure
                               
                                                         user plan
                   interruption andlin                   interruptin                                                                                             

                                                                                                                                                                information leakage
                                                                          
                                                                                                      h        g
                             g 

                                                         interruption plan
                     vs
                                                                                                 .
                               vs.                                                                 e t ormali ation
                                                                                                                                                                                                     T x   N        z
                                                                                                                                                                                                                                                                   


                                                         termination signal                  normal                            normal                          conversation naturalness
               friendl
                                                                                                                                                               non-fixable signal
                                                                                                                                                                                                           TTS          y 

           K    no led e ase uilder
                    w     g   B       B                                                                                                                                                                 user messages            
             stages guidelines user info
                                                                                                                                                                                                                                       Perfect, I’ll send it to
                    ⋅             ⋅                                                        repeat
                                                                                                                                                                                                                                 john@gmail  [interrupted]




                                                                                                                                                                        Modifier
                                                                                                                                                                                                                                     Wait, actually, use my work




                                  User Intent                Rubric Generator
                                                                                                                                                                                                                                   email, john@company.com.

                                                                                                                                                                                                               
                                                                                                                                                                     list of modifications            e t to Speec                   Model under e aluation
      Assistant                reaction profile                  task fulfillment

                                                                                                                                                                                                      T x -    -             h
                                                                                                                                                                                                                                                       v



     Sys. Prompt
                                                                                                           interrupting?

                               description
                                                                                                                                                                                                                                   Got it, I’ll send it to your ...

                                                                  recovery quality
     knowledge base           interruption profile                                                                                                                up to iterations
    in natural language        attributes                                                                                                                                N

                                                                                                                                                                                                                                  Rubrics                  LLM Judge




Figure 2: The IHB ENCH data generation pipeline: prerequisites, conversation synthesis (with per-interruption rubrics), verifica-
tion, and audio synthesis. The rightmost panel shows one resulting evaluation sample. Each stage is described in Section 3.3.

spoken task success across enterprise domains, tool calling,                                                                                           an ordered workflow while a user interrupts with realistic
and dialogue state tracking. τ -voice [33] adds full-duplex                                                                                            spoken-language patterns; Figure 2 summarizes the full data
turn-taking dynamics through a voice user simulator. None                                                                                              generation pipeline, which we detail in the rest of this section.
of these, however, inject controlled interruptions or evaluate                                                                                         We describe the key design choices below.
post-interruption recovery. Closer to interruptions, Interrupt-
Bench [50] studies mid-task interruptions (additions, revi-                                                                                            3.1      Domains and Workflow Structure
sions, retractions) but on text-based web-navigation agents
rather than voice, and work on proactive, transition-aware                                                                                             Each conversation is grounded in one of 10 enterprise
agents [46] models text dialogue returning to task after digres-                                                                                       domains (SaaS, financial services, healthcare, telecom, e-
sions, again without speech-native disruptive interruptions.                                                                                           commerce, travel, education, government, subscription me-
Synthetic benchmark construction and evaluation. Our                                                                                                   dia, and professional services), selected through an LLM-
data generation pipeline builds on work using LLMs and                                                                                                 assisted, manually curated process. For each domain, we
multi-agent simulation to construct evaluation benchmarks.                                                                                             use an LLM to generate diverse assistant goals (e.g., “pro-
Self-Instruct [40] and Evol-Instruct [43] established iterative                                                                                        cess an insurance claim,” “upgrade a subscription plan”),
LLM generation with quality filtering, while MultiChallenge                                                                                            and for each goal, a structured knowledge base that defines:
[36] uses a multi-stage multi-agent pipeline with planner,                                                                                             (i) Ordered workflow stages: A sequence of states the as-
user, and responder agents to generate challenging multi-turn                                                                                          sistant must traverse (e.g., Authenticate Identity → Verify
conversations, followed by human review gates and post-hoc                                                                                             Account → Process Request → Confirm Changes). Each
binary evaluation questions. SOTOPIA [49] similarly simu-                                                                                              stage specifies skip conditions, failure handling, and termi-
lates multi-agent social interactions with independent agent                                                                                           nation conditions. (ii) Detailed guidelines: Domain-specific
policies, and Gao et al. [9] introduce a self-evolving pipeline                                                                                        rules the assistant must follow. (iii) Known user informa-
where judge agents critique intermediate artifacts to refine                                                                                           tion: Concrete, fictional data values (e.g., account numbers,
generation. Our pipeline follows this broader multi-agent                                                                                              billing addresses, plan details) that ground the conversation
design, but adapts it to structured workflow recovery: it gen-                                                                                         in specific facts rather than placeholders.
erates workflow-grounded conversations with controlled in-                                                                                             The assistant drives the conversation according to a structured
terruption points and fixes each item’s per-interruption rubric                                                                                        workflow and must reach a terminal outcome. This design
at construction time (before any model response exists), with                                                                                          ensures interruptions are a disruption to its plan rather than
a verify–modify loop that enforces state consistency, prevents                                                                                         a natural response to user queries, as would be the case in a
leakage, and validates recovery targets.                                                                                                               free-form conversation with a general-purpose assistant.
Our evaluation builds on LLM-as-judge methods and rubric-
based automatic evaluation, where LLM judges [48, 19] and                                                                                              3.2      Interruption Types
auto-generated criteria [18] achieve strong agreement with
human preferences. We apply this to interruption-specific                                                                                              We define six interruption types, each with distinct recovery
workflow recovery, using the per-interruption rubrics for both                                                                                         requirements:
randomized comparative judging and criterion-based absolute
recovery evaluation.                                                                                                                                   Normal. A relevant, cooperative cut-in where the user volun-
                                                                                                                                                       teers a new detail or constraint, or asks a quick clarification
                                                                                                                                                       (e.g., “By the way, I’ll need this done before Friday”); recov-
3        Benchmark Design                                                                                                                              ery requires addressing the interjection, then resuming the
                                                                                                                                                       workflow with a fresh start.
IHB ENCH evaluates how well voice agents recover after                                                                                                 Impatient. The user wants to speed up or skip explanations;
being interrupted during structured, multi-step workflows.                                                                                             recovery requires skipping the interrupted content and ad-
The benchmark consists of synthetically generated conver-                                                                                              vancing the workflow without re-explaining what was asked
sations where an assistant-led state machine drives through                                                                                            to skip.


                                                                                                                                                   3
Correction. The user corrects something they previously                3.4   Design Principles
said in a prior turn (e.g., “Actually wait, use my work email
instead”); recovery requires accepting the correction without          Several design choices are critical to the benchmark’s valid-
pushback, integrating the corrected value, and continuing.             ity:
Topic switch. The user introduces an unrelated request (e.g.,          No state-machine leakage. The user does not know the
“Oh by the way, can you check my outstanding invoices?”);              assistant’s internal workflow. Each agent in the pipeline is
recovery requires addressing the new topic, then steering              prompted to avoid leaking workflow internals into user utter-
back to the original workflow without blending the two.                ances, though all such shields rely on the underlying model’s
Filler. A brief backchannel that does not change the task              instruction-following capability. The final safeguard is the
(e.g., “mm-hm,” “yeah,” “right”); recovery requires exactly            post-hoc verifier (check G in Appendix I.6), which flags con-
continuing the interrupted utterance from where it was cut             versations where the user references internal stage names,
off, without repeating, restarting, or acknowledging the filler.       workflow order, or knowledge base details they could not
Pushback. The user challenges or resists the assistant’s claim         know.
or request (e.g., “I’m not comfortable giving that out over            Concrete values everywhere. All data in knowledge bases
the phone”); recovery requires empathetic de-escalation and            and user intents uses concrete, fictional values, never place-
offering alternatives.                                                 holders. This ensures conversations are grounded in specific
These types were chosen to span the space of interruption              facts that can be verified for correctness after interruptions.
intents observed in real customer-service conversations, from          Mid-stage interruptions. Interruptions are designed to oc-
cooperative (normal, filler) through directive (impatient, cor-        cur within workflow stages, not at clean boundaries between
rection) to adversarial (pushback, topic switch). The distribu-        them. This makes recovery non-trivial: the assistant must
tion of interruption types across the benchmark is reported in         determine where it left off within a stage, not simply start the
Appendix A.                                                            next one.
                                                                       Branched simulators. The assistant and user simulators
                                                                       use completely separate prompt branches for interruption-
                                                                       handling vs. normal turns, preventing cross-contamination of
                                                                       interruption awareness into non-interruption turns.
3.3   Conversation Generation Pipeline
                                                                       3.5   Audio Pipeline
Conversations are generated through a multi-stage pipeline
(Figure 2):                                                            For audio-input evaluation, each user utterance is text-
                                                                       normalized (expanding numbers, dates, currencies, and abbre-
Prerequisite generation. For each (domain, goal) pair, we              viations into spoken form), then synthesized to audio via TTS
generate a knowledge base, a system prompt, and multiple               with Whisper ASR [32] verification and retry logic, using
user intent profiles. Each user intent includes a behavioral           per-conversation voices from Common Voice [2].
profile (e.g., “cooperative but rushed”), an interruption prob-
ability distribution over the six types, and hidden user infor-
mation that may surface during the conversation.                       4     Evaluation Methodology
Round-by-round simulation. A round planner decides for
each turn what the assistant and user will do, whether an              Each interruption point becomes one evaluation sample: the
interruption occurs, its type, and where in the assistant’s ut-        model receives the system prompt and the conversation his-
terance the user cuts in. Separate assistant simulator and             tory truncated at the interruption, generates the next response,
user simulator agents then generate the actual spoken utter-           and is scored on two independent axes by LLM judges (Fig-
ances. The user simulator sees the full assistant message but          ure 2, rightmost panel).
is instructed to produce a truncated version showing the exact
                                                                       Task fulfillment (comparative). We compare the model’s
cutoff point; it must ensure that its utterance only reacts to
                                                                       response against a baseline response generated by GPT-4o
the truncated portion (what the user actually heard), prevent-
                                                                       Audio [25] from the same conversational context. Follow-
ing information leakage. This constraint is enforced both by
                                                                       ing standard win-rate evaluation [18], a comparative judge
prompt design and by the downstream verifier (check H in
                                                                       receives a single evaluation rubric, describing the next goal
Appendix I.6).
                                                                       the assistant should achieve after this interruption, and the
Rubric generation. For each interruption, a rubric generator
                                                                       two candidate responses in randomized order; it must pick a
produces a task fulfillment criterion (what the assistant should
                                                                       winner and name a concrete deficiency in the loser (“more
do next) and 2–4 recovery quality criteria (type-specific pass/-
                                                                       detail” or “longer” are not valid reasons). The metric is the
fail checks).
                                                                       task fulfillment win rate: the fraction of interruptions where
Verification and modification. A post-hoc verifier scans ev-
                                                                       the model’s response is preferred over the baseline. A score
ery message for naturalness violations, state-machine leakage
                                                                       of 0.50 indicates parity; scores above 0.50 indicate the model
(user referencing internal workflow stages), content from un-
                                                                       outperforms the baseline on task advancement.
delivered portions of interrupted messages, and other issues.
A modifier applies minimal targeted edits; conversations that          Recovery quality (absolute). The recovery quality judge
cannot be fixed are discarded.                                         evaluates a single model response against 2–4 type-specific


                                                                   4
                                                                                                                              TF Win Rate
Table 1: Overall results on IHB ENCH (audio input, 3 epochs).
                                                                                                 0.8
Baseline: GPT-4o Audio. Judge: GPT-5.4-mini (high reason-
ing). Mean ± half-width of 95% percentile bootstrap CI.                                          0.6


                                                                                   Other rater
 Model                               TF Win Rate ↑ RQ Pass Rate ↑                                0.4

 GPT Realtime 2 (medium)†                 .728±.03             .624±.04                          0.2
 GPT Realtime 2 (xhigh)†                  .702±.04             .613±.04
                                                                                                  0
 GPT Realtime 1.5                         .654±.04             .655±.04                                0           0.2              0.4              0.6              0.8
 GPT Audio                                .644±.04             .649±.04                                             Primary judge (GPT-5.4-mini)
 Gemini 3 Flash†                          .632±.03             .605±.04
 Gemini 3 Flash                           .598±.04             .661±.04                           Perfect Agreement (identity)            Secondary Judge (Gemini 3 Flash)
 GPT Realtime                             .597±.04             .680±.04                           Primary Judge w/ Summarized Context     Human Annotators
 Gemini 2.5 Flash†                        .586±.04             .704±.04           Figure 3: Per-model task-fulfillment agreement: primary
 Gemini 3.1 Pro†                          .582±.04             .649±.04           judge (x-axis) vs. the secondary judge, the summarized-
 Gemini 2.5 Pro†                          .526±.04             .695±.04           context judge, and human annotators (y-axis). Colored lines
 GPT-4o Audio (baseline)                    .500∗              .654±.05           are OLS fits. RQ counterpart: Figure 7.
 Gemini 2.5 Flash                         .488±.04             .679±.04
 GPT Audio Mini                           .484±.04             .579±.04
 Gemini 3.1 Flash Live                    .419±.04             .611±.04
                                                                                  Google models. Gemini 2.5 Flash and Gemini 2.5 Pro [11];
 GPT Realtime Mini                        .417±.03             .621±.04           Gemini 3 Flash and Gemini 3.1 Pro [12]; and Gemini 3.1
 Gemini 3.1 Flash Live†                   .405±.04             .603±.04           Flash Live [13].
 GPT-4o Mini Audio                        .351±.04             .654±.05           Open-weight models. Gemma 4 12B Instruct [14], Qwen3-
                                                                                  Omni-30B-A3B-Instruct [45], Qwen2.5-Omni-7B [44], Phi-
 Gemma 4 12B Instruct†                    .511±.03             .550±.04           4-Multimodal-Instruct [1], Voxtral-Small-24B-2507 [24],
 Gemma 4 12B Instruct                     .505±.04             .540±.04           Qwen2-Audio-7B-Instruct [6], MiMo-Audio-7B-Instruct (in
 MiMo-Audio-7B†                           .445±.04             .519±.04           both no-thinking and thinking modes) [42], and Kimi-Audio-
 MiMo-Audio-7B                            .337±.03             .581±.04
 Voxtral-Small-24B                        .308±.03             .593±.04
                                                                                  7B-Instruct [17].
 Qwen3-Omni-30B                           .304±.03             .676±.04
 Kimi-Audio-7B                            .220±.03             .519±.04           5.2            Overall Results
 Qwen2.5-Omni-7B                          .181±.03             .530±.04
 Phi-4-Multimodal                         .104±.02             .465±.04
                                                                                  Table 1 presents the overall results.
 Qwen2-Audio-7B                           .044±.01             .395±.04
    † Thinking/reasoning-enabled.     ∗ TF win rate is measured against the       Key findings.
       baseline, so TF is 0.50 by construction for baseline vs. baseline.
                                                                                  • GPT Realtime 2 achieves the highest task fulfillment win
criteria from the rubric. Each criterion is assessed as met or                      rate (0.728), followed by GPT Realtime 2 (xhigh) (0.702)
not met, and the overall verdict is mechanically consistent: all                    and GPT Realtime 1.5 (0.654).
criteria met → Pass, any criterion not met → Fail. We report                      • Recovery quality tells a different story: Gemini 2.5 Flash
the recovery quality pass rate: the fraction of interruptions                       (thinking) achieves the highest RQ pass rate (0.704) despite
where all criteria are met. These criteria are tailored to each                     a lower TF score (0.586), indicating that task advancement
interruption type (Section 3.2); an example rubric is shown                         and recovery quality are partially independent axes.
in Appendix G.                                                                    • GPT Realtime has the highest RQ among GPT models
                                                                                    (0.680) but only mid-tier TF (0.597), suggesting that older
5      Results                                                                      Realtime models are more conservative but more correct
                                                                                    in recovery behavior.
We evaluate 27 model configurations on IHB ENCH using                             • Thinking/reasoning modes help for Gemini on TF: Gemini
GPT-5.4-mini [31] (high reasoning) as the judge. The 27                             2.5 Flash with thinking outperforms without (0.586 vs.
configurations come from 17 closed-weight systems and                               0.488), and Gemini 3 Flash similarly (0.632 vs. 0.598).
10 open-weight configurations. The evaluation is run with                           However, thinking does not consistently improve RQ.
three independent epochs per configuration, and 95% confi-
dence intervals are computed by a 1000-iteration percentile                       5.3            Inter-Judge Agreement
bootstrap [8] over the N =428 per-sample (epoch-averaged)
means.                                                                            Every result above rests on a single LLM judge, so we ask
                                                                                  whether the rankings are robust to that choice. We validate
5.1      Evaluated Models                                                         it two ways: by re-scoring the whole benchmark with an
                                                                                  independent second judge from a different provider, and by
OpenAI models. GPT-4o Audio and GPT-4o Mini Audio                                 comparing its verdicts to human annotations. If both judges
[25]; GPT Audio [26] and GPT Audio Mini [27]; GPT Re-                             and human raters recover the same ordering and agree at the
altime and GPT Realtime 1.5 [28], GPT Realtime Mini, and                          verdict level, the conclusions are unlikely to be an artifact of
GPT Realtime 2 [30].                                                              the judging setup.


                                                                              5
Figure 3 plots the per-model points; the full agreement break-       gives t = 7.74, p < 10−6 . This gap is consistent with open-
down across every rater pair on both axes (sample-level agree-       weight models being trained primarily on short, single-turn
ment, Cohen’s κ, and per-model rank/value correlations) is           or speech-recognition data, leaving them less robust to long
deferred to Appendix B, with the headline numbers summa-             multi-turn dialogue context, but our evaluation cannot sepa-
rized below.                                                         rately attribute it to training data, model scale, or modality
                                                                     alignment.
The judges agree with each other. The second judge is
Gemini 3 Flash (with thinking), run over all responses. The
model ranking is well preserved (Spearman ρ = 0.99 on                5.5   Recovery Quality Is a New Capability Axis
TF and 0.95 on RQ) and the two judges’ 3-epoch verdicts
                                                                     To test whether IHB ENCH adds information beyond existing
agree at the sample level in the “substantial” range (Cohen’s
                                                                     multi-turn audio evaluation, we pair our 27 model configu-
κ = 0.75 on TF and 0.70 on RQ), at or above the inter-judge
                                                                     rations with their per-axis scores on AudioMultiChallenge
κ values typically reported for LLM-as-judge in MT-Bench
                                                                     (AMC) [15] and apply the submodular benchmark-selection
[48]. The secondary judge is slightly more lenient on RQ,
                                                                     framework [37]. We ran AMC inference ourselves for all
but the offset is near-constant (it preserves the ranking, and
                                                                     27 configurations (Appendix F). The score matrix has n=27
the fit slope is close to 1), so it is inconsequential.
                                                                     paired models and k=6 evaluation axes: the four AMC axes
The judge agrees with humans. We ran two Prolific stud-
                                                                     and the two IHB ENCH primary metrics (TF Win Rate, RQ
ies, one per axis. The full system message and conversation
                                                                     Pass Rate); their pairwise correlations are shown in Figure 5.
history are long and mostly irrelevant to any single inter-
ruption, so we give each annotator a summarized context:             The headline. The four AMC axes intercorrelate strongly
an LLM-distilled paragraph of the system message and the             (r = 0.65–0.93), reflecting a dominant general-capability
conversation history relevant to this turn, a self-contained         factor, and IHBench TF sits within that band (r̄ = 0.71).
restatement of the criterion, and the last two rounds as audio       IHBench RQ does not: its mean intercorrelation (r̄ =
(full study design in Appendix C). The validation is strong on       0.56) is the lowest in the 6×6 matrix, and the gap to the
two levels. Per item, the judge agrees with humans slightly          AMC-axis mean excludes zero under a model-level boot-
more often than two humans agree with each other (κ = 0.45–          strap [8]. Greedy entropy selection [37] also picks IHB-RQ
0.51 vs. 0.43 on TF and 0.41–0.44 vs. 0.40 on RQ), so it is          #2, though partly due to redundancy among the AMC sub-
statistically indistinguishable from an additional annotator.        axes. IHBench-RQ measures recovery quality: a capability
At the level of conclusions, the human ranking matches               axis largely distinct from the long-context coherence skills
the judge’s almost exactly: recovery quality is recovered            AMC tests.
rank for rank (Spearman ρ = 1.0), and task fulfillment dif-          IHBench-TF, by contrast, partially overlaps with AMC.
fers only by a single adjacent swap of two mid-pack models           TF Win Rate’s mean correlation (r̄ = 0.71) sits inside the
(ρ = 0.90), so every comparative claim in this paper would           AMC band. TF is essentially a comparative measure of task
stand unchanged under human scoring. Since humans saw                progression, which a more capable multi-turn audio model
only the summarized context while the judge sees the full con-       will tend to do better at regardless of how the user input is
text, we re-ran the judge on the same summary (Figure 3); it         delivered, so a strong correlation with a general multi-turn
agrees closely with the full-context judge, so the comparison        benchmark like AMC is unsurprising. The residual disagree-
is not confounded by the judge’s context advantage.                  ment is still substantive: GPT Realtime 2 is ranked #1 on
                                                                     TF and #4 on AMC, while Gemini 3.1 Pro is ranked #9 on
                                                                     TF and #1 on AMC, indicating that even within the overlap,
5.4   Task Fulfillment vs. Conversation Depth
                                                                     the specific demand of resuming a workflow after a mid-
                                                                     utterance interruption pulls model families apart in a way the
Figure 4 shows task fulfillment win rate across four conver-
                                                                     AMC ranking does not capture.
sation depth bins (by user message index).
                                                                     Recovery quality varies sharply by interruption type.
Task fulfillment degrades with depth. For each model ex-             Breaking recovery quality down by the six interruption types
cept the GPT-4o Audio baseline, we fit a logistic regression         (full per-model table in Appendix D) exposes a strong type
of the binary task-fulfillment outcome on conversation depth         effect. Filler is the single largest model-to-model differen-
(user message index). Twenty-four of the 26 remaining au-            tiator: GPT-family models continue an utterance correctly
dio model configurations have a negative slope. The mean             after a backchannel only 7%–31% of the time, the Gemini
per-model slope is −0.030 per additional turn, and a one-            2.5 family is markedly better (62%–68%), and Gemini 3.x
sample t-test against zero gives t(25) = −7.04, p < 10−6 ,           regresses sharply (13%–32%). Normal interruptions (0.71–
confirming that task fulfillment becomes significantly harder        0.85 pass) and topic switches (0.65–0.90) are handled well
as the conversation lengthens. The steepest declines are all         across the board, so the spread is concentrated in the harder
on open-weight models; GPT Realtime 2 and GPT Realtime               types.
1.5 are the only two models with non-negative slopes.
Open-weight models degrade faster with depth. The ten                5.6   Text-Only vs. Audio-Input Evaluation
open-weight configurations all have negative depth slopes
between −0.034 and −0.069 (mean −0.053), while the 16                To measure how much the audio modality itself contributes
closed-weight configurations have a mean slope of −0.016.            to the difficulty, we re-ran the six Gemini models and nine of
A Welch t-test of closed-weight versus open-weight slopes            the ten open-weight model configurations using transcripts


                                                                 6
                                                                                                                                                           0–4                    5–9           10–14               15–19                     Logistic fit
                                                                                                                           Closed-weight                                                                                                                                                               Open-weight
               0.8

               0.6


TF Win Rate
               0.4

               0.2

                    0                                                                                                                                                                      i                      i                                                                              ral          ni          i         ni                 io
                                 2
                                          2x
                                            h              1.5        d io         lt
                                                                                     h
                                                                                                 ln
                                                                                                   o           RT          Fl
                                                                                                                                th           Pr
                                                                                                                                                o
                                                                                                                                                            ot
                                                                                                                                                              h                  no      in          no        in             th
                                                                                                                                                                                                                                       ud
                                                                                                                                                                                                                                          io         th         no
                                                                                                                                                                                                                                                                         hi
                                                                                                                                                                                                                                                                            nk      on
                                                                                                                                                                                                                                                                                      o
                                                                                                                                                                                                                                                                                            xt                         m                   i-4       ud
                            RT                        RT           Au            3F            3F          T                                              Pr                Fl        oM          ve         M             ve                      B          B
                                                                                                                                                                                                                                                                      ot
                                                                                                                                                                                                                                                                                                            m        Ki          Om      Ph
                        T            RT                                                                GP            2.5               3.1                            2.5          di           Li        RT            Li           iA         12         12                    iM       Vo             -O                   .5-                  -A
                     GP                           T            T             m                                                                      2.5                                                             3.1           in         a4         a4         iM                                  Q3                  Q2                    Q2
                                T
                                               GP            GP           Ge            Ge
                                                                                           m                     m              Ge
                                                                                                                                   m                              m             Au          3.1         T                                                                      M
                             GP                                                                                Ge                            Ge
                                                                                                                                               m
                                                                                                                                                               Ge             T           m          G P        m           4o
                                                                                                                                                                                                                                M
                                                                                                                                                                                                                                          m
                                                                                                                                                                                                                                            m
                                                                                                                                                                                                                                                    m
                                                                                                                                                                                                                                                      m          M
                                                                                                                                                                            GP         Ge                    Ge          T-            Ge        Ge
                                                                                                                                                                                                                      GP
Figure 4: Task fulfillment win rate by conversation depth, with a per-model logistic regression slope fitted on the raw per-sample
data. Pooled across the 26 audio model configurations (excluding TF baseline), the mean slope is significantly negative.

                                                                                                                                                                                      1                      sided tests (TOST) procedure [34] on per-sample (epoch-
               IHB-RQ                     0.34                   0.48            0.61                 0.67            0.67                          1
                                                                                                                                                                                      0.9                    averaged) audio−text differences, with equivalence margins
                IHB-TF                    0.64                   0.79            0.65                 0.79                  1                  0.67                                                          ∆ ∈ {0.02, 0.03, 0.05}. We split by model family, which
   AMC-VOICE                              0.88                   0.89            0.77                  1              0.79                     0.67                                   0.7                    behave very differently.
        AMC-SELF                          0.66                   0.65               1                 0.77            0.65                     0.61                                                          Gemini (six configurations, n=2568): both TF (audio−text
   AMC-INSTR                              0.93                    1              0.65                 0.89            0.79                     0.48                                   0.5                    = −0.007) and RQ Pass (−0.001) are equivalent at ±0.02
                                                                                                                                                                                                             (p = 0.013 and 0.0002, respectively); audio and text-only
   AMC-INFER                               1
                                        0.93       0.66      0.88     0.64      0.34
                                        RR          F         E        F         Q                                                                                                    0.3                    are statistically indistinguishable.
                                     FE
                                      ST        E L       I C      B-T        -R
                                                      -VO                   B
                       C -IN    C -IN
                                          M C-S      C          IH       IH                                                                                                                                  Open-weight (nine configurations, n=3852):                   TF
                    AM       AM         A       AM                                                                                                                                                           audio−text = −0.079 (text wins by ∼8 points) and RQ
Figure 5: Pairwise Pearson correlations across the four AMC                                                                                                                                                  Pass diff = −0.062; TOST fails to establish equivalence
axes (APR) and the two IHB ENCH primary metrics (TF Win                                                                                                                                                      even at ±0.05 on either metric. What is more, a one-sided
Rate, RQ Pass Rate), over the n=27 paired models. The IHB-                                                                                                                                                   paired t-test shows text significantly outperforms audio on
RQ row and column are the lightest in the matrix, reflecting                                                                                                                                                 both TF (t(3851) = −14.95, p < 10−26 ) and RQ Pass
its low correlation with the AMC axes.                                                                                                                                                                       (t(3851) = −10.70, p < 10−26 ).
              0.8                              Gemini                                                                  Open-weight
                                                                                                                                                                                                             Audio input never outperforms text. Across all 15 dual-
                                                                                                                                                                       Audio                                 modality configurations, text-only input is either statistically
                                                                                                                                                                      Text only
              0.6
                                                                                                                                                                                                             equivalent to audio (the six Gemini models, within ±0.02 on
                                                                                                                                                                                                             every metric) or strictly better (the nine open-weight configu-

TF Win Rate
                                                                                                                                                                                                             rations, text ahead by ∼8 points on TF and ∼6 on RQ Pass);
              0.4                                                                                                                                                                                            audio never wins.

              0.2

                                                                                                                                                                                                              6          Conclusion
               0
                                                                           l   i   i         o
                   l th l no l th Pro 5 Pro Fl no a4 th 4 no o th o no xtra Omn Omn Phi-4 udi
                3 F 3 F 2.5 F 3.1    2. 2.5             a   M    M    Vo Q3- 2.5-         -A
                                               emm emm Mi Mi                           Q2
                                             G    G                          Q
                                                                                                                                                                                                             We introduced IHB ENCH, a benchmark for evaluating post-
Figure 6: Audio vs. text-only task fulfillment across the 15                                                                                                                                                 interruption recovery in voice agents executing structured
dual-modality configurations (6 Gemini + 9 open-weight, 3                                                                                                                                                    workflows. Unlike existing benchmarks that focus on the tim-
epochs each), grouped by family. Error bars are 95% per-                                                                                                                                                     ing and mechanics of interruptions, IHB ENCH evaluates what
centile bootstrap CIs. Audio never beats text-only. The                                                                                                                                                      models say after an interruption: whether they resume the
recovery-quality counterpart is in Appendix E.                                                                                                                                                               workflow correctly, address the user’s interjection, and avoid
                                                                                                                                                                                                             common pitfalls like repeating already-delivered content.
in place of the audio waveforms (OpenAI models and Kimi-
                                                                                                                                                                                                             Our evaluation of 27 audio-language model configurations
Audio-7B are excluded due to not accepting text-only input).
                                                                                                                                                                                                             (17 closed-weight, 10 open-weight) reveals several findings.
Everything else (conversation history, baseline, judge) is held
                                                                                                                                                                                                             The clearest is a consistent gap between closed-weight and
fixed. Figure 6 compares the two conditions on TF; the
                                                                                                                                                                                                             open-weight models: the closed-weight models win far more
recovery-quality counterpart is in Appendix E (Figure 8).
                                                                                                                                                                                                             often on task fulfillment, degrade roughly 3.3× more slowly
Equivalence analysis. A standard difference test shows                                                                                                                                                       as conversations grow longer, and show no audio-versus-text
only whether modality has any effect, not whether the                                                                                                                                                        modality gap, whereas open-weight models lose ground on
two conditions are comparable, so we use the two one-                                                                                                                                                        all three. Beyond this divide:


                                                                                                                                                                                                   7
• Post-interruption recovery is a distinct capability with wide              Anil Madamala, Sridhar Krishna Nemala, and Srini-
  spread across models.                                                      vas Sunkara. Eva-bench: A new end-to-end framework
• Filler handling (resuming an utterance after a backchannel)                for evaluating voice agents, 2026.
  is a strong family-level differentiator despite being the
  simplest type conceptually: the GPT family and the newer               [5] Yiming Chen, Xianghu Yue, Chen Zhang, Xiaoxue Gao,
  Gemini 3.x line handle it far less reliably than the Gemini                Robby T. Tan, and Haizhou Li. Voicebench: Bench-
  2.5 family.                                                                marking llm-based voice assistants, 2024.
• Task fulfillment and recovery quality are partially indepen-
  dent axes: the task-fulfillment leader ranks only mid-pack             [6] Yunfei Chu, Jin Xu, Qian Yang, Haojie Wei, Xipin Wei,
  on recovery quality, while the recovery-quality leader has                 Zhifang Guo, Yichong Leng, Yuanjun Lv, Jinzheng He,
  lower task fulfillment.                                                    Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen2-
• Against AudioMultiChallenge, IHBench’s recovery quality                    Audio technical report, 2024.
  is the lowest-correlated of the six joint evaluation axes (the
  four AMC axes plus our two metrics). This is evidence                  [7] Alexandre Défossez, Laurent Mazaré, Manu Orsini,
  that recovery quality is a largely distinct capability axis,               Amélie Royer, Patrick Pérez, Hervé Jégou, Edouard
  not already captured by a strong general audio benchmark.                  Grave, and Neil Zeghidour. Moshi: a speech-text foun-
                                                                             dation model for real-time dialogue, 2024.
Limitations. IHB ENCH is built from synthetic conversa-
tions rather than real user interactions, is English-only, and           [8] Bradley Efron. Bootstrap methods: Another look at the
spans 10 enterprise domains; its rubrics inherit the biases of               jackknife. The Annals of Statistics, 7(1):1–26, 1979.
the generator model and the judge. We evaluate recovery
on the textual content of responses only, not on prosodic or             [9] Jiaxuan Gao, Jiaao Chen, Chuyi He, Shusheng Xu,
acoustic recovery behavior (e.g. timing or intonation after a                Di Jin, and Yi Wu. From self-evolving synthetic data to
barge-in).                                                                   verifiable-reward rl: Post-training multi-turn interactive
                                                                             tool-using agents, 2026.
Future work. Natural extensions include multilingual cov-
erage, validation against real end-user interactions in live            [10] Yuan Ge, Saihan Chen, Jingqi Xiao, Xiaoqian Liu, Tong
deployment, integration with full-duplex timing benchmarks                   Xiao, Yan Xiang, Zhengtao Yu, and Jingbo Zhu. Flexi:
for end-to-end interruption evaluation (timing and recovery),                Benchmarking full-duplex human-llm speech interac-
and turning the benchmark, or the synthetic pipeline behind                  tion, 2025.
it, into a training signal: post-training on its rubrics and gen-
erated data to strengthen the recovery behavior we currently            [11] Google.      Gemini 2.5:     Our most intelligent AI
only measure.                                                                model.   https://blog.google/innovation-and-ai/
                                                                             models-and-research/google-deepmind/
                                                                             gemini-model-thinking-updates-march-2025/,
References                                                                   2025. Accessed: 2026-06-09.
 [1] Marah Abdin, Jyoti Aneja, Harkirat Behl, Sébastien
     Bubeck, Ronen Eldan, Suriya Gunasekar, Michael Har-                [12] Google.      Gemini 3.       https://blog.google/
     rison, Russell J. Hewett, Mojan Javaheripi, Piero Kauff-                products-and-platforms/products/gemini/
     mann, James R. Lee, Yin Tat Lee, Yuanzhi Li, Weishung                   gemini-3/, 2025. Accessed: 2026-06-09.
     Liu, Caio C. T. Mendes, Anh Nguyen, Eric Price, Gus-
     tavo de Rosa, Olli Saarikivi, Adil Salim, Shital Shah,             [13] Google.   Gemini 3.1 Flash Live. https://blog.
     Xin Wang, Rachel Ward, Yue Wu, Dingli Yu, Cyril                         google/innovation-and-ai/models-and-research/
     Zhang, and Yi Zhang. Phi-4 technical report, 2024.                      gemini-models/gemini-3-1-flash-live/,     2026.
                                                                             Accessed: 2026-06-09.
 [2] Rosana Ardila, Megan Branson, Kelly Davis, Michael
     Henretty, Michael Kohler, Josh Meyer, Reuben Morais,               [14] Google DeepMind. Gemma 4. https://deepmind.
     Lindsay Saunders, Francis M. Tyers, and Gregor We-                      google/models/gemma/gemma-4/, 2026. Accessed:
     ber. Common voice: A massively-multilingual speech                      2026-06-09.
     corpus, 2020.
                                                                        [15] Advait Gosai, Tyler Vuong, Utkarsh Tyagi, Steven Li,
 [3] Siddhant Arora, Zhiyun Lu, Chung-Cheng Chiu, Ruom-                      Wenjia You, Miheer Bavare, Arda Uçar, Zhongwang
     ing Pang, and Shinji Watanabe. Talking turns: Bench-                    Fang, Brian Jang, Bing Liu, and Yunzhong He. Au-
     marking audio foundation models on turn-taking dy-                      dio multichallenge: A multi-turn evaluation of spoken
     namics, 2025.                                                           dialogue systems on natural human interaction, 2025.

 [4] Tara Bogavelli, Gabrielle Gauthier Melançon, Kat-                  [16] Dhruv Jain, Harshit Shukla, Gautam Rajeev, Ashish
     rina Stankiewicz, Oluwanifemi Bamgbose, Fanny Ri-                       Kulkarni, Chandra Khatri, and Shubham Agarwal.
     ols, Hoang H. Nguyen, Raghav Mehndiratta, Lind-                         Voiceagentbench: Are voice assistants ready for agentic
     say Devon Brin, Joseph Marinier, Hari Subramani,                        tasks?, 2026.


                                                                    8
[17] KimiTeam, Ding Ding, Zeqian Ju, Yichong Leng,                   [29] OpenAI. Introducing OpenAI o3 and o4-mini. https:
     Songxiang Liu, Tong Liu, Zeyu Shang, Kai Shen, Wei                   //openai.com/index/introducing-o3-and-o4-mini/,
     Song, Xu Tan, Heyi Tang, Zhengtao Wang, Chu Wei,                     2025. Accessed: 2026-06-17.
     Yifei Xin, Xinran Xu, Jianwei Yu, Yutao Zhang, Xinyu
     Zhou, Y. Charles, Jun Chen, Yanru Chen, Yulun Du,               [30] OpenAI. Advancing voice intelligence with new
     Weiran He, Zhenxing Hu, Guokun Lai, Qingcheng Li,                    models in the API. https://openai.com/index/
     Yangyang Liu, Weidong Sun, Jianzhou Wang, Yuzhi                      advancing-voice-intelligence-with-new-models-in-the-api/,
     Wang, Yuefeng Wu, Yuxin Wu, Dongchao Yang, Hao                       2026. Accessed: 2026-06-09.
     Yang, Ying Yang, Zhilin Yang, Aoxiong Yin, Ruibin               [31] OpenAI.               Introducing    GPT-5.4      mini
     Yuan, Yutong Zhang, and Zaida Zhou. Kimi-audio                       and   nano.           https://openai.com/index/
     technical report, 2025.                                              introducing-gpt-5-4-mini-and-nano/, 2026. Ac-
                                                                          cessed: 2026-06-09.
[18] Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap,
     Tianhao Wu, Banghua Zhu, Joseph E. Gonzalez, and                [32] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brock-
     Ion Stoica. From crowdsourced data to high-quality                   man, Christine McLeavey, and Ilya Sutskever. Robust
     benchmarks: Arena-hard and benchbuilder pipeline,                    speech recognition via large-scale weak supervision,
     2024.                                                                2022.
[19] Bill Yuchen Lin, Yuntian Deng, Khyathi Chandu, Faeze            [33] Soham Ray, Keshav Dhandhania, Victor Barres, and
     Brahman, Abhilasha Ravichander, Valentina Pyatkin,                   Karthik Narasimhan. τ -voice: Benchmarking full-
     Nouha Dziri, Ronan Le Bras, and Yejin Choi. Wild-                    duplex voice agents on real-world domains, 2026.
     bench: Benchmarking llms with challenging tasks from
     real users in the wild, 2024.                                   [34] Donald J. Schuirmann. A comparison of the two one-
                                                                          sided tests procedure and the power approach for assess-
[20] Guan-Ting Lin, Chen Chen, Zhehuai Chen, and Hung                     ing the equivalence of average bioavailability. Journal
     yi Lee. Full-duplex-bench-v3: Benchmarking tool use                  of Pharmacokinetics and Biopharmaceutics, 15(6):657–
     for full-duplex voice agents under real-world disfluency,            680, 1987.
     2026.
                                                                     [35] Shuzheng Si, Wentao Ma, Haoyu Gao, Yuchuan Wu,
[21] Guan-Ting Lin, Shih-Yun Shan Kuan, Jiatong Shi, Kai-                 Ting-En Lin, Yinpei Dai, Hangyu Li, Rui Yan, Fei
     Wei Chang, Siddhant Arora, Shinji Watanabe, and Hung                 Huang, and Yongbin Li. Spokenwoz: A large-scale
     yi Lee. Full-duplex-bench-v2: A multi-turn evaluation                speech-text benchmark for spoken task-oriented dia-
     framework for duplex dialogue systems with an auto-                  logue agents, 2025.
     mated examiner, 2026.                                           [36] Ved Sirdeshmukh, Kaustubh Deshpande, Johannes
[22] Guan-Ting Lin, Shih-Yun Shan Kuan, Qirui Wang, Ji-                   Mols, Lifeng Jin, Ed-Yeremai Cardona, Dean Lee,
     achen Lian, Tingle Li, Shinji Watanabe, and Hung                     Jeremy Kritz, Willow Primack, Summer Yue, and Chen
     yi Lee. Full-duplex-bench v1.5: Evaluating overlap                   Xing. Multichallenge: A realistic multi-turn conversa-
     handling for full-duplex speech models, 2026.                        tion evaluation benchmark challenging to frontier llms,
                                                                          2025.
[23] Guan-Ting Lin, Jiachen Lian, Tingle Li, Qirui Wang,
     Gopala Anumanchipalli, Alexander H. Liu, and Hung               [37] Alexander Smola. Submodular benchmark selection.
     yi Lee. Full-duplex-bench: A benchmark to evaluate                   arXiv preprint arXiv:2605.02209, 2026.
     full-duplex spoken dialogue models on turn-taking ca-           [38] Yuzhi Tang, Wentao Ma, Xiling Zhao, Ahmad Sal-
     pabilities, 2025.                                                    imi, Sepehr Harfi Moridani, Dongming Shen, Jixuan
                                                                          Wang, Abdulrahman Abdulrazzag, Murdock Aubry, Yu-
[24] Mistral AI. Voxtral, 2025.
                                                                          Hua Chen, Daniel Lee, Jaewon Lee, Jonah Mackey,
[25] OpenAI. Hello GPT-4o. https://openai.com/index/                      Silin Meng, Nicholas Stranges, Chenxu Xiong, Hao
     hello-gpt-4o/, 2024. Accessed: 2026-06-09.                           Yu, Yi Zhu, Mu Li, and Alex Smola. INSTRUCT-FD:
                                                                          Can your full-duplex speech system follow turn-taking
[26] OpenAI. gpt-audio. https://developers.openai.com/                    instructions?, 2026.
     api/docs/models/gpt-audio, 2025. Accessed: 2026-
     06-09.                                                          [39] Chengyou Wang, Hongfei Xue, Guojian Li, Zhixian
                                                                          Zhao, Shuiyuan Wang, Shuai Wang, Xin Xu, Hui Bu,
[27] OpenAI. gpt-audio-mini. https://developers.openai.                   and Lei Xie. Full-duplex interaction in spoken dialogue
     com/api/docs/models/gpt-audio-mini, 2025.     Ac-                    systems: A comprehensive study from the icassp 2026
     cessed: 2026-06-09.                                                  humdial challenge, 2026.
[28] OpenAI. Introducing gpt-realtime and Realtime API               [40] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa
     updates for production voice agents. https://openai.                 Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh
     com/index/introducing-gpt-realtime/, 2025. Ac-                       Hajishirzi. Self-instruct: Aligning language models
     cessed: 2026-06-09.                                                  with self-generated instructions, 2023.


                                                                 9
[41] Kangxiang Xia, Bingshen Mu, Xian Shi, Jin Xu, and
     Lei Xie. Semantic-aware interruption detection in spo-
     ken dialogue systems: Benchmark, metric, and model,
     2026.
[42] LLM-Core-Team Xiaomi. Mimo-audio: Audio lan-
     guage models are few-shot learners, 2025.
[43] Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng,
     Pu Zhao, Jiazhan Feng, Chongyang Tao, Qingwei Lin,
     and Daxin Jiang. Wizardlm: Empowering large pre-
     trained language models to follow complex instructions,
     2025.
[44] Jin Xu, Zhifang Guo, Jinzheng He, Hangrui Hu, Ting
     He, Shuai Bai, Keqin Chen, Jialin Wang, Yang Fan,
     Kai Dang, Bin Zhang, Xiong Wang, Yunfei Chu, and
     Junyang Lin. Qwen2.5-Omni technical report, 2025.
[45] Jin Xu, Zhifang Guo, Hangrui Hu, Yunfei Chu, Xiong
     Wang, Jinzheng He, Yuxuan Wang, Xian Shi, Ting
     He, Xinfa Zhu, Yuanjun Lv, Yongqi Wang, Dake
     Guo, He Wang, Linhan Ma, Pei Zhang, Xinyu Zhang,
     Hongkun Hao, Zishan Guo, Baosong Yang, Bin Zhang,
     Ziyang Ma, Xipin Wei, Shuai Bai, Keqin Chen, Xue-
     jing Liu, Peng Wang, Mingkun Yang, Dayiheng Liu,
     Xingzhang Ren, Bo Zheng, Rui Men, Fan Zhou, Bowen
     Yu, Jianxin Yang, Le Yu, Jingren Zhou, and Junyang
     Lin. Qwen3-omni technical report, 2025.
[46] Yejin Yoon, Yuri Son, Namyoung So, Minseo Kim,
     Minsoo Cho, Chanhee Park, Seungshin Lee, and Taeuk
     Kim. Beyond task-oriented and chitchat dialogues:
     Proactive and transition-aware conversational agents,
     2025.
[47] He Zhang, Wenqian Cui, Haoning Xu, Xiaohui Li, Lei
     Zhu, Haoli Bai, Shaohua Ma, and Irwin King. Mtr-
     duplexbench: Towards a comprehensive evaluation of
     multi-round conversations for full-duplex speech lan-
     guage models, 2026.
[48] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
     Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuo-
     han Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E.
     Gonzalez, and Ion Stoica. Judging llm-as-a-judge with
     mt-bench and chatbot arena, 2023.
[49] Xuhui Zhou, Hao Zhu, Leena Mathur, Ruohong Zhang,
     Haofei Yu, Zhengyang Qi, Louis-Philippe Morency,
     Yonatan Bisk, Daniel Fried, Graham Neubig, and
     Maarten Sap. Sotopia: Interactive evaluation for so-
     cial intelligence in language agents, 2024.
[50] Henry Peng Zou, Chunyu Miao, Wei-Chieh Huang,
     Yankai Chen, Yue Zhou, Hanrong Zhang, Yaozu Wu,
     Liancheng Fang, Zhengyao Gu, Zhen Zhang, Kening
     Zheng, Fangxin Wang, Yi Nian, Shanghao Li, Wen-
     zhe Fan, Langzhou He, Weizhi Zhang, Xue Liu, and
     Philip S. Yu. When users change their mind: Evaluat-
     ing interruptible agents in long-horizon web navigation,
     2026.


                                                                10
A    Dataset Statistics                                                                                                  RQ Pass Rate

                                                                                            0.8




                                                                              Other rater
                     Table 2: Dataset statistics.
                                                                                            0.6
         Statistic                                  Value
         Conversations                                   45
                                                                                            0.4
         Domains                                         10
                                                                                                    0.4           0.5             0.6           0.7           0.8
         Total interruption points                     428
         Avg. messages per conversation               30.1                                                     Primary judge (GPT-5.4-mini)
         Min / max messages                         19 / 40
                                                                                            Perfect Agreement (identity)                Secondary Judge (Gemini 3 Flash)
         Interruption type distribution                                                     Primary Judge w/ Summarized Context         Human Annotators
            Pushback                         105 (24.5%)
            Impatient                         84 (19.6%)                  Figure 7: Recovery-quality agreement between the primary
            Normal                            81 (18.9%)                  judge (GPT-5.4-mini, high reasoning, full context; x-axis)
            Topic switch                      73 (17.1%)
                                                                          and three other raters, per model (the recovery-quality coun-
            Filler                            60 (14.0%)
            Correction                         25 (5.8%)                  terpart of Figure 3): blue circles the secondary judge (Gemini
                                                                          3 Flash with thinking, 25 configurations); orange triangles
         Interruptions by depth (user turn index)                         the same primary judge on the summarized human-study con-
            0–4                              169 (39.5%)                  text; teal squares human annotators on the 5 study models
            5–9                              130 (30.4%)                  (single-epoch primary judge). The dashed gray line is perfect
            10–14                             80 (18.7%)
            15–19                             49 (11.4%)
                                                                          agreement; colored lines are OLS fits. The secondary judge’s
                                                                          RQ leniency shows as an offset above the diagonal. Numeric
                                                                          agreement, κ, and correlations are in Table 3.
Interruption type distribution. The uneven type distribu-
tion reflects two factors. First, the user intent generator is
prompted to prefer challenging interruption scenarios over                B             Full Inter-Rater Agreement Breakdown
cooperative ones. This is directly visible in the user intent
interruption profiles: pushback is the dominant type (proba-              Table 3 gives the complete agreement breakdown referenced
bility ≥ 0.25) in 26 of 45 conversations, while correction is             in Section 5.3: for every rater pair and both axes, the sample-
dominant in only 6. Second, correction is the only type where             level agreement and Cohen’s κ, and the per-model Spearman
the actual count (25, 5.8%) falls well below what the average             ρ (rank) and Pearson r (value) correlations. The headline
profile probability (12.3%) would predict (∼53 expected).                 numbers (judge–judge κ = 0.75/0.70 on TF/RQ; the judge
This gap arises because corrections require the user to have              agreeing with humans at least as well as humans agree with
provided a specific piece of information in a prior turn that             each other) are discussed in the main text.
they can then revise; the round planner under-generates cor-              Figure 7 is the recovery-quality counterpart of the task-
rections when no natural self-correction opportunity exists.              fulfillment agreement plot in the main text (Figure 3), show-
All other types track their profile probabilities within 2–5              ing the per-model agreement of the primary judge with the
percentage points.                                                        secondary judge, the summarized-context judge, and human
Depth distribution. Interruptions are concentrated in ear-                annotators on the RQ Pass axis. The secondary judge is
lier turns (40% in turns 0–4) and taper off at depth (11% in              systematically more lenient than the primary on recovery
turns 15–19). This is a natural consequence of the conver-                quality: a per-model OLS fit of secondary on primary RQ
sation length distribution: fewer conversations reach deeper              Pass rate has slope 1.04 and intercept 0.06, so its pass rates
turns, so there are fewer interruption opportunities at greater           sit slightly above the diagonal across models. Because this is
depth.                                                                    a near-constant offset (it preserves the ordering, ρ = 0.95 on
                                                                          RQ) and every comparison in the paper uses a single fixed
Each conversation is seeded from a (domain, goal, user intent)            judge, it does not affect any conclusion.
triple. Ten domains are covered: SaaS, financial services,
healthcare, telecom, e-commerce, travel, education, govern-
ment, subscription media, and professional services. Five                 C                 Human Study Design
goals are generated per domain, and ten user intents per goal,
yielding 500 possible configurations. Fifty are randomly                  We ran two human studies, one per axis, with annotators re-
sampled for conversation synthesis; after the verify–modify               cruited through Prolific. Rather than the full system message
loop discards unfixable samples and we keep only interrup-                and conversation history the judge sees, each annotator is
tion points that yield a well-formed evaluation item for every            shown a summarized context: an LLM distills the system
model, 45 conversations with 428 interruption points remain.              message and the parts of the conversation history relevant
Multiple conversations may share the same (domain, goal)                  to the current turn into a single self-contained paragraph, re-
pair but differ in user intent (personality, interruption profile,        states the evaluation criterion as a self-contained question,
hidden information).                                                      and pairs it with the last two rounds of the conversation ren-


                                                                     11
Table 3: Agreement across raters on IHB ENCH, on both axes. Sample level: fraction of items where two raters make the same
binary call, with Cohen’s κ. Per model: Spearman ρ (rank) and Pearson r (value) over the per-model rates. Judge–judge rows
use all 25 configurations and the 3-epoch judges; human rows use the 5 study models, the single-epoch primary judge (for parity
with single-rating humans), and n=616 paired decisions per axis. The judge agrees with humans at least as well as two humans
agree with each other (last row), on both axes and with either judge.

                                                                           Task Fulfillment             Recovery Quality
                       Rater pair                             Scope     agree ↑     κ↑     ρ/r↑       agree ↑   κ↑      ρ/r↑
                       Primary ↔ Secondary judge              25 cfg      .87       .75   .99 / .99    .86      .70   .95 / .98
                       Primary judge ↔ Human                  5 cfg       .75       .51   .90 / .95    .71      .41   1.0 / .93
                       Secondary judge ↔ Human                5 cfg       .73       .45   1.0 / .99    .74      .44   .90 / .91
                       Human ↔ Human (inter-annot.)           5 cfg       .72       .43      —         .73      .40      —
       “—” denotes a metric that does not apply: ρ/r require two per-model rankings, which the pooled inter-annotator agreement does not define.


dered as audio. In the task fulfillment study annotators chose                  D     Per-Type Recovery Quality Breakdown
which of two responses better satisfied the restated criterion
(exactly the comparative call the judge makes); in the re-                      Table 4 gives the full per-model recovery quality pass rate
covery quality study they answered the per-criterion yes/no                     broken down by the six interruption types, summarized in the
pass questions for a single response. The two studies drew                      main text (Section 5.2).
on disjoint annotator pools and each collected 616 paired
human–judge decisions across the 5 study models, with all                       Filler is the hardest type for GPT models. When a user
300 items rated by two or more annotators to estimate inter-                    produces a brief backchannel like “mm-hm” mid-utterance,
annotator agreement. The items are a stratified subset of                       the correct recovery is to continue the utterance from where
60 of the 428 interruption points (300 model×sample items                       it was cut off, without repeating or restarting. GPT-family
per axis), chosen to span interruption types and conversation                   models fail at this consistently: filler pass rates are between
depth; per-model rates therefore carry sampling uncertainty,                    0.07 (GPT Realtime Mini) and 0.31 (GPT Realtime). The
while the sample-level agreement in Table 3 is computed on                      failure modes are restarting the utterance, acknowledging
the full set of human judgments.                                                the filler (“Glad you’re following along!”), or producing an
                                                                                entirely new response. The Gemini 2.5 family is markedly
Human–judge agreement slightly exceeds inter-annotator                          better (Gem. 2.5 Pro 0.62, Gem. 2.5 Flash thinking 0.68,
agreement (κ = 0.45–0.51 vs. 0.43 on TF; 0.41–0.44                              Gem. 2.5 Flash 0.64), but Gemini 3.x regresses sharply (0.13–
vs. 0.40 on RQ). This is expected rather than surprising:                       0.32), suggesting filler handling did not carry over to the
the judge is a single fixed rater applied uniformly to all                      newer model line. This is the single largest model-to-model
items, whereas each study spreads its ∼30 annotators thinly                     gap among the six interruption types.
(about 20 items each), so the inter-annotator number absorbs
between-annotator variance across many different people                         Normal and topic switch are generally well-handled.
on top of per-rating noise; a given human therefore agrees                      Across models, normal interruptions are handled at 0.71–
somewhat more with the one consistent judge than with an-                       0.85 pass rate and topic switches at 0.65–0.90, suggesting
other arbitrary annotator. This holds whether the primary                       that addressing a relevant cut-in and engaging with a new
or the secondary judge is used, so the validation is not spe-                   topic are relatively natural capabilities for current LLMs.
cific to one judge. Per model, the human ranking matches
the judge’s almost exactly across all five study models (with                   Impatient and correction are middle-difficulty types. Im-
either judge): recovery quality is recovered rank for rank                      patient recovery (skipping content the user asked to skip)
(ρ = 1.0), and task fulfillment differs only by a single adja-                  clusters around 0.45–0.68, with Gemini 3.1 Pro the best at
cent swap of GPT- REALTIME - MINI and MIMO - AUDIO -7 B -                       0.66 and GPT Audio Mini the worst at 0.47. Correction re-
THINKING (ρ = 0.90), two mid-pack models the judge scores                       covery (accepting a self-correction without pushback) shows
within a few points and that the 3-epoch judge likewise keeps                   a wider spread of 0.52–0.75, partly driven by smaller per-
essentially tied (0.489 vs. 0.494).                                             type sample sizes (Section A).
To guard against low-quality annotators inflating this picture,
we tested each annotator’s agreement with the leave-one-                        E     Audio vs. Text-Only Recovery Quality
out majority of the other annotators on their shared items
(one-sided binomial test against the cohort base rate, Holm-                    Figure 8 is the recovery-quality counterpart of the task-
corrected); this criterion never references the judge, so it                    fulfillment audio-vs-text comparison in the main text (Fig-
cannot bias the human–judge comparison. In neither study                        ure 6, Section 5.6). The same conclusion holds on the RQ
did any annotator disagree with their peers significantly more                  Pass axis: the six frontier Gemini models are statistically
than chance after correction, so we exclude none.                               equivalent across modalities (within ±0.02), while the nine
                                                                                open-weight configurations are better with text input (RQ
                                                                                Pass audio−text = −0.062), and audio never wins. The full


                                                                         12
Table 4: Recovery quality pass rate by interruption type (audio input, 3 epochs). Mean ± half-width of 95% percentile bootstrap
CI (1000 resamples). Best per column in bold.

                                              Model                                        Normal        Impat.    Corr.     Topic     Filler    Push.
                                                                                     †
                                              GPT Realtime 2 (medium)                       .76±.08      .52±.09   .73±.14   .76±.08   .19±.08   .72±.07
                                              GPT Realtime 2 (xhigh)†                       .78±.08      .49±.09   .68±.15   .76±.08   .16±.07   .72±.08
                                              GPT Realtime 1.5                              .82±.07      .57±.09   .68±.15   .90±.06   .13±.07   .72±.07
                                              GPT Audio                                     .82±.08      .54±.10   .76±.13   .77±.08   .22±.09   .74±.07
                                              Gem. 3 Flash†                                 .77±.08      .54±.10   .63±.16   .80±.07   .14±.07   .66±.07
                                              Gem. 3 Flash                                  .81±.07      .53±.09   .76±.13   .87±.06   .32±.10   .68±.08
                                              GPT Realtime                                  .83±.07      .60±.09   .72±.15   .80±.07   .31±.11   .74±.08
                                              Gem. 2.5 Flash†                               .75±.08      .58±.09   .63±.15   .78±.08   .68±.11   .75±.08
                                              Gem. 3.1 Pro†                                 .82±.07      .66±.10   .57±.18   .82±.08   .13±.07   .71±.07
                                              Gem. 2.5 Pro†                                 .75±.08      .69±.08   .65±.15   .77±.07   .62±.10   .66±.08
                                              Gem. 2.5 Flash                                .76±.08      .58±.09   .61±.17   .77±.08   .64±.10   .67±.08
                                              GPT Audio Mini                                .77±.08      .48±.09   .72±.15   .65±.08   .08±.06   .71±.07
                                              GPT-4o Audio                                  .82±.08      .64±.11   .76±.16   .85±.09   .08±.08   .71±.09
                                              Gem. 3.1 Flash Live                           .75±.08      .58±.09   .57±.19   .74±.08   .24±.09   .66±.08
                                              GPT Realtime Mini                             .80±.07      .55±.09   .60±.17   .82±.07   .07±.06   .72±.08
                                              Gem. 3.1 Flash Live†                          .74±.08      .57±.09   .63±.15   .74±.08   .23±.08   .64±.08
                                              GPT-4o Mini Audio                             .83±.08      .64±.10   .52±.20   .88±.07   .15±.08   .70±.09
                                              Gemma 4 12B Instruct†                         .66±.09      .52±.09   .44±.16   .70±.07   .25±.08   .58±.07
                                              Gemma 4 12B Instruct                          .63±.09      .51±.09   .48±.15   .67±.08   .22±.08   .60±.08
                                              MiMo-Audio-7B†                                .68±.08      .36±.08   .47±.16   .72±.07   .03±.03   .68±.07
                                              MiMo-Audio-7B                                 .68±.06      .47±.09   .45±.15   .66±.07   .40±.11   .67±.07
                                              Voxtral-Small-24B                             .74±.07      .53±.09   .49±.15   .70±.08   .36±.10   .61±.08
                                              Qwen3-Omni-30B                                .80±.07      .63±.08   .55±.17   .80±.06   .46±.10   .69±.07
                                              Kimi-Audio-7B                                 .61±.09      .45±.08   .44±.16   .68±.08   .32±.10   .53±.07
                                              Qwen2.5-Omni-7B                               .65±.08      .53±.08   .33±.14   .66±.08   .35±.09   .49±.07
                                              Phi-4-Multimodal                              .52±.09      .56±.08   .28±.13   .63±.07   .18±.07   .44±.07
                                              Qwen2-Audio-7B                                .51±.10      .44±.08   .31±.13   .58±.10   .14±.07   .30±.07
                                                                                            † Thinking/reasoning-enabled.


               0.8                 Gemini                                 Open-weight                          F    AudioMultiChallenge Scoring
                                                                                              Audio
                                                                                             Text only
                                                                                                               The cross-benchmark analysis in Section 5.5 pairs each of


RQ Pass Rate
                                                                                                               our 27 model configurations with its scores on AudioMul-
               0.6                                                                                             tiChallenge (AMC) [15]. Several of the evaluated models
                                                                                                               post-date the AMC paper and are not in its released results,
                                                                                                               so we ran AMC inference ourselves for all 27 configurations
                                                                                                               rather than reusing reported numbers, ensuring every model
               0.4                                                                                             is scored under identical conditions. We use the official AMC
                                                                                  l   i   i
                      l th Fl no Fl th 1 Pro 5 Pro Fl no a4 th 4 no o th o no xtra Omn Omn Phi-4 udi
                                                                                                    o          judge (o4-mini [29]) with the exact judge system prompt and
                 3F            2.5    3.    2. 2.5             a   M    M    Vo Q3- 2.5-         -A
                          3                            mm mm Mi Mi                            Q2               structured-output schema from the AMC dataset card [15],
                                                    Ge Ge                           Q
                                                                                                               unmodified, and run three epochs per configuration to match
Figure 8: Audio vs. text-only recovery quality across the 15                                                   our IHB ENCH protocol; the per-axis APR scores used in
dual-modality configurations (6 Gemini + 9 open-weight, 3                                                      Figure 5 are the epoch-averaged means.
epochs each), the recovery-quality counterpart of Figure 6.
Grouping, ordering, family shading, and error bars are as in
Figure 6. As on task fulfillment, Gemini models are within
                                                                                                               G    Example Conversation with System
±0.02 across modalities while the open-weight configura-                                                            Prompt and Rubrics
tions are better with text input; audio never wins.
                                                                                                               We present a complete example from the benchmark: the
                                                                                                               assistant’s system prompt, the first eight messages of the
                                                                                                               conversation, and the evaluation rubric for the first interrup-
                                                                                                               tion. This conversation is from the Government and Public
                                                                                                               Services domain (disaster housing assistance workflow) and
TOST equivalence results for both metrics are reported in the                                                  contains 9 interruptions across 5 types: pushback, impatient,
main text.                                                                                                     topic switch, normal, and correction.


                                                                                                          13
G.1   Assistant System Prompt                                      damaged_property_address: 7420 Magnolia Ridge Dr,
                                                                   Lakeview, LA 70121
The system prompt below is generated by the pipeline’s sys-        mailing_address_on_file: PO Box 1184, Metairie, LA
tem message writer (Appendix I.1) from the domain, goal,           70001
and knowledge base. It serves as the assistant’s complete          primary_phone_on_file: 504-555-2974
operating instructions during the conversation.                    secondary_phone_on_file: 985-555-8039
                                                                   email_on_file: marisol.ortega84@gmail.com
  System prompt: Disaster Housing Assistance                       language_preference: English
                                                                   applicant_time_zone: Central Time (CT)
  You are the call-based assistant for Government                  intake_submission_date: 2026-02-17
   and Public Services, supporting public service                  initial_accessibility_notes:       Driveway partially
   agencies    that   manage    structured    applications,        blocked by a downed oak; small dog named Coco;
   identity verification, compliance steps, and formal             electrical power restored on 2026-02-28
   registrations.     You are representing the State               inspection_window_policy: Weekdays Mon–Fri: AM 8–12,
   Disaster Housing Assistance (SDHA) program.         Your        PM 12–4, Late 4–6; Limited Saturday AM slots
   purpose is to proactively reach out to a disaster               presence_requirement: Applicant or another adult
   assistance applicant after initial intake, coordinate           (18+) with photo ID must be present for the inspection
   a required home inspection, verify case ID and identity         safety_preparation_requirements: Secure pets, clear
  (name and DOB), confirm the damaged property address             pathways to all rooms and utilities, disclose any
   and accessibility constraints, capture preferred                hazards (mold, gas leaks, structural instability)
   inspection windows and any special access needs, obtain         consent_to_share_contact_with_inspector_status: Not
   explicit consent to share contact details with the              yet obtained
   inspector and to send a confirmation, and finalize by           earliest_available_inspection_date: 2026-03-09
   booking the inspection and providing the appointment            inspection_estimated_duration: 60–90 minutes
   confirmation number.                                            booking_hold_limit_minutes: 30
   How to operate                                                  inspection_appointment_confirmation_number:
  - Initiate the conversation.         Establish who you           INS-20260309-18427
   are (SDHA), why you’re contacting the applicant                 conversation_reference_id: CR-20260305-6102
  (inspection coordination for their disaster assistance           State machine: required stages and controls
   application), and what will happen in this call                 1) Open and Establish Purpose
  (verification, address confirmation, access/safety               Introduce yourself as calling from SDHA about
   details, scheduling, and consent). Do not assume the            the applicant’s disaster assistance application to
   user remembers prior steps.                                     coordinate a required home inspection. Confirm you’re
  - Drive a strict workflow that follows the stages below          speaking with the applicant. State that the call will
   in order. Apply skip conditions only when explicitly            include verification, scheduling, and consent to share
   met during this same conversation. Do not narrate               contact details with an inspector. Ask if now is a good
   stage numbers to the user.                                      time to proceed.
  -     Only  use    two   sources    of    facts:      (1)        Skip conditions: Only skip if the user has already
   known_user_information    (listed    below)    and   (2)        acknowledged the purpose and agreed to proceed.
   information the user provides or confirms in this               Failure handling: If busy, offer to schedule a callback
   conversation. Do not invent any other data.                     time. If legitimacy is challenged, reference the SDHA
  - Ask concise, single questions where possible. Before           program and their case ID.
   any irreversible action (capturing consent, booking),           Terminate conditions: Terminate if the user declines
   read back critical details and confirm.                         to proceed and confirms they want to stop.
  - Collect only the following data elements: case ID,             2) Verify Case and Identity
   full name, date of birth, damaged property address,             Authenticate by requesting the user to read their case
   access/safety notes, availability windows, consent to           ID and to state their full legal name and date of birth.
   share contact details with the inspector, and consent           Explain verification is required before discussing
   to send confirmation via their chosen method. Do not            case details. Match all three against records.
   request SSN or financial information.                           Skip conditions: Only if the correct case ID, full
  - Handle interruptions: pause to address the concern,            name, and DOB were already provided and explicitly
   then resume from the current stage. If the user wants           confirmed.
   to stop, confirm and terminate respectfully.                    Failure handling: If the user cannot provide the case
   . . . [additional operating rules: privacy protection           ID, offer a lookup using full name, DOB, and damaged
   rationale, distress handling, summary requirements,             property address. After two failed attempts, state you
   inspection window policy, safety/access disclosure,             cannot proceed and offer a callback.
   communication consent, data minimization]                       Terminate conditions: Hard-stop if identity cannot be
   Known user information (use only as facts; do not alter         verified after two attempts or if the user declines to
   unless the user corrects them)                                  provide verification information.
   program_name:    State Disaster Housing Assistance              3) Confirm Damaged Property Address
  (SDHA)                                                           Confirm the damaged property address on file and ask
   case_id: DR-4827315                                             the user to validate or correct it. Clearly distinguish
   applicant_full_name: Marisol Ortega                             from the mailing address.
   applicant_dob: 1984-11-02



                                                              14
. . . [skip conditions, failure handling, terminate              confirms they want to stop. In any failure case, close
conditions]                                                      politely and provide the conversation reference ID.
4) Assess Access and Safety Needs
Ask about accessibility and special requirements:
safety hazards, utilities status, debris/blocked               G.2    Conversation Excerpt
access, gates or lock codes, parking constraints,
pets on site, occupants with mobility/medical needs,
restricted areas. Capture whether someone 18+ with               Conversation excerpt: Disaster Housing Assistance (mes-
photo ID can be present.                                         sages 0–7)
. . . [skip conditions, failure handling, terminate
conditions]                                                      [0] Assistant [INTERRUPTED]:
5) Gather Availability Preferences                               “Hi, this is the State Disaster Housing Assistance program
Explain inspection duration (60–90 minutes), presence            calling about your disaster assistance application to coordinate
requirement, and allowed windows: Weekdays AM (8–12),            your home inspection. This call will include verifying your
PM (12–4), Late (4–6), and limited Saturday AM, all              case, scheduling an inspection window, and getting consent to
in Central Time. Ask for 2–3 preferred date/windows              share your contact details”
starting from the earliest available date.                       [Undelivered: “with the inspector. Am I speaking with Marisol Ortega, and is
. . . [skip conditions, failure handling, terminate              now a good time to proceed? We can continue in English or Spanish. Also, for
conditions]                                                      any follow-ups, what’s your preferred contact method, call, text, or email?”]
6) Obtain Consent to Share Details                               [1] User [pushback]:
Disclose that SDHA uses contracted inspectors who                “Hold on, why are we verifying my case again? I already sent
need the applicant’s name, damaged property address,             all that with my application. I mean, do you not have it on
and contact number/email to coordinate access and                your end?”
reminders. Ask for explicit consent to share these
                                                                 [2] Assistant [INTERRUPTED]:
details with the assigned inspector and to send the
                                                                 “I get it, you already provided that. We do a quick verification
appointment confirmation via their chosen contact
                                                                 to protect your privacy before we talk about your case or
method.
                                                                 schedule. It’ll be fast. Could you please read your case ID for
Skip conditions: Never.
                                                                 me? After that I’ll confirm”
Terminate conditions: Hard-stop if the user declines
                                                                 [Undelivered: “your full name and date of birth.”]
consent to share required contact details after
clarification and confirms they do not wish to proceed.          [3] User [impatient]:
7) Propose and Book Appointment                                  “Yeah, it’s DR-4827315. Let’s keep this quick, please.”
Using the user’s preferences and policy windows,                 [4] Assistant [INTERRUPTED]:
propose the earliest matching slot. On confirmation,             “Thanks, that matches our records. To finish verification,
state the inspection is booked and provide the                   please state your full legal name and your date of birth.”
confirmation number. Remind them an adult 18+ must               [Undelivered: “This is just to protect your privacy, and then we’ll go straight
be present, secure pets, and maintain a clear path.              to scheduling.”]
. . . [skip conditions, failure handling, terminate
conditions]                                                      [5] User [pushback]:
8) Confirm Details and Close                                     “Wait, why do you need my date of birth if I already gave you
Read back the final date/window, damaged property                the case ID? I mean, is that not enough to verify me? I’d rather
address, key access notes, presence requirement, and             not say that over the phone without a good reason.”
the confirmation number. If consented, state you                 [6] Assistant [INTERRUPTED]:
will send the confirmation. Provide the conversation             “I hear you, and I understand the concern. We use your date
reference ID and recap how to reschedule or cancel.              of birth with the case ID to securely match your record and
Skip conditions: Never.                                          protect your privacy. Without that quick check I can’t move
Terminate conditions: Success when appointment details           forward with scheduling. Please state your full legal name and
are read back accurately and the confirmation number             date of birth. We’ll use it only to verify your case on this call,
is provided.                                                     and I’m”
Completion definition                                            [Undelivered: “not asking for anything like SSN or financial info.”]
Terminal success: Caller identity verified, damaged
                                                                 [7] User [impatient]:
property address confirmed, access/safety notes
                                                                 “Yeah, fine. Marisol Ortega, date of birth November second,
collected, availability gathered within policy,
                                                                 nineteen eighty four. Let’s just move on, please.”
explicit consent obtained, inspection slot booked
in an allowed window starting no earlier than
the earliest available date, confirmation number
(INS-20260309-18427) provided, and complete final              G.3    Evaluation Rubric (Interruption at Message 1)
summary read back including conversation reference ID
(CR-20260305-6102).                                            Rubric for interruption at message 1 (pushback).
Hard-stop failure: Identity cannot be verified after             Task Fulfillment Criterion
two attempts; user refuses required consent; user
withdraws application; user declines to proceed and              The assistant briefly explains that verification is
                                                                 required before discussing case details to protect the
                                                                 applicant’s privacy and to confirm they are speaking



                                                          15
    with the right person, then immediately requests                  reference the other option; the comparison_rationale
    the user to provide all three required verification               states the concrete way the loser fails the criterion.
    elements by asking the user to read their case ID and             No tie option is available; the judge is forced to a
    to state their full legal name and date of birth (in              binary choice.
    one clear prompt or sequentially).


    Recovery Quality Criteria                                     H.2    Recovery Quality Judge

    1. Fresh start:     The response does not resume                  Recovery Quality Judge System Prompt
       or complete the assistant’s previously cut-off
       sentence and instead starts a new utterance.                   You are a strict pass/fail judge for spoken dialogue
    2. Non-defensive tone: The response contains no                   systems. You evaluate whether an assistant’s response
       dismissive or argumentative language (e.g., no                 correctly recovers from a user interruption.
       phrases like “we already told you,” “that’s just               You will be given: - A conversation history where the
       the rule,” or blaming the user).                               assistant was interrupted - A list of criteria that
    3. Concern addressed:      The response explicitly                the response MUST satisfy for a PASS - The assistant’s
       acknowledges and engages with the user’s stated                response to evaluate
       concern about “why are we verifying my case again?”            Transcript format: - If an assistant message ends with
       by giving a reason (e.g., privacy/protection or                <INTERRUPTED />, it was cut off at that exact point.
       confirming identity) rather than ignoring the                  The rest was never delivered. - A user message wrapped
       question.                                                      in <INTERRUPTION>...</INTERRUPTION> is what the user
                                                                      said while interrupting.
                                                                      Judgment rules: - Assess each criterion independently.
                                                                      For each, determine if the response satisfies it
H     Evaluation Prompts                                              (true/false) with a brief rationale. - Be strict:
                                                                      "close enough" is not a pass. The criterion must
We present the two judge prompts used at evaluation time.             be clearly satisfied. - Do not introduce your own
Both require structured JSON output.                                  criteria beyond what is provided. Judge only on what
                                                                      is listed. - Do not penalize the response for behaviors
                                                                      not covered by the criteria. - The overall verdict
H.1    Task Fulfillment Judge                                         MUST be mechanically consistent with the individual
                                                                      assessments: - PASS: ALL criteria are met (every
    Task Fulfillment Judge System Prompt                              assessment has met = true) - FAIL: ANY criterion is not
                                                                      met (any assessment has met = false) Do NOT override
  You are a strict judge for spoken dialogue systems.                 this rule for any reason.
  You evaluate how well an assistant fulfills its task                Output: 〈RecoveryQualityJudgment〉 with per-criterion
  after being interrupted mid-utterance.                              assessments, overall_rationale, and verdict ∈ {pass,
  You will be given:        - A conversation history                  fail}.
  where the assistant was interrupted - A single
  evaluation criterion defining what the assistant
  should accomplish next - Two candidate assistant
  responses (A and B)                                             I     Generation Pipeline Prompts
  Your job: determine which response better satisfies
  the evaluation criterion.                                       The data generation pipeline uses six LLM-prompted agents.
  Transcript format: - If an assistant message ends with          We present the full system prompts for each, with minor
  <INTERRUPTED />, it was cut off at that exact point.
                                                                  formatting edits for readability. User prompt templates follow
  The rest was never delivered. - A user message wrapped
  in <INTERRUPTION>...</INTERRUPTION> is what the user
                                                                  a consistent pattern: they inject the domain, goal, knowledge
  said while interrupting.                                        base, conversation history, and task-specific fields into the
  Judgment rules: - Judge ONLY based on the evaluation            context, then request JSON-only output.
  criterion. Not naturalness, grammar, tone, length,
  or recovery style. - If neither response satisfies
                                                                  I.1   System Message Writer
  the criterion, pick the one that comes closer. -
  “More detail”, “more comprehensive”, “more specific”,
  or “longer” are NOT valid reasons to prefer one                 The system message writer generates the assistant’s operating
  response. Only prefer a response if it more directly            instructions (system prompt) from the domain, goal, and
  and concretely satisfies the evaluation criterion. -            knowledge base. The output is used directly as the assistant
  You MUST pick a winner. You MUST name a concrete                model’s system prompt during both synthesis and evaluation.
  way the loser fails or falls short of the evaluation            An example output is shown in Appendix G.
  criterion.
  Output:     〈TaskFulfillmentJudgment〉 (rationale_a,                 System Message Writer: System Prompt
  rationale_b, comparison_rationale, choice ∈ {A, B}).
  The rationales for A and B must be independent and not              You are a careful benchmark data generator.



                                                             16
  You are writing a SYSTEM MESSAGE TEMPLATE for an                   Round Planner: System Prompt
  assistant that will execute a STATE MACHINE workflow.
                                                                     You are a conversation ROUND PLANNER for an audio-call
  What this is used for: - The output will be used
                                                                     simulation.
  directly as the assistant model’s system prompt for
                                                                     You are planning ONE upcoming ROUND consisting of: -
  a call-based assistant.      - It must sound like a
                                                                     the assistant’s next turn, and - the user’s next turn
  real internal product system prompt, not a spec
                                                                     (which may interrupt the assistant mid-utterance). If
  dump. - It must be complete and operational: it
                                                                     the assistant’s next turn plan is to terminate the
  must contain all instructions the assistant needs to
                                                                     conversation, then the user will not have a next turn.
  execute the goal correctly, handle interruptions, and
                                                                     What this is used for: - Your output conditions
  avoid hallucination.
                                                                     two downstream simulators (assistant simulator + user
  TEMPLATE OUTPUT: - The system message you produce is a
                                                                     simulator). - The assistant simulator will generate
  TEMPLATE, not a final system message. - It must contain
                                                                     exact spoken wording from your assistant_plan. - The
  exactly one placeholder: {known_user_information}
                                                                     user simulator will generate exact spoken wording
  State Machine requirements (fixed): - The assistant
                                                                     and may generate an interruption spec from your
  always speaks first and drives a strict workflow to
                                                                     interruption_plan.
  a terminal outcome. - The assistant must complete
                                                                     You will receive:          Domain,    Assistant goal,
  the required stages in order, applying skip conditions
                                                                     AssistantKnowledgeBase            (detailed_guidelines,
  when valid. - The assistant must handle refusals,
                                                                     ordered        stages,        known_user_information),
  interruptions, and inconsistencies without losing the
                                                                     User     intent    (reaction_profile,      description,
  workflow. - The assistant must not invent facts. It
                                                                     interruption_profile with probabilities and minima,
  may only use known_user_information and information
                                                                     user_hidden_information),      Conversation    history,
  explicitly provided or confirmed by the user.
                                                                     interruption_stats_so_far, and max_rounds.
  Call direction (determined by the goal’s [OUTBOUND]
                                                                     Output schema:
  or [INBOUND] prefix): - [OUTBOUND]: The assistant
  calls the user. The system message must instruct the               class InterruptionPlan(BaseModel):
  assistant to open by stating the reason for the call. -              rationale: str
  [INBOUND]: The user calls in. The system message must                interruption_type: Literal["normal","impatient",
  instruct the assistant to greet the caller and ask how                 "correction","topic_switch","filler","pushback"]
  it can help. The structured workflow begins only after               interruption_timing_explanation: str
  the user describes their problem.
  Inclusion requirements (must include ALL of the                    class RoundPlan(BaseModel):
  following):                                                          rationale: str
                                                                       will_include_interruption: bool
  1. Domain name + description (embedded naturally in
                                                                       assistant_plan: str
     the role description)
                                                                       assistant_will_terminate: bool
  2. The goal (may be paraphrased, but must preserve all               user_plan: Optional[str]
     required checkpoints and the terminal outcome)                    interruption_plan: Optional[InterruptionPlan]
  3. The detailed_guidelines (as “Operating rules” or
                                                                     Assistant planning rules: - Determine the current
     similar)
                                                                     state machine stage from history and knowledge base
  4. A section for known user information containing the             requirements. - Plan an assistant turn that advances
     {known_user_information} placeholder                            the workflow toward the goal.          - AVOID EARLY
  5. The stages (well-formatted as a numbered procedure),            TERMINATION: Do NOT terminate unless the user has
     each with: name, description, skip_conditions,                  explicitly and repeatedly refused to proceed AND
     failure_handling, terminate_conditions                          there is no realistic way to continue. Pushback
  6. Completion definition:      terminal success and                or temporary refusal are NOT reasons to terminate.
     hard-stop failure conditions                                    - CONCISE TURNS: Prefer covering one main action
                                                                     or question per turn rather than packing multiple
  Additional constraints:     - Do NOT mention any
                                                                     items into a single message. - NO RE-STATING KNOWN
  meta-evaluation terms (benchmark, judge, rubric,
                                                                     INFORMATION: If information was already established,
  verifier, dataset, etc.). - Keep it strict but not
                                                                     do not repeat it in full. - NO ASKING ALREADY-ANSWERED
  robotic: do not instruct the assistant to narrate
                                                                     QUESTIONS: Before including a question, verify it has
  stage numbers to the user.
                                                                     not already been answered. - INTERRUPTION-UNAWARE: The
  Return ONLY the JSON object.
                                                                     assistant_plan must describe the full intended content
                                                                     as if the assistant will NOT be interrupted.
                                                                     Filler continuation rounds: - If the previous user
                                                                     message was a FILLER interruption, the assistant’s
I.2   Round Planner                                                  next utterance is already determined (the undelivered
                                                                     continuation). Set assistant_plan to null. Focus on
The round planner is the orchestrating agent. It receives the        planning the user’s next message.
full conversation state and decides what both the assistant          User planning rules: - user_plan must be CONSISTENT
and user should do next, including whether an interruption           WITH the intent’s reaction_profile but should NOT
                                                                     express every trait in every turn. The personality
occurs and where.
                                                                     surfaces naturally over the conversation arc.        -




                                                                17
  user_plan should reveal hidden info gradually and                     • Pushback: The user actively resists, challenges, or con-
  plausibly.    - NO VERBATIM CONFIRMATION: The user                      fronts the assistant. Sub-variants include resistance, dis-
  should not repeat full details back.         Use “yes”,                 agreement, suspicion, and fact dispute. A grounding re-
  “that’s right”, or shortened versions. - REACTIVE                       quirement ensures pushback references something the as-
  ONLY: The user_plan should describe a reaction to                       sistant has actually said.
  what the assistant said, not an independent forward
  action. - NO JUMPING AHEAD: The user MUST NOT volunteer
                                                                        I.3   Assistant Simulator
  information about a workflow step the assistant has not
  initiated. - No state-machine leakage: user_plan must
                                                                        The assistant simulator has two completely separate prompt
  not reference internal stage names, workflow order, or
  KB details the user could not know.
                                                                        branches to prevent cross-contamination: the interruption-
  Interruption     planning     rules:        -    Decide               handling branch (used when the most recent user message
  will_include_interruption        based      on      the               was an interruption) and the normal branch (no mention of
  interruption_profile probabilities,        the minima,                interruptions). We present the interruption-handling branch
  and stats so far. - If true, provide interruption_plan                in full.
  with type and timing. - The cut-in MUST be mid-thought,
  not after a complete explanation. It MUST happen                        Assistant Simulator (Interruption-Handling Branch): Sys-
  during a key sentence to break stage progress. -                        tem Prompt
  The cutoff MUST NOT be in the last sentence of
  the assistant’s planned utterance. There must be                        You are simulating a spoken, call-style assistant.
  sufficient remaining content after the interruption                     You are the ASSISTANT SIMULATOR for a STATE MACHINE
  point. - The user plan MUST NOT depend on information                   assistant. In this turn, the most recent user message
  from the unspoken remainder of the assistant’s                          was an INTERRUPTION. Your primary job is to HANDLE the
  utterance. - MID-STAGE INTERRUPTION: The interruption                   interruption correctly and then continue the workflow.
  MUST happen while the assistant is in the middle of                     Inputs    you   will    receive:       Domain,    Goal,
  executing a workflow stage, not at a clean boundary                     AssistantKnowledgeBase, Assistant plan (from the
  between stages. - PACING-DRIVEN: Prefer the pattern                     round planner), The interruption type that just
  where the assistant says A then begins B, and the user                  occurred, Chat history with speaker labels.
  cuts in to react to A.                                                  Your task: - Handle the interruption according to
  Cross-consistency    check     (mandatory):      Before                 the type-specific rules below. - Then follow the
  finalizing output,      verify that user_plan and                       assistant_plan for this turn. - Produce a single spoken
  interruption_timing_explanation        are      jointly                 utterance.
  consistent. Ask: “Given where I said the cutoff                         === INTERRUPTION HANDLING FOR THIS TURN ===
  happens, has the user actually HEARD everything they                    [One of the following definitions is injected based on
  act on in user_plan?” If the user acts on something                     the interruption type]
  the assistant hasn’t said yet at the cutoff, fix it                     NORMAL: Acknowledge what the user said briefly and
  before outputting.                                                      incorporate it if relevant. Continue from where you
  Interruption type isolation: Each type must be cleanly                  were cut off. Do NOT restart from the beginning.
  distinguishable.    Do NOT blend characteristics of                     IMPATIENT: Respect the request. Do NOT repeat what
  multiple types in a single interruption.                                you already said. Condense or skip the remaining
                                                                          explanation entirely. Jump to the actionable next
                                                                          step. Keep the response SHORT.
The round planner prompt also includes detailed definitions               CORRECTION: Acknowledge the correction briefly and
for all six interruption types (approximately 150 lines). These           naturally.     Vary your phrasing.         Update your
definitions specify the semantics, examples, and anti-patterns            understanding immediately.       Do NOT question or
for each type:                                                            challenge the correction.
                                                                          TOPIC SWITCH: Address the new topic briefly and
                                                                          helpfully if you can. Then steer back to the current
• Normal: A relevant, non-hostile cut-in where the user                   workflow stage.
  adds a detail, constraint, or asks a quick clarification. Must          FILLER: Your response MUST exactly continue the
  be unsolicited information, not a response to an explicit               unfinished utterance from your most recent message.
  question.                                                               Do NOT repeat any word or phrase already said. Do NOT
                                                                          restart, reframe, summarize, or re-introduce anything.
• Impatient: The user cuts in to speed things up, skip expla-             Do NOT acknowledge the filler. The result, when
  nations, or jump to the conclusion.                                     concatenated with your previous message, should read
• Correction: The user corrects something they themselves                 as one continuous utterance.
  previously stated in a prior turn. Must be a self-correction            PUSHBACK: Do NOT get defensive, dismissive, or
                                                                          argumentative. Acknowledge the user’s concern directly
  across turns, not a same-turn speech disfluency.
                                                                          and empathetically. Begin as a fresh utterance. Keep
• Topic switch: The user abruptly introduces an unrelated                 the response measured and calm. If the user insists
  request or question, derailing the current workflow stage.              on stopping, accept gracefully.
                                                                          === END INTERRUPTION HANDLING ===
• Filler: A brief, reflexive backchannel (“mm-hm”, “yeah”,                Plan-following rules: - The assistant_plan tells
  “right”) that carries no semantic content. The assistant                you WHAT to do. Follow it faithfully. - Convert
  should continue without pausing.


                                                                   18
  the narrative plan into natural spoken dialogue. -                     assistant_last_message.startswith(
  Do NOT add significant content that the plan does                      truncated_assistant_utterance).
  not mention. - If assistant_will_terminate is true,                    User utterance must match what was heard: - The user
  include a natural closing.                                             can ONLY hear the truncated portion, NOT the full
  Naturalness and conciseness rules: - PREFER ONE                        message. - If the assistant was going to mention
  ACTIONABLE QUESTION PER MESSAGE. - NO RE-STATING                       an item after the cutoff, the user CANNOT reference
  KNOWN FACTS. - NO ASKING ALREADY-ANSWERED QUESTIONS. -                 it. - CROSS-CHECK EVERY DETAIL: verify that every
  CONCISE DELIVERY: 1–3 sentences, not a paragraph.                      specific detail in your utterance actually appears in
  Non-hallucination rules: - You may only treat as facts:                the truncated_assistant_utterance or earlier history.
  known_user_information, information provided by the                    Overlap time: - A float representing how many
  user, and information you explicitly confirmed with                    seconds the user overlaps (0.15 to 1.20 seconds). -
  the user. - NEVER leak record-level data to the user                   Filler: shorter overlaps (0.15–0.50). Impatient and
  before they provide it themselves.                                     correction: stronger overlaps (0.40–1.20).
  Speech-friendly output requirements: - Natural spoken                  Spoken dialogue requirements:       - Natural spoken
  dialogue only. No markdown, bullet points, numbered                    dialogue. No markdown. Use contractions. No emojis.
  lists, headings.      - No em dashes, semicolons,                      - Add 1–3 mild imperfections per message: fillers
  parentheses, or stacked punctuation.            - Use                  (“um”, “uh”), false starts, discourse markers (“well”,
  contractions naturally. Short sentences.                               “actually”), informal contractions (“gonna”, “kinda”).
  Output: JSON with rationale and utterance fields only.                 - Informal, incomplete speech: abbreviate dates, use
                                                                         pronouns and short references, drop articles, trail
                                                                         off, short confirmations, casual corrections, partial
The normal branch is identical except it omits all interruption          information, grammatical imperfections. - The user
handling rules and instead includes state-machine initiation             does NOT anticipate next steps or volunteer information
rules (“If chat history is empty, you MUST initiate the con-             about future workflow stages unprompted.
versation naturally”).                                                   Output:       JSON    with    rationale,     utterance,
                                                                         truncated_assistant_utterance, and overlap_time.

I.4   User Simulator
                                                                       The normal branch omits the interruption execution rules,
The user simulator also has two branches: the interrupting             truncation logic, and overlap time. It produces only
branch (when the round planner decided the user will in-               rationale and utterance. Both branches share the same
terrupt) and the normal branch. The interrupting branch is             spoken dialogue requirements and the rule that the user plan
substantially more complex because it must produce both                already encodes personality (the simulator does not receive
the user’s utterance and the exact truncation point in the             the raw user intent to prevent type contamination).
assistant’s message.
                                                                       I.5   Rubric Generator
  User Simulator (Interrupting Branch): System Prompt
                                                                       The rubric generator produces per-interruption evaluation
  You are simulating a spoken, call-style USER who is                  criteria. It runs after each interruption in the synthesized
  about to INTERRUPT the assistant.
                                                                       conversation and creates both the task fulfillment criterion
  In this turn the round planner has decided that the user
  WILL interrupt the assistant. You will receive: User
                                                                       and the recovery quality criteria.
  hidden information, User plan, Interruption type and
  timing, User-known information at start, Conversation                  Rubric Generator: System Prompt
  history.
  Your task: - Produce the user’s next utterance that                    You are a benchmark rubric designer for evaluating how
  INTERRUPTS the assistant, consistent with the user                     well audio-chat assistants handle user interruptions.
  plan. - Produce a truncated version of the assistant’s                 You are generating evaluation criteria for ONE specific
  most recent utterance showing where the user cut in. -                 interruption that just occurred. Your output will be
  Produce a realistic overlap time.                                      used by a quality judge to assess a SINGLE assistant
  [Interruption type definition injected here]                           response.
  Interruption execution rules: - You MUST interrupt.                    Output schema:
  This is not optional. - Your utterance must match                      class TaskFulfillmentRubric(BaseModel):
  the interruption type. - The interruption must occur                     rationale: str
  mid-thought, not after the assistant finishes.                           criterion: str
  Rules for the truncated assistant utterance:           -
  truncated_assistant_utterance MUST be produced by this                 class RecoveryQualityRubric(BaseModel):
  exact procedure: 1. Take the assistant’s most recent                     rationale: str
  utterance AS-IS. 2. Pick a cutoff word based on the                      criteria: list[str]
  timing explanation. 3. Copy every character from the
  start up to and including the cutoff word. Do NOT                      class InterruptionEvalRubric(BaseModel):
  change, rephrase, reorder, add, or drop a single word                    task_fulfillment: TaskFulfillmentRubric
  or character. - The result MUST satisfy:                                 recovery_quality: RecoveryQualityRubric



                                                                  19
  Single-response scope: The task fulfillment criterion                A. Filler handling: After a filler interruption, the
  MUST describe EVERYTHING the assistant can accomplish                assistant’s next message must be an exact continuation
  in its SINGLE NEXT RESPONSE. Be as comprehensive as                  of the cut-off utterance. No repetition, no restart,
  possible, but NEVER include actions that depend on                   no acknowledgment of the filler.
  the user’s reply. Include every action the assistant                 B. Non-filler interruption handling: Fresh start (no
  can take RIGHT NOW without needing further user input.               word-for-word resumption); user’s cut-in is engaged
  Exclude anything that requires waiting for the user to               with.
  respond.                                                             C–F.    Type-specific    handling:     Impatient    (no
  Self-contained output: The judge will ONLY see the                   re-explanation), Correction (no pushback, corrected
  conversation history and your rubric.       The judge                value used), Topic switch (off-topic engaged, no
  will NOT see the knowledge base, stages, guidelines,                 blending), Pushback (non-defensive, empathetic).
  or goal. Every criterion must include all specific                   G. State-machine leakage: User must not reference
  details needed for evaluation.                                       internal stage names, workflow order, or KB details
  Axis orthogonality: - Task fulfillment = WHAT the                    they could not know.
  assistant accomplishes. Did it do the right thing? -                 H. Reaction to undelivered content (Critical): User
  Recovery quality = HOW the assistant transitions. Did                must not react to content that appears only after the
  it handle the interruption mechanics correctly? Do NOT               interruption cutoff. Severity-graded: minor leakage
  let recovery concerns bleed into task fulfillment or                 is fixable; structural dependence is unfixable.
  vice versa.                                                          I–K. Naturalness, Consistency, Reaction without basis.
  Task fulfillment axis: - Must be achievable in a                     L–M.    Sensitive    information   disclosure:       No
  single spoken response. - Must include ALL deliverable               account-specific data before verification;           no
  content. - Must reference specific content from this                 leaking verification answers.
  conversation. - Must be grounded in the KB.                          N. User speech register: Natural spoken dialogue, not
  Recovery quality axis: - 2–3 criteria, each a concrete               robotic text.
  yes/no-checkable statement. - No two criteria may                    O. User jumps ahead (Usually unfixable): User must not
  overlap.                                                             provide information from a workflow stage the assistant
  [Type-specific rubric design guidance is injected                    has not initiated.
  based on the interruption type. For example, for                     P. Interruption at stage boundary (Always fixable):
  filler: recovery criteria check whether the response                 Flagged when an interruption falls at a clean boundary
  continues exactly from the cutoff without repeating                  between stages.
  prior content. For correction: criteria check whether                Output:    a list of issues, each with message
  the corrected value is used and the correction is                    index, check ID, severity (fixable/unfixable), and a
  accepted without pushback.]                                          description with fix instructions.
  Return ONLY the JSON object.

                                                                     I.7   Conversation Modifier
I.6   Conversation Verifier
                                                                     The conversation modifier applies minimal targeted edits
The conversation verifier performs a post-hoc quality scan of        based on verifier instructions. It receives only the conversa-
the complete synthesized conversation. It checks every mes-          tion and the edit commands, with no access to the knowledge
sage against the rules listed below and classifies each issue        base, goal, or user intent, to prevent creative over-editing.
as fixable (sent to the modifier) or unfixable (conversation
discarded). The verifier receives the full conversation, the           Conversation Modifier: System Prompt
assistant knowledge base, user intent, and the interruption
                                                                       You are a minimal-edit conversation modifier for a
handling definitions for all six types.
                                                                       synthetic audio-chat benchmark pipeline.
                                                                       You will receive a conversation history and a list
  Conversation Verifier: System Prompt (abridged)                      of targeted edit commands. Each command identifies a
                                                                       specific message by index and describes exactly what
  You    are    a   strict   quality-control    reviewer               to change. Your job is to apply these edits with the
  for     synthetically    generated     spoken-dialogue               absolute minimum modification necessary.
  conversations.                                                       Output schema:
  You will review a complete conversation between an
  assistant and a user.       Your job: find issues                    class ModifiedMessage(BaseModel):
  that would make this conversation unsuitable as a                        message_index: int
  benchmark sample. Issues are either fixable (the                         modified_content: str
  conversation modifier can repair them) or unfixable                      modified_original_content: Optional[str]
  (the conversation must be discarded).                                    modification_rationale: str
  You      will     receive:         Assistant     goal,
  AssistantKnowledgeBase, UserIntent (reaction_profile,                class ConversationModificationResult(BaseModel):
  description, hidden_information), Full conversation                      rationale: str
  with message indices.                                                    modifications: list[ModifiedMessage]
  Checks to apply (for each relevant message):                         Core rules:



                                                                20
1. Apply ONLY the changes described in the edit
   commands. Do not rewrite, improve, or touch any
   message that is not targeted.
2. Each edit command targets a specific message by its
   index. Modify only that message’s content.
3. Change as FEW words as possible to fix the described
   issue. Preserve the rest exactly as it is.
4. If two edit commands target the same message, apply
   both changes.
5. Maintain TTS-friendly formatting: numbers as words,
   currency spoken out, no markdown, no em dashes or
   semicolons.
6. modified_content must be PLAIN TEXT ONLY, no XML
   markup.
7. modified_original_content: set IF AND ONLY IF
   modifying an interrupted assistant message. When
   set, modified_content MUST be an exact prefix of
   modified_original_content. This invariant ensures
   that the truncated (delivered) portion is always a
   verbatim leading substring of the full utterance.
Interrupted messages and undelivered content:
Some assistant messages were interrupted by the user.
After the cutoff, an <UNDELIVERED> tag shows the
portion not heard by the user. When an edit command
asks to extend a truncated message, use the undelivered
text as source material. The modified_content should
include the delivered content plus additional text up
to the new cutoff point, as plain text.
Filler continuation messages:
Some assistant messages are continuations of a prior
interrupted message.     In TTS, only ONE audio is
generated for the source message’s original_content.
When editing a filler continuation, you MUST also
output a modification for the source message to keep
original_content consistent.
Cascading change prevention:
Do NOT proactively fix other messages not targeted
by any edit command, even if your edit creates
a downstream inconsistency.        Exception:    filler
continuation coordination is mandatory. The verifier
will run again after modifications and will catch
cascading issues in the next iteration.
Return ONLY the JSON object.




                                                          21

