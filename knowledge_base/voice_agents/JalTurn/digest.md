> [[index|Wiki]] | [[summary|Summary]]

# JAL-Turn: Joint Acoustic-Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialog — Digest

## 1. [[wiki/01-overview-and-problem|JAL-Turn: Joint Acoustic–Linguistic Modeling for Real-Time — Overview and Problem]]

**In one sentence:** This chunk is truncated and contains only the paper's title block, author list, and the opening fragment of the abstract, so no substantive claim of the paper can be documented from it.

- The chunk gives the full paper title as "JAL-Turn: Joint Acoustic–Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialogue Systems".
- The chunk lists the authors as Guangzhao Yang, Yu Pan, Shi Qiu, and Ningjie Bai, with affiliation Recho Inc, Japan.
- The chunk's abstract fragment states that "efficient and robust turn-taking detection remains a significant challenge in industrial-grade Voice" systems.
- The chunk's abstract fragment states that accurately determining whether a user has "genuinely finished their speaking turn" matters for interaction quality, user experience, and trust.
- The abstract text cuts off mid-sentence at "while still maintaining", so no complete argument, method, number, or result is present in this chunk.
- No tables, exact numbers, mechanisms, or verbatim citable quotes beyond the fragments above can be extracted from this chunk.

## 2. [[wiki/02-background-and-data-pipeline|Background and scalable data pipeline]]

**In one sentence:** JAL-Turn is motivated by the failure of silence-based heuristics, simple acoustic/linguistic models, and costly LLM/SLM full-duplex systems to deliver real-time robust turn-taking, and it addresses training-data scarcity with an automatic VAD future-window labeling and context/dataset construction pipeline.

- Traditional silence-based turn-taking waits for a fixed or adaptive silence duration, but silence alone is unreliable because users produce within-utterance pauses, hesitations, thinking pauses, and self-repairs that do not signal handover.
- Turn transitions in many languages are rapid, often 100–500 ms, so listeners must proactively anticipate completions using lexical, prosodic, and multimodal cues rather than merely reacting to silence.
- Prior data-driven acoustic- or linguistic-feature models use relatively simple architectures under real-time constraints, limiting fine-grained cue capture and leaving room for improvement in accuracy and robustness.
- LLM/SLM full-duplex integrations improve quality but need large manually annotated dialogue data, add ASR/latency overhead, prioritize semantics while discarding fine-grained acoustic cues, and degrade in complex real-world scenarios.
- The pipeline extracts frame-level stereo VAD at 50 Hz as binary sequences per channel and labels each frame with a weighted 2-second future-window VAD score, keeping a label only when linear, square-root, and exponential weighting schemes all agree.
- Training samples are anchored at each VAD falling edge after a speech segment, with context extended backward to the previous long silence (≥ 2 seconds) and normalized to a fixed 10-second window via left-padding or truncation.
- Applying the pipeline to 1,128 hours of in-house stereo conversational data yields ~2,299 hours of trainable segments at ~85% labeling accuracy (manual inspection), plus a 95-hour single-utterance set yielding 749 hours where all frames except the final one are Hold (~100% accurate but lacking conversational variability), and the model trains on a mixture of both.

## 3. [[wiki/03-architecture-dual-encoder-and-fusion|Architecture: dual encoders, fusion, and classifier]]

**In one sentence:** JAL-Turn jointly models turn-taking with a frozen SenseVoice encoder for high-level semantic/linguistic cues and a frozen CPC encoder for low-level acoustic regularities, fused via cross-attention and processed by an ALiBi Transformer, temporal pooling, and a sigmoid classification head.

