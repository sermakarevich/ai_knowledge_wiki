> [[index|Wiki]] | [[summary|Summary]]

# StepAudio 3 Realtime Technical Report — Digest

## 1. [[wiki/01-overview-listen-converse-think-act-loop|Overview: Listen-Converse-Think-Act Loop]]

**In one sentence:** StepAudio 3 Realtime is an audio-language foundation model organized around a continuous listen-converse-think-act loop that combines Deep Perception, Seamless Duplex, Think-While-Speaking, and a streaming Voice Agent to deliver deep reasoning in real-time spoken interaction.

## Key points
- The core problem is the tension between deep deliberation and latency: the model must reason carefully about complex requests while keeping pauses, backchannels, and interruptions fluid.
- Deep Perception captures linguistic and nonverbal acoustic evidence to interpret user intent, while Seamless Duplex models synchronized user and model audio streams to manage the conversational floor.
- Think-While-Speaking executes private reasoning in parallel with spoken delivery, supported by Adaptive Thinking and multi-token prediction, reaching 73.0 macro average on StepAudioChat in reasoning mode.
- With Think-While-Speaking it achieves dialogue and reasoning performance comparable to dedicated reasoning models while speaking in real time (Interactive mode 70.4 on StepAudioChat dialogue average).
- An integrated streaming Voice Agent handles asynchronous tool execution without disrupting dialogue flow, carrying conversational intent into tools and folding results back into subsequent dialogue.
- Headline results: 90.6 on MMSU, 98.9 Overall on the Artificial Analysis Full-Duplex Bench, and 56.0% macro task-success on τ-Voice; leads reported baselines on four of eight audio-understanding benchmarks.
- StepAudio 3 ASR Max reports error rates of 1.18 (LibriSpeech clean), 4.35 (WenetSpeech meeting), and 0.49 (AISHELL-1); remaining gaps are noted in multi-turn constraint following and retail tool-use tasks.

## 2. [[wiki/02-architecture-foundation-training|Architecture and Foundation Training]]

**In one sentence:** Conversational context — acoustic and linguistic evidence, dialogue history, current turn, reasoning progress, and tool-execution status — drives listen/speak, reason-further, and act decisions in a full-duplex mixture-of-experts system built by three-stage pretraining (32K length, 1.2T tokens) plus 128K-context midtraining for realtime interaction and perception.

## Key points
- Conversational context combines acoustic and linguistic evidence, dialogue history, current speaking turn, reasoning progress, and tool-execution status, retaining what the user says and how it is said.
- Model-side speech is itself context: it helps interpret user utterances that overlap with a response, and newly observed speech or returned tool results can change listen/speak/reason/act decisions.
- Seamless Duplex handles pauses, backchannels, and substantive interruptions; Think-While-Speaking starts spoken delivery before the full reasoning trace is complete; Adaptive Thinking selects when explicit reasoning is useful and MTP accelerates private reasoning.
- The Voice Agent resolves the request and required arguments before execution, incorporates returned evidence into the conversation, and lets the user keep speaking while a task is in progress so external work proceeds alongside dialogue.
- System is mixture-of-experts: audio frontend uses the Audio Transformer (AuT) encoder from Qwen3-Omni with an adapter mapping encoder outputs into the LLM's representation space; LLM decoder jointly conditions on acoustic info plus separate text input; generator output returns to the model audio stream.
- Pretraining runs three stages — modality alignment (acoustic-to-LM interface), multimodal mixed training (joint audio-text modeling at scale), cooldown (greater weight on high-quality data) — at fixed 32K sequence length over 1.2T tokens, with increased pure-text share to preserve base-LM capabilities.
- Midtraining extends context to 128K for longer histories, earlier requirements, and intermediate tool results, and increases audio-understanding (speech, music, environmental sound, audio-grounded reasoning) and agent-interaction data share.
- ASR specialization diverges only at supervised fine-tuning: ASR Max packs examples into 32K-token sequences, freezes the audio encoder, updates adapter plus language decoder with SpecAugment-style time-frequency masking, and fuses multi-system hypotheses with ROVER plus LLM punctuation/consistency restoration.

