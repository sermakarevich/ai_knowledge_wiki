---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: StepAudio 3 Realtime Technical Report

### Q1. What is the listen-converse-think-act loop, and what tension does Think-While-Speaking resolve?
> [!tip]- Answer
> StepAudio 3 Realtime organizes realtime interaction as a continuous loop where Deep Perception interprets intent, Seamless Duplex manages the floor, Think-While-Speaking reasons in parallel with delivery, and a streaming Voice Agent executes tools asynchronously. The core tension is deep deliberation versus latency: complex requests need careful reasoning while pauses, backchannels, and interruptions must stay fluid. Think-While-Speaking resolves it by executing private reasoning in parallel with spoken delivery, reaching 73.0 macro average on StepAudioChat in reasoning mode and 70.4 in Interactive realtime mode. See [[wiki/01-overview-listen-converse-think-act-loop|Overview: Listen-Converse-Think-Act Loop]].

### Q2. What makes up the shared conversational context, and how is model-side speech used?
> [!tip]- Answer
> The context combines acoustic and linguistic evidence, dialogue history, the current speaking turn, reasoning progress, and tool-execution status, retaining what the user says and how it is said. Model-side speech is itself context: it helps interpret user utterances that overlap with a response. Newly observed speech or returned tool results can change listen/speak, reason-further, and act decisions as the conversation proceeds. See [[wiki/02-architecture-foundation-training|Architecture and Foundation Training]].

### Q3. What are the three pretraining stages and the midtraining extension, and how does ASR Max diverge?
> [!tip]- Answer
> Pretraining runs modality alignment (acoustic-to-LM interface), multimodal mixed training (joint audio-text modeling at scale), and cooldown (greater weight on high-quality data) at fixed 32K length over 1.2T tokens with an increased pure-text share. Midtraining extends context to 128K for longer histories and tool results and raises the audio-understanding and agent-interaction data share. ASR Max diverges only at SFT: it packs examples into 32K sequences, freezes the audio encoder, updates adapter plus decoder with SpecAugment-style masking, and fuses hypotheses with ROVER plus LLM punctuation restoration. See [[wiki/02-architecture-foundation-training|Architecture and Foundation Training]].

### Q4. How is StepAudio 3 ASR Max evaluated, and what does it achieve on standard sets and ContextASR-Bench?
> [!tip]- Answer
> ASR Max is tested on LibriSpeech test-clean/test-other, AISHELL-1, and WenetSpeech test-net/test-meeting (WER for English, CER for Mandarin), plus ContextASR-Bench in the Contextless setting with no domain labels or hotword injection. It is best on both LibriSpeech subsets and AISHELL-1, ahead of Doubao 2.0 ASR and Seed 2.0 Lite on both WenetSpeech subsets while trailing HY3.0 ASR Preview by a small margin. On ContextASR-Bench it leads all four subsets (English/Mandarin × Speech/Dialogue) with macro averages of 5.67% English and 1.23% Mandarin versus 6.60% and 1.69% for HY3.0. See [[wiki/03-deep-perception-asr-max|Deep perception: StepAudio 3 ASR Max and audio understanding]].

### Q5. How is audio-understanding SFT data built, and what does the quality-over-volume ablation show?
> [!tip]- Answer
> Data follow a five-stage pipeline — sampling, description, capability tagging, query construction, labelling with multi-model agreement — plus deterministic checks, text-only LLM quality/case-value judging, and cross-model consistency filtering for grounding. The ablation compares ~2M random examples against ~100K quality-controlled ones with SFT data as the only changed factor. Despite using roughly one twentieth the examples, the curated set lifts MMSU 78.78 → 89.70, MMAR 74.70 → 84.50, WildSpeech 74.20 → 77.11, and MTalk-Bench ambient/paralinguistic/semantic macro 88.83 → 90.84. See [[wiki/03-deep-perception-asr-max|Deep perception: StepAudio 3 ASR Max and audio understanding]].

### Q6. How does Seamless Duplex decide when to listen, speak, or yield?
> [!tip]- Answer
> Roles are context-dependent (e.g. "right" as backchannel versus correction preface) and interpreted from both audio streams plus dialogue history. Pauses versus turn endings are distinguished by acoustic timing plus semantic completeness; brief acknowledgments during model speech signal engagement without floor transfer while substantive requests signal interruption intent. Background speech is rejected using dialogue history as evidence for whether speech is directed at the assistant. See [[wiki/04-seamless-duplex-floor-management|The conversational role of a user: seamless duplex floor management]].

