> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Federated Multilingual Speech-LLMs: Architecture and Aggregation
**In one sentence:** This chunk benchmarks federated learning for multilingual ASR with four Speech-LLM architectures on Multilingual LibriSpeech, comparing FedAvg vs FedProx under frozen/unfrozen encoders and showing that per-component learning rates and full three-component adaptation give the best results, with FedProx gains depending on LLM backbone capacity.
## Key points
- Benchmarks four Speech-LLM (encoder–LLM) families for federated multilingual ASR on Multilingual LibriSpeech.
- Compares FedAvg and FedProx across frozen and unfrozen speech-encoder configurations.
- Independently tuning learning rates for speech encoder, connector, and decoder yields the lowest error rates.
- Full three-component adaptation — LoRA for encoder and decoder, full training for the connector — produces the best FL results.
- FedProx efficacy is architecture-dependent, with notable advantages in multilingual pretrained architectures (e.g., EuroLLM over TinyLlama when keeping the encoder fixed).
- LLM backbone capacity mediates resilience to heterogeneous (non-IID) data distributions.
- FL setup uses a speaker-partitioned Multilingual LibriSpeech split: 8 European languages, 316 clients, one speaker per client.
---
## Abstract: benchmark scope and findings
**Covers:** Abstract

Evaluates four Speech-LLM architectures on Multilingual LibriSpeech, comparing FedAvg and FedProx across frozen and unfrozen encoder configurations. Claims optimized learning rates are critical; specifically, independently tuning learning rates for speech encoder, connector, and decoder yields the lowest error rates. Full three-component adaptation (LoRA for encoder and decoder, full training for the connector) produces the best FL results. FedProx efficacy is architecture-dependent, with advantages in multilingual pretrained architectures (e.g., "EuroLLM over TinyLlama when keeping the encoder fixed"); LLM backbone capacity plays a key role in resilience to heterogeneous data distributions.

Verbatim: "These findings offer concrete design guidance for deploying multilingual Speech-LLMs in privacy-sensitive, distributed environments."

## Introduction: research questions
**Covers:** 1. Introduction

Speech-LLMs combine acoustic encoders with pretrained language decoders through a lightweight cross-modal connector, leveraging large-scale text pretraining for language priors and state-of-the-art multilingual/low-resource results. Privacy-sensitive deployments (healthcare, legal, personal assistants) motivate FL without centralising raw audio. Prior federated speech work targeted encoder-only or language-based architectures; no previous work directly investigated federated training of Speech-LLMs.

Two questions:
- (Q1) Architecture: which encoder–LLM combination best handles multilingual non-IID client distributions; does encoder type (ASR-supervised vs. self-supervised) affect federated adaptability?
- (Q2) Aggregation: does FedProx mitigate client language drift in this multilingual Speech-LLM setting?

Multilingual clients differ simultaneously in language, accent, speaker population, and recording conditions, causing client drift that destabilises FL optimisation and motivates FedProx or SCAFFOLD.

## Experimental framing
**Covers:** 1. Introduction (setup paragraph)

Speaker-partitioned Multilingual LibriSpeech: 8 European languages, 316 clients, one speaker per client — inducing simultaneous acoustic, linguistic, and domain-level heterogeneity. Local Speech-LLMs fine-tuned with LoRA under frozen and unfrozen speech encoders, with connector and LLM always unfrozen. Analyses cover pretrained encoder vs. LLM backbone interplay, differential per-component learning rates, and FedAvg vs. FedProx behaviour.

## System architecture: encoder–connector–decoder
**Covers:** 2. System Architectures

Speech-LLMs couple three components — acoustic encoder (E), cross-modal connector (C), language decoder (L):

| Symbol | Meaning |
|---|---|
| E | acoustic encoder |
| C | cross-modal connector |
| L | language decoder |
| Etext | text/prompt embeddings |

Transcript equation (1):

```
ŷ = L ([C(E(x)); Etext])
```

All three trained jointly by minimising standard autoregressive cross-entropy over ground-truth transcript tokens y = (y1, …, yS) (equation 2):

```
              S
LCE(θ) = − Σ log pθ (ys | C(E(x)), Etext, y<s)
             s=1
```

where θ collects all trainable parameters (LoRA adapters and connector projection), and y<s denotes preceding tokens via teacher forcing. Loss computed over transcript tokens; audio tokens and prompt embeddings appear as conditioning context.

## Federated optimisation: FedAvg
**Covers:** Algorithm 1 FedAvg

Algorithm 1 states: θ = LoRA adapters + connector; K = clients; nk = samples on client k; C = client fraction/round; B = batch size; E = 10 local epochs; η = 1e-4.

Server: initialise θ0; each round t = 1, 2, …, T: sample St = random set of max(C·K, 1) clients; each client k ∈ St runs ClientUpdate(k, θt−1) in parallel; aggregate θt = Σ (nk / Σ nj) θtk over k ∈ St.

ClientUpdate: for local epoch e = 1…E, for each batch b ⊆ Pk with |b| = B: θ ← AdamW(θ, ∇ℓ(θ; b), η); return θ.

Chunk tail notes a 2-layer MLP projector connector variant: "a deeper, higher-compression connector in which both MLP layers are trained."
