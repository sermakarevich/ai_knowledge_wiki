> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Speech-LLM architecture: encoder, connector, decoder

**In one sentence:** Figure 1 defines a three-part speech-LLM where encoder E maps speech x to frame-level features, connector C downsamples by factor k, and decoder L generates ŷ from the projected tokens plus a task prompt, instantiated in four Whisper/WavLM × TinyLlama/EuroLLM pairings.

## Key points
- Encoder E maps speech input x to frame-level acoustic features; connector C downsamples those features by factor k; decoder L generates output ŷ from the projected tokens and a task prompt.
- The paper evaluates four encoder–LLM pairings built from two encoders (Whisper, WavLM) and two decoders (TinyLlama, EuroLLM).
- Whisper large-v3-turbo encodes audio into 768-dimensional speech frame representations, projected to 2048-dimensional tokens to align with TinyLlama-1.1B (22 layers).
- Whisper's encoder has 32 layers and, as a pretrained end-to-end multilingual ASR model, already captures robust cross-lingual acoustic features.
- The Whisper + EuroLLM variant keeps the identical Whisper encoder but replaces the decoder with EuroLLM-1.7B-Instruct, a decoder-only model pretrained on multilingual European text corpora.
- The WavLM + TinyLlama variant replaces Whisper with WavLM-Large (1024-dimensional tokens, 24 layers) while keeping TinyLlama as decoder.
- WavLM is a self-supervised learning (SSL) model pretrained on masked speech prediction and, unlike Whisper, has never seen ASR supervision.

---

## Figure 1 pipeline

> "encoder E maps speech x to frame-level features; connector C downsamples by k; decoder L generates ŷ from the projected tokens and task prompt."

- E: speech x → frame-level features.
- C: downsamples by k.
- L: projected tokens + task prompt → ŷ.

**Covers:** Figure 1; §2.1 Encoder–LLM Models (chunk also contains the opening fragment of §3–§3.1 Federated Setup / Aggregation Strategies, transcribed below)

## Encoder–LLM pairings (§2.1)

| Pairing | Encoder | Decoder |
|---|---|---|
| Whisper + TinyLlama | Whisper large-v3-turbo, 768-dim frames, 32 layers | TinyLlama-1.1B, 2048-dim tokens, 22 layers |
| Whisper + EuroLLM | Identical Whisper encoder | EuroLLM-1.7B-Instruct, decoder-only, pretrained on multilingual European text corpora |
| WavLM + TinyLlama | WavLM-Large, 1024-dim tokens, 24 layers | TinyLlama (as above) |
| (fourth pairing) | — | — |

Notes from the chunk:
- "The combination of foundational acoustic encoders and pretrained LLMs has become a prominent recipe for multilingual end-to-end speech recognition [3]."
- "Whisper is a pretrained end-to-end multilingual ASR model, and its encoder (32 layers) already captures robust cross-lingual acoustic features."
- "WavLM is a self-supervised learning (SSL) model pretrained on masked speech prediction."
- "Unlike Whisper it has never seen ASR supervision, making it…" (sentence truncated in chunk).
- The chunk names "four encoder–LLM pairings" but its visible body details only three (Whisper + TinyLlama, Whisper + EuroLLM, WavLM + TinyLlama); the fourth pairing's description is not present in the chunk and is not invented here.

## Federated setup fragment present in this chunk (§3–§3.1)

- Synchronous client-server optimization where participating clients (C = 0.3) perform E = 10 local AdamW epochs before server aggregation via FedAvg or FedProx.
- "We compute the loss gradient over all data held by these clients, C ∗ K = 94 clients for the global server; see Algorithm 1."
- FedAvg: "Standard weighted averaging of client updates [6]" per round: θ(t+1) = Σ_{k∈St} (n_k / Σ_{j∈St} n_j) θ(t,k), where n_k are training samples on client k and S_t is the random fraction of clients sampled every round.
- FedProx: "Regularises the client loss… with the proximal term µ to limit client drift [15], due to data heterogeneity," per round: min_θ L_local(θ) + (µ/2)||θ − θ(t)||².

**Covers:** Figure 1; §2.1 Encoder–LLM Models (§3–§3.1 fragment as extracted in chunk)
