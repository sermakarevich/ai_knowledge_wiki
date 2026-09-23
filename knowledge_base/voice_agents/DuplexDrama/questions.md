---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events

### Q1. What is DuplexDrama's core claim and what four dimensions does it cover?

> [!tip]- Answer
> DuplexDrama is presented as the first synthesized spoken dialogue dataset that simultaneously covers (i) complete persona and scenario settings, (ii) three full-duplex behaviors (interruption, backchannel, incomplete), (iii) expressive speech with persona-aligned emotion labels, and (iv) script-aware sound events. It is built via a 4-stage pipeline with quality validation on both scripts and synthesized audio, and the abstract reports more than 2,000 dialogues produced. See [[wiki/01-overview-and-contributions|Overview and Contributions]].

### Q2. What does the Lisa-and-Tom example illustrate about personas, scripts, and audio tracks?

> [!tip]- Answer
> The example sets Role 1 as Lisa (29, nurse, caring but tired) and Role 2 as Tom (31, teacher, supportive) in a home-living, face-to-face, bedroom-vs-living-room scene at 11:30 PM. Its script excerpt shows inline tags such as `<env: home living>`, `<user interrupt>`, `<evt: object hit>`, and `<emo: Surprised>`, and each dialogue is represented as multi-track audio with 4 files: Role 1 speech, Role 2 speech, Role 1 background, and Role 2 background. See [[wiki/01-overview-and-contributions|Overview and Contributions]].

### Q3. How do pipeline Stages 1 and 2 generate setups and tagged scripts?

> [!tip]- Answer
> Stage 1 uses DeepSeek-v4.1-pro to draw seeds from a persona pool (24 macro categories / 134 sub-types by social function) and a topic pool (46 macro categories / 404 sub-types by narrative scenario), then expands them into two persona tuples (name, gender, age, occupation, personality, role) plus a scenario specification (scene, tone, narrative type, scene medium, a three-event chain, and a segmented emotional arc) under consistency constraints. Stage 2 uses Gemini-3.1-pro-preview to write spoken-style dialogue annotated with three orthogonal tag families: full-duplex behavior tags (`<user interrupt>`, `<user backchannel>`, `<user incomplete>`), seven IndexTTS2-aligned emotion labels, and environmental-noise / sound-event tags referencing the audio bank. See [[wiki/02-pipeline-persona-script-synthesis|Pipeline, Persona/Script Generation, and Expressive Synthesis]].

### Q4. How does Stage 3 synthesize expressive speech and realize full-duplex acoustics?

> [!tip]- Answer
> Stage 3 synthesizes with IndexTTS2 for disentangled timbre–emotion control, drawing on a 64-speaker pool spanning 13 core personas and 5 age buckets (mostly MOSS-Audio-generated prompt audios plus some natural snippets), with each utterance force-aligned for word-level timestamps and assembled in turn order into two parallel speaker tracks with silence during the other's turns. The three duplex tags become acoustic effects: `<user incomplete>` renders as a literal ". . . " in-sentence pause, `<user interrupt>` fades the utterance out while the other turn is brought in to produce overlap, and `<user backchannel>` is time-aligned and overlaid while the other track keeps speaking. See [[wiki/02-pipeline-persona-script-synthesis|Pipeline, Persona/Script Generation, and Expressive Synthesis]].

### Q5. How are script-placed sound events turned into mixed audio?

> [!tip]- Answer
> Each event tag from the Stage 2 script is matched to an asset from the event bank (52 categories / 2,203 short clips; e.g. doorbell, page turn, footstep, object hit, cup glass) and aligned to the trigger word's onset by forced alignment of the synthesized speech, then mixed in at a configurable SNR. The worked example is Turn 4 (HM, A) ". . . the pen slipped out and hit the floor" with event class `object hit` at FA onset 2.34 s mixed as speech + event. Environmental noise comes from a separate bank of 7 scene categories / 600 long clips that persist for several turns, with two background channels per dialogue (one per speech channel) of which only the input (HM)-side channel is required for full-duplex training. See [[wiki/03-audio-assembly-background-validation|Audio Assembly, Background/Event Mixing, and Quality Validation]].

### Q6. What does the §2.5 quality validator check, and what corpus scale does Table 1 report?

