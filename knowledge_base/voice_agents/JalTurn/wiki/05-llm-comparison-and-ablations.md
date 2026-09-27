> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Comparison with LLM-based Methods and Component Ablations
**In one sentence:** On the in-house benchmark JAL-Turn beats LLM-based detectors (92.03% accuracy, 0.925 F1, 38 ms) while ablations show SenseVoice is the primary driver, CPC adds complementary acoustic cues, and cross-attention plus attention pooling improve both accuracy and latency.
## Key points
- JAL-Turn reaches 92.03% accuracy and 0.925 F1 at 38 ms latency on the in-house benchmark, vs 76.91%/0.817/595 ms (Gemini-2.5-Flash), 78.70%/0.782/124 ms (Qwen3-0.6B), and 85.52%/0.874/1205 ms (GPT-5.1) per Table 4.
- Vs Gemini-2.5-Flash and Qwen3-0.6B, JAL-Turn gains 15.1 and 13.3 absolute accuracy points and +0.108/+0.143 F1 while cutting latency from 595 ms and 124 ms to 38 ms.
- Vs GPT-5.1, JAL-Turn raises accuracy 85.52% to 92.03% and F1 0.874 to 0.925, with latency stated as lowered "by more than a factor of five (205 ms → 38 ms)" despite Table 4 listing GPT-5.1 at 1205 ms.
- Dropping the SenseVoice encoder (w/o Sense) collapses accuracy 92.03% to 72.01% and F1 0.925 to 0.698, indicating linguistically enriched representations are the primary driver.
- Dropping the CPC encoder (w/o CPC) reduces accuracy to 84.18% and F1 to 0.839, showing CPC contributes complementary fine-grained acoustic cues and robustness.
- Removing cross-attention (w/o CrossATT) with both encoders retained drops accuracy to 88.59% and F1 to 0.873, confirming explicit acoustic–linguistic interaction beats co-presenting features.
- Removing attention-based temporal pooling (w/o ATTPooling) gives 90.23% accuracy and 0.895 F1 while increasing latency 38 ms to 48 ms, i.e. lightweight attention pooling yields better representations and a better accuracy–latency trade-off than simpler aggregation.
---
## 4.2.3. Comparison with LLM-based Methods
**Covers:** §4.2.3, Table 4 (in-house benchmark)

Table 4 as given in the chunk:

| Model | Acc | F1 | Latency (ms) |
|---|---|---|---|
| Gemini-2.5-Flash | 76.91 | 0.817 | 595 |
| Qwen3-0.6B | 78.70 | 0.782 | 124 |
| GPT-5.1 | 85.52 | 0.874 | 1205 |
| JAL-Turn | 92.03 | 0.925 | 38 |

Verbatim claims from the chunk:
- "JAL-Turn also compares favorably with LLM-based turn-taking detectors on the in-house benchmark."
- "Compared with Gemini-2.5-Flash and Qwen3-0.6B, JAL-Turn improves accuracy by 15.1 and 13.3 absolute points (92.03% vs. 76.91% / 78.70%), respectively, and increases F1 by 0.108 and 0.143, while reducing latency from 595 ms and 124 ms to only 38 ms."
- "Relative to GPT-5.1, JAL-Turn further raises accuracy from 85.52% to 92.03% and F1 from 0.874 to 0.925, and lowers latency by more than a factor of five (205 ms → 38 ms)."
- "These results indicate that JAL-Turn not only matches or surpasses the" [sentence truncated in chunk].
- Note: the chunk states "(205 ms → 38 ms)" for GPT-5.1 while Table 4 in the same chunk lists GPT-5.1 latency as 1205 ms; both values reproduced as printed.

## Ablations: Removing Encoders, Cross-Attention, and Attention Pooling
**Covers:** ablation paragraph block following Table 4 (w/o Sense, w/o CPC, w/o CrossATT, w/o ATTPooling)

- Full model reference in chunk: 92.03% accuracy, 0.925 F1, 38 ms latency.
- w/o Sense (dropping SenseVoice encoder): accuracy 92.03% → 72.01%, F1 0.925 → 0.698; chunk gloss: "linguistically enriched representations are the primary driver of performance."
- w/o CPC (removing CPC encoder): accuracy → 84.18%, F1 → 0.839; chunk gloss: "less catastrophic but still non-trivial" and "CPC contributes complementary fine-grained acoustic cues that further enhance robustness."
- w/o CrossATT (eliminating cross-attention while retaining both encoders): accuracy → 88.59%, F1 → 0.873; chunk gloss: "explicitly modeling interactions between acoustic and linguistic streams is more effective than simply co-presenting their features."
- w/o ATTPooling (removing attention-based temporal pooling): accuracy → 90.23%, F1 → 0.895, latency 38 ms → 48 ms; chunk gloss: "the proposed lightweight attention pooling not only yields more informative utterance-level representations, but also provides a better accuracy–latency trade-off than simpler temporal aggregation schemes."

**Covers:** §4.2.3 + component ablations on the in-house benchmark (chunk file additionally contains overflow text from §4.4–§5 covered by page 06-analysis-and-conclusion.md, not detailed here).