### Q7. How is full-duplex trained and what does it score on the Artificial Analysis bench?
> [!tip]- Answer
> Midtraining adapts the model to time-interleaved 320 ms-block representations with streaming ASR, VAD, and utterance-completeness supervision on 10,000+ hours of synthetic full-duplex data plus text data; post-training refines turn taking, backchannel, interruption, and background-rejection behavior. On the AA full-duplex subset (pause, turn taking, interruption, backchannel handling) it ranks first with 98.9 overall versus 98.4 for Qwen Audio 3.0 Realtime Plus. Category scores are 100.0 turn taking, 99.0 interruption handling, 98.9 pause handling, and 98.0 backchannel handling. See [[wiki/04-seamless-duplex-floor-management|The conversational role of a user: seamless duplex floor management]].

### Q8. What does StepAudio 3 score in reasoning mode on StepAudioChat, and where does it lead or lag?
> [!tip]- Answer
> In reasoning mode it scores 73.0 macro average, ahead of Doubao 2.0 Lite (70.5) and DeepSeek-V4-Flash (71.4) but behind Kimi K3 (77.1). It ranks second on reasoning (73.0), memory (72.0), knowledge (73.1), conversational pragmatics (67.2), and persona & role consistency (80.9). Kimi K3 leads six of eight dimensions including reasoning at 81.9, while Doubao leads instruction following (72.9) and persona consistency (82.6), showing strong aggregate reasoning does not imply uniform instruction-following strength. See [[wiki/05-conversational-intelligence-stepaudiochat|Conversational Intelligence — Reasoning-Mode Evaluation]].

### Q9. How do Think-While-Speaking and Adaptive Thinking work?
> [!tip]- Answer
> Two concurrent calls to the same model act as Formulation Brain (private reasoning trace) and Articulation Brain (short spoken segments conditioned on reasoning so far), with playback-aware scheduling; Speak-First starts without a reasoning prefix by default while Think-First waits for one. Adaptive Thinking routes each turn to immediate (empty think block) versus deliberate response, supervised by a blind-judge comparison of original versus no-think answers with per-domain no-think budgets. Think rates range 51.5–82.0% across categories, but Reasoning gets only 59.5% despite gaining most from full thinking (+11.37 over forced no-think). See [[wiki/05-conversational-intelligence-stepaudiochat|Conversational Intelligence — Reasoning-Mode Evaluation]].

### Q10. What are the MTP acceleration results and the strict-versus-typical acceptance trade-off?
> [!tip]- Answer
> MTP3/MTP5 draft up to three/five future tokens per target step with 1.05 repetition penalty on private reasoning only; Medusa-style typical acceptance uses an entropy-adaptive threshold to accept plausible drafts strict verification would reject. Accepted tokens per step are 1.231 (MTP3 strict), 1.801 (MTP3 typical), 1.353 (MTP5 strict), 2.153 (MTP5 typical) with wall-clock speedups of 1.76×, 2.05×, 1.49×, and 1.72×. All MTP configs improve Reasoning (up to 74.30 vs 70.76) and Memory but lower Instruction Following, and strict marginal rates for MTP5 heads 4–5 fall to 10.7% and 5.7%, showing diminishing depth gains. See [[wiki/06-think-while-speaking-adaptive-reasoning|Think While Speaking, Adaptive Reasoning and MTP Acceleration]].

### Q11. How are the four specialized teachers merged, and what balance does the merge achieve?
> [!tip]- Answer
> Four compatible teachers from a common base with different data mixtures are averaged in parameter space as θmerge = Σαiθi (αi ≥ 0, Σαi = 1) with normalized 3:1:1:1 weighting selected on held-out dialogue, audio, and text evaluations, adding no components or routing. The merge reaches 81.3 macro on audio understanding (tying the best teacher, leading MMAU and WildSpeech), 76.5 on general text (highest, best HMMT 2026 Feb and GPQA Diamond), and 73.0 on dialogue (above Teachers 2–4, below Teacher 1 at 74.2). It is framed as retaining complementary strengths rather than matching the best teacher on every metric. See [[wiki/06-think-while-speaking-adaptive-reasoning|Think While Speaking, Adaptive Reasoning and MTP Acceleration]].