## 3. [[wiki/03-deep-perception-asr-max|Deep perception: StepAudio 3 ASR Max and audio understanding]]

**In one sentence:** StepAudio 3 ASR Max leads standard ASR families and all four ContextASR-Bench subsets, while StepAudio 3 Realtime leads four of eight audio-understanding benchmarks with its largest margins on MMSU and MMAR, and a quality-controlled ~100K SFT set beats a ~2M random set.

## Key points
- StepAudio 3 ASR Max is evaluated on five standard public test sets — LibriSpeech test-clean and test-other, AISHELL-1, and WenetSpeech test-net and test-meeting — with WER for English and CER for Mandarin.
- ContextASR-Bench is used in its Contextless setting (no domain labels, entity lists, or external hotword injection) to test long-tail terminology on long-form, multi-domain, entity-rich English and Mandarin speech.
- On standard ASR sets, ASR Max is best on both LibriSpeech subsets and AISHELL-1, ahead of Doubao 2.0 ASR and Seed 2.0 Lite on both WenetSpeech subsets while trailing HY3.0 ASR Preview only by a small margin.
- On ContextASR-Bench, ASR Max is best on all four subsets (English and Mandarin × Speech and Dialogue), with macro-average error rates of 5.67% English and 1.23% Mandarin vs 6.60% and 1.69% for HY3.0 ASR Preview.
- These ASR results characterize the ASR-specialized model, not the transcription behavior of the realtime model.
- StepAudio 3 Realtime leads four of eight audio-understanding benchmarks, with its largest margins on MMSU (90.6 vs 83.6) and MMAR (86.5 vs 81.7), gains of 7.0 and 4.8 points; it trails Gemini 3.1 Pro by 17.7 points on AudioMultiChallenge.
- Audio-understanding SFT data are built by a five-stage pipeline (sampling, description, capability tagging, query construction, multi-model labelling with agreement filtering) plus deterministic checks, text-only LLM quality/case-value judging, and cross-model consistency filtering for grounding reliability.
- Ablation: ~100K quality-controlled SFT examples (roughly one twentieth of ~2M random examples) improve MMSU 78.78 → 89.70, MMAR 74.70 → 84.50, WildSpeech 74.20 → 77.11, and MTalk-Bench ambient/paralinguistic/semantic macro average 88.83 → 90.84.

## 4. [[wiki/04-seamless-duplex-floor-management|The conversational role of a user: seamless duplex floor management]]

**In one sentence:** StepAudio 3 Realtime manages the conversational floor by interpreting user speech roles (pauses, backchannels, interruptions, background speech) from audio streams plus dialogue history, trained with 10,000+ hours of synthetic full-duplex data, ranking first on the Artificial Analysis full-duplex subset with 98.9 overall while conversational intelligence and reasoning are handled separately via Think-While-Speaking, StepAudioChat, and factorized multi-turn dialogue data.