- Dual-path encoders produce frame-level features `hl = EncoderSense(x)` with `d1 = 512` and `ha = EncoderCPC(x)` with `d2 = 256` from waveform `x ∈ R1×L`, then map them via linear projections into a shared latent space.
- Both CPC and SenseVoice encoders are kept frozen during training to preserve pre-trained knowledge; SenseVoice emphasizes high-level semantic/linguistic elements while CPC emphasizes low-level acoustic regularities via self-supervised contrastive learning.
- The SenseVoice encoder is shared between ASR and JAL-Turn, so turn-taking predictions are computed synchronously with ASR in parallel from a single forward pass of the shared encoder with no extra stages before or after ASR decoding.
- Fusion uses `L = 2` stacked cross-attention layers where SenseVoice features act as queries and CPC features serve as keys/values, with `Q = LayerNorm(h′l)`, `K/V = LayerNorm(h′a)`, model dimension `d = 256`, and `H = 4` heads plus residual connections and position-wise FFN.
- On top of the fused representation sits a causal self-attention Transformer using Attention with Linear Biases (ALiBi), which adds a distance-dependent bias to attention logits, aids length extrapolation, and encodes a recency bias suited to local turn-taking patterns.
- An attention-based temporal pooling layer computes `αt = softmax(w⊤ht + b)` and `hpool = Σt αt · ht` to focus on the most informative segments before a linear head outputs shift logit `ŷ` with sigmoid activation and a fixed `τ = 0.5` hold-vs-shift threshold trained with binary cross-entropy (`1` = shift, `0` = hold).

## 4. [[wiki/04-experiments-slm-and-audio-baselines|Experiments: setups and comparison with SLM-based systems]]

**In one sentence:** On Mandarin Easy-Turn JAL-Turn matches or slightly beats the SLM-based EasyTurn on complete turns (96.67% vs 96.33%) at 12 ms versus 263 ms latency, while trailing on backchannels (80% vs 91%), giving a substantially more favorable quality–latency trade-off overall.

- Evaluation uses Mandarin Easy-Turn (~1145 hours), multilingual STurn-v3 (~700 hours, 23 languages), and a large-scale in-house corpus of real-world Japanese dialogues, with 9:1 train/validation splits and original test sets for Easy-Turn/STurn-v3 plus 500 human-labeled real-world business samples for the in-house test.
- Training is end-to-end on a single H100 GPU for 10 epochs in PyTorch with AdamW (lr 1×10−4, weight decay 0.001, batch 64) and cosine annealing to 1×10−6; metrics are accuracy, F1-score, and latency for full-duplex responsiveness.
- On Easy-Turn Table 1, states are complete (cp), incomplete (incp), backchannel (bc), and wait, where JAL-Turn scores 96.67% / 93.67% / 80% / 92% at 12 ms latency.
- JAL-Turn achieves the best cp accuracy (96.67%) at 12 ms, markedly exceeds Paraformer+TEN Turn Detection (86.67% cp, 89.3% incp, 91% wait, 204 ms) and STurn-v2 (78.67% cp, 62% incp, 27 ms), reducing latency from 204 ms / 27 ms to 12 ms.
- Against SLM-based EasyTurn (96.33% cp, 97.67% incp, 91% bc, 98% wait, 263 ms), JAL-Turn is within 4.0 points on incp and 6.0 points on wait, slightly improves cp (96.67% vs 96.33%), but underperforms on bc (80% vs 91%).
- The chunk conjectures the bc gap stems from the intrinsically context-dependent nature of backchannels — often short, semantically light responses whose role is better determined with explicit lexical/semantic cues.
- Despite the bc gap, the chunk concludes JAL-Turn offers a substantially more favorable quality–latency trade-off with competitive state-wise accuracy under strict real-time constraints.

## 5. [[wiki/05-llm-comparison-and-ablations|Comparison with LLM-based Methods and Component Ablations]]

**In one sentence:** On the in-house benchmark JAL-Turn beats LLM-based detectors (92.03% accuracy, 0.925 F1, 38 ms) while ablations show SenseVoice is the primary driver, CPC adds complementary acoustic cues, and cross-attention plus attention pooling improve both accuracy and latency.

