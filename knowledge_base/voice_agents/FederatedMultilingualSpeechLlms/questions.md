---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking

### Q1. What are the paper's two research questions (Q1 architecture, Q2 aggregation) and the speaker-partitioned FL setup used to test them?

> [!tip]- Answer
> Q1 asks which encoder–LLM combination best handles multilingual non-IID client distributions and whether ASR-supervised versus self-supervised encoder type affects federated adaptability, while Q2 asks whether FedProx mitigates client language drift in this Speech-LLM setting. The testbed is speaker-partitioned Multilingual LibriSpeech with 8 European languages and K=316 single-speaker clients, inducing simultaneous acoustic, linguistic, and domain heterogeneity, with local Speech-LLMs fine-tuned via LoRA under frozen and unfrozen encoder configurations. See [[wiki/01-federated-multilingual-speech-llms-architecture|Federated Multilingual Speech-LLMs: Architecture and Aggregation]].

### Q2. What adaptation strategy gives the best federated results, and how does FedProx efficacy depend on architecture?

> [!tip]- Answer
> Independently tuning learning rates for the speech encoder, connector, and decoder yields the lowest error rates, and full three-component adaptation — LoRA adapters on encoder and decoder plus a fully-trained connector — produces the best FL results. FedProx efficacy is architecture-dependent: it helps multilingual-pretrained backbones such as EuroLLM over TinyLlama when keeping the encoder fixed, so LLM backbone capacity mediates resilience to heterogeneous non-IID distributions. See [[wiki/01-federated-multilingual-speech-llms-architecture|Federated Multilingual Speech-LLMs: Architecture and Aggregation]].

### Q3. How does the three-component Speech-LLM pipeline map speech to transcript, and what is the training objective?

> [!tip]- Answer
> Encoder E maps speech x to frame-level acoustic features, connector C downsamples those features by factor k (frame-stacking with stride 2 plus a trainable projection to LLM dimension), and decoder L generates output ŷ from the projected tokens plus the task prompt as ŷ = L([C(E(x)); Etext]). All trainable parameters (LoRA adapters plus connector projection) are trained jointly by minimizing standard autoregressive cross-entropy over ground-truth transcript tokens, with audio tokens and prompt embeddings as conditioning context. See [[wiki/02-speech-llm-architecture-encoder-connector-decoder|Speech-LLM architecture: encoder, connector, decoder]].

### Q4. What are the four Whisper/WavLM × TinyLlama/EuroLLM pairings, and how do the FedAvg and FedProx updates differ?

> [!tip]- Answer
> The benchmark pairs two encoders — Whisper large-v3-turbo (768-dim frames, 32 layers, ASR-supervised cross-lingual acoustics) and WavLM-Large (1024-dim tokens, 24 layers, SSL masked-prediction pretraining without ASR supervision) — with two decoders, TinyLlama-1.1B (2048-dim, 22 layers) and EuroLLM-1.7B-Instruct (decoder-only, multilingual European text pretraining). FedAvg performs sample-weighted averaging of client updates each round, θ(t+1) = Σ (n_k/Σn_j) θ(t,k) over the sampled fraction (C = 0.3, E = 10 local AdamW epochs), while FedProx adds a proximal penalty min L_local(θ) + (µ/2)||θ − θ(t)||² to limit drift from narrow per-client acoustic distributions. See [[wiki/02-speech-llm-architecture-encoder-connector-decoder|Speech-LLM architecture: encoder, connector, decoder]].

### Q5. How do the multilingual (A) and speaker (B) partitions differ, and what are the key dataset, leakage, and training details?

> [!tip]- Answer
> Partition A (approximately IID) assigns a random multilingual mixture of utterances to each client as a heterogeneity control, while partition B (non-IID) assigns all utterances of one speaker to one client (K=316), creating simultaneous single-language and single-acoustic-identity heterogeneity across 685.7 h of MLS training audio (dev for validation, 138 h / 19,492-sample test for evaluation). Speaker leakage inherited from LibriVox/MLS means partition A contaminates 59/316 clients (18.7%) versus only 8/316 (2.5%) in partition B, so raw FL-to-centralized gaps slightly overstate non-IID degradation. Training uses Flower with Ray, E=10 local epochs, AdamW at max lr 1e-4 with cosine decay and bf16, T=40 rounds for B but T=9 for A due to rapid-convergence WER collapse, with only LoRA adapters (r=8, α=16) plus a from-scratch connector trainable and transmitted. See [[wiki/03-ssl-vs-asr-encoder-adaptability|SSL vs ASR Encoder Adaptability — A Stronger Test of Whether FL Can Adapt an SSL Encoder]].

### Q6. What do the centralized ceilings and per-language FedAvg/FedProx results show about encoders, EuroLLM, and FedProx?

> [!tip]- Answer
> Centralized ceilings show ASR pretraining decisively beats SSL pretraining (Whisper+TinyLlama 0.0719 vs WavLM+TinyLlama 0.2409, ~3.3×) with a multilingual-decoder edge (Whisper+EuroLLM 0.0660), proving FL cannot rescue a mismatched SSL encoder for ASR. Under frozen-encoder FedAvg, EuroLLM beats TinyLlama overall (0.133 vs 0.142) on six of eight languages with the largest gains on low-resource Portuguese (−6.5%), Italian (−4.8%), and Polish (−3.3%), and the macro-averaged gap (−2.0 points) exceeds the word-weighted gap (−0.9), confirming the advantage is low-resource-driven. FedProx (µ=0.001) improves EuroLLM to 0.122 overall with its strongest gain on least-represented Dutch (0.265 → 0.195) plus Polish, English, French, and Spanish, but degrades German (+2.6%), Italian, and Portuguese while monotonically hurting TinyLlama and Voxtral. See [[wiki/04-per-language-wer-fedavg-vs-fedprox|Per-Language WER: FedAvg vs FedProx (TinyLlama vs EuroLLM)]].

### Q7. For a privacy-sensitive deployment covering low-resource European languages under single-speaker non-IID clients, which architecture–aggregation combination would you recommend and why?

> [!tip]- Answer
> Recommend Whisper (frozen or carefully LR-scaled unfrozen) paired with EuroLLM-1.7B plus FedProx at µ=0.001 with per-component learning rates and full three-component adaptation, because this is the only combination that jointly holds the best centralized ceiling, the best frozen-encoder FL result (0.122), and the largest low-resource gains including Dutch. Avoid WavLM-based builds since neither centralized nor federated training overcomes the SSL-to-ASR mismatch, and avoid applying FedProx to TinyLlama or Voxtral where it degrades WER. Accept the trade-off that FedProx still degrades German, Italian, and Portuguese relative to FedAvg EuroLLM, so monitor those languages explicitly. See [[wiki/04-per-language-wer-fedavg-vs-fedprox|Per-Language WER: FedAvg vs FedProx (TinyLlama vs EuroLLM)]].
