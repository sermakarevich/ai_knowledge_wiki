# DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events

**Paper:** [DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events (Guo et al., 2026)](https://arxiv.org/abs/2609.12872)

## Human Readable TL;DR

Think of most AI conversation datasets as rehearsed stage plays where actors politely wait their turn in a silent room. Real life sounds more like a late-night kitchen chat with interruptions, "uh-huh" backchannels, trailing-off sentences, shifting moods, and a pen clattering to the floor. DuplexDrama is a factory for manufacturing exactly that kind of messy realism at scale, using AI voices and script-placed sound effects so researchers can train voice assistants that handle overlapping, emotional, noisy talk.

## TL;DR

DuplexDrama is presented as the first synthesized spoken dialogue dataset that jointly covers persona/scenario settings, three full-duplex behaviors (interruption, backchannel, incomplete), persona-aligned expressive speech, and script-aware sound events. It is built via a four-stage pipeline (persona–scenario generation with DeepSeek-v4.1-pro, tagged script generation with Gemini-3.1-pro-preview, IndexTTS2 expressive synthesis with forced-alignment-based dual-track assembly, and script-aware background/event mixing) plus a quality validator, yielding a released corpus of about 6,400 dialogues / 800 hours with 64 voice timbres and roughly 362k turns. Validation combines a dual-LLM script check on asset rationality, tag rationality, and script-scenario consistency with four objective audio metrics (WER via Qwen3-ASR, UTMOSv2, NISQA, and SpeechBrain speaker-consistency with a 0.9 discard rule), and a comparison against five prior corpora claims DuplexDrama is the only one covering all four annotation dimensions.

---

## Problem & Motivation

Spoken dialogue models that aim at full-duplex interaction must cope with overlapping speech, interruptions, backchannels, expressive delivery, and environmental sound, yet existing corpora cover only fragments of this space. Large natural conversation collections such as Fisher, CANDOR, Open-Yap-1K, and DuplexConv provide real overlap but lack scripted personas, scenarios, and sound-event annotations, while the synthesized SpeechDialogueFactory provides persona and scenario labels but no full-duplex behavior. DuplexDrama is motivated by this gap: a large-scale, controllable, richly annotated synthetic corpus where who is speaking, where they are, how they interrupt or trail off, how they feel, and what is happening in the background are all jointly scripted and rendered into multi-track audio for training and evaluating full-duplex spoken dialogue systems.

## Main Original Ideas

1. **Four-dimension joint coverage:** the central dataset claim is a single synthesized corpus that simultaneously provides complete persona and scenario settings (e.g., Lisa the tired nurse and Tom the supportive teacher at home at 11:30 PM), three full-duplex behaviors, persona-aligned emotion labels, and script-aware sound events, with script-aware event tags stated as unique to this work.

2. **Seed-pool persona–scenario generation:** two seed pools (24 macro / 134 sub-type personas by social function; 46 macro / 404 sub-type topics by narrative scenario) are sampled and expanded by DeepSeek-v4.1-pro into coupled persona tuples (name, gender, age, occupation, personality, role) and scenario specifications (scene, tone, narrative type, scene medium, a three-event chain, and a segmented emotional arc) under consistency constraints.

3. **Orthogonally tagged spoken-style scripts:** Gemini-3.1-pro-preview writes dialogue annotated with three tag families — full-duplex tags (`<user interrupt>`, `<user backchannel>`, `<user incomplete>`), seven IndexTTS2-aligned emotions (`[Neutral]`, `[Happy]`, `[Angry]`, `[Sad]`, `[Whispering]`, `[Hesitant]`, `[Surprised]`), and environmental-noise / sound-event tags referencing a curated audio bank.

4. **Acoustic realization of full-duplex behavior:** per-utterance IndexTTS2 synthesis with disentangled timbre–emotion control (64-speaker pool across 13 core personas and 5 age buckets, mostly MOSS-Audio prompts) is force-aligned to word timestamps and assembled into two parallel speaker tracks, where incomplete tags become literal ". . . " in-sentence pauses, interrupts become fade-out plus overlap, and backchannels become time-aligned overlays on the continuing track.

5. **Script-aware background and event mixing:** two time-aligned background channels (one per speech channel) combine 7 scene categories / 600 long-duration noise clips persisting across turns with 52 categories / 2,203 short event clips inserted at forced-alignment trigger-word onsets (e.g., `object hit` at 2.34 s) at configurable SNR, with only the input-side channel required for full-duplex training.

6. **Dual-LLM plus objective quality validator:** scripts are judged by DeepSeek-v4.1-pro and Gemini-3.1-pro-preview on asset rationality, tag rationality, and script-scenario consistency (the latter two cross-checked), while audio is scored on WER, UTMOSv2/NISQA MOS, and SpeechBrain speaker-consistency cosine similarity with dialogues below 0.9 discarded, retaining only the high-quality subset.

## Key Findings

The released corpus overview reports 6,400 dialogues, 800 total audio hours, 460 s average dialogue length, about 362k turns at 8 s average turn length, and 64 voice timbres, with behavior-tag shares of 8,996 interrupts (2.4%), 2,455 backchannels (0.6%), and 2,271 incompletes (0.7%), plus seven-category environment and top-10 event distributions. Per-dialogue audio metrics on clean TTS audio give WER 1.8% and speaker consistency 97.3%, with UTMOSv2 2.57 clean / 2.52 mixed and NISQA-MOS 3.65 clean / 3.18 mixed, showing background mixing costs UTMOSv2 only 0.05 but NISQA 0.47 because UTMOSv2 targets synthetic-speech naturalness while NISQA also penalizes additive noise, and the lower-than-typical UTMOSv2 is attributed to diverse persona stylings and emotion injection. Script-rationality scores after filtering are reported via Table 4, and the six-corpus comparison (Fisher 2,000 hr natural, CANDOR 850 hr natural, Open-Yap-1K 1,000 hr natural, DuplexConv 2,000 hr natural, SDF 146 hr synthetic, Ours 800 hr synthetic) concludes DuplexDrama is the only corpus with persona+scenario, full-duplex, and sound-event coverage jointly present.

## Suggestions & Future Directions

The authors state they will release approximately 800 hours of data to facilitate full-duplex spoken dialogue modeling and name three directions for future work: more realistic duplex label distributions, paralinguistic phenomena in TTS output, and more flexible sound-event label matching. The work also notes its construction constraints — TTS synthesis plus publicly available audio with no human-subject data, non-commercial academic use of processed audio assets, and LLM use limited to English polishing — which frame natural extensions around closing the synthetic-to-real gap and broadening behavior, paralinguistic, and acoustic coverage.

## Authors & Institutions

Qingxiang Guo, Wenke Fan, Shuofeng Zhao, Dawei Yang, Zhiyang Zhou, Yingxin Shang, Hongwei Cai, Zhou Wang, Weixu Wang, Lin Yang, Shuran Zhou, and Yang Song, all of Zuoyebang Education Technology, Beijing, China.