- JAL-Turn reaches 92.03% accuracy and 0.925 F1 at 38 ms latency on the in-house benchmark, vs 76.91%/0.817/595 ms (Gemini-2.5-Flash), 78.70%/0.782/124 ms (Qwen3-0.6B), and 85.52%/0.874/1205 ms (GPT-5.1) per Table 4.
- Vs Gemini-2.5-Flash and Qwen3-0.6B, JAL-Turn gains 15.1 and 13.3 absolute accuracy points and +0.108/+0.143 F1 while cutting latency from 595 ms and 124 ms to 38 ms.
- Vs GPT-5.1, JAL-Turn raises accuracy 85.52% to 92.03% and F1 0.874 to 0.925, with latency stated as lowered "by more than a factor of five (205 ms → 38 ms)" despite Table 4 listing GPT-5.1 at 1205 ms.
- Dropping the SenseVoice encoder (w/o Sense) collapses accuracy 92.03% to 72.01% and F1 0.925 to 0.698, indicating linguistically enriched representations are the primary driver.
- Dropping the CPC encoder (w/o CPC) reduces accuracy to 84.18% and F1 to 0.839, showing CPC contributes complementary fine-grained acoustic cues and robustness.
- Removing cross-attention (w/o CrossATT) with both encoders retained drops accuracy to 88.59% and F1 to 0.873, confirming explicit acoustic–linguistic interaction beats co-presenting features.
- Removing attention-based temporal pooling (w/o ATTPooling) gives 90.23% accuracy and 0.895 F1 while increasing latency 38 ms to 48 ms, i.e. lightweight attention pooling yields better representations and a better accuracy–latency trade-off than simpler aggregation.

## 6. [[wiki/06-analysis-and-conclusion|Automatic Extraction of Reliable Turn-Taking Labels — Analysis and Conclusion]]

**In one sentence:** This chunk fragment is largely the reference list, preserving only an abstract tail claiming automatic extraction of reliable turn-taking labels from large-scale real-world corpora with strong multilingual and in-house results at real-time performance.

- The chunk's only substantive claim is "automatic extraction of reliable turn-taking labels from large-scale real-world corpora."
- It states experiments were run on "multilingual public benchmarks and an in-house Japanese customer-service dataset."
- It claims "JAL-Turn consistently outperforms strong baselines in both accuracy and robustness."
- It claims the model maintains "real-time performance" alongside those accuracy and robustness gains.
- Beyond that abstract tail, the chunk contains no methods, numbers, tables, or analysis — only reference entries [1]–[25].
- The references span turn-taking reviews, VAP/multilingual VAP, LLM/SLM dialogue systems (Qwen, GPT-4, Llama-Omni, Moshi, Salmonn-Omni, OmniFlatten, EasyTurn, FunAudioLLM), and speech encoders (Whisper transfer, Conformer, Hybridformer, Paraformer, wav2vec-style pretraining).

## The argument in five moves

1. Real-time robust turn-taking cannot rely on silence waits or simple acoustic/linguistic models, and LLM/SLM full-duplex alternatives cost too much in annotation, latency, and lost acoustic detail.
2. Training data is therefore generated automatically by scoring 50 Hz stereo VAD over a 2-second future window with three weighting schemes that must agree, anchoring samples at VAD falling edges with 10-second backward context to a ≥ 2-second silence.
3. JAL-Turn jointly encodes each window with a frozen SenseVoice path for linguistic/semantic cues and a frozen CPC path for fine-grained acoustic cues, sharing SenseVoice with ASR for parallel low-latency inference.
4. The two streams are fused with two cross-attention layers (linguistic queries over acoustic keys/values), refined by an ALiBi causal Transformer with recency bias, pooled by learned temporal attention, and classified by a sigmoid head at threshold 0.5.
5. On Mandarin Easy-Turn this yields best complete-turn accuracy (96.67%) at 12 ms versus 263 ms for the SLM EasyTurn, with only the context-dependent backchannel state lagging (80% vs 91%).
6. On the in-house Japanese benchmark it beats LLM detectors (92.03%/0.925/38 ms vs 76.91–85.52%) and ablations confirm SenseVoice as primary driver, CPC as complementary acoustic robustness, and cross-attention plus attention pooling as accuracy- and latency-positive — supporting the closing claim of automatic scalable labels with consistently stronger accuracy and robustness at real-time performance.
