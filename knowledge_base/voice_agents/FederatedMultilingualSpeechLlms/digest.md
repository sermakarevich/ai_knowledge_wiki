> [[index|Wiki]] | [[summary|Summary]]
# Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking — Digest

## 1. [[wiki/01-federated-multilingual-speech-llms-architecture|Federated Multilingual Speech-LLMs: Architecture and Aggregation]]
**In one sentence:** This chunk benchmarks federated learning for multilingual ASR with four Speech-LLM architectures on Multilingual LibriSpeech, comparing FedAvg vs FedProx under frozen/unfrozen encoders and showing that per-component learning rates and full three-component adaptation give the best results, with FedProx gains depending on LLM backbone capacity.
## Key points
- Benchmarks four Speech-LLM (encoder–LLM) families for federated multilingual ASR on Multilingual LibriSpeech.
- Compares FedAvg and FedProx across frozen and unfrozen speech-encoder configurations.
- Independently tuning learning rates for speech encoder, connector, and decoder yields the lowest error rates.
- Full three-component adaptation — LoRA for encoder and decoder, full training for the connector — produces the best FL results.
- FedProx efficacy is architecture-dependent, with notable advantages in multilingual pretrained architectures (e.g., EuroLLM over TinyLlama when keeping the encoder fixed).
- LLM backbone capacity mediates resilience to heterogeneous (non-IID) data distributions.
- FL setup uses a speaker-partitioned Multilingual LibriSpeech split: 8 European languages, 316 clients, one speaker per client.

## 2. [[wiki/02-speech-llm-architecture-encoder-connector-decoder|Speech-LLM architecture: encoder, connector, decoder]]
**In one sentence:** Figure 1 defines a three-part speech-LLM where encoder E maps speech x to frame-level features, connector C downsamples by factor k, and decoder L generates ŷ from the projected tokens plus a task prompt, instantiated in four Whisper/WavLM × TinyLlama/EuroLLM pairings.
## Key points
- Encoder E maps speech input x to frame-level acoustic features; connector C downsamples those features by factor k; decoder L generates output ŷ from the projected tokens and a task prompt.
- The paper evaluates four encoder–LLM pairings built from two encoders (Whisper, WavLM) and two decoders (TinyLlama, EuroLLM).
- Whisper large-v3-turbo encodes audio into 768-dimensional speech frame representations, projected to 2048-dimensional tokens to align with TinyLlama-1.1B (22 layers).
- Whisper's encoder has 32 layers and, as a pretrained end-to-end multilingual ASR model, already captures robust cross-lingual acoustic features.
- The Whisper + EuroLLM variant keeps the identical Whisper encoder but replaces the decoder with EuroLLM-1.7B-Instruct, a decoder-only model pretrained on multilingual European text corpora.
- The WavLM + TinyLlama variant replaces Whisper with WavLM-Large (1024-dimensional tokens, 24 layers) while keeping TinyLlama as decoder.
- WavLM is a self-supervised learning (SSL) model pretrained on masked speech prediction and, unlike Whisper, has never seen ASR supervision.

