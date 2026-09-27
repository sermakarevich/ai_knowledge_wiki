[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Training Objective and Dataset
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
---
## Streaming formulation and delay parameter
> "The delay parameter d determines the trade-off between latency and available input context. In particular, y1 is predicted from hd after the first d raw tokens have been observed."
- At the next aligned step the model consumes the embedding of the previously generated token together with the next available raw-token embedding and predicts y2.
- "Thus, no target token is included in the hidden state used to predict itself."

## Training objective
- Supervision applied only to valid normalized target tokens; zero-padded positions excluded by the target mask.
- Objective (Eq. 8): `LTN = −Σ_{i=1}^{m} log pθ(yi | x≤min(n,i+d−1), y<i)`.
- "This objective trains the model to perform normalization under partial input context, rather than relying on the complete raw sequence."

## Inference alignment
- "During inference, StreamTN follows the same alignment using the autoregressive key–value cache."
- Model first receives d raw tokens and predicts ŷ1 from hd; for i > 1, aligned step t = i+d−1 combines the next raw-token embedding, when available, with E(ŷi−1), and the resulting hidden state predicts ŷi.
- After raw stream ends, raw-input state becomes ⟨pad⟩, whose mapped representation is 0, and decoding continues until an end-of-sequence token or predefined maximum generation budget.

## Latency measurement
- Implementation measures model-side first-token computation time after the first d raw tokens have become available.
- End-to-end first-packet delay additionally includes upstream LLM time (Eq. 9): `FPDe2e(d) = Twait^LLM(d) + Tfirst^TN(d)`.
- `Twait^LLM(d)` is upstream waiting time; `Tfirst^TN(d)` includes embedding the available prefix, the initial Transformer prefill, and computation of the first normalized-token logits.
- "Reporting these two terms separately distinguishes intrinsic TN computation latency from the token-arrival rate of a particular upstream LLM."

## Dataset construction
- Consolidated taxonomy: FlatTN's fine-grained NSW scheme consolidated into ten unified types; four new categories introduced: simple chemical substances, complex chemical equations, simple mathematical formulas, and complex mathematical equations; an evaluation benchmark for Chinese SDS is constructed on this taxonomy.
- Category-specific TN guidelines defined from Chinese TTS pronunciation/readability requirements and applied to annotation and evaluation.
- Source 1: DuReader questions/supporting documents from Baidu Search and Baidu Zhidao, screened with regular-expression NSW detectors, retaining only matched samples as raw inputs.
- Source 2: Qwen3-32B generated additional raw samples for the four scientific categories, manually reviewed to remove unnatural expressions and synthetic artifacts.
- Normalized targets for both sources produced with DeepSeek-R1-70B under the same TN specifications; 5% of training set manually verified with 98.2% judged consistent; all 1,262 held-out test references manually inspected and corrected.
- Scale: 95,793 training samples and 1,262 held-out test samples.

## Experimental setup (as given in chunk)
- Datasets: training set for optimization, test set for generalization to unseen/challenging TN scenarios.
- Baselines: WeTextProcessing (default rules, numerals/dates/units); FlatTN (rule-guided end-to-end, same test set); BiLSTM (data-driven lightweight encoder-decoder, no handcrafted rules); Qwen3-0.6B (task-prompted, no fine-tuning/streaming adaptation).
- Metrics: character-level micro-averaged precision/recall/F1 via minimum-cost Levenshtein alignment counting matches (M), substitutions (S), deletions (D), insertions (I); matches = true positives, substitutions = FP+FN, insertions = FP, deletions = FN; counts accumulated corpus-wide before computing metrics (Eqs. 10–11).
- Environment: PyTorch with Hugging Face Transformers; full-parameter fine-tuning unless noted; LoRA ablation (rank 8, scaling factor 32, dropout 0.05 on q/k/v/o projections, backbone frozen); 4× NVIDIA A6000 with dynamic batching; learning rate 1×10⁻⁵ decaying to 1×10⁻⁶ with cosine annealing over 5,000 steps; five random seeds reported as mean ± std; rule-based/off-the-shelf baselines evaluated once; StreamTN inference greedy on single A6000; upstream Qwen3-32B served with vLLM tensor parallelism on two A6000s at ~20 tokens/s streamed to StreamTN; reported delay follows Eq. (9).

## Overall performance (partial, as given in chunk)
- WeTextProcessing reasonable on predefined patterns but limited by rule coverage; FlatTN Micro-F1 0.7569 vs WeTextProcessing 0.7853.
- Qwen3-0.6B substantially worse than task-specific models; susceptible to format instability and hallucination; elaborate prompts raise prefill cost and first-token latency.
- StreamTN at four-frame delay: Micro-F1 0.8937 ± 0.0009 vs BiLSTM 0.8941 ± 0.0015, with higher Micro-Precision 0.8931 ± 0.0022 vs 0.8677 ± 0.0012; operating point balances quality and first-packet delay, and Table IV shows more input context further improves StreamTN past BiLSTM in Micro-F1.

**Covers:** Streaming formulation (delay d, Eqs. 8–9) through §III.A dataset/benchmark construction and experimental setup into §III.B.1 Overall Performance (partial, Tables I/III/IV referenced but truncated)