## Key points
- User utterance roles are context-dependent (e.g. "right" as backchannel vs correction preface) and interpreted from both audio streams and dialogue history to guide floor-management decisions.
- Pauses vs turn endings are distinguished by combining acoustic timing with semantic completeness, deciding whether to keep listening or respond.
- During model speech, brief acknowledgments signal engagement without floor transfer while substantive requests or corrections signal interruption intent, deciding whether to continue or yield.
- Background speech is rejected using dialogue history as contextual evidence for whether speech is directed at the assistant.
- Midtraining adapts the model to time-interleaved representation with streaming ASR, VAD, and utterance-completeness prediction on over 10,000 hours of synthetic full-duplex data plus text data; post-training refines turn taking, backchannel, interruption, and background-rejection behavior.
- StepAudio 3 Realtime ranks first on the Artificial Analysis full-duplex evaluation (Full Duplex Bench v1/v1.5 subset) with 98.9 overall, ahead of Qwen Audio 3.0 Realtime Plus at 98.4, scoring 100.0 turn taking, 99.0 interruption handling, 98.9 pause handling, and 98.0 backchannel handling.
- Conversational intelligence (how to engage, how much to reason) is separated from floor control (when to respond): routine turns avoid deliberation, complex requests retain reasoning, via joint dialogue-reasoning training, Think-While-Speaking, Adaptive Thinking, and MTP acceleration.
- StepAudioChat is a closed text-based benchmark isolating text-level response quality, with a hierarchical capability taxonomy, naturalistic items (prompt, checkable criteria, valid + flawed responses), calibrated difficulty, and factorized multi-turn training data retained only after three independent quality reviews.

## 5. [[wiki/05-conversational-intelligence-stepaudiochat|Conversational Intelligence — Reasoning-Mode Evaluation]]

**In one sentence:** StepAudio 3 in reasoning mode scores 73.0 macro average on the eight StepAudioChat dimensions — ahead of Doubao 2.0 Lite (70.5) and DeepSeek-V4-Flash (71.4) but behind Kimi K3 (77.1) — while its realtime system adds Think-While-Speaking, Adaptive Thinking routing, and MTP acceleration on top of that reasoning checkpoint.

## Key points
- Reasoning-mode macro average is 73.0 for StepAudio 3, vs 70.5 (Doubao 2.0 Lite), 71.4 (DeepSeek-V4-Flash), and 77.1 (Kimi K3).
- StepAudio 3 ranks second on reasoning (73.0), memory (72.0), knowledge (73.1), conversational pragmatics (67.2), and persona & role consistency (80.9).
- Kimi K3 leads six of eight dimensions, including reasoning at 81.9, memory at 77.6, and safety & reliability at 84.8.
- Doubao 2.0 Lite leads instruction following (72.9) and persona & role consistency (82.6).
- Think-While-Speaking uses two concurrent calls as Formulation Brain (private reasoning trace) and Articulation Brain (short spoken segments), with playback-aware scheduling, Speak-First by default, and Think-First as the prefix-waiting option.
- Adaptive Thinking routes turns to immediate (empty think block) vs deliberate response, with think rates from 51.5% to 82.0% across the eight categories on StepAudioChat (46 benchmark members).
- Full thinking gains most over forced no-think in Reasoning (+11.37), Persona and Role Consistency (+8.37), and Knowledge (+5.94); vs Direct SFT, Adaptive Thinking improves Dialogue Pragmatics 63.59 → 65.87 but reduces Reasoning 71.89 → 66.80, with Reasoning think rate only 59.5% despite benefiting most.

## 6. [[wiki/06-think-while-speaking-adaptive-reasoning|Think While Speaking, Adaptive Reasoning and MTP Acceleration]]

**In one sentence:** MTP3/MTP5 with Medusa-style typical acceptance accelerate private reasoning (1.49×–2.05× wall-clock) while improving Reasoning and Memory but lowering Instruction Following, and a 3:1:1:1 weighted merge of four specialized teachers balances audio, text, and dialogue capabilities.

