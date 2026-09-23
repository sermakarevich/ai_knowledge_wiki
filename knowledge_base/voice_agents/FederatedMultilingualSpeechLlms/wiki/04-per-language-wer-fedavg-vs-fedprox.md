> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Per-Language WER: FedAvg vs FedProx (TinyLlama vs EuroLLM)
**In one sentence:** Per-language results show EuroLLM beats TinyLlama on six of eight languages with the largest gains on low-resource languages, and FedProx (µ=0.001) further improves EuroLLM to 0.122 overall with its strongest gain on Dutch, the least-represented language.
## Key points
- FedAvg overall WER: Whisper+TinyLlama 0.142 vs Whisper+EuroLLM 0.133 vs FedProx EuroLLM (µ=0.001) 0.122, against centralized 0.072.
- EuroLLM outperforms TinyLlama under FedAvg on six of eight languages, with the largest absolute gains on Portuguese (−6.5%), Italian (−4.8%), and Polish (−3.3%).
- FedProx EuroLLM (µ=0.001) improves over FedAvg EuroLLM on five of eight languages: Dutch (0.265 → 0.195, −7.0% abs.), Polish, English, French, and Spanish.
- FedProx EuroLLM degrades three languages relative to FedAvg EuroLLM: German (+2.6% abs.), Italian, and Portuguese.
- The FedProx benefit is strongest for the least-represented languages (≤ 4 clients), while moderate-resource languages show mixed results.
- Client distribution is strongly skewed toward English (256 of 316 clients) and overall WER is dominated by high-resource evaluation words.
- Macro-averaged WER (unweighted mean of per-language values): FedAvg TinyLlama 0.170 versus EuroLLM 0.150; the macro gap (−2.0 points) exceeds the word-weighted gap (−0.9 points), confirming the EuroLLM advantage is driven by low-resource languages.
---
## Table 3 — Per-language WER (Cent. / FedAvgWT / FedAvgEL / FPEL)
| Lang. | Cent. | FedAvgWT | FedAvgEL | FPEL |
|---|---|---|---|---|
| Dutch | 0.110 | 0.270 | 0.265 | 0.195 |
| English | 0.049 | 0.100 | 0.098 | 0.090 |
| French | 0.061 | 0.075 | 0.078 | 0.072 |
| German | 0.071 | 0.104 | 0.098 | 0.125 |
| Italian | 0.121 | 0.233 | 0.186 | 0.189 |
| Polish | 0.110 | 0.270 | 0.237 | 0.228 |
| Portuguese | 0.093 | 0.225 | 0.160 | 0.177 |
| Spanish | 0.046 | 0.085 | 0.075 | 0.068 |
| Overall | 0.072 | 0.142 | 0.133 | 0.122 |
## Per-language analysis (Section 4.4)
- "Table 3 compares FedAvg TinyLlama and EuroLLM against the FedProx with µ=0.001 which reaches the lower WER 0.122 between frozen-encoder FL results."
- "EuroLLM also outperforms TinyLlama on six of eight languages; with the largest gains are on most of low-resource languages, see Table 1, where multilingual priors matter most: Portuguese (−6.5% abs.), Italian (−4.8%), Polish (−3.3%)."
- "FedProx EuroLLM improves over FedAvg on five of eight languages: Dutch (0.265 → 0.195, −7.0% abs.), Polish, English, French, and Spanish."
- "Conversely, it degrades German (+2.6% abs.), Italian, and Portuguese."
- "Note that benefit is strongest for the least-represented languages (≤ 4 clients), while moderate-resource languages show mixed results."
## Skew and macro-averaged WER
- "Because the client distribution is strongly skewed toward English (256 of 316 clients) and the overall WER is dominated by high-resource evaluation words, we also report macro-averaged WER (unweighted mean of the per-language values in Table 3): FedAvg Whisper+TinyLlama is 0.170 versus 0.150 for Whisper+EuroLLM."
- "This macro gap (−2.0 points) is larger than the word-weighted gap (−0.9 points), confirming that the EuroLLM advantage is driven particularly by the low-resource languages rather than being masked by them."
## Context from surrounding sections present in chunk
- Frozen-encoder FedAvg: Whisper+TinyLlama WER 0.1415 (96.8% relative degradation from centralized); EuroLLM 0.133 (−6.0% relative); Voxtral 0.144; WavLM 0.56.
- FedProx µ=0.001 improves Whisper+EuroLLM to WER 0.1217 (−8.5% relative), "the best frozen-encoder result", while degrading Whisper+TinyLlama monotonically and Voxtral (frozen 0.144 → 0.149, unfrozen 0.1362 → 0.1468).
- Figure 2 caption in chunk: "WER vs. encoder learning-rate multiplier (relative to LLM LR). Whisper+TinyLlama (blue, E=5) stays flat at its frozen baseline while Whisper+EuroLLM (green, E=10) improves monotonically; dashed: frozen-encoder baselines."
**Covers:** Section 4.4 Per-Language Analysis (Table 3) with surrounding 4.2–4.3 / Conclusion context as present in chunk