### Q12. How does the voice agent handle tools, and what are the τ-Voice results?
> [!tip]- Answer
> Requests route by type: stable knowledge answered directly, up-to-date public info via lightweight tools (weather, web search), and private-context/multi-step/beyond-turn work to asynchronous backend execution that continues alongside conversation. Before external action the model clarifies missing info or retrieves context and obtains required confirmation; during execution it links task-related input to the ongoing task, separates unrelated dialogue, and folds results back per the ReAct pattern. On τ-Voice it reaches 56.0% macro (Grok 56.5%, Qwen 54.6%, GPT 45.7%), best telecom 70.2% and near-best airline 60.0% but weak retail 37.7%. See [[wiki/07-voice-agent-tool-execution|Voice Agent Tool Execution and Agentic Task-Completion Results]].

### Q13. What does Table 10 show across the five capability domains?
> [!tip]- Answer
> Table 10 uses a 0–100 higher-is-better scale with bold/underline for best/second-best; for dialogue, StepAudio 3 uses realtime Interactive mode while others use reasoning mode. It leads MMSU (90.6) and MMAR (86.5) plus Step-Caption and MTalk-Bench, but trails Gemini 3.1 Pro on Big Bench Audio, MMAU, WildSpeech, and AudioMultiChallenge (49.3 vs 67.0). Interactive StepAudioChat is 70.4 macro, comparable to Doubao (70.5) and DeepSeek (71.4) behind Kimi K3 (77.1); it leads HMMT 2026 Feb (86.8), ranks first on AA Full-Duplex (98.9), and reaches 56.0 on τ-Voice near Grok's 56.5. See [[wiki/08-capability-evaluation-benchmarks|Capability Evaluation Benchmarks (Table 10)]].

### Q14. Which references anchor the audio-model foundations, full-duplex systems, and decoding methods?
> [!tip]- Answer
> Foundations include AudioLM [4], SALMONN [5], and a paralinguistics-aware speech LLM [6], with lineage from Step-Audio unified work through Step-Audio-R1/R1.5 and StepAudio 2.5 plus Mind-Paced Speaking dual-brain reasoning [13]–[17] and the Qwen3-Omni encoder source [8]. Full-duplex cites Freeze-Omni [9], Moshi [10], chronological thinking and DuplexSLA [11]–[12], and Bayling-Duplex [26]. ASR and acceleration cite SpecAugment [18], ROVER [19], and speculative/Medusa/MTP decoding [28]–[31], with agent grounding from Toolformer, Gorilla, and ReAct [32]–[34]. See [[wiki/09-references-audio-language-models|References: Audio Language Models and Streaming Speech Systems]].

### Q15. Which references cover the evaluation benchmarks and the industry baseline models?
> [!tip]- Answer
> Speech/dialogue benchmarks are WildSpeech-Bench [40], AudioMultiChallenge [41], Step-Caption [42], MTalk-Bench [43], and the HMMT February 2026 archive [44]. General LLM evaluation cites GPQA [45] and MultiChallenge [46]. Industry baselines [47]–[56] document Seed2.0, Tencent HY ASR 3.0, Gemini 3 Flash / 3.1 Pro, DeepSeek-V4-Flash, Kimi K3, GPT-Realtime-2/2.1, Qwen speech-to-speech models, and Grok Voice Think Fast 2.0. See [[wiki/10-references-benchmarks-evaluation|References: Benchmarks and Evaluation (Refs 40–56)]].

### Q16. For a customer-service voice deployment strong on telecom but weak on retail, would you recommend StepAudio 3 Realtime, and what would you watch?
> [!tip]- Answer
> I would recommend it for telecom-heavy use since it leads τ-Voice telecom at 70.2% with first-place 98.9 full-duplex floor control and near-parity Interactive dialogue (70.4 vs 70.5–71.4), accepting the retail gap (37.7% vs Grok 49.7%). I would watch multi-turn constraint handling and AudioMultiChallenge-style revision tracking, plus Adaptive Thinking's under-allocation of reasoning (59.5% think rate on Reasoning) and retail tool-use failures before committing to external actions. Pilot with telecom scripts first and add confirmation-gated retail flows with progress-update handling. See [[wiki/07-voice-agent-tool-execution|Voice Agent Tool Execution and Agentic Task-Completion Results]].
