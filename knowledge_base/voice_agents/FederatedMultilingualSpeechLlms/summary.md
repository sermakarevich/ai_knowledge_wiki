# Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking

**Paper:** [Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking](http://arxiv.org/abs/2609.23825v1)

## Human Readable TL;DR

This paper asks how to train voice-transcription AI across many phones or hospitals without ever collecting the raw audio in one place, like having hundreds of choirs rehearse separately but still produce one shared songbook. It tests different combinations of ears (speech encoders) and brains (language models) on eight European languages where each volunteer speaks only one language, which makes the shared learning wobbly because everyone pulls toward their own accent and vocabulary. The big lessons are that the language-model brain matters most for rare languages, that each part of the system needs its own practice speed, and that a stabilizing technique called FedProx only helps when the brain is already strong and multilingual.

## TL;DR

The paper provides the first systematic benchmark of federated multilingual ASR with Speech-LLMs on speaker-partitioned Multilingual LibriSpeech (8 languages, 316 single-speaker clients), comparing four Whisper/WavLM × TinyLlama/EuroLLM pairings plus Voxtral-Mini under FedAvg versus FedProx with frozen and unfrozen encoders. Independently tuning per-component learning rates for encoder, connector, and decoder and adapting all three components (LoRA on encoder and decoder plus a fully trained connector) gives the lowest error rates. FedProx is architecture-dependent rather than universally helpful: it yields the best frozen-encoder result for Whisper + EuroLLM (0.133 to 0.122 WER) while degrading Whisper + TinyLlama and Voxtral, with the gains concentrated in low-resource languages such as Dutch.

---

## Problem & Motivation

Speech-LLMs that pair an acoustic encoder with a pretrained language decoder through a lightweight connector have become a leading recipe for multilingual and low-resource speech recognition, yet privacy-sensitive settings such as healthcare, legal work, and personal assistants cannot centralize raw audio for training. Prior federated speech research focused on encoder-only or language-specific models, leaving open how full Speech-LLMs behave when clients differ simultaneously in language, accent, speaker identity, and recording conditions. The paper therefore frames two questions: which encoder–LLM combination best withstands multilingual non-IID client drift, including whether ASR-supervised or self-supervised encoders adapt better, and whether FedProx mitigates language drift in this setting. To answer them it builds a deliberately harsh testbed from Multilingual LibriSpeech, assigning each of 316 clients all utterances of a single speaker so that every client speaks at most one language with its own acoustic signature, and contrasts this with an approximately IID multilingual-mixture control.

## Main Original Ideas

1. **Federated Speech-LLM benchmark design:** the first head-to-head federated evaluation of four encoder–LLM pairings (Whisper large-v3-turbo or WavLM-Large with TinyLlama-1.1B or EuroLLM-1.7B-Instruct, plus Voxtral-Mini-3B) on the same speaker-partitioned MLS pool, with synchronized Flower/Ray training, 10 local AdamW epochs per round, LoRA adapters on encoder and decoder plus a from-scratch connector as the only trainable and communicated parameters, and centralized plus IID-partition upper bounds for calibration.

2. **Three-component adaptation with differential learning rates:** the finding that the encoder, connector, and decoder each need their own learning-rate scale, and that full three-way adaptation (LoRA for encoder and decoder, full training of the connector that must learn the cross-modal bridge from federated data alone) outperforms frozen-encoder or partially tuned variants when the rates are chosen on the dev set.

3. **Architecture-conditioned aggregation analysis:** a systematic FedAvg versus FedProx comparison showing that the proximal penalty is not a generic fix for multilingual drift but interacts with backbone capacity and pretraining, helping the multilingual EuroLLM decoder while hurting smaller or already tightly co-adapted models, supported by per-language and macro-averaged WER breakdowns that reveal where the gains come from.

## Key Findings

Centralized ceilings already separate the architectures sharply: Whisper + EuroLLM reaches 0.066 WER versus 0.072 for Whisper + TinyLlama, confirming a multilingual-decoder advantage even without federated pressure, while WavLM + TinyLlama stalls at 0.24, roughly 3.3× worse, showing that ASR-supervised encoder pretraining decisively beats self-supervised pretraining for this ASR task. Under frozen-encoder federated training on the non-IID speaker partition, Whisper + TinyLlama degrades to 0.1415, Whisper + EuroLLM to 0.133, Voxtral-Mini to 0.144, and WavLM + TinyLlama collapses to 0.56, so federated averaging preserves the centralized ranking but roughly doubles error for the Whisper families. Unfreezing the encoder only helps when its learning rate is scaled far below the LLM rate (around 0.02×), turning Whisper + EuroLLM from 0.178 down to 0.117, whereas naive equal-rate unfreezing hurts and TinyLlama stays flat at its frozen baseline. FedProx with µ=0.001 improves Whisper + EuroLLM from 0.133 to 0.122, the best frozen-encoder federated result, but monotonically degrades Whisper + TinyLlama and both Voxtral settings as µ grows, proving the regularizer is architecture-dependent. Per-language results show EuroLLM beating TinyLlama under FedAvg on six of eight languages with the largest gains on low-resource Portuguese, Italian, and Polish, and FedProx adding further wins on Dutch (0.265 to 0.195), Polish, English, French, and Spanish while losing on German, Italian, and Portuguese; because English dominates the client count and overall WER, the macro-averaged gap (0.170 versus 0.150) better exposes EuroLLM's low-resource advantage than the word-weighted gap.

## Suggestions & Future Directions

The wiki chunks point toward concrete deployment guidance for privacy-sensitive multilingual settings: prefer ASR-pretrained encoders over SSL encoders when the downstream task is transcription, pair them with a multilingual LLM backbone for resilience to non-IID drift, always adapt and separately tune the connector alongside LoRA adapters, and apply FedProx selectively with small µ after dev-set validation rather than as a default. Natural extensions include testing stronger heterogeneity remedies beyond FedProx, exploring deeper or higher-compression connectors, extending beyond the eight European MLS languages to truly low-resource and typologically distant languages, and quantifying the communication–accuracy tradeoff of transmitting encoder adapters versus keeping the encoder frozen. Careful handling of speaker leakage between MLS splits should also continue, since the chunks note that raw gaps to centralized bounds slightly overstate non-IID degradation.

## Authors & Institutions

The wiki chunks used for this summary do not record author names or institutional affiliations, so no authors or institutions are listed here rather than inventing them from the source paper or the web.