## Key points
- All tested MTP configurations improve Reasoning (up to 74.30 vs 70.76 baseline) and Memory (up to 71.36 vs 67.99) over baseline, while Instruction Following declines (61.21–62.73 vs 64.15 baseline).
- Accepted draft tokens per target-model step are 1.231 (MTP3 strict), 1.801 (MTP3 Medusa-typical), 1.353 (MTP5 strict), and 2.153 (MTP5 Medusa-typical), with wall-clock speedups of 1.76×, 2.05×, 1.49×, and 1.72× respectively (baseline 0 and 1.00×).
- MTP3 uses three prediction heads drafting up to three future tokens per target-model step; Medusa-style typical acceptance uses an entropy-adaptive confidence threshold to accept plausible drafts strict verification would reject, plus a 1.05 repetition penalty on private reasoning only, with strict verification retained for spoken responses.
- Marginal acceptance (Table 7) under typical acceptance reaches 82.4%/58.2%/39.4% for MTP3 heads 1–3 and 80.6%/55.7%/37.6%/24.9%/16.4% for MTP5 heads 1–5; strict rates for MTP5 heads 4–5 fall to 10.7% and 5.7%, showing diminishing gains from added depth.
- Acceptance alone does not determine net efficiency since reasoning length and decoding costs also matter, so reported wall-clock ratios "should not be interpreted as a controlled comparison of draft depth," and keeping strict verification for spoken output "does not eliminate errors arising from incomplete private reasoning."
- Four compatible teachers trained from a common base with different data mixtures are merged as θmerge = Σ αi θi (αi ≥ 0, Σαi = 1) with normalized 3:1:1:1 weighting and held-out coefficient selection, adding neither model components nor inference-time routing.
- The merge reaches macro averages of 81.3 on audio understanding (tying best teacher, leading MMAU and WildSpeech), 76.5 on general text (highest, with best HMMT 2026 Feb and GPQA Diamond), and 73.0 on dialogue (above Teachers 2–4, below Teacher 1 at 74.2) — a balanced trade-off, not uniform dominance.
- The full-duplex voice agent routes stable-knowledge requests to direct responses, up-to-date public information to lightweight tools (weather, web search), and private-context/multi-step/beyond-turn work to asynchronous backend execution that continues alongside conversation.

## 7. [[wiki/07-voice-agent-tool-execution|Voice Agent Tool Execution and Agentic Task-Completion Results]]

**In one sentence:** StepAudio 3 Realtime achieves a 56.0% macro task-success rate on τ-Voice — close to Grok's 56.5% and above Qwen (54.6%) and GPT (45.7%) — with the best telecom score (70.2%) and near-best airline score (60.0%) but weaker retail (37.7%), supported by training that grounds tool use in clarification, confirmation, and evidence from asynchronous backend execution.

## Key points
- Macro task-success rate on τ-Voice is 56.0% for StepAudio 3 Realtime, versus 56.5% for Grok Voice Think Fast 2.0 High, 54.6% for Qwen Audio 3.0 Realtime Plus, and 45.7% for GPT-Realtime-2.1 High.
- Telecom is StepAudio 3 Realtime's strongest domain at 70.2%, exceeding Grok by 6.5 percentage points and the highest among evaluated models.
- Airline score is 60.0%, within 2.0 percentage points of the best reported score of 62.0% (GPT-Realtime-2.1 High).
- Retail score is 37.7%, trailing Grok's 49.7%, leaving room for further improvement.
- Before committing to an external action, the model is trained to gather missing information through clarification or context retrieval and to obtain required confirmation.
- Backend tasks execute asynchronously while conversation continues: the model associates task-related input with the ongoing task, distinguishes it from unrelated dialogue, and incorporates results into conversational context.
- Training combines targeted voice-agent dialogues (routing, clarification, private-context retrieval, confirmation, execution-time updates, progress queries, result reporting) with filtered multi-step agent trajectories, plus negative examples against unnecessary tool invocation and unsupported claims.

## 8. [[wiki/08-capability-evaluation-benchmarks|Capability Evaluation Benchmarks (Table 10)]]

**In one sentence:** Table 10 compares StepAudio 3 Realtime against domain-specific baselines across audio understanding, dialogue and reasoning, general text, full duplex, and agentic tasks, showing strong audio understanding and floor management with variation across reasoning and tool-use tasks.

## Key points