> [!tip]- Answer
> The validator combines a dual-LLM script check (DeepSeek-v4.1-pro and Gemini-3.1-pro-preview over asset rationality, tag rationality, and script-scenario consistency) with four objective audio metrics — WER via Qwen3-ASR, quality via UTMOSv2 and NISQA (MOS), and speaker consistency via SpeechBrain cosine similarity — discarding dialogues with SpkCons below 0.9, where WER and SpkCons run on clean TTS audio without background. The Table 1 fragment reports a released corpus of 6,400 dialogues, 800 total audio hours, 460 s average dialogue length, ~362k turns, 8 s average turns, and 64 voice timbres, with behavior-tag shares of `<user interrupt>` 8,996 (2.4%), `<user backchannel>` 2,455 (0.6%), and `<user incomplete>` 2,271 (0.7%). See [[wiki/03-audio-assembly-background-validation|Audio Assembly, Background/Event Mixing, and Quality Validation]].

### Q7. What do the Table 3 clean-vs-mixed scores show about background mixing?

> [!tip]- Answer
> Table 3 reports per-dialogue WER 1.8% and SpkCons 97.3% on clean audio, plus UTMOSv2 2.57 clean / 2.52 mixed and NISQA-MOS 3.65 clean / 3.18 mixed, with UTMOSv2 and NISQA deliberately predicted on both since speech quality should not be affected by additive background noise. Mixing costs UTMOSv2 only 0.05 but NISQA-MOS 0.47, because UTMOSv2 targets synthetic-speech naturalness while NISQA also penalises additive noise, so the speech itself is left intact; the lower-than-typical UTMOSv2 scores are attributed primarily to diverse persona stylings and emotion injection. See [[wiki/04-dataset-statistics-audio-quality|Dataset Statistics and Audio Quality]].

### Q8. How does Table 5 position DuplexDrama against prior corpora?

> [!tip]- Answer
> Table 5 compares six corpora on duration, type, persona+scenario, full-duplex status, and sound events: Fisher (2,000 hr, natural), CANDOR (850 hr, natural), and Open-Yap-1K (1,000 hr, natural) lack scripted scenarios, persona attributes, and sound-event annotations, DuplexConv (2,000 hr, natural) has overlap but the same gaps, and SpeechDialogueFactory (146 hr, synthesized) has persona/scenario annotations but no full-duplex coverage. DuplexDrama (800 hr, synthesized) is the only corpus marked present on all three annotation axes, with its script-aware sound-event tags claimed as unique to the work. See [[wiki/04-dataset-statistics-audio-quality|Dataset Statistics and Audio Quality]].

### Q9. What does the paper conclude, promise, and disclose?

> [!tip]- Answer
> The conclusion restates DuplexDrama as the first TTS-synthesized spoken dialogue dataset jointly covering persona/scenario annotations, full-duplex behaviors, expressive speech, and sound events, built through the four-stage pipeline with four objective audio metrics plus dual-LLM script-rationality cross-checking, and promises approximately 800 hours of released data. Future work lists more realistic duplex label distributions, paralinguistic phenomena in TTS output, and more flexible sound-event label matching. The ethics disclosure states the corpus uses only TTS synthesis and publicly available audio with no human-subject data, so no ethical approval was required, and LLMs were used solely to polish English. See [[wiki/05-script-validation-comparison-conclusion|Script Rationality Validation via Dual LLM Judges, Comparison, and Conclusion]].

### Q10. Should a team adopt DuplexDrama as training data for a full-duplex spoken dialogue model?

> [!tip]- Answer
> Yes, if the team's bottleneck is full-duplex behavior under realistic acoustics, because DuplexDrama is the only corpus in its comparison jointly providing scenario grounding, interrupt/backchannel/incomplete overlap, expressive multi-persona speech, and FA-aligned sound events at ~800 hours with documented script and audio validation. The caveat is that all speech is synthesized (with admittedly atypical UTMOSv2 scores and rare duplex tags under 3% of turns), so the team should fine-tune or validate on natural conversational audio and treat the dual-LLM script scores as a proxy rather than human judgment. See [[wiki/05-script-validation-comparison-conclusion|Script Rationality Validation via Dual LLM Judges, Comparison, and Conclusion]].
