---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection

### Q1. In full-duplex spoken dialogue, what decision must the agent make mid-utterance, and what role does turn detection play as an interface?

> [!tip]- Answer
> The agent must decide when to speak, yield, or interrupt while the user is still talking, rather than waiting for a clean turn boundary. In practical deployments, existing full-duplex systems rely on turn detection as the controllable interface between speech processing and response generation. See [[wiki/01-overview-and-problem|FastTurn: Unifying Acoustic and Streaming Semantic]].

### Q2. What are the two broad groups of existing turn-detection approaches named in the introduction fragment, and what limitation is stated for the VAD-based group?

> [!tip]- Answer
> The chunk names VAD-based methods and an ASR-based alternative, though the ASR description is cut off before its properties are stated. VAD-based methods infer interruption timing from acoustic energy or activity patterns and are described as lightweight and fast, but they primarily capture speech presence and lack semantic understanding. See [[wiki/01-overview-and-problem|FastTurn: Unifying Acoustic and Streaming Semantic]].

### Q3. How does FastTurn-Cascaded produce a low-latency turn decision, and why is it fragile under overlap and noise?

> [!tip]- Answer
> FastTurn-Cascaded uses a CTC branch with greedy decoding for streaming transcription, formats the transcript as a CTC prompt, and feeds it into the LLM (Qwen3-0.6B) for turn prediction with minimal decoding overhead. Because the LLM input is dominated by that CTC transcript, predictions are sensitive to CTC errors, especially under speech overlap and noise. See [[wiki/02-architecture-variants|FastTurn Architecture Variants: Cascaded, Semantic, Unified]].

### Q4. How do FastTurn-Semantic and FastTurn-Unified each reduce transcript dependence, and what training trick prevents overfitting to the CTC prompt?

> [!tip]- Answer
> FastTurn-Semantic projects Conformer encoder acoustic representations plus the CTC prompt into the LLM input space via an LLM adapter, so the LLM reasons over both and mitigates CTC errors while keeping early textual conditioning. FastTurn-Unified goes further by fusing intermediate Conformer states processed through an acoustic adapter with the LLM hidden states into a 3-layer MLP turn detector. Joint training applies prompt dropout (p < 0.5), randomly dropping the CTC prompt to prevent overfitting to the CTC branch. See [[wiki/02-architecture-variants|FastTurn Architecture Variants: Cascaded, Semantic, Unified]].

### Q5. What data grounds FastTurn's ASR pretraining and its turn-detection training, and how are synthetic complete/incomplete states created?

> [!tip]- Answer
> ASR training uses AISHELL-1, AISHELL-2, WenetSpeech, LibriSpeech, GigaSpeech, and MLS, totaling over 30,000 hours of Chinese and English speech. Turn-detection training uses the Easy Turn set augmented with internal conversational data plus synthetic corpora whose texts come from Qwen3-32B and DeepSeek-V3 and whose audio comes from IndexTTS2. Complete/incomplete synthetic states are made by forced alignment for word-level timestamps plus truncation of complete turns at random positions, with filtering to ensure linguistic incompleteness. See [[wiki/03-training-and-test-set|Training and Test Set: ASR Data, Turn-Detection Data, Setup, Metrics]].

### Q6. What is the composition of the FastTurn test set and which three metrics score turn-state prediction?

> [!tip]- Answer
> The test set combines real-world segments — Complete (14,709 samples / 9.64 h), Incomplete (3,643 / 2.15 h), Backchannel (3,080 / 0.42 h) — with 1,000 synthesized Wait samples (0.71 h) whose text comes from DeepSeek V3 and audio from IndexTTS2, since Wait is rare in natural conversation. Scoring uses Accuracy = (TP+TN)/(TP+TN+FP+FN), Miss Rate = FN/(TP+FN), and False Alarm Rate = FP/(FP+TN). Semantic-only models do poorly on Complete/Incomplete while FastTurn-Unified is best across all categories. See [[wiki/03-training-and-test-set|Training and Test Set: ASR Data, Turn-Detection Data, Setup, Metrics]].

### Q7. Across the Smart Turn, Easy Turn, and FastTurn test sets, how do accuracy and latency compare, and what explains each set's pattern?

> [!tip]- Answer
> The Smart Turn model wins only on its own simplified two-class (complete/incomplete) set due to data and label mismatch, with low latency but poor complex-scenario performance. The clean 800-sample Easy Turn set with no background noise favors semantic cues, so FastTurn-Cascaded is strong there, while the FastTurn set with echo signals and acoustic ambiguity is hardest. FastTurn-Unified achieves lower latency than both Easy Turn and FastTurn-Cascaded while holding similar or better accuracy, though its English subset still trails Paraformer+Ten Turn for lack of optimization and English dialogue data. See [[wiki/04-main-results-and-latency|Main Results and Latency: Capabilities Across Smart Turn, Easy Turn, and FastTurn Test Sets]].

### Q8. In the Table 4 ASR ablation, how does CTC greedy decoding compare with the LLM-decoding adapter variants, and what does the paper conclude about FastTurn?

> [!tip]- Answer
> CTC greedy decoding is best in the table at 7.06% WER on LibriClean, 9.52% on TestNet, and 2.33% CER on AISHELL-1, while LLM decoding with a 2-layer MLP adapter is worst (14.09% / 16.80% / 6.45%). Swapping to a 2-layer Transformer adapter improves LLM decoding markedly, and a 4-layer Transformer adapter further improves LibriClean to 5.56% and AISHELL-1 to 3.69% with TestNet unchanged at 10.74%. The conclusion attributes FastTurn's low latency to fast CTC decoding and its robustness to integrated acoustic features, alongside a released test set capturing echo and overlap dynamics. See [[wiki/05-asr-ablation-and-conclusion|ASR Results and Conclusion]].

### Q9. For a production full-duplex voice agent deployed in noisy, overlapping speech with echo, which FastTurn variant would you recommend and what is the strongest reason to hesitate?

> [!tip]- Answer
> Recommend FastTurn-Unified, since it alone fuses streaming acoustic cues with LLM-conditioned semantics, achieves the best accuracy across Complete/Incomplete/Backchannel/Wait, and still undercuts Easy Turn and Cascaded on latency. Hesitate because its cross-set edge is uneven — the English subset still trails Paraformer+Ten Turn and the hardest echo/overlap conditions remain the least forgiving — so validate on your own noisy echo-heavy traffic and weigh the extra adapter-plus-detector complexity before committing. See [[wiki/05-asr-ablation-and-conclusion|ASR Results and Conclusion]].