- Table 10 uses a 0–100 scale (higher is better), with protocols and aggregation specified in Section 8.3, and bold/underline marking best/second-best per row.
- For Dialogue and Reasoning evaluation, StepAudio 3 Realtime uses realtime mode while the other models use reasoning mode.
- On audio understanding, StepAudio 3 Realtime leads Step-Caption (78.2) and MTalk-Bench (91.7), leads MMSU (90.6) and MMAR (86.5), and trails Gemini 3.1 Pro on Big Bench Audio (98.1 vs 99.6), AudioMultiChallenge (49.3 vs 67.0), MMAU (79.0 vs 80.5), and WildSpeech (77.1 vs 77.7).
- On StepAudioChat dialogue/reasoning, StepAudio 3 Realtime (Interactive) reaches 70.4 macro average, comparable to Doubao 2.0 Lite at 70.5 and DeepSeek-V4-Flash at 71.4, behind Kimi K3 at 77.1, with its best subscore in Persona and Role Consistency (78.3).
- On general text, StepAudio 3 Realtime leads HMMT 2026 Feb with 86.8 (vs 73.9 Doubao, 85.9 Gemini 3 Flash) but trails Gemini 3 Flash on GPQA Diamond (83.0 vs 90.3) and MultiChallenge (59.7 vs 68.1).
- On full duplex, StepAudio 3 Realtime ranks first on AA Full-Duplex Bench with 98.9 overall, including 100.0 on turn taking and 99.0 on interruption handling, while remaining strong on pauses and backchannels.
- On agentic τ-Voice, StepAudio 3 Realtime reaches 56.0, close to the best reported 56.5 (Grok Voice Think Fast 2.0 High), ahead of Qwen Audio 3.0 Realtime Plus (54.6) and GPT-Realtime-2.1 High (45.7).

## 9. [[wiki/09-references-audio-language-models|References: Audio Language Models and Streaming Speech Systems]]

**In one sentence:** This chunk lists references [4]–[39] of the StepAudio 3 Realtime Technical Report, covering audio-language modeling foundations, prior Step-Audio/omni systems, full-duplex dialogue, ASR data/augmentation, and agent/inference benchmarks.

## Key points
- Reference [4] cites Borsos et al., AudioLM (2023), "a language modeling approach to audio generation," in IEEE/ACM Transactions on Audio, Speech, and Language Processing, 31:2523–2533.
- References [5]–[6] cite generic-hearing and paralinguistic conversation work: SALMONN (ICLR 2024, pp. 16607–16629) and a NeurIPS 2024 (37:131072–131103) paralinguistics-aware speech LLM paper.
- References [7]–[8] cite the direct lineage and omni peers: Step-Audio 2 technical report (arXiv:2507.16632, 2025) and Qwen3-Omni technical report (arXiv:2509.17765, 2025).
- References [9]–[12] cite real-time/full-duplex dialogue systems: Freeze-Omni (arXiv:2411.00774, 2024), Moshi (arXiv:2410.00037, 2024), plus 2026 full-duplex papers on chronological thinking (SIGDIAL pp. 473–485) and DuplexSLA (arXiv:2605.20755, 2026).
- References [13]–[17] cite the Step-Audio research line: Step-Audio unified understanding/generation (arXiv:2502.11946, 2025), Step-Audio-R1 (arXiv:2511.15848, 2025), Step-Audio-R1.5 (arXiv:2604.25719, 2026), StepAudio 2.5 (arXiv:2605.23463, 2026), and mind-paced speaking dual-brain reasoning (arXiv:2510.09592, 2025).
- References [18]–[26] cite ASR methods, data, and robustness work: SpecAugment (arXiv:1904.08779, 2019), ROVER (1997 IEEE ASRU Workshop, pp. 347–354), code-switching ASR (IEEE TASLP 34:1853–1865, 2026), LibriSpeech (ICASSP 2015, pp. 5206–5210), AISHELL-1 (O-COCOSDA 2017, pp. 1–5), WenetSpeech 10000+ hours (ICASSP 2022, pp. 6182–6186), ContextASR-Bench (arXiv:2507.05727, 2025), omni-modal post-training (arXiv:2605.12034, 2026), and Bayling-Duplex (arXiv:2606.14528, 2026).
- References [27]–[31] cite dialogue/inference acceleration work: Multi-bench emotional-intelligence benchmark (arXiv:2511.00850, 2025), speculative sampling (arXiv:2302.01318, 2023), speculative decoding (ICML, pp. 19274–19286, 2023), Medusa multi-head decoding (arXiv:2401.10774, 2024), and multi-token prediction (arXiv:2404.19737, 2024).
- References [32]–[39] cite tool use, agent, and audio-reasoning benchmarks: Toolformer (NeurIPS 36:68539–68551, 2023), Gorilla (NeurIPS 37:126544–126565, 2024), ReAct (arXiv:2210.03629, 2022), Artificial Analysis speech-to-speech methodology (2026) and Big Bench Audio (Hugging Face Blog, 2024), MMSU (ICLR 2026, pp. 31374–31410), MMAU (ICLR 2025, pp. 84929–84964), and MMAR (NeurIPS 38, 2026).

