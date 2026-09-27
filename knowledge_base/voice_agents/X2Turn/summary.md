# [2608.10878] X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction

**Article:** [2608.10878](https://doi.org/10.48550/arxiv.2608.10878) — arXiv, 8 Sep 2026 (v3)

## Human Readable TL;DR

Spoken voice assistants constantly face a tricky judgment call: when someone makes a sound mid-conversation, is it a real interruption that deserves a response, just a background "uh-huh" that should be ignored, or the natural end of their sentence? Older systems tend to answer this question in clumsy, chunky steps, like only checking the traffic light every ten seconds, and they often need a separate speech-recognition helper running alongside, which adds delay and complexity. X2-Turn instead works like a skilled simultaneous interpreter who both transcribes and reads the room moment by moment, attaching a tiny "what is happening in the conversation right now" label to every instant of audio while transcribing it. Because both jobs share the same live understanding of the sound, the system can react faster and more accurately without an extra helper model. Tested in two languages, it strikes a practical balance between getting the call right and making it quickly.

## TL;DR

X2-Turn adds a frame-synchronous turn-state head in parallel with the ASR head on shared streaming representations from pretrained Voxtral Realtime, jointly predicting ASR tokens and fine-grained turn states at the frame level via delayed-stream modeling. It targets real-time discrimination of interruptions, ignorable backchannels, and utterance completion, addressing the mismatch of utterance- or fixed-chunk-level predictors and the dependence on auxiliary ASR models. Experiments on bilingual EasyTurn and Full-Duplex-Bench are reported to show an effective trade-off between turn-state accuracy and decision latency.

---

## Problem & Motivation

Accurate and responsive turn-taking is essential for spoken dialogue systems, which must decide in real time whether the user is interrupting, producing a backchannel that should be ignored, or finishing an utterance. Prior modular approaches typically optimize turn-state prediction at the utterance or fixed-chunk level, which mismatches the continuous nature of turn-state estimation and limits responsiveness, and they often depend on an auxiliary ASR model, increasing overall system complexity. The motivation is therefore a unified streaming approach that produces a continuous, low-latency turn-state estimate directly alongside recognition, without a separate helper model.

## Main Original Ideas

1. **Frame-synchronous dual-head modeling:** X2-Turn introduces a turn-state head that operates in parallel with the ASR head on shared streaming representations, so transcription and turn-state prediction proceed together rather than in separate stages.
2. **Frame-level joint prediction via delayed-stream modeling:** built on the pretrained Voxtral Realtime model, the method jointly predicts ASR tokens and fine-grained turn states at the frame level, giving a continuous turn-state estimate suited to real-time dialogue.
3. **Unified bilingual turn-taking evaluation:** the work evaluates on bilingual EasyTurn and Full-Duplex-Bench, framing turn-taking quality as an explicit trade-off between turn-state accuracy and decision latency.

## Key Findings

Experiments on bilingual EasyTurn and Full-Duplex-Bench demonstrate that the proposed method achieves an effective trade-off between turn-state accuracy and decision latency. No quantitative results, ablations, figures, or latency numbers are present in the available wiki source beyond this abstract-level claim, so effect sizes and per-benchmark breakdowns cannot be stated here. The version history (v1 on 11 Aug 2026, v2 on 19 Aug 2026, v3 on 8 Sep 2026) indicates active revision, with the latest version at 923 KB.

## Suggestions & Future Directions

A natural next step is to quantify the accuracy–latency trade-off explicitly with per-benchmark numbers, latency distributions, and comparisons against utterance-level, fixed-chunk-level, and auxiliary-ASR baselines. Further work could ablate the contribution of the shared streaming representation versus the delayed-stream modeling, and probe robustness on noisier, multi-speaker, and multilingual settings beyond the two reported benchmarks. Since only the abstract-level claim is available in the wiki source, consulting the full paper would be needed to ground concrete error analysis and deployment guidance.

## Authors & Institutions

Kaiqi Fu, Rime Wen, Altman Lin, Shawn Qin, Roy Gan, Hao Wang, and Qian Wang (7 authors). Institutions are not listed in the available wiki source. Submitted by Kaiqi Fu; subjects: Computation and Language (cs.CL) and Audio and Speech Processing (eess.AS); cite as arXiv:2608.10878 [cs.CL] (v3: arXiv:2608.10878v3 [cs.CL]).
