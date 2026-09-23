> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Deep perception: StepAudio 3 ASR Max and audio understanding
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
---
## ASR evaluation setup
StepAudio 3 ASR Max is evaluated on "five standard public test sets: LibriSpeech test-clean and test-other [21], AISHELL-1 [22], and WenetSpeech test-net and test-meeting [23]." Quoting the chunk: "English results use word error rate (WER), while Mandarin results use character error rate (CER)."
To assess long-tail terminology augmentation, the chunk additionally uses "the publicly released ContextASR-Bench [24], which provides long-form, multi-domain, entity-rich speech in English and Mandarin," in "its Contextless setting without domain labels, entity lists, or external hotword injection; English subsets are evaluated with WER and Mandarin subsets with CER."
## ASR results
"Table 1 compares ASR performance across benchmark subsets." Per-subset numeric values of Table 1 are not present in this chunk body; the chunk states only these outcomes:
- "StepAudio 3 ASR Max leads on all three standard benchmark families: it is best on both LibriSpeech subsets and AISHELL-1, and it remains ahead of Doubao 2.0 ASR and Seed 2.0 Lite on both WenetSpeech subsets while trailing HY3.0 ASR Preview only by a small margin."
- "On ContextASR-Bench, StepAudio 3 ASR Max is the best-performing model on all four subsets, covering both English and Mandarin and both Speech and Dialogue settings."
- "Its macro-average error rate is 5.67% on the English subsets and 1.23% on the Mandarin subsets, compared with 6.60% and 1.69% for HY3.0 ASR Preview."
- "This consistent lead indicates strong overall transcription accuracy on the benchmark's long-form, multi-domain, entity-rich speech without external context injection."
- "Note that these results characterize the ASR-specialized model, not the transcription behavior of the realtime model."
## Audio understanding: data construction
Section 4.2, "Audio Understanding": "A hierarchical taxonomy covers lexical content, paralinguistics, acoustic events, speaker and temporal structure, music, and audio-grounded reasoning. Sampling controls balance duration and language coverage while removing duplicates and unsuitable recordings."
"Each recording is first described and mapped to the capabilities supported by its content." The five-stage pipeline (Figure 4) is: (1) Sampling — "duration and language quotas, dedup"; (2) Description — "a caption of what the clip contains"; (3) Capability tagging — "which aspects the clip supports"; (4) Query construction — "one or more questions tailored to each clip"; (5) Labelling — "the answers, grounded in the audio." "Multiple models then independently label each audio–question pair, and their outputs are consolidated through agreement and quality checks."
## Audio understanding: selection and quality control
"Deterministic checks first remove empty, truncated, malformed, or severely repetitive outputs. Text-only LLM judges then assess query and response quality and assign a case-value score." Case value "jointly considers the query, the response, the amount of useful information available in the audio as represented by its annotations, and the training value of the question."
"These judges do not directly evaluate audio grounding. Instead, grounding reliability is estimated from the consistency of responses independently produced by multiple models for the same audio–question pair." Only "candidates with high quality, high case value, and strong cross-model consistency are retained as SFT candidates; broadly useful examples may enter midtraining, while disagreements and correctable cases are routed to relabeling or further review."
## Audio understanding: evaluation (Table 2)
"We evaluate the post-trained conversational model on eight audio-understanding benchmarks covering audio-grounded reasoning, fine-grained perception, nonverbal acoustic cues, and multi-turn understanding. Results are reported in Table 2." Table 2 (0–100 scale, higher better; bold = best, underline = second-best):
| Benchmark | StepAudio 3 Realtime | Doubao 2.0 Lite | Gemini 3 Flash | Gemini 3.1 Pro |
|---|---|---|---|---|
| Big Bench Audio | 98.1 | 98.8 | 99.4 | 99.6 |
| AudioMultiChallenge | 49.3 | 48.5 | 56.6 | 67.0 |
| MMSU | 90.6 | 80.0 | 77.0 | 83.6 |
| MMAU | 79.0 | 77.5 | 77.6 | 80.5 |
| WildSpeech | 77.1 | 73.9 | 74.4 | 77.7 |
| MMAR | 86.5 | 75.9 | 75.4 | 81.7 |
| Step-Caption | 78.2 | 76.8 | 67.8 | 74.8 |
| MTalk-Bench | 91.7 | 89.9 | 88.5 | 89.1 |
| Macro Average | 81.3 | 77.7 | 77.1 | 81.8 |
Chunk summary: "StepAudio 3 Realtime leads the reported baselines on four of the eight benchmarks, with its largest margins on MMSU (90.6 versus 83.6) and MMAR (86.5 versus 81.7), gains of 7.0 and 4.8 points." "It also leads on Step-Caption and MTalk-Bench, and is close to Gemini 3.1 Pro on MMAU and WildSpeech." "In contrast, it trails Gemini 3.1 Pro by 17.7 points on AudioMultiChallenge, while Big Bench Audio is nearly saturated for all systems." Overall: "broad strength in spoken-language understanding, audio-grounded reasoning, and nonverbal acoustic perception, with maintaining and revising constraints over natural multi-turn audio remaining a clear area for improvement."
## Less is more: SFT quality ablation
"We conduct a separate ablation in which the SFT data are the only changed factor, comparing roughly two million randomly sampled examples with about 100K high-quality examples retained after quality control." Results: "The quality-controlled set improves MMSU from 78.78 to 89.70 and MMAR from 74.70 to 84.50. WildSpeech rises from 74.20 to 77.11, while the macro average across the ambient, paralinguistic, and semantic subsets of MTalk-Bench increases from 88.83 to 90.84." Conclusion quoted: "Despite using roughly one twentieth as many examples, the quality-controlled data yield consistent gains, highlighting the importance of data quality over raw SFT volume."
## Seamless duplex lead-in (in this chunk)
Section 5, "Seamless Duplex: Conversational Floor Management": "A central challenge in full-duplex dialogue is determining when to take, retain, or yield the conversational floor," distinguishing "pauses within an unfinished utterance from turn completion, and brief acknowledgments from attempts to interrupt." "StepAudio 3 Realtime integrates incoming user speech, ongoing model speech, and dialogue history for context-aware conversational-floor management" via a "dual-stream architecture" with "temporal interleaving of audio blocks with interaction-state tokens" (Figure 5). Audio is organized "into 320 ms blocks, each followed by a state or text token." Full detail continues in the next wiki page.
**Covers:** Sections 4.1–5 intro (ASR benchmarks incl. Table 1 reference, audio-understanding data/evaluation incl. Table 2, duplex floor-management lead-in)
