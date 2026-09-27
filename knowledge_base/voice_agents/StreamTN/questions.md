---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems

### Q1. Why does an LLM-centered cascaded spoken dialogue system need text normalization before TTS, and what makes non-standard words hard?

> [!tip]- Answer
> > LLM responses contain non-standard words readable to humans but ambiguous for synthesis, such as numbers, dates, phone numbers, amounts, units, and chemical or mathematical expressions. The same written form can require different pronunciations depending on context, so without normalization the TTS output risks mispronunciations, unnatural prosody, or synthesis failures. See [[wiki/01-introduction-and-motivation|StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Dialogue Systems]].

### Q2. How does StreamTN's dual-track streaming architecture process raw input and normalized output?

> [!tip]- Answer
> > StreamTN decouples raw-text input tokens and normalized-text output tokens into two parallel tracks whose embeddings are fused before the Qwen3-0.6B backbone. The input track carries currently available raw context while the output track carries delayed normalized history, so the model generates normalized tokens autoregressively while still consuming new raw tokens. See [[wiki/02-dual-track-streaming-architecture|Dual-Track Streaming Architecture]].

### Q3. Why can't prompt-based LLM text normalization meet streaming dialogue demands?

> [!tip]- Answer
> > Prompt-based methods such as PolyNorm few-shot normalization usually wait for sufficient or complete context, which adds latency in a cascaded system where both the upstream LLM and downstream TTS operate incrementally. They also risk unstable formatting and hallucinated outputs, whereas StreamTN uses task-specific fine-tuning to learn structured patterns with controllable first-packet delay and reduced hallucination risk. See [[wiki/02-dual-track-streaming-architecture|Dual-Track Streaming Architecture]].

### Q4. What is the training objective of StreamTN and how does the delay parameter d control the latency–context trade-off?

> [!tip]- Answer
> > The delay parameter d sets how many raw tokens are observed before the first normalized token is emitted, with y1 predicted from hd only after d raw tokens arrive and no target token included in the hidden state used to predict itself. Training uses masked negative log-likelihood LTN = −Σ log pθ(yi | x≤min(n,i+d−1), y<i) with supervision only on valid target tokens, forcing normalization under partial context. See [[wiki/03-training-objective-and-dataset|Training Objective and Dataset]].

### Q5. How was StreamTN's Chinese dialogue-oriented TN benchmark constructed and at what scale?

> [!tip]- Answer
> > The taxonomy consolidates FlatTN categories into ten unified types and adds four scientific categories covering simple and complex chemical and mathematical expressions. Raw inputs combine regex-filtered DuReader samples with Qwen3-32B-generated scientific samples, normalized by DeepSeek-R1-70B, yielding 95,793 training and 1,262 manually verified test samples. See [[wiki/03-training-objective-and-dataset|Training Objective and Dataset]].

### Q6. What were StreamTN's key experimental results, including ablations and the streaming delay trade-off?

> [!tip]- Answer
> > At 4-frame delay StreamTN reaches 0.8937 Micro-F1 and 0.8931 Micro-Precision at 213 ms first-packet delay, matching BiLSTM while streaming and well above rule-based and prompted baselines. Full-parameter fine-tuning beats LoRA (0.6335 Micro-F1) and adding a system prompt slightly hurts (0.8852), while increasing delay from 1 to 16 frames raises Micro-F1 from 0.7030 to 0.9239 at the cost of 75 to 756 ms latency. See [[wiki/04-experiments-results-and-conclusions|Experiments, Results, and Conclusions]].

### Q7. Would you recommend adopting StreamTN's 4-frame configuration for a production Chinese voice assistant, and why?

> [!tip]- Answer
> > Yes, the 4-frame setting is a sound default because it matches BiLSTM quality while streaming at only 213 ms first-packet delay without prompt engineering. The main caveat is that complex mathematical equations and chemical formulas remain the hardest cases, so a deployment heavy in scientific content should budget longer delay or added handling for those categories. See [[wiki/04-experiments-results-and-conclusions|Experiments, Results, and Conclusions]].