## 3. [[wiki/03-ssl-vs-asr-encoder-adaptability|SSL vs ASR Encoder Adaptability — A Stronger Test of Whether FL Can Adapt an SSL Encoder]]
**In one sentence:** The chunk sets up a stronger test of whether FL can adapt an SSL encoder to ASR by contrasting WavLM (SSL) with Whisper (ASR-supervised) encoders under IID multilingual versus single-speaker non-IID partitions, with centralized results showing ASR pretraining decisively beats SSL pretraining (0.072 vs 0.24 WER).
## Key points
- The chunk frames the comparison as "a stronger test of whether FL can adapt an SSL encoder to the downstream ASR task", i.e. WavLM-Large (SSL) versus Whisper (ASR-supervised) paired with the same TinyLlama-1.1B decoder.
- Voxtral-Mini is an end-to-end multimodal Speech-LLM composed of a Whisper-large-v3-based audio encoder and a 30-layer Ministral-3B text decoder, jointly pretrained on audio understanding and ASR.
- All experiments use Multilingual LibriSpeech (MLS): 685.7 h federated training pool, MLS dev for validation, MLS test as held-out benchmark (138 h, 19,492 samples) across 8 European languages.
- The multilingual partition (A, approximately IID) assigns a multilingual mixture of utterances to each client irrespective of speaker identity as a control isolating heterogeneity from architecture choice; the speaker partition (B, non-IID) assigns all utterances of one speaker to one client (K=316), creating simultaneous linguistic and acoustic heterogeneity.
- Speaker leakage is inherited from LibriVox/MLS splits: centralized training carries 3.5% leakage; partition (A) contaminates 59/316 clients (18.7%, 60,825 of 1,726,583 samples); partition (B) has 8/316 clients (2.5%, 4,747 of 169,586 samples) overlapping test speakers — so "the actual degradation caused by FL non-IID conditions is slightly less severe than the raw distance to the upper bounds suggests".
- Training uses Flower with Ray backend, E=10 local epochs per round, AdamW with max lr 1e-4, cosine decay, batch 16, bf16; partition (B) trains T=40 rounds while partition (A) is reported at T=9 because its "rapid convergence leading to early WER optimization collapse".
- Only LoRA adapters (rank r=8, α=16, dropout 0.05; Voxtral α=32) on encoder (q, k, v) and LLM decoder (q, v) plus the fully-trained connector are trainable/transmitted; the connector (except Voxtral) is initialised from scratch so "it must learn to bridge the modalities entirely from the federated fine-tuning data".
- Centralized ceilings: Whisper+EuroLLM WER 0.0660 vs Whisper+TinyLlama 0.0719 ("confirming the multilingual LLM advantage even without non-IID pressure"); WavLM+TinyLlama 0.2409 (3.3× higher), "showing that ASR pretraining of the encoder decisively beats SSL pretraining for ASR".

## 4. [[wiki/04-per-language-wer-fedavg-vs-fedprox|Per-Language WER: FedAvg vs FedProx (TinyLlama vs EuroLLM)]]
**In one sentence:** Per-language results show EuroLLM beats TinyLlama on six of eight languages with the largest gains on low-resource languages, and FedProx (µ=0.001) further improves EuroLLM to 0.122 overall with its strongest gain on Dutch, the least-represented language.
## Key points
- FedAvg overall WER: Whisper+TinyLlama 0.142 vs Whisper+EuroLLM 0.133 vs FedProx EuroLLM (µ=0.001) 0.122, against centralized 0.072.
- EuroLLM outperforms TinyLlama under FedAvg on six of eight languages, with the largest absolute gains on Portuguese (−6.5%), Italian (−4.8%), and Polish (−3.3%).
- FedProx EuroLLM (µ=0.001) improves over FedAvg EuroLLM on five of eight languages: Dutch (0.265 → 0.195, −7.0% abs.), Polish, English, French, and Spanish.
- FedProx EuroLLM degrades three languages relative to FedAvg EuroLLM: German (+2.6% abs.), Italian, and Portuguese.
- The FedProx benefit is strongest for the least-represented languages (≤ 4 clients), while moderate-resource languages show mixed results.
- Client distribution is strongly skewed toward English (256 of 316 clients) and overall WER is dominated by high-resource evaluation words.
- Macro-averaged WER (unweighted mean of per-language values): FedAvg TinyLlama 0.170 versus EuroLLM 0.150; the macro gap (−2.0 points) exceeds the word-weighted gap (−0.9 points), confirming the EuroLLM advantage is driven by low-resource languages.

## The argument in five moves
1. Federated multilingual Speech-LLMs must be benchmarked under realistic speaker-partitioned non-IID heterogeneity (8 languages, 316 single-speaker clients), where architecture and aggregation choices jointly determine robustness.
2. The three-component design (encoder–connector–decoder) makes adaptation strategy decisive: per-component learning rates and full three-component adaptation (LoRA encoder/decoder plus fully-trained connector) give the best FL results.
3. Encoder pretraining sets the ceiling: ASR-supervised Whisper decisively beats SSL-pretrained WavLM both centrally (0.072 vs 0.24 WER) and under FL, showing FL cannot rescue a mismatched SSL encoder for ASR.
4. Decoder capacity and multilingual priors mediate non-IID resilience: EuroLLM beats TinyLlama overall (0.133 vs 0.142) and especially on low-resource languages, confirmed by the larger macro-averaged gap.
5. Aggregation must match backbone capacity: FedProx (µ=0.001) yields the best frozen-encoder result on EuroLLM (0.122, strongest on least-represented Dutch) while degrading TinyLlama and Voxtral, so proximal regularisation helps only when the multilingual backbone can exploit it.
