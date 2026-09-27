> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Background and scalable data pipeline

**In one sentence:** JAL-Turn is motivated by the failure of silence-based heuristics, simple acoustic/linguistic models, and costly LLM/SLM full-duplex systems to deliver real-time robust turn-taking, and it addresses training-data scarcity with an automatic VAD future-window labeling and context/dataset construction pipeline.

## Key points

- Traditional silence-based turn-taking waits for a fixed or adaptive silence duration, but silence alone is unreliable because users produce within-utterance pauses, hesitations, thinking pauses, and self-repairs that do not signal handover.
- Turn transitions in many languages are rapid, often 100–500 ms, so listeners must proactively anticipate completions using lexical, prosodic, and multimodal cues rather than merely reacting to silence.
- Prior data-driven acoustic- or linguistic-feature models use relatively simple architectures under real-time constraints, limiting fine-grained cue capture and leaving room for improvement in accuracy and robustness.
- LLM/SLM full-duplex integrations improve quality but need large manually annotated dialogue data, add ASR/latency overhead, prioritize semantics while discarding fine-grained acoustic cues, and degrade in complex real-world scenarios.
- The pipeline extracts frame-level stereo VAD at 50 Hz as binary sequences per channel and labels each frame with a weighted 2-second future-window VAD score, keeping a label only when linear, square-root, and exponential weighting schemes all agree.
- Training samples are anchored at each VAD falling edge after a speech segment, with context extended backward to the previous long silence (≥ 2 seconds) and normalized to a fixed 10-second window via left-padding or truncation.
- Applying the pipeline to 1,128 hours of in-house stereo conversational data yields ~2,299 hours of trainable segments at ~85% labeling accuracy (manual inspection), plus a 95-hour single-utterance set yielding 749 hours where all frames except the final one are Hold (~100% accurate but lacking conversational variability), and the model trains on a mixture of both.

---

## 1. Motivation: why real-time robust turn-taking is hard

**Covers:** chunk Introduction (voice AI agents, silence heuristics, data-driven models, LLM/SLM limits, contributions)

Voice AI agents in customer service, personal assistants, and human–AI collaboration demand natural, extremely low-latency, continuously-listening interaction, which makes them prone to interrupting users before utterances complete. Overly aggressive responses to thinking pauses, hesitations, and self-repairs cause frequent interruptions, disrupted flow, and degraded experience.

Prior approaches and their stated limits:

| Approach | Stated limitation in chunk |
|---|---|
| Heuristic silence-based (fixed/adaptive silence wait) | Unreliable: within-utterance pauses do not signal handover [3,7] |
| Data-driven linguistic- or acoustic-feature models | Simple architectures under real-time constraints; cannot capture fine-grained discriminative cues |
| LLM/SLM full-duplex backbones [14–17] | (1) Need large manually annotated dialogue data, expensive and hard to scale; (2) multi-function backbones (e.g. ASR) add latency [17]; (3) prioritize semantics, discard fine-grained acoustic cues, degrade in complex real-world scenarios |

Verbatim framing quotes from the chunk:

> "Turn-taking is a fundamental property of human spoken interaction [1]."

> "silence alone is an unreliable cue for turn completion: users frequently produce within-utterance pauses that do not signal a handover [3,7]."

> "turn transitions in many languages are rapid, often on the order of 100–500 ms, suggesting listeners do not merely react to silences, but proactively anticipate upcoming turn completions using a combination of lexical, prosodic, and multimodal cues."

Paper contributions as listed in the chunk:

- JAL-Turn: lightweight speech-only turn-taking model jointly leveraging pre-trained acoustic and linguistic encoders, with parallel ASR inference through encoder sharing for low-latency deployment.
- Scalable data construction pipeline that automatically derives reliable turn-taking labels from large-scale real-world dialogue corpora without manual annotation, across domains and languages.
- Extensive experiments on a public multilingual benchmark and an in-house Japanese customer-service corpus, with ablation and attribution analyses, outperforming strong audio-only and LLM-based baselines under real-time constraints.

## 2. Data pipeline: automatic labels from stereo conversation

**Covers:** Section 2 (VAD extraction, future-window labeling, context construction, dataset generation)

Given stereo conversational audio, the pipeline extracts frame-level voice activity detection (VAD) at 50 Hz. For each channel `c ∈ {0, 1}`, it obtains a binary sequence `vc = [vc1, ..., vcT] ∈ {0, 1}^T`, where `vct = 1` indicates speech activity at frame `t`.

### 2.1 Future-window labeling

Motivated by future voice activity projection [18], each frame `t` gets a weighted VAD score over a 2-second future window (Eq. 1):

```text
stc = Σ_{i=0}^{τ·fs} w(i) · vct+i,   with τ = 2 seconds, fs = 50 Hz
```

where `w(i)` is a non-negative weighting function. Three temporal weighting schemes — linear, square-root, and exponential — independently assign Hold/Shift labels (`Hold if stc ≥ st(1−c)`), and a label is kept only when all three schemes agree.

The chunk states this design "effectively suppresses backchannels: instantaneous VAD comparisons are easily confounded by brief listener responses, whereas future VAD patterns provide more reliable cues for genuine turn transitions."

### 2.2 Context construction

Training samples are extracted from each VAD falling edge following a speech segment (natural decision points). For each point, the context window extends backward to the previous long silence (duration ≥ 2 seconds), then is normalized to a fixed 10-second length through left-padding or truncation, ensuring the window always includes a complete preceding speech segment for sufficient semantic context.

### 2.3 Dataset generation

| Source | Input | Output trainable segments | Labeling accuracy (chunk) |
|---|---|---|---|
| In-house stereo conversational data | 1,128 hours | ~2,299 hours | ~85% (manual inspection) |
| In-house single-utterance set, one complete utterance per recording (e.g. "My phone number is 090-8987-2023") | 95 hours | 749 hours, all frames except the final one labeled Hold | nearly 100%, but lacks conversational variability |

The model trains on a mixture of both datasets, combining large-scale conversational dynamics with high-quality utterance-level supervision. The chunk introduces Section 3 (JAL-Turn, five components starting with the dual-path encoder from pre-trained SenseVoice-Small [19]) but this chunk cuts off mid-sentence, so architectural detail belongs to chunk 03.

**Covers:** Introduction motivation through Section 2 Data Pipeline (VAD 50 Hz, Eq. 1 future-window τ = 2 s with 3-scheme agreement, 10-s context with ≥ 2-s silence anchor, 1,128 h → 2,299 h @ ~85% plus 95 h → 749 h @ ~100%).