## 10. [[wiki/10-references-benchmarks-evaluation|References: Benchmarks and Evaluation (Refs 40–56)]]

**In one sentence:** This chunk lists references [40]–[56] covering speech/dialogue benchmarks, general LLM evaluation, and industry speech-model documentation cited by the report.

## Key points
- [40] cites Linhao Zhang et al., "Wildspeech-bench: Benchmarking end-to-end speechllms in the wild," arXiv preprint arXiv:2506.21875, 2025.
- [41] cites Gosai et al., "Audio multichallenge: A multi-turn evaluation of spoken dialogue systems on natural human interaction," ACL 2026, pages 35740–35770.
- [42] cites StepFun, "Step-caption: Benchmark and evaluation protocol, 2026," with the Step-Audio-R1 step_caption GitHub URL.
- [43] cites Du et al., "Mtalk-bench: Evaluating speech-to-speech models in multi-turn dialogues via arena-style and rubrics protocols," arXiv preprint arXiv:2508.18240, 2025.
- [44] cites HMMT, "Archive of february 2026, 2026," URL https://www.hmmt.co/www/archive/292.
- [45]–[46] cite general LLM benchmarks: GPQA (arXiv:2311.12022, 2023) and MultiChallenge (ACL 2025 Findings, pages 18632–18702).
- [47]–[56] cite industry model cards and docs: Seed2.0, Tencent Hy ASR 3.0, Gemini 3 Flash / 3.1 Pro, DeepSeek-V4-Flash, Kimi K3, GPT-Realtime-2 / 2.1, Qwen speech-to-speech models, and Grok Voice Think Fast 2.0.

## The argument in five moves

1. Realtime spoken interaction demands a continuous listen-converse-think-act loop where perception, floor management, reasoning, and tool use proceed concurrently rather than in strict sequence.
2. Deep Perception (with the ASR Max specialization) and quality-controlled audio-understanding data establish the acoustic and linguistic evidence base, leading standard ASR families and ContextASR-Bench while topping MMSU/MMAR among audio-understanding benchmarks.
3. Seamless Duplex converts that evidence into conversational control — distinguishing pauses from turn endings, backchannels from interruptions, and background speech — trained on 10,000+ hours of synthetic full-duplex data to rank first (98.9 overall) on the Artificial Analysis full-duplex bench.
4. Think-While-Speaking with Adaptive Thinking and MTP acceleration resolves the deliberation-vs-latency tension by speaking before reasoning completes, routing only selected turns to explicit reasoning and speeding private thought 1.49×–2.05×, keeping Interactive-mode dialogue (70.4) near dedicated reasoning models (73.0).
5. A streaming Voice Agent extends the loop to action, clarifying and confirming before external calls and executing asynchronously alongside dialogue, yielding competitive τ-Voice task completion (56.0% macro, best telecom 70.2%) with retail and multi-turn constraint following left as stated areas for improvement.
