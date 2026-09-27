> [[index|Wiki]] | [[summary|Summary]]

# StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems — Digest

## 1. [[wiki/01-introduction-and-motivation|StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Dialogue Systems]]

**In one sentence:** LLM-centered spoken dialogue systems need low-latency text normalization of non-standard words before TTS, and the authors propose StreamTN — a lightweight Qwen3-0.6B-based Chinese streaming TN model with a dual-track streaming framework — plus a diverse TN benchmark.

## Key points

- TTS in an LLM-centered spoken dialogue system (SDS) requires converting LLM responses into TTS-readable formats via text normalization (TN), with strict low-latency requirements in real-time scenarios.
- Existing TN solutions are largely rule-based, rely on manual engineering, and generalize poorly to unseen patterns.
- Using a general LLM itself for TN via prompt engineering suffers high first-token latency from non-streaming processing, hallucination risks, and degraded reasoning when the core LLM is fine-tuned solely for TN.
- StreamTN is a lightweight LLM-based Chinese streaming TN model built on Qwen3-0.6B, using a dual-track streaming framework where input tokens and output tokens are processed on two parallel tracks for low-latency real-time inference without complex prompting.
- Task-specific fine-tuning gives StreamTN superior TN performance and fewer hallucinations than rule-based systems and general-purpose LLMs (as claimed in the abstract).
- The authors introduce a TN benchmark spanning diverse text scenarios as an evaluation standard for speech generation in SDS; experiments are said to demonstrate effectiveness in accuracy and inference latency.
- LLM outputs contain non-standard words (NSWs) — numbers, dates, time expressions, phone numbers, units, chemical formulas, mathematical expressions — whose pronunciation depends on context (e.g., a number read as a date vs. phone number vs. amount vs. math expression), causing mispronunciations, unnatural prosody, or synthesis failures without TN.

## 2. [[wiki/02-dual-track-streaming-architecture|Dual-Track Streaming Architecture]]

**In one sentence:** Prompt-based LLM text normalization cannot meet streaming dialogue demands, so StreamTN uses a fine-tuned Qwen3-0.6B dual-track architecture that incrementally converts partial LLM outputs into TTS-readable text with controllable first-packet delay.

## Key points

- Prompt-based TN (e.g., PolyNorm few-shot LLM TN with a multilingual benchmark [16]) requires waiting for sufficient or complete context, adds latency, and risks unstable formatting or hallucinated outputs in cascaded spoken dialogue systems (SDS).
- In cascaded SDS the TN module must process partial LLM outputs and feed normalized text to the TTS module in real time, while both upstream LLM and downstream streaming TTS (cf. [17]) operate incrementally.
- An effective dialogue TN module must satisfy two requirements simultaneously: produce accurate TTS-readable text preserving pronunciation correctness and semantic consistency, and do so incrementally with low latency.
- Existing TN datasets focus on conventional NSW categories, offline sentence-level normalization, or multilingual TTS normalization, and miss the distribution, diversity, and latency requirements of real LLM dialogue responses.
- StreamTN is a lightweight Chinese streaming TN model built on Qwen3-0.6B [19] that decouples raw-text input tokens and normalized-text output tokens into two parallel tracks, starting normalization after only a small number of input tokens.
- Task-specific fine-tuning lets StreamTN learn structured normalization patterns without complex prompting and with reduced hallucination risk.
- A new Chinese dialogue-oriented TN benchmark covers 14 categories — numbers, dates, time, phone numbers, units, plus chemical formulas, mathematical equations, and scientific terms — evaluating accuracy, robustness, and streaming-inference latency.
- Emitting too early risks incorrect readings while waiting too long increases first-packet TTS latency, so StreamTN controls input lookahead with a fixed delay parameter while remaining compatible with standard autoregressive decoding.

## 3. [[wiki/03-training-objective-and-dataset|Training Objective and Dataset]]

**In one sentence:** The delay parameter d controls the latency–context trade-off in StreamTN's aligned streaming formulation, trained with a masked negative log-likelihood under partial context and evaluated on a newly constructed 95,793/1,262 Chinese SDS benchmark.

## Key points

