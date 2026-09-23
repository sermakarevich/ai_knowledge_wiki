> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Main Results and Latency: Capabilities Across Smart Turn, Easy Turn, and FastTurn Test Sets

**In one sentence:** Table 3 compares turn-detection accuracy and latency across the Smart Turn, Easy Turn, and FastTurn test sets, showing Smart Turn best only on its own simplified two-class set, FastTurn-Cascaded strong on the clean Easy Turn set, and FastTurn-Unified achieving lower latency than Easy Turn and FastTurn-Cascaded with similar or better accuracy while the English subset still trails Paraformer+Ten Turn.

## Key points

- Table 3 reports results on three test sets — Smart Turn, Easy Turn, and FastTurn — and the Smart Turn model outperforms others only on its own test set, attributed to data and label-category mismatch.
- The Smart Turn test set uses only two categories ("complete" and "incomplete"), which does not fully align with the multi-class model, and its simplified data contributes to its better performance there.
- The Easy Turn test set has 800 samples with no background noise and relies on semantic cues, leading to strong performance from FastTurn-Cascaded, while FastTurn performs slightly worse due to small sample size and sensitivity to variations.
- The FastTurn test set contains more echo signals and acoustic ambiguity, presenting a greater challenge for turn-state modeling.
- Smart Turn's simplified design gives low latency but poorer performance in complex scenarios, while FastTurn-Unified achieves lower latency than both Easy Turn and FastTurn-Cascaded while maintaining similar or better accuracy.
- On the English subset results met expectations but did not surpass Paraformer+Ten Turn[30], with limited optimization and English dialogue data affecting performance.
- FastTurn-Semantic improves turn detection over FastTurn-Cascaded by reducing reliance on transcript quality and adding speech-derived features that compensate for CTC errors in noisy or overlapping speech, and FastTurn-Unified further shows the benefit of combining semantic and acoustic cues.

---

## Cross-test-set results (Table 3)

> "capabilities. Table 3 shows results for the Smart Turn, Easy Turn, and FastTurn test sets."

No numeric Table 3 cell values are present in this chunk; only the qualitative comparisons below are stated.

## Smart Turn test set

> "The Smart Turn model outperforms others on its test set due to mismatches in data and label categories."

> "The test set, with only two categories ("complete" and "incomplete"), does not fully align with our multi-class model, and its simplified data contributes to its better performance."

## Easy Turn test set

> "The Easy Turn test set, with 800 samples and no background noise, relies on semantic cues, leading to strong performance from FastTurn-Cascaded."

> "However, FastTurn performs slightly worse due to a small sample size and sensitivity to variations."

## FastTurn test set

> "The FastTurn test set, with more echo signals and acoustic ambiguity, presents a greater challenge for turn-state modeling."

## Latency

> "In terms of latency, Smart Turn's simplified design results in low latency but poorer performance in complex scenarios."

> "FastTurn-Unified achieves lower latency than both Easy Turn and FastTurn-Cascaded while maintaining similar or better accuracy."

## English subset

> "For the English subset, results met expectations, but did not surpass Paraformer+Ten Turn[30]."

> "Limited optimization and English dialogue data affected the model's performance."

## ASR decoding note in chunk

> "achieves performance close to CTC decoding on most evaluation sets."

> "During training, only the adapter parameters are updated while all other components remain frozen."

> "This constrained setting limits full adaptation to the ASR objective and results in a consistent yet moderate gap compared with CTC decoding."

> "Nevertheless, the aligned representations effectively inject high-level semantic information into the LLM, enabling competitive autoregressive decoding despite restricted parameter updates."

## Ablation study (Section 3.6)

> "As shown in Table 2, FastTurn-Semantic improves turn detection performance over FastTurn-Cascaded by reducing reliance on transcript quality and incorporating speech-derived features, which helps compensate for CTC errors in noisy or overlapping speech conditions."

> "FastTurn-Unified further demonstrates the effectiveness of combining semantic and acoustic cues for real-time turn detection."

**Covers:** Sections 3.4–3.6 (Table 3 capabilities across Smart Turn / Easy Turn / FastTurn test sets, latency comparison, English subset note; ASR decoding adapter note; 3.6 ablation of Semantic vs Cascaded and Unified fusion)