- Delay d sets the trade-off between latency and available input context: y1 is predicted from hd only after the first d raw tokens are observed, and no target token is included in the hidden state used to predict itself.
- Training objective is masked negative log-likelihood `LTN = −Σ log pθ(yi | x≤min(n,i+d−1), y<i)` (Eq. 8), with supervision only on valid normalized target tokens and zero-padded positions excluded by the target mask.
- Inference reuses the same alignment with an autoregressive key–value cache: start from d raw tokens to predict ŷ1 from hd, then at aligned step t = i+d−1 combine the next raw-token embedding (when available) with E(ŷi−1) to predict ŷi.
- After the raw stream ends the raw-input state becomes ⟨pad⟩ (mapped representation 0) and decoding continues until end-of-sequence or a predefined maximum generation budget.
- End-to-end first-packet delay is `FPDe2e(d) = Twait^LLM(d) + Tfirst^TN(d)` (Eq. 9), where Tfirst^TN covers embedding the prefix, the initial Transformer prefill, and first normalized-token logits; the two terms separate intrinsic TN latency from the upstream LLM token-arrival rate.
- Benchmark taxonomy consolidates FlatTN categories into ten unified types and adds four new scientific categories (simple chemical substances, complex chemical equations, simple mathematical formulas, complex mathematical equations), with 95,793 training and 1,262 held-out test samples.
- Training corpus combines regex-filtered DuReader (Baidu Search/Zhidao) samples with Qwen3-32B-generated scientific samples (manually reviewed), normalized by DeepSeek-R1-70B; 5% manual check gives 98.2% guideline consistency and all 1,262 test references were manually inspected and corrected.
- At four-frame delay StreamTN reaches Micro-F1 0.8937 ± 0.0009 (vs BiLSTM 0.8941 ± 0.0015) with higher Micro-Precision (0.8931 ± 0.0022 vs 0.8677 ± 0.0012); FlatTN is 0.7569 vs WeTextProcessing 0.7853, and more context (Table IV) lets StreamTN surpass BiLSTM in Micro-F1.

## 4. [[wiki/04-experiments-results-and-conclusions|Experiments, Results, and Conclusions]]

**In one sentence:** StreamTN (4-frame delay) reaches 0.8937 Micro-F1 / 0.8931 Micro-Precision at 213 ms FPD — matching BiLSTM while streaming — with regular categories above 0.95, math/chemical formulas as the hardest cases, full-parameter fine-tuning beating LoRA and system-prompt variants, and longer delay steadily trading latency for accuracy.

## Key points

- Baseline comparison: StreamTN achieves 0.8937 ± 0.0009 Micro-F1 and 0.8931 ± 0.0022 Micro-Precision, comparable to BiLSTM (0.8941 ± 0.0015 / 0.8677 ± 0.0012) while supporting incremental processing, and well above WeTextProcessing (0.7853 / 0.7586), FlatTN (0.7569 ± 0.0019 / 0.7390 ± 0.0017), and Qwen3-0.6B (0.4872 / 0.5282).
- Per-category peaks: physical units (0.977 Micro-F1), capital amounts (0.975), and time expressions (0.967) perform best; integers and decimals, fractions and percentages, and years and dates all exceed 0.95 Micro-F1.
- Hardest categories: complex mathematical equations (0.750 Micro-F1) and chemical formulas (0.791 Micro-F1), attributed to "specialized notation, long verbalizations, and structural diversity" increasing character-level normalization difficulty.
- Ablation on tuning: replacing full-parameter fine-tuning with LoRA drops performance to 0.6335 ± 0.0012 Micro-F1 and 0.6250 ± 0.0015 Micro-Precision, indicating "updating only low-rank adapters is insufficient to learn the precise transformations required by TN."
- Ablation on prompting: adding a system prompt yields "a small but consistent decrease" to 0.8852 ± 0.0018 Micro-F1 and 0.8824 ± 0.0021 Micro-Precision, showing StreamTN can "generate structured normalized text without carefully engineered prompts."
- Delay trade-off: increasing delay from 1 to 16 frames raises Micro-F1 from 0.7030 to 0.9239 and Micro-Precision from 0.7135 to 0.9303, while FPD rises from 75 ms to 756 ms; the non-streaming model is highest (0.9639 / 0.9620) but "cannot produce normalized output until the entire sequence has been received."
- Adopted setting: the 4-frame configuration is adopted "as a practical trade-off between normalization quality and responsiveness," achieving 0.8937 Micro-F1 and 0.8931 Micro-Precision with 213 ms FPD.

## The argument in five moves

1. Cascaded LLM-centered spoken dialogue systems need text normalization of context-dependent non-standard words before streaming TTS, but existing rule-based, neural-offline, and prompt-based LLM approaches fail on generality, streaming latency, or hallucination risk.
2. StreamTN answers this with a lightweight Qwen3-0.6B model using a dual-track streaming architecture that decouples raw-input and normalized-output tokens into parallel tracks, emitting after only a small fixed delay while staying compatible with standard autoregressive decoding.
3. The delay parameter d formalizes the latency–context trade-off: training by masked negative log-likelihood under partial context and inference with KV-cache alignment, with end-to-end first-packet delay split into upstream-LLM wait and intrinsic TN compute.
4. A new Chinese dialogue-oriented benchmark (ten consolidated FlatTN types plus four scientific categories; 95,793 training / 1,262 manually verified test samples) grounds evaluation in real SDS distributions including chemical and mathematical expressions.
5. Experiments show the 4-frame setting matches BiLSTM quality (0.8937 Micro-F1) at 213 ms FPD while streaming, dominates rule-based and prompted baselines, needs full-parameter fine-tuning rather than LoRA or system prompts, and improves steadily with longer delay — leaving complex math/chemical formulas as the remaining hard cases and future work.
